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
async def update_site(site_id: str, site_data: SiteCreateRequest, db: Session = Depends(get_db)):
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
