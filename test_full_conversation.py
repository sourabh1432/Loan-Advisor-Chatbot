
from src.conversation_manager import LoanConversationManager

manager = LoanConversationManager()

# =====================================
# STEP 1: INITIAL LOAN APPLICATION
# =====================================

message = (
    "I need a personal loan of 5 lakh for 5 years. "
    "My monthly income is 60000. "
    "My CIBIL score is 750 and I have 2 dependents. "
    "Interest rate is 10%."
)

print("\nUser:", message)
response = manager.process_message(message)
print("\nBot:", response)


# =====================================
# STEP 2: COMPLETE MISSING DETAILS
# =====================================

answers = [
    "Graduate",
    "No",
    "1000000",
    "500000",
    "200000",
    "300000"
]

for answer in answers:
    print("\nUser:", answer)

    response = manager.process_message(answer)

    print("\nBot:", response)


# =====================================
# STEP 3: CORRECT CIBIL SCORE
# =====================================

correction_messages = [
    "No",
    "CIBIL score",
    "800"
]

for message in correction_messages:
    print("\nUser:", message)

    response = manager.process_message(message)

    print("\nBot:", response)


# =====================================
# STEP 4: FINAL CONFIRMATION
# =====================================

print("\nUser: Yes")

response = manager.process_message("Yes")

print("\nBot:", response)


# =====================================
# STEP 5: FINAL APPLICANT DETAILS
# =====================================

print("\nFinal Applicant Details:")
print(manager.applicant)
