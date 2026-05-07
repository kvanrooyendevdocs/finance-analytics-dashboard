SELECT
    clients.client_id,
    clients.client_name,
    clients.industry,
    clients.country,
    ROUND(SUM(invoices.invoice_amount), 2) AS total_invoiced,
    COUNT(invoices.invoice_id) AS number_of_invoices,

    SUM(CASE WHEN invoices.invoice_status = 'Paid' THEN 1 ELSE 0 END) AS paid_invoices,
    SUM(CASE WHEN invoices.invoice_status = 'Overdue' THEN 1 ELSE 0 END) AS overdue_invoices,
    SUM(CASE WHEN invoices.is_late_payment = true THEN 1 ELSE 0 END) AS late_payments,

    ROUND(AVG(invoices.days_to_payment), 1) AS average_days_to_payment,
    ROUND(AVG(invoices.days_late), 1) AS average_days_late,

    ROUND(
        SUM(CASE WHEN invoices.is_late_payment = true THEN 1 ELSE 0 END)::NUMERIC
        / NULLIF(SUM(CASE WHEN invoices.invoice_status = 'Paid' THEN 1 ELSE 0 END), 0) * 100,
        1
    ) AS late_payment_rate,

    ROUND(
        SUM(CASE WHEN invoices.invoice_status = 'Overdue' THEN 1 ELSE 0 END)::NUMERIC
        / COUNT(invoices.invoice_id) * 100,
        1
    ) AS overdue_invoice_rate,

    CASE
        WHEN
            ROUND(
                SUM(CASE WHEN invoices.invoice_status = 'Overdue' THEN 1 ELSE 0 END)::NUMERIC
                / COUNT(invoices.invoice_id) * 100,
                1
            ) >= 20
            OR
            ROUND(
                SUM(CASE WHEN invoices.is_late_payment = true THEN 1 ELSE 0 END)::NUMERIC
                / NULLIF(SUM(CASE WHEN invoices.invoice_status = 'Paid' THEN 1 ELSE 0 END), 0) * 100,
                1
            ) >= 50
            THEN 'High Risk'

        WHEN
            ROUND(
                SUM(CASE WHEN invoices.invoice_status = 'Overdue' THEN 1 ELSE 0 END)::NUMERIC
                / COUNT(invoices.invoice_id) * 100,
                1
            ) >= 10
            OR
            ROUND(
                SUM(CASE WHEN invoices.is_late_payment = true THEN 1 ELSE 0 END)::NUMERIC
                / NULLIF(SUM(CASE WHEN invoices.invoice_status = 'Paid' THEN 1 ELSE 0 END), 0) * 100,
                1
            ) >= 25
            THEN 'Medium Risk'

        ELSE 'Low Risk'
    END AS payment_risk_level

FROM invoices
JOIN clients
    ON invoices.client_id = clients.client_id
GROUP BY
    clients.client_id,
    clients.client_name,
    clients.industry,
    clients.country
ORDER BY
    overdue_invoice_rate DESC,
    late_payment_rate DESC;