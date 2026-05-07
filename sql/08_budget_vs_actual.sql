WITH department_monthly_expenses AS (
    SELECT
        department_id,
        expense_month,
        ROUND(SUM(expense_amount), 2) AS actual_spend,
        COUNT(expense_id) AS number_of_expenses
    FROM expenses
    GROUP BY
        department_id,
        expense_month
)

SELECT
    budgets.department_id,
    departments.department_name,
    budgets.budget_month_name,
    budgets.budget_amount,
    COALESCE(department_monthly_expenses.actual_spend, 0) AS actual_spend,
    ROUND(
        budgets.budget_amount - COALESCE(department_monthly_expenses.actual_spend, 0),
        2
    ) AS variance,
    ROUND(
        (
            budgets.budget_amount - COALESCE(department_monthly_expenses.actual_spend, 0)
        ) / budgets.budget_amount * 100,
        1
    ) AS variance_percentage,
    CASE
        WHEN budgets.budget_amount - COALESCE(department_monthly_expenses.actual_spend, 0) < 0
            THEN 'Over Budget'
        ELSE 'Under Budget'
    END AS budget_status,
    COALESCE(department_monthly_expenses.number_of_expenses, 0) AS number_of_expenses
FROM budgets
JOIN departments
    ON budgets.department_id = departments.department_id
LEFT JOIN department_monthly_expenses
    ON budgets.department_id = department_monthly_expenses.department_id
    AND budgets.budget_month_name = department_monthly_expenses.expense_month
ORDER BY
    budget_status,
    variance;