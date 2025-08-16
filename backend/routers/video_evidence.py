"""
Video & Evidence Management API Routes
Handles: Video Bookmarks, Access Logs, Exports, Quality Metrics
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from database import get_db
from models import *
from schemas import *
from datetime import datetime, date, timedelta

router = APIRouter()

# VIDEO BOOKMARKS ENDPOINTS
@router.get("/video-bookmarks", response_model=List[VideoBookmarkResponse])
async def get_video_bookmarks(camera_id: Optional[str] = None, user_id: Optional[str] = None, 
                             skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get video bookmarks with optional filtering"""
    query = db.query(VideoBookmark)
    if camera_id:
        query = query.filter(VideoBookmark.camera_id == camera_id)
    if user_id:
        query = query.filter(VideoBookmark.user_id == user_id)
    
    bookmarks = query.order_by(VideoBookmark.created_at.desc()).offset(skip).limit(limit).all()
    return bookmarks

@router.post("/video-bookmarks", response_model=VideoBookmarkResponse)
async def create_video_bookmark(bookmark_data: VideoBookmarkCreateRequest, current_user_id: str = "system", db: Session = Depends(get_db)):
    """Create a new video bookmark"""
    # Parse the date string
    bookmark_date = datetime.strptime(bookmark_data.bookmark_date, '%Y-%m-%d').date()
    
    new_bookmark = VideoBookmark(
        camera_id=bookmark_data.camera_id,
        user_id=current_user_id,  # TODO: Get from auth
        bookmark_date=bookmark_date,
        timestamp_seconds=bookmark_data.timestamp_seconds,
        title=bookmark_data.title,
        description=bookmark_data.description,
        bookmark_type=bookmark_data.bookmark_type,
        priority_level=bookmark_data.priority_level
    )
    
    db.add(new_bookmark)
    db.commit()
    db.refresh(new_bookmark)
    return new_bookmark

@router.get("/video-bookmarks/{bookmark_id}", response_model=VideoBookmarkResponse)
async def get_video_bookmark(bookmark_id: str, db: Session = Depends(get_db)):
    """Get a specific video bookmark by ID"""
    bookmark = db.query(VideoBookmark).filter(VideoBookmark.id == bookmark_id).first()
    if not bookmark:
        raise HTTPException(status_code=404, detail="Video bookmark not found")
    return bookmark

@router.put("/video-bookmarks/{bookmark_id}/status")
async def update_bookmark_status(bookmark_id: str, status: str, db: Session = Depends(get_db)):
    """Update bookmark status"""
    bookmark = db.query(VideoBookmark).filter(VideoBookmark.id == bookmark_id).first()
    if not bookmark:
        raise HTTPException(status_code=404, detail="Video bookmark not found")
    
    bookmark.status = status
    db.commit()
    return {"message": "Bookmark status updated successfully"}

@router.delete("/video-bookmarks/{bookmark_id}")
async def delete_video_bookmark(bookmark_id: str, db: Session = Depends(get_db)):
    """Delete a video bookmark"""
    bookmark = db.query(VideoBookmark).filter(VideoBookmark.id == bookmark_id).first()
    if not bookmark:
        raise HTTPException(status_code=404, detail="Video bookmark not found")
    
    db.delete(bookmark)
    db.commit()
    return {"message": "Video bookmark deleted successfully"}

# VIDEO ACCESS LOGS ENDPOINTS
@router.get("/video-access-logs", response_model=List[VideoAccessLogResponse])
async def get_video_access_logs(user_id: Optional[str] = None, camera_id: Optional[str] = None,
                               skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get video access logs with optional filtering"""
    query = db.query(VideoAccessLog)
    if user_id:
        query = query.filter(VideoAccessLog.user_id == user_id)
    if camera_id:
        query = query.filter(VideoAccessLog.camera_id == camera_id)
    
    logs = query.order_by(VideoAccessLog.access_start.desc()).offset(skip).limit(limit).all()
    return logs

@router.get("/cameras/{camera_id}/access-logs", response_model=List[VideoAccessLogResponse])
async def get_camera_access_logs(camera_id: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get access logs for a specific camera"""
    logs = db.query(VideoAccessLog).filter(VideoAccessLog.camera_id == camera_id).order_by(VideoAccessLog.access_start.desc()).offset(skip).limit(limit).all()
    return logs

@router.get("/users/{user_id}/video-access-logs", response_model=List[VideoAccessLogResponse])
async def get_user_video_access_logs(user_id: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get video access logs for a specific user"""
    logs = db.query(VideoAccessLog).filter(VideoAccessLog.user_id == user_id).order_by(VideoAccessLog.access_start.desc()).offset(skip).limit(limit).all()
    return logs

# VIDEO EXPORTS ENDPOINTS
@router.get("/video-exports", response_model=List[VideoExportResponse])
async def get_video_exports(user_id: Optional[str] = None, camera_id: Optional[str] = None,
                           status: Optional[str] = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get video exports with optional filtering"""
    query = db.query(VideoExport)
    if user_id:
        query = query.filter(VideoExport.user_id == user_id)
    if camera_id:
        query = query.filter(VideoExport.camera_id == camera_id)
    if status:
        query = query.filter(VideoExport.export_status == status)
    
    exports = query.order_by(VideoExport.created_at.desc()).offset(skip).limit(limit).all()
    return exports

@router.post("/video-exports", response_model=VideoExportResponse)
async def create_video_export(export_data: VideoExportCreateRequest, current_user_id: str = "system", db: Session = Depends(get_db)):
    """Create a new video export request"""
    # Parse the date string
    video_date = datetime.strptime(export_data.source_video_date, '%Y-%m-%d').date()
    
    # Calculate export duration
    duration = export_data.end_timestamp_seconds - export_data.start_timestamp_seconds
    
    new_export = VideoExport(
        user_id=current_user_id,  # TODO: Get from auth
        camera_id=export_data.camera_id,
        source_video_date=video_date,
        start_timestamp_seconds=export_data.start_timestamp_seconds,
        end_timestamp_seconds=export_data.end_timestamp_seconds,
        export_duration_seconds=duration,
        export_type=export_data.export_type,
        export_format=export_data.export_format,
        export_purpose=export_data.export_purpose,
        export_justification=export_data.export_justification,
        quality_setting=export_data.quality_setting
    )
    
    db.add(new_export)
    db.commit()
    db.refresh(new_export)
    return new_export

@router.get("/video-exports/{export_id}", response_model=VideoExportResponse)
async def get_video_export(export_id: str, db: Session = Depends(get_db)):
    """Get a specific video export by ID"""
    export = db.query(VideoExport).filter(VideoExport.id == export_id).first()
    if not export:
        raise HTTPException(status_code=404, detail="Video export not found")
    return export

@router.put("/video-exports/{export_id}/status")
async def update_export_status(export_id: str, status: str, download_url: Optional[str] = None, db: Session = Depends(get_db)):
    """Update video export status"""
    export = db.query(VideoExport).filter(VideoExport.id == export_id).first()
    if not export:
        raise HTTPException(status_code=404, detail="Video export not found")
    
    export.export_status = status
    if download_url:
        export.download_url = download_url
    
    if status == "completed":
        export.processing_completed_at = func.current_timestamp()
    
    db.commit()
    return {"message": "Export status updated successfully"}

# VIDEO QUALITY METRICS ENDPOINTS
@router.get("/video-quality-metrics", response_model=List[VideoQualityMetricResponse])
async def get_video_quality_metrics(camera_id: Optional[str] = None, days: int = 7, 
                                   skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get video quality metrics with optional filtering"""
    query = db.query(VideoQualityMetric)
    if camera_id:
        query = query.filter(VideoQualityMetric.camera_id == camera_id)
    
    # Filter by date range
    end_date = date.today()
    start_date = end_date - timedelta(days=days)
    query = query.filter(VideoQualityMetric.analysis_date >= start_date)
    
    metrics = query.order_by(VideoQualityMetric.analysis_date.desc()).offset(skip).limit(limit).all()
    return metrics

@router.get("/cameras/{camera_id}/quality-metrics", response_model=List[VideoQualityMetricResponse])
async def get_camera_quality_metrics(camera_id: str, days: int = 30, db: Session = Depends(get_db)):
    """Get quality metrics for a specific camera"""
    end_date = date.today()
    start_date = end_date - timedelta(days=days)
    
    metrics = db.query(VideoQualityMetric).filter(
        VideoQualityMetric.camera_id == camera_id,
        VideoQualityMetric.analysis_date >= start_date
    ).order_by(VideoQualityMetric.analysis_date.desc()).all()
    
    return metrics

@router.get("/cameras/{camera_id}/quality-summary")
async def get_camera_quality_summary(camera_id: str, days: int = 7, db: Session = Depends(get_db)):
    """Get quality summary statistics for a camera"""
    end_date = date.today()
    start_date = end_date - timedelta(days=days)
    
    metrics = db.query(VideoQualityMetric).filter(
        VideoQualityMetric.camera_id == camera_id,
        VideoQualityMetric.analysis_date >= start_date
    ).all()
    
    if not metrics:
        return {"message": "No quality data found for this camera"}
    
    # Calculate average scores
    avg_sharpness = sum(m.sharpness_score or 0 for m in metrics) / len(metrics)
    avg_brightness = sum(m.brightness_score or 0 for m in metrics) / len(metrics)
    avg_contrast = sum(m.contrast_score or 0 for m in metrics) / len(metrics)
    
    # Count quality ratings
    forensic_ratings = [m.forensic_quality_rating for m in metrics if m.forensic_quality_rating]
    
    return {
        "camera_id": camera_id,
        "date_range": {"start": start_date, "end": end_date},
        "metrics_count": len(metrics),
        "average_sharpness": round(avg_sharpness, 2),
        "average_brightness": round(avg_brightness, 2),
        "average_contrast": round(avg_contrast, 2),
        "forensic_quality_distribution": {rating: forensic_ratings.count(rating) for rating in set(forensic_ratings)}
    }