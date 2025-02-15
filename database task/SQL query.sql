--naming the first table as customers
--naming the second table as salesmen

SELECT c.cust_name, c.city AS customer_city, s.name AS salesman, s.city AS salesman_city, s.commission
FROM customers c
JOIN salesmen s ON c.salesman_id = s.salesman_id
WHERE c.city != s.city AND s.commission > 0.12;