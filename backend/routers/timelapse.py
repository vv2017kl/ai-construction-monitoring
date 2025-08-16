"""
Time-Lapse & Progress Tracking API Routes
Handles: Timelapse Sequences, Bookmarks, Events, Shares, Construction Milestones
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from database import get_db
from models import *
from schemas import *
from datetime import datetime, date

router = APIRouter()

# TIMELAPSE SEQUENCES ENDPOINTS
@router.get("/timelapse-sequences", response_model=List[TimelapseSequenceResponse])
async def get_timelapse_sequences(site_id: Optional[str] = None, status: Optional[str] = None,
                                 skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get timelapse sequences with optional filtering"""
    query = db.query(TimelapseSequence)
    if site_id:
        query = query.filter(TimelapseSequence.site_id == site_id)
    if status:
        query = query.filter(TimelapseSequence.generation_status == status)
    
    sequences = query.order_by(TimelapseSequence.created_at.desc()).offset(skip).limit(limit).all()
    return sequences

@router.post("/timelapse-sequences", response_model=TimelapseSequenceResponse)
async def create_timelapse_sequence(sequence_data: TimelapseSequenceCreateRequest, current_user_id: str = "system", db: Session = Depends(get_db)):
    """Create a new timelapse sequence"""
    # Parse datetime strings
    start_dt = datetime.fromisoformat(sequence_data.start_datetime.replace('Z', '+00:00'))
    end_dt = datetime.fromisoformat(sequence_data.end_datetime.replace('Z', '+00:00'))
    
    # Calculate duration
    duration = int((end_dt - start_dt).total_seconds())
    
    new_sequence = TimelapseSequence(
        title=sequence_data.title,
        site_id=sequence_data.site_id,
        created_by=current_user_id,  # TODO: Get from auth
        primary_camera_id=sequence_data.primary_camera_id,
        start_datetime=start_dt,
        end_datetime=end_dt,
        duration_seconds=duration,
        description=sequence_data.description,
        compression_level=sequence_data.compression_level,
        frame_rate_fps=sequence_data.frame_rate_fps
    )
    
    db.add(new_sequence)
    db.commit()
    db.refresh(new_sequence)
    return new_sequence

@router.get("/timelapse-sequences/{sequence_id}", response_model=TimelapseSequenceResponse)
async def get_timelapse_sequence(sequence_id: str, db: Session = Depends(get_db)):
    """Get a specific timelapse sequence by ID"""
    sequence = db.query(TimelapseSequence).filter(TimelapseSequence.id == sequence_id).first()
    if not sequence:
        raise HTTPException(status_code=404, detail="Timelapse sequence not found")
    return sequence

@router.put("/timelapse-sequences/{sequence_id}/status")
async def update_sequence_status(sequence_id: str, status: str, db: Session = Depends(get_db)):
    """Update timelapse sequence generation status"""
    sequence = db.query(TimelapseSequence).filter(TimelapseSequence.id == sequence_id).first()
    if not sequence:
        raise HTTPException(status_code=404, detail="Timelapse sequence not found")
    
    sequence.generation_status = status
    if status == "completed":
        sequence.processing_completed_at = func.current_timestamp()
    
    db.commit()
    return {"message": "Sequence status updated successfully"}

@router.get("/sites/{site_id}/timelapse-sequences", response_model=List[TimelapseSequenceResponse])
async def get_site_timelapse_sequences(site_id: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get timelapse sequences for a specific site"""
    sequences = db.query(TimelapseSequence).filter(TimelapseSequence.site_id == site_id).order_by(TimelapseSequence.created_at.desc()).offset(skip).limit(limit).all()
    return sequences

# TIMELAPSE BOOKMARKS ENDPOINTS
@router.get("/timelapse-bookmarks", response_model=List[TimelapseBookmarkResponse])
async def get_timelapse_bookmarks(sequence_id: Optional[str] = None, user_id: Optional[str] = None,
                                 skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get timelapse bookmarks with optional filtering"""
    query = db.query(TimelapseBookmark)
    if sequence_id:
        query = query.filter(TimelapseBookmark.timelapse_sequence_id == sequence_id)
    if user_id:
        query = query.filter(TimelapseBookmark.user_id == user_id)
    
    bookmarks = query.order_by(TimelapseBookmark.timestamp_seconds).offset(skip).limit(limit).all()
    return bookmarks

@router.post("/timelapse-bookmarks", response_model=TimelapseBookmarkResponse)
async def create_timelapse_bookmark(bookmark_data: TimelapseBookmarkCreateRequest, current_user_id: str = "system", db: Session = Depends(get_db)):
    """Create a new timelapse bookmark"""
    new_bookmark = TimelapseBookmark(
        timelapse_sequence_id=bookmark_data.timelapse_sequence_id,
        user_id=current_user_id,  # TODO: Get from auth
        bookmark_name=bookmark_data.bookmark_name,
        timestamp_seconds=bookmark_data.timestamp_seconds,
        description=bookmark_data.description,
        bookmark_type=bookmark_data.bookmark_type
    )
    
    db.add(new_bookmark)
    db.commit()
    db.refresh(new_bookmark)
    return new_bookmark

@router.get("/timelapse-sequences/{sequence_id}/bookmarks", response_model=List[TimelapseBookmarkResponse])
async def get_sequence_bookmarks(sequence_id: str, db: Session = Depends(get_db)):
    """Get all bookmarks for a specific timelapse sequence"""
    bookmarks = db.query(TimelapseBookmark).filter(TimelapseBookmark.timelapse_sequence_id == sequence_id).order_by(TimelapseBookmark.timestamp_seconds).all()
    return bookmarks

@router.delete("/timelapse-bookmarks/{bookmark_id}")
async def delete_timelapse_bookmark(bookmark_id: str, db: Session = Depends(get_db)):
    """Delete a timelapse bookmark"""
    bookmark = db.query(TimelapseBookmark).filter(TimelapseBookmark.id == bookmark_id).first()
    if not bookmark:
        raise HTTPException(status_code=404, detail="Timelapse bookmark not found")
    
    db.delete(bookmark)
    db.commit()
    return {"message": "Timelapse bookmark deleted successfully"}

# TIMELAPSE EVENTS ENDPOINTS
@router.get("/timelapse-events")
async def get_timelapse_events(sequence_id: Optional[str] = None, event_type: Optional[str] = None,
                              skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get timelapse events with optional filtering"""
    query = db.query(TimelapseEvent)
    if sequence_id:
        query = query.filter(TimelapseEvent.timelapse_sequence_id == sequence_id)
    if event_type:
        query = query.filter(TimelapseEvent.event_type == event_type)
    
    events = query.order_by(TimelapseEvent.sequence_timestamp_seconds).offset(skip).limit(limit).all()
    
    return [
        {
            "id": event.id,
            "timelapse_sequence_id": event.timelapse_sequence_id,
            "event_title": event.event_title,
            "event_type": event.event_type,
            "event_timestamp": event.event_timestamp,
            "sequence_timestamp_seconds": float(event.sequence_timestamp_seconds),
            "confidence_score": float(event.confidence_score) if event.confidence_score else None,
            "impact_level": event.impact_level,
            "status": event.status
        } for event in events
    ]

@router.get("/timelapse-sequences/{sequence_id}/events")
async def get_sequence_events(sequence_id: str, db: Session = Depends(get_db)):
    """Get all events for a specific timelapse sequence"""
    events = db.query(TimelapseEvent).filter(TimelapseEvent.timelapse_sequence_id == sequence_id).order_by(TimelapseEvent.sequence_timestamp_seconds).all()
    
    return [
        {
            "id": event.id,
            "event_title": event.event_title,
            "event_type": event.event_type,
            "sequence_timestamp_seconds": float(event.sequence_timestamp_seconds),
            "impact_level": event.impact_level,
            "status": event.status
        } for event in events
    ]

# CONSTRUCTION MILESTONES ENDPOINTS
@router.get("/construction-milestones", response_model=List[ConstructionMilestoneResponse])
async def get_construction_milestones(site_id: Optional[str] = None, status: Optional[str] = None,
                                     skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get construction milestones with optional filtering"""
    query = db.query(ConstructionMilestone)
    if site_id:
        query = query.filter(ConstructionMilestone.site_id == site_id)
    if status:
        query = query.filter(ConstructionMilestone.status == status)
    
    milestones = query.order_by(ConstructionMilestone.planned_completion_date).offset(skip).limit(limit).all()
    return milestones

@router.post("/construction-milestones", response_model=ConstructionMilestoneResponse)
async def create_construction_milestone(milestone_data: ConstructionMilestoneCreateRequest, current_user_id: str = "system", db: Session = Depends(get_db)):
    """Create a new construction milestone"""
    # Parse date strings if provided
    planned_start = None
    planned_completion = None
    
    if milestone_data.planned_start_date:
        planned_start = datetime.strptime(milestone_data.planned_start_date, '%Y-%m-%d').date()
    if milestone_data.planned_completion_date:
        planned_completion = datetime.strptime(milestone_data.planned_completion_date, '%Y-%m-%d').date()
    
    new_milestone = ConstructionMilestone(
        site_id=milestone_data.site_id,
        milestone_name=milestone_data.milestone_name,
        milestone_code=milestone_data.milestone_code,
        description=milestone_data.description,
        project_phase=milestone_data.project_phase,
        planned_start_date=planned_start,
        planned_completion_date=planned_completion,
        created_by=current_user_id  # TODO: Get from auth
    )
    
    db.add(new_milestone)
    db.commit()
    db.refresh(new_milestone)
    return new_milestone

@router.get("/construction-milestones/{milestone_id}", response_model=ConstructionMilestoneResponse)
async def get_construction_milestone(milestone_id: str, db: Session = Depends(get_db)):
    """Get a specific construction milestone by ID"""
    milestone = db.query(ConstructionMilestone).filter(ConstructionMilestone.id == milestone_id).first()
    if not milestone:
        raise HTTPException(status_code=404, detail="Construction milestone not found")
    return milestone

@router.put("/construction-milestones/{milestone_id}/progress")
async def update_milestone_progress(milestone_id: str, completion_percentage: float, status: Optional[str] = None, db: Session = Depends(get_db)):
    """Update construction milestone progress"""
    milestone = db.query(ConstructionMilestone).filter(ConstructionMilestone.id == milestone_id).first()
    if not milestone:
        raise HTTPException(status_code=404, detail="Construction milestone not found")
    
    milestone.completion_percentage = completion_percentage
    if status:
        milestone.status = status
    
    # Auto-complete if 100%
    if completion_percentage >= 100.0:
        milestone.status = "completed"
        if not milestone.actual_completion_date:
            milestone.actual_completion_date = date.today()
    
    db.commit()
    return {"message": "Milestone progress updated successfully"}

@router.get("/sites/{site_id}/construction-milestones", response_model=List[ConstructionMilestoneResponse])
async def get_site_construction_milestones(site_id: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get construction milestones for a specific site"""
    milestones = db.query(ConstructionMilestone).filter(ConstructionMilestone.site_id == site_id).order_by(ConstructionMilestone.planned_completion_date).offset(skip).limit(limit).all()
    return milestones