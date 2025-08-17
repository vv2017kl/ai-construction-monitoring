"""
Personnel & HR Management API Routes
Handles personnel attendance, safety scores, and department assignments
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_
from typing import List, Optional
from datetime import datetime, timedelta, date, time

from database import get_db
from models import (
    PersonnelAttendance, PersonnelSafetyScore, DepartmentAssignment,
    User, Site, AttendanceStatus, ShiftType, SafetyRating, 
    DepartmentType, TrendDirection
)

router = APIRouter(prefix="/api/personnel-hr", tags=["Personnel & HR Management"])

# PERSONNEL ATTENDANCE ENDPOINTS

@router.get("/attendance", response_model=List[dict])
def get_all_attendance(
    user_id: Optional[str] = Query(None, description="Filter by user ID"),
    site_id: Optional[str] = Query(None, description="Filter by site ID"),
    date_from: Optional[str] = Query(None, description="Filter from date (YYYY-MM-DD)"),
    date_to: Optional[str] = Query(None, description="Filter to date (YYYY-MM-DD)"),
    status: Optional[str] = Query(None, description="Filter by attendance status"),
    db: Session = Depends(get_db)
):
    """Get all personnel attendance records with optional filtering"""
    query = db.query(PersonnelAttendance)
    
    if user_id:
        query = query.filter(PersonnelAttendance.user_id == user_id)
    
    if site_id:
        query = query.filter(PersonnelAttendance.site_id == site_id)
    
    if date_from:
        try:
            from_date = datetime.strptime(date_from, "%Y-%m-%d").date()
            query = query.filter(PersonnelAttendance.attendance_date >= from_date)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date_from format. Use YYYY-MM-DD")
    
    if date_to:
        try:
            to_date = datetime.strptime(date_to, "%Y-%m-%d").date()
            query = query.filter(PersonnelAttendance.attendance_date <= to_date)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date_to format. Use YYYY-MM-DD")
    
    if status:
        try:
            status_enum = AttendanceStatus(status)
            query = query.filter(PersonnelAttendance.status == status_enum)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid status: {status}")
    
    attendance_records = query.order_by(PersonnelAttendance.attendance_date.desc()).all()
    return [
        {
            "id": str(a.id),
            "user_id": str(a.user_id),
            "site_id": str(a.site_id),
            "attendance_date": a.attendance_date.isoformat(),
            "shift_type": a.shift_type.value,
            "status": a.status.value,
            "scheduled_start": a.scheduled_start.isoformat(),
            "scheduled_end": a.scheduled_end.isoformat(),
            "actual_start": a.actual_start.isoformat() if a.actual_start else None,
            "actual_end": a.actual_end.isoformat() if a.actual_end else None,
            "total_scheduled_hours": float(a.total_scheduled_hours),
            "total_actual_hours": float(a.total_actual_hours) if a.total_actual_hours else None,
            "overtime_hours": float(a.overtime_hours),
            "punctuality_score": float(a.punctuality_score) if a.punctuality_score else None,
            "created_at": a.created_at.isoformat()
        }
        for a in attendance_records
    ]

@router.post("/attendance", response_model=dict)
def create_attendance(
    user_id: str = Query(..., description="User ID"),
    site_id: str = Query(..., description="Site ID"),
    attendance_date: str = Query(..., description="Attendance date (YYYY-MM-DD)"),
    shift_type: str = Query(..., description="Shift type"),
    scheduled_start: str = Query(..., description="Scheduled start time (HH:MM:SS)"),
    scheduled_end: str = Query(..., description="Scheduled end time (HH:MM:SS)"),
    total_scheduled_hours: float = Query(..., description="Total scheduled hours"),
    status: str = Query("present", description="Attendance status"),
    db: Session = Depends(get_db)
):
    """Create a new attendance record"""
    # Verify user and site exist
    user = db.query(User).filter(User.id == user_id).first()
    site = db.query(Site).filter(Site.id == site_id).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    
    # Parse dates and times
    try:
        att_date = datetime.strptime(attendance_date, "%Y-%m-%d").date()
        start_time = datetime.strptime(scheduled_start, "%H:%M:%S").time()
        end_time = datetime.strptime(scheduled_end, "%H:%M:%S").time()
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date/time format")
    
    db_attendance = PersonnelAttendance(
        user_id=user_id,
        site_id=site_id,
        attendance_date=att_date,
        shift_type=ShiftType(shift_type),
        scheduled_start=start_time,
        scheduled_end=end_time,
        total_scheduled_hours=total_scheduled_hours,
        status=AttendanceStatus(status)
    )
    
    db.add(db_attendance)
    db.commit()
    db.refresh(db_attendance)
    
    return {
        "id": str(db_attendance.id),
        "attendance_date": db_attendance.attendance_date.isoformat(),
        "status": db_attendance.status.value,
        "created_at": db_attendance.created_at.isoformat()
    }

# PERSONNEL SAFETY SCORES ENDPOINTS

@router.get("/safety-scores", response_model=List[dict])
def get_all_safety_scores(
    user_id: Optional[str] = Query(None, description="Filter by user ID"),
    site_id: Optional[str] = Query(None, description="Filter by site ID"),
    safety_rating: Optional[str] = Query(None, description="Filter by safety rating"),
    is_current: Optional[bool] = Query(None, description="Filter by current scores"),
    db: Session = Depends(get_db)
):
    """Get all personnel safety scores with optional filtering"""
    query = db.query(PersonnelSafetyScore)
    
    if user_id:
        query = query.filter(PersonnelSafetyScore.user_id == user_id)
    
    if site_id:
        query = query.filter(PersonnelSafetyScore.site_id == site_id)
    
    if safety_rating:
        try:
            rating_enum = SafetyRating(safety_rating)
            query = query.filter(PersonnelSafetyScore.safety_rating == rating_enum)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid safety rating: {safety_rating}")
    
    if is_current is not None:
        query = query.filter(PersonnelSafetyScore.is_current == is_current)
    
    scores = query.order_by(PersonnelSafetyScore.evaluation_date.desc()).all()
    return [
        {
            "id": str(s.id),
            "user_id": str(s.user_id),
            "site_id": str(s.site_id),
            "evaluation_date": s.evaluation_date.isoformat(),
            "overall_safety_score": float(s.overall_safety_score),
            "safety_rating": s.safety_rating.value,
            "compliance_score": float(s.compliance_score) if s.compliance_score else None,
            "training_score": float(s.training_score) if s.training_score else None,
            "incident_count": s.incident_count,
            "near_miss_reports": s.near_miss_reports,
            "safety_violations": s.safety_violations,
            "is_current": s.is_current,
            "trend_direction": s.trend_direction.value if s.trend_direction else None,
            "created_at": s.created_at.isoformat()
        }
        for s in scores
    ]

@router.post("/safety-scores", response_model=dict)
def create_safety_score(
    user_id: str = Query(..., description="User ID"),
    site_id: str = Query(..., description="Site ID"),
    evaluation_date: str = Query(..., description="Evaluation date (YYYY-MM-DD)"),
    evaluation_period_start: str = Query(..., description="Period start (YYYY-MM-DD)"),
    evaluation_period_end: str = Query(..., description="Period end (YYYY-MM-DD)"),
    overall_safety_score: float = Query(..., description="Overall safety score (0-100)"),
    safety_rating: str = Query(..., description="Safety rating"),
    db: Session = Depends(get_db)
):
    """Create a new personnel safety score"""
    # Verify user and site exist
    user = db.query(User).filter(User.id == user_id).first()
    site = db.query(Site).filter(Site.id == site_id).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    
    # Parse dates
    try:
        eval_date = datetime.strptime(evaluation_date, "%Y-%m-%d").date()
        period_start = datetime.strptime(evaluation_period_start, "%Y-%m-%d").date()
        period_end = datetime.strptime(evaluation_period_end, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")
    
    db_score = PersonnelSafetyScore(
        user_id=user_id,
        site_id=site_id,
        evaluation_date=eval_date,
        evaluation_period_start=period_start,
        evaluation_period_end=period_end,
        overall_safety_score=overall_safety_score,
        safety_rating=SafetyRating(safety_rating)
    )
    
    db.add(db_score)
    db.commit()
    db.refresh(db_score)
    
    return {
        "id": str(db_score.id),
        "overall_safety_score": float(db_score.overall_safety_score),
        "safety_rating": db_score.safety_rating.value,
        "created_at": db_score.created_at.isoformat()
    }

# DEPARTMENT ASSIGNMENTS ENDPOINTS

@router.get("/department-assignments", response_model=List[dict])
def get_all_assignments(
    user_id: Optional[str] = Query(None, description="Filter by user ID"),
    site_id: Optional[str] = Query(None, description="Filter by site ID"),
    department_type: Optional[str] = Query(None, description="Filter by department type"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    db: Session = Depends(get_db)
):
    """Get all department assignments with optional filtering"""
    query = db.query(DepartmentAssignment)
    
    if user_id:
        query = query.filter(DepartmentAssignment.user_id == user_id)
    
    if site_id:
        query = query.filter(DepartmentAssignment.site_id == site_id)
    
    if department_type:
        try:
            dept_enum = DepartmentType(department_type)
            query = query.filter(DepartmentAssignment.department_type == dept_enum)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid department type: {department_type}")
    
    if is_active is not None:
        query = query.filter(DepartmentAssignment.is_active == is_active)
    
    assignments = query.order_by(DepartmentAssignment.assignment_start_date.desc()).all()
    return [
        {
            "id": str(a.id),
            "user_id": str(a.user_id),
            "site_id": str(a.site_id),
            "department_name": a.department_name,
            "department_type": a.department_type.value,
            "job_title": a.job_title,
            "assignment_start_date": a.assignment_start_date.isoformat(),
            "assignment_end_date": a.assignment_end_date.isoformat() if a.assignment_end_date else None,
            "is_active": a.is_active,
            "supervisor_id": str(a.supervisor_id) if a.supervisor_id else None,
            "reporting_level": a.reporting_level,
            "team_lead_flag": a.team_lead_flag,
            "performance_rating": float(a.performance_rating) if a.performance_rating else None,
            "created_at": a.created_at.isoformat()
        }
        for a in assignments
    ]

@router.post("/department-assignments", response_model=dict)
def create_assignment(
    user_id: str = Query(..., description="User ID"),
    site_id: str = Query(..., description="Site ID"),
    department_name: str = Query(..., description="Department name"),
    department_type: str = Query(..., description="Department type"),
    job_title: str = Query(..., description="Job title"),
    assignment_start_date: str = Query(..., description="Start date (YYYY-MM-DD)"),
    created_by: str = Query(..., description="Creator user ID"),
    db: Session = Depends(get_db)
):
    """Create a new department assignment"""
    # Verify user, site, and creator exist
    user = db.query(User).filter(User.id == user_id).first()
    site = db.query(Site).filter(Site.id == site_id).first()
    creator = db.query(User).filter(User.id == created_by).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    if not creator:
        raise HTTPException(status_code=404, detail="Creator not found")
    
    # Parse start date
    try:
        start_date = datetime.strptime(assignment_start_date, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid start date format. Use YYYY-MM-DD")
    
    db_assignment = DepartmentAssignment(
        user_id=user_id,
        site_id=site_id,
        department_name=department_name,
        department_type=DepartmentType(department_type),
        job_title=job_title,
        assignment_start_date=start_date,
        created_by=created_by
    )
    
    db.add(db_assignment)
    db.commit()
    db.refresh(db_assignment)
    
    return {
        "id": str(db_assignment.id),
        "department_name": db_assignment.department_name,
        "job_title": db_assignment.job_title,
        "assignment_start_date": db_assignment.assignment_start_date.isoformat(),
        "created_at": db_assignment.created_at.isoformat()
    }

@router.get("/attendance/analytics/summary")
def get_attendance_analytics(
    site_id: Optional[str] = Query(None, description="Filter by site ID"),
    days: Optional[int] = Query(30, description="Days back for analysis"),
    db: Session = Depends(get_db)
):
    """Get attendance analytics summary"""
    query = db.query(PersonnelAttendance)
    
    if site_id:
        query = query.filter(PersonnelAttendance.site_id == site_id)
    
    if days:
        cutoff_date = datetime.now() - timedelta(days=days)
        query = query.filter(PersonnelAttendance.attendance_date >= cutoff_date.date())
    
    total_records = query.count()
    present_count = query.filter(PersonnelAttendance.status == AttendanceStatus.present).count()
    late_count = query.filter(PersonnelAttendance.status == AttendanceStatus.late).count()
    absent_count = query.filter(PersonnelAttendance.status == AttendanceStatus.absent).count()
    
    avg_punctuality = query.with_entities(func.avg(PersonnelAttendance.punctuality_score)).scalar() or 0
    
    return {
        "total_attendance_records": total_records,
        "present_count": present_count,
        "late_count": late_count,
        "absent_count": absent_count,
        "attendance_rate": (present_count / total_records * 100) if total_records > 0 else 0,
        "average_punctuality_score": float(avg_punctuality),
        "analysis_period_days": days
    }