SELECT 'departments' AS table_name, COUNT(*) AS row_count
FROM departments

UNION ALL

SELECT 'clients' AS table_name, COUNT(*) AS row_count
FROM clients

UNION ALL

SELECT 'vendors' AS table_name, COUNT(*) AS row_count
FROM vendors

UNION ALL

SELECT 'invoices' AS table_name, COUNT(*) AS row_count
FROM invoices

UNION ALL

SELECT 'expenses' AS table_name, COUNT(*) AS row_count
FROM expenses

UNION ALL

SELECT 'budgets' AS table_name, COUNT(*) AS row_count
FROM budgets;