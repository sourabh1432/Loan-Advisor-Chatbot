
from src.conversation_manager import LoanConversationManager

bot = LoanConversationManager()

print("\n1. Starting EMI workflow")
response = bot.process_message("calculate emi")
print("Response:", response)
print("Pending field:", bot.emi_pending_field)
print("EMI details:", bot.emi_details)

print("\n2. Entering loan amount")
response = bot.process_message("300000")
print("Response:", response)
print("Pending field:", bot.emi_pending_field)
print("EMI details:", bot.emi_details)

print("\n3. Entering interest rate")
response = bot.process_message("10")
print("Response:", response)
print("Pending field:", bot.emi_pending_field)
print("EMI details:", bot.emi_details)

print("\n4. Entering loan tenure")
response = bot.process_message("5")
print("Response:", response)
print("Pending field:", bot.emi_pending_field)
print("EMI details:", bot.emi_details)

print("\n5. Final verification")
print("Loan amount:", bot.emi_details.get("loan_amount"))
print("Interest rate:", bot.emi_details.get("interest_rate"))
print("Loan tenure:", bot.emi_details.get("loan_tenure"))
print("Final response:", response)
