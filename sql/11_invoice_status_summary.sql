SELECT
    invoice_status,
    ROUND(SUM(invoice_amount), 2) AS total_invoiced,
    COUNT(invoice_id) AS number_of_invoices,
    ROUND(AVG(invoice_amount), 2) AS average_invoice_amount
FROM invoices
GROUP BY invoice_status
ORDER BY total_invoiced DESC;