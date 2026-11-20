
from numbers import Real
import pandas as pd


NUMERIC_FIELDS = [
    "no_of_dependents",
    "income_annum",
    "loan_amount",
    "loan_term",
    "cibil_score",
    "residential_assets_value",
    "commercial_assets_value",
    "luxury_assets_value",
    "bank_asset_value",
]

VALID_EDUCATION = {"Graduate", "Not Graduate"}
VALID_SELF_EMPLOYED = {"Yes", "No"}


def validate_field(field, value):
    """Validate one applicant field."""

    if value is None:
        return False, f"{field} is required."

    # Dependents
    if field == "no_of_dependents":
        if isinstance(value, bool) or not isinstance(value, Real):
            return False, "Number of dependents must be a valid number."

        if pd.isna(value) or not float(value).is_integer():
            return False, "Number of dependents must be a whole number."

        if not 0 <= value <= 20:
            return False, "Number of dependents must be between 0 and 20."

        return True, "Valid input."

    # Education
    if field == "education":
        if value not in VALID_EDUCATION:
            return False, "Education must be Graduate or Not Graduate."

        return True, "Valid input."

    # Self-employed
    if field == "self_employed":
        if value not in VALID_SELF_EMPLOYED:
            return False, "Self-employed must be Yes or No."

        return True, "Valid input."

    # Interest rate: used for EMI, not as a model feature
    if field == "interest_rate":
        if isinstance(value, bool) or not isinstance(value, Real):
            return False, "Interest rate must be a valid number."

        if pd.isna(value):
            return False, "Interest rate must be a valid number."

        if not 0 <= value <= 100:
            return False, "Annual interest rate must be between 0 and 100%."

        return True, "Valid input."

    # Other numeric fields
    if field in NUMERIC_FIELDS:
        if isinstance(value, bool) or not isinstance(value, Real):
            return False, f"{field} must be a valid number."

        if pd.isna(value):
            return False, f"{field} must be a valid number."

        if value < 0:
            return False, f"{field} cannot be negative."

        if field == "loan_amount" and value <= 0:
            return False, "Loan amount must be greater than zero."

        if field == "cibil_score" and not 300 <= value <= 900:
            return False, "CIBIL score must be between 300 and 900."

        if field == "loan_term" and not 1 <= value <= 40:
            return False, "Loan term must be between 1 and 40 years."
        
        if field == "income_annum" and value < 0:
            return False, "Income cannot be negative."

        return True, "Valid input."

    return False, f"Unknown field: {field}"


def validate_applicant(applicant):
    """Validate all required applicant fields."""

    errors = []

    required_fields = NUMERIC_FIELDS + [
        "education",
        "self_employed",
        "interest_rate",
    ]

    for field in required_fields:
        value = applicant.get(field)
        is_valid, message = validate_field(field, value)

        if not is_valid:
            errors.append(message)

    return errors


def prepare_model_input(applicant, feature_names):
    """Prepare applicant data in the exact order expected by the model."""

    errors = validate_applicant(applicant)

    if errors:
        raise ValueError("\n".join(errors))

    # Interest rate is intentionally excluded from model features.
    row = {
        field: applicant[field]
        for field in NUMERIC_FIELDS
    }

    for field, categories in [
        ("education", VALID_EDUCATION),
        ("self_employed", VALID_SELF_EMPLOYED),
    ]:
        for category in categories:
            feature_name = f"{field}_ {category}"
            row[feature_name] = int(applicant[field] == category)

    model_input = pd.DataFrame([row])

    model_input = model_input.reindex(
        columns=feature_names,
        fill_value=0,
    )

    return model_input






# from numbers import Real
# import pandas as pd

# NUMERIC_FIELDS = [
#     "no_of_dependents",
#     "income_annum",
#     "loan_amount",
#     "loan_term",
#     "cibil_score",
#     "residential_assets_value",
#     "commercial_assets_value",
#     "luxury_assets_value",
#     "bank_asset_value",
# ]

# VALID_EDUCATION = {"Graduate", "Not Graduate"}
# VALID_SELF_EMPLOYED = {"Yes", "No"}


# def validate_field(field, value):
#     """Validate one applicant field."""

#     if value is None:
#         return False, f"{field} is required."
    
#         # Dependents validation
#     if field == "no_of_dependents":
#         if not isinstance(value, Real) or isinstance(value, bool):
#             return False, "Number of dependents must be a valid number."

#         if pd.isna(value) or not float(value).is_integer():

#             return False, "Number of dependents must be a whole number."

#         if value < 0 or value > 20:
#             return False, "Number of dependents must be between 0 and 20."

#         return True, "Valid input."

#     if field in NUMERIC_FIELDS:
#         if isinstance(value, bool) or not isinstance(value, Real):
#             return False, f"{field} must be a valid number."

#         if pd.isna(value):
#             return False, f"{field} must be a valid number."

#         if value < 0:
#             return False, f"{field} cannot be negative."
        
#         if field == "loan_amount" and value <= 0:
#             return False, "Loan amount must be greater than zero."

#     if field == "no_of_dependents":
#         if not float(value).is_integer():
#             return False, "Number of dependents must be a whole number."

#     if field == "cibil_score":
#         if not 300 <= value <= 900:
#             return False, "CIBIL score must be between 300 and 900."

#     if field == "loan_term":
#         if not 1 <= value <= 40:
#             return False, "Loan term must be between 1 and 40 years."

#     if field == "education":
#         if value not in VALID_EDUCATION:
#             return False, "Education must be Graduate or Not Graduate."

#     if field == "self_employed":
#         if value not in VALID_SELF_EMPLOYED:
#             return False, "Self-employed must be Yes or No."
        
#     if field == "interest_rate":
#         if isinstance(value, bool) or not isinstance(value, Real):
#             return False, "Interest rate must be a valid number."

#         if pd.isna(value):
#             return False, "Interest rate must be a valid number."

#         if not 0 <= value <= 100:
#             return False, "Annual interest rate must be between 0 and 100%."

#     return True, "Valid input."


# def validate_applicant(applicant):
#     """Validate all applicant fields."""

#     errors = []

#     required_fields = NUMERIC_FIELDS + [
#         "education",
#         "self_employed",
#     ]

#     for field in required_fields:
#         value = applicant.get(field)

#         is_valid, message = validate_field(field, value)

#         if not is_valid:
#             errors.append(message)

#     return errors


# def prepare_model_input(applicant, feature_names):
#     """Prepare applicant data in the exact order expected by the model."""

#     errors = validate_applicant(applicant)

#     if errors:
#         raise ValueError("\n".join(errors))

#     row = {
#         field: applicant[field]
#         for field in NUMERIC_FIELDS
#     }

#     # Keep the feature names compatible with the trained model.
#     for field, categories in [
#         ("education", VALID_EDUCATION),
#         ("self_employed", VALID_SELF_EMPLOYED),
#     ]:
#         for category in categories:
#             feature_name = f"{field}_ {category}"
#             row[feature_name] = int(applicant[field] == category)

#     model_input = pd.DataFrame([row])

#     # Ensure all model features exist and are in training order.
#     model_input = model_input.reindex(
#         columns=feature_names,
#         fill_value=0,
#     )

#     return model_input