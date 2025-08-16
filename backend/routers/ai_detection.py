"""
AI & Detection API Routes
Handles: AI Detections, AI Models, Recording Sessions, Analytics
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from database import get_db
from models import *
from schemas import *
from datetime import date, timedelta

router = APIRouter()

# AI DETECTIONS ENDPOINTS
@router.get("/ai-detections", response_model=List[AIDetectionResponse])
async def get_ai_detections(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all AI detections with pagination"""
    detections = db.query(AIDetection).order_by(AIDetection.timestamp.desc()).offset(skip).limit(limit).all()
    return detections

@router.get("/sites/{site_id}/ai-detections", response_model=List[AIDetectionResponse])
async def get_site_ai_detections(site_id: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get AI detections for a specific site"""
    detections = db.query(AIDetection).filter(AIDetection.site_id == site_id).order_by(AIDetection.timestamp.desc()).offset(skip).limit(limit).all()
    return detections

@router.get("/cameras/{camera_id}/ai-detections", response_model=List[AIDetectionResponse])
async def get_camera_ai_detections(camera_id: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get AI detections for a specific camera"""
    detections = db.query(AIDetection).filter(AIDetection.camera_id == camera_id).order_by(AIDetection.timestamp.desc()).offset(skip).limit(limit).all()
    return detections

@router.post("/ai-detections", response_model=AIDetectionResponse)
async def create_ai_detection(detection_data: AIDetectionCreateRequest, db: Session = Depends(get_db)):
    """Create a new AI detection"""
    new_detection = AIDetection(
        camera_id=detection_data.camera_id,
        site_id=detection_data.site_id,
        zone_id=detection_data.zone_id,
        detection_type=detection_data.detection_type,
        person_count=detection_data.person_count,
        confidence_score=detection_data.confidence_score,
        detection_results=detection_data.detection_results,
        safety_score=detection_data.safety_score
    )
    
    db.add(new_detection)
    db.commit()
    db.refresh(new_detection)
    return new_detection

@router.get("/ai-detections/{detection_id}", response_model=AIDetectionResponse)
async def get_ai_detection(detection_id: str, db: Session = Depends(get_db)):
    """Get a specific AI detection by ID"""
    detection = db.query(AIDetection).filter(AIDetection.id == detection_id).first()
    if not detection:
        raise HTTPException(status_code=404, detail="AI Detection not found")
    return detection

# AI MODELS ENDPOINTS
@router.get("/ai-models", response_model=List[AIModelResponse])
async def get_ai_models(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all AI models with pagination"""
    models = db.query(AIModel).offset(skip).limit(limit).all()
    return models

# AI Model endpoints moved to dedicated ai_models router
# @router.post("/ai-models", response_model=AIModelResponse)
# async def create_ai_model(model_data: AIModelCreateRequest, db: Session = Depends(get_db)):
#     """Create a new AI model"""
#     new_model = AIModel(
#         name=model_data.name,
#         description=model_data.description,
#         model_type=model_data.model_type,
#         provider=model_data.provider,
#         endpoint_url=model_data.endpoint_url,
#         confidence_threshold=model_data.confidence_threshold
#     )
#     
#     db.add(new_model)
#     db.commit()
#     db.refresh(new_model)
#     return new_model

# @router.get("/ai-models/{model_id}", response_model=AIModelResponse)
# async def get_ai_model(model_id: str, db: Session = Depends(get_db)):
#     """Get a specific AI model by ID"""
#     model = db.query(AIModel).filter(AIModel.id == model_id).first()
#     if not model:
#         raise HTTPException(status_code=404, detail="AI Model not found")
#     return model

# @router.put("/ai-models/{model_id}", response_model=AIModelResponse)
# async def update_ai_model(model_id: str, model_data: AIModelCreateRequest, db: Session = Depends(get_db)):
#     """Update an existing AI model"""
#     model = db.query(AIModel).filter(AIModel.id == model_id).first()
#     if not model:
#         raise HTTPException(status_code=404, detail="AI Model not found")
#     
#     for field, value in model_data.dict(exclude_unset=True).items():
#         setattr(model, field, value)
#     
#     db.commit()
#     db.refresh(model)
#     return model

# @router.delete("/ai-models/{model_id}")
# async def delete_ai_model(model_id: str, db: Session = Depends(get_db)):
#     """Delete an AI model"""
#     model = db.query(AIModel).filter(AIModel.id == model_id).first()
#     if not model:
#         raise HTTPException(status_code=404, detail="AI Model not found")
#     
#     db.delete(model)
#     db.commit()
#     return {"message": "AI Model deleted successfully"}

# RECORDING SESSIONS ENDPOINTS
@router.get("/recording-sessions", response_model=List[RecordingSessionResponse])
async def get_recording_sessions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all recording sessions with pagination"""
    sessions = db.query(RecordingSession).order_by(RecordingSession.start_time.desc()).offset(skip).limit(limit).all()
    return sessions

@router.get("/cameras/{camera_id}/recording-sessions", response_model=List[RecordingSessionResponse])
async def get_camera_recording_sessions(camera_id: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get recording sessions for a specific camera"""
    sessions = db.query(RecordingSession).filter(RecordingSession.camera_id == camera_id).order_by(RecordingSession.start_time.desc()).offset(skip).limit(limit).all()
    return sessions

@router.get("/sites/{site_id}/recording-sessions", response_model=List[RecordingSessionResponse])
async def get_site_recording_sessions(site_id: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get recording sessions for a specific site"""
    sessions = db.query(RecordingSession).filter(RecordingSession.site_id == site_id).order_by(RecordingSession.start_time.desc()).offset(skip).limit(limit).all()
    return sessions

@router.get("/recording-sessions/{session_id}", response_model=RecordingSessionResponse)
async def get_recording_session(session_id: str, db: Session = Depends(get_db)):
    """Get a specific recording session by ID"""
    session = db.query(RecordingSession).filter(RecordingSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Recording Session not found")
    return session

# AI ANALYTICS ENDPOINTS
@router.get("/ai-analytics/detection-stats")
async def get_detection_analytics(site_id: Optional[str] = None, camera_id: Optional[str] = None, days: int = 7, db: Session = Depends(get_db)):
    """Get AI detection analytics for the specified time period"""
    query = db.query(AIDetectionAnalytics)
    
    if site_id:
        query = query.filter(AIDetectionAnalytics.site_id == site_id)
    if camera_id:
        query = query.filter(AIDetectionAnalytics.camera_id == camera_id)
    
    # Filter by date range
    end_date = date.today()
    start_date = end_date - timedelta(days=days)
    query = query.filter(AIDetectionAnalytics.analysis_date >= start_date)
    
    analytics = query.all()
    
    # Aggregate the results
    total_detections = sum(a.total_detections for a in analytics)
    avg_confidence = sum(a.avg_confidence_score or 0 for a in analytics) / len(analytics) if analytics else 0
    
    return {
        "total_detections": total_detections,
        "average_confidence": round(avg_confidence, 2),
        "analytics_records": len(analytics),
        "date_range": {"start": start_date, "end": end_date}
    }

@router.get("/cameras/{camera_id}/ai-performance")
async def get_camera_ai_performance(camera_id: str, days: int = 30, db: Session = Depends(get_db)):
    """Get AI performance metrics for a specific camera"""
    end_date = date.today()
    start_date = end_date - timedelta(days=days)
    
    performance_records = db.query(CameraAIPerformance).filter(
        CameraAIPerformance.camera_id == camera_id,
        CameraAIPerformance.analysis_date >= start_date
    ).all()
    
    if not performance_records:
        return {"message": "No performance data found for this camera"}
    
    # Calculate aggregated metrics
    avg_accuracy = sum(p.accuracy_rate or 0 for p in performance_records) / len(performance_records)
    avg_processing_time = sum(p.avg_processing_time_ms or 0 for p in performance_records) / len(performance_records)
    total_detections = sum(p.total_detections for p in performance_records)
    
    return {
        "camera_id": camera_id,
        "date_range": {"start": start_date, "end": end_date},
        "average_accuracy_rate": round(avg_accuracy, 2),
        "average_processing_time_ms": int(avg_processing_time),
        "total_detections": total_detections,
        "performance_records": len(performance_records)
    }