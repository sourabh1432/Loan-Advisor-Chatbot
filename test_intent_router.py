
import joblib
from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).resolve().parent

MODEL_PATH = BASE_DIR / "models" / "intent_classifier.pkl"
VECTORIZER_PATH = BASE_DIR / "models" / "intent_tfidf.pkl"

# Load existing trained models
intent_model = joblib.load(MODEL_PATH)
tfidf = joblib.load(VECTORIZER_PATH)

# Display all trained intents
print("\n========== AVAILABLE INTENTS ==========")

for intent in intent_model.classes_:
    print(intent)

print("\n========== INTENT PREDICTION TEST ==========")

test_messages = [
    "Hello",
    "I need a personal loan of 5 lakh",
    "Calculate EMI for 5 lakh",
    "What is CIBIL score?",
    "I want to check my loan eligibility",
    "How can I repay my loan early?",
    "Tell me a joke",
    "Thank you"
]

for message in test_messages:

    transformed_text = tfidf.transform([message])

    prediction = intent_model.predict(transformed_text)[0]

    print("\nUser:", message)
    print("Predicted intent:", prediction)

    if hasattr(intent_model, "predict_proba"):
        probabilities = intent_model.predict_proba(
            transformed_text
        )[0]

        confidence = max(probabilities) * 100

        print("Confidence:", round(confidence, 2), "%")
