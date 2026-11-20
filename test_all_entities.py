
from src.entity_extraction import extract_entities

test_messages = [
    "I need a personal loan of 5 lakh for 5 years. My monthly income is 60000. My CIBIL score is 750 and I have 2 dependents.",

    "I want a home loan of 25 lakh for 20 years. My annual income is 900000 and my CIBIL score is 800.",

    "I need a car loan of 6 lakh for 5 years. My monthly income is 50000.",

    "I need an education loan of 12 lakh for 7 years.",

    "I need a business loan of 25 lakh. My annual income is 1200000.",

    "I need a loan of -500000.",
    
    "I need a personal loan of 5 lakh at 10% interest for 5 years.",

    "I need a home loan of 25 lakh with an interest rate of 8.5%.",

    "I want a car loan of 6 lakh at 9 percent interest."
]

for message in test_messages:

    print("\nUser:", message)

    entities = extract_entities(message)

    print("\nExtracted entities:")

    for field, value in entities.items():
        print(f"{field}: {value}")

    print("=" * 60)
