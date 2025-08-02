-- ================================================================
-- DATABASE CREATION SCRIPT
-- Construction Site AI Monitoring System
-- Version: 1.0
-- ================================================================

-- Set proper SQL modes
SET sql_mode = 'STRICT_TRANS_TABLES,NO_ZERO_DATE,NO_ZERO_IN_DATE,ERROR_FOR_DIVISION_BY_ZERO';

-- Enable event scheduler for maintenance tasks
SET GLOBAL event_scheduler = ON;

-- Create VMS/NVR System Database
CREATE DATABASE IF NOT EXISTS construction_vms 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci
COMMENT 'Video Management System - handles cameras, video storage, and recording';

-- Create Construction Management System Database
CREATE DATABASE IF NOT EXISTS construction_management 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci
COMMENT 'Construction AI Management - handles business logic, users, sites, and AI analysis';

-- Verify databases were created
SHOW DATABASES LIKE 'construction_%';

-- Display success message
SELECT 'Databases created successfully!' as Status;