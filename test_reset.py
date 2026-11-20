
from src.conversation_manager import LoanConversationManager

chatbot = LoanConversationManager()

# Add sample data
chatbot.applicant["cibil_score"] = 750
chatbot.applicant["loan_amount"] = 500000
chatbot.pending_field = "education"
chatbot.awaiting_confirmation = True

# Reset the conversation
print(chatbot.reset_conversation())

# Verify the reset
assert chatbot.applicant["cibil_score"] is None
assert chatbot.applicant["loan_amount"] is None
assert chatbot.pending_field is None
assert chatbot.awaiting_confirmation is False
assert chatbot.awaiting_correction is False

print("PASS: Conversation reset successfully.")
