
from src.conversation_manager import LoanConversationManager

manager = LoanConversationManager()

print("Intent model loaded:", hasattr(manager, "intent_model"))
print("TF-IDF loaded:", hasattr(manager, "intent_tfidf"))

test_messages = [
    "Hello",
    "Good morning",
    "I need a personal loan of 5 lakh",
    "Calculate EMI for 5 lakh",
    "What is CIBIL score?",
    "I want to check my loan eligibility",
    "How can I repay my loan early?",
    "Tell me a joke",
    "Thank you",
    "Can I close my loan before the tenure ends?",
    "I want to repay my loan before time",
    "What is loan prepayment?",
    "Are there charges for early loan repayment?",
    "I want to repay my loan before time",
    "Are there charges for early loan repayment?",
    "What is loan prepayment?",
    "Can I make a partial payment?",
    "How does foreclosure work?"
]

for message in test_messages:

    intent = manager.detect_intent(message)

    print("\nUser:", message)
    print("Detected intent:", intent)
    print("-" * 50)
