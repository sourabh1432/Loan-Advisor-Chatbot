from src.conversation_manager import LoanConversationManager
from src.emi_calculator import calculate_emi
from src.input_validation import validate_field


# 1. Test EMI calculation
print("\n--- EMI Calculation Test ---")

result = calculate_emi(
    loan_amount=500000,
    annual_interest_rate=10,
    tenure_years=5
)

print("Monthly EMI:", result["monthly_emi"])
print("Total Interest:", result["total_interest"])
print("Total Payment:", result["total_payment"])


# 2. Test interest rate validation
print("\n--- Interest Rate Validation Test ---")

test_rates = [10, 0, 100, -5, 105, "abc"]

for rate in test_rates:
    print(rate, "->", validate_field("interest_rate", rate))


# 3. Test conversation manager
print("\n--- Conversation Manager Test ---")

chatbot = LoanConversationManager()

print("Initial interest rate:",
      chatbot.applicant["interest_rate"])

print("Interest rate question:",
      chatbot.get_question("interest_rate"))

print("Saving interest rate 10:",
      chatbot.save_answer("interest_rate", "10%"))

print("Saved interest rate:",
      chatbot.applicant["interest_rate"])