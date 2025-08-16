from fastapi import FastAPI, APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import get_db, test_connection
from models import *
from schemas import StatusCheck, StatusCheckCreate
import os
import logging
from pathlib import Path
from datetime import datetime

# Import modular routers
from routers import core, ai_detection, video_evidence, system_reports, timelapse, field_operations

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# Create the main app without a prefix
app = FastAPI(title="AI Construction Management API", version="1.0.0")

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Test database connection on startup
if not test_connection():
    raise RuntimeError("Failed to connect to database")

# Basic API routes
@api_router.get("/")
async def root():
    return {"message": "AI Construction Management API", "version": "1.0.0", "status": "running"}

@api_router.get("/health")
async def health_check():
    db_status = test_connection()
    return {
        "status": "healthy" if db_status else "unhealthy",
        "database": "connected" if db_status else "disconnected",
        "timestamp": datetime.utcnow()
    }

# Legacy status check endpoints (for backward compatibility)
@api_router.post("/status", response_model=StatusCheck)
async def create_status_check(input: StatusCheckCreate):
    status_obj = StatusCheck(**input.dict())
    return status_obj

@api_router.get("/status", response_model=list[StatusCheck])
async def get_status_checks():
    # Return empty list for now - this was the old MongoDB endpoint
    return []

# Dashboard stats endpoint
@api_router.get("/dashboard/stats")
async def get_dashboard_stats(db: Session = Depends(get_db)):
    """Get dashboard statistics"""
    total_sites = db.query(Site).count()
    active_sites = db.query(Site).filter(Site.status == SiteStatus.active).count()
    total_users = db.query(User).count()
    total_cameras = db.query(Camera).count()
    active_alerts = db.query(Alert).filter(Alert.status == AlertStatus.open).count()
    
    return {
        "total_sites": total_sites,
        "active_sites": active_sites,
        "total_users": total_users,
        "total_cameras": total_cameras,
        "active_alerts": active_alerts,
        "timestamp": datetime.utcnow()
    }

# Include modular routers
api_router.include_router(core.router, tags=["Core Foundation"])
api_router.include_router(ai_detection.router, tags=["AI & Detection"])
api_router.include_router(video_evidence.router, tags=["Video & Evidence"])
api_router.include_router(system_reports.router, tags=["System & Reports"])
api_router.include_router(timelapse.router, tags=["Time-lapse & Progress"])
api_router.include_router(field_operations.router, tags=["Field Operations & Assessment"])

# Include the main router in the app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("startup")
async def startup_event():
    logger.info("AI Construction Management API starting up...")
    logger.info(f"Database connection: {'OK' if test_connection() else 'FAILED'}")
    logger.info("Modular router structure loaded:")
    logger.info("  - Core Foundation: Sites, Users, Zones, Cameras, Alerts, Personnel")
    logger.info("  - AI & Detection: AI Models, Detections, Recording Sessions, Analytics")
    logger.info("  - Video & Evidence: Bookmarks, Access Logs, Exports, Quality Metrics")
    logger.info("  - System & Reports: Reports, Config, Notifications, Audit Logs")
    logger.info("  - Time-lapse & Progress: Sequences, Bookmarks, Events, Milestones")
    logger.info("  - Field Operations & Assessment: Inspection Paths, Waypoints, Executions, Templates")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("AI Construction Management API shutting down...")
