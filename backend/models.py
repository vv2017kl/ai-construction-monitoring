"""
SQLAlchemy models for AI Construction Management System
Based on MASTER_DATABASE_SCHEMA.md
"""
from sqlalchemy import (
    Column, String, Text, Integer, DateTime, Boolean, 
    ForeignKey, Index, JSON, Enum as SQLEnum, Date, TIMESTAMP,
    UniqueConstraint, DECIMAL as Decimal
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