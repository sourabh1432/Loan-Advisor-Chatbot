
from src.conversation_manager import LoanConversationManager


def main():

    print("=" * 55)
    print("          WELCOME TO LOAN ADVISOR CHATBOT")
    print("=" * 55)

    print("\nI can help you with:")
    print("1. Loan eligibility")
    print("2. EMI calculation")
    print("3. CIBIL score information")
    print("4. Loan-related questions")
    print("5. Hello")
    print("6. I need a personal loan of 5 lakh")
    print("7. What is CIBIL score?")
    print("8. Tell me a joke")
    print("9. Thank you")
    print("\nType 'exit' to close the chatbot.")

    manager = LoanConversationManager()
    
    menu_options = {
    "1": "I want to check my loan eligibility",
    "2": "I want to calculate EMI",
    "3": "Tell me about CIBIL score",
    "4": "Tell me about loans",
    "5": "Hello",
    "6": "I need a personal loan of 5 lakh",
    "7": "What is CIBIL score?",
    "8": "Tell me a joke",
    "9": "Thank you"
}

    while True:

        try:
            user_message = input("\nYou: ").strip()

        except EOFError:
            print("\nBot: Input stream closed. Exiting chatbot.")
            break

        if not user_message:
            print("Bot: Please enter a message.")
            continue

        if user_message.lower() in ["exit", "quit", "bye"]:
            print("Bot: Thank you for using Loan Advisor Chatbot!")
            break
        
        # Convert menu selection only when no conversation state is active
        if (
            manager.pending_field is None
            and manager.emi_pending_field is None
            and not manager.awaiting_confirmation
            and not manager.awaiting_correction
            and not manager.awaiting_reset_confirmation
        ):
            user_message = menu_options.get(user_message, user_message)

        response = manager.process_message(user_message)

        print("\nBot:", response)


if __name__ == "__main__":
    main()
