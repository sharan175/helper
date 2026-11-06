-- Load clickstream data
clicks = LOAD 'clickstream.csv'
    USING PigStorage(',')
    AS (uid:chararray, pid:chararray,
        action:chararray, timestamp:chararray);

-- Load product metadata
products = LOAD 'products.csv'
    USING PigStorage(',')
    AS (pid:chararray, price:float, category:chararray);

-- 1. Filter only purchase records
purchases = FILTER clicks
    BY LOWER(action) == 'purchase';

-- 2. Group and count number of views per product
views = FILTER clicks BY LOWER(action) == 'view';
views_grouped = GROUP views BY pid;
view_counts = FOREACH views_grouped
    GENERATE group AS pid, COUNT(views) AS view_count;

-- 3. Join with product metadata
joined = JOIN view_counts BY pid, products BY pid;

-- 4. Sort by most viewed
sorted_views = ORDER joined BY view_count DESC;

-- 5. Store outputs
STORE purchases INTO 'output_purchases'
    USING PigStorage(',');
STORE sorted_views INTO 'output_views'
    USING PigStorage(',');
