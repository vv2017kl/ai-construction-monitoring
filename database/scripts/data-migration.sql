-- ================================================================
-- DATA MIGRATION UTILITIES
-- Construction Site AI Monitoring System
-- Version: 1.0
-- ================================================================

-- ================================================================
-- BACKUP UTILITIES
-- ================================================================

-- Create backup of critical tables before major changes
DELIMITER //

CREATE PROCEDURE CreateBackupTables()
BEGIN
    DECLARE backup_suffix VARCHAR(20);
    SET backup_suffix = DATE_FORMAT(NOW(), '%Y%m%d_%H%i%s');
    
    -- Construction Management backups
    USE construction_management;
    
    SET @sql = CONCAT('CREATE TABLE detection_results_backup_', backup_suffix, ' AS SELECT * FROM detection_results WHERE detection_timestamp >= DATE_SUB(NOW(), INTERVAL 7 DAY)');
    PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;
    
    SET @sql = CONCAT('CREATE TABLE alerts_backup_', backup_suffix, ' AS SELECT * FROM alerts WHERE triggered_at >= DATE_SUB(NOW(), INTERVAL 30 DAY)');
    PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;
    
    SET @sql = CONCAT('CREATE TABLE users_backup_', backup_suffix, ' AS SELECT * FROM users');
    PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;
    
    -- VMS backups
    USE construction_vms;
    
    SET @sql = CONCAT('CREATE TABLE cameras_backup_', backup_suffix, ' AS SELECT * FROM cameras');
    PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;
    
    SET @sql = CONCAT('CREATE TABLE video_storage_backup_', backup_suffix, ' AS SELECT * FROM video_storage WHERE start_time >= DATE_SUB(NOW(), INTERVAL 7 DAY)');
    PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;
    
    SELECT CONCAT('Backup tables created with suffix: ', backup_suffix) as Result;
END//

DELIMITER ;

-- ================================================================
-- DATA MIGRATION FROM EXTERNAL SYSTEMS
-- ================================================================

-- Template for migrating user data from external systems
DELIMITER //

CREATE PROCEDURE MigrateUsersFromExternal(
    IN source_table VARCHAR(64),
    IN company_uuid CHAR(36),
    IN default_role_uuid CHAR(36)
)
BEGIN
    DECLARE migration_count INT DEFAULT 0;
    
    -- Assuming external table structure: username, email, first_name, last_name, department
    SET @sql = CONCAT('
        INSERT INTO users (
            id, company_id, username, email, first_name, last_name, 
            department, password_hash, status, created_at
        )
        SELECT 
            UUID() as id,
            ''', company_uuid, ''' as company_id,
            username,
            email,
            first_name,
            last_name,
            department,
            ''$2b$12$defaulthash'' as password_hash,
            ''active'' as status,
            NOW() as created_at
        FROM ', source_table, '
        WHERE email NOT IN (SELECT email FROM users WHERE company_id = ''', company_uuid, ''')
    ');
    
    PREPARE stmt FROM @sql;
    EXECUTE stmt;
    SET migration_count = ROW_COUNT();
    DEALLOCATE PREPARE stmt;
    
    SELECT CONCAT('Migrated ', migration_count, ' users from external system') as Result;
END//

DELIMITER ;

-- ================================================================
-- DATA VALIDATION AND CLEANUP
-- ================================================================

-- Validate data integrity across tables
DELIMITER //

CREATE PROCEDURE ValidateDataIntegrity()
BEGIN
    DECLARE validation_errors INT DEFAULT 0;
    DECLARE error_details TEXT DEFAULT '';
    
    -- Check for users without valid companies
    SELECT COUNT(*) INTO @temp_count
    FROM users u 
    LEFT JOIN companies c ON u.company_id = c.id 
    WHERE c.id IS NULL;
    
    IF @temp_count > 0 THEN
        SET validation_errors = validation_errors + @temp_count;
        SET error_details = CONCAT(error_details, @temp_count, ' users without valid companies; ');
    END IF;
    
    -- Check for sites without valid groups
    SELECT COUNT(*) INTO @temp_count
    FROM sites s 
    LEFT JOIN groups g ON s.group_id = g.id 
    WHERE g.id IS NULL;
    
    IF @temp_count > 0 THEN
        SET validation_errors = validation_errors + @temp_count;
        SET error_details = CONCAT(error_details, @temp_count, ' sites without valid groups; ');
    END IF;
    
    -- Check for detection results without valid sites
    SELECT COUNT(*) INTO @temp_count
    FROM detection_results dr 
    LEFT JOIN sites s ON dr.site_id = s.id 
    WHERE s.id IS NULL;
    
    IF @temp_count > 0 THEN
        SET validation_errors = validation_errors + @temp_count;
        SET error_details = CONCAT(error_details, @temp_count, ' detection results without valid sites; ');
    END IF;
    
    -- Report results
    IF validation_errors = 0 THEN
        SELECT 'Data integrity validation passed - no errors found' as Result;
    ELSE
        SELECT CONCAT('Data integrity validation found ', validation_errors, ' errors: ', error_details) as Result;
    END IF;
END//

DELIMITER ;

-- ================================================================
-- SYSTEM UPGRADE UTILITIES
-- ================================================================

-- Handle schema version upgrades
DELIMITER //

CREATE PROCEDURE UpgradeSchemaVersion(IN target_version VARCHAR(10))
BEGIN
    DECLARE current_version VARCHAR(10) DEFAULT '1.0';
    
    -- Get current version from system configurations
    SELECT JSON_UNQUOTE(config_value) INTO current_version
    FROM system_configurations 
    WHERE config_key = 'schema_version'
    LIMIT 1;
    
    IF current_version IS NULL THEN
        SET current_version = '1.0';
        INSERT INTO system_configurations (id, config_key, config_value, description, category)
        VALUES (UUID(), 'schema_version', '"1.0"', 'Database schema version', 'system');
    END IF;
    
    -- Version-specific upgrade logic would go here
    CASE target_version
        WHEN '1.1' THEN
            -- Example: Add new columns or indexes for version 1.1
            -- ALTER TABLE detection_results ADD COLUMN new_field VARCHAR(100);
            SELECT 'Upgrading to version 1.1 - no changes required yet' as Status;
            
        WHEN '1.2' THEN
            -- Example: Version 1.2 changes
            SELECT 'Upgrading to version 1.2 - no changes required yet' as Status;
            
        ELSE
            SELECT CONCAT('Unknown target version: ', target_version) as Error;
    END CASE;
    
    -- Update version in configurations
    UPDATE system_configurations 
    SET config_value = JSON_QUOTE(target_version), updated_at = NOW()
    WHERE config_key = 'schema_version';
    
    SELECT CONCAT('Schema upgraded from version ', current_version, ' to ', target_version) as Result;
END//

DELIMITER ;

-- ================================================================
-- DATA EXPORT UTILITIES
-- ================================================================

-- Export data for reporting or external system integration
DELIMITER //

CREATE PROCEDURE ExportComplianceData(
    IN site_uuid CHAR(36),
    IN start_date DATE,
    IN end_date DATE
)
BEGIN
    DECLARE export_table_name VARCHAR(100);
    SET export_table_name = CONCAT('compliance_export_', DATE_FORMAT(NOW(), '%Y%m%d_%H%i%s'));
    
    SET @sql = CONCAT('
        CREATE TABLE ', export_table_name, ' AS
        SELECT 
            s.name as site_name,
            s.site_code,
            DATE(dr.detection_timestamp) as detection_date,
            COUNT(*) as total_detections,
            SUM(dr.personnel_count) as total_personnel_detected,
            SUM(dr.ppe_violations_detected) as total_ppe_violations,
            ROUND(AVG(JSON_EXTRACT(dr.ppe_compliance, "$.overall_compliance")), 4) as avg_compliance_rate,
            COUNT(DISTINCT dr.camera_id) as cameras_active
        FROM detection_results dr
        JOIN sites s ON dr.site_id = s.id
        WHERE dr.site_id = ''', site_uuid, '''
        AND DATE(dr.detection_timestamp) BETWEEN ''', start_date, ''' AND ''', end_date, '''
        GROUP BY s.name, s.site_code, DATE(dr.detection_timestamp)
        ORDER BY detection_date DESC
    ');
    
    PREPARE stmt FROM @sql;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;
    
    SELECT CONCAT('Compliance data exported to table: ', export_table_name) as Result;
    
    -- Optionally export to CSV file
    SET @export_sql = CONCAT('
        SELECT * FROM ', export_table_name, '
        INTO OUTFILE ''/tmp/compliance_export_', DATE_FORMAT(NOW(), '%Y%m%d_%H%i%s'), '.csv''
        FIELDS TERMINATED BY '',''
        OPTIONALLY ENCLOSED BY ''"''
        LINES TERMINATED BY ''\n''
    ');
    
    -- Note: This would require FILE privilege and secure_file_priv configuration
END//

DELIMITER ;

-- ================================================================
-- DATA ANONYMIZATION FOR TESTING
-- ================================================================

-- Create anonymized dataset for testing environments
DELIMITER //

CREATE PROCEDURE AnonymizeDataForTesting()
BEGIN
    -- Create anonymized users
    UPDATE users SET 
        email = CONCAT('user', id, '@testdomain.com'),
        phone = CONCAT('555-', LPAD(FLOOR(RAND() * 10000), 4, '0')),
        first_name = CONCAT('Test', SUBSTRING(id, 1, 4)),
        last_name = CONCAT('User', SUBSTRING(id, -4)),
        emergency_contact_name = 'Emergency Contact',
        emergency_contact_phone = '555-9999'
    WHERE status = 'active';
    
    -- Anonymize company information
    UPDATE companies SET
        name = CONCAT('Test Company ', SUBSTRING(id, 1, 8)),
        legal_name = CONCAT('Test Company ', SUBSTRING(id, 1, 8), ' LLC'),
        headquarters_address = '123 Test Street, Test City, TS 12345',
        phone = '555-TEST',
        email = CONCAT('contact@testcompany', SUBSTRING(id, 1, 4), '.com');
    
    -- Anonymize site information
    UPDATE sites SET
        address = CONCAT('Test Construction Site ', SUBSTRING(id, 1, 8)),
        site_phone = '555-SITE',
        site_email = CONCAT('site', SUBSTRING(id, 1, 4), '@testdomain.com');
    
    SELECT 'Data anonymized for testing environment' as Result;
END//

DELIMITER ;

-- Show all created procedures
SELECT 'Data migration utilities created successfully!' as Status;
SHOW PROCEDURE STATUS WHERE Db IN ('construction_vms', 'construction_management');