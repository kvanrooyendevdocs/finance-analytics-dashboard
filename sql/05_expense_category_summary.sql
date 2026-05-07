SELECT
    expense_category,
    ROUND(SUM(expense_amount), 2) AS total_expenses,
    COUNT(expense_id) AS number_of_expenses,
    ROUND(AVG(expense_amount), 2) AS average_expense
FROM expenses
GROUP BY expense_category
ORDER BY total_expenses DESC;