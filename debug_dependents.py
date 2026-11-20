
from src.conversation_manager import LoanConversationManager

manager = LoanConversationManager()

manager.pending_field = "no_of_dependents"

print("Pending field:", repr(manager.pending_field))

test_values = ["2", "two", "0", "5", "-1", "21"]

for value in test_values:

    manager.pending_field = "no_of_dependents"

    print("\nTesting input:", repr(value))

    result = manager.save_answer("no_of_dependents", value)

    print("Save result:", result)
    print("Saved value:", manager.applicant["no_of_dependents"])
    print("Validation error:", manager.last_validation_error)
