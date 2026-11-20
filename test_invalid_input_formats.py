
from src.input_validation import validate_field

# Stage 6.2 - Invalid Input Format Testing

test_cases = [
    # Invalid numeric formats
    ("no_of_dependents", "two", False),
    ("income_annum", "abc", False),
    ("loan_amount", "five lakh", False),
    ("loan_term", "five years", False),
    ("cibil_score", "seven hundred", False),
    ("interest_rate", "ten percent", False),

    # Empty values
    ("no_of_dependents", "", False),
    ("income_annum", "", False),
    ("loan_amount", "", False),
    ("cibil_score", "", False),
    ("education", "", False),
    ("self_employed", "", False),

    # Invalid asset formats
    ("residential_assets_value", "unknown", False),
    ("commercial_assets_value", "abc", False),
    ("luxury_assets_value", "not sure", False),
    ("bank_asset_value", "none", False),
]

passed = 0
failed = 0

print("=" * 65)
print("       STAGE 6.2 - INVALID INPUT FORMAT TESTING")
print("=" * 65)

for field, value, expected in test_cases:

    try:
        is_valid, message = validate_field(field, value)

        if is_valid == expected:
            passed += 1
            print(f"PASS | {field:<28} | Value: {value!r}")
        else:
            failed += 1
            print(f"FAIL | {field:<28} | Value: {value!r}")
            print(f"     Expected: {expected}, Actual: {is_valid}")
            print(f"     Message: {message}")

    except Exception as error:
        failed += 1
        print(f"ERROR | {field:<27} | Value: {value!r}")
        print(f"      Exception: {error}")

print("\n" + "=" * 65)
print("                 TEST SUMMARY")
print("=" * 65)

print("Total tests :", len(test_cases))
print("Passed      :", passed)
print("Failed      :", failed)

if failed == 0:
    print("\nAll invalid-format tests passed!")
else:
    print("\nSome tests need attention.")

print("=" * 65)
