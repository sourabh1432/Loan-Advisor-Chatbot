
from src.conversation_manager import LoanConversationManager

manager = LoanConversationManager()

# =====================================
# TEST 1: GENERAL LOAN QUESTIONS
# =====================================

questions = [
    "What is CIBIL score?",
    "What is EMI?",
    "Explain interest rate.",
    "What is loan tenure?",
    "Tell me a joke."
]

print("\n========== GENERAL QUERY TESTS ==========")

for question in questions:
    print("\nUser:", question)
    print("Bot:", manager.handle_general_loan_query(question))


# =====================================
# TEST 2: INVALID INPUT VALIDATION
# =====================================

from src.input_validation import validate_field

invalid_tests = [
    ("income_annum", -50000),
    ("loan_amount", -500000),
    ("loan_amount", 0),
    ("cibil_score", 950),
    ("cibil_score", 250),
    ("no_of_dependents", -2),
    ("interest_rate", 150)
]

print("\n========== INVALID INPUT TESTS ==========")

for field, value in invalid_tests:

    is_valid, message = validate_field(field, value)

    print(
        f"Field: {field} | Value: {value} | "
        f"Valid: {is_valid} | Message: {message}"
    )
