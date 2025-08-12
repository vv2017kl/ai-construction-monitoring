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
- **Personnel & Users**: 7 tables  
- **Cameras & Monitoring**: 2 tables
- **AI & Detection**: 7 tables
- **Alerts & Safety**: 6 tables
- **Analytics & Reporting**: 2 tables
- **System & Configuration**: 3 tables
- **Video & Evidence Management**: 4 tables

**Total Tables**: 34 tables

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

### **ai_model_performance_logs**
```sql
CREATE TABLE ai_model_performance_logs (
    id UUID PRIMARY KEY,
    model_id UUID NOT NULL,
    
    -- Performance metrics
    evaluation_date DATE NOT NULL,
    evaluation_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    accuracy_score DECIMAL(5,2) NOT NULL,
    precision_score DECIMAL(5,2) NOT NULL,
    recall_score DECIMAL(5,2) NOT NULL,
    f1_score DECIMAL(5,2) NOT NULL,
    
    -- Processing performance
    avg_processing_time_ms INT NOT NULL,
    median_processing_time_ms INT,
    max_processing_time_ms INT,
    min_processing_time_ms INT,
    
    -- Detection statistics
    total_detections_processed INT DEFAULT 0,
    true_positives INT DEFAULT 0,
    false_positives INT DEFAULT 0,
    false_negatives INT DEFAULT 0,
    confidence_score_avg DECIMAL(5,2),
    confidence_score_std DECIMAL(5,2),
    
    -- Context information
    test_dataset_id UUID,
    site_id UUID,
    camera_subset JSON, -- Array of camera IDs used for evaluation
    
    -- Evaluation metadata
    evaluation_type ENUM('automated', 'manual', 'field_test', 'benchmark') DEFAULT 'automated',
    evaluated_by UUID,
    evaluation_notes TEXT,
    
    -- Comparison data
    compared_to_model_id UUID,
    performance_change_percentage DECIMAL(6,2),
    
    FOREIGN KEY (model_id) REFERENCES ai_models(id),
    FOREIGN KEY (site_id) REFERENCES sites(id),
    FOREIGN KEY (evaluated_by) REFERENCES users(id),
    FOREIGN KEY (compared_to_model_id) REFERENCES ai_models(id),
    
    INDEX idx_model_performance_model_date (model_id, evaluation_date DESC),
    INDEX idx_model_performance_accuracy (accuracy_score DESC),
    INDEX idx_model_performance_processing (avg_processing_time_ms),
    INDEX idx_model_performance_site (site_id, evaluation_date DESC)
);
```

### **ai_detection_analytics**
```sql
CREATE TABLE ai_detection_analytics (
    id UUID PRIMARY KEY,
    
    -- Time and scope
    analysis_date DATE NOT NULL,
    analysis_hour INT, -- 0-23 for hourly granularity
    site_id UUID NOT NULL,
    camera_id UUID,
    zone_id UUID,
    
    -- Detection counts by type
    person_detections INT DEFAULT 0,
    ppe_detections INT DEFAULT 0,
    vehicle_detections INT DEFAULT 0,
    safety_violation_detections INT DEFAULT 0,
    equipment_detections INT DEFAULT 0,
    activity_detections INT DEFAULT 0,
    
    -- Quality metrics
    total_detections INT DEFAULT 0,
    high_confidence_detections INT DEFAULT 0, -- confidence > 0.8
    medium_confidence_detections INT DEFAULT 0, -- confidence 0.6-0.8
    low_confidence_detections INT DEFAULT 0, -- confidence < 0.6
    avg_confidence_score DECIMAL(5,2),
    
    -- Performance metrics
    avg_processing_time_ms INT,
    total_processing_time_ms BIGINT,
    failed_processing_count INT DEFAULT 0,
    
    -- Safety analysis
    safety_violations_detected INT DEFAULT 0,
    ppe_compliance_rate DECIMAL(5,2),
    risk_level_high_count INT DEFAULT 0,
    risk_level_medium_count INT DEFAULT 0,
    risk_level_low_count INT DEFAULT 0,
    
    -- Trend indicators
    detection_trend ENUM('increasing', 'stable', 'decreasing'),
    accuracy_trend ENUM('improving', 'stable', 'declining'),
    
    -- Model information
    primary_model_id UUID,
    model_version VARCHAR(50),
    
    calculated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (site_id) REFERENCES sites(id),
    FOREIGN KEY (camera_id) REFERENCES cameras(id),
    FOREIGN KEY (zone_id) REFERENCES zones(id),
    FOREIGN KEY (primary_model_id) REFERENCES ai_models(id),
    
    UNIQUE KEY unique_analytics_scope (site_id, camera_id, zone_id, analysis_date, analysis_hour),
    INDEX idx_detection_analytics_site_date (site_id, analysis_date DESC),
    INDEX idx_detection_analytics_camera_date (camera_id, analysis_date DESC),
    INDEX idx_detection_analytics_confidence (avg_confidence_score DESC),
    INDEX idx_detection_analytics_performance (avg_processing_time_ms)
);
```

### **camera_ai_performance**
```sql
CREATE TABLE camera_ai_performance (
    id UUID PRIMARY KEY,
    camera_id UUID NOT NULL,
    analysis_date DATE NOT NULL,
    
    -- Detection performance
    total_detections INT DEFAULT 0,
    successful_detections INT DEFAULT 0,
    failed_detections INT DEFAULT 0,
    detection_success_rate DECIMAL(5,2),
    
    -- Accuracy metrics
    validated_detections INT DEFAULT 0,
    confirmed_true_positives INT DEFAULT 0,
    confirmed_false_positives INT DEFAULT 0,
    accuracy_rate DECIMAL(5,2),
    
    -- Processing performance
    avg_processing_time_ms INT,
    max_processing_time_ms INT,
    min_processing_time_ms INT,
    timeout_count INT DEFAULT 0,
    
    -- Quality scores
    image_quality_score DECIMAL(5,2), -- Based on resolution, lighting, etc.
    detection_quality_score DECIMAL(5,2), -- Based on detection success
    overall_performance_score DECIMAL(5,2),
    
    -- Camera health indicators
    uptime_percentage DECIMAL(5,2),
    connection_issues_count INT DEFAULT 0,
    stream_quality_issues_count INT DEFAULT 0,
    
    -- Detection type breakdown
    person_detection_rate DECIMAL(5,2),
    ppe_detection_rate DECIMAL(5,2),
    vehicle_detection_rate DECIMAL(5,2),
    equipment_detection_rate DECIMAL(5,2),
    
    -- Comparative ranking
    site_ranking INT, -- Rank among cameras at the site
    performance_tier ENUM('excellent', 'good', 'average', 'poor', 'critical'),
    
    -- Environment factors
    lighting_conditions_avg DECIMAL(5,2), -- 0-10 scale
    weather_impact_score DECIMAL(5,2), -- Weather effect on performance
    
    calculated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (camera_id) REFERENCES cameras(id),
    
    UNIQUE KEY unique_camera_date (camera_id, analysis_date),
    INDEX idx_camera_performance_date (analysis_date DESC),
    INDEX idx_camera_performance_score (overall_performance_score DESC),
    INDEX idx_camera_performance_accuracy (accuracy_rate DESC),
    INDEX idx_camera_performance_tier (performance_tier, overall_performance_score DESC)
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

### **alert_comments**
```sql
CREATE TABLE alert_comments (
    id UUID PRIMARY KEY,
    alert_id UUID NOT NULL,
    author_id UUID NOT NULL,
    
    -- Comment content
    comment_text TEXT NOT NULL,
    comment_type ENUM('note', 'status_update', 'evidence', 'resolution', 'escalation') DEFAULT 'note',
    
    -- Threading support
    parent_comment_id UUID NULL, -- For reply threading
    thread_level INT DEFAULT 0,
    
    -- Mentions and notifications
    mentioned_users JSON, -- Array of user IDs mentioned
    notifications_sent JSON, -- Notification delivery tracking
    
    -- Attachments
    attachment_urls JSON, -- Array of attachment URLs
    attachment_metadata JSON, -- File names, sizes, types
    
    -- Status and visibility
    is_internal BOOLEAN DEFAULT FALSE, -- Internal vs external comments
    is_edited BOOLEAN DEFAULT FALSE,
    edit_history JSON, -- Edit tracking
    visibility_level ENUM('public', 'team', 'management', 'admin') DEFAULT 'team',
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (alert_id) REFERENCES alerts(id) ON DELETE CASCADE,
    FOREIGN KEY (author_id) REFERENCES users(id),
    FOREIGN KEY (parent_comment_id) REFERENCES alert_comments(id),
    
    INDEX idx_alert_comments_alert (alert_id, created_at DESC),
    INDEX idx_alert_comments_author (author_id),
    INDEX idx_alert_comments_thread (parent_comment_id, thread_level),
    INDEX idx_alert_comments_mentions (mentioned_users),
    FULLTEXT INDEX idx_alert_comments_search (comment_text)
);
```

### **alert_evidence**
```sql
CREATE TABLE alert_evidence (
    id UUID PRIMARY KEY,
    alert_id UUID NOT NULL,
    
    -- Evidence source
    source_type ENUM('ai_detection', 'manual_upload', 'zoneminder_event', 'camera_snapshot', 'document') NOT NULL,
    source_reference_id VARCHAR(255), -- Reference to source (detection_id, event_id, etc.)
    
    -- File information
    evidence_type ENUM('image', 'video', 'document', 'audio', 'data') NOT NULL,
    file_name VARCHAR(255) NOT NULL,
    original_file_name VARCHAR(255),
    file_path VARCHAR(500) NOT NULL,
    file_size_bytes BIGINT,
    file_format VARCHAR(50), -- jpg, mp4, pdf, json, etc.
    
    -- Content metadata
    duration_seconds INT NULL, -- For videos/audio
    image_width INT NULL,
    image_height INT NULL,
    thumbnail_path VARCHAR(500),
    
    -- Evidence details
    title VARCHAR(255),
    description TEXT,
    evidence_timestamp TIMESTAMP, -- When evidence was captured (vs when added)
    location_metadata JSON, -- Camera position, GPS, etc.
    
    -- AI Analysis metadata
    ai_annotations JSON, -- Bounding boxes, detections, etc.
    analysis_metadata JSON, -- Confidence scores, model versions, etc.
    
    -- Access and workflow
    uploaded_by UUID NOT NULL,
    is_primary_evidence BOOLEAN DEFAULT FALSE,
    evidence_chain_verified BOOLEAN DEFAULT FALSE,
    access_permissions JSON, -- Who can view this evidence
    
    -- Status
    status ENUM('processing', 'available', 'archived', 'deleted') DEFAULT 'available',
    retention_date DATE, -- When evidence expires
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (alert_id) REFERENCES alerts(id) ON DELETE CASCADE,
    FOREIGN KEY (uploaded_by) REFERENCES users(id),
    
    INDEX idx_alert_evidence_alert (alert_id, evidence_timestamp DESC),
    INDEX idx_alert_evidence_type (evidence_type, source_type),
    INDEX idx_alert_evidence_uploader (uploaded_by),
    INDEX idx_alert_evidence_primary (is_primary_evidence),
    INDEX idx_alert_evidence_retention (retention_date)
);
```

### **alert_assignments**
```sql
CREATE TABLE alert_assignments (
    id UUID PRIMARY KEY,
    alert_id UUID NOT NULL,
    
    -- Assignment details
    assigned_to UUID NOT NULL,
    assigned_by UUID NOT NULL,
    assignment_type ENUM('manual', 'automatic', 'escalation', 'reassignment') DEFAULT 'manual',
    
    -- Timing
    assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    accepted_at TIMESTAMP NULL,
    started_work_at TIMESTAMP NULL,
    estimated_completion TIMESTAMP NULL,
    actual_completion TIMESTAMP NULL,
    
    -- Assignment metadata
    assignment_reason TEXT,
    priority_override ENUM('critical', 'high', 'medium', 'low') NULL,
    skill_requirements JSON, -- Required skills/certifications
    assignment_notes TEXT,
    
    -- Status tracking
    status ENUM('assigned', 'accepted', 'in_progress', 'completed', 'reassigned', 'declined') DEFAULT 'assigned',
    completion_percentage INT DEFAULT 0,
    
    -- Performance metrics
    response_time_minutes INT, -- Time to start work
    resolution_time_minutes INT, -- Total time to complete
    quality_score DECIMAL(3,1), -- 1-10 quality rating
    
    -- Workload context
    concurrent_assignments INT, -- How many other active assignments at time of assignment
    workload_score DECIMAL(5,2), -- Calculated workload at assignment time
    
    -- Status changes
    status_changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status_changed_by UUID,
    
    FOREIGN KEY (alert_id) REFERENCES alerts(id) ON DELETE CASCADE,
    FOREIGN KEY (assigned_to) REFERENCES users(id),
    FOREIGN KEY (assigned_by) REFERENCES users(id),
    FOREIGN KEY (status_changed_by) REFERENCES users(id),
    
    INDEX idx_alert_assignments_alert (alert_id, assigned_at DESC),
    INDEX idx_alert_assignments_user (assigned_to, status, assigned_at DESC),
    INDEX idx_alert_assignments_performance (resolution_time_minutes, quality_score),
    INDEX idx_alert_assignments_workload (workload_score, concurrent_assignments)
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

### **user_certifications**
```sql
CREATE TABLE user_certifications (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL,
    
    -- Certification details
    certification_name VARCHAR(255) NOT NULL,
    certification_type ENUM('safety', 'technical', 'license', 'training', 'medical') NOT NULL,
    certification_number VARCHAR(100),
    issuing_authority VARCHAR(255),
    
    -- Validity and compliance
    issue_date DATE NOT NULL,
    expiry_date DATE,
    renewal_required BOOLEAN DEFAULT TRUE,
    renewal_period_months INT,
    
    -- Status tracking
    status ENUM('active', 'expired', 'suspended', 'pending_renewal') DEFAULT 'active',
    verification_status ENUM('verified', 'pending', 'rejected') DEFAULT 'pending',
    
    -- Compliance requirements
    required_for_roles JSON, -- Array of roles requiring this certification
    required_for_zones JSON, -- Array of zone IDs requiring this certification
    
    -- Files and documentation
    certificate_file_path VARCHAR(500),
    verification_documents JSON, -- Array of document paths
    
    -- Audit trail
    created_by UUID,
    verified_by UUID,
    last_verification_check DATE,
    
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (created_by) REFERENCES users(id),
    FOREIGN KEY (verified_by) REFERENCES users(id),
    
    INDEX idx_user_certifications_user (user_id),
    INDEX idx_user_certifications_type (certification_type),
    INDEX idx_user_certifications_status (status),
    INDEX idx_user_certifications_expiry (expiry_date),
    INDEX idx_user_certifications_required_roles (required_for_roles),
    UNIQUE KEY unique_user_certification (user_id, certification_name, certification_number)
);
```

### **personnel_attendance**
```sql
CREATE TABLE personnel_attendance (
    id UUID PRIMARY KEY,
    personnel_id UUID NOT NULL,
    attendance_date DATE NOT NULL,
    
    -- Check-in/Check-out
    check_in_time TIMESTAMP,
    check_out_time TIMESTAMP,
    scheduled_start_time TIME,
    scheduled_end_time TIME,
    
    -- Break management
    break_start_time TIMESTAMP,
    break_end_time TIMESTAMP,
    total_break_minutes INT DEFAULT 0,
    authorized_break_minutes INT DEFAULT 30,
    
    -- Time calculations
    total_work_minutes INT DEFAULT 0,
    overtime_hours DECIMAL(4,2) DEFAULT 0.00,
    overtime_approved BOOLEAN DEFAULT FALSE,
    
    -- Location verification
    location_check_in POINT,
    location_check_out POINT,
    gps_accuracy_check_in DECIMAL(8,2), -- meters
    gps_accuracy_check_out DECIMAL(8,2),
    
    -- Device and method tracking
    device_used_check_in VARCHAR(255), -- mobile, tablet, terminal, etc.
    device_used_check_out VARCHAR(255),
    check_in_method ENUM('gps', 'qr_code', 'nfc', 'manual', 'facial_recognition') DEFAULT 'gps',
    check_out_method ENUM('gps', 'qr_code', 'nfc', 'manual', 'facial_recognition') DEFAULT 'gps',
    
    -- Status and compliance
    attendance_status ENUM('present', 'late', 'absent', 'partial', 'overtime') DEFAULT 'present',
    tardiness_minutes INT DEFAULT 0,
    early_departure_minutes INT DEFAULT 0,
    
    -- Approval and notes
    approved_by UUID,
    supervisor_notes TEXT,
    employee_notes TEXT,
    
    FOREIGN KEY (personnel_id) REFERENCES site_personnel(id),
    FOREIGN KEY (approved_by) REFERENCES users(id),
    
    UNIQUE KEY unique_personnel_date (personnel_id, attendance_date),
    INDEX idx_attendance_personnel_date (personnel_id, attendance_date DESC),
    INDEX idx_attendance_status (attendance_status),
    INDEX idx_attendance_overtime (overtime_hours DESC),
    SPATIAL INDEX idx_attendance_checkin_location (location_check_in),
    SPATIAL INDEX idx_attendance_checkout_location (location_check_out)
);
```

### **personnel_safety_scores**
```sql
CREATE TABLE personnel_safety_scores (
    id UUID PRIMARY KEY,
    personnel_id UUID NOT NULL,
    recorded_date DATE NOT NULL,
    recorded_time TIME DEFAULT CURRENT_TIME,
    
    -- Safety metrics
    safety_score DECIMAL(5,2) NOT NULL, -- 0.00 to 100.00
    ppe_compliance_score DECIMAL(5,2) NOT NULL,
    behavior_score DECIMAL(5,2) DEFAULT 100.00,
    zone_compliance_score DECIMAL(5,2) DEFAULT 100.00,
    
    -- Assessment details
    assessment_type ENUM('ai_automated', 'supervisor_review', 'incident_based', 'periodic_review') NOT NULL,
    assessed_by UUID,
    assessment_camera_id UUID,
    assessment_zone_id UUID,
    
    -- Detailed breakdown
    ppe_items_status JSON, -- Detailed PPE compliance by item
    safety_violations JSON, -- Array of violations detected
    positive_behaviors JSON, -- Array of positive safety behaviors
    
    -- Context and evidence
    assessment_context TEXT,
    evidence_files JSON, -- Array of evidence file paths
    ai_confidence_score DECIMAL(5,2),
    
    -- Improvement tracking
    previous_score DECIMAL(5,2),
    score_change DECIMAL(6,2), -- Can be negative
    improvement_notes TEXT,
    corrective_actions JSON,
    
    FOREIGN KEY (personnel_id) REFERENCES site_personnel(id),
    FOREIGN KEY (assessed_by) REFERENCES users(id),
    FOREIGN KEY (assessment_camera_id) REFERENCES cameras(id),
    FOREIGN KEY (assessment_zone_id) REFERENCES zones(id),
    
    INDEX idx_safety_scores_personnel_date (personnel_id, recorded_date DESC),
    INDEX idx_safety_scores_type (assessment_type),
    INDEX idx_safety_scores_score (safety_score DESC),
    INDEX idx_safety_scores_assessor (assessed_by),
    INDEX idx_safety_scores_zone (assessment_zone_id)
);
```

### **department_assignments**
```sql
CREATE TABLE department_assignments (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL,
    site_id UUID NOT NULL,
    
    -- Department and position
    department_name VARCHAR(255) NOT NULL,
    position_title VARCHAR(255) NOT NULL,
    position_level ENUM('entry', 'junior', 'mid', 'senior', 'lead', 'supervisor', 'manager') DEFAULT 'entry',
    
    -- Reporting structure
    reporting_manager_id UUID,
    department_head_id UUID,
    
    -- Assignment details
    start_date DATE NOT NULL,
    end_date DATE,
    is_active BOOLEAN DEFAULT TRUE,
    assignment_type ENUM('permanent', 'temporary', 'contract', 'intern') DEFAULT 'permanent',
    
    -- Responsibilities and permissions
    job_responsibilities JSON, -- Array of responsibility descriptions
    zone_access_permissions JSON, -- Array of zone IDs user can access
    equipment_permissions JSON, -- Array of equipment IDs user can operate
    
    -- Work schedule
    default_shift_start TIME,
    default_shift_end TIME,
    work_days JSON, -- Array of weekdays (0=Sunday, 1=Monday, etc.)
    
    -- Compensation (optional)
    hourly_rate DECIMAL(8,2),
    overtime_rate DECIMAL(8,2),
    
    -- Assignment history
    assigned_by UUID,
    assignment_reason TEXT,
    previous_assignment_id UUID, -- Reference to previous assignment
    
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (site_id) REFERENCES sites(id),
    FOREIGN KEY (reporting_manager_id) REFERENCES users(id),
    FOREIGN KEY (department_head_id) REFERENCES users(id),
    FOREIGN KEY (assigned_by) REFERENCES users(id),
    FOREIGN KEY (previous_assignment_id) REFERENCES department_assignments(id),
    
    INDEX idx_department_assignments_user (user_id),
    INDEX idx_department_assignments_site (site_id),
    INDEX idx_department_assignments_department (department_name),
    INDEX idx_department_assignments_manager (reporting_manager_id),
    INDEX idx_department_assignments_active (is_active, start_date DESC)
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
- **Next update**: Screen Analysis #03 (Live View)

### **Version 1.2.0 (2025-01-12)**
- **Updated from**: Screen Analysis #03 (Live View)
- **Tables added**: 1 new table (`recording_sessions`)
- **Tables enhanced**: `cameras`, `site_cameras` with live view capabilities
- **New fields added**:
  - `cameras`: audio_enabled, ptz_capabilities, recording_capabilities
  - `site_cameras`: current_zoom_level, recording_active, stream_quality
- **New indexes**: Live view performance indexes for recording and PTZ state
- **Focus**: Real-time video streaming, recording management, PTZ control
- **Next update**: Screen Analysis #04 (Alert Center)

### **Version 1.3.0 (2025-01-12)**
- **Updated from**: Screen Analysis #04 (Alert Center)
- **Tables added**: 3 new tables (`alert_comments`, `alert_evidence`, `alert_assignments`)
- **Tables enhanced**: None (alert workflow extended through new tables)
- **New features added**:
  - Complete commenting system with threading and mentions
  - Evidence management with AI analysis metadata and retention
  - Assignment workflow tracking with performance metrics
- **New indexes**: Alert management performance indexes for real-time operations
- **Focus**: Alert workflow management, evidence tracking, collaboration systems
- **Next update**: Screen Analysis #05 (Next screen analysis)

### **Version 1.4.0 (2025-01-12)**
- **Updated from**: Screen Analysis #07 (AI Analytics)
- **Tables added**: 3 new tables (`ai_model_performance_logs`, `ai_detection_analytics`, `camera_ai_performance`)
- **Tables enhanced**: None (new AI analytics capabilities through dedicated tables)
- **New features added**:
  - Comprehensive AI model performance tracking with evaluation metrics
  - Detection analytics with time-based granularity and quality metrics
  - Individual camera AI performance monitoring and ranking
  - AI performance trend analysis and comparative metrics
- **New indexes**: AI performance optimization indexes for analytics queries
- **Focus**: AI model performance monitoring, detection analytics, camera-level AI tracking
- **Next update**: Screen Analysis #08 (Next screen analysis)

---

## 🎥 **VIDEO & EVIDENCE MANAGEMENT**

### **video_bookmarks**
```sql
CREATE TABLE video_bookmarks (
    id UUID PRIMARY KEY,
    camera_id UUID NOT NULL,
    user_id UUID NOT NULL,
    
    -- Temporal information
    bookmark_date DATE NOT NULL,
    timestamp_seconds INT NOT NULL, -- Seconds from start of day
    duration_seconds INT DEFAULT 10, -- Bookmark duration for clips
    
    -- Bookmark details
    title VARCHAR(255) NOT NULL,
    description TEXT,
    bookmark_type ENUM('safety_incident', 'ppe_violation', 'equipment_issue', 'person_activity', 'vehicle_activity', 'custom', 'alert_related', 'compliance_check') NOT NULL,
    
    -- Classification and priority
    priority_level ENUM('low', 'medium', 'high', 'critical') DEFAULT 'medium',
    severity ENUM('info', 'warning', 'error', 'critical') DEFAULT 'info',
    
    -- Evidence and correlation
    related_alert_id UUID,
    related_detection_id UUID,
    evidence_quality ENUM('poor', 'fair', 'good', 'excellent') DEFAULT 'good',
    
    -- User interaction
    is_shared BOOLEAN DEFAULT FALSE,
    share_permissions JSON, -- Array of user IDs or roles with access
    
    -- Visual markers
    thumbnail_timestamp INT, -- Best representative frame
    color_code VARCHAR(7) DEFAULT '#FFA500', -- Hex color for timeline display
    
    -- Metadata
    video_quality_at_time VARCHAR(50), -- Resolution/quality at bookmark time
    weather_conditions VARCHAR(100),
    lighting_conditions ENUM('excellent', 'good', 'fair', 'poor', 'very_poor'),
    
    -- Workflow status
    status ENUM('active', 'reviewed', 'resolved', 'archived') DEFAULT 'active',
    reviewed_by UUID,
    reviewed_at TIMESTAMP,
    review_notes TEXT,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (camera_id) REFERENCES cameras(id),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (related_alert_id) REFERENCES alerts(id),
    FOREIGN KEY (related_detection_id) REFERENCES ai_detections(id),
    FOREIGN KEY (reviewed_by) REFERENCES users(id),
    
    INDEX idx_video_bookmarks_camera_date (camera_id, bookmark_date DESC),
    INDEX idx_video_bookmarks_user (user_id, created_at DESC),
    INDEX idx_video_bookmarks_type (bookmark_type, priority_level),
    INDEX idx_video_bookmarks_timestamp (bookmark_date, timestamp_seconds),
    INDEX idx_video_bookmarks_status (status, created_at DESC),
    INDEX idx_video_bookmarks_shared (is_shared),
    UNIQUE KEY unique_user_camera_timestamp (user_id, camera_id, bookmark_date, timestamp_seconds)
);
```

### **video_access_logs**
```sql
CREATE TABLE video_access_logs (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL,
    camera_id UUID NOT NULL,
    
    -- Access session details
    session_id UUID NOT NULL,
    access_start TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    access_end TIMESTAMP,
    session_duration_minutes INT,
    
    -- Video details accessed
    video_date DATE NOT NULL,
    start_timestamp_seconds INT NOT NULL, -- Start time in video
    end_timestamp_seconds INT, -- End time (if session completed)
    total_video_watched_seconds INT DEFAULT 0,
    
    -- Access method and context
    access_method ENUM('web_browser', 'mobile_app', 'api', 'export') DEFAULT 'web_browser',
    access_reason ENUM('routine_review', 'incident_investigation', 'compliance_audit', 'training', 'maintenance', 'legal_request') NOT NULL,
    
    -- User activity during session
    bookmarks_created INT DEFAULT 0,
    screenshots_taken INT DEFAULT 0,
    clips_exported INT DEFAULT 0,
    playback_speed_changes INT DEFAULT 0,
    
    -- Technical details
    ip_address INET,
    user_agent TEXT,
    browser_info JSON,
    
    -- Legal and compliance
    legal_hold_flag BOOLEAN DEFAULT FALSE,
    audit_flag BOOLEAN DEFAULT FALSE,
    retention_period_override INT, -- Days to retain this access record
    
    -- Performance metrics
    initial_load_time_ms INT,
    average_seek_time_ms INT,
    total_pause_time_seconds INT DEFAULT 0,
    
    -- Access outcome
    session_complete BOOLEAN DEFAULT FALSE,
    premature_termination_reason ENUM('user_logout', 'session_timeout', 'technical_error', 'policy_violation', 'system_maintenance'),
    
    -- Data export tracking
    export_count INT DEFAULT 0,
    export_details JSON, -- Details of any exports performed
    
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (camera_id) REFERENCES cameras(id),
    
    INDEX idx_video_access_user_time (user_id, access_start DESC),
    INDEX idx_video_access_camera_date (camera_id, video_date DESC),
    INDEX idx_video_access_session (session_id),
    INDEX idx_video_access_legal (legal_hold_flag, audit_flag),
    INDEX idx_video_access_reason (access_reason, access_start DESC)
);
```

### **video_exports**
```sql
CREATE TABLE video_exports (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL,
    camera_id UUID NOT NULL,
    
    -- Export source details
    source_video_date DATE NOT NULL,
    start_timestamp_seconds INT NOT NULL,
    end_timestamp_seconds INT NOT NULL,
    export_duration_seconds INT NOT NULL,
    
    -- Export configuration
    export_type ENUM('video_clip', 'screenshot', 'evidence_package', 'compliance_report', 'share_link') NOT NULL,
    export_format VARCHAR(20) NOT NULL, -- mp4, jpg, png, pdf, zip
    resolution VARCHAR(20), -- Original, 1080p, 720p, 480p
    quality_setting ENUM('high', 'medium', 'low') DEFAULT 'high',
    include_audio BOOLEAN DEFAULT TRUE,
    
    -- Evidence and legal
    export_purpose ENUM('evidence', 'training', 'analysis', 'compliance', 'documentation', 'legal_proceeding') NOT NULL,
    chain_of_custody JSON, -- Evidence handling chain
    hash_verification VARCHAR(128), -- File integrity hash
    digital_signature VARCHAR(512), -- Legal authentication
    
    -- File information
    original_filename VARCHAR(255),
    stored_filename VARCHAR(255),
    file_path VARCHAR(500),
    file_size_bytes BIGINT,
    
    -- Processing status
    export_status ENUM('requested', 'processing', 'completed', 'failed', 'expired') DEFAULT 'requested',
    processing_started_at TIMESTAMP,
    processing_completed_at TIMESTAMP,
    processing_time_seconds INT,
    error_message TEXT,
    
    -- Access and sharing
    download_url VARCHAR(500),
    share_token VARCHAR(255) UNIQUE,
    download_expires_at TIMESTAMP,
    download_count INT DEFAULT 0,
    max_download_count INT DEFAULT 5,
    
    -- Metadata preservation
    original_metadata JSON, -- Camera settings, weather, etc.
    bookmark_data JSON, -- Any bookmarks within the export timeframe
    incident_data JSON, -- Related alerts and detections
    
    -- Audit and compliance
    export_justification TEXT NOT NULL,
    approval_required BOOLEAN DEFAULT FALSE,
    approved_by UUID,
    approved_at TIMESTAMP,
    legal_hold_applied BOOLEAN DEFAULT FALSE,
    retention_period_days INT DEFAULT 90,
    
    -- Performance tracking
    compression_ratio DECIMAL(5,2), -- Original size vs final size
    processing_efficiency_score DECIMAL(3,1), -- 1-10 efficiency rating
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (camera_id) REFERENCES cameras(id),
    FOREIGN KEY (approved_by) REFERENCES users(id),
    
    INDEX idx_video_exports_user_date (user_id, created_at DESC),
    INDEX idx_video_exports_camera (camera_id, source_video_date DESC),
    INDEX idx_video_exports_status (export_status, created_at DESC),
    INDEX idx_video_exports_purpose (export_purpose, created_at DESC),
    INDEX idx_video_exports_legal (legal_hold_applied, retention_period_days),
    INDEX idx_video_exports_share (share_token, download_expires_at)
);
```

### **video_quality_metrics**
```sql
CREATE TABLE video_quality_metrics (
    id UUID PRIMARY KEY,
    camera_id UUID NOT NULL,
    analysis_date DATE NOT NULL,
    analysis_hour INT DEFAULT 0, -- 0-23 for hourly analysis
    
    -- Technical quality metrics
    average_bitrate_kbps INT,
    average_fps DECIMAL(5,2),
    resolution_width INT,
    resolution_height INT,
    
    -- Visual quality assessment
    sharpness_score DECIMAL(5,2), -- 0-10 scale
    brightness_score DECIMAL(5,2), -- 0-10 scale
    contrast_score DECIMAL(5,2), -- 0-10 scale
    color_accuracy_score DECIMAL(5,2), -- 0-10 scale
    noise_level_score DECIMAL(5,2), -- 0-10 scale (lower is better)
    
    -- Environmental factors
    lighting_condition ENUM('excellent', 'good', 'fair', 'poor', 'very_poor'),
    weather_impact ENUM('none', 'minimal', 'moderate', 'significant', 'severe'),
    obstruction_detected BOOLEAN DEFAULT FALSE,
    camera_shake_detected BOOLEAN DEFAULT FALSE,
    
    -- Usability for analysis
    forensic_quality_rating ENUM('excellent', 'good', 'acceptable', 'poor', 'unusable'),
    person_identification_viability ENUM('clear', 'good', 'limited', 'poor', 'impossible'),
    activity_recognition_viability ENUM('clear', 'good', 'limited', 'poor', 'impossible'),
    
    -- Storage and compression
    compression_efficiency DECIMAL(5,2),
    storage_size_mb DECIMAL(10,2),
    file_corruption_detected BOOLEAN DEFAULT FALSE,
    
    -- Recording continuity
    recording_gaps_detected BOOLEAN DEFAULT FALSE,
    total_gap_duration_seconds INT DEFAULT 0,
    frame_drops_count INT DEFAULT 0,
    sync_issues_detected BOOLEAN DEFAULT FALSE,
    
    -- Analysis metadata
    analysis_method ENUM('automated', 'manual', 'hybrid') DEFAULT 'automated',
    analysis_tool VARCHAR(100),
    analysis_confidence DECIMAL(5,2), -- Confidence in the quality assessment
    
    -- Improvement recommendations
    recommended_adjustments JSON, -- Settings adjustments to improve quality
    maintenance_flags JSON, -- Issues requiring camera maintenance
    
    calculated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (camera_id) REFERENCES cameras(id),
    
    UNIQUE KEY unique_camera_datetime (camera_id, analysis_date, analysis_hour),
    INDEX idx_video_quality_camera_date (camera_id, analysis_date DESC),
    INDEX idx_video_quality_forensic (forensic_quality_rating, camera_id),
    INDEX idx_video_quality_overall (sharpness_score, brightness_score, contrast_score),
    INDEX idx_video_quality_issues (file_corruption_detected, recording_gaps_detected),
    INDEX idx_video_quality_lighting (lighting_condition, analysis_date DESC)
);
```

---

**Document Maintained By**: AI Construction Management System Team
**Last Review**: 2025-01-12  
**Next Review**: After each screen analysis completion