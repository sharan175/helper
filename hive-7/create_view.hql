CREATE VIEW high_usage_customers AS
SELECT caller_id, SUM(duration) AS total_duration,
COUNT(*) AS total_calls
FROM cdr
GROUP BY caller_id
HAVING SUM(duration) > 100;

SELECT * FROM high_usage_customers;
