from pathlib import Path
import pandas as pd
import random
from faker import Faker

fake = Faker()

random.seed(42)
Faker.seed(42)

RAW_DATA_PATH = Path("data/raw")
RAW_DATA_PATH.mkdir(parents=True, exist_ok=True)

# -----------------------------
# Create departments
# -----------------------------

departments = [
    "Sales",
    "Marketing",
    "Operations",
    "Finance",
    "Human Resources",
    "IT",
    "Customer Support",
    "Research and Development"
]

department_records = []

for department_id, department_name in enumerate(departments, start=1):
    department_records.append({
        "department_id": department_id,
        "department_name": department_name
    })

departments_df = pd.DataFrame(department_records)

departments_df.to_csv(RAW_DATA_PATH / "departments.csv", index=False)

# -----------------------------
# Create clients
# -----------------------------

NUM_CLIENTS = 50

client_records = []

industries = [
    "Banking",
    "Insurance",
    "Retail",
    "Healthcare",
    "Education",
    "Manufacturing",
    "Technology",
    "Logistics"
]

for client_id in range(1, NUM_CLIENTS + 1):
    client_records.append({
        "client_id": client_id,
        "client_name": fake.company(),
        "industry": random.choice(industries),
        "country": random.choice(["South Africa", "United Kingdom", "United States", "Germany", "Australia"])
    })

clients_df = pd.DataFrame(client_records)

clients_df.to_csv(RAW_DATA_PATH / "clients.csv", index=False)

# -----------------------------
# Create vendors
# -----------------------------

NUM_VENDORS = 40

vendor_records = []

vendor_categories = [
    "Software",
    "Office Supplies",
    "Consulting",
    "Travel",
    "Utilities",
    "Equipment",
    "Marketing Services",
    "Training"
]

for vendor_id in range(1, NUM_VENDORS + 1):
    vendor_records.append({
        "vendor_id": vendor_id,
        "vendor_name": fake.company(),
        "vendor_category": random.choice(vendor_categories)
    })

vendors_df = pd.DataFrame(vendor_records)

vendors_df.to_csv(RAW_DATA_PATH / "vendors.csv", index=False)

# -----------------------------
# Create invoices
# -----------------------------

NUM_INVOICES = 600

invoice_records = []

invoice_statuses = [
    "Paid",
    "Paid",
    "Paid",
    "Paid",
    "Unpaid",
    "Overdue"
]

for invoice_id in range(1, NUM_INVOICES + 1):
    client = clients_df.sample(1).iloc[0]

    invoice_date = fake.date_between(
        start_date="-12M",
        end_date="today"
    )

    due_days = random.choice([14, 30, 45, 60])
    due_date = invoice_date + pd.Timedelta(days=due_days)

    status = random.choice(invoice_statuses)

    if status == "Paid":
        payment_date = due_date + pd.Timedelta(days=random.randint(-10, 20))
    elif status == "Overdue":
        payment_date = None
    else:
        payment_date = None

    amount = round(random.uniform(5_000, 150_000), 2)

    invoice_records.append({
        "invoice_id": invoice_id,
        "client_id": client["client_id"],
        "invoice_date": invoice_date,
        "due_date": due_date,
        "payment_date": payment_date,
        "invoice_amount": amount,
        "invoice_status": status
    })

invoices_df = pd.DataFrame(invoice_records)

invoices_df.to_csv(RAW_DATA_PATH / "invoices.csv", index=False)

# -----------------------------
# Create expenses
# -----------------------------

NUM_EXPENSES = 900

expense_records = []

expense_categories = [
    "Salaries",
    "Software",
    "Travel",
    "Marketing",
    "Office Supplies",
    "Utilities",
    "Training",
    "Consulting",
    "Equipment"
]

for expense_id in range(1, NUM_EXPENSES + 1):
    department = departments_df.sample(1).iloc[0]
    vendor = vendors_df.sample(1).iloc[0]

    expense_date = fake.date_between(
        start_date="-12M",
        end_date="today"
    )

    category = random.choice(expense_categories)

    amount = round(random.uniform(500, 80_000), 2)

    expense_records.append({
        "expense_id": expense_id,
        "department_id": department["department_id"],
        "vendor_id": vendor["vendor_id"],
        "expense_date": expense_date,
        "expense_category": category,
        "expense_amount": amount
    })

expenses_df = pd.DataFrame(expense_records)

expenses_df.to_csv(RAW_DATA_PATH / "expenses.csv", index=False)

# -----------------------------
# Create monthly department budgets
# -----------------------------

budget_records = []
budget_id = 1

months = pd.date_range(
    start="2025-01-01",
    periods=12,
    freq="MS"
)

for _, department in departments_df.iterrows():
    for month in months:
        base_budget = random.uniform(80_000, 350_000)

        # Some departments naturally have larger budgets
        department_multiplier = {
            "Sales": 1.3,
            "Marketing": 1.2,
            "Operations": 1.4,
            "Finance": 0.9,
            "Human Resources": 0.8,
            "IT": 1.1,
            "Customer Support": 1.0,
            "Research and Development": 1.5
        }.get(department["department_name"], 1.0)

        monthly_budget = round(base_budget * department_multiplier, 2)

        budget_records.append({
            "budget_id": budget_id,
            "department_id": department["department_id"],
            "budget_month": month.date(),
            "budget_amount": monthly_budget
        })

        budget_id += 1

budgets_df = pd.DataFrame(budget_records)

budgets_df.to_csv(RAW_DATA_PATH / "budgets.csv", index=False)

print("Departments data generated.")
print("Clients data generated.")
print("Vendors data generated.")
print("Invoices data generated.")
print("Expenses data generated.")
print("Budgets data generated.")
print(budgets_df.head())
