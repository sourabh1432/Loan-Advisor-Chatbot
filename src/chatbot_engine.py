
from pathlib import Path
import joblib

from src.entity_extraction import extract_entities


# --------------------------------------------------
# 1. Load saved models
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent
MODEL_DIR = PROJECT_ROOT / "models"

intent_vectorizer = joblib.load(
    MODEL_DIR / "intent_tfidf.pkl"
)

intent_model = joblib.load(
    MODEL_DIR / "intent_classifier.pkl"
)

loan_approval_model = joblib.load(
    MODEL_DIR / "loan_approval_rf.pkl"
)

loan_approval_features = joblib.load(
    MODEL_DIR / "loan_approval_features.pkl"
)


# --------------------------------------------------
# 2. Predict user intent
# --------------------------------------------------


def predict_intent(message):
    message = message.lower().strip()

    if not message:
        return {
            "intent": None,
            "confidence": 0.0
        }

    # Rule-based handling for clear, common requests
    eligibility_phrases = [
        "loan eligibility",
        "eligible for a loan",
        "eligible for personal loan",
        "am i eligible",
        "check my eligibility"
    ]

    application_status_phrases = [
        "application status",
        "status of my application",
        "track my application",
        "loan status"
    ]

    if any(phrase in message for phrase in eligibility_phrases):
        return {
            "intent": "loan_eligibility",
            "confidence": 1.0
        }

    if any(phrase in message for phrase in application_status_phrases):
        return {
            "intent": "application_status",
            "confidence": 1.0
        }

    # ML prediction for other messages
    message_vector = intent_vectorizer.transform([message])

    predicted_intent = intent_model.predict(
        message_vector
    )[0]

    probabilities = intent_model.predict_proba(
        message_vector
    )[0]

    confidence = float(probabilities.max())

    return {
        "intent": predicted_intent,
        "confidence": round(confidence, 4)
    }


# --------------------------------------------------
# 3. Process user message
# --------------------------------------------------

def process_message(message):
    intent_result = predict_intent(message)

    entities = extract_entities(message)

    return {
        "message": message,
        "intent": intent_result["intent"],
        "confidence": intent_result["confidence"],
        "entities": entities
    }


# --------------------------------------------------
# 4. Basic test
# --------------------------------------------------

if __name__ == "__main__":
    test_messages = [
        "Hello",
        "I want to check my loan eligibility",
        "What is my loan application status?",
        (
            "I earn 60000 per month and need "
            "5 lakh for 5 years. My CIBIL score "
            "is 750 and I have 2 dependents."
        )
    ]

    for message in test_messages:
        print("\nUser:", message)

        result = process_message(message)

        print("Intent:", result["intent"])
        print("Confidence:", result["confidence"])
        print("Entities:", result["entities"])
