"""
SQLAlchemy models for AI Construction Management System
Based on MASTER_DATABASE_SCHEMA.md - Phase 1: Core Tables
"""
from sqlalchemy import (
    Column, String, Text, Integer, DateTime, Boolean, 
    ForeignKey, Index, JSON, Enum as SQLEnum, Date, TIMESTAMP, Time,
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

class ReportGenerationStatus(enum.Enum):
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

class PathType(enum.Enum):
    inspection = "inspection"
    maintenance = "maintenance"
    emergency = "emergency"
    quality = "quality"
    tour = "tour"
    custom = "custom"

class PathStatus(enum.Enum):
    active = "active"
    inactive = "inactive"
    draft = "draft"
    archived = "archived"

class PathPriority(enum.Enum):
    critical = "critical"
    high = "high"
    medium = "medium"
    low = "low"

class ScheduleFrequency(enum.Enum):
    daily = "daily"
    weekly = "weekly"
    monthly = "monthly"
    on_demand = "on_demand"

class WeatherDependency(enum.Enum):
    any = "any"
    clear_only = "clear_only"
    daylight_only = "daylight_only"

class SkillLevel(enum.Enum):
    basic = "basic"
    intermediate = "intermediate"
    advanced = "advanced"
    expert = "expert"

class WaypointType(enum.Enum):
    checkpoint = "checkpoint"
    inspection = "inspection"
    maintenance = "maintenance"
    safety = "safety"
    assembly = "assembly"
    exit = "exit"
    viewpoint = "viewpoint"
    start = "start"
    end = "end"
    rest = "rest"

class ExecutionType(enum.Enum):
    scheduled = "scheduled"
    on_demand = "on_demand"
    emergency = "emergency"
    training = "training"
    audit = "audit"

class ExecutionStatus(enum.Enum):
    in_progress = "in_progress"
    completed = "completed"
    paused = "paused"
    cancelled = "cancelled"
    failed = "failed"

class TemplateType(enum.Enum):
    inspection = "inspection"
    maintenance = "maintenance"
    emergency = "emergency"
    quality = "quality"
    tour = "tour"
    custom = "custom"

class DifficultyLevel(enum.Enum):
    basic = "basic"
    intermediate = "intermediate"
    advanced = "advanced"
    expert = "expert"

class InspectionSafetyLevel(enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"

class AlertStatus(enum.Enum):
    open = "open"
    acknowledged = "acknowledged"
    investigating = "investigating"
    resolved = "resolved"
    false_positive = "false_positive"

class Status(enum.Enum):
    active = "active"
    inactive = "inactive"
    archived = "archived"

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
    generation_status = Column(SQLEnum(ReportGenerationStatus), default=ReportGenerationStatus.pending)
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

# FIELD OPERATIONS & ASSESSMENT TABLES
class InspectionPath(Base):
    __tablename__ = "inspection_paths"
    
    id = Column(CHAR(36), primary_key=True, default=generate_uuid)
    site_id = Column(CHAR(36), ForeignKey('sites.id'), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    
    # Path classification
    path_type = Column(SQLEnum(PathType), nullable=False)
    status = Column(SQLEnum(PathStatus), default=PathStatus.draft)
    priority = Column(SQLEnum(PathPriority), default=PathPriority.medium)
    
    # Assignment and ownership
    created_by = Column(CHAR(36), ForeignKey('users.id'), nullable=False)
    assigned_to = Column(String(255))  # Team or individual assignment
    assigned_user_ids = Column(JSON)  # Array of specific user IDs
    
    # Path characteristics
    estimated_duration_minutes = Column(Integer)
    total_distance_meters = Column(Decimal(10,2))
    waypoint_count = Column(Integer, default=0)
    zone_coverage = Column(JSON)  # Array of zone IDs covered
    
    # Performance metrics
    usage_count = Column(Integer, default=0)
    completion_rate = Column(Decimal(5,2), default=0.00)
    average_completion_time_minutes = Column(Integer)
    success_rate = Column(Decimal(5,2), default=0.00)
    
    # Path configuration
    path_coordinates = Column(JSON)  # Array of waypoint coordinates
    zone_sequence = Column(JSON)  # Ordered zone visit sequence
    required_equipment = Column(JSON)  # Required tools/equipment
    safety_requirements = Column(JSON)  # Safety protocols
    
    # Schedule and timing
    is_scheduled = Column(Boolean, default=False)
    schedule_frequency = Column(SQLEnum(ScheduleFrequency))
    schedule_days = Column(JSON)  # Days of week if recurring
    preferred_time_slots = Column(JSON)  # Time ranges for execution
    
    # Metadata
    weather_dependency = Column(SQLEnum(WeatherDependency))
    skill_level_required = Column(SQLEnum(SkillLevel))
    certification_required = Column(JSON)  # Required certifications
    
    created_at = Column(TIMESTAMP, default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, default=func.current_timestamp(), onupdate=func.current_timestamp())
    last_used = Column(TIMESTAMP)
    archived_at = Column(TIMESTAMP)
    
    # Relationships
    site = relationship("Site")
    created_by_user = relationship("User")
    waypoints = relationship("PathWaypoint", back_populates="path")
    executions = relationship("PathExecution", back_populates="path")
    
    # Indexes
    __table_args__ = (
        Index('idx_inspection_paths_site_type', 'site_id', 'path_type', 'status'),
        Index('idx_inspection_paths_priority', 'priority', 'status'),
        Index('idx_inspection_paths_usage', 'usage_count', 'completion_rate'),
        Index('idx_inspection_paths_schedule', 'is_scheduled', 'schedule_frequency'),
    )

class PathWaypoint(Base):
    __tablename__ = "path_waypoints"
    
    id = Column(CHAR(36), primary_key=True, default=generate_uuid)
    path_id = Column(CHAR(36), ForeignKey('inspection_paths.id'), nullable=False)
    waypoint_order = Column(Integer, nullable=False)
    waypoint_name = Column(String(255), nullable=False)
    description = Column(Text)
    
    # Location details
    coordinates_x = Column(Decimal(10,6), nullable=False)
    coordinates_y = Column(Decimal(10,6), nullable=False)
    elevation = Column(Decimal(8,2))
    zone_id = Column(CHAR(36), ForeignKey('zones.id'))
    
    # Waypoint configuration
    waypoint_type = Column(SQLEnum(WaypointType), nullable=False)
    is_mandatory = Column(Boolean, default=True)
    estimated_time_minutes = Column(Integer, default=5)
    inspection_checklist = Column(JSON)  # Inspection items at this waypoint
    
    # Camera and monitoring
    camera_id = Column(CHAR(36), ForeignKey('cameras.id'))
    monitoring_required = Column(Boolean, default=False)
    photo_required = Column(Boolean, default=False)
    notes_required = Column(Boolean, default=False)
    
    # Safety and access
    safety_level = Column(SQLEnum(SafetyLevel), default=SafetyLevel.safe)
    required_ppe = Column(JSON)  # PPE required at this waypoint
    access_restrictions = Column(JSON)  # Access level requirements
    weather_restrictions = Column(JSON)  # Weather limitations
    
    # Performance tracking
    visit_count = Column(Integer, default=0)
    average_time_spent_minutes = Column(Decimal(5,2), default=0.00)
    issue_frequency = Column(Decimal(5,2), default=0.00)
    last_visited = Column(TIMESTAMP)
    
    created_at = Column(TIMESTAMP, default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, default=func.current_timestamp(), onupdate=func.current_timestamp())
    
    # Relationships
    path = relationship("InspectionPath", back_populates="waypoints")
    zone = relationship("Zone")
    camera = relationship("Camera")
    
    # Indexes
    __table_args__ = (
        UniqueConstraint('path_id', 'waypoint_order', name='unique_path_waypoint_order'),
        Index('idx_path_waypoints_path_order', 'path_id', 'waypoint_order'),
        Index('idx_path_waypoints_zone', 'zone_id', 'waypoint_type'),
        Index('idx_path_waypoints_camera', 'camera_id', 'monitoring_required'),
        Index('idx_path_waypoints_performance', 'visit_count', 'issue_frequency'),
    )

class PathExecution(Base):
    __tablename__ = "path_executions"
    
    id = Column(CHAR(36), primary_key=True, default=generate_uuid)
    path_id = Column(CHAR(36), ForeignKey('inspection_paths.id'), nullable=False)
    executor_id = Column(CHAR(36), ForeignKey('users.id'), nullable=False)
    session_id = Column(CHAR(36), unique=True)  # Unique session identifier
    
    # Execution timing
    started_at = Column(TIMESTAMP, default=func.current_timestamp())
    completed_at = Column(TIMESTAMP)
    planned_duration_minutes = Column(Integer)
    actual_duration_minutes = Column(Integer)
    is_completed = Column(Boolean, default=False)
    
    # Execution details
    execution_type = Column(SQLEnum(ExecutionType), nullable=False)
    execution_reason = Column(Text)
    weather_conditions = Column(Text)
    equipment_used = Column(JSON)  # Equipment/tools used during execution
    
    # Progress tracking
    waypoints_visited = Column(Integer, default=0)
    waypoints_total = Column(Integer)
    completion_percentage = Column(Decimal(5,2), default=0.00)
    current_waypoint_id = Column(CHAR(36), ForeignKey('path_waypoints.id'))
    
    # Quality metrics
    quality_score = Column(Decimal(5,2), default=0.00)
    issues_found = Column(Integer, default=0)
    photos_taken = Column(Integer, default=0)
    notes_count = Column(Integer, default=0)
    
    # Performance indicators
    deviation_from_path = Column(Decimal(8,2), default=0.00)  # Meters off path
    pause_time_minutes = Column(Integer, default=0)
    break_count = Column(Integer, default=0)
    interruption_count = Column(Integer, default=0)
    
    # Status and outcome
    execution_status = Column(SQLEnum(ExecutionStatus), default=ExecutionStatus.in_progress)
    cancellation_reason = Column(Text)
    supervisor_reviewed = Column(Boolean, default=False)
    reviewed_by = Column(CHAR(36), ForeignKey('users.id'))
    review_score = Column(Decimal(3,1))  # 1-10 supervisor rating
    
    # Safety and compliance
    safety_incidents = Column(Integer, default=0)
    ppe_violations = Column(Integer, default=0)
    compliance_score = Column(Decimal(5,2), default=100.00)
    safety_notes = Column(Text)
    
    # GPS and tracking
    gps_tracking_enabled = Column(Boolean, default=True)
    gps_accuracy_avg = Column(Decimal(8,2))  # Average GPS accuracy in meters
    distance_traveled = Column(Decimal(10,2))  # Actual distance traveled
    route_deviation_score = Column(Decimal(5,2))  # How closely route was followed
    
    created_at = Column(TIMESTAMP, default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, default=func.current_timestamp(), onupdate=func.current_timestamp())
    
    # Relationships
    path = relationship("InspectionPath", back_populates="executions")
    executor = relationship("User", foreign_keys=[executor_id])
    current_waypoint = relationship("PathWaypoint")
    reviewed_by_user = relationship("User", foreign_keys=[reviewed_by])
    waypoint_visits = relationship("PathExecutionWaypoint", back_populates="execution")
    
    # Indexes
    __table_args__ = (
        Index('idx_path_executions_path_time', 'path_id', 'started_at'),
        Index('idx_path_executions_executor', 'executor_id', 'execution_status', 'started_at'),
        Index('idx_path_executions_status', 'execution_status', 'started_at'),
        Index('idx_path_executions_quality', 'quality_score', 'compliance_score'),
        Index('idx_path_executions_session', 'session_id', 'execution_status'),
    )

class PathExecutionWaypoint(Base):
    __tablename__ = "path_execution_waypoints"
    
    id = Column(CHAR(36), primary_key=True, default=generate_uuid)
    execution_id = Column(CHAR(36), ForeignKey('path_executions.id'), nullable=False)
    waypoint_id = Column(CHAR(36), ForeignKey('path_waypoints.id'), nullable=False)
    
    # Visit details
    visited_at = Column(TIMESTAMP)
    departure_at = Column(TIMESTAMP)
    time_spent_minutes = Column(Decimal(5,2))
    is_skipped = Column(Boolean, default=False)
    skip_reason = Column(Text)
    
    # Location verification
    actual_coordinates_x = Column(Decimal(10,6))
    actual_coordinates_y = Column(Decimal(10,6))
    gps_accuracy = Column(Decimal(8,2))
    location_verified = Column(Boolean, default=False)
    distance_from_waypoint = Column(Decimal(8,2))  # Distance from intended waypoint
    
    # Inspection results
    inspection_completed = Column(Boolean, default=False)
    inspection_score = Column(Decimal(5,2))
    issues_found = Column(Integer, default=0)
    photos_taken = Column(Integer, default=0)
    notes = Column(Text)
    
    # Compliance and safety
    ppe_compliance = Column(Boolean, default=True)
    safety_protocol_followed = Column(Boolean, default=True)
    environmental_conditions = Column(Text)
    
    # Media evidence
    photo_urls = Column(JSON)  # Array of photo URLs
    video_urls = Column(JSON)  # Array of video URLs
    document_urls = Column(JSON)  # Array of document URLs
    
    # Quality metrics
    inspector_confidence = Column(Decimal(5,2))  # Confidence in inspection quality
    requires_follow_up = Column(Boolean, default=False)
    follow_up_notes = Column(Text)
    priority_level = Column(SQLEnum(PathPriority))
    
    created_at = Column(TIMESTAMP, default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, default=func.current_timestamp(), onupdate=func.current_timestamp())
    
    # Relationships
    execution = relationship("PathExecution", back_populates="waypoint_visits")
    waypoint = relationship("PathWaypoint")
    
    # Indexes
    __table_args__ = (
        UniqueConstraint('execution_id', 'waypoint_id', name='unique_execution_waypoint'),
        Index('idx_execution_waypoints_execution', 'execution_id', 'visited_at'),
        Index('idx_execution_waypoints_waypoint', 'waypoint_id', 'visited_at'),
        Index('idx_execution_waypoints_issues', 'issues_found', 'requires_follow_up'),
        Index('idx_execution_waypoints_compliance', 'ppe_compliance', 'safety_protocol_followed'),
    )

class PathTemplate(Base):
    __tablename__ = "path_templates"
    
    id = Column(CHAR(36), primary_key=True, default=generate_uuid)
    template_name = Column(String(255), nullable=False)
    description = Column(Text)
    template_type = Column(SQLEnum(TemplateType), nullable=False)
    
    # Template configuration
    base_waypoint_count = Column(Integer)
    estimated_duration_minutes = Column(Integer)
    recommended_zones = Column(JSON)  # Suggested zone types
    required_equipment = Column(JSON)  # Standard equipment list
    
    # Template characteristics
    difficulty_level = Column(SQLEnum(DifficultyLevel), default=DifficultyLevel.basic)
    skill_requirements = Column(JSON)  # Required skills/certifications
    safety_level = Column(SQLEnum(InspectionSafetyLevel), default=InspectionSafetyLevel.medium)
    
    # Usage and popularity
    usage_count = Column(Integer, default=0)
    success_rate = Column(Decimal(5,2), default=0.00)
    user_rating = Column(Decimal(3,1), default=0.0)
    rating_count = Column(Integer, default=0)
    
    # Template structure
    waypoint_template = Column(JSON)  # Default waypoint configuration
    inspection_checklist = Column(JSON)  # Standard checklist items
    customizable_fields = Column(JSON)  # Fields that can be modified
    
    # Access and permissions
    is_public = Column(Boolean, default=True)
    created_by = Column(CHAR(36), ForeignKey('users.id'), nullable=False)
    organization_specific = Column(Boolean, default=False)
    industry_category = Column(String(100))
    
    # Versioning
    version = Column(String(20), default='1.0')
    parent_template_id = Column(CHAR(36), ForeignKey('path_templates.id'))
    is_active = Column(Boolean, default=True)
    
    created_at = Column(TIMESTAMP, default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, default=func.current_timestamp(), onupdate=func.current_timestamp())
    
    # Relationships
    created_by_user = relationship("User")
    parent_template = relationship("PathTemplate", remote_side=[id])
    
    # Indexes
    __table_args__ = (
        Index('idx_path_templates_type', 'template_type', 'is_active'),
        Index('idx_path_templates_difficulty', 'difficulty_level', 'safety_level'),
        Index('idx_path_templates_popularity', 'usage_count', 'user_rating'),
        Index('idx_path_templates_creator', 'created_by', 'created_at'),
    )


# NAVIGATION & STREET VIEW TABLES

# Navigation enums
class RouteType(enum.Enum):
    patrol = "patrol"
    inspection = "inspection"
    emergency_evacuation = "emergency_evacuation"
    material_transport = "material_transport"
    visitor_tour = "visitor_tour"
    maintenance = "maintenance"
    custom = "custom"

class PriorityLevel(enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"

class DifficultyLevel(enum.Enum):
    easy = "easy"
    moderate = "moderate"
    difficult = "difficult"
    expert = "expert"

class SafetyRating(enum.Enum):
    very_safe = "very_safe"
    safe = "safe"
    caution = "caution"
    hazardous = "hazardous"
    restricted = "restricted"

class AccessibilityLevel(enum.Enum):
    wheelchair = "wheelchair"
    mobility_aid = "mobility_aid"
    walking = "walking"
    restricted = "restricted"

class RouteCondition(enum.Enum):
    excellent = "excellent"
    good = "good"
    fair = "fair"
    poor = "poor"
    closed = "closed"

class AccessLevel(enum.Enum):
    public = "public"
    staff = "staff"
    supervisor = "supervisor"
    manager = "manager"
    restricted = "restricted"

class WaypointType(enum.Enum):
    start = "start"
    checkpoint = "checkpoint"
    turn = "turn"
    caution = "caution"
    stop = "stop"
    inspection = "inspection"
    emergency = "emergency"
    end = "end"
    custom = "custom"

class ActionRequired(enum.Enum):
    pass_through = "pass_through"
    pause = "pause"
    inspect = "inspect"
    report = "report"
    confirm = "confirm"
    emergency_check = "emergency_check"

class WaypointSafetyLevel(enum.Enum):
    safe = "safe"
    caution = "caution"
    danger = "danger"
    restricted = "restricted"

class IndoorOutdoor(enum.Enum):
    indoor = "indoor"
    outdoor = "outdoor"
    covered = "covered"

class LightingConditions(enum.Enum):
    excellent = "excellent"
    good = "good"
    poor = "poor"
    requires_flashlight = "requires_flashlight"

class WeatherExposure(enum.Enum):
    none = "none"
    partial = "partial"
    full = "full"

class ValidationMethod(enum.Enum):
    gps = "gps"
    qr_code = "qr_code"
    nfc = "nfc"
    manual_confirmation = "manual_confirmation"
    photo = "photo"

class ConditionStatus(enum.Enum):
    excellent = "excellent"
    good = "good"
    fair = "fair"
    poor = "poor"
    blocked = "blocked"

class SessionPurpose(enum.Enum):
    patrol = "patrol"
    inspection = "inspection"
    emergency = "emergency"
    training = "training"
    tour = "tour"
    maintenance = "maintenance"
    other = "other"

class SessionStatus(enum.Enum):
    started = "started"
    in_progress = "in_progress"
    paused = "paused"
    completed = "completed"
    cancelled = "cancelled"
    emergency_stopped = "emergency_stopped"

class VisibilityConditions(enum.Enum):
    excellent = "excellent"
    good = "good"
    fair = "fair"
    poor = "poor"
    very_poor = "very_poor"

class ZoomCapability(enum.Enum):
    none = "none"
    digital = "digital"
    optical = "optical"
    both = "both"

class StreamingProtocol(enum.Enum):
    RTSP = "RTSP"
    HTTP = "HTTP"
    WebRTC = "WebRTC"
    HLS = "HLS"

class HealthStatus(enum.Enum):
    excellent = "excellent"
    good = "good"
    fair = "fair"
    poor = "poor"
    offline = "offline"

class CameraStatus(enum.Enum):
    active = "active"
    inactive = "inactive"
    maintenance = "maintenance"
    decommissioned = "decommissioned"


class NavigationRoute(Base):
    __tablename__ = 'navigation_routes'
    
    id = Column(CHAR(36), primary_key=True, default=generate_uuid)
    site_id = Column(CHAR(36), ForeignKey('sites.id'), nullable=False)
    
    # Route identification
    route_name = Column(String(255), nullable=False)
    route_code = Column(String(50))
    description = Column(Text)
    
    # Route type and purpose
    route_type = Column(SQLEnum(RouteType), nullable=False)
    purpose = Column(String(255))
    priority_level = Column(SQLEnum(PriorityLevel), default=PriorityLevel.medium)
    
    # Geographic information
    start_coordinates = Column(JSON, nullable=False)
    end_coordinates = Column(JSON, nullable=False)
    bounding_box = Column(JSON)
    
    # Route characteristics
    total_distance_meters = Column(Decimal(10,2), nullable=False)
    estimated_duration_minutes = Column(Integer, nullable=False)
    elevation_change_meters = Column(Decimal(6,2), default=0)
    difficulty_level = Column(SQLEnum(DifficultyLevel), default=DifficultyLevel.easy)
    
    # Safety and accessibility
    safety_rating = Column(SQLEnum(SafetyRating), default=SafetyRating.safe)
    accessibility_level = Column(SQLEnum(AccessibilityLevel), default=AccessibilityLevel.walking)
    ppe_requirements = Column(JSON)
    hazard_warnings = Column(JSON)
    
    # Time and weather constraints
    time_restrictions = Column(JSON)
    weather_limitations = Column(JSON)
    seasonal_availability = Column(JSON)
    
    # Performance tracking
    usage_count = Column(Integer, default=0)
    completion_rate = Column(Decimal(5,2), default=100.00)
    average_completion_time_minutes = Column(Decimal(6,2))
    success_rate = Column(Decimal(5,2), default=100.00)
    last_successful_completion = Column(TIMESTAMP)
    
    # Route optimization
    optimization_score = Column(Decimal(5,2))
    alternative_routes = Column(JSON)
    traffic_pattern_data = Column(JSON)
    
    # Maintenance and updates
    last_survey_date = Column(Date)
    next_maintenance_date = Column(Date)
    route_condition = Column(SQLEnum(RouteCondition), default=RouteCondition.good)
    maintenance_notes = Column(Text)
    
    # Access control
    access_level = Column(SQLEnum(AccessLevel), default=AccessLevel.staff)
    authorized_roles = Column(JSON)
    restricted_users = Column(JSON)
    
    # Version control
    version_number = Column(Integer, default=1)
    previous_version_id = Column(CHAR(36), ForeignKey('navigation_routes.id'))
    change_log = Column(JSON)
    
    # Status
    status = Column(SQLEnum(Status), default=Status.active)
    created_by = Column(CHAR(36), ForeignKey('users.id'), nullable=False)
    created_at = Column(TIMESTAMP, default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, default=func.current_timestamp(), onupdate=func.current_timestamp())
    
    # Relationships
    site = relationship("Site")
    created_by_user = relationship("User")
    previous_version = relationship("NavigationRoute", remote_side=[id])
    
    # Indexes
    __table_args__ = (
        Index('idx_navigation_routes_site', 'site_id', 'status'),
        Index('idx_navigation_routes_type', 'route_type', 'priority_level'),
        Index('idx_navigation_routes_performance', 'completion_rate', 'success_rate'),
        Index('idx_navigation_routes_safety', 'safety_rating', 'accessibility_level'),
        Index('idx_navigation_routes_creator', 'created_by', 'created_at'),
        UniqueConstraint('site_id', 'route_code', name='unique_site_route_code'),
    )


class RouteWaypoint(Base):
    __tablename__ = 'route_waypoints'
    
    id = Column(CHAR(36), primary_key=True, default=generate_uuid)
    route_id = Column(CHAR(36), ForeignKey('navigation_routes.id'), nullable=False)
    
    # Waypoint identification
    waypoint_name = Column(String(255), nullable=False)
    waypoint_code = Column(String(50))
    sequence_order = Column(Integer, nullable=False)
    
    # Geographic coordinates
    latitude = Column(Decimal(10,7), nullable=False)
    longitude = Column(Decimal(10,7), nullable=False)
    elevation = Column(Decimal(6,2), default=0)
    coordinate_system = Column(String(50), default='WGS84')
    
    # Positioning accuracy
    horizontal_accuracy_meters = Column(Decimal(5,2), default=3.0)
    vertical_accuracy_meters = Column(Decimal(5,2), default=5.0)
    gps_quality_score = Column(Decimal(3,1), default=8.0)
    
    # Waypoint type and purpose
    waypoint_type = Column(SQLEnum(WaypointType), nullable=False)
    action_required = Column(SQLEnum(ActionRequired), default=ActionRequired.pass_through)
    
    # Navigation instructions
    approach_instructions = Column(Text, nullable=False)
    departure_instructions = Column(Text)
    audio_instructions = Column(Text)
    visual_markers = Column(Text)
    
    # Distance and timing
    distance_from_previous_meters = Column(Decimal(8,2), default=0)
    estimated_travel_time_minutes = Column(Decimal(5,2), default=0)
    recommended_pause_duration_seconds = Column(Integer, default=0)
    
    # Safety and hazard information
    safety_level = Column(SQLEnum(WaypointSafetyLevel), default=WaypointSafetyLevel.safe)
    hazard_types = Column(JSON)
    safety_equipment_required = Column(JSON)
    emergency_procedures = Column(Text)
    
    # Camera and monitoring
    associated_camera_ids = Column(JSON)
    monitoring_required = Column(Boolean, default=False)
    photo_documentation_required = Column(Boolean, default=False)
    
    # Environmental conditions
    indoor_outdoor = Column(SQLEnum(IndoorOutdoor), default=IndoorOutdoor.outdoor)
    lighting_conditions = Column(SQLEnum(LightingConditions), default=LightingConditions.good)
    weather_exposure = Column(SQLEnum(WeatherExposure), default=WeatherExposure.partial)
    
    # Interactive features
    qr_code_present = Column(Boolean, default=False)
    qr_code_data = Column(String(255))
    nfc_tag_present = Column(Boolean, default=False)
    beacon_uuid = Column(String(255))
    
    # Validation and verification
    checkpoint_validation_required = Column(Boolean, default=False)
    validation_method = Column(SQLEnum(ValidationMethod), default=ValidationMethod.gps)
    validation_radius_meters = Column(Decimal(5,2), default=5.0)
    
    # Performance tracking
    average_arrival_time_minutes = Column(Decimal(6,2))
    completion_rate = Column(Decimal(5,2), default=100.00)
    skip_rate = Column(Decimal(5,2), default=0.00)
    issue_report_count = Column(Integer, default=0)
    
    # Maintenance
    last_inspection_date = Column(Date)
    condition_status = Column(SQLEnum(ConditionStatus), default=ConditionStatus.good)
    maintenance_required = Column(Boolean, default=False)
    maintenance_notes = Column(Text)
    
    # Status
    status = Column(SQLEnum(Status), default=Status.active)
    created_at = Column(TIMESTAMP, default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, default=func.current_timestamp(), onupdate=func.current_timestamp())
    
    # Relationships
    route = relationship("NavigationRoute")
    
    # Indexes
    __table_args__ = (
        Index('idx_route_waypoints_route_sequence', 'route_id', 'sequence_order'),
        Index('idx_route_waypoints_coordinates', 'latitude', 'longitude'),
        Index('idx_route_waypoints_type', 'waypoint_type', 'action_required'),
        Index('idx_route_waypoints_safety', 'safety_level'),
        Index('idx_route_waypoints_performance', 'completion_rate'),
        UniqueConstraint('route_id', 'sequence_order', name='unique_route_sequence'),
        UniqueConstraint('route_id', 'waypoint_code', name='unique_route_waypoint_code'),
    )


class NavigationSession(Base):
    __tablename__ = 'navigation_sessions'
    
    id = Column(CHAR(36), primary_key=True, default=generate_uuid)
    user_id = Column(CHAR(36), ForeignKey('users.id'), nullable=False)
    route_id = Column(CHAR(36), ForeignKey('navigation_routes.id'), nullable=False)
    
    # Session identification
    session_name = Column(String(255))
    session_purpose = Column(SQLEnum(SessionPurpose), nullable=False)
    
    # Timing information
    started_at = Column(TIMESTAMP, default=func.current_timestamp())
    ended_at = Column(TIMESTAMP)
    total_duration_minutes = Column(Decimal(8,2))
    planned_duration_minutes = Column(Integer)
    
    # Session status
    session_status = Column(SQLEnum(SessionStatus), nullable=False, default=SessionStatus.started)
    completion_percentage = Column(Decimal(5,2), default=0.00)
    
    # Route progress
    current_waypoint_id = Column(CHAR(36), ForeignKey('route_waypoints.id'))
    waypoints_completed = Column(Integer, default=0)
    waypoints_skipped = Column(Integer, default=0)
    total_waypoints = Column(Integer, nullable=False)
    
    # Distance and movement
    total_distance_traveled_meters = Column(Decimal(10,2), default=0)
    planned_distance_meters = Column(Decimal(10,2))
    deviation_distance_meters = Column(Decimal(8,2), default=0)
    
    # Performance metrics
    average_speed_mps = Column(Decimal(5,2))
    max_speed_mps = Column(Decimal(5,2))
    pause_count = Column(Integer, default=0)
    total_pause_duration_minutes = Column(Decimal(8,2), default=0)
    
    # GPS tracking data
    gps_track_data = Column(JSON)
    gps_accuracy_average = Column(Decimal(5,2))
    gps_signal_quality_average = Column(Decimal(3,1))
    indoor_positioning_used = Column(Boolean, default=False)
    
    # Safety and compliance
    safety_incidents = Column(Integer, default=0)
    ppe_compliance_checks = Column(Integer, default=0)
    ppe_compliance_failures = Column(Integer, default=0)
    hazard_encounters = Column(Integer, default=0)
    emergency_stops = Column(Integer, default=0)
    
    # Communication and reporting
    reports_submitted = Column(Integer, default=0)
    photos_taken = Column(Integer, default=0)
    voice_notes_recorded = Column(Integer, default=0)
    emergency_calls_made = Column(Integer, default=0)
    
    # Device and connectivity
    device_type = Column(String(100))
    device_id = Column(String(255))
    connectivity_issues = Column(Integer, default=0)
    offline_periods = Column(JSON)
    
    # Weather and environmental
    weather_conditions = Column(JSON)
    visibility_conditions = Column(SQLEnum(VisibilityConditions), default=VisibilityConditions.good)
    temperature_celsius = Column(Decimal(4,1))
    
    # Session quality assessment
    navigation_accuracy_score = Column(Decimal(3,1))
    route_efficiency_score = Column(Decimal(3,1))
    safety_compliance_score = Column(Decimal(3,1))
    overall_session_rating = Column(Decimal(3,1))
    
    # Issues and feedback
    technical_issues = Column(JSON)
    route_feedback = Column(Text)
    improvement_suggestions = Column(Text)
    
    # Approval and verification
    supervisor_review_required = Column(Boolean, default=False)
    reviewed_by = Column(CHAR(36), ForeignKey('users.id'))
    reviewed_at = Column(TIMESTAMP)
    approved = Column(Boolean, default=False)
    
    # Data export and sharing
    session_report_generated = Column(Boolean, default=False)
    report_file_path = Column(String(500))
    shared_with_users = Column(JSON)
    
    # Status
    archived = Column(Boolean, default=False)
    archived_at = Column(TIMESTAMP)
    
    # Relationships
    user = relationship("User", foreign_keys=[user_id])
    route = relationship("NavigationRoute")
    current_waypoint = relationship("RouteWaypoint")
    reviewed_by_user = relationship("User", foreign_keys=[reviewed_by])
    
    # Indexes
    __table_args__ = (
        Index('idx_navigation_sessions_user_time', 'user_id', 'started_at'),
        Index('idx_navigation_sessions_route', 'route_id', 'started_at'),
        Index('idx_navigation_sessions_status', 'session_status', 'started_at'),
        Index('idx_navigation_sessions_performance', 'completion_percentage', 'total_duration_minutes'),
        Index('idx_navigation_sessions_safety', 'safety_incidents', 'ppe_compliance_failures'),
        Index('idx_navigation_sessions_reviewed', 'supervisor_review_required', 'reviewed_by'),
    )


class StreetViewCamera(Base):
    __tablename__ = 'street_view_cameras'
    
    id = Column(CHAR(36), primary_key=True, default=generate_uuid)
    camera_id = Column(CHAR(36), ForeignKey('cameras.id'), nullable=False)
    
    # Street view specific configuration
    is_street_view_enabled = Column(Boolean, default=False)
    street_view_priority = Column(Integer, default=1)
    
    # Camera positioning and coverage
    field_of_view_degrees = Column(Integer, default=90)
    tilt_angle_degrees = Column(Integer, default=0)
    pan_range_start_degrees = Column(Integer, default=0)
    pan_range_end_degrees = Column(Integer, default=360)
    zoom_capability = Column(SQLEnum(ZoomCapability), default=ZoomCapability.digital)
    
    # PTZ capabilities
    ptz_enabled = Column(Boolean, default=False)
    pan_speed_degrees_per_second = Column(Decimal(6,2), default=10.0)
    tilt_speed_degrees_per_second = Column(Decimal(6,2), default=10.0)
    zoom_levels = Column(JSON)
    preset_positions = Column(JSON)
    
    # Street view quality settings
    streaming_resolution = Column(String(20), default='1080p')
    streaming_fps = Column(Integer, default=30)
    streaming_bitrate_kbps = Column(Integer, default=5000)
    low_light_enhancement = Column(Boolean, default=True)
    image_stabilization = Column(Boolean, default=True)
    
    # GPS and positioning
    precise_latitude = Column(Decimal(10,7))
    precise_longitude = Column(Decimal(10,7))
    precise_elevation = Column(Decimal(6,2))
    mounting_height_meters = Column(Decimal(5,2), default=3.0)
    orientation_degrees = Column(Decimal(6,2), default=0)
    
    # Coverage and routing integration
    route_coverage = Column(JSON)
    waypoint_coverage = Column(JSON)
    coverage_radius_meters = Column(Decimal(6,2), default=50)
    optimal_viewing_distance_meters = Column(Decimal(6,2), default=25)
    
    # AI and analytics integration
    ai_detection_enabled = Column(Boolean, default=True)
    real_time_analysis = Column(Boolean, default=True)
    detection_confidence_threshold = Column(Decimal(3,2), default=0.70)
    alert_trigger_types = Column(JSON)
    
    # Overlay and augmented reality
    overlay_enabled = Column(Boolean, default=True)
    overlay_elements = Column(JSON)
    ar_markers_supported = Column(Boolean, default=False)
    compass_overlay = Column(Boolean, default=True)
    coordinate_overlay = Column(Boolean, default=False)
    
    # Environmental considerations
    weather_protection_rating = Column(String(10))
    operating_temperature_min_celsius = Column(Decimal(4,1), default=-20)
    operating_temperature_max_celsius = Column(Decimal(4,1), default=50)
    night_vision_capability = Column(Boolean, default=False)
    infrared_illumination = Column(Boolean, default=False)
    
    # Maintenance and monitoring
    health_check_interval_minutes = Column(Integer, default=60)
    last_health_check = Column(TIMESTAMP)
    health_status = Column(SQLEnum(HealthStatus), default=HealthStatus.good)
    maintenance_schedule = Column(JSON)
    
    # Performance metrics
    uptime_percentage = Column(Decimal(5,2), default=99.0)
    average_response_time_ms = Column(Integer, default=200)
    data_usage_mb_per_hour = Column(Decimal(8,2), default=1000)
    viewer_session_count = Column(Integer, default=0)
    
    # Access control
    public_access = Column(Boolean, default=False)
    authorized_user_roles = Column(JSON)
    viewing_restrictions = Column(JSON)
    
    # Integration settings
    zoneminder_monitor_id = Column(String(50))
    streaming_protocol = Column(SQLEnum(StreamingProtocol), default=StreamingProtocol.RTSP)
    streaming_url = Column(String(500))
    backup_streaming_url = Column(String(500))
    
    # Status and lifecycle
    status = Column(SQLEnum(CameraStatus), default=CameraStatus.active)
    installation_date = Column(Date)
    warranty_expiration_date = Column(Date)
    
    created_at = Column(TIMESTAMP, default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, default=func.current_timestamp(), onupdate=func.current_timestamp())
    
    # Relationships
    camera = relationship("Camera")
    
    # Indexes
    __table_args__ = (
        Index('idx_street_view_cameras_enabled', 'is_street_view_enabled', 'street_view_priority'),
        Index('idx_street_view_cameras_ptz', 'ptz_enabled', 'status'),
        Index('idx_street_view_cameras_coordinates', 'precise_latitude', 'precise_longitude'),
        Index('idx_street_view_cameras_health', 'health_status', 'last_health_check'),
        Index('idx_street_view_cameras_performance', 'uptime_percentage', 'average_response_time_ms'),
    )


# COMPLETE ANALYTICS & REPORTING TABLES

# Analytics enums
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

class Visibility(enum.Enum):
    private = "private"
    site = "site"
    company = "company"
    public = "public"

class CertificationType(enum.Enum):
    safety = "safety"
    technical = "technical"
    license = "license"
    training = "training"
    medical = "medical"

class CertificationStatus(enum.Enum):
    active = "active"
    expired = "expired"
    suspended = "suspended"
    pending_renewal = "pending_renewal"

class VerificationStatus(enum.Enum):
    verified = "verified"
    pending = "pending"
    rejected = "rejected"


class UserCertification(Base):
    __tablename__ = 'user_certifications'
    
    id = Column(CHAR(36), primary_key=True, default=generate_uuid)
    user_id = Column(CHAR(36), ForeignKey('users.id'), nullable=False)
    
    # Certification details
    certification_name = Column(String(255), nullable=False)
    certification_type = Column(SQLEnum(CertificationType), nullable=False)
    certification_number = Column(String(100))
    issuing_authority = Column(String(255))
    
    # Validity and compliance
    issue_date = Column(Date, nullable=False)
    expiry_date = Column(Date)
    renewal_required = Column(Boolean, default=True)
    renewal_period_months = Column(Integer)
    
    # Status tracking
    status = Column(SQLEnum(CertificationStatus), default=CertificationStatus.active)
    verification_status = Column(SQLEnum(VerificationStatus), default=VerificationStatus.pending)
    
    # Compliance requirements
    required_for_roles = Column(JSON)
    required_for_zones = Column(JSON)
    
    # Files and documentation
    certificate_file_path = Column(String(500))
    verification_documents = Column(JSON)
    
    # Audit trail
    created_by = Column(CHAR(36), ForeignKey('users.id'))
    verified_by = Column(CHAR(36), ForeignKey('users.id'))
    last_verification_check = Column(Date)
    
    created_at = Column(TIMESTAMP, default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, default=func.current_timestamp(), onupdate=func.current_timestamp())
    
    # Relationships
    user = relationship("User", foreign_keys=[user_id])
    created_by_user = relationship("User", foreign_keys=[created_by])
    verified_by_user = relationship("User", foreign_keys=[verified_by])
    
    # Indexes
    __table_args__ = (
        Index('idx_user_certifications_user', 'user_id'),
        Index('idx_user_certifications_type', 'certification_type'),
        Index('idx_user_certifications_status', 'status'),
        Index('idx_user_certifications_expiry', 'expiry_date'),
        UniqueConstraint('user_id', 'certification_name', 'certification_number', name='unique_user_certification'),
    )


class PerformanceMetric(Base):
    __tablename__ = 'performance_metrics'
    
    id = Column(CHAR(36), primary_key=True, default=generate_uuid)
    site_id = Column(CHAR(36), ForeignKey('sites.id'), nullable=False)
    metric_date = Column(Date, nullable=False)
    metric_hour = Column(Integer)  # 0-23 for hourly granularity
    metric_type = Column(String(100), nullable=False)  # 'safety', 'productivity', 'efficiency'
    
    # Metric values
    metric_value = Column(Decimal(10,2), nullable=False)
    target_value = Column(Decimal(10,2))
    baseline_value = Column(Decimal(10,2))
    threshold_warning = Column(Decimal(10,2))
    threshold_critical = Column(Decimal(10,2))
    
    # Context and metadata
    measurement_unit = Column(String(50))  # 'percentage', 'count', 'minutes', etc.
    data_source = Column(String(100))  # 'ai_detection', 'manual_entry', 'sensor'
    calculation_method = Column(String(200))
    confidence_score = Column(Decimal(3,2))  # 0-1 confidence in measurement
    
    # Performance indicators
    is_kpi = Column(Boolean, default=False)  # Key Performance Indicator
    trend_direction = Column(String(20))  # 'up', 'down', 'stable'
    variance_from_target = Column(Decimal(10,2))
    performance_grade = Column(String(5))  # 'A+', 'A', 'B', 'C', 'D', 'F'
    
    # Aggregation info
    sample_size = Column(Integer)
    aggregation_period = Column(String(20))  # 'hourly', 'daily', 'weekly'
    raw_data_points = Column(JSON)
    
    created_at = Column(TIMESTAMP, default=func.current_timestamp())
    calculated_by = Column(CHAR(36), ForeignKey('users.id'))
    
    # Relationships
    site = relationship("Site")
    calculated_by_user = relationship("User")
    
    # Indexes
    __table_args__ = (
        Index('idx_performance_metrics_site_date', 'site_id', 'metric_date'),
        Index('idx_performance_metrics_type', 'metric_type', 'is_kpi'),
        Index('idx_performance_metrics_value', 'metric_value'),
        UniqueConstraint('site_id', 'metric_date', 'metric_hour', 'metric_type', name='unique_performance_metric'),
    )


class TrendAnalysis(Base):
    __tablename__ = 'trend_analyses'
    
    id = Column(CHAR(36), primary_key=True, default=generate_uuid)
    site_id = Column(CHAR(36), ForeignKey('sites.id'))
    analysis_name = Column(String(255), nullable=False)
    analysis_type = Column(String(100), nullable=False)  # 'safety_trend', 'productivity_trend'
    
    # Analysis period
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    analysis_period_days = Column(Integer, nullable=False)
    
    # Trend data
    trend_direction = Column(String(20))  # 'improving', 'declining', 'stable', 'volatile'
    trend_strength = Column(Decimal(3,2))  # 0-1 strength of trend
    correlation_coefficient = Column(Decimal(4,3))  # -1 to 1
    statistical_significance = Column(Decimal(4,3))  # p-value
    
    # Trend metrics
    starting_value = Column(Decimal(10,2))
    ending_value = Column(Decimal(10,2))
    peak_value = Column(Decimal(10,2))
    lowest_value = Column(Decimal(10,2))
    average_value = Column(Decimal(10,2))
    change_percentage = Column(Decimal(6,2))
    
    # Predictions and forecasting
    predicted_next_value = Column(Decimal(10,2))
    prediction_confidence = Column(Decimal(3,2))
    forecast_horizon_days = Column(Integer, default=30)
    seasonal_patterns = Column(JSON)
    
    # Analysis results
    key_insights = Column(JSON)
    contributing_factors = Column(JSON)
    recommendations = Column(JSON)
    risk_indicators = Column(JSON)
    
    # Metadata
    analysis_algorithm = Column(String(100))  # 'linear_regression', 'moving_average'
    data_quality_score = Column(Decimal(3,2))
    sample_size = Column(Integer)
    
    created_at = Column(TIMESTAMP, default=func.current_timestamp())
    created_by = Column(CHAR(36), ForeignKey('users.id'), nullable=False)
    
    # Relationships
    site = relationship("Site")
    created_by_user = relationship("User")
    
    # Indexes
    __table_args__ = (
        Index('idx_trend_analyses_site_date', 'site_id', 'start_date'),
        Index('idx_trend_analyses_type', 'analysis_type'),
        Index('idx_trend_analyses_trend', 'trend_direction', 'trend_strength'),
    )


class ReportTemplate(Base):
    __tablename__ = 'report_templates'
    
    id = Column(CHAR(36), primary_key=True, default=generate_uuid)
    template_name = Column(String(255), nullable=False)
    template_type = Column(SQLEnum(ReportType), nullable=False)
    description = Column(Text)
    
    # Template configuration
    template_structure = Column(JSON, nullable=False)  # Report sections and layout
    default_parameters = Column(JSON)  # Default parameter values
    required_parameters = Column(JSON)  # Array of required parameter names
    
    # Data requirements
    required_data_sources = Column(JSON)  # Array of required data sources
    minimum_data_period_days = Column(Integer, default=1)
    data_freshness_required_hours = Column(Integer, default=24)
    
    # Output configuration
    supported_formats = Column(JSON)  # Array of supported output formats
    default_format = Column(SQLEnum(OutputFormat), default=OutputFormat.pdf)
    
    # Access and permissions
    is_public = Column(Boolean, default=False)
    allowed_roles = Column(JSON)  # Array of roles that can use this template
    created_by = Column(CHAR(36), ForeignKey('users.id'), nullable=False)
    
    # Usage tracking
    usage_count = Column(Integer, default=0)
    last_used = Column(TIMESTAMP)
    average_generation_time_seconds = Column(Integer)
    
    # Template status
    is_active = Column(Boolean, default=True)
    version = Column(String(20), default='1.0')
    
    created_at = Column(TIMESTAMP, default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, default=func.current_timestamp(), onupdate=func.current_timestamp())
    
    # Relationships  
    created_by_user = relationship("User")
    
    # Indexes
    __table_args__ = (
        Index('idx_report_templates_type', 'template_type', 'is_active'),
        Index('idx_report_templates_creator', 'created_by'),
        Index('idx_report_templates_usage', 'usage_count'),
    )


class DashboardWidget(Base):
    __tablename__ = 'dashboard_widgets'
    
    id = Column(CHAR(36), primary_key=True, default=generate_uuid)
    user_id = Column(CHAR(36), ForeignKey('users.id'), nullable=False)
    widget_name = Column(String(255), nullable=False)
    widget_type = Column(String(100), nullable=False)  # 'chart', 'metric', 'table', 'map'
    
    # Widget configuration
    widget_config = Column(JSON, nullable=False)  # Widget-specific configuration
    data_source = Column(String(100), nullable=False)  # Data source for widget
    refresh_interval_minutes = Column(Integer, default=15)
    
    # Layout and positioning
    dashboard_tab = Column(String(100), default='main')
    position_x = Column(Integer, default=0)
    position_y = Column(Integer, default=0)
    width = Column(Integer, default=4)
    height = Column(Integer, default=3)
    z_index = Column(Integer, default=1)
    
    # Display settings
    title = Column(String(255))
    show_title = Column(Boolean, default=True)
    color_scheme = Column(String(50), default='default')
    
    # Data filtering
    site_filter = Column(JSON)  # Array of site IDs to include
    date_range_filter = Column(String(50))  # 'last_7_days', 'last_30_days', 'custom'
    custom_filters = Column(JSON)  # Additional filters
    
    # Widget status
    is_visible = Column(Boolean, default=True)
    is_shared = Column(Boolean, default=False)
    shared_with_users = Column(JSON)  # Array of user IDs
    
    # Performance tracking
    last_data_update = Column(TIMESTAMP)
    update_count = Column(Integer, default=0)
    error_count = Column(Integer, default=0)
    last_error_message = Column(Text)
    
    created_at = Column(TIMESTAMP, default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, default=func.current_timestamp(), onupdate=func.current_timestamp())
    
    # Relationships
    user = relationship("User")
    
    # Indexes
    __table_args__ = (
        Index('idx_dashboard_widgets_user', 'user_id', 'dashboard_tab'),
        Index('idx_dashboard_widgets_type', 'widget_type'),
        Index('idx_dashboard_widgets_position', 'position_x', 'position_y'),
    )


# ADMIN DASHBOARD & SYSTEM MANAGEMENT TABLES

# Admin enums
class AggregationLevel(enum.Enum):
    hourly = "hourly"
    daily = "daily"
    weekly = "weekly"
    monthly = "monthly"

class PerformanceTrend(enum.Enum):
    improving = "improving"
    stable = "stable"
    declining = "declining"
    volatile = "volatile"

class SafetyTrend(enum.Enum):
    improving = "improving"
    stable = "stable"
    declining = "declining"

class ComponentType(enum.Enum):
    cpu = "cpu"
    memory = "memory"
    disk = "disk"
    network = "network"
    database = "database"
    ai_service = "ai_service"
    web_service = "web_service"

class ServiceStatus(enum.Enum):
    healthy = "healthy"
    degraded = "degraded"
    unhealthy = "unhealthy"
    offline = "offline"

class ActivityType(enum.Enum):
    user_management = "user_management"
    site_configuration = "site_configuration"
    system_settings = "system_settings"
    alert_management = "alert_management"
    report_generation = "report_generation"
    data_export = "data_export"
    security_action = "security_action"
    maintenance = "maintenance"

class ImpactLevel(enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"

class ActionStatus(enum.Enum):
    pending = "pending"
    completed = "completed"
    failed = "failed"
    rolled_back = "rolled_back"

class ExecutiveReportType(enum.Enum):
    performance_summary = "performance_summary"
    safety_audit = "safety_audit"
    financial_overview = "financial_overview"
    resource_utilization = "resource_utilization"
    compliance_report = "compliance_report"
    executive_dashboard = "executive_dashboard"

class ReportStatus(enum.Enum):
    generating = "generating"
    completed = "completed"
    failed = "failed"
    archived = "archived"

class ConfidentialityLevel(enum.Enum):
    public = "public"
    internal = "internal"
    confidential = "confidential"
    restricted = "restricted"

class ExecutiveReportFormat(enum.Enum):
    pdf = "pdf"
    excel = "excel"
    powerpoint = "powerpoint"
    html = "html"
    json = "json"


class AdminDashboardMetric(Base):
    __tablename__ = 'admin_dashboard_metrics'
    
    id = Column(CHAR(36), primary_key=True, default=generate_uuid)
    metric_date = Column(Date, nullable=False)
    metric_hour = Column(Integer)  # 0-23 for hourly granularity
    aggregation_level = Column(SQLEnum(AggregationLevel), nullable=False)
    
    # System-wide metrics
    total_users = Column(Integer, default=0)
    active_users_24h = Column(Integer, default=0)
    total_sites = Column(Integer, default=0)
    active_sites = Column(Integer, default=0)
    total_cameras = Column(Integer, default=0)
    online_cameras = Column(Integer, default=0)
    
    # Performance metrics
    system_uptime_percentage = Column(Decimal(5,2), default=100.00)
    avg_response_time_ms = Column(Integer, default=0)
    total_api_calls = Column(BigInteger, default=0)
    data_processed_gb = Column(Decimal(10,2), default=0.00)
    
    # Alert metrics
    total_alerts_generated = Column(Integer, default=0)
    alerts_resolved = Column(Integer, default=0)
    alerts_pending = Column(Integer, default=0)
    avg_resolution_time_minutes = Column(Integer, default=0)
    
    # Safety and compliance
    overall_safety_score = Column(Decimal(5,2), default=100.00)
    ppe_compliance_rate = Column(Decimal(5,2), default=100.00)
    incident_count = Column(Integer, default=0)
    near_miss_count = Column(Integer, default=0)
    
    # AI and detection metrics
    ai_model_accuracy_avg = Column(Decimal(5,2), default=0.00)
    total_detections = Column(BigInteger, default=0)
    detection_accuracy_rate = Column(Decimal(5,2), default=0.00)
    false_positive_rate = Column(Decimal(5,2), default=0.00)
    
    # Resource utilization
    cpu_usage_avg = Column(Decimal(5,2), default=0.00)
    memory_usage_avg = Column(Decimal(5,2), default=0.00)
    disk_usage_avg = Column(Decimal(5,2), default=0.00)
    network_utilization_avg = Column(Decimal(5,2), default=0.00)
    database_performance_score = Column(Decimal(5,2), default=100.00)
    
    created_at = Column(TIMESTAMP, default=func.current_timestamp())
    calculated_at = Column(TIMESTAMP, default=func.current_timestamp())
    
    # Indexes
    __table_args__ = (
        Index('idx_admin_metrics_date', 'metric_date', 'aggregation_level'),
        Index('idx_admin_metrics_performance', 'system_uptime_percentage', 'avg_response_time_ms'),
        Index('idx_admin_metrics_safety', 'overall_safety_score', 'ppe_compliance_rate'),
        UniqueConstraint('metric_date', 'metric_hour', 'aggregation_level', name='unique_metric_period'),
    )


class SitePerformanceSummary(Base):
    __tablename__ = 'site_performance_summaries'
    
    id = Column(CHAR(36), primary_key=True, default=generate_uuid)
    site_id = Column(CHAR(36), ForeignKey('sites.id'), nullable=False)
    summary_date = Column(Date, nullable=False)
    summary_period = Column(SQLEnum(AggregationLevel), nullable=False)
    
    # Site operations
    personnel_count = Column(Integer, default=0)
    active_personnel = Column(Integer, default=0)
    camera_count = Column(Integer, default=0)
    online_cameras = Column(Integer, default=0)
    
    # Performance indicators
    site_uptime_percentage = Column(Decimal(5,2), default=100.00)
    ai_accuracy_percentage = Column(Decimal(5,2), default=0.00)
    safety_score = Column(Decimal(5,2), default=100.00)
    compliance_score = Column(Decimal(5,2), default=100.00)
    
    # Alert statistics
    alerts_generated = Column(Integer, default=0)
    alerts_resolved = Column(Integer, default=0)
    critical_alerts = Column(Integer, default=0)
    avg_alert_resolution_minutes = Column(Integer, default=0)
    
    # Activity metrics
    total_detections = Column(Integer, default=0)
    ppe_violations = Column(Integer, default=0)
    safety_incidents = Column(Integer, default=0)
    equipment_issues = Column(Integer, default=0)
    
    # Resource usage
    data_storage_usage_gb = Column(Decimal(10,2), default=0.00)
    bandwidth_usage_gb = Column(Decimal(10,2), default=0.00)
    processing_time_hours = Column(Decimal(8,2), default=0.00)
    
    # Quality metrics
    inspection_completion_rate = Column(Decimal(5,2), default=100.00)
    maintenance_completion_rate = Column(Decimal(5,2), default=100.00)
    documentation_completeness = Column(Decimal(5,2), default=100.00)
    
    # Trend indicators
    performance_trend = Column(SQLEnum(PerformanceTrend), default=PerformanceTrend.stable)
    safety_trend = Column(SQLEnum(SafetyTrend), default=SafetyTrend.stable)
    efficiency_score = Column(Decimal(5,2), default=100.00)
    
    # Metadata
    last_updated = Column(TIMESTAMP, default=func.current_timestamp())
    calculated_by = Column(String(100))
    notes = Column(Text)
    
    created_at = Column(TIMESTAMP, default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, default=func.current_timestamp(), onupdate=func.current_timestamp())
    
    # Relationships
    site = relationship("Site")
    
    # Indexes
    __table_args__ = (
        Index('idx_site_performance_site_date', 'site_id', 'summary_date'),
        Index('idx_site_performance_period', 'summary_period', 'summary_date'),
        Index('idx_site_performance_scores', 'safety_score', 'efficiency_score'),
        UniqueConstraint('site_id', 'summary_date', 'summary_period', name='unique_site_summary'),
    )


class SystemHealthLog(Base):
    __tablename__ = 'system_health_logs'
    
    id = Column(CHAR(36), primary_key=True, default=generate_uuid)
    server_id = Column(String(100), nullable=False)
    component_type = Column(SQLEnum(ComponentType), nullable=False)
    measurement_timestamp = Column(TIMESTAMP, default=func.current_timestamp())
    
    # Resource metrics
    cpu_usage_percentage = Column(Decimal(5,2))
    memory_usage_percentage = Column(Decimal(5,2))
    disk_usage_percentage = Column(Decimal(5,2))
    network_usage_percentage = Column(Decimal(5,2))
    
    # Performance metrics
    response_time_ms = Column(Integer)
    throughput_ops_per_second = Column(Integer)
    error_rate_percentage = Column(Decimal(5,2))
    uptime_percentage = Column(Decimal(5,2))
    
    # Database specific metrics
    db_connection_count = Column(Integer)
    db_query_time_avg_ms = Column(Integer)
    db_slow_queries_count = Column(Integer)
    db_deadlock_count = Column(Integer, default=0)
    
    # AI service metrics
    model_inference_time_ms = Column(Integer)
    model_accuracy_score = Column(Decimal(5,2))
    queue_size = Column(Integer)
    processing_backlog = Column(Integer)
    
    # Service health
    service_status = Column(SQLEnum(ServiceStatus), default=ServiceStatus.healthy)
    alert_threshold_exceeded = Column(Boolean, default=False)
    requires_attention = Column(Boolean, default=False)
    maintenance_required = Column(Boolean, default=False)
    
    # Error tracking
    error_count = Column(Integer, default=0)
    warning_count = Column(Integer, default=0)
    last_error_message = Column(Text)
    last_error_timestamp = Column(TIMESTAMP)
    
    # Metadata
    monitoring_source = Column(String(100))
    tags = Column(JSON)
    raw_metrics = Column(JSON)
    
    created_at = Column(TIMESTAMP, default=func.current_timestamp())
    
    # Indexes
    __table_args__ = (
        Index('idx_system_health_server_time', 'server_id', 'measurement_timestamp'),
        Index('idx_system_health_component', 'component_type', 'service_status'),
        Index('idx_system_health_status', 'service_status', 'requires_attention'),
        Index('idx_system_health_performance', 'response_time_ms', 'error_rate_percentage'),
    )


class AdminActivityLog(Base):
    __tablename__ = 'admin_activity_logs'
    
    id = Column(CHAR(36), primary_key=True, default=generate_uuid)
    admin_user_id = Column(CHAR(36), ForeignKey('users.id'), nullable=False)
    activity_type = Column(SQLEnum(ActivityType), nullable=False)
    action = Column(String(255), nullable=False)
    
    # Activity details
    resource_type = Column(String(100))
    resource_id = Column(CHAR(36))
    resource_name = Column(String(255))
    
    # Change tracking
    old_values = Column(JSON)
    new_values = Column(JSON)
    change_summary = Column(Text)
    
    # Context information
    site_id = Column(CHAR(36), ForeignKey('sites.id'))
    ip_address = Column(String(45), nullable=False)  # Support IPv6
    user_agent = Column(Text)
    session_id = Column(String(255))
    
    # Impact assessment
    impact_level = Column(SQLEnum(ImpactLevel), default=ImpactLevel.medium)
    affected_users_count = Column(Integer, default=0)
    affected_sites_count = Column(Integer, default=0)
    system_wide_impact = Column(Boolean, default=False)
    
    # Approval and review
    requires_approval = Column(Boolean, default=False)
    approved_by = Column(CHAR(36), ForeignKey('users.id'))
    approved_at = Column(TIMESTAMP)
    approval_notes = Column(Text)
    
    # Status and outcome
    action_status = Column(SQLEnum(ActionStatus), default=ActionStatus.completed)
    error_message = Column(Text)
    rollback_possible = Column(Boolean, default=True)
    
    # Compliance and audit
    compliance_category = Column(String(100))
    audit_trail_required = Column(Boolean, default=True)
    retention_period_days = Column(Integer, default=2555)  # 7 years default
    
    created_at = Column(TIMESTAMP, default=func.current_timestamp())
    
    # Relationships
    admin_user = relationship("User", foreign_keys=[admin_user_id])
    site = relationship("Site")
    approved_by_user = relationship("User", foreign_keys=[approved_by])
    
    # Indexes
    __table_args__ = (
        Index('idx_admin_activity_user_time', 'admin_user_id', 'created_at'),
        Index('idx_admin_activity_type', 'activity_type', 'action_status'),
        Index('idx_admin_activity_impact', 'impact_level', 'system_wide_impact'),
        Index('idx_admin_activity_resource', 'resource_type', 'resource_id'),
        Index('idx_admin_activity_approval', 'requires_approval', 'approved_by'),
    )


class ExecutiveReport(Base):
    __tablename__ = 'executive_reports'
    
    id = Column(CHAR(36), primary_key=True, default=generate_uuid)
    report_name = Column(String(255), nullable=False)
    report_type = Column(SQLEnum(ExecutiveReportType), nullable=False)
    reporting_period_start = Column(Date, nullable=False)
    reporting_period_end = Column(Date, nullable=False)
    
    # Report generation
    generated_by = Column(CHAR(36), ForeignKey('users.id'), nullable=False)
    generation_timestamp = Column(TIMESTAMP, default=func.current_timestamp())
    generation_duration_seconds = Column(Integer)
    report_status = Column(SQLEnum(ReportStatus), default=ReportStatus.generating)
    
    # Report content
    executive_summary = Column(Text)
    key_metrics = Column(JSON)
    trend_analysis = Column(JSON)
    recommendations = Column(JSON)
    risk_assessment = Column(JSON)
    
    # Data sources
    included_sites = Column(JSON)
    data_quality_score = Column(Decimal(5,2), default=100.00)
    data_completeness_percentage = Column(Decimal(5,2), default=100.00)
    data_sources = Column(JSON)
    
    # Distribution and access
    recipient_list = Column(JSON)
    confidentiality_level = Column(SQLEnum(ConfidentialityLevel), default=ConfidentialityLevel.internal)
    access_permissions = Column(JSON)
    
    # File information
    report_file_path = Column(String(500))
    report_file_format = Column(SQLEnum(ExecutiveReportFormat), default=ExecutiveReportFormat.pdf)
    report_file_size_mb = Column(Decimal(10,2))
    
    # Versioning and history
    version = Column(String(20), default='1.0')
    previous_report_id = Column(CHAR(36), ForeignKey('executive_reports.id'))
    is_latest_version = Column(Boolean, default=True)
    
    # Scheduling and automation
    is_automated = Column(Boolean, default=False)
    next_generation_date = Column(Date)
    automation_schedule = Column(String(100))
    
    # Performance metrics
    view_count = Column(Integer, default=0)
    download_count = Column(Integer, default=0)
    last_accessed = Column(TIMESTAMP)
    user_feedback_score = Column(Decimal(3,1))
    
    created_at = Column(TIMESTAMP, default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, default=func.current_timestamp(), onupdate=func.current_timestamp())
    archived_at = Column(TIMESTAMP)
    
    # Relationships
    generated_by_user = relationship("User")
    previous_report = relationship("ExecutiveReport", remote_side=[id])
    
    # Indexes
    __table_args__ = (
        Index('idx_executive_reports_type_period', 'report_type', 'reporting_period_end'),
        Index('idx_executive_reports_generator', 'generated_by', 'generation_timestamp'),
        Index('idx_executive_reports_status', 'report_status', 'is_latest_version'),
        Index('idx_executive_reports_automation', 'is_automated', 'next_generation_date'),
    )


# USER MANAGEMENT & ADMINISTRATION TABLES

# User management enums
class Gender(enum.Enum):
    male = "male"
    female = "female"
    other = "other"
    prefer_not_to_say = "prefer_not_to_say"

class PositionLevel(enum.Enum):
    entry = "entry"
    junior = "junior"
    mid = "mid"
    senior = "senior"
    lead = "lead"
    supervisor = "supervisor"
    manager = "manager"
    director = "director"
    executive = "executive"

class EmploymentType(enum.Enum):
    full_time = "full_time"
    part_time = "part_time"
    contract = "contract"
    temporary = "temporary"
    consultant = "consultant"
    intern = "intern"

class EmploymentStatus(enum.Enum):
    active = "active"
    on_leave = "on_leave"
    terminated = "terminated"
    retired = "retired"
    suspended = "suspended"

class RoleType(enum.Enum):
    system_role = "system_role"
    site_role = "site_role"
    department_role = "department_role"
    project_role = "project_role"
    temporary_role = "temporary_role"

class AccessLevel(enum.Enum):
    read = "read"
    write = "write"
    admin = "admin"
    super_admin = "super_admin"

class AssignmentStatus(enum.Enum):
    pending = "pending"
    active = "active"
    suspended = "suspended"
    expired = "expired"
    revoked = "revoked"

class AccessMethod(enum.Enum):
    web = "web"
    mobile_app = "mobile_app"
    api = "api"
    sso = "sso"
    ldap = "ldap"

class AuthenticationMethod(enum.Enum):
    password = "password"
    sso = "sso"
    mfa = "mfa"
    biometric = "biometric"
    certificate = "certificate"

class ActivityType(enum.Enum):
    login = "login"
    logout = "logout"
    page_view = "page_view"
    api_call = "api_call"
    data_access = "data_access"
    configuration_change = "configuration_change"
    user_management = "user_management"
    report_generation = "report_generation"
    alert_action = "alert_action"

class SecurityLevel(enum.Enum):
    public = "public"
    internal = "internal"
    confidential = "confidential"
    restricted = "restricted"

class PermissionAccessLevel(enum.Enum):
    none = "none"
    read = "read"
    write = "write"
    admin = "admin"
    owner = "owner"

class ScopeType(enum.Enum):
    global_scope = "global"
    site = "site"
    department = "department"
    project = "project"
    resource = "resource"

class PermissionStatus(enum.Enum):
    pending = "pending"
    active = "active"
    suspended = "suspended"
    expired = "expired"
    revoked = "revoked"


class UserManagementProfile(Base):
    __tablename__ = 'user_management_profiles'
    
    id = Column(CHAR(36), primary_key=True, default=generate_uuid)
    user_id = Column(CHAR(36), ForeignKey('users.id'), unique=True, nullable=False)
    
    # Extended profile information
    employee_number = Column(String(50), unique=True)
    badge_number = Column(String(50), unique=True)
    social_security_number = Column(String(20))  # Encrypted
    date_of_birth = Column(Date)
    gender = Column(SQLEnum(Gender))
    nationality = Column(String(100))
    
    # Address and contact
    home_address = Column(Text)
    home_city = Column(String(100))
    home_state = Column(String(100))
    home_zip_code = Column(String(20))
    home_country = Column(String(100))
    emergency_contact_name = Column(String(255))
    emergency_contact_phone = Column(String(20))
    emergency_contact_relationship = Column(String(100))
    
    # Professional details
    position_title = Column(String(255))
    position_level = Column(SQLEnum(PositionLevel))
    pay_grade = Column(String(50))
    reports_to_user_id = Column(CHAR(36), ForeignKey('users.id'))
    direct_reports_count = Column(Integer, default=0)
    
    # Employment information
    employment_type = Column(SQLEnum(EmploymentType))
    employment_status = Column(SQLEnum(EmploymentStatus))
    start_date = Column(Date, nullable=False)
    end_date = Column(Date)
    probation_end_date = Column(Date)
    performance_review_due = Column(Date)
    
    # Skills and qualifications
    skills = Column(JSON)
    qualifications = Column(JSON)
    languages = Column(JSON)
    special_certifications = Column(JSON)
    
    # Preferences and settings
    notification_preferences = Column(JSON)
    ui_theme = Column(String(50), default='default')
    timezone = Column(String(100))
    language_preference = Column(String(10), default='en')
    
    # Privacy and compliance
    privacy_settings = Column(JSON)
    gdpr_consent = Column(Boolean, default=False)
    marketing_consent = Column(Boolean, default=False)
    data_retention_consent = Column(Boolean, default=True)
    
    created_at = Column(TIMESTAMP, default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, default=func.current_timestamp(), onupdate=func.current_timestamp())
    
    # Relationships
    user = relationship("User", foreign_keys=[user_id])
    reports_to_user = relationship("User", foreign_keys=[reports_to_user_id])
    
    # Indexes
    __table_args__ = (
        Index('idx_user_profiles_employee', 'employee_number', 'badge_number'),
        Index('idx_user_profiles_position', 'position_level', 'employment_status'),
        Index('idx_user_profiles_dates', 'start_date', 'end_date'),
    )


class UserRoleAssignment(Base):
    __tablename__ = 'user_role_assignments'
    
    id = Column(CHAR(36), primary_key=True, default=generate_uuid)
    user_id = Column(CHAR(36), ForeignKey('users.id'), nullable=False)
    role_type = Column(SQLEnum(RoleType), nullable=False)
    role_name = Column(String(255), nullable=False)
    role_description = Column(Text)
    
    # Assignment scope
    site_id = Column(CHAR(36), ForeignKey('sites.id'))
    department_id = Column(CHAR(36))
    project_id = Column(CHAR(36))
    
    # Permission details
    permissions = Column(JSON)
    access_level = Column(SQLEnum(AccessLevel), default=AccessLevel.read)
    resource_restrictions = Column(JSON)
    time_restrictions = Column(JSON)
    
    # Assignment metadata
    assigned_by = Column(CHAR(36), ForeignKey('users.id'), nullable=False)
    assigned_at = Column(TIMESTAMP, default=func.current_timestamp())
    effective_from = Column(Date, nullable=False)
    effective_until = Column(Date)
    is_primary_role = Column(Boolean, default=False)
    
    # Approval workflow
    requires_approval = Column(Boolean, default=False)
    approved_by = Column(CHAR(36), ForeignKey('users.id'))
    approved_at = Column(TIMESTAMP)
    approval_notes = Column(Text)
    
    # Status and monitoring
    assignment_status = Column(SQLEnum(AssignmentStatus), default=AssignmentStatus.pending)
    last_used = Column(TIMESTAMP)
    usage_count = Column(Integer, default=0)
    
    # Audit trail
    revoked_by = Column(CHAR(36), ForeignKey('users.id'))
    revoked_at = Column(TIMESTAMP)
    revocation_reason = Column(Text)
    
    created_at = Column(TIMESTAMP, default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, default=func.current_timestamp(), onupdate=func.current_timestamp())
    
    # Relationships
    user = relationship("User", foreign_keys=[user_id])
    site = relationship("Site")
    assigned_by_user = relationship("User", foreign_keys=[assigned_by])
    approved_by_user = relationship("User", foreign_keys=[approved_by])
    revoked_by_user = relationship("User", foreign_keys=[revoked_by])
    
    # Indexes
    __table_args__ = (
        Index('idx_role_assignments_user', 'user_id', 'assignment_status'),
        Index('idx_role_assignments_role', 'role_type', 'role_name'),
        Index('idx_role_assignments_scope', 'site_id', 'department_id'),
        Index('idx_role_assignments_effective', 'effective_from', 'effective_until'),
    )


class UserSessionManagement(Base):
    __tablename__ = 'user_session_management'
    
    id = Column(CHAR(36), primary_key=True, default=generate_uuid)
    user_id = Column(CHAR(36), ForeignKey('users.id'), nullable=False)
    session_id = Column(String(255), unique=True, nullable=False)
    session_token = Column(String(512), unique=True, nullable=False)
    
    # Session details
    login_timestamp = Column(TIMESTAMP, default=func.current_timestamp())
    logout_timestamp = Column(TIMESTAMP)
    last_activity = Column(TIMESTAMP, default=func.current_timestamp())
    session_duration_seconds = Column(Integer)
    is_active = Column(Boolean, default=True)
    
    # Client information
    ip_address = Column(String(45), nullable=False)  # Support IPv6
    user_agent = Column(Text)
    browser_info = Column(JSON)
    device_info = Column(JSON)
    operating_system = Column(String(100))
    
    # Location and access
    login_location = Column(String(255))  # Simplified from POINT
    access_method = Column(SQLEnum(AccessMethod), default=AccessMethod.web)
    authentication_method = Column(SQLEnum(AuthenticationMethod), default=AuthenticationMethod.password)
    
    # Security context
    mfa_verified = Column(Boolean, default=False)
    risk_score = Column(Decimal(3,1))
    suspicious_activity = Column(Boolean, default=False)
    concurrent_sessions = Column(Integer, default=1)
    
    # Session management
    force_logout = Column(Boolean, default=False)
    session_timeout_minutes = Column(Integer, default=480)
    remember_me = Column(Boolean, default=False)
    auto_logout_at = Column(TIMESTAMP)
    
    # Activity tracking
    page_views = Column(Integer, default=0)
    api_calls = Column(Integer, default=0)
    downloads = Column(Integer, default=0)
    uploads = Column(Integer, default=0)
    
    # Compliance and audit
    compliance_acknowledgment = Column(Boolean, default=False)
    terms_accepted_version = Column(String(20))
    privacy_policy_accepted = Column(Boolean, default=False)
    
    created_at = Column(TIMESTAMP, default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, default=func.current_timestamp(), onupdate=func.current_timestamp())
    
    # Relationships
    user = relationship("User")
    
    # Indexes
    __table_args__ = (
        Index('idx_sessions_user_active', 'user_id', 'is_active', 'last_activity'),
        Index('idx_sessions_token', 'session_token', 'is_active'),
        Index('idx_sessions_security', 'risk_score', 'suspicious_activity'),
        Index('idx_sessions_cleanup', 'is_active', 'auto_logout_at'),
    )


class UserActivityTracking(Base):
    __tablename__ = 'user_activity_tracking'
    
    id = Column(CHAR(36), primary_key=True, default=generate_uuid)
    user_id = Column(CHAR(36), ForeignKey('users.id'), nullable=False)
    session_id = Column(CHAR(36), ForeignKey('user_session_management.id'), nullable=False)
    
    # Activity details
    activity_type = Column(SQLEnum(ActivityType), nullable=False)
    activity_description = Column(Text, nullable=False)
    activity_category = Column(String(100))
    
    # Context information
    resource_type = Column(String(100))
    resource_id = Column(CHAR(36))
    resource_name = Column(String(255))
    site_id = Column(CHAR(36), ForeignKey('sites.id'))
    
    # Request details
    request_method = Column(String(10))
    request_url = Column(Text)
    request_payload = Column(JSON)
    response_status = Column(Integer)
    response_time_ms = Column(Integer)
    
    # Geolocation and timing
    activity_timestamp = Column(TIMESTAMP, default=func.current_timestamp())
    location_coordinates = Column(String(255))  # Simplified from POINT
    location_accuracy = Column(Decimal(8,2))
    timezone_offset = Column(Integer)
    
    # Security and compliance
    security_level = Column(SQLEnum(SecurityLevel), default=SecurityLevel.internal)
    data_classification = Column(String(100))
    requires_audit = Column(Boolean, default=True)
    compliance_tags = Column(JSON)
    
    # Performance metrics
    processing_time_ms = Column(Integer)
    database_queries = Column(Integer, default=0)
    cache_hits = Column(Integer, default=0)
    errors_count = Column(Integer, default=0)
    
    # User behavior analysis
    is_automated = Column(Boolean, default=False)
    pattern_anomaly = Column(Boolean, default=False)
    risk_indicator = Column(Decimal(3,1))
    
    created_at = Column(TIMESTAMP, default=func.current_timestamp())
    
    # Relationships
    user = relationship("User")
    session = relationship("UserSessionManagement")
    site = relationship("Site")
    
    # Indexes
    __table_args__ = (
        Index('idx_activity_user_time', 'user_id', 'activity_timestamp'),
        Index('idx_activity_type', 'activity_type', 'activity_category'),
        Index('idx_activity_security', 'security_level', 'requires_audit'),
        Index('idx_activity_performance', 'response_time_ms', 'processing_time_ms'),
    )


class UserPermissionsMatrix(Base):
    __tablename__ = 'user_permissions_matrix'
    
    id = Column(CHAR(36), primary_key=True, default=generate_uuid)
    user_id = Column(CHAR(36), ForeignKey('users.id'), nullable=False)
    permission_category = Column(String(100), nullable=False)
    permission_name = Column(String(255), nullable=False)
    
    # Permission scope
    scope_type = Column(SQLEnum(ScopeType), nullable=False)
    scope_id = Column(CHAR(36))
    scope_name = Column(String(255))
    
    # Access details
    access_level = Column(SQLEnum(PermissionAccessLevel), nullable=False)
    can_delegate = Column(Boolean, default=False)
    can_revoke = Column(Boolean, default=False)
    
    # Conditions and restrictions
    conditions = Column(JSON)
    time_restrictions = Column(JSON)
    location_restrictions = Column(JSON)
    device_restrictions = Column(JSON)
    
    # Grant information
    granted_by = Column(CHAR(36), ForeignKey('users.id'), nullable=False)
    granted_at = Column(TIMESTAMP, default=func.current_timestamp())
    granted_reason = Column(Text)
    approval_required = Column(Boolean, default=False)
    approved_by = Column(CHAR(36), ForeignKey('users.id'))
    
    # Status and lifecycle
    status = Column(SQLEnum(PermissionStatus), default=PermissionStatus.pending)
    effective_from = Column(TIMESTAMP, default=func.current_timestamp())
    effective_until = Column(TIMESTAMP)
    auto_renewal = Column(Boolean, default=False)
    renewal_period_days = Column(Integer)
    
    # Usage tracking
    first_used = Column(TIMESTAMP)
    last_used = Column(TIMESTAMP)
    usage_count = Column(Integer, default=0)
    abuse_reports = Column(Integer, default=0)
    
    # Audit and compliance
    audit_required = Column(Boolean, default=True)
    compliance_notes = Column(Text)
    last_reviewed = Column(Date)
    next_review_due = Column(Date)
    reviewer_user_id = Column(CHAR(36), ForeignKey('users.id'))
    
    created_at = Column(TIMESTAMP, default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, default=func.current_timestamp(), onupdate=func.current_timestamp())
    
    # Relationships
    user = relationship("User", foreign_keys=[user_id])
    granted_by_user = relationship("User", foreign_keys=[granted_by])
    approved_by_user = relationship("User", foreign_keys=[approved_by])
    reviewer_user = relationship("User", foreign_keys=[reviewer_user_id])
    
    # Indexes
    __table_args__ = (
        Index('idx_permissions_user_category', 'user_id', 'permission_category'),
        Index('idx_permissions_scope', 'scope_type', 'scope_id'),
        Index('idx_permissions_status', 'status', 'effective_until'),
        Index('idx_permissions_review', 'next_review_due', 'audit_required'),
        UniqueConstraint('user_id', 'permission_category', 'permission_name', 'scope_type', 'scope_id', name='unique_user_permission_scope'),
    )


# ACCESS CONTROL & SECURITY MANAGEMENT TABLES

# Access control enums
class RoleLevel(enum.Enum):
    system = "system"
    site = "site"
    management = "management"
    operations = "operations"
    specialized = "specialized"
    worker = "worker"

class RiskLevel(enum.Enum):
    critical = "critical"
    high = "high"
    medium = "medium"
    low = "low"

class SiteAccessType(enum.Enum):
    all_sites = "all_sites"
    assigned_sites = "assigned_sites"
    multi_site = "multi_site"
    single_site = "single_site"
    none = "none"

class ResourceScope(enum.Enum):
    global_scope = "global"
    site = "site"
    zone = "zone"
    equipment = "equipment"
    personnel = "personnel"
    data = "data"

class OperationType(enum.Enum):
    create = "create"
    read = "read"
    update = "update"
    delete = "delete"
    execute = "execute"
    admin = "admin"
    full = "full"

class AssignmentType(enum.Enum):
    direct = "direct"
    inherited = "inherited"
    conditional = "conditional"
    temporary = "temporary"

class PolicyCategory(enum.Enum):
    authentication = "authentication"
    authorization = "authorization"
    session = "session"
    password = "password"
    mfa = "mfa"
    data_access = "data_access"
    network = "network"
    compliance = "compliance"

class PolicyType(enum.Enum):
    system = "system"
    site = "site"
    role = "role"
    user = "user"

class EnforcementLevel(enum.Enum):
    advisory = "advisory"
    warning = "warning"
    blocking = "blocking"
    strict = "strict"

class ViolationHandling(enum.Enum):
    log_only = "log_only"
    warn_user = "warn_user"
    block_action = "block_action"
    escalate = "escalate"

class EventType(enum.Enum):
    role_assignment = "role_assignment"
    permission_grant = "permission_grant"
    permission_revoke = "permission_revoke"
    policy_change = "policy_change"
    access_attempt = "access_attempt"
    violation = "violation"
    escalation = "escalation"

class EventCategory(enum.Enum):
    authentication = "authentication"
    authorization = "authorization"
    administration = "administration"
    compliance = "compliance"
    security = "security"

class ViolationSeverity(enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"


class AccessControlRole(Base):
    __tablename__ = 'access_control_roles'
    
    id = Column(CHAR(36), primary_key=True, default=generate_uuid)
    role_name = Column(String(255), nullable=False, unique=True)
    role_code = Column(String(100), nullable=False, unique=True)
    description = Column(Text, nullable=False)
    role_level = Column(SQLEnum(RoleLevel), nullable=False)
    risk_level = Column(SQLEnum(RiskLevel), nullable=False)
    color_code = Column(String(7), default='#6B7280')
    
    # Role hierarchy and inheritance
    parent_role_id = Column(CHAR(36), ForeignKey('access_control_roles.id'))
    inherits_permissions = Column(Boolean, default=True)
    inheritance_level = Column(Integer, default=0)
    role_path = Column(String(1000))
    
    # Site access configuration
    site_access_type = Column(SQLEnum(SiteAccessType), default=SiteAccessType.assigned_sites)
    default_site_assignments = Column(JSON)
    site_restrictions = Column(JSON)
    
    # Role metadata
    is_system_role = Column(Boolean, default=False)
    is_default_role = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    is_assignable = Column(Boolean, default=True)
    requires_approval = Column(Boolean, default=False)
    auto_expire_days = Column(Integer)
    
    # Usage tracking
    user_count = Column(Integer, default=0)
    assignment_count = Column(Integer, default=0)
    last_assigned = Column(TIMESTAMP)
    
    created_at = Column(TIMESTAMP, default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, default=func.current_timestamp(), onupdate=func.current_timestamp())
    created_by = Column(CHAR(36), ForeignKey('users.id'), nullable=False)
    updated_by = Column(CHAR(36), ForeignKey('users.id'))
    
    # Relationships
    parent_role = relationship("AccessControlRole", remote_side=[id])
    created_by_user = relationship("User", foreign_keys=[created_by])
    updated_by_user = relationship("User", foreign_keys=[updated_by])
    
    # Indexes
    __table_args__ = (
        Index('idx_roles_level_risk', 'role_level', 'risk_level'),
        Index('idx_roles_hierarchy', 'parent_role_id', 'inheritance_level'),
        Index('idx_roles_usage', 'user_count', 'assignment_count'),
    )


class SystemPermission(Base):
    __tablename__ = 'system_permissions'
    
    id = Column(CHAR(36), primary_key=True, default=generate_uuid)
    permission_name = Column(String(255), nullable=False, unique=True)
    permission_code = Column(String(100), nullable=False, unique=True)
    description = Column(Text, nullable=False)
    category = Column(String(100), nullable=False)
    subcategory = Column(String(100))
    risk_level = Column(SQLEnum(RiskLevel), nullable=False)
    
    # Permission scope and context
    resource_type = Column(String(100))
    resource_scope = Column(SQLEnum(ResourceScope), nullable=False)
    operation_type = Column(SQLEnum(OperationType), nullable=False)
    
    # Permission attributes
    is_system_permission = Column(Boolean, default=False)
    is_assignable = Column(Boolean, default=True)
    requires_mfa = Column(Boolean, default=False)
    requires_approval = Column(Boolean, default=False)
    is_delegatable = Column(Boolean, default=False)
    
    # Dependencies and relationships
    prerequisite_permissions = Column(JSON)
    conflicting_permissions = Column(JSON)
    implies_permissions = Column(JSON)
    
    # Usage tracking
    usage_count = Column(Integer, default=0)
    assignment_count = Column(Integer, default=0)
    last_used = Column(TIMESTAMP)
    
    created_at = Column(TIMESTAMP, default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, default=func.current_timestamp(), onupdate=func.current_timestamp())
    created_by = Column(CHAR(36), ForeignKey('users.id'), nullable=False)
    
    # Relationships
    created_by_user = relationship("User")
    
    # Indexes
    __table_args__ = (
        Index('idx_permissions_category', 'category', 'subcategory', 'risk_level'),
        Index('idx_permissions_scope', 'resource_scope', 'operation_type'),
        Index('idx_permissions_usage', 'usage_count', 'assignment_count'),
    )


class RolePermissionAssignment(Base):
    __tablename__ = 'role_permission_assignments'
    
    id = Column(CHAR(36), primary_key=True, default=generate_uuid)
    role_id = Column(CHAR(36), ForeignKey('access_control_roles.id'), nullable=False)
    permission_id = Column(CHAR(36), ForeignKey('system_permissions.id'), nullable=False)
    
    # Assignment configuration
    assignment_type = Column(SQLEnum(AssignmentType), default=AssignmentType.direct)
    granted_by = Column(CHAR(36), ForeignKey('users.id'), nullable=False)
    granted_at = Column(TIMESTAMP, default=func.current_timestamp())
    effective_from = Column(TIMESTAMP, default=func.current_timestamp())
    effective_until = Column(TIMESTAMP)
    is_active = Column(Boolean, default=True)
    
    # Conditional access
    conditions = Column(JSON)
    restrictions = Column(JSON)
    scope_limitations = Column(JSON)
    
    # Usage tracking
    usage_count = Column(Integer, default=0)
    last_used = Column(TIMESTAMP)
    
    created_at = Column(TIMESTAMP, default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, default=func.current_timestamp(), onupdate=func.current_timestamp())
    
    # Relationships
    role = relationship("AccessControlRole")
    permission = relationship("SystemPermission")
    granted_by_user = relationship("User")
    
    # Indexes
    __table_args__ = (
        Index('idx_role_permissions', 'role_id', 'permission_id', 'is_active'),
        Index('idx_permission_roles', 'permission_id', 'role_id'),
        UniqueConstraint('role_id', 'permission_id', 'assignment_type', name='unique_role_permission'),
    )


class SecurityPolicy(Base):
    __tablename__ = 'security_policies'
    
    id = Column(CHAR(36), primary_key=True, default=generate_uuid)
    policy_name = Column(String(255), nullable=False, unique=True)
    policy_code = Column(String(100), nullable=False, unique=True)
    description = Column(Text, nullable=False)
    category = Column(SQLEnum(PolicyCategory), nullable=False)
    policy_type = Column(SQLEnum(PolicyType), nullable=False)
    
    # Policy configuration
    policy_rules = Column(JSON, nullable=False)
    enforcement_level = Column(SQLEnum(EnforcementLevel), default=EnforcementLevel.blocking)
    is_mandatory = Column(Boolean, default=True)
    is_active = Column(Boolean, default=True)
    
    # Scope and application
    applies_to_roles = Column(JSON)
    applies_to_users = Column(JSON)
    applies_to_sites = Column(JSON)
    exclusions = Column(JSON)
    
    # Monitoring and enforcement
    violation_handling = Column(SQLEnum(ViolationHandling), default=ViolationHandling.block_action)
    violation_count = Column(Integer, default=0)
    last_violation = Column(TIMESTAMP)
    
    created_at = Column(TIMESTAMP, default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, default=func.current_timestamp(), onupdate=func.current_timestamp())
    created_by = Column(CHAR(36), ForeignKey('users.id'), nullable=False)
    
    # Relationships
    created_by_user = relationship("User")
    
    # Indexes
    __table_args__ = (
        Index('idx_policies_category', 'category', 'policy_type', 'is_active'),
        Index('idx_policies_enforcement', 'enforcement_level', 'violation_count'),
    )


class AccessControlAuditLog(Base):
    __tablename__ = 'access_control_audit_log'
    
    id = Column(CHAR(36), primary_key=True, default=generate_uuid)
    event_type = Column(SQLEnum(EventType), nullable=False)
    event_category = Column(SQLEnum(EventCategory), nullable=False)
    
    # Event participants
    user_id = Column(CHAR(36), ForeignKey('users.id'))
    target_user_id = Column(CHAR(36), ForeignKey('users.id'))
    role_id = Column(CHAR(36), ForeignKey('access_control_roles.id'))
    permission_id = Column(CHAR(36), ForeignKey('system_permissions.id'))
    policy_id = Column(CHAR(36), ForeignKey('security_policies.id'))
    
    # Event details
    action_performed = Column(String(255), nullable=False)
    resource_type = Column(String(100))
    resource_id = Column(CHAR(36))
    site_id = Column(CHAR(36), ForeignKey('sites.id'))
    
    # Access attempt details
    access_granted = Column(Boolean)
    denial_reason = Column(Text)
    risk_score = Column(Decimal(3,1))
    violation_type = Column(String(100))
    violation_severity = Column(SQLEnum(ViolationSeverity))
    
    # Session and client information
    session_id = Column(CHAR(36))
    ip_address = Column(String(45))
    user_agent = Column(Text)
    client_application = Column(String(100))
    
    # State tracking
    previous_state = Column(JSON)
    new_state = Column(JSON)
    change_summary = Column(Text)
    
    event_timestamp = Column(TIMESTAMP, default=func.current_timestamp())
    
    # Relationships
    user = relationship("User", foreign_keys=[user_id])
    target_user = relationship("User", foreign_keys=[target_user_id])
    role = relationship("AccessControlRole")
    permission = relationship("SystemPermission")
    policy = relationship("SecurityPolicy")
    site = relationship("Site")
    
    # Indexes
    __table_args__ = (
        Index('idx_audit_log_event', 'event_type', 'event_category', 'event_timestamp'),
        Index('idx_audit_log_user', 'user_id', 'event_timestamp'),
        Index('idx_audit_log_violations', 'violation_severity', 'access_granted', 'event_timestamp'),
    )


# AI MODEL MANAGEMENT & DEPLOYMENT TABLES

# AI model enums
class ModelType(enum.Enum):
    object_detection = "object_detection"
    object_tracking = "object_tracking"
    person_detection = "person_detection"
    behavior_analysis = "behavior_analysis"
    defect_detection = "defect_detection"
    classification = "classification"
    segmentation = "segmentation"
    custom = "custom"

class ModelStatus(enum.Enum):
    development = "development"
    training = "training"
    testing = "testing"
    validation = "validation"
    approved = "approved"
    deprecated = "deprecated"
    archived = "archived"

class LifecycleStage(enum.Enum):
    experimental = "experimental"
    beta = "beta"
    stable = "stable"
    mature = "mature"
    legacy = "legacy"

class ApprovalStatus(enum.Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"
    requires_review = "requires_review"

class DeploymentStatus(enum.Enum):
    pending = "pending"
    deploying = "deploying"
    active = "active"
    paused = "paused"
    failed = "failed"
    terminated = "terminated"

class DeploymentType(enum.Enum):
    production = "production"
    staging = "staging"
    testing = "testing"
    canary = "canary"
    blue_green = "blue_green"

class DeploymentStrategy(enum.Enum):
    immediate = "immediate"
    gradual = "gradual"
    scheduled = "scheduled"
    on_demand = "on_demand"

class PriorityLevel(enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"


class AIModel(Base):
    __tablename__ = 'ai_models'
    
    id = Column(CHAR(36), primary_key=True, default=generate_uuid)
    name = Column(String(255), nullable=False)
    model_type = Column(SQLEnum(ModelType), nullable=False)
    category = Column(String(255), nullable=False)
    
    # Version and metadata
    version = Column(String(50), nullable=False)
    description = Column(Text)
    framework = Column(String(100))
    architecture = Column(String(255))
    author = Column(String(255))
    organization = Column(String(255))
    
    # Model files and storage
    model_file_path = Column(String(500), nullable=False)
    model_file_size_mb = Column(Decimal(10,2))
    config_file_path = Column(String(500))
    weights_file_path = Column(String(500))
    labels_file_path = Column(String(500))
    documentation_url = Column(String(500))
    
    # Training information
    training_dataset_info = Column(JSON)
    training_images_count = Column(Integer)
    validation_images_count = Column(Integer)
    test_images_count = Column(Integer)
    training_duration_hours = Column(Decimal(8,2))
    training_completed_date = Column(TIMESTAMP)
    training_compute_cost = Column(Decimal(10,2))
    
    # Model specifications
    input_resolution_width = Column(Integer)
    input_resolution_height = Column(Integer)
    input_channels = Column(Integer, default=3)
    output_classes = Column(JSON)
    batch_size_optimal = Column(Integer)
    batch_size_max = Column(Integer)
    memory_requirement_gb = Column(Decimal(8,2))
    
    # Performance characteristics
    baseline_accuracy = Column(Decimal(5,2))
    baseline_precision = Column(Decimal(5,2))
    baseline_recall = Column(Decimal(5,2))
    baseline_f1_score = Column(Decimal(5,2))
    inference_time_ms = Column(Decimal(8,3))
    throughput_fps = Column(Decimal(8,2))
    confidence_threshold_default = Column(Decimal(3,2), default=0.50)
    
    # Deployment requirements
    min_gpu_memory_gb = Column(Decimal(6,2))
    recommended_gpu_models = Column(JSON)
    cpu_cores_required = Column(Integer)
    ram_requirement_gb = Column(Decimal(6,2))
    storage_requirement_gb = Column(Decimal(8,2))
    network_bandwidth_mbps = Column(Integer)
    
    # Status and lifecycle
    status = Column(SQLEnum(ModelStatus), default=ModelStatus.development)
    lifecycle_stage = Column(SQLEnum(LifecycleStage), default=LifecycleStage.experimental)
    approval_status = Column(SQLEnum(ApprovalStatus), default=ApprovalStatus.pending)
    approved_by = Column(CHAR(36), ForeignKey('users.id'))
    approved_at = Column(TIMESTAMP)
    
    # Licensing and compliance
    license_type = Column(String(100))
    license_restrictions = Column(Text)
    compliance_certifications = Column(JSON)
    regulatory_approvals = Column(JSON)
    export_restrictions = Column(Text)
    intellectual_property_notes = Column(Text)
    
    # Dependencies and compatibility
    dependency_requirements = Column(JSON)
    framework_version = Column(String(50))
    python_version_min = Column(String(20))
    cuda_version_required = Column(String(20))
    compatibility_notes = Column(Text)
    
    created_at = Column(TIMESTAMP, default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, default=func.current_timestamp(), onupdate=func.current_timestamp())
    created_by = Column(CHAR(36), ForeignKey('users.id'), nullable=False)
    last_modified_by = Column(CHAR(36), ForeignKey('users.id'), nullable=False)
    
    # Relationships
    approved_by_user = relationship("User", foreign_keys=[approved_by])
    created_by_user = relationship("User", foreign_keys=[created_by])
    last_modified_by_user = relationship("User", foreign_keys=[last_modified_by])
    
    # Indexes
    __table_args__ = (
        Index('idx_ai_models_type', 'model_type', 'category'),
        Index('idx_ai_models_status', 'status', 'lifecycle_stage'),
        Index('idx_ai_models_performance', 'baseline_accuracy', 'inference_time_ms'),
        Index('idx_ai_models_approval', 'approval_status', 'approved_at'),
    )


class ModelDeployment(Base):
    __tablename__ = 'model_deployments'
    
    id = Column(CHAR(36), primary_key=True, default=generate_uuid)
    model_id = Column(CHAR(36), ForeignKey('ai_models.id'), nullable=False)
    site_id = Column(CHAR(36), ForeignKey('sites.id'), nullable=False)
    deployment_name = Column(String(255), nullable=False)
    
    # Deployment configuration
    deployment_status = Column(SQLEnum(DeploymentStatus), default=DeploymentStatus.pending)
    deployment_type = Column(SQLEnum(DeploymentType), default=DeploymentType.production)
    deployment_strategy = Column(SQLEnum(DeploymentStrategy), default=DeploymentStrategy.immediate)
    
    # Configuration parameters
    confidence_threshold = Column(Decimal(3,2), nullable=False)
    batch_size = Column(Integer, nullable=False)
    processing_interval_seconds = Column(Integer, default=1)
    max_concurrent_requests = Column(Integer, default=10)
    timeout_seconds = Column(Integer, default=30)
    
    # Resource allocation
    allocated_gpu_memory_gb = Column(Decimal(6,2))
    allocated_cpu_cores = Column(Integer)
    allocated_ram_gb = Column(Decimal(6,2))
    priority_level = Column(SQLEnum(PriorityLevel), default=PriorityLevel.medium)
    resource_limits = Column(JSON)
    
    # Deployment timing
    scheduled_start_time = Column(TIMESTAMP)
    scheduled_end_time = Column(TIMESTAMP)
    deployed_at = Column(TIMESTAMP)
    last_health_check = Column(TIMESTAMP)
    next_maintenance_window = Column(TIMESTAMP)
    
    # Performance settings
    auto_scaling_enabled = Column(Boolean, default=False)
    min_instances = Column(Integer, default=1)
    max_instances = Column(Integer, default=3)
    scale_up_threshold = Column(Decimal(5,2), default=80.00)
    scale_down_threshold = Column(Decimal(5,2), default=30.00)
    
    # Monitoring and alerting
    monitoring_enabled = Column(Boolean, default=True)
    alert_on_errors = Column(Boolean, default=True)
    alert_on_performance_degradation = Column(Boolean, default=True)
    performance_alert_threshold = Column(Decimal(5,2), default=10.00)
    error_rate_alert_threshold = Column(Decimal(5,2), default=5.00)
    
    # Integration settings
    input_sources = Column(JSON)
    output_destinations = Column(JSON)
    preprocessing_pipeline = Column(JSON)
    postprocessing_pipeline = Column(JSON)
    
    # Rollback and versioning
    rollback_model_id = Column(CHAR(36), ForeignKey('ai_models.id'))
    rollback_enabled = Column(Boolean, default=True)
    previous_deployment_id = Column(CHAR(36), ForeignKey('model_deployments.id'))
    deployment_notes = Column(Text)
    rollback_trigger_conditions = Column(JSON)
    
    # Access control
    authorized_users = Column(JSON)
    api_access_enabled = Column(Boolean, default=False)
    api_key = Column(String(255))
    rate_limit_requests_per_minute = Column(Integer, default=100)
    
    created_at = Column(TIMESTAMP, default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, default=func.current_timestamp(), onupdate=func.current_timestamp())
    deployed_by = Column(CHAR(36), ForeignKey('users.id'), nullable=False)
    
    # Relationships
    model = relationship("AIModel", foreign_keys=[model_id])
    site = relationship("Site")
    rollback_model = relationship("AIModel", foreign_keys=[rollback_model_id])
    previous_deployment = relationship("ModelDeployment", remote_side=[id])
    deployed_by_user = relationship("User")
    
    # Indexes
    __table_args__ = (
        Index('idx_deployments_model_site', 'model_id', 'site_id', 'deployment_status'),
        Index('idx_deployments_status', 'deployment_status', 'deployed_at'),
        Index('idx_deployments_type', 'deployment_type', 'deployment_strategy'),
        Index('idx_deployments_performance', 'performance_alert_threshold', 'error_rate_alert_threshold'),
    )


class ModelPerformanceMetric(Base):
    __tablename__ = 'model_performance_metrics'
    
    id = Column(CHAR(36), primary_key=True, default=generate_uuid)
    deployment_id = Column(CHAR(36), ForeignKey('model_deployments.id'), nullable=False)
    metric_timestamp = Column(TIMESTAMP, default=func.current_timestamp())
    collection_period_minutes = Column(Integer, default=5)
    
    # Performance metrics
    accuracy_percentage = Column(Decimal(5,2))
    precision_percentage = Column(Decimal(5,2))
    recall_percentage = Column(Decimal(5,2))
    f1_score = Column(Decimal(5,2))
    confidence_score_avg = Column(Decimal(3,2))
    inference_time_avg_ms = Column(Decimal(8,3))
    inference_time_p95_ms = Column(Decimal(8,3))
    throughput_fps = Column(Decimal(8,2))
    
    # Detection statistics
    total_detections = Column(Integer, default=0)
    true_positives = Column(Integer, default=0)
    false_positives = Column(Integer, default=0)
    true_negatives = Column(Integer, default=0)
    false_negatives = Column(Integer, default=0)
    detection_rate_per_hour = Column(Decimal(8,2))
    
    # Resource utilization
    cpu_utilization_avg = Column(Decimal(5,2))
    cpu_utilization_max = Column(Decimal(5,2))
    gpu_utilization_avg = Column(Decimal(5,2))
    gpu_utilization_max = Column(Decimal(5,2))
    memory_usage_avg_gb = Column(Decimal(8,2))
    memory_usage_max_gb = Column(Decimal(8,2))
    gpu_memory_usage_avg_gb = Column(Decimal(6,2))
    gpu_memory_usage_max_gb = Column(Decimal(6,2))
    
    # Error tracking
    total_errors = Column(Integer, default=0)
    preprocessing_errors = Column(Integer, default=0)
    inference_errors = Column(Integer, default=0)
    postprocessing_errors = Column(Integer, default=0)
    error_rate_percentage = Column(Decimal(5,2))
    
    # Quality and business metrics
    data_quality_score = Column(Decimal(5,2))
    prediction_consistency_score = Column(Decimal(5,2))
    drift_detection_score = Column(Decimal(5,2))
    cost_per_inference = Column(Decimal(10,6))
    roi_impact_score = Column(Decimal(8,2))
    
    created_at = Column(TIMESTAMP, default=func.current_timestamp())
    calculated_at = Column(TIMESTAMP, default=func.current_timestamp())
    
    # Relationships
    deployment = relationship("ModelDeployment")
    
    # Indexes
    __table_args__ = (
        Index('idx_performance_deployment_time', 'deployment_id', 'metric_timestamp'),
        Index('idx_performance_metrics', 'accuracy_percentage', 'f1_score'),
        Index('idx_performance_resource', 'cpu_utilization_avg', 'gpu_utilization_avg'),
        Index('idx_performance_errors', 'error_rate_percentage', 'total_errors'),
    )


# Training and evaluation enums
class TrainingType(enum.Enum):
    initial_training = "initial_training"
    fine_tuning = "fine_tuning"
    transfer_learning = "transfer_learning"
    incremental_learning = "incremental_learning"
    reinforcement_learning = "reinforcement_learning"

class JobStatus(enum.Enum):
    queued = "queued"
    initializing = "initializing"
    running = "running"
    paused = "paused"
    completed = "completed"
    failed = "failed"
    cancelled = "cancelled"

class EvaluationType(enum.Enum):
    validation = "validation"
    test = "test"
    benchmark = "benchmark"
    production_sample = "production_sample"
    a_b_test = "a_b_test"
    stress_test = "stress_test"

class ReviewStatus(enum.Enum):
    pending = "pending"
    approved = "approved"
    requires_revision = "requires_revision"
    rejected = "rejected"


class ModelTrainingJob(Base):
    __tablename__ = 'model_training_jobs'
    
    id = Column(CHAR(36), primary_key=True, default=generate_uuid)
    model_id = Column(CHAR(36), ForeignKey('ai_models.id'), nullable=False)
    job_name = Column(String(255), nullable=False)
    job_description = Column(Text)
    
    # Job configuration
    training_type = Column(SQLEnum(TrainingType), nullable=False)
    base_model_id = Column(CHAR(36), ForeignKey('ai_models.id'))
    dataset_id = Column(CHAR(36))
    hyperparameters = Column(JSON)
    
    # Resource allocation
    compute_instance_type = Column(String(100))
    gpu_count = Column(Integer, default=1)
    gpu_type = Column(String(100))
    cpu_cores = Column(Integer, default=8)
    memory_gb = Column(Integer, default=32)
    storage_gb = Column(Integer, default=100)
    
    # Training parameters
    epochs = Column(Integer, default=100)
    batch_size = Column(Integer, default=32)
    learning_rate = Column(Decimal(10,8), default=0.001)
    optimizer = Column(String(50), default='Adam')
    loss_function = Column(String(100))
    validation_split = Column(Decimal(3,2), default=0.20)
    early_stopping_patience = Column(Integer, default=10)
    
    # Status tracking
    job_status = Column(SQLEnum(JobStatus), default=JobStatus.queued)
    progress_percentage = Column(Decimal(5,2), default=0.00)
    current_epoch = Column(Integer, default=0)
    estimated_completion_time = Column(TIMESTAMP)
    actual_completion_time = Column(TIMESTAMP)
    
    # Performance tracking
    current_loss = Column(Decimal(12,8))
    current_accuracy = Column(Decimal(5,2))
    best_loss = Column(Decimal(12,8))
    best_accuracy = Column(Decimal(5,2))
    best_epoch = Column(Integer)
    validation_loss = Column(Decimal(12,8))
    validation_accuracy = Column(Decimal(5,2))
    
    # Cost tracking
    compute_cost_per_hour = Column(Decimal(8,4))
    estimated_total_cost = Column(Decimal(10,2))
    actual_cost = Column(Decimal(10,2))
    cost_budget_limit = Column(Decimal(10,2))
    
    # Results and artifacts
    output_model_path = Column(String(500))
    checkpoint_paths = Column(JSON)
    log_file_path = Column(String(500))
    metrics_file_path = Column(String(500))
    
    # Error handling
    error_message = Column(Text)
    retry_count = Column(Integer, default=0)
    max_retries = Column(Integer, default=3)
    auto_restart_on_failure = Column(Boolean, default=True)
    
    # Notifications and experiment tracking
    notification_recipients = Column(JSON)
    notification_on_completion = Column(Boolean, default=True)
    notification_on_failure = Column(Boolean, default=True)
    experiment_name = Column(String(255))
    experiment_tags = Column(JSON)
    parent_experiment_id = Column(CHAR(36), ForeignKey('model_training_jobs.id'))
    reproducibility_seed = Column(Integer)
    
    created_at = Column(TIMESTAMP, default=func.current_timestamp())
    started_at = Column(TIMESTAMP)
    completed_at = Column(TIMESTAMP)
    created_by = Column(CHAR(36), ForeignKey('users.id'), nullable=False)
    
    # Relationships
    model = relationship("AIModel", foreign_keys=[model_id])
    base_model = relationship("AIModel", foreign_keys=[base_model_id])
    parent_experiment = relationship("ModelTrainingJob", remote_side=[id])
    created_by_user = relationship("User")
    
    # Indexes
    __table_args__ = (
        Index('idx_training_jobs_model', 'model_id', 'job_status'),
        Index('idx_training_jobs_status', 'job_status', 'created_at'),
        Index('idx_training_jobs_performance', 'best_accuracy', 'current_accuracy'),
        Index('idx_training_jobs_cost', 'actual_cost', 'cost_budget_limit'),
    )


class ModelEvaluationResult(Base):
    __tablename__ = 'model_evaluation_results'
    
    id = Column(CHAR(36), primary_key=True, default=generate_uuid)
    model_id = Column(CHAR(36), ForeignKey('ai_models.id'), nullable=False)
    evaluation_name = Column(String(255), nullable=False)
    evaluation_type = Column(SQLEnum(EvaluationType), nullable=False)
    
    # Evaluation dataset information
    dataset_id = Column(CHAR(36))
    dataset_size = Column(Integer)
    dataset_description = Column(Text)
    evaluation_date = Column(TIMESTAMP, default=func.current_timestamp())
    evaluation_duration_minutes = Column(Integer)
    
    # Overall performance metrics
    overall_accuracy = Column(Decimal(5,2))
    overall_precision = Column(Decimal(5,2))
    overall_recall = Column(Decimal(5,2))
    overall_f1_score = Column(Decimal(5,2))
    micro_f1_score = Column(Decimal(5,2))
    macro_f1_score = Column(Decimal(5,2))
    weighted_f1_score = Column(Decimal(5,2))
    
    # Per-class and detailed metrics
    class_wise_metrics = Column(JSON)
    confusion_matrix = Column(JSON)
    classification_report = Column(JSON)
    
    # Detection-specific metrics
    mean_average_precision_50 = Column(Decimal(5,2))
    mean_average_precision_75 = Column(Decimal(5,2))
    mean_average_precision_50_95 = Column(Decimal(5,2))
    average_recall_100 = Column(Decimal(5,2))
    
    # Performance distribution
    confidence_score_distribution = Column(JSON)
    inference_time_distribution = Column(JSON)
    accuracy_by_confidence_threshold = Column(JSON)
    roc_curve_data = Column(JSON)
    precision_recall_curve_data = Column(JSON)
    
    # Resource performance
    evaluation_cpu_time_seconds = Column(Decimal(10,3))
    evaluation_gpu_time_seconds = Column(Decimal(10,3))
    peak_memory_usage_gb = Column(Decimal(8,2))
    average_inference_time_ms = Column(Decimal(8,3))
    throughput_images_per_second = Column(Decimal(8,2))
    
    # Robustness and bias metrics
    adversarial_accuracy = Column(Decimal(5,2))
    noise_robustness_score = Column(Decimal(5,2))
    lighting_robustness_score = Column(Decimal(5,2))
    demographic_parity_score = Column(Decimal(5,2))
    calibration_score = Column(Decimal(5,2))
    bias_detection_results = Column(JSON)
    fairness_constraints_met = Column(Boolean, default=False)
    
    # Business impact assessment
    cost_per_evaluation = Column(Decimal(8,4))
    business_accuracy_score = Column(Decimal(5,2))
    false_positive_cost_impact = Column(Decimal(10,2))
    false_negative_cost_impact = Column(Decimal(10,2))
    roi_projection = Column(Decimal(10,2))
    
    # Comparison and quality metrics
    baseline_model_comparison = Column(JSON)
    previous_version_comparison = Column(JSON)
    human_performance_comparison = Column(Decimal(6,2))
    model_quality_score = Column(Decimal(5,2))
    deployment_readiness_score = Column(Decimal(5,2))
    risk_assessment_score = Column(Decimal(5,2))
    
    # Files and artifacts
    evaluation_report_path = Column(String(500))
    detailed_results_path = Column(String(500))
    visualization_files = Column(JSON)
    raw_predictions_path = Column(String(500))
    
    # Review and approval
    reviewed_by = Column(CHAR(36), ForeignKey('users.id'))
    review_status = Column(SQLEnum(ReviewStatus), default=ReviewStatus.pending)
    review_date = Column(TIMESTAMP)
    review_comments = Column(Text)
    approval_for_production = Column(Boolean, default=False)
    
    created_at = Column(TIMESTAMP, default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, default=func.current_timestamp(), onupdate=func.current_timestamp())
    evaluated_by = Column(CHAR(36), ForeignKey('users.id'), nullable=False)
    
    # Relationships
    model = relationship("AIModel")
    reviewed_by_user = relationship("User", foreign_keys=[reviewed_by])
    evaluated_by_user = relationship("User", foreign_keys=[evaluated_by])
    
    # Indexes
    __table_args__ = (
        Index('idx_evaluation_model_type', 'model_id', 'evaluation_type', 'evaluation_date'),
        Index('idx_evaluation_performance', 'overall_accuracy', 'overall_f1_score'),
        Index('idx_evaluation_review', 'review_status', 'approval_for_production'),
        Index('idx_evaluation_business', 'business_accuracy_score', 'roi_projection'),
    )


# SITE CONFIGURATION & INFRASTRUCTURE TABLES

# Site configuration enums
class SafetyLevel(enum.Enum):
    standard = "standard"
    high = "high"
    critical = "critical"

class AISensitivityLevel(enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"

class RecordingQuality(enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"
    ultra = "ultra"

class AccessControlType(enum.Enum):
    manual = "manual"
    keycard = "keycard"
    biometric = "biometric"
    mobile = "mobile"

class AuditFrequency(enum.Enum):
    weekly = "weekly"
    monthly = "monthly"
    quarterly = "quarterly"
    annually = "annually"

class NetworkStatus(enum.Enum):
    excellent = "excellent"
    good = "good"
    fair = "fair"
    poor = "poor"
    offline = "offline"

class PowerStatus(enum.Enum):
    stable = "stable"
    unstable = "unstable"
    backup_active = "backup_active"
    critical = "critical"
    offline = "offline"

class CellularCoverage(enum.Enum):
    excellent = "excellent"
    good = "good"
    fair = "fair"
    poor = "poor"
    none = "none"

class MonitoringLevel(enum.Enum):
    basic = "basic"
    standard = "standard"
    enhanced = "enhanced"
    maximum = "maximum"

class ZoneStatus(enum.Enum):
    active = "active"
    maintenance = "maintenance"
    restricted = "restricted"
    inactive = "inactive"

class DetectionSensitivity(enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"

class TrackingPeriod(enum.Enum):
    hourly = "hourly"
    daily = "daily"
    weekly = "weekly"
    monthly = "monthly"

class PerformanceTrend(enum.Enum):
    improving = "improving"
    stable = "stable"
    declining = "declining"
    volatile = "volatile"

class HealthTrend(enum.Enum):
    improving = "improving"
    stable = "stable"
    declining = "declining"

class EfficiencyTrend(enum.Enum):
    improving = "improving"
    stable = "stable"
    declining = "declining"

class ComplianceStatus(enum.Enum):
    compliant = "compliant"
    minor_issues = "minor_issues"
    major_issues = "major_issues"
    non_compliant = "non_compliant"

class AuditType(enum.Enum):
    internal = "internal"
    external = "external"
    regulatory = "regulatory"
    third_party = "third_party"

class ComplianceTrend(enum.Enum):
    improving = "improving"
    stable = "stable"
    declining = "declining"


class SiteConfiguration(Base):
    __tablename__ = 'site_configurations'
    
    id = Column(CHAR(36), primary_key=True, default=generate_uuid)
    site_id = Column(CHAR(36), ForeignKey('sites.id'), unique=True, nullable=False)
    
    # Basic configuration
    timezone = Column(String(100), default='America/New_York')
    working_hours_start = Column(Time, default='06:00')
    working_hours_end = Column(Time, default='18:00')
    max_occupancy = Column(Integer, default=100)
    safety_level = Column(SQLEnum(SafetyLevel), default=SafetyLevel.standard)
    
    # AI and detection settings
    ai_detection_enabled = Column(Boolean, default=True)
    ai_sensitivity_level = Column(SQLEnum(AISensitivityLevel), default=AISensitivityLevel.medium)
    detection_zones = Column(JSON)
    detection_models = Column(JSON)
    real_time_analysis = Column(Boolean, default=True)
    
    # Recording and storage
    recording_retention_days = Column(Integer, default=30)
    recording_quality = Column(SQLEnum(RecordingQuality), default=RecordingQuality.high)
    recording_schedule = Column(JSON)
    storage_location = Column(String(255))
    backup_retention_days = Column(Integer, default=90)
    
    # Alert and notification settings
    alert_notifications_enabled = Column(Boolean, default=True)
    notification_methods = Column(JSON)
    alert_escalation_rules = Column(JSON)
    notification_recipients = Column(JSON)
    
    # Emergency contacts and procedures
    emergency_contacts = Column(JSON)
    emergency_procedures = Column(JSON)
    evacuation_plan_url = Column(String(500))
    safety_protocols = Column(JSON)
    
    # Access control settings
    access_control_type = Column(SQLEnum(AccessControlType), default=AccessControlType.keycard)
    visitor_management = Column(Boolean, default=True)
    contractor_access_rules = Column(JSON)
    multi_factor_auth_required = Column(Boolean, default=False)
    
    # Integration settings
    weather_monitoring = Column(Boolean, default=False)
    environmental_sensors = Column(JSON)
    third_party_integrations = Column(JSON)
    api_access_tokens = Column(JSON)
    
    # Performance and maintenance
    system_health_threshold = Column(Integer, default=85)
    maintenance_schedule = Column(JSON)
    performance_monitoring = Column(Boolean, default=True)
    automated_diagnostics = Column(Boolean, default=True)
    
    # Compliance and regulations
    compliance_frameworks = Column(JSON)
    audit_frequency = Column(SQLEnum(AuditFrequency), default=AuditFrequency.monthly)
    documentation_requirements = Column(JSON)
    regulatory_contacts = Column(JSON)
    
    # Custom configurations
    custom_fields = Column(JSON)
    feature_flags = Column(JSON)
    integration_endpoints = Column(JSON)
    
    created_at = Column(TIMESTAMP, default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, default=func.current_timestamp(), onupdate=func.current_timestamp())
    configured_by = Column(CHAR(36), ForeignKey('users.id'), nullable=False)
    last_modified_by = Column(CHAR(36), ForeignKey('users.id'), nullable=False)
    
    # Relationships
    site = relationship("Site")
    configured_by_user = relationship("User", foreign_keys=[configured_by])
    last_modified_by_user = relationship("User", foreign_keys=[last_modified_by])
    
    # Indexes
    __table_args__ = (
        Index('idx_site_configs_safety', 'safety_level', 'ai_detection_enabled'),
        Index('idx_site_configs_audit', 'audit_frequency'),
        Index('idx_site_configs_performance', 'system_health_threshold', 'performance_monitoring'),
    )


class SiteInfrastructure(Base):
    __tablename__ = 'site_infrastructure'
    
    id = Column(CHAR(36), primary_key=True, default=generate_uuid)
    site_id = Column(CHAR(36), ForeignKey('sites.id'), unique=True, nullable=False)
    
    # Network infrastructure
    network_status = Column(SQLEnum(NetworkStatus), default=NetworkStatus.fair)
    internet_speed_mbps = Column(Integer)
    network_provider = Column(String(255))
    ip_range = Column(String(50))
    wifi_networks = Column(JSON)
    network_monitoring = Column(Boolean, default=True)
    
    # Power infrastructure
    power_status = Column(SQLEnum(PowerStatus), default=PowerStatus.stable)
    main_power_source = Column(String(255))
    backup_power_available = Column(Boolean, default=False)
    backup_power_capacity_hours = Column(Integer)
    ups_systems = Column(JSON)
    power_consumption_kw = Column(Decimal(8,2))
    
    # Environmental systems
    weather_station_installed = Column(Boolean, default=False)
    environmental_sensors = Column(JSON)
    hvac_systems = Column(JSON)
    lighting_systems = Column(JSON)
    security_systems = Column(JSON)
    
    # Communication systems
    radio_communication = Column(Boolean, default=False)
    intercom_systems = Column(JSON)
    emergency_communication = Column(JSON)
    cellular_coverage = Column(SQLEnum(CellularCoverage), default=CellularCoverage.good)
    
    # Storage and computing
    local_servers = Column(JSON)
    storage_capacity_tb = Column(Decimal(8,2))
    cloud_storage_enabled = Column(Boolean, default=True)
    computing_resources = Column(JSON)
    data_backup_systems = Column(JSON)
    
    # Maintenance tracking
    last_infrastructure_audit = Column(Date)
    next_infrastructure_audit = Column(Date)
    maintenance_contracts = Column(JSON)
    equipment_warranties = Column(JSON)
    upgrade_schedule = Column(JSON)
    
    # Performance metrics
    uptime_percentage = Column(Decimal(5,2), default=100.00)
    average_response_time_ms = Column(Integer)
    network_utilization_percentage = Column(Decimal(5,2))
    storage_utilization_percentage = Column(Decimal(5,2))
    system_temperature_celsius = Column(Decimal(4,1))
    
    # Compliance and certifications
    infrastructure_certifications = Column(JSON)
    inspection_records = Column(JSON)
    regulatory_compliance = Column(JSON)
    insurance_information = Column(JSON)
    
    # Integration points
    camera_network_config = Column(JSON)
    sensor_network_config = Column(JSON)
    third_party_connections = Column(JSON)
    api_endpoints = Column(JSON)
    
    created_at = Column(TIMESTAMP, default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, default=func.current_timestamp(), onupdate=func.current_timestamp())
    last_audit_by = Column(CHAR(36), ForeignKey('users.id'))
    
    # Relationships
    site = relationship("Site")
    last_audit_by_user = relationship("User")
    
    # Indexes
    __table_args__ = (
        Index('idx_site_infrastructure_status', 'network_status', 'power_status'),
        Index('idx_site_infrastructure_performance', 'uptime_percentage', 'average_response_time_ms'),
        Index('idx_site_infrastructure_audit', 'next_infrastructure_audit', 'last_audit_by'),
    )


class SiteZoneConfiguration(Base):
    __tablename__ = 'site_zone_configurations'
    
    id = Column(CHAR(36), primary_key=True, default=generate_uuid)
    site_id = Column(CHAR(36), ForeignKey('sites.id'), nullable=False)
    zone_id = Column(CHAR(36), ForeignKey('zones.id'), nullable=False)
    
    # Zone-specific settings
    zone_configuration = Column(JSON)
    access_restrictions = Column(JSON)
    safety_requirements = Column(JSON)
    monitoring_level = Column(SQLEnum(MonitoringLevel), default=MonitoringLevel.standard)
    
    # Camera assignments
    assigned_cameras = Column(JSON)
    camera_coverage_percentage = Column(Decimal(5,2), default=0.00)
    blind_spots = Column(JSON)
    camera_positioning_optimal = Column(Boolean, default=False)
    
    # Personnel settings
    max_personnel = Column(Integer)
    authorized_roles = Column(JSON)
    restricted_hours = Column(JSON)
    ppe_requirements = Column(JSON)
    
    # Environmental settings
    environmental_hazards = Column(JSON)
    weather_restrictions = Column(JSON)
    emergency_procedures = Column(JSON)
    evacuation_routes = Column(JSON)
    
    # AI and detection settings
    ai_detection_rules = Column(JSON)
    alert_thresholds = Column(JSON)
    detection_sensitivity = Column(SQLEnum(DetectionSensitivity), default=DetectionSensitivity.medium)
    notification_overrides = Column(JSON)
    
    # Performance tracking
    zone_utilization_percentage = Column(Decimal(5,2), default=0.00)
    incident_frequency = Column(Decimal(8,2), default=0.00)
    safety_score = Column(Decimal(5,2), default=100.00)
    compliance_score = Column(Decimal(5,2), default=100.00)
    
    # Status and maintenance
    zone_status = Column(SQLEnum(ZoneStatus), default=ZoneStatus.active)
    last_inspection = Column(Date)
    next_inspection = Column(Date)
    maintenance_notes = Column(Text)
    
    created_at = Column(TIMESTAMP, default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, default=func.current_timestamp(), onupdate=func.current_timestamp())
    configured_by = Column(CHAR(36), ForeignKey('users.id'), nullable=False)
    
    # Relationships
    site = relationship("Site")
    zone = relationship("Zone")
    configured_by_user = relationship("User")
    
    # Indexes
    __table_args__ = (
        Index('idx_zone_configs_site', 'site_id', 'zone_status'),
        Index('idx_zone_configs_performance', 'safety_score', 'compliance_score'),
        Index('idx_zone_configs_monitoring', 'monitoring_level', 'camera_coverage_percentage'),
        UniqueConstraint('site_id', 'zone_id', name='unique_site_zone_config'),
    )


class SitePerformanceTracking(Base):
    __tablename__ = 'site_performance_tracking'
    
    id = Column(CHAR(36), primary_key=True, default=generate_uuid)
    site_id = Column(CHAR(36), ForeignKey('sites.id'), nullable=False)
    tracking_date = Column(Date, nullable=False)
    tracking_period = Column(SQLEnum(TrackingPeriod), nullable=False)
    
    # System performance metrics
    system_health_score = Column(Decimal(5,2), default=100.00)
    uptime_percentage = Column(Decimal(5,2), default=100.00)
    response_time_avg_ms = Column(Integer, default=0)
    error_rate_percentage = Column(Decimal(5,2), default=0.00)
    throughput_operations_per_hour = Column(Integer, default=0)
    
    # Infrastructure performance
    network_performance_score = Column(Decimal(5,2), default=100.00)
    power_stability_score = Column(Decimal(5,2), default=100.00)
    storage_performance_score = Column(Decimal(5,2), default=100.00)
    camera_system_score = Column(Decimal(5,2), default=100.00)
    
    # Operational metrics
    personnel_capacity_utilization = Column(Decimal(5,2), default=0.00)
    zone_utilization_average = Column(Decimal(5,2), default=0.00)
    safety_incident_count = Column(Integer, default=0)
    compliance_violation_count = Column(Integer, default=0)
    
    # Alert and response metrics
    alerts_generated = Column(Integer, default=0)
    alerts_resolved = Column(Integer, default=0)
    average_response_time_minutes = Column(Integer, default=0)
    escalated_incidents = Column(Integer, default=0)
    
    # AI and detection performance
    detection_accuracy_rate = Column(Decimal(5,2), default=0.00)
    false_positive_rate = Column(Decimal(5,2), default=0.00)
    ai_processing_time_avg_ms = Column(Integer, default=0)
    detection_coverage_percentage = Column(Decimal(5,2), default=0.00)
    
    # Resource utilization
    cpu_utilization_avg = Column(Decimal(5,2), default=0.00)
    memory_utilization_avg = Column(Decimal(5,2), default=0.00)
    storage_utilization_percentage = Column(Decimal(5,2), default=0.00)
    bandwidth_utilization_percentage = Column(Decimal(5,2), default=0.00)
    
    # Compliance and quality metrics
    compliance_score = Column(Decimal(5,2), default=100.00)
    audit_findings = Column(Integer, default=0)
    documentation_completeness = Column(Decimal(5,2), default=100.00)
    training_compliance_rate = Column(Decimal(5,2), default=100.00)
    
    # Trend indicators
    performance_trend = Column(SQLEnum(PerformanceTrend), default=PerformanceTrend.stable)
    health_trend = Column(SQLEnum(HealthTrend), default=HealthTrend.stable)
    efficiency_trend = Column(SQLEnum(EfficiencyTrend), default=EfficiencyTrend.stable)
    
    # Comparison metrics
    site_ranking = Column(Integer)
    industry_benchmark_comparison = Column(Decimal(6,2))
    historical_performance_change = Column(Decimal(6,2))
    
    # Notes and analysis
    performance_notes = Column(Text)
    improvement_recommendations = Column(JSON)
    issues_identified = Column(JSON)
    action_items = Column(JSON)
    
    created_at = Column(TIMESTAMP, default=func.current_timestamp())
    calculated_at = Column(TIMESTAMP, default=func.current_timestamp())
    analyst_id = Column(CHAR(36), ForeignKey('users.id'))
    
    # Relationships
    site = relationship("Site")
    analyst = relationship("User")
    
    # Indexes
    __table_args__ = (
        Index('idx_site_performance_date', 'site_id', 'tracking_date', 'tracking_period'),
        Index('idx_site_performance_scores', 'system_health_score', 'compliance_score'),
        Index('idx_site_performance_trends', 'performance_trend', 'health_trend'),
        UniqueConstraint('site_id', 'tracking_date', 'tracking_period', name='unique_site_tracking_period'),
    )


class SiteComplianceTracking(Base):
    __tablename__ = 'site_compliance_tracking'
    
    id = Column(CHAR(36), primary_key=True, default=generate_uuid)
    site_id = Column(CHAR(36), ForeignKey('sites.id'), nullable=False)
    compliance_framework = Column(String(255), nullable=False)
    compliance_date = Column(Date, nullable=False)
    
    # Compliance status
    overall_compliance_score = Column(Decimal(5,2), nullable=False)
    compliance_status = Column(SQLEnum(ComplianceStatus), default=ComplianceStatus.compliant)
    certification_valid = Column(Boolean, default=True)
    certification_expiry_date = Column(Date)
    
    # Audit information
    audit_type = Column(SQLEnum(AuditType), nullable=False)
    auditor_name = Column(String(255))
    auditor_organization = Column(String(255))
    audit_date = Column(Date, nullable=False)
    next_audit_date = Column(Date)
    
    # Findings and issues
    total_findings = Column(Integer, default=0)
    critical_findings = Column(Integer, default=0)
    major_findings = Column(Integer, default=0)
    minor_findings = Column(Integer, default=0)
    observations = Column(Integer, default=0)
    
    # Compliance areas
    safety_compliance_score = Column(Decimal(5,2), default=100.00)
    environmental_compliance_score = Column(Decimal(5,2), default=100.00)
    quality_compliance_score = Column(Decimal(5,2), default=100.00)
    security_compliance_score = Column(Decimal(5,2), default=100.00)
    
    # Documentation compliance
    documentation_completeness = Column(Decimal(5,2), default=100.00)
    training_records_current = Column(Boolean, default=True)
    procedure_documentation_current = Column(Boolean, default=True)
    incident_reporting_compliant = Column(Boolean, default=True)
    
    # Corrective actions
    corrective_actions_required = Column(Integer, default=0)
    corrective_actions_completed = Column(Integer, default=0)
    corrective_actions_overdue = Column(Integer, default=0)
    preventive_actions_implemented = Column(Integer, default=0)
    
    # Timeline tracking
    findings_resolved_days = Column(Integer)
    compliance_maintenance_effort_hours = Column(Integer)
    cost_of_compliance_usd = Column(Decimal(12,2))
    
    # Regulatory requirements
    regulatory_updates_applied = Column(Integer, default=0)
    regulatory_notifications_pending = Column(Integer, default=0)
    license_renewals_due = Column(JSON)
    permit_status = Column(JSON)
    
    # Risk assessment
    compliance_risk_score = Column(Decimal(5,2), default=0.00)
    risk_mitigation_plans = Column(JSON)
    insurance_compliance = Column(Boolean, default=True)
    legal_exposure_assessment = Column(Text)
    
    # Performance tracking
    compliance_trend = Column(SQLEnum(ComplianceTrend), default=ComplianceTrend.stable)
    benchmark_comparison = Column(Decimal(6,2))
    historical_compliance_change = Column(Decimal(6,2))
    
    # Stakeholder information
    compliance_officer_id = Column(CHAR(36), ForeignKey('users.id'))
    regulatory_contact_info = Column(JSON)
    consultant_information = Column(JSON)
    
    created_at = Column(TIMESTAMP, default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, default=func.current_timestamp(), onupdate=func.current_timestamp())
    reported_by = Column(CHAR(36), ForeignKey('users.id'), nullable=False)
    approved_by = Column(CHAR(36), ForeignKey('users.id'))
    
    # Relationships
    site = relationship("Site")
    compliance_officer = relationship("User", foreign_keys=[compliance_officer_id])
    reported_by_user = relationship("User", foreign_keys=[reported_by])
    approved_by_user = relationship("User", foreign_keys=[approved_by])
    
    # Indexes
    __table_args__ = (
        Index('idx_compliance_site_framework', 'site_id', 'compliance_framework', 'compliance_date'),
        Index('idx_compliance_status', 'compliance_status', 'certification_valid'),
        Index('idx_compliance_audit', 'audit_type', 'next_audit_date'),
        Index('idx_compliance_scores', 'overall_compliance_score', 'safety_compliance_score'),
    )


# SYSTEM MONITORING & INFRASTRUCTURE HEALTH TABLES

# System monitoring enums
class SystemStatus(enum.Enum):
    healthy = "healthy"
    warning = "warning"
    critical = "critical"
    maintenance = "maintenance"

class SystemHealthTrend(enum.Enum):
    improving = "improving"
    stable = "stable"
    declining = "declining"
    volatile = "volatile"

class SystemPerformanceTrend(enum.Enum):
    improving = "improving"
    stable = "stable"
    declining = "declining"

class CapacityTrend(enum.Enum):
    increasing = "increasing"
    stable = "stable"
    decreasing = "decreasing"

class ServiceType(enum.Enum):
    ai_detection = "ai_detection"
    video_streaming = "video_streaming"
    database = "database"
    api_gateway = "api_gateway"
    notification = "notification"
    file_storage = "file_storage"
    authentication = "authentication"
    monitoring = "monitoring"
    backup = "backup"

class ComponentType(enum.Enum):
    load_balancer = "load_balancer"
    cdn = "cdn"
    cache = "cache"
    message_queue = "message_queue"
    dns = "dns"
    firewall = "firewall"
    proxy = "proxy"
    storage = "storage"
    network = "network"

class ComponentStatus(enum.Enum):
    healthy = "healthy"
    warning = "warning"
    critical = "critical"
    offline = "offline"
    maintenance = "maintenance"

class AlertLevel(enum.Enum):
    info = "info"
    warning = "warning"
    critical = "critical"
    emergency = "emergency"

class AlertCategory(enum.Enum):
    performance = "performance"
    availability = "availability"
    security = "security"
    capacity = "capacity"
    configuration = "configuration"
    compliance = "compliance"

class BusinessImpact(enum.Enum):
    none = "none"
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"

class AlertStatus(enum.Enum):
    active = "active"
    investigating = "investigating"
    acknowledged = "acknowledged"
    resolved = "resolved"
    suppressed = "suppressed"
    expired = "expired"

class DashboardType(enum.Enum):
    system_overview = "system_overview"
    service_monitoring = "service_monitoring"
    infrastructure = "infrastructure"
    site_monitoring = "site_monitoring"
    custom = "custom"

class ViewPermissions(enum.Enum):
    read = "read"
    read_write = "read_write"
    admin = "admin"


class SystemHealthMonitoring(Base):
    __tablename__ = 'system_health_monitoring'
    
    id = Column(CHAR(36), primary_key=True, default=generate_uuid)
    timestamp = Column(TIMESTAMP, default=func.current_timestamp())
    monitoring_interval_minutes = Column(Integer, default=5)
    
    # Overall system health
    overall_health_score = Column(Decimal(5,2), nullable=False)
    system_status = Column(SQLEnum(SystemStatus), default=SystemStatus.healthy)
    availability_percentage = Column(Decimal(5,2), default=100.00)
    response_time_avg_ms = Column(Integer)
    throughput_requests_per_second = Column(Decimal(10,2))
    
    # Resource utilization aggregates
    total_cpu_utilization = Column(Decimal(5,2))
    total_memory_utilization = Column(Decimal(5,2))
    total_storage_utilization = Column(Decimal(5,2))
    total_network_utilization = Column(Decimal(5,2))
    
    # Service and infrastructure health summary
    healthy_services_count = Column(Integer, default=0)
    warning_services_count = Column(Integer, default=0)
    critical_services_count = Column(Integer, default=0)
    total_services_count = Column(Integer, default=0)
    
    healthy_sites_count = Column(Integer, default=0)
    warning_sites_count = Column(Integer, default=0)
    critical_sites_count = Column(Integer, default=0)
    total_sites_count = Column(Integer, default=0)
    
    # Performance indicators
    error_rate_percentage = Column(Decimal(5,2), default=0.00)
    alert_rate_per_hour = Column(Decimal(8,2), default=0.00)
    incident_resolution_time_avg_minutes = Column(Integer)
    sla_compliance_percentage = Column(Decimal(5,2), default=100.00)
    
    # Trend indicators
    health_trend = Column(SQLEnum(SystemHealthTrend), default=SystemHealthTrend.stable)
    performance_trend = Column(SQLEnum(SystemPerformanceTrend), default=SystemPerformanceTrend.stable)
    capacity_trend = Column(SQLEnum(CapacityTrend), default=CapacityTrend.stable)
    
    created_at = Column(TIMESTAMP, default=func.current_timestamp())
    
    # Indexes
    __table_args__ = (
        Index('idx_system_health_timestamp', 'timestamp'),
        Index('idx_system_health_status', 'system_status', 'overall_health_score'),
        Index('idx_system_health_trends', 'health_trend', 'performance_trend'),
    )


class ServiceHealthMetric(Base):
    __tablename__ = 'service_health_metrics'
    
    id = Column(CHAR(36), primary_key=True, default=generate_uuid)
    service_name = Column(String(255), nullable=False)
    service_type = Column(SQLEnum(ServiceType), nullable=False)
    timestamp = Column(TIMESTAMP, default=func.current_timestamp())
    
    # Service status
    service_status = Column(SQLEnum(ComponentStatus), default=ComponentStatus.healthy)
    uptime_percentage = Column(Decimal(5,2), default=100.00)
    last_restart = Column(TIMESTAMP)
    restart_count_24h = Column(Integer, default=0)
    
    # Performance metrics
    response_time_avg_ms = Column(Decimal(8,3))
    response_time_p95_ms = Column(Decimal(8,3))
    response_time_p99_ms = Column(Decimal(8,3))
    throughput_requests_per_second = Column(Decimal(8,2))
    success_rate_percentage = Column(Decimal(5,2), default=100.00)
    
    # Resource utilization
    cpu_utilization_percentage = Column(Decimal(5,2))
    memory_utilization_percentage = Column(Decimal(5,2))
    memory_usage_gb = Column(Decimal(8,2))
    disk_utilization_percentage = Column(Decimal(5,2))
    network_io_mbps = Column(Decimal(8,2))
    
    # Error tracking
    total_errors_24h = Column(Integer, default=0)
    error_rate_percentage = Column(Decimal(5,2), default=0.00)
    timeout_errors = Column(Integer, default=0)
    connection_errors = Column(Integer, default=0)
    processing_errors = Column(Integer, default=0)
    
    # Service-specific metrics
    active_connections = Column(Integer)
    queue_length = Column(Integer, default=0)
    cache_hit_ratio = Column(Decimal(5,2))
    database_connections = Column(Integer)
    concurrent_requests = Column(Integer)
    
    # Health check results
    health_check_status = Column(Boolean, default=True)
    health_check_response_time_ms = Column(Integer)
    dependency_status = Column(JSON)
    external_service_status = Column(JSON)
    
    created_at = Column(TIMESTAMP, default=func.current_timestamp())
    
    # Indexes
    __table_args__ = (
        Index('idx_service_health_name_time', 'service_name', 'timestamp'),
        Index('idx_service_health_status', 'service_status', 'uptime_percentage'),
        Index('idx_service_health_performance', 'response_time_avg_ms', 'error_rate_percentage'),
    )


class InfrastructureMonitoring(Base):
    __tablename__ = 'infrastructure_monitoring'
    
    id = Column(CHAR(36), primary_key=True, default=generate_uuid)
    component_name = Column(String(255), nullable=False)
    component_type = Column(SQLEnum(ComponentType), nullable=False)
    timestamp = Column(TIMESTAMP, default=func.current_timestamp())
    
    # Component status
    component_status = Column(SQLEnum(ComponentStatus), default=ComponentStatus.healthy)
    availability_percentage = Column(Decimal(5,2), default=100.00)
    capacity_utilization_percentage = Column(Decimal(5,2))
    
    # Performance metrics
    throughput_mbps = Column(Decimal(10,2))
    latency_avg_ms = Column(Decimal(8,3))
    latency_p95_ms = Column(Decimal(8,3))
    
    # Component-specific metrics
    active_connections = Column(Integer)
    hit_ratio_percentage = Column(Decimal(5,2))
    cache_size_gb = Column(Decimal(10,2))
    queue_size = Column(Integer)
    message_processing_rate = Column(Decimal(8,2))
    
    # Resource utilization
    cpu_utilization_percentage = Column(Decimal(5,2))
    memory_utilization_percentage = Column(Decimal(5,2))
    disk_utilization_percentage = Column(Decimal(5,2))
    network_utilization_percentage = Column(Decimal(5,2))
    
    # Error tracking
    error_count_24h = Column(Integer, default=0)
    error_rate_percentage = Column(Decimal(5,2), default=0.00)
    timeout_count = Column(Integer, default=0)
    connection_failures = Column(Integer, default=0)
    
    created_at = Column(TIMESTAMP, default=func.current_timestamp())
    
    # Indexes
    __table_args__ = (
        Index('idx_infrastructure_component_time', 'component_name', 'timestamp'),
        Index('idx_infrastructure_status', 'component_status', 'availability_percentage'),
        Index('idx_infrastructure_utilization', 'capacity_utilization_percentage', 'cpu_utilization_percentage'),
    )


class SystemAlert(Base):
    __tablename__ = 'system_alerts'
    
    id = Column(CHAR(36), primary_key=True, default=generate_uuid)
    alert_id = Column(String(255), unique=True, nullable=False)
    
    # Alert classification
    alert_level = Column(SQLEnum(AlertLevel), nullable=False)
    alert_category = Column(SQLEnum(AlertCategory), nullable=False)
    alert_type = Column(String(255), nullable=False)
    alert_source = Column(String(255), nullable=False)
    
    # Alert content
    title = Column(String(500), nullable=False)
    message = Column(Text, nullable=False)
    detailed_description = Column(Text)
    recommended_actions = Column(JSON)
    
    # Scope and impact
    affected_services = Column(JSON)
    affected_sites = Column(JSON)
    affected_users_count = Column(Integer, default=0)
    business_impact = Column(SQLEnum(BusinessImpact), default=BusinessImpact.none)
    
    # Alert lifecycle
    triggered_at = Column(TIMESTAMP, nullable=False)
    status = Column(SQLEnum(AlertStatus), default=AlertStatus.active)
    assigned_to = Column(CHAR(36), ForeignKey('users.id'))
    acknowledged_by = Column(CHAR(36), ForeignKey('users.id'))
    acknowledged_at = Column(TIMESTAMP)
    resolved_by = Column(CHAR(36), ForeignKey('users.id'))
    resolved_at = Column(TIMESTAMP)
    resolution_notes = Column(Text)
    
    created_at = Column(TIMESTAMP, default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, default=func.current_timestamp(), onupdate=func.current_timestamp())
    
    # Relationships
    assigned_to_user = relationship("User", foreign_keys=[assigned_to])
    acknowledged_by_user = relationship("User", foreign_keys=[acknowledged_by])
    resolved_by_user = relationship("User", foreign_keys=[resolved_by])
    
    # Indexes
    __table_args__ = (
        Index('idx_alerts_level_status', 'alert_level', 'status', 'triggered_at'),
        Index('idx_alerts_category', 'alert_category', 'alert_type'),
        Index('idx_alerts_assigned', 'assigned_to', 'status'),
    )


class MonitoringDashboard(Base):
    __tablename__ = 'monitoring_dashboards'
    
    id = Column(CHAR(36), primary_key=True, default=generate_uuid)
    dashboard_name = Column(String(255), nullable=False)
    dashboard_type = Column(SQLEnum(DashboardType), nullable=False)
    created_by = Column(CHAR(36), ForeignKey('users.id'), nullable=False)
    
    # Dashboard configuration
    layout_config = Column(JSON)
    refresh_interval_seconds = Column(Integer, default=30)
    auto_refresh_enabled = Column(Boolean, default=True)
    time_range_default = Column(String(50), default='24h')
    
    # Widget configuration
    widgets = Column(JSON)
    widget_count = Column(Integer, default=0)
    custom_metrics = Column(JSON)
    filter_presets = Column(JSON)
    
    # Access control
    is_public = Column(Boolean, default=False)
    shared_with_users = Column(JSON)
    shared_with_roles = Column(JSON)
    view_permissions = Column(SQLEnum(ViewPermissions), default=ViewPermissions.read)
    
    # Usage tracking
    view_count = Column(Integer, default=0)
    last_viewed = Column(TIMESTAMP)
    favorite_count = Column(Integer, default=0)
    
    created_at = Column(TIMESTAMP, default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, default=func.current_timestamp(), onupdate=func.current_timestamp())
    
    # Relationships
    created_by_user = relationship("User")
    
    # Indexes
    __table_args__ = (
        Index('idx_dashboards_type', 'dashboard_type', 'is_public'),
        Index('idx_dashboards_creator', 'created_by', 'created_at'),
    )


# INTEGRATION & USER EXPERIENCE TABLES

# Integration enums
class IntegrationType(enum.Enum):
    communication = "communication"
    storage = "storage"
    analytics = "analytics"
    ai_ml = "ai_ml"
    monitoring = "monitoring"
    payment = "payment"
    identity = "identity"

class IntegrationStatus(enum.Enum):
    active = "active"
    inactive = "inactive"
    error = "error"
    testing = "testing"
    pending = "pending"

class TimeFormat(enum.Enum):
    twelve_hour = "12h"
    twenty_four_hour = "24h"

class Theme(enum.Enum):
    light = "light"
    dark = "dark"
    auto = "auto"

class FontSize(enum.Enum):
    small = "small"
    medium = "medium"
    large = "large"

class FeedbackType(enum.Enum):
    bug_report = "bug_report"
    feature_request = "feature_request"
    documentation = "documentation"
    general = "general"

class FeedbackStatus(enum.Enum):
    submitted = "submitted"
    reviewing = "reviewing"
    in_progress = "in_progress"
    resolved = "resolved"
    closed = "closed"


class ThirdPartyIntegration(Base):
    __tablename__ = 'third_party_integrations'
    
    id = Column(CHAR(36), primary_key=True, default=generate_uuid)
    integration_name = Column(String(255), nullable=False)
    integration_type = Column(SQLEnum(IntegrationType), nullable=False)
    provider_name = Column(String(255), nullable=False)
    description = Column(Text)
    
    # Status and health
    status = Column(SQLEnum(IntegrationStatus), default=IntegrationStatus.pending)
    health_score = Column(Decimal(5,2), default=0.00)
    last_health_check = Column(TIMESTAMP)
    next_health_check = Column(TIMESTAMP)
    
    # Configuration
    configuration = Column(JSON, nullable=False)
    credentials = Column(JSON)  # Encrypted
    endpoints = Column(JSON)
    rate_limits = Column(JSON)
    
    # Usage tracking
    monthly_usage = Column(BigInteger, default=0)
    monthly_limit = Column(BigInteger)
    error_rate = Column(Decimal(5,2), default=0.00)
    avg_response_time_ms = Column(Decimal(8,2))
    
    created_at = Column(TIMESTAMP, default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, default=func.current_timestamp(), onupdate=func.current_timestamp())
    created_by = Column(CHAR(36), ForeignKey('users.id'), nullable=False)
    
    # Relationships
    created_by_user = relationship("User")
    
    # Indexes
    __table_args__ = (
        Index('idx_integrations_type_status', 'integration_type', 'status'),
        Index('idx_integrations_health', 'health_score', 'last_health_check'),
    )


class UserProfileSetting(Base):
    __tablename__ = 'user_profile_settings'
    
    id = Column(CHAR(36), primary_key=True, default=generate_uuid)
    user_id = Column(CHAR(36), ForeignKey('users.id'), unique=True, nullable=False)
    profile_picture_url = Column(String(500))
    bio = Column(Text)
    preferences = Column(JSON)
    notification_settings = Column(JSON)
    dashboard_config = Column(JSON)
    theme_settings = Column(JSON)
    privacy_settings = Column(JSON)
    
    created_at = Column(TIMESTAMP, default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, default=func.current_timestamp(), onupdate=func.current_timestamp())
    
    # Relationships
    user = relationship("User")
    
    # Indexes
    __table_args__ = (
        Index('idx_profile_settings_user', 'user_id'),
    )


class UserApplicationSetting(Base):
    __tablename__ = 'user_application_settings'
    
    id = Column(CHAR(36), primary_key=True, default=generate_uuid)
    user_id = Column(CHAR(36), ForeignKey('users.id'), unique=True, nullable=False)
    language = Column(String(10), default='en')
    timezone = Column(String(100))
    date_format = Column(String(50))
    time_format = Column(SQLEnum(TimeFormat), default=TimeFormat.twelve_hour)
    theme = Column(SQLEnum(Theme), default=Theme.light)
    font_size = Column(SQLEnum(FontSize), default=FontSize.medium)
    notifications_enabled = Column(Boolean, default=True)
    email_notifications = Column(Boolean, default=True)
    quiet_hours_enabled = Column(Boolean, default=False)
    quiet_hours_start = Column(Time)
    quiet_hours_end = Column(Time)
    data_sharing_enabled = Column(Boolean, default=True)
    analytics_enabled = Column(Boolean, default=True)
    
    created_at = Column(TIMESTAMP, default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, default=func.current_timestamp(), onupdate=func.current_timestamp())
    
    # Relationships
    user = relationship("User")
    
    # Indexes
    __table_args__ = (
        Index('idx_app_settings_user', 'user_id'),
    )


class HelpArticle(Base):
    __tablename__ = 'help_articles'
    
    id = Column(CHAR(36), primary_key=True, default=generate_uuid)
    title = Column(String(500), nullable=False)
    content = Column(Text, nullable=False)
    category = Column(String(100), nullable=False)
    subcategory = Column(String(100))
    tags = Column(JSON)
    author_id = Column(CHAR(36), ForeignKey('users.id'), nullable=False)
    is_published = Column(Boolean, default=False)
    view_count = Column(Integer, default=0)
    helpful_count = Column(Integer, default=0)
    unhelpful_count = Column(Integer, default=0)
    search_keywords = Column(Text)
    
    created_at = Column(TIMESTAMP, default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, default=func.current_timestamp(), onupdate=func.current_timestamp())
    
    # Relationships
    author = relationship("User")
    
    # Indexes
    __table_args__ = (
        Index('idx_help_articles_category', 'category', 'subcategory', 'is_published'),
        Index('idx_help_articles_popularity', 'view_count', 'helpful_count'),
        Index('idx_help_articles_title', 'title'),
    )


class UserFeedback(Base):
    __tablename__ = 'user_feedback'
    
    id = Column(CHAR(36), primary_key=True, default=generate_uuid)
    user_id = Column(CHAR(36), ForeignKey('users.id'), nullable=False)
    feedback_type = Column(SQLEnum(FeedbackType), nullable=False)
    title = Column(String(500), nullable=False)
    description = Column(Text, nullable=False)
    priority = Column(SQLEnum(PriorityLevel), default=PriorityLevel.medium)
    status = Column(SQLEnum(FeedbackStatus), default=FeedbackStatus.submitted)
    category = Column(String(100))
    attachments = Column(JSON)
    upvote_count = Column(Integer, default=0)
    admin_response = Column(Text)
    responded_by = Column(CHAR(36), ForeignKey('users.id'))
    responded_at = Column(TIMESTAMP)
    
    created_at = Column(TIMESTAMP, default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, default=func.current_timestamp(), onupdate=func.current_timestamp())
    
    # Relationships
    user = relationship("User", foreign_keys=[user_id])
    responded_by_user = relationship("User", foreign_keys=[responded_by])
    
    # Indexes
    __table_args__ = (
        Index('idx_feedback_type_status', 'feedback_type', 'status', 'created_at'),
        Index('idx_feedback_user', 'user_id', 'created_at'),
        Index('idx_feedback_priority', 'priority', 'status'),
    )