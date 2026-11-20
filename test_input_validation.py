
from src.input_validation import validate_field


# -----------------------------------------
# STAGE 6.1 - INPUT VALIDATION TESTING
# -----------------------------------------

test_cases = [

    # Valid inputs
    ("no_of_dependents", 2, True),
    ("no_of_dependents", 0, True),
    ("education", "Graduate", True),
    ("education", "Not Graduate", True),
    ("self_employed", "Yes", True),
    ("self_employed", "No", True),
    ("income_annum", 600000, True),
    ("loan_amount", 500000, True),
    ("loan_term", 5, True),
    ("cibil_score", 750, True),
    ("interest_rate", 9, True),
    ("residential_assets_value", 1000000, True),
    ("commercial_assets_value", 200000, True),
    ("luxury_assets_value", 100000, True),
    ("bank_asset_value", 150000, True),

    # Invalid inputs
    ("no_of_dependents", -1, False),
    ("no_of_dependents", 21, False),
    ("education", "Postgraduate", False),
    ("self_employed", "Maybe", False),
    ("income_annum", -50000, False),
    ("loan_amount", 0, False),
    ("loan_amount", -100000, False),
    ("loan_term", 0, False),
    ("loan_term", 41, False),
    ("cibil_score", 250, False),
    ("cibil_score", 950, False),
    ("interest_rate", -5, False),
    ("interest_rate", 101, False),
    ("residential_assets_value", -1000, False),
    ("commercial_assets_value", -5000, False),
    ("luxury_assets_value", -2000, False),
    ("bank_asset_value", -3000, False),
]


# -----------------------------------------
# RUN TESTS
# -----------------------------------------

passed = 0
failed = 0

print("=" * 65)
print("       STAGE 6.1 - INPUT VALIDATION TESTING")
print("=" * 65)

for field, value, expected in test_cases:

    try:
        is_valid, message = validate_field(field, value)

        if is_valid == expected:
            passed += 1
            status = "PASS"
        else:
            failed += 1
            status = "FAIL"

        print(
            f"{status} | Field: {field:<25} "
            f"Value: {str(value):<15} "
            f"Expected: {expected} | Actual: {is_valid}"
        )

        if status == "FAIL":
            print("       Validation message:", message)

    except Exception as error:
        failed += 1
        print(
            f"ERROR | Field: {field} | "
            f"Value: {value} | Error: {error}"
        )


# -----------------------------------------
# FINAL REPORT
# -----------------------------------------

total = passed + failed

print("\n" + "=" * 65)
print("                 TEST SUMMARY")
print("=" * 65)

print("Total tests :", total)
print("Passed      :", passed)
print("Failed      :", failed)

if failed == 0:
    print("\nAll input validation tests passed!")

else:
    print("\nSome tests failed. Check the validation rules.")

print("=" * 65)
