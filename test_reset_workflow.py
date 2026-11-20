
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


def test_reset_application():
    bot = LoanConversationManager()

    # Start application
    bot.process_message("1")
    bot.process_message("2")

    assert bot.applicant.get("no_of_dependents") == 2

    # Request reset and confirm
    bot.process_message("reset")
    bot.process_message("yes")

    # Check all application values are cleared
    assert all(
        value is None for value in bot.applicant.values()
    ), "Applicant data was not cleared"

    assert bot.pending_field is None
    assert bot.awaiting_reset_confirmation is False
    assert bot.last_prediction is None


def test_reset_emi():
    bot = LoanConversationManager()

    # Start EMI calculation
    bot.process_message("calculate emi")
    bot.process_message("500000")

    assert bot.emi_details.get("loan_amount") == 500000

    # Request reset and confirm
    bot.process_message("reset")
    bot.process_message("yes")

    # Check EMI values are cleared
    assert all(
        value is None for value in bot.emi_details.values()
    ), "EMI details were not cleared"

    assert bot.emi_pending_field is None
    assert bot.awaiting_reset_confirmation is False


def test_reset_cancel():
    bot = LoanConversationManager()

    # Start application
    bot.process_message("1")
    bot.process_message("2")

    # Request reset but cancel
    bot.process_message("reset")
    bot.process_message("no")

    # Existing data must remain
    assert bot.applicant.get("no_of_dependents") == 2

    assert bot.awaiting_reset_confirmation is False


print("=" * 65)
print("       STAGE 6.6 - RESET AND RESTART TESTS")
print("=" * 65)

run_test("Reset Application Workflow", test_reset_application)
run_test("Reset EMI Workflow", test_reset_emi)
run_test("Cancel Reset and Preserve Data", test_reset_cancel)

print("\n" + "=" * 65)
print("                    TEST SUMMARY")
print("=" * 65)

print("Total tests:", passed + failed)
print("Passed:", passed)
print("Failed:", failed)

if failed == 0:
    print("\nAll reset workflow tests passed!")
else:
    print("\nSome tests failed. Check the errors above.")

print("=" * 65)




# from src.conversation_manager import LoanConversationManager

# passed = 0
# failed = 0


# def run_test(name, test_function):
#     global passed, failed

#     print(f"\nTEST: {name}")

#     try:
#         test_function()
#         passed += 1
#         print("PASS")

#     except Exception as error:
#         failed += 1
#         print("FAIL:", error)


# def test_reset_application():
#     bot = LoanConversationManager()

#     # Start application and enter dependents
#     bot.process_message("1")
#     bot.process_message("2")

#     assert bot.applicant.get("no_of_dependents") == 2

#     # Request reset and confirm
#     bot.process_message("reset")
#     bot.process_message("yes")

#     # Verify application data is cleared
#     assert all(
#         value is None for value in bot.applicant.values()
#     ), "Applicant data was not cleared"
#     assert bot.pending_field is None, "Pending field was not cleared"


# def test_reset_emi():
#     bot = LoanConversationManager()

#     # Start EMI workflow and enter loan amount
#     bot.process_message("calculate emi")
#     bot.process_message("500000")

#     assert bot.emi_details.get("loan_amount") == 500000

#     # Request reset and confirm
#     bot.process_message("reset")
#     bot.process_message("yes")

#     # Verify EMI data is cleared
#     assert bot.emi_pending_field is None, "EMI pending field was not cleared"
#     assert not bot.emi_details, "EMI details were not cleared"


# def test_reset_cancel():
#     bot = LoanConversationManager()

#     bot.process_message("1")
#     bot.process_message("2")

#     # Request reset, then cancel
#     bot.process_message("reset")
#     bot.process_message("no")

#     # Existing application data should remain
#     assert bot.applicant.get("no_of_dependents") == 2, (
#         "Application data was lost after cancelling reset"
#     )


# print("=" * 65)
# print("       STAGE 6.6 - RESET AND RESTART TESTS")
# print("=" * 65)

# run_test("Reset Application Workflow", test_reset_application)
# run_test("Reset EMI Workflow", test_reset_emi)
# run_test("Cancel Reset and Preserve Data", test_reset_cancel)

# print("\n" + "=" * 65)
# print("                    TEST SUMMARY")
# print("=" * 65)
# print("Total tests:", passed + failed)
# print("Passed:", passed)
# print("Failed:", failed)

# if failed == 0:
#     print("\nAll reset workflow tests passed!")
# else:
#     print("\nSome tests failed. Check the errors above.")

# print("=" * 65)
