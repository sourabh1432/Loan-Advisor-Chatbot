
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


def test_invalid_dependents_recovery():
    bot = LoanConversationManager()

    # Start application
    bot.process_message("1")

    assert bot.pending_field == "no_of_dependents"

    # Enter invalid input
    bot.process_message("two")

    # Pending field should remain unchanged
    assert bot.pending_field == "no_of_dependents", (
        "Chatbot moved forward after invalid dependents"
    )

    # Enter valid input
    bot.process_message("2")

    assert bot.applicant.get("no_of_dependents") == 2
    assert bot.pending_field == "education", (
        "Chatbot did not move to education after valid input"
    )


def test_invalid_emi_amount_recovery():
    bot = LoanConversationManager()

    # Start EMI calculation
    bot.process_message("calculate emi")

    assert bot.emi_pending_field == "loan_amount"

    # Enter invalid loan amount
    bot.process_message("abc")

    assert bot.emi_pending_field == "loan_amount", (
        "EMI workflow moved forward after invalid amount"
    )

    # Enter valid loan amount
    bot.process_message("300000")

    assert bot.emi_details.get("loan_amount") == 300000
    assert bot.emi_pending_field == "interest_rate", (
        "EMI workflow did not move to interest rate"
    )


def test_invalid_interest_rate_recovery():
    bot = LoanConversationManager()

    # Start EMI calculation
    bot.process_message("calculate emi")

    # Enter valid loan amount
    bot.process_message("300000")

    assert bot.emi_pending_field == "interest_rate"

    # Enter invalid interest rate
    bot.process_message("abc")

    assert bot.emi_pending_field == "interest_rate", (
        "EMI workflow moved forward after invalid interest rate"
    )

    # Enter valid interest rate
    bot.process_message("10")

    assert bot.emi_details.get("interest_rate") == 10
    assert bot.emi_pending_field == "loan_tenure", (
        "EMI workflow did not move to loan tenure"
    )


print("=" * 65)
print("   STAGE 6.8 - INPUT ERROR RECOVERY INTEGRATION TESTS")
print("=" * 65)

run_test(
    "Invalid Dependents -> Valid Dependents",
    test_invalid_dependents_recovery
)

run_test(
    "Invalid EMI Amount -> Valid Amount",
    test_invalid_emi_amount_recovery
)

run_test(
    "Invalid Interest Rate -> Valid Rate",
    test_invalid_interest_rate_recovery
)

print("\n" + "=" * 65)
print("                    TEST SUMMARY")
print("=" * 65)

print("Total tests:", passed + failed)
print("Passed:", passed)
print("Failed:", failed)

if failed == 0:
    print("\nAll input recovery integration tests passed!")
else:
    print("\nSome tests failed. Check the errors above.")

print("=" * 65)
