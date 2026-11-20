def calculate_emi(loan_amount, annual_interest_rate, tenure_years):
    """Calculate estimated monthly EMI."""

    if loan_amount <= 0:
        raise ValueError("Loan amount must be greater than zero.")

    if annual_interest_rate < 0:
        raise ValueError("Interest rate cannot be negative.")

    if tenure_years <= 0:
        raise ValueError("Tenure must be greater than zero.")

    monthly_rate = annual_interest_rate / (12 * 100)
    total_months = int(tenure_years * 12)

    if monthly_rate == 0:
        emi = loan_amount / total_months
    else:
        emi = (
            loan_amount
            * monthly_rate
            * (1 + monthly_rate) ** total_months
            / ((1 + monthly_rate) ** total_months - 1)
        )

    total_payment = emi * total_months
    total_interest = total_payment - loan_amount

    return {
        "monthly_emi": round(emi, 2),
        "total_payment": round(total_payment, 2),
        "total_interest": round(total_interest, 2),
        "total_months": total_months
    }