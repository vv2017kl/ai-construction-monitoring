-- ================================================================
-- MAINTENANCE PROCEDURES AND AUTOMATED TASKS
-- Construction Site AI Monitoring System
-- Version: 1.0
-- ================================================================

DELIMITER //

-- ================================================================
-- DATA ARCHIVAL PROCEDURES
-- ================================================================

-- Archive old detection results (keeps last N days in main table)
CREATE PROCEDURE ArchiveDetectionResults(IN days_to_keep INT)
BEGIN
    DECLARE done INT DEFAULT FALSE;
    DECLARE archive_date DATETIME;
    DECLARE archived_count INT DEFAULT 0;
    
    -- Calculate cutoff date
    SET archive_date = DATE_SUB(NOW(), INTERVAL days_to_keep DAY);
    
    -- Start transaction
    START TRANSACTION;
    
    -- Create archive table if it doesn't exist
    CREATE TABLE IF NOT EXISTS detection_results_archive LIKE detection_results;
    
    -- Move old records to archive
    INSERT INTO detection_results_archive 
    SELECT * FROM detection_results 
    WHERE detection_timestamp < archive_date;
    
    SET archived_count = ROW_COUNT();
    
    -- Delete archived records from main table
    DELETE FROM detection_results 
    WHERE detection_timestamp < archive_date;
    
    COMMIT;
    
    SELECT CONCAT('Archived ', archived_count, ' detection results older than ', days_to_keep, ' days') as Result;
END//

-- Archive old video files
CREATE PROCEDURE ArchiveVideoFiles(IN days_to_keep INT)
BEGIN
    DECLARE archive_date DATETIME;
    DECLARE archived_count INT DEFAULT 0;
    
    SET archive_date = DATE_SUB(NOW(), INTERVAL days_to_keep DAY);
    
    START TRANSACTION;
    
    -- Update video files to archived status
    UPDATE video_storage 
    SET is_archived = TRUE, archive_date = NOW()
    WHERE start_time < archive_date 
    AND is_archived = FALSE
    AND status = 'completed';
    
    SET archived_count = ROW_COUNT();
    
    COMMIT;
    
    SELECT CONCAT('Marked ', archived_count, ' video files as archived') as Result;
END//

-- Clean up old alerts (resolved alerts older than retention period)
CREATE PROCEDURE CleanupOldAlerts(IN days_to_keep INT)
BEGIN
    DECLARE cleanup_date DATETIME;
    DECLARE deleted_count INT DEFAULT 0;
    
    SET cleanup_date = DATE_SUB(NOW(), INTERVAL days_to_keep DAY);
    
    START TRANSACTION;
    
    -- Delete old resolved alerts and their related data
    DELETE FROM notifications WHERE alert_id IN (
        SELECT id FROM alerts 
        WHERE status IN ('resolved', 'closed', 'false_positive') 
        AND resolved_at < cleanup_date
    );
    
    DELETE FROM alert_escalations WHERE alert_id IN (
        SELECT id FROM alerts 
        WHERE status IN ('resolved', 'closed', 'false_positive') 
        AND resolved_at < cleanup_date
    );
    
    DELETE FROM alerts 
    WHERE status IN ('resolved', 'closed', 'false_positive') 
    AND resolved_at < cleanup_date;
    
    SET deleted_count = ROW_COUNT();
    
    COMMIT;
    
    SELECT CONCAT('Cleaned up ', deleted_count, ' old resolved alerts') as Result;
END//

-- ================================================================
-- PARTITION MAINTENANCE PROCEDURES
-- ================================================================

-- Add new partition for future data
CREATE PROCEDURE AddFuturePartition(IN table_name VARCHAR(64), IN year_value INT)
BEGIN
    DECLARE partition_sql TEXT;
    DECLARE partition_name VARCHAR(20);
    
    SET partition_name = CONCAT('p', year_value);
    SET partition_sql = CONCAT(
        'ALTER TABLE ', table_name, 
        ' ADD PARTITION (PARTITION ', partition_name, 
        ' VALUES LESS THAN (', year_value + 1, '))'
    );
    
    SET @sql = partition_sql;
    PREPARE stmt FROM @sql;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;
    
    SELECT CONCAT('Added partition ', partition_name, ' to table ', table_name) as Result;
END//

-- Drop old partitions
CREATE PROCEDURE DropOldPartition(IN table_name VARCHAR(64), IN partition_name VARCHAR(20))
BEGIN
    DECLARE partition_sql TEXT;
    
    SET partition_sql = CONCAT('ALTER TABLE ', table_name, ' DROP PARTITION ', partition_name);
    
    SET @sql = partition_sql;
    PREPARE stmt FROM @sql;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;
    
    SELECT CONCAT('Dropped partition ', partition_name, ' from table ', table_name) as Result;
END//

-- ================================================================
-- PERFORMANCE OPTIMIZATION PROCEDURES
-- ================================================================

-- Optimize fragmented tables
CREATE PROCEDURE OptimizeFragmentedTables(IN fragmentation_threshold DECIMAL(5,2))
BEGIN
    DECLARE done INT DEFAULT FALSE;
    DECLARE table_schema_name VARCHAR(64);
    DECLARE table_name_val VARCHAR(64);
    DECLARE fragmentation_pct DECIMAL(5,2);
    DECLARE optimize_sql TEXT;
    
    DECLARE table_cursor CURSOR FOR
        SELECT table_schema, table_name, 
               ROUND((data_free/data_length)*100, 2) as frag_pct
        FROM information_schema.tables 
        WHERE table_schema IN ('construction_vms', 'construction_management')
        AND data_free > 0
        AND (data_free/data_length)*100 > fragmentation_threshold;
    
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;
    
    OPEN table_cursor;
    
    read_loop: LOOP
        FETCH table_cursor INTO table_schema_name, table_name_val, fragmentation_pct;
        IF done THEN
            LEAVE read_loop;
        END IF;
        
        SET optimize_sql = CONCAT('OPTIMIZE TABLE ', table_schema_name, '.', table_name_val);
        SET @sql = optimize_sql;
        PREPARE stmt FROM @sql;
        EXECUTE stmt;
        DEALLOCATE PREPARE stmt;
        
        SELECT CONCAT('Optimized ', table_schema_name, '.', table_name_val, 
                     ' (was ', fragmentation_pct, '% fragmented)') as Result;
    END LOOP;
    
    CLOSE table_cursor;
END//

-- Update table statistics
CREATE PROCEDURE UpdateTableStatistics()
BEGIN
    DECLARE done INT DEFAULT FALSE;
    DECLARE table_schema_name VARCHAR(64);
    DECLARE table_name_val VARCHAR(64);
    DECLARE analyze_sql TEXT;
    
    DECLARE table_cursor CURSOR FOR
        SELECT table_schema, table_name
        FROM information_schema.tables 
        WHERE table_schema IN ('construction_vms', 'construction_management')
        AND table_type = 'BASE TABLE';
    
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;
    
    OPEN table_cursor;
    
    read_loop: LOOP
        FETCH table_cursor INTO table_schema_name, table_name_val;
        IF done THEN
            LEAVE read_loop;
        END IF;
        
        SET analyze_sql = CONCAT('ANALYZE TABLE ', table_schema_name, '.', table_name_val);
        SET @sql = analyze_sql;
        PREPARE stmt FROM @sql;
        EXECUTE stmt;
        DEALLOCATE PREPARE stmt;
    END LOOP;
    
    CLOSE table_cursor;
    
    SELECT 'Table statistics updated for all construction tables' as Result;
END//

-- ================================================================
-- DATA QUALITY PROCEDURES
-- ================================================================

-- Check for orphaned records (cross-database references)
CREATE PROCEDURE CheckOrphanedRecords()
BEGIN
    DECLARE orphaned_detections INT DEFAULT 0;
    DECLARE orphaned_alerts INT DEFAULT 0;
    DECLARE orphaned_violations INT DEFAULT 0;
    
    -- This would need to be implemented with application-level checks
    -- since we can't use foreign keys across databases
    
    -- Check detection_results without valid camera_id (requires application logic)
    -- Check alerts without valid camera_id (requires application logic)
    -- Check safety_violations without valid camera_id (requires application logic)
    
    SELECT 'Orphaned record check requires application-level validation due to cross-database references' as Result;
END//

-- Validate JSON field integrity
CREATE PROCEDURE ValidateJSONFields()
BEGIN
    DECLARE invalid_json_count INT DEFAULT 0;
    
    -- Check for invalid JSON in critical fields
    SELECT COUNT(*) INTO invalid_json_count
    FROM detection_results 
    WHERE (raw_detections IS NOT NULL AND NOT JSON_VALID(raw_detections))
       OR (processed_detections IS NOT NULL AND NOT JSON_VALID(processed_detections))
       OR (safety_violations IS NOT NULL AND NOT JSON_VALID(safety_violations));
    
    IF invalid_json_count > 0 THEN
        SELECT CONCAT('Found ', invalid_json_count, ' records with invalid JSON in detection_results') as Warning;
    ELSE
        SELECT 'All JSON fields validated successfully' as Result;
    END IF;
END//

-- ================================================================
-- AUTOMATED MAINTENANCE MASTER PROCEDURE
-- ================================================================

-- Master maintenance procedure that runs all maintenance tasks
CREATE PROCEDURE RunDailyMaintenance()
BEGIN
    DECLARE maintenance_start DATETIME;
    DECLARE maintenance_end DATETIME;
    
    SET maintenance_start = NOW();
    
    SELECT CONCAT('Starting daily maintenance at ', maintenance_start) as Status;
    
    -- Archive old data (keep 90 days of detection results)
    CALL ArchiveDetectionResults(90);
    
    -- Archive old video files (keep 30 days active)
    CALL ArchiveVideoFiles(30);
    
    -- Clean up old resolved alerts (keep 365 days)
    CALL CleanupOldAlerts(365);
    
    -- Optimize fragmented tables (>10% fragmentation)
    CALL OptimizeFragmentedTables(10.0);
    
    -- Update table statistics
    CALL UpdateTableStatistics();
    
    -- Validate data integrity
    CALL ValidateJSONFields();
    
    SET maintenance_end = NOW();
    
    SELECT CONCAT('Daily maintenance completed at ', maintenance_end,
                  '. Duration: ', TIMESTAMPDIFF(MINUTE, maintenance_start, maintenance_end), ' minutes') as Status;
END//

DELIMITER ;

-- ================================================================
-- AUTOMATED MAINTENANCE EVENTS
-- ================================================================

-- Daily maintenance event (runs at 2 AM)
CREATE EVENT IF NOT EXISTS daily_maintenance_event
ON SCHEDULE EVERY 1 DAY
STARTS CONCAT(CURDATE() + INTERVAL 1 DAY, ' 02:00:00')
DO
BEGIN
    CALL RunDailyMaintenance();
END;

-- Weekly optimization event (runs Sunday at 3 AM)
CREATE EVENT IF NOT EXISTS weekly_optimization_event
ON SCHEDULE EVERY 1 WEEK
STARTS CONCAT(DATE_ADD(CURDATE(), INTERVAL (7 - WEEKDAY(CURDATE())) DAY), ' 03:00:00')
DO
BEGIN
    -- Optimize all tables
    CALL OptimizeFragmentedTables(5.0);
    
    -- Check for partition maintenance needs
    -- Add future partitions for next year if needed
    SET @current_year = YEAR(NOW());
    SET @next_year = @current_year + 1;
    
    -- This would need dynamic SQL to check if partitions exist
    SELECT 'Weekly optimization completed' as Status;
END;

-- Monthly partition maintenance (runs first day of month at 1 AM)
CREATE EVENT IF NOT EXISTS monthly_partition_maintenance
ON SCHEDULE EVERY 1 MONTH
STARTS CONCAT(DATE_FORMAT(NOW() ,'%Y-%m-01') + INTERVAL 1 MONTH, ' 01:00:00')
DO
BEGIN
    -- Add partition for next year if we're in December
    IF MONTH(NOW()) = 12 THEN
        SET @next_year = YEAR(NOW()) + 1;
        CALL AddFuturePartition('detection_results', @next_year);
        CALL AddFuturePartition('alerts', @next_year);
        CALL AddFuturePartition('zone_action_logs', @next_year);
        
        -- Switch to VMS database
        USE construction_vms;
        CALL AddFuturePartition('video_storage', @next_year);
        USE construction_management;
    END IF;
    
    SELECT 'Monthly partition maintenance completed' as Status;
END;

-- Enable event scheduler
SET GLOBAL event_scheduler = ON;

-- Show created events
SHOW EVENTS WHERE Db IN ('construction_vms', 'construction_management');

SELECT 'Maintenance procedures and automated events created successfully!' as Status;