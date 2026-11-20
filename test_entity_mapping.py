
from src.conversation_manager import LoanConversationManager
from src.entity_extraction import extract_entities

manager = LoanConversationManager()

message = (
    "I need a personal loan of 5 lakh for 5 years. "
    "My monthly income is 60000. "
    "My CIBIL score is 750 and I have 2 dependents. "
    "Interest rate is 10%."
)

entities = extract_entities(message)

print("Extracted entities:")
print(entities)

updated_fields, validation_errors = (
    manager.update_from_entities(entities)
)

print("\nUpdated applicant fields:")
print(updated_fields)

print("\nValidation errors:")
print(validation_errors)

print("\nApplicant details:")
print(manager.applicant)
