-- ================================================================
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