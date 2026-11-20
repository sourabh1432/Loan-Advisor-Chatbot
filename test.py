from src.conversation_manager import LoanConversationManager

manager = LoanConversationManager()

test_messages = [
    "Hello",
    "Thank you",
    "Tell me a joke",
    "I need a personal loan of 5 lakh"
]

for message in test_messages:
    print("User:", message)
    print("Response:", manager.route_intent(message))
    print("-" * 60)