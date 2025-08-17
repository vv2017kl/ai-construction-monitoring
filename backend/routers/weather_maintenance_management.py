"""
Weather & Maintenance Management API Routes
Handles weather integration and maintenance scheduling
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from datetime import datetime, timedelta, date, time

from database import get_db
from models import (
    WeatherIntegration, MaintenanceSchedule, User, Site,
    WeatherCondition, MaintenanceType
)

router = APIRouter(prefix="/api/weather-maintenance", tags=["Weather & Maintenance Management"])

# WEATHER INTEGRATION ENDPOINTS

@router.get("/weather", response_model=List[dict])
def get_all_weather_data(
    site_id: Optional[str] = Query(None, description="Filter by site ID"),
    service_status: Optional[str] = Query(None, description="Filter by service status"),
    db: Session = Depends(get_db)
):
    """Get all weather integration data with optional filtering"""
    query = db.query(WeatherIntegration)
    
    if site_id:
        query = query.filter(WeatherIntegration.site_id == site_id)
    
    if service_status:
        query = query.filter(WeatherIntegration.service_status == service_status)
    
    weather_data = query.order_by(WeatherIntegration.last_update_timestamp.desc()).all()
    return [
        {
            "id": str(w.id),
            "site_id": str(w.site_id),
            "weather_service_provider": w.weather_service_provider,
            "service_status": w.service_status,
            "current_temperature_celsius": float(w.current_temperature_celsius) if w.current_temperature_celsius else None,
            "current_humidity_percentage": float(w.current_humidity_percentage) if w.current_humidity_percentage else None,
            "current_wind_speed_kmh": float(w.current_wind_speed_kmh) if w.current_wind_speed_kmh else None,
            "current_condition": w.current_condition.value if w.current_condition else None,
            "current_precipitation_mm": float(w.current_precipitation_mm) if w.current_precipitation_mm else None,
            "work_suitability_score": float(w.work_suitability_score) if w.work_suitability_score else None,
            "severe_weather_probability": float(w.severe_weather_probability) if w.severe_weather_probability else None,
            "last_update_timestamp": w.last_update_timestamp.isoformat() if w.last_update_timestamp else None,
            "created_at": w.created_at.isoformat()
        }
        for w in weather_data
    ]

@router.post("/weather", response_model=dict)
def create_weather_integration(
    site_id: str = Query(..., description="Site ID"),
    weather_service_provider: str = Query(..., description="Weather service provider"),
    latitude: float = Query(..., description="Latitude"),
    longitude: float = Query(..., description="Longitude"),
    db: Session = Depends(get_db)
):
    """Create a new weather integration configuration"""
    # Verify site exists
    site = db.query(Site).filter(Site.id == site_id).first()
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    
    # Check if weather integration already exists for this site
    existing = db.query(WeatherIntegration).filter(WeatherIntegration.site_id == site_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Weather integration already exists for this site")
    
    db_weather = WeatherIntegration(
        site_id=site_id,
        weather_service_provider=weather_service_provider,
        latitude=latitude,
        longitude=longitude
    )
    
    db.add(db_weather)
    db.commit()
    db.refresh(db_weather)
    
    return {
        "id": str(db_weather.id),
        "weather_service_provider": db_weather.weather_service_provider,
        "service_status": db_weather.service_status,
        "created_at": db_weather.created_at.isoformat()
    }

@router.get("/weather/{site_id}/current", response_model=dict)
def get_current_weather(site_id: str, db: Session = Depends(get_db)):
    """Get current weather conditions for a specific site"""
    weather = db.query(WeatherIntegration).filter(WeatherIntegration.site_id == site_id).first()
    if not weather:
        raise HTTPException(status_code=404, detail="Weather integration not found for this site")
    
    return {
        "site_id": str(weather.site_id),
        "current_temperature_celsius": float(weather.current_temperature_celsius) if weather.current_temperature_celsius else None,
        "current_humidity_percentage": float(weather.current_humidity_percentage) if weather.current_humidity_percentage else None,
        "current_wind_speed_kmh": float(weather.current_wind_speed_kmh) if weather.current_wind_speed_kmh else None,
        "current_condition": weather.current_condition.value if weather.current_condition else None,
        "current_precipitation_mm": float(weather.current_precipitation_mm) if weather.current_precipitation_mm else None,
        "work_suitability_score": float(weather.work_suitability_score) if weather.work_suitability_score else None,
        "recommended_work_types": weather.recommended_work_types,
        "work_restrictions": weather.work_restrictions,
        "active_weather_alerts": weather.active_weather_alerts,
        "last_update_timestamp": weather.last_update_timestamp.isoformat() if weather.last_update_timestamp else None
    }

@router.put("/weather/{site_id}/update", response_model=dict)
def update_weather_data(
    site_id: str,
    current_temperature_celsius: Optional[float] = Query(None, description="Current temperature"),
    current_humidity_percentage: Optional[float] = Query(None, description="Current humidity"),
    current_wind_speed_kmh: Optional[float] = Query(None, description="Current wind speed"),
    current_condition: Optional[str] = Query(None, description="Current weather condition"),
    work_suitability_score: Optional[float] = Query(None, description="Work suitability score"),
    db: Session = Depends(get_db)
):
    """Update current weather data for a site"""
    weather = db.query(WeatherIntegration).filter(WeatherIntegration.site_id == site_id).first()
    if not weather:
        raise HTTPException(status_code=404, detail="Weather integration not found for this site")
    
    # Update provided fields
    if current_temperature_celsius is not None:
        weather.current_temperature_celsius = current_temperature_celsius
    if current_humidity_percentage is not None:
        weather.current_humidity_percentage = current_humidity_percentage
    if current_wind_speed_kmh is not None:
        weather.current_wind_speed_kmh = current_wind_speed_kmh
    if current_condition is not None:
        try:
            weather.current_condition = WeatherCondition(current_condition)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid weather condition: {current_condition}")
    if work_suitability_score is not None:
        weather.work_suitability_score = work_suitability_score
    
    weather.last_update_timestamp = datetime.now()
    
    db.commit()
    db.refresh(weather)
    
    return {
        "site_id": str(weather.site_id),
        "updated_fields": {
            "temperature": current_temperature_celsius,
            "humidity": current_humidity_percentage,
            "wind_speed": current_wind_speed_kmh,
            "condition": current_condition,
            "work_suitability": work_suitability_score
        },
        "last_update_timestamp": weather.last_update_timestamp.isoformat()
    }

# MAINTENANCE SCHEDULE ENDPOINTS

@router.get("/maintenance", response_model=List[dict])
def get_all_maintenance(
    site_id: Optional[str] = Query(None, description="Filter by site ID"),
    maintenance_type: Optional[str] = Query(None, description="Filter by maintenance type"),
    status: Optional[str] = Query(None, description="Filter by status"),
    assigned_technician_id: Optional[str] = Query(None, description="Filter by assigned technician"),
    date_from: Optional[str] = Query(None, description="Filter from date (YYYY-MM-DD)"),
    date_to: Optional[str] = Query(None, description="Filter to date (YYYY-MM-DD)"),
    db: Session = Depends(get_db)
):
    """Get all maintenance schedules with optional filtering"""
    query = db.query(MaintenanceSchedule)
    
    if site_id:
        query = query.filter(MaintenanceSchedule.site_id == site_id)
    
    if maintenance_type:
        try:
            type_enum = MaintenanceType(maintenance_type)
            query = query.filter(MaintenanceSchedule.maintenance_type == type_enum)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid maintenance type: {maintenance_type}")
    
    if status:
        query = query.filter(MaintenanceSchedule.status == status)
    
    if assigned_technician_id:
        query = query.filter(MaintenanceSchedule.assigned_technician_id == assigned_technician_id)
    
    if date_from:
        try:
            from_date = datetime.strptime(date_from, "%Y-%m-%d").date()
            query = query.filter(MaintenanceSchedule.scheduled_date >= from_date)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date_from format. Use YYYY-MM-DD")
    
    if date_to:
        try:
            to_date = datetime.strptime(date_to, "%Y-%m-%d").date()
            query = query.filter(MaintenanceSchedule.scheduled_date <= to_date)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date_to format. Use YYYY-MM-DD")
    
    maintenance = query.order_by(MaintenanceSchedule.scheduled_date).all()
    return [
        {
            "id": str(m.id),
            "site_id": str(m.site_id),
            "asset_type": m.asset_type,
            "asset_id": str(m.asset_id),
            "asset_name": m.asset_name,
            "maintenance_type": m.maintenance_type.value,
            "maintenance_description": m.maintenance_description,
            "scheduled_date": m.scheduled_date.isoformat(),
            "scheduled_start_time": m.scheduled_start_time.isoformat() if m.scheduled_start_time else None,
            "scheduled_end_time": m.scheduled_end_time.isoformat() if m.scheduled_end_time else None,
            "estimated_duration_hours": float(m.estimated_duration_hours) if m.estimated_duration_hours else None,
            "assigned_technician_id": str(m.assigned_technician_id) if m.assigned_technician_id else None,
            "status": m.status,
            "completion_percentage": float(m.completion_percentage),
            "next_maintenance_due": m.next_maintenance_due.isoformat() if m.next_maintenance_due else None,
            "estimated_cost": float(m.estimated_cost) if m.estimated_cost else None,
            "actual_cost": float(m.actual_cost) if m.actual_cost else None,
            "created_at": m.created_at.isoformat()
        }
        for m in maintenance
    ]

@router.post("/maintenance", response_model=dict)
def create_maintenance(
    site_id: str = Query(..., description="Site ID"),
    asset_type: str = Query(..., description="Asset type"),
    asset_id: str = Query(..., description="Asset ID"),
    asset_name: str = Query(..., description="Asset name"),
    maintenance_type: str = Query(..., description="Maintenance type"),
    maintenance_description: str = Query(..., description="Maintenance description"),
    scheduled_date: str = Query(..., description="Scheduled date (YYYY-MM-DD)"),
    created_by: str = Query(..., description="Creator user ID"),
    db: Session = Depends(get_db)
):
    """Create a new maintenance schedule"""
    # Verify site and creator exist
    site = db.query(Site).filter(Site.id == site_id).first()
    creator = db.query(User).filter(User.id == created_by).first()
    
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    if not creator:
        raise HTTPException(status_code=404, detail="Creator not found")
    
    # Parse scheduled date
    try:
        sched_date = datetime.strptime(scheduled_date, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")
    
    db_maintenance = MaintenanceSchedule(
        site_id=site_id,
        asset_type=asset_type,
        asset_id=asset_id,
        asset_name=asset_name,
        maintenance_type=MaintenanceType(maintenance_type),
        maintenance_description=maintenance_description,
        scheduled_date=sched_date,
        quality_checklist={},  # Empty checklist initially
        created_by=created_by
    )
    
    db.add(db_maintenance)
    db.commit()
    db.refresh(db_maintenance)
    
    return {
        "id": str(db_maintenance.id),
        "asset_name": db_maintenance.asset_name,
        "maintenance_type": db_maintenance.maintenance_type.value,
        "scheduled_date": db_maintenance.scheduled_date.isoformat(),
        "created_at": db_maintenance.created_at.isoformat()
    }

@router.put("/maintenance/{maintenance_id}/status", response_model=dict)
def update_maintenance_status(
    maintenance_id: str,
    status: str = Query(..., description="New status"),
    completion_percentage: Optional[float] = Query(None, description="Completion percentage"),
    actual_start_timestamp: Optional[str] = Query(None, description="Actual start timestamp (ISO format)"),
    actual_end_timestamp: Optional[str] = Query(None, description="Actual end timestamp (ISO format)"),
    db: Session = Depends(get_db)
):
    """Update maintenance status and progress"""
    maintenance = db.query(MaintenanceSchedule).filter(MaintenanceSchedule.id == maintenance_id).first()
    if not maintenance:
        raise HTTPException(status_code=404, detail="Maintenance schedule not found")
    
    # Update status
    maintenance.status = status
    
    if completion_percentage is not None:
        maintenance.completion_percentage = completion_percentage
    
    if actual_start_timestamp:
        try:
            maintenance.actual_start_timestamp = datetime.fromisoformat(actual_start_timestamp.replace('Z', '+00:00'))
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid actual_start_timestamp format")
    
    if actual_end_timestamp:
        try:
            maintenance.actual_end_timestamp = datetime.fromisoformat(actual_end_timestamp.replace('Z', '+00:00'))
            # Calculate actual duration if both start and end times are provided
            if maintenance.actual_start_timestamp:
                duration = maintenance.actual_end_timestamp - maintenance.actual_start_timestamp
                maintenance.actual_duration_hours = duration.total_seconds() / 3600
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid actual_end_timestamp format")
    
    db.commit()
    db.refresh(maintenance)
    
    return {
        "id": str(maintenance.id),
        "status": maintenance.status,
        "completion_percentage": float(maintenance.completion_percentage),
        "actual_start_timestamp": maintenance.actual_start_timestamp.isoformat() if maintenance.actual_start_timestamp else None,
        "actual_end_timestamp": maintenance.actual_end_timestamp.isoformat() if maintenance.actual_end_timestamp else None,
        "actual_duration_hours": float(maintenance.actual_duration_hours) if maintenance.actual_duration_hours else None,
        "updated_at": maintenance.updated_at.isoformat()
    }

@router.get("/maintenance/analytics/summary")
def get_maintenance_analytics(
    site_id: Optional[str] = Query(None, description="Filter by site ID"),
    days: Optional[int] = Query(30, description="Days back for analysis"),
    db: Session = Depends(get_db)
):
    """Get maintenance analytics summary"""
    query = db.query(MaintenanceSchedule)
    
    if site_id:
        query = query.filter(MaintenanceSchedule.site_id == site_id)
    
    if days:
        cutoff_date = datetime.now() - timedelta(days=days)
        query = query.filter(MaintenanceSchedule.scheduled_date >= cutoff_date.date())
    
    total_maintenance = query.count()
    completed = query.filter(MaintenanceSchedule.status == "completed").count()
    in_progress = query.filter(MaintenanceSchedule.status == "in_progress").count()
    scheduled = query.filter(MaintenanceSchedule.status == "scheduled").count()
    
    avg_completion = query.with_entities(func.avg(MaintenanceSchedule.completion_percentage)).scalar() or 0
    total_cost = query.with_entities(func.sum(MaintenanceSchedule.actual_cost)).scalar() or 0
    
    return {
        "total_maintenance_items": total_maintenance,
        "completed_items": completed,
        "in_progress_items": in_progress,
        "scheduled_items": scheduled,
        "completion_rate": (completed / total_maintenance * 100) if total_maintenance > 0 else 0,
        "average_completion_percentage": float(avg_completion),
        "total_actual_cost": float(total_cost),
        "analysis_period_days": days
    }