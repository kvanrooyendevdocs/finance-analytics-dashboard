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
),

budget_vs_actual AS (
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
        CASE
            WHEN budgets.budget_amount - COALESCE(department_monthly_expenses.actual_spend, 0) < 0
                THEN 'Over Budget'
            ELSE 'Under Budget'
        END AS budget_status
    FROM budgets
    JOIN departments
        ON budgets.department_id = departments.department_id
    LEFT JOIN department_monthly_expenses
        ON budgets.department_id = department_monthly_expenses.department_id
        AND budgets.budget_month_name = department_monthly_expenses.expense_month
)

SELECT
    department_name,
    ROUND(SUM(budget_amount), 2) AS total_budget,
    ROUND(SUM(actual_spend), 2) AS total_actual_spend,
    ROUND(SUM(variance), 2) AS total_variance,
    SUM(CASE WHEN budget_status = 'Over Budget' THEN 1 ELSE 0 END) AS over_budget_months,
    SUM(CASE WHEN budget_status = 'Under Budget' THEN 1 ELSE 0 END) AS under_budget_months,
    ROUND(SUM(variance) / SUM(budget_amount) * 100, 1) AS variance_percentage,
    CASE
        WHEN SUM(variance) < 0
            THEN 'Over Budget'
        ELSE 'Under Budget'
    END AS overall_budget_status
FROM budget_vs_actual
GROUP BY department_name
ORDER BY total_variance;