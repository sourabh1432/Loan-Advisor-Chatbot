
from src.entity_extraction import extract_entities
from src.input_validation import validate_applicant, prepare_model_input
from src.conversation_manager import LoanConversationManager


def test_entity_extraction():
    message = (
        "I earn ₹60,000 per month and need ₹5 lakh for 5 years. "
        "My CIBIL score is 750 and I have 2 dependents."
    )

    entities = extract_entities(message)

    print("\nEntity extraction:")
    print(entities)

    assert entities is not None
    assert entities.get("income") == 60000
    assert entities.get("credit_score") == 750
    assert entities.get("dependents") == 2

    print("PASS: Entity extraction")


def test_input_validation():
    applicant = {
        "no_of_dependents": 2,
        "education": "Graduate",
        "self_employed": "No",
        "income_annum": 720000,
        "loan_amount": 500000,
        "loan_term": 5,
        "cibil_score": 750,
        "residential_assets_value": 20000,
        "commercial_assets_value": 22000,
        "luxury_assets_value": 56000,
        "bank_asset_value": 0,
    }

    errors = validate_applicant(applicant)
    assert errors == [], f"Unexpected validation errors: {errors}"

    invalid_applicant = applicant.copy()
    invalid_applicant["cibil_score"] = 950

    errors = validate_applicant(invalid_applicant)
    assert errors, "Invalid CIBIL score was not rejected"

    print("PASS: Input validation")


def test_model_prediction():
    chatbot = LoanConversationManager()

    applicant = {
        "no_of_dependents": 2,
        "education": "Graduate",
        "self_employed": "No",
        "income_annum": 720000,
        "loan_amount": 500000,
        "loan_term": 5,
        "cibil_score": 750,
        "residential_assets_value": 20000,
        "commercial_assets_value": 22000,
        "luxury_assets_value": 56000,
        "bank_asset_value": 0,
    }

    chatbot.applicant.update(applicant)

    result = chatbot.predict_loan_approval()

    print("\nModel prediction:")
    print(result)

    assert result.get("success") is True
    assert result.get("prediction") in ("Approved", "Rejected")

    print("PASS: Random Forest prediction")


def test_reset():
    chatbot = LoanConversationManager()
    chatbot.applicant["cibil_score"] = 750
    chatbot.awaiting_confirmation = True

    chatbot.reset_conversation()

    assert chatbot.applicant["cibil_score"] is None
    assert chatbot.awaiting_confirmation is False
    assert chatbot.pending_field is None

    print("PASS: Reset conversation")


if __name__ == "__main__":
    test_entity_extraction()
    test_input_validation()
    test_model_prediction()
    test_reset()

    print("\nAll end-to-end component tests passed.")
