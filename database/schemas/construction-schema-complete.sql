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
) ENGINE=InnoDB COMMENT='Individual construction sites';

-- ================================================================
-- TABLE 4: USERS
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
-- TABLE 5: ROLES
-- ================================================================
CREATE TABLE roles (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    company_id CHAR(36) NOT NULL,
    name VARCHAR(100) NOT NULL,
    display_name VARCHAR(150) NOT NULL,
    description TEXT,
    
    -- Role hierarchy (1=highest, 5=lowest)
    hierarchy_level ENUM('1', '2', '3', '4', '5') NOT NULL COMMENT '1=SYSADMIN, 2=EXEC, 3=GROUP_MGR, 4=SITE_MGR, 5=COORDINATOR',
    
    -- Permissions (JSON structure for flexibility)
    permissions JSON NOT NULL COMMENT 'Detailed permissions configuration',
    
    -- Scope limitations
    scope_type ENUM('global', 'group', 'site', 'personal') DEFAULT 'site',
    max_sites_access INT COMMENT 'Maximum sites this role can access',
    max_cameras_access INT COMMENT 'Maximum cameras this role can manage',
    
    -- Alert and escalation
    can_acknowledge_alerts BOOLEAN DEFAULT FALSE,
    can_create_alert_rules BOOLEAN DEFAULT FALSE,
    alert_escalation_level INT COMMENT 'Level in escalation chain',
    
    -- System administration
    can_manage_users BOOLEAN DEFAULT FALSE,
    can_manage_sites BOOLEAN DEFAULT FALSE,
    can_manage_cameras BOOLEAN DEFAULT FALSE,
    can_access_system_config BOOLEAN DEFAULT FALSE,
    
    -- Reporting and analytics
    can_generate_reports BOOLEAN DEFAULT TRUE,
    can_export_data BOOLEAN DEFAULT FALSE,
    can_access_analytics BOOLEAN DEFAULT TRUE,
    
    -- Field operations
    can_use_mobile_app BOOLEAN DEFAULT TRUE,
    can_create_field_reports BOOLEAN DEFAULT FALSE,
    can_control_cameras BOOLEAN DEFAULT FALSE,
    
    -- Zone and integration
    can_manage_zones BOOLEAN DEFAULT FALSE,
    can_execute_zone_actions BOOLEAN DEFAULT FALSE,
    can_configure_integrations BOOLEAN DEFAULT FALSE,
    
    -- Status
    is_active BOOLEAN DEFAULT TRUE,
    is_system_role BOOLEAN DEFAULT FALSE COMMENT 'Cannot be deleted',
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (company_id) REFERENCES companies(id) ON DELETE CASCADE,
    UNIQUE KEY uk_role_name (company_id, name),
    INDEX idx_role_company (company_id),
    INDEX idx_role_hierarchy (hierarchy_level),
    INDEX idx_role_active (is_active)
) ENGINE=InnoDB COMMENT='User roles and permissions';

-- ================================================================
-- TABLE 6: USER ROLES
-- ================================================================
CREATE TABLE user_roles (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    user_id CHAR(36) NOT NULL,
    role_id CHAR(36) NOT NULL,
    
    -- Assignment context
    assigned_by_user_id CHAR(36),
    assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Scope limitations for this assignment
    site_restrictions JSON COMMENT 'Specific sites this role assignment applies to',
    group_restrictions JSON COMMENT 'Specific groups this role assignment applies to',
    
    -- Temporary assignments
    valid_from TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    valid_until TIMESTAMP NULL COMMENT 'NULL for permanent assignments',
    
    -- Status
    is_active BOOLEAN DEFAULT TRUE,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE,
    FOREIGN KEY (assigned_by_user_id) REFERENCES users(id) ON DELETE SET NULL,
    UNIQUE KEY uk_user_role_active (user_id, role_id, is_active),
    INDEX idx_user_roles_user (user_id),
    INDEX idx_user_roles_role (role_id),
    INDEX idx_user_roles_active (is_active),
    INDEX idx_user_roles_validity (valid_from, valid_until)
) ENGINE=InnoDB COMMENT='User role assignments';

-- ================================================================
-- TABLE 7: USER SESSIONS
-- ================================================================
CREATE TABLE user_sessions (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    user_id CHAR(36) NOT NULL,
    session_token VARCHAR(255) NOT NULL UNIQUE,
    
    -- Session information
    ip_address VARCHAR(45) NOT NULL,
    user_agent TEXT,
    device_info JSON COMMENT 'Browser, OS, device type',
    
    -- Geographic information
    country VARCHAR(100),
    region VARCHAR(100),
    city VARCHAR(100),
    
    -- Session lifecycle
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_activity_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NOT NULL,
    
    -- Status
    is_active BOOLEAN DEFAULT TRUE,
    logout_reason ENUM('user_logout', 'timeout', 'forced_logout', 'security') NULL,
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_session_user (user_id),
    INDEX idx_session_token (session_token),
    INDEX idx_session_active (is_active),
    INDEX idx_session_expires (expires_at),
    INDEX idx_session_activity (last_activity_at)
) ENGINE=InnoDB COMMENT='User session tracking';

-- ================================================================
-- TABLE 8: SITE COORDINATES
-- ================================================================
CREATE TABLE site_coordinates (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    site_id CHAR(36) NOT NULL,
    
    -- Primary coordinates
    latitude DECIMAL(10, 7) NOT NULL,
    longitude DECIMAL(10, 7) NOT NULL,
    elevation_meters DECIMAL(8, 2),
    
    -- Coordinate system information
    coordinate_system VARCHAR(50) DEFAULT 'WGS84',
    projection VARCHAR(100),
    accuracy_meters DECIMAL(6, 2) COMMENT 'GPS accuracy in meters',
    
    -- Site boundaries and areas
    site_boundary JSON COMMENT 'Polygon coordinates for site boundary',
    construction_area JSON COMMENT 'Active construction area coordinates',
    restricted_areas JSON COMMENT 'Areas with access restrictions',
    
    -- Reference points
    main_entrance_coords JSON,
    office_location_coords JSON,
    emergency_assembly_point JSON,
    
    -- Surveying information
    survey_date DATE,
    surveyor_name VARCHAR(150),
    survey_accuracy_class VARCHAR(20),
    benchmark_reference VARCHAR(100),
    
    -- Address verification
    address_verified BOOLEAN DEFAULT FALSE,
    address_verification_date DATE,
    geocoding_service VARCHAR(50) COMMENT 'Service used for geocoding',
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (site_id) REFERENCES sites(id) ON DELETE CASCADE,
    UNIQUE KEY uk_site_coordinates (site_id),
    INDEX idx_coordinates_location (latitude, longitude),
    INDEX idx_coordinates_verified (address_verified)
) ENGINE=InnoDB COMMENT='Site geographic coordinates and boundaries';

-- ================================================================
-- TABLE 9: SITE ZONES
-- ================================================================
CREATE TABLE site_zones (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    site_id CHAR(36) NOT NULL,
    name VARCHAR(150) NOT NULL,
    description TEXT,
    
    -- Zone classification
    zone_type ENUM('safety', 'restricted', 'equipment', 'storage', 'office', 'parking', 'emergency', 'work_area', 'custom') NOT NULL,
    zone_category VARCHAR(100) COMMENT 'Sub-category within type',
    
    -- Geometric properties
    coordinates JSON NOT NULL COMMENT 'Polygon/circle coordinates defining the zone',
    area_sqm DECIMAL(10, 2),
    perimeter_meters DECIMAL(10, 2),
    
    -- Visual properties (for map display)
    color VARCHAR(7) DEFAULT '#FF0000' COMMENT 'Hex color code',
    opacity DECIMAL(3, 2) DEFAULT 0.30,
    border_color VARCHAR(7) DEFAULT '#000000',
    border_width INT DEFAULT 2,
    fill_pattern ENUM('solid', 'striped', 'dotted', 'crosshatch') DEFAULT 'solid',
    
    -- Zone template information
    template_id CHAR(36) NULL COMMENT 'Reference to zone template if used',
    template_name VARCHAR(100),
    
    -- Interactive features
    is_interactive BOOLEAN DEFAULT FALSE,
    click_actions JSON COMMENT 'Actions available when zone is clicked',
    hover_info JSON COMMENT 'Information displayed on hover',
    
    -- External data integration
    external_data_sources JSON COMMENT 'IoT sensors, SCADA systems feeding data to this zone',
    real_time_data_config JSON COMMENT 'Configuration for real-time data display',
    
    -- Safety and compliance
    safety_requirements JSON COMMENT 'PPE requirements, access restrictions',
    hazard_level ENUM('none', 'low', 'medium', 'high', 'critical') DEFAULT 'none',
    access_permissions JSON COMMENT 'User roles/IDs that can access this zone',
    
    -- Monitoring and alerts
    monitoring_enabled BOOLEAN DEFAULT FALSE,
    alert_triggers JSON COMMENT 'Conditions that trigger alerts in this zone',
    camera_coverage JSON COMMENT 'Cameras that monitor this zone',
    
    -- Event integration
    event_types JSON COMMENT 'Types of events that can occur in this zone',
    iot_device_ids JSON COMMENT 'IoT devices associated with this zone',
    
    -- Capacity and limits
    max_personnel INT COMMENT 'Maximum people allowed in zone',
    max_equipment INT COMMENT 'Maximum equipment pieces allowed',
    weight_limit_kg DECIMAL(10, 2),
    
    -- Scheduling
    active_hours JSON COMMENT 'Hours when zone restrictions are active',
    seasonal_adjustments JSON COMMENT 'Changes based on season/weather',
    
    -- Status and lifecycle
    status ENUM('active', 'inactive', 'under_construction', 'archived') DEFAULT 'active',
    effective_from TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    effective_until TIMESTAMP NULL,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (site_id) REFERENCES sites(id) ON DELETE CASCADE,
    INDEX idx_zone_site (site_id),
    INDEX idx_zone_type (zone_type),
    INDEX idx_zone_status (status),
    INDEX idx_zone_interactive (is_interactive),
    INDEX idx_zone_monitoring (monitoring_enabled),
    INDEX idx_zone_template (template_id)
) ENGINE=InnoDB COMMENT='Site zones for safety, equipment, and operational areas';

-- ================================================================
-- TABLE 10: SITE MAPS
-- ================================================================
CREATE TABLE site_maps (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    site_id CHAR(36) NOT NULL,
    name VARCHAR(150) NOT NULL,
    description TEXT,
    
    -- Map file information
    filename VARCHAR(255) NOT NULL,
    file_path VARCHAR(1000) NOT NULL,
    file_size_bytes BIGINT NOT NULL,
    file_format VARCHAR(20) NOT NULL COMMENT 'PNG, JPG, PDF, DWG, etc.',
    
    -- Map properties
    map_type ENUM('site_plan', 'floor_plan', 'elevation', 'aerial', 'survey', 'as_built') NOT NULL,
    scale_ratio VARCHAR(50) COMMENT 'e.g., 1:100, 1:500',
    resolution_dpi INT,
    dimensions_pixels JSON COMMENT 'Width and height in pixels',
    
    -- Coordinate system and calibration
    coordinate_system VARCHAR(50) DEFAULT 'WGS84',
    calibration_points JSON COMMENT 'Ground control points for geo-referencing',
    is_georeferenced BOOLEAN DEFAULT FALSE,
    
    -- Map bounds (for positioning elements)
    top_left_coords JSON COMMENT 'Real-world coordinates of top-left corner',
    bottom_right_coords JSON COMMENT 'Real-world coordinates of bottom-right corner',
    pixels_per_meter DECIMAL(10, 4) COMMENT 'Scale factor for positioning',
    
    -- Version control
    version VARCHAR(20) DEFAULT '1.0',
    revision_number INT DEFAULT 1,
    supersedes_map_id CHAR(36) NULL COMMENT 'Previous version of this map',
    
    -- Source information
    created_by_company VARCHAR(200),
    architect_engineer VARCHAR(200),
    drawing_date DATE,
    last_survey_date DATE,
    
    -- Usage settings
    is_primary BOOLEAN DEFAULT FALSE COMMENT 'Primary map for the site',
    display_order INT DEFAULT 1,
    zoom_levels JSON COMMENT 'Supported zoom levels',
    
    -- Overlays and layers
    available_layers JSON COMMENT 'Layer names that can be toggled on/off',
    default_layers JSON COMMENT 'Layers visible by default',
    
    -- Access control
    access_level ENUM('public', 'internal', 'restricted', 'confidential') DEFAULT 'internal',
    authorized_roles JSON COMMENT 'Roles that can view this map',
    
    -- Status
    status ENUM('active', 'draft', 'archived', 'superseded') DEFAULT 'active',
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (site_id) REFERENCES sites(id) ON DELETE CASCADE,
    FOREIGN KEY (supersedes_map_id) REFERENCES site_maps(id) ON DELETE SET NULL,
    INDEX idx_map_site (site_id),
    INDEX idx_map_type (map_type),
    INDEX idx_map_status (status),
    INDEX idx_map_primary (is_primary),
    INDEX idx_map_georeferenced (is_georeferenced)
) ENGINE=InnoDB COMMENT='Site maps and technical drawings';

-- ================================================================
-- TABLE 11: AI MODELS
-- ================================================================
CREATE TABLE ai_models (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    name VARCHAR(150) NOT NULL,
    display_name VARCHAR(200) NOT NULL,
    description TEXT,
    
    -- Model information
    model_type ENUM('object_detection', 'classification', 'segmentation', 'pose_estimation') NOT NULL,
    framework VARCHAR(50) NOT NULL COMMENT 'YOLOv8, TensorRT, ONNX, etc.',
    version VARCHAR(50) NOT NULL,
    
    -- Model files and paths
    model_file_path VARCHAR(1000) NOT NULL,
    config_file_path VARCHAR(1000),
    weights_file_path VARCHAR(1000),
    model_size_mb DECIMAL(8,2),
    
    -- Model capabilities
    supported_classes JSON NOT NULL COMMENT 'Classes the model can detect/classify',
    input_resolution JSON NOT NULL COMMENT 'Required input image dimensions',
    supported_formats JSON COMMENT 'Image formats supported',
    
    -- Performance characteristics
    inference_time_ms DECIMAL(8,2) COMMENT 'Average inference time per frame',
    memory_requirements_mb INT COMMENT 'Memory required to load model',
    gpu_required BOOLEAN DEFAULT FALSE,
    min_confidence_threshold DECIMAL(3,2) DEFAULT 0.1,
    max_confidence_threshold DECIMAL(3,2) DEFAULT 1.0,
    
    -- Training information
    training_dataset VARCHAR(200),
    training_date DATE,
    trained_by VARCHAR(150),
    accuracy_metrics JSON COMMENT 'mAP, precision, recall, etc.',
    
    -- Deployment settings
    default_confidence DECIMAL(3,2) DEFAULT 0.5,
    default_iou_threshold DECIMAL(3,2) DEFAULT 0.4,
    preprocessing_config JSON COMMENT 'Image preprocessing requirements',
    postprocessing_config JSON COMMENT 'Output processing configuration',
    
    -- Construction-specific settings
    construction_categories JSON COMMENT 'PPE, equipment, personnel categories',
    safety_rule_mappings JSON COMMENT 'Mapping detections to safety violations',
    
    -- Version control and updates
    parent_model_id CHAR(36) NULL COMMENT 'Base model this was derived from',
    is_custom_trained BOOLEAN DEFAULT FALSE,
    update_available BOOLEAN DEFAULT FALSE,
    update_notes TEXT,
    
    -- Status and deployment
    status ENUM('active', 'testing', 'deprecated', 'failed') DEFAULT 'testing',
    deployment_date DATE,
    last_tested_date DATE,
    test_results JSON COMMENT 'Latest test results',
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (parent_model_id) REFERENCES ai_models(id) ON DELETE SET NULL,
    INDEX idx_model_type (model_type),
    INDEX idx_model_status (status),
    INDEX idx_model_framework (framework),
    INDEX idx_model_custom (is_custom_trained),
    INDEX idx_model_parent (parent_model_id)
) ENGINE=InnoDB COMMENT='AI models for construction site analysis';

-- Continue with remaining 12 tables...
-- (Part 2 of construction schema will be in next file due to size limit)

SELECT 'Construction Management Schema Part 1 (11 tables) created successfully!' as Status;
SHOW TABLES;