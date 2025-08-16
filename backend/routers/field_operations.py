"""
Field Operations & Assessment API Routes
Handles: Inspection Paths, Waypoints, Executions, Execution Waypoints, Path Templates
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from database import get_db
from models import *
from schemas import *
from datetime import datetime

router = APIRouter()

# INSPECTION PATHS ENDPOINTS
@router.get("/inspection-paths", response_model=List[InspectionPathResponse])
async def get_inspection_paths(site_id: Optional[str] = None, path_type: Optional[str] = None,
                              status: Optional[str] = None, skip: int = 0, limit: int = 100, 
                              db: Session = Depends(get_db)):
    """Get inspection paths with optional filtering"""
    query = db.query(InspectionPath)
    if site_id:
        query = query.filter(InspectionPath.site_id == site_id)
    if path_type:
        query = query.filter(InspectionPath.path_type == path_type)
    if status:
        query = query.filter(InspectionPath.status == status)
    
    paths = query.order_by(InspectionPath.created_at.desc()).offset(skip).limit(limit).all()
    return paths

@router.post("/inspection-paths", response_model=InspectionPathResponse)
async def create_inspection_path(path_data: InspectionPathCreateRequest, current_user_id: str = "system", db: Session = Depends(get_db)):
    """Create a new inspection path"""
    new_path = InspectionPath(
        site_id=path_data.site_id,
        name=path_data.name,
        description=path_data.description,
        path_type=path_data.path_type,
        priority=path_data.priority,
        created_by=current_user_id,  # TODO: Get from auth
        assigned_to=path_data.assigned_to,
        estimated_duration_minutes=path_data.estimated_duration_minutes,
        zone_coverage=path_data.zone_coverage,
        is_scheduled=path_data.is_scheduled,
        schedule_frequency=path_data.schedule_frequency
    )
    
    db.add(new_path)
    db.commit()
    db.refresh(new_path)
    return new_path

@router.get("/inspection-paths/{path_id}", response_model=InspectionPathResponse)
async def get_inspection_path(path_id: str, db: Session = Depends(get_db)):
    """Get a specific inspection path by ID"""
    path = db.query(InspectionPath).filter(InspectionPath.id == path_id).first()
    if not path:
        raise HTTPException(status_code=404, detail="Inspection path not found")
    return path

@router.put("/inspection-paths/{path_id}", response_model=InspectionPathResponse)
async def update_inspection_path(path_id: str, path_data: InspectionPathCreateRequest, db: Session = Depends(get_db)):
    """Update an existing inspection path"""
    path = db.query(InspectionPath).filter(InspectionPath.id == path_id).first()
    if not path:
        raise HTTPException(status_code=404, detail="Inspection path not found")
    
    for field, value in path_data.dict(exclude_unset=True).items():
        setattr(path, field, value)
    
    db.commit()
    db.refresh(path)
    return path

@router.delete("/inspection-paths/{path_id}")
async def delete_inspection_path(path_id: str, db: Session = Depends(get_db)):
    """Delete an inspection path"""
    path = db.query(InspectionPath).filter(InspectionPath.id == path_id).first()
    if not path:
        raise HTTPException(status_code=404, detail="Inspection path not found")
    
    db.delete(path)
    db.commit()
    return {"message": "Inspection path deleted successfully"}

@router.get("/sites/{site_id}/inspection-paths", response_model=List[InspectionPathResponse])
async def get_site_inspection_paths(site_id: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get inspection paths for a specific site"""
    paths = db.query(InspectionPath).filter(InspectionPath.site_id == site_id).order_by(InspectionPath.created_at.desc()).offset(skip).limit(limit).all()
    return paths

# PATH WAYPOINTS ENDPOINTS
@router.get("/path-waypoints", response_model=List[PathWaypointResponse])
async def get_path_waypoints(path_id: Optional[str] = None, waypoint_type: Optional[str] = None,
                            skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get path waypoints with optional filtering"""
    query = db.query(PathWaypoint)
    if path_id:
        query = query.filter(PathWaypoint.path_id == path_id)
    if waypoint_type:
        query = query.filter(PathWaypoint.waypoint_type == waypoint_type)
    
    waypoints = query.order_by(PathWaypoint.path_id, PathWaypoint.waypoint_order).offset(skip).limit(limit).all()
    return waypoints

@router.post("/path-waypoints", response_model=PathWaypointResponse)
async def create_path_waypoint(waypoint_data: PathWaypointCreateRequest, db: Session = Depends(get_db)):
    """Create a new path waypoint"""
    new_waypoint = PathWaypoint(
        path_id=waypoint_data.path_id,
        waypoint_order=waypoint_data.waypoint_order,
        waypoint_name=waypoint_data.waypoint_name,
        description=waypoint_data.description,
        coordinates_x=waypoint_data.coordinates_x,
        coordinates_y=waypoint_data.coordinates_y,
        waypoint_type=waypoint_data.waypoint_type,
        zone_id=waypoint_data.zone_id,
        is_mandatory=waypoint_data.is_mandatory,
        estimated_time_minutes=waypoint_data.estimated_time_minutes,
        inspection_checklist=waypoint_data.inspection_checklist
    )
    
    db.add(new_waypoint)
    
    # Update waypoint count in parent path
    path = db.query(InspectionPath).filter(InspectionPath.id == waypoint_data.path_id).first()
    if path:
        path.waypoint_count = db.query(PathWaypoint).filter(PathWaypoint.path_id == waypoint_data.path_id).count() + 1
    
    db.commit()
    db.refresh(new_waypoint)
    return new_waypoint

@router.get("/path-waypoints/{waypoint_id}", response_model=PathWaypointResponse)
async def get_path_waypoint(waypoint_id: str, db: Session = Depends(get_db)):
    """Get a specific path waypoint by ID"""
    waypoint = db.query(PathWaypoint).filter(PathWaypoint.id == waypoint_id).first()
    if not waypoint:
        raise HTTPException(status_code=404, detail="Path waypoint not found")
    return waypoint

@router.get("/inspection-paths/{path_id}/waypoints", response_model=List[PathWaypointResponse])
async def get_path_waypoints_by_path(path_id: str, db: Session = Depends(get_db)):
    """Get all waypoints for a specific inspection path"""
    waypoints = db.query(PathWaypoint).filter(PathWaypoint.path_id == path_id).order_by(PathWaypoint.waypoint_order).all()
    return waypoints

@router.delete("/path-waypoints/{waypoint_id}")
async def delete_path_waypoint(waypoint_id: str, db: Session = Depends(get_db)):
    """Delete a path waypoint"""
    waypoint = db.query(PathWaypoint).filter(PathWaypoint.id == waypoint_id).first()
    if not waypoint:
        raise HTTPException(status_code=404, detail="Path waypoint not found")
    
    path_id = waypoint.path_id
    db.delete(waypoint)
    
    # Update waypoint count in parent path
    path = db.query(InspectionPath).filter(InspectionPath.id == path_id).first()
    if path:
        path.waypoint_count = db.query(PathWaypoint).filter(PathWaypoint.path_id == path_id).count() - 1
    
    db.commit()
    return {"message": "Path waypoint deleted successfully"}

# PATH EXECUTIONS ENDPOINTS
@router.get("/path-executions", response_model=List[PathExecutionResponse])
async def get_path_executions(path_id: Optional[str] = None, executor_id: Optional[str] = None,
                             status: Optional[str] = None, skip: int = 0, limit: int = 100, 
                             db: Session = Depends(get_db)):
    """Get path executions with optional filtering"""
    query = db.query(PathExecution)
    if path_id:
        query = query.filter(PathExecution.path_id == path_id)
    if executor_id:
        query = query.filter(PathExecution.executor_id == executor_id)
    if status:
        query = query.filter(PathExecution.execution_status == status)
    
    executions = query.order_by(PathExecution.started_at.desc()).offset(skip).limit(limit).all()
    return executions

@router.post("/path-executions", response_model=PathExecutionResponse)
async def create_path_execution(execution_data: PathExecutionCreateRequest, current_user_id: str = "system", db: Session = Depends(get_db)):
    """Create a new path execution"""
    import uuid
    
    # Get path details for initialization
    path = db.query(InspectionPath).filter(InspectionPath.id == execution_data.path_id).first()
    if not path:
        raise HTTPException(status_code=404, detail="Inspection path not found")
    
    new_execution = PathExecution(
        path_id=execution_data.path_id,
        executor_id=current_user_id,  # TODO: Get from auth
        session_id=str(uuid.uuid4()),
        execution_type=execution_data.execution_type,
        execution_reason=execution_data.execution_reason,
        planned_duration_minutes=execution_data.planned_duration_minutes or path.estimated_duration_minutes,
        weather_conditions=execution_data.weather_conditions,
        equipment_used=execution_data.equipment_used,
        waypoints_total=path.waypoint_count
    )
    
    db.add(new_execution)
    
    # Update path usage count
    path.usage_count += 1
    
    db.commit()
    db.refresh(new_execution)
    return new_execution

@router.get("/path-executions/{execution_id}", response_model=PathExecutionResponse)
async def get_path_execution(execution_id: str, db: Session = Depends(get_db)):
    """Get a specific path execution by ID"""
    execution = db.query(PathExecution).filter(PathExecution.id == execution_id).first()
    if not execution:
        raise HTTPException(status_code=404, detail="Path execution not found")
    return execution

@router.put("/path-executions/{execution_id}/status")
async def update_execution_status(execution_id: str, status: str, completion_percentage: Optional[float] = None, db: Session = Depends(get_db)):
    """Update path execution status and progress"""
    execution = db.query(PathExecution).filter(PathExecution.id == execution_id).first()
    if not execution:
        raise HTTPException(status_code=404, detail="Path execution not found")
    
    execution.execution_status = status
    if completion_percentage is not None:
        execution.completion_percentage = completion_percentage
    
    if status == "completed":
        execution.completed_at = func.current_timestamp()
        execution.is_completed = True
        if execution.started_at and execution.completed_at:
            # Calculate actual duration (this would need proper datetime handling)
            pass
    
    db.commit()
    return {"message": "Execution status updated successfully"}

@router.get("/inspection-paths/{path_id}/executions", response_model=List[PathExecutionResponse])
async def get_path_executions_by_path(path_id: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all executions for a specific inspection path"""
    executions = db.query(PathExecution).filter(PathExecution.path_id == path_id).order_by(PathExecution.started_at.desc()).offset(skip).limit(limit).all()
    return executions

# PATH EXECUTION WAYPOINTS ENDPOINTS
@router.get("/path-execution-waypoints", response_model=List[PathExecutionWaypointResponse])
async def get_execution_waypoints(execution_id: Optional[str] = None, waypoint_id: Optional[str] = None,
                                 skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get path execution waypoints with optional filtering"""
    query = db.query(PathExecutionWaypoint)
    if execution_id:
        query = query.filter(PathExecutionWaypoint.execution_id == execution_id)
    if waypoint_id:
        query = query.filter(PathExecutionWaypoint.waypoint_id == waypoint_id)
    
    execution_waypoints = query.order_by(PathExecutionWaypoint.visited_at.desc()).offset(skip).limit(limit).all()
    return execution_waypoints

@router.get("/path-executions/{execution_id}/waypoints", response_model=List[PathExecutionWaypointResponse])
async def get_execution_waypoints_by_execution(execution_id: str, db: Session = Depends(get_db)):
    """Get all waypoint visits for a specific path execution"""
    execution_waypoints = db.query(PathExecutionWaypoint).filter(PathExecutionWaypoint.execution_id == execution_id).order_by(PathExecutionWaypoint.visited_at).all()
    return execution_waypoints

@router.post("/path-executions/{execution_id}/waypoints/{waypoint_id}/visit")
async def record_waypoint_visit(execution_id: str, waypoint_id: str, 
                               inspection_completed: bool = False, issues_found: int = 0,
                               photos_taken: int = 0, notes: Optional[str] = None,
                               db: Session = Depends(get_db)):
    """Record a waypoint visit during path execution"""
    # Check if visit already exists
    existing_visit = db.query(PathExecutionWaypoint).filter(
        PathExecutionWaypoint.execution_id == execution_id,
        PathExecutionWaypoint.waypoint_id == waypoint_id
    ).first()
    
    if existing_visit:
        # Update existing visit
        existing_visit.visited_at = func.current_timestamp()
        existing_visit.inspection_completed = inspection_completed
        existing_visit.issues_found = issues_found
        existing_visit.photos_taken = photos_taken
        existing_visit.notes = notes
        db.commit()
        return {"message": "Waypoint visit updated successfully"}
    else:
        # Create new visit record
        new_visit = PathExecutionWaypoint(
            execution_id=execution_id,
            waypoint_id=waypoint_id,
            visited_at=func.current_timestamp(),
            inspection_completed=inspection_completed,
            issues_found=issues_found,
            photos_taken=photos_taken,
            notes=notes
        )
        
        db.add(new_visit)
        
        # Update execution progress
        execution = db.query(PathExecution).filter(PathExecution.id == execution_id).first()
        if execution:
            execution.waypoints_visited += 1
            execution.issues_found += issues_found
            execution.photos_taken += photos_taken
            if execution.waypoints_total > 0:
                execution.completion_percentage = (execution.waypoints_visited / execution.waypoints_total) * 100
        
        db.commit()
        return {"message": "Waypoint visit recorded successfully"}

# PATH TEMPLATES ENDPOINTS
@router.get("/path-templates", response_model=List[PathTemplateResponse])
async def get_path_templates(template_type: Optional[str] = None, difficulty_level: Optional[str] = None,
                            is_public: Optional[bool] = None, skip: int = 0, limit: int = 100, 
                            db: Session = Depends(get_db)):
    """Get path templates with optional filtering"""
    query = db.query(PathTemplate).filter(PathTemplate.is_active == True)
    if template_type:
        query = query.filter(PathTemplate.template_type == template_type)
    if difficulty_level:
        query = query.filter(PathTemplate.difficulty_level == difficulty_level)
    if is_public is not None:
        query = query.filter(PathTemplate.is_public == is_public)
    
    templates = query.order_by(PathTemplate.usage_count.desc()).offset(skip).limit(limit).all()
    return templates

@router.post("/path-templates", response_model=PathTemplateResponse)
async def create_path_template(template_data: PathTemplateCreateRequest, current_user_id: str = "system", db: Session = Depends(get_db)):
    """Create a new path template"""
    new_template = PathTemplate(
        template_name=template_data.template_name,
        description=template_data.description,
        template_type=template_data.template_type,
        difficulty_level=template_data.difficulty_level,
        safety_level=template_data.safety_level,
        base_waypoint_count=template_data.base_waypoint_count,
        estimated_duration_minutes=template_data.estimated_duration_minutes,
        recommended_zones=template_data.recommended_zones,
        required_equipment=template_data.required_equipment,
        is_public=template_data.is_public,
        created_by=current_user_id  # TODO: Get from auth
    )
    
    db.add(new_template)
    db.commit()
    db.refresh(new_template)
    return new_template

@router.get("/path-templates/{template_id}", response_model=PathTemplateResponse)
async def get_path_template(template_id: str, db: Session = Depends(get_db)):
    """Get a specific path template by ID"""
    template = db.query(PathTemplate).filter(PathTemplate.id == template_id).first()
    if not template:
        raise HTTPException(status_code=404, detail="Path template not found")
    return template

@router.put("/path-templates/{template_id}", response_model=PathTemplateResponse)
async def update_path_template(template_id: str, template_data: PathTemplateCreateRequest, db: Session = Depends(get_db)):
    """Update an existing path template"""
    template = db.query(PathTemplate).filter(PathTemplate.id == template_id).first()
    if not template:
        raise HTTPException(status_code=404, detail="Path template not found")
    
    for field, value in template_data.dict(exclude_unset=True).items():
        setattr(template, field, value)
    
    db.commit()
    db.refresh(template)
    return template

@router.delete("/path-templates/{template_id}")
async def delete_path_template(template_id: str, db: Session = Depends(get_db)):
    """Delete (deactivate) a path template"""
    template = db.query(PathTemplate).filter(PathTemplate.id == template_id).first()
    if not template:
        raise HTTPException(status_code=404, detail="Path template not found")
    
    template.is_active = False
    db.commit()
    return {"message": "Path template deactivated successfully"}

# ANALYTICS AND REPORTING ENDPOINTS
@router.get("/path-analytics/summary")
async def get_path_analytics_summary(site_id: Optional[str] = None, days: int = 30, db: Session = Depends(get_db)):
    """Get path execution analytics summary"""
    from datetime import date, timedelta
    
    query = db.query(PathExecution)
    if site_id:
        query = query.join(InspectionPath).filter(InspectionPath.site_id == site_id)
    
    # Filter by date range
    end_date = date.today()
    start_date = end_date - timedelta(days=days)
    query = query.filter(PathExecution.started_at >= start_date)
    
    executions = query.all()
    
    if not executions:
        return {"message": "No execution data found for the specified period"}
    
    # Calculate summary metrics
    total_executions = len(executions)
    completed_executions = len([e for e in executions if e.is_completed])
    avg_completion_rate = sum(e.completion_percentage or 0 for e in executions) / total_executions
    avg_quality_score = sum(e.quality_score or 0 for e in executions) / total_executions
    total_issues = sum(e.issues_found for e in executions)
    avg_compliance = sum(e.compliance_score or 100 for e in executions) / total_executions
    
    return {
        "date_range": {"start": start_date, "end": end_date},
        "total_executions": total_executions,
        "completed_executions": completed_executions,
        "completion_success_rate": round((completed_executions / total_executions) * 100, 2) if total_executions > 0 else 0,
        "average_completion_percentage": round(avg_completion_rate, 2),
        "average_quality_score": round(avg_quality_score, 2),
        "total_issues_found": total_issues,
        "average_compliance_score": round(avg_compliance, 2)
    }