"""
Pydantic schemas for request/response models
Separated from main server file for better organization
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
import uuid

# SHARED RESPONSE MODELS
class StatusCheck(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    client_name: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class StatusCheckCreate(BaseModel):
    client_name: str

# SITES SCHEMAS
class SiteResponse(BaseModel):
    id: str
    name: str
    code: str
    address: Optional[str] = None
    status: str
    type: Optional[str] = None
    phase: Optional[str] = None
    progress_percentage: Optional[float] = None
    manager_id: Optional[str] = None
    total_cameras: int = 0
    active_cameras: int = 0
    weather_condition: Optional[str] = None
    weather_temp: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class SiteCreateRequest(BaseModel):
    name: str
    code: str
    address: Optional[str] = None
    type: Optional[str] = None
    phase: Optional[str] = None
    manager_id: Optional[str] = None

# USERS SCHEMAS
class UserResponse(BaseModel):
    id: str
    username: str
    email: str
    first_name: str
    last_name: str
    display_name: Optional[str] = None
    role: str
    status: str
    department: Optional[str] = None
    phone: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

class UserCreateRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str
    department: Optional[str] = None
    phone: Optional[str] = None

# ZONES SCHEMAS
class ZoneResponse(BaseModel):
    id: str
    site_id: str
    name: str
    description: Optional[str] = None
    zone_type: str
    safety_level: str
    status: str
    capacity_limit: Optional[int] = None
    current_occupancy: int = 0
    created_at: datetime

    class Config:
        from_attributes = True

# CAMERAS SCHEMAS
class CameraResponse(BaseModel):
    id: str
    name: str
    camera_type: str
    status: str
    ip_address: Optional[str] = None
    resolution: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

# ALERTS SCHEMAS
class AlertResponse(BaseModel):
    id: str
    site_id: str
    title: str
    description: Optional[str] = None
    priority: str
    status: str
    alert_type: Optional[str] = None
    timestamp: datetime
    acknowledged_by: Optional[str] = None
    resolved_by: Optional[str] = None

    class Config:
        from_attributes = True

# AI & DETECTION SCHEMAS
class AIDetectionResponse(BaseModel):
    id: str
    camera_id: str
    site_id: str
    zone_id: Optional[str] = None
    detection_type: Optional[str] = None
    person_count: int = 0
    confidence_score: Optional[float] = None
    activity_level: Optional[str] = None
    safety_score: Optional[float] = None
    timestamp: datetime
    processed: bool = False
    alert_generated: bool = False

    class Config:
        from_attributes = True

class AIDetectionCreateRequest(BaseModel):
    camera_id: str
    site_id: str
    zone_id: Optional[str] = None
    detection_type: Optional[str] = None
    person_count: int = 0
    confidence_score: Optional[float] = None
    detection_results: Optional[dict] = None
    safety_score: Optional[float] = None

class AIModelResponse(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    model_type: Optional[str] = None
    provider: Optional[str] = None
    status: str
    accuracy_score: Optional[float] = None
    avg_processing_time_ms: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True

class AIModelCreateRequest(BaseModel):
    name: str
    description: Optional[str] = None
    model_type: Optional[str] = None
    provider: Optional[str] = None
    endpoint_url: Optional[str] = None
    confidence_threshold: Optional[float] = 0.50

# RECORDING SESSIONS SCHEMAS
class RecordingSessionResponse(BaseModel):
    id: str
    camera_id: str
    site_id: str
    session_type: str
    trigger_type: str
    status: str
    start_time: datetime
    end_time: Optional[datetime] = None
    recording_quality: Optional[str] = None
    file_size_mb: Optional[float] = None

    class Config:
        from_attributes = True

# REPORTS SCHEMAS
class ReportResponse(BaseModel):
    id: str
    site_id: str
    name: str
    description: Optional[str] = None
    report_type: str
    generation_status: str
    created_by: str
    file_url: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

class ReportCreateRequest(BaseModel):
    site_id: str
    name: str
    description: Optional[str] = None
    report_type: str
    parameters: Optional[dict] = None
    output_format: Optional[str] = "pdf"

# SYSTEM CONFIG SCHEMAS
class SystemConfigResponse(BaseModel):
    id: str
    config_key: str
    config_value: dict
    config_type: str
    description: Optional[str] = None
    category: Optional[str] = None
    is_sensitive: bool = False
    created_at: datetime

    class Config:
        from_attributes = True

class SystemConfigCreateRequest(BaseModel):
    config_key: str
    config_value: dict
    config_type: str
    description: Optional[str] = None
    category: Optional[str] = None
    is_sensitive: bool = False

# NOTIFICATIONS SCHEMAS
class NotificationResponse(BaseModel):
    id: str
    user_id: str
    title: str
    message: Optional[str] = None
    notification_type: str
    priority: str
    read_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True

class NotificationCreateRequest(BaseModel):
    user_id: str
    title: str
    message: Optional[str] = None
    notification_type: str
    priority: Optional[str] = "medium"
    related_id: Optional[str] = None
    related_type: Optional[str] = None

# VIDEO & EVIDENCE MANAGEMENT SCHEMAS
class VideoBookmarkResponse(BaseModel):
    id: str
    camera_id: str
    user_id: str
    bookmark_date: datetime
    timestamp_seconds: int
    title: str
    description: Optional[str] = None
    bookmark_type: str
    priority_level: Optional[str] = None
    status: str
    created_at: datetime

    class Config:
        from_attributes = True

class VideoBookmarkCreateRequest(BaseModel):
    camera_id: str
    bookmark_date: str  # YYYY-MM-DD format
    timestamp_seconds: int
    title: str
    description: Optional[str] = None
    bookmark_type: str
    priority_level: Optional[str] = "medium"

class VideoAccessLogResponse(BaseModel):
    id: str
    user_id: str
    camera_id: str
    session_id: str
    video_date: datetime
    access_method: str
    access_reason: str
    session_duration_minutes: Optional[int] = None
    total_video_watched_seconds: int = 0
    access_start: datetime

    class Config:
        from_attributes = True

class VideoExportResponse(BaseModel):
    id: str
    user_id: str
    camera_id: str
    source_video_date: datetime
    export_type: str
    export_format: str
    export_status: str
    export_purpose: str
    file_size_bytes: Optional[int] = None
    download_url: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

class VideoExportCreateRequest(BaseModel):
    camera_id: str
    source_video_date: str  # YYYY-MM-DD format
    start_timestamp_seconds: int
    end_timestamp_seconds: int
    export_type: str
    export_format: str
    export_purpose: str
    export_justification: str
    quality_setting: Optional[str] = "high"

class VideoQualityMetricResponse(BaseModel):
    id: str
    camera_id: str
    analysis_date: datetime
    analysis_hour: int = 0
    sharpness_score: Optional[float] = None
    brightness_score: Optional[float] = None
    forensic_quality_rating: Optional[str] = None
    lighting_condition: Optional[str] = None
    calculated_at: datetime

    class Config:
        from_attributes = True

# TIME-LAPSE & PROGRESS TRACKING SCHEMAS
class TimelapseSequenceResponse(BaseModel):
    id: str
    title: str
    site_id: str
    created_by: str
    primary_camera_id: str
    start_datetime: datetime
    end_datetime: datetime
    duration_seconds: int
    generation_status: str
    activity_score: Optional[float] = None
    quality_score: Optional[float] = None
    view_count: int = 0
    created_at: datetime

    class Config:
        from_attributes = True

class TimelapseSequenceCreateRequest(BaseModel):
    title: str
    site_id: str
    primary_camera_id: str
    start_datetime: str  # ISO format string
    end_datetime: str    # ISO format string
    description: Optional[str] = None
    compression_level: Optional[str] = "medium"
    frame_rate_fps: Optional[int] = 30

class TimelapseBookmarkResponse(BaseModel):
    id: str
    timelapse_sequence_id: str
    user_id: str
    bookmark_name: str
    timestamp_seconds: float
    bookmark_type: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True

class TimelapseBookmarkCreateRequest(BaseModel):
    timelapse_sequence_id: str
    bookmark_name: str
    timestamp_seconds: float
    description: Optional[str] = None
    bookmark_type: Optional[str] = "manual"

class ConstructionMilestoneResponse(BaseModel):
    id: str
    site_id: str
    milestone_name: str
    milestone_code: Optional[str] = None
    description: Optional[str] = None
    status: str
    completion_percentage: Optional[float] = None
    planned_completion_date: Optional[datetime] = None
    actual_completion_date: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True

class ConstructionMilestoneCreateRequest(BaseModel):
    site_id: str
    milestone_name: str
    milestone_code: Optional[str] = None
    description: Optional[str] = None
    project_phase: Optional[str] = None
    planned_start_date: Optional[str] = None    # YYYY-MM-DD format
    planned_completion_date: Optional[str] = None  # YYYY-MM-DD format

# FIELD OPERATIONS & ASSESSMENT SCHEMAS
class InspectionPathResponse(BaseModel):
    id: str
    site_id: str
    name: str
    description: Optional[str] = None
    path_type: str
    status: str
    priority: str
    created_by: str
    estimated_duration_minutes: Optional[int] = None
    waypoint_count: int = 0
    usage_count: int = 0
    completion_rate: Optional[float] = None
    is_scheduled: bool = False
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class InspectionPathCreateRequest(BaseModel):
    site_id: str
    name: str
    description: Optional[str] = None
    path_type: str
    priority: Optional[str] = "medium"
    assigned_to: Optional[str] = None
    estimated_duration_minutes: Optional[int] = None
    zone_coverage: Optional[list] = None
    is_scheduled: Optional[bool] = False
    schedule_frequency: Optional[str] = None

class PathWaypointResponse(BaseModel):
    id: str
    path_id: str
    waypoint_order: int
    waypoint_name: str
    description: Optional[str] = None
    coordinates_x: float
    coordinates_y: float
    waypoint_type: str
    is_mandatory: bool = True
    estimated_time_minutes: int = 5
    safety_level: str
    visit_count: int = 0
    created_at: datetime

    class Config:
        from_attributes = True

class PathWaypointCreateRequest(BaseModel):
    path_id: str
    waypoint_order: int
    waypoint_name: str
    description: Optional[str] = None
    coordinates_x: float
    coordinates_y: float
    waypoint_type: str
    zone_id: Optional[str] = None
    is_mandatory: Optional[bool] = True
    estimated_time_minutes: Optional[int] = 5
    inspection_checklist: Optional[dict] = None

class PathExecutionResponse(BaseModel):
    id: str
    path_id: str
    executor_id: str
    session_id: str
    execution_type: str
    execution_status: str
    started_at: datetime
    completed_at: Optional[datetime] = None
    completion_percentage: Optional[float] = None
    quality_score: Optional[float] = None
    issues_found: int = 0
    safety_incidents: int = 0
    compliance_score: Optional[float] = None
    is_completed: bool = False
    created_at: datetime

    class Config:
        from_attributes = True

class PathExecutionCreateRequest(BaseModel):
    path_id: str
    execution_type: str
    execution_reason: Optional[str] = None
    planned_duration_minutes: Optional[int] = None
    weather_conditions: Optional[str] = None
    equipment_used: Optional[list] = None

class PathExecutionWaypointResponse(BaseModel):
    id: str
    execution_id: str
    waypoint_id: str
    visited_at: Optional[datetime] = None
    time_spent_minutes: Optional[float] = None
    is_skipped: bool = False
    inspection_completed: bool = False
    issues_found: int = 0
    photos_taken: int = 0
    ppe_compliance: bool = True
    safety_protocol_followed: bool = True
    requires_follow_up: bool = False
    created_at: datetime

    class Config:
        from_attributes = True

class PathTemplateResponse(BaseModel):
    id: str
    template_name: str
    description: Optional[str] = None
    template_type: str
    difficulty_level: str
    safety_level: str
    base_waypoint_count: Optional[int] = None
    estimated_duration_minutes: Optional[int] = None
    usage_count: int = 0
    success_rate: Optional[float] = None
    user_rating: Optional[float] = None
    is_public: bool = True
    is_active: bool = True
    created_at: datetime

    class Config:
        from_attributes = True

class PathTemplateCreateRequest(BaseModel):
    template_name: str
    description: Optional[str] = None
    template_type: str
    difficulty_level: Optional[str] = "basic"
    safety_level: Optional[str] = "medium"
    base_waypoint_count: Optional[int] = None
    estimated_duration_minutes: Optional[int] = None
    recommended_zones: Optional[list] = None
    required_equipment: Optional[list] = None
    is_public: Optional[bool] = True


# NAVIGATION & STREET VIEW SCHEMAS

class NavigationRouteResponse(BaseModel):
    id: str
    site_id: str
    route_name: str
    route_code: Optional[str] = None
    description: Optional[str] = None
    route_type: str
    purpose: Optional[str] = None
    priority_level: str
    start_coordinates: dict
    end_coordinates: dict
    total_distance_meters: float
    estimated_duration_minutes: int
    safety_rating: str
    accessibility_level: str
    usage_count: int = 0
    completion_rate: Optional[float] = None
    route_condition: str
    status: str
    created_by: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class NavigationRouteCreateRequest(BaseModel):
    site_id: str
    route_name: str
    route_code: Optional[str] = None
    description: Optional[str] = None
    route_type: str
    purpose: Optional[str] = None
    priority_level: Optional[str] = "medium"
    start_coordinates: dict  # {lat: float, lng: float, elevation: float}
    end_coordinates: dict
    total_distance_meters: float
    estimated_duration_minutes: int
    elevation_change_meters: Optional[float] = 0
    difficulty_level: Optional[str] = "easy"
    safety_rating: Optional[str] = "safe"
    accessibility_level: Optional[str] = "walking"
    ppe_requirements: Optional[list] = None
    hazard_warnings: Optional[list] = None

class RouteWaypointResponse(BaseModel):
    id: str
    route_id: str
    waypoint_name: str
    waypoint_code: Optional[str] = None
    sequence_order: int
    latitude: float
    longitude: float
    elevation: Optional[float] = None
    waypoint_type: str
    action_required: str
    approach_instructions: str
    safety_level: str
    monitoring_required: bool = False
    photo_documentation_required: bool = False
    completion_rate: Optional[float] = None
    condition_status: str
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class RouteWaypointCreateRequest(BaseModel):
    route_id: str
    waypoint_name: str
    waypoint_code: Optional[str] = None
    sequence_order: int
    latitude: float
    longitude: float
    elevation: Optional[float] = 0
    waypoint_type: str
    action_required: Optional[str] = "pass_through"
    approach_instructions: str
    departure_instructions: Optional[str] = None
    safety_level: Optional[str] = "safe"
    hazard_types: Optional[list] = None
    associated_camera_ids: Optional[list] = None
    monitoring_required: Optional[bool] = False
    photo_documentation_required: Optional[bool] = False

class NavigationSessionResponse(BaseModel):
    id: str
    user_id: str
    route_id: str
    session_name: Optional[str] = None
    session_purpose: str
    started_at: datetime
    ended_at: Optional[datetime] = None
    total_duration_minutes: Optional[float] = None
    session_status: str
    completion_percentage: Optional[float] = None
    waypoints_completed: int = 0
    waypoints_skipped: int = 0
    total_waypoints: int
    total_distance_traveled_meters: Optional[float] = None
    safety_incidents: int = 0
    navigation_accuracy_score: Optional[float] = None
    overall_session_rating: Optional[float] = None
    supervisor_review_required: bool = False
    approved: bool = False
    archived: bool = False

    class Config:
        from_attributes = True

class NavigationSessionCreateRequest(BaseModel):
    user_id: str
    route_id: str
    session_name: Optional[str] = None
    session_purpose: str
    planned_duration_minutes: Optional[int] = None
    total_waypoints: int
    device_type: Optional[str] = None
    device_id: Optional[str] = None
    weather_conditions: Optional[dict] = None

class StreetViewCameraResponse(BaseModel):
    id: str
    camera_id: str
    is_street_view_enabled: bool = False
    street_view_priority: int = 1
    field_of_view_degrees: int = 90
    ptz_enabled: bool = False
    streaming_resolution: str = "1080p"
    streaming_fps: int = 30
    ai_detection_enabled: bool = True
    precise_latitude: Optional[float] = None
    precise_longitude: Optional[float] = None
    mounting_height_meters: Optional[float] = None
    coverage_radius_meters: Optional[float] = None
    health_status: str
    uptime_percentage: Optional[float] = None
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class StreetViewCameraCreateRequest(BaseModel):
    camera_id: str
    is_street_view_enabled: Optional[bool] = False
    street_view_priority: Optional[int] = 1
    field_of_view_degrees: Optional[int] = 90
    ptz_enabled: Optional[bool] = False
    streaming_resolution: Optional[str] = "1080p"
    streaming_fps: Optional[int] = 30
    ai_detection_enabled: Optional[bool] = True
    precise_latitude: Optional[float] = None
    precise_longitude: Optional[float] = None
    mounting_height_meters: Optional[float] = None
    orientation_degrees: Optional[float] = None
    route_coverage: Optional[list] = None
    waypoint_coverage: Optional[list] = None


# COMPLETE ANALYTICS & REPORTING SCHEMAS

class UserCertificationResponse(BaseModel):
    id: str
    user_id: str
    certification_name: str
    certification_type: str
    certification_number: Optional[str] = None
    issuing_authority: Optional[str] = None
    issue_date: datetime
    expiry_date: Optional[datetime] = None
    status: str
    verification_status: str
    renewal_required: bool = True
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class UserCertificationCreateRequest(BaseModel):
    user_id: str
    certification_name: str
    certification_type: str
    certification_number: Optional[str] = None
    issuing_authority: Optional[str] = None
    issue_date: str  # YYYY-MM-DD format
    expiry_date: Optional[str] = None  # YYYY-MM-DD format
    renewal_period_months: Optional[int] = None
    required_for_roles: Optional[list] = None
    certificate_file_path: Optional[str] = None

class PerformanceMetricResponse(BaseModel):
    id: str
    site_id: str
    metric_date: datetime
    metric_hour: Optional[int] = None
    metric_type: str
    metric_value: float
    target_value: Optional[float] = None
    measurement_unit: Optional[str] = None
    is_kpi: bool = False
    trend_direction: Optional[str] = None
    performance_grade: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

class PerformanceMetricCreateRequest(BaseModel):
    site_id: str
    metric_date: str  # YYYY-MM-DD format
    metric_hour: Optional[int] = None
    metric_type: str
    metric_value: float
    target_value: Optional[float] = None
    measurement_unit: Optional[str] = None
    data_source: Optional[str] = None
    is_kpi: Optional[bool] = False
    confidence_score: Optional[float] = None

class TrendAnalysisResponse(BaseModel):
    id: str
    site_id: Optional[str] = None
    analysis_name: str
    analysis_type: str
    start_date: datetime
    end_date: datetime
    trend_direction: Optional[str] = None
    trend_strength: Optional[float] = None
    starting_value: Optional[float] = None
    ending_value: Optional[float] = None
    change_percentage: Optional[float] = None
    created_at: datetime
    created_by: str

    class Config:
        from_attributes = True

class TrendAnalysisCreateRequest(BaseModel):
    site_id: Optional[str] = None
    analysis_name: str
    analysis_type: str
    start_date: str  # YYYY-MM-DD format
    end_date: str    # YYYY-MM-DD format
    analysis_algorithm: Optional[str] = "linear_regression"
    forecast_horizon_days: Optional[int] = 30

class ReportTemplateResponse(BaseModel):
    id: str
    template_name: str
    template_type: str
    description: Optional[str] = None
    template_structure: dict
    is_public: bool = False
    usage_count: int = 0
    is_active: bool = True
    created_by: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ReportTemplateCreateRequest(BaseModel):
    template_name: str
    template_type: str
    description: Optional[str] = None
    template_structure: dict
    default_parameters: Optional[dict] = None
    required_parameters: Optional[list] = None
    supported_formats: Optional[list] = None
    is_public: Optional[bool] = False

class DashboardWidgetResponse(BaseModel):
    id: str
    user_id: str
    widget_name: str
    widget_type: str
    widget_config: dict
    data_source: str
    dashboard_tab: str = "main"
    position_x: int = 0
    position_y: int = 0
    width: int = 4
    height: int = 3
    is_visible: bool = True
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class DashboardWidgetCreateRequest(BaseModel):
    user_id: str
    widget_name: str
    widget_type: str
    widget_config: dict
    data_source: str
    dashboard_tab: Optional[str] = "main"
    position_x: Optional[int] = 0
    position_y: Optional[int] = 0
    width: Optional[int] = 4
    height: Optional[int] = 3
    refresh_interval_minutes: Optional[int] = 15

# ADMIN DASHBOARD & SYSTEM MANAGEMENT SCHEMAS

class AdminDashboardMetricResponse(BaseModel):
    id: str
    metric_date: datetime
    metric_hour: Optional[int] = None
    aggregation_level: str
    total_users: int = 0
    active_users_24h: int = 0
    total_sites: int = 0
    active_sites: int = 0
    total_cameras: int = 0
    online_cameras: int = 0
    system_uptime_percentage: Optional[float] = None
    avg_response_time_ms: int = 0
    overall_safety_score: Optional[float] = None
    ai_model_accuracy_avg: Optional[float] = None
    created_at: datetime
    calculated_at: datetime

    class Config:
        from_attributes = True

class AdminDashboardMetricCreateRequest(BaseModel):
    metric_date: str  # YYYY-MM-DD format
    metric_hour: Optional[int] = None
    aggregation_level: str
    total_users: Optional[int] = 0
    active_users_24h: Optional[int] = 0
    total_sites: Optional[int] = 0
    active_sites: Optional[int] = 0
    total_cameras: Optional[int] = 0
    online_cameras: Optional[int] = 0

class SitePerformanceSummaryResponse(BaseModel):
    id: str
    site_id: str
    summary_date: datetime
    summary_period: str
    personnel_count: int = 0
    active_personnel: int = 0
    camera_count: int = 0
    online_cameras: int = 0
    site_uptime_percentage: Optional[float] = None
    safety_score: Optional[float] = None
    compliance_score: Optional[float] = None
    alerts_generated: int = 0
    alerts_resolved: int = 0
    total_detections: int = 0
    performance_trend: str
    safety_trend: str
    efficiency_score: Optional[float] = None
    created_at: datetime

    class Config:
        from_attributes = True

class SitePerformanceSummaryCreateRequest(BaseModel):
    site_id: str
    summary_date: str  # YYYY-MM-DD format
    summary_period: str
    personnel_count: Optional[int] = 0
    camera_count: Optional[int] = 0
    online_cameras: Optional[int] = 0
    safety_score: Optional[float] = None
    notes: Optional[str] = None

class SystemHealthLogResponse(BaseModel):
    id: str
    server_id: str
    component_type: str
    measurement_timestamp: datetime
    cpu_usage_percentage: Optional[float] = None
    memory_usage_percentage: Optional[float] = None
    disk_usage_percentage: Optional[float] = None
    response_time_ms: Optional[int] = None
    service_status: str
    error_count: int = 0
    requires_attention: bool = False
    created_at: datetime

    class Config:
        from_attributes = True

class SystemHealthLogCreateRequest(BaseModel):
    server_id: str
    component_type: str
    cpu_usage_percentage: Optional[float] = None
    memory_usage_percentage: Optional[float] = None
    disk_usage_percentage: Optional[float] = None
    response_time_ms: Optional[int] = None
    service_status: Optional[str] = "healthy"
    monitoring_source: Optional[str] = None

class AdminActivityLogResponse(BaseModel):
    id: str
    admin_user_id: str
    activity_type: str
    action: str
    resource_type: Optional[str] = None
    resource_id: Optional[str] = None
    resource_name: Optional[str] = None
    change_summary: Optional[str] = None
    site_id: Optional[str] = None
    ip_address: str
    impact_level: str
    action_status: str
    created_at: datetime

    class Config:
        from_attributes = True

class AdminActivityLogCreateRequest(BaseModel):
    admin_user_id: str
    activity_type: str
    action: str
    resource_type: Optional[str] = None
    resource_id: Optional[str] = None
    resource_name: Optional[str] = None
    old_values: Optional[dict] = None
    new_values: Optional[dict] = None
    change_summary: Optional[str] = None
    ip_address: str
    impact_level: Optional[str] = "medium"

class ExecutiveReportResponse(BaseModel):
    id: str
    report_name: str
    report_type: str
    reporting_period_start: datetime
    reporting_period_end: datetime
    generated_by: str
    generation_timestamp: datetime
    report_status: str
    executive_summary: Optional[str] = None
    confidentiality_level: str
    report_file_path: Optional[str] = None
    report_file_format: str
    version: str = "1.0"
    is_automated: bool = False
    view_count: int = 0
    download_count: int = 0
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ExecutiveReportCreateRequest(BaseModel):
    report_name: str
    report_type: str
    reporting_period_start: str  # YYYY-MM-DD format
    reporting_period_end: str    # YYYY-MM-DD format
    generated_by: str
    executive_summary: Optional[str] = None
    included_sites: Optional[list] = None
    confidentiality_level: Optional[str] = "internal"
    report_file_format: Optional[str] = "pdf"