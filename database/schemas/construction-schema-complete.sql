-- ================================================================
-- COMPLETE CONSTRUCTION MANAGEMENT SYSTEM SCHEMA  
-- Construction Site AI Monitoring System - Construction Database
-- Version: 1.0
-- Tables: 23 (COMPLETE)
-- ================================================================

USE construction_management;

-- ================================================================
-- TABLE 1: COMPANIES
-- ================================================================
CREATE TABLE companies (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    name VARCHAR(200) NOT NULL,
    legal_name VARCHAR(250),
    registration_number VARCHAR(100),
    tax_id VARCHAR(50),
    
    -- Contact information
    headquarters_address TEXT,
    phone VARCHAR(20),
    email VARCHAR(100),
    website VARCHAR(255),
    
    -- Business information
    industry VARCHAR(100) DEFAULT 'Construction',
    company_size ENUM('small', 'medium', 'large', 'enterprise') DEFAULT 'medium',
    annual_revenue_range VARCHAR(50),
    
    -- Subscription and licensing
    license_type ENUM('trial', 'basic', 'professional', 'enterprise') DEFAULT 'trial',
    license_expiry DATE,
    max_sites INT DEFAULT 5,
    max_users INT DEFAULT 50,
    max_cameras INT DEFAULT 100,
    
    -- Configuration
    timezone VARCHAR(50) DEFAULT 'UTC',
    date_format VARCHAR(20) DEFAULT 'YYYY-MM-DD',
    currency VARCHAR(3) DEFAULT 'USD',
    
    -- Status
    status ENUM('active', 'suspended', 'cancelled') DEFAULT 'active',
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    UNIQUE KEY uk_company_registration (registration_number),
    INDEX idx_company_status (status),
    INDEX idx_company_license (license_type, license_expiry)
) ENGINE=InnoDB COMMENT='Top-level company entities';

-- ================================================================
-- TABLE 2: GROUPS
-- ================================================================
CREATE TABLE groups (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    company_id CHAR(36) NOT NULL,
    name VARCHAR(150) NOT NULL,
    description TEXT,
    
    -- Hierarchy
    parent_group_id CHAR(36) NULL COMMENT 'For nested group structures',
    group_level INT DEFAULT 1 COMMENT 'Hierarchy level',
    
    -- Geographic coverage
    region VARCHAR(100),
    country VARCHAR(100),
    state_province VARCHAR(100),
    coverage_area JSON COMMENT 'Geographic boundaries',
    
    -- Management
    group_manager_user_id CHAR(36),
    budget_allocation DECIMAL(15,2),
    
    -- Contact information
    office_address TEXT,
    phone VARCHAR(20),
    email VARCHAR(100),
    
    -- Status
    status ENUM('active', 'inactive') DEFAULT 'active',
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (company_id) REFERENCES companies(id) ON DELETE CASCADE,
    FOREIGN KEY (parent_group_id) REFERENCES groups(id) ON DELETE SET NULL,
    INDEX idx_group_company (company_id),
    INDEX idx_group_parent (parent_group_id),
    INDEX idx_group_manager (group_manager_user_id),
    INDEX idx_group_status (status)
) ENGINE=InnoDB COMMENT='Regional or divisional groupings within companies';

-- ================================================================
-- TABLE 3: SITES
-- ================================================================
CREATE TABLE sites (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    company_id CHAR(36) NOT NULL,
    group_id CHAR(36) NOT NULL,
    
    -- Basic information
    site_code VARCHAR(50) NOT NULL COMMENT 'Human-readable site identifier',
    name VARCHAR(200) NOT NULL,
    description TEXT,
    
    -- Project information
    project_type ENUM('residential', 'commercial', 'industrial', 'infrastructure', 'renovation') NOT NULL,
    project_phase ENUM('planning', 'preparation', 'construction', 'finishing', 'completed', 'maintenance') DEFAULT 'planning',
    
    -- Location
    address TEXT NOT NULL,
    city VARCHAR(100) NOT NULL,
    state_province VARCHAR(100),
    country VARCHAR(100) NOT NULL,
    postal_code VARCHAR(20),
    
    -- Geographic coordinates
    latitude DECIMAL(10, 7),
    longitude DECIMAL(10, 7),
    elevation_meters DECIMAL(8, 2),
    
    -- Site boundaries (for map display)
    boundary_coordinates JSON COMMENT 'Polygon coordinates defining site boundaries',
    site_area_sqm DECIMAL(12, 2),
    
    -- Timeline
    planned_start_date DATE,
    planned_end_date DATE,
    actual_start_date DATE,
    actual_end_date DATE,
    
    -- Management  
    site_manager_user_id CHAR(36),
    site_coordinator_user_id CHAR(36),
    contractor_company VARCHAR(200),
    
    -- Safety and compliance
    safety_requirements JSON COMMENT 'Site-specific safety requirements',
    compliance_standards JSON COMMENT 'OSHA, local regulations, etc.',
    hazard_classifications JSON COMMENT 'Known hazards at the site',
    
    -- Budget and resources
    project_budget DECIMAL(15,2),
    allocated_budget DECIMAL(15,2),
    
    -- Contact and access
    site_phone VARCHAR(20),
    site_email VARCHAR(100),
    access_instructions TEXT,
    emergency_contact JSON,
    
    -- Configuration
    timezone VARCHAR(50) DEFAULT 'UTC',
    working_hours JSON COMMENT 'Standard working hours for the site',
    
    -- Status
    status ENUM('planning', 'active', 'suspended', 'completed', 'archived') DEFAULT 'planning',
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (company_id) REFERENCES companies(id) ON DELETE CASCADE,
    FOREIGN KEY (group_id) REFERENCES groups(id) ON DELETE CASCADE,
    UNIQUE KEY uk_site_code (company_id, site_code),
    INDEX idx_site_company (company_id),
    INDEX idx_site_group (group_id),
    INDEX idx_site_status (status),
    INDEX idx_site_project_type (project_type),
    INDEX idx_site_location (city, state_province, country),
    INDEX idx_site_coordinates (latitude, longitude),
    INDEX idx_site_manager (site_manager_user_id),
    INDEX idx_site_timeline (planned_start_date, planned_end_date)
) ENGINE=InnoDB COMMENT='Individual construction sites';-- ================================================================
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

SELECT 'Construction Management Schema Part 2 (Tables 4-11) created successfully!' as Status;-- ================================================================
-- CONSTRUCTION MANAGEMENT SCHEMA - PART 3 (Final Advanced Tables)
-- Tables 12-23: Detection Results, Alerts, Field Assessment, Security Patrol, etc.
-- ================================================================

USE construction_management;

-- ================================================================
-- TABLE 12: DETECTION_RESULTS
-- ================================================================
CREATE TABLE detection_results (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    
    -- Source information
    camera_id CHAR(36) NOT NULL COMMENT 'Camera ID from VMS system (application-level reference)',
    site_id CHAR(36) NOT NULL,
    ai_model_id CHAR(36) NOT NULL,
    
    -- Detection timing
    detection_timestamp TIMESTAMP NOT NULL,
    frame_timestamp TIMESTAMP NOT NULL COMMENT 'Timestamp of the analyzed frame',
    processing_time_ms DECIMAL(8, 2),
    
    -- Image/frame information
    source_image_path VARCHAR(1000),
    annotated_image_path VARCHAR(1000),
    frame_width INT NOT NULL,
    frame_height INT NOT NULL,
    
    -- Detection results
    detected_objects JSON NOT NULL COMMENT 'Array of detected objects with bounding boxes and confidence',
    total_detections INT NOT NULL DEFAULT 0,
    high_confidence_detections INT DEFAULT 0 COMMENT 'Detections above optimal threshold',
    
    -- Specific detection categories
    person_count INT DEFAULT 0,
    vehicle_count INT DEFAULT 0,
    equipment_count INT DEFAULT 0,
    ppe_violations_count INT DEFAULT 0,
    safety_violations_count INT DEFAULT 0,
    
    -- Analysis results
    zone_analysis JSON COMMENT 'Which zones detected objects are in',
    safety_analysis JSON COMMENT 'Safety compliance analysis results',
    anomaly_score DECIMAL(5, 3) DEFAULT 0.000 COMMENT 'Anomaly detection score',
    
    -- Alert triggers
    triggered_alerts BOOLEAN DEFAULT FALSE,
    alert_reasons JSON COMMENT 'Reasons why alerts were triggered',
    
    -- Performance metrics
    gpu_utilization_percentage DECIMAL(5, 2),
    memory_usage_mb INT,
    
    -- Status and flags
    processing_status ENUM('pending', 'completed', 'failed', 'archived') DEFAULT 'completed',
    requires_review BOOLEAN DEFAULT FALSE,
    reviewed_by_user_id CHAR(36) NULL,
    reviewed_at TIMESTAMP NULL,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (site_id) REFERENCES sites(id) ON DELETE CASCADE,
    FOREIGN KEY (ai_model_id) REFERENCES ai_models(id) ON DELETE RESTRICT,
    FOREIGN KEY (reviewed_by_user_id) REFERENCES users(id) ON DELETE SET NULL,
    INDEX idx_detection_camera_time (camera_id, detection_timestamp),
    INDEX idx_detection_site_time (site_id, detection_timestamp),
    INDEX idx_detection_model (ai_model_id),
    INDEX idx_detection_status (processing_status),
    INDEX idx_detection_alerts (triggered_alerts),
    INDEX idx_detection_review (requires_review, reviewed_at)
) ENGINE=InnoDB 
PARTITION BY RANGE (UNIX_TIMESTAMP(detection_timestamp)) (
    PARTITION p_current VALUES LESS THAN (UNIX_TIMESTAMP('2025-02-01')),
    PARTITION p_future VALUES LESS THAN MAXVALUE
) COMMENT='AI detection results from camera feeds';

-- ================================================================
-- TABLE 13: SAFETY_VIOLATIONS
-- ================================================================
CREATE TABLE safety_violations (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    
    -- Source and context
    detection_result_id CHAR(36) NOT NULL,
    site_id CHAR(36) NOT NULL,
    zone_id CHAR(36) NULL,
    camera_id CHAR(36) NOT NULL COMMENT 'Camera ID from VMS system',
    
    -- Violation details
    violation_type ENUM('missing_ppe', 'unauthorized_area', 'unsafe_behavior', 'equipment_violation', 'overcrowding', 'after_hours') NOT NULL,
    violation_category ENUM('ppe', 'access_control', 'behavior', 'equipment', 'occupancy', 'schedule') NOT NULL,
    severity ENUM('low', 'medium', 'high', 'critical') NOT NULL,
    
    -- Violation specifics
    violation_description TEXT NOT NULL,
    missing_ppe_types JSON COMMENT 'Specific PPE items missing',
    involved_person_count INT DEFAULT 1,
    equipment_involved VARCHAR(200),
    
    -- Location and evidence
    violation_coordinates JSON COMMENT 'Bounding box or coordinates of violation',
    evidence_image_path VARCHAR(1000),
    evidence_video_clip_path VARCHAR(1000),
    
    -- Detection confidence and validation
    ai_confidence DECIMAL(5, 3) NOT NULL,
    manual_verification_required BOOLEAN DEFAULT TRUE,
    is_false_positive BOOLEAN DEFAULT FALSE,
    
    -- Timeline
    violation_timestamp TIMESTAMP NOT NULL,
    duration_seconds INT COMMENT 'How long the violation lasted',
    
    -- Response and resolution
    alert_generated BOOLEAN DEFAULT FALSE,
    notification_sent BOOLEAN DEFAULT FALSE,
    assigned_to_user_id CHAR(36) NULL,
    response_time_minutes INT,
    
    -- Status tracking
    status ENUM('open', 'investigating', 'resolved', 'dismissed', 'escalated') DEFAULT 'open',
    resolution_notes TEXT,
    resolved_by_user_id CHAR(36) NULL,
    resolved_at TIMESTAMP NULL,
    
    -- Escalation
    escalated_at TIMESTAMP NULL,
    escalated_to_user_id CHAR(36) NULL,
    escalation_reason TEXT,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (detection_result_id) REFERENCES detection_results(id) ON DELETE CASCADE,
    FOREIGN KEY (site_id) REFERENCES sites(id) ON DELETE CASCADE,
    FOREIGN KEY (zone_id) REFERENCES site_zones(id) ON DELETE SET NULL,
    FOREIGN KEY (assigned_to_user_id) REFERENCES users(id) ON DELETE SET NULL,
    FOREIGN KEY (resolved_by_user_id) REFERENCES users(id) ON DELETE SET NULL,
    FOREIGN KEY (escalated_to_user_id) REFERENCES users(id) ON DELETE SET NULL,
    INDEX idx_violation_site_time (site_id, violation_timestamp),
    INDEX idx_violation_camera_time (camera_id, violation_timestamp),
    INDEX idx_violation_type_severity (violation_type, severity),
    INDEX idx_violation_status (status),
    INDEX idx_violation_assigned (assigned_to_user_id),
    INDEX idx_violation_escalated (escalated_at, escalated_to_user_id)
) ENGINE=InnoDB 
PARTITION BY RANGE (UNIX_TIMESTAMP(violation_timestamp)) (
    PARTITION p_current VALUES LESS THAN (UNIX_TIMESTAMP('2025-02-01')),
    PARTITION p_future VALUES LESS THAN MAXVALUE
) COMMENT='Safety violations detected by AI analysis';

-- ================================================================
-- TABLE 14: PERSONNEL_TRACKING
-- ================================================================
CREATE TABLE personnel_tracking (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    
    -- Detection source
    detection_result_id CHAR(36) NOT NULL,
    site_id CHAR(36) NOT NULL,
    camera_id CHAR(36) NOT NULL COMMENT 'Camera ID from VMS system',
    
    -- Person tracking
    person_tracking_id VARCHAR(100) COMMENT 'Unique ID for tracking same person across frames',
    detection_timestamp TIMESTAMP NOT NULL,
    
    -- Location information
    zone_id CHAR(36) NULL,
    position_coordinates JSON COMMENT 'X,Y coordinates within frame and site map',
    movement_vector JSON COMMENT 'Direction and speed of movement',
    
    -- Person characteristics
    person_bbox JSON NOT NULL COMMENT 'Bounding box coordinates',
    confidence_score DECIMAL(5, 3) NOT NULL,
    person_height_estimate DECIMAL(5, 2) COMMENT 'Estimated height in meters',
    
    -- PPE Detection
    ppe_detected JSON COMMENT 'Detected PPE items with confidence scores',
    ppe_compliance_score DECIMAL(5, 3) DEFAULT 0.000,
    missing_ppe JSON COMMENT 'Required but missing PPE items',
    
    -- Behavior analysis
    activity_classification VARCHAR(100) COMMENT 'Walking, working, standing, etc.',
    posture_analysis JSON COMMENT 'Posture-related safety analysis',
    interaction_with_equipment BOOLEAN DEFAULT FALSE,
    
    -- Access control
    authorized_for_zone BOOLEAN NULL COMMENT 'Null if unknown, true/false if determinable',
    access_violation BOOLEAN DEFAULT FALSE,
    
    -- Aggregation helpers
    time_in_zone_seconds INT COMMENT 'Cumulative time spent in current zone',
    site_entry_time TIMESTAMP COMMENT 'When person first appeared on site',
    site_exit_time TIMESTAMP NULL COMMENT 'When person left site (if detected)',
    
    -- Status
    tracking_status ENUM('active', 'lost', 'exited') DEFAULT 'active',
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (detection_result_id) REFERENCES detection_results(id) ON DELETE CASCADE,
    FOREIGN KEY (site_id) REFERENCES sites(id) ON DELETE CASCADE,
    FOREIGN KEY (zone_id) REFERENCES site_zones(id) ON DELETE SET NULL,
    INDEX idx_personnel_site_time (site_id, detection_timestamp),
    INDEX idx_personnel_camera_time (camera_id, detection_timestamp),
    INDEX idx_personnel_tracking (person_tracking_id, detection_timestamp),
    INDEX idx_personnel_zone (zone_id, detection_timestamp),
    INDEX idx_personnel_compliance (ppe_compliance_score),
    INDEX idx_personnel_violations (access_violation)
) ENGINE=InnoDB 
PARTITION BY RANGE (UNIX_TIMESTAMP(detection_timestamp)) (
    PARTITION p_current VALUES LESS THAN (UNIX_TIMESTAMP('2025-02-01')),
    PARTITION p_future VALUES LESS THAN MAXVALUE
) COMMENT='Personnel tracking and PPE compliance monitoring';

-- ================================================================
-- TABLE 15: EQUIPMENT_DETECTIONS
-- ================================================================
CREATE TABLE equipment_detections (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    
    -- Detection source
    detection_result_id CHAR(36) NOT NULL,
    site_id CHAR(36) NOT NULL,
    camera_id CHAR(36) NOT NULL COMMENT 'Camera ID from VMS system',
    
    -- Equipment identification
    equipment_type VARCHAR(100) NOT NULL COMMENT 'excavator, crane, truck, etc.',
    equipment_subtype VARCHAR(100) COMMENT 'More specific classification',
    equipment_id VARCHAR(100) COMMENT 'Unique equipment identifier if recognizable',
    
    -- Detection details
    detection_timestamp TIMESTAMP NOT NULL,
    equipment_bbox JSON NOT NULL COMMENT 'Bounding box coordinates',
    confidence_score DECIMAL(5, 3) NOT NULL,
    
    -- Location and positioning
    zone_id CHAR(36) NULL,
    position_coordinates JSON COMMENT 'Equipment position on site map',
    equipment_orientation DECIMAL(5, 2) COMMENT 'Equipment facing direction in degrees',
    
    -- Equipment status
    operational_status ENUM('idle', 'active', 'moving', 'loading', 'unknown') DEFAULT 'unknown',
    safety_status ENUM('safe', 'warning', 'danger', 'unknown') DEFAULT 'unknown',
    
    -- Safety analysis
    proximity_to_personnel JSON COMMENT 'Personnel within safety radius',
    safety_violations JSON COMMENT 'Detected safety issues',
    required_safety_zones JSON COMMENT 'Areas that should be clear',
    
    -- Equipment characteristics
    estimated_size JSON COMMENT 'Width, height, length estimates',
    load_status ENUM('empty', 'loaded', 'overloaded', 'unknown') DEFAULT 'unknown',
    
    -- Compliance and authorization
    authorized_for_zone BOOLEAN NULL,
    requires_spotter BOOLEAN DEFAULT FALSE,
    spotter_present BOOLEAN NULL,
    
    -- Movement tracking
    movement_detected BOOLEAN DEFAULT FALSE,
    movement_speed_kmh DECIMAL(5, 2),
    movement_direction_degrees DECIMAL(5, 2),
    
    -- Maintenance and inspection
    last_inspection_visible BOOLEAN DEFAULT FALSE,
    inspection_stickers_detected JSON,
    visible_damage BOOLEAN DEFAULT FALSE,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (detection_result_id) REFERENCES detection_results(id) ON DELETE CASCADE,
    FOREIGN KEY (site_id) REFERENCES sites(id) ON DELETE CASCADE,
    FOREIGN KEY (zone_id) REFERENCES site_zones(id) ON DELETE SET NULL,
    INDEX idx_equipment_site_time (site_id, detection_timestamp),
    INDEX idx_equipment_camera_time (camera_id, detection_timestamp),
    INDEX idx_equipment_type (equipment_type, equipment_subtype),
    INDEX idx_equipment_zone (zone_id, detection_timestamp),
    INDEX idx_equipment_status (operational_status, safety_status),
    INDEX idx_equipment_confidence (confidence_score)
) ENGINE=InnoDB 
PARTITION BY RANGE (UNIX_TIMESTAMP(detection_timestamp)) (
    PARTITION p_current VALUES LESS THAN (UNIX_TIMESTAMP('2025-02-01')),
    PARTITION p_future VALUES LESS THAN MAXVALUE
) COMMENT='Equipment detection and safety monitoring';

-- ================================================================
-- TABLE 16: CONFIDENCE_METRICS
-- ================================================================
CREATE TABLE confidence_metrics (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    
    -- Source reference
    detection_result_id CHAR(36) NOT NULL,
    site_id CHAR(36) NOT NULL,
    ai_model_id CHAR(36) NOT NULL,
    
    -- Timing
    metric_timestamp TIMESTAMP NOT NULL,
    
    -- Overall confidence metrics
    average_confidence DECIMAL(5, 3) NOT NULL,
    min_confidence DECIMAL(5, 3) NOT NULL,
    max_confidence DECIMAL(5, 3) NOT NULL,
    confidence_variance DECIMAL(8, 6),
    
    -- Detection category confidences
    person_detection_confidence DECIMAL(5, 3),
    ppe_detection_confidence DECIMAL(5, 3),
    vehicle_detection_confidence DECIMAL(5, 3),
    equipment_detection_confidence DECIMAL(5, 3),
    
    -- Quality indicators
    image_quality_score DECIMAL(5, 3) COMMENT 'Overall image quality assessment',
    lighting_quality ENUM('poor', 'fair', 'good', 'excellent') DEFAULT 'fair',
    weather_impact ENUM('none', 'minimal', 'moderate', 'severe') DEFAULT 'none',
    camera_stability ENUM('stable', 'slight_shake', 'unstable') DEFAULT 'stable',
    
    -- Environmental factors
    time_of_day ENUM('dawn', 'morning', 'midday', 'afternoon', 'dusk', 'night') NOT NULL,
    visibility_conditions VARCHAR(50),
    environmental_notes TEXT,
    
    -- Model performance
    inference_time_ms DECIMAL(8, 2) NOT NULL,
    preprocessing_time_ms DECIMAL(8, 2),
    postprocessing_time_ms DECIMAL(8, 2),
    
    -- Accuracy indicators
    false_positive_likelihood DECIMAL(5, 3) DEFAULT 0.000,
    false_negative_likelihood DECIMAL(5, 3) DEFAULT 0.000,
    calibration_score DECIMAL(5, 3) COMMENT 'How well-calibrated the confidence scores are',
    
    -- Validation status
    manual_validation_available BOOLEAN DEFAULT FALSE,
    validation_agreement_score DECIMAL(5, 3) NULL COMMENT 'Agreement with manual validation',
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (detection_result_id) REFERENCES detection_results(id) ON DELETE CASCADE,
    FOREIGN KEY (site_id) REFERENCES sites(id) ON DELETE CASCADE,
    FOREIGN KEY (ai_model_id) REFERENCES ai_models(id) ON DELETE CASCADE,
    INDEX idx_confidence_site_time (site_id, metric_timestamp),
    INDEX idx_confidence_model (ai_model_id, metric_timestamp),
    INDEX idx_confidence_quality (average_confidence, image_quality_score),
    INDEX idx_confidence_performance (inference_time_ms),
    INDEX idx_confidence_validation (manual_validation_available, validation_agreement_score)
) ENGINE=InnoDB 
PARTITION BY RANGE (UNIX_TIMESTAMP(metric_timestamp)) (
    PARTITION p_current VALUES LESS THAN (UNIX_TIMESTAMP('2025-02-01')),
    PARTITION p_future VALUES LESS THAN MAXVALUE
) COMMENT='AI model confidence metrics and quality assessment';

-- ================================================================
-- TABLE 17: ALERT_RULES
-- ================================================================
CREATE TABLE alert_rules (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    company_id CHAR(36) NOT NULL,
    
    -- Rule identification
    rule_name VARCHAR(150) NOT NULL,
    rule_description TEXT,
    rule_category ENUM('safety', 'security', 'compliance', 'equipment', 'custom') NOT NULL,
    
    -- Scope
    applies_to_sites JSON COMMENT 'Array of site IDs, null means all sites',
    applies_to_zones JSON COMMENT 'Array of zone IDs, null means all zones',
    applies_to_cameras JSON COMMENT 'Array of camera IDs, null means all cameras',
    
    -- Trigger conditions
    trigger_conditions JSON NOT NULL COMMENT 'Complex conditions for triggering alerts',
    trigger_logic ENUM('AND', 'OR', 'CUSTOM') DEFAULT 'AND',
    
    -- Timing constraints
    active_hours JSON COMMENT 'When this rule is active',
    ignore_periods JSON COMMENT 'Time periods to ignore (maintenance, etc.)',
    cooldown_minutes INT DEFAULT 5 COMMENT 'Minimum time between alerts of same type',
    
    -- Alert configuration
    alert_priority ENUM('low', 'medium', 'high', 'critical') NOT NULL,
    alert_message_template TEXT NOT NULL,
    requires_acknowledgment BOOLEAN DEFAULT FALSE,
    auto_resolve_after_minutes INT COMMENT 'Auto-resolve if condition clears',
    
    -- Escalation rules
    escalation_enabled BOOLEAN DEFAULT FALSE,
    escalation_delay_minutes INT DEFAULT 15,
    escalation_roles JSON COMMENT 'Roles to escalate to',
    escalation_users JSON COMMENT 'Specific users to escalate to',
    
    -- Notification settings
    notification_methods JSON COMMENT 'email, sms, push, webhook',
    notification_recipients JSON COMMENT 'Who should be notified',
    
    -- Advanced features
    ml_confidence_threshold DECIMAL(5, 3) DEFAULT 0.500,
    require_multiple_detections BOOLEAN DEFAULT FALSE,
    detection_window_seconds INT DEFAULT 30,
    
    -- Status and management
    status ENUM('active', 'inactive', 'testing') DEFAULT 'active',
    created_by_user_id CHAR(36) NOT NULL,
    last_modified_by_user_id CHAR(36),
    
    -- Usage statistics
    total_alerts_generated INT DEFAULT 0,
    last_triggered_at TIMESTAMP NULL,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (company_id) REFERENCES companies(id) ON DELETE CASCADE,
    FOREIGN KEY (created_by_user_id) REFERENCES users(id) ON DELETE RESTRICT,
    FOREIGN KEY (last_modified_by_user_id) REFERENCES users(id) ON DELETE SET NULL,
    UNIQUE KEY uk_rule_name (company_id, rule_name),
    INDEX idx_rule_company (company_id),
    INDEX idx_rule_category (rule_category),
    INDEX idx_rule_status (status),
    INDEX idx_rule_priority (alert_priority)
) ENGINE=InnoDB COMMENT='Configurable alert rules and triggers';

-- ================================================================
-- TABLE 18: ALERTS
-- ================================================================
CREATE TABLE alerts (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    
    -- Alert source
    alert_rule_id CHAR(36) NOT NULL,
    site_id CHAR(36) NOT NULL,
    detection_result_id CHAR(36) NULL COMMENT 'Source detection if applicable',
    safety_violation_id CHAR(36) NULL COMMENT 'Related safety violation if applicable',
    
    -- Alert details
    alert_type VARCHAR(100) NOT NULL,
    alert_category ENUM('safety', 'security', 'compliance', 'equipment', 'system', 'custom') NOT NULL,
    priority ENUM('low', 'medium', 'high', 'critical') NOT NULL,
    severity_score DECIMAL(5, 3) DEFAULT 0.000,
    
    -- Alert content
    title VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    additional_context JSON COMMENT 'Extra data specific to alert type',
    
    -- Location and evidence
    camera_id CHAR(36) COMMENT 'Camera that triggered alert',
    zone_id CHAR(36) NULL,
    alert_coordinates JSON COMMENT 'Location of alert trigger',
    evidence_urls JSON COMMENT 'Images, videos, documents',
    
    -- Timing
    triggered_at TIMESTAMP NOT NULL,
    acknowledged_at TIMESTAMP NULL,
    resolved_at TIMESTAMP NULL,
    
    -- Status and lifecycle
    status ENUM('open', 'acknowledged', 'investigating', 'resolved', 'dismissed', 'escalated') DEFAULT 'open',
    resolution_type ENUM('automatic', 'manual', 'timeout', 'dismissed') NULL,
    resolution_notes TEXT,
    
    -- Assignment and ownership
    assigned_to_user_id CHAR(36) NULL,
    acknowledged_by_user_id CHAR(36) NULL,
    resolved_by_user_id CHAR(36) NULL,
    
    -- Escalation tracking
    escalation_level INT DEFAULT 0,
    escalated_at TIMESTAMP NULL,
    escalated_to_user_id CHAR(36) NULL,
    
    -- Response metrics
    response_time_minutes INT COMMENT 'Time to acknowledgment',
    resolution_time_minutes INT COMMENT 'Time to resolution',
    
    -- Notification tracking
    notifications_sent INT DEFAULT 0,
    last_notification_at TIMESTAMP NULL,
    notification_log JSON COMMENT 'Log of all notifications sent',
    
    -- Feedback and quality
    false_positive BOOLEAN NULL COMMENT 'True/False after investigation',
    user_feedback TEXT,
    alert_quality_score DECIMAL(3, 2) COMMENT 'User rating of alert usefulness',
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (alert_rule_id) REFERENCES alert_rules(id) ON DELETE CASCADE,
    FOREIGN KEY (site_id) REFERENCES sites(id) ON DELETE CASCADE,
    FOREIGN KEY (detection_result_id) REFERENCES detection_results(id) ON DELETE SET NULL,
    FOREIGN KEY (safety_violation_id) REFERENCES safety_violations(id) ON DELETE SET NULL,
    FOREIGN KEY (zone_id) REFERENCES site_zones(id) ON DELETE SET NULL,
    FOREIGN KEY (assigned_to_user_id) REFERENCES users(id) ON DELETE SET NULL,
    FOREIGN KEY (acknowledged_by_user_id) REFERENCES users(id) ON DELETE SET NULL,
    FOREIGN KEY (resolved_by_user_id) REFERENCES users(id) ON DELETE SET NULL,
    FOREIGN KEY (escalated_to_user_id) REFERENCES users(id) ON DELETE SET NULL,
    INDEX idx_alert_site_time (site_id, triggered_at),
    INDEX idx_alert_camera_time (camera_id, triggered_at),
    INDEX idx_alert_status (status),
    INDEX idx_alert_priority (priority),
    INDEX idx_alert_assigned (assigned_to_user_id),
    INDEX idx_alert_escalation (escalation_level, escalated_at),
    INDEX idx_alert_response_time (response_time_minutes),
    INDEX idx_alert_resolution_time (resolution_time_minutes)
) ENGINE=InnoDB 
PARTITION BY RANGE (UNIX_TIMESTAMP(triggered_at)) (
    PARTITION p_current VALUES LESS THAN (UNIX_TIMESTAMP('2025-02-01')),
    PARTITION p_future VALUES LESS THAN MAXVALUE
) COMMENT='System alerts and notifications';

SELECT 'Construction Management Schema Part 3 (Tables 12-18) created successfully!' as Status;-- ================================================================
-- CONSTRUCTION MANAGEMENT SCHEMA - PART 4 (Final Tables)
-- Tables 19-23: Alert Escalations, Notifications, Field Assessment, etc.
-- ================================================================

USE construction_management;

-- ================================================================
-- TABLE 19: ALERT_ESCALATIONS
-- ================================================================
CREATE TABLE alert_escalations (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    alert_id CHAR(36) NOT NULL,
    
    -- Escalation details
    escalation_level INT NOT NULL,
    escalation_trigger ENUM('timeout', 'manual', 'severity_increase', 'rule_based') NOT NULL,
    escalated_from_user_id CHAR(36) NULL,
    escalated_to_user_id CHAR(36) NOT NULL,
    
    -- Timing
    escalated_at TIMESTAMP NOT NULL,
    response_deadline TIMESTAMP NULL,
    responded_at TIMESTAMP NULL,
    
    -- Escalation context
    escalation_reason TEXT NOT NULL,
    escalation_notes TEXT,
    original_priority ENUM('low', 'medium', 'high', 'critical') NOT NULL,
    new_priority ENUM('low', 'medium', 'high', 'critical') NOT NULL,
    
    -- Response tracking
    response_type ENUM('acknowledged', 'delegated', 'resolved', 'escalated_further', 'ignored') NULL,
    response_notes TEXT,
    delegated_to_user_id CHAR(36) NULL,
    
    -- Notification tracking
    notification_sent BOOLEAN DEFAULT FALSE,
    notification_method VARCHAR(50),
    notification_sent_at TIMESTAMP NULL,
    notification_acknowledged_at TIMESTAMP NULL,
    
    -- Metrics
    escalation_effectiveness ENUM('effective', 'ineffective', 'too_late', 'unnecessary') NULL,
    response_time_minutes INT COMMENT 'Time from escalation to response',
    
    -- Status
    status ENUM('pending', 'responded', 'expired', 'cancelled') DEFAULT 'pending',
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (alert_id) REFERENCES alerts(id) ON DELETE CASCADE,
    FOREIGN KEY (escalated_from_user_id) REFERENCES users(id) ON DELETE SET NULL,
    FOREIGN KEY (escalated_to_user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (delegated_to_user_id) REFERENCES users(id) ON DELETE SET NULL,
    INDEX idx_escalation_alert (alert_id),
    INDEX idx_escalation_to_user (escalated_to_user_id),
    INDEX idx_escalation_status (status),
    INDEX idx_escalation_deadline (response_deadline),
    INDEX idx_escalation_level (escalation_level)
) ENGINE=InnoDB COMMENT='Alert escalation tracking and management';

-- ================================================================
-- TABLE 20: NOTIFICATIONS
-- ================================================================
CREATE TABLE notifications (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    
    -- Source
    alert_id CHAR(36) NULL COMMENT 'Related alert if applicable',
    user_id CHAR(36) NOT NULL COMMENT 'Recipient user',
    
    -- Notification details
    notification_type ENUM('alert', 'system', 'reminder', 'update', 'report') NOT NULL,
    category VARCHAR(100) NOT NULL,
    title VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    
    -- Delivery
    delivery_method ENUM('in_app', 'email', 'sms', 'push', 'webhook') NOT NULL,
    delivery_address VARCHAR(255) COMMENT 'Email, phone, webhook URL, etc.',
    
    -- Timing
    scheduled_for TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    sent_at TIMESTAMP NULL,
    delivered_at TIMESTAMP NULL,
    read_at TIMESTAMP NULL,
    
    -- Status tracking
    status ENUM('pending', 'sent', 'delivered', 'failed', 'read', 'dismissed') DEFAULT 'pending',
    delivery_attempts INT DEFAULT 0,
    max_delivery_attempts INT DEFAULT 3,
    failure_reason TEXT,
    
    -- Priority and urgency
    priority ENUM('low', 'medium', 'high', 'critical') DEFAULT 'medium',
    expires_at TIMESTAMP NULL COMMENT 'When notification becomes irrelevant',
    
    -- Interaction tracking
    clicked BOOLEAN DEFAULT FALSE,
    clicked_at TIMESTAMP NULL,
    action_taken VARCHAR(100) COMMENT 'What action user took from notification',
    
    -- Metadata
    metadata JSON COMMENT 'Additional data for rich notifications',
    template_used VARCHAR(100),
    
    -- Grouping and batching
    notification_group VARCHAR(100) COMMENT 'For grouping related notifications',
    batch_id CHAR(36) COMMENT 'For batch sending',
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (alert_id) REFERENCES alerts(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_notification_user (user_id),
    INDEX idx_notification_alert (alert_id),
    INDEX idx_notification_status (status),
    INDEX idx_notification_scheduled (scheduled_for),
    INDEX idx_notification_method (delivery_method),
    INDEX idx_notification_priority (priority),
    INDEX idx_notification_group (notification_group)
) ENGINE=InnoDB COMMENT='User notifications and delivery tracking';

-- ================================================================
-- TABLE 21: ASSESSMENT_ROUTES
-- ================================================================
CREATE TABLE assessment_routes (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    site_id CHAR(36) NOT NULL,
    
    -- Route identification
    route_name VARCHAR(200) NOT NULL,
    route_code VARCHAR(50) NOT NULL,
    description TEXT,
    
    -- Route configuration
    route_type ENUM('inspection', 'patrol', 'emergency', 'maintenance', 'custom') NOT NULL,
    difficulty_level ENUM('easy', 'moderate', 'difficult') DEFAULT 'moderate',
    estimated_duration_minutes INT NOT NULL,
    
    -- Route path
    waypoints JSON NOT NULL COMMENT 'Array of coordinates defining the route',
    total_distance_meters DECIMAL(10, 2),
    elevation_change_meters DECIMAL(8, 2),
    
    -- Schedule and frequency
    schedule_type ENUM('on_demand', 'daily', 'weekly', 'monthly', 'custom') DEFAULT 'on_demand',
    schedule_config JSON COMMENT 'Specific scheduling parameters',
    next_scheduled_assessment TIMESTAMP NULL,
    
    -- Safety and requirements
    safety_requirements JSON COMMENT 'Required PPE, certifications, etc.',
    required_equipment JSON COMMENT 'Tools, devices needed for assessment',
    hazards_along_route JSON COMMENT 'Known hazards and precautions',
    
    -- Assessment configuration
    mandatory_checkpoints JSON COMMENT 'Points that must be visited',
    optional_checkpoints JSON COMMENT 'Points that can be visited if needed',
    photo_requirements JSON COMMENT 'Required photos at specific points',
    
    -- Access control
    authorized_roles JSON COMMENT 'Roles that can perform this assessment',
    requires_supervisor_approval BOOLEAN DEFAULT FALSE,
    requires_two_person_team BOOLEAN DEFAULT FALSE,
    
    -- Completion tracking
    last_completed_at TIMESTAMP NULL,
    last_completed_by_user_id CHAR(36) NULL,
    completion_rate_percentage DECIMAL(5, 2) DEFAULT 0.00,
    average_completion_time_minutes INT,
    
    -- Quality metrics
    average_rating DECIMAL(3, 2) COMMENT 'Average rating from assessors',
    total_completions INT DEFAULT 0,
    
    -- Status
    status ENUM('active', 'inactive', 'maintenance', 'archived') DEFAULT 'active',
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (site_id) REFERENCES sites(id) ON DELETE CASCADE,
    FOREIGN KEY (last_completed_by_user_id) REFERENCES users(id) ON DELETE SET NULL,
    UNIQUE KEY uk_route_code (site_id, route_code),
    INDEX idx_route_site (site_id),
    INDEX idx_route_type (route_type),
    INDEX idx_route_status (status),
    INDEX idx_route_schedule (next_scheduled_assessment),
    INDEX idx_route_completion (last_completed_at)
) ENGINE=InnoDB COMMENT='Assessment routes for mobile field inspections';

-- ================================================================
-- TABLE 22: MOBILE_RECORDINGS
-- ================================================================
CREATE TABLE mobile_recordings (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    
    -- Assessment context
    assessment_route_id CHAR(36) NULL,
    site_id CHAR(36) NOT NULL,
    recorded_by_user_id CHAR(36) NOT NULL,
    
    -- Recording identification
    recording_name VARCHAR(200),
    recording_code VARCHAR(50),
    
    -- File information
    file_path VARCHAR(1000) NOT NULL,
    file_name VARCHAR(255) NOT NULL,
    file_size_bytes BIGINT NOT NULL,
    file_format VARCHAR(20) NOT NULL COMMENT 'mp4, mov, etc.',
    duration_seconds INT NOT NULL,
    
    -- Recording metadata
    recording_start_time TIMESTAMP NOT NULL,
    recording_end_time TIMESTAMP NOT NULL,
    device_type VARCHAR(100) COMMENT 'tablet, smartphone, etc.',
    device_id VARCHAR(100),
    
    -- Location data
    start_coordinates JSON COMMENT 'GPS coordinates where recording started',
    end_coordinates JSON COMMENT 'GPS coordinates where recording ended',
    gps_track JSON COMMENT 'GPS track during recording',
    
    -- Technical details
    resolution VARCHAR(20),
    frame_rate DECIMAL(5, 2),
    codec VARCHAR(20),
    bitrate_kbps INT,
    
    -- Content classification
    content_type ENUM('inspection', 'incident', 'progress', 'safety_issue', 'equipment', 'personnel', 'general') NOT NULL,
    tags JSON COMMENT 'User-defined tags for categorization',
    
    -- Analysis and processing
    ai_analysis_completed BOOLEAN DEFAULT FALSE,
    ai_analysis_results JSON COMMENT 'AI analysis results if processed',
    manual_review_required BOOLEAN DEFAULT FALSE,
    transcription TEXT COMMENT 'Audio transcription if available',
    
    -- Quality assessment
    video_quality ENUM('poor', 'fair', 'good', 'excellent') DEFAULT 'good',
    audio_quality ENUM('none', 'poor', 'fair', 'good', 'excellent') DEFAULT 'fair',
    stability_rating ENUM('very_shaky', 'shaky', 'stable', 'very_stable') DEFAULT 'stable',
    
    -- Annotations and notes
    user_notes TEXT,
    annotations JSON COMMENT 'Time-based annotations within the video',
    key_moments JSON COMMENT 'Important timestamps and descriptions',
    
    -- Approval and review
    requires_approval BOOLEAN DEFAULT FALSE,
    approved_by_user_id CHAR(36) NULL,
    approved_at TIMESTAMP NULL,
    approval_notes TEXT,
    
    -- Usage and sharing
    shared_with_users JSON COMMENT 'Users who have access to this recording',
    external_sharing_enabled BOOLEAN DEFAULT FALSE,
    public_link VARCHAR(255),
    
    -- Status
    processing_status ENUM('uploading', 'processing', 'completed', 'failed', 'archived') DEFAULT 'completed',
    status ENUM('active', 'archived', 'deleted') DEFAULT 'active',
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (assessment_route_id) REFERENCES assessment_routes(id) ON DELETE SET NULL,
    FOREIGN KEY (site_id) REFERENCES sites(id) ON DELETE CASCADE,
    FOREIGN KEY (recorded_by_user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (approved_by_user_id) REFERENCES users(id) ON DELETE SET NULL,
    INDEX idx_recording_site_time (site_id, recording_start_time),
    INDEX idx_recording_user (recorded_by_user_id),
    INDEX idx_recording_route (assessment_route_id),
    INDEX idx_recording_content_type (content_type),
    INDEX idx_recording_status (processing_status, status),
    INDEX idx_recording_approval (requires_approval, approved_at)
) ENGINE=InnoDB COMMENT='Mobile recordings from field assessments';

-- ================================================================
-- TABLE 23: FIELD_REPORTS
-- ================================================================
CREATE TABLE field_reports (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    
    -- Report context
    site_id CHAR(36) NOT NULL,
    assessment_route_id CHAR(36) NULL,
    mobile_recording_id CHAR(36) NULL,
    created_by_user_id CHAR(36) NOT NULL,
    
    -- Report identification
    report_number VARCHAR(100) NOT NULL,
    report_title VARCHAR(255) NOT NULL,
    report_type ENUM('inspection', 'incident', 'safety', 'progress', 'compliance', 'maintenance', 'custom') NOT NULL,
    
    -- Report content
    executive_summary TEXT,
    detailed_findings TEXT NOT NULL,
    recommendations TEXT,
    follow_up_actions JSON COMMENT 'Required actions with deadlines',
    
    -- Assessment details
    assessment_date DATE NOT NULL,
    assessment_start_time TIME,
    assessment_end_time TIME,
    weather_conditions VARCHAR(100),
    site_conditions TEXT,
    
    -- Findings and observations
    safety_issues JSON COMMENT 'Identified safety issues',
    compliance_status JSON COMMENT 'Compliance with standards/regulations',
    progress_assessment JSON COMMENT 'Project progress evaluation',
    quality_issues JSON COMMENT 'Quality concerns or defects',
    
    -- Evidence and documentation
    photos JSON COMMENT 'Associated photo files and descriptions',
    videos JSON COMMENT 'Associated video files and descriptions',
    documents JSON COMMENT 'Additional documents or attachments',
    
    -- Scoring and ratings
    overall_safety_score DECIMAL(3, 2) COMMENT 'Overall safety score (0-10)',
    overall_quality_score DECIMAL(3, 2) COMMENT 'Overall quality score (0-10)',
    compliance_score DECIMAL(3, 2) COMMENT 'Compliance score (0-10)',
    progress_percentage DECIMAL(5, 2) COMMENT 'Estimated progress completion',
    
    -- People involved
    personnel_on_site JSON COMMENT 'Personnel present during assessment',
    interviewed_personnel JSON COMMENT 'Personnel interviewed',
    contractor_representatives JSON COMMENT 'Contractor reps present',
    
    -- Review and approval workflow
    review_status ENUM('draft', 'submitted', 'under_review', 'approved', 'rejected', 'archived') DEFAULT 'draft',
    submitted_at TIMESTAMP NULL,
    reviewed_by_user_id CHAR(36) NULL,
    reviewed_at TIMESTAMP NULL,
    review_comments TEXT,
    
    -- Distribution and notifications
    distribution_list JSON COMMENT 'Users/roles who should receive this report',
    notification_sent BOOLEAN DEFAULT FALSE,
    external_recipients JSON COMMENT 'External parties to notify',
    
    -- Follow-up tracking
    requires_follow_up BOOLEAN DEFAULT FALSE,
    follow_up_due_date DATE NULL,
    follow_up_assigned_to_user_id CHAR(36) NULL,
    follow_up_completed BOOLEAN DEFAULT FALSE,
    follow_up_notes TEXT,
    
    -- Report metadata
    report_template_used VARCHAR(100),
    estimated_completion_time_minutes INT,
    report_confidence ENUM('low', 'medium', 'high') DEFAULT 'high',
    
    -- Version control
    version_number INT DEFAULT 1,
    previous_version_id CHAR(36) NULL,
    
    -- Status
    status ENUM('active', 'superseded', 'archived') DEFAULT 'active',
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (site_id) REFERENCES sites(id) ON DELETE CASCADE,
    FOREIGN KEY (assessment_route_id) REFERENCES assessment_routes(id) ON DELETE SET NULL,
    FOREIGN KEY (mobile_recording_id) REFERENCES mobile_recordings(id) ON DELETE SET NULL,
    FOREIGN KEY (created_by_user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (reviewed_by_user_id) REFERENCES users(id) ON DELETE SET NULL,
    FOREIGN KEY (follow_up_assigned_to_user_id) REFERENCES users(id) ON DELETE SET NULL,
    FOREIGN KEY (previous_version_id) REFERENCES field_reports(id) ON DELETE SET NULL,
    UNIQUE KEY uk_report_number (site_id, report_number),
    INDEX idx_report_site_date (site_id, assessment_date),
    INDEX idx_report_creator (created_by_user_id),
    INDEX idx_report_type (report_type),
    INDEX idx_report_status (review_status, status),
    INDEX idx_report_follow_up (requires_follow_up, follow_up_due_date),
    INDEX idx_report_scores (overall_safety_score, overall_quality_score)
) ENGINE=InnoDB COMMENT='Field assessment reports and documentation';

-- ================================================================
-- FINAL VERIFICATION AND SUMMARY
-- ================================================================
SELECT 'COMPLETE Construction Management Schema (23 tables) created successfully!' as Status;

-- Show all created tables
SHOW TABLES;

-- Summary of what we've created:
SELECT 
    'Construction Management Database Complete!' as Message,
    '23 Tables Created' as Count,
    'Core: Companies, Groups, Sites, Users, Roles' as Core_Tables,
    'Advanced: AI Models, Detection Results, Safety Violations, Alerts' as AI_Tables,
    'Field: Assessment Routes, Mobile Recordings, Field Reports' as Field_Tables,
    'Zone: Site Zones, Site Maps, Interactive Controls' as Zone_Tables,
    'Security: User Sessions, Alert Escalations, Notifications' as Security_Tables;