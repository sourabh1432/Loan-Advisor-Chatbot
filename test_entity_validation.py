
from src.conversation_manager import LoanConversationManager

manager = LoanConversationManager()

test_messages = [
    "I need a personal loan of 5 lakh. My annual income is 720000.",
    "My CIBIL score is 750 and I have 2 dependents.",
    "I need a loan of -500000.",
]

for message in test_messages:

    print("\nUser:", message)

    response = manager.process_message(message)

    print("Bot:", response)

    print("\nApplicant details:")
    print(manager.applicant)

    print("-" * 60)


# from src.conversation_manager import LoanConversationManager


# manager = LoanConversationManager()

# test_entities = {
#     "no_of_dependents": 2,
#     "income_annum": 720000,
#     "loan_amount": -500000,
#     "cibil_score": 750
# }

# updated_fields, validation_errors = manager.update_from_entities(
#     test_entities
# )

# print("=" * 50)
# print("ENTITY VALIDATION TEST")
# print("=" * 50)

# print("\nSuccessfully saved fields:")
# print(updated_fields)

# print("\nValidation errors:")
# print(validation_errors)

# print("\nApplicant details:")
# print(manager.applicant)
