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