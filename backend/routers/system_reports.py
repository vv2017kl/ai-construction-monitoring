"""
System & Reports API Routes
Handles: Reports, System Config, Notifications, Audit Logs, Analytics Cache
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from database import get_db
from models import *
from schemas import *

router = APIRouter()

# REPORTS ENDPOINTS
@router.get("/reports", response_model=List[ReportResponse])
async def get_reports(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all reports with pagination"""
    reports = db.query(Report).order_by(Report.created_at.desc()).offset(skip).limit(limit).all()
    return reports

@router.get("/sites/{site_id}/reports", response_model=List[ReportResponse])
async def get_site_reports(site_id: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get reports for a specific site"""
    reports = db.query(Report).filter(Report.site_id == site_id).order_by(Report.created_at.desc()).offset(skip).limit(limit).all()
    return reports

@router.post("/reports", response_model=ReportResponse)
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

@router.get("/reports/{report_id}", response_model=ReportResponse)
async def get_report(report_id: str, db: Session = Depends(get_db)):
    """Get a specific report by ID"""
    report = db.query(Report).filter(Report.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return report

@router.delete("/reports/{report_id}")
async def delete_report(report_id: str, db: Session = Depends(get_db)):
    """Delete a report"""
    report = db.query(Report).filter(Report.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    
    db.delete(report)
    db.commit()
    return {"message": "Report deleted successfully"}

# SYSTEM CONFIG ENDPOINTS
@router.get("/system-config", response_model=List[SystemConfigResponse])
async def get_system_configs(category: Optional[str] = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get system configuration settings"""
    query = db.query(SystemConfig)
    if category:
        query = query.filter(SystemConfig.category == category)
    configs = query.offset(skip).limit(limit).all()
    return configs

@router.post("/system-config", response_model=SystemConfigResponse)
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

@router.get("/system-config/{config_key}", response_model=SystemConfigResponse)
async def get_system_config(config_key: str, db: Session = Depends(get_db)):
    """Get a specific system configuration by key"""
    config = db.query(SystemConfig).filter(SystemConfig.config_key == config_key).first()
    if not config:
        raise HTTPException(status_code=404, detail="Configuration not found")
    return config

@router.put("/system-config/{config_key}", response_model=SystemConfigResponse)
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

@router.delete("/system-config/{config_key}")
async def delete_system_config(config_key: str, db: Session = Depends(get_db)):
    """Delete a system configuration"""
    config = db.query(SystemConfig).filter(SystemConfig.config_key == config_key).first()
    if not config:
        raise HTTPException(status_code=404, detail="Configuration not found")
    
    db.delete(config)
    db.commit()
    return {"message": "Configuration deleted successfully"}

# NOTIFICATIONS ENDPOINTS
@router.get("/notifications", response_model=List[NotificationResponse])
async def get_notifications(user_id: Optional[str] = None, unread_only: bool = False, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get notifications with optional filtering"""
    query = db.query(Notification)
    if user_id:
        query = query.filter(Notification.user_id == user_id)
    if unread_only:
        query = query.filter(Notification.read_at.is_(None))
    
    notifications = query.order_by(Notification.created_at.desc()).offset(skip).limit(limit).all()
    return notifications

@router.post("/notifications", response_model=NotificationResponse)
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

@router.get("/notifications/{notification_id}", response_model=NotificationResponse)
async def get_notification(notification_id: str, db: Session = Depends(get_db)):
    """Get a specific notification by ID"""
    notification = db.query(Notification).filter(Notification.id == notification_id).first()
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    return notification

@router.put("/notifications/{notification_id}/read")
async def mark_notification_read(notification_id: str, db: Session = Depends(get_db)):
    """Mark a notification as read"""
    notification = db.query(Notification).filter(Notification.id == notification_id).first()
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    
    notification.read_at = func.current_timestamp()
    db.commit()
    return {"message": "Notification marked as read"}

@router.get("/users/{user_id}/notifications/unread-count")
async def get_unread_notifications_count(user_id: str, db: Session = Depends(get_db)):
    """Get count of unread notifications for a user"""
    count = db.query(Notification).filter(
        Notification.user_id == user_id,
        Notification.read_at.is_(None)
    ).count()
    
    return {"unread_count": count}

# AUDIT LOGS ENDPOINTS
@router.get("/audit-logs")
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
@router.get("/analytics-cache/{site_id}")
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