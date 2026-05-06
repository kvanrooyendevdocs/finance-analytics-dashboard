from pathlib import Path
import pandas as pd

RAW_DATA_PATH = Path("data/raw")
CLEANED_DATA_PATH = Path("data/cleaned")

CLEANED_DATA_PATH.mkdir(parents=True, exist_ok=True)

departments = pd.read_csv(RAW_DATA_PATH / "departments.csv")
clients = pd.read_csv(RAW_DATA_PATH / "clients.csv")
vendors = pd.read_csv(RAW_DATA_PATH / "vendors.csv")
invoices = pd.read_csv(RAW_DATA_PATH / "invoices.csv")
expenses = pd.read_csv(RAW_DATA_PATH / "expenses.csv")
budgets = pd.read_csv(RAW_DATA_PATH / "budgets.csv")

print("Raw finance data loaded successfully.")

print("Departments:", departments.shape)
print("Clients:", clients.shape)
print("Vendors:", vendors.shape)
print("Invoices:", invoices.shape)
print("Expenses:", expenses.shape)
print("Budgets:", budgets.shape)

# -----------------------------
# Basic text cleaning
# -----------------------------

departments["department_name"] = departments["department_name"].str.strip()

clients["client_name"] = clients["client_name"].str.strip()
clients["industry"] = clients["industry"].str.strip()
clients["country"] = clients["country"].str.strip()

vendors["vendor_name"] = vendors["vendor_name"].str.strip()
vendors["vendor_category"] = vendors["vendor_category"].str.strip()

invoices["invoice_status"] = invoices["invoice_status"].str.strip()
expenses["expense_category"] = expenses["expense_category"].str.strip()

# -----------------------------
# Date cleaning
# -----------------------------

invoices["invoice_date"] = pd.to_datetime(invoices["invoice_date"])
invoices["due_date"] = pd.to_datetime(invoices["due_date"])
invoices["payment_date"] = pd.to_datetime(invoices["payment_date"], errors="coerce")

expenses["expense_date"] = pd.to_datetime(expenses["expense_date"])
budgets["budget_month"] = pd.to_datetime(budgets["budget_month"])

# -----------------------------
# Money cleaning
# -----------------------------

invoices["invoice_amount"] = pd.to_numeric(invoices["invoice_amount"], errors="coerce")
expenses["expense_amount"] = pd.to_numeric(expenses["expense_amount"], errors="coerce")
budgets["budget_amount"] = pd.to_numeric(budgets["budget_amount"], errors="coerce")

invoices["invoice_amount"] = invoices["invoice_amount"].clip(lower=0)
expenses["expense_amount"] = expenses["expense_amount"].clip(lower=0)
budgets["budget_amount"] = budgets["budget_amount"].clip(lower=0)

# -----------------------------
# Create useful reporting columns
# -----------------------------

invoices["invoice_month"] = invoices["invoice_date"].dt.to_period("M").astype(str)
expenses["expense_month"] = expenses["expense_date"].dt.to_period("M").astype(str)
budgets["budget_month_name"] = budgets["budget_month"].dt.to_period("M").astype(str)

invoices["days_to_payment"] = (invoices["payment_date"] - invoices["invoice_date"]).dt.days
invoices["days_late"] = (invoices["payment_date"] - invoices["due_date"]).dt.days

invoices["is_paid"] = invoices["invoice_status"] == "Paid"
invoices["is_overdue"] = invoices["invoice_status"] == "Overdue"
invoices["is_late_payment"] = invoices["days_late"] > 0

# For unpaid or overdue invoices, days_late may be blank because there is no payment date yet.
# We keep that blank for now.

print("Finance cleaning rules applied.")

# -----------------------------
# Save cleaned data
# -----------------------------

departments.to_csv(CLEANED_DATA_PATH / "departments_cleaned.csv", index=False)
clients.to_csv(CLEANED_DATA_PATH / "clients_cleaned.csv", index=False)
vendors.to_csv(CLEANED_DATA_PATH / "vendors_cleaned.csv", index=False)
invoices.to_csv(CLEANED_DATA_PATH / "invoices_cleaned.csv", index=False)
expenses.to_csv(CLEANED_DATA_PATH / "expenses_cleaned.csv", index=False)
budgets.to_csv(CLEANED_DATA_PATH / "budgets_cleaned.csv", index=False)

print("Cleaned finance files saved successfully.")