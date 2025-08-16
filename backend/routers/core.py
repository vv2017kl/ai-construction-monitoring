"""
Core Foundation API Routes
Handles: Sites, Users, Zones, Cameras, Alerts, Personnel
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from database import get_db
from models import *
from schemas import *

router = APIRouter()

# SITES ENDPOINTS
@router.get("/sites", response_model=List[SiteResponse])
async def get_sites(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all sites with pagination"""
    sites = db.query(Site).offset(skip).limit(limit).all()
    return sites

@router.get("/sites/{site_id}", response_model=SiteResponse)
async def get_site(site_id: str, db: Session = Depends(get_db)):
    """Get a specific site by ID"""
    site = db.query(Site).filter(Site.id == site_id).first()
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    return site

@router.post("/sites", response_model=SiteResponse)
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

@router.put("/sites/{site_id}", response_model=SiteResponse)
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

@router.delete("/sites/{site_id}")
async def delete_site(site_id: str, db: Session = Depends(get_db)):
    """Delete a site"""
    site = db.query(Site).filter(Site.id == site_id).first()
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    
    db.delete(site)
    db.commit()
    return {"message": "Site deleted successfully"}

# USERS ENDPOINTS
@router.get("/users", response_model=List[UserResponse])
async def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all users with pagination"""
    users = db.query(User).offset(skip).limit(limit).all()
    return users

@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: str, db: Session = Depends(get_db)):
    """Get a specific user by ID"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/users", response_model=UserResponse)
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
@router.get("/sites/{site_id}/zones", response_model=List[ZoneResponse])
async def get_site_zones(site_id: str, db: Session = Depends(get_db)):
    """Get all zones for a specific site"""
    zones = db.query(Zone).filter(Zone.site_id == site_id).all()
    return zones

@router.get("/zones/{zone_id}", response_model=ZoneResponse)
async def get_zone(zone_id: str, db: Session = Depends(get_db)):
    """Get a specific zone by ID"""
    zone = db.query(Zone).filter(Zone.id == zone_id).first()
    if not zone:
        raise HTTPException(status_code=404, detail="Zone not found")
    return zone

# CAMERAS ENDPOINTS
@router.get("/sites/{site_id}/cameras", response_model=List[CameraResponse])
async def get_site_cameras(site_id: str, db: Session = Depends(get_db)):
    """Get all cameras for a specific site"""
    site_cameras = db.query(SiteCamera).filter(SiteCamera.site_id == site_id).all()
    cameras = []
    for sc in site_cameras:
        camera = db.query(Camera).filter(Camera.id == sc.camera_id).first()
        if camera:
            cameras.append(camera)
    return cameras

@router.get("/cameras", response_model=List[CameraResponse])
async def get_cameras(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all cameras with pagination"""
    cameras = db.query(Camera).offset(skip).limit(limit).all()
    return cameras

# ALERTS ENDPOINTS
@router.get("/sites/{site_id}/alerts", response_model=List[AlertResponse])
async def get_site_alerts(site_id: str, status: Optional[str] = None, db: Session = Depends(get_db)):
    """Get all alerts for a specific site, optionally filtered by status"""
    query = db.query(Alert).filter(Alert.site_id == site_id)
    if status:
        query = query.filter(Alert.status == status)
    alerts = query.order_by(Alert.timestamp.desc()).all()
    return alerts

@router.get("/alerts", response_model=List[AlertResponse])
async def get_alerts(skip: int = 0, limit: int = 100, priority: Optional[str] = None, db: Session = Depends(get_db)):
    """Get all alerts with pagination and optional priority filter"""
    query = db.query(Alert)
    if priority:
        query = query.filter(Alert.priority == priority)
    alerts = query.order_by(Alert.timestamp.desc()).offset(skip).limit(limit).all()
    return alerts

@router.get("/alerts/{alert_id}", response_model=AlertResponse)
async def get_alert(alert_id: str, db: Session = Depends(get_db)):
    """Get a specific alert by ID"""
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    return alert

# PERSONNEL ENDPOINTS
@router.get("/sites/{site_id}/personnel")
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