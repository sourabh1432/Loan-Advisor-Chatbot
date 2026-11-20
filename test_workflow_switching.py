
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


# ==========================================
# TEST 1: APPLICATION -> EMI -> APPLICATION
# ==========================================

def test_application_to_emi_resume():

    bot = LoanConversationManager()

    # Start application
    bot.process_message("1")

    # Save dependents
    bot.process_message("2")

    assert bot.pending_field == "education", (
        "Application should be waiting for education"
    )

    # Request EMI
    bot.process_message("calculate emi")

    # Confirm workflow switch
    response = bot.process_message("yes")

    assert bot.emi_pending_field == "loan_amount", (
        "EMI workflow did not start"
    )

    # Complete EMI calculation
    bot.process_message("300000")
    bot.process_message("10")
    bot.process_message("5")

    # Resume previous application
    response = bot.process_message("resume previous")

    assert bot.pending_field == "education", (
        "Application did not resume at education"
    )

    assert bot.applicant.get("no_of_dependents") == 2, (
        "Previously saved dependents were lost"
    )


# ==========================================
# TEST 2: EMI -> APPLICATION -> EMI
# ==========================================

def test_emi_to_application_resume():

    bot = LoanConversationManager()

    # Start EMI
    bot.process_message("calculate emi")

    # Enter loan amount
    bot.process_message("500000")

    assert bot.emi_pending_field == "interest_rate", (
        "EMI should be waiting for interest rate"
    )

    # Request loan application
    bot.process_message("I want to apply for a personal loan")

    # Confirm switch
    bot.process_message("yes")

    assert bot.pending_field == "no_of_dependents", (
        "Loan application did not start correctly"
    )

    # Resume previous EMI
    response = bot.process_message("resume previous")

    assert bot.emi_pending_field == "interest_rate", (
        "Previous EMI did not resume at interest rate"
    )

    assert bot.emi_details.get("loan_amount") == 500000, (
        "Previously entered EMI loan amount was lost"
    )


# ==========================================
# RUN TESTS
# ==========================================

print("=" * 70)
print("       STAGE 6.5 - WORKFLOW SWITCHING TESTS")
print("=" * 70)

run_test(
    "Application -> EMI -> Resume Application",
    test_application_to_emi_resume
)

run_test(
    "EMI -> Application -> Resume EMI",
    test_emi_to_application_resume
)


# ==========================================
# FINAL SUMMARY
# ==========================================

print("\n" + "=" * 70)
print("                    TEST SUMMARY")
print("=" * 70)

print("Total tests:", passed + failed)
print("Passed:", passed)
print("Failed:", failed)

if failed == 0:
    print("\nAll workflow switching tests passed!")
else:
    print("\nSome workflow switching tests failed.")

print("=" * 70)
