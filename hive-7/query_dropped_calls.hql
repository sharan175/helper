SELECT location, COUNT(*) AS dropped_calls
FROM cdr
WHERE duration = 0
GROUP BY location
ORDER BY dropped_calls DESC;
