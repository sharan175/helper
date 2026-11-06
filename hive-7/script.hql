-- Lab Experiment 7: Hive CDR analysis (run: hive -f script.hql)
-- Place cdr.csv at /home/cloudera/cdr.csv before running, or edit the LOAD path.

CREATE TABLE IF NOT EXISTS cdr (
  caller_id STRING,
  receiver_id STRING,
  duration INT,
  timestamp STRING,
  location STRING
)
ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
STORED AS TEXTFILE
TBLPROPERTIES ("skip.header.line.count"="1");

LOAD DATA LOCAL INPATH '/home/cloudera/cdr.csv'
INTO TABLE cdr;

SELECT * FROM cdr;

SELECT caller_id, SUM(duration) AS total_duration
FROM cdr
GROUP BY caller_id
ORDER BY total_duration DESC
LIMIT 5;

SELECT location, COUNT(*) AS dropped_calls
FROM cdr
WHERE duration = 0
GROUP BY location
ORDER BY dropped_calls DESC;

CREATE VIEW IF NOT EXISTS high_usage_customers AS
SELECT caller_id, SUM(duration) AS total_duration,
COUNT(*) AS total_calls
FROM cdr
GROUP BY caller_id
HAVING SUM(duration) > 100;

SELECT * FROM high_usage_customers;

CREATE INDEX idx_caller_id
ON TABLE cdr (caller_id)
AS 'COMPACT'
WITH DEFERRED REBUILD;

ALTER INDEX idx_caller_id
ON cdr REBUILD;
