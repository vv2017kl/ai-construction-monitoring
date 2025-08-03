-- ================================================================
-- COMPLETE VMS/NVR SYSTEM SCHEMA
-- Construction Site AI Monitoring System - VMS Database
-- Version: 1.0
-- Tables: 12 (COMPLETE)
-- ================================================================

USE construction_vms;

-- ================================================================
-- TABLE 1: CAMERA MANUFACTURERS
-- ================================================================
CREATE TABLE camera_manufacturers (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    name VARCHAR(100) NOT NULL UNIQUE,
    display_name VARCHAR(150) NOT NULL,
    website_url VARCHAR(255),
    support_contact VARCHAR(255),
    api_documentation_url VARCHAR(255),
    default_protocols JSON COMMENT 'Supported protocols: ONVIF, RTSP, HTTP',
    status ENUM('active', 'deprecated', 'discontinued') DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_manufacturer_status (status),
    INDEX idx_manufacturer_name (name)
) ENGINE=InnoDB COMMENT='Camera manufacturers and vendor information';

-- ================================================================
-- TABLE 2: CAMERA MODELS
-- ================================================================
CREATE TABLE camera_models (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    manufacturer_id CHAR(36) NOT NULL,
    model_number VARCHAR(100) NOT NULL,
    model_name VARCHAR(150) NOT NULL,
    category ENUM('fixed', 'ptz', 'dome', 'bullet', 'fisheye', '360', 'thermal') NOT NULL,
    
    -- Technical specifications
    max_resolution VARCHAR(20) COMMENT 'e.g., 4K, 1080p, 720p',
    supported_codecs JSON COMMENT 'H.264, H.265, MJPEG',
    frame_rates JSON COMMENT 'Supported frame rates',
    lens_specifications JSON COMMENT 'Focal length, angle of view',
    night_vision BOOLEAN DEFAULT FALSE,
    ir_range_meters INT,
    ptz_capabilities JSON COMMENT 'Pan, tilt, zoom ranges',
    
    -- Network and power
    power_consumption_watts DECIMAL(5,2),
    power_requirements VARCHAR(50) COMMENT 'PoE+, 12V DC, 24V AC',
    network_interfaces JSON COMMENT 'Ethernet, WiFi, etc.',
    
    -- Environmental
    operating_temperature_min INT COMMENT 'Celsius',
    operating_temperature_max INT COMMENT 'Celsius',
    ip_rating VARCHAR(10) COMMENT 'IP65, IP67, etc.',
    
    -- API and control
    default_api_settings JSON COMMENT 'Default API endpoints and methods',
    configuration_schema JSON COMMENT 'Available configuration parameters',
    
    status ENUM('active', 'discontinued') DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (manufacturer_id) REFERENCES camera_manufacturers(id) ON DELETE RESTRICT,
    UNIQUE KEY uk_model_manufacturer (manufacturer_id, model_number),
    INDEX idx_model_category (category),
    INDEX idx_model_status (status)
) ENGINE=InnoDB COMMENT='Camera models and technical specifications';

-- ================================================================
-- TABLE 3: CAMERAS
-- ================================================================
CREATE TABLE cameras (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    camera_identifier VARCHAR(100) NOT NULL UNIQUE COMMENT 'Human-readable camera ID',
    name VARCHAR(150) NOT NULL,
    description TEXT,
    
    -- Hardware information
    manufacturer_id CHAR(36) NOT NULL,
    model_id CHAR(36) NOT NULL,
    serial_number VARCHAR(100),
    mac_address VARCHAR(17),
    firmware_version VARCHAR(50),
    
    -- Network configuration
    ip_address VARCHAR(45) NOT NULL COMMENT 'IPv4 or IPv6',
    port INT DEFAULT 554,
    username VARCHAR(100),
    password_hash VARCHAR(255) COMMENT 'Encrypted password',
    
    -- Stream configuration
    primary_stream_url VARCHAR(500) NOT NULL,
    secondary_stream_url VARCHAR(500),
    snapshot_url VARCHAR(500),
    
    -- Physical installation
    installation_date DATE,
    installation_notes TEXT,
    location_description VARCHAR(255),
    mounting_type ENUM('wall', 'ceiling', 'pole', 'mobile') DEFAULT 'wall',
    height_meters DECIMAL(4,2),
    
    -- Positioning (for site map overlay)
    map_x DECIMAL(10,6) COMMENT 'X coordinate on site map',
    map_y DECIMAL(10,6) COMMENT 'Y coordinate on site map', 
    map_rotation DECIMAL(5,2) DEFAULT 0 COMMENT 'Camera rotation in degrees',
    field_of_view_degrees DECIMAL(5,2),
    
    -- Operational status
    status ENUM('active', 'inactive', 'maintenance', 'failed') DEFAULT 'active',
    last_seen_at TIMESTAMP NULL,
    health_status JSON COMMENT 'Stream quality, connectivity, etc.',
    
    -- Configuration
    current_settings JSON COMMENT 'Current camera configuration',
    recording_enabled BOOLEAN DEFAULT TRUE,
    motion_detection_enabled BOOLEAN DEFAULT TRUE,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (manufacturer_id) REFERENCES camera_manufacturers(id) ON DELETE RESTRICT,
    FOREIGN KEY (model_id) REFERENCES camera_models(id) ON DELETE RESTRICT,
    INDEX idx_camera_status (status),
    INDEX idx_camera_ip (ip_address),
    INDEX idx_camera_identifier (camera_identifier),
    INDEX idx_camera_last_seen (last_seen_at)
) ENGINE=InnoDB COMMENT='Physical cameras and their configurations';

-- ================================================================
-- TABLE 4: CAMERA CONFIGURATIONS
-- ================================================================
CREATE TABLE camera_configurations (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    camera_id CHAR(36) NOT NULL,
    configuration_name VARCHAR(100) NOT NULL,
    is_active BOOLEAN DEFAULT FALSE,
    
    -- Configuration data
    video_settings JSON COMMENT 'Resolution, bitrate, frame rate',
    audio_settings JSON COMMENT 'Audio codec, bitrate if supported',
    image_settings JSON COMMENT 'Brightness, contrast, saturation',
    network_settings JSON COMMENT 'RTSP, HTTP, multicast settings',
    motion_detection_settings JSON COMMENT 'Sensitivity, zones, actions',
    ptz_settings JSON COMMENT 'PTZ presets, patrol routes',
    recording_settings JSON COMMENT 'Resolution, quality for recording',
    alert_settings JSON COMMENT 'Motion alerts, tampering detection',
    privacy_mask_settings JSON COMMENT 'Privacy mask coordinates',
    overlay_settings JSON COMMENT 'Text overlays, timestamp settings',
    
    -- Version control
    version_number INT DEFAULT 1,
    applied_at TIMESTAMP NULL,
    applied_by VARCHAR(100),
    application_status ENUM('pending', 'applied', 'failed', 'rolled_back') DEFAULT 'pending',
    application_error TEXT,
    
    -- Backup and restore
    previous_config_id CHAR(36) NULL COMMENT 'Reference to previous configuration',
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (camera_id) REFERENCES cameras(id) ON DELETE CASCADE,
    FOREIGN KEY (previous_config_id) REFERENCES camera_configurations(id) ON DELETE SET NULL,
    UNIQUE KEY uk_camera_active_config (camera_id, is_active),
    INDEX idx_config_status (application_status),
    INDEX idx_config_applied_at (applied_at)
) ENGINE=InnoDB COMMENT='Camera configuration versions and settings';

-- ================================================================
-- TABLE 5: CAMERA API ENDPOINTS
-- ================================================================
CREATE TABLE camera_api_endpoints (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    camera_id CHAR(36) NOT NULL,
    endpoint_type ENUM('configuration', 'control', 'status', 'streaming', 'recording') NOT NULL,
    
    -- API details
    method ENUM('GET', 'POST', 'PUT', 'DELETE', 'PATCH') NOT NULL,
    url_template VARCHAR(500) NOT NULL COMMENT 'Template with placeholders',
    headers JSON COMMENT 'Required headers for the request',
    authentication JSON COMMENT 'Auth type and parameters',
    
    -- Request/Response format
    request_schema JSON COMMENT 'Expected request format',
    response_schema JSON COMMENT 'Expected response format',
    
    -- Error handling
    retry_attempts INT DEFAULT 3,
    timeout_seconds INT DEFAULT 30,
    rate_limit_per_minute INT DEFAULT 60,
    
    -- Status
    is_enabled BOOLEAN DEFAULT TRUE,
    last_tested_at TIMESTAMP NULL,
    test_status ENUM('success', 'failed', 'not_tested') DEFAULT 'not_tested',
    test_error TEXT,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (camera_id) REFERENCES cameras(id) ON DELETE CASCADE,
    INDEX idx_endpoint_type (endpoint_type),
    INDEX idx_endpoint_camera (camera_id, endpoint_type)
) ENGINE=InnoDB COMMENT='Camera API endpoints for control and configuration';

-- ================================================================
-- TABLE 6: VIDEO STORAGE
-- ================================================================
CREATE TABLE video_storage (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    camera_id CHAR(36) NOT NULL,
    
    -- File information
    filename VARCHAR(255) NOT NULL,
    file_path VARCHAR(1000) NOT NULL COMMENT 'Full path including storage mount point',
    storage_location VARCHAR(100) NOT NULL COMMENT 'S3 bucket, disk mount, etc.',
    file_size_bytes BIGINT NOT NULL,
    
    -- Time range
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP NOT NULL,
    duration_seconds INT GENERATED ALWAYS AS (TIMESTAMPDIFF(SECOND, start_time, end_time)) STORED,
    
    -- Video properties
    video_codec VARCHAR(20) NOT NULL,
    resolution VARCHAR(20) NOT NULL,
    frame_rate DECIMAL(5,2) NOT NULL,
    bitrate_kbps INT,
    
    -- Chunking information
    chunk_sequence INT NOT NULL DEFAULT 1,
    parent_recording_id CHAR(36) NULL COMMENT 'Groups chunks from same recording session',
    
    -- Recording metadata
    recording_trigger ENUM('scheduled', 'motion', 'manual', 'alert', 'continuous') NOT NULL,
    recording_quality ENUM('high', 'medium', 'low') DEFAULT 'medium',
    
    -- Storage optimization
    compression_level ENUM('none', 'low', 'medium', 'high') DEFAULT 'medium',
    is_archived BOOLEAN DEFAULT FALSE,
    archive_date TIMESTAMP NULL,
    
    -- Access tracking
    access_count INT DEFAULT 0,
    last_accessed_at TIMESTAMP NULL,
    
    -- Status
    status ENUM('recording', 'completed', 'corrupted', 'archived', 'deleted') DEFAULT 'completed',
    checksum VARCHAR(64) COMMENT 'File integrity checksum',
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (camera_id) REFERENCES cameras(id) ON DELETE CASCADE,
    FOREIGN KEY (parent_recording_id) REFERENCES video_storage(id) ON DELETE SET NULL,
    INDEX idx_video_camera_time (camera_id, start_time, end_time),
    INDEX idx_video_time_range (start_time, end_time),
    INDEX idx_video_status (status),
    INDEX idx_video_storage_location (storage_location),
    INDEX idx_video_archived (is_archived, archive_date)
) ENGINE=InnoDB COMMENT='Video file storage and metadata';

-- ================================================================
-- TABLE 7: VIDEO ENCODERS
-- ================================================================
CREATE TABLE video_encoders (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    name VARCHAR(100) NOT NULL UNIQUE,
    encoder_type ENUM('hardware', 'software') NOT NULL,
    
    -- Capabilities
    supported_codecs JSON NOT NULL COMMENT 'H.264, H.265, MJPEG',
    max_concurrent_streams INT NOT NULL,
    supported_resolutions JSON NOT NULL,
    supported_frame_rates JSON NOT NULL,
    
    -- Hardware information (if applicable)
    hardware_model VARCHAR(100),
    gpu_model VARCHAR(100),
    cuda_cores INT,
    memory_gb INT,
    
    -- Performance metrics
    avg_encoding_time_ms DECIMAL(8,2),
    max_throughput_mbps DECIMAL(8,2),
    
    -- Configuration
    default_settings JSON COMMENT 'Default encoding parameters',
    optimization_profiles JSON COMMENT 'Preset configurations for different scenarios',
    
    -- Status
    status ENUM('active', 'inactive', 'maintenance', 'failed') DEFAULT 'active',
    current_load_percentage DECIMAL(5,2) DEFAULT 0.00,
    last_health_check TIMESTAMP NULL,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_encoder_status (status),
    INDEX idx_encoder_type (encoder_type),
    INDEX idx_encoder_load (current_load_percentage)
) ENGINE=InnoDB COMMENT='Video encoding hardware and software';

-- ================================================================
-- TABLE 8: RECORDING POLICIES
-- ================================================================
CREATE TABLE recording_policies (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    
    -- Schedule configuration
    schedule_type ENUM('continuous', 'scheduled', 'motion_triggered', 'event_triggered') NOT NULL,
    schedule_config JSON COMMENT 'Time ranges, days of week, etc.',
    
    -- Recording parameters
    recording_quality ENUM('high', 'medium', 'low') DEFAULT 'medium',
    max_duration_minutes INT COMMENT 'Maximum single recording duration',
    pre_event_seconds INT DEFAULT 10 COMMENT 'Seconds to record before trigger',
    post_event_seconds INT DEFAULT 30 COMMENT 'Seconds to record after trigger',
    
    -- Retention settings
    retention_days INT NOT NULL DEFAULT 30,
    archive_after_days INT COMMENT 'Move to archive storage after X days',
    delete_after_days INT COMMENT 'Permanent deletion after X days',
    
    -- Storage settings
    storage_location VARCHAR(100) NOT NULL DEFAULT 'primary',
    compression_enabled BOOLEAN DEFAULT TRUE,
    encryption_enabled BOOLEAN DEFAULT FALSE,
    
    -- Triggers
    motion_sensitivity ENUM('low', 'medium', 'high') DEFAULT 'medium',
    motion_zones JSON COMMENT 'Specific areas to monitor for motion',
    trigger_events JSON COMMENT 'Events that should trigger recording',
    
    -- Notifications
    notification_enabled BOOLEAN DEFAULT FALSE,
    notification_recipients JSON COMMENT 'Email addresses, webhooks, etc.',
    
    -- Priority and resource management
    priority ENUM('low', 'medium', 'high', 'critical') DEFAULT 'medium',
    max_bandwidth_mbps DECIMAL(8,2) COMMENT 'Bandwidth limit for this policy',
    
    -- Status
    is_active BOOLEAN DEFAULT TRUE,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_policy_active (is_active),
    INDEX idx_policy_schedule_type (schedule_type),
    INDEX idx_policy_priority (priority)
) ENGINE=InnoDB COMMENT='Recording policies and schedules';

-- ================================================================
-- TABLE 9: PERFORMANCE METRICS
-- ================================================================
CREATE TABLE performance_metrics (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    metric_timestamp TIMESTAMP NOT NULL,
    metric_type ENUM('system', 'camera', 'encoder', 'storage', 'network') NOT NULL,
    entity_id CHAR(36) COMMENT 'ID of camera, encoder, etc.',
    
    -- System metrics
    cpu_usage_percentage DECIMAL(5,2),
    memory_usage_percentage DECIMAL(5,2),
    disk_usage_percentage DECIMAL(5,2),
    network_usage_mbps DECIMAL(8,2),
    
    -- Camera-specific metrics
    stream_bitrate_kbps INT,
    frame_rate_actual DECIMAL(5,2),
    dropped_frames_count INT,
    connection_status ENUM('connected', 'disconnected', 'unstable'),
    
    -- Encoder metrics
    encoding_queue_size INT,
    average_encoding_time_ms DECIMAL(8,2),
    encoder_temperature_celsius DECIMAL(5,2),
    
    -- Storage metrics
    write_speed_mbps DECIMAL(8,2),
    read_speed_mbps DECIMAL(8,2),
    available_space_gb BIGINT,
    total_space_gb BIGINT,
    
    -- Custom metrics
    custom_metrics JSON COMMENT 'Additional metrics as key-value pairs',
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_metrics_timestamp (metric_timestamp),
    INDEX idx_metrics_type_entity (metric_type, entity_id),
    INDEX idx_metrics_entity_time (entity_id, metric_timestamp)
) ENGINE=InnoDB COMMENT='System performance metrics and monitoring';

-- ================================================================
-- TABLE 10: SYSTEM CONFIGURATIONS
-- ================================================================
CREATE TABLE system_configurations (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    config_key VARCHAR(100) NOT NULL UNIQUE,
    config_value JSON NOT NULL,
    
    -- Metadata
    description TEXT,
    category VARCHAR(50) NOT NULL DEFAULT 'general',
    data_type ENUM('string', 'integer', 'boolean', 'json', 'array') NOT NULL,
    
    -- Validation
    validation_rules JSON COMMENT 'Validation constraints for the value',
    default_value JSON,
    
    -- Security
    is_sensitive BOOLEAN DEFAULT FALSE COMMENT 'Contains passwords, keys, etc.',
    requires_restart BOOLEAN DEFAULT FALSE COMMENT 'System restart required after change',
    
    -- Change tracking
    previous_value JSON,
    changed_by VARCHAR(100),
    changed_at TIMESTAMP NULL,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_config_category (category),
    INDEX idx_config_sensitive (is_sensitive)
) ENGINE=InnoDB COMMENT='System configuration parameters';

-- ================================================================
-- TABLE 11: AUDIT LOGS
-- ================================================================
CREATE TABLE audit_logs (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    action_timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    -- User and action information
    user_id VARCHAR(100) COMMENT 'User who performed the action',
    user_ip VARCHAR(45) COMMENT 'IP address of the user',
    action_type ENUM('create', 'read', 'update', 'delete', 'login', 'logout', 'configure') NOT NULL,
    resource_type VARCHAR(50) NOT NULL COMMENT 'camera, video, configuration, etc.',
    resource_id CHAR(36) COMMENT 'ID of the affected resource',
    
    -- Action details
    action_description TEXT NOT NULL,
    old_values JSON COMMENT 'Previous values before change',
    new_values JSON COMMENT 'New values after change',
    
    -- Request context
    request_method VARCHAR(10),
    request_url VARCHAR(500),
    request_headers JSON,
    response_status INT,
    
    -- System context
    system_component VARCHAR(50) DEFAULT 'vms',
    severity ENUM('low', 'medium', 'high', 'critical') DEFAULT 'medium',
    
    INDEX idx_audit_timestamp (action_timestamp),
    INDEX idx_audit_user (user_id),
    INDEX idx_audit_resource (resource_type, resource_id),
    INDEX idx_audit_action_type (action_type),
    INDEX idx_audit_severity (severity)
) ENGINE=InnoDB COMMENT='Audit trail for all VMS operations';

-- ================================================================
-- TABLE 12: API ACCESS LOGS
-- ================================================================
CREATE TABLE api_access_logs (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    request_timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    -- Request information
    method ENUM('GET', 'POST', 'PUT', 'DELETE', 'PATCH') NOT NULL,
    endpoint VARCHAR(500) NOT NULL,
    query_parameters JSON,
    request_headers JSON,
    request_body_size INT,
    
    -- Client information
    client_ip VARCHAR(45) NOT NULL,
    user_agent TEXT,
    api_key_hash VARCHAR(64) COMMENT 'Hashed API key for identification',
    user_id VARCHAR(100),
    
    -- Response information
    response_status INT NOT NULL,
    response_time_ms INT NOT NULL,
    response_size_bytes INT,
    
    -- Error information
    error_message TEXT,
    error_code VARCHAR(50),
    
    -- Rate limiting
    rate_limit_remaining INT,
    rate_limit_reset_time TIMESTAMP,
    
    INDEX idx_api_timestamp (request_timestamp),
    INDEX idx_api_endpoint (endpoint(100)),
    INDEX idx_api_client_ip (client_ip),
    INDEX idx_api_status (response_status),
    INDEX idx_api_user (user_id),
    INDEX idx_api_response_time (response_time_ms)
) ENGINE=InnoDB COMMENT='API access logs and performance tracking';

-- ================================================================
-- VERIFICATION
-- ================================================================
SELECT 'VMS Schema (12 tables) created successfully!' as Status;

-- Show all created tables
SHOW TABLES;