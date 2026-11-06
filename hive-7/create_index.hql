CREATE INDEX idx_caller_id
ON TABLE cdr (caller_id)
AS 'COMPACT'
WITH DEFERRED REBUILD;

ALTER INDEX idx_caller_id
ON cdr REBUILD;
