
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


def test_unexpected_message_during_application():
    bot = LoanConversationManager()

    # Start application
    bot.process_message("1")

    original_field = bot.pending_field

    assert original_field == "no_of_dependents"

    # Send unrelated message
    response = bot.process_message("Tell me a joke")

    # Application should remain at the same field
    assert bot.pending_field == original_field, (
        "Application lost its pending field"
    )

    # Enter correct answer
    bot.process_message("2")

    assert bot.applicant.get("no_of_dependents") == 2, (
        "Valid answer was not saved"
    )

    assert bot.pending_field == "education", (
        "Application did not continue to education"
    )


def test_unexpected_message_during_emi():
    bot = LoanConversationManager()

    # Start EMI calculation
    bot.process_message("calculate emi")

    original_field = bot.emi_pending_field

    assert original_field == "loan_amount"

    # Send unrelated message
    response = bot.process_message("What is the weather today?")

    # EMI workflow should remain active
    assert bot.emi_pending_field == original_field, (
        "EMI workflow lost its pending field"
    )

    # Enter valid loan amount
    bot.process_message("300000")

    assert bot.emi_details.get("loan_amount") == 300000, (
        "Loan amount was not saved"
    )

    assert bot.emi_pending_field == "interest_rate", (
        "EMI workflow did not continue to interest rate"
    )


def test_random_message_during_application():
    bot = LoanConversationManager()

    # Start application
    bot.process_message("1")

    original_field = bot.pending_field

    # Send random message
    bot.process_message("xyz123 random message")

    # Pending field should remain unchanged
    assert bot.pending_field == original_field, (
        "Random message changed application state"
    )

    # Submit valid answer
    bot.process_message("3")

    assert bot.applicant.get("no_of_dependents") == 3, (
        "Valid dependent value was not saved"
    )


print("=" * 65)
print("    STAGE 6.7 - UNEXPECTED MESSAGE TESTS")
print("=" * 65)

run_test(
    "Unexpected Message During Application",
    test_unexpected_message_during_application
)

run_test(
    "Unexpected Message During EMI",
    test_unexpected_message_during_emi
)

run_test(
    "Random Message During Application",
    test_random_message_during_application
)

print("\n" + "=" * 65)
print("                    TEST SUMMARY")
print("=" * 65)

print("Total tests:", passed + failed)
print("Passed:", passed)
print("Failed:", failed)

if failed == 0:
    print("\nAll unexpected message tests passed!")
else:
    print("\nSome tests failed. Check the errors above.")

print("=" * 65)
