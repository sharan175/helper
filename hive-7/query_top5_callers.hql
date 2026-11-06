SELECT caller_id, SUM(duration) AS total_duration
FROM cdr
GROUP BY caller_id
ORDER BY total_duration DESC
LIMIT 5;
