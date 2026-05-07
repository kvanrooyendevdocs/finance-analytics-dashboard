SELECT
    clients.client_id,
    clients.client_name,
    clients.industry,
    clients.country,
    ROUND(SUM(invoices.invoice_amount), 2) AS total_invoiced,
    COUNT(invoices.invoice_id) AS number_of_invoices,
    SUM(CASE WHEN invoices.invoice_status = 'Paid' THEN 1 ELSE 0 END) AS paid_invoices,
    SUM(CASE WHEN invoices.invoice_status = 'Unpaid' THEN 1 ELSE 0 END) AS unpaid_invoices,
    SUM(CASE WHEN invoices.invoice_status = 'Overdue' THEN 1 ELSE 0 END) AS overdue_invoices
FROM invoices
JOIN clients
    ON invoices.client_id = clients.client_id
GROUP BY
    clients.client_id,
    clients.client_name,
    clients.industry,
    clients.country
ORDER BY total_invoiced DESC;