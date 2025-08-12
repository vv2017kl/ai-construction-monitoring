# 🗃️ MASTER DATABASE SCHEMA - AI Construction Management System

## 📋 **Document Information**
- **Document Type**: Master Database Schema Reference
- **Version**: 1.0.0
- **Last Updated**: 2025-01-12
- **Created From**: Screen Analysis #01 (My Dashboard)
- **Status**: ✅ Active - Referenced by all screen analyses

---

## 🎯 **Purpose & Usage**

This document serves as the **single source of truth** for all database table definitions in the AI Construction Management System. 

### **How to Use:**
- **Screen Analysis Documents**: Reference tables by name only
- **Backend Developers**: Use this for complete DDL statements
- **Database Administrators**: Primary reference for schema management
- **Updates**: Add new tables/fields as discovered in screen analyses

---

## 📊 **Database Overview**

### **Core Entity Count:**
- **Sites & Locations**: 3 tables
- **Personnel & Users**: 3 tables  
- **Cameras & Monitoring**: 2 tables
- **AI & Detection**: 3 tables
- **Alerts & Safety**: 3 tables
- **Analytics & Reporting**: 2 tables
- **System & Configuration**: 3 tables

**Total Tables**: 19 tables

---

## 🏗️ **SITES & LOCATIONS**

### **sites**
```sql
CREATE TABLE sites (
    id UUID PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    code VARCHAR(50) UNIQUE NOT NULL,
    address TEXT,
    coordinates POINT,
    status ENUM('active', 'inactive', 'maintenance') DEFAULT 'active',
    type ENUM('commercial', 'residential', 'industrial', 'infrastructure'),
    phase ENUM('planning', 'construction', 'finishing', 'completed'),
    progress_percentage DECIMAL(5,2) DEFAULT 0.00,
    budget DECIMAL(15,2),
    completion_date DATE,
    manager_id UUID,
    
    -- Weather Integration
    weather_temp INT,
    weather_condition VARCHAR(100),
    weather_wind_speed VARCHAR(50),
    weather_humidity DECIMAL(5,2),
    weather_last_updated TIMESTAMP,
    weather_api_source VARCHAR(100),
    
    -- Activity Tracking
    last_activity_timestamp TIMESTAMP,
    last_activity_type VARCHAR(100),
    activity_summary TEXT,
    
    -- Camera Metrics
    total_cameras INT DEFAULT 0,
    active_cameras INT DEFAULT 0,
    offline_cameras INT DEFAULT 0,
    maintenance_cameras INT DEFAULT 0,
    
    -- ✅ GEOSPATIAL VIEW ENHANCEMENTS
    region VARCHAR(100), -- Geographic region for map grouping
    timezone VARCHAR(100), -- Site timezone for proper time display
    site_boundary_coordinates POLYGON, -- Geographic boundary for 3D visualization
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (manager_id) REFERENCES users(id),
    
    INDEX idx_sites_status (status),
    INDEX idx_sites_type_phase (type, phase),
    INDEX idx_sites_coordinates (coordinates),
    INDEX idx_sites_manager (manager_id),
    INDEX idx_sites_weather_updated (weather_last_updated),
    -- ✅ GEOSPATIAL INDEXES
    INDEX idx_sites_region (region),
    INDEX idx_sites_boundary (site_boundary_coordinates)
);
```

### **zones**
```sql
CREATE TABLE zones (
    id UUID PRIMARY KEY,
    site_id UUID NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    zone_type ENUM('construction', 'safety', 'restricted', 'office', 'storage', 'parking') NOT NULL,
    coordinates POLYGON, -- Geographic boundary
    safety_level ENUM('safe', 'caution', 'restricted', 'danger') DEFAULT 'safe',
    required_ppe JSON, -- ["hardhat", "safety_vest", "boots"]
    access_level ENUM('public', 'personnel', 'authorized', 'management') DEFAULT 'personnel',
    
    -- Zone status
    status ENUM('active', 'inactive', 'under_construction') DEFAULT 'active',
    capacity_limit INT,
    current_occupancy INT DEFAULT 0,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (site_id) REFERENCES sites(id),
    
    INDEX idx_zones_site (site_id),
    INDEX idx_zones_type (zone_type),
    INDEX idx_zones_safety (safety_level),
    INDEX idx_zones_status (status)
);
```

### **weather_data**
```sql
CREATE TABLE weather_data (
    id UUID PRIMARY KEY,
    site_id UUID NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Weather metrics
    temperature DECIMAL(5,2),
    humidity DECIMAL(5,2),
    wind_speed DECIMAL(5,2),
    wind_direction VARCHAR(10), -- 'N', 'NE', 'E', etc.
    pressure DECIMAL(7,2),
    visibility DECIMAL(5,2), -- Kilometers
    uv_index DECIMAL(3,1),
    
    -- Conditions
    condition VARCHAR(100), -- 'Partly Cloudy', 'Rain', etc.
    precipitation DECIMAL(5,2), -- mm/hour
    cloud_cover DECIMAL(5,2), -- Percentage
    
    -- Safety impact
    work_safety_score DECIMAL(3,1), -- 0-10 (weather suitability for construction)
    safety_warnings JSON, -- ['high_wind', 'low_visibility', 'extreme_temp']
    recommended_precautions JSON,
    
    -- Data source
    weather_api_source VARCHAR(100),
    api_response_raw JSON,
    
    FOREIGN KEY (site_id) REFERENCES sites(id),
    
    INDEX idx_weather_site_time (site_id, timestamp DESC),
    INDEX idx_weather_conditions (condition),
    INDEX idx_weather_safety (work_safety_score)
);
```

---

## 👥 **PERSONNEL & USERS**

### **users**
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    display_name VARCHAR(255),
    phone VARCHAR(20),
    avatar_url VARCHAR(500),
    
    -- Authentication
    password_hash VARCHAR(255) NOT NULL,
    email_verified BOOLEAN DEFAULT FALSE,
    last_login TIMESTAMP,
    failed_login_attempts INT DEFAULT 0,
    locked_until TIMESTAMP NULL,
    
    -- Role & Permissions
    role ENUM('admin', 'site_manager', 'supervisor', 'worker', 'security', 'readonly') NOT NULL,
    permissions JSON, -- Array of specific permissions
    company_id UUID,
    department VARCHAR(100),
    
    -- Profile
    hire_date DATE,
    employee_id VARCHAR(50),
    certification_level VARCHAR(100),
    emergency_contact JSON,
    
    status ENUM('active', 'inactive', 'suspended') DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_users_username (username),
    INDEX idx_users_email (email),
    INDEX idx_users_role (role),
    INDEX idx_users_company (company_id),
    INDEX idx_users_status (status)
);
```

### **user_site_access**
```sql
CREATE TABLE user_site_access (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL,
    site_id UUID NOT NULL,
    access_level ENUM('view', 'manage', 'admin') DEFAULT 'view',
    granted_by UUID NOT NULL,
    granted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NULL,
    status ENUM('active', 'suspended', 'expired') DEFAULT 'active',
    
    -- Permission details
    permissions JSON, -- Specific permissions array
    zone_restrictions JSON, -- Array of restricted zone IDs
    time_restrictions JSON, -- Time-based access rules
    
    -- Audit fields
    last_accessed TIMESTAMP,
    access_count INT DEFAULT 0,
    
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (site_id) REFERENCES sites(id), 
    FOREIGN KEY (granted_by) REFERENCES users(id),
    
    UNIQUE KEY unique_user_site (user_id, site_id),
    INDEX idx_user_access_user (user_id),
    INDEX idx_user_access_site (site_id),
    INDEX idx_user_access_level (access_level),
    INDEX idx_user_access_status (status),
    INDEX idx_user_access_expires (expires_at)
);
```

### **site_personnel**
```sql
CREATE TABLE site_personnel (
    id UUID PRIMARY KEY,
    site_id UUID NOT NULL,
    user_id UUID NOT NULL,
    role VARCHAR(100),
    status ENUM('active', 'inactive', 'break', 'offsite') DEFAULT 'active',
    check_in_time TIMESTAMP,
    check_out_time TIMESTAMP,
    
    -- Real-time Location Tracking
    current_zone_id UUID,
    current_zone_name VARCHAR(100),
    last_known_coordinates POINT,
    location_updated_at TIMESTAMP,
    
    -- PPE Compliance Tracking
    ppe_compliance_score DECIMAL(5,2) DEFAULT 0.00,
    ppe_status JSON, -- {"hardhat": true, "vest": true, "boots": false}
    last_ppe_check_timestamp TIMESTAMP,
    ppe_violations_count INT DEFAULT 0,
    
    -- Activity Tracking
    last_detection_timestamp TIMESTAMP,
    last_detection_camera_id UUID,
    activity_level ENUM('low', 'moderate', 'high') DEFAULT 'moderate',
    break_start_time TIMESTAMP NULL,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (site_id) REFERENCES sites(id),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (current_zone_id) REFERENCES zones(id),
    FOREIGN KEY (last_detection_camera_id) REFERENCES cameras(id),
    
    UNIQUE KEY unique_site_user_active (site_id, user_id, status),
    INDEX idx_personnel_site_status (site_id, status),
    INDEX idx_personnel_zone (current_zone_id),
    INDEX idx_personnel_compliance (ppe_compliance_score),
    INDEX idx_personnel_activity (last_detection_timestamp)
);
```

---

## 📹 **CAMERAS & MONITORING**

### **cameras**
```sql
CREATE TABLE cameras (
    id UUID PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    camera_type ENUM('fixed', 'ptz', 'fisheye', 'thermal', 'infrared') NOT NULL,
    manufacturer VARCHAR(100),
    model VARCHAR(100),
    serial_number VARCHAR(100),
    
    -- Technical specifications
    resolution VARCHAR(20), -- '1920x1080'
    frame_rate INT DEFAULT 30,
    field_of_view DECIMAL(5,2), -- Degrees
    night_vision BOOLEAN DEFAULT FALSE,
    weather_resistant BOOLEAN DEFAULT FALSE,
    
    -- ✅ LIVE VIEW ENHANCEMENTS
    audio_enabled BOOLEAN DEFAULT FALSE,
    ptz_capabilities JSON, -- PTZ range, presets, speed settings
    recording_capabilities JSON, -- Max resolution, frame rates, bitrate limits
    
    -- Network & streaming
    ip_address INET,
    mac_address VARCHAR(17),
    rtsp_url VARCHAR(500),
    http_url VARCHAR(500),
    
    -- Status
    status ENUM('active', 'inactive', 'maintenance', 'offline') DEFAULT 'active',
    installation_date DATE,
    last_maintenance DATE,
    maintenance_schedule VARCHAR(100),
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_cameras_type (camera_type),
    INDEX idx_cameras_status (status),
    INDEX idx_cameras_ip (ip_address),
    INDEX idx_cameras_maintenance (last_maintenance)
);
```

### **site_cameras**
```sql
CREATE TABLE site_cameras (
    id UUID PRIMARY KEY,
    site_id UUID NOT NULL,
    camera_id UUID NOT NULL,
    zoneminder_monitor_id INT NOT NULL, -- ZoneMinder integration
    
    -- Positioning for 3D mapping
    coordinates POINT,
    elevation DECIMAL(8,2), -- Meters above sea level
    orientation_angle DECIMAL(5,2), -- 0-360 degrees
    tilt_angle DECIMAL(5,2), -- -90 to +90 degrees
    
    -- Zone coverage
    primary_zone_id UUID,
    coverage_zones JSON, -- Array of zone IDs this camera covers
    
    -- Site-specific status
    status ENUM('active', 'inactive', 'maintenance', 'offline') DEFAULT 'active',
    last_online TIMESTAMP,
    health_score DECIMAL(3,1), -- 0-10 camera health rating
    
    -- ✅ GEOSPATIAL VIEW ENHANCEMENTS
    region VARCHAR(100), -- Geographic region grouping
    zone_coverage JSON, -- Array of zone IDs this camera covers
    field_of_view DECIMAL(5,2), -- Camera FOV in degrees for 3D visualization
    detection_range DECIMAL(8,2), -- Detection range in meters
    
    -- ✅ LIVE VIEW ENHANCEMENTS
    current_zoom_level DECIMAL(5,2) DEFAULT 1.0, -- Current PTZ zoom level
    recording_active BOOLEAN DEFAULT FALSE, -- Current recording status
    stream_quality ENUM('low', 'medium', 'high') DEFAULT 'high', -- Current stream quality
    
    FOREIGN KEY (site_id) REFERENCES sites(id),
    FOREIGN KEY (camera_id) REFERENCES cameras(id),
    FOREIGN KEY (primary_zone_id) REFERENCES zones(id),
    
    UNIQUE KEY unique_site_camera (site_id, camera_id),
    UNIQUE KEY unique_zm_monitor (zoneminder_monitor_id),
    INDEX idx_site_cameras_site (site_id),
    INDEX idx_site_cameras_status (status),
    INDEX idx_site_cameras_zone (primary_zone_id),
    INDEX idx_site_cameras_health (health_score),
    -- ✅ GEOSPATIAL INDEXES
    INDEX idx_site_cameras_region (region),
    INDEX idx_site_cameras_coordinates (coordinates),
    INDEX idx_site_cameras_elevation (elevation),
    -- ✅ LIVE VIEW INDEXES
    INDEX idx_site_cameras_recording (recording_active),
    INDEX idx_site_cameras_zoom (current_zoom_level)
);
```

---

## 🤖 **AI & DETECTION**

### **ai_detections**
```sql
CREATE TABLE ai_detections (
    id UUID PRIMARY KEY,
    camera_id UUID NOT NULL,
    site_id UUID NOT NULL,
    zone_id UUID,
    zone_name VARCHAR(100),
    
    -- Detection Data
    detection_type ENUM('person', 'vehicle', 'ppe', 'safety_violation', 'equipment', 'activity'),
    person_count INT DEFAULT 0,
    confidence_score DECIMAL(5,2),
    overall_confidence DECIMAL(5,2),
    
    -- AI Results
    bounding_boxes JSON, -- All detection coordinates
    detection_results JSON, -- Complete AI model response
    ppe_compliance_data JSON, -- Detailed PPE analysis
    safety_violations JSON, -- List of detected violations
    
    -- Activity Analysis
    activity_summary TEXT,
    activity_level ENUM('low', 'moderate', 'high'),
    risk_assessment ENUM('safe', 'caution', 'danger'),
    safety_score DECIMAL(5,2),
    
    -- Media Evidence
    snapshot_image_url VARCHAR(500),
    video_clip_url VARCHAR(500),
    annotated_image_url VARCHAR(500),
    
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    processed BOOLEAN DEFAULT FALSE,
    alert_generated BOOLEAN DEFAULT FALSE,
    alert_ids JSON, -- Array of generated alert IDs
    
    -- Processing Metadata
    model_version VARCHAR(50),
    processing_time_ms INT,
    ai_server_id VARCHAR(100),
    
    FOREIGN KEY (camera_id) REFERENCES cameras(id),
    FOREIGN KEY (site_id) REFERENCES sites(id),
    FOREIGN KEY (zone_id) REFERENCES zones(id),
    
    INDEX idx_detections_camera_time (camera_id, timestamp DESC),
    INDEX idx_detections_site_time (site_id, timestamp DESC),
    INDEX idx_detections_zone (zone_id),
    INDEX idx_detections_type (detection_type),
    INDEX idx_detections_alerts (alert_generated),
    INDEX idx_detections_confidence (confidence_score),
    INDEX idx_detections_processed (processed, timestamp)
);
```

### **ai_models**
```sql
CREATE TABLE ai_models (
    id UUID PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    model_type ENUM('person_detection', 'ppe_detection', 'vehicle_detection', 'activity_recognition'),
    provider VARCHAR(100), -- 'roboflow', 'custom', 'openai', etc.
    
    -- Model configuration
    endpoint_url VARCHAR(500),
    model_version VARCHAR(50),
    confidence_threshold DECIMAL(5,2) DEFAULT 0.50,
    overlap_threshold DECIMAL(5,2) DEFAULT 0.30,
    
    -- Performance metrics
    accuracy_score DECIMAL(5,2),
    precision_score DECIMAL(5,2),
    recall_score DECIMAL(5,2),
    avg_processing_time_ms INT,
    
    -- Status & lifecycle
    status ENUM('active', 'inactive', 'training', 'deprecated') DEFAULT 'active',
    deployed_at TIMESTAMP,
    last_updated TIMESTAMP,
    
    -- Configuration
    input_requirements JSON, -- Image size, format, etc.
    output_format JSON, -- Expected response structure
    api_configuration JSON, -- API keys, headers, etc.
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_models_type (model_type),
    INDEX idx_models_provider (provider),
    INDEX idx_models_status (status),
    INDEX idx_models_performance (accuracy_score DESC)
);
```

### **event_correlations**
```sql
CREATE TABLE event_correlations (
    id UUID PRIMARY KEY,
    zoneminder_event_id BIGINT NOT NULL,
    ai_detection_id UUID NOT NULL,
    correlation_confidence DECIMAL(5,2),
    correlation_type ENUM('direct', 'temporal', 'spatial') NOT NULL,
    time_diff_seconds INT, -- Time difference between ZM event and AI detection
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (ai_detection_id) REFERENCES ai_detections(id),
    
    INDEX idx_correlations_zm_event (zoneminder_event_id),
    INDEX idx_correlations_ai_detection (ai_detection_id),
    INDEX idx_correlations_confidence (correlation_confidence)
);
```

### **recording_sessions**
```sql
CREATE TABLE recording_sessions (
    id UUID PRIMARY KEY,
    camera_id UUID NOT NULL,
    site_id UUID NOT NULL,
    
    -- Session details
    session_type ENUM('manual', 'scheduled', 'triggered', 'continuous') NOT NULL,
    trigger_type ENUM('user_initiated', 'ai_detection', 'motion', 'alert', 'schedule') DEFAULT 'user_initiated',
    trigger_event_id UUID, -- Reference to alert or detection that triggered recording
    
    -- Timing
    start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    end_time TIMESTAMP NULL,
    planned_duration_seconds INT,
    actual_duration_seconds INT,
    
    -- Quality & Storage
    recording_quality ENUM('low', 'medium', 'high', 'ultra') DEFAULT 'high',
    resolution VARCHAR(20), -- '1920x1080'
    frame_rate INT DEFAULT 30,
    bitrate_kbps INT,
    
    -- File information
    file_path VARCHAR(500),
    file_size_mb DECIMAL(10,2),
    segment_count INT DEFAULT 1,
    current_segment INT DEFAULT 1,
    storage_location VARCHAR(500),
    
    -- Status
    status ENUM('starting', 'active', 'stopping', 'completed', 'failed', 'interrupted') DEFAULT 'starting',
    error_message TEXT,
    
    -- Metadata
    include_ai_overlay BOOLEAN DEFAULT FALSE,
    retention_days INT DEFAULT 30,
    created_by UUID,
    
    -- ZoneMinder Integration
    zoneminder_event_id BIGINT,
    
    FOREIGN KEY (camera_id) REFERENCES cameras(id),
    FOREIGN KEY (site_id) REFERENCES sites(id),
    FOREIGN KEY (trigger_event_id) REFERENCES alerts(id),
    FOREIGN KEY (created_by) REFERENCES users(id),
    
    INDEX idx_recording_camera_active (camera_id, status),
    INDEX idx_recording_site_time (site_id, start_time DESC),
    INDEX idx_recording_status (status),
    INDEX idx_recording_trigger (trigger_type, trigger_event_id)
);
```

---

## 🚨 **ALERTS & SAFETY**

### **alerts**
```sql
CREATE TABLE alerts (
    id UUID PRIMARY KEY,
    site_id UUID NOT NULL,
    camera_id UUID,
    zone_id UUID,
    
    -- Alert Information
    title VARCHAR(255) NOT NULL,
    description TEXT,
    priority ENUM('critical', 'high', 'medium', 'low', 'info') NOT NULL,
    status ENUM('open', 'acknowledged', 'investigating', 'resolved', 'false_positive') DEFAULT 'open',
    alert_type VARCHAR(100), -- 'ppe_violation', 'safety_breach', 'unauthorized_access'
    
    -- AI Integration
    detection_id UUID, -- Link to AI detection that triggered this alert
    confidence_score DECIMAL(5,2),
    ai_model_used VARCHAR(100),
    detection_data JSON, -- Complete AI detection results
    
    -- Evidence
    primary_image_url VARCHAR(500),
    secondary_images JSON, -- Array of additional images
    video_clip_url VARCHAR(500),
    annotated_evidence_url VARCHAR(500),
    
    -- Workflow
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    acknowledged_at TIMESTAMP NULL,
    acknowledged_by UUID NULL,
    acknowledged_notes TEXT,
    investigating_started_at TIMESTAMP NULL,
    investigating_by UUID NULL,
    resolved_at TIMESTAMP NULL,
    resolved_by UUID NULL,
    resolution_notes TEXT,
    resolution_type ENUM('fixed', 'false_positive', 'training_needed', 'policy_update'),
    
    -- Impact Assessment
    severity_score DECIMAL(5,2), -- 0-10 impact rating
    affected_personnel_count INT DEFAULT 0,
    estimated_risk_level ENUM('low', 'medium', 'high', 'critical'),
    
    -- Escalation & Notifications
    escalated BOOLEAN DEFAULT FALSE,
    escalated_at TIMESTAMP NULL,
    escalated_to UUID NULL,
    notification_sent BOOLEAN DEFAULT FALSE,
    notification_channels JSON, -- ['email', 'sms', 'push', 'radio']
    
    FOREIGN KEY (site_id) REFERENCES sites(id),
    FOREIGN KEY (camera_id) REFERENCES cameras(id),
    FOREIGN KEY (zone_id) REFERENCES zones(id),
    FOREIGN KEY (detection_id) REFERENCES ai_detections(id),
    FOREIGN KEY (acknowledged_by) REFERENCES users(id),
    FOREIGN KEY (investigating_by) REFERENCES users(id),
    FOREIGN KEY (resolved_by) REFERENCES users(id),
    FOREIGN KEY (escalated_to) REFERENCES users(id),
    
    INDEX idx_alerts_site_priority (site_id, priority, status),
    INDEX idx_alerts_status_time (status, timestamp DESC),
    INDEX idx_alerts_camera (camera_id),
    INDEX idx_alerts_assigned (acknowledged_by, investigating_by),
    INDEX idx_alerts_detection (detection_id),
    INDEX idx_alerts_escalated (escalated, escalated_at)
);
```

### **safety_metrics**
```sql
CREATE TABLE safety_metrics (
    id UUID PRIMARY KEY,
    site_id UUID NOT NULL,
    date DATE NOT NULL,
    hour INT, -- Hourly granularity for real-time dashboard
    
    -- Core Safety Metrics
    safety_score DECIMAL(3,1), -- 0.0 to 10.0
    ppe_compliance_rate DECIMAL(5,2), -- Percentage
    incident_count INT DEFAULT 0,
    near_miss_count INT DEFAULT 0,
    personnel_violations INT DEFAULT 0,
    equipment_violations INT DEFAULT 0,
    
    -- Detailed PPE Breakdown
    hardhat_compliance_rate DECIMAL(5,2),
    vest_compliance_rate DECIMAL(5,2),
    boots_compliance_rate DECIMAL(5,2),
    gloves_compliance_rate DECIMAL(5,2),
    total_ppe_checks INT DEFAULT 0,
    
    -- Personnel Metrics
    total_personnel_detected INT DEFAULT 0,
    peak_personnel_count INT DEFAULT 0,
    average_personnel_count DECIMAL(5,2),
    unauthorized_personnel_count INT DEFAULT 0,
    
    -- Activity Metrics
    total_detections INT DEFAULT 0,
    high_risk_activities INT DEFAULT 0,
    safe_activities INT DEFAULT 0,
    
    -- Trend Analysis (Auto-calculated)
    day_comparison DECIMAL(5,2), -- % change from previous day
    week_comparison DECIMAL(5,2), -- % change from last week
    month_comparison DECIMAL(5,2), -- % change from last month
    
    -- Weather Correlation
    weather_temp INT,
    weather_condition VARCHAR(50),
    weather_impact_score DECIMAL(3,1), -- How weather affected safety
    
    calculated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (site_id) REFERENCES sites(id),
    
    UNIQUE KEY unique_site_date_hour (site_id, date, hour),
    INDEX idx_safety_site_date (site_id, date DESC),
    INDEX idx_safety_score (safety_score),
    INDEX idx_safety_compliance (ppe_compliance_rate),
    INDEX idx_safety_calculated (calculated_at)
);
```

### **activity_feed**
```sql
CREATE TABLE activity_feed (
    id UUID PRIMARY KEY,
    site_id UUID NOT NULL,
    activity_type ENUM('detection', 'alert', 'personnel', 'camera', 'system') NOT NULL,
    
    -- Activity details
    title VARCHAR(255) NOT NULL,
    description TEXT,
    severity ENUM('info', 'low', 'medium', 'high', 'critical') DEFAULT 'info',
    
    -- Source references
    detection_id UUID NULL,
    alert_id UUID NULL,
    camera_id UUID NULL,
    user_id UUID NULL,
    
    -- Activity metadata
    metadata JSON, -- Flexible data storage
    thumbnail_url VARCHAR(500),
    
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    read_by JSON, -- Array of user IDs who have seen this activity
    
    -- Dashboard display
    show_on_dashboard BOOLEAN DEFAULT TRUE,
    priority_score DECIMAL(3,1) DEFAULT 5.0, -- For sorting
    
    FOREIGN KEY (site_id) REFERENCES sites(id),
    FOREIGN KEY (detection_id) REFERENCES ai_detections(id),
    FOREIGN KEY (alert_id) REFERENCES alerts(id),
    FOREIGN KEY (camera_id) REFERENCES cameras(id),
    FOREIGN KEY (user_id) REFERENCES users(id),
    
    INDEX idx_activity_site_time (site_id, timestamp DESC),
    INDEX idx_activity_type (activity_type),
    INDEX idx_activity_severity (severity),
    INDEX idx_activity_dashboard (show_on_dashboard, priority_score DESC)
);
```

---

## 📊 **ANALYTICS & REPORTING**

### **reports**
```sql
CREATE TABLE reports (
    id UUID PRIMARY KEY,
    site_id UUID NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    report_type ENUM('safety', 'compliance', 'activity', 'performance', 'custom') NOT NULL,
    
    -- Report configuration
    parameters JSON, -- Report generation parameters
    schedule_cron VARCHAR(100), -- Cron expression for scheduled reports
    output_format ENUM('pdf', 'excel', 'csv', 'json') DEFAULT 'pdf',
    
    -- Generation tracking
    created_by UUID NOT NULL,
    last_generated TIMESTAMP,
    generation_status ENUM('pending', 'generating', 'completed', 'failed') DEFAULT 'pending',
    file_url VARCHAR(500),
    file_size_bytes BIGINT,
    
    -- Access control
    visibility ENUM('private', 'site', 'company', 'public') DEFAULT 'site',
    shared_with JSON, -- Array of user IDs with access
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (site_id) REFERENCES sites(id),
    FOREIGN KEY (created_by) REFERENCES users(id),
    
    INDEX idx_reports_site (site_id),
    INDEX idx_reports_type (report_type),
    INDEX idx_reports_creator (created_by),
    INDEX idx_reports_schedule (schedule_cron),
    INDEX idx_reports_status (generation_status)
);
```

### **analytics_cache**
```sql
CREATE TABLE analytics_cache (
    id UUID PRIMARY KEY,
    site_id UUID NOT NULL,
    metric_type VARCHAR(100) NOT NULL, -- 'dashboard_summary', 'safety_trends', etc.
    time_period VARCHAR(50) NOT NULL, -- 'hourly', 'daily', 'weekly', 'monthly'
    
    -- Cache data
    data JSON NOT NULL,
    calculated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NOT NULL,
    
    -- Cache metadata
    calculation_time_ms INT,
    data_points_count INT,
    
    FOREIGN KEY (site_id) REFERENCES sites(id),
    
    UNIQUE KEY unique_cache_key (site_id, metric_type, time_period),
    INDEX idx_cache_expires (expires_at),
    INDEX idx_cache_site_metric (site_id, metric_type),
    INDEX idx_cache_calculated (calculated_at DESC)
);
```

---

## ⚙️ **SYSTEM & CONFIGURATION**

### **system_config**
```sql
CREATE TABLE system_config (
    id UUID PRIMARY KEY,
    config_key VARCHAR(255) UNIQUE NOT NULL,
    config_value JSON NOT NULL,
    config_type ENUM('string', 'number', 'boolean', 'json', 'array') NOT NULL,
    description TEXT,
    
    -- Configuration metadata
    category VARCHAR(100), -- 'ai', 'camera', 'alerts', 'system'
    is_sensitive BOOLEAN DEFAULT FALSE, -- For passwords, API keys
    requires_restart BOOLEAN DEFAULT FALSE,
    
    -- Change tracking
    created_by UUID,
    updated_by UUID,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (created_by) REFERENCES users(id),
    FOREIGN KEY (updated_by) REFERENCES users(id),
    
    INDEX idx_config_category (category),
    INDEX idx_config_sensitive (is_sensitive),
    INDEX idx_config_updated (updated_at DESC)
);
```

### **audit_logs**
```sql
CREATE TABLE audit_logs (
    id UUID PRIMARY KEY,
    user_id UUID,
    action VARCHAR(255) NOT NULL,
    resource_type VARCHAR(100), -- 'alert', 'camera', 'site', etc.
    resource_id UUID,
    
    -- Action details
    old_values JSON,
    new_values JSON,
    ip_address INET,
    user_agent TEXT,
    
    -- Context
    site_id UUID,
    session_id VARCHAR(255),
    request_id VARCHAR(255),
    
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (site_id) REFERENCES sites(id),
    
    INDEX idx_audit_user_time (user_id, timestamp DESC),
    INDEX idx_audit_resource (resource_type, resource_id),
    INDEX idx_audit_site (site_id),
    INDEX idx_audit_action (action),
    INDEX idx_audit_timestamp (timestamp DESC)
);
```

### **notifications**
```sql
CREATE TABLE notifications (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL,
    title VARCHAR(255) NOT NULL,
    message TEXT,
    notification_type ENUM('alert', 'system', 'report', 'reminder') NOT NULL,
    
    -- Notification data
    related_id UUID, -- ID of related alert, report, etc.
    related_type VARCHAR(100), -- 'alert', 'report', 'detection'
    data JSON, -- Additional notification data
    
    -- Delivery
    channels JSON, -- ['in_app', 'email', 'sms', 'push']
    sent_at TIMESTAMP,
    delivery_status JSON, -- Status per channel
    
    -- User interaction
    read_at TIMESTAMP,
    action_taken VARCHAR(100), -- 'acknowledged', 'dismissed', 'clicked'
    action_taken_at TIMESTAMP,
    
    -- Priority and expiry
    priority ENUM('low', 'medium', 'high', 'urgent') DEFAULT 'medium',
    expires_at TIMESTAMP,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id),
    
    INDEX idx_notifications_user_time (user_id, created_at DESC),
    INDEX idx_notifications_type (notification_type),
    INDEX idx_notifications_unread (user_id, read_at),
    INDEX idx_notifications_priority (priority, created_at DESC),
    INDEX idx_notifications_expires (expires_at)
);
```

---

## 📈 **Database Statistics**

### **Table Size Estimates (Production)**
- **High Volume**: `ai_detections` (1M+ records/month), `activity_feed`, `audit_logs`
- **Medium Volume**: `alerts`, `safety_metrics`, `notifications`, `weather_data`  
- **Low Volume**: `sites`, `users`, `cameras`, `zones`, `reports`

### **Critical Indexes for Performance**
- **Time-based queries**: All `timestamp DESC` indexes
- **Site-based filtering**: All `site_id` indexes  
- **Real-time dashboards**: `ai_detections`, `activity_feed` indexes
- **Alert management**: `alerts` status and priority indexes

### **Storage Considerations**
- **JSON fields**: Consider PostgreSQL for better JSON performance
- **POINT/POLYGON fields**: PostGIS extension for spatial queries
- **Large BLOBs**: Store images/videos in object storage, reference URLs only
- **Archive strategy**: Move old records to archive tables after 2+ years

---

## 🔄 **Change History**

### **Version 1.0.0 (2025-01-12)**
- **Created from**: Screen Analysis #01 (My Dashboard)
- **Tables added**: 18 core system tables
- **Focus**: Dashboard functionality requirements
- **Next update**: Screen Analysis #02 (GeoSpatial View)

### **Version 1.1.0 (2025-01-12)**
- **Updated from**: Screen Analysis #02 (GeoSpatial View)
- **Tables added**: 1 new table (`user_site_access`)
- **Tables enhanced**: `sites`, `site_cameras` with geospatial fields
- **New fields added**:
  - `sites`: region, timezone, site_boundary_coordinates
  - `site_cameras`: region, zone_coverage, field_of_view, detection_range
- **New indexes**: Geospatial performance indexes for coordinates and regions
- **Focus**: 3D visualization and user permission requirements
- **Next update**: Screen Analysis #03 (Next screen analysis)

---

**Document Maintained By**: AI Construction Management System Team
**Last Review**: 2025-01-12  
**Next Review**: After each screen analysis completion