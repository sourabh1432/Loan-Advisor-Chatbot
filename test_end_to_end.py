
from src.conversation_manager import LoanConversationManager

passed = 0
failed = 0


def run_test(name, test_function):
    global passed, failed

    print(f"\nTEST: {name}")

    try:
        test_function()
        passed += 1
        print("PASS")

    except Exception as error:
        failed += 1
        print("FAIL:", error)


def test_complete_loan_application():
    bot = LoanConversationManager()

    # Start application
    bot.process_message("1")

    # Provide applicant information
    answers = [
        "2",          # Dependents
        "Graduate",   # Education
        "No",         # Self employed
        "600000",     # Annual income
        "500000",     # Loan amount
        "5",          # Loan tenure
        "750",        # CIBIL score
        "1000000",    # Residential assets
        "200000",     # Commercial assets
        "100000",     # Luxury assets
        "150000",     # Bank assets
        "7"           # Interest rate
    ]

    for answer in answers:
        bot.process_message(answer)

    # Verify collected information
    expected_values = {
        "no_of_dependents": 2,
        "education": "Graduate",
        "self_employed": "No",
        "income_annum": 600000,
        "loan_amount": 500000,
        "loan_term": 5,
        "cibil_score": 750,
        "residential_assets_value": 1000000,
        "commercial_assets_value": 200000,
        "luxury_assets_value": 100000,
        "bank_asset_value": 150000,
        "interest_rate": 7
    }

    for field, expected in expected_values.items():
        actual = bot.applicant.get(field)

        assert actual == expected, (
            f"{field}: expected {expected}, got {actual}"
        )



def test_complete_emi_calculation():
    bot = LoanConversationManager()

    # Start EMI calculation
    bot.process_message("calculate emi")

    assert bot.emi_pending_field == "loan_amount"

    # Enter loan amount
    bot.process_message("300000")

    assert bot.emi_pending_field == "interest_rate"

    # Enter interest rate
    bot.process_message("10")

    assert bot.emi_pending_field == "loan_tenure"

    # Enter loan tenure and capture final response
    response = bot.process_message("5")

    # Verify calculation response
    assert response is not None
    assert "6,374.11" in response, (
        "Expected EMI amount was not found"
    )

    assert "82,446.80" in response, (
        "Expected total interest was not found"
    )

    # Verify workflow completed
    assert bot.emi_pending_field is None, (
        "EMI workflow did not finish"
    )

    # EMI details should be reset after successful calculation
    assert all(
        value is None for value in bot.emi_details.values()
    ), "EMI details were not reset after calculation"



def test_faq_and_intent_detection():
    bot = LoanConversationManager()

    # Check intent detection
    assert bot.detect_intent("Hello") == "greeting"

    assert bot.detect_intent(
        "I want a personal loan"
    ) == "personal_loan"

    assert bot.detect_intent(
        "What documents are required?"
    ) == "required_documents"


print("=" * 70)
print("          STAGE 6.9 - END-TO-END CHATBOT TESTS")
print("=" * 70)

run_test(
    "Complete Loan Application Data Collection",
    test_complete_loan_application
)

run_test(
    "Complete EMI Calculation",
    test_complete_emi_calculation
)

run_test(
    "FAQ and Intent Detection",
    test_faq_and_intent_detection
)

print("\n" + "=" * 70)
print("                    TEST SUMMARY")
print("=" * 70)

print("Total tests:", passed + failed)
print("Passed:", passed)
print("Failed:", failed)

if failed == 0:
    print("\nAll end-to-end tests passed!")
else:
    print("\nSome tests failed. Check the errors above.")

print("=" * 70)
