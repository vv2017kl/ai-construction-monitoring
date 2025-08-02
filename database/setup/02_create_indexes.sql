-- ================================================================
-- PERFORMANCE INDEXES AND OPTIMIZATIONS
-- Construction Site AI Monitoring System
-- Version: 1.0
-- ================================================================

-- ================================================================
-- VMS DATABASE INDEXES
-- ================================================================
USE construction_vms;

-- Time-series query optimization for video storage
CREATE INDEX idx_video_storage_time_camera ON video_storage (camera_id, start_time DESC, end_time DESC);
CREATE INDEX idx_video_storage_size ON video_storage (file_size_bytes DESC);
CREATE INDEX idx_video_storage_archived ON video_storage (is_archived, archive_date);

-- Performance metrics time-series optimization
CREATE INDEX idx_performance_metrics_time_entity ON performance_metrics (entity_id, metric_timestamp DESC);
CREATE INDEX idx_performance_metrics_type_time ON performance_metrics (metric_type, metric_timestamp DESC);

-- Camera health and status monitoring
CREATE INDEX idx_cameras_health_status ON cameras (status, last_seen_at DESC);
CREATE INDEX idx_cameras_location ON cameras (map_x, map_y);

-- Configuration management
CREATE INDEX idx_camera_configs_active ON camera_configurations (camera_id, is_active, version_number DESC);

-- API access log optimization
CREATE INDEX idx_api_logs_timestamp ON api_access_logs (request_timestamp DESC);
CREATE INDEX idx_api_logs_response_time ON api_access_logs (response_time_ms DESC);
CREATE INDEX idx_api_logs_status ON api_access_logs (response_status, request_timestamp DESC);

-- Audit trail optimization
CREATE INDEX idx_audit_logs_resource ON audit_logs (resource_type, resource_id, action_timestamp DESC);
CREATE INDEX idx_audit_logs_user_time ON audit_logs (user_id, action_timestamp DESC);

SELECT 'VMS indexes created successfully!' as Status;

-- ================================================================
-- CONSTRUCTION DATABASE INDEXES
-- ================================================================
USE construction_management;

-- Time-series indexes for detection results (critical for performance)
CREATE INDEX idx_detection_results_time_camera ON detection_results (camera_id, detection_timestamp DESC);
CREATE INDEX idx_detection_results_site_time ON detection_results (site_id, detection_timestamp DESC);
CREATE INDEX idx_detection_results_violations ON detection_results (ppe_violations_detected DESC, detection_timestamp DESC);
CREATE INDEX idx_detection_results_personnel ON detection_results (personnel_count, detection_timestamp DESC);

-- Safety violations optimization
CREATE INDEX idx_safety_violations_site_time ON safety_violations (site_id, detected_at DESC);
CREATE INDEX idx_safety_violations_severity ON safety_violations (severity, detected_at DESC);
CREATE INDEX idx_safety_violations_status ON safety_violations (resolution_status, detected_at DESC);
CREATE INDEX idx_safety_violations_camera_time ON safety_violations (camera_id, detected_at DESC);

-- Personnel tracking optimization
CREATE INDEX idx_personnel_tracking_site_time ON personnel_tracking (site_id, tracked_at DESC);
CREATE INDEX idx_personnel_tracking_compliance ON personnel_tracking (ppe_compliant, tracked_at DESC);
CREATE INDEX idx_personnel_tracking_camera ON personnel_tracking (camera_id, tracked_at DESC);

-- Alert system optimization
CREATE INDEX idx_alerts_site_status ON alerts (site_id, status, triggered_at DESC);
CREATE INDEX idx_alerts_severity_time ON alerts (severity, triggered_at DESC);
CREATE INDEX idx_alerts_camera_time ON alerts (camera_id, triggered_at DESC);
CREATE INDEX idx_alerts_acknowledged ON alerts (acknowledged_at, status);
CREATE INDEX idx_alerts_escalation ON alerts (escalation_level, triggered_at DESC);

-- Alert escalations
CREATE INDEX idx_alert_escalations_time ON alert_escalations (escalated_at DESC);
CREATE INDEX idx_alert_escalations_assignee ON alert_escalations (escalated_to, escalated_at DESC);
CREATE INDEX idx_alert_escalations_response ON alert_escalations (responded_at, escalation_level);

-- Notification system
CREATE INDEX idx_notifications_status ON notifications (delivery_status, scheduled_for);
CREATE INDEX idx_notifications_recipient ON notifications (recipient_user_id, sent_at DESC);
CREATE INDEX idx_notifications_type_time ON notifications (notification_type, sent_at DESC);

-- User and authentication optimization
CREATE INDEX idx_users_company_status ON users (company_id, status, last_login_at DESC);
CREATE INDEX idx_users_email_status ON users (email, status);
CREATE INDEX idx_user_sessions_active ON user_sessions (user_id, is_active, expires_at);
CREATE INDEX idx_user_sessions_token ON user_sessions (session_token, is_active);

-- Site and geographic optimization
CREATE INDEX idx_sites_coordinates ON sites (latitude, longitude);
CREATE INDEX idx_sites_company_status ON sites (company_id, status, project_phase);
CREATE INDEX idx_sites_timeline ON sites (planned_start_date, planned_end_date, status);

-- Zone management optimization
CREATE INDEX idx_site_zones_type_status ON site_zones (zone_type, status, site_id);
CREATE INDEX idx_site_zones_interactive ON site_zones (is_interactive, site_id);
CREATE INDEX idx_site_zones_monitoring ON site_zones (monitoring_enabled, site_id);

-- Zone actions and logs
CREATE INDEX idx_zone_actions_zone_status ON zone_actions (site_zone_id, status);
CREATE INDEX idx_zone_action_logs_time ON zone_action_logs (executed_at DESC);
CREATE INDEX idx_zone_action_logs_user ON zone_action_logs (executed_by, executed_at DESC);
CREATE INDEX idx_zone_action_logs_status ON zone_action_logs (execution_status, executed_at DESC);

-- Field assessment optimization
CREATE INDEX idx_mobile_recordings_site_time ON mobile_recordings (site_id, recording_started_at DESC);
CREATE INDEX idx_mobile_recordings_assessor ON mobile_recordings (assessor_user_id, recording_started_at DESC);
CREATE INDEX idx_mobile_recordings_sync ON mobile_recordings (sync_status, sync_started_at DESC);

-- Field reports
CREATE INDEX idx_field_reports_site_date ON field_reports (site_id, report_date DESC);
CREATE INDEX idx_field_reports_type_status ON field_reports (report_type, review_status);
CREATE INDEX idx_field_reports_assessor ON field_reports (assessor_user_id, report_date DESC);

-- Security patrol system
CREATE INDEX idx_patrol_routes_site_status ON security_patrol_routes (site_id, status);
CREATE INDEX idx_patrol_sequences_route_order ON patrol_camera_sequences (patrol_route_id, sequence_order);
CREATE INDEX idx_patrol_schedules_execution ON patrol_schedules (next_scheduled_execution, status);

-- AI models and confidence
CREATE INDEX idx_ai_models_type_status ON ai_models (model_type, status);
CREATE INDEX idx_confidence_metrics_model ON confidence_metrics (ai_model_id, calculated_at DESC);

-- Reporting and analytics
CREATE INDEX idx_compliance_reports_company_time ON compliance_reports (company_id, report_period_start DESC);
CREATE INDEX idx_compliance_reports_type_status ON compliance_reports (report_type, review_status);

-- External systems integration
CREATE INDEX idx_external_systems_type_status ON external_systems (system_type, status);
CREATE INDEX idx_external_systems_connection ON external_systems (connection_status, last_successful_connection DESC);

-- API webhooks
CREATE INDEX idx_api_webhooks_status ON api_webhooks (status, last_successful_delivery DESC);
CREATE INDEX idx_api_webhooks_health ON api_webhooks (health_status, last_health_check DESC);

-- JSON field optimization (MySQL 8.0+)
-- Site zones coordinates optimization
CREATE INDEX idx_site_zones_coordinates ON site_zones ((CAST(coordinates -> '$.type' AS CHAR(20))));

-- Detection results JSON optimization
CREATE INDEX idx_detection_violations_json ON detection_results ((JSON_LENGTH(safety_violations)));
CREATE INDEX idx_detection_equipment_json ON detection_results ((JSON_LENGTH(equipment_detected)));

-- Alert conditions JSON optimization
CREATE INDEX idx_alert_rules_conditions ON alert_rules ((CAST(trigger_conditions -> '$.violation_type' AS CHAR(50))));

SELECT 'Construction Management indexes created successfully!' as Status;

-- ================================================================
-- PARTITIONING SETUP FOR LARGE TABLES
-- ================================================================

-- Partition detection_results by year
ALTER TABLE detection_results 
PARTITION BY RANGE (YEAR(detection_timestamp)) (
    PARTITION p2024 VALUES LESS THAN (2025),
    PARTITION p2025 VALUES LESS THAN (2026),
    PARTITION p2026 VALUES LESS THAN (2027),
    PARTITION p2027 VALUES LESS THAN (2028),
    PARTITION p_future VALUES LESS THAN MAXVALUE
);

-- Partition alerts by year
ALTER TABLE alerts
PARTITION BY RANGE (YEAR(triggered_at)) (
    PARTITION p2024 VALUES LESS THAN (2025),
    PARTITION p2025 VALUES LESS THAN (2026),
    PARTITION p2026 VALUES LESS THAN (2027),
    PARTITION p2027 VALUES LESS THAN (2028),
    PARTITION p_future VALUES LESS THAN MAXVALUE
);

-- Partition zone_action_logs by year
ALTER TABLE zone_action_logs
PARTITION BY RANGE (YEAR(executed_at)) (
    PARTITION p2024 VALUES LESS THAN (2025),
    PARTITION p2025 VALUES LESS THAN (2026),
    PARTITION p2026 VALUES LESS THAN (2027),
    PARTITION p2027 VALUES LESS THAN (2028),
    PARTITION p_future VALUES LESS THAN MAXVALUE
);

-- Switch to VMS database for video storage partitioning
USE construction_vms;

-- Partition video_storage by year
ALTER TABLE video_storage
PARTITION BY RANGE (YEAR(start_time)) (
    PARTITION p2024 VALUES LESS THAN (2025),
    PARTITION p2025 VALUES LESS THAN (2026),
    PARTITION p2026 VALUES LESS THAN (2027),
    PARTITION p2027 VALUES LESS THAN (2028),
    PARTITION p_future VALUES LESS THAN MAXVALUE
);

SELECT 'Partitioning setup completed successfully!' as Status;
SELECT 'All indexes and optimizations created!' as FinalStatus;