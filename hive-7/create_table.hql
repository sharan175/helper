CREATE TABLE cdr (
  caller_id STRING,
  receiver_id STRING,
  duration INT,
  timestamp STRING,
  location STRING
)
ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
STORED AS TEXTFILE
TBLPROPERTIES ("skip.header.line.count"="1");
