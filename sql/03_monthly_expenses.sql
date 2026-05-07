SELECT
    expense_month,
    ROUND(SUM(expense_amount), 2) AS total_expenses,
    COUNT(expense_id) AS number_of_expenses
FROM expenses
GROUP BY expense_month
ORDER BY expense_month;