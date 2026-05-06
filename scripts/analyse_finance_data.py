from pathlib import Path
import pandas as pd

CLEANED_DATA_PATH = Path("data/cleaned")
REPORTS_PATH = Path("reports")

REPORTS_PATH.mkdir(parents=True, exist_ok=True)

departments = pd.read_csv(CLEANED_DATA_PATH / "departments_cleaned.csv")
clients = pd.read_csv(CLEANED_DATA_PATH / "clients_cleaned.csv")
vendors = pd.read_csv(CLEANED_DATA_PATH / "vendors_cleaned.csv")
invoices = pd.read_csv(CLEANED_DATA_PATH / "invoices_cleaned.csv")
expenses = pd.read_csv(CLEANED_DATA_PATH / "expenses_cleaned.csv")
budgets = pd.read_csv(CLEANED_DATA_PATH / "budgets_cleaned.csv")

print("Cleaned finance data loaded successfully.")

print("Invoices:", invoices.shape)
print("Expenses:", expenses.shape)
print("Budgets:", budgets.shape)

# -----------------------------
# Monthly revenue summary
# -----------------------------

monthly_revenue = (
    invoices
    .groupby("invoice_month")
    .agg(
        total_invoiced=("invoice_amount", "sum"),
        number_of_invoices=("invoice_id", "count"),
        paid_invoices=("is_paid", "sum"),
        overdue_invoices=("is_overdue", "sum")
    )
    .reset_index()
)

monthly_revenue["total_invoiced"] = monthly_revenue["total_invoiced"].round(2)

monthly_revenue = monthly_revenue.sort_values("invoice_month")

monthly_revenue.to_csv(REPORTS_PATH / "monthly_revenue.csv", index=False)

print()
print("Monthly revenue summary:")
print(monthly_revenue.head())

print()
print("Monthly revenue report saved to reports/monthly_revenue.csv")

# -----------------------------
# Monthly expense summary
# -----------------------------

monthly_expenses = (
    expenses
    .groupby("expense_month")
    .agg(
        total_expenses=("expense_amount", "sum"),
        number_of_expenses=("expense_id", "count")
    )
    .reset_index()
)

monthly_expenses["total_expenses"] = monthly_expenses["total_expenses"].round(2)

monthly_expenses = monthly_expenses.sort_values("expense_month")

monthly_expenses.to_csv(REPORTS_PATH / "monthly_expenses.csv", index=False)

print()
print("Monthly expense summary:")
print(monthly_expenses.head())

print()
print("Monthly expense report saved to reports/monthly_expenses.csv")

# -----------------------------
# Monthly profit summary
# -----------------------------

monthly_profit = monthly_revenue.merge(
    monthly_expenses,
    left_on="invoice_month",
    right_on="expense_month",
    how="outer"
)

monthly_profit["month"] = monthly_profit["invoice_month"].fillna(
    monthly_profit["expense_month"]
)

monthly_profit["total_invoiced"] = monthly_profit["total_invoiced"].fillna(0)
monthly_profit["total_expenses"] = monthly_profit["total_expenses"].fillna(0)

monthly_profit["profit"] = (
    monthly_profit["total_invoiced"] - monthly_profit["total_expenses"]
).round(2)

monthly_profit["profit_margin"] = (
    monthly_profit["profit"] / monthly_profit["total_invoiced"]
).replace([float("inf"), -float("inf")], 0).fillna(0)

monthly_profit["profit_margin"] = (monthly_profit["profit_margin"] * 100).round(1)

monthly_profit = monthly_profit[
    [
        "month",
        "total_invoiced",
        "total_expenses",
        "profit",
        "profit_margin",
        "number_of_invoices",
        "number_of_expenses",
        "paid_invoices",
        "overdue_invoices"
    ]
]

monthly_profit = monthly_profit.sort_values("month")

monthly_profit.to_csv(REPORTS_PATH / "monthly_profit.csv", index=False)

print()
print("Monthly profit summary:")
print(monthly_profit.head())

print()
print("Monthly profit report saved to reports/monthly_profit.csv")

# -----------------------------
# Expense category summary
# -----------------------------

expense_category_summary = (
    expenses
    .groupby("expense_category")
    .agg(
        total_expenses=("expense_amount", "sum"),
        number_of_expenses=("expense_id", "count"),
        average_expense=("expense_amount", "mean")
    )
    .reset_index()
)

expense_category_summary["total_expenses"] = expense_category_summary["total_expenses"].round(2)
expense_category_summary["average_expense"] = expense_category_summary["average_expense"].round(2)

expense_category_summary = expense_category_summary.sort_values(
    "total_expenses",
    ascending=False
)

expense_category_summary.to_csv(
    REPORTS_PATH / "expense_category_summary.csv",
    index=False
)

print()
print("Expense category summary:")
print(expense_category_summary)

print()
print("Expense category report saved to reports/expense_category_summary.csv")

# -----------------------------
# Client revenue summary
# -----------------------------

client_revenue_summary = invoices.merge(
    clients,
    on="client_id",
    how="left"
)

client_revenue_summary = (
    client_revenue_summary
    .groupby(["client_id", "client_name", "industry", "country"])
    .agg(
        total_invoiced=("invoice_amount", "sum"),
        number_of_invoices=("invoice_id", "count"),
        paid_invoices=("is_paid", "sum"),
        overdue_invoices=("is_overdue", "sum")
    )
    .reset_index()
)

client_revenue_summary["total_invoiced"] = client_revenue_summary["total_invoiced"].round(2)

client_revenue_summary = client_revenue_summary.sort_values(
    "total_invoiced",
    ascending=False
)

client_revenue_summary.to_csv(
    REPORTS_PATH / "client_revenue_summary.csv",
    index=False
)

print()
print("Client revenue summary:")
print(client_revenue_summary.head(10))

print()
print("Client revenue report saved to reports/client_revenue_summary.csv")

# -----------------------------
# Vendor spend summary
# -----------------------------

vendor_spend_summary = expenses.merge(
    vendors,
    on="vendor_id",
    how="left"
)

vendor_spend_summary = (
    vendor_spend_summary
    .groupby(["vendor_id", "vendor_name", "vendor_category"])
    .agg(
        total_spend=("expense_amount", "sum"),
        number_of_expenses=("expense_id", "count"),
        average_expense=("expense_amount", "mean")
    )
    .reset_index()
)

vendor_spend_summary["total_spend"] = vendor_spend_summary["total_spend"].round(2)
vendor_spend_summary["average_expense"] = vendor_spend_summary["average_expense"].round(2)

vendor_spend_summary = vendor_spend_summary.sort_values(
    "total_spend",
    ascending=False
)

vendor_spend_summary.to_csv(
    REPORTS_PATH / "vendor_spend_summary.csv",
    index=False
)

print()
print("Vendor spend summary:")
print(vendor_spend_summary.head(10))

print()
print("Vendor spend report saved to reports/vendor_spend_summary.csv")
# -----------------------------
# Budget vs actual summary
# -----------------------------

# -----------------------------
# Budget vs actual summary
# -----------------------------

expenses_with_departments = expenses.merge(
    departments,
    on="department_id",
    how="left"
)

department_monthly_expenses = (
    expenses_with_departments
    .groupby(["department_id", "expense_month"])
    .agg(
        actual_spend=("expense_amount", "sum"),
        number_of_expenses=("expense_id", "count")
    )
    .reset_index()
)

budget_vs_actual = budgets.merge(
    department_monthly_expenses,
    left_on=["department_id", "budget_month_name"],
    right_on=["department_id", "expense_month"],
    how="left"
)

budget_vs_actual = budget_vs_actual.merge(
    departments,
    on="department_id",
    how="left"
)

budget_vs_actual["actual_spend"] = budget_vs_actual["actual_spend"].fillna(0)
budget_vs_actual["number_of_expenses"] = budget_vs_actual["number_of_expenses"].fillna(0)

budget_vs_actual["variance"] = (
    budget_vs_actual["budget_amount"] - budget_vs_actual["actual_spend"]
).round(2)

budget_vs_actual["variance_percentage"] = (
    budget_vs_actual["variance"] / budget_vs_actual["budget_amount"] * 100
).round(1)

budget_vs_actual["budget_status"] = budget_vs_actual["variance"].apply(
    lambda value: "Over Budget" if value < 0 else "Under Budget"
)

budget_vs_actual = budget_vs_actual[
    [
        "department_id",
        "department_name",
        "budget_month_name",
        "budget_amount",
        "actual_spend",
        "variance",
        "variance_percentage",
        "budget_status",
        "number_of_expenses"
    ]
]

budget_vs_actual = budget_vs_actual.sort_values(
    ["budget_status", "variance"]
)

budget_vs_actual.to_csv(
    REPORTS_PATH / "budget_vs_actual.csv",
    index=False
)

print()
print("Budget vs actual summary:")
print(budget_vs_actual.head(10))

print()
print("Budget vs actual report saved to reports/budget_vs_actual.csv")

# -----------------------------
# Department budget summary
# -----------------------------

department_budget_summary = (
    budget_vs_actual
    .groupby("department_name")
    .agg(
        total_budget=("budget_amount", "sum"),
        total_actual_spend=("actual_spend", "sum"),
        total_variance=("variance", "sum"),
        over_budget_months=("budget_status", lambda x: (x == "Over Budget").sum()),
        under_budget_months=("budget_status", lambda x: (x == "Under Budget").sum())
    )
    .reset_index()
)

department_budget_summary["variance_percentage"] = (
    department_budget_summary["total_variance"] /
    department_budget_summary["total_budget"] * 100
).round(1)

department_budget_summary["overall_budget_status"] = department_budget_summary["total_variance"].apply(
    lambda value: "Over Budget" if value < 0 else "Under Budget"
)

department_budget_summary = department_budget_summary.sort_values(
    "total_variance"
)

department_budget_summary.to_csv(
    REPORTS_PATH / "department_budget_summary.csv",
    index=False
)

print()
print("Department budget summary:")
print(department_budget_summary)

print()
print("Department budget summary saved to reports/department_budget_summary.csv")

# -----------------------------
# Client payment risk summary
# -----------------------------

client_payment_risk = invoices.merge(
    clients,
    on="client_id",
    how="left"
)

client_payment_risk_summary = (
    client_payment_risk
    .groupby(["client_id", "client_name", "industry", "country"])
    .agg(
        total_invoiced=("invoice_amount", "sum"),
        number_of_invoices=("invoice_id", "count"),
        paid_invoices=("is_paid", "sum"),
        overdue_invoices=("is_overdue", "sum"),
        late_payments=("is_late_payment", "sum"),
        average_days_to_payment=("days_to_payment", "mean"),
        average_days_late=("days_late", "mean")
    )
    .reset_index()
)

client_payment_risk_summary["late_payment_rate"] = (
    client_payment_risk_summary["late_payments"] /
    client_payment_risk_summary["paid_invoices"] * 100
).round(1)

client_payment_risk_summary["overdue_invoice_rate"] = (
    client_payment_risk_summary["overdue_invoices"] /
    client_payment_risk_summary["number_of_invoices"] * 100
).round(1)

client_payment_risk_summary["average_days_to_payment"] = (
    client_payment_risk_summary["average_days_to_payment"].round(1)
)

client_payment_risk_summary["average_days_late"] = (
    client_payment_risk_summary["average_days_late"].round(1)
)

client_payment_risk_summary["payment_risk_level"] = client_payment_risk_summary.apply(
    lambda row: "High Risk"
    if row["overdue_invoice_rate"] >= 20 or row["late_payment_rate"] >= 50
    else "Medium Risk"
    if row["overdue_invoice_rate"] >= 10 or row["late_payment_rate"] >= 25
    else "Low Risk",
    axis=1
)

client_payment_risk_summary = client_payment_risk_summary.sort_values(
    ["payment_risk_level", "overdue_invoice_rate", "late_payment_rate"],
    ascending=[True, False, False]
)

client_payment_risk_summary.to_csv(
    REPORTS_PATH / "client_payment_risk_summary.csv",
    index=False
)

print()
print("Client payment risk summary:")
print(client_payment_risk_summary.head(10))

print()
print("Client payment risk report saved to reports/client_payment_risk_summary.csv")

# -----------------------------
# Invoice status summary
# -----------------------------

invoice_status_summary = (
    invoices
    .groupby("invoice_status")
    .agg(
        total_invoiced=("invoice_amount", "sum"),
        number_of_invoices=("invoice_id", "count"),
        average_invoice_amount=("invoice_amount", "mean")
    )
    .reset_index()
)

invoice_status_summary["total_invoiced"] = invoice_status_summary["total_invoiced"].round(2)
invoice_status_summary["average_invoice_amount"] = invoice_status_summary["average_invoice_amount"].round(2)

invoice_status_summary = invoice_status_summary.sort_values(
    "total_invoiced",
    ascending=False
)

invoice_status_summary.to_csv(
    REPORTS_PATH / "invoice_status_summary.csv",
    index=False
)

print()
print("Invoice status summary:")
print(invoice_status_summary)

print()
print("Invoice status summary saved to reports/invoice_status_summary.csv")

# -----------------------------
# Monthly cashflow risk summary
# -----------------------------

monthly_cashflow_risk = (
    invoices
    .groupby(["invoice_month", "invoice_status"])
    .agg(
        total_invoiced=("invoice_amount", "sum"),
        number_of_invoices=("invoice_id", "count")
    )
    .reset_index()
)

monthly_cashflow_risk.to_csv(
    REPORTS_PATH / "monthly_cashflow_risk.csv",
    index=False
)

print()
print("Monthly cashflow risk summary:")
print(monthly_cashflow_risk.head(15))

print()
print("Monthly cashflow risk summary saved to reports/monthly_cashflow_risk.csv")

# -----------------------------
# Monthly finance KPI summary
# -----------------------------

monthly_invoice_status_pivot = (
    monthly_cashflow_risk
    .pivot_table(
        index="invoice_month",
        columns="invoice_status",
        values="total_invoiced",
        aggfunc="sum",
        fill_value=0
    )
    .reset_index()
)

monthly_invoice_status_pivot.columns.name = None

monthly_finance_kpis = monthly_profit.merge(
    monthly_invoice_status_pivot,
    left_on="month",
    right_on="invoice_month",
    how="left"
)

for column in ["Paid", "Unpaid", "Overdue"]:
    if column not in monthly_finance_kpis.columns:
        monthly_finance_kpis[column] = 0

monthly_finance_kpis = monthly_finance_kpis.rename(
    columns={
        "Paid": "paid_amount",
        "Unpaid": "unpaid_amount",
        "Overdue": "overdue_amount"
    }
)

monthly_finance_kpis["outstanding_amount"] = (
    monthly_finance_kpis["unpaid_amount"] + monthly_finance_kpis["overdue_amount"]
).round(2)

monthly_finance_kpis["collection_rate"] = (
    monthly_finance_kpis["paid_amount"] /
    monthly_finance_kpis["total_invoiced"] * 100
).round(1)

monthly_finance_kpis = monthly_finance_kpis[
    [
        "month",
        "total_invoiced",
        "total_expenses",
        "profit",
        "profit_margin",
        "number_of_invoices",
        "number_of_expenses",
        "paid_invoices",
        "overdue_invoices",
        "paid_amount",
        "unpaid_amount",
        "overdue_amount",
        "outstanding_amount",
        "collection_rate"
    ]
]

monthly_finance_kpis.to_csv(
    REPORTS_PATH / "monthly_finance_kpis.csv",
    index=False
)

print()
print("Monthly finance KPI summary:")
print(monthly_finance_kpis)

print()
print("Monthly finance KPI summary saved to reports/monthly_finance_kpis.csv")

# -----------------------------
# Executive summary
# -----------------------------

total_revenue = monthly_finance_kpis["total_invoiced"].sum()
total_expenses = monthly_finance_kpis["total_expenses"].sum()
total_profit = monthly_finance_kpis["profit"].sum()
overall_profit_margin = (total_profit / total_revenue * 100).round(1)

total_paid = monthly_finance_kpis["paid_amount"].sum()
total_unpaid = monthly_finance_kpis["unpaid_amount"].sum()
total_overdue = monthly_finance_kpis["overdue_amount"].sum()
total_outstanding = monthly_finance_kpis["outstanding_amount"].sum()
overall_collection_rate = (total_paid / total_revenue * 100).round(1)

best_profit_month = monthly_finance_kpis.sort_values(
    "profit",
    ascending=False
).iloc[0]

worst_profit_month = monthly_finance_kpis.sort_values(
    "profit",
    ascending=True
).iloc[0]

highest_outstanding_month = monthly_finance_kpis.sort_values(
    "outstanding_amount",
    ascending=False
).iloc[0]

top_expense_category = expense_category_summary.sort_values(
    "total_expenses",
    ascending=False
).iloc[0]

top_client = client_revenue_summary.sort_values(
    "total_invoiced",
    ascending=False
).iloc[0]

top_vendor = vendor_spend_summary.sort_values(
    "total_spend",
    ascending=False
).iloc[0]

most_over_budget_department = department_budget_summary.sort_values(
    "total_variance",
    ascending=True
).iloc[0]

highest_risk_client = client_payment_risk_summary.sort_values(
    ["overdue_invoice_rate", "late_payment_rate"],
    ascending=False
).iloc[0]

summary_text = f"""
FINANCE ANALYTICS DASHBOARD - EXECUTIVE SUMMARY
===============================================

Overall Performance
-------------------
Total invoiced revenue: R{total_revenue:,.2f}
Total expenses: R{total_expenses:,.2f}
Total profit: R{total_profit:,.2f}
Overall profit margin: {overall_profit_margin}%

The business generated a positive overall profit across the reporting period. However, several months showed weaker profitability due to high expenses and outstanding invoice balances.

Best and Worst Months
---------------------
Best profit month: {best_profit_month["month"]}
Profit: R{best_profit_month["profit"]:,.2f}
Profit margin: {best_profit_month["profit_margin"]}%

Worst profit month: {worst_profit_month["month"]}
Profit: R{worst_profit_month["profit"]:,.2f}
Profit margin: {worst_profit_month["profit_margin"]}%

Cashflow and Collection Risk
----------------------------
Total paid amount: R{total_paid:,.2f}
Total unpaid amount: R{total_unpaid:,.2f}
Total overdue amount: R{total_overdue:,.2f}
Total outstanding amount: R{total_outstanding:,.2f}
Overall collection rate: {overall_collection_rate}%

Highest outstanding month: {highest_outstanding_month["month"]}
Outstanding amount: R{highest_outstanding_month["outstanding_amount"]:,.2f}
Collection rate: {highest_outstanding_month["collection_rate"]}%

Revenue and Client Insights
---------------------------
Top client by invoiced revenue: {top_client["client_name"]}
Industry: {top_client["industry"]}
Country: {top_client["country"]}
Total invoiced: R{top_client["total_invoiced"]:,.2f}

Highest payment-risk client: {highest_risk_client["client_name"]}
Industry: {highest_risk_client["industry"]}
Country: {highest_risk_client["country"]}
Overdue invoice rate: {highest_risk_client["overdue_invoice_rate"]}%
Late payment rate: {highest_risk_client["late_payment_rate"]}%

Expense and Vendor Insights
---------------------------
Largest expense category: {top_expense_category["expense_category"]}
Total expenses: R{top_expense_category["total_expenses"]:,.2f}

Highest-spend vendor: {top_vendor["vendor_name"]}
Vendor category: {top_vendor["vendor_category"]}
Total spend: R{top_vendor["total_spend"]:,.2f}

Budget Control
--------------
Most over-budget department: {most_over_budget_department["department_name"]}
Total budget: R{most_over_budget_department["total_budget"]:,.2f}
Total actual spend: R{most_over_budget_department["total_actual_spend"]:,.2f}
Total variance: R{most_over_budget_department["total_variance"]:,.2f}
Variance percentage: {most_over_budget_department["variance_percentage"]}%

Key Business Interpretation
---------------------------
The business is profitable overall, but cashflow risk is a major concern. A large amount of invoiced revenue remains unpaid or overdue, meaning reported profit does not fully reflect cash collected.

The dashboard should therefore focus on both profitability and collection risk. This allows decision-makers to identify strong revenue months, high-cost departments, over-budget areas, and risky clients who may affect future cashflow.
"""

with open(REPORTS_PATH / "executive_summary.txt", "w", encoding="utf-8") as file:
    file.write(summary_text)

print()
print("Executive summary saved to reports/executive_summary.txt")