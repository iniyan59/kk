# Banking Loan Approval System
# File: LoanProcessingSystem.py

print("===== BANKING LOAN APPROVAL SYSTEM =====")

# Sample Input
customer_id = "C101"
age = 30
salary = 60000
existing_loan = 100000
credit_score = 780
employment_type = "Salaried"
requested_loan = 800000
tenure = 5

print("\n===== CUSTOMER DETAILS =====")
print("Customer ID         :", customer_id)
print("Age                 :", age)
print("Monthly Salary      : ₹", salary)
print("Existing Loan       : ₹", existing_loan)
print("Credit Score        :", credit_score)
print("Employment Type     :", employment_type)
print("Requested Loan      : ₹", requested_loan)
print("Loan Tenure         :", tenure, "years")


# 1. Debt-to-Income Ratio
monthly_existing_emi = existing_loan / 60
dti = (monthly_existing_emi / salary) * 100


# 2. Eligible Loan Amount
if credit_score >= 750:
    eligible_loan = salary * 20
elif credit_score >= 650:
    eligible_loan = salary * 15
else:
    eligible_loan = salary * 10


# 3. Interest Rate
if credit_score >= 750:
    interest_rate = 8.5
elif credit_score >= 650:
    interest_rate = 10.0
else:
    interest_rate = 12.0


# 4. EMI Calculation
monthly_rate = interest_rate / (12 * 100)
months = tenure * 12

emi = (requested_loan * monthly_rate * (1 + monthly_rate) ** months) / \
      ((1 + monthly_rate) ** months - 1)


# 5. Loan Approval Conditions
if (age >= 21 and
    age <= 60 and
    credit_score >= 650 and
    dti <= 50 and
    requested_loan <= eligible_loan):

    status = "APPROVED"

else:
    status = "REJECTED"


# 6. Final Result
print("\n===== LOAN PROCESSING RESULT =====")

print("Debt-to-Income Ratio : {:.2f}%".format(dti))
print("Eligible Loan Amount : ₹{:.2f}".format(eligible_loan))
print("Interest Rate        : {:.2f}%".format(interest_rate))
print("Monthly EMI          : ₹{:.2f}".format(emi))
print("Loan Status          :", status)

print("\n===== PROCESS COMPLETED =====")