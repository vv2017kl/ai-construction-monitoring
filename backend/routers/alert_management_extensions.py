"""
Alert Management Extensions API Routes
Handles alert comments, evidence, assignments, safety metrics, and activity feed
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_
from typing import List, Optional
from datetime import datetime, timedelta

from database import get_db
from models import (
    AlertComment, AlertEvidence, AlertAssignment, SafetyMetric, ActivityFeed,
    User, Alert, Site, CommentType, VisibilityLevel, EvidenceType, 
    AssignmentStatus, SeverityLevel, AggregationPeriod, TrendDirection
)

router = APIRouter(prefix="/api/alert-extensions", tags=["Alert Management Extensions"])

# ALERT COMMENTS ENDPOINTS

@router.get("/comments", response_model=List[dict])
def get_all_comments(
    alert_id: Optional[str] = Query(None, description="Filter by alert ID"),
    author_id: Optional[str] = Query(None, description="Filter by author ID"),
    visibility_level: Optional[str] = Query(None, description="Filter by visibility level"),
    db: Session = Depends(get_db)
):
    """Get all alert comments with optional filtering"""
    query = db.query(AlertComment)
    
    if alert_id:
        query = query.filter(AlertComment.alert_id == alert_id)
    
    if author_id:
        query = query.filter(AlertComment.author_id == author_id)
    
    if visibility_level:
        try:
            vis_enum = VisibilityLevel(visibility_level)
            query = query.filter(AlertComment.visibility_level == vis_enum)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid visibility level: {visibility_level}")
    
    comments = query.order_by(AlertComment.created_at.desc()).all()
    return [
        {
            "id": str(c.id),
            "alert_id": str(c.alert_id),
            "author_id": str(c.author_id),
            "comment_text": c.comment_text,
            "comment_type": c.comment_type.value,
            "visibility_level": c.visibility_level.value,
            "is_internal": c.is_internal,
            "created_at": c.created_at.isoformat()
        }
        for c in comments
    ]

@router.post("/comments", response_model=dict)
def create_comment(
    alert_id: str = Query(..., description="Alert ID"),
    author_id: str = Query(..., description="Author user ID"),
    comment_text: str = Query(..., description="Comment text"),
    comment_type: Optional[str] = Query("note", description="Comment type"),
    visibility_level: Optional[str] = Query("team", description="Visibility level"),
    is_internal: Optional[bool] = Query(False, description="Internal comment flag"),
    db: Session = Depends(get_db)
):
    """Create a new alert comment"""
    # Verify alert and author exist
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    author = db.query(User).filter(User.id == author_id).first()
    
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    
    db_comment = AlertComment(
        alert_id=alert_id,
        author_id=author_id,
        comment_text=comment_text,
        comment_type=CommentType(comment_type),
        visibility_level=VisibilityLevel(visibility_level),
        is_internal=is_internal
    )
    
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    
    return {
        "id": str(db_comment.id),
        "alert_id": str(db_comment.alert_id),
        "comment_text": db_comment.comment_text,
        "created_at": db_comment.created_at.isoformat()
    }

# ALERT EVIDENCE ENDPOINTS

@router.get("/evidence", response_model=List[dict])
def get_all_evidence(
    alert_id: Optional[str] = Query(None, description="Filter by alert ID"),
    evidence_type: Optional[str] = Query(None, description="Filter by evidence type"),
    db: Session = Depends(get_db)
):
    """Get all alert evidence with optional filtering"""
    query = db.query(AlertEvidence)
    
    if alert_id:
        query = query.filter(AlertEvidence.alert_id == alert_id)
    
    if evidence_type:
        try:
            type_enum = EvidenceType(evidence_type)
            query = query.filter(AlertEvidence.evidence_type == type_enum)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid evidence type: {evidence_type}")
    
    evidence = query.order_by(AlertEvidence.created_at.desc()).all()
    return [
        {
            "id": str(e.id),
            "alert_id": str(e.alert_id),
            "evidence_type": e.evidence_type.value,
            "file_name": e.file_name,
            "file_path": e.file_path,
            "collected_by": str(e.collected_by),
            "created_at": e.created_at.isoformat()
        }
        for e in evidence
    ]

@router.post("/evidence", response_model=dict)
def create_evidence(
    alert_id: str = Query(..., description="Alert ID"),
    evidence_type: str = Query(..., description="Evidence type"),
    file_name: str = Query(..., description="File name"),
    file_path: str = Query(..., description="File path"),
    collected_by: str = Query(..., description="Collector user ID"),
    db: Session = Depends(get_db)
):
    """Create new alert evidence"""
    # Verify alert and collector exist
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    collector = db.query(User).filter(User.id == collected_by).first()
    
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    if not collector:
        raise HTTPException(status_code=404, detail="Collector not found")
    
    db_evidence = AlertEvidence(
        alert_id=alert_id,
        source_type="manual_upload",
        evidence_type=EvidenceType(evidence_type),
        file_name=file_name,
        file_path=file_path,
        collected_by=collected_by
    )
    
    db.add(db_evidence)
    db.commit()
    db.refresh(db_evidence)
    
    return {
        "id": str(db_evidence.id),
        "alert_id": str(db_evidence.alert_id),
        "file_name": db_evidence.file_name,
        "created_at": db_evidence.created_at.isoformat()
    }

# SAFETY METRICS ENDPOINTS

@router.get("/safety-metrics", response_model=List[dict])
def get_all_safety_metrics(
    site_id: Optional[str] = Query(None, description="Filter by site ID"),
    metric_category: Optional[str] = Query(None, description="Filter by category"),
    db: Session = Depends(get_db)
):
    """Get all safety metrics with optional filtering"""
    query = db.query(SafetyMetric)
    
    if site_id:
        query = query.filter(SafetyMetric.site_id == site_id)
    
    if metric_category:
        query = query.filter(SafetyMetric.metric_category.ilike(f"%{metric_category}%"))
    
    metrics = query.order_by(SafetyMetric.measurement_date.desc()).all()
    return [
        {
            "id": str(m.id),
            "site_id": str(m.site_id),
            "metric_name": m.metric_name,
            "metric_category": m.metric_category,
            "measurement_date": m.measurement_date.isoformat(),
            "incident_count": m.incident_count,
            "compliance_score": float(m.compliance_score) if m.compliance_score else None,
            "created_at": m.created_at.isoformat()
        }
        for m in metrics
    ]

@router.post("/safety-metrics", response_model=dict)
def create_safety_metric(
    site_id: str = Query(..., description="Site ID"),
    metric_name: str = Query(..., description="Metric name"),
    metric_category: str = Query(..., description="Metric category"),
    measurement_date: str = Query(..., description="Measurement date (YYYY-MM-DD)"),
    measurement_period: str = Query(..., description="Measurement period"),
    created_by: str = Query(..., description="Creator user ID"),
    db: Session = Depends(get_db)
):
    """Create a new safety metric"""
    # Verify site and creator exist
    site = db.query(Site).filter(Site.id == site_id).first()
    creator = db.query(User).filter(User.id == created_by).first()
    
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    if not creator:
        raise HTTPException(status_code=404, detail="Creator not found")
    
    # Parse measurement date
    try:
        measure_date = datetime.strptime(measurement_date, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")
    
    db_metric = SafetyMetric(
        site_id=site_id,
        metric_name=metric_name,
        metric_category=metric_category,
        measurement_date=measure_date,
        measurement_period=AggregationPeriod(measurement_period),
        created_by=created_by
    )
    
    db.add(db_metric)
    db.commit()
    db.refresh(db_metric)
    
    return {
        "id": str(db_metric.id),
        "metric_name": db_metric.metric_name,
        "measurement_date": db_metric.measurement_date.isoformat(),
        "created_at": db_metric.created_at.isoformat()
    }

# ACTIVITY FEED ENDPOINTS

@router.get("/activity-feed", response_model=List[dict])
def get_activity_feed(
    site_id: Optional[str] = Query(None, description="Filter by site ID"),
    user_id: Optional[str] = Query(None, description="Filter by user ID"),
    activity_category: Optional[str] = Query(None, description="Filter by category"),
    limit: Optional[int] = Query(50, description="Limit results"),
    db: Session = Depends(get_db)
):
    """Get activity feed with optional filtering"""
    query = db.query(ActivityFeed)
    
    if site_id:
        query = query.filter(ActivityFeed.site_id == site_id)
    
    if user_id:
        query = query.filter(ActivityFeed.user_id == user_id)
    
    if activity_category:
        query = query.filter(ActivityFeed.activity_category == activity_category)
    
    activities = query.order_by(ActivityFeed.created_at.desc()).limit(limit).all()
    return [
        {
            "id": str(a.id),
            "site_id": str(a.site_id),
            "user_id": str(a.user_id),
            "activity_type": a.activity_type,
            "activity_category": a.activity_category,
            "title": a.title,
            "description": a.description,
            "impact_level": a.impact_level.value,
            "requires_attention": a.requires_attention,
            "created_at": a.created_at.isoformat()
        }
        for a in activities
    ]

@router.post("/activity-feed", response_model=dict)
def create_activity(
    site_id: str = Query(..., description="Site ID"),
    user_id: str = Query(..., description="User ID"),
    activity_type: str = Query(..., description="Activity type"),
    activity_category: str = Query(..., description="Activity category"),
    title: str = Query(..., description="Activity title"),
    description: Optional[str] = Query(None, description="Activity description"),
    db: Session = Depends(get_db)
):
    """Create a new activity feed entry"""
    # Verify site and user exist
    site = db.query(Site).filter(Site.id == site_id).first()
    user = db.query(User).filter(User.id == user_id).first()
    
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db_activity = ActivityFeed(
        site_id=site_id,
        user_id=user_id,
        activity_type=activity_type,
        activity_category=activity_category,
        title=title,
        description=description
    )
    
    db.add(db_activity)
    db.commit()
    db.refresh(db_activity)
    
    return {
        "id": str(db_activity.id),
        "title": db_activity.title,
        "activity_type": db_activity.activity_type,
        "created_at": db_activity.created_at.isoformat()
    }