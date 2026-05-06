from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


BASE_PATH = Path(__file__).resolve().parent.parent
REPORTS_PATH = BASE_PATH / "reports"


monthly_finance_kpis = pd.read_csv(REPORTS_PATH / "monthly_finance_kpis.csv")
expense_category_summary = pd.read_csv(REPORTS_PATH / "expense_category_summary.csv")
department_budget_summary = pd.read_csv(REPORTS_PATH / "department_budget_summary.csv")
client_payment_risk_summary = pd.read_csv(REPORTS_PATH / "client_payment_risk_summary.csv")


# -----------------------------
# Chart 1: Monthly profit
# -----------------------------

plt.figure(figsize=(12, 6))
plt.bar(monthly_finance_kpis["month"], monthly_finance_kpis["profit"])
plt.title("Monthly Profit")
plt.xlabel("Month")
plt.ylabel("Profit")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(REPORTS_PATH / "monthly_profit.png")
plt.close()


# -----------------------------
# Chart 2: Revenue vs expenses
# -----------------------------

plt.figure(figsize=(12, 6))
plt.plot(monthly_finance_kpis["month"], monthly_finance_kpis["total_invoiced"], marker="o", label="Revenue")
plt.plot(monthly_finance_kpis["month"], monthly_finance_kpis["total_expenses"], marker="o", label="Expenses")
plt.title("Revenue vs Expenses")
plt.xlabel("Month")
plt.ylabel("Amount")
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.savefig(REPORTS_PATH / "revenue_vs_expenses.png")
plt.close()


# -----------------------------
# Chart 3: Expense category summary
# -----------------------------

top_expense_categories = expense_category_summary.sort_values(
    "total_expenses",
    ascending=True
)

plt.figure(figsize=(12, 6))
plt.barh(top_expense_categories["expense_category"], top_expense_categories["total_expenses"])
plt.title("Expenses by Category")
plt.xlabel("Total Expenses")
plt.ylabel("Expense Category")
plt.tight_layout()
plt.savefig(REPORTS_PATH / "expenses_by_category.png")
plt.close()


# -----------------------------
# Chart 4: Department budget variance
# -----------------------------

department_budget_chart = department_budget_summary.sort_values(
    "total_variance",
    ascending=True
)

plt.figure(figsize=(12, 6))
plt.barh(department_budget_chart["department_name"], department_budget_chart["total_variance"])
plt.title("Department Budget Variance")
plt.xlabel("Variance")
plt.ylabel("Department")
plt.tight_layout()
plt.savefig(REPORTS_PATH / "department_budget_variance.png")
plt.close()


# -----------------------------
# Chart 5: Outstanding amount by month
# -----------------------------

plt.figure(figsize=(12, 6))
plt.bar(monthly_finance_kpis["month"], monthly_finance_kpis["outstanding_amount"])
plt.title("Outstanding Amount by Month")
plt.xlabel("Month")
plt.ylabel("Outstanding Amount")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(REPORTS_PATH / "outstanding_amount_by_month.png")
plt.close()


# -----------------------------
# Chart 6: Top risky clients
# -----------------------------

top_risky_clients = client_payment_risk_summary.head(10).sort_values(
    "overdue_invoice_rate",
    ascending=True
)

plt.figure(figsize=(12, 6))
plt.barh(top_risky_clients["client_name"], top_risky_clients["overdue_invoice_rate"])
plt.title("Top 10 Risky Clients by Overdue Invoice Rate")
plt.xlabel("Overdue Invoice Rate (%)")
plt.ylabel("Client")
plt.tight_layout()
plt.savefig(REPORTS_PATH / "top_risky_clients.png")
plt.close()


print("Finance chart images created successfully.")