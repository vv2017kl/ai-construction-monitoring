from fastapi import FastAPI, APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
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
