"""
ZoneMinder Integration API Router
================================

Provides REST API endpoints to interact with the ZoneMinder connector library.
Supports both mock and real ZoneMinder implementations.
"""

from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List, Dict, Any, Optional
from datetime import datetime, date
from pydantic import BaseModel

from zoneminder_connector import get_zoneminder_connector
from zoneminder_connector.base_connector import DetectionType, StreamQuality

router = APIRouter(prefix="/zoneminder", tags=["ZoneMinder"])

# Pydantic models for request/response validation
class CameraCreateRequest(BaseModel):
    name: str
    camera_type: str
    site_id: str
    location_description: str
    coordinates: List[float]
    recording_enabled: bool = True
    motion_detection: bool = True
    night_vision: bool = False
    ptz_capable: bool = False

class ZoneCreateRequest(BaseModel):
    camera_id: str
    name: str
    zone_type: str
    coordinates: List[List[int]]
    detection_enabled: bool = True
    sensitivity: float = 0.8
    alert_threshold: int = 3
    description: str

class EventFilters(BaseModel):
    camera_id: Optional[str] = None
    detection_type: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    severity: Optional[str] = None
    limit: int = 100

# Dependency to get connector instance
async def get_connector():
    """Dependency to get ZoneMinder connector instance"""
    try:
        connector = get_zoneminder_connector()
        if not connector:
            raise HTTPException(status_code=503, detail="ZoneMinder connector not available")
        
        # Initialize if not already done
        if not getattr(connector, 'is_initialized', False):
            success = await connector.initialize()
            if not success:
                raise HTTPException(status_code=503, detail="Failed to initialize ZoneMinder connector")
        
        return connector
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"ZoneMinder connector error: {str(e)}")

# System Health and Status
@router.get("/status", summary="Get ZoneMinder system status")
async def get_system_status(connector = Depends(get_connector)):
    """Get overall ZoneMinder system health and status"""
    try:
        health = await connector.get_system_health()
        storage = await connector.get_storage_info()
        
        return {
            "status": "operational",
            "system_health": health,
            "storage_info": storage,
            "connector_mode": getattr(connector, 'config', {}).get('mode', 'unknown')
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get system status: {str(e)}")

# Camera Management
@router.get("/cameras", summary="Get all cameras")
async def get_cameras(
    site_id: Optional[str] = Query(None, description="Filter by site ID"),
    connector = Depends(get_connector)
):
    """Get all cameras or cameras for a specific site"""
    try:
        cameras = await connector.get_cameras(site_id=site_id)
        return {
            "cameras": [
                {
                    "camera_id": cam.camera_id,
                    "name": cam.name,
                    "camera_type": cam.camera_type.value,
                    "status": cam.status.value,
                    "site_id": cam.site_id,
                    "location_description": cam.location_description,
                    "coordinates": cam.coordinates,
                    "stream_url": cam.stream_url,
                    "recording_enabled": cam.recording_enabled,
                    "motion_detection": cam.motion_detection,
                    "night_vision": cam.night_vision,
                    "ptz_capable": cam.ptz_capable,
                    "resolution": cam.resolution.value,
                    "created_at": cam.created_at.isoformat() if cam.created_at else None,
                    "last_seen": cam.last_seen.isoformat() if cam.last_seen else None,
                    "metadata": cam.metadata
                }
                for cam in cameras
            ],
            "total_count": len(cameras)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get cameras: {str(e)}")

@router.get("/cameras/{camera_id}", summary="Get specific camera")
async def get_camera(camera_id: str, connector = Depends(get_connector)):
    """Get detailed information about a specific camera"""
    try:
        camera = await connector.get_camera(camera_id)
        if not camera:
            raise HTTPException(status_code=404, detail=f"Camera {camera_id} not found")
        
        return {
            "camera_id": camera.camera_id,
            "name": camera.name,
            "camera_type": camera.camera_type.value,
            "status": camera.status.value,
            "site_id": camera.site_id,
            "location_description": camera.location_description,
            "coordinates": camera.coordinates,
            "stream_url": camera.stream_url,
            "recording_enabled": camera.recording_enabled,
            "motion_detection": camera.motion_detection,
            "night_vision": camera.night_vision,
            "ptz_capable": camera.ptz_capable,
            "resolution": camera.resolution.value,
            "created_at": camera.created_at.isoformat() if camera.created_at else None,
            "last_seen": camera.last_seen.isoformat() if camera.last_seen else None,
            "metadata": camera.metadata
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get camera: {str(e)}")

@router.post("/cameras", summary="Create new camera")
async def create_camera(camera_data: CameraCreateRequest, connector = Depends(get_connector)):
    """Create a new camera configuration"""
    try:
        camera = await connector.create_camera(camera_data.dict())
        return {
            "camera_id": camera.camera_id,
            "name": camera.name,
            "message": "Camera created successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create camera: {str(e)}")

# Stream Management
@router.get("/cameras/{camera_id}/stream", summary="Get live stream info")
async def get_live_stream(
    camera_id: str,
    quality: str = Query("high", description="Stream quality: low, medium, high, ultra"),
    connector = Depends(get_connector)
):
    """Get live stream URL and metadata for a camera"""
    try:
        stream_quality = StreamQuality(quality)
        stream_metadata = await connector.get_live_stream(camera_id, stream_quality)
        
        return {
            "camera_id": stream_metadata.camera_id,
            "stream_url": stream_metadata.stream_url,
            "backup_url": stream_metadata.backup_url,
            "quality": stream_metadata.quality.value,
            "fps": stream_metadata.fps,
            "codec": stream_metadata.codec,
            "bitrate": stream_metadata.bitrate,
            "is_live": stream_metadata.is_live,
            "viewer_count": stream_metadata.viewer_count,
            "uptime_seconds": stream_metadata.uptime_seconds
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid quality parameter: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get stream: {str(e)}")

@router.get("/cameras/{camera_id}/snapshot", summary="Get camera snapshot")
async def get_snapshot(camera_id: str, connector = Depends(get_connector)):
    """Get current snapshot image URL from camera"""
    try:
        snapshot_url = await connector.get_stream_snapshot(camera_id)
        return {
            "camera_id": camera_id,
            "snapshot_url": snapshot_url,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get snapshot: {str(e)}")

# Detection Events
@router.get("/events", summary="Get detection events")
async def get_events(
    camera_id: Optional[str] = Query(None, description="Filter by camera ID"),
    detection_type: Optional[str] = Query(None, description="Filter by detection type"),
    start_date: Optional[datetime] = Query(None, description="Start date filter"),
    end_date: Optional[datetime] = Query(None, description="End date filter"),
    severity: Optional[str] = Query(None, description="Filter by severity"),
    limit: int = Query(100, description="Maximum number of events to return"),
    connector = Depends(get_connector)
):
    """Get detection events with filtering options"""
    try:
        # Convert detection_type string to enum if provided
        detection_type_enum = None
        if detection_type:
            try:
                detection_type_enum = DetectionType(detection_type)
            except ValueError:
                raise HTTPException(status_code=400, detail=f"Invalid detection type: {detection_type}")
        
        events = await connector.get_events(
            camera_id=camera_id,
            detection_type=detection_type_enum,
            start_date=start_date,
            end_date=end_date,
            severity=severity,
            limit=limit
        )
        
        return {
            "events": [
                {
                    "event_id": event.event_id,
                    "camera_id": event.camera_id,
                    "detection_type": event.detection_type.value,
                    "timestamp": event.timestamp.isoformat(),
                    "confidence_score": event.confidence_score,
                    "bounding_boxes": event.bounding_boxes,
                    "description": event.description,
                    "severity": event.severity,
                    "location": event.location,
                    "personnel_involved": event.personnel_involved,
                    "equipment_involved": event.equipment_involved,
                    "image_url": event.image_url,
                    "video_clip_url": event.video_clip_url,
                    "acknowledged": event.acknowledged,
                    "resolved": event.resolved,
                    "metadata": event.metadata
                }
                for event in events
            ],
            "total_count": len(events),
            "filters_applied": {
                "camera_id": camera_id,
                "detection_type": detection_type,
                "start_date": start_date.isoformat() if start_date else None,
                "end_date": end_date.isoformat() if end_date else None,
                "severity": severity,
                "limit": limit
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get events: {str(e)}")

@router.get("/events/{event_id}", summary="Get specific event")
async def get_event(event_id: str, connector = Depends(get_connector)):
    """Get detailed information about a specific detection event"""
    try:
        event = await connector.get_event(event_id)
        if not event:
            raise HTTPException(status_code=404, detail=f"Event {event_id} not found")
        
        return {
            "event_id": event.event_id,
            "camera_id": event.camera_id,
            "detection_type": event.detection_type.value,
            "timestamp": event.timestamp.isoformat(),
            "confidence_score": event.confidence_score,
            "bounding_boxes": event.bounding_boxes,
            "description": event.description,
            "severity": event.severity,
            "location": event.location,
            "personnel_involved": event.personnel_involved,
            "equipment_involved": event.equipment_involved,
            "image_url": event.image_url,
            "video_clip_url": event.video_clip_url,
            "acknowledged": event.acknowledged,
            "resolved": event.resolved,
            "metadata": event.metadata
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get event: {str(e)}")

@router.post("/events/{event_id}/acknowledge", summary="Acknowledge event")
async def acknowledge_event(
    event_id: str,
    user_id: str = Query(..., description="ID of user acknowledging the event"),
    connector = Depends(get_connector)
):
    """Acknowledge a detection event"""
    try:
        success = await connector.acknowledge_event(event_id, user_id)
        if not success:
            raise HTTPException(status_code=404, detail=f"Event {event_id} not found")
        
        return {
            "event_id": event_id,
            "acknowledged_by": user_id,
            "acknowledged_at": datetime.now().isoformat(),
            "message": "Event acknowledged successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to acknowledge event: {str(e)}")

# Monitoring Zones
@router.get("/zones", summary="Get monitoring zones")
async def get_zones(
    camera_id: Optional[str] = Query(None, description="Filter by camera ID"),
    connector = Depends(get_connector)
):
    """Get monitoring zones for camera(s)"""
    try:
        zones = await connector.get_zones(camera_id=camera_id)
        
        return {
            "zones": [
                {
                    "zone_id": zone.zone_id,
                    "camera_id": zone.camera_id,
                    "name": zone.name,
                    "zone_type": zone.zone_type,
                    "coordinates": zone.coordinates,
                    "detection_enabled": zone.detection_enabled,
                    "sensitivity": zone.sensitivity,
                    "alert_threshold": zone.alert_threshold,
                    "description": zone.description,
                    "created_at": zone.created_at.isoformat() if zone.created_at else None
                }
                for zone in zones
            ],
            "total_count": len(zones)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get zones: {str(e)}")

@router.post("/zones", summary="Create monitoring zone")
async def create_zone(zone_data: ZoneCreateRequest, connector = Depends(get_connector)):
    """Create a new monitoring zone"""
    try:
        zone = await connector.create_zone(zone_data.dict())
        return {
            "zone_id": zone.zone_id,
            "name": zone.name,
            "message": "Monitoring zone created successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create zone: {str(e)}")

# Analytics
@router.get("/cameras/{camera_id}/statistics", summary="Get camera statistics")
async def get_camera_statistics(
    camera_id: str,
    start_date: date = Query(..., description="Start date for statistics"),
    end_date: date = Query(..., description="End date for statistics"),
    connector = Depends(get_connector)
):
    """Get camera performance and detection statistics"""
    try:
        stats = await connector.get_camera_statistics(camera_id, start_date, end_date)
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get camera statistics: {str(e)}")

@router.get("/sites/{site_id}/analytics", summary="Get site analytics")
async def get_site_analytics(
    site_id: str,
    start_date: date = Query(..., description="Start date for analytics"),
    end_date: date = Query(..., description="End date for analytics"),
    connector = Depends(get_connector)
):
    """Get site-wide analytics and insights"""
    try:
        analytics = await connector.get_site_analytics(site_id, start_date, end_date)
        return analytics
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get site analytics: {str(e)}")

# Mock Data Information (only available in mock mode)
@router.get("/mock/statistics", summary="Get mock data statistics")
async def get_mock_statistics(connector = Depends(get_connector)):
    """Get statistics about generated mock data (only available in mock mode)"""
    try:
        # Check if this is a mock connector
        if not hasattr(connector, 'get_mock_statistics'):
            raise HTTPException(
                status_code=400, 
                detail="Mock statistics only available in mock mode"
            )
        
        stats = connector.get_mock_statistics()
        return stats
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get mock statistics: {str(e)}")

@router.get("/mock/config", summary="Get mock configuration")
async def get_mock_config(connector = Depends(get_connector)):
    """Get current mock configuration settings"""
    try:
        config = getattr(connector, 'config', {})
        return {
            "mode": config.get('mode', 'unknown'),
            "mock_settings": {
                key: value for key, value in config.items()
                if key.startswith(('sites_', 'cameras_', 'events_', 'zones_', 'rtsp_', 'http_'))
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get mock config: {str(e)}")