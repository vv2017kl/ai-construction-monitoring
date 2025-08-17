"""
Environmental & Equipment Monitoring API Routes
Handles communication logs, environmental sensors, sensor readings, equipment monitoring, quality control inspections, and project milestones
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_
from typing import List, Optional
from datetime import datetime, timedelta

from database import get_db
from models import (
    CommunicationLog, EnvironmentalSensor, SensorReading, EquipmentMonitoring,
    QualityControlInspection, ProjectMilestone, User, Site,
    MessagePriority, SensorType, CalibrationStatus, SeverityLevel
)

router = APIRouter(prefix="/api/environmental-equipment", tags=["Environmental & Equipment Monitoring"])

# ENVIRONMENTAL SENSORS ENDPOINTS

@router.get("/sensors", response_model=List[dict])
def get_all_sensors(
    site_id: Optional[str] = Query(None, description="Filter by site ID"),
    sensor_type: Optional[str] = Query(None, description="Filter by sensor type"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    db: Session = Depends(get_db)
):
    """Get all environmental sensors with optional filtering"""
    query = db.query(EnvironmentalSensor)
    
    if site_id:
        query = query.filter(EnvironmentalSensor.site_id == site_id)
    
    if sensor_type:
        try:
            type_enum = SensorType(sensor_type)
            query = query.filter(EnvironmentalSensor.sensor_type == type_enum)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid sensor type: {sensor_type}")
    
    if is_active is not None:
        query = query.filter(EnvironmentalSensor.is_active == is_active)
    
    sensors = query.order_by(EnvironmentalSensor.sensor_name).all()
    return [
        {
            "id": str(s.id),
            "site_id": str(s.site_id),
            "sensor_name": s.sensor_name,
            "sensor_type": s.sensor_type.value,
            "measurement_unit": s.measurement_unit,
            "is_active": s.is_active,
            "operational_status": s.operational_status,
            "last_reading_value": float(s.last_reading_value) if s.last_reading_value else None,
            "last_reading_timestamp": s.last_reading_timestamp.isoformat() if s.last_reading_timestamp else None,
            "calibration_status": s.calibration_status.value,
            "created_at": s.created_at.isoformat()
        }
        for s in sensors
    ]

@router.post("/sensors", response_model=dict)
def create_sensor(
    site_id: str = Query(..., description="Site ID"),
    sensor_name: str = Query(..., description="Sensor name"),
    sensor_type: str = Query(..., description="Sensor type"),
    measurement_unit: str = Query(..., description="Measurement unit"),
    db: Session = Depends(get_db)
):
    """Create a new environmental sensor"""
    # Verify site exists
    site = db.query(Site).filter(Site.id == site_id).first()
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    
    db_sensor = EnvironmentalSensor(
        site_id=site_id,
        sensor_name=sensor_name,
        sensor_type=SensorType(sensor_type),
        measurement_unit=measurement_unit
    )
    
    db.add(db_sensor)
    db.commit()
    db.refresh(db_sensor)
    
    return {
        "id": str(db_sensor.id),
        "sensor_name": db_sensor.sensor_name,
        "sensor_type": db_sensor.sensor_type.value,
        "created_at": db_sensor.created_at.isoformat()
    }

# SENSOR READINGS ENDPOINTS

@router.get("/sensor-readings", response_model=List[dict])
def get_all_readings(
    sensor_id: Optional[str] = Query(None, description="Filter by sensor ID"),
    date_from: Optional[str] = Query(None, description="Filter from date (YYYY-MM-DD)"),
    date_to: Optional[str] = Query(None, description="Filter to date (YYYY-MM-DD)"),
    is_anomaly: Optional[bool] = Query(None, description="Filter by anomaly status"),
    limit: Optional[int] = Query(100, description="Limit results"),
    db: Session = Depends(get_db)
):
    """Get all sensor readings with optional filtering"""
    query = db.query(SensorReading)
    
    if sensor_id:
        query = query.filter(SensorReading.sensor_id == sensor_id)
    
    if date_from:
        try:
            from_date = datetime.strptime(date_from, "%Y-%m-%d")
            query = query.filter(SensorReading.reading_timestamp >= from_date)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date_from format. Use YYYY-MM-DD")
    
    if date_to:
        try:
            to_date = datetime.strptime(date_to, "%Y-%m-%d")
            query = query.filter(SensorReading.reading_timestamp <= to_date)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date_to format. Use YYYY-MM-DD")
    
    if is_anomaly is not None:
        query = query.filter(SensorReading.is_anomaly == is_anomaly)
    
    readings = query.order_by(SensorReading.reading_timestamp.desc()).limit(limit).all()
    return [
        {
            "id": str(r.id),
            "sensor_id": str(r.sensor_id),
            "reading_timestamp": r.reading_timestamp.isoformat(),
            "reading_value": float(r.reading_value),
            "reading_unit": r.reading_unit,
            "data_quality_score": float(r.data_quality_score),
            "is_validated": r.is_validated,
            "is_anomaly": r.is_anomaly,
            "exceeds_threshold": r.exceeds_threshold,
            "created_at": r.created_at.isoformat()
        }
        for r in readings
    ]

@router.post("/sensor-readings", response_model=dict)
def create_reading(
    sensor_id: str = Query(..., description="Sensor ID"),
    reading_value: float = Query(..., description="Reading value"),
    reading_unit: str = Query(..., description="Reading unit"),
    db: Session = Depends(get_db)
):
    """Create a new sensor reading"""
    # Verify sensor exists
    sensor = db.query(EnvironmentalSensor).filter(EnvironmentalSensor.id == sensor_id).first()
    if not sensor:
        raise HTTPException(status_code=404, detail="Sensor not found")
    
    db_reading = SensorReading(
        sensor_id=sensor_id,
        reading_timestamp=datetime.now(),
        reading_value=reading_value,
        reading_unit=reading_unit
    )
    
    db.add(db_reading)
    db.commit()
    db.refresh(db_reading)
    
    return {
        "id": str(db_reading.id),
        "reading_value": float(db_reading.reading_value),
        "reading_timestamp": db_reading.reading_timestamp.isoformat(),
        "created_at": db_reading.created_at.isoformat()
    }

# EQUIPMENT MONITORING ENDPOINTS

@router.get("/equipment", response_model=List[dict])
def get_all_equipment(
    site_id: Optional[str] = Query(None, description="Filter by site ID"),
    equipment_type: Optional[str] = Query(None, description="Filter by equipment type"),
    operational_status: Optional[str] = Query(None, description="Filter by operational status"),
    db: Session = Depends(get_db)
):
    """Get all equipment monitoring records with optional filtering"""
    query = db.query(EquipmentMonitoring)
    
    if site_id:
        query = query.filter(EquipmentMonitoring.site_id == site_id)
    
    if equipment_type:
        query = query.filter(EquipmentMonitoring.equipment_type.ilike(f"%{equipment_type}%"))
    
    if operational_status:
        query = query.filter(EquipmentMonitoring.operational_status == operational_status)
    
    equipment = query.order_by(EquipmentMonitoring.equipment_name).all()
    return [
        {
            "id": str(e.id),
            "site_id": str(e.site_id),
            "equipment_name": e.equipment_name,
            "equipment_type": e.equipment_type,
            "operational_status": e.operational_status,
            "utilization_percentage": float(e.utilization_percentage) if e.utilization_percentage else None,
            "total_operating_hours": float(e.total_operating_hours),
            "next_maintenance_due": e.next_maintenance_due.isoformat() if e.next_maintenance_due else None,
            "current_operator_id": str(e.current_operator_id) if e.current_operator_id else None,
            "created_at": e.created_at.isoformat()
        }
        for e in equipment
    ]

@router.post("/equipment", response_model=dict)
def create_equipment(
    site_id: str = Query(..., description="Site ID"),
    equipment_name: str = Query(..., description="Equipment name"),
    equipment_type: str = Query(..., description="Equipment type"),
    db: Session = Depends(get_db)
):
    """Create a new equipment monitoring record"""
    # Verify site exists
    site = db.query(Site).filter(Site.id == site_id).first()
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    
    db_equipment = EquipmentMonitoring(
        site_id=site_id,
        equipment_name=equipment_name,
        equipment_type=equipment_type
    )
    
    db.add(db_equipment)
    db.commit()
    db.refresh(db_equipment)
    
    return {
        "id": str(db_equipment.id),
        "equipment_name": db_equipment.equipment_name,
        "equipment_type": db_equipment.equipment_type,
        "created_at": db_equipment.created_at.isoformat()
    }

# QUALITY CONTROL INSPECTIONS ENDPOINTS

@router.get("/inspections", response_model=List[dict])
def get_all_inspections(
    site_id: Optional[str] = Query(None, description="Filter by site ID"),
    inspection_type: Optional[str] = Query(None, description="Filter by inspection type"),
    overall_result: Optional[str] = Query(None, description="Filter by overall result"),
    db: Session = Depends(get_db)
):
    """Get all quality control inspections with optional filtering"""
    query = db.query(QualityControlInspection)
    
    if site_id:
        query = query.filter(QualityControlInspection.site_id == site_id)
    
    if inspection_type:
        query = query.filter(QualityControlInspection.inspection_type.ilike(f"%{inspection_type}%"))
    
    if overall_result:
        query = query.filter(QualityControlInspection.overall_result == overall_result)
    
    inspections = query.order_by(QualityControlInspection.scheduled_date.desc()).all()
    return [
        {
            "id": str(i.id),
            "site_id": str(i.site_id),
            "inspection_type": i.inspection_type,
            "inspection_category": i.inspection_category,
            "scheduled_date": i.scheduled_date.isoformat(),
            "actual_date": i.actual_date.isoformat() if i.actual_date else None,
            "inspector_id": str(i.inspector_id),
            "overall_result": i.overall_result,
            "compliance_percentage": float(i.compliance_percentage) if i.compliance_percentage else None,
            "requires_reinspection": i.requires_reinspection,
            "approval_status": i.approval_status,
            "created_at": i.created_at.isoformat()
        }
        for i in inspections
    ]

@router.post("/inspections", response_model=dict)
def create_inspection(
    site_id: str = Query(..., description="Site ID"),
    inspection_type: str = Query(..., description="Inspection type"),
    inspection_category: str = Query(..., description="Inspection category"),
    scheduled_date: str = Query(..., description="Scheduled date (YYYY-MM-DD)"),
    inspector_id: str = Query(..., description="Inspector user ID"),
    inspection_scope: str = Query(..., description="Inspection scope"),
    db: Session = Depends(get_db)
):
    """Create a new quality control inspection"""
    # Verify site and inspector exist
    site = db.query(Site).filter(Site.id == site_id).first()
    inspector = db.query(User).filter(User.id == inspector_id).first()
    
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    if not inspector:
        raise HTTPException(status_code=404, detail="Inspector not found")
    
    # Parse scheduled date
    try:
        sched_date = datetime.strptime(scheduled_date, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")
    
    db_inspection = QualityControlInspection(
        site_id=site_id,
        inspection_type=inspection_type,
        inspection_category=inspection_category,
        scheduled_date=sched_date,
        inspector_id=inspector_id,
        inspection_scope=inspection_scope,
        overall_result="pending",
        checklist_items={}  # Empty checklist initially
    )
    
    db.add(db_inspection)
    db.commit()
    db.refresh(db_inspection)
    
    return {
        "id": str(db_inspection.id),
        "inspection_type": db_inspection.inspection_type,
        "scheduled_date": db_inspection.scheduled_date.isoformat(),
        "created_at": db_inspection.created_at.isoformat()
    }

# PROJECT MILESTONES ENDPOINTS

@router.get("/milestones", response_model=List[dict])
def get_all_milestones(
    site_id: Optional[str] = Query(None, description="Filter by site ID"),
    milestone_category: Optional[str] = Query(None, description="Filter by milestone category"),
    status: Optional[str] = Query(None, description="Filter by status"),
    db: Session = Depends(get_db)
):
    """Get all project milestones with optional filtering"""
    query = db.query(ProjectMilestone)
    
    if site_id:
        query = query.filter(ProjectMilestone.site_id == site_id)
    
    if milestone_category:
        query = query.filter(ProjectMilestone.milestone_category.ilike(f"%{milestone_category}%"))
    
    if status:
        query = query.filter(ProjectMilestone.status == status)
    
    milestones = query.order_by(ProjectMilestone.planned_completion_date).all()
    return [
        {
            "id": str(m.id),
            "site_id": str(m.site_id),
            "milestone_name": m.milestone_name,
            "milestone_category": m.milestone_category,
            "status": m.status,
            "completion_percentage": float(m.completion_percentage),
            "planned_start_date": m.planned_start_date.isoformat(),
            "planned_completion_date": m.planned_completion_date.isoformat(),
            "actual_start_date": m.actual_start_date.isoformat() if m.actual_start_date else None,
            "actual_completion_date": m.actual_completion_date.isoformat() if m.actual_completion_date else None,
            "critical_path_flag": m.critical_path_flag,
            "created_at": m.created_at.isoformat()
        }
        for m in milestones
    ]

@router.post("/milestones", response_model=dict)
def create_milestone(
    site_id: str = Query(..., description="Site ID"),
    milestone_name: str = Query(..., description="Milestone name"),
    milestone_category: str = Query(..., description="Milestone category"),
    planned_start_date: str = Query(..., description="Planned start date (YYYY-MM-DD)"),
    planned_completion_date: str = Query(..., description="Planned completion date (YYYY-MM-DD)"),
    tasks_total: int = Query(..., description="Total number of tasks"),
    created_by: str = Query(..., description="Creator user ID"),
    db: Session = Depends(get_db)
):
    """Create a new project milestone"""
    # Verify site and creator exist
    site = db.query(Site).filter(Site.id == site_id).first()
    creator = db.query(User).filter(User.id == created_by).first()
    
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    if not creator:
        raise HTTPException(status_code=404, detail="Creator not found")
    
    # Parse dates
    try:
        start_date = datetime.strptime(planned_start_date, "%Y-%m-%d").date()
        completion_date = datetime.strptime(planned_completion_date, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")
    
    db_milestone = ProjectMilestone(
        site_id=site_id,
        milestone_name=milestone_name,
        milestone_category=milestone_category,
        planned_start_date=start_date,
        planned_completion_date=completion_date,
        tasks_total=tasks_total,
        deliverables=[],  # Empty deliverables initially
        created_by=created_by
    )
    
    db.add(db_milestone)
    db.commit()
    db.refresh(db_milestone)
    
    return {
        "id": str(db_milestone.id),
        "milestone_name": db_milestone.milestone_name,
        "planned_completion_date": db_milestone.planned_completion_date.isoformat(),
        "created_at": db_milestone.created_at.isoformat()
    }