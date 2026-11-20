
from src.entity_extraction import extract_entities

test_messages = [
    "I need a loan of -500000.",
    "My annual income is -50000.",
    "My CIBIL score is 950.",
    "I need a loan of 0.",
    "My monthly income is 60000."
]

for message in test_messages:

    print("\nUser:", message)

    entities = extract_entities(message)

    print("Extracted entities:")

    for field, value in entities.items():
        print(f"{field}: {value}")

    print("-" * 60)
