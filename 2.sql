-- A
SELECT ticket_client
FROM tickets
WHERE csat < 3;

-- Б
SELECT ticket_id
FROM tickets
WHERE text LIKE '%отлично%'
ORDER BY csat DESC;

-- В
SELECT order_client_id AS frequent_customer, MAX(price) AS max_sum
FROM orders
WHERE place IN ('Теремок', 'Вкусно и точка') AND price BETWEEN 2000 AND 10000
GROUP BY order_client_id
HAVING COUNT(order_id) > 5;

-- Г
SELECT
    o.order_id,
    o.price,
    o.order_client_id,
    o.place,
    c.client_id,
    c.username,
    c.name,
    c.age,
    c.city,
    t.ticket_id,
    t.ticket_client,
    t.csat,
    t.text,
    t.date,
    t.ticket_order_id
FROM orders o
LEFT JOIN clients c ON o.order_client_id = c.client_id
LEFT JOIN tickets t ON o.order_id = t.ticket_order_id
LIMIT 1000;
