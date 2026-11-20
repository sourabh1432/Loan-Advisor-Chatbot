from pathlib import Path

import joblib

from src.entity_extraction import extract_entities
from src.emi_calculator import calculate_emi
from src.input_validation import (
    validate_applicant,
    prepare_model_input,
    validate_field,
)

# Load the loan approval model and its expected feature list
PROJECT_ROOT = Path(__file__).resolve().parent.parent
MODEL_DIR = PROJECT_ROOT / "models"

loan_approval_model = joblib.load(
    MODEL_DIR / "loan_approval_rf.pkl"
)

loan_approval_features = joblib.load(
    MODEL_DIR / "loan_approval_features.pkl"
)

# Load intent classification model and TF-IDF vectorizer
intent_model = joblib.load(
    MODEL_DIR / "intent_classifier.pkl"
)

intent_tfidf = joblib.load(
    MODEL_DIR / "intent_tfidf.pkl"
)

class LoanConversationManager:

    def __init__(self):
        self.applicant = {
            "no_of_dependents": None,
            "education": None,
            "self_employed": None,
            "income_annum": None,
            "loan_amount": None,
            "loan_term": None,
            "cibil_score": None,
            "residential_assets_value": None,
            "commercial_assets_value": None,
            "luxury_assets_value": None,
            "bank_asset_value": None,
            "interest_rate": None,
        }

        self.pending_field = None
        self.awaiting_correction_value = False
        self.awaiting_confirmation = False
        self.awaiting_correction = False
        self.awaiting_reset_confirmation = False
        self.last_prediction = None
        self.last_validation_error = None
        self.intent_model = intent_model
        self.intent_tfidf = intent_tfidf
        self.emi_pending_field = None
        self.last_topic = None
        # Workflow switching state
        self.awaiting_workflow_switch = False
        self.pending_workflow = None

        # Store paused workflows
        self.paused_application_state = None
        self.paused_emi_state = None

        self.emi_details = {
            "loan_amount": None,
            "interest_rate": None,
            "loan_tenure": None
        }

    # --------------------------------------------------
    # 1. Identify missing fields
    # --------------------------------------------------

    def get_missing_fields(self):
        return [
            field
            for field, value in self.applicant.items()
            if value is None
        ]

    # --------------------------------------------------
    # 2. Questions for missing fields
    # --------------------------------------------------

    def get_question(self, field):
        questions = {
            "no_of_dependents":
                "How many dependents do you have?",

            "education":
                "Are you Graduate or Not Graduate?",

            "self_employed":
                "Are you self-employed? Please answer Yes or No.",

            "income_annum":
                "What is your annual income in rupees?",

            "loan_amount":
                "What loan amount do you need in rupees?",

            "loan_term":
                "What is your loan tenure in years?",

            "cibil_score":
                "What is your CIBIL score?",

            "residential_assets_value":
                "What is the value of your residential assets in rupees?",

            "commercial_assets_value":
                "What is the value of your commercial assets in rupees?",

            "luxury_assets_value":
                "What is the value of your luxury assets in rupees?",

            "bank_asset_value":
                "What is the value of your bank assets in rupees?",

            "interest_rate":
                "What annual interest rate should I use for your EMI "
                "estimate? Enter a percentage, for example 10.",
        }

        return questions[field]

    # --------------------------------------------------
    # 3. Validate and save answers
    # --------------------------------------------------

    def save_answer(self, field, message):
        """Validate and save an answer to the requested field."""

        answer = message.strip().lower()
        value = None

        # Education
        if field == "education":
            if answer in ("graduate", "graduated"):
                value = "Graduate"

            elif answer in (
                "not graduate",
                "non graduate",
                "non-graduate",
                "not a graduate",
                "undergraduate",
            ):
                value = "Not Graduate"

        # Self-employed
        elif field == "self_employed":
            if answer in ("yes", "y", "true"):
                value = "Yes"

            elif answer in ("no", "n", "false"):
                value = "No"

        # Number of dependents
        elif field == "no_of_dependents":

            number_words = {
                "zero": 0,
                "one": 1,
                "two": 2,
                "three": 3,
                "four": 4,
                "five": 5,
                "six": 6,
                "seven": 7,
                "eight": 8,
                "nine": 9,
                "ten": 10
            }

            if answer in number_words:
                value = number_words[answer]

            else:
                try:
                    number = float(answer)

                    if number >= 0 and number.is_integer():
                        value = int(number)

                except ValueError:
                    value = None

        # CIBIL score
        elif field == "cibil_score":
            try:
                number = float(answer)

                if number.is_integer():
                    value = int(number)

            except ValueError:
                value = None

        # Annual income, loan amount and assets
        elif field in (
            "income_annum",
            "loan_amount",
            "residential_assets_value",
            "commercial_assets_value",
            "luxury_assets_value",
            "bank_asset_value",
        ):
            if answer in ("no", "none", "zero", "nil", "₹0", "0"):
                value = 0.0

            else:
                cleaned = (
                    answer.replace(",", "")
                    .replace("₹", "")
                    .replace("rs.", "")
                    .replace("rs", "")
                    .strip()
                )

                try:
                    number = float(cleaned)

                    if number >= 0:
                        value = number

                except ValueError:
                    value = None

        # Loan tenure in years
        elif field == "loan_term":
            cleaned = (
                answer.replace("years", "")
                .replace("year", "")
                .replace("yrs", "")
                .replace("yr", "")
                .strip()
            )

            try:
                number = float(cleaned)

                if 0 < number <= 40:
                    value = number

            except ValueError:
                value = None

        # Annual interest rate for EMI calculation
        elif field == "interest_rate":
            cleaned = (
                answer.replace("%", "")
                .replace(",", "")
                .strip()
            )

            try:
                value = float(cleaned)

            except ValueError:
                value = None

        # Centralized validation
       # Centralized validation
        if value is None:
            self.last_validation_error = (
                f"Please enter a valid value for {field.replace('_', ' ')}."
            )
            return False

        is_valid, validation_message = validate_field(field, value)

        if not is_valid:
            self.last_validation_error = validation_message
            return False

        self.applicant[field] = value
        self.pending_field = None
        self.last_validation_error = None

        return True
    # --------------------------------------------------
    # 4. Extract details from the user's message
    # --------------------------------------------------

    
    def update_from_entities(self, entities):

        updated_fields = {}
        validation_errors = {}

        # Convert extracted income into annual income
        income = entities.get("income")
        income_frequency = entities.get("income_frequency")

        if income is not None:
             if income < 0:
                validation_errors["income_annum"] = (
                    "Income cannot be negative. Please enter a valid income."
                )
             else:
                if income_frequency == "monthly":
                    annual_income = income * 12
                else:
                    annual_income = income

                is_valid, message = validate_field(
                    "income_annum", annual_income
                )

                if is_valid:
                    self.applicant["income_annum"] = annual_income
                    updated_fields["income_annum"] = annual_income
                else:
                    validation_errors["income_annum"] = message

        # Map extracted entities to applicant fields
        field_mapping = {
            "credit_score": "cibil_score",
            "dependents": "no_of_dependents",
            "loan_amount": "loan_amount",
        }

        for extracted_field, applicant_field in field_mapping.items():

            value = entities.get(extracted_field)

            if value is None:
                continue

            is_valid, message = validate_field(applicant_field, value)

            if is_valid:
                self.applicant[applicant_field] = value
                updated_fields[applicant_field] = value
            else:
                validation_errors[applicant_field] = message

        # Map extracted tenure to loan_term
        tenure = entities.get("tenure")

        if tenure is not None:
            tenure_value = tenure.get("value")
            tenure_unit = tenure.get("unit")

            if tenure_unit == "months":
                loan_term = tenure_value / 12
            else:
                loan_term = tenure_value

            is_valid, message = validate_field("loan_term", loan_term)

            if is_valid:
                self.applicant["loan_term"] = loan_term
                updated_fields["loan_term"] = loan_term
            else:
                validation_errors["loan_term"] = message

        # Map interest rate
        interest_rate = entities.get("interest_rate")

        if interest_rate is not None:
            rate_value = interest_rate.get("value")

            is_valid, message = validate_field(
                "interest_rate", rate_value
            )

            if is_valid:
                self.applicant["interest_rate"] = rate_value
                updated_fields["interest_rate"] = rate_value
            else:
                validation_errors["interest_rate"] = message

        return updated_fields, validation_errors

   
    



    # --------------------------------------------------
    # 5. Predict loan approval
    # --------------------------------------------------

    def predict_loan_approval(self):
        """Validate model fields and predict using the existing model."""

        # The validation function checks model-related applicant fields.
        # Interest rate is deliberately excluded from the model input.
        errors = validate_applicant(self.applicant)

        if errors:
            return {
                "success": False,
                "message": "Please correct these details:\n- "
                + "\n- ".join(errors),
            }

        try:
            applicant_df = prepare_model_input(
                self.applicant,
                loan_approval_features,
            )

            prediction = loan_approval_model.predict(
                applicant_df
            )[0]

            probabilities = loan_approval_model.predict_proba(
                applicant_df
            )[0]

            class_names = loan_approval_model.classes_

            probability_by_class = {
                str(name): round(float(prob) * 100, 2)
                for name, prob in zip(
                    class_names, probabilities
                )
            }

            return {
                "success": True,
                "prediction": str(prediction),
                "probabilities": probability_by_class,
            }

        except (ValueError, KeyError, TypeError) as error:
            return {
                "success": False,
                "message": f"Could not predict: {error}",
            }

    # --------------------------------------------------
    # 6. Display applicant summary and estimated EMI
    # --------------------------------------------------

    def show_applicant_summary(self):
        labels = {
            "no_of_dependents": "Number of dependents",
            "education": "Education",
            "self_employed": "Self-employed",
            "income_annum": "Annual income",
            "loan_amount": "Loan amount",
            "loan_term": "Loan tenure (years)",
            "cibil_score": "CIBIL score",
            "residential_assets_value": "Residential assets",
            "commercial_assets_value": "Commercial assets",
            "luxury_assets_value": "Luxury assets",
            "bank_asset_value": "Bank assets",
            "interest_rate": "Annual interest rate (%)",
        }

        print("\n" + "=" * 45)
        print("       APPLICANT DETAILS SUMMARY")
        print("=" * 45)

        currency_fields = {
            "income_annum",
            "loan_amount",
            "residential_assets_value",
            "commercial_assets_value",
            "luxury_assets_value",
            "bank_asset_value",
        }

        for field, label in labels.items():
            value = self.applicant.get(field)

            if field in currency_fields and value is not None:
                print(f"{label}: ₹{value:,.2f}")

            elif field == "interest_rate" and value is not None:
                print(f"{label}: {value:.2f}%")

            else:
                print(f"{label}: {value}")

        # EMI is a separate estimate, not an ML prediction.
        try:
            emi_result = calculate_emi(
                loan_amount=self.applicant["loan_amount"],
                annual_interest_rate=self.applicant["interest_rate"],
                tenure_years=self.applicant["loan_term"],
            )

            print("\n--- EMI ESTIMATE ---")
            print(
                f"Monthly EMI: "
                f"₹{emi_result['monthly_emi']:,.2f}"
            )
            print(
                f"Total interest: "
                f"₹{emi_result['total_interest']:,.2f}"
            )
            print(
                f"Total repayment: "
                f"₹{emi_result['total_payment']:,.2f}"
            )
            print(
                f"Repayment period: "
                f"{emi_result['total_months']} months"
            )
            print(
                "Note: This estimate uses the interest rate you entered. "
                "It is not a bank offer."
            )

        except (ValueError, TypeError, KeyError) as error:
            print(f"\nEMI estimate unavailable: {error}")

        print("=" * 45)

    # --------------------------------------------------
    # 7. Reset conversation
    # --------------------------------------------------

    def reset_conversation(self):
        """Clear the current application and begin again."""

        self.applicant = {
            "no_of_dependents": None,
            "education": None,
            "self_employed": None,
            "income_annum": None,
            "loan_amount": None,
            "loan_term": None,
            "cibil_score": None,
            "residential_assets_value": None,
            "commercial_assets_value": None,
            "luxury_assets_value": None,
            "bank_asset_value": None,
            "interest_rate": None,
        }

        self.pending_field = None
        self.awaiting_confirmation = False
        self.awaiting_correction = False
        self.awaiting_reset_confirmation = False
        self.last_prediction = None
        self.awaiting_correction_value = False
        self.last_validation_error = None
        self.last_topic = None
        self.emi_pending_field = None
        self.awaiting_workflow_switch = False
        self.pending_workflow = None
        self.paused_application_state = None
        self.paused_emi_state = None

        self.emi_details = {
            "loan_amount": None,
            "interest_rate": None,
            "loan_tenure": None
        }
        return (
            "Your previous conversation has been cleared successfully.\n"
            "You can now start a new loan application, "
            "calculate EMI, or ask a loan-related question."
        )
        
        
    def start_emi_calculation(self):

        self.emi_details = {
            "loan_amount": None,
            "interest_rate": None,
            "loan_tenure": None
        }

        self.emi_pending_field = "loan_amount"

        return (
            "Let's calculate your loan EMI.\n"
            "What is your loan amount in rupees?"
        )
        
    def handle_emi_input(self, message):

        field = self.emi_pending_field

        # Convert user input into a number
        try:
            value = float(
                message.lower()
                .replace("₹", "")
                .replace(",", "")
                .replace("rs.", "")
                .replace("rs", "")
                .strip()
            )

        except ValueError:
            return "Please enter a valid numerical value."

        # Validate loan amount
        if field == "loan_amount":

            if value <= 0:
                return "Loan amount must be greater than zero."

            self.emi_details["loan_amount"] = value

            self.emi_pending_field = "interest_rate"

            return (
                "What is the annual interest rate in percentage?\n"
                "For example, enter 10 for 10%."
            )

        # Validate interest rate
        elif field == "interest_rate":

            if value < 0 or value > 100:
                return "Interest rate must be between 0 and 100."

            self.emi_details["interest_rate"] = value

            self.emi_pending_field = "loan_tenure"

            return (
                "What is your loan tenure in years?\n"
                "For example, enter 5 for 5 years."
            )

        # Validate loan tenure
        elif field == "loan_tenure":

            if value <= 0 or value > 40:
                return "Loan tenure must be greater than 0 and not more than 40 years."

            self.emi_details["loan_tenure"] = value

            # Get EMI inputs
            principal = self.emi_details["loan_amount"]
            annual_rate = self.emi_details["interest_rate"]
            years = self.emi_details["loan_tenure"]

            months = round(years * 12)

            monthly_rate = annual_rate / (12 * 100)

            # Calculate EMI
            if monthly_rate == 0:

                emi = principal / months

            else:

                emi = (
                    principal
                    * monthly_rate
                    * (1 + monthly_rate) ** months
                ) / (
                    (1 + monthly_rate) ** months - 1
                )

            total_payment = emi * months

            total_interest = total_payment - principal

            # Reset EMI conversation state
            self.emi_pending_field = None

            self.emi_details = {
                "loan_amount": None,
                "interest_rate": None,
                "loan_tenure": None
            }

            # Display results
            return (
                    "**🏦 EMI CALCULATION RESULT**\n\n"
                    "**Loan Details**\n"
                    f"Loan Amount: ₹{principal:,.2f}\n\n"
                    f"Interest Rate: {annual_rate:.2f}%\n\n"
                    f"Loan Tenure: {years:g} years\n\n"
                    f"Repayment Period: {months} months\n\n"
                    "---\n\n"
                    "**💰 REPAYMENT SUMMARY**\n\n"
                    f"**Monthly EMI: ₹{emi:,.2f}**\n\n"
                    f"Total Interest: ₹{total_interest:,.2f}\n\n"
                    f"Total Repayment: ₹{total_payment:,.2f}\n\n"
                    "---\n\n"
                    "ℹ️ *This is an estimated EMI, not a bank offer.*"
                )

        return "Something went wrong with EMI calculation."

    # --------------------------------------------------
    # 8. Process conversation
    # --------------------------------------------------
    
    def process_message(self, message):
        """Process messages and manage the application conversation."""

        message = message.strip()

        if not message:
            return "Please enter a message."

        answer = message.lower().strip()

        # Exit
        if answer in ("exit", "quit", "bye"):
            return "Thank you for using Loan Advisor Chatbot!"

        # Restart request
        if answer in ("restart", "reset", "start over", "new application"):
            self.awaiting_reset_confirmation = True

            return (
                "Starting a new application will clear the current details. "
                "Are you sure? Enter Yes to restart or No to continue."
            )

        # Reset confirmation
        if self.awaiting_reset_confirmation:

            if answer in ("yes", "y"):
                return self.reset_conversation()

            if answer in ("no", "n"):
                self.awaiting_reset_confirmation = False
                return "Reset cancelled. Your current application is unchanged."

            return "Please answer Yes or No."
        
        #  # Handle general loan questions
        # general_response = self.handle_general_loan_query(message)

        # if general_response is not None:
        #     return general_response

        # -----------------------------------------
        # STAGE 5.3: WORKFLOW SWITCHING
        # -----------------------------------------

        detected_intent = self.detect_intent(message)

        # Identify a request to start a loan application
        application_request = (
            any(phrase in answer for phrase in [
                "i need",
                "i want",
                "apply for",
                "apply loan",
                "loan application",
                "start application"
            ])
            and "loan" in answer
        )

        # Handle user's confirmation to switch workflows
        if self.awaiting_workflow_switch:

            if answer in ("yes", "y"):

                self.awaiting_workflow_switch = False

                # Switch to EMI calculation
                if self.pending_workflow == "emi":

                    self.paused_application_state = {
                        "pending_field": self.pending_field,
                        "awaiting_confirmation": self.awaiting_confirmation,
                        "awaiting_correction": self.awaiting_correction,
                        "awaiting_correction_value": self.awaiting_correction_value
                    }

                    self.pending_field = None
                    self.awaiting_confirmation = False
                    self.awaiting_correction = False
                    self.awaiting_correction_value = False

                    self.pending_workflow = None

                    return self.start_emi_calculation()

                # Switch to loan application
                elif self.pending_workflow == "application":

                    self.paused_emi_state = {
                        "emi_pending_field": self.emi_pending_field,
                        "emi_details": self.emi_details.copy()
                    }

                    self.emi_pending_field = None

                    # Resume an earlier application if available
                    if self.paused_application_state is not None:

                        state = self.paused_application_state

                        self.pending_field = state["pending_field"]
                        self.awaiting_confirmation = state["awaiting_confirmation"]
                        self.awaiting_correction = state["awaiting_correction"]
                        self.awaiting_correction_value = state["awaiting_correction_value"]

                        self.paused_application_state = None

                        if self.pending_field is not None:
                            return self.get_question(self.pending_field)

                        return (
                            "Your previous loan application has been resumed."
                        )

                    # Otherwise start a new application
                    missing_fields = self.get_missing_fields()

                    if missing_fields:
                        self.pending_field = missing_fields[0]
                        self.pending_workflow = None

                        return (
                            "Let's start your loan application.\n"
                            + self.get_question(self.pending_field)
                        )

                    return "Your loan application details are already complete."

                self.pending_workflow = None
                return "Unable to switch workflows. Please try again."

            elif answer in ("no", "n"):

                self.awaiting_workflow_switch = False
                self.pending_workflow = None

                return (
                    "Workflow switch cancelled. "
                    "Your current conversation is unchanged."
                )

            return "Please answer Yes or No."

        # Detect switching from EMI to loan application
        if (
            self.emi_pending_field is not None
            and application_request
        ):

            self.awaiting_workflow_switch = True
            self.pending_workflow = "application"

            return (
                "You are currently calculating EMI.\n"
                "Would you like to switch to a loan application?\n"
                "Enter Yes or No."
            )

        # Detect switching from loan application to EMI
        application_active = (
            self.pending_field is not None
            or self.awaiting_confirmation
            or self.awaiting_correction
            or self.awaiting_correction_value
        )

        if (
            application_active
            and detected_intent == "emi_calculation"
        ):

            self.awaiting_workflow_switch = True
            self.pending_workflow = "emi"

            return (
                "You are currently filling out a loan application.\n"
                "Would you like to switch to EMI calculation?\n"
                "Enter Yes or No."
            )

        # Resume a previously paused workflow
        if answer in ("resume previous", "resume", "continue previous"):

            if self.paused_application_state is not None:

                state = self.paused_application_state

                self.pending_field = state["pending_field"]
                self.awaiting_confirmation = state["awaiting_confirmation"]
                self.awaiting_correction = state["awaiting_correction"]
                self.awaiting_correction_value = state["awaiting_correction_value"]

                self.paused_application_state = None

                if self.pending_field is not None:
                    return self.get_question(self.pending_field)

                return "Your previous loan application has been resumed."

            if self.paused_emi_state is not None:

                state = self.paused_emi_state

                self.emi_pending_field = state["emi_pending_field"]
                self.emi_details = state["emi_details"].copy()

                self.paused_emi_state = None

                emi_questions = {
                    "loan_amount": "What is your loan amount in rupees?",
                    "interest_rate": "What is the annual interest rate in percentage?",
                    "loan_tenure": "What is your loan tenure in years?"
                }

                return emi_questions.get(
                    self.emi_pending_field,
                    "Your previous EMI calculation has been resumed."
                )

            return "There is no paused conversation to resume."

        # Final confirmation
        if self.awaiting_confirmation:

            if answer in ("yes", "y"):
                try:
                    result = self.predict_loan_approval()

                    if not result.get("success"):
                        return (
                            "Prediction could not be completed: "
                            + result.get(
                                "message",
                                "Please check your application details."
                            )
                        )

                    prediction = result.get("prediction")

                    if prediction not in ("Approved", "Rejected"):
                        return "The model returned an unexpected prediction."

                    self.last_prediction = result
                    self.awaiting_confirmation = False

                    return (
                        f"Model prediction: {prediction}\n"
                        f"Estimated class probabilities: "
                        f"{result.get('probabilities', {})}\n"
                        "This is an ML estimate, not a guaranteed bank "
                        "lending decision."
                    )

                except Exception as error:
                    return (
                        "An error occurred during prediction. "
                        f"Details: {error}"
                    )

            if answer in ("no", "n"):
                self.awaiting_confirmation = False
                self.awaiting_correction = True

                return (
                    "Which field would you like to correct?\n"
                    "Examples: income, loan amount, CIBIL score, "
                    "dependents, education, self-employed, tenure, "
                    "interest rate, or assets."
                )

            return "Please answer Yes or No."

        # Field correction
        if self.awaiting_correction:
            
            
            # Allow multiple corrections in one message
            try:
                correction_entities = extract_entities(message)

                updated_fields, validation_errors = (
                    self.update_from_entities(correction_entities)
                )

                if updated_fields or validation_errors:

                    if validation_errors:
                        error_details = "\n".join(
                            f"- {field.replace('_', ' ')}: {error}"
                            for field, error in validation_errors.items()
                        )

                        return (
                            "Some corrections could not be accepted:\n"
                            f"{error_details}\n"
                            "Please provide valid values."
                        )

                    self.awaiting_correction = False
                    self.show_applicant_summary()
                    self.awaiting_confirmation = True

                    updated_details = "\n".join(
                        f"- {field.replace('_', ' ')}: {value}"
                        for field, value in updated_fields.items()
                    )

                    return (
                        "The following details were updated:\n"
                        f"{updated_details}\n\n"
                        "Are these details correct? Enter Yes or No."
                    )

            except (ValueError, TypeError, KeyError) as error:
                return (
                    "I couldn't process the corrections. "
                    f"Please rephrase your message. Details: {error}"
                )


            field_aliases = {
                "dependents": "no_of_dependents",
                "number of dependents": "no_of_dependents",
                "no_of_dependents": "no_of_dependents",

                "income": "income_annum",
                "annual income": "income_annum",
                "income_annum": "income_annum",

                "loan amount": "loan_amount",
                "loan_amount": "loan_amount",

                "tenure": "loan_term",
                "loan tenure": "loan_term",
                "loan term": "loan_term",
                "loan_term": "loan_term",

                "cibil": "cibil_score",
                "cibil score": "cibil_score",
                "cibil_score": "cibil_score",

                "education": "education",

                "self employed": "self_employed",
                "self-employed": "self_employed",
                "self_employed": "self_employed",

                "residential assets": "residential_assets_value",
                "residential_assets_value": "residential_assets_value",

                "commercial assets": "commercial_assets_value",
                "commercial_assets_value": "commercial_assets_value",

                "luxury assets": "luxury_assets_value",
                "luxury_assets_value": "luxury_assets_value",

                "bank assets": "bank_asset_value",
                "bank assets value": "bank_asset_value",
                "bank_asset_value": "bank_asset_value",

                "interest rate": "interest_rate",
                "annual interest rate": "interest_rate",
                "interest_rate": "interest_rate"
            }

            requested_field = field_aliases.get(answer)

            if requested_field is None or requested_field not in self.applicant:
                return (
                    "I couldn't identify that field. Please enter a valid "
                    "field such as income, loan amount, CIBIL score, "
                    "education, or interest rate."
                )

            self.awaiting_correction = False
            self.awaiting_correction_value = True
            self.pending_field = requested_field

            return (
                "Please enter the corrected value for "
                f"{requested_field.replace('_', ' ')}."
            )

        # Save an answer to the requested or corrected field
        if self.pending_field is not None:

            field = self.pending_field

            saved = self.save_answer(field, message)
            
            if not saved:
                error_message = (
                    self.last_validation_error
                    or f"Invalid value for {field.replace('_', ' ')}."
                )

                return f"{error_message}\n{self.get_question(field)}"

            print(f"[Saved {field}: {self.applicant[field]}]")

            self.pending_field = None

            # If this was a correction, show the updated summary
            if self.awaiting_correction_value:
                self.awaiting_correction_value = False
                self.show_applicant_summary()
                self.awaiting_confirmation = True

                return (
                    "Applicant details updated successfully.\n"
                    "Are these details correct? Enter Yes to continue "
                    "or No to correct details."
                )
                
                
            #  # -----------------------------------------
            #  # HANDLE UNKNOWN OR UNRELATED MESSAGES
            # # -----------------------------------------

            # if detected_intent == "unknown" and not updated_fields:
            #         return (
            #             "I'm sorry, I couldn't understand your message.\n\n"
            #             "I can help you with:\n"
            #             "1. Loan eligibility\n"
            #             "2. EMI calculation\n"
            #             "3. Personal, home, car and education loans\n"
            #             "4. CIBIL score information\n"
            #             "5. Required loan documents\n\n"
            #             "Please ask a loan-related question."
            #         )

             # Ask for remaining information
            missing_fields = self.get_missing_fields()

            if missing_fields:
                    next_field = missing_fields[0]
                    self.pending_field = next_field
                    return self.get_question(next_field)

            # All information collected
            self.show_applicant_summary()
            self.awaiting_confirmation = True

            return (
                    "All required details have been collected.\n"
                    "Are these details correct? Enter Yes to continue "
                    "or No to correct details."
                )
                
        # Handle active EMI conversation
        if self.emi_pending_field is not None:
            return self.handle_emi_input(message)

        # Start a new EMI calculation conversation
        if self.detect_intent(message) == "emi_calculation":
            return self.start_emi_calculation()
        
        
        # -----------------------------------------
        # SMART INTENT AND CONTEXT ROUTING
        # -----------------------------------------

        # Detect the user's intent
        detected_intent = self.detect_intent(message)

        # Explicitly start independent EMI workflow
        if detected_intent == "emi_calculation":
            return self.start_emi_calculation()

        # Check whether the message is a follow-up
        followup_intent = self.resolve_followup_intent(message)

        # Avoid intercepting new application workflows
        workflow_intents = {
            "loan_eligibility",
            "loan_application",
            "emi_calculation"
        }

        if followup_intent and detected_intent not in workflow_intents:

            contextual_response = self.get_contextual_response(
                followup_intent
            )

            if contextual_response:
                return contextual_response

        # -----------------------------------------
        # NORMAL INTENT ROUTING
        # -----------------------------------------

        # Remember the latest informational loan topic
        topic_intents = {
            "personal_loan",
            "home_loan",
            "car_loan",
            "business_loan",
            "education_loan",
            "loan_types"
        }

        if detected_intent in topic_intents:
            self.last_topic = detected_intent

        # Do not route unknown messages to the unknown-intent
        # response yet; allow FAQ and entity extraction to run.
        if detected_intent != "unknown":

            route_response = self.route_intent(detected_intent)

            if route_response is not None:
                return route_response

        # -----------------------------------------
        # GENERAL LOAN FAQ
        # -----------------------------------------

        general_response = self.handle_general_loan_query(message)

        if general_response is not None:
            return general_response

        # -----------------------------------------
        # ENTITY EXTRACTION
        # -----------------------------------------

        try:
            entities = extract_entities(message)

            updated_fields, validation_errors = (
                self.update_from_entities(entities)
            )

            # Display extracted fields
            if updated_fields:
                print("\n[Successfully extracted fields]")

                for field, value in updated_fields.items():
                    print(f"{field}: {value}")

            # Handle invalid extracted values
            if validation_errors:

                error_details = "\n".join(
                    f"- {field.replace('_', ' ')}: {error}"
                    for field, error in validation_errors.items()
                )

                first_invalid_field = next(iter(validation_errors))

                self.pending_field = first_invalid_field

                return (
                    "Some details could not be accepted:\n"
                    f"{error_details}\n\n"
                    f"{self.get_question(first_invalid_field)}"
                )

        except (ValueError, TypeError, KeyError) as error:

            return (
                "I couldn't extract the application details. "
                f"Please rephrase your message. Details: {error}"
            )

        # -----------------------------------------
        # CONTINUE LOAN APPLICATION
        # -----------------------------------------

        missing_fields = self.get_missing_fields()

        if missing_fields:

            next_field = missing_fields[0]

            self.pending_field = next_field

            return self.get_question(next_field)

        # All required information collected
        self.show_applicant_summary()

        self.awaiting_confirmation = True

        return (
            "All required details have been collected.\n"
            "Are these details correct? Enter Yes to continue "
            "or No to correct details."
        )


        # # -----------------------------------------
        # # Smart intent routing for new messages
        # # -----------------------------------------

        # route_response = self.route_intent(message)

        # if route_response is not None:
        #     return route_response

        # # Handle general loan-related FAQ questions
        # general_response = self.handle_general_loan_query(message)

        # if general_response is not None:
        #     return general_response


        # else:
        #    # Extract entities from a new message
        #     try:
        #         entities = extract_entities(message)

        #         updated_fields, validation_errors = (
        #             self.update_from_entities(entities)
        #         )

        #         # Display successfully extracted fields
        #         if updated_fields:
        #             print("\n[Successfully extracted fields]")
        #             for field, value in updated_fields.items():
        #                 print(f"{field}: {value}")

        #         # Display rejected values
                
                
        #         if validation_errors:
        #             error_details = "\n".join(
        #                 f"- {field.replace('_', ' ')}: {error}"
        #                 for field, error in validation_errors.items()
        #             )

        #             first_invalid_field = next(iter(validation_errors))

        #             self.pending_field = first_invalid_field

        #             return (
        #                 "Some details could not be accepted:\n"
        #                 f"{error_details}\n\n"
        #                 f"{self.get_question(first_invalid_field)}"
        #             )



        #     except (ValueError, TypeError, KeyError) as error:
        #         return (
        #             "I couldn't extract the application details. "
        #             f"Please rephrase your message. Details: {error}"
        #         )
                
        #     # -----------------------------------------
        #     # Continue loan application
        #     # -----------------------------------------

        #     missing_fields = self.get_missing_fields()

        #     if missing_fields:

        #         next_field = missing_fields[0]

        #         self.pending_field = next_field

        #         return self.get_question(next_field)

        #     # All required information collected
        #     self.show_applicant_summary()

        #     self.awaiting_confirmation = True

        #     return (
        #         "All required details have been collected.\n"
        #         "Are these details correct? Enter Yes to continue "
        #         "or No to correct details."
        #     )


       


    def get_correction_field(self, user_input):

        correction_fields = {
            "dependents": "no_of_dependents",
            "no_of_dependents": "no_of_dependents",
            "education": "education",
            "self employed": "self_employed",
            "self_employed": "self_employed",
            "income": "income_annum",
            "annual income": "income_annum",
            "income_annum": "income_annum",
            "loan amount": "loan_amount",
            "loan_amount": "loan_amount",
            "tenure": "loan_term",
            "loan term": "loan_term",
            "loan_term": "loan_term",
            "cibil": "cibil_score",
            "cibil score": "cibil_score",
            "cibil_score": "cibil_score",
            "residential assets": "residential_assets_value",
            "residential_assets_value": "residential_assets_value",
            "commercial assets": "commercial_assets_value",
            "commercial_assets_value": "commercial_assets_value",
            "luxury assets": "luxury_assets_value",
            "luxury_assets_value": "luxury_assets_value",
            "bank assets": "bank_asset_value",
            "bank_asset_value": "bank_asset_value",
            "interest rate": "interest_rate",
            "interest_rate": "interest_rate"
        }

        return correction_fields.get(user_input.lower().strip())

    
    def handle_general_loan_query(self, message):

        text = message.lower().strip()

        loan_faq = {
            "cibil": (
                "A CIBIL score is a three-digit credit score "
                "ranging from 300 to 900. Lenders may use it "
                "to assess your credit history."
            ),

            "emi": (
                "EMI stands for Equated Monthly Instalment. "
                "It is the fixed monthly payment towards "
                "repaying a loan."
            ),

            "interest rate": (
                "An interest rate is the percentage charged "
                "by a lender on the borrowed amount. "
                "It affects your monthly EMI and total repayment."
            ),

            "loan tenure": (
                "Loan tenure is the period over which you "
                "repay your loan. A longer tenure generally "
                "reduces the EMI but can increase total interest."
            ),

            "credit score": (
                "A credit score reflects your credit history "
                "and repayment behaviour. Lenders may consider "
                "it while evaluating a loan application."
            ),

            "down payment": (
                "A down payment is the amount you pay upfront "
                "towards a purchase. The remaining amount may "
                "be financed through a loan."
            ),

            "foreclosure": (
                "Loan foreclosure means repaying the outstanding "
                "loan amount before the scheduled end of the tenure. "
                "Applicable charges depend on the lender and loan terms."
            )
        }

        for keyword, answer in loan_faq.items():
            if keyword in text:
                return answer

        question_starters = (
            "what", "why", "how", "when", "where",
            "who", "can you", "could you", "tell me"
        )

        if text.endswith("?") or text.startswith(question_starters):
            return (
                "I can help with loan amounts, EMI calculations, "
                "interest rates, CIBIL scores, loan eligibility, "
                "and repayment information. Please ask a "
                "loan-related question or continue your application."
            )

        return None
    
    
    def detect_intent(self, message):

        text = message.lower().strip()
        
        
        # -----------------------------------------
        # PREVENT FALSE LOAN APPLICATION DETECTION
        # -----------------------------------------

        unrelated_patterns = [
            "learn python",
            "learn java",
            "learn programming",
            "learn coding",
            "artificial intelligence",
            "machine learning",
            "weather today",
            "tell me a joke",
            "about cricket",
            "play cricket",
            "cook biryani",
            "prime minister of india"
        ]

        if any(pattern in text for pattern in unrelated_patterns):
            return "unknown"


        # ----------------------------------
        # 1. RULE-BASED INTENT DETECTION
        # ----------------------------------

        # Greeting
        greeting_patterns = [
            "hello",
            "hi",
            "hey",
            "good morning",
            "good afternoon",
            "good evening"
        ]

        if text in greeting_patterns:
            return "greeting"

        # Goodbye
        goodbye_patterns = [
            "bye",
            "goodbye",
            "see you",
            "thank you",
            "thanks"
        ]
        

        if text in goodbye_patterns:
            return "goodbye"
        
        # Loan application detection
        application_patterns = [
            "apply for a loan",
            "apply for personal loan",
            "apply for home loan",
            "apply for car loan",
            "apply for education loan",
            "i want to apply",
            "i need to apply",
            "start loan application",
            "start application",
            "loan application"
        ]

        if any(pattern in text for pattern in application_patterns):
            return "loan_application"

        # Personal loan
        if any(word in text for word in [
            "personal loan",
            "need personal loan",
            "want personal loan"
        ]):
            return "personal_loan"
        
         # CIBIL / credit score
        if any(word in text for word in [
            "cibil",
            "credit score",
            "improve my score",
            "check my score"
        ]):
            return "credit_score"
        
         # Foreclosure
        foreclosure_patterns = [
                "foreclosure",
                "foreclose",
                "close my loan",
                "close the loan",
                "loan closure",
                "close loan before tenure"
        ]

        if any(pattern in text for pattern in foreclosure_patterns):
            return "foreclosure"

        # Loan eligibility
        eligibility_patterns = [
            "loan eligibility",
            "check eligibility",
            "eligible for loan",
            "am i eligible",
            "qualify for loan"
        ]
        
        if any(pattern in text for pattern in eligibility_patterns):
            return "loan_eligibility"

        # EMI calculation
        emi_patterns = [
            "calculate emi",
            "emi calculation",
            "monthly emi",
            "calculate my emi",
            "emi for"
        ]

        if any(pattern in text for pattern in emi_patterns):
            return "emi_calculation"

        # Early loan repayment
        prepayment_patterns = [
                "repay early",
                "repay my loan early",
                "repay my loan before time",
                "repay loan before time",
                "repay before time",
                "pay loan early",
                "pay my loan early",
                "pay off my loan early",
                "early repayment",
                "early loan repayment",
                "partial payment",
                "partial prepayment",
                "prepayment",
                "charges for prepayment",
                "charges for early loan repayment",
                "early repayment charges",
                "pay before tenure",
                "repay before tenure"
        ]

        if any(pattern in text for pattern in prepayment_patterns):
            return "prepayment"
        
                # Loan types detection
        if any(keyword in text for keyword in [
            "types of loan",
            "type of loan",
            "types of loans",
            "loan types",
            "different loans",
            "available loans"
        ]):
            return "loan_types"
        
        # Required documents detection
        if any(keyword in text for keyword in [
            "required documents",
            "documents required",
            "documents needed",
            "loan documents",
            "which documents",
            "what documents",
            "paperwork required"
        ]):
            return "required_documents"


        # ----------------------------------
        # 2. ML INTENT CLASSIFICATION
        # ----------------------------------

        if not hasattr(self, "intent_model") or not hasattr(self, "intent_tfidf"):
            return "unknown"

        transformed_text = self.intent_tfidf.transform([text])

        prediction = self.intent_model.predict(
            transformed_text
        )[0]

        if hasattr(self.intent_model, "predict_proba"):

            probabilities = self.intent_model.predict_proba(
                transformed_text
            )[0]

            confidence = max(probabilities)

            # Low-confidence prediction
            if confidence < 0.35:
                return "unknown"

        return prediction
    
    
    
    def route_intent(self, intent):

        if not intent:
            return None

        intent = intent.lower().strip()

        # --------------------------------
        # 1. GREETING
        # --------------------------------
        if intent == "greeting":
            return (
                "Hello! Welcome to Loan Advisor Chatbot.\n"
                "I can help you with loan eligibility, EMI calculation, "
                "CIBIL score and different types of loans.\n"
                "How can I help you today?"
            )

        # --------------------------------
        # 2. GOODBYE
        # --------------------------------
        if intent == "goodbye":
            return (
                "Thank you for using Loan Advisor Chatbot!\n"
                "Have a great day."
            )

        # --------------------------------
        # 3. UNKNOWN INTENT
        # --------------------------------
        if intent == "unknown":
            return (
                "Sorry, I couldn't understand your question.\n"
                "You can ask me about personal loans, home loans, "
                "car loans, EMI, CIBIL score or loan eligibility."
            )

        # --------------------------------
        # 4. INFORMATIONAL INTENT RESPONSES
        # --------------------------------
        responses = {

            "personal_loan": (
                "A personal loan is an unsecured loan that can be used "
                "for medical expenses, travel, education or personal needs.\n\n"
                "Common features:\n"
                "- Usually no collateral is required.\n"
                "- Interest rates depend on your credit profile.\n"
                "- Repayment is generally through monthly EMIs.\n"
                "- Approval depends on income, credit score and lender policy."
            ),

            "home_loan": (
                "A home loan is a secured loan used to purchase, construct "
                "or renovate a residential property.\n\n"
                "Common features:\n"
                "- Property is generally used as security.\n"
                "- Repayment is made through monthly EMIs.\n"
                "- Tenure and interest rates depend on the lender.\n"
                "- Property documents and income proof are generally required."
            ),

            "car_loan": (
                "A car loan is used to purchase a new or used vehicle.\n\n"
                "Common features:\n"
                "- The vehicle generally acts as security.\n"
                "- Down payment may be required.\n"
                "- EMI depends on loan amount, interest rate and tenure.\n"
                "- Approval depends on income and credit profile."
            ),

            "business_loan": (
                "A business loan provides funds for business operations, "
                "expansion, equipment or working capital.\n\n"
                "Lenders may evaluate:\n"
                "- Business income and financial statements.\n"
                "- Business vintage and stability.\n"
                "- Credit history.\n"
                "- Existing financial obligations."
            ),

            "education_loan": (
                "An education loan helps students finance higher education "
                "in India or abroad.\n\n"
                "It may cover tuition fees, accommodation, books and "
                "other eligible education expenses.\n"
                "Eligibility and repayment conditions depend on the lender."
            ),

            "credit_score": (
                "A credit score represents your credit repayment history "
                "and creditworthiness.\n\n"
                "In India, CIBIL scores generally range from 300 to 900.\n"
                "A higher score can improve your chances of getting "
                "favourable loan terms, subject to lender policies."
            ),

            "loan_types": (
                "Common types of loans include:\n"
                "1. Personal Loan\n"
                "2. Home Loan\n"
                "3. Car Loan\n"
                "4. Education Loan\n"
                "5. Business Loan\n"
                "6. Gold Loan\n"
                "7. Loan Against Property\n\n"
                "Each loan has different eligibility requirements and terms."
            ),

            "required_documents": (
                "Common documents required for loan applications include:\n"
                "- PAN card and identity proof.\n"
                "- Address proof.\n"
                "- Recent bank statements.\n"
                "- Salary slips or income proof.\n"
                "- Income tax returns, where applicable.\n"
                "- Property or vehicle documents for secured loans.\n\n"
                "Exact requirements depend on the lender and loan type."
            ),

            "processing_fee": (
                "A loan processing fee is a charge collected by a lender "
                "for processing a loan application.\n\n"
                "The fee may depend on:\n"
                "- Loan type.\n"
                "- Loan amount.\n"
                "- Lender's pricing policy.\n\n"
                "Check the lender's official fee schedule before applying."
            ),

            "interest_rate": (
                "Loan interest rates represent the cost of borrowing money.\n\n"
                "Rates depend on factors such as:\n"
                "- Credit score.\n"
                "- Income and repayment capacity.\n"
                "- Loan type and tenure.\n"
                "- Lender's policies and market conditions.\n\n"
                "Compare the annual interest rate and applicable charges "
                "before selecting a loan."
            ),

            "loan_tenure": (
                "Loan tenure is the period over which you repay a loan.\n\n"
                "A longer tenure generally reduces monthly EMI but may "
                "increase total interest paid.\n"
                "A shorter tenure generally increases EMI but reduces "
                "total interest."
            ),

            "loan_amount": (
                "The loan amount is the money borrowed from a lender.\n\n"
                "The eligible amount depends on:\n"
                "- Monthly or annual income.\n"
                "- Existing EMIs and financial obligations.\n"
                "- Credit score.\n"
                "- Loan type and lender policy."
            ),

            "income_requirement": (
                "Income requirements vary according to the loan type "
                "and lender.\n\n"
                "Lenders generally evaluate income stability, employment "
                "type, existing EMIs and repayment capacity."
            ),

            # "loan_eligibility": (
            #     "Let's check your loan eligibility.\n"
            #     "I will collect your financial and personal details."
            # ),

            # "loan_application": (
            #     "To apply for a loan, you generally need to select a loan "
            #     "type, check eligibility, prepare the required documents "
            #     "and submit an application to a lender."
            # ),

            "application_status": (
                "I cannot access your bank's live application status.\n\n"
                "Please check the lender's official website, mobile app "
                "or contact customer support using your application number."
            ),

            "coapplicant": (
                "A co-applicant is another person who applies for a loan "
                "along with the primary applicant.\n\n"
                "A co-applicant's income and credit history may be considered "
                "when evaluating eligibility. Both applicants may share "
                "repayment responsibility."
            ),

            "existing_loan": (
                "Existing loans and EMIs affect your repayment capacity.\n\n"
                "Lenders may consider your outstanding loan balance, "
                "monthly EMI obligations and repayment history when "
                "evaluating a new application."
            ),

            "prepayment": (
                "Loan prepayment means paying some or all of your outstanding "
                "loan amount before the scheduled repayment date.\n\n"
                "Partial prepayment may reduce your outstanding principal "
                "and future interest.\n"
                "Applicable charges depend on the loan agreement and lender."
            ),

            "foreclosure": (
                "Loan foreclosure means repaying the entire outstanding "
                "loan amount before the end of its tenure.\n\n"
                "Before foreclosure, request the outstanding amount and "
                "check applicable charges with your lender."
            ),

            "loan_rejection": (
                "A loan application may be rejected for several reasons:\n"
                "- Low credit score.\n"
                "- Insufficient income.\n"
                "- High existing EMI obligations.\n"
                "- Incomplete or incorrect documents.\n"
                "- Not meeting lender eligibility requirements.\n\n"
                "Check the rejection reason with your lender before reapplying."
            ),

            "loan_top_up": (
                "A loan top-up is an additional loan amount offered to "
                "an existing borrower, usually on an existing loan.\n\n"
                "Eligibility depends on repayment history, outstanding "
                "balance, income and lender policy."
            )
        }

        # --------------------------------
        # 5. RETURN MATCHING RESPONSE
        # --------------------------------
        return responses.get(intent)
    
    
    
    def resolve_followup_intent(self, user_message):

            text = user_message.lower().strip()

            # No previous topic: cannot resolve a contextual question
            if not self.last_topic:
                return None

            # Interest rate follow-up
            if any(word in text for word in [
                "interest rate",
                "rate of interest",
                "how much interest"
            ]):
                return "interest_rate"

            # Document follow-up
            if any(word in text for word in [
                "documents",
                "document",
                "paperwork",
                "proof required"
            ]):
                return "required_documents"

            # Tenure follow-up
            if any(word in text for word in [
                "tenure",
                "repayment period",
                "repayment duration"
            ]):
                return "loan_tenure"

            # EMI follow-up
            if any(word in text for word in [
                "emi",
                "monthly installment",
                "monthly payment"
            ]):
                return "emi_calculation"

            # Eligibility follow-up
            if any(word in text for word in [
                "eligibility",
                "eligible",
                "qualify"
            ]):
                return "loan_eligibility"

            return None
        
    
    def get_contextual_response(self, intent):

        topic_names = {
            "personal_loan": "personal loan",
            "home_loan": "home loan",
            "car_loan": "car loan",
            "business_loan": "business loan",
            "education_loan": "education loan",
            "loan_types": "loan options"
        }

        topic = topic_names.get(self.last_topic)

        if not topic:
            return None

        if intent == "interest_rate":
            return (
                f"For a {topic}, interest rates depend on "
                "your credit score, income, repayment capacity "
                "and lender policy. Compare current offers "
                "before choosing a lender."
            )

        if intent == "required_documents":
            return (
                f"For a {topic}, commonly requested documents include:\n"
                "- PAN card and identity proof\n"
                "- Address proof\n"
                "- Recent bank statements\n"
                "- Income proof\n\n"
                "Exact requirements depend on the lender."
            )

        if intent == "loan_tenure":
            return (
                f"For a {topic}, repayment tenure depends on "
                "the lender and your eligibility. A longer tenure "
                "usually reduces EMI but increases total interest."
            )

        if intent == "emi_calculation":
            return (
                f"I can calculate the EMI for your {topic}. "
                "Please select the EMI calculator and enter "
                "your loan amount, interest rate and tenure."
            )

        if intent == "loan_eligibility":
            return (
                f"To check eligibility for a {topic}, "
                "I can collect your financial details and "
                "provide an estimated result."
            )

        return None





if __name__ == "__main__":
    chatbot = LoanConversationManager()

    print("Loan Advisor Chatbot")
    print("Type 'exit' to stop.\n")

    while True:
        message = input("You: ").strip()
        response = chatbot.process_message(message)
        print("Bot:", response)

        if message.lower() in ("exit", "quit", "bye"):
            break

