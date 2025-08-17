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


# USER MANAGEMENT & ADMINISTRATION SCHEMAS

class UserManagementProfileResponse(BaseModel):
    id: str
    user_id: str
    employee_number: Optional[str] = None
    badge_number: Optional[str] = None
    date_of_birth: Optional[datetime] = None
    gender: Optional[str] = None
    position_title: Optional[str] = None
    position_level: Optional[str] = None
    employment_type: Optional[str] = None
    employment_status: Optional[str] = None
    start_date: datetime
    skills: Optional[list] = None
    ui_theme: str = "default"
    language_preference: str = "en"
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class UserManagementProfileCreateRequest(BaseModel):
    user_id: str
    employee_number: Optional[str] = None
    badge_number: Optional[str] = None
    position_title: Optional[str] = None
    position_level: Optional[str] = None
    employment_type: Optional[str] = None
    employment_status: Optional[str] = "active"
    start_date: str  # YYYY-MM-DD
    skills: Optional[list] = None
    notification_preferences: Optional[dict] = None

class UserRoleAssignmentResponse(BaseModel):
    id: str
    user_id: str
    role_type: str
    role_name: str
    role_description: Optional[str] = None
    site_id: Optional[str] = None
    access_level: str
    assignment_status: str
    effective_from: datetime
    effective_until: Optional[datetime] = None
    is_primary_role: bool = False
    assigned_by: str
    created_at: datetime

    class Config:
        from_attributes = True

class UserRoleAssignmentCreateRequest(BaseModel):
    user_id: str
    role_type: str
    role_name: str
    role_description: Optional[str] = None
    site_id: Optional[str] = None
    access_level: Optional[str] = "read"
    effective_from: str  # YYYY-MM-DD
    effective_until: Optional[str] = None
    permissions: Optional[list] = None
    is_primary_role: Optional[bool] = False

class UserSessionManagementResponse(BaseModel):
    id: str
    user_id: str
    session_id: str
    login_timestamp: datetime
    logout_timestamp: Optional[datetime] = None
    last_activity: datetime
    is_active: bool = True
    ip_address: str
    access_method: str
    authentication_method: str
    mfa_verified: bool = False
    page_views: int = 0
    api_calls: int = 0
    created_at: datetime

    class Config:
        from_attributes = True

class UserSessionManagementCreateRequest(BaseModel):
    user_id: str
    session_id: str
    session_token: str
    ip_address: str
    access_method: Optional[str] = "web"
    authentication_method: Optional[str] = "password"
    device_info: Optional[dict] = None
    browser_info: Optional[dict] = None

class UserActivityTrackingResponse(BaseModel):
    id: str
    user_id: str
    session_id: str
    activity_type: str
    activity_description: str
    resource_type: Optional[str] = None
    resource_id: Optional[str] = None
    site_id: Optional[str] = None
    activity_timestamp: datetime
    security_level: str
    requires_audit: bool = True
    created_at: datetime

    class Config:
        from_attributes = True

class UserActivityTrackingCreateRequest(BaseModel):
    user_id: str
    session_id: str
    activity_type: str
    activity_description: str
    activity_category: Optional[str] = None
    resource_type: Optional[str] = None
    resource_id: Optional[str] = None
    site_id: Optional[str] = None
    request_method: Optional[str] = None
    security_level: Optional[str] = "internal"

# ACCESS CONTROL & SECURITY MANAGEMENT SCHEMAS

class AccessControlRoleResponse(BaseModel):
    id: str
    role_name: str
    role_code: str
    description: str
    role_level: str
    risk_level: str
    color_code: str = "#6B7280"
    parent_role_id: Optional[str] = None
    site_access_type: str = "assigned_sites"
    is_active: bool = True
    user_count: int = 0
    created_by: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class AccessControlRoleCreateRequest(BaseModel):
    role_name: str
    role_code: str
    description: str
    role_level: str
    risk_level: str
    color_code: Optional[str] = "#6B7280"
    parent_role_id: Optional[str] = None
    site_access_type: Optional[str] = "assigned_sites"
    default_site_assignments: Optional[list] = None
    is_assignable: Optional[bool] = True

class SystemPermissionResponse(BaseModel):
    id: str
    permission_name: str
    permission_code: str
    description: str
    category: str
    subcategory: Optional[str] = None
    risk_level: str
    resource_scope: str
    operation_type: str
    is_assignable: bool = True
    requires_mfa: bool = False
    usage_count: int = 0
    created_by: str
    created_at: datetime

    class Config:
        from_attributes = True

class SystemPermissionCreateRequest(BaseModel):
    permission_name: str
    permission_code: str
    description: str
    category: str
    subcategory: Optional[str] = None
    risk_level: str
    resource_scope: str
    operation_type: str
    is_assignable: Optional[bool] = True
    requires_mfa: Optional[bool] = False

class SecurityPolicyResponse(BaseModel):
    id: str
    policy_name: str
    policy_code: str
    description: str
    category: str
    policy_type: str
    policy_rules: dict
    enforcement_level: str = "blocking"
    is_mandatory: bool = True
    is_active: bool = True
    violation_count: int = 0
    created_by: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class SecurityPolicyCreateRequest(BaseModel):
    policy_name: str
    policy_code: str
    description: str
    category: str
    policy_type: str
    policy_rules: dict
    enforcement_level: Optional[str] = "blocking"
    is_mandatory: Optional[bool] = True
    applies_to_roles: Optional[list] = None

class AccessControlAuditLogResponse(BaseModel):
    id: str
    event_type: str
    event_category: str
    user_id: Optional[str] = None
    target_user_id: Optional[str] = None
    action_performed: str
    resource_type: Optional[str] = None
    site_id: Optional[str] = None
    access_granted: Optional[bool] = None
    denial_reason: Optional[str] = None
    violation_severity: Optional[str] = None
    ip_address: Optional[str] = None
    event_timestamp: datetime

    class Config:
        from_attributes = True

class AccessControlAuditLogCreateRequest(BaseModel):
    event_type: str
    event_category: str
    user_id: Optional[str] = None
    target_user_id: Optional[str] = None
    action_performed: str
    resource_type: Optional[str] = None
    site_id: Optional[str] = None
    access_granted: Optional[bool] = None
    denial_reason: Optional[str] = None
    ip_address: Optional[str] = None

# AI MODEL MANAGEMENT & DEPLOYMENT SCHEMAS

class AIModelResponse(BaseModel):
    id: str
    name: str
    model_type: str
    category: str
    version: str
    description: Optional[str] = None
    framework: Optional[str] = None
    model_file_path: str
    model_file_size_mb: Optional[float] = None
    baseline_accuracy: Optional[float] = None
    inference_time_ms: Optional[float] = None
    status: str = "development"
    lifecycle_stage: str = "experimental"
    approval_status: str = "pending"
    created_by: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class AIModelCreateRequest(BaseModel):
    name: str
    model_type: str
    category: str
    version: str
    description: Optional[str] = None
    framework: Optional[str] = None
    model_file_path: str
    training_dataset_info: Optional[dict] = None
    baseline_accuracy: Optional[float] = None
    license_type: Optional[str] = None

class ModelDeploymentResponse(BaseModel):
    id: str
    model_id: str
    site_id: str
    deployment_name: str
    deployment_status: str = "pending"
    deployment_type: str = "production"
    confidence_threshold: float
    batch_size: int
    auto_scaling_enabled: bool = False
    monitoring_enabled: bool = True
    deployed_by: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ModelDeploymentCreateRequest(BaseModel):
    model_id: str
    site_id: str
    deployment_name: str
    deployment_type: Optional[str] = "production"
    confidence_threshold: float
    batch_size: int
    processing_interval_seconds: Optional[int] = 1
    auto_scaling_enabled: Optional[bool] = False
    monitoring_enabled: Optional[bool] = True

class ModelTrainingJobResponse(BaseModel):
    id: str
    model_id: str
    job_name: str
    training_type: str
    job_status: str = "queued"
    progress_percentage: Optional[float] = 0.0
    current_epoch: int = 0
    current_accuracy: Optional[float] = None
    best_accuracy: Optional[float] = None
    estimated_total_cost: Optional[float] = None
    created_by: str
    created_at: datetime

    class Config:
        from_attributes = True

class ModelTrainingJobCreateRequest(BaseModel):
    model_id: str
    job_name: str
    training_type: str
    job_description: Optional[str] = None
    base_model_id: Optional[str] = None
    epochs: Optional[int] = 100
    batch_size: Optional[int] = 32
    learning_rate: Optional[float] = 0.001
    cost_budget_limit: Optional[float] = None

class ModelEvaluationResultResponse(BaseModel):
    id: str
    model_id: str
    evaluation_name: str
    evaluation_type: str
    evaluation_date: datetime
    overall_accuracy: Optional[float] = None
    overall_f1_score: Optional[float] = None
    business_accuracy_score: Optional[float] = None
    review_status: str = "pending"
    approval_for_production: bool = False
    evaluated_by: str
    created_at: datetime

    class Config:
        from_attributes = True

class ModelEvaluationResultCreateRequest(BaseModel):
    model_id: str
    evaluation_name: str
    evaluation_type: str
    dataset_size: Optional[int] = None
    overall_accuracy: Optional[float] = None
    overall_precision: Optional[float] = None
    overall_recall: Optional[float] = None
    overall_f1_score: Optional[float] = None
    business_accuracy_score: Optional[float] = None


# SITE CONFIGURATION & INFRASTRUCTURE SCHEMAS

class SiteConfigurationResponse(BaseModel):
    id: str
    site_id: str
    timezone: str = "America/New_York"
    working_hours_start: Optional[str] = None  # Time field as string
    working_hours_end: Optional[str] = None    # Time field as string
    max_occupancy: int = 100
    safety_level: str = "standard"
    ai_detection_enabled: bool = True
    ai_sensitivity_level: str = "medium"
    recording_retention_days: int = 30
    recording_quality: str = "high"
    alert_notifications_enabled: bool = True
    access_control_type: str = "keycard"
    configured_by: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class SiteConfigurationCreateRequest(BaseModel):
    site_id: str
    timezone: Optional[str] = "America/New_York"
    working_hours_start: Optional[str] = None  # "HH:MM" format
    working_hours_end: Optional[str] = None    # "HH:MM" format
    max_occupancy: Optional[int] = 100
    safety_level: Optional[str] = "standard"
    ai_detection_enabled: Optional[bool] = True
    ai_sensitivity_level: Optional[str] = "medium"
    recording_retention_days: Optional[int] = 30
    recording_quality: Optional[str] = "high"
    alert_notifications_enabled: Optional[bool] = True
    access_control_type: Optional[str] = "keycard"
    emergency_contacts: Optional[list] = None
    safety_protocols: Optional[list] = None

class SiteInfrastructureResponse(BaseModel):
    id: str
    site_id: str
    network_status: str = "fair"
    internet_speed_mbps: Optional[int] = None
    network_provider: Optional[str] = None
    power_status: str = "stable"
    backup_power_available: bool = False
    cellular_coverage: str = "good"
    uptime_percentage: Optional[float] = 100.0
    storage_capacity_tb: Optional[float] = None
    cloud_storage_enabled: bool = True
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class SiteInfrastructureCreateRequest(BaseModel):
    site_id: str
    network_status: Optional[str] = "fair"
    internet_speed_mbps: Optional[int] = None
    network_provider: Optional[str] = None
    power_status: Optional[str] = "stable"
    backup_power_available: Optional[bool] = False
    cellular_coverage: Optional[str] = "good"
    storage_capacity_tb: Optional[float] = None
    cloud_storage_enabled: Optional[bool] = True
    environmental_sensors: Optional[list] = None

class SiteZoneConfigurationResponse(BaseModel):
    id: str
    site_id: str
    zone_id: str
    monitoring_level: str = "standard"
    camera_coverage_percentage: Optional[float] = 0.0
    max_personnel: Optional[int] = None
    safety_score: Optional[float] = 100.0
    compliance_score: Optional[float] = 100.0
    zone_status: str = "active"
    configured_by: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class SiteZoneConfigurationCreateRequest(BaseModel):
    site_id: str
    zone_id: str
    monitoring_level: Optional[str] = "standard"
    max_personnel: Optional[int] = None
    authorized_roles: Optional[list] = None
    ppe_requirements: Optional[list] = None
    detection_sensitivity: Optional[str] = "medium"
    safety_requirements: Optional[list] = None

class SitePerformanceTrackingResponse(BaseModel):
    id: str
    site_id: str
    tracking_date: datetime
    tracking_period: str
    system_health_score: Optional[float] = 100.0
    uptime_percentage: Optional[float] = 100.0
    safety_incident_count: int = 0
    compliance_score: Optional[float] = 100.0
    performance_trend: str = "stable"
    health_trend: str = "stable"
    created_at: datetime

    class Config:
        from_attributes = True

class SitePerformanceTrackingCreateRequest(BaseModel):
    site_id: str
    tracking_date: str  # YYYY-MM-DD format
    tracking_period: str
    system_health_score: Optional[float] = 100.0
    uptime_percentage: Optional[float] = 100.0
    safety_incident_count: Optional[int] = 0
    compliance_score: Optional[float] = 100.0
    performance_notes: Optional[str] = None

class SiteComplianceTrackingResponse(BaseModel):
    id: str
    site_id: str
    compliance_framework: str
    compliance_date: datetime
    overall_compliance_score: float
    compliance_status: str = "compliant"
    audit_type: str
    audit_date: datetime
    total_findings: int = 0
    safety_compliance_score: Optional[float] = 100.0
    reported_by: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class SiteComplianceTrackingCreateRequest(BaseModel):
    site_id: str
    compliance_framework: str
    compliance_date: str  # YYYY-MM-DD format
    overall_compliance_score: float
    audit_type: str
    audit_date: str  # YYYY-MM-DD format
    auditor_name: Optional[str] = None
    total_findings: Optional[int] = 0
    safety_compliance_score: Optional[float] = 100.0

# SYSTEM MONITORING & INFRASTRUCTURE HEALTH SCHEMAS

class SystemHealthMonitoringResponse(BaseModel):
    id: str
    timestamp: datetime
    overall_health_score: float
    system_status: str = "healthy"
    availability_percentage: Optional[float] = 100.0
    total_services_count: int = 0
    healthy_services_count: int = 0
    warning_services_count: int = 0
    critical_services_count: int = 0
    health_trend: str = "stable"
    performance_trend: str = "stable"
    created_at: datetime

    class Config:
        from_attributes = True

class SystemHealthMonitoringCreateRequest(BaseModel):
    overall_health_score: float
    system_status: Optional[str] = "healthy"
    availability_percentage: Optional[float] = 100.0
    total_services_count: Optional[int] = 0
    healthy_services_count: Optional[int] = 0
    warning_services_count: Optional[int] = 0
    critical_services_count: Optional[int] = 0
    monitoring_interval_minutes: Optional[int] = 5

class ServiceHealthMetricResponse(BaseModel):
    id: str
    service_name: str
    service_type: str
    timestamp: datetime
    service_status: str = "healthy"
    uptime_percentage: Optional[float] = 100.0
    response_time_avg_ms: Optional[float] = None
    success_rate_percentage: Optional[float] = 100.0
    cpu_utilization_percentage: Optional[float] = None
    memory_utilization_percentage: Optional[float] = None
    error_rate_percentage: Optional[float] = 0.0
    created_at: datetime

    class Config:
        from_attributes = True

class ServiceHealthMetricCreateRequest(BaseModel):
    service_name: str
    service_type: str
    service_status: Optional[str] = "healthy"
    uptime_percentage: Optional[float] = 100.0
    response_time_avg_ms: Optional[float] = None
    success_rate_percentage: Optional[float] = 100.0
    cpu_utilization_percentage: Optional[float] = None
    memory_utilization_percentage: Optional[float] = None

class SystemAlertResponse(BaseModel):
    id: str
    alert_id: str
    alert_level: str
    alert_category: str
    alert_type: str
    alert_source: str
    title: str
    message: str
    triggered_at: datetime
    status: str = "active"
    business_impact: str = "none"
    assigned_to: Optional[str] = None
    resolved_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class SystemAlertCreateRequest(BaseModel):
    alert_id: str
    alert_level: str
    alert_category: str
    alert_type: str
    alert_source: str
    title: str
    message: str
    triggered_at: Optional[str] = None  # ISO datetime string
    business_impact: Optional[str] = "none"
    detailed_description: Optional[str] = None
    recommended_actions: Optional[list] = None

class MonitoringDashboardResponse(BaseModel):
    id: str
    dashboard_name: str
    dashboard_type: str
    created_by: str
    refresh_interval_seconds: int = 30
    auto_refresh_enabled: bool = True
    is_public: bool = False
    view_count: int = 0
    widget_count: int = 0
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class MonitoringDashboardCreateRequest(BaseModel):
    dashboard_name: str
    dashboard_type: str
    created_by: str
    layout_config: Optional[dict] = None
    refresh_interval_seconds: Optional[int] = 30
    auto_refresh_enabled: Optional[bool] = True
    is_public: Optional[bool] = False
    widgets: Optional[list] = None

# INTEGRATION & USER EXPERIENCE SCHEMAS

class ThirdPartyIntegrationResponse(BaseModel):
    id: str
    integration_name: str
    integration_type: str
    provider_name: str
    description: Optional[str] = None
    status: str = "pending"
    health_score: Optional[float] = 0.0
    monthly_usage: int = 0
    error_rate: Optional[float] = 0.0
    created_by: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ThirdPartyIntegrationCreateRequest(BaseModel):
    integration_name: str
    integration_type: str
    provider_name: str
    description: Optional[str] = None
    configuration: dict
    endpoints: Optional[dict] = None
    rate_limits: Optional[dict] = None
    monthly_limit: Optional[int] = None

class UserProfileSettingResponse(BaseModel):
    id: str
    user_id: str
    profile_picture_url: Optional[str] = None
    bio: Optional[str] = None
    preferences: Optional[dict] = None
    notification_settings: Optional[dict] = None
    dashboard_config: Optional[dict] = None
    theme_settings: Optional[dict] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class UserProfileSettingCreateRequest(BaseModel):
    user_id: str
    profile_picture_url: Optional[str] = None
    bio: Optional[str] = None
    preferences: Optional[dict] = None
    notification_settings: Optional[dict] = None
    dashboard_config: Optional[dict] = None
    theme_settings: Optional[dict] = None

class UserApplicationSettingResponse(BaseModel):
    id: str
    user_id: str
    language: str = "en"
    timezone: Optional[str] = None
    time_format: str = "12h"
    theme: str = "light"
    font_size: str = "medium"
    notifications_enabled: bool = True
    email_notifications: bool = True
    quiet_hours_enabled: bool = False
    data_sharing_enabled: bool = True
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class UserApplicationSettingCreateRequest(BaseModel):
    user_id: str
    language: Optional[str] = "en"
    timezone: Optional[str] = None
    time_format: Optional[str] = "12h"
    theme: Optional[str] = "light"
    font_size: Optional[str] = "medium"
    notifications_enabled: Optional[bool] = True
    email_notifications: Optional[bool] = True
    quiet_hours_enabled: Optional[bool] = False

class HelpArticleResponse(BaseModel):
    id: str
    title: str
    content: str
    category: str
    subcategory: Optional[str] = None
    tags: Optional[list] = None
    author_id: str
    is_published: bool = False
    view_count: int = 0
    helpful_count: int = 0
    unhelpful_count: int = 0
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class HelpArticleCreateRequest(BaseModel):
    title: str
    content: str
    category: str
    subcategory: Optional[str] = None
    tags: Optional[list] = None
    is_published: Optional[bool] = False
    search_keywords: Optional[str] = None

class UserFeedbackResponse(BaseModel):
    id: str
    user_id: str
    feedback_type: str
    title: str
    description: str
    priority: str = "medium"
    status: str = "submitted"
    category: Optional[str] = None
    upvote_count: int = 0
    admin_response: Optional[str] = None
    responded_by: Optional[str] = None
    responded_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class UserFeedbackCreateRequest(BaseModel):
    user_id: str
    feedback_type: str
    title: str
    description: str
    priority: Optional[str] = "medium"
    category: Optional[str] = None
    attachments: Optional[list] = None


# STREET VIEW COMPARISON & ANALYSIS SCHEMAS

class StreetViewComparisonResponse(BaseModel):
    id: str
    session_before_id: str
    session_after_id: str
    site_id: str
    location_zone: Optional[str] = None
    comparison_type: str
    timespan_days: int
    overall_progress_percentage: Optional[float] = None
    construction_growth: Optional[float] = None
    equipment_changes_count: int = 0
    safety_improvements_count: int = 0
    personnel_variation_percentage: Optional[float] = None
    analysis_status: str = "pending"
    processing_time_seconds: Optional[int] = None
    error_message: Optional[str] = None
    created_by: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class StreetViewComparisonCreateRequest(BaseModel):
    session_before_id: str
    session_after_id: str
    site_id: str
    location_zone: Optional[str] = None
    comparison_type: str
    timespan_days: int

class StreetViewSessionResponse(BaseModel):
    id: str
    site_id: str
    camera_id: str
    session_label: str
    session_date: str
    session_time: str
    location_coordinates_x: Optional[float] = None
    location_coordinates_y: Optional[float] = None
    heading_degrees: Optional[float] = None
    weather_conditions: Optional[str] = None
    recording_quality: str = "high"
    file_path: Optional[str] = None
    file_size_mb: Optional[float] = None
    duration_seconds: Optional[int] = None
    created_by: str
    created_at: datetime

    class Config:
        from_attributes = True

class StreetViewSessionCreateRequest(BaseModel):
    site_id: str
    camera_id: str
    session_label: str
    session_date: str
    session_time: str
    location_coordinates_x: Optional[float] = None
    location_coordinates_y: Optional[float] = None
    heading_degrees: Optional[float] = None
    weather_conditions: Optional[str] = None
    recording_quality: Optional[str] = "high"
    file_path: Optional[str] = None
    file_size_mb: Optional[float] = None
    duration_seconds: Optional[int] = None

class DetectedChangeResponse(BaseModel):
    id: str
    comparison_id: str
    change_type: str
    severity: str
    description: str
    location_name: Optional[str] = None
    location_coordinates_x: Optional[float] = None
    location_coordinates_y: Optional[float] = None
    confidence_percentage: float
    impact_description: Optional[str] = None
    ai_model_version: Optional[str] = None
    detection_algorithm: Optional[str] = None
    reviewed_by: Optional[str] = None
    review_status: str = "pending"
    review_notes: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

class DetectedChangeCreateRequest(BaseModel):
    comparison_id: str
    change_type: str
    severity: str
    description: str
    location_name: Optional[str] = None
    location_coordinates_x: Optional[float] = None
    location_coordinates_y: Optional[float] = None
    confidence_percentage: float
    impact_description: Optional[str] = None
    ai_model_version: Optional[str] = None
    detection_algorithm: Optional[str] = None

class ComparisonLocationResponse(BaseModel):
    id: str
    site_id: str
    location_name: str
    description: Optional[str] = None
    coordinates_x: Optional[float] = None
    coordinates_y: Optional[float] = None
    zone_type: str
    monitoring_priority: str = "medium"
    is_active: bool = True
    last_comparison_date: Optional[datetime] = None
    change_frequency_score: Optional[float] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ComparisonLocationCreateRequest(BaseModel):
    site_id: str
    location_name: str
    description: Optional[str] = None
    coordinates_x: Optional[float] = None
    coordinates_y: Optional[float] = None
    zone_type: str
    monitoring_priority: Optional[str] = "medium"

class ComparisonAnalysisMetricResponse(BaseModel):
    id: str
    comparison_id: str
    metric_type: str
    metric_value: float
    metric_unit: Optional[str] = None
    calculation_method: Optional[str] = None
    baseline_value: Optional[float] = None
    improvement_percentage: Optional[float] = None
    trend_direction: Optional[str] = None
    confidence_level: Optional[float] = None
    calculated_by: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


# HISTORICAL DATA & TEMPORAL ANALYSIS SCHEMAS

class HistoricalDataSnapshotResponse(BaseModel):
    id: str
    site_id: str
    snapshot_date: str
    snapshot_time: str
    data_source_type: str
    source_entity_id: Optional[str] = None
    source_entity_name: Optional[str] = None
    data_payload: dict
    data_metadata: Optional[dict] = None
    data_completeness_percentage: float = 100.0
    data_accuracy_score: float = 100.0
    processing_duration_ms: Optional[int] = None
    created_by: str
    processing_timestamp: datetime

    class Config:
        from_attributes = True

class HistoricalDataSnapshotCreateRequest(BaseModel):
    site_id: str
    snapshot_date: str
    snapshot_time: str
    data_source_type: str
    source_entity_id: Optional[str] = None
    source_entity_name: Optional[str] = None
    data_payload: dict
    data_metadata: Optional[dict] = None
    data_completeness_percentage: Optional[float] = 100.0
    data_accuracy_score: Optional[float] = 100.0

class TemporalAnalysisJobResponse(BaseModel):
    id: str
    site_id: str
    job_name: str
    analysis_type: str
    aggregation_period: str
    algorithm: str
    start_date: str
    end_date: str
    data_sources: dict
    status: str = "pending"
    scheduled_at: Optional[datetime] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    execution_duration_seconds: Optional[int] = None
    results_summary: Optional[dict] = None
    error_message: Optional[str] = None
    retry_count: int = 0
    created_by: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class TemporalAnalysisJobCreateRequest(BaseModel):
    site_id: str
    job_name: str
    analysis_type: str
    aggregation_period: str
    algorithm: str
    start_date: str
    end_date: str
    data_sources: dict
    include_weekends: Optional[bool] = True
    include_holidays: Optional[bool] = True
    filter_criteria: Optional[dict] = None
    scheduled_at: Optional[datetime] = None

class PerformanceBenchmarkResponse(BaseModel):
    id: str
    site_id: str
    benchmark_name: str
    benchmark_category: str
    measurement_date: str
    current_value: float
    target_value: float
    baseline_value: Optional[float] = None
    industry_average: Optional[float] = None
    performance_percentage: Optional[float] = None
    improvement_percentage: Optional[float] = None
    variance_percentage: Optional[float] = None
    trend_direction: Optional[str] = None
    trend_strength: Optional[float] = None
    confidence_level: float = 95.0
    created_by: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class PerformanceBenchmarkCreateRequest(BaseModel):
    site_id: str
    benchmark_name: str
    benchmark_category: str
    measurement_date: str
    current_value: float
    target_value: float
    baseline_value: Optional[float] = None
    industry_average: Optional[float] = None
    measurement_method: Optional[str] = None
    data_source_entities: Optional[dict] = None
    external_factors: Optional[dict] = None
    confidence_level: Optional[float] = 95.0
    sample_size: Optional[int] = None

class PredictiveModelResponse(BaseModel):
    id: str
    site_id: str
    model_name: str
    model_type: str
    prediction_target: str
    algorithm: str
    input_features: dict
    training_data_period_days: int
    training_start_date: str
    training_end_date: str
    accuracy_score: Optional[float] = None
    status: str = "training"
    version: str
    is_active: bool = False
    deployment_date: Optional[str] = None
    prediction_horizon_days: int
    prediction_frequency: str
    confidence_threshold: float = 80.0
    created_by: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class PredictiveModelCreateRequest(BaseModel):
    site_id: str
    model_name: str
    model_type: str
    prediction_target: str
    algorithm: str
    input_features: dict
    training_data_period_days: int
    training_start_date: str
    training_end_date: str
    prediction_horizon_days: int
    prediction_frequency: str
    hyperparameters: Optional[dict] = None
    confidence_threshold: Optional[float] = 80.0
    version: str = "1.0"

class PredictiveModelPredictionResponse(BaseModel):
    id: str
    model_id: str
    site_id: str
    prediction_date: str
    target_date: str
    target_time: Optional[str] = None
    predicted_value: float
    confidence_score: float
    prediction_interval_lower: Optional[float] = None
    prediction_interval_upper: Optional[float] = None
    input_features_snapshot: dict
    feature_values: dict
    actual_value: Optional[float] = None
    prediction_error: Optional[float] = None
    percentage_error: Optional[float] = None
    is_accurate: Optional[bool] = None
    prediction_context: Optional[dict] = None
    created_at: datetime
    validated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class PredictiveModelPredictionCreateRequest(BaseModel):
    model_id: str
    site_id: str
    prediction_date: str
    target_date: str
    target_time: Optional[str] = None
    predicted_value: float
    confidence_score: float
    prediction_interval_lower: Optional[float] = None
    prediction_interval_upper: Optional[float] = None
    input_features_snapshot: dict
    feature_values: dict
    prediction_context: Optional[dict] = None


# ALERT MANAGEMENT EXTENSIONS SCHEMAS

class AlertCommentResponse(BaseModel):
    id: str
    alert_id: str
    author_id: str
    comment_text: str
    comment_type: str = "note"
    parent_comment_id: Optional[str] = None
    thread_level: int = 0
    mentioned_users: Optional[list] = None
    attachment_urls: Optional[list] = None
    is_internal: bool = False
    is_edited: bool = False
    visibility_level: str = "team"
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class AlertCommentCreateRequest(BaseModel):
    alert_id: str
    comment_text: str
    comment_type: Optional[str] = "note"
    parent_comment_id: Optional[str] = None
    mentioned_users: Optional[list] = None
    attachment_urls: Optional[list] = None
    is_internal: Optional[bool] = False
    visibility_level: Optional[str] = "team"

class AlertEvidenceResponse(BaseModel):
    id: str
    alert_id: str
    source_type: str
    evidence_type: str
    file_name: str
    file_path: str
    file_size_bytes: Optional[int] = None
    location_description: Optional[str] = None
    evidence_description: Optional[str] = None
    is_processed: bool = False
    evidence_quality_score: Optional[float] = None
    collected_by: str
    verified_by: Optional[str] = None
    access_level: str = "team"
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class AlertEvidenceCreateRequest(BaseModel):
    alert_id: str
    source_type: str
    evidence_type: str
    file_name: str
    file_path: str
    file_size_bytes: Optional[int] = None
    location_description: Optional[str] = None
    evidence_description: Optional[str] = None
    camera_id: Optional[str] = None
    access_level: Optional[str] = "team"

class SafetyMetricResponse(BaseModel):
    id: str
    site_id: str
    metric_name: str
    metric_category: str
    measurement_date: str
    measurement_period: str
    incident_count: int = 0
    near_miss_count: int = 0
    safety_violation_count: int = 0
    compliance_score: Optional[float] = None
    training_completion_rate: Optional[float] = None
    performance_vs_target: Optional[float] = None
    trend_direction: Optional[str] = None
    improvement_percentage: Optional[float] = None
    created_by: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class SafetyMetricCreateRequest(BaseModel):
    site_id: str
    metric_name: str
    metric_category: str
    measurement_date: str
    measurement_period: str
    incident_count: Optional[int] = 0
    near_miss_count: Optional[int] = 0
    safety_violation_count: Optional[int] = 0
    compliance_score: Optional[float] = None
    target_value: Optional[float] = None


# PERSONNEL MANAGEMENT EXTENSIONS SCHEMAS

class PersonnelAttendanceResponse(BaseModel):
    id: str
    user_id: str
    site_id: str
    attendance_date: str
    shift_type: str
    scheduled_start: str
    scheduled_end: str
    actual_start: Optional[str] = None
    actual_end: Optional[str] = None
    status: str
    total_scheduled_hours: float
    total_actual_hours: Optional[float] = None
    overtime_hours: float = 0.0
    punctuality_score: Optional[float] = None
    attendance_quality: Optional[str] = None
    approved_by: Optional[str] = None
    approval_status: str = "approved"
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class PersonnelAttendanceCreateRequest(BaseModel):
    user_id: str
    site_id: str
    attendance_date: str
    shift_type: str
    scheduled_start: str
    scheduled_end: str
    total_scheduled_hours: float
    actual_start: Optional[str] = None
    actual_end: Optional[str] = None
    status: str = "present"

class PersonnelSafetyScoreResponse(BaseModel):
    id: str
    user_id: str
    site_id: str
    evaluation_date: str
    overall_safety_score: float
    safety_rating: str
    compliance_score: Optional[float] = None
    training_score: Optional[float] = None
    incident_score: Optional[float] = None
    incident_count: int = 0
    near_miss_reports: int = 0
    safety_violations: int = 0
    previous_score: Optional[float] = None
    score_improvement: Optional[float] = None
    trend_direction: Optional[str] = None
    target_score: Optional[float] = None
    is_current: bool = True
    evaluator_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class PersonnelSafetyScoreCreateRequest(BaseModel):
    user_id: str
    site_id: str
    evaluation_date: str
    evaluation_period_start: str
    evaluation_period_end: str
    overall_safety_score: float
    safety_rating: str
    incident_count: Optional[int] = 0
    target_score: Optional[float] = None


# ADVANCED MONITORING & COMMUNICATION SCHEMAS

class EnvironmentalSensorResponse(BaseModel):
    id: str
    site_id: str
    sensor_name: str
    sensor_type: str
    location_description: Optional[str] = None
    measurement_unit: str
    sampling_interval_seconds: int = 300
    calibration_status: str = "calibrated"
    is_active: bool = True
    operational_status: str = "operational"
    last_reading_value: Optional[float] = None
    last_reading_timestamp: Optional[datetime] = None
    warning_threshold_low: Optional[float] = None
    warning_threshold_high: Optional[float] = None
    alert_enabled: bool = True
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class EnvironmentalSensorCreateRequest(BaseModel):
    site_id: str
    sensor_name: str
    sensor_type: str
    measurement_unit: str
    location_description: Optional[str] = None
    sampling_interval_seconds: Optional[int] = 300
    warning_threshold_low: Optional[float] = None
    warning_threshold_high: Optional[float] = None

class SensorReadingResponse(BaseModel):
    id: str
    sensor_id: str
    reading_timestamp: datetime
    reading_value: float
    reading_unit: str
    data_quality_score: float = 100.0
    is_validated: bool = True
    is_anomaly: bool = False
    exceeds_threshold: bool = False
    threshold_type: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

class SensorReadingCreateRequest(BaseModel):
    sensor_id: str
    reading_timestamp: datetime
    reading_value: float
    reading_unit: str
    data_quality_score: Optional[float] = 100.0
    weather_conditions: Optional[str] = None

class QualityControlInspectionResponse(BaseModel):
    id: str
    site_id: str
    inspection_type: str
    inspection_category: str
    scheduled_date: str
    actual_date: Optional[str] = None
    inspector_id: str
    inspection_scope: str
    overall_result: str
    compliance_percentage: Optional[float] = None
    passed_items_count: int = 0
    failed_items_count: int = 0
    deficiency_count: int = 0
    critical_issues_count: int = 0
    requires_reinspection: bool = False
    approved_by: Optional[str] = None
    approval_status: str = "pending"
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class QualityControlInspectionCreateRequest(BaseModel):
    site_id: str
    inspection_type: str
    inspection_category: str
    scheduled_date: str
    inspector_id: str
    inspection_scope: str
    checklist_items: dict
    overall_result: str = "pending"

class ComparisonAnalysisMetricCreateRequest(BaseModel):
    comparison_id: str
    metric_type: str
    metric_value: float
    metric_unit: Optional[str] = None
    calculation_method: Optional[str] = None
    baseline_value: Optional[float] = None
    improvement_percentage: Optional[float] = None
    trend_direction: Optional[str] = None
    confidence_level: Optional[float] = None
    calculated_by: Optional[str] = None


# INTEGRATION & USER EXPERIENCE SCHEMAS

class ThirdPartyIntegrationResponse(BaseModel):
    id: str
    integration_name: str
    integration_type: str
    provider_name: str
    description: Optional[str] = None
    status: str = "pending"
    health_score: Optional[float] = 0.0
    monthly_usage: int = 0
    error_rate: Optional[float] = 0.0
    created_by: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ThirdPartyIntegrationCreateRequest(BaseModel):
    integration_name: str
    integration_type: str
    provider_name: str
    description: Optional[str] = None
    configuration: dict
    endpoints: Optional[dict] = None
    rate_limits: Optional[dict] = None
    monthly_limit: Optional[int] = None

class UserProfileSettingResponse(BaseModel):
    id: str
    user_id: str
    profile_picture_url: Optional[str] = None
    bio: Optional[str] = None
    preferences: Optional[dict] = None
    notification_settings: Optional[dict] = None
    dashboard_config: Optional[dict] = None
    theme_settings: Optional[dict] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class UserProfileSettingCreateRequest(BaseModel):
    user_id: str
    profile_picture_url: Optional[str] = None
    bio: Optional[str] = None
    preferences: Optional[dict] = None
    notification_settings: Optional[dict] = None
    dashboard_config: Optional[dict] = None
    theme_settings: Optional[dict] = None

class UserApplicationSettingResponse(BaseModel):
    id: str
    user_id: str
    language: str = "en"
    timezone: Optional[str] = None
    time_format: str = "12h"
    theme: str = "light"
    font_size: str = "medium"
    notifications_enabled: bool = True
    email_notifications: bool = True
    quiet_hours_enabled: bool = False
    data_sharing_enabled: bool = True
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class UserApplicationSettingCreateRequest(BaseModel):
    user_id: str
    language: Optional[str] = "en"
    timezone: Optional[str] = None
    time_format: Optional[str] = "12h"
    theme: Optional[str] = "light"
    font_size: Optional[str] = "medium"
    notifications_enabled: Optional[bool] = True
    email_notifications: Optional[bool] = True
    quiet_hours_enabled: Optional[bool] = False

class HelpArticleResponse(BaseModel):
    id: str
    title: str
    content: str
    category: str
    subcategory: Optional[str] = None
    tags: Optional[list] = None
    author_id: str
    is_published: bool = False
    view_count: int = 0
    helpful_count: int = 0
    unhelpful_count: int = 0
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class HelpArticleCreateRequest(BaseModel):
    title: str
    content: str
    category: str
    subcategory: Optional[str] = None
    tags: Optional[list] = None
    is_published: Optional[bool] = False
    search_keywords: Optional[str] = None

class UserFeedbackResponse(BaseModel):
    id: str
    user_id: str
    feedback_type: str
    title: str
    description: str
    priority: str = "medium"
    status: str = "submitted"
    category: Optional[str] = None
    upvote_count: int = 0
    admin_response: Optional[str] = None
    responded_by: Optional[str] = None
    responded_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class UserFeedbackCreateRequest(BaseModel):
    user_id: str
    feedback_type: str
    title: str
    description: str
    priority: Optional[str] = "medium"
    category: Optional[str] = None
    attachments: Optional[list] = None