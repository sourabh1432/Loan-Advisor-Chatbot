
from src.input_validation import validate_field

# ==========================================
# STAGE 6.3 - CONVERSATION RECOVERY TESTING
# ==========================================

test_cases = [
    {
        "field": "no_of_dependents",
        "invalid": "two",
        "valid": 2,
        "description": "Dependents: text to valid integer"
    },
    {
        "field": "education",
        "invalid": "Postgraduate",
        "valid": "Graduate",
        "description": "Education: invalid option to valid option"
    },
    {
        "field": "self_employed",
        "invalid": "Maybe",
        "valid": "No",
        "description": "Employment: invalid option to valid option"
    },
    {
        "field": "income_annum",
        "invalid": "abc",
        "valid": 600000,
        "description": "Income: text to valid number"
    },
    {
        "field": "loan_amount",
        "invalid": -500000,
        "valid": 500000,
        "description": "Loan amount: negative to valid amount"
    },
    {
        "field": "loan_term",
        "invalid": 0,
        "valid": 5,
        "description": "Tenure: zero to valid years"
    },
    {
        "field": "cibil_score",
        "invalid": 950,
        "valid": 750,
        "description": "CIBIL: out-of-range to valid score"
    },
    {
        "field": "interest_rate",
        "invalid": 101,
        "valid": 9,
        "description": "Interest rate: out-of-range to valid rate"
    },
    {
        "field": "residential_assets_value",
        "invalid": -1000,
        "valid": 1000000,
        "description": "Residential assets: negative to valid amount"
    }
]

passed = 0
failed = 0

print("=" * 75)
print("          STAGE 6.3 - CONVERSATION RECOVERY TESTING")
print("=" * 75)

for case in test_cases:

    field = case["field"]
    invalid_value = case["invalid"]
    valid_value = case["valid"]

    try:
        # Step 1: Check invalid input
        invalid_result = validate_field(field, invalid_value)

        # Step 2: Check valid input
        valid_result = validate_field(field, valid_value)

        invalid_rejected = invalid_result[0] is False
        valid_accepted = valid_result[0] is True

        if invalid_rejected and valid_accepted:
            passed += 1
            print(f"PASS | {case['description']}")
        else:
            failed += 1
            print(f"FAIL | {case['description']}")

            print("      Invalid result:", invalid_result)
            print("      Valid result:", valid_result)

    except Exception as error:
        failed += 1
        print(f"ERROR | {case['description']}")
        print("       ", error)


print("\n" + "=" * 75)
print("                    TEST SUMMARY")
print("=" * 75)

print("Total tests :", passed + failed)
print("Passed      :", passed)
print("Failed      :", failed)

if failed == 0:
    print("\nAll recovery validation tests passed!")
else:
    print("\nSome recovery validation tests failed.")

print("=" * 75)
