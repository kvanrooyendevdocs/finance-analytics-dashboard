# Finance Analytics Dashboard

This project is a finance analytics portfolio dashboard built with Python, pandas, SQL/PostgreSQL, Power BI, and GitHub.

The goal of the project is to analyse synthetic company finance data and identify key business insights around revenue, expenses, profitability, budgets, clients, vendors, and payment risk.

## Project Objectives

The dashboard answers the following business questions:

- How much revenue is being invoiced each month?
- How much is being spent each month?
- Which months are profitable or loss-making?
- Which expense categories drive the highest costs?
- Which clients generate the most revenue?
- Which vendors receive the highest spend?
- Which departments are over or under budget?
- Which clients create payment and cashflow risk?
- How much revenue is paid, unpaid, or overdue?

## Tools Used

- Python
- pandas
- NumPy
- Faker
- Matplotlib
- PostgreSQL
- SQL
- Power BI
- Git
- GitHub

## Project Structure

```text
finance-analytics-dashboard/
│
├── data/
│   ├── raw/
│   └── cleaned/
│
├── powerbi/
│
├── reports/
│
├── scripts/
│   ├── generate_fake_finance_data.py
│   ├── clean_finance_data.py
│   ├── analyse_finance_data.py
│   └── create_finance_charts.py
│
├── sql/
│
├── README.md
└── .gitignore

Dataset Overview

This project uses synthetic finance data generated with Python and Faker.

The raw datasets include:

Departments
Clients
Vendors
Invoices
Expenses
Budgets

The generated raw data includes:

Dataset	Rows	Description
departments.csv	8	Company departments
clients.csv	50	Client companies
vendors.csv	40	Vendor companies
invoices.csv	600	Client invoice records
expenses.csv	900	Company expense records
budgets.csv	96	Monthly department budgets
Analysis Outputs

The Python analysis creates the following reports:

Report	Purpose
monthly_revenue.csv	Monthly invoiced revenue and invoice counts
monthly_expenses.csv	Monthly expense totals
monthly_profit.csv	Monthly revenue, expenses, profit, and margin
expense_category_summary.csv	Expense breakdown by category
client_revenue_summary.csv	Revenue by client
vendor_spend_summary.csv	Spend by vendor
budget_vs_actual.csv	Monthly department budget comparison
department_budget_summary.csv	Yearly department budget performance
client_payment_risk_summary.csv	Client payment risk analysis
invoice_status_summary.csv	Paid, unpaid, and overdue invoice totals
monthly_cashflow_risk.csv	Monthly paid, unpaid, and overdue amounts
monthly_finance_kpis.csv	Dashboard-ready monthly KPI table
executive_summary.txt	Plain-English business summary
Key Insights

The business was profitable overall, but cashflow risk was a major concern because a large amount of invoiced revenue remained unpaid or overdue.

March 2026 was the strongest profit month, with a profit of R1,846,911.00 and a profit margin of 40.5%. However, March 2026 also had the highest outstanding amount of R2,061,065.73 and a low collection rate of 54.8%.

Human Resources was the most over-budget department overall. It spent R2,868,959.31 against a budget of R1,516,905.06, creating a negative variance of R1,352,054.25.

Training was the largest expense category, followed by Travel, Utilities, and Software.

Doyle Ltd was the highest-value client by invoiced revenue, generating R1,547,427.78 across 17 invoices.

Gardner, Robinson and Lawrence was the highest payment-risk client, with an overdue invoice rate of 60.0% and a late payment rate of 100.0%.

Chart Preview
Monthly Profit

Revenue vs Expenses

Expenses by Category

Department Budget Variance

Outstanding Amount by Month

Top Risky Clients

Business Interpretation

This project shows that profit alone does not tell the full finance story. A business may appear profitable on paper while still facing cashflow pressure if a large portion of revenue remains unpaid or overdue.

The most important dashboard focus areas are:

Profitability
Expense control
Budget variance
Outstanding revenue
Overdue invoices
Client payment risk