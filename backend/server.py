from fastapi import FastAPI, APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import get_db, test_connection
from models import *
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Optional
import uuid
from datetime import datetime


ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# Create the main app without a prefix
app = FastAPI(title="AI Construction Management API", version="1.0.0")

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Test database connection on startup
if not test_connection():
    raise RuntimeError("Failed to connect to database")

# Define Response Models
class StatusCheck(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    client_name: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class StatusCheckCreate(BaseModel):
    client_name: str

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

class SiteUpdateRequest(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    address: Optional[str] = None
    type: Optional[str] = None
    phase: Optional[str] = None
    manager_id: Optional[str] = None

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

class AIDetectionCreateRequest(BaseModel):
    camera_id: str
    site_id: str
    zone_id: Optional[str] = None
    detection_type: Optional[str] = None
    person_count: int = 0
    confidence_score: Optional[float] = None
    detection_results: Optional[dict] = None
    safety_score: Optional[float] = None

class AIModelCreateRequest(BaseModel):
    name: str
    description: Optional[str] = None
    model_type: Optional[str] = None
    provider: Optional[str] = None
    endpoint_url: Optional[str] = None
    confidence_threshold: Optional[float] = 0.50

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

# Basic API routes
@api_router.get("/")
async def root():
    return {"message": "AI Construction Management API", "version": "1.0.0", "status": "running"}

@api_router.get("/health")
async def health_check():
    db_status = test_connection()
    return {
        "status": "healthy" if db_status else "unhealthy",
        "database": "connected" if db_status else "disconnected",
        "timestamp": datetime.utcnow()
    }

# Legacy status check endpoints (for backward compatibility)
@api_router.post("/status", response_model=StatusCheck)
async def create_status_check(input: StatusCheckCreate):
    status_obj = StatusCheck(**input.dict())
    return status_obj

@api_router.get("/status", response_model=List[StatusCheck])
async def get_status_checks():
    # Return empty list for now - this was the old MongoDB endpoint
    return []

# SITES ENDPOINTS
@api_router.get("/sites", response_model=List[SiteResponse])
async def get_sites(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all sites with pagination"""
    sites = db.query(Site).offset(skip).limit(limit).all()
    return sites

@api_router.get("/sites/{site_id}", response_model=SiteResponse)
async def get_site(site_id: str, db: Session = Depends(get_db)):
    """Get a specific site by ID"""
    site = db.query(Site).filter(Site.id == site_id).first()
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    return site

@api_router.post("/sites", response_model=SiteResponse)
async def create_site(site_data: SiteCreateRequest, db: Session = Depends(get_db)):
    """Create a new site"""
    # Check if code already exists
    existing = db.query(Site).filter(Site.code == site_data.code).first()
    if existing:
        raise HTTPException(status_code=400, detail="Site code already exists")
    
    new_site = Site(
        name=site_data.name,
        code=site_data.code,
        address=site_data.address,
        type=site_data.type,
        phase=site_data.phase,
        manager_id=site_data.manager_id
    )
    
    db.add(new_site)
    db.commit()
    db.refresh(new_site)
    return new_site

@api_router.put("/sites/{site_id}", response_model=SiteResponse)
async def update_site(site_id: str, site_data: SiteUpdateRequest, db: Session = Depends(get_db)):
    """Update an existing site"""
    site = db.query(Site).filter(Site.id == site_id).first()
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    
    for field, value in site_data.dict(exclude_unset=True).items():
        setattr(site, field, value)
    
    db.commit()
    db.refresh(site)
    return site

@api_router.delete("/sites/{site_id}")
async def delete_site(site_id: str, db: Session = Depends(get_db)):
    """Delete a site"""
    site = db.query(Site).filter(Site.id == site_id).first()
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    
    db.delete(site)
    db.commit()
    return {"message": "Site deleted successfully"}

# USERS ENDPOINTS
@api_router.get("/users", response_model=List[UserResponse])
async def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all users with pagination"""
    users = db.query(User).offset(skip).limit(limit).all()
    return users

@api_router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: str, db: Session = Depends(get_db)):
    """Get a specific user by ID"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@api_router.post("/users", response_model=UserResponse)
async def create_user(user_data: UserCreateRequest, db: Session = Depends(get_db)):
    """Create a new user"""
    # Check if username or email already exists
    existing = db.query(User).filter(
        (User.username == user_data.username) | (User.email == user_data.email)
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username or email already exists")
    
    # Simple password hashing (in production, use proper hashing)
    import hashlib
    hashed_password = hashlib.sha256(user_data.password.encode()).hexdigest()
    
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        password_hash=hashed_password,
        role=user_data.role,
        department=user_data.department,
        phone=user_data.phone
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# ZONES ENDPOINTS
@api_router.get("/sites/{site_id}/zones", response_model=List[ZoneResponse])
async def get_site_zones(site_id: str, db: Session = Depends(get_db)):
    """Get all zones for a specific site"""
    zones = db.query(Zone).filter(Zone.site_id == site_id).all()
    return zones

@api_router.get("/zones/{zone_id}", response_model=ZoneResponse)
async def get_zone(zone_id: str, db: Session = Depends(get_db)):
    """Get a specific zone by ID"""
    zone = db.query(Zone).filter(Zone.id == zone_id).first()
    if not zone:
        raise HTTPException(status_code=404, detail="Zone not found")
    return zone

# CAMERAS ENDPOINTS
@api_router.get("/sites/{site_id}/cameras", response_model=List[CameraResponse])
async def get_site_cameras(site_id: str, db: Session = Depends(get_db)):
    """Get all cameras for a specific site"""
    site_cameras = db.query(SiteCamera).filter(SiteCamera.site_id == site_id).all()
    cameras = []
    for sc in site_cameras:
        camera = db.query(Camera).filter(Camera.id == sc.camera_id).first()
        if camera:
            cameras.append(camera)
    return cameras

@api_router.get("/cameras", response_model=List[CameraResponse])
async def get_cameras(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all cameras with pagination"""
    cameras = db.query(Camera).offset(skip).limit(limit).all()
    return cameras

# ALERTS ENDPOINTS
@api_router.get("/sites/{site_id}/alerts", response_model=List[AlertResponse])
async def get_site_alerts(site_id: str, status: Optional[str] = None, db: Session = Depends(get_db)):
    """Get all alerts for a specific site, optionally filtered by status"""
    query = db.query(Alert).filter(Alert.site_id == site_id)
    if status:
        query = query.filter(Alert.status == status)
    alerts = query.order_by(Alert.timestamp.desc()).all()
    return alerts

@api_router.get("/alerts", response_model=List[AlertResponse])
async def get_alerts(skip: int = 0, limit: int = 100, priority: Optional[str] = None, db: Session = Depends(get_db)):
    """Get all alerts with pagination and optional priority filter"""
    query = db.query(Alert)
    if priority:
        query = query.filter(Alert.priority == priority)
    alerts = query.order_by(Alert.timestamp.desc()).offset(skip).limit(limit).all()
    return alerts

@api_router.get("/alerts/{alert_id}", response_model=AlertResponse)
async def get_alert(alert_id: str, db: Session = Depends(get_db)):
    """Get a specific alert by ID"""
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    return alert

# PERSONNEL ENDPOINTS
@api_router.get("/sites/{site_id}/personnel")
async def get_site_personnel(site_id: str, db: Session = Depends(get_db)):
    """Get all personnel for a specific site"""
    personnel = db.query(SitePersonnel).filter(SitePersonnel.site_id == site_id).all()
    results = []
    for p in personnel:
        user = db.query(User).filter(User.id == p.user_id).first()
        if user:
            results.append({
                "id": p.id,
                "user": {
                    "id": user.id,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "email": user.email,
                    "role": user.role
                },
                "role": p.role,
                "status": p.status,
                "check_in_time": p.check_in_time,
                "current_zone_name": p.current_zone_name,
                "activity_level": p.activity_level,
                "ppe_compliance_score": float(p.ppe_compliance_score) if p.ppe_compliance_score else 0,
                "created_at": p.created_at
            })
    return results

# Dashboard stats endpoint
@api_router.get("/dashboard/stats")
async def get_dashboard_stats(db: Session = Depends(get_db)):
    """Get dashboard statistics"""
    total_sites = db.query(Site).count()
    active_sites = db.query(Site).filter(Site.status == SiteStatus.active).count()
    total_users = db.query(User).count()
    total_cameras = db.query(Camera).count()
    active_alerts = db.query(Alert).filter(Alert.status == AlertStatus.open).count()
    
    return {
        "total_sites": total_sites,
        "active_sites": active_sites,
        "total_users": total_users,
        "total_cameras": total_cameras,
        "active_alerts": active_alerts,
        "timestamp": datetime.utcnow()
    }

# AI DETECTIONS ENDPOINTS
@api_router.get("/ai-detections", response_model=List[AIDetectionResponse])
async def get_ai_detections(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all AI detections with pagination"""
    detections = db.query(AIDetection).order_by(AIDetection.timestamp.desc()).offset(skip).limit(limit).all()
    return detections

@api_router.get("/sites/{site_id}/ai-detections", response_model=List[AIDetectionResponse])
async def get_site_ai_detections(site_id: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get AI detections for a specific site"""
    detections = db.query(AIDetection).filter(AIDetection.site_id == site_id).order_by(AIDetection.timestamp.desc()).offset(skip).limit(limit).all()
    return detections

@api_router.get("/cameras/{camera_id}/ai-detections", response_model=List[AIDetectionResponse])
async def get_camera_ai_detections(camera_id: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get AI detections for a specific camera"""
    detections = db.query(AIDetection).filter(AIDetection.camera_id == camera_id).order_by(AIDetection.timestamp.desc()).offset(skip).limit(limit).all()
    return detections

@api_router.post("/ai-detections", response_model=AIDetectionResponse)
async def create_ai_detection(detection_data: AIDetectionCreateRequest, db: Session = Depends(get_db)):
    """Create a new AI detection"""
    new_detection = AIDetection(
        camera_id=detection_data.camera_id,
        site_id=detection_data.site_id,
        zone_id=detection_data.zone_id,
        detection_type=detection_data.detection_type,
        person_count=detection_data.person_count,
        confidence_score=detection_data.confidence_score,
        detection_results=detection_data.detection_results,
        safety_score=detection_data.safety_score
    )
    
    db.add(new_detection)
    db.commit()
    db.refresh(new_detection)
    return new_detection

@api_router.get("/ai-detections/{detection_id}", response_model=AIDetectionResponse)
async def get_ai_detection(detection_id: str, db: Session = Depends(get_db)):
    """Get a specific AI detection by ID"""
    detection = db.query(AIDetection).filter(AIDetection.id == detection_id).first()
    if not detection:
        raise HTTPException(status_code=404, detail="AI Detection not found")
    return detection

# AI MODELS ENDPOINTS
@api_router.get("/ai-models", response_model=List[AIModelResponse])
async def get_ai_models(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all AI models with pagination"""
    models = db.query(AIModel).offset(skip).limit(limit).all()
    return models

@api_router.post("/ai-models", response_model=AIModelResponse)
async def create_ai_model(model_data: AIModelCreateRequest, db: Session = Depends(get_db)):
    """Create a new AI model"""
    new_model = AIModel(
        name=model_data.name,
        description=model_data.description,
        model_type=model_data.model_type,
        provider=model_data.provider,
        endpoint_url=model_data.endpoint_url,
        confidence_threshold=model_data.confidence_threshold
    )
    
    db.add(new_model)
    db.commit()
    db.refresh(new_model)
    return new_model

@api_router.get("/ai-models/{model_id}", response_model=AIModelResponse)
async def get_ai_model(model_id: str, db: Session = Depends(get_db)):
    """Get a specific AI model by ID"""
    model = db.query(AIModel).filter(AIModel.id == model_id).first()
    if not model:
        raise HTTPException(status_code=404, detail="AI Model not found")
    return model

@api_router.put("/ai-models/{model_id}", response_model=AIModelResponse)
async def update_ai_model(model_id: str, model_data: AIModelCreateRequest, db: Session = Depends(get_db)):
    """Update an existing AI model"""
    model = db.query(AIModel).filter(AIModel.id == model_id).first()
    if not model:
        raise HTTPException(status_code=404, detail="AI Model not found")
    
    for field, value in model_data.dict(exclude_unset=True).items():
        setattr(model, field, value)
    
    db.commit()
    db.refresh(model)
    return model

@api_router.delete("/ai-models/{model_id}")
async def delete_ai_model(model_id: str, db: Session = Depends(get_db)):
    """Delete an AI model"""
    model = db.query(AIModel).filter(AIModel.id == model_id).first()
    if not model:
        raise HTTPException(status_code=404, detail="AI Model not found")
    
    db.delete(model)
    db.commit()
    return {"message": "AI Model deleted successfully"}

# RECORDING SESSIONS ENDPOINTS
@api_router.get("/recording-sessions", response_model=List[RecordingSessionResponse])
async def get_recording_sessions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all recording sessions with pagination"""
    sessions = db.query(RecordingSession).order_by(RecordingSession.start_time.desc()).offset(skip).limit(limit).all()
    return sessions

@api_router.get("/cameras/{camera_id}/recording-sessions", response_model=List[RecordingSessionResponse])
async def get_camera_recording_sessions(camera_id: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get recording sessions for a specific camera"""
    sessions = db.query(RecordingSession).filter(RecordingSession.camera_id == camera_id).order_by(RecordingSession.start_time.desc()).offset(skip).limit(limit).all()
    return sessions

@api_router.get("/sites/{site_id}/recording-sessions", response_model=List[RecordingSessionResponse])
async def get_site_recording_sessions(site_id: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get recording sessions for a specific site"""
    sessions = db.query(RecordingSession).filter(RecordingSession.site_id == site_id).order_by(RecordingSession.start_time.desc()).offset(skip).limit(limit).all()
    return sessions

@api_router.get("/recording-sessions/{session_id}", response_model=RecordingSessionResponse)
async def get_recording_session(session_id: str, db: Session = Depends(get_db)):
    """Get a specific recording session by ID"""
    session = db.query(RecordingSession).filter(RecordingSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Recording Session not found")
    return session

# AI ANALYTICS ENDPOINTS
@api_router.get("/ai-analytics/detection-stats")
async def get_detection_analytics(site_id: Optional[str] = None, camera_id: Optional[str] = None, days: int = 7, db: Session = Depends(get_db)):
    """Get AI detection analytics for the specified time period"""
    from datetime import date, timedelta
    
    query = db.query(AIDetectionAnalytics)
    
    if site_id:
        query = query.filter(AIDetectionAnalytics.site_id == site_id)
    if camera_id:
        query = query.filter(AIDetectionAnalytics.camera_id == camera_id)
    
    # Filter by date range
    end_date = date.today()
    start_date = end_date - timedelta(days=days)
    query = query.filter(AIDetectionAnalytics.analysis_date >= start_date)
    
    analytics = query.all()
    
    # Aggregate the results
    total_detections = sum(a.total_detections for a in analytics)
    avg_confidence = sum(a.avg_confidence_score or 0 for a in analytics) / len(analytics) if analytics else 0
    
    return {
        "total_detections": total_detections,
        "average_confidence": round(avg_confidence, 2),
        "analytics_records": len(analytics),
        "date_range": {"start": start_date, "end": end_date}
    }

@api_router.get("/cameras/{camera_id}/ai-performance")
async def get_camera_ai_performance(camera_id: str, days: int = 30, db: Session = Depends(get_db)):
    """Get AI performance metrics for a specific camera"""
    from datetime import date, timedelta
    
    end_date = date.today()
    start_date = end_date - timedelta(days=days)
    
    performance_records = db.query(CameraAIPerformance).filter(
        CameraAIPerformance.camera_id == camera_id,
        CameraAIPerformance.analysis_date >= start_date
    ).all()
    
    if not performance_records:
        return {"message": "No performance data found for this camera"}
    
    # Calculate aggregated metrics
    avg_accuracy = sum(p.accuracy_rate or 0 for p in performance_records) / len(performance_records)
    avg_processing_time = sum(p.avg_processing_time_ms or 0 for p in performance_records) / len(performance_records)
    total_detections = sum(p.total_detections for p in performance_records)
    
    return {
        "camera_id": camera_id,
        "date_range": {"start": start_date, "end": end_date},
        "average_accuracy_rate": round(avg_accuracy, 2),
        "average_processing_time_ms": int(avg_processing_time),
        "total_detections": total_detections,
        "performance_records": len(performance_records)
    }

# REPORTS ENDPOINTS
@api_router.get("/reports", response_model=List[ReportResponse])
async def get_reports(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all reports with pagination"""
    reports = db.query(Report).order_by(Report.created_at.desc()).offset(skip).limit(limit).all()
    return reports

@api_router.get("/sites/{site_id}/reports", response_model=List[ReportResponse])
async def get_site_reports(site_id: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get reports for a specific site"""
    reports = db.query(Report).filter(Report.site_id == site_id).order_by(Report.created_at.desc()).offset(skip).limit(limit).all()
    return reports

@api_router.post("/reports", response_model=ReportResponse)
async def create_report(report_data: ReportCreateRequest, db: Session = Depends(get_db)):
    """Create a new report"""
    # For now, set created_by to a default user - in production, get from auth
    new_report = Report(
        site_id=report_data.site_id,
        name=report_data.name,
        description=report_data.description,
        report_type=report_data.report_type,
        parameters=report_data.parameters,
        output_format=report_data.output_format,
        created_by="system"  # TODO: Replace with authenticated user ID
    )
    
    db.add(new_report)
    db.commit()
    db.refresh(new_report)
    return new_report

@api_router.get("/reports/{report_id}", response_model=ReportResponse)
async def get_report(report_id: str, db: Session = Depends(get_db)):
    """Get a specific report by ID"""
    report = db.query(Report).filter(Report.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return report

@api_router.delete("/reports/{report_id}")
async def delete_report(report_id: str, db: Session = Depends(get_db)):
    """Delete a report"""
    report = db.query(Report).filter(Report.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    
    db.delete(report)
    db.commit()
    return {"message": "Report deleted successfully"}

# SYSTEM CONFIG ENDPOINTS
@api_router.get("/system-config", response_model=List[SystemConfigResponse])
async def get_system_configs(category: Optional[str] = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get system configuration settings"""
    query = db.query(SystemConfig)
    if category:
        query = query.filter(SystemConfig.category == category)
    configs = query.offset(skip).limit(limit).all()
    return configs

@api_router.post("/system-config", response_model=SystemConfigResponse)
async def create_system_config(config_data: SystemConfigCreateRequest, db: Session = Depends(get_db)):
    """Create a new system configuration"""
    # Check if config key already exists
    existing = db.query(SystemConfig).filter(SystemConfig.config_key == config_data.config_key).first()
    if existing:
        raise HTTPException(status_code=400, detail="Configuration key already exists")
    
    new_config = SystemConfig(
        config_key=config_data.config_key,
        config_value=config_data.config_value,
        config_type=config_data.config_type,
        description=config_data.description,
        category=config_data.category,
        is_sensitive=config_data.is_sensitive
    )
    
    db.add(new_config)
    db.commit()
    db.refresh(new_config)
    return new_config

@api_router.get("/system-config/{config_key}", response_model=SystemConfigResponse)
async def get_system_config(config_key: str, db: Session = Depends(get_db)):
    """Get a specific system configuration by key"""
    config = db.query(SystemConfig).filter(SystemConfig.config_key == config_key).first()
    if not config:
        raise HTTPException(status_code=404, detail="Configuration not found")
    return config

@api_router.put("/system-config/{config_key}", response_model=SystemConfigResponse)
async def update_system_config(config_key: str, config_data: SystemConfigCreateRequest, db: Session = Depends(get_db)):
    """Update an existing system configuration"""
    config = db.query(SystemConfig).filter(SystemConfig.config_key == config_key).first()
    if not config:
        raise HTTPException(status_code=404, detail="Configuration not found")
    
    config.config_value = config_data.config_value
    config.config_type = config_data.config_type
    config.description = config_data.description
    config.category = config_data.category
    config.is_sensitive = config_data.is_sensitive
    
    db.commit()
    db.refresh(config)
    return config

@api_router.delete("/system-config/{config_key}")
async def delete_system_config(config_key: str, db: Session = Depends(get_db)):
    """Delete a system configuration"""
    config = db.query(SystemConfig).filter(SystemConfig.config_key == config_key).first()
    if not config:
        raise HTTPException(status_code=404, detail="Configuration not found")
    
    db.delete(config)
    db.commit()
    return {"message": "Configuration deleted successfully"}

# NOTIFICATIONS ENDPOINTS
@api_router.get("/notifications", response_model=List[NotificationResponse])
async def get_notifications(user_id: Optional[str] = None, unread_only: bool = False, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get notifications with optional filtering"""
    query = db.query(Notification)
    if user_id:
        query = query.filter(Notification.user_id == user_id)
    if unread_only:
        query = query.filter(Notification.read_at.is_(None))
    
    notifications = query.order_by(Notification.created_at.desc()).offset(skip).limit(limit).all()
    return notifications

@api_router.post("/notifications", response_model=NotificationResponse)
async def create_notification(notification_data: NotificationCreateRequest, db: Session = Depends(get_db)):
    """Create a new notification"""
    new_notification = Notification(
        user_id=notification_data.user_id,
        title=notification_data.title,
        message=notification_data.message,
        notification_type=notification_data.notification_type,
        priority=notification_data.priority,
        related_id=notification_data.related_id,
        related_type=notification_data.related_type
    )
    
    db.add(new_notification)
    db.commit()
    db.refresh(new_notification)
    return new_notification

@api_router.get("/notifications/{notification_id}", response_model=NotificationResponse)
async def get_notification(notification_id: str, db: Session = Depends(get_db)):
    """Get a specific notification by ID"""
    notification = db.query(Notification).filter(Notification.id == notification_id).first()
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    return notification

@api_router.put("/notifications/{notification_id}/read")
async def mark_notification_read(notification_id: str, db: Session = Depends(get_db)):
    """Mark a notification as read"""
    notification = db.query(Notification).filter(Notification.id == notification_id).first()
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    
    notification.read_at = func.current_timestamp()
    db.commit()
    return {"message": "Notification marked as read"}

@api_router.get("/users/{user_id}/notifications/unread-count")
async def get_unread_notifications_count(user_id: str, db: Session = Depends(get_db)):
    """Get count of unread notifications for a user"""
    count = db.query(Notification).filter(
        Notification.user_id == user_id,
        Notification.read_at.is_(None)
    ).count()
    
    return {"unread_count": count}

# AUDIT LOGS ENDPOINTS
@api_router.get("/audit-logs")
async def get_audit_logs(user_id: Optional[str] = None, resource_type: Optional[str] = None, 
                        skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get audit logs with optional filtering"""
    query = db.query(AuditLog)
    if user_id:
        query = query.filter(AuditLog.user_id == user_id)
    if resource_type:
        query = query.filter(AuditLog.resource_type == resource_type)
    
    logs = query.order_by(AuditLog.timestamp.desc()).offset(skip).limit(limit).all()
    
    return [
        {
            "id": log.id,
            "user_id": log.user_id,
            "action": log.action,
            "resource_type": log.resource_type,
            "resource_id": log.resource_id,
            "timestamp": log.timestamp,
            "ip_address": log.ip_address
        } for log in logs
    ]

# ANALYTICS CACHE ENDPOINTS
@api_router.get("/analytics-cache/{site_id}")
async def get_analytics_cache(site_id: str, metric_type: Optional[str] = None, db: Session = Depends(get_db)):
    """Get cached analytics data for a site"""
    query = db.query(AnalyticsCache).filter(AnalyticsCache.site_id == site_id)
    if metric_type:
        query = query.filter(AnalyticsCache.metric_type == metric_type)
    
    # Only return non-expired cache entries
    query = query.filter(AnalyticsCache.expires_at > func.current_timestamp())
    
    cache_entries = query.all()
    
    return [
        {
            "id": entry.id,
            "metric_type": entry.metric_type,
            "time_period": entry.time_period,
            "data": entry.data,
            "calculated_at": entry.calculated_at,
            "expires_at": entry.expires_at
        } for entry in cache_entries
    ]

# VIDEO BOOKMARKS ENDPOINTS
@api_router.get("/video-bookmarks", response_model=List[VideoBookmarkResponse])
async def get_video_bookmarks(camera_id: Optional[str] = None, user_id: Optional[str] = None, 
                             skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get video bookmarks with optional filtering"""
    query = db.query(VideoBookmark)
    if camera_id:
        query = query.filter(VideoBookmark.camera_id == camera_id)
    if user_id:
        query = query.filter(VideoBookmark.user_id == user_id)
    
    bookmarks = query.order_by(VideoBookmark.created_at.desc()).offset(skip).limit(limit).all()
    return bookmarks

@api_router.post("/video-bookmarks", response_model=VideoBookmarkResponse)
async def create_video_bookmark(bookmark_data: VideoBookmarkCreateRequest, current_user_id: str = "system", db: Session = Depends(get_db)):
    """Create a new video bookmark"""
    from datetime import datetime
    
    # Parse the date string
    bookmark_date = datetime.strptime(bookmark_data.bookmark_date, '%Y-%m-%d').date()
    
    new_bookmark = VideoBookmark(
        camera_id=bookmark_data.camera_id,
        user_id=current_user_id,  # TODO: Get from auth
        bookmark_date=bookmark_date,
        timestamp_seconds=bookmark_data.timestamp_seconds,
        title=bookmark_data.title,
        description=bookmark_data.description,
        bookmark_type=bookmark_data.bookmark_type,
        priority_level=bookmark_data.priority_level
    )
    
    db.add(new_bookmark)
    db.commit()
    db.refresh(new_bookmark)
    return new_bookmark

@api_router.get("/video-bookmarks/{bookmark_id}", response_model=VideoBookmarkResponse)
async def get_video_bookmark(bookmark_id: str, db: Session = Depends(get_db)):
    """Get a specific video bookmark by ID"""
    bookmark = db.query(VideoBookmark).filter(VideoBookmark.id == bookmark_id).first()
    if not bookmark:
        raise HTTPException(status_code=404, detail="Video bookmark not found")
    return bookmark

@api_router.put("/video-bookmarks/{bookmark_id}/status")
async def update_bookmark_status(bookmark_id: str, status: str, db: Session = Depends(get_db)):
    """Update bookmark status"""
    bookmark = db.query(VideoBookmark).filter(VideoBookmark.id == bookmark_id).first()
    if not bookmark:
        raise HTTPException(status_code=404, detail="Video bookmark not found")
    
    bookmark.status = status
    db.commit()
    return {"message": "Bookmark status updated successfully"}

@api_router.delete("/video-bookmarks/{bookmark_id}")
async def delete_video_bookmark(bookmark_id: str, db: Session = Depends(get_db)):
    """Delete a video bookmark"""
    bookmark = db.query(VideoBookmark).filter(VideoBookmark.id == bookmark_id).first()
    if not bookmark:
        raise HTTPException(status_code=404, detail="Video bookmark not found")
    
    db.delete(bookmark)
    db.commit()
    return {"message": "Video bookmark deleted successfully"}

# VIDEO ACCESS LOGS ENDPOINTS
@api_router.get("/video-access-logs", response_model=List[VideoAccessLogResponse])
async def get_video_access_logs(user_id: Optional[str] = None, camera_id: Optional[str] = None,
                               skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get video access logs with optional filtering"""
    query = db.query(VideoAccessLog)
    if user_id:
        query = query.filter(VideoAccessLog.user_id == user_id)
    if camera_id:
        query = query.filter(VideoAccessLog.camera_id == camera_id)
    
    logs = query.order_by(VideoAccessLog.access_start.desc()).offset(skip).limit(limit).all()
    return logs

@api_router.get("/cameras/{camera_id}/access-logs", response_model=List[VideoAccessLogResponse])
async def get_camera_access_logs(camera_id: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get access logs for a specific camera"""
    logs = db.query(VideoAccessLog).filter(VideoAccessLog.camera_id == camera_id).order_by(VideoAccessLog.access_start.desc()).offset(skip).limit(limit).all()
    return logs

@api_router.get("/users/{user_id}/video-access-logs", response_model=List[VideoAccessLogResponse])
async def get_user_video_access_logs(user_id: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get video access logs for a specific user"""
    logs = db.query(VideoAccessLog).filter(VideoAccessLog.user_id == user_id).order_by(VideoAccessLog.access_start.desc()).offset(skip).limit(limit).all()
    return logs

# VIDEO EXPORTS ENDPOINTS
@api_router.get("/video-exports", response_model=List[VideoExportResponse])
async def get_video_exports(user_id: Optional[str] = None, camera_id: Optional[str] = None,
                           status: Optional[str] = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get video exports with optional filtering"""
    query = db.query(VideoExport)
    if user_id:
        query = query.filter(VideoExport.user_id == user_id)
    if camera_id:
        query = query.filter(VideoExport.camera_id == camera_id)
    if status:
        query = query.filter(VideoExport.export_status == status)
    
    exports = query.order_by(VideoExport.created_at.desc()).offset(skip).limit(limit).all()
    return exports

@api_router.post("/video-exports", response_model=VideoExportResponse)
async def create_video_export(export_data: VideoExportCreateRequest, current_user_id: str = "system", db: Session = Depends(get_db)):
    """Create a new video export request"""
    from datetime import datetime
    
    # Parse the date string
    video_date = datetime.strptime(export_data.source_video_date, '%Y-%m-%d').date()
    
    # Calculate export duration
    duration = export_data.end_timestamp_seconds - export_data.start_timestamp_seconds
    
    new_export = VideoExport(
        user_id=current_user_id,  # TODO: Get from auth
        camera_id=export_data.camera_id,
        source_video_date=video_date,
        start_timestamp_seconds=export_data.start_timestamp_seconds,
        end_timestamp_seconds=export_data.end_timestamp_seconds,
        export_duration_seconds=duration,
        export_type=export_data.export_type,
        export_format=export_data.export_format,
        export_purpose=export_data.export_purpose,
        export_justification=export_data.export_justification,
        quality_setting=export_data.quality_setting
    )
    
    db.add(new_export)
    db.commit()
    db.refresh(new_export)
    return new_export

@api_router.get("/video-exports/{export_id}", response_model=VideoExportResponse)
async def get_video_export(export_id: str, db: Session = Depends(get_db)):
    """Get a specific video export by ID"""
    export = db.query(VideoExport).filter(VideoExport.id == export_id).first()
    if not export:
        raise HTTPException(status_code=404, detail="Video export not found")
    return export

@api_router.put("/video-exports/{export_id}/status")
async def update_export_status(export_id: str, status: str, download_url: Optional[str] = None, db: Session = Depends(get_db)):
    """Update video export status"""
    export = db.query(VideoExport).filter(VideoExport.id == export_id).first()
    if not export:
        raise HTTPException(status_code=404, detail="Video export not found")
    
    export.export_status = status
    if download_url:
        export.download_url = download_url
    
    if status == "completed":
        export.processing_completed_at = func.current_timestamp()
    
    db.commit()
    return {"message": "Export status updated successfully"}

# VIDEO QUALITY METRICS ENDPOINTS
@api_router.get("/video-quality-metrics", response_model=List[VideoQualityMetricResponse])
async def get_video_quality_metrics(camera_id: Optional[str] = None, days: int = 7, 
                                   skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get video quality metrics with optional filtering"""
    from datetime import date, timedelta
    
    query = db.query(VideoQualityMetric)
    if camera_id:
        query = query.filter(VideoQualityMetric.camera_id == camera_id)
    
    # Filter by date range
    end_date = date.today()
    start_date = end_date - timedelta(days=days)
    query = query.filter(VideoQualityMetric.analysis_date >= start_date)
    
    metrics = query.order_by(VideoQualityMetric.analysis_date.desc()).offset(skip).limit(limit).all()
    return metrics

@api_router.get("/cameras/{camera_id}/quality-metrics", response_model=List[VideoQualityMetricResponse])
async def get_camera_quality_metrics(camera_id: str, days: int = 30, db: Session = Depends(get_db)):
    """Get quality metrics for a specific camera"""
    from datetime import date, timedelta
    
    end_date = date.today()
    start_date = end_date - timedelta(days=days)
    
    metrics = db.query(VideoQualityMetric).filter(
        VideoQualityMetric.camera_id == camera_id,
        VideoQualityMetric.analysis_date >= start_date
    ).order_by(VideoQualityMetric.analysis_date.desc()).all()
    
    return metrics

@api_router.get("/cameras/{camera_id}/quality-summary")
async def get_camera_quality_summary(camera_id: str, days: int = 7, db: Session = Depends(get_db)):
    """Get quality summary statistics for a camera"""
    from datetime import date, timedelta
    
    end_date = date.today()
    start_date = end_date - timedelta(days=days)
    
    metrics = db.query(VideoQualityMetric).filter(
        VideoQualityMetric.camera_id == camera_id,
        VideoQualityMetric.analysis_date >= start_date
    ).all()
    
    if not metrics:
        return {"message": "No quality data found for this camera"}
    
    # Calculate average scores
    avg_sharpness = sum(m.sharpness_score or 0 for m in metrics) / len(metrics)
    avg_brightness = sum(m.brightness_score or 0 for m in metrics) / len(metrics)
    avg_contrast = sum(m.contrast_score or 0 for m in metrics) / len(metrics)
    
    # Count quality ratings
    forensic_ratings = [m.forensic_quality_rating for m in metrics if m.forensic_quality_rating]
    
    return {
        "camera_id": camera_id,
        "date_range": {"start": start_date, "end": end_date},
        "metrics_count": len(metrics),
        "average_sharpness": round(avg_sharpness, 2),
        "average_brightness": round(avg_brightness, 2),
        "average_contrast": round(avg_contrast, 2),
        "forensic_quality_distribution": {rating: forensic_ratings.count(rating) for rating in set(forensic_ratings)}
    }

# TIMELAPSE SEQUENCES ENDPOINTS
@api_router.get("/timelapse-sequences", response_model=List[TimelapseSequenceResponse])
async def get_timelapse_sequences(site_id: Optional[str] = None, status: Optional[str] = None,
                                 skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get timelapse sequences with optional filtering"""
    query = db.query(TimelapseSequence)
    if site_id:
        query = query.filter(TimelapseSequence.site_id == site_id)
    if status:
        query = query.filter(TimelapseSequence.generation_status == status)
    
    sequences = query.order_by(TimelapseSequence.created_at.desc()).offset(skip).limit(limit).all()
    return sequences

@api_router.post("/timelapse-sequences", response_model=TimelapseSequenceResponse)
async def create_timelapse_sequence(sequence_data: TimelapseSequenceCreateRequest, current_user_id: str = "system", db: Session = Depends(get_db)):
    """Create a new timelapse sequence"""
    from datetime import datetime
    
    # Parse datetime strings
    start_dt = datetime.fromisoformat(sequence_data.start_datetime.replace('Z', '+00:00'))
    end_dt = datetime.fromisoformat(sequence_data.end_datetime.replace('Z', '+00:00'))
    
    # Calculate duration
    duration = int((end_dt - start_dt).total_seconds())
    
    new_sequence = TimelapseSequence(
        title=sequence_data.title,
        site_id=sequence_data.site_id,
        created_by=current_user_id,  # TODO: Get from auth
        primary_camera_id=sequence_data.primary_camera_id,
        start_datetime=start_dt,
        end_datetime=end_dt,
        duration_seconds=duration,
        description=sequence_data.description,
        compression_level=sequence_data.compression_level,
        frame_rate_fps=sequence_data.frame_rate_fps
    )
    
    db.add(new_sequence)
    db.commit()
    db.refresh(new_sequence)
    return new_sequence

@api_router.get("/timelapse-sequences/{sequence_id}", response_model=TimelapseSequenceResponse)
async def get_timelapse_sequence(sequence_id: str, db: Session = Depends(get_db)):
    """Get a specific timelapse sequence by ID"""
    sequence = db.query(TimelapseSequence).filter(TimelapseSequence.id == sequence_id).first()
    if not sequence:
        raise HTTPException(status_code=404, detail="Timelapse sequence not found")
    return sequence

@api_router.put("/timelapse-sequences/{sequence_id}/status")
async def update_sequence_status(sequence_id: str, status: str, db: Session = Depends(get_db)):
    """Update timelapse sequence generation status"""
    sequence = db.query(TimelapseSequence).filter(TimelapseSequence.id == sequence_id).first()
    if not sequence:
        raise HTTPException(status_code=404, detail="Timelapse sequence not found")
    
    sequence.generation_status = status
    if status == "completed":
        sequence.processing_completed_at = func.current_timestamp()
    
    db.commit()
    return {"message": "Sequence status updated successfully"}

@api_router.get("/sites/{site_id}/timelapse-sequences", response_model=List[TimelapseSequenceResponse])
async def get_site_timelapse_sequences(site_id: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get timelapse sequences for a specific site"""
    sequences = db.query(TimelapseSequence).filter(TimelapseSequence.site_id == site_id).order_by(TimelapseSequence.created_at.desc()).offset(skip).limit(limit).all()
    return sequences

# TIMELAPSE BOOKMARKS ENDPOINTS
@api_router.get("/timelapse-bookmarks", response_model=List[TimelapseBookmarkResponse])
async def get_timelapse_bookmarks(sequence_id: Optional[str] = None, user_id: Optional[str] = None,
                                 skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get timelapse bookmarks with optional filtering"""
    query = db.query(TimelapseBookmark)
    if sequence_id:
        query = query.filter(TimelapseBookmark.timelapse_sequence_id == sequence_id)
    if user_id:
        query = query.filter(TimelapseBookmark.user_id == user_id)
    
    bookmarks = query.order_by(TimelapseBookmark.timestamp_seconds).offset(skip).limit(limit).all()
    return bookmarks

@api_router.post("/timelapse-bookmarks", response_model=TimelapseBookmarkResponse)
async def create_timelapse_bookmark(bookmark_data: TimelapseBookmarkCreateRequest, current_user_id: str = "system", db: Session = Depends(get_db)):
    """Create a new timelapse bookmark"""
    new_bookmark = TimelapseBookmark(
        timelapse_sequence_id=bookmark_data.timelapse_sequence_id,
        user_id=current_user_id,  # TODO: Get from auth
        bookmark_name=bookmark_data.bookmark_name,
        timestamp_seconds=bookmark_data.timestamp_seconds,
        description=bookmark_data.description,
        bookmark_type=bookmark_data.bookmark_type
    )
    
    db.add(new_bookmark)
    db.commit()
    db.refresh(new_bookmark)
    return new_bookmark

@api_router.get("/timelapse-sequences/{sequence_id}/bookmarks", response_model=List[TimelapseBookmarkResponse])
async def get_sequence_bookmarks(sequence_id: str, db: Session = Depends(get_db)):
    """Get all bookmarks for a specific timelapse sequence"""
    bookmarks = db.query(TimelapseBookmark).filter(TimelapseBookmark.timelapse_sequence_id == sequence_id).order_by(TimelapseBookmark.timestamp_seconds).all()
    return bookmarks

@api_router.delete("/timelapse-bookmarks/{bookmark_id}")
async def delete_timelapse_bookmark(bookmark_id: str, db: Session = Depends(get_db)):
    """Delete a timelapse bookmark"""
    bookmark = db.query(TimelapseBookmark).filter(TimelapseBookmark.id == bookmark_id).first()
    if not bookmark:
        raise HTTPException(status_code=404, detail="Timelapse bookmark not found")
    
    db.delete(bookmark)
    db.commit()
    return {"message": "Timelapse bookmark deleted successfully"}

# TIMELAPSE EVENTS ENDPOINTS
@api_router.get("/timelapse-events")
async def get_timelapse_events(sequence_id: Optional[str] = None, event_type: Optional[str] = None,
                              skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get timelapse events with optional filtering"""
    query = db.query(TimelapseEvent)
    if sequence_id:
        query = query.filter(TimelapseEvent.timelapse_sequence_id == sequence_id)
    if event_type:
        query = query.filter(TimelapseEvent.event_type == event_type)
    
    events = query.order_by(TimelapseEvent.sequence_timestamp_seconds).offset(skip).limit(limit).all()
    
    return [
        {
            "id": event.id,
            "timelapse_sequence_id": event.timelapse_sequence_id,
            "event_title": event.event_title,
            "event_type": event.event_type,
            "event_timestamp": event.event_timestamp,
            "sequence_timestamp_seconds": float(event.sequence_timestamp_seconds),
            "confidence_score": float(event.confidence_score) if event.confidence_score else None,
            "impact_level": event.impact_level,
            "status": event.status
        } for event in events
    ]

@api_router.get("/timelapse-sequences/{sequence_id}/events")
async def get_sequence_events(sequence_id: str, db: Session = Depends(get_db)):
    """Get all events for a specific timelapse sequence"""
    events = db.query(TimelapseEvent).filter(TimelapseEvent.timelapse_sequence_id == sequence_id).order_by(TimelapseEvent.sequence_timestamp_seconds).all()
    
    return [
        {
            "id": event.id,
            "event_title": event.event_title,
            "event_type": event.event_type,
            "sequence_timestamp_seconds": float(event.sequence_timestamp_seconds),
            "impact_level": event.impact_level,
            "status": event.status
        } for event in events
    ]

# CONSTRUCTION MILESTONES ENDPOINTS
@api_router.get("/construction-milestones", response_model=List[ConstructionMilestoneResponse])
async def get_construction_milestones(site_id: Optional[str] = None, status: Optional[str] = None,
                                     skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get construction milestones with optional filtering"""
    query = db.query(ConstructionMilestone)
    if site_id:
        query = query.filter(ConstructionMilestone.site_id == site_id)
    if status:
        query = query.filter(ConstructionMilestone.status == status)
    
    milestones = query.order_by(ConstructionMilestone.planned_completion_date).offset(skip).limit(limit).all()
    return milestones

@api_router.post("/construction-milestones", response_model=ConstructionMilestoneResponse)
async def create_construction_milestone(milestone_data: ConstructionMilestoneCreateRequest, current_user_id: str = "system", db: Session = Depends(get_db)):
    """Create a new construction milestone"""
    from datetime import datetime
    
    # Parse date strings if provided
    planned_start = None
    planned_completion = None
    
    if milestone_data.planned_start_date:
        planned_start = datetime.strptime(milestone_data.planned_start_date, '%Y-%m-%d').date()
    if milestone_data.planned_completion_date:
        planned_completion = datetime.strptime(milestone_data.planned_completion_date, '%Y-%m-%d').date()
    
    new_milestone = ConstructionMilestone(
        site_id=milestone_data.site_id,
        milestone_name=milestone_data.milestone_name,
        milestone_code=milestone_data.milestone_code,
        description=milestone_data.description,
        project_phase=milestone_data.project_phase,
        planned_start_date=planned_start,
        planned_completion_date=planned_completion,
        created_by=current_user_id  # TODO: Get from auth
    )
    
    db.add(new_milestone)
    db.commit()
    db.refresh(new_milestone)
    return new_milestone

@api_router.get("/construction-milestones/{milestone_id}", response_model=ConstructionMilestoneResponse)
async def get_construction_milestone(milestone_id: str, db: Session = Depends(get_db)):
    """Get a specific construction milestone by ID"""
    milestone = db.query(ConstructionMilestone).filter(ConstructionMilestone.id == milestone_id).first()
    if not milestone:
        raise HTTPException(status_code=404, detail="Construction milestone not found")
    return milestone

@api_router.put("/construction-milestones/{milestone_id}/progress")
async def update_milestone_progress(milestone_id: str, completion_percentage: float, status: Optional[str] = None, db: Session = Depends(get_db)):
    """Update construction milestone progress"""
    milestone = db.query(ConstructionMilestone).filter(ConstructionMilestone.id == milestone_id).first()
    if not milestone:
        raise HTTPException(status_code=404, detail="Construction milestone not found")
    
    milestone.completion_percentage = completion_percentage
    if status:
        milestone.status = status
    
    # Auto-complete if 100%
    if completion_percentage >= 100.0:
        milestone.status = "completed"
        if not milestone.actual_completion_date:
            from datetime import date
            milestone.actual_completion_date = date.today()
    
    db.commit()
    return {"message": "Milestone progress updated successfully"}

@api_router.get("/sites/{site_id}/construction-milestones", response_model=List[ConstructionMilestoneResponse])
async def get_site_construction_milestones(site_id: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get construction milestones for a specific site"""
    milestones = db.query(ConstructionMilestone).filter(ConstructionMilestone.site_id == site_id).order_by(ConstructionMilestone.planned_completion_date).offset(skip).limit(limit).all()
    return milestones

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("startup")
async def startup_event():
    logger.info("AI Construction Management API starting up...")
    logger.info(f"Database connection: {'OK' if test_connection() else 'FAILED'}")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("AI Construction Management API shutting down...")
