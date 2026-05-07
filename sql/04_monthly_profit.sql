WITH monthly_revenue AS (
    SELECT
        invoice_month AS month,
        ROUND(SUM(invoice_amount), 2) AS total_invoiced,
        COUNT(invoice_id) AS number_of_invoices,
        SUM(CASE WHEN invoice_status = 'Paid' THEN 1 ELSE 0 END) AS paid_invoices,
        SUM(CASE WHEN invoice_status = 'Unpaid' THEN 1 ELSE 0 END) AS unpaid_invoices,
        SUM(CASE WHEN invoice_status = 'Overdue' THEN 1 ELSE 0 END) AS overdue_invoices
    FROM invoices
    GROUP BY invoice_month
),

monthly_expenses AS (
    SELECT
        expense_month AS month,
        ROUND(SUM(expense_amount), 2) AS total_expenses,
        COUNT(expense_id) AS number_of_expenses
    FROM expenses
    GROUP BY expense_month
)

SELECT
    monthly_revenue.month,
    monthly_revenue.total_invoiced,
    monthly_expenses.total_expenses,
    ROUND(monthly_revenue.total_invoiced - monthly_expenses.total_expenses, 2) AS profit,
    ROUND(
        (monthly_revenue.total_invoiced - monthly_expenses.total_expenses)
        / monthly_revenue.total_invoiced * 100,
        1
    ) AS profit_margin,
    monthly_revenue.number_of_invoices,
    monthly_expenses.number_of_expenses,
    monthly_revenue.paid_invoices,
    monthly_revenue.unpaid_invoices,
    monthly_revenue.overdue_invoices
FROM monthly_revenue
JOIN monthly_expenses
    ON monthly_revenue.month = monthly_expenses.month
ORDER BY monthly_revenue.month;