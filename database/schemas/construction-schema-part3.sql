-- ================================================================
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

SELECT 'Construction Management Schema Part 3 (Tables 12-18) created successfully!' as Status;