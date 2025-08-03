-- ================================================================
-- CONSTRUCTION MANAGEMENT SCHEMA - PART 2 (Advanced Tables)
-- Tables 4-23: Users, Roles, AI, Detection, Alerts, Zones, etc.
-- ================================================================

USE construction_management;

-- ================================================================
-- TABLE 4: ROLES  
-- ================================================================
CREATE TABLE roles (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    company_id CHAR(36) NOT NULL,
    name VARCHAR(100) NOT NULL,
    display_name VARCHAR(150) NOT NULL,
    description TEXT,
    
    -- Hierarchy and permissions
    role_level INT NOT NULL COMMENT '1=SYSADMIN, 2=COMPANY_EXEC, 3=GROUP_MANAGER, 4=SITE_MANAGER, 5=SITE_COORDINATOR',
    permissions JSON NOT NULL COMMENT 'Array of permission strings',
    
    -- Scope restrictions
    can_access_all_sites BOOLEAN DEFAULT FALSE,
    can_access_all_groups BOOLEAN DEFAULT FALSE,
    can_manage_users BOOLEAN DEFAULT FALSE,
    can_configure_system BOOLEAN DEFAULT FALSE,
    can_view_financials BOOLEAN DEFAULT FALSE,
    
    -- Dashboard and UI permissions
    allowed_dashboard_sections JSON COMMENT 'Which dashboard sections this role can access',
    allowed_features JSON COMMENT 'Specific feature permissions',
    
    -- Data access permissions
    can_export_data BOOLEAN DEFAULT FALSE,
    can_delete_data BOOLEAN DEFAULT FALSE,
    data_retention_days INT COMMENT 'How long this role can access historical data',
    
    -- Mobile and field permissions
    mobile_access_enabled BOOLEAN DEFAULT FALSE,
    field_assessment_access BOOLEAN DEFAULT FALSE,
    can_create_field_reports BOOLEAN DEFAULT FALSE,
    
    -- Status
    is_system_role BOOLEAN DEFAULT FALSE COMMENT 'True for built-in system roles',
    status ENUM('active', 'inactive') DEFAULT 'active',
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (company_id) REFERENCES companies(id) ON DELETE CASCADE,
    UNIQUE KEY uk_role_name (company_id, name),
    INDEX idx_role_company (company_id),
    INDEX idx_role_level (role_level),
    INDEX idx_role_status (status)
) ENGINE=InnoDB COMMENT='User roles and permissions';

-- ================================================================
-- TABLE 5: USERS
-- ================================================================
CREATE TABLE users (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    company_id CHAR(36) NOT NULL,
    
    -- Basic information
    username VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL,
    phone VARCHAR(20),
    
    -- Personal information
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    middle_name VARCHAR(100),
    display_name VARCHAR(200),
    
    -- Authentication
    password_hash VARCHAR(255) NOT NULL,
    password_salt VARCHAR(100),
    password_changed_at TIMESTAMP NULL,
    failed_login_attempts INT DEFAULT 0,
    locked_until TIMESTAMP NULL,
    
    -- Two-factor authentication
    two_factor_enabled BOOLEAN DEFAULT FALSE,
    two_factor_secret VARCHAR(100),
    backup_codes JSON,
    
    -- Employment information
    employee_id VARCHAR(50),
    department VARCHAR(100),
    job_title VARCHAR(150),
    hire_date DATE,
    supervisor_user_id CHAR(36),
    
    -- Organizational access
    default_site_id CHAR(36) COMMENT 'User''s primary/home site',
    accessible_sites JSON COMMENT 'Array of site IDs user can access',
    accessible_groups JSON COMMENT 'Array of group IDs user can access',
    
    -- Contact and emergency
    emergency_contact_name VARCHAR(200),
    emergency_contact_phone VARCHAR(20),
    emergency_contact_relationship VARCHAR(50),
    
    -- Preferences and settings
    language VARCHAR(10) DEFAULT 'en',
    timezone VARCHAR(50) DEFAULT 'UTC',
    notification_preferences JSON,
    ui_preferences JSON,
    
    -- Mobile and field access
    mobile_device_id VARCHAR(100),
    field_access_enabled BOOLEAN DEFAULT FALSE,
    tablet_assigned VARCHAR(100),
    
    -- Training and certifications
    safety_training_completed BOOLEAN DEFAULT FALSE,
    safety_training_date DATE,
    certifications JSON COMMENT 'Safety certifications and expiry dates',
    
    -- Session management
    last_login_at TIMESTAMP NULL,
    last_activity_at TIMESTAMP NULL,
    current_session_id VARCHAR(100),
    
    -- Status and flags
    status ENUM('active', 'inactive', 'suspended', 'terminated') DEFAULT 'active',
    email_verified BOOLEAN DEFAULT FALSE,
    phone_verified BOOLEAN DEFAULT FALSE,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (company_id) REFERENCES companies(id) ON DELETE CASCADE,
    FOREIGN KEY (supervisor_user_id) REFERENCES users(id) ON DELETE SET NULL,
    FOREIGN KEY (default_site_id) REFERENCES sites(id) ON DELETE SET NULL,
    UNIQUE KEY uk_user_username (company_id, username),
    UNIQUE KEY uk_user_email (company_id, email),
    INDEX idx_user_company (company_id),
    INDEX idx_user_status (status),
    INDEX idx_user_email (email),
    INDEX idx_user_employee_id (employee_id),
    INDEX idx_user_last_login (last_login_at),
    INDEX idx_user_supervisor (supervisor_user_id)
) ENGINE=InnoDB COMMENT='System users with hierarchical roles';

-- ================================================================
-- TABLE 6: USER_ROLES
-- ================================================================
CREATE TABLE user_roles (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    user_id CHAR(36) NOT NULL,
    role_id CHAR(36) NOT NULL,
    
    -- Scope limitations
    assigned_site_ids JSON COMMENT 'Specific sites this role assignment applies to',
    assigned_group_ids JSON COMMENT 'Specific groups this role assignment applies to',
    
    -- Assignment details
    assigned_by_user_id CHAR(36) NOT NULL,
    assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    effective_from DATE NOT NULL,
    effective_until DATE NULL COMMENT 'Null means no expiry',
    
    -- Assignment context
    assignment_reason TEXT,
    assignment_notes TEXT,
    
    -- Status
    status ENUM('active', 'suspended', 'expired', 'revoked') DEFAULT 'active',
    revoked_by_user_id CHAR(36) NULL,
    revoked_at TIMESTAMP NULL,
    revocation_reason TEXT,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE,
    FOREIGN KEY (assigned_by_user_id) REFERENCES users(id) ON DELETE RESTRICT,
    FOREIGN KEY (revoked_by_user_id) REFERENCES users(id) ON DELETE SET NULL,
    UNIQUE KEY uk_user_role_active (user_id, role_id, status),
    INDEX idx_user_role_user (user_id),
    INDEX idx_user_role_role (role_id),
    INDEX idx_user_role_status (status),
    INDEX idx_user_role_effective (effective_from, effective_until)
) ENGINE=InnoDB COMMENT='User role assignments with scope and temporal controls';

-- ================================================================
-- TABLE 7: USER_SESSIONS
-- ================================================================
CREATE TABLE user_sessions (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    user_id CHAR(36) NOT NULL,
    session_token VARCHAR(255) NOT NULL UNIQUE,
    
    -- Session details
    ip_address VARCHAR(45) NOT NULL,
    user_agent TEXT,
    device_fingerprint VARCHAR(255),
    
    -- Location and context
    login_location VARCHAR(100) COMMENT 'City, Country from IP geolocation',
    device_type ENUM('desktop', 'mobile', 'tablet', 'unknown') DEFAULT 'unknown',
    browser VARCHAR(100),
    operating_system VARCHAR(100),
    
    -- Session lifecycle
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_activity_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NOT NULL,
    
    -- Security flags
    is_suspicious BOOLEAN DEFAULT FALSE,
    security_flags JSON COMMENT 'Security-related metadata',
    
    -- Status
    status ENUM('active', 'expired', 'terminated', 'suspicious') DEFAULT 'active',
    terminated_by_user_id CHAR(36) NULL,
    termination_reason VARCHAR(255),
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (terminated_by_user_id) REFERENCES users(id) ON DELETE SET NULL,
    INDEX idx_session_user (user_id),
    INDEX idx_session_token (session_token),
    INDEX idx_session_status (status),
    INDEX idx_session_expires (expires_at),
    INDEX idx_session_activity (last_activity_at)
) ENGINE=InnoDB COMMENT='User session management and tracking';

-- ================================================================
-- TABLE 8: SITE_COORDINATES
-- ================================================================
CREATE TABLE site_coordinates (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    site_id CHAR(36) NOT NULL,
    
    -- Coordinate information
    coordinate_type ENUM('boundary', 'entrance', 'building', 'hazard', 'utility', 'landmark', 'camera_position') NOT NULL,
    name VARCHAR(150) NOT NULL,
    description TEXT,
    
    -- Geographic position
    latitude DECIMAL(10, 7) NOT NULL,
    longitude DECIMAL(10, 7) NOT NULL,
    elevation_meters DECIMAL(8, 2),
    
    -- Map display properties
    map_x DECIMAL(10, 6) COMMENT 'X coordinate on site map overlay',
    map_y DECIMAL(10, 6) COMMENT 'Y coordinate on site map overlay',
    map_layer VARCHAR(50) DEFAULT 'default',
    display_priority INT DEFAULT 1,
    
    -- Visual properties
    icon_type VARCHAR(50),
    icon_color VARCHAR(20),
    icon_size ENUM('small', 'medium', 'large') DEFAULT 'medium',
    
    -- Additional metadata
    properties JSON COMMENT 'Custom properties specific to coordinate type',
    
    -- Relationships
    related_camera_id CHAR(36) COMMENT 'Camera ID from VMS system (application-level reference)',
    parent_coordinate_id CHAR(36) COMMENT 'For grouped coordinates',
    
    -- Status
    status ENUM('active', 'inactive', 'temporary') DEFAULT 'active',
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (site_id) REFERENCES sites(id) ON DELETE CASCADE,
    FOREIGN KEY (parent_coordinate_id) REFERENCES site_coordinates(id) ON DELETE SET NULL,
    INDEX idx_coordinate_site (site_id),
    INDEX idx_coordinate_type (coordinate_type),
    INDEX idx_coordinate_position (latitude, longitude),
    INDEX idx_coordinate_map (map_x, map_y),
    INDEX idx_coordinate_camera (related_camera_id),
    INDEX idx_coordinate_status (status)
) ENGINE=InnoDB COMMENT='Geographic coordinates and map markers for sites';

-- ================================================================
-- TABLE 9: SITE_ZONES
-- ================================================================
CREATE TABLE site_zones (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    site_id CHAR(36) NOT NULL,
    
    -- Zone identification
    zone_code VARCHAR(50) NOT NULL,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    
    -- Zone type and purpose
    zone_type ENUM('safety', 'restricted', 'work_area', 'storage', 'equipment', 'pedestrian', 'vehicle', 'hazardous', 'emergency') NOT NULL,
    safety_level ENUM('low', 'medium', 'high', 'critical') DEFAULT 'medium',
    
    -- Geographic definition
    boundary_coordinates JSON NOT NULL COMMENT 'Polygon coordinates defining zone boundary',
    area_sqm DECIMAL(12, 2),
    
    -- Zone properties
    max_occupancy INT COMMENT 'Maximum allowed people in zone',
    requires_ppe BOOLEAN DEFAULT FALSE,
    required_ppe_types JSON COMMENT 'Hard hat, safety vest, etc.',
    access_restrictions JSON COMMENT 'Who can access this zone and when',
    
    -- Monitoring configuration
    monitoring_enabled BOOLEAN DEFAULT TRUE,
    ai_detection_enabled BOOLEAN DEFAULT TRUE,
    motion_detection_enabled BOOLEAN DEFAULT TRUE,
    occupancy_tracking_enabled BOOLEAN DEFAULT FALSE,
    
    -- Alert configuration
    alert_on_unauthorized_entry BOOLEAN DEFAULT FALSE,
    alert_on_ppe_violation BOOLEAN DEFAULT FALSE,
    alert_on_overcrowding BOOLEAN DEFAULT FALSE,
    alert_on_after_hours_activity BOOLEAN DEFAULT FALSE,
    
    -- Associated cameras (application-level references to VMS)
    monitoring_camera_ids JSON COMMENT 'Array of camera IDs that monitor this zone',
    primary_camera_id CHAR(36) COMMENT 'Primary camera for this zone',
    
    -- Interactive features
    has_interactive_controls BOOLEAN DEFAULT FALSE,
    control_panel_config JSON COMMENT 'IoT controls, switches, etc.',
    
    -- Schedule and operational hours
    operational_hours JSON COMMENT 'When this zone is normally active',
    maintenance_schedule JSON COMMENT 'Scheduled maintenance windows',
    
    -- Status
    status ENUM('active', 'inactive', 'maintenance', 'restricted') DEFAULT 'active',
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (site_id) REFERENCES sites(id) ON DELETE CASCADE,
    UNIQUE KEY uk_zone_code (site_id, zone_code),
    INDEX idx_zone_site (site_id),
    INDEX idx_zone_type (zone_type),
    INDEX idx_zone_safety_level (safety_level),
    INDEX idx_zone_status (status),
    INDEX idx_zone_monitoring (monitoring_enabled, ai_detection_enabled)
) ENGINE=InnoDB COMMENT='Defined zones within construction sites for monitoring and control';

-- ================================================================
-- TABLE 10: SITE_MAPS
-- ================================================================
CREATE TABLE site_maps (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    site_id CHAR(36) NOT NULL,
    
    -- Map information
    name VARCHAR(200) NOT NULL,
    description TEXT,
    map_type ENUM('satellite', 'blueprint', 'cad', 'hand_drawn', 'drone_survey') NOT NULL,
    
    -- File information
    file_path VARCHAR(1000) NOT NULL,
    file_name VARCHAR(255) NOT NULL,
    file_size_bytes BIGINT NOT NULL,
    file_format VARCHAR(20) NOT NULL COMMENT 'jpg, png, pdf, dwg, etc.',
    
    -- Map properties
    map_scale VARCHAR(50) COMMENT 'e.g., 1:100, 1:500',
    coordinate_system VARCHAR(100) COMMENT 'GPS, UTM, local grid, etc.',
    map_orientation_degrees DECIMAL(5, 2) DEFAULT 0 COMMENT 'North orientation',
    
    -- Geographic referencing
    southwest_lat DECIMAL(10, 7) COMMENT 'Southwest corner latitude',
    southwest_lng DECIMAL(10, 7) COMMENT 'Southwest corner longitude',
    northeast_lat DECIMAL(10, 7) COMMENT 'Northeast corner latitude',
    northeast_lng DECIMAL(10, 7) COMMENT 'Northeast corner longitude',
    
    -- Map overlay settings
    overlay_opacity DECIMAL(3, 2) DEFAULT 0.80,
    default_zoom_level INT DEFAULT 15,
    min_zoom_level INT DEFAULT 10,
    max_zoom_level INT DEFAULT 20,
    
    -- Version control
    version_number INT DEFAULT 1,
    is_current_version BOOLEAN DEFAULT TRUE,
    previous_version_id CHAR(36) NULL,
    
    -- Usage tracking
    last_updated_by_user_id CHAR(36),
    upload_source VARCHAR(100) COMMENT 'Web upload, mobile app, API, etc.',
    
    -- Status
    status ENUM('active', 'archived', 'processing', 'failed') DEFAULT 'active',
    processing_status VARCHAR(100),
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (site_id) REFERENCES sites(id) ON DELETE CASCADE,
    FOREIGN KEY (previous_version_id) REFERENCES site_maps(id) ON DELETE SET NULL,
    FOREIGN KEY (last_updated_by_user_id) REFERENCES users(id) ON DELETE SET NULL,
    UNIQUE KEY uk_site_current_map (site_id, is_current_version),
    INDEX idx_map_site (site_id),
    INDEX idx_map_status (status),
    INDEX idx_map_version (version_number),
    INDEX idx_map_coordinates (southwest_lat, southwest_lng, northeast_lat, northeast_lng)
) ENGINE=InnoDB COMMENT='Site maps and blueprints for overlay visualization';

-- ================================================================
-- TABLE 11: AI_MODELS
-- ================================================================
CREATE TABLE ai_models (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    
    -- Model identification
    model_name VARCHAR(100) NOT NULL UNIQUE,
    display_name VARCHAR(150) NOT NULL,
    version VARCHAR(50) NOT NULL,
    model_type ENUM('yolo_v8', 'yolo_v9', 'custom', 'third_party') NOT NULL,
    
    -- Model capabilities
    detection_classes JSON NOT NULL COMMENT 'Array of object classes this model can detect',
    supported_formats JSON COMMENT 'Input formats: image, video, rtsp',
    max_resolution VARCHAR(20) COMMENT 'Maximum supported input resolution',
    
    -- Performance characteristics
    inference_time_ms DECIMAL(8, 2) COMMENT 'Average inference time per frame',
    accuracy_percentage DECIMAL(5, 2) COMMENT 'Model accuracy on test dataset',
    min_confidence_threshold DECIMAL(3, 2) DEFAULT 0.25,
    optimal_confidence_threshold DECIMAL(3, 2) DEFAULT 0.50,
    
    -- Hardware requirements
    requires_gpu BOOLEAN DEFAULT TRUE,
    min_gpu_memory_mb INT,
    tensorrt_optimized BOOLEAN DEFAULT FALSE,
    batch_processing_supported BOOLEAN DEFAULT TRUE,
    max_batch_size INT DEFAULT 1,
    
    -- Model files and paths
    model_file_path VARCHAR(1000) NOT NULL,
    weights_file_path VARCHAR(1000),
    config_file_path VARCHAR(1000),
    labels_file_path VARCHAR(1000),
    
    -- Training information
    training_dataset VARCHAR(200),
    training_date DATE,
    training_epochs INT,
    training_notes TEXT,
    
    -- Usage and deployment
    deployment_environments JSON COMMENT 'Where this model can be deployed',
    use_cases JSON COMMENT 'PPE detection, personnel counting, equipment monitoring',
    
    -- Status and lifecycle
    status ENUM('development', 'testing', 'production', 'deprecated', 'archived') DEFAULT 'development',
    is_default_model BOOLEAN DEFAULT FALSE,
    
    -- Metadata
    created_by_user_id CHAR(36),
    model_source VARCHAR(100) COMMENT 'ultralytics, custom_training, third_party',
    license_type VARCHAR(100),
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (created_by_user_id) REFERENCES users(id) ON DELETE SET NULL,
    INDEX idx_model_type (model_type),
    INDEX idx_model_status (status),
    INDEX idx_model_version (model_name, version),
    INDEX idx_model_default (is_default_model)
) ENGINE=InnoDB COMMENT='AI/ML models for object detection and analysis';

SELECT 'Construction Management Schema Part 2 (Tables 4-11) created successfully!' as Status;