"""
Street View Comparison & Analysis API Routes
Handles street view comparisons, sessions, detected changes, comparison locations, and analysis metrics
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_
from typing import List, Optional
from datetime import datetime, timedelta, date, time

from database import get_db
from models import (
    StreetViewComparison, StreetViewSession, DetectedChange, 
    ComparisonLocation, ComparisonAnalysisMetric, User, Site, Camera,
    ComparisonType, AnalysisStatus, RecordingQuality, ChangeType, 
    SeverityLevel, ZoneType, MonitoringPriority, ReviewStatus, 
    MetricType, TrendDirection
)
from schemas import (
    StreetViewComparisonResponse, StreetViewComparisonCreateRequest,
    StreetViewSessionResponse, StreetViewSessionCreateRequest,
    DetectedChangeResponse, DetectedChangeCreateRequest,
    ComparisonLocationResponse, ComparisonLocationCreateRequest,
    ComparisonAnalysisMetricResponse, ComparisonAnalysisMetricCreateRequest
)

router = APIRouter(prefix="/street-view", tags=["Street View Comparison & Analysis"])

# STREET VIEW COMPARISONS ENDPOINTS

@router.get("/comparisons", response_model=List[StreetViewComparisonResponse])
def get_all_comparisons(
    site_id: Optional[str] = Query(None, description="Filter by site ID"),
    comparison_type: Optional[str] = Query(None, description="Filter by comparison type"),
    analysis_status: Optional[str] = Query(None, description="Filter by analysis status"),
    days: Optional[int] = Query(None, description="Filter by days back"),
    db: Session = Depends(get_db)
):
    """Get all street view comparisons with optional filtering"""
    query = db.query(StreetViewComparison)
    
    if site_id:
        query = query.filter(StreetViewComparison.site_id == site_id)
    
    if comparison_type:
        try:
            type_enum = ComparisonType(comparison_type)
            query = query.filter(StreetViewComparison.comparison_type == type_enum)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid comparison type: {comparison_type}")
    
    if analysis_status:
        try:
            status_enum = AnalysisStatus(analysis_status)
            query = query.filter(StreetViewComparison.analysis_status == status_enum)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid analysis status: {analysis_status}")
    
    if days:
        cutoff_date = datetime.now() - timedelta(days=days)
        query = query.filter(StreetViewComparison.created_at >= cutoff_date)
    
    return query.order_by(StreetViewComparison.created_at.desc()).all()

@router.post("/comparisons", response_model=StreetViewComparisonResponse)
def create_comparison(
    comparison: StreetViewComparisonCreateRequest,
    created_by: str = Query(..., description="User ID creating the comparison"),
    db: Session = Depends(get_db)
):
    """Create a new street view comparison"""
    # Verify user exists
    user = db.query(User).filter(User.id == created_by).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Verify site exists
    site = db.query(Site).filter(Site.id == comparison.site_id).first()
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    
    # Verify sessions exist
    session_before = db.query(StreetViewSession).filter(StreetViewSession.id == comparison.session_before_id).first()
    session_after = db.query(StreetViewSession).filter(StreetViewSession.id == comparison.session_after_id).first()
    
    if not session_before:
        raise HTTPException(status_code=404, detail="Before session not found")
    if not session_after:
        raise HTTPException(status_code=404, detail="After session not found")
    
    # Validate comparison type
    try:
        ComparisonType(comparison.comparison_type)
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid comparison type: {comparison.comparison_type}")
    
    db_comparison = StreetViewComparison(
        session_before_id=comparison.session_before_id,
        session_after_id=comparison.session_after_id,
        site_id=comparison.site_id,
        location_zone=comparison.location_zone,
        comparison_type=comparison.comparison_type,
        timespan_days=comparison.timespan_days,
        created_by=created_by
    )
    
    db.add(db_comparison)
    db.commit()
    db.refresh(db_comparison)
    
    return db_comparison

@router.get("/comparisons/{comparison_id}", response_model=StreetViewComparisonResponse)
def get_comparison(comparison_id: str, db: Session = Depends(get_db)):
    """Get a specific street view comparison"""
    comparison = db.query(StreetViewComparison).filter(StreetViewComparison.id == comparison_id).first()
    if not comparison:
        raise HTTPException(status_code=404, detail="Comparison not found")
    return comparison

@router.put("/comparisons/{comparison_id}", response_model=StreetViewComparisonResponse)
def update_comparison(
    comparison_id: str,
    comparison_data: dict,
    db: Session = Depends(get_db)
):
    """Update a street view comparison (typically for analysis results)"""
    comparison = db.query(StreetViewComparison).filter(StreetViewComparison.id == comparison_id).first()
    if not comparison:
        raise HTTPException(status_code=404, detail="Comparison not found")
    
    # Update processing completion time if status changed to completed
    if "analysis_status" in comparison_data and comparison_data["analysis_status"] == "completed":
        comparison_data["processing_completed_at"] = datetime.now()
    
    for key, value in comparison_data.items():
        if hasattr(comparison, key):
            setattr(comparison, key, value)
    
    db.commit()
    db.refresh(comparison)
    return comparison

@router.delete("/comparisons/{comparison_id}")
def delete_comparison(comparison_id: str, db: Session = Depends(get_db)):
    """Delete a street view comparison"""
    comparison = db.query(StreetViewComparison).filter(StreetViewComparison.id == comparison_id).first()
    if not comparison:
        raise HTTPException(status_code=404, detail="Comparison not found")
    
    db.delete(comparison)
    db.commit()
    return {"message": "Comparison deleted successfully"}

@router.get("/comparisons/analytics/summary")
def get_comparison_analytics_summary(
    site_id: Optional[str] = Query(None, description="Filter by site ID"),
    days: Optional[int] = Query(None, description="Analytics period in days"),
    db: Session = Depends(get_db)
):
    """Get street view comparison analytics summary"""
    query = db.query(StreetViewComparison)
    
    if site_id:
        query = query.filter(StreetViewComparison.site_id == site_id)
    
    if days:
        cutoff_date = datetime.now() - timedelta(days=days)
        query = query.filter(StreetViewComparison.created_at >= cutoff_date)
    
    total = query.count()
    completed = query.filter(StreetViewComparison.analysis_status == AnalysisStatus.completed).count()
    pending = query.filter(StreetViewComparison.analysis_status == AnalysisStatus.pending).count()
    failed = query.filter(StreetViewComparison.analysis_status == AnalysisStatus.failed).count()
    
    avg_progress = query.with_entities(func.avg(StreetViewComparison.overall_progress_percentage)).scalar() or 0
    avg_processing_time = query.filter(StreetViewComparison.processing_time_seconds.isnot(None))\
        .with_entities(func.avg(StreetViewComparison.processing_time_seconds)).scalar() or 0
    
    return {
        "total_comparisons": total,
        "completed_comparisons": completed,
        "pending_comparisons": pending,
        "failed_comparisons": failed,
        "completion_rate": (completed / total * 100) if total > 0 else 0,
        "average_progress_percentage": float(avg_progress),
        "average_processing_time_seconds": float(avg_processing_time),
        "period_days": days or "all_time"
    }

# STREET VIEW SESSIONS ENDPOINTS

@router.get("/sessions", response_model=List[StreetViewSessionResponse])
def get_all_sessions(
    site_id: Optional[str] = Query(None, description="Filter by site ID"),
    camera_id: Optional[str] = Query(None, description="Filter by camera ID"),
    recording_quality: Optional[str] = Query(None, description="Filter by recording quality"),
    date_from: Optional[str] = Query(None, description="Filter from date (YYYY-MM-DD)"),
    date_to: Optional[str] = Query(None, description="Filter to date (YYYY-MM-DD)"),
    db: Session = Depends(get_db)
):
    """Get all street view sessions with optional filtering"""
    query = db.query(StreetViewSession)
    
    if site_id:
        query = query.filter(StreetViewSession.site_id == site_id)
    
    if camera_id:
        query = query.filter(StreetViewSession.camera_id == camera_id)
    
    if recording_quality:
        try:
            quality_enum = RecordingQuality(recording_quality)
            query = query.filter(StreetViewSession.recording_quality == quality_enum)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid recording quality: {recording_quality}")
    
    if date_from:
        try:
            from_date = datetime.strptime(date_from, "%Y-%m-%d").date()
            query = query.filter(StreetViewSession.session_date >= from_date)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date_from format. Use YYYY-MM-DD")
    
    if date_to:
        try:
            to_date = datetime.strptime(date_to, "%Y-%m-%d").date()
            query = query.filter(StreetViewSession.session_date <= to_date)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date_to format. Use YYYY-MM-DD")
    
    return query.order_by(StreetViewSession.session_date.desc(), StreetViewSession.session_time.desc()).all()

@router.post("/sessions", response_model=StreetViewSessionResponse)
def create_session(
    session: StreetViewSessionCreateRequest,
    created_by: str = Query(..., description="User ID creating the session"),
    db: Session = Depends(get_db)
):
    """Create a new street view session"""
    # Verify user exists
    user = db.query(User).filter(User.id == created_by).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Verify site and camera exist
    site = db.query(Site).filter(Site.id == session.site_id).first()
    camera = db.query(Camera).filter(Camera.id == session.camera_id).first()
    
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    if not camera:
        raise HTTPException(status_code=404, detail="Camera not found")
    
    # Validate recording quality
    if session.recording_quality:
        try:
            RecordingQuality(session.recording_quality)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid recording quality: {session.recording_quality}")
    
    # Parse date and time
    try:
        session_date = datetime.strptime(session.session_date, "%Y-%m-%d").date()
        session_time = datetime.strptime(session.session_time, "%H:%M:%S").time()
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date/time format. Use YYYY-MM-DD for date and HH:MM:SS for time")
    
    db_session = StreetViewSession(
        site_id=session.site_id,
        camera_id=session.camera_id,
        session_label=session.session_label,
        session_date=session_date,
        session_time=session_time,
        location_coordinates_x=session.location_coordinates_x,
        location_coordinates_y=session.location_coordinates_y,
        heading_degrees=session.heading_degrees,
        weather_conditions=session.weather_conditions,
        recording_quality=session.recording_quality or RecordingQuality.high,
        file_path=session.file_path,
        file_size_mb=session.file_size_mb,
        duration_seconds=session.duration_seconds,
        created_by=created_by
    )
    
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    
    return db_session

@router.get("/sessions/{session_id}", response_model=StreetViewSessionResponse)
def get_session(session_id: str, db: Session = Depends(get_db)):
    """Get a specific street view session"""
    session = db.query(StreetViewSession).filter(StreetViewSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session

@router.put("/sessions/{session_id}", response_model=StreetViewSessionResponse)
def update_session(
    session_id: str,
    session_data: dict,
    db: Session = Depends(get_db)
):
    """Update a street view session"""
    session = db.query(StreetViewSession).filter(StreetViewSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    for key, value in session_data.items():
        if hasattr(session, key):
            setattr(session, key, value)
    
    db.commit()
    db.refresh(session)
    return session

@router.delete("/sessions/{session_id}")
def delete_session(session_id: str, db: Session = Depends(get_db)):
    """Delete a street view session"""
    session = db.query(StreetViewSession).filter(StreetViewSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    db.delete(session)
    db.commit()
    return {"message": "Session deleted successfully"}

# DETECTED CHANGES ENDPOINTS

@router.get("/changes", response_model=List[DetectedChangeResponse])
def get_all_changes(
    comparison_id: Optional[str] = Query(None, description="Filter by comparison ID"),
    change_type: Optional[str] = Query(None, description="Filter by change type"),
    severity: Optional[str] = Query(None, description="Filter by severity"),
    review_status: Optional[str] = Query(None, description="Filter by review status"),
    confidence_min: Optional[float] = Query(None, description="Minimum confidence percentage"),
    db: Session = Depends(get_db)
):
    """Get all detected changes with optional filtering"""
    query = db.query(DetectedChange)
    
    if comparison_id:
        query = query.filter(DetectedChange.comparison_id == comparison_id)
    
    if change_type:
        try:
            type_enum = ChangeType(change_type)
            query = query.filter(DetectedChange.change_type == type_enum)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid change type: {change_type}")
    
    if severity:
        try:
            severity_enum = SeverityLevel(severity)
            query = query.filter(DetectedChange.severity == severity_enum)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid severity: {severity}")
    
    if review_status:
        try:
            status_enum = ReviewStatus(review_status)
            query = query.filter(DetectedChange.review_status == status_enum)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid review status: {review_status}")
    
    if confidence_min:
        query = query.filter(DetectedChange.confidence_percentage >= confidence_min)
    
    return query.order_by(DetectedChange.created_at.desc()).all()

@router.post("/changes", response_model=DetectedChangeResponse)
def create_change(
    change: DetectedChangeCreateRequest,
    db: Session = Depends(get_db)
):
    """Create a new detected change"""
    # Verify comparison exists
    comparison = db.query(StreetViewComparison).filter(StreetViewComparison.id == change.comparison_id).first()
    if not comparison:
        raise HTTPException(status_code=404, detail="Comparison not found")
    
    # Validate enums
    try:
        ChangeType(change.change_type)
        SeverityLevel(change.severity)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid enum value: {str(e)}")
    
    db_change = DetectedChange(**change.model_dump())
    db.add(db_change)
    db.commit()
    db.refresh(db_change)
    
    return db_change

@router.get("/changes/{change_id}", response_model=DetectedChangeResponse)
def get_change(change_id: str, db: Session = Depends(get_db)):
    """Get a specific detected change"""
    change = db.query(DetectedChange).filter(DetectedChange.id == change_id).first()
    if not change:
        raise HTTPException(status_code=404, detail="Change not found")
    return change

@router.put("/changes/{change_id}", response_model=DetectedChangeResponse)
def update_change(
    change_id: str,
    change_data: dict,
    reviewed_by: Optional[str] = Query(None, description="User ID reviewing the change"),
    db: Session = Depends(get_db)
):
    """Update a detected change (typically for review)"""
    change = db.query(DetectedChange).filter(DetectedChange.id == change_id).first()
    if not change:
        raise HTTPException(status_code=404, detail="Change not found")
    
    # If review status is being updated, set reviewed_by
    if reviewed_by and ("review_status" in change_data or "review_notes" in change_data):
        user = db.query(User).filter(User.id == reviewed_by).first()
        if not user:
            raise HTTPException(status_code=404, detail="Reviewer not found")
        change_data["reviewed_by"] = reviewed_by
    
    for key, value in change_data.items():
        if hasattr(change, key):
            setattr(change, key, value)
    
    db.commit()
    db.refresh(change)
    return change

# COMPARISON LOCATIONS ENDPOINTS

@router.get("/locations", response_model=List[ComparisonLocationResponse])
def get_all_locations(
    site_id: Optional[str] = Query(None, description="Filter by site ID"),
    zone_type: Optional[str] = Query(None, description="Filter by zone type"),
    monitoring_priority: Optional[str] = Query(None, description="Filter by monitoring priority"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    db: Session = Depends(get_db)
):
    """Get all comparison locations with optional filtering"""
    query = db.query(ComparisonLocation)
    
    if site_id:
        query = query.filter(ComparisonLocation.site_id == site_id)
    
    if zone_type:
        try:
            type_enum = ZoneType(zone_type)
            query = query.filter(ComparisonLocation.zone_type == type_enum)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid zone type: {zone_type}")
    
    if monitoring_priority:
        try:
            priority_enum = MonitoringPriority(monitoring_priority)
            query = query.filter(ComparisonLocation.monitoring_priority == priority_enum)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid monitoring priority: {monitoring_priority}")
    
    if is_active is not None:
        query = query.filter(ComparisonLocation.is_active == is_active)
    
    return query.order_by(ComparisonLocation.location_name).all()

@router.post("/locations", response_model=ComparisonLocationResponse)
def create_location(
    location: ComparisonLocationCreateRequest,
    db: Session = Depends(get_db)
):
    """Create a new comparison location"""
    # Verify site exists
    site = db.query(Site).filter(Site.id == location.site_id).first()
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    
    # Validate enums
    try:
        ZoneType(location.zone_type)
        if location.monitoring_priority:
            MonitoringPriority(location.monitoring_priority)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid enum value: {str(e)}")
    
    db_location = ComparisonLocation(**location.model_dump())
    db.add(db_location)
    db.commit()
    db.refresh(db_location)
    
    return db_location

@router.get("/locations/{location_id}", response_model=ComparisonLocationResponse)
def get_location(location_id: str, db: Session = Depends(get_db)):
    """Get a specific comparison location"""
    location = db.query(ComparisonLocation).filter(ComparisonLocation.id == location_id).first()
    if not location:
        raise HTTPException(status_code=404, detail="Location not found")
    return location

@router.put("/locations/{location_id}", response_model=ComparisonLocationResponse)
def update_location(
    location_id: str,
    location_data: dict,
    db: Session = Depends(get_db)
):
    """Update a comparison location"""
    location = db.query(ComparisonLocation).filter(ComparisonLocation.id == location_id).first()
    if not location:
        raise HTTPException(status_code=404, detail="Location not found")
    
    for key, value in location_data.items():
        if hasattr(location, key):
            setattr(location, key, value)
    
    db.commit()
    db.refresh(location)
    return location

@router.delete("/locations/{location_id}")
def delete_location(location_id: str, db: Session = Depends(get_db)):
    """Delete a comparison location"""
    location = db.query(ComparisonLocation).filter(ComparisonLocation.id == location_id).first()
    if not location:
        raise HTTPException(status_code=404, detail="Location not found")
    
    db.delete(location)
    db.commit()
    return {"message": "Location deleted successfully"}

# COMPARISON ANALYSIS METRICS ENDPOINTS

@router.get("/metrics", response_model=List[ComparisonAnalysisMetricResponse])
def get_all_metrics(
    comparison_id: Optional[str] = Query(None, description="Filter by comparison ID"),
    metric_type: Optional[str] = Query(None, description="Filter by metric type"),
    trend_direction: Optional[str] = Query(None, description="Filter by trend direction"),
    db: Session = Depends(get_db)
):
    """Get all comparison analysis metrics with optional filtering"""
    query = db.query(ComparisonAnalysisMetric)
    
    if comparison_id:
        query = query.filter(ComparisonAnalysisMetric.comparison_id == comparison_id)
    
    if metric_type:
        try:
            type_enum = MetricType(metric_type)
            query = query.filter(ComparisonAnalysisMetric.metric_type == type_enum)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid metric type: {metric_type}")
    
    if trend_direction:
        try:
            trend_enum = TrendDirection(trend_direction)
            query = query.filter(ComparisonAnalysisMetric.trend_direction == trend_enum)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid trend direction: {trend_direction}")
    
    return query.order_by(ComparisonAnalysisMetric.created_at.desc()).all()

@router.post("/metrics", response_model=ComparisonAnalysisMetricResponse)
def create_metric(
    metric: ComparisonAnalysisMetricCreateRequest,
    db: Session = Depends(get_db)
):
    """Create a new comparison analysis metric"""
    # Verify comparison exists
    comparison = db.query(StreetViewComparison).filter(StreetViewComparison.id == metric.comparison_id).first()
    if not comparison:
        raise HTTPException(status_code=404, detail="Comparison not found")
    
    # Validate enums
    try:
        MetricType(metric.metric_type)
        if metric.trend_direction:
            TrendDirection(metric.trend_direction)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid enum value: {str(e)}")
    
    db_metric = ComparisonAnalysisMetric(**metric.model_dump())
    db.add(db_metric)
    db.commit()
    db.refresh(db_metric)
    
    return db_metric

@router.get("/metrics/{metric_id}", response_model=ComparisonAnalysisMetricResponse)
def get_metric(metric_id: str, db: Session = Depends(get_db)):
    """Get a specific comparison analysis metric"""
    metric = db.query(ComparisonAnalysisMetric).filter(ComparisonAnalysisMetric.id == metric_id).first()
    if not metric:
        raise HTTPException(status_code=404, detail="Metric not found")
    return metric

@router.get("/analytics/metrics-summary")
def get_metrics_analytics_summary(
    comparison_id: Optional[str] = Query(None, description="Filter by comparison ID"),
    db: Session = Depends(get_db)
):
    """Get analysis metrics summary analytics"""
    query = db.query(ComparisonAnalysisMetric)
    
    if comparison_id:
        query = query.filter(ComparisonAnalysisMetric.comparison_id == comparison_id)
    
    total_metrics = query.count()
    
    by_type = query.with_entities(
        ComparisonAnalysisMetric.metric_type,
        func.count(ComparisonAnalysisMetric.id).label('count'),
        func.avg(ComparisonAnalysisMetric.metric_value).label('avg_value'),
        func.avg(ComparisonAnalysisMetric.improvement_percentage).label('avg_improvement')
    ).group_by(ComparisonAnalysisMetric.metric_type).all()
    
    by_trend = query.filter(ComparisonAnalysisMetric.trend_direction.isnot(None))\
        .with_entities(
            ComparisonAnalysisMetric.trend_direction,
            func.count(ComparisonAnalysisMetric.id).label('count')
        ).group_by(ComparisonAnalysisMetric.trend_direction).all()
    
    return {
        "total_metrics": total_metrics,
        "by_type": [
            {
                "metric_type": item.metric_type.value,
                "count": item.count,
                "average_value": float(item.avg_value or 0),
                "average_improvement": float(item.avg_improvement or 0)
            }
            for item in by_type
        ],
        "by_trend": [
            {
                "trend_direction": item.trend_direction.value,
                "count": item.count
            }
            for item in by_trend
        ]
    }