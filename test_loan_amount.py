
from src.entity_extraction import extract_loan_amount

test_messages = [
    "I need a loan of 5 lakh.",
    "I need a loan of -500000.",
    "Loan amount is 10 lakh.",
    "I want 2 lakh.",
    "I need ₹25 lakh.",
    "I require 500000.",
    "I need a loan of 1 crore."
]

for message in test_messages:

    result = extract_loan_amount(message)

    print("Input:", message)
    print("Extracted amount:", result)
    print("-" * 50)
