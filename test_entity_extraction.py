
from src.conversation_manager import LoanConversationManager


def test_save_answer():
    chatbot = LoanConversationManager()

    test_cases = [
        ("cibil_score", "750", True),
        ("cibil_score", "950", False),
        ("no_of_dependents", "2.5", False),
        ("no_of_dependents", "-1", False),
        ("education", "Graduate", True),
        ("self_employed", "Maybe", False),
        ("loan_term", "5", True),
        ("loan_term", "0", False),
        ("bank_asset_value", "no", True),
    ]

    print("\nTesting save_answer()")
    print("=" * 50)

    for field, answer, expected in test_cases:
        chatbot.pending_field = field
        result = chatbot.save_answer(field, answer)

        status = "PASS" if result == expected else "FAIL"

        print(
            f"{status} | Field: {field} | "
            f"Input: {answer} | Expected: {expected} | "
            f"Actual: {result}"
        )


if __name__ == "__main__":
    test_save_answer()


# from src.entity_extraction import extract_entities
# from src.input_validation import validate_field

# test_cases = [
#     ("cibil_score", 750),
#     ("cibil_score", 950),
#     ("no_of_dependents", -1),
#     ("no_of_dependents", 2.5),
#     ("loan_amount", -50000),
#     ("loan_term", 5),
#     ("education", "Graduate"),
#     ("self_employed", "Maybe"),
# ]

# for field, value in test_cases:
#     valid, message = validate_field(field, value)

#     print(
#         f"{field} = {value} -> "
#         f"{'VALID' if valid else 'INVALID'}: {message}"
#     )

# # message = (
# #     "I earn ₹60,000 per month and need ₹5 lakh "
# #     "for 5 years. My CIBIL score is 750 "
# #     "and I have 2 dependents."
# # )

# # result = extract_entities(message)

# # for entity, value in result.items():
# #     print(f"{entity}: {value}")