SELECT
    invoice_month,
    ROUND(SUM(invoice_amount), 2) AS total_invoiced,
    COUNT(invoice_id) AS number_of_invoices,
    SUM(CASE WHEN invoice_status = 'Paid' THEN 1 ELSE 0 END) AS paid_invoices,
    SUM(CASE WHEN invoice_status = 'Unpaid' THEN 1 ELSE 0 END) AS unpaid_invoices,
    SUM(CASE WHEN invoice_status = 'Overdue' THEN 1 ELSE 0 END) AS overdue_invoices
FROM invoices
GROUP BY invoice_month
ORDER BY invoice_month;