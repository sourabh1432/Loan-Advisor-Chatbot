from src.emi_calculator import calculate_emi

result = calculate_emi(
    loan_amount=500000,
    annual_interest_rate=10,
    tenure_years=5
)

print("Monthly EMI:", result["monthly_emi"])
print("Total Payment:", result["total_payment"])
print("Total Interest:", result["total_interest"])
print("Tenure in Months:", result["total_months"])