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

class AccessLevel(enum.Enum):
    public = "public"
    personnel = "personnel"
    authorized = "authorized"
    management = "management"

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
    access_level = Column(SQLEnum(AccessLevel), default=AccessLevel.personnel)
    
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
    site_access = relationship("UserSiteAccess", back_populates="user")
    
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