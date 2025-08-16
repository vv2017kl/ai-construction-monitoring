"""
SQLAlchemy models for AI Construction Management System
Based on MASTER_DATABASE_SCHEMA.md - Phase 1: Core Tables
"""
from sqlalchemy import (
    Column, String, Text, Integer, DateTime, Boolean, 
    ForeignKey, Index, JSON, Enum as SQLEnum, Date, TIMESTAMP,
    UniqueConstraint, DECIMAL as Decimal, BigInteger
)
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
import uuid
import enum

Base = declarative_base()

def generate_uuid():
    return str(uuid.uuid4())

# Enums
class SiteStatus(enum.Enum):
    active = "active"
    inactive = "inactive"
    maintenance = "maintenance"

class SiteType(enum.Enum):
    commercial = "commercial"
    residential = "residential"
    industrial = "industrial"
    infrastructure = "infrastructure"

class SitePhase(enum.Enum):
    planning = "planning"
    construction = "construction"
    finishing = "finishing"
    completed = "completed"

class ZoneType(enum.Enum):
    construction = "construction"
    safety = "safety"
    restricted = "restricted"
    office = "office"
    storage = "storage"
    parking = "parking"

class SafetyLevel(enum.Enum):
    safe = "safe"
    caution = "caution"
    restricted = "restricted"
    danger = "danger"

class ZoneAccessLevel(enum.Enum):
    public = "public"
    personnel = "personnel"
    authorized = "authorized"
    management = "management"

class AccessLevel(enum.Enum):
    view = "view"
    comment = "comment"
    bookmark = "bookmark"
    download = "download"

class ZoneStatus(enum.Enum):
    active = "active"
    inactive = "inactive"
    under_construction = "under_construction"

class UserRole(enum.Enum):
    admin = "admin"
    site_manager = "site_manager"
    supervisor = "supervisor"
    worker = "worker"
    security = "security"
    readonly = "readonly"

class UserStatus(enum.Enum):
    active = "active"
    inactive = "inactive"
    suspended = "suspended"

class UserSiteAccessLevel(enum.Enum):
    view = "view"
    manage = "manage"
    admin = "admin"

class UserSiteAccessStatus(enum.Enum):
    active = "active"
    suspended = "suspended"
    expired = "expired"

class CameraType(enum.Enum):
    fixed = "fixed"
    ptz = "ptz"
    fisheye = "fisheye"
    thermal = "thermal"
    infrared = "infrared"

class CameraStatus(enum.Enum):
    active = "active"
    inactive = "inactive"
    maintenance = "maintenance"
    offline = "offline"

class PersonnelStatus(enum.Enum):
    active = "active"
    inactive = "inactive"
    break_status = "break"
    offsite = "offsite"

class ActivityLevel(enum.Enum):
    low = "low"
    moderate = "moderate"
    high = "high"

class AlertPriority(enum.Enum):
    critical = "critical"
    high = "high"
    medium = "medium"
    low = "low"
    info = "info"

class DetectionType(enum.Enum):
    person = "person"
    vehicle = "vehicle"
    ppe = "ppe"
    safety_violation = "safety_violation"
    equipment = "equipment"
    activity = "activity"

class ModelType(enum.Enum):
    person_detection = "person_detection"
    ppe_detection = "ppe_detection"
    vehicle_detection = "vehicle_detection"
    activity_recognition = "activity_recognition"

class ModelStatus(enum.Enum):
    active = "active"
    inactive = "inactive"
    training = "training"
    deprecated = "deprecated"

class CorrelationType(enum.Enum):
    direct = "direct"
    temporal = "temporal"
    spatial = "spatial"

class RecordingSessionType(enum.Enum):
    manual = "manual"
    scheduled = "scheduled"
    triggered = "triggered"
    continuous = "continuous"

class TriggerType(enum.Enum):
    user_initiated = "user_initiated"
    ai_detection = "ai_detection"
    motion = "motion"
    alert = "alert"
    schedule = "schedule"

class RecordingStatus(enum.Enum):
    starting = "starting"
    active = "active"
    stopping = "stopping"
    completed = "completed"
    failed = "failed"
    interrupted = "interrupted"

class EvaluationType(enum.Enum):
    automated = "automated"
    manual = "manual"
    field_test = "field_test"
    benchmark = "benchmark"

class TrendType(enum.Enum):
    increasing = "increasing"
    stable = "stable"
    decreasing = "decreasing"

class PerformanceTier(enum.Enum):
    excellent = "excellent"
    good = "good"
    average = "average"
    poor = "poor"
    critical = "critical"

class ReportType(enum.Enum):
    safety = "safety"
    compliance = "compliance"
    activity = "activity"
    performance = "performance"
    custom = "custom"

class OutputFormat(enum.Enum):
    pdf = "pdf"
    excel = "excel"
    csv = "csv"
    json = "json"

class GenerationStatus(enum.Enum):
    pending = "pending"
    generating = "generating"
    completed = "completed"
    failed = "failed"

class ReportVisibility(enum.Enum):
    private = "private"
    site = "site"
    company = "company"
    public = "public"

class ConfigType(enum.Enum):
    string = "string"
    number = "number"
    boolean = "boolean"
    json = "json"
    array = "array"

class NotificationType(enum.Enum):
    alert = "alert"
    system = "system"
    report = "report"
    reminder = "reminder"

class NotificationPriority(enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"
    urgent = "urgent"

class BookmarkType(enum.Enum):
    safety_incident = "safety_incident"
    ppe_violation = "ppe_violation"
    equipment_issue = "equipment_issue"
    person_activity = "person_activity"
    vehicle_activity = "vehicle_activity"
    custom = "custom"
    alert_related = "alert_related"
    compliance_check = "compliance_check"

class PriorityLevel(enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"

class Severity(enum.Enum):
    info = "info"
    warning = "warning"
    error = "error"
    critical = "critical"

class EvidenceQuality(enum.Enum):
    poor = "poor"
    fair = "fair"
    good = "good"
    excellent = "excellent"

class LightingCondition(enum.Enum):
    excellent = "excellent"
    good = "good"
    fair = "fair"
    poor = "poor"
    very_poor = "very_poor"

class BookmarkStatus(enum.Enum):
    active = "active"
    reviewed = "reviewed"
    resolved = "resolved"
    archived = "archived"

class AccessMethod(enum.Enum):
    web_browser = "web_browser"
    mobile_app = "mobile_app"
    api = "api"
    export = "export"

class AccessReason(enum.Enum):
    routine_review = "routine_review"
    incident_investigation = "incident_investigation"
    compliance_audit = "compliance_audit"
    training = "training"
    maintenance = "maintenance"
    legal_request = "legal_request"

class TerminationReason(enum.Enum):
    user_logout = "user_logout"
    session_timeout = "session_timeout"
    technical_error = "technical_error"
    policy_violation = "policy_violation"
    system_maintenance = "system_maintenance"

class ExportType(enum.Enum):
    video_clip = "video_clip"
    screenshot = "screenshot"
    evidence_package = "evidence_package"
    compliance_report = "compliance_report"
    share_link = "share_link"

class QualitySetting(enum.Enum):
    high = "high"
    medium = "medium"
    low = "low"

class ExportPurpose(enum.Enum):
    evidence = "evidence"
    training = "training"
    analysis = "analysis"
    compliance = "compliance"
    documentation = "documentation"
    legal_proceeding = "legal_proceeding"

class ExportStatus(enum.Enum):
    requested = "requested"
    processing = "processing"
    completed = "completed"
    failed = "failed"
    expired = "expired"

class WeatherImpact(enum.Enum):
    none = "none"
    minimal = "minimal"
    moderate = "moderate"
    significant = "significant"
    severe = "severe"

class ForensicQuality(enum.Enum):
    excellent = "excellent"
    good = "good"
    acceptable = "acceptable"
    poor = "poor"
    unusable = "unusable"

class IdentificationViability(enum.Enum):
    clear = "clear"
    good = "good"
    limited = "limited"
    poor = "poor"
    impossible = "impossible"

class AnalysisMethod(enum.Enum):
    automated = "automated"
    manual = "manual"
    hybrid = "hybrid"

class CompressionLevel(enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"

class GenerationStatus(enum.Enum):
    queued = "queued"
    processing = "processing"
    completed = "completed"
    failed = "failed"
    cancelled = "cancelled"

class SequenceStatus(enum.Enum):
    active = "active"
    archived = "archived"
    deleted = "deleted"

class TimelapseBookmarkType(enum.Enum):
    manual = "manual"
    milestone = "milestone"
    activity = "activity"
    safety = "safety"
    progress = "progress"
    custom = "custom"

class TimelapseEventType(enum.Enum):
    personnel_activity = "personnel_activity"
    equipment_movement = "equipment_movement"
    safety_incident = "safety_incident"
    milestone_completion = "milestone_completion"
    weather_change = "weather_change"
    construction_phase = "construction_phase"
    inspection = "inspection"
    delivery = "delivery"

class ImpactLevel(enum.Enum):
    minimal = "minimal"
    low = "low"
    moderate = "moderate"
    significant = "significant"
    critical = "critical"

class SafetyImplications(enum.Enum):
    none = "none"
    minor = "minor"
    moderate = "moderate"
    serious = "serious"
    critical = "critical"

class EventStatus(enum.Enum):
    detected = "detected"
    verified = "verified"
    false_positive = "false_positive"
    archived = "archived"

class ShareType(enum.Enum):
    link = "link"
    email = "email"
    embed = "embed"
    download = "download"

class AccessLevel(enum.Enum):
    view = "view"
    comment = "comment"
    bookmark = "bookmark"
    download = "download"

class ShareStatus(enum.Enum):
    active = "active"
    expired = "expired"
    disabled = "disabled"
    revoked = "revoked"

class MilestoneStatus(enum.Enum):
    not_started = "not_started"
    in_progress = "in_progress"
    completed = "completed"
    delayed = "delayed"
    cancelled = "cancelled"
    on_hold = "on_hold"

class AlertStatus(enum.Enum):
    open = "open"
    acknowledged = "acknowledged"
    investigating = "investigating"
    resolved = "resolved"
    false_positive = "false_positive"

# SITES & LOCATIONS
class Site(Base):
    __tablename__ = "sites"
    
    id = Column(CHAR(36), primary_key=True, default=generate_uuid)
    name = Column(String(255), nullable=False)
    code = Column(String(50), unique=True, nullable=False)
    address = Column(Text)
    coordinates = Column(String(255))  # Simplified for now - can be enhanced to actual POINT type
    status = Column(SQLEnum(SiteStatus), default=SiteStatus.active)
    type = Column(SQLEnum(SiteType))
    phase = Column(SQLEnum(SitePhase))
    progress_percentage = Column(Decimal(5,2), default=0.00)
    budget = Column(Decimal(15,2))
    completion_date = Column(Date)
    manager_id = Column(CHAR(36), ForeignKey('users.id'))
    
    # Weather Integration
    weather_temp = Column(Integer)
    weather_condition = Column(String(100))
    weather_wind_speed = Column(String(50))
    weather_humidity = Column(Decimal(5,2))
    weather_last_updated = Column(TIMESTAMP)
    weather_api_source = Column(String(100))
    
    # Activity Tracking
    last_activity_timestamp = Column(TIMESTAMP)
    last_activity_type = Column(String(100))
    activity_summary = Column(Text)
    
    # Camera Metrics
    total_cameras = Column(Integer, default=0)
    active_cameras = Column(Integer, default=0)
    offline_cameras = Column(Integer, default=0)
    maintenance_cameras = Column(Integer, default=0)
    
    # Geospatial View Enhancements
    region = Column(String(100))
    timezone = Column(String(100))
    site_boundary_coordinates = Column(Text)  # Simplified polygon representation
    
    created_at = Column(TIMESTAMP, default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, default=func.current_timestamp(), onupdate=func.current_timestamp())
    
    # Relationships
    manager = relationship("User", back_populates="managed_sites")
    zones = relationship("Zone", back_populates="site")
    weather_data = relationship("WeatherData", back_populates="site")
    
    # Indexes
    __table_args__ = (
        Index('idx_sites_status', 'status'),
        Index('idx_sites_type_phase', 'type', 'phase'),
        Index('idx_sites_manager', 'manager_id'),
        Index('idx_sites_weather_updated', 'weather_last_updated'),
        Index('idx_sites_region', 'region'),
    )

class Zone(Base):
    __tablename__ = "zones"
    
    id = Column(CHAR(36), primary_key=True, default=generate_uuid)
    site_id = Column(CHAR(36), ForeignKey('sites.id'), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    zone_type = Column(SQLEnum(ZoneType), nullable=False)
    coordinates = Column(Text)  # Simplified polygon representation
    safety_level = Column(SQLEnum(SafetyLevel), default=SafetyLevel.safe)
    required_ppe = Column(JSON)
    access_level = Column(SQLEnum(ZoneAccessLevel), default=ZoneAccessLevel.personnel)
    
    # Zone status
    status = Column(SQLEnum(ZoneStatus), default=ZoneStatus.active)
    capacity_limit = Column(Integer)
    current_occupancy = Column(Integer, default=0)
    
    created_at = Column(TIMESTAMP, default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, default=func.current_timestamp(), onupdate=func.current_timestamp())
    
    # Relationships
    site = relationship("Site", back_populates="zones")
    
    # Indexes
    __table_args__ = (
        Index('idx_zones_site', 'site_id'),
        Index('idx_zones_type', 'zone_type'),
        Index('idx_zones_safety', 'safety_level'),
        Index('idx_zones_status', 'status'),
    )

class WeatherData(Base):
    __tablename__ = "weather_data"
    
    id = Column(CHAR(36), primary_key=True, default=generate_uuid)
    site_id = Column(CHAR(36), ForeignKey('sites.id'), nullable=False)
    timestamp = Column(TIMESTAMP, default=func.current_timestamp())
    
    # Weather metrics
    temperature = Column(Decimal(5,2))
    humidity = Column(Decimal(5,2))
    wind_speed = Column(Decimal(5,2))
    wind_direction = Column(String(10))
    pressure = Column(Decimal(7,2))
    visibility = Column(Decimal(5,2))
    uv_index = Column(Decimal(3,1))
    
    # Conditions
    condition = Column(String(100))
    precipitation = Column(Decimal(5,2))
    cloud_cover = Column(Decimal(5,2))
    
    # Safety impact
    work_safety_score = Column(Decimal(3,1))
    safety_warnings = Column(JSON)
    recommended_precautions = Column(JSON)
    
    # Data source
    weather_api_source = Column(String(100))
    api_response_raw = Column(JSON)
    
    # Relationships
    site = relationship("Site", back_populates="weather_data")
    
    # Indexes
    __table_args__ = (
        Index('idx_weather_site_time', 'site_id', 'timestamp'),
        Index('idx_weather_conditions', 'condition'),
        Index('idx_weather_safety', 'work_safety_score'),
    )

# PERSONNEL & USERS
class User(Base):
    __tablename__ = "users"
    
    id = Column(CHAR(36), primary_key=True, default=generate_uuid)
    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    display_name = Column(String(255))
    phone = Column(String(20))
    avatar_url = Column(String(500))
    
    # Authentication
    password_hash = Column(String(255), nullable=False)
    email_verified = Column(Boolean, default=False)
    last_login = Column(TIMESTAMP)
    failed_login_attempts = Column(Integer, default=0)
    locked_until = Column(TIMESTAMP)
    
    # Role & Permissions
    role = Column(SQLEnum(UserRole), nullable=False)
    permissions = Column(JSON)
    company_id = Column(CHAR(36))
    department = Column(String(100))
    
    # Profile
    hire_date = Column(Date)
    employee_id = Column(String(50))
    certification_level = Column(String(100))
    emergency_contact = Column(JSON)
    
    status = Column(SQLEnum(UserStatus), default=UserStatus.active)
    created_at = Column(TIMESTAMP, default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, default=func.current_timestamp(), onupdate=func.current_timestamp())
    
    # Relationships
    managed_sites = relationship("Site", back_populates="manager")
    site_access = relationship("UserSiteAccess", back_populates="user", foreign_keys="UserSiteAccess.user_id")
    
    # Indexes
    __table_args__ = (
        Index('idx_users_username', 'username'),
        Index('idx_users_email', 'email'),
        Index('idx_users_role', 'role'),
        Index('idx_users_company', 'company_id'),
        Index('idx_users_status', 'status'),
    )

class UserSiteAccess(Base):
    __tablename__ = "user_site_access"
    
    id = Column(CHAR(36), primary_key=True, default=generate_uuid)
    user_id = Column(CHAR(36), ForeignKey('users.id'), nullable=False)
    site_id = Column(CHAR(36), ForeignKey('sites.id'), nullable=False)
    access_level = Column(SQLEnum(UserSiteAccessLevel), default=UserSiteAccessLevel.view)
    granted_by = Column(CHAR(36), ForeignKey('users.id'), nullable=False)
    granted_at = Column(TIMESTAMP, default=func.current_timestamp())
    expires_at = Column(TIMESTAMP)
    status = Column(SQLEnum(UserSiteAccessStatus), default=UserSiteAccessStatus.active)
    
    # Permission details
    permissions = Column(JSON)
    zone_restrictions = Column(JSON)
    time_restrictions = Column(JSON)
    
    # Audit fields
    last_accessed = Column(TIMESTAMP)
    access_count = Column(Integer, default=0)
    
    # Relationships
    user = relationship("User", back_populates="site_access", foreign_keys=[user_id])
    site = relationship("Site", foreign_keys=[site_id])
    granted_by_user = relationship("User", foreign_keys=[granted_by])
    
    # Constraints and Indexes
    __table_args__ = (
        UniqueConstraint('user_id', 'site_id', name='unique_user_site'),
        Index('idx_user_access_user', 'user_id'),
        Index('idx_user_access_site', 'site_id'),
        Index('idx_user_access_level', 'access_level'),
        Index('idx_user_access_status', 'status'),
        Index('idx_user_access_expires', 'expires_at'),
    )

class SitePersonnel(Base):
    __tablename__ = "site_personnel"
    
    id = Column(CHAR(36), primary_key=True, default=generate_uuid)
    site_id = Column(CHAR(36), ForeignKey('sites.id'), nullable=False)
    user_id = Column(CHAR(36), ForeignKey('users.id'), nullable=False)
    role = Column(String(100))
    status = Column(SQLEnum(PersonnelStatus), default=PersonnelStatus.active)
    check_in_time = Column(TIMESTAMP)
    check_out_time = Column(TIMESTAMP)
    
    # Real-time Location Tracking
    current_zone_id = Column(CHAR(36), ForeignKey('zones.id'))
    current_zone_name = Column(String(100))
    last_known_coordinates = Column(String(255))  # Simplified POINT
    location_updated_at = Column(TIMESTAMP)
    
    # PPE Compliance Tracking
    ppe_compliance_score = Column(Decimal(5,2), default=0.00)
    ppe_status = Column(JSON)  # {"hardhat": true, "vest": true, "boots": false}
    last_ppe_check_timestamp = Column(TIMESTAMP)
    ppe_violations_count = Column(Integer, default=0)
    
    # Activity Tracking
    last_detection_timestamp = Column(TIMESTAMP)
    last_detection_camera_id = Column(CHAR(36), ForeignKey('cameras.id'))
    activity_level = Column(SQLEnum(ActivityLevel), default=ActivityLevel.moderate)
    break_start_time = Column(TIMESTAMP)
    
    created_at = Column(TIMESTAMP, default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, default=func.current_timestamp(), onupdate=func.current_timestamp())
    
    # Relationships
    site = relationship("Site")
    user = relationship("User")
    current_zone = relationship("Zone")
    
    # Indexes
    __table_args__ = (
        UniqueConstraint('site_id', 'user_id', 'status', name='unique_site_user_active'),
        Index('idx_personnel_site_status', 'site_id', 'status'),
        Index('idx_personnel_zone', 'current_zone_id'),
        Index('idx_personnel_compliance', 'ppe_compliance_score'),
        Index('idx_personnel_activity', 'last_detection_timestamp'),
    )

# CAMERAS & MONITORING
class Camera(Base):
    __tablename__ = "cameras"
    
    id = Column(CHAR(36), primary_key=True, default=generate_uuid)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    camera_type = Column(SQLEnum(CameraType), nullable=False)
    manufacturer = Column(String(100))
    model = Column(String(100))
    serial_number = Column(String(100))
    
    # Technical specifications
    resolution = Column(String(20))  # '1920x1080'
    frame_rate = Column(Integer, default=30)
    field_of_view = Column(Decimal(5,2))  # Degrees
    night_vision = Column(Boolean, default=False)
    weather_resistant = Column(Boolean, default=False)
    
    # Live View Enhancements
    audio_enabled = Column(Boolean, default=False)
    ptz_capabilities = Column(JSON)  # PTZ range, presets, speed settings
    recording_capabilities = Column(JSON)  # Max resolution, frame rates, bitrate limits
    
    # Network & streaming
    ip_address = Column(String(39))  # IPv6 compatible
    mac_address = Column(String(17))
    rtsp_url = Column(String(500))
    http_url = Column(String(500))
    
    # Status
    status = Column(SQLEnum(CameraStatus), default=CameraStatus.active)
    installation_date = Column(Date)
    last_maintenance = Column(Date)
    maintenance_schedule = Column(String(100))
    
    created_at = Column(TIMESTAMP, default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, default=func.current_timestamp(), onupdate=func.current_timestamp())
    
    # Indexes
    __table_args__ = (
        Index('idx_cameras_type', 'camera_type'),
        Index('idx_cameras_status', 'status'),
        Index('idx_cameras_ip', 'ip_address'),
        Index('idx_cameras_maintenance', 'last_maintenance'),
    )

class SiteCamera(Base):
    __tablename__ = "site_cameras"
    
    id = Column(CHAR(36), primary_key=True, default=generate_uuid)
    site_id = Column(CHAR(36), ForeignKey('sites.id'), nullable=False)
    camera_id = Column(CHAR(36), ForeignKey('cameras.id'), nullable=False)
    zoneminder_monitor_id = Column(Integer, nullable=False)  # ZoneMinder integration
    
    # Positioning for 3D mapping
    coordinates = Column(String(255))  # Simplified POINT
    elevation = Column(Decimal(8,2))  # Meters above sea level
    orientation_angle = Column(Decimal(5,2))  # 0-360 degrees
    tilt_angle = Column(Decimal(5,2))  # -90 to +90 degrees
    
    # Zone coverage
    primary_zone_id = Column(CHAR(36), ForeignKey('zones.id'))
    coverage_zones = Column(JSON)  # Array of zone IDs this camera covers
    
    # Site-specific status
    status = Column(SQLEnum(CameraStatus), default=CameraStatus.active)
    last_online = Column(TIMESTAMP)
    health_score = Column(Decimal(3,1))  # 0-10 camera health rating
    
    # Geospatial View Enhancements
    region = Column(String(100))  # Geographic region grouping
    zone_coverage = Column(JSON)  # Array of zone IDs this camera covers
    detection_range = Column(Decimal(8,2))  # Detection range in meters
    
    # Live View Enhancements
    current_zoom_level = Column(Decimal(5,2), default=1.0)  # Current PTZ zoom level
    recording_active = Column(Boolean, default=False)  # Current recording status
    stream_quality = Column(String(10), default='high')  # Current stream quality
    
    # Relationships
    site = relationship("Site")
    camera = relationship("Camera")
    primary_zone = relationship("Zone")
    
    # Constraints and Indexes
    __table_args__ = (
        UniqueConstraint('site_id', 'camera_id', name='unique_site_camera'),
        UniqueConstraint('zoneminder_monitor_id', name='unique_zm_monitor'),
        Index('idx_site_cameras_site', 'site_id'),
        Index('idx_site_cameras_status', 'status'),
        Index('idx_site_cameras_zone', 'primary_zone_id'),
        Index('idx_site_cameras_health', 'health_score'),
        Index('idx_site_cameras_region', 'region'),
        Index('idx_site_cameras_recording', 'recording_active'),
        Index('idx_site_cameras_zoom', 'current_zoom_level'),
    )

# ALERTS & SAFETY
class Alert(Base):
    __tablename__ = "alerts"
    
    id = Column(CHAR(36), primary_key=True, default=generate_uuid)
    site_id = Column(CHAR(36), ForeignKey('sites.id'), nullable=False)
    camera_id = Column(CHAR(36), ForeignKey('cameras.id'))
    zone_id = Column(CHAR(36), ForeignKey('zones.id'))
    
    # Alert Information
    title = Column(String(255), nullable=False)
    description = Column(Text)
    priority = Column(SQLEnum(AlertPriority), nullable=False)
    status = Column(SQLEnum(AlertStatus), default=AlertStatus.open)
    alert_type = Column(String(100))  # 'ppe_violation', 'safety_breach', 'unauthorized_access'
    
    # AI Integration
    detection_id = Column(CHAR(36))  # Link to AI detection that triggered this alert
    confidence_score = Column(Decimal(5,2))
    ai_model_used = Column(String(100))
    detection_data = Column(JSON)  # Complete AI detection results
    
    # Evidence
    primary_image_url = Column(String(500))
    secondary_images = Column(JSON)  # Array of additional images
    video_clip_url = Column(String(500))
    annotated_evidence_url = Column(String(500))
    
    # Workflow
    timestamp = Column(TIMESTAMP, default=func.current_timestamp())
    acknowledged_at = Column(TIMESTAMP)
    acknowledged_by = Column(CHAR(36), ForeignKey('users.id'))
    acknowledged_notes = Column(Text)
    investigating_started_at = Column(TIMESTAMP)
    investigating_by = Column(CHAR(36), ForeignKey('users.id'))
    resolved_at = Column(TIMESTAMP)
    resolved_by = Column(CHAR(36), ForeignKey('users.id'))
    resolution_notes = Column(Text)
    resolution_type = Column(String(50))
    
    # Impact Assessment
    severity_score = Column(Decimal(5,2))  # 0-10 impact rating
    affected_personnel_count = Column(Integer, default=0)
    estimated_risk_level = Column(String(20))
    
    # Escalation & Notifications
    escalated = Column(Boolean, default=False)
    escalated_at = Column(TIMESTAMP)
    escalated_to = Column(CHAR(36), ForeignKey('users.id'))
    notification_sent = Column(Boolean, default=False)
    notification_channels = Column(JSON)  # ['email', 'sms', 'push', 'radio']
    
    # Relationships
    site = relationship("Site")
    camera = relationship("Camera")
    zone = relationship("Zone")
    acknowledged_by_user = relationship("User", foreign_keys=[acknowledged_by])
    investigating_by_user = relationship("User", foreign_keys=[investigating_by])
    resolved_by_user = relationship("User", foreign_keys=[resolved_by])
    escalated_to_user = relationship("User", foreign_keys=[escalated_to])
    
    # Indexes
    __table_args__ = (
        Index('idx_alerts_site_priority', 'site_id', 'priority', 'status'),
        Index('idx_alerts_status_time', 'status', 'timestamp'),
        Index('idx_alerts_camera', 'camera_id'),
        Index('idx_alerts_escalated', 'escalated', 'escalated_at'),
    )

# AI & DETECTION TABLES
class AIDetection(Base):
    __tablename__ = "ai_detections"
    
    id = Column(CHAR(36), primary_key=True, default=generate_uuid)
    camera_id = Column(CHAR(36), ForeignKey('cameras.id'), nullable=False)
    site_id = Column(CHAR(36), ForeignKey('sites.id'), nullable=False)
    zone_id = Column(CHAR(36), ForeignKey('zones.id'))
    zone_name = Column(String(100))
    
    # Detection Data
    detection_type = Column(SQLEnum(DetectionType))
    person_count = Column(Integer, default=0)
    confidence_score = Column(Decimal(5,2))
    overall_confidence = Column(Decimal(5,2))
    
    # AI Results
    bounding_boxes = Column(JSON)  # All detection coordinates
    detection_results = Column(JSON)  # Complete AI model response
    ppe_compliance_data = Column(JSON)  # Detailed PPE analysis
    safety_violations = Column(JSON)  # List of detected violations
    
    # Activity Analysis
    activity_summary = Column(Text)
    activity_level = Column(SQLEnum(ActivityLevel))
    risk_assessment = Column(String(20))  # 'safe', 'caution', 'danger'
    safety_score = Column(Decimal(5,2))
    
    # Media Evidence
    snapshot_image_url = Column(String(500))
    video_clip_url = Column(String(500))
    annotated_image_url = Column(String(500))
    
    timestamp = Column(TIMESTAMP, default=func.current_timestamp())
    processed = Column(Boolean, default=False)
    alert_generated = Column(Boolean, default=False)
    alert_ids = Column(JSON)  # Array of generated alert IDs
    
    # Processing Metadata
    model_version = Column(String(50))
    processing_time_ms = Column(Integer)
    ai_server_id = Column(String(100))
    
    # Relationships
    camera = relationship("Camera")
    site = relationship("Site")
    zone = relationship("Zone")
    
    # Indexes
    __table_args__ = (
        Index('idx_detections_camera_time', 'camera_id', 'timestamp'),
        Index('idx_detections_site_time', 'site_id', 'timestamp'),
        Index('idx_detections_zone', 'zone_id'),
        Index('idx_detections_type', 'detection_type'),
        Index('idx_detections_alerts', 'alert_generated'),
        Index('idx_detections_confidence', 'confidence_score'),
        Index('idx_detections_processed', 'processed', 'timestamp'),
    )

class AIModel(Base):
    __tablename__ = "ai_models"
    
    id = Column(CHAR(36), primary_key=True, default=generate_uuid)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    model_type = Column(SQLEnum(ModelType))
    provider = Column(String(100))  # 'roboflow', 'custom', 'openai', etc.
    
    # Model configuration
    endpoint_url = Column(String(500))
    model_version = Column(String(50))
    confidence_threshold = Column(Decimal(5,2), default=0.50)
    overlap_threshold = Column(Decimal(5,2), default=0.30)
    
    # Performance metrics
    accuracy_score = Column(Decimal(5,2))
    precision_score = Column(Decimal(5,2))
    recall_score = Column(Decimal(5,2))
    avg_processing_time_ms = Column(Integer)
    
    # Status & lifecycle
    status = Column(SQLEnum(ModelStatus), default=ModelStatus.active)
    deployed_at = Column(TIMESTAMP)
    last_updated = Column(TIMESTAMP)
    
    # Configuration
    input_requirements = Column(JSON)  # Image size, format, etc.
    output_format = Column(JSON)  # Expected response structure
    api_configuration = Column(JSON)  # API keys, headers, etc.
    
    created_at = Column(TIMESTAMP, default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, default=func.current_timestamp(), onupdate=func.current_timestamp())
    
    # Indexes
    __table_args__ = (
        Index('idx_models_type', 'model_type'),
        Index('idx_models_provider', 'provider'),
        Index('idx_models_status', 'status'),
        Index('idx_models_performance', 'accuracy_score'),
    )

class EventCorrelation(Base):
    __tablename__ = "event_correlations"
    
    id = Column(CHAR(36), primary_key=True, default=generate_uuid)
    zoneminder_event_id = Column(BigInteger, nullable=False)
    ai_detection_id = Column(CHAR(36), ForeignKey('ai_detections.id'), nullable=False)
    correlation_confidence = Column(Decimal(5,2))
    correlation_type = Column(SQLEnum(CorrelationType), nullable=False)
    time_diff_seconds = Column(Integer)  # Time difference between ZM event and AI detection
    created_at = Column(TIMESTAMP, default=func.current_timestamp())
    
    # Relationships
    ai_detection = relationship("AIDetection")
    
    # Indexes
    __table_args__ = (
        Index('idx_correlations_zm_event', 'zoneminder_event_id'),
        Index('idx_correlations_ai_detection', 'ai_detection_id'),
        Index('idx_correlations_confidence', 'correlation_confidence'),
    )

class RecordingSession(Base):
    __tablename__ = "recording_sessions"
    
    id = Column(CHAR(36), primary_key=True, default=generate_uuid)
    camera_id = Column(CHAR(36), ForeignKey('cameras.id'), nullable=False)
    site_id = Column(CHAR(36), ForeignKey('sites.id'), nullable=False)
    
    # Session details
    session_type = Column(SQLEnum(RecordingSessionType), nullable=False)
    trigger_type = Column(SQLEnum(TriggerType), default=TriggerType.user_initiated)
    trigger_event_id = Column(CHAR(36))  # Reference to alert or detection that triggered recording
    
    # Timing
    start_time = Column(TIMESTAMP, default=func.current_timestamp())
    end_time = Column(TIMESTAMP)
    planned_duration_seconds = Column(Integer)
    actual_duration_seconds = Column(Integer)
    
    # Quality & Storage
    recording_quality = Column(String(10), default='high')  # 'low', 'medium', 'high', 'ultra'
    resolution = Column(String(20))  # '1920x1080'
    frame_rate = Column(Integer, default=30)
    bitrate_kbps = Column(Integer)
    
    # File information
    file_path = Column(String(500))
    file_size_mb = Column(Decimal(10,2))
    segment_count = Column(Integer, default=1)
    current_segment = Column(Integer, default=1)
    storage_location = Column(String(500))
    
    # Status
    status = Column(SQLEnum(RecordingStatus), default=RecordingStatus.starting)
    error_message = Column(Text)
    
    # Metadata
    include_ai_overlay = Column(Boolean, default=False)
    retention_days = Column(Integer, default=30)
    created_by = Column(CHAR(36), ForeignKey('users.id'))
    
    # ZoneMinder Integration
    zoneminder_event_id = Column(BigInteger)
    
    # Relationships
    camera = relationship("Camera")
    site = relationship("Site")
    created_by_user = relationship("User")
    
    # Indexes
    __table_args__ = (
        Index('idx_recording_camera_active', 'camera_id', 'status'),
        Index('idx_recording_site_time', 'site_id', 'start_time'),
        Index('idx_recording_status', 'status'),
        Index('idx_recording_trigger', 'trigger_type', 'trigger_event_id'),
    )

class AIModelPerformanceLog(Base):
    __tablename__ = "ai_model_performance_logs"
    
    id = Column(CHAR(36), primary_key=True, default=generate_uuid)
    model_id = Column(CHAR(36), ForeignKey('ai_models.id'), nullable=False)
    
    # Performance metrics
    evaluation_date = Column(Date, nullable=False)
    evaluation_timestamp = Column(TIMESTAMP, default=func.current_timestamp())
    accuracy_score = Column(Decimal(5,2), nullable=False)
    precision_score = Column(Decimal(5,2), nullable=False)
    recall_score = Column(Decimal(5,2), nullable=False)
    f1_score = Column(Decimal(5,2), nullable=False)
    
    # Processing performance
    avg_processing_time_ms = Column(Integer, nullable=False)
    median_processing_time_ms = Column(Integer)
    max_processing_time_ms = Column(Integer)
    min_processing_time_ms = Column(Integer)
    
    # Detection statistics
    total_detections_processed = Column(Integer, default=0)
    true_positives = Column(Integer, default=0)
    false_positives = Column(Integer, default=0)
    false_negatives = Column(Integer, default=0)
    confidence_score_avg = Column(Decimal(5,2))
    confidence_score_std = Column(Decimal(5,2))
    
    # Context information
    test_dataset_id = Column(CHAR(36))
    site_id = Column(CHAR(36), ForeignKey('sites.id'))
    camera_subset = Column(JSON)  # Array of camera IDs used for evaluation
    
    # Evaluation metadata
    evaluation_type = Column(SQLEnum(EvaluationType), default=EvaluationType.automated)
    evaluated_by = Column(CHAR(36), ForeignKey('users.id'))
    evaluation_notes = Column(Text)
    
    # Comparison data
    compared_to_model_id = Column(CHAR(36), ForeignKey('ai_models.id'))
    performance_change_percentage = Column(Decimal(6,2))
    
    # Relationships
    model = relationship("AIModel", foreign_keys=[model_id])
    site = relationship("Site")
    evaluated_by_user = relationship("User")
    compared_to_model = relationship("AIModel", foreign_keys=[compared_to_model_id])
    
    # Indexes
    __table_args__ = (
        Index('idx_model_performance_model_date', 'model_id', 'evaluation_date'),
        Index('idx_model_performance_accuracy', 'accuracy_score'),
        Index('idx_model_performance_processing', 'avg_processing_time_ms'),
        Index('idx_model_performance_site', 'site_id', 'evaluation_date'),
    )

class AIDetectionAnalytics(Base):
    __tablename__ = "ai_detection_analytics"
    
    id = Column(CHAR(36), primary_key=True, default=generate_uuid)
    
    # Time and scope
    analysis_date = Column(Date, nullable=False)
    analysis_hour = Column(Integer)  # 0-23 for hourly granularity
    site_id = Column(CHAR(36), ForeignKey('sites.id'), nullable=False)
    camera_id = Column(CHAR(36), ForeignKey('cameras.id'))
    zone_id = Column(CHAR(36), ForeignKey('zones.id'))
    
    # Detection counts by type
    person_detections = Column(Integer, default=0)
    ppe_detections = Column(Integer, default=0)
    vehicle_detections = Column(Integer, default=0)
    safety_violation_detections = Column(Integer, default=0)
    equipment_detections = Column(Integer, default=0)
    activity_detections = Column(Integer, default=0)
    
    # Quality metrics
    total_detections = Column(Integer, default=0)
    high_confidence_detections = Column(Integer, default=0)  # confidence > 0.8
    medium_confidence_detections = Column(Integer, default=0)  # confidence 0.6-0.8
    low_confidence_detections = Column(Integer, default=0)  # confidence < 0.6
    avg_confidence_score = Column(Decimal(5,2))
    
    # Performance metrics
    avg_processing_time_ms = Column(Integer)
    total_processing_time_ms = Column(BigInteger)
    failed_processing_count = Column(Integer, default=0)
    
    # Safety analysis
    safety_violations_detected = Column(Integer, default=0)
    ppe_compliance_rate = Column(Decimal(5,2))
    risk_level_high_count = Column(Integer, default=0)
    risk_level_medium_count = Column(Integer, default=0)
    risk_level_low_count = Column(Integer, default=0)
    
    # Trend indicators
    detection_trend = Column(SQLEnum(TrendType))
    accuracy_trend = Column(SQLEnum(TrendType))
    
    # Model information
    primary_model_id = Column(CHAR(36), ForeignKey('ai_models.id'))
    model_version = Column(String(50))
    
    calculated_at = Column(TIMESTAMP, default=func.current_timestamp())
    
    # Relationships
    site = relationship("Site")
    camera = relationship("Camera")
    zone = relationship("Zone")
    primary_model = relationship("AIModel")
    
    # Indexes
    __table_args__ = (
        UniqueConstraint('site_id', 'camera_id', 'zone_id', 'analysis_date', 'analysis_hour', 
                        name='unique_analytics_scope'),
        Index('idx_detection_analytics_site_date', 'site_id', 'analysis_date'),
        Index('idx_detection_analytics_camera_date', 'camera_id', 'analysis_date'),
        Index('idx_detection_analytics_confidence', 'avg_confidence_score'),
        Index('idx_detection_analytics_performance', 'avg_processing_time_ms'),
    )

class CameraAIPerformance(Base):
    __tablename__ = "camera_ai_performance"
    
    id = Column(CHAR(36), primary_key=True, default=generate_uuid)
    camera_id = Column(CHAR(36), ForeignKey('cameras.id'), nullable=False)
    analysis_date = Column(Date, nullable=False)
    
    # Detection performance
    total_detections = Column(Integer, default=0)
    successful_detections = Column(Integer, default=0)
    failed_detections = Column(Integer, default=0)
    detection_success_rate = Column(Decimal(5,2))
    
    # Accuracy metrics
    validated_detections = Column(Integer, default=0)
    confirmed_true_positives = Column(Integer, default=0)
    confirmed_false_positives = Column(Integer, default=0)
    accuracy_rate = Column(Decimal(5,2))
    
    # Processing performance
    avg_processing_time_ms = Column(Integer)
    max_processing_time_ms = Column(Integer)
    min_processing_time_ms = Column(Integer)
    timeout_count = Column(Integer, default=0)
    
    # Quality scores
    image_quality_score = Column(Decimal(5,2))  # Based on resolution, lighting, etc.
    detection_quality_score = Column(Decimal(5,2))  # Based on detection success
    overall_performance_score = Column(Decimal(5,2))
    
    # Camera health indicators
    uptime_percentage = Column(Decimal(5,2))
    connection_issues_count = Column(Integer, default=0)
    stream_quality_issues_count = Column(Integer, default=0)
    
    # Detection type breakdown
    person_detection_rate = Column(Decimal(5,2))
    ppe_detection_rate = Column(Decimal(5,2))
    vehicle_detection_rate = Column(Decimal(5,2))
    equipment_detection_rate = Column(Decimal(5,2))
    
    # Comparative ranking
    site_ranking = Column(Integer)  # Rank among cameras at the site
    performance_tier = Column(SQLEnum(PerformanceTier))
    
    # Environment factors
    lighting_conditions_avg = Column(Decimal(5,2))  # 0-10 scale
    weather_impact_score = Column(Decimal(5,2))  # Weather effect on performance
    
    calculated_at = Column(TIMESTAMP, default=func.current_timestamp())
    
    # Relationships
    camera = relationship("Camera")
    
    # Indexes
    __table_args__ = (
        UniqueConstraint('camera_id', 'analysis_date', name='unique_camera_date'),
        Index('idx_camera_performance_date', 'analysis_date'),
        Index('idx_camera_performance_score', 'overall_performance_score'),
        Index('idx_camera_performance_accuracy', 'accuracy_rate'),
        Index('idx_camera_performance_tier', 'performance_tier', 'overall_performance_score'),
    )

# ANALYTICS & REPORTING TABLES
class Report(Base):
    __tablename__ = "reports"
    
    id = Column(CHAR(36), primary_key=True, default=generate_uuid)
    site_id = Column(CHAR(36), ForeignKey('sites.id'), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    report_type = Column(SQLEnum(ReportType), nullable=False)
    
    # Report configuration
    parameters = Column(JSON)  # Report generation parameters
    schedule_cron = Column(String(100))  # Cron expression for scheduled reports
    output_format = Column(SQLEnum(OutputFormat), default=OutputFormat.pdf)
    
    # Generation tracking
    created_by = Column(CHAR(36), ForeignKey('users.id'), nullable=False)
    last_generated = Column(TIMESTAMP)
    generation_status = Column(SQLEnum(GenerationStatus), default=GenerationStatus.pending)
    file_url = Column(String(500))
    file_size_bytes = Column(BigInteger)
    
    # Access control
    visibility = Column(SQLEnum(ReportVisibility), default=ReportVisibility.site)
    shared_with = Column(JSON)  # Array of user IDs with access
    
    created_at = Column(TIMESTAMP, default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, default=func.current_timestamp(), onupdate=func.current_timestamp())
    
    # Relationships
    site = relationship("Site")
    created_by_user = relationship("User")
    
    # Indexes
    __table_args__ = (
        Index('idx_reports_site', 'site_id'),
        Index('idx_reports_type', 'report_type'),
        Index('idx_reports_creator', 'created_by'),
        Index('idx_reports_schedule', 'schedule_cron'),
        Index('idx_reports_status', 'generation_status'),
    )

class AnalyticsCache(Base):
    __tablename__ = "analytics_cache"
    
    id = Column(CHAR(36), primary_key=True, default=generate_uuid)
    site_id = Column(CHAR(36), ForeignKey('sites.id'), nullable=False)
    metric_type = Column(String(100), nullable=False)  # 'dashboard_summary', 'safety_trends', etc.
    time_period = Column(String(50), nullable=False)  # 'hourly', 'daily', 'weekly', 'monthly'
    
    # Cache data
    data = Column(JSON, nullable=False)
    calculated_at = Column(TIMESTAMP, default=func.current_timestamp())
    expires_at = Column(TIMESTAMP, nullable=False)
    
    # Cache metadata
    calculation_time_ms = Column(Integer)
    data_points_count = Column(Integer)
    
    # Relationships
    site = relationship("Site")
    
    # Indexes
    __table_args__ = (
        UniqueConstraint('site_id', 'metric_type', 'time_period', name='unique_cache_key'),
        Index('idx_cache_expires', 'expires_at'),
        Index('idx_cache_site_metric', 'site_id', 'metric_type'),
        Index('idx_cache_calculated', 'calculated_at'),
    )

# SYSTEM & CONFIGURATION TABLES
class SystemConfig(Base):
    __tablename__ = "system_config"
    
    id = Column(CHAR(36), primary_key=True, default=generate_uuid)
    config_key = Column(String(255), unique=True, nullable=False)
    config_value = Column(JSON, nullable=False)
    config_type = Column(SQLEnum(ConfigType), nullable=False)
    description = Column(Text)
    
    # Configuration metadata
    category = Column(String(100))  # 'ai', 'camera', 'alerts', 'system'
    is_sensitive = Column(Boolean, default=False)  # For passwords, API keys
    requires_restart = Column(Boolean, default=False)
    
    # Change tracking
    created_by = Column(CHAR(36), ForeignKey('users.id'))
    updated_by = Column(CHAR(36), ForeignKey('users.id'))
    created_at = Column(TIMESTAMP, default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, default=func.current_timestamp(), onupdate=func.current_timestamp())
    
    # Relationships
    created_by_user = relationship("User", foreign_keys=[created_by])
    updated_by_user = relationship("User", foreign_keys=[updated_by])
    
    # Indexes
    __table_args__ = (
        Index('idx_config_category', 'category'),
        Index('idx_config_sensitive', 'is_sensitive'),
        Index('idx_config_updated', 'updated_at'),
    )

class AuditLog(Base):
    __tablename__ = "audit_logs"
    
    id = Column(CHAR(36), primary_key=True, default=generate_uuid)
    user_id = Column(CHAR(36), ForeignKey('users.id'))
    action = Column(String(255), nullable=False)
    resource_type = Column(String(100))  # 'alert', 'camera', 'site', etc.
    resource_id = Column(CHAR(36))
    
    # Action details
    old_values = Column(JSON)
    new_values = Column(JSON)
    ip_address = Column(String(45))  # IPv6 compatible
    user_agent = Column(Text)
    
    # Context
    site_id = Column(CHAR(36), ForeignKey('sites.id'))
    session_id = Column(String(255))
    request_id = Column(String(255))
    
    timestamp = Column(TIMESTAMP, default=func.current_timestamp())
    
    # Relationships
    user = relationship("User")
    site = relationship("Site")
    
    # Indexes
    __table_args__ = (
        Index('idx_audit_user_time', 'user_id', 'timestamp'),
        Index('idx_audit_resource', 'resource_type', 'resource_id'),
        Index('idx_audit_site', 'site_id'),
        Index('idx_audit_action', 'action'),
        Index('idx_audit_timestamp', 'timestamp'),
    )

class Notification(Base):
    __tablename__ = "notifications"
    
    id = Column(CHAR(36), primary_key=True, default=generate_uuid)
    user_id = Column(CHAR(36), ForeignKey('users.id'), nullable=False)
    title = Column(String(255), nullable=False)
    message = Column(Text)
    notification_type = Column(SQLEnum(NotificationType), nullable=False)
    
    # Notification data
    related_id = Column(CHAR(36))  # ID of related alert, report, etc.
    related_type = Column(String(100))  # 'alert', 'report', 'detection'
    data = Column(JSON)  # Additional notification data
    
    # Delivery
    channels = Column(JSON)  # ['in_app', 'email', 'sms', 'push']
    sent_at = Column(TIMESTAMP)
    delivery_status = Column(JSON)  # Status per channel
    
    # User interaction
    read_at = Column(TIMESTAMP)
    action_taken = Column(String(100))  # 'acknowledged', 'dismissed', 'clicked'
    action_taken_at = Column(TIMESTAMP)
    
    # Priority and expiry
    priority = Column(SQLEnum(NotificationPriority), default=NotificationPriority.medium)
    expires_at = Column(TIMESTAMP)
    
    created_at = Column(TIMESTAMP, default=func.current_timestamp())
    
    # Relationships
    user = relationship("User")
    
    # Indexes
    __table_args__ = (
        Index('idx_notifications_user_time', 'user_id', 'created_at'),
        Index('idx_notifications_type', 'notification_type'),
        Index('idx_notifications_unread', 'user_id', 'read_at'),
        Index('idx_notifications_priority', 'priority', 'created_at'),
        Index('idx_notifications_expires', 'expires_at'),
    )

# VIDEO & EVIDENCE MANAGEMENT TABLES
class VideoBookmark(Base):
    __tablename__ = "video_bookmarks"
    
    id = Column(CHAR(36), primary_key=True, default=generate_uuid)
    camera_id = Column(CHAR(36), ForeignKey('cameras.id'), nullable=False)
    user_id = Column(CHAR(36), ForeignKey('users.id'), nullable=False)
    
    # Temporal information
    bookmark_date = Column(Date, nullable=False)
    timestamp_seconds = Column(Integer, nullable=False)  # Seconds from start of day
    duration_seconds = Column(Integer, default=10)  # Bookmark duration for clips
    
    # Bookmark details
    title = Column(String(255), nullable=False)
    description = Column(Text)
    bookmark_type = Column(SQLEnum(BookmarkType), nullable=False)
    
    # Classification and priority
    priority_level = Column(SQLEnum(PriorityLevel), default=PriorityLevel.medium)
    severity = Column(SQLEnum(Severity), default=Severity.info)
    
    # Evidence and correlation
    related_alert_id = Column(CHAR(36), ForeignKey('alerts.id'))
    related_detection_id = Column(CHAR(36), ForeignKey('ai_detections.id'))
    evidence_quality = Column(SQLEnum(EvidenceQuality), default=EvidenceQuality.good)
    
    # User interaction
    is_shared = Column(Boolean, default=False)
    share_permissions = Column(JSON)  # Array of user IDs or roles with access
    
    # Visual markers
    thumbnail_timestamp = Column(Integer)  # Best representative frame
    color_code = Column(String(7), default='#FFA500')  # Hex color for timeline display
    
    # Metadata
    video_quality_at_time = Column(String(50))  # Resolution/quality at bookmark time
    weather_conditions = Column(String(100))
    lighting_conditions = Column(SQLEnum(LightingCondition))
    
    # Workflow status
    status = Column(SQLEnum(BookmarkStatus), default=BookmarkStatus.active)
    reviewed_by = Column(CHAR(36), ForeignKey('users.id'))
    reviewed_at = Column(TIMESTAMP)
    review_notes = Column(Text)
    
    created_at = Column(TIMESTAMP, default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, default=func.current_timestamp(), onupdate=func.current_timestamp())
    
    # Relationships
    camera = relationship("Camera")
    user = relationship("User", foreign_keys=[user_id])
    related_alert = relationship("Alert")
    related_detection = relationship("AIDetection")
    reviewed_by_user = relationship("User", foreign_keys=[reviewed_by])
    
    # Indexes
    __table_args__ = (
        UniqueConstraint('user_id', 'camera_id', 'bookmark_date', 'timestamp_seconds', 
                        name='unique_user_camera_timestamp'),
        Index('idx_video_bookmarks_camera_date', 'camera_id', 'bookmark_date'),
        Index('idx_video_bookmarks_user', 'user_id', 'created_at'),
        Index('idx_video_bookmarks_type', 'bookmark_type', 'priority_level'),
        Index('idx_video_bookmarks_timestamp', 'bookmark_date', 'timestamp_seconds'),
        Index('idx_video_bookmarks_status', 'status', 'created_at'),
        Index('idx_video_bookmarks_shared', 'is_shared'),
    )

class VideoAccessLog(Base):
    __tablename__ = "video_access_logs"
    
    id = Column(CHAR(36), primary_key=True, default=generate_uuid)
    user_id = Column(CHAR(36), ForeignKey('users.id'), nullable=False)
    camera_id = Column(CHAR(36), ForeignKey('cameras.id'), nullable=False)
    
    # Access session details
    session_id = Column(CHAR(36), nullable=False)
    access_start = Column(TIMESTAMP, default=func.current_timestamp())
    access_end = Column(TIMESTAMP)
    session_duration_minutes = Column(Integer)
    
    # Video details accessed
    video_date = Column(Date, nullable=False)
    start_timestamp_seconds = Column(Integer, nullable=False)  # Start time in video
    end_timestamp_seconds = Column(Integer)  # End time (if session completed)
    total_video_watched_seconds = Column(Integer, default=0)
    
    # Access method and context
    access_method = Column(SQLEnum(AccessMethod), default=AccessMethod.web_browser)
    access_reason = Column(SQLEnum(AccessReason), nullable=False)
    
    # User activity during session
    bookmarks_created = Column(Integer, default=0)
    screenshots_taken = Column(Integer, default=0)
    clips_exported = Column(Integer, default=0)
    playback_speed_changes = Column(Integer, default=0)
    
    # Technical details
    ip_address = Column(String(45))  # IPv6 compatible
    user_agent = Column(Text)
    browser_info = Column(JSON)
    
    # Legal and compliance
    legal_hold_flag = Column(Boolean, default=False)
    audit_flag = Column(Boolean, default=False)
    retention_period_override = Column(Integer)  # Days to retain this access record
    
    # Performance metrics
    initial_load_time_ms = Column(Integer)
    average_seek_time_ms = Column(Integer)
    total_pause_time_seconds = Column(Integer, default=0)
    
    # Access outcome
    session_complete = Column(Boolean, default=False)
    premature_termination_reason = Column(SQLEnum(TerminationReason))
    
    # Data export tracking
    export_count = Column(Integer, default=0)
    export_details = Column(JSON)  # Details of any exports performed
    
    # Relationships
    user = relationship("User")
    camera = relationship("Camera")
    
    # Indexes
    __table_args__ = (
        Index('idx_video_access_user_time', 'user_id', 'access_start'),
        Index('idx_video_access_camera_date', 'camera_id', 'video_date'),
        Index('idx_video_access_session', 'session_id'),
        Index('idx_video_access_legal', 'legal_hold_flag', 'audit_flag'),
        Index('idx_video_access_reason', 'access_reason', 'access_start'),
    )

class VideoExport(Base):
    __tablename__ = "video_exports"
    
    id = Column(CHAR(36), primary_key=True, default=generate_uuid)
    user_id = Column(CHAR(36), ForeignKey('users.id'), nullable=False)
    camera_id = Column(CHAR(36), ForeignKey('cameras.id'), nullable=False)
    
    # Export source details
    source_video_date = Column(Date, nullable=False)
    start_timestamp_seconds = Column(Integer, nullable=False)
    end_timestamp_seconds = Column(Integer, nullable=False)
    export_duration_seconds = Column(Integer, nullable=False)
    
    # Export configuration
    export_type = Column(SQLEnum(ExportType), nullable=False)
    export_format = Column(String(20), nullable=False)  # mp4, jpg, png, pdf, zip
    resolution = Column(String(20))  # Original, 1080p, 720p, 480p
    quality_setting = Column(SQLEnum(QualitySetting), default=QualitySetting.high)
    include_audio = Column(Boolean, default=True)
    
    # Evidence and legal
    export_purpose = Column(SQLEnum(ExportPurpose), nullable=False)
    chain_of_custody = Column(JSON)  # Evidence handling chain
    hash_verification = Column(String(128))  # File integrity hash
    digital_signature = Column(String(512))  # Legal authentication
    
    # File information
    original_filename = Column(String(255))
    stored_filename = Column(String(255))
    file_path = Column(String(500))
    file_size_bytes = Column(BigInteger)
    
    # Processing status
    export_status = Column(SQLEnum(ExportStatus), default=ExportStatus.requested)
    processing_started_at = Column(TIMESTAMP)
    processing_completed_at = Column(TIMESTAMP)
    processing_time_seconds = Column(Integer)
    error_message = Column(Text)
    
    # Access and sharing
    download_url = Column(String(500))
    share_token = Column(String(255), unique=True)
    download_expires_at = Column(TIMESTAMP)
    download_count = Column(Integer, default=0)
    max_download_count = Column(Integer, default=5)
    
    # Metadata preservation
    original_metadata = Column(JSON)  # Camera settings, weather, etc.
    bookmark_data = Column(JSON)  # Any bookmarks within the export timeframe
    incident_data = Column(JSON)  # Related alerts and detections
    
    # Audit and compliance
    export_justification = Column(Text, nullable=False)
    approval_required = Column(Boolean, default=False)
    approved_by = Column(CHAR(36), ForeignKey('users.id'))
    approved_at = Column(TIMESTAMP)
    legal_hold_applied = Column(Boolean, default=False)
    retention_period_days = Column(Integer, default=90)
    
    # Performance tracking
    compression_ratio = Column(Decimal(5,2))  # Original size vs final size
    processing_efficiency_score = Column(Decimal(3,1))  # 1-10 efficiency rating
    
    created_at = Column(TIMESTAMP, default=func.current_timestamp())
    
    # Relationships
    user = relationship("User", foreign_keys=[user_id])
    camera = relationship("Camera")
    approved_by_user = relationship("User", foreign_keys=[approved_by])
    
    # Indexes
    __table_args__ = (
        Index('idx_video_exports_user_date', 'user_id', 'created_at'),
        Index('idx_video_exports_camera', 'camera_id', 'source_video_date'),
        Index('idx_video_exports_status', 'export_status', 'created_at'),
        Index('idx_video_exports_purpose', 'export_purpose', 'created_at'),
        Index('idx_video_exports_legal', 'legal_hold_applied', 'retention_period_days'),
        Index('idx_video_exports_share', 'share_token', 'download_expires_at'),
    )

class VideoQualityMetric(Base):
    __tablename__ = "video_quality_metrics"
    
    id = Column(CHAR(36), primary_key=True, default=generate_uuid)
    camera_id = Column(CHAR(36), ForeignKey('cameras.id'), nullable=False)
    analysis_date = Column(Date, nullable=False)
    analysis_hour = Column(Integer, default=0)  # 0-23 for hourly analysis
    
    # Technical quality metrics
    average_bitrate_kbps = Column(Integer)
    average_fps = Column(Decimal(5,2))
    resolution_width = Column(Integer)
    resolution_height = Column(Integer)
    
    # Visual quality assessment
    sharpness_score = Column(Decimal(5,2))  # 0-10 scale
    brightness_score = Column(Decimal(5,2))  # 0-10 scale
    contrast_score = Column(Decimal(5,2))  # 0-10 scale
    color_accuracy_score = Column(Decimal(5,2))  # 0-10 scale
    noise_level_score = Column(Decimal(5,2))  # 0-10 scale (lower is better)
    
    # Environmental factors
    lighting_condition = Column(SQLEnum(LightingCondition))
    weather_impact = Column(SQLEnum(WeatherImpact))
    obstruction_detected = Column(Boolean, default=False)
    camera_shake_detected = Column(Boolean, default=False)
    
    # Usability for analysis
    forensic_quality_rating = Column(SQLEnum(ForensicQuality))
    person_identification_viability = Column(SQLEnum(IdentificationViability))
    activity_recognition_viability = Column(SQLEnum(IdentificationViability))
    
    # Storage and compression
    compression_efficiency = Column(Decimal(5,2))
    storage_size_mb = Column(Decimal(10,2))
    file_corruption_detected = Column(Boolean, default=False)
    
    # Recording continuity
    recording_gaps_detected = Column(Boolean, default=False)
    total_gap_duration_seconds = Column(Integer, default=0)
    frame_drops_count = Column(Integer, default=0)
    sync_issues_detected = Column(Boolean, default=False)
    
    # Analysis metadata
    analysis_method = Column(SQLEnum(AnalysisMethod), default=AnalysisMethod.automated)
    analysis_tool = Column(String(100))
    analysis_confidence = Column(Decimal(5,2))  # Confidence in the quality assessment
    
    # Improvement recommendations
    recommended_adjustments = Column(JSON)  # Settings adjustments to improve quality
    maintenance_flags = Column(JSON)  # Issues requiring camera maintenance
    
    calculated_at = Column(TIMESTAMP, default=func.current_timestamp())
    
    # Relationships
    camera = relationship("Camera")
    
    # Indexes
    __table_args__ = (
        UniqueConstraint('camera_id', 'analysis_date', 'analysis_hour', 
                        name='unique_camera_datetime'),
        Index('idx_video_quality_camera_date', 'camera_id', 'analysis_date'),
        Index('idx_video_quality_forensic', 'forensic_quality_rating', 'camera_id'),
        Index('idx_video_quality_overall', 'sharpness_score', 'brightness_score', 'contrast_score'),
        Index('idx_video_quality_issues', 'file_corruption_detected', 'recording_gaps_detected'),
        Index('idx_video_quality_lighting', 'lighting_condition', 'analysis_date'),
    )

# TIME-LAPSE & PROGRESS TRACKING TABLES
class TimelapseSequence(Base):
    __tablename__ = "timelapse_sequences"
    
    id = Column(CHAR(36), primary_key=True, default=generate_uuid)
    
    # Basic sequence information
    title = Column(String(255), nullable=False)
    description = Column(Text)
    site_id = Column(CHAR(36), ForeignKey('sites.id'), nullable=False)
    created_by = Column(CHAR(36), ForeignKey('users.id'), nullable=False)
    
    # Source configuration
    primary_camera_id = Column(CHAR(36), ForeignKey('cameras.id'), nullable=False)
    additional_camera_ids = Column(JSON)  # Array of additional camera IDs for multi-camera sequences
    
    # Time range
    start_datetime = Column(TIMESTAMP, nullable=False)
    end_datetime = Column(TIMESTAMP, nullable=False)
    duration_seconds = Column(Integer, nullable=False)
    
    # Generation settings
    compression_level = Column(SQLEnum(CompressionLevel), default=CompressionLevel.medium)
    frame_rate_fps = Column(Integer, default=30)
    playback_speed = Column(Decimal(5,2), default=1.0)  # Default playback speed multiplier
    resolution_width = Column(Integer, default=1920)
    resolution_height = Column(Integer, default=1080)
    
    # Processing information
    generation_status = Column(SQLEnum(GenerationStatus), default=GenerationStatus.queued)
    processing_started_at = Column(TIMESTAMP)
    processing_completed_at = Column(TIMESTAMP)
    processing_duration_seconds = Column(Integer)
    
    # File information
    output_file_path = Column(String(500))
    output_file_format = Column(String(10))  # mp4, gif, webm, avi
    file_size_bytes = Column(BigInteger)
    thumbnail_path = Column(String(500))
    preview_gif_path = Column(String(500))
    
    # Quality metrics
    total_frames_processed = Column(Integer)
    frames_with_activity = Column(Integer)
    activity_score = Column(Decimal(5,2))  # 0-10 overall activity level
    quality_score = Column(Decimal(5,2))  # 0-10 visual quality assessment
    
    # Metadata
    weather_conditions = Column(JSON)  # Weather during the time period
    project_phase = Column(String(100))  # Construction phase during sequence
    milestone_events = Column(JSON)  # Major milestones captured in sequence
    
    # Usage and sharing
    view_count = Column(Integer, default=0)
    download_count = Column(Integer, default=0)
    share_count = Column(Integer, default=0)
    bookmark_count = Column(Integer, default=0)
    
    # Status and lifecycle
    status = Column(SQLEnum(SequenceStatus), default=SequenceStatus.active)
    archived_at = Column(TIMESTAMP)
    retention_date = Column(Date)  # When sequence can be deleted
    
    # Error handling
    error_message = Column(Text)
    retry_count = Column(Integer, default=0)
    
    created_at = Column(TIMESTAMP, default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, default=func.current_timestamp(), onupdate=func.current_timestamp())
    
    # Relationships
    site = relationship("Site")
    created_by_user = relationship("User")
    primary_camera = relationship("Camera")
    
    # Indexes
    __table_args__ = (
        Index('idx_timelapse_sequences_site', 'site_id', 'created_at'),
        Index('idx_timelapse_sequences_creator', 'created_by', 'created_at'),
        Index('idx_timelapse_sequences_camera', 'primary_camera_id', 'start_datetime'),
        Index('idx_timelapse_sequences_status', 'generation_status', 'processing_started_at'),
        Index('idx_timelapse_sequences_timerange', 'start_datetime', 'end_datetime'),
        Index('idx_timelapse_sequences_quality', 'quality_score', 'activity_score'),
    )

class TimelapseBookmark(Base):
    __tablename__ = "timelapse_bookmarks"
    
    id = Column(CHAR(36), primary_key=True, default=generate_uuid)
    timelapse_sequence_id = Column(CHAR(36), ForeignKey('timelapse_sequences.id'), nullable=False)
    user_id = Column(CHAR(36), ForeignKey('users.id'), nullable=False)
    
    # Bookmark details
    bookmark_name = Column(String(255), nullable=False)
    description = Column(Text)
    
    # Temporal information
    timestamp_seconds = Column(Decimal(10,3), nullable=False)  # Precise timestamp within sequence
    frame_number = Column(Integer)  # Exact frame number for precise positioning
    
    # Context information
    bookmark_type = Column(SQLEnum(TimelapseBookmarkType), default=TimelapseBookmarkType.manual)
    activity_detected = Column(String(100))  # Type of activity at bookmark
    personnel_count = Column(Integer)  # Number of personnel visible at bookmark
    equipment_present = Column(JSON)  # Array of equipment visible
    
    # Visual markers
    thumbnail_path = Column(String(500))  # Thumbnail image at bookmark time
    marker_color = Column(String(7), default='#FFA500')  # Hex color for timeline display
    marker_icon = Column(String(50))  # Icon identifier for bookmark type
    
    # Annotations
    annotations = Column(JSON)  # Array of annotation objects with coordinates and text
    highlight_areas = Column(JSON)  # Array of highlight regions in the frame
    
    # Collaboration
    is_shared = Column(Boolean, default=False)
    shared_with = Column(JSON)  # Array of user IDs with access
    comments_enabled = Column(Boolean, default=True)
    
    # Workflow status
    status = Column(SQLEnum(SequenceStatus), default=SequenceStatus.active)
    reviewed = Column(Boolean, default=False)
    reviewed_by = Column(CHAR(36), ForeignKey('users.id'))
    reviewed_at = Column(TIMESTAMP)
    
    # Usage tracking
    access_count = Column(Integer, default=0)
    last_accessed = Column(TIMESTAMP)
    
    created_at = Column(TIMESTAMP, default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, default=func.current_timestamp(), onupdate=func.current_timestamp())
    
    # Relationships
    timelapse_sequence = relationship("TimelapseSequence")
    user = relationship("User", foreign_keys=[user_id])
    reviewed_by_user = relationship("User", foreign_keys=[reviewed_by])
    
    # Indexes
    __table_args__ = (
        UniqueConstraint('user_id', 'timelapse_sequence_id', 'timestamp_seconds', 
                        name='unique_user_sequence_timestamp'),
        Index('idx_timelapse_bookmarks_sequence', 'timelapse_sequence_id', 'timestamp_seconds'),
        Index('idx_timelapse_bookmarks_user', 'user_id', 'created_at'),
        Index('idx_timelapse_bookmarks_type', 'bookmark_type', 'status'),
        Index('idx_timelapse_bookmarks_shared', 'is_shared'),
    )

class TimelapseEvent(Base):
    __tablename__ = "timelapse_events"
    
    id = Column(CHAR(36), primary_key=True, default=generate_uuid)
    timelapse_sequence_id = Column(CHAR(36), ForeignKey('timelapse_sequences.id'), nullable=False)
    
    # Event timing
    event_timestamp = Column(TIMESTAMP, nullable=False)
    sequence_timestamp_seconds = Column(Decimal(10,3), nullable=False)  # Time within the sequence
    duration_seconds = Column(Integer)  # Event duration if applicable
    
    # Event classification
    event_type = Column(SQLEnum(TimelapseEventType), nullable=False)
    event_category = Column(String(100))  # More specific categorization
    
    # Event details
    event_title = Column(String(255), nullable=False)
    event_description = Column(Text)
    confidence_score = Column(Decimal(5,2))  # AI confidence in event detection
    
    # Detected elements
    personnel_count = Column(Integer, default=0)
    equipment_detected = Column(JSON)  # Array of detected equipment
    vehicle_count = Column(Integer, default=0)
    activity_level = Column(SQLEnum(ActivityLevel), default=ActivityLevel.moderate)
    
    # Spatial information
    detection_zones = Column(JSON)  # Array of zone IDs where event occurred
    bounding_boxes = Column(JSON)  # Coordinate data for detected objects
    camera_angle_info = Column(JSON)  # Camera positioning data
    
    # Correlation data
    related_alert_id = Column(CHAR(36), ForeignKey('alerts.id'))  # Link to safety alerts if applicable
    related_detection_ids = Column(JSON)  # Array of AI detection IDs
    milestone_reference = Column(String(255))  # Project milestone reference
    
    # Visual evidence
    thumbnail_path = Column(String(500))
    evidence_images = Column(JSON)  # Array of evidence image paths
    annotation_data = Column(JSON)  # Visual annotations and highlights
    
    # Impact assessment
    impact_level = Column(SQLEnum(ImpactLevel), default=ImpactLevel.minimal)
    safety_implications = Column(SQLEnum(SafetyImplications), default=SafetyImplications.none)
    
    # Verification and validation
    auto_detected = Column(Boolean, default=True)
    manually_verified = Column(Boolean, default=False)
    verified_by = Column(CHAR(36), ForeignKey('users.id'))
    verified_at = Column(TIMESTAMP)
    
    # Status
    status = Column(SQLEnum(EventStatus), default=EventStatus.detected)
    
    # Relationships
    timelapse_sequence = relationship("TimelapseSequence")
    related_alert = relationship("Alert")
    verified_by_user = relationship("User")
    
    # Indexes
    __table_args__ = (
        Index('idx_timelapse_events_sequence_time', 'timelapse_sequence_id', 'sequence_timestamp_seconds'),
        Index('idx_timelapse_events_type', 'event_type', 'event_category'),
        Index('idx_timelapse_events_timestamp', 'event_timestamp'),
        Index('idx_timelapse_events_impact', 'impact_level', 'safety_implications'),
        Index('idx_timelapse_events_verification', 'auto_detected', 'manually_verified'),
        Index('idx_timelapse_events_confidence', 'confidence_score'),
    )

class TimelapseShare(Base):
    __tablename__ = "timelapse_shares"
    
    id = Column(CHAR(36), primary_key=True, default=generate_uuid)
    timelapse_sequence_id = Column(CHAR(36), ForeignKey('timelapse_sequences.id'), nullable=False)
    
    # Sharing details
    shared_by = Column(CHAR(36), ForeignKey('users.id'), nullable=False)
    share_type = Column(SQLEnum(ShareType), nullable=False)
    
    # Recipients and access
    shared_with_users = Column(JSON)  # Array of user IDs
    shared_with_emails = Column(JSON)  # Array of email addresses for external sharing
    access_level = Column(SQLEnum(AccessLevel), default=AccessLevel.view)
    
    # Share configuration
    share_token = Column(String(255), unique=True)
    password_protected = Column(Boolean, default=False)
    password_hash = Column(String(255))
    
    # Playback context
    start_time_seconds = Column(Decimal(10,3), default=0)  # Starting playback position
    playback_speed = Column(Decimal(5,2), default=1.0)
    include_bookmarks = Column(Boolean, default=True)
    include_annotations = Column(Boolean, default=True)
    
    # Restrictions and limits
    expires_at = Column(TIMESTAMP)
    max_views = Column(Integer)
    max_downloads = Column(Integer)
    allowed_ip_ranges = Column(JSON)
    
    # Usage tracking
    view_count = Column(Integer, default=0)
    download_count = Column(Integer, default=0)
    unique_viewers = Column(Integer, default=0)
    last_accessed_at = Column(TIMESTAMP)
    
    # Access logs summary
    total_watch_time_seconds = Column(Integer, default=0)
    average_session_duration_seconds = Column(Integer)
    bookmarks_created_by_viewers = Column(Integer, default=0)
    
    # Feedback collection
    allow_feedback = Column(Boolean, default=False)
    feedback_collected = Column(JSON)  # Array of feedback objects
    
    # Share metadata
    share_title = Column(String(255))
    share_description = Column(Text)
    custom_thumbnail_path = Column(String(500))
    
    # Status and lifecycle
    status = Column(SQLEnum(ShareStatus), default=ShareStatus.active)
    revoked_at = Column(TIMESTAMP)
    revoked_by = Column(CHAR(36), ForeignKey('users.id'))
    
    created_at = Column(TIMESTAMP, default=func.current_timestamp())
    
    # Relationships
    timelapse_sequence = relationship("TimelapseSequence")
    shared_by_user = relationship("User", foreign_keys=[shared_by])
    revoked_by_user = relationship("User", foreign_keys=[revoked_by])
    
    # Indexes
    __table_args__ = (
        Index('idx_timelapse_shares_sequence', 'timelapse_sequence_id', 'created_at'),
        Index('idx_timelapse_shares_token', 'share_token', 'status'),
        Index('idx_timelapse_shares_sharer', 'shared_by', 'created_at'),
        Index('idx_timelapse_shares_expires', 'expires_at', 'status'),
        Index('idx_timelapse_shares_usage', 'view_count', 'download_count'),
    )

class ConstructionMilestone(Base):
    __tablename__ = "construction_milestones"
    
    id = Column(CHAR(36), primary_key=True, default=generate_uuid)
    site_id = Column(CHAR(36), ForeignKey('sites.id'), nullable=False)
    
    # Milestone identification
    milestone_name = Column(String(255), nullable=False)
    milestone_code = Column(String(50))  # Project-specific milestone identifier
    description = Column(Text)
    
    # Project context
    project_phase = Column(String(100))
    work_package = Column(String(100))
    contractor = Column(String(255))
    
    # Scheduling information
    planned_start_date = Column(Date)
    planned_completion_date = Column(Date)
    actual_start_date = Column(Date)
    actual_completion_date = Column(Date)
    
    # Progress tracking
    completion_percentage = Column(Decimal(5,2), default=0.00)
    status = Column(SQLEnum(MilestoneStatus), default=MilestoneStatus.not_started)
    
    # Dependencies
    prerequisite_milestones = Column(JSON)  # Array of milestone IDs that must be completed first
    dependent_milestones = Column(JSON)  # Array of milestone IDs that depend on this one
    
    # Quality and compliance
    quality_checkpoints = Column(JSON)  # Array of quality check requirements
    compliance_requirements = Column(JSON)  # Regulatory compliance requirements
    safety_requirements = Column(JSON)  # Safety-specific requirements
    
    # Documentation
    specification_documents = Column(JSON)  # Array of specification document references
    approval_documents = Column(JSON)  # Array of approval document references
    inspection_records = Column(JSON)  # Array of inspection record references
    
    # Visual documentation
    reference_images = Column(JSON)  # Array of reference/plan images
    progress_images = Column(JSON)  # Array of progress photos
    timelapse_sequences = Column(JSON)  # Array of related time-lapse sequence IDs
    
    # Budget and resources
    budgeted_amount = Column(Decimal(12,2))
    actual_cost = Column(Decimal(12,2))
    allocated_resources = Column(JSON)  # Personnel and equipment allocations
    
    # Timeline analysis
    planned_duration_days = Column(Integer)
    actual_duration_days = Column(Integer)
    delay_days = Column(Integer, default=0)
    delay_reasons = Column(JSON)  # Array of delay reason descriptions
    
    # Automated detection
    auto_detection_enabled = Column(Boolean, default=False)
    detection_criteria = Column(JSON)  # Criteria for automated milestone detection
    last_detection_check = Column(TIMESTAMP)
    
    # Approval workflow
    requires_approval = Column(Boolean, default=False)
    approved_by = Column(CHAR(36), ForeignKey('users.id'))
    approved_at = Column(TIMESTAMP)
    approval_notes = Column(Text)
    
    # Change management
    change_requests = Column(JSON)  # Array of change request references
    revision_number = Column(Integer, default=1)
    previous_version_id = Column(CHAR(36), ForeignKey('construction_milestones.id'))
    
    created_by = Column(CHAR(36), ForeignKey('users.id'), nullable=False)
    created_at = Column(TIMESTAMP, default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, default=func.current_timestamp(), onupdate=func.current_timestamp())
    
    # Relationships
    site = relationship("Site")
    created_by_user = relationship("User", foreign_keys=[created_by])
    approved_by_user = relationship("User", foreign_keys=[approved_by])
    previous_version = relationship("ConstructionMilestone", remote_side=[id])
    
    # Indexes
    __table_args__ = (
        UniqueConstraint('site_id', 'milestone_code', name='unique_site_milestone_code'),
        Index('idx_construction_milestones_site', 'site_id', 'planned_completion_date'),
        Index('idx_construction_milestones_status', 'status', 'completion_percentage'),
        Index('idx_construction_milestones_phase', 'project_phase', 'status'),
        Index('idx_construction_milestones_schedule', 'planned_start_date', 'planned_completion_date'),
        Index('idx_construction_milestones_delays', 'delay_days', 'status'),
        Index('idx_construction_milestones_creator', 'created_by', 'created_at'),
    )