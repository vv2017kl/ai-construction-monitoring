-- ================================================================
-- PERFORMANCE MONITORING QUERIES
-- Construction Site AI Monitoring System
-- Version: 1.0
-- ================================================================

-- ================================================================
-- DATABASE SIZE AND GROWTH MONITORING
-- ================================================================

-- Check overall database sizes
SELECT 'DATABASE_SIZES' as QueryType;
SELECT 
    table_schema as 'Database',
    ROUND(SUM(data_length + index_length) / 1024 / 1024, 2) AS 'Size (MB)',
    ROUND(SUM(data_length) / 1024 / 1024, 2) AS 'Data (MB)',
    ROUND(SUM(index_length) / 1024 / 1024, 2) AS 'Indexes (MB)',
    COUNT(*) as 'Tables'
FROM information_schema.TABLES 
WHERE table_schema IN ('construction_vms', 'construction_management')
GROUP BY table_schema
ORDER BY SUM(data_length + index_length) DESC;

-- Check largest tables
SELECT 'LARGEST_TABLES' as QueryType;
SELECT 
    table_schema,
    table_name,
    ROUND(((data_length + index_length) / 1024 / 1024), 2) AS 'Size (MB)',
    ROUND((data_length / 1024 / 1024), 2) AS 'Data (MB)',
    ROUND((index_length / 1024 / 1024), 2) AS 'Indexes (MB)',
    table_rows as 'Rows'
FROM information_schema.TABLES 
WHERE table_schema IN ('construction_vms', 'construction_management')
ORDER BY (data_length + index_length) DESC
LIMIT 20;

-- ================================================================
-- PARTITION MONITORING
-- ================================================================

-- Monitor partition usage and sizes
SELECT 'PARTITION_USAGE' as QueryType;
SELECT 
    TABLE_SCHEMA as 'Database',
    TABLE_NAME as 'Table',
    PARTITION_NAME as 'Partition',
    TABLE_ROWS as 'Rows',
    ROUND((DATA_LENGTH / 1024 / 1024), 2) AS 'Data (MB)',
    ROUND((INDEX_LENGTH / 1024 / 1024), 2) AS 'Indexes (MB)',
    PARTITION_DESCRIPTION as 'Range'
FROM INFORMATION_SCHEMA.PARTITIONS 
WHERE TABLE_SCHEMA IN ('construction_vms', 'construction_management')
AND PARTITION_NAME IS NOT NULL
ORDER BY TABLE_SCHEMA, TABLE_NAME, PARTITION_NAME;

-- ================================================================
-- INDEX USAGE ANALYSIS
-- ================================================================

-- Check unused indexes (MySQL 8.0+)
SELECT 'UNUSED_INDEXES' as QueryType;
SELECT 
    object_schema as 'Database',
    object_name as 'Table',
    index_name as 'Index',
    'Never Used' as Status
FROM performance_schema.table_io_waits_summary_by_index_usage 
WHERE object_schema IN ('construction_vms', 'construction_management')
AND index_name IS NOT NULL 
AND index_name != 'PRIMARY'
AND count_star = 0
ORDER BY object_schema, object_name;

-- Check most used indexes
SELECT 'MOST_USED_INDEXES' as QueryType;
SELECT 
    object_schema as 'Database',
    object_name as 'Table',
    index_name as 'Index',
    count_star as 'Usage Count',
    sum_timer_wait/1000000000 as 'Total Wait (sec)'
FROM performance_schema.table_io_waits_summary_by_index_usage 
WHERE object_schema IN ('construction_vms', 'construction_management')
AND index_name IS NOT NULL 
ORDER BY count_star DESC
LIMIT 20;

-- ================================================================
-- QUERY PERFORMANCE ANALYSIS
-- ================================================================

-- Check slow queries related to construction tables
SELECT 'SLOW_QUERIES' as QueryType;
SELECT 
    ROUND(total_latency/1000000000, 2) as 'Total Time (sec)',
    ROUND(avg_latency/1000000, 2) as 'Avg Time (ms)',
    exec_count as 'Executions',
    ROUND((total_latency/exec_count)/1000000, 2) as 'Avg per Exec (ms)',
    LEFT(digest_text, 100) as 'Query Preview'
FROM performance_schema.statement_analysis 
WHERE digest_text LIKE '%detection_results%' 
   OR digest_text LIKE '%alerts%'
   OR digest_text LIKE '%cameras%'
   OR digest_text LIKE '%video_storage%'
ORDER BY total_latency DESC 
LIMIT 10;

-- ================================================================
-- TABLE STATISTICS AND HEALTH
-- ================================================================

-- Check table statistics for construction tables
SELECT 'TABLE_STATISTICS' as QueryType;
SELECT 
    TABLE_SCHEMA as 'Database',
    TABLE_NAME as 'Table',
    TABLE_ROWS as 'Rows',
    ROUND(DATA_LENGTH/1024/1024, 2) as 'Data (MB)',
    ROUND(INDEX_LENGTH/1024/1024, 2) as 'Index (MB)',
    ROUND((DATA_LENGTH + INDEX_LENGTH)/1024/1024, 2) as 'Total (MB)',
    UPDATE_TIME as 'Last Updated',
    CHECK_TIME as 'Last Checked'
FROM information_schema.TABLES 
WHERE TABLE_SCHEMA IN ('construction_vms', 'construction_management')
AND TABLE_TYPE = 'BASE TABLE'
ORDER BY TABLE_ROWS DESC;

-- ================================================================
-- REAL-TIME PERFORMANCE METRICS
-- ================================================================

-- Current connection and thread information
SELECT 'CONNECTION_STATUS' as QueryType;
SELECT 
    'Active Connections' as Metric,
    COUNT(*) as Value
FROM information_schema.PROCESSLIST 
WHERE DB IN ('construction_vms', 'construction_management')
UNION ALL
SELECT 
    'Long Running Queries' as Metric,
    COUNT(*) as Value
FROM information_schema.PROCESSLIST 
WHERE DB IN ('construction_vms', 'construction_management')
AND TIME > 60;

-- Buffer pool usage
SELECT 'BUFFER_POOL_STATUS' as QueryType;
SELECT 
    VARIABLE_NAME as 'Metric',
    VARIABLE_VALUE as 'Value'
FROM performance_schema.global_status 
WHERE VARIABLE_NAME IN (
    'Innodb_buffer_pool_pages_total',
    'Innodb_buffer_pool_pages_free',
    'Innodb_buffer_pool_pages_data',
    'Innodb_buffer_pool_read_requests',
    'Innodb_buffer_pool_reads'
);

-- ================================================================
-- DATA GROWTH TRENDS
-- ================================================================

-- Detection results growth by day (last 30 days)
USE construction_management;
SELECT 'DETECTION_GROWTH' as QueryType;
SELECT 
    DATE(detection_timestamp) as 'Date',
    COUNT(*) as 'Daily Detections',
    SUM(personnel_count) as 'Total Personnel Detected',
    SUM(ppe_violations_detected) as 'Total PPE Violations'
FROM detection_results 
WHERE detection_timestamp >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
GROUP BY DATE(detection_timestamp)
ORDER BY DATE(detection_timestamp) DESC
LIMIT 30;

-- Alert generation trends
SELECT 'ALERT_TRENDS' as QueryType;
SELECT 
    DATE(triggered_at) as 'Date',
    severity,
    COUNT(*) as 'Alert Count'
FROM alerts 
WHERE triggered_at >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
GROUP BY DATE(triggered_at), severity
ORDER BY DATE(triggered_at) DESC, severity;

-- Video storage growth
USE construction_vms;
SELECT 'VIDEO_STORAGE_GROWTH' as QueryType;
SELECT 
    DATE(start_time) as 'Date',
    COUNT(*) as 'Videos Created',
    ROUND(SUM(file_size_bytes)/1024/1024/1024, 2) as 'Total Size (GB)',
    ROUND(AVG(file_size_bytes)/1024/1024, 2) as 'Avg Size (MB)'
FROM video_storage 
WHERE start_time >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
GROUP BY DATE(start_time)
ORDER BY DATE(start_time) DESC
LIMIT 30;

-- ================================================================
-- SYSTEM HEALTH CHECKS
-- ================================================================

-- Check for fragmented tables
SELECT 'FRAGMENTED_TABLES' as QueryType;
SELECT 
    table_schema as 'Database',
    table_name as 'Table',
    ROUND(data_length/1024/1024, 2) as 'Data (MB)',
    ROUND(data_free/1024/1024, 2) as 'Free Space (MB)',
    ROUND((data_free/data_length)*100, 2) as 'Fragmentation %'
FROM information_schema.tables 
WHERE table_schema IN ('construction_vms', 'construction_management')
AND data_free > 0
AND (data_free/data_length) > 0.1
ORDER BY (data_free/data_length) DESC;

-- Check for tables needing optimization
SELECT 'TABLES_NEED_OPTIMIZATION' as QueryType;
SELECT 
    CONCAT(table_schema, '.', table_name) as 'Table',
    ROUND(((data_length + index_length) / 1024 / 1024), 2) AS 'Size (MB)',
    table_rows as 'Rows',
    ROUND(((data_length + index_length) / table_rows), 2) AS 'Bytes per Row',
    'OPTIMIZE TABLE ' + CONCAT(table_schema, '.', table_name) + ';' as 'Optimization Command'
FROM information_schema.TABLES 
WHERE table_schema IN ('construction_vms', 'construction_management')
AND table_rows > 10000
AND ((data_length + index_length) / table_rows) > 1000
ORDER BY ((data_length + index_length) / table_rows) DESC;

SELECT 'Performance monitoring queries completed!' as Status;