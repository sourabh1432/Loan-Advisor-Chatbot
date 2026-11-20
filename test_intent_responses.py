
from src.conversation_manager import LoanConversationManager


def test_intent_responses():

    manager = LoanConversationManager()

    test_messages = [

        ("Hello", "greeting"),

        ("Tell me about personal loans", "personal_loan"),

        ("What is a home loan?", "home_loan"),

        ("Explain car loan", "car_loan"),

        ("What is a business loan?", "business_loan"),

        ("Tell me about education loans", "education_loan"),

        ("What is CIBIL score?", "credit_score"),

        ("What types of loans are available?", "loan_types"),

        ("What documents are required for a loan?", "required_documents"),

        ("What is loan processing fee?", "processing_fee"),

        ("What is the interest rate?", "interest_rate"),

        ("What is loan tenure?", "loan_tenure"),

        ("How much loan can I get?", "loan_amount"),

        ("What income is required for a loan?", "income_requirement"),

        ("Check my loan eligibility", "loan_eligibility"),

        ("I want to apply for a loan", "loan_application"),

        ("How can I check my application status?", "application_status"),

        ("What is a co applicant?", "coapplicant"),

        ("I already have an existing loan", "existing_loan"),

        ("Can I make a loan prepayment?", "prepayment"),

        ("I want to close my loan early", "foreclosure"),

        ("Why was my loan rejected?", "loan_rejection"),

        ("What is a loan top up?", "loan_top_up"),

        ("Calculate my EMI", "emi_calculation"),

        ("Thank you", "goodbye"),

    ]

    workflow_intents = {
        "loan_eligibility",
        "emi_calculation",
        "loan_application"
    }

    passed = 0
    failed = 0

    print("\n========== INTENT RESPONSE TESTING ==========\n")

    for message, expected_intent in test_messages:

        detected_intent = manager.detect_intent(message)

        response = manager.route_intent(detected_intent)

        print("User Message:", message)
        print("Expected Intent:", expected_intent)
        print("Detected Intent:", detected_intent)

        if detected_intent == expected_intent:

            if expected_intent in workflow_intents:

                if response is None:
                    print("Result: PASS - Workflow handled separately")
                    passed += 1
                else:
                    print("Result: FAIL - Workflow was intercepted")
                    failed += 1

            elif response is not None:

                print("Result: PASS - Response generated")
                passed += 1

            else:

                print("Result: FAIL - No response generated")
                failed += 1

        else:

            print("Result: FAIL - Intent mismatch")
            failed += 1

        print("-" * 55)

    print("\n========== FINAL TEST SUMMARY ==========")
    print("Total Tests:", len(test_messages))
    print("Passed:", passed)
    print("Failed:", failed)

    if failed == 0:
        print("\nAll intent response tests passed!")
    else:
        print("\nSome tests failed. Check the detected intents.")
    

if __name__ == "__main__":
    test_intent_responses()
