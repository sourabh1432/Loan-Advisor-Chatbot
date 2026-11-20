from src.input_validation import validate_field

test_values = [10, 0, 100, -5, 105, "abc"]

for value in test_values:
    print(value, "->", validate_field("interest_rate", value))