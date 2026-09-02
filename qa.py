# Loan Processing QA Program
# File: LoanProcessingQA.py

import math


# ==========================================
# LOAN PROCESSING FUNCTION
# ==========================================

def process_loan(age, salary, existing_loan, credit_score,
                 employment_type, requested_loan, tenure):

    # Invalid input handling
    if age < 0:
        raise ValueError("Age cannot be negative")

    if salary <= 0:
        raise ValueError("Salary must be greater than zero")

    if existing_loan < 0:
        raise ValueError("Existing loan cannot be negative")

    if credit_score < 0 or credit_score > 900:
        raise ValueError("Invalid credit score")

    if requested_loan <= 0:
        raise ValueError("Requested loan must be greater than zero")

    if tenure <= 0:
        raise ValueError("Loan tenure must be greater than zero")

    # Debt-to-Income Ratio
    monthly_existing_emi = existing_loan / 60
    dti = (monthly_existing_emi / salary) * 100

    # Eligible Loan Amount
    if credit_score >= 750:
        eligible_loan = salary * 20
    elif credit_score >= 650:
        eligible_loan = salary * 15
    else:
        eligible_loan = salary * 10

    # Employment category adjustment
    if employment_type.lower() == "salaried":
        eligible_loan = eligible_loan

    elif employment_type.lower() == "self-employed":
        eligible_loan = eligible_loan * 0.90

    elif employment_type.lower() == "business":
        eligible_loan = eligible_loan * 0.85

    else:
        raise ValueError("Invalid employment category")

    # Interest rate
    if credit_score >= 750:
        interest_rate = 8.5
    elif credit_score >= 650:
        interest_rate = 10.0
    else:
        interest_rate = 12.0

    # EMI Calculation
    monthly_rate = interest_rate / (12 * 100)
    months = tenure * 12

    emi = (
        requested_loan * monthly_rate *
        (1 + monthly_rate) ** months
    ) / (
        (1 + monthly_rate) ** months - 1
    )

    # Approval conditions
    approved = True

    if age < 21 or age > 60:
        approved = False

    if credit_score < 650:
        approved = False

    if dti > 50:
        approved = False

    if requested_loan > eligible_loan:
        approved = False

    return {
        "dti": dti,
        "eligible_loan": eligible_loan,
        "interest_rate": interest_rate,
        "emi": emi,
        "status": "APPROVED" if approved else "REJECTED"
    }


# ==========================================
# QA TESTING
# ==========================================

passed = 0
failed = 0


def run_test(test_name, condition):
    global passed, failed

    if condition:
        print("PASS:", test_name)
        passed += 1
    else:
        print("FAIL:", test_name)
        failed += 1


print("==========================================")
print("       LOAN PROCESSING QA TESTING")
print("==========================================\n")


# ==========================================
# 1. MINIMUM AGE TEST
# ==========================================

try:
    result = process_loan(
        21, 60000, 100000, 750,
        "Salaried", 500000, 5
    )

    run_test(
        "Minimum Age (21)",
        result["status"] == "APPROVED"
    )

except Exception as e:
    print("FAIL: Minimum Age Test -", e)
    failed += 1


# ==========================================
# 2. MAXIMUM AGE TEST
# ==========================================

try:
    result = process_loan(
        60, 60000, 100000, 750,
        "Salaried", 500000, 5
    )

    run_test(
        "Maximum Age (60)",
        result["status"] == "APPROVED"
    )

except Exception as e:
    print("FAIL: Maximum Age Test -", e)
    failed += 1


# ==========================================
# 3. INVALID AGE TEST
# ==========================================

try:
    result = process_loan(
        20, 60000, 100000, 750,
        "Salaried", 500000, 5
    )

    run_test(
        "Invalid Age (20)",
        result["status"] == "REJECTED"
    )

except Exception as e:
    print("FAIL: Invalid Age Test -", e)
    failed += 1


# ==========================================
# 4. INVALID SALARY TEST
# ==========================================

try:
    process_loan(
        30, 0, 100000, 750,
        "Salaried", 500000, 5
    )

    print("FAIL: Invalid Salary")
    failed += 1

except ValueError:
    print("PASS: Invalid Salary")
    passed += 1


# ==========================================
# 5. POOR CREDIT SCORE TEST
# ==========================================

try:
    result = process_loan(
        30, 60000, 100000, 500,
        "Salaried", 500000, 5
    )

    run_test(
        "Poor Credit Score",
        result["status"] == "REJECTED"
    )

except Exception as e:
    print("FAIL: Poor Credit Score -", e)
    failed += 1


# ==========================================
# 6. EXISTING LOAN EXCEEDING THRESHOLD
# ==========================================

try:
    result = process_loan(
        30, 30000, 2000000, 750,
        "Salaried", 500000, 5
    )

    run_test(
        "Existing Loan Exceeding Threshold",
        result["dti"] > 50
    )

except Exception as e:
    print("FAIL: Existing Loan Test -", e)
    failed += 1


# ==========================================
# 7. HIGH DTI TEST
# ==========================================

try:
    result = process_loan(
        30, 30000, 1000000, 750,
        "Salaried", 500000, 5
    )

    run_test(
        "High Debt-to-Income Ratio",
        result["dti"] > 50 and result["status"] == "REJECTED"
    )

except Exception as e:
    print("FAIL: High DTI Test -", e)
    failed += 1


# ==========================================
# 8. SALARIED EMPLOYMENT TEST
# ==========================================

try:
    result = process_loan(
        30, 60000, 100000, 750,
        "Salaried", 500000, 5
    )

    run_test(
        "Salaried Employment",
        result["status"] == "APPROVED"
    )

except Exception as e:
    print("FAIL: Salaried Test -", e)
    failed += 1


# ==========================================
# 9. SELF-EMPLOYED TEST
# ==========================================

try:
    result = process_loan(
        30, 60000, 100000, 750,
        "Self-Employed", 500000, 5
    )

    run_test(
        "Self-Employed Category",
        result["eligible_loan"] == 1080000
    )

except Exception as e:
    print("FAIL: Self-Employed Test -", e)
    failed += 1


# ==========================================
# 10. BUSINESS EMPLOYMENT TEST
# ==========================================

try:
    result = process_loan(
        30, 60000, 100000, 750,
        "Business", 500000, 5
    )

    run_test(
        "Business Employment Category",
        result["eligible_loan"] == 1020000
    )

except Exception as e:
    print("FAIL: Business Test -", e)
    failed += 1


# ==========================================
# 11. BOUNDARY LOAN AMOUNT TEST
# ==========================================

try:
    # Credit score 750 and salary 60000
    # Eligible loan = 60000 * 20 = 1200000

    result = process_loan(
        30, 60000, 100000, 750,
        "Salaried", 1200000, 5
    )

    run_test(
        "Boundary Loan Amount",
        result["status"] == "APPROVED"
    )

except Exception as e:
    print("FAIL: Boundary Loan Test -", e)
    failed += 1


# ==========================================
# 12. EMI CALCULATION ACCURACY TEST
# ==========================================

try:
    result = process_loan(
        30, 60000, 100000, 750,
        "Salaried", 800000, 5
    )

    # Expected EMI calculated independently
    rate = 8.5 / (12 * 100)
    months = 5 * 12

    expected_emi = (
        800000 * rate * (1 + rate) ** months
    ) / (
        (1 + rate) ** months - 1
    )

    run_test(
        "EMI Calculation Accuracy",
        math.isclose(
            result["emi"],
            expected_emi,
            rel_tol=1e-9
        )
    )

except Exception as e:
    print("FAIL: EMI Accuracy Test -", e)
    failed += 1


# ==========================================
# 13. INVALID INPUT TEST
# ==========================================

try:
    process_loan(
        30, -50000, 100000, 750,
        "Salaried", 500000, 5
    )

    print("FAIL: Negative Salary Input")
    failed += 1

except ValueError:
    print("PASS: Negative Salary Input")
    passed += 1


# ==========================================
# 14. INVALID EMPLOYMENT CATEGORY
# ==========================================

try:
    process_loan(
        30, 60000, 100000, 750,
        "Student", 500000, 5
    )

    print("FAIL: Invalid Employment Category")
    failed += 1

except ValueError:
    print("PASS: Invalid Employment Category")
    passed += 1


# ==========================================
# 15. EXCEPTION HANDLING TEST
# ==========================================

try:
    process_loan(
        30, 60000, 100000, 950,
        "Salaried", 500000, 5
    )

    print("FAIL: Exception Handling")
    failed += 1

except ValueError:
    print("PASS: Exception Handling")
    passed += 1


# ==========================================
# FINAL TEST REPORT
# ==========================================

print("\n==========================================")
print("             QA TEST SUMMARY")
print("==========================================")

print("Total Tests Passed :", passed)
print("Total Tests Failed :", failed)

if failed == 0:
    print("\nALL TEST CASES PASSED")
else:
    print("\nSOME TEST CASES FAILED")

print("==========================================")