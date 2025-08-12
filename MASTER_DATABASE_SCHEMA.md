# 🗃️ MASTER DATABASE SCHEMA - AI Construction Management System

## 📋 **Document Information**
- **Document Type**: Master Database Schema Reference
- **Version**: 1.0.0
- **Last Updated**: 2025-01-12
- **Created From**: Screen Analysis #01 (My Dashboard)
- **Status**: ✅ Active - Referenced by all screen analyses

### **Version 1.7.0 (2025-01-12) - PHASE 1 COMPLETION**
- **Updated from**: Screen Analysis #10 (Time Lapse) - **FINAL PHASE 1 SCREEN**
- **Tables added**: 5 new tables (`timelapse_sequences`, `timelapse_bookmarks`, `timelapse_events`, `timelapse_shares`, `construction_milestones`)
- **New section added**: Time-Lapse & Progress Tracking (5 tables)
- **Milestone achieved**: **PHASE 1 COMPLETE - All 10 core operational screens analyzed**
- **New features added**:
  - Comprehensive time-lapse sequence management with multi-camera support
  - Advanced bookmarking system with precise timing and collaboration features
  - Automated event detection within time-lapse sequences with AI analysis
  - Secure sharing system with access controls and usage analytics
  - Construction milestone tracking with dependency management and automated detection
- **New indexes**: Time-lapse performance optimization indexes for sequence processing and timeline navigation
- **Focus**: Progress documentation, time-series analysis, construction milestone tracking, collaborative project review
- **Next update**: Screen Analysis #11 (Phase 2 begins - Enhanced Functionality screens)

### **Version 1.8.0 (2025-01-12) - PHASE 2 START**
- **Updated from**: Screen Analysis #11 (Live Street View) - **FIRST PHASE 2 SCREEN**
- **Tables added**: 4 new tables (`navigation_routes`, `route_waypoints`, `navigation_sessions`, `street_view_cameras`)
- **New section added**: Navigation & Street View (4 tables)
- **Milestone achieved**: **PHASE 2 BEGINS - Enhanced Functionality screens**
- **New features added**:
  - Comprehensive navigation route management with GPS-guided routing
  - Detailed waypoint system with interactive features and safety protocols
  - Navigation session tracking with performance metrics and safety compliance
  - Street view camera management with PTZ controls and AI integration
- **New indexes**: Navigation and street view performance optimization indexes for GPS tracking and route management
- **Focus**: GPS navigation, street-level monitoring, enhanced live surveillance, route optimization
- **Next update**: Screen Analysis #12 (Phase 2 continues)

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
- **Sites & Locations**: 4 tables
- **Personnel & Users**: 7 tables  
- **Cameras & Monitoring**: 3 tables
- **AI & Detection**: 7 tables
- **Alerts & Safety**: 6 tables
- **Analytics & Reporting**: 7 tables
- **System & Configuration**: 3 tables
- **Video & Evidence Management**: 4 tables
- **Time-Lapse & Progress Tracking**: 5 tables
- **Navigation & Street View**: 4 tables
- **Historical Navigation & Analysis**: 4 tables
- **Field Operations & Assessment**: 5 tables
- **Temporal Analysis & Comparison**: 4 tables
- **Street View Comparison & Analysis**: 5 tables
- **Path Administration & Routing**: 5 tables
- **Admin Dashboard & System Management**: 5 tables
- **User Management & Administration**: 5 tables
- **Site Configuration & Infrastructure**: 5 tables
- **AI Model Management & Deployment**: 5 tables
- **System Monitoring & Infrastructure Health**: 5 tables
- **Access Control & Security Management**: 5 tables
- **Integration & User Experience**: 7 tables

**Total Tables**: 110 tables

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

### **Version 1.5.0 (2025-01-12)**
- **Updated from**: Screen Analysis #08 (Video Review)
- **Tables added**: 4 new tables (`video_bookmarks`, `video_access_logs`, `video_exports`, `video_quality_metrics`)
- **New section added**: Video & Evidence Management (4 tables)
- **New features added**:
  - Comprehensive video bookmarking system with evidence correlation
  - Video access logging and audit trail capabilities
  - Video export management with legal compliance support
  - Video quality assessment and forensic analysis tracking
- **New indexes**: Video management performance indexes for timeline and search operations
- **Focus**: Historical video review, forensic analysis, evidence management, compliance auditing
- **Next update**: Screen Analysis #09 (Next screen analysis)

### **Version 1.6.0 (2025-01-12)**
- **Updated from**: Screen Analysis #09 (Reports Center)
- **Tables added**: 5 new tables (`report_templates`, `report_schedules`, `report_generation_logs`, `report_shares`, `report_data_sources`)
- **Tables enhanced**: None (comprehensive reporting infrastructure through new dedicated tables)
- **New features added**:
  - Advanced report template management with usage tracking and popularity metrics
  - Automated report scheduling with frequency, timing, and recipient configuration
  - Comprehensive report generation logging with performance and quality metrics
  - Report sharing system with access control, expiration, and usage tracking
  - Data source management with connection configuration and performance monitoring
- **New indexes**: Comprehensive reporting performance indexes for template, schedule, and generation operations
- **Focus**: Business intelligence, compliance reporting, automated report generation, data analytics
- **Next update**: Screen Analysis #10 (Next screen analysis)

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

### **report_templates**
```sql
CREATE TABLE report_templates (
    id UUID PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    
    -- Template configuration
    template_type ENUM('safety', 'personnel', 'ai_analytics', 'equipment', 'progress', 'compliance', 'custom') NOT NULL,
    category VARCHAR(100), -- Grouping for organization
    subcategory VARCHAR(100),
    
    -- Template structure
    sections JSON NOT NULL, -- Array of report sections and their configurations
    data_sources JSON NOT NULL, -- Required data sources and queries
    chart_configurations JSON, -- Chart and visualization settings
    formatting_rules JSON, -- Layout and styling rules
    
    -- Generation settings
    estimated_generation_time_minutes INT DEFAULT 5,
    complexity_level ENUM('simple', 'moderate', 'complex', 'advanced') DEFAULT 'simple',
    data_requirements JSON, -- Required data availability for generation
    
    -- Usage and popularity
    usage_count INT DEFAULT 0,
    success_rate DECIMAL(5,2) DEFAULT 100.00,
    average_generation_time_minutes DECIMAL(5,2),
    popularity_score DECIMAL(5,2) DEFAULT 0.00, -- Calculated popularity
    
    -- Template metadata
    created_by UUID NOT NULL,
    last_updated_by UUID,
    version VARCHAR(20) DEFAULT '1.0',
    changelog JSON, -- Version history and changes
    
    -- Status and availability
    status ENUM('active', 'deprecated', 'draft', 'archived') DEFAULT 'active',
    availability ENUM('public', 'private', 'team', 'site_specific') DEFAULT 'public',
    
    -- Customization options
    customizable_fields JSON, -- Fields that can be modified by users
    required_permissions JSON, -- Permissions required to use this template
    
    -- Preview and documentation
    preview_image_url VARCHAR(500),
    documentation_url VARCHAR(500),
    sample_output_url VARCHAR(500),
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (created_by) REFERENCES users(id),
    FOREIGN KEY (last_updated_by) REFERENCES users(id),
    
    INDEX idx_report_templates_type (template_type, status),
    INDEX idx_report_templates_popularity (popularity_score DESC, usage_count DESC),
    INDEX idx_report_templates_category (category, subcategory),
    INDEX idx_report_templates_creator (created_by, created_at DESC),
    INDEX idx_report_templates_status (status, availability),
    FULLTEXT INDEX idx_report_templates_search (name, description)
);
```

### **report_schedules**
```sql
CREATE TABLE report_schedules (
    id UUID PRIMARY KEY,
    
    -- Schedule identification
    schedule_name VARCHAR(255) NOT NULL,
    description TEXT,
    report_template_id UUID,
    
    -- Generation configuration
    report_type ENUM('safety', 'personnel', 'ai_analytics', 'equipment', 'progress', 'compliance', 'custom') NOT NULL,
    report_title VARCHAR(255), -- Title pattern for generated reports
    output_format ENUM('pdf', 'excel', 'csv', 'json', 'html') DEFAULT 'pdf',
    
    -- Scheduling configuration
    frequency ENUM('hourly', 'daily', 'weekly', 'bi_weekly', 'monthly', 'quarterly', 'yearly', 'custom') NOT NULL,
    custom_cron_expression VARCHAR(100), -- For custom frequencies
    
    -- Timing configuration
    scheduled_time TIME DEFAULT '09:00:00',
    timezone VARCHAR(50) DEFAULT 'UTC',
    
    -- Date constraints
    start_date DATE,
    end_date DATE,
    next_execution TIMESTAMP,
    last_execution TIMESTAMP,
    
    -- Recipients and distribution
    email_recipients JSON, -- Array of email addresses
    user_recipients JSON, -- Array of user IDs
    team_recipients JSON, -- Array of team/role IDs
    
    -- Content configuration
    data_filters JSON, -- Filters applied to report data
    date_range_type ENUM('fixed', 'relative', 'custom') DEFAULT 'relative',
    relative_date_range VARCHAR(50), -- 'last_7_days', 'last_month', etc.
    
    -- Output and delivery
    delivery_method ENUM('email', 'file_storage', 'both') DEFAULT 'email',
    storage_location VARCHAR(500),
    email_subject_pattern VARCHAR(255),
    email_body_template TEXT,
    
    -- Status and monitoring
    status ENUM('active', 'paused', 'disabled', 'error') DEFAULT 'active',
    execution_count INT DEFAULT 0,
    success_count INT DEFAULT 0,
    failure_count INT DEFAULT 0,
    last_error_message TEXT,
    
    -- Performance tracking
    average_generation_time_seconds INT,
    average_file_size_mb DECIMAL(10,2),
    
    -- Approval workflow
    requires_approval BOOLEAN DEFAULT FALSE,
    approval_required_by JSON, -- Array of user IDs who can approve
    auto_approve BOOLEAN DEFAULT TRUE,
    
    -- Ownership and permissions
    created_by UUID NOT NULL,
    owned_by UUID NOT NULL,
    shared_with JSON, -- Array of user/team IDs with access
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (report_template_id) REFERENCES report_templates(id),
    FOREIGN KEY (created_by) REFERENCES users(id),
    FOREIGN KEY (owned_by) REFERENCES users(id),
    
    INDEX idx_report_schedules_next_execution (next_execution, status),
    INDEX idx_report_schedules_frequency (frequency, status),
    INDEX idx_report_schedules_owner (owned_by, created_at DESC),
    INDEX idx_report_schedules_type (report_type, status),
    INDEX idx_report_schedules_status (status, next_execution)
);
```

### **report_generation_logs**
```sql
CREATE TABLE report_generation_logs (
    id UUID PRIMARY KEY,
    
    -- Generation context
    report_id UUID, -- Links to reports table if applicable
    schedule_id UUID, -- Links to report_schedules if scheduled
    template_id UUID, -- Template used for generation
    
    -- Generation details
    generation_type ENUM('manual', 'scheduled', 'api', 'bulk') NOT NULL,
    initiated_by UUID, -- User who initiated the generation
    generation_method ENUM('template', 'custom', 'quick', 'clone') NOT NULL,
    
    -- Timing information
    generation_started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    generation_completed_at TIMESTAMP,
    generation_duration_seconds INT,
    
    -- Content configuration
    report_title VARCHAR(255),
    report_type VARCHAR(100),
    output_format VARCHAR(20),
    data_range_start DATE,
    data_range_end DATE,
    
    -- Data processing
    data_sources_queried JSON, -- List of tables/sources accessed
    total_records_processed INT DEFAULT 0,
    data_processing_time_seconds INT,
    
    -- Generation status
    status ENUM('started', 'processing_data', 'generating', 'formatting', 'completed', 'failed', 'cancelled') NOT NULL,
    progress_percentage INT DEFAULT 0,
    current_step VARCHAR(255),
    
    -- Output information
    output_file_path VARCHAR(500),
    output_file_size_bytes BIGINT,
    output_page_count INT,
    file_hash VARCHAR(128), -- For integrity verification
    
    -- Error handling
    error_code VARCHAR(50),
    error_message TEXT,
    error_stack_trace TEXT,
    retry_count INT DEFAULT 0,
    max_retries INT DEFAULT 3,
    
    -- Performance metrics
    cpu_usage_avg DECIMAL(5,2),
    memory_usage_mb INT,
    database_query_count INT,
    database_query_time_seconds INT,
    
    -- Quality metrics
    data_quality_score DECIMAL(5,2), -- 0-10 data quality rating
    report_completeness DECIMAL(5,2), -- Percentage of expected data included
    validation_errors_count INT DEFAULT 0,
    
    -- Notification and delivery
    email_sent BOOLEAN DEFAULT FALSE,
    email_sent_at TIMESTAMP,
    notification_recipients JSON,
    delivery_status ENUM('pending', 'delivered', 'failed', 'not_required') DEFAULT 'pending',
    
    FOREIGN KEY (report_id) REFERENCES reports(id),
    FOREIGN KEY (schedule_id) REFERENCES report_schedules(id),
    FOREIGN KEY (template_id) REFERENCES report_templates(id),
    FOREIGN KEY (initiated_by) REFERENCES users(id),
    
    INDEX idx_generation_logs_status_time (status, generation_started_at DESC),
    INDEX idx_generation_logs_report (report_id, generation_started_at DESC),
    INDEX idx_generation_logs_schedule (schedule_id, generation_started_at DESC),
    INDEX idx_generation_logs_user (initiated_by, generation_started_at DESC),
    INDEX idx_generation_logs_performance (generation_duration_seconds, output_file_size_bytes)
);
```

### **report_shares**
```sql
CREATE TABLE report_shares (
    id UUID PRIMARY KEY,
    report_id UUID NOT NULL,
    
    -- Sharing details
    shared_by UUID NOT NULL,
    share_type ENUM('link', 'email', 'team', 'public', 'download') NOT NULL,
    
    -- Recipients (depending on share_type)
    shared_with_users JSON, -- Array of user IDs
    shared_with_teams JSON, -- Array of team/role IDs
    shared_with_emails JSON, -- Array of email addresses for external sharing
    
    -- Share configuration
    share_token VARCHAR(255) UNIQUE, -- Unique token for link sharing
    access_level ENUM('view', 'download', 'comment', 'edit') DEFAULT 'view',
    password_protected BOOLEAN DEFAULT FALSE,
    password_hash VARCHAR(255),
    
    -- Permissions and restrictions
    allow_download BOOLEAN DEFAULT TRUE,
    allow_sharing BOOLEAN DEFAULT FALSE, -- Allow recipients to share further
    restrict_ip_addresses JSON, -- Array of allowed IP addresses/ranges
    
    -- Expiration and limits
    expires_at TIMESTAMP,
    max_views INT, -- Maximum number of views allowed
    max_downloads INT, -- Maximum number of downloads allowed
    
    -- Usage tracking
    view_count INT DEFAULT 0,
    download_count INT DEFAULT 0,
    last_accessed_at TIMESTAMP,
    last_accessed_by VARCHAR(255), -- Email or user identifier
    
    -- Access logs summary
    unique_viewers INT DEFAULT 0,
    total_view_time_minutes INT DEFAULT 0,
    
    -- Notification settings
    notify_on_access BOOLEAN DEFAULT FALSE,
    access_notification_emails JSON, -- Who gets notified on access
    
    -- Status
    status ENUM('active', 'expired', 'revoked', 'disabled') DEFAULT 'active',
    revoked_at TIMESTAMP,
    revoked_by UUID,
    revoke_reason TEXT,
    
    -- Metadata
    share_title VARCHAR(255), -- Custom title for the shared report
    share_message TEXT, -- Message included with share
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (report_id) REFERENCES reports(id),
    FOREIGN KEY (shared_by) REFERENCES users(id),
    FOREIGN KEY (revoked_by) REFERENCES users(id),
    
    INDEX idx_report_shares_report (report_id, created_at DESC),
    INDEX idx_report_shares_token (share_token, status),
    INDEX idx_report_shares_sharer (shared_by, created_at DESC),
    INDEX idx_report_shares_expires (expires_at, status),
    INDEX idx_report_shares_status (status, created_at DESC)
);
```

### **report_data_sources**
```sql
CREATE TABLE report_data_sources (
    id UUID PRIMARY KEY,
    
    -- Data source identification
    source_name VARCHAR(255) NOT NULL UNIQUE,
    source_type ENUM('database_table', 'api_endpoint', 'file_import', 'external_service', 'calculated_metric') NOT NULL,
    description TEXT,
    
    -- Connection configuration
    connection_string VARCHAR(500), -- Database connection or API URL
    authentication_method ENUM('none', 'api_key', 'oauth', 'database_credentials', 'token') DEFAULT 'none',
    credentials_encrypted JSON, -- Encrypted authentication data
    
    -- Data structure
    schema_definition JSON, -- Expected data structure and field types
    primary_key_fields JSON, -- Array of primary key field names
    required_fields JSON, -- Fields that must be present
    optional_fields JSON, -- Optional fields that may be included
    
    -- Query configuration
    base_query TEXT, -- Base SQL query or API parameters
    filter_parameters JSON, -- Available filter options
    aggregation_options JSON, -- Available aggregation methods
    
    -- Data quality and validation
    validation_rules JSON, -- Data validation rules and checks
    data_quality_threshold DECIMAL(5,2) DEFAULT 80.00, -- Minimum quality score
    last_quality_check TIMESTAMP,
    quality_score DECIMAL(5,2),
    
    -- Performance and caching
    cache_duration_minutes INT DEFAULT 60,
    enable_caching BOOLEAN DEFAULT TRUE,
    query_timeout_seconds INT DEFAULT 300,
    max_records_limit INT DEFAULT 100000,
    
    -- Usage and monitoring
    usage_count INT DEFAULT 0,
    last_accessed TIMESTAMP,
    average_query_time_ms INT,
    error_count INT DEFAULT 0,
    last_error TIMESTAMP,
    last_error_message TEXT,
    
    -- Availability and maintenance
    status ENUM('active', 'inactive', 'maintenance', 'deprecated') DEFAULT 'active',
    maintenance_window JSON, -- Scheduled maintenance times
    health_check_url VARCHAR(500),
    
    -- Documentation
    documentation TEXT,
    sample_data JSON, -- Sample data for testing
    field_descriptions JSON, -- Description of each field
    
    -- Access control
    required_permissions JSON, -- Permissions needed to access this source
    restricted_fields JSON, -- Fields with restricted access
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_data_sources_type (source_type, status),
    INDEX idx_data_sources_status (status, last_accessed DESC),
    INDEX idx_data_sources_performance (average_query_time_ms, usage_count),
    FULLTEXT INDEX idx_data_sources_search (source_name, description)
);
```

---

## ⏱️ **TIME-LAPSE & PROGRESS TRACKING**

### **timelapse_sequences**
```sql
CREATE TABLE timelapse_sequences (
    id UUID PRIMARY KEY,
    
    -- Basic sequence information
    title VARCHAR(255) NOT NULL,
    description TEXT,
    site_id UUID NOT NULL,
    created_by UUID NOT NULL,
    
    -- Source configuration
    primary_camera_id UUID NOT NULL,
    additional_camera_ids JSON, -- Array of additional camera IDs for multi-camera sequences
    
    -- Time range
    start_datetime TIMESTAMP NOT NULL,
    end_datetime TIMESTAMP NOT NULL,
    duration_seconds INT NOT NULL,
    
    -- Generation settings
    compression_level ENUM('low', 'medium', 'high') DEFAULT 'medium',
    frame_rate_fps INT DEFAULT 30,
    playback_speed DECIMAL(5,2) DEFAULT 1.0, -- Default playback speed multiplier
    resolution_width INT DEFAULT 1920,
    resolution_height INT DEFAULT 1080,
    
    -- Processing information
    generation_status ENUM('queued', 'processing', 'completed', 'failed', 'cancelled') DEFAULT 'queued',
    processing_started_at TIMESTAMP,
    processing_completed_at TIMESTAMP,
    processing_duration_seconds INT,
    
    -- File information
    output_file_path VARCHAR(500),
    output_file_format VARCHAR(10), -- mp4, gif, webm, avi
    file_size_bytes BIGINT,
    thumbnail_path VARCHAR(500),
    preview_gif_path VARCHAR(500),
    
    -- Quality metrics
    total_frames_processed INT,
    frames_with_activity INT,
    activity_score DECIMAL(5,2), -- 0-10 overall activity level
    quality_score DECIMAL(5,2), -- 0-10 visual quality assessment
    
    -- Metadata
    weather_conditions JSON, -- Weather during the time period
    project_phase VARCHAR(100), -- Construction phase during sequence
    milestone_events JSON, -- Major milestones captured in sequence
    
    -- Usage and sharing
    view_count INT DEFAULT 0,
    download_count INT DEFAULT 0,
    share_count INT DEFAULT 0,
    bookmark_count INT DEFAULT 0,
    
    -- Status and lifecycle
    status ENUM('active', 'archived', 'deleted') DEFAULT 'active',
    archived_at TIMESTAMP,
    retention_date DATE, -- When sequence can be deleted
    
    -- Error handling
    error_message TEXT,
    retry_count INT DEFAULT 0,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (site_id) REFERENCES sites(id),
    FOREIGN KEY (created_by) REFERENCES users(id),
    FOREIGN KEY (primary_camera_id) REFERENCES cameras(id),
    
    INDEX idx_timelapse_sequences_site (site_id, created_at DESC),
    INDEX idx_timelapse_sequences_creator (created_by, created_at DESC),
    INDEX idx_timelapse_sequences_camera (primary_camera_id, start_datetime DESC),
    INDEX idx_timelapse_sequences_status (generation_status, processing_started_at),
    INDEX idx_timelapse_sequences_timerange (start_datetime, end_datetime),
    INDEX idx_timelapse_sequences_quality (quality_score DESC, activity_score DESC)
);
```

### **timelapse_bookmarks**
```sql
CREATE TABLE timelapse_bookmarks (
    id UUID PRIMARY KEY,
    timelapse_sequence_id UUID NOT NULL,
    user_id UUID NOT NULL,
    
    -- Bookmark details
    bookmark_name VARCHAR(255) NOT NULL,
    description TEXT,
    
    -- Temporal information
    timestamp_seconds DECIMAL(10,3) NOT NULL, -- Precise timestamp within sequence
    frame_number INT, -- Exact frame number for precise positioning
    
    -- Context information
    bookmark_type ENUM('manual', 'milestone', 'activity', 'safety', 'progress', 'custom') DEFAULT 'manual',
    activity_detected VARCHAR(100), -- Type of activity at bookmark
    personnel_count INT, -- Number of personnel visible at bookmark
    equipment_present JSON, -- Array of equipment visible
    
    -- Visual markers
    thumbnail_path VARCHAR(500), -- Thumbnail image at bookmark time
    marker_color VARCHAR(7) DEFAULT '#FFA500', -- Hex color for timeline display
    marker_icon VARCHAR(50), -- Icon identifier for bookmark type
    
    -- Annotations
    annotations JSON, -- Array of annotation objects with coordinates and text
    highlight_areas JSON, -- Array of highlight regions in the frame
    
    -- Collaboration
    is_shared BOOLEAN DEFAULT FALSE,
    shared_with JSON, -- Array of user IDs with access
    comments_enabled BOOLEAN DEFAULT TRUE,
    
    -- Workflow status
    status ENUM('active', 'archived', 'deleted') DEFAULT 'active',
    reviewed BOOLEAN DEFAULT FALSE,
    reviewed_by UUID,
    reviewed_at TIMESTAMP,
    
    -- Usage tracking
    access_count INT DEFAULT 0,
    last_accessed TIMESTAMP,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (timelapse_sequence_id) REFERENCES timelapse_sequences(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (reviewed_by) REFERENCES users(id),
    
    INDEX idx_timelapse_bookmarks_sequence (timelapse_sequence_id, timestamp_seconds),
    INDEX idx_timelapse_bookmarks_user (user_id, created_at DESC),
    INDEX idx_timelapse_bookmarks_type (bookmark_type, status),
    INDEX idx_timelapse_bookmarks_shared (is_shared, shared_with),
    UNIQUE KEY unique_user_sequence_timestamp (user_id, timelapse_sequence_id, timestamp_seconds)
);
```

### **timelapse_events**
```sql
CREATE TABLE timelapse_events (
    id UUID PRIMARY KEY,
    timelapse_sequence_id UUID NOT NULL,
    
    -- Event timing
    event_timestamp TIMESTAMP NOT NULL,
    sequence_timestamp_seconds DECIMAL(10,3) NOT NULL, -- Time within the sequence
    duration_seconds INT, -- Event duration if applicable
    
    -- Event classification
    event_type ENUM('personnel_activity', 'equipment_movement', 'safety_incident', 'milestone_completion', 'weather_change', 'construction_phase', 'inspection', 'delivery') NOT NULL,
    event_category VARCHAR(100), -- More specific categorization
    
    -- Event details
    event_title VARCHAR(255) NOT NULL,
    event_description TEXT,
    confidence_score DECIMAL(5,2), -- AI confidence in event detection
    
    -- Detected elements
    personnel_count INT DEFAULT 0,
    equipment_detected JSON, -- Array of detected equipment
    vehicle_count INT DEFAULT 0,
    activity_level ENUM('low', 'moderate', 'high', 'peak') DEFAULT 'moderate',
    
    -- Spatial information
    detection_zones JSON, -- Array of zone IDs where event occurred
    bounding_boxes JSON, -- Coordinate data for detected objects
    camera_angle_info JSON, -- Camera positioning data
    
    -- Correlation data
    related_alert_id UUID, -- Link to safety alerts if applicable
    related_detection_ids JSON, -- Array of AI detection IDs
    milestone_reference VARCHAR(255), -- Project milestone reference
    
    -- Visual evidence
    thumbnail_path VARCHAR(500),
    evidence_images JSON, -- Array of evidence image paths
    annotation_data JSON, -- Visual annotations and highlights
    
    -- Impact assessment
    impact_level ENUM('minimal', 'low', 'moderate', 'significant', 'critical') DEFAULT 'minimal',
    safety_implications ENUM('none', 'minor', 'moderate', 'serious', 'critical') DEFAULT 'none',
    
    -- Verification and validation
    auto_detected BOOLEAN DEFAULT TRUE,
    manually_verified BOOLEAN DEFAULT FALSE,
    verified_by UUID,
    verified_at TIMESTAMP,
    
    -- Status
    status ENUM('detected', 'verified', 'false_positive', 'archived') DEFAULT 'detected',
    
    FOREIGN KEY (timelapse_sequence_id) REFERENCES timelapse_sequences(id) ON DELETE CASCADE,
    FOREIGN KEY (related_alert_id) REFERENCES alerts(id),
    FOREIGN KEY (verified_by) REFERENCES users(id),
    
    INDEX idx_timelapse_events_sequence_time (timelapse_sequence_id, sequence_timestamp_seconds),
    INDEX idx_timelapse_events_type (event_type, event_category),
    INDEX idx_timelapse_events_timestamp (event_timestamp DESC),
    INDEX idx_timelapse_events_impact (impact_level, safety_implications),
    INDEX idx_timelapse_events_verification (auto_detected, manually_verified),
    INDEX idx_timelapse_events_confidence (confidence_score DESC)
);
```

### **timelapse_shares**
```sql
CREATE TABLE timelapse_shares (
    id UUID PRIMARY KEY,
    timelapse_sequence_id UUID NOT NULL,
    
    -- Sharing details
    shared_by UUID NOT NULL,
    share_type ENUM('link', 'email', 'embed', 'download') NOT NULL,
    
    -- Recipients and access
    shared_with_users JSON, -- Array of user IDs
    shared_with_emails JSON, -- Array of email addresses for external sharing
    access_level ENUM('view', 'comment', 'bookmark', 'download') DEFAULT 'view',
    
    -- Share configuration
    share_token VARCHAR(255) UNIQUE,
    password_protected BOOLEAN DEFAULT FALSE,
    password_hash VARCHAR(255),
    
    -- Playback context
    start_time_seconds DECIMAL(10,3) DEFAULT 0, -- Starting playback position
    playback_speed DECIMAL(5,2) DEFAULT 1.0,
    include_bookmarks BOOLEAN DEFAULT TRUE,
    include_annotations BOOLEAN DEFAULT TRUE,
    
    -- Restrictions and limits
    expires_at TIMESTAMP,
    max_views INT,
    max_downloads INT,
    allowed_ip_ranges JSON,
    
    -- Usage tracking
    view_count INT DEFAULT 0,
    download_count INT DEFAULT 0,
    unique_viewers INT DEFAULT 0,
    last_accessed_at TIMESTAMP,
    
    -- Access logs summary
    total_watch_time_seconds INT DEFAULT 0,
    average_session_duration_seconds INT,
    bookmarks_created_by_viewers INT DEFAULT 0,
    
    -- Feedback collection
    allow_feedback BOOLEAN DEFAULT FALSE,
    feedback_collected JSON, -- Array of feedback objects
    
    -- Share metadata
    share_title VARCHAR(255),
    share_description TEXT,
    custom_thumbnail_path VARCHAR(500),
    
    -- Status and lifecycle
    status ENUM('active', 'expired', 'disabled', 'revoked') DEFAULT 'active',
    revoked_at TIMESTAMP,
    revoked_by UUID,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (timelapse_sequence_id) REFERENCES timelapse_sequences(id),
    FOREIGN KEY (shared_by) REFERENCES users(id),
    FOREIGN KEY (revoked_by) REFERENCES users(id),
    
    INDEX idx_timelapse_shares_sequence (timelapse_sequence_id, created_at DESC),
    INDEX idx_timelapse_shares_token (share_token, status),
    INDEX idx_timelapse_shares_sharer (shared_by, created_at DESC),
    INDEX idx_timelapse_shares_expires (expires_at, status),
    INDEX idx_timelapse_shares_usage (view_count DESC, download_count DESC)
);
```

### **construction_milestones**
```sql
CREATE TABLE construction_milestones (
    id UUID PRIMARY KEY,
    site_id UUID NOT NULL,
    
    -- Milestone identification
    milestone_name VARCHAR(255) NOT NULL,
    milestone_code VARCHAR(50), -- Project-specific milestone identifier
    description TEXT,
    
    -- Project context
    project_phase VARCHAR(100),
    work_package VARCHAR(100),
    contractor VARCHAR(255),
    
    -- Scheduling information
    planned_start_date DATE,
    planned_completion_date DATE,
    actual_start_date DATE,
    actual_completion_date DATE,
    
    -- Progress tracking
    completion_percentage DECIMAL(5,2) DEFAULT 0.00,
    status ENUM('not_started', 'in_progress', 'completed', 'delayed', 'cancelled', 'on_hold') DEFAULT 'not_started',
    
    -- Dependencies
    prerequisite_milestones JSON, -- Array of milestone IDs that must be completed first
    dependent_milestones JSON, -- Array of milestone IDs that depend on this one
    
    -- Quality and compliance
    quality_checkpoints JSON, -- Array of quality check requirements
    compliance_requirements JSON, -- Regulatory compliance requirements
    safety_requirements JSON, -- Safety-specific requirements
    
    -- Documentation
    specification_documents JSON, -- Array of specification document references
    approval_documents JSON, -- Array of approval document references
    inspection_records JSON, -- Array of inspection record references
    
    -- Visual documentation
    reference_images JSON, -- Array of reference/plan images
    progress_images JSON, -- Array of progress photos
    timelapse_sequences JSON, -- Array of related time-lapse sequence IDs
    
    -- Budget and resources
    budgeted_amount DECIMAL(12,2),
    actual_cost DECIMAL(12,2),
    allocated_resources JSON, -- Personnel and equipment allocations
    
    -- Timeline analysis
    planned_duration_days INT,
    actual_duration_days INT,
    delay_days INT DEFAULT 0,
    delay_reasons JSON, -- Array of delay reason descriptions
    
    -- Automated detection
    auto_detection_enabled BOOLEAN DEFAULT FALSE,
    detection_criteria JSON, -- Criteria for automated milestone detection
    last_detection_check TIMESTAMP,
    
    -- Approval workflow
    requires_approval BOOLEAN DEFAULT FALSE,
    approved_by UUID,
    approved_at TIMESTAMP,
    approval_notes TEXT,
    
    -- Change management
    change_requests JSON, -- Array of change request references
    revision_number INT DEFAULT 1,
    previous_version_id UUID,
    
    created_by UUID NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (site_id) REFERENCES sites(id),
    FOREIGN KEY (created_by) REFERENCES users(id),
    FOREIGN KEY (approved_by) REFERENCES users(id),
    FOREIGN KEY (previous_version_id) REFERENCES construction_milestones(id),
    
    INDEX idx_construction_milestones_site (site_id, planned_completion_date),
    INDEX idx_construction_milestones_status (status, completion_percentage DESC),
    INDEX idx_construction_milestones_phase (project_phase, status),
    INDEX idx_construction_milestones_schedule (planned_start_date, planned_completion_date),
    INDEX idx_construction_milestones_delays (delay_days DESC, status),
    INDEX idx_construction_milestones_creator (created_by, created_at DESC),
    UNIQUE KEY unique_site_milestone_code (site_id, milestone_code)
);
```

### **street_view_cameras**
```sql
CREATE TABLE street_view_cameras (
    id UUID PRIMARY KEY,
    camera_id UUID NOT NULL, -- Reference to main cameras table
    
    -- Street view specific configuration
    is_street_view_enabled BOOLEAN DEFAULT FALSE,
    street_view_priority INT DEFAULT 1, -- 1=highest, 10=lowest
    
    -- Camera positioning and coverage
    field_of_view_degrees INT DEFAULT 90, -- Horizontal field of view
    tilt_angle_degrees INT DEFAULT 0, -- Up/down tilt from horizontal
    pan_range_start_degrees INT DEFAULT 0, -- Start of pan range (0-360)
    pan_range_end_degrees INT DEFAULT 360, -- End of pan range
    zoom_capability ENUM('none', 'digital', 'optical', 'both') DEFAULT 'digital',
    
    -- PTZ (Pan-Tilt-Zoom) capabilities
    ptz_enabled BOOLEAN DEFAULT FALSE,
    pan_speed_degrees_per_second DECIMAL(6,2) DEFAULT 10.0,
    tilt_speed_degrees_per_second DECIMAL(6,2) DEFAULT 10.0,
    zoom_levels JSON, -- Array of available zoom levels
    preset_positions JSON, -- Array of preset PTZ positions
    
    -- Street view quality settings
    streaming_resolution VARCHAR(20) DEFAULT '1080p', -- 720p, 1080p, 4K
    streaming_fps INT DEFAULT 30,
    streaming_bitrate_kbps INT DEFAULT 5000,
    low_light_enhancement BOOLEAN DEFAULT TRUE,
    image_stabilization BOOLEAN DEFAULT TRUE,
    
    -- GPS and positioning
    precise_latitude DECIMAL(10,7),
    precise_longitude DECIMAL(10,7),
    precise_elevation DECIMAL(6,2),
    mounting_height_meters DECIMAL(5,2) DEFAULT 3.0,
    orientation_degrees DECIMAL(6,2) DEFAULT 0, -- 0=North, 90=East, etc.
    
    -- Coverage and routing integration
    route_coverage JSON, -- Array of route IDs this camera covers
    waypoint_coverage JSON, -- Array of waypoint IDs this camera monitors
    coverage_radius_meters DECIMAL(6,2) DEFAULT 50,
    optimal_viewing_distance_meters DECIMAL(6,2) DEFAULT 25,
    
    -- AI and analytics integration
    ai_detection_enabled BOOLEAN DEFAULT TRUE,
    real_time_analysis BOOLEAN DEFAULT TRUE,
    detection_confidence_threshold DECIMAL(3,2) DEFAULT 0.70,
    alert_trigger_types JSON, -- Types of detections that should trigger alerts
    
    -- Overlay and augmented reality
    overlay_enabled BOOLEAN DEFAULT TRUE,
    overlay_elements JSON, -- Array of overlay element configurations
    ar_markers_supported BOOLEAN DEFAULT FALSE,
    compass_overlay BOOLEAN DEFAULT TRUE,
    coordinate_overlay BOOLEAN DEFAULT FALSE,
    
    -- Environmental considerations
    weather_protection_rating VARCHAR(10), -- IP rating (IP65, IP67, etc.)
    operating_temperature_min_celsius DECIMAL(4,1) DEFAULT -20,
    operating_temperature_max_celsius DECIMAL(4,1) DEFAULT 50,
    night_vision_capability BOOLEAN DEFAULT FALSE,
    infrared_illumination BOOLEAN DEFAULT FALSE,
    
    -- Maintenance and monitoring
    health_check_interval_minutes INT DEFAULT 60,
    last_health_check TIMESTAMP,
    health_status ENUM('excellent', 'good', 'fair', 'poor', 'offline') DEFAULT 'good',
    maintenance_schedule JSON, -- Maintenance schedule configuration
    
    -- Performance metrics
    uptime_percentage DECIMAL(5,2) DEFAULT 99.0,
    average_response_time_ms INT DEFAULT 200,
    data_usage_mb_per_hour DECIMAL(8,2) DEFAULT 1000,
    viewer_session_count INT DEFAULT 0,
    
    -- Access control
    public_access BOOLEAN DEFAULT FALSE,
    authorized_user_roles JSON, -- Array of roles that can access this camera
    viewing_restrictions JSON, -- Time-based or condition-based restrictions
    
    -- Integration settings
    zoneminder_monitor_id VARCHAR(50),
    streaming_protocol ENUM('RTSP', 'HTTP', 'WebRTC', 'HLS') DEFAULT 'RTSP',
    streaming_url VARCHAR(500),
    backup_streaming_url VARCHAR(500),
    
    -- Status and lifecycle
    status ENUM('active', 'inactive', 'maintenance', 'decommissioned') DEFAULT 'active',
    installation_date DATE,
    warranty_expiration_date DATE,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (camera_id) REFERENCES cameras(id),
    
    INDEX idx_street_view_cameras_enabled (is_street_view_enabled, street_view_priority),
    INDEX idx_street_view_cameras_ptz (ptz_enabled, status),
    INDEX idx_street_view_cameras_coordinates (precise_latitude, precise_longitude),
    INDEX idx_street_view_cameras_health (health_status, last_health_check),
    INDEX idx_street_view_cameras_route_coverage (route_coverage),
    INDEX idx_street_view_cameras_performance (uptime_percentage DESC, average_response_time_ms)
);
```

---

## 🗺️ **NAVIGATION & STREET VIEW**

### **navigation_routes**
```sql
CREATE TABLE navigation_routes (
    id UUID PRIMARY KEY,
    site_id UUID NOT NULL,
    
    -- Route identification
    route_name VARCHAR(255) NOT NULL,
    route_code VARCHAR(50) UNIQUE,
    description TEXT,
    
    -- Route type and purpose
    route_type ENUM('patrol', 'inspection', 'emergency_evacuation', 'material_transport', 'visitor_tour', 'maintenance', 'custom') NOT NULL,
    purpose VARCHAR(255),
    priority_level ENUM('low', 'medium', 'high', 'critical') DEFAULT 'medium',
    
    -- Geographic information
    start_coordinates JSON NOT NULL, -- {lat: float, lng: float, elevation: float}
    end_coordinates JSON NOT NULL,
    bounding_box JSON, -- Geographic boundary for the route
    
    -- Route characteristics
    total_distance_meters DECIMAL(10,2) NOT NULL,
    estimated_duration_minutes INT NOT NULL,
    elevation_change_meters DECIMAL(6,2) DEFAULT 0,
    difficulty_level ENUM('easy', 'moderate', 'difficult', 'expert') DEFAULT 'easy',
    
    -- Safety and accessibility
    safety_rating ENUM('very_safe', 'safe', 'caution', 'hazardous', 'restricted') DEFAULT 'safe',
    accessibility_level ENUM('wheelchair', 'mobility_aid', 'walking', 'restricted') DEFAULT 'walking',
    ppe_requirements JSON, -- Array of required PPE for this route
    hazard_warnings JSON, -- Array of potential hazards along route
    
    -- Time and weather constraints
    time_restrictions JSON, -- Operating hours and restricted times
    weather_limitations JSON, -- Weather conditions that restrict route usage
    seasonal_availability JSON, -- Seasonal restrictions or modifications
    
    -- Performance tracking
    usage_count INT DEFAULT 0,
    completion_rate DECIMAL(5,2) DEFAULT 100.00,
    average_completion_time_minutes DECIMAL(6,2),
    success_rate DECIMAL(5,2) DEFAULT 100.00,
    last_successful_completion TIMESTAMP,
    
    -- Route optimization
    optimization_score DECIMAL(5,2), -- Route efficiency score 0-10
    alternative_routes JSON, -- Array of alternative route IDs
    traffic_pattern_data JSON, -- Historical traffic/usage patterns
    
    -- Maintenance and updates
    last_survey_date DATE,
    next_maintenance_date DATE,
    route_condition ENUM('excellent', 'good', 'fair', 'poor', 'closed') DEFAULT 'good',
    maintenance_notes TEXT,
    
    -- Access control
    access_level ENUM('public', 'staff', 'supervisor', 'manager', 'restricted') DEFAULT 'staff',
    authorized_roles JSON, -- Array of roles that can use this route
    restricted_users JSON, -- Array of user IDs with restricted access
    
    -- Version control
    version_number INT DEFAULT 1,
    previous_version_id UUID,
    change_log JSON, -- History of route modifications
    
    -- Status
    status ENUM('active', 'inactive', 'maintenance', 'archived') DEFAULT 'active',
    created_by UUID NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (site_id) REFERENCES sites(id),
    FOREIGN KEY (created_by) REFERENCES users(id),
    FOREIGN KEY (previous_version_id) REFERENCES navigation_routes(id),
    
    INDEX idx_navigation_routes_site (site_id, status),
    INDEX idx_navigation_routes_type (route_type, priority_level),
    INDEX idx_navigation_routes_performance (completion_rate DESC, success_rate DESC),
    INDEX idx_navigation_routes_safety (safety_rating, accessibility_level),
    INDEX idx_navigation_routes_creator (created_by, created_at DESC),
    UNIQUE KEY unique_site_route_code (site_id, route_code)
);
```

### **route_waypoints**
```sql
CREATE TABLE route_waypoints (
    id UUID PRIMARY KEY,
    route_id UUID NOT NULL,
    
    -- Waypoint identification
    waypoint_name VARCHAR(255) NOT NULL,
    waypoint_code VARCHAR(50),
    sequence_order INT NOT NULL, -- Order of waypoint in route
    
    -- Geographic coordinates
    latitude DECIMAL(10,7) NOT NULL,
    longitude DECIMAL(10,7) NOT NULL,
    elevation DECIMAL(6,2) DEFAULT 0,
    coordinate_system VARCHAR(50) DEFAULT 'WGS84',
    
    -- Positioning accuracy
    horizontal_accuracy_meters DECIMAL(5,2) DEFAULT 3.0,
    vertical_accuracy_meters DECIMAL(5,2) DEFAULT 5.0,
    gps_quality_score DECIMAL(3,1) DEFAULT 8.0, -- 0-10 GPS signal quality
    
    -- Waypoint type and purpose
    waypoint_type ENUM('start', 'checkpoint', 'turn', 'caution', 'stop', 'inspection', 'emergency', 'end', 'custom') NOT NULL,
    action_required ENUM('pass_through', 'pause', 'inspect', 'report', 'confirm', 'emergency_check') DEFAULT 'pass_through',
    
    -- Navigation instructions
    approach_instructions TEXT NOT NULL,
    departure_instructions TEXT,
    audio_instructions TEXT, -- Text-to-speech navigation guidance
    visual_markers TEXT, -- Description of visual landmarks
    
    -- Distance and timing
    distance_from_previous_meters DECIMAL(8,2) DEFAULT 0,
    estimated_travel_time_minutes DECIMAL(5,2) DEFAULT 0,
    recommended_pause_duration_seconds INT DEFAULT 0,
    
    -- Safety and hazard information
    safety_level ENUM('safe', 'caution', 'danger', 'restricted') DEFAULT 'safe',
    hazard_types JSON, -- Array of hazard types at this waypoint
    safety_equipment_required JSON, -- Additional safety equipment needed
    emergency_procedures TEXT, -- Emergency procedures specific to this waypoint
    
    -- Camera and monitoring
    associated_camera_ids JSON, -- Array of camera IDs covering this waypoint
    monitoring_required BOOLEAN DEFAULT FALSE,
    photo_documentation_required BOOLEAN DEFAULT FALSE,
    
    -- Environmental conditions
    indoor_outdoor ENUM('indoor', 'outdoor', 'covered') DEFAULT 'outdoor',
    lighting_conditions ENUM('excellent', 'good', 'poor', 'requires_flashlight') DEFAULT 'good',
    weather_exposure ENUM('none', 'partial', 'full') DEFAULT 'partial',
    
    -- Interactive features
    qr_code_present BOOLEAN DEFAULT FALSE,
    qr_code_data VARCHAR(255),
    nfc_tag_present BOOLEAN DEFAULT FALSE,
    beacon_uuid VARCHAR(255), -- Bluetooth beacon identifier
    
    -- Validation and verification
    checkpoint_validation_required BOOLEAN DEFAULT FALSE,
    validation_method ENUM('gps', 'qr_code', 'nfc', 'manual_confirmation', 'photo') DEFAULT 'gps',
    validation_radius_meters DECIMAL(5,2) DEFAULT 5.0,
    
    -- Performance tracking
    average_arrival_time_minutes DECIMAL(6,2),
    completion_rate DECIMAL(5,2) DEFAULT 100.00,
    skip_rate DECIMAL(5,2) DEFAULT 0.00, -- Percentage of times waypoint was skipped
    issue_report_count INT DEFAULT 0,
    
    -- Maintenance
    last_inspection_date DATE,
    condition_status ENUM('excellent', 'good', 'fair', 'poor', 'blocked') DEFAULT 'good',
    maintenance_required BOOLEAN DEFAULT FALSE,
    maintenance_notes TEXT,
    
    -- Status
    status ENUM('active', 'inactive', 'temporary', 'archived') DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (route_id) REFERENCES navigation_routes(id) ON DELETE CASCADE,
    
    INDEX idx_route_waypoints_route_sequence (route_id, sequence_order),
    INDEX idx_route_waypoints_coordinates (latitude, longitude),
    INDEX idx_route_waypoints_type (waypoint_type, action_required),
    INDEX idx_route_waypoints_safety (safety_level, hazard_types),
    INDEX idx_route_waypoints_performance (completion_rate DESC),
    UNIQUE KEY unique_route_sequence (route_id, sequence_order),
    UNIQUE KEY unique_route_waypoint_code (route_id, waypoint_code)
);
```

### **navigation_sessions**
```sql
CREATE TABLE navigation_sessions (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL,
    route_id UUID NOT NULL,
    
    -- Session identification
    session_name VARCHAR(255),
    session_purpose ENUM('patrol', 'inspection', 'emergency', 'training', 'tour', 'maintenance', 'other') NOT NULL,
    
    -- Timing information
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ended_at TIMESTAMP,
    total_duration_minutes DECIMAL(8,2),
    planned_duration_minutes INT,
    
    -- Session status
    session_status ENUM('started', 'in_progress', 'paused', 'completed', 'cancelled', 'emergency_stopped') NOT NULL DEFAULT 'started',
    completion_percentage DECIMAL(5,2) DEFAULT 0.00,
    
    -- Route progress
    current_waypoint_id UUID,
    waypoints_completed INT DEFAULT 0,
    waypoints_skipped INT DEFAULT 0,
    total_waypoints INT NOT NULL,
    
    -- Distance and movement
    total_distance_traveled_meters DECIMAL(10,2) DEFAULT 0,
    planned_distance_meters DECIMAL(10,2),
    deviation_distance_meters DECIMAL(8,2) DEFAULT 0, -- Distance off planned route
    
    -- Performance metrics
    average_speed_mps DECIMAL(5,2), -- Meters per second
    max_speed_mps DECIMAL(5,2),
    pause_count INT DEFAULT 0,
    total_pause_duration_minutes DECIMAL(8,2) DEFAULT 0,
    
    -- GPS tracking data
    gps_track_data JSON, -- Array of GPS coordinates with timestamps
    gps_accuracy_average DECIMAL(5,2),
    gps_signal_quality_average DECIMAL(3,1),
    indoor_positioning_used BOOLEAN DEFAULT FALSE,
    
    -- Safety and compliance
    safety_incidents INT DEFAULT 0,
    ppe_compliance_checks INT DEFAULT 0,
    ppe_compliance_failures INT DEFAULT 0,
    hazard_encounters INT DEFAULT 0,
    emergency_stops INT DEFAULT 0,
    
    -- Communication and reporting
    reports_submitted INT DEFAULT 0,
    photos_taken INT DEFAULT 0,
    voice_notes_recorded INT DEFAULT 0,
    emergency_calls_made INT DEFAULT 0,
    
    -- Device and connectivity
    device_type VARCHAR(100),
    device_id VARCHAR(255),
    connectivity_issues INT DEFAULT 0,
    offline_periods JSON, -- Array of offline time periods
    
    -- Weather and environmental
    weather_conditions JSON, -- Weather data during session
    visibility_conditions ENUM('excellent', 'good', 'fair', 'poor', 'very_poor') DEFAULT 'good',
    temperature_celsius DECIMAL(4,1),
    
    -- Session quality assessment
    navigation_accuracy_score DECIMAL(3,1), -- 0-10 score
    route_efficiency_score DECIMAL(3,1),
    safety_compliance_score DECIMAL(3,1),
    overall_session_rating DECIMAL(3,1),
    
    -- Issues and feedback
    technical_issues JSON, -- Array of technical issues encountered
    route_feedback TEXT,
    improvement_suggestions TEXT,
    
    -- Approval and verification
    supervisor_review_required BOOLEAN DEFAULT FALSE,
    reviewed_by UUID,
    reviewed_at TIMESTAMP,
    approved BOOLEAN DEFAULT FALSE,
    
    -- Data export and sharing
    session_report_generated BOOLEAN DEFAULT FALSE,
    report_file_path VARCHAR(500),
    shared_with_users JSON, -- Array of user IDs who have access
    
    -- Status
    archived BOOLEAN DEFAULT FALSE,
    archived_at TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (route_id) REFERENCES navigation_routes(id),
    FOREIGN KEY (current_waypoint_id) REFERENCES route_waypoints(id),
    FOREIGN KEY (reviewed_by) REFERENCES users(id),
    
    INDEX idx_navigation_sessions_user_time (user_id, started_at DESC),
    INDEX idx_navigation_sessions_route (route_id, started_at DESC),
    INDEX idx_navigation_sessions_status (session_status, started_at DESC),
    INDEX idx_navigation_sessions_performance (completion_percentage DESC, total_duration_minutes),
    INDEX idx_navigation_sessions_safety (safety_incidents, ppe_compliance_failures),
    INDEX idx_navigation_sessions_reviewed (supervisor_review_required, reviewed_by)
);
```

---

## 🔍 **STREET VIEW COMPARISON & ANALYSIS**

### **street_view_comparisons**
```sql
CREATE TABLE street_view_comparisons (
    id UUID PRIMARY KEY,
    session_before_id UUID NOT NULL, -- Reference to earlier session
    session_after_id UUID NOT NULL, -- Reference to later session 
    site_id UUID NOT NULL,
    location_zone VARCHAR(255),
    
    -- Comparison configuration
    comparison_type ENUM('construction_progress', 'equipment_changes', 'safety_compliance', 'personnel_activity') NOT NULL,
    timespan_days INTEGER NOT NULL,
    
    -- Analysis results
    overall_progress_percentage DECIMAL(5,2),
    construction_growth DECIMAL(5,2),
    equipment_changes_count INTEGER DEFAULT 0,
    safety_improvements_count INTEGER DEFAULT 0,
    personnel_variation_percentage DECIMAL(5,2),
    
    -- Processing status
    analysis_status ENUM('pending', 'processing', 'completed', 'failed') DEFAULT 'pending',
    processing_started_at TIMESTAMP,
    processing_completed_at TIMESTAMP,
    processing_time_seconds INT,
    error_message TEXT,
    
    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by UUID NOT NULL,
    
    FOREIGN KEY (session_before_id) REFERENCES street_view_sessions(id),
    FOREIGN KEY (session_after_id) REFERENCES street_view_sessions(id),
    FOREIGN KEY (site_id) REFERENCES sites(id),
    FOREIGN KEY (created_by) REFERENCES users(id),
    
    INDEX idx_sv_comparisons_site (site_id, created_at DESC),
    INDEX idx_sv_comparisons_type (comparison_type, analysis_status),
    INDEX idx_sv_comparisons_timespan (timespan_days, overall_progress_percentage),
    INDEX idx_sv_comparisons_status (analysis_status, processing_completed_at),
    UNIQUE KEY unique_comparison_sessions (session_before_id, session_after_id, comparison_type)
);
```

### **street_view_sessions**
```sql
CREATE TABLE street_view_sessions (
    id UUID PRIMARY KEY,
    site_id UUID NOT NULL,
    camera_id UUID NOT NULL,
    
    -- Session metadata
    session_label VARCHAR(255) NOT NULL,
    session_date DATE NOT NULL,
    session_time TIME NOT NULL,
    
    -- Location and positioning
    location_coordinates_x DECIMAL(10,6),
    location_coordinates_y DECIMAL(10,6),
    heading_degrees DECIMAL(5,2), -- 0-360 degrees
    
    -- Recording details
    weather_conditions TEXT,
    recording_quality ENUM('low', 'medium', 'high', 'ultra') DEFAULT 'high',
    file_path TEXT,
    file_size_mb DECIMAL(10,2),
    duration_seconds INTEGER,
    
    -- Status and metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by UUID NOT NULL,
    
    FOREIGN KEY (site_id) REFERENCES sites(id),
    FOREIGN KEY (camera_id) REFERENCES cameras(id),
    FOREIGN KEY (created_by) REFERENCES users(id),
    
    INDEX idx_sv_sessions_site_date (site_id, session_date DESC),
    INDEX idx_sv_sessions_camera (camera_id, session_date DESC),
    INDEX idx_sv_sessions_location (location_coordinates_x, location_coordinates_y),
    INDEX idx_sv_sessions_quality (recording_quality, file_size_mb)
);
```

### **detected_changes**
```sql
CREATE TABLE detected_changes (
    id UUID PRIMARY KEY,
    comparison_id UUID NOT NULL,
    
    -- Change details
    change_type ENUM('construction_progress', 'equipment_addition', 'safety_improvement', 'personnel_increase', 'material_change', 'structural_change') NOT NULL,
    severity ENUM('low', 'medium', 'high', 'critical') NOT NULL,
    description TEXT NOT NULL,
    
    -- Location information
    location_name VARCHAR(255),
    location_coordinates_x DECIMAL(10,6),
    location_coordinates_y DECIMAL(10,6),
    
    -- AI analysis results
    confidence_percentage DECIMAL(5,2) NOT NULL,
    impact_description TEXT,
    ai_model_version VARCHAR(50),
    detection_algorithm VARCHAR(100),
    
    -- Review workflow
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    reviewed_by UUID,
    review_status ENUM('pending', 'confirmed', 'rejected', 'needs_review') DEFAULT 'pending',
    review_notes TEXT,
    
    FOREIGN KEY (comparison_id) REFERENCES street_view_comparisons(id) ON DELETE CASCADE,
    FOREIGN KEY (reviewed_by) REFERENCES users(id),
    
    INDEX idx_detected_changes_comparison (comparison_id, change_type),
    INDEX idx_detected_changes_severity (severity, confidence_percentage DESC),
    INDEX idx_detected_changes_location (location_name, change_type),
    INDEX idx_detected_changes_review (review_status, created_at DESC)
);
```

### **comparison_locations**
```sql
CREATE TABLE comparison_locations (
    id UUID PRIMARY KEY,
    site_id UUID NOT NULL,
    
    -- Location details
    location_name VARCHAR(255) NOT NULL,
    description TEXT,
    coordinates_x DECIMAL(10,6),
    coordinates_y DECIMAL(10,6),
    
    -- Classification
    zone_type ENUM('foundation', 'structural', 'entrance', 'equipment_yard', 'storage', 'office', 'safety') NOT NULL,
    monitoring_priority ENUM('low', 'medium', 'high', 'critical') DEFAULT 'medium',
    
    -- Status and activity
    is_active BOOLEAN DEFAULT TRUE,
    last_comparison_date TIMESTAMP,
    change_frequency_score DECIMAL(5,2), -- Historical change frequency
    
    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (site_id) REFERENCES sites(id),
    
    INDEX idx_comparison_locations_site (site_id, is_active),
    INDEX idx_comparison_locations_zone (zone_type, monitoring_priority),
    INDEX idx_comparison_locations_activity (change_frequency_score DESC, last_comparison_date),
    INDEX idx_comparison_locations_coordinates (coordinates_x, coordinates_y)
);
```

### **comparison_analysis_metrics**
```sql
CREATE TABLE comparison_analysis_metrics (
    id UUID PRIMARY KEY,
    comparison_id UUID NOT NULL,
    
    -- Metric details
    metric_type ENUM('overall_progress', 'construction_growth', 'equipment_changes', 'safety_improvements', 'personnel_variation', 'cost_impact', 'timeline_impact') NOT NULL,
    metric_value DECIMAL(10,4) NOT NULL,
    metric_unit VARCHAR(50),
    
    -- Analysis metadata
    calculation_method TEXT,
    baseline_value DECIMAL(10,4),
    improvement_percentage DECIMAL(5,2),
    trend_direction ENUM('increasing', 'decreasing', 'stable', 'volatile'),
    confidence_level DECIMAL(5,2),
    
    -- Processing information
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    calculated_by VARCHAR(100), -- AI model or user ID
    
    FOREIGN KEY (comparison_id) REFERENCES street_view_comparisons(id) ON DELETE CASCADE,
    
    INDEX idx_analysis_metrics_comparison (comparison_id, metric_type),
    INDEX idx_analysis_metrics_value (metric_value DESC, improvement_percentage),
    INDEX idx_analysis_metrics_trend (trend_direction, confidence_level DESC),
    UNIQUE KEY unique_comparison_metric (comparison_id, metric_type)
);
```

---

## 🛣️ **PATH ADMINISTRATION & ROUTING**

### **inspection_paths**
```sql
CREATE TABLE inspection_paths (
    id UUID PRIMARY KEY,
    site_id UUID NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    
    -- Path classification
    path_type ENUM('inspection', 'maintenance', 'emergency', 'quality', 'tour', 'custom') NOT NULL,
    status ENUM('active', 'inactive', 'draft', 'archived') DEFAULT 'draft',
    priority ENUM('critical', 'high', 'medium', 'low') DEFAULT 'medium',
    
    -- Assignment and ownership
    created_by UUID NOT NULL,
    assigned_to VARCHAR(255), -- Team or individual assignment
    assigned_user_ids JSON, -- Array of specific user IDs
    
    -- Path characteristics
    estimated_duration_minutes INTEGER,
    total_distance_meters DECIMAL(10,2),
    waypoint_count INTEGER DEFAULT 0,
    zone_coverage JSON, -- Array of zone IDs covered
    
    -- Performance metrics
    usage_count INTEGER DEFAULT 0,
    completion_rate DECIMAL(5,2) DEFAULT 0.00,
    average_completion_time_minutes INTEGER,
    success_rate DECIMAL(5,2) DEFAULT 0.00,
    
    -- Path configuration
    path_coordinates JSON, -- Array of waypoint coordinates
    zone_sequence JSON, -- Ordered zone visit sequence
    required_equipment JSON, -- Required tools/equipment
    safety_requirements JSON, -- Safety protocols
    
    -- Schedule and timing
    is_scheduled BOOLEAN DEFAULT FALSE,
    schedule_frequency ENUM('daily', 'weekly', 'monthly', 'on_demand'),
    schedule_days JSON, -- Days of week if recurring
    preferred_time_slots JSON, -- Time ranges for execution
    
    -- Metadata
    weather_dependency ENUM('any', 'clear_only', 'daylight_only'),
    skill_level_required ENUM('basic', 'intermediate', 'advanced', 'expert'),
    certification_required JSON, -- Required certifications
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    last_used TIMESTAMP,
    archived_at TIMESTAMP,
    
    FOREIGN KEY (site_id) REFERENCES sites(id),
    FOREIGN KEY (created_by) REFERENCES users(id),
    
    INDEX idx_inspection_paths_site_type (site_id, path_type, status),
    INDEX idx_inspection_paths_priority (priority, status),
    INDEX idx_inspection_paths_usage (usage_count DESC, completion_rate DESC),
    INDEX idx_inspection_paths_schedule (is_scheduled, schedule_frequency),
    FULLTEXT INDEX idx_inspection_paths_search (name, description)
);
```

### **path_waypoints**
```sql
CREATE TABLE path_waypoints (
    id UUID PRIMARY KEY,
    path_id UUID NOT NULL,
    waypoint_order INTEGER NOT NULL,
    waypoint_name VARCHAR(255) NOT NULL,
    description TEXT,
    
    -- Location details
    coordinates_x DECIMAL(10,6) NOT NULL,
    coordinates_y DECIMAL(10,6) NOT NULL,
    elevation DECIMAL(8,2),
    zone_id UUID,
    
    -- Waypoint configuration
    waypoint_type ENUM('checkpoint', 'inspection', 'maintenance', 'safety', 'assembly', 'exit', 'viewpoint', 'start', 'end', 'rest') NOT NULL,
    is_mandatory BOOLEAN DEFAULT TRUE,
    estimated_time_minutes INTEGER DEFAULT 5,
    inspection_checklist JSON, -- Inspection items at this waypoint
    
    -- Camera and monitoring
    camera_id UUID,
    monitoring_required BOOLEAN DEFAULT FALSE,
    photo_required BOOLEAN DEFAULT FALSE,
    notes_required BOOLEAN DEFAULT FALSE,
    
    -- Safety and access
    safety_level ENUM('safe', 'caution', 'restricted', 'danger') DEFAULT 'safe',
    required_ppe JSON, -- PPE required at this waypoint
    access_restrictions JSON, -- Access level requirements
    weather_restrictions JSON, -- Weather limitations
    
    -- Performance tracking
    visit_count INTEGER DEFAULT 0,
    average_time_spent_minutes DECIMAL(5,2) DEFAULT 0.00,
    issue_frequency DECIMAL(5,2) DEFAULT 0.00,
    last_visited TIMESTAMP,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (path_id) REFERENCES inspection_paths(id) ON DELETE CASCADE,
    FOREIGN KEY (zone_id) REFERENCES zones(id),
    FOREIGN KEY (camera_id) REFERENCES cameras(id),
    
    INDEX idx_path_waypoints_path_order (path_id, waypoint_order),
    INDEX idx_path_waypoints_zone (zone_id, waypoint_type),
    INDEX idx_path_waypoints_camera (camera_id, monitoring_required),
    INDEX idx_path_waypoints_performance (visit_count DESC, issue_frequency),
    UNIQUE KEY unique_path_waypoint_order (path_id, waypoint_order)
);
```

### **path_executions**
```sql
CREATE TABLE path_executions (
    id UUID PRIMARY KEY,
    path_id UUID NOT NULL,
    executor_id UUID NOT NULL,
    session_id UUID UNIQUE, -- Unique session identifier
    
    -- Execution timing
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    planned_duration_minutes INTEGER,
    actual_duration_minutes INTEGER,
    is_completed BOOLEAN DEFAULT FALSE,
    
    -- Execution details
    execution_type ENUM('scheduled', 'on_demand', 'emergency', 'training', 'audit') NOT NULL,
    execution_reason TEXT,
    weather_conditions TEXT,
    equipment_used JSON, -- Equipment/tools used during execution
    
    -- Progress tracking
    waypoints_visited INTEGER DEFAULT 0,
    waypoints_total INTEGER,
    completion_percentage DECIMAL(5,2) DEFAULT 0.00,
    current_waypoint_id UUID,
    
    -- Quality metrics
    quality_score DECIMAL(5,2) DEFAULT 0.00,
    issues_found INTEGER DEFAULT 0,
    photos_taken INTEGER DEFAULT 0,
    notes_count INTEGER DEFAULT 0,
    
    -- Performance indicators
    deviation_from_path DECIMAL(8,2) DEFAULT 0.00, -- Meters off path
    pause_time_minutes INTEGER DEFAULT 0,
    break_count INTEGER DEFAULT 0,
    interruption_count INTEGER DEFAULT 0,
    
    -- Status and outcome
    execution_status ENUM('in_progress', 'completed', 'paused', 'cancelled', 'failed') DEFAULT 'in_progress',
    cancellation_reason TEXT,
    supervisor_reviewed BOOLEAN DEFAULT FALSE,
    reviewed_by UUID,
    review_score DECIMAL(3,1), -- 1-10 supervisor rating
    
    -- Safety and compliance
    safety_incidents INTEGER DEFAULT 0,
    ppe_violations INTEGER DEFAULT 0,
    compliance_score DECIMAL(5,2) DEFAULT 100.00,
    safety_notes TEXT,
    
    -- GPS and tracking
    gps_tracking_enabled BOOLEAN DEFAULT TRUE,
    gps_accuracy_avg DECIMAL(8,2), -- Average GPS accuracy in meters
    distance_traveled DECIMAL(10,2), -- Actual distance traveled
    route_deviation_score DECIMAL(5,2), -- How closely route was followed
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (path_id) REFERENCES inspection_paths(id),
    FOREIGN KEY (executor_id) REFERENCES users(id),
    FOREIGN KEY (current_waypoint_id) REFERENCES path_waypoints(id),
    FOREIGN KEY (reviewed_by) REFERENCES users(id),
    
    INDEX idx_path_executions_path_time (path_id, started_at DESC),
    INDEX idx_path_executions_executor (executor_id, execution_status, started_at DESC),
    INDEX idx_path_executions_status (execution_status, started_at DESC),
    INDEX idx_path_executions_quality (quality_score DESC, compliance_score DESC),
    INDEX idx_path_executions_session (session_id, execution_status)
);
```

### **path_execution_waypoints**
```sql
CREATE TABLE path_execution_waypoints (
    id UUID PRIMARY KEY,
    execution_id UUID NOT NULL,
    waypoint_id UUID NOT NULL,
    
    -- Visit details
    visited_at TIMESTAMP,
    departure_at TIMESTAMP,
    time_spent_minutes DECIMAL(5,2),
    is_skipped BOOLEAN DEFAULT FALSE,
    skip_reason TEXT,
    
    -- Location verification
    actual_coordinates_x DECIMAL(10,6),
    actual_coordinates_y DECIMAL(10,6),
    gps_accuracy DECIMAL(8,2),
    location_verified BOOLEAN DEFAULT FALSE,
    distance_from_waypoint DECIMAL(8,2), -- Distance from intended waypoint
    
    -- Inspection results
    inspection_completed BOOLEAN DEFAULT FALSE,
    inspection_score DECIMAL(5,2),
    issues_found INTEGER DEFAULT 0,
    photos_taken INTEGER DEFAULT 0,
    notes TEXT,
    
    -- Compliance and safety
    ppe_compliance BOOLEAN DEFAULT TRUE,
    safety_protocol_followed BOOLEAN DEFAULT TRUE,
    environmental_conditions TEXT,
    
    -- Media evidence
    photo_urls JSON, -- Array of photo URLs
    video_urls JSON, -- Array of video URLs
    document_urls JSON, -- Array of document URLs
    
    -- Quality metrics
    inspector_confidence DECIMAL(5,2), -- Confidence in inspection quality
    requires_follow_up BOOLEAN DEFAULT FALSE,
    follow_up_notes TEXT,
    priority_level ENUM('low', 'medium', 'high', 'urgent'),
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (execution_id) REFERENCES path_executions(id) ON DELETE CASCADE,
    FOREIGN KEY (waypoint_id) REFERENCES path_waypoints(id),
    
    INDEX idx_execution_waypoints_execution (execution_id, visited_at DESC),
    INDEX idx_execution_waypoints_waypoint (waypoint_id, visited_at DESC),
    INDEX idx_execution_waypoints_issues (issues_found DESC, requires_follow_up),
    INDEX idx_execution_waypoints_compliance (ppe_compliance, safety_protocol_followed),
    UNIQUE KEY unique_execution_waypoint (execution_id, waypoint_id)
);
```

### **path_templates**
```sql
CREATE TABLE path_templates (
    id UUID PRIMARY KEY,
    template_name VARCHAR(255) NOT NULL,
    description TEXT,
    template_type ENUM('inspection', 'maintenance', 'emergency', 'quality', 'tour', 'custom') NOT NULL,
    
    -- Template configuration
    base_waypoint_count INTEGER,
    estimated_duration_minutes INTEGER,
    recommended_zones JSON, -- Suggested zone types
    required_equipment JSON, -- Standard equipment list
    
    -- Template characteristics
    difficulty_level ENUM('basic', 'intermediate', 'advanced', 'expert') DEFAULT 'basic',
    skill_requirements JSON, -- Required skills/certifications
    safety_level ENUM('low', 'medium', 'high', 'critical') DEFAULT 'medium',
    
    -- Usage and popularity
    usage_count INTEGER DEFAULT 0,
    success_rate DECIMAL(5,2) DEFAULT 0.00,
    user_rating DECIMAL(3,1) DEFAULT 0.0,
    rating_count INTEGER DEFAULT 0,
    
    -- Template structure
    waypoint_template JSON, -- Default waypoint configuration
    inspection_checklist JSON, -- Standard checklist items
    customizable_fields JSON, -- Fields that can be modified
    
    -- Access and permissions
    is_public BOOLEAN DEFAULT TRUE,
    created_by UUID NOT NULL,
    organization_specific BOOLEAN DEFAULT FALSE,
    industry_category VARCHAR(100),
    
    -- Versioning
    version VARCHAR(20) DEFAULT '1.0',
    parent_template_id UUID, -- Reference to parent template
    is_active BOOLEAN DEFAULT TRUE,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deprecated_at TIMESTAMP,
    
    FOREIGN KEY (created_by) REFERENCES users(id),
    FOREIGN KEY (parent_template_id) REFERENCES path_templates(id),
    
    INDEX idx_path_templates_type (template_type, is_active),
    INDEX idx_path_templates_popularity (usage_count DESC, user_rating DESC),
    INDEX idx_path_templates_difficulty (difficulty_level, safety_level),
    FULLTEXT INDEX idx_path_templates_search (template_name, description)
);
```

---

## 🏢 **ADMIN DASHBOARD & SYSTEM MANAGEMENT**

### **admin_dashboard_metrics**
```sql
CREATE TABLE admin_dashboard_metrics (
    id UUID PRIMARY KEY,
    metric_date DATE NOT NULL,
    metric_hour INTEGER, -- 0-23 for hourly granularity
    aggregation_level ENUM('hourly', 'daily', 'weekly', 'monthly') NOT NULL,
    
    -- System-wide metrics
    total_users INTEGER DEFAULT 0,
    active_users_24h INTEGER DEFAULT 0,
    total_sites INTEGER DEFAULT 0,
    active_sites INTEGER DEFAULT 0,
    total_cameras INTEGER DEFAULT 0,
    online_cameras INTEGER DEFAULT 0,
    
    -- Performance metrics
    system_uptime_percentage DECIMAL(5,2) DEFAULT 100.00,
    avg_response_time_ms INTEGER DEFAULT 0,
    total_api_calls BIGINT DEFAULT 0,
    data_processed_gb DECIMAL(10,2) DEFAULT 0.00,
    
    -- Alert metrics
    total_alerts_generated INTEGER DEFAULT 0,
    alerts_resolved INTEGER DEFAULT 0,
    alerts_pending INTEGER DEFAULT 0,
    avg_resolution_time_minutes INTEGER DEFAULT 0,
    
    -- Safety and compliance
    overall_safety_score DECIMAL(5,2) DEFAULT 100.00,
    ppe_compliance_rate DECIMAL(5,2) DEFAULT 100.00,
    incident_count INTEGER DEFAULT 0,
    near_miss_count INTEGER DEFAULT 0,
    
    -- AI and detection metrics
    ai_model_accuracy_avg DECIMAL(5,2) DEFAULT 0.00,
    total_detections BIGINT DEFAULT 0,
    detection_accuracy_rate DECIMAL(5,2) DEFAULT 0.00,
    false_positive_rate DECIMAL(5,2) DEFAULT 0.00,
    
    -- Resource utilization
    cpu_usage_avg DECIMAL(5,2) DEFAULT 0.00,
    memory_usage_avg DECIMAL(5,2) DEFAULT 0.00,
    disk_usage_avg DECIMAL(5,2) DEFAULT 0.00,
    network_utilization_avg DECIMAL(5,2) DEFAULT 0.00,
    database_performance_score DECIMAL(5,2) DEFAULT 100.00,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    calculated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_admin_metrics_date (metric_date DESC, aggregation_level),
    INDEX idx_admin_metrics_performance (system_uptime_percentage, avg_response_time_ms),
    INDEX idx_admin_metrics_safety (overall_safety_score, ppe_compliance_rate),
    UNIQUE KEY unique_metric_period (metric_date, metric_hour, aggregation_level)
);
```

### **site_performance_summary**
```sql
CREATE TABLE site_performance_summary (
    id UUID PRIMARY KEY,
    site_id UUID NOT NULL,
    summary_date DATE NOT NULL,
    summary_period ENUM('daily', 'weekly', 'monthly') NOT NULL,
    
    -- Site operations
    personnel_count INTEGER DEFAULT 0,
    active_personnel INTEGER DEFAULT 0,
    camera_count INTEGER DEFAULT 0,
    online_cameras INTEGER DEFAULT 0,
    
    -- Performance indicators
    site_uptime_percentage DECIMAL(5,2) DEFAULT 100.00,
    ai_accuracy_percentage DECIMAL(5,2) DEFAULT 0.00,
    safety_score DECIMAL(5,2) DEFAULT 100.00,
    compliance_score DECIMAL(5,2) DEFAULT 100.00,
    
    -- Alert statistics
    alerts_generated INTEGER DEFAULT 0,
    alerts_resolved INTEGER DEFAULT 0,
    critical_alerts INTEGER DEFAULT 0,
    avg_alert_resolution_minutes INTEGER DEFAULT 0,
    
    -- Activity metrics
    total_detections INTEGER DEFAULT 0,
    ppe_violations INTEGER DEFAULT 0,
    safety_incidents INTEGER DEFAULT 0,
    equipment_issues INTEGER DEFAULT 0,
    
    -- Resource usage
    data_storage_usage_gb DECIMAL(10,2) DEFAULT 0.00,
    bandwidth_usage_gb DECIMAL(10,2) DEFAULT 0.00,
    processing_time_hours DECIMAL(8,2) DEFAULT 0.00,
    
    -- Quality metrics
    inspection_completion_rate DECIMAL(5,2) DEFAULT 100.00,
    maintenance_completion_rate DECIMAL(5,2) DEFAULT 100.00,
    documentation_completeness DECIMAL(5,2) DEFAULT 100.00,
    
    -- Trend indicators
    performance_trend ENUM('improving', 'stable', 'declining', 'volatile') DEFAULT 'stable',
    safety_trend ENUM('improving', 'stable', 'declining') DEFAULT 'stable',
    efficiency_score DECIMAL(5,2) DEFAULT 100.00,
    
    -- Metadata
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    calculated_by VARCHAR(100), -- System or admin user ID
    notes TEXT,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (site_id) REFERENCES sites(id),
    
    INDEX idx_site_performance_site_date (site_id, summary_date DESC),
    INDEX idx_site_performance_period (summary_period, summary_date DESC),
    INDEX idx_site_performance_scores (safety_score DESC, efficiency_score DESC),
    UNIQUE KEY unique_site_summary (site_id, summary_date, summary_period)
);
```

### **system_health_logs**
```sql
CREATE TABLE system_health_logs (
    id UUID PRIMARY KEY,
    server_id VARCHAR(100) NOT NULL, -- Server/service identifier
    component_type ENUM('cpu', 'memory', 'disk', 'network', 'database', 'ai_service', 'web_service') NOT NULL,
    measurement_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Resource metrics
    cpu_usage_percentage DECIMAL(5,2),
    memory_usage_percentage DECIMAL(5,2),
    disk_usage_percentage DECIMAL(5,2),
    network_usage_percentage DECIMAL(5,2),
    
    -- Performance metrics
    response_time_ms INTEGER,
    throughput_ops_per_second INTEGER,
    error_rate_percentage DECIMAL(5,2),
    uptime_percentage DECIMAL(5,2),
    
    -- Database specific metrics
    db_connection_count INTEGER,
    db_query_time_avg_ms INTEGER,
    db_slow_queries_count INTEGER,
    db_deadlock_count INTEGER DEFAULT 0,
    
    -- AI service metrics
    model_inference_time_ms INTEGER,
    model_accuracy_score DECIMAL(5,2),
    queue_size INTEGER,
    processing_backlog INTEGER,
    
    -- Service health
    service_status ENUM('healthy', 'degraded', 'unhealthy', 'offline') DEFAULT 'healthy',
    alert_threshold_exceeded BOOLEAN DEFAULT FALSE,
    requires_attention BOOLEAN DEFAULT FALSE,
    maintenance_required BOOLEAN DEFAULT FALSE,
    
    -- Error tracking
    error_count INTEGER DEFAULT 0,
    warning_count INTEGER DEFAULT 0,
    last_error_message TEXT,
    last_error_timestamp TIMESTAMP,
    
    -- Metadata
    monitoring_source VARCHAR(100), -- Source of monitoring data
    tags JSON, -- Additional metadata tags
    raw_metrics JSON, -- Complete metrics dump
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_system_health_server_time (server_id, measurement_timestamp DESC),
    INDEX idx_system_health_component (component_type, service_status),
    INDEX idx_system_health_status (service_status, requires_attention),
    INDEX idx_system_health_performance (response_time_ms, error_rate_percentage)
);
```

### **admin_activity_log**
```sql
CREATE TABLE admin_activity_log (
    id UUID PRIMARY KEY,
    admin_user_id UUID NOT NULL,
    activity_type ENUM('user_management', 'site_configuration', 'system_settings', 'alert_management', 'report_generation', 'data_export', 'security_action', 'maintenance') NOT NULL,
    action VARCHAR(255) NOT NULL, -- Specific action performed
    
    -- Activity details
    resource_type VARCHAR(100), -- Type of resource affected
    resource_id UUID, -- ID of affected resource
    resource_name VARCHAR(255), -- Human-readable name
    
    -- Change tracking
    old_values JSON, -- Previous values (for updates)
    new_values JSON, -- New values (for updates)
    change_summary TEXT, -- Human-readable change description
    
    -- Context information
    site_id UUID, -- Site context if applicable
    ip_address INET NOT NULL,
    user_agent TEXT,
    session_id VARCHAR(255),
    
    -- Impact assessment
    impact_level ENUM('low', 'medium', 'high', 'critical') DEFAULT 'medium',
    affected_users_count INTEGER DEFAULT 0,
    affected_sites_count INTEGER DEFAULT 0,
    system_wide_impact BOOLEAN DEFAULT FALSE,
    
    -- Approval and review
    requires_approval BOOLEAN DEFAULT FALSE,
    approved_by UUID, -- Reference to approving admin
    approved_at TIMESTAMP,
    approval_notes TEXT,
    
    -- Status and outcome
    action_status ENUM('pending', 'completed', 'failed', 'rolled_back') DEFAULT 'completed',
    error_message TEXT, -- If action failed
    rollback_possible BOOLEAN DEFAULT TRUE,
    
    -- Compliance and audit
    compliance_category VARCHAR(100), -- Compliance framework category
    audit_trail_required BOOLEAN DEFAULT TRUE,
    retention_period_days INTEGER DEFAULT 2555, -- 7 years default
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (admin_user_id) REFERENCES users(id),
    FOREIGN KEY (site_id) REFERENCES sites(id),
    FOREIGN KEY (approved_by) REFERENCES users(id),
    
    INDEX idx_admin_activity_user_time (admin_user_id, created_at DESC),
    INDEX idx_admin_activity_type (activity_type, action_status),
    INDEX idx_admin_activity_impact (impact_level, system_wide_impact),
    INDEX idx_admin_activity_resource (resource_type, resource_id),
    INDEX idx_admin_activity_approval (requires_approval, approved_by)
);
```

### **executive_reports**
```sql
CREATE TABLE executive_reports (
    id UUID PRIMARY KEY,
    report_name VARCHAR(255) NOT NULL,
    report_type ENUM('performance_summary', 'safety_audit', 'financial_overview', 'resource_utilization', 'compliance_report', 'executive_dashboard') NOT NULL,
    reporting_period_start DATE NOT NULL,
    reporting_period_end DATE NOT NULL,
    
    -- Report generation
    generated_by UUID NOT NULL,
    generation_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    generation_duration_seconds INTEGER,
    report_status ENUM('generating', 'completed', 'failed', 'archived') DEFAULT 'generating',
    
    -- Report content
    executive_summary TEXT,
    key_metrics JSON, -- Key performance indicators
    trend_analysis JSON, -- Trend data and insights
    recommendations JSON, -- Action items and recommendations
    risk_assessment JSON, -- Risk factors and mitigation strategies
    
    -- Data sources
    included_sites JSON, -- Array of site IDs included
    data_quality_score DECIMAL(5,2) DEFAULT 100.00,
    data_completeness_percentage DECIMAL(5,2) DEFAULT 100.00,
    data_sources JSON, -- List of data sources used
    
    -- Distribution and access
    recipient_list JSON, -- Array of user IDs who should receive report
    confidentiality_level ENUM('public', 'internal', 'confidential', 'restricted') DEFAULT 'internal',
    access_permissions JSON, -- Detailed access control
    
    -- File information
    report_file_path VARCHAR(500),
    report_file_format ENUM('pdf', 'excel', 'powerpoint', 'html', 'json') DEFAULT 'pdf',
    report_file_size_mb DECIMAL(10,2),
    
    -- Versioning and history
    version VARCHAR(20) DEFAULT '1.0',
    previous_report_id UUID, -- Reference to previous version
    is_latest_version BOOLEAN DEFAULT TRUE,
    
    -- Scheduling and automation
    is_automated BOOLEAN DEFAULT FALSE,
    next_generation_date DATE,
    automation_schedule VARCHAR(100), -- Cron expression
    
    -- Performance metrics
    view_count INTEGER DEFAULT 0,
    download_count INTEGER DEFAULT 0,
    last_accessed TIMESTAMP,
    user_feedback_score DECIMAL(3,1), -- 1-10 rating
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    archived_at TIMESTAMP,
    
    FOREIGN KEY (generated_by) REFERENCES users(id),
    FOREIGN KEY (previous_report_id) REFERENCES executive_reports(id),
    
    INDEX idx_executive_reports_type_period (report_type, reporting_period_end DESC),
    INDEX idx_executive_reports_generator (generated_by, generation_timestamp DESC),
    INDEX idx_executive_reports_status (report_status, is_latest_version),
    INDEX idx_executive_reports_automation (is_automated, next_generation_date),
    FULLTEXT INDEX idx_executive_reports_search (report_name, executive_summary)
);
```

---

## 👥 **USER MANAGEMENT & ADMINISTRATION**

### **user_management_profiles**
```sql
CREATE TABLE user_management_profiles (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL UNIQUE,
    
    -- Extended profile information
    employee_number VARCHAR(50) UNIQUE,
    badge_number VARCHAR(50) UNIQUE,
    social_security_number VARCHAR(20), -- Encrypted
    date_of_birth DATE,
    gender ENUM('male', 'female', 'other', 'prefer_not_to_say'),
    nationality VARCHAR(100),
    
    -- Address and contact
    home_address TEXT,
    home_city VARCHAR(100),
    home_state VARCHAR(100),
    home_zip_code VARCHAR(20),
    home_country VARCHAR(100),
    emergency_contact_name VARCHAR(255),
    emergency_contact_phone VARCHAR(20),
    emergency_contact_relationship VARCHAR(100),
    
    -- Professional details
    position_title VARCHAR(255),
    position_level ENUM('entry', 'junior', 'mid', 'senior', 'lead', 'supervisor', 'manager', 'director', 'executive'),
    pay_grade VARCHAR(50),
    reports_to_user_id UUID,
    direct_reports_count INTEGER DEFAULT 0,
    
    -- Employment information
    employment_type ENUM('full_time', 'part_time', 'contract', 'temporary', 'consultant', 'intern'),
    employment_status ENUM('active', 'on_leave', 'terminated', 'retired', 'suspended'),
    start_date DATE NOT NULL,
    end_date DATE,
    probation_end_date DATE,
    performance_review_due DATE,
    
    -- Skills and qualifications
    skills JSON,
    qualifications JSON,
    languages JSON,
    special_certifications JSON,
    
    -- Preferences and settings
    notification_preferences JSON,
    ui_theme VARCHAR(50) DEFAULT 'default',
    timezone VARCHAR(100),
    language_preference VARCHAR(10) DEFAULT 'en',
    
    -- Privacy and compliance
    privacy_settings JSON,
    gdpr_consent BOOLEAN DEFAULT FALSE,
    marketing_consent BOOLEAN DEFAULT FALSE,
    data_retention_consent BOOLEAN DEFAULT TRUE,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (reports_to_user_id) REFERENCES users(id),
    
    INDEX idx_user_profiles_employee (employee_number, badge_number),
    INDEX idx_user_profiles_position (position_level, employment_status),
    INDEX idx_user_profiles_dates (start_date, end_date)
);
```

### **user_role_assignments**
```sql
CREATE TABLE user_role_assignments (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL,
    role_type ENUM('system_role', 'site_role', 'department_role', 'project_role', 'temporary_role'),
    role_name VARCHAR(255) NOT NULL,
    role_description TEXT,
    
    -- Assignment scope
    site_id UUID,
    department_id UUID,
    project_id UUID,
    
    -- Permission details
    permissions JSON,
    access_level ENUM('read', 'write', 'admin', 'super_admin') DEFAULT 'read',
    resource_restrictions JSON,
    time_restrictions JSON,
    
    -- Assignment metadata
    assigned_by UUID NOT NULL,
    assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    effective_from DATE NOT NULL,
    effective_until DATE,
    is_primary_role BOOLEAN DEFAULT FALSE,
    
    -- Approval workflow
    requires_approval BOOLEAN DEFAULT FALSE,
    approved_by UUID,
    approved_at TIMESTAMP,
    approval_notes TEXT,
    
    -- Status and monitoring
    assignment_status ENUM('pending', 'active', 'suspended', 'expired', 'revoked') DEFAULT 'pending',
    last_used TIMESTAMP,
    usage_count INTEGER DEFAULT 0,
    
    -- Audit trail
    revoked_by UUID,
    revoked_at TIMESTAMP,
    revocation_reason TEXT,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (site_id) REFERENCES sites(id),
    FOREIGN KEY (assigned_by) REFERENCES users(id),
    FOREIGN KEY (approved_by) REFERENCES users(id),
    FOREIGN KEY (revoked_by) REFERENCES users(id),
    
    INDEX idx_role_assignments_user (user_id, assignment_status),
    INDEX idx_role_assignments_role (role_type, role_name),
    INDEX idx_role_assignments_scope (site_id, department_id),
    INDEX idx_role_assignments_effective (effective_from, effective_until)
);
```

### **user_session_management**
```sql
CREATE TABLE user_session_management (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL,
    session_id VARCHAR(255) UNIQUE NOT NULL,
    session_token VARCHAR(512) UNIQUE NOT NULL,
    
    -- Session details
    login_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    logout_timestamp TIMESTAMP,
    last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    session_duration_seconds INTEGER,
    is_active BOOLEAN DEFAULT TRUE,
    
    -- Client information
    ip_address INET NOT NULL,
    user_agent TEXT,
    browser_info JSON,
    device_info JSON,
    operating_system VARCHAR(100),
    
    -- Location and access
    login_location POINT,
    access_method ENUM('web', 'mobile_app', 'api', 'sso', 'ldap') DEFAULT 'web',
    authentication_method ENUM('password', 'sso', 'mfa', 'biometric', 'certificate') DEFAULT 'password',
    
    -- Security context
    mfa_verified BOOLEAN DEFAULT FALSE,
    risk_score DECIMAL(3,1),
    suspicious_activity BOOLEAN DEFAULT FALSE,
    concurrent_sessions INTEGER DEFAULT 1,
    
    -- Session management
    force_logout BOOLEAN DEFAULT FALSE,
    session_timeout_minutes INTEGER DEFAULT 480,
    remember_me BOOLEAN DEFAULT FALSE,
    auto_logout_at TIMESTAMP,
    
    -- Activity tracking
    page_views INTEGER DEFAULT 0,
    api_calls INTEGER DEFAULT 0,
    downloads INTEGER DEFAULT 0,
    uploads INTEGER DEFAULT 0,
    
    -- Compliance and audit
    compliance_acknowledgment BOOLEAN DEFAULT FALSE,
    terms_accepted_version VARCHAR(20),
    privacy_policy_accepted BOOLEAN DEFAULT FALSE,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id),
    
    INDEX idx_sessions_user_active (user_id, is_active, last_activity),
    INDEX idx_sessions_token (session_token, is_active),
    INDEX idx_sessions_security (risk_score, suspicious_activity),
    INDEX idx_sessions_cleanup (is_active, auto_logout_at)
);
```

### **user_activity_tracking**
```sql
CREATE TABLE user_activity_tracking (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL,
    session_id UUID NOT NULL,
    
    -- Activity details
    activity_type ENUM('login', 'logout', 'page_view', 'api_call', 'data_access', 'configuration_change', 'user_management', 'report_generation', 'alert_action') NOT NULL,
    activity_description TEXT NOT NULL,
    activity_category VARCHAR(100),
    
    -- Context information
    resource_type VARCHAR(100),
    resource_id UUID,
    resource_name VARCHAR(255),
    site_id UUID,
    
    -- Request details
    request_method VARCHAR(10),
    request_url TEXT,
    request_payload JSON,
    response_status INTEGER,
    response_time_ms INTEGER,
    
    -- Geolocation and timing
    activity_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    location_coordinates POINT,
    location_accuracy DECIMAL(8,2),
    timezone_offset INTEGER,
    
    -- Security and compliance
    security_level ENUM('public', 'internal', 'confidential', 'restricted') DEFAULT 'internal',
    data_classification VARCHAR(100),
    requires_audit BOOLEAN DEFAULT TRUE,
    compliance_tags JSON,
    
    -- Performance metrics
    processing_time_ms INTEGER,
    database_queries INTEGER DEFAULT 0,
    cache_hits INTEGER DEFAULT 0,
    errors_count INTEGER DEFAULT 0,
    
    -- User behavior analysis
    is_automated BOOLEAN DEFAULT FALSE,
    pattern_anomaly BOOLEAN DEFAULT FALSE,
    risk_indicator DECIMAL(3,1),
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (session_id) REFERENCES user_session_management(id),
    FOREIGN KEY (site_id) REFERENCES sites(id),
    
    INDEX idx_activity_user_time (user_id, activity_timestamp DESC),
    INDEX idx_activity_type (activity_type, activity_category),
    INDEX idx_activity_security (security_level, requires_audit),
    INDEX idx_activity_performance (response_time_ms, processing_time_ms)
);
```

### **user_permissions_matrix**
```sql
CREATE TABLE user_permissions_matrix (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL,
    permission_category VARCHAR(100) NOT NULL,
    permission_name VARCHAR(255) NOT NULL,
    
    -- Permission scope
    scope_type ENUM('global', 'site', 'department', 'project', 'resource') NOT NULL,
    scope_id UUID,
    scope_name VARCHAR(255),
    
    -- Access details
    access_level ENUM('none', 'read', 'write', 'admin', 'owner') NOT NULL,
    can_delegate BOOLEAN DEFAULT FALSE,
    can_revoke BOOLEAN DEFAULT FALSE,
    
    -- Conditions and restrictions
    conditions JSON,
    time_restrictions JSON,
    location_restrictions JSON,
    device_restrictions JSON,
    
    -- Grant information
    granted_by UUID NOT NULL,
    granted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    granted_reason TEXT,
    approval_required BOOLEAN DEFAULT FALSE,
    approved_by UUID,
    
    -- Status and lifecycle
    status ENUM('pending', 'active', 'suspended', 'expired', 'revoked') DEFAULT 'pending',
    effective_from TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    effective_until TIMESTAMP,
    auto_renewal BOOLEAN DEFAULT FALSE,
    renewal_period_days INTEGER,
    
    -- Usage tracking
    first_used TIMESTAMP,
    last_used TIMESTAMP,
    usage_count INTEGER DEFAULT 0,
    abuse_reports INTEGER DEFAULT 0,
    
    -- Audit and compliance
    audit_required BOOLEAN DEFAULT TRUE,
    compliance_notes TEXT,
    last_reviewed DATE,
    next_review_due DATE,
    reviewer_user_id UUID,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (granted_by) REFERENCES users(id),
    FOREIGN KEY (approved_by) REFERENCES users(id),
    FOREIGN KEY (reviewer_user_id) REFERENCES users(id),
    
    INDEX idx_permissions_user_category (user_id, permission_category),
    INDEX idx_permissions_scope (scope_type, scope_id),
    INDEX idx_permissions_status (status, effective_until),
    INDEX idx_permissions_review (next_review_due, audit_required),
    UNIQUE KEY unique_user_permission_scope (user_id, permission_category, permission_name, scope_type, scope_id)
);
```

---

## 🏗️ **SITE CONFIGURATION & INFRASTRUCTURE**

### **site_configurations**
```sql
CREATE TABLE site_configurations (
    id UUID PRIMARY KEY,
    site_id UUID NOT NULL UNIQUE,
    
    -- Basic configuration
    timezone VARCHAR(100) DEFAULT 'America/New_York',
    working_hours_start TIME DEFAULT '06:00',
    working_hours_end TIME DEFAULT '18:00',
    max_occupancy INTEGER DEFAULT 100,
    safety_level ENUM('standard', 'high', 'critical') DEFAULT 'standard',
    
    -- AI and detection settings
    ai_detection_enabled BOOLEAN DEFAULT TRUE,
    ai_sensitivity_level ENUM('low', 'medium', 'high') DEFAULT 'medium',
    detection_zones JSON,
    detection_models JSON,
    real_time_analysis BOOLEAN DEFAULT TRUE,
    
    -- Recording and storage
    recording_retention_days INTEGER DEFAULT 30,
    recording_quality ENUM('low', 'medium', 'high', 'ultra') DEFAULT 'high',
    recording_schedule JSON,
    storage_location VARCHAR(255),
    backup_retention_days INTEGER DEFAULT 90,
    
    -- Alert and notification settings
    alert_notifications_enabled BOOLEAN DEFAULT TRUE,
    notification_methods JSON,
    alert_escalation_rules JSON,
    notification_recipients JSON,
    
    -- Emergency contacts and procedures
    emergency_contacts JSON,
    emergency_procedures JSON,
    evacuation_plan_url VARCHAR(500),
    safety_protocols JSON,
    
    -- Access control settings
    access_control_type ENUM('manual', 'keycard', 'biometric', 'mobile') DEFAULT 'keycard',
    visitor_management BOOLEAN DEFAULT TRUE,
    contractor_access_rules JSON,
    multi_factor_auth_required BOOLEAN DEFAULT FALSE,
    
    -- Integration settings
    weather_monitoring BOOLEAN DEFAULT FALSE,
    environmental_sensors JSON,
    third_party_integrations JSON,
    api_access_tokens JSON,
    
    -- Performance and maintenance
    system_health_threshold INTEGER DEFAULT 85,
    maintenance_schedule JSON,
    performance_monitoring BOOLEAN DEFAULT TRUE,
    automated_diagnostics BOOLEAN DEFAULT TRUE,
    
    -- Compliance and regulations
    compliance_frameworks JSON,
    audit_frequency ENUM('weekly', 'monthly', 'quarterly', 'annually') DEFAULT 'monthly',
    documentation_requirements JSON,
    regulatory_contacts JSON,
    
    -- Custom configurations
    custom_fields JSON,
    feature_flags JSON,
    integration_endpoints JSON,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    configured_by UUID NOT NULL,
    last_modified_by UUID NOT NULL,
    
    FOREIGN KEY (site_id) REFERENCES sites(id),
    FOREIGN KEY (configured_by) REFERENCES users(id),
    FOREIGN KEY (last_modified_by) REFERENCES users(id),
    
    INDEX idx_site_configs_safety (safety_level, ai_detection_enabled),
    INDEX idx_site_configs_compliance (compliance_frameworks, audit_frequency),
    INDEX idx_site_configs_performance (system_health_threshold, performance_monitoring)
);
```

### **site_infrastructure**
```sql
CREATE TABLE site_infrastructure (
    id UUID PRIMARY KEY,
    site_id UUID NOT NULL UNIQUE,
    
    -- Network infrastructure
    network_status ENUM('excellent', 'good', 'fair', 'poor', 'offline') DEFAULT 'fair',
    internet_speed_mbps INTEGER,
    network_provider VARCHAR(255),
    ip_range VARCHAR(50),
    wifi_networks JSON,
    network_monitoring BOOLEAN DEFAULT TRUE,
    
    -- Power infrastructure
    power_status ENUM('stable', 'unstable', 'backup_active', 'critical', 'offline') DEFAULT 'stable',
    main_power_source VARCHAR(255),
    backup_power_available BOOLEAN DEFAULT FALSE,
    backup_power_capacity_hours INTEGER,
    ups_systems JSON,
    power_consumption_kw DECIMAL(8,2),
    
    -- Environmental systems
    weather_station_installed BOOLEAN DEFAULT FALSE,
    environmental_sensors JSON,
    hvac_systems JSON,
    lighting_systems JSON,
    security_systems JSON,
    
    -- Communication systems
    radio_communication BOOLEAN DEFAULT FALSE,
    intercom_systems JSON,
    emergency_communication JSON,
    cellular_coverage ENUM('excellent', 'good', 'fair', 'poor', 'none') DEFAULT 'good',
    
    -- Storage and computing
    local_servers JSON,
    storage_capacity_tb DECIMAL(8,2),
    cloud_storage_enabled BOOLEAN DEFAULT TRUE,
    computing_resources JSON,
    data_backup_systems JSON,
    
    -- Maintenance tracking
    last_infrastructure_audit DATE,
    next_infrastructure_audit DATE,
    maintenance_contracts JSON,
    equipment_warranties JSON,
    upgrade_schedule JSON,
    
    -- Performance metrics
    uptime_percentage DECIMAL(5,2) DEFAULT 100.00,
    average_response_time_ms INTEGER,
    network_utilization_percentage DECIMAL(5,2),
    storage_utilization_percentage DECIMAL(5,2),
    system_temperature_celsius DECIMAL(4,1),
    
    -- Compliance and certifications
    infrastructure_certifications JSON,
    inspection_records JSON,
    regulatory_compliance JSON,
    insurance_information JSON,
    
    -- Integration points
    camera_network_config JSON,
    sensor_network_config JSON,
    third_party_connections JSON,
    api_endpoints JSON,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    last_audit_by UUID,
    
    FOREIGN KEY (site_id) REFERENCES sites(id),
    FOREIGN KEY (last_audit_by) REFERENCES users(id),
    
    INDEX idx_site_infrastructure_status (network_status, power_status),
    INDEX idx_site_infrastructure_performance (uptime_percentage, average_response_time_ms),
    INDEX idx_site_infrastructure_audit (next_infrastructure_audit, last_audit_by)
);
```

### **site_zone_configurations**
```sql
CREATE TABLE site_zone_configurations (
    id UUID PRIMARY KEY,
    site_id UUID NOT NULL,
    zone_id UUID NOT NULL,
    
    -- Zone-specific settings
    zone_configuration JSON,
    access_restrictions JSON,
    safety_requirements JSON,
    monitoring_level ENUM('basic', 'standard', 'enhanced', 'maximum') DEFAULT 'standard',
    
    -- Camera assignments
    assigned_cameras JSON,
    camera_coverage_percentage DECIMAL(5,2) DEFAULT 0.00,
    blind_spots JSON,
    camera_positioning_optimal BOOLEAN DEFAULT FALSE,
    
    -- Personnel settings
    max_personnel INTEGER,
    authorized_roles JSON,
    restricted_hours JSON,
    ppe_requirements JSON,
    
    -- Environmental settings
    environmental_hazards JSON,
    weather_restrictions JSON,
    emergency_procedures JSON,
    evacuation_routes JSON,
    
    -- AI and detection settings
    ai_detection_rules JSON,
    alert_thresholds JSON,
    detection_sensitivity ENUM('low', 'medium', 'high') DEFAULT 'medium',
    notification_overrides JSON,
    
    -- Performance tracking
    zone_utilization_percentage DECIMAL(5,2) DEFAULT 0.00,
    incident_frequency DECIMAL(8,2) DEFAULT 0.00,
    safety_score DECIMAL(5,2) DEFAULT 100.00,
    compliance_score DECIMAL(5,2) DEFAULT 100.00,
    
    -- Status and maintenance
    zone_status ENUM('active', 'maintenance', 'restricted', 'inactive') DEFAULT 'active',
    last_inspection DATE,
    next_inspection DATE,
    maintenance_notes TEXT,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    configured_by UUID NOT NULL,
    
    FOREIGN KEY (site_id) REFERENCES sites(id),
    FOREIGN KEY (zone_id) REFERENCES zones(id),
    FOREIGN KEY (configured_by) REFERENCES users(id),
    
    INDEX idx_zone_configs_site (site_id, zone_status),
    INDEX idx_zone_configs_performance (safety_score, compliance_score),
    INDEX idx_zone_configs_monitoring (monitoring_level, camera_coverage_percentage),
    UNIQUE KEY unique_site_zone_config (site_id, zone_id)
);
```

### **site_performance_tracking**
```sql
CREATE TABLE site_performance_tracking (
    id UUID PRIMARY KEY,
    site_id UUID NOT NULL,
    tracking_date DATE NOT NULL,
    tracking_period ENUM('hourly', 'daily', 'weekly', 'monthly') NOT NULL,
    
    -- System performance metrics
    system_health_score DECIMAL(5,2) DEFAULT 100.00,
    uptime_percentage DECIMAL(5,2) DEFAULT 100.00,
    response_time_avg_ms INTEGER DEFAULT 0,
    error_rate_percentage DECIMAL(5,2) DEFAULT 0.00,
    throughput_operations_per_hour INTEGER DEFAULT 0,
    
    -- Infrastructure performance
    network_performance_score DECIMAL(5,2) DEFAULT 100.00,
    power_stability_score DECIMAL(5,2) DEFAULT 100.00,
    storage_performance_score DECIMAL(5,2) DEFAULT 100.00,
    camera_system_score DECIMAL(5,2) DEFAULT 100.00,
    
    -- Operational metrics
    personnel_capacity_utilization DECIMAL(5,2) DEFAULT 0.00,
    zone_utilization_average DECIMAL(5,2) DEFAULT 0.00,
    safety_incident_count INTEGER DEFAULT 0,
    compliance_violation_count INTEGER DEFAULT 0,
    
    -- Alert and response metrics
    alerts_generated INTEGER DEFAULT 0,
    alerts_resolved INTEGER DEFAULT 0,
    average_response_time_minutes INTEGER DEFAULT 0,
    escalated_incidents INTEGER DEFAULT 0,
    
    -- AI and detection performance
    detection_accuracy_rate DECIMAL(5,2) DEFAULT 0.00,
    false_positive_rate DECIMAL(5,2) DEFAULT 0.00,
    ai_processing_time_avg_ms INTEGER DEFAULT 0,
    detection_coverage_percentage DECIMAL(5,2) DEFAULT 0.00,
    
    -- Resource utilization
    cpu_utilization_avg DECIMAL(5,2) DEFAULT 0.00,
    memory_utilization_avg DECIMAL(5,2) DEFAULT 0.00,
    storage_utilization_percentage DECIMAL(5,2) DEFAULT 0.00,
    bandwidth_utilization_percentage DECIMAL(5,2) DEFAULT 0.00,
    
    -- Compliance and quality metrics
    compliance_score DECIMAL(5,2) DEFAULT 100.00,
    audit_findings INTEGER DEFAULT 0,
    documentation_completeness DECIMAL(5,2) DEFAULT 100.00,
    training_compliance_rate DECIMAL(5,2) DEFAULT 100.00,
    
    -- Trend indicators
    performance_trend ENUM('improving', 'stable', 'declining', 'volatile') DEFAULT 'stable',
    health_trend ENUM('improving', 'stable', 'declining') DEFAULT 'stable',
    efficiency_trend ENUM('improving', 'stable', 'declining') DEFAULT 'stable',
    
    -- Comparison metrics
    site_ranking INTEGER,
    industry_benchmark_comparison DECIMAL(6,2),
    historical_performance_change DECIMAL(6,2),
    
    -- Notes and analysis
    performance_notes TEXT,
    improvement_recommendations JSON,
    issues_identified JSON,
    action_items JSON,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    calculated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    analyst_id UUID,
    
    FOREIGN KEY (site_id) REFERENCES sites(id),
    FOREIGN KEY (analyst_id) REFERENCES users(id),
    
    INDEX idx_site_performance_date (site_id, tracking_date DESC, tracking_period),
    INDEX idx_site_performance_scores (system_health_score DESC, compliance_score DESC),
    INDEX idx_site_performance_trends (performance_trend, health_trend),
    UNIQUE KEY unique_site_tracking_period (site_id, tracking_date, tracking_period)
);
```

### **site_compliance_tracking**
```sql
CREATE TABLE site_compliance_tracking (
    id UUID PRIMARY KEY,
    site_id UUID NOT NULL,
    compliance_framework VARCHAR(255) NOT NULL,
    compliance_date DATE NOT NULL,
    
    -- Compliance status
    overall_compliance_score DECIMAL(5,2) NOT NULL,
    compliance_status ENUM('compliant', 'minor_issues', 'major_issues', 'non_compliant') DEFAULT 'compliant',
    certification_valid BOOLEAN DEFAULT TRUE,
    certification_expiry_date DATE,
    
    -- Audit information
    audit_type ENUM('internal', 'external', 'regulatory', 'third_party') NOT NULL,
    auditor_name VARCHAR(255),
    auditor_organization VARCHAR(255),
    audit_date DATE NOT NULL,
    next_audit_date DATE,
    
    -- Findings and issues
    total_findings INTEGER DEFAULT 0,
    critical_findings INTEGER DEFAULT 0,
    major_findings INTEGER DEFAULT 0,
    minor_findings INTEGER DEFAULT 0,
    observations INTEGER DEFAULT 0,
    
    -- Compliance areas
    safety_compliance_score DECIMAL(5,2) DEFAULT 100.00,
    environmental_compliance_score DECIMAL(5,2) DEFAULT 100.00,
    quality_compliance_score DECIMAL(5,2) DEFAULT 100.00,
    security_compliance_score DECIMAL(5,2) DEFAULT 100.00,
    
    -- Documentation compliance
    documentation_completeness DECIMAL(5,2) DEFAULT 100.00,
    training_records_current BOOLEAN DEFAULT TRUE,
    procedure_documentation_current BOOLEAN DEFAULT TRUE,
    incident_reporting_compliant BOOLEAN DEFAULT TRUE,
    
    -- Corrective actions
    corrective_actions_required INTEGER DEFAULT 0,
    corrective_actions_completed INTEGER DEFAULT 0,
    corrective_actions_overdue INTEGER DEFAULT 0,
    preventive_actions_implemented INTEGER DEFAULT 0,
    
    -- Timeline tracking
    findings_resolved_days INTEGER,
    compliance_maintenance_effort_hours INTEGER,
    cost_of_compliance_usd DECIMAL(12,2),
    
    -- Regulatory requirements
    regulatory_updates_applied INTEGER DEFAULT 0,
    regulatory_notifications_pending INTEGER DEFAULT 0,
    license_renewals_due JSON,
    permit_status JSON,
    
    -- Risk assessment
    compliance_risk_score DECIMAL(5,2) DEFAULT 0.00,
    risk_mitigation_plans JSON,
    insurance_compliance BOOLEAN DEFAULT TRUE,
    legal_exposure_assessment TEXT,
    
    -- Performance tracking
    compliance_trend ENUM('improving', 'stable', 'declining') DEFAULT 'stable',
    benchmark_comparison DECIMAL(6,2),
    historical_compliance_change DECIMAL(6,2),
    
    -- Stakeholder information
    compliance_officer_id UUID,
    regulatory_contact_info JSON,
    consultant_information JSON,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    reported_by UUID NOT NULL,
    approved_by UUID,
    
    FOREIGN KEY (site_id) REFERENCES sites(id),
    FOREIGN KEY (compliance_officer_id) REFERENCES users(id),
    FOREIGN KEY (reported_by) REFERENCES users(id),
    FOREIGN KEY (approved_by) REFERENCES users(id),
    
    INDEX idx_compliance_site_framework (site_id, compliance_framework, compliance_date DESC),
    INDEX idx_compliance_status (compliance_status, certification_valid),
    INDEX idx_compliance_audit (audit_type, next_audit_date),
    INDEX idx_compliance_scores (overall_compliance_score DESC, safety_compliance_score DESC)
);
```

---

## 🧠 **AI MODEL MANAGEMENT & DEPLOYMENT**

### **ai_models**
```sql
CREATE TABLE ai_models (
    id UUID PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    model_type ENUM('object_detection', 'object_tracking', 'person_detection', 'behavior_analysis', 'defect_detection', 'classification', 'segmentation', 'custom') NOT NULL,
    category VARCHAR(255) NOT NULL,
    
    -- Version and metadata
    version VARCHAR(50) NOT NULL,
    description TEXT,
    framework VARCHAR(100),
    architecture VARCHAR(255),
    author VARCHAR(255),
    organization VARCHAR(255),
    
    -- Model files and storage
    model_file_path VARCHAR(500) NOT NULL,
    model_file_size_mb DECIMAL(10,2),
    config_file_path VARCHAR(500),
    weights_file_path VARCHAR(500),
    labels_file_path VARCHAR(500),
    documentation_url VARCHAR(500),
    
    -- Training information
    training_dataset_info JSON,
    training_images_count INTEGER,
    validation_images_count INTEGER,
    test_images_count INTEGER,
    training_duration_hours DECIMAL(8,2),
    training_completed_date TIMESTAMP,
    training_compute_cost DECIMAL(10,2),
    
    -- Model specifications
    input_resolution_width INTEGER,
    input_resolution_height INTEGER,
    input_channels INTEGER DEFAULT 3,
    output_classes JSON,
    batch_size_optimal INTEGER,
    batch_size_max INTEGER,
    memory_requirement_gb DECIMAL(8,2),
    
    -- Performance characteristics
    baseline_accuracy DECIMAL(5,2),
    baseline_precision DECIMAL(5,2),
    baseline_recall DECIMAL(5,2),
    baseline_f1_score DECIMAL(5,2),
    inference_time_ms DECIMAL(8,3),
    throughput_fps DECIMAL(8,2),
    confidence_threshold_default DECIMAL(3,2) DEFAULT 0.50,
    
    -- Deployment requirements
    min_gpu_memory_gb DECIMAL(6,2),
    recommended_gpu_models JSON,
    cpu_cores_required INTEGER,
    ram_requirement_gb DECIMAL(6,2),
    storage_requirement_gb DECIMAL(8,2),
    network_bandwidth_mbps INTEGER,
    
    -- Status and lifecycle
    status ENUM('development', 'training', 'testing', 'validation', 'approved', 'deprecated', 'archived') DEFAULT 'development',
    lifecycle_stage ENUM('experimental', 'beta', 'stable', 'mature', 'legacy') DEFAULT 'experimental',
    approval_status ENUM('pending', 'approved', 'rejected', 'requires_review') DEFAULT 'pending',
    approved_by UUID,
    approved_at TIMESTAMP,
    
    -- Licensing and compliance
    license_type VARCHAR(100),
    license_restrictions TEXT,
    compliance_certifications JSON,
    regulatory_approvals JSON,
    export_restrictions TEXT,
    intellectual_property_notes TEXT,
    
    -- Dependencies and compatibility
    dependency_requirements JSON,
    framework_version VARCHAR(50),
    python_version_min VARCHAR(20),
    cuda_version_required VARCHAR(20),
    compatibility_notes TEXT,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by UUID NOT NULL,
    last_modified_by UUID NOT NULL,
    
    FOREIGN KEY (approved_by) REFERENCES users(id),
    FOREIGN KEY (created_by) REFERENCES users(id),
    FOREIGN KEY (last_modified_by) REFERENCES users(id),
    
    INDEX idx_ai_models_type (model_type, category),
    INDEX idx_ai_models_status (status, lifecycle_stage),
    INDEX idx_ai_models_performance (baseline_accuracy DESC, inference_time_ms),
    INDEX idx_ai_models_approval (approval_status, approved_at),
    FULLTEXT INDEX idx_ai_models_search (name, description, category)
);
```

### **model_deployments**
```sql
CREATE TABLE model_deployments (
    id UUID PRIMARY KEY,
    model_id UUID NOT NULL,
    site_id UUID NOT NULL,
    deployment_name VARCHAR(255) NOT NULL,
    
    -- Deployment configuration
    deployment_status ENUM('pending', 'deploying', 'active', 'paused', 'failed', 'terminated') DEFAULT 'pending',
    deployment_type ENUM('production', 'staging', 'testing', 'canary', 'blue_green') DEFAULT 'production',
    deployment_strategy ENUM('immediate', 'gradual', 'scheduled', 'on_demand') DEFAULT 'immediate',
    
    -- Configuration parameters
    confidence_threshold DECIMAL(3,2) NOT NULL,
    batch_size INTEGER NOT NULL,
    processing_interval_seconds INTEGER DEFAULT 1,
    max_concurrent_requests INTEGER DEFAULT 10,
    timeout_seconds INTEGER DEFAULT 30,
    
    -- Resource allocation
    allocated_gpu_memory_gb DECIMAL(6,2),
    allocated_cpu_cores INTEGER,
    allocated_ram_gb DECIMAL(6,2),
    priority_level ENUM('low', 'medium', 'high', 'critical') DEFAULT 'medium',
    resource_limits JSON,
    
    -- Deployment timing
    scheduled_start_time TIMESTAMP,
    scheduled_end_time TIMESTAMP,
    deployed_at TIMESTAMP,
    last_health_check TIMESTAMP,
    next_maintenance_window TIMESTAMP,
    
    -- Performance settings
    auto_scaling_enabled BOOLEAN DEFAULT FALSE,
    min_instances INTEGER DEFAULT 1,
    max_instances INTEGER DEFAULT 3,
    scale_up_threshold DECIMAL(5,2) DEFAULT 80.00,
    scale_down_threshold DECIMAL(5,2) DEFAULT 30.00,
    
    -- Monitoring and alerting
    monitoring_enabled BOOLEAN DEFAULT TRUE,
    alert_on_errors BOOLEAN DEFAULT TRUE,
    alert_on_performance_degradation BOOLEAN DEFAULT TRUE,
    performance_alert_threshold DECIMAL(5,2) DEFAULT 10.00,
    error_rate_alert_threshold DECIMAL(5,2) DEFAULT 5.00,
    
    -- Integration settings
    input_sources JSON,
    output_destinations JSON,
    preprocessing_pipeline JSON,
    postprocessing_pipeline JSON,
    
    -- Rollback and versioning
    rollback_model_id UUID,
    rollback_enabled BOOLEAN DEFAULT TRUE,
    previous_deployment_id UUID,
    deployment_notes TEXT,
    rollback_trigger_conditions JSON,
    
    -- Access control
    authorized_users JSON,
    api_access_enabled BOOLEAN DEFAULT FALSE,
    api_key VARCHAR(255),
    rate_limit_requests_per_minute INTEGER DEFAULT 100,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deployed_by UUID NOT NULL,
    
    FOREIGN KEY (model_id) REFERENCES ai_models(id),
    FOREIGN KEY (site_id) REFERENCES sites(id),
    FOREIGN KEY (rollback_model_id) REFERENCES ai_models(id),
    FOREIGN KEY (previous_deployment_id) REFERENCES model_deployments(id),
    FOREIGN KEY (deployed_by) REFERENCES users(id),
    
    INDEX idx_deployments_model_site (model_id, site_id, deployment_status),
    INDEX idx_deployments_status (deployment_status, deployed_at DESC),
    INDEX idx_deployments_type (deployment_type, deployment_strategy),
    INDEX idx_deployments_performance (performance_alert_threshold, error_rate_alert_threshold)
);
```

### **model_performance_metrics**
```sql
CREATE TABLE model_performance_metrics (
    id UUID PRIMARY KEY,
    deployment_id UUID NOT NULL,
    metric_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    collection_period_minutes INTEGER DEFAULT 5,
    
    -- Performance metrics
    accuracy_percentage DECIMAL(5,2),
    precision_percentage DECIMAL(5,2),
    recall_percentage DECIMAL(5,2),
    f1_score DECIMAL(5,2),
    confidence_score_avg DECIMAL(3,2),
    inference_time_avg_ms DECIMAL(8,3),
    inference_time_p95_ms DECIMAL(8,3),
    throughput_fps DECIMAL(8,2),
    
    -- Detection statistics
    total_detections INTEGER DEFAULT 0,
    true_positives INTEGER DEFAULT 0,
    false_positives INTEGER DEFAULT 0,
    true_negatives INTEGER DEFAULT 0,
    false_negatives INTEGER DEFAULT 0,
    detection_rate_per_hour DECIMAL(8,2),
    
    -- Resource utilization
    cpu_utilization_avg DECIMAL(5,2),
    cpu_utilization_max DECIMAL(5,2),
    gpu_utilization_avg DECIMAL(5,2),
    gpu_utilization_max DECIMAL(5,2),
    memory_usage_avg_gb DECIMAL(8,2),
    memory_usage_max_gb DECIMAL(8,2),
    gpu_memory_usage_avg_gb DECIMAL(6,2),
    gpu_memory_usage_max_gb DECIMAL(6,2),
    
    -- Network and I/O metrics
    network_bandwidth_usage_mbps DECIMAL(8,2),
    disk_io_read_mb DECIMAL(10,2),
    disk_io_write_mb DECIMAL(10,2),
    api_requests_per_minute INTEGER DEFAULT 0,
    api_response_time_avg_ms DECIMAL(8,2),
    
    -- Error tracking
    total_errors INTEGER DEFAULT 0,
    preprocessing_errors INTEGER DEFAULT 0,
    inference_errors INTEGER DEFAULT 0,
    postprocessing_errors INTEGER DEFAULT 0,
    timeout_errors INTEGER DEFAULT 0,
    memory_errors INTEGER DEFAULT 0,
    error_rate_percentage DECIMAL(5,2),
    
    -- Quality metrics
    data_quality_score DECIMAL(5,2),
    prediction_consistency_score DECIMAL(5,2),
    drift_detection_score DECIMAL(5,2),
    anomaly_detection_count INTEGER DEFAULT 0,
    
    -- Business impact metrics
    cost_per_inference DECIMAL(10,6),
    cost_per_detection DECIMAL(10,4),
    roi_impact_score DECIMAL(8,2),
    user_satisfaction_score DECIMAL(3,1),
    business_value_generated DECIMAL(12,2),
    
    -- Comparative analysis
    baseline_performance_diff DECIMAL(6,2),
    previous_period_performance_diff DECIMAL(6,2),
    industry_benchmark_comparison DECIMAL(6,2),
    peer_model_performance_rank INTEGER,
    
    -- Environmental factors
    temperature_celsius DECIMAL(4,1),
    humidity_percentage DECIMAL(5,2),
    ambient_light_conditions VARCHAR(100),
    network_latency_ms INTEGER,
    data_center_load_percentage DECIMAL(5,2),
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    calculated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (deployment_id) REFERENCES model_deployments(id) ON DELETE CASCADE,
    
    INDEX idx_performance_deployment_time (deployment_id, metric_timestamp DESC),
    INDEX idx_performance_metrics (accuracy_percentage DESC, f1_score DESC),
    INDEX idx_performance_resource (cpu_utilization_avg, gpu_utilization_avg),
    INDEX idx_performance_errors (error_rate_percentage, total_errors)
);
```

### **model_training_jobs**
```sql
CREATE TABLE model_training_jobs (
    id UUID PRIMARY KEY,
    model_id UUID NOT NULL,
    job_name VARCHAR(255) NOT NULL,
    job_description TEXT,
    
    -- Job configuration
    training_type ENUM('initial_training', 'fine_tuning', 'transfer_learning', 'incremental_learning', 'reinforcement_learning') NOT NULL,
    base_model_id UUID,
    dataset_id UUID,
    hyperparameters JSON,
    
    -- Resource allocation
    compute_instance_type VARCHAR(100),
    gpu_count INTEGER DEFAULT 1,
    gpu_type VARCHAR(100),
    cpu_cores INTEGER DEFAULT 8,
    memory_gb INTEGER DEFAULT 32,
    storage_gb INTEGER DEFAULT 100,
    
    -- Training parameters
    epochs INTEGER DEFAULT 100,
    batch_size INTEGER DEFAULT 32,
    learning_rate DECIMAL(10,8) DEFAULT 0.001,
    optimizer VARCHAR(50) DEFAULT 'Adam',
    loss_function VARCHAR(100),
    validation_split DECIMAL(3,2) DEFAULT 0.20,
    early_stopping_patience INTEGER DEFAULT 10,
    
    -- Status tracking
    job_status ENUM('queued', 'initializing', 'running', 'paused', 'completed', 'failed', 'cancelled') DEFAULT 'queued',
    progress_percentage DECIMAL(5,2) DEFAULT 0.00,
    current_epoch INTEGER DEFAULT 0,
    estimated_completion_time TIMESTAMP,
    actual_completion_time TIMESTAMP,
    
    -- Performance tracking
    current_loss DECIMAL(12,8),
    current_accuracy DECIMAL(5,2),
    best_loss DECIMAL(12,8),
    best_accuracy DECIMAL(5,2),
    best_epoch INTEGER,
    validation_loss DECIMAL(12,8),
    validation_accuracy DECIMAL(5,2),
    
    -- Cost tracking
    compute_cost_per_hour DECIMAL(8,4),
    estimated_total_cost DECIMAL(10,2),
    actual_cost DECIMAL(10,2),
    cost_budget_limit DECIMAL(10,2),
    cost_alert_threshold DECIMAL(10,2),
    
    -- Results and artifacts
    output_model_path VARCHAR(500),
    checkpoint_paths JSON,
    log_file_path VARCHAR(500),
    tensorboard_log_path VARCHAR(500),
    metrics_file_path VARCHAR(500),
    confusion_matrix_path VARCHAR(500),
    
    -- Error handling
    error_message TEXT,
    error_stack_trace TEXT,
    retry_count INTEGER DEFAULT 0,
    max_retries INTEGER DEFAULT 3,
    auto_restart_on_failure BOOLEAN DEFAULT TRUE,
    
    -- Notifications
    notification_recipients JSON,
    notification_on_completion BOOLEAN DEFAULT TRUE,
    notification_on_failure BOOLEAN DEFAULT TRUE,
    notification_on_milestone BOOLEAN DEFAULT FALSE,
    slack_webhook_url VARCHAR(500),
    
    -- Experiment tracking
    experiment_name VARCHAR(255),
    experiment_tags JSON,
    parent_experiment_id UUID,
    experiment_notes TEXT,
    reproducibility_seed INTEGER,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    created_by UUID NOT NULL,
    
    FOREIGN KEY (model_id) REFERENCES ai_models(id),
    FOREIGN KEY (base_model_id) REFERENCES ai_models(id),
    FOREIGN KEY (parent_experiment_id) REFERENCES model_training_jobs(id),
    FOREIGN KEY (created_by) REFERENCES users(id),
    
    INDEX idx_training_jobs_model (model_id, job_status),
    INDEX idx_training_jobs_status (job_status, created_at DESC),
    INDEX idx_training_jobs_performance (best_accuracy DESC, current_accuracy DESC),
    INDEX idx_training_jobs_cost (actual_cost, cost_budget_limit)
);
```

### **model_evaluation_results**
```sql
CREATE TABLE model_evaluation_results (
    id UUID PRIMARY KEY,
    model_id UUID NOT NULL,
    evaluation_name VARCHAR(255) NOT NULL,
    evaluation_type ENUM('validation', 'test', 'benchmark', 'production_sample', 'a_b_test', 'stress_test') NOT NULL,
    
    -- Evaluation dataset information
    dataset_id UUID,
    dataset_size INTEGER,
    dataset_description TEXT,
    evaluation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    evaluation_duration_minutes INTEGER,
    
    -- Overall performance metrics
    overall_accuracy DECIMAL(5,2),
    overall_precision DECIMAL(5,2),
    overall_recall DECIMAL(5,2),
    overall_f1_score DECIMAL(5,2),
    micro_f1_score DECIMAL(5,2),
    macro_f1_score DECIMAL(5,2),
    weighted_f1_score DECIMAL(5,2),
    
    -- Per-class performance metrics
    class_wise_metrics JSON,
    confusion_matrix JSON,
    classification_report JSON,
    
    -- Detection-specific metrics
    mean_average_precision_50 DECIMAL(5,2),
    mean_average_precision_75 DECIMAL(5,2),
    mean_average_precision_50_95 DECIMAL(5,2),
    average_recall_100 DECIMAL(5,2),
    average_recall_300 DECIMAL(5,2),
    average_recall_1000 DECIMAL(5,2),
    
    -- Performance distribution
    confidence_score_distribution JSON,
    inference_time_distribution JSON,
    accuracy_by_confidence_threshold JSON,
    roc_curve_data JSON,
    precision_recall_curve_data JSON,
    
    -- Resource performance
    evaluation_cpu_time_seconds DECIMAL(10,3),
    evaluation_gpu_time_seconds DECIMAL(10,3),
    peak_memory_usage_gb DECIMAL(8,2),
    average_inference_time_ms DECIMAL(8,3),
    throughput_images_per_second DECIMAL(8,2),
    
    -- Robustness testing
    adversarial_accuracy DECIMAL(5,2),
    noise_robustness_score DECIMAL(5,2),
    lighting_robustness_score DECIMAL(5,2),
    occlusion_robustness_score DECIMAL(5,2),
    scale_robustness_score DECIMAL(5,2),
    
    -- Bias and fairness metrics
    demographic_parity_score DECIMAL(5,2),
    equalized_odds_score DECIMAL(5,2),
    calibration_score DECIMAL(5,2),
    bias_detection_results JSON,
    fairness_constraints_met BOOLEAN DEFAULT FALSE,
    
    -- Business impact assessment
    cost_per_evaluation DECIMAL(8,4),
    business_accuracy_score DECIMAL(5,2),
    false_positive_cost_impact DECIMAL(10,2),
    false_negative_cost_impact DECIMAL(10,2),
    roi_projection DECIMAL(10,2),
    
    -- Comparison metrics
    baseline_model_comparison JSON,
    previous_version_comparison JSON,
    competitor_model_comparison JSON,
    human_performance_comparison DECIMAL(6,2),
    
    -- Quality assurance
    data_quality_issues JSON,
    model_quality_score DECIMAL(5,2),
    deployment_readiness_score DECIMAL(5,2),
    risk_assessment_score DECIMAL(5,2),
    
    -- Files and artifacts
    evaluation_report_path VARCHAR(500),
    detailed_results_path VARCHAR(500),
    visualization_files JSON,
    raw_predictions_path VARCHAR(500),
    error_analysis_path VARCHAR(500),
    
    -- Review and approval
    reviewed_by UUID,
    review_status ENUM('pending', 'approved', 'requires_revision', 'rejected') DEFAULT 'pending',
    review_date TIMESTAMP,
    review_comments TEXT,
    approval_for_production BOOLEAN DEFAULT FALSE,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    evaluated_by UUID NOT NULL,
    
    FOREIGN KEY (model_id) REFERENCES ai_models(id),
    FOREIGN KEY (reviewed_by) REFERENCES users(id),
    FOREIGN KEY (evaluated_by) REFERENCES users(id),
    
    INDEX idx_evaluation_model_type (model_id, evaluation_type, evaluation_date DESC),
    INDEX idx_evaluation_performance (overall_accuracy DESC, overall_f1_score DESC),
    INDEX idx_evaluation_review (review_status, approval_for_production),
    INDEX idx_evaluation_business (business_accuracy_score DESC, roi_projection DESC)
);
```

---

## 📊 **SYSTEM MONITORING & INFRASTRUCTURE HEALTH**

### **system_health_monitoring**
```sql
CREATE TABLE system_health_monitoring (
    id UUID PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    monitoring_interval_minutes INTEGER DEFAULT 5,
    
    -- Overall system health
    overall_health_score DECIMAL(5,2) NOT NULL,
    system_status ENUM('healthy', 'warning', 'critical', 'maintenance') DEFAULT 'healthy',
    availability_percentage DECIMAL(5,2) DEFAULT 100.00,
    response_time_avg_ms INTEGER,
    throughput_requests_per_second DECIMAL(10,2),
    
    -- Resource utilization aggregates
    total_cpu_utilization DECIMAL(5,2),
    total_memory_utilization DECIMAL(5,2),
    total_storage_utilization DECIMAL(5,2),
    total_network_utilization DECIMAL(5,2),
    
    -- Service and infrastructure health summary
    healthy_services_count INTEGER DEFAULT 0,
    warning_services_count INTEGER DEFAULT 0,
    critical_services_count INTEGER DEFAULT 0,
    total_services_count INTEGER DEFAULT 0,
    
    healthy_sites_count INTEGER DEFAULT 0,
    warning_sites_count INTEGER DEFAULT 0,
    critical_sites_count INTEGER DEFAULT 0,
    total_sites_count INTEGER DEFAULT 0,
    
    -- Performance indicators
    error_rate_percentage DECIMAL(5,2) DEFAULT 0.00,
    alert_rate_per_hour DECIMAL(8,2) DEFAULT 0.00,
    incident_resolution_time_avg_minutes INTEGER,
    sla_compliance_percentage DECIMAL(5,2) DEFAULT 100.00,
    
    -- Trend indicators
    health_trend ENUM('improving', 'stable', 'declining', 'volatile') DEFAULT 'stable',
    performance_trend ENUM('improving', 'stable', 'declining') DEFAULT 'stable',
    capacity_trend ENUM('increasing', 'stable', 'decreasing') DEFAULT 'stable',
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_system_health_timestamp (timestamp DESC),
    INDEX idx_system_health_status (system_status, overall_health_score),
    INDEX idx_system_health_trends (health_trend, performance_trend)
);
```

### **service_health_metrics**
```sql
CREATE TABLE service_health_metrics (
    id UUID PRIMARY KEY,
    service_name VARCHAR(255) NOT NULL,
    service_type ENUM('ai_detection', 'video_streaming', 'database', 'api_gateway', 'notification', 'file_storage', 'authentication', 'monitoring', 'backup') NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Service status
    service_status ENUM('healthy', 'warning', 'critical', 'offline', 'maintenance') DEFAULT 'healthy',
    uptime_percentage DECIMAL(5,2) DEFAULT 100.00,
    last_restart TIMESTAMP,
    restart_count_24h INTEGER DEFAULT 0,
    
    -- Performance metrics
    response_time_avg_ms DECIMAL(8,3),
    response_time_p95_ms DECIMAL(8,3),
    response_time_p99_ms DECIMAL(8,3),
    throughput_requests_per_second DECIMAL(8,2),
    success_rate_percentage DECIMAL(5,2) DEFAULT 100.00,
    
    -- Resource utilization
    cpu_utilization_percentage DECIMAL(5,2),
    memory_utilization_percentage DECIMAL(5,2),
    memory_usage_gb DECIMAL(8,2),
    disk_utilization_percentage DECIMAL(5,2),
    network_io_mbps DECIMAL(8,2),
    
    -- Error tracking
    total_errors_24h INTEGER DEFAULT 0,
    error_rate_percentage DECIMAL(5,2) DEFAULT 0.00,
    timeout_errors INTEGER DEFAULT 0,
    connection_errors INTEGER DEFAULT 0,
    processing_errors INTEGER DEFAULT 0,
    
    -- Service-specific metrics
    active_connections INTEGER,
    queue_length INTEGER DEFAULT 0,
    cache_hit_ratio DECIMAL(5,2),
    database_connections INTEGER,
    concurrent_requests INTEGER,
    
    -- Health check results
    health_check_status BOOLEAN DEFAULT TRUE,
    health_check_response_time_ms INTEGER,
    dependency_status JSON,
    external_service_status JSON,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_service_health_name_time (service_name, timestamp DESC),
    INDEX idx_service_health_status (service_status, uptime_percentage),
    INDEX idx_service_health_performance (response_time_avg_ms, error_rate_percentage)
);
```

### **infrastructure_monitoring**
```sql
CREATE TABLE infrastructure_monitoring (
    id UUID PRIMARY KEY,
    component_name VARCHAR(255) NOT NULL,
    component_type ENUM('load_balancer', 'cdn', 'cache', 'message_queue', 'dns', 'firewall', 'proxy', 'storage', 'network') NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Component status
    component_status ENUM('healthy', 'warning', 'critical', 'offline', 'maintenance') DEFAULT 'healthy',
    availability_percentage DECIMAL(5,2) DEFAULT 100.00,
    capacity_utilization_percentage DECIMAL(5,2),
    
    -- Performance metrics
    throughput_mbps DECIMAL(10,2),
    latency_avg_ms DECIMAL(8,3),
    latency_p95_ms DECIMAL(8,3),
    
    -- Component-specific metrics
    active_connections INTEGER,
    hit_ratio_percentage DECIMAL(5,2),
    cache_size_gb DECIMAL(10,2),
    queue_size INTEGER,
    message_processing_rate DECIMAL(8,2),
    
    -- Resource utilization
    cpu_utilization_percentage DECIMAL(5,2),
    memory_utilization_percentage DECIMAL(5,2),
    disk_utilization_percentage DECIMAL(5,2),
    network_utilization_percentage DECIMAL(5,2),
    
    -- Error tracking
    error_count_24h INTEGER DEFAULT 0,
    error_rate_percentage DECIMAL(5,2) DEFAULT 0.00,
    timeout_count INTEGER DEFAULT 0,
    connection_failures INTEGER DEFAULT 0,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_infrastructure_component_time (component_name, timestamp DESC),
    INDEX idx_infrastructure_status (component_status, availability_percentage),
    INDEX idx_infrastructure_utilization (capacity_utilization_percentage, cpu_utilization_percentage)
);
```

### **system_alerts**
```sql
CREATE TABLE system_alerts (
    id UUID PRIMARY KEY,
    alert_id VARCHAR(255) UNIQUE NOT NULL,
    
    -- Alert classification
    alert_level ENUM('info', 'warning', 'critical', 'emergency') NOT NULL,
    alert_category ENUM('performance', 'availability', 'security', 'capacity', 'configuration', 'compliance') NOT NULL,
    alert_type VARCHAR(255) NOT NULL,
    alert_source VARCHAR(255) NOT NULL,
    
    -- Alert content
    title VARCHAR(500) NOT NULL,
    message TEXT NOT NULL,
    detailed_description TEXT,
    recommended_actions JSON,
    
    -- Scope and impact
    affected_services JSON,
    affected_sites JSON,
    affected_users_count INTEGER DEFAULT 0,
    business_impact ENUM('none', 'low', 'medium', 'high', 'critical') DEFAULT 'none',
    
    -- Alert lifecycle
    triggered_at TIMESTAMP NOT NULL,
    status ENUM('active', 'investigating', 'acknowledged', 'resolved', 'suppressed', 'expired') DEFAULT 'active',
    assigned_to UUID,
    acknowledged_by UUID,
    acknowledged_at TIMESTAMP,
    resolved_by UUID,
    resolved_at TIMESTAMP,
    resolution_notes TEXT,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (assigned_to) REFERENCES users(id),
    FOREIGN KEY (acknowledged_by) REFERENCES users(id),
    FOREIGN KEY (resolved_by) REFERENCES users(id),
    
    INDEX idx_alerts_level_status (alert_level, status, triggered_at DESC),
    INDEX idx_alerts_category (alert_category, alert_type),
    INDEX idx_alerts_assigned (assigned_to, status)
);
```

### **monitoring_dashboards**
```sql
CREATE TABLE monitoring_dashboards (
    id UUID PRIMARY KEY,
    dashboard_name VARCHAR(255) NOT NULL,
    dashboard_type ENUM('system_overview', 'service_monitoring', 'infrastructure', 'site_monitoring', 'custom') NOT NULL,
    created_by UUID NOT NULL,
    
    -- Dashboard configuration
    layout_config JSON,
    refresh_interval_seconds INTEGER DEFAULT 30,
    auto_refresh_enabled BOOLEAN DEFAULT TRUE,
    time_range_default VARCHAR(50) DEFAULT '24h',
    
    -- Widget configuration
    widgets JSON,
    widget_count INTEGER DEFAULT 0,
    custom_metrics JSON,
    filter_presets JSON,
    
    -- Access control
    is_public BOOLEAN DEFAULT FALSE,
    shared_with_users JSON,
    shared_with_roles JSON,
    view_permissions ENUM('read', 'read_write', 'admin') DEFAULT 'read',
    
    -- Usage tracking
    view_count INTEGER DEFAULT 0,
    last_viewed TIMESTAMP,
    favorite_count INTEGER DEFAULT 0,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (created_by) REFERENCES users(id),
    
    INDEX idx_dashboards_type (dashboard_type, is_public),
    INDEX idx_dashboards_creator (created_by, created_at DESC)
);
```

---

## 🔐 **ACCESS CONTROL & SECURITY MANAGEMENT**

### **access_control_roles**
```sql
CREATE TABLE access_control_roles (
    id UUID PRIMARY KEY,
    role_name VARCHAR(255) NOT NULL UNIQUE,
    role_code VARCHAR(100) NOT NULL UNIQUE,
    description TEXT NOT NULL,
    role_level ENUM('system', 'site', 'management', 'operations', 'specialized', 'worker') NOT NULL,
    risk_level ENUM('critical', 'high', 'medium', 'low') NOT NULL,
    color_code VARCHAR(7) DEFAULT '#6B7280',
    
    -- Role hierarchy and inheritance
    parent_role_id UUID,
    inherits_permissions BOOLEAN DEFAULT TRUE,
    inheritance_level INTEGER DEFAULT 0,
    role_path VARCHAR(1000),
    
    -- Site access configuration
    site_access_type ENUM('all_sites', 'assigned_sites', 'multi_site', 'single_site', 'none') DEFAULT 'assigned_sites',
    default_site_assignments JSON,
    site_restrictions JSON,
    
    -- Role metadata
    is_system_role BOOLEAN DEFAULT FALSE,
    is_default_role BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    is_assignable BOOLEAN DEFAULT TRUE,
    requires_approval BOOLEAN DEFAULT FALSE,
    auto_expire_days INTEGER,
    
    -- Usage tracking
    user_count INTEGER DEFAULT 0,
    assignment_count INTEGER DEFAULT 0,
    last_assigned TIMESTAMP,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by UUID NOT NULL,
    updated_by UUID,
    
    FOREIGN KEY (parent_role_id) REFERENCES access_control_roles(id),
    FOREIGN KEY (created_by) REFERENCES users(id),
    FOREIGN KEY (updated_by) REFERENCES users(id),
    
    INDEX idx_roles_level_risk (role_level, risk_level),
    INDEX idx_roles_hierarchy (parent_role_id, inheritance_level),
    INDEX idx_roles_usage (user_count DESC, assignment_count DESC)
);
```

### **system_permissions**
```sql
CREATE TABLE system_permissions (
    id UUID PRIMARY KEY,
    permission_name VARCHAR(255) NOT NULL UNIQUE,
    permission_code VARCHAR(100) NOT NULL UNIQUE,
    description TEXT NOT NULL,
    category VARCHAR(100) NOT NULL,
    subcategory VARCHAR(100),
    risk_level ENUM('critical', 'high', 'medium', 'low') NOT NULL,
    
    -- Permission scope and context
    resource_type VARCHAR(100),
    resource_scope ENUM('global', 'site', 'zone', 'equipment', 'personnel', 'data') NOT NULL,
    operation_type ENUM('create', 'read', 'update', 'delete', 'execute', 'admin', 'full') NOT NULL,
    
    -- Permission attributes
    is_system_permission BOOLEAN DEFAULT FALSE,
    is_assignable BOOLEAN DEFAULT TRUE,
    requires_mfa BOOLEAN DEFAULT FALSE,
    requires_approval BOOLEAN DEFAULT FALSE,
    is_delegatable BOOLEAN DEFAULT FALSE,
    
    -- Dependencies and relationships
    prerequisite_permissions JSON,
    conflicting_permissions JSON,
    implies_permissions JSON,
    
    -- Usage tracking
    usage_count INTEGER DEFAULT 0,
    assignment_count INTEGER DEFAULT 0,
    last_used TIMESTAMP,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by UUID NOT NULL,
    
    FOREIGN KEY (created_by) REFERENCES users(id),
    
    INDEX idx_permissions_category (category, subcategory, risk_level),
    INDEX idx_permissions_scope (resource_scope, operation_type),
    INDEX idx_permissions_usage (usage_count DESC, assignment_count DESC)
);
```

### **role_permission_assignments**
```sql
CREATE TABLE role_permission_assignments (
    id UUID PRIMARY KEY,
    role_id UUID NOT NULL,
    permission_id UUID NOT NULL,
    
    -- Assignment configuration
    assignment_type ENUM('direct', 'inherited', 'conditional', 'temporary') DEFAULT 'direct',
    granted_by UUID NOT NULL,
    granted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    effective_from TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    effective_until TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    
    -- Conditional access
    conditions JSON,
    restrictions JSON,
    scope_limitations JSON,
    
    -- Usage tracking
    usage_count INTEGER DEFAULT 0,
    last_used TIMESTAMP,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (role_id) REFERENCES access_control_roles(id) ON DELETE CASCADE,
    FOREIGN KEY (permission_id) REFERENCES system_permissions(id),
    FOREIGN KEY (granted_by) REFERENCES users(id),
    
    INDEX idx_role_permissions (role_id, permission_id, is_active),
    INDEX idx_permission_roles (permission_id, role_id),
    UNIQUE KEY unique_role_permission (role_id, permission_id, assignment_type)
);
```

### **security_policies**
```sql
CREATE TABLE security_policies (
    id UUID PRIMARY KEY,
    policy_name VARCHAR(255) NOT NULL UNIQUE,
    policy_code VARCHAR(100) NOT NULL UNIQUE,
    description TEXT NOT NULL,
    category ENUM('authentication', 'authorization', 'session', 'password', 'mfa', 'data_access', 'network', 'compliance') NOT NULL,
    policy_type ENUM('system', 'site', 'role', 'user') NOT NULL,
    
    -- Policy configuration
    policy_rules JSON NOT NULL,
    enforcement_level ENUM('advisory', 'warning', 'blocking', 'strict') DEFAULT 'blocking',
    is_mandatory BOOLEAN DEFAULT TRUE,
    is_active BOOLEAN DEFAULT TRUE,
    
    -- Scope and application
    applies_to_roles JSON,
    applies_to_users JSON,
    applies_to_sites JSON,
    exclusions JSON,
    
    -- Monitoring and enforcement
    violation_handling ENUM('log_only', 'warn_user', 'block_action', 'escalate') DEFAULT 'block_action',
    violation_count INTEGER DEFAULT 0,
    last_violation TIMESTAMP,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by UUID NOT NULL,
    
    FOREIGN KEY (created_by) REFERENCES users(id),
    
    INDEX idx_policies_category (category, policy_type, is_active),
    INDEX idx_policies_enforcement (enforcement_level, violation_count)
);
```

### **access_control_audit_log**
```sql
CREATE TABLE access_control_audit_log (
    id UUID PRIMARY KEY,
    event_type ENUM('role_assignment', 'permission_grant', 'permission_revoke', 'policy_change', 'access_attempt', 'violation', 'escalation') NOT NULL,
    event_category ENUM('authentication', 'authorization', 'administration', 'compliance', 'security') NOT NULL,
    
    -- Event participants
    user_id UUID,
    target_user_id UUID,
    role_id UUID,
    permission_id UUID,
    policy_id UUID,
    
    -- Event details
    action_performed VARCHAR(255) NOT NULL,
    resource_type VARCHAR(100),
    resource_id UUID,
    site_id UUID,
    
    -- Access attempt details
    access_granted BOOLEAN,
    denial_reason TEXT,
    risk_score DECIMAL(3,1),
    violation_type VARCHAR(100),
    violation_severity ENUM('low', 'medium', 'high', 'critical'),
    
    -- Session and client information
    session_id UUID,
    ip_address INET,
    user_agent TEXT,
    client_application VARCHAR(100),
    
    -- State tracking
    previous_state JSON,
    new_state JSON,
    change_summary TEXT,
    
    event_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (target_user_id) REFERENCES users(id),
    FOREIGN KEY (role_id) REFERENCES access_control_roles(id),
    FOREIGN KEY (permission_id) REFERENCES system_permissions(id),
    FOREIGN KEY (policy_id) REFERENCES security_policies(id),
    FOREIGN KEY (site_id) REFERENCES sites(id),
    
    INDEX idx_audit_log_event (event_type, event_category, event_timestamp DESC),
    INDEX idx_audit_log_user (user_id, event_timestamp DESC),
    INDEX idx_audit_log_violations (violation_severity, access_granted, event_timestamp DESC)
);
```

---

## ⚙️ **INTEGRATION & USER EXPERIENCE**

### **third_party_integrations**
```sql
CREATE TABLE third_party_integrations (
    id UUID PRIMARY KEY,
    integration_name VARCHAR(255) NOT NULL,
    integration_type ENUM('communication', 'storage', 'analytics', 'ai_ml', 'monitoring', 'payment', 'identity') NOT NULL,
    provider_name VARCHAR(255) NOT NULL,
    description TEXT,
    
    -- Status and health
    status ENUM('active', 'inactive', 'error', 'testing', 'pending') DEFAULT 'pending',
    health_score DECIMAL(5,2) DEFAULT 0.00,
    last_health_check TIMESTAMP,
    next_health_check TIMESTAMP,
    
    -- Configuration
    configuration JSON NOT NULL,
    credentials JSON, -- Encrypted
    endpoints JSON,
    rate_limits JSON,
    
    -- Usage tracking
    monthly_usage BIGINT DEFAULT 0,
    monthly_limit BIGINT,
    error_rate DECIMAL(5,2) DEFAULT 0.00,
    avg_response_time_ms DECIMAL(8,2),
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by UUID NOT NULL,
    
    FOREIGN KEY (created_by) REFERENCES users(id),
    
    INDEX idx_integrations_type_status (integration_type, status),
    INDEX idx_integrations_health (health_score, last_health_check)
);
```

### **user_profile_settings**
```sql
CREATE TABLE user_profile_settings (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL UNIQUE,
    profile_picture_url VARCHAR(500),
    bio TEXT,
    preferences JSON,
    notification_settings JSON,
    dashboard_config JSON,
    theme_settings JSON,
    privacy_settings JSON,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    
    INDEX idx_profile_settings_user (user_id)
);
```

### **user_application_settings**
```sql
CREATE TABLE user_application_settings (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL UNIQUE,
    language VARCHAR(10) DEFAULT 'en',
    timezone VARCHAR(100),
    date_format VARCHAR(50),
    time_format ENUM('12h', '24h') DEFAULT '12h',
    theme ENUM('light', 'dark', 'auto') DEFAULT 'light',
    font_size ENUM('small', 'medium', 'large') DEFAULT 'medium',
    notifications_enabled BOOLEAN DEFAULT TRUE,
    email_notifications BOOLEAN DEFAULT TRUE,
    quiet_hours_enabled BOOLEAN DEFAULT FALSE,
    quiet_hours_start TIME,
    quiet_hours_end TIME,
    data_sharing_enabled BOOLEAN DEFAULT TRUE,
    analytics_enabled BOOLEAN DEFAULT TRUE,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    
    INDEX idx_app_settings_user (user_id)
);
```

### **help_articles**
```sql
CREATE TABLE help_articles (
    id UUID PRIMARY KEY,
    title VARCHAR(500) NOT NULL,
    content TEXT NOT NULL,
    category VARCHAR(100) NOT NULL,
    subcategory VARCHAR(100),
    tags JSON,
    author_id UUID NOT NULL,
    is_published BOOLEAN DEFAULT FALSE,
    view_count INTEGER DEFAULT 0,
    helpful_count INTEGER DEFAULT 0,
    unhelpful_count INTEGER DEFAULT 0,
    search_keywords TEXT,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (author_id) REFERENCES users(id),
    
    INDEX idx_help_articles_category (category, subcategory, is_published),
    INDEX idx_help_articles_popularity (view_count DESC, helpful_count DESC),
    FULLTEXT INDEX idx_help_articles_search (title, content, search_keywords)
);
```

### **user_feedback**
```sql
CREATE TABLE user_feedback (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL,
    feedback_type ENUM('bug_report', 'feature_request', 'documentation', 'general') NOT NULL,
    title VARCHAR(500) NOT NULL,
    description TEXT NOT NULL,
    priority ENUM('low', 'medium', 'high') DEFAULT 'medium',
    status ENUM('submitted', 'reviewing', 'in_progress', 'resolved', 'closed') DEFAULT 'submitted',
    category VARCHAR(100),
    attachments JSON,
    upvote_count INTEGER DEFAULT 0,
    admin_response TEXT,
    responded_by UUID,
    responded_at TIMESTAMP,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (responded_by) REFERENCES users(id),
    
    INDEX idx_feedback_type_status (feedback_type, status, created_at DESC),
    INDEX idx_feedback_user (user_id, created_at DESC),
    INDEX idx_feedback_priority (priority, status)
);
```

---

### **Version 2.0.0 (2025-01-12) - COMPLETE SYSTEM ANALYSIS 🎉**
- **Updated from**: Screen Analysis #22-27 (System Monitoring, Access Control, Integration Settings, My Profile, Settings, Help & Documentation)
- **Tables added**: 17 new tables across system monitoring, access control, integrations, and user experience
- **New sections added**: System Monitoring & Infrastructure Health (5 tables), Access Control & Security Management (5 tables), Integration & User Experience (7 tables)
- **Final milestone achieved**: Complete 27/27 screen analysis with comprehensive database schema
- **New features added**:
  - Real-time system monitoring with infrastructure health tracking and alerting
  - Enterprise-grade access control with role-based permissions and security policies
  - Third-party integration management with health monitoring and usage tracking
  - Complete user experience with profile management, settings, and help system
- **Focus**: System administration completion, security governance, user experience optimization
- **Updated table count**: **93 → 110 tables** 
- **🏆 ACHIEVEMENT**: 100% Complete System Analysis

---

**Document Maintained By**: AI Construction Management System Team
**Last Review**: 2025-01-12  
**Status**: ✅ **COMPLETE** - All 27 screens analyzed with comprehensive database schema