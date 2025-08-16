"""
Navigation & Street View API Router
Handles navigation routes, waypoints, sessions, and street view cameras
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc
from typing import List, Optional
from datetime import datetime, timedelta
import uuid

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import get_db
from models import (
    NavigationRoute, RouteWaypoint, NavigationSession, StreetViewCamera,
    Site, User, Camera
)
from schemas import (
    NavigationRouteResponse, NavigationRouteCreateRequest,
    RouteWaypointResponse, RouteWaypointCreateRequest,
    NavigationSessionResponse, NavigationSessionCreateRequest,
    StreetViewCameraResponse, StreetViewCameraCreateRequest
)

router = APIRouter(prefix="/navigation", tags=["Navigation & Street View"])

# NAVIGATION ROUTES ENDPOINTS

@router.get("/routes", response_model=List[NavigationRouteResponse])
async def get_navigation_routes(
    site_id: Optional[str] = Query(None, description="Filter by site ID"),
    route_type: Optional[str] = Query(None, description="Filter by route type"),
    status: Optional[str] = Query(None, description="Filter by status"),
    db: Session = Depends(get_db)
):
    """Get all navigation routes"""
    query = db.query(NavigationRoute)
    
    if site_id:
        query = query.filter(NavigationRoute.site_id == site_id)
    if route_type:
        query = query.filter(NavigationRoute.route_type == route_type)
    if status:
        query = query.filter(NavigationRoute.status == status)
    
    routes = query.order_by(desc(NavigationRoute.created_at)).all()
    return routes

@router.post("/routes", response_model=NavigationRouteResponse)
async def create_navigation_route(route_data: NavigationRouteCreateRequest, db: Session = Depends(get_db)):
    """Create a new navigation route"""
    # Verify site exists
    site = db.query(Site).filter(Site.id == route_data.site_id).first()
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    
    # Find a valid user to use as created_by
    existing_user = db.query(User).first()
    if not existing_user:
        raise HTTPException(status_code=400, detail="No users found in system. Cannot create navigation route without a valid created_by user.")
    
    new_route = NavigationRoute(
        site_id=route_data.site_id,
        route_name=route_data.route_name,
        route_code=route_data.route_code,
        description=route_data.description,
        route_type=route_data.route_type,
        purpose=route_data.purpose,
        priority_level=route_data.priority_level,
        start_coordinates=route_data.start_coordinates,
        end_coordinates=route_data.end_coordinates,
        total_distance_meters=route_data.total_distance_meters,
        estimated_duration_minutes=route_data.estimated_duration_minutes,
        elevation_change_meters=route_data.elevation_change_meters,
        difficulty_level=route_data.difficulty_level,
        safety_rating=route_data.safety_rating,
        accessibility_level=route_data.accessibility_level,
        ppe_requirements=route_data.ppe_requirements,
        hazard_warnings=route_data.hazard_warnings,
        created_by=existing_user.id
    )
    
    db.add(new_route)
    db.commit()
    db.refresh(new_route)
    return new_route

@router.get("/routes/{route_id}", response_model=NavigationRouteResponse)
async def get_navigation_route(route_id: str, db: Session = Depends(get_db)):
    """Get a specific navigation route"""
    route = db.query(NavigationRoute).filter(NavigationRoute.id == route_id).first()
    if not route:
        raise HTTPException(status_code=404, detail="Navigation route not found")
    return route

@router.put("/routes/{route_id}", response_model=NavigationRouteResponse)
async def update_navigation_route(route_id: str, route_data: NavigationRouteCreateRequest, db: Session = Depends(get_db)):
    """Update a navigation route"""
    route = db.query(NavigationRoute).filter(NavigationRoute.id == route_id).first()
    if not route:
        raise HTTPException(status_code=404, detail="Navigation route not found")
    
    # Update fields
    for field, value in route_data.dict(exclude_unset=True).items():
        setattr(route, field, value)
    
    db.commit()
    db.refresh(route)
    return route

@router.delete("/routes/{route_id}")
async def delete_navigation_route(route_id: str, db: Session = Depends(get_db)):
    """Delete a navigation route"""
    route = db.query(NavigationRoute).filter(NavigationRoute.id == route_id).first()
    if not route:
        raise HTTPException(status_code=404, detail="Navigation route not found")
    
    db.delete(route)
    db.commit()
    return {"message": "Navigation route deleted successfully"}

# ROUTE WAYPOINTS ENDPOINTS

@router.get("/waypoints", response_model=List[RouteWaypointResponse])
async def get_route_waypoints(
    route_id: Optional[str] = Query(None, description="Filter by route ID"),
    waypoint_type: Optional[str] = Query(None, description="Filter by waypoint type"),
    db: Session = Depends(get_db)
):
    """Get all route waypoints"""
    query = db.query(RouteWaypoint)
    
    if route_id:
        query = query.filter(RouteWaypoint.route_id == route_id)
    if waypoint_type:
        query = query.filter(RouteWaypoint.waypoint_type == waypoint_type)
    
    waypoints = query.order_by(RouteWaypoint.sequence_order).all()
    return waypoints

@router.post("/waypoints", response_model=RouteWaypointResponse)
async def create_route_waypoint(waypoint_data: RouteWaypointCreateRequest, db: Session = Depends(get_db)):
    """Create a new route waypoint"""
    # Verify route exists
    route = db.query(NavigationRoute).filter(NavigationRoute.id == waypoint_data.route_id).first()
    if not route:
        raise HTTPException(status_code=404, detail="Navigation route not found")
    
    new_waypoint = RouteWaypoint(
        route_id=waypoint_data.route_id,
        waypoint_name=waypoint_data.waypoint_name,
        waypoint_code=waypoint_data.waypoint_code,
        sequence_order=waypoint_data.sequence_order,
        latitude=waypoint_data.latitude,
        longitude=waypoint_data.longitude,
        elevation=waypoint_data.elevation,
        waypoint_type=waypoint_data.waypoint_type,
        action_required=waypoint_data.action_required,
        approach_instructions=waypoint_data.approach_instructions,
        departure_instructions=waypoint_data.departure_instructions,
        safety_level=waypoint_data.safety_level,
        hazard_types=waypoint_data.hazard_types,
        associated_camera_ids=waypoint_data.associated_camera_ids,
        monitoring_required=waypoint_data.monitoring_required,
        photo_documentation_required=waypoint_data.photo_documentation_required
    )
    
    db.add(new_waypoint)
    db.commit()
    db.refresh(new_waypoint)
    return new_waypoint

@router.get("/waypoints/{waypoint_id}", response_model=RouteWaypointResponse)
async def get_route_waypoint(waypoint_id: str, db: Session = Depends(get_db)):
    """Get a specific route waypoint"""
    waypoint = db.query(RouteWaypoint).filter(RouteWaypoint.id == waypoint_id).first()
    if not waypoint:
        raise HTTPException(status_code=404, detail="Route waypoint not found")
    return waypoint

@router.delete("/waypoints/{waypoint_id}")
async def delete_route_waypoint(waypoint_id: str, db: Session = Depends(get_db)):
    """Delete a route waypoint"""
    waypoint = db.query(RouteWaypoint).filter(RouteWaypoint.id == waypoint_id).first()
    if not waypoint:
        raise HTTPException(status_code=404, detail="Route waypoint not found")
    
    db.delete(waypoint)
    db.commit()
    return {"message": "Route waypoint deleted successfully"}

# NAVIGATION SESSIONS ENDPOINTS

@router.get("/sessions", response_model=List[NavigationSessionResponse])
async def get_navigation_sessions(
    user_id: Optional[str] = Query(None, description="Filter by user ID"),
    route_id: Optional[str] = Query(None, description="Filter by route ID"),
    session_status: Optional[str] = Query(None, description="Filter by session status"),
    db: Session = Depends(get_db)
):
    """Get all navigation sessions"""
    query = db.query(NavigationSession)
    
    if user_id:
        query = query.filter(NavigationSession.user_id == user_id)
    if route_id:
        query = query.filter(NavigationSession.route_id == route_id)
    if session_status:
        query = query.filter(NavigationSession.session_status == session_status)
    
    sessions = query.order_by(desc(NavigationSession.started_at)).all()
    return sessions

@router.post("/sessions", response_model=NavigationSessionResponse)
async def create_navigation_session(session_data: NavigationSessionCreateRequest, db: Session = Depends(get_db)):
    """Create a new navigation session"""
    # Verify user and route exist
    user = db.query(User).filter(User.id == session_data.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    route = db.query(NavigationRoute).filter(NavigationRoute.id == session_data.route_id).first()
    if not route:
        raise HTTPException(status_code=404, detail="Navigation route not found")
    
    new_session = NavigationSession(
        user_id=session_data.user_id,
        route_id=session_data.route_id,
        session_name=session_data.session_name,
        session_purpose=session_data.session_purpose,
        planned_duration_minutes=session_data.planned_duration_minutes,
        total_waypoints=session_data.total_waypoints,
        device_type=session_data.device_type,
        device_id=session_data.device_id,
        weather_conditions=session_data.weather_conditions
    )
    
    db.add(new_session)
    db.commit()
    db.refresh(new_session)
    return new_session

@router.get("/sessions/{session_id}", response_model=NavigationSessionResponse)
async def get_navigation_session(session_id: str, db: Session = Depends(get_db)):
    """Get a specific navigation session"""
    session = db.query(NavigationSession).filter(NavigationSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Navigation session not found")
    return session

@router.put("/sessions/{session_id}/complete")
async def complete_navigation_session(session_id: str, db: Session = Depends(get_db)):
    """Mark a navigation session as completed"""
    session = db.query(NavigationSession).filter(NavigationSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Navigation session not found")
    
    session.session_status = "completed"
    session.ended_at = datetime.utcnow()
    session.completion_percentage = 100.0
    
    if session.started_at:
        duration = datetime.utcnow() - session.started_at
        session.total_duration_minutes = duration.total_seconds() / 60
    
    db.commit()
    db.refresh(session)
    return {"message": "Navigation session completed successfully"}

# STREET VIEW CAMERAS ENDPOINTS

@router.get("/street-view-cameras", response_model=List[StreetViewCameraResponse])
async def get_street_view_cameras(
    camera_id: Optional[str] = Query(None, description="Filter by camera ID"),
    is_enabled: Optional[bool] = Query(None, description="Filter by street view enabled status"),
    status: Optional[str] = Query(None, description="Filter by status"),
    db: Session = Depends(get_db)
):
    """Get all street view cameras"""
    query = db.query(StreetViewCamera)
    
    if camera_id:
        query = query.filter(StreetViewCamera.camera_id == camera_id)
    if is_enabled is not None:
        query = query.filter(StreetViewCamera.is_street_view_enabled == is_enabled)
    if status:
        query = query.filter(StreetViewCamera.status == status)
    
    cameras = query.order_by(StreetViewCamera.street_view_priority).all()
    return cameras

@router.post("/street-view-cameras", response_model=StreetViewCameraResponse)
async def create_street_view_camera(camera_data: StreetViewCameraCreateRequest, db: Session = Depends(get_db)):
    """Create a new street view camera configuration"""
    # Verify camera exists
    camera = db.query(Camera).filter(Camera.id == camera_data.camera_id).first()
    if not camera:
        raise HTTPException(status_code=404, detail="Camera not found")
    
    # Check if street view configuration already exists for this camera
    existing = db.query(StreetViewCamera).filter(StreetViewCamera.camera_id == camera_data.camera_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Street view configuration already exists for this camera")
    
    new_street_view_camera = StreetViewCamera(
        camera_id=camera_data.camera_id,
        is_street_view_enabled=camera_data.is_street_view_enabled,
        street_view_priority=camera_data.street_view_priority,
        field_of_view_degrees=camera_data.field_of_view_degrees,
        ptz_enabled=camera_data.ptz_enabled,
        streaming_resolution=camera_data.streaming_resolution,
        streaming_fps=camera_data.streaming_fps,
        ai_detection_enabled=camera_data.ai_detection_enabled,
        precise_latitude=camera_data.precise_latitude,
        precise_longitude=camera_data.precise_longitude,
        mounting_height_meters=camera_data.mounting_height_meters,
        orientation_degrees=camera_data.orientation_degrees,
        route_coverage=camera_data.route_coverage,
        waypoint_coverage=camera_data.waypoint_coverage
    )
    
    db.add(new_street_view_camera)
    db.commit()
    db.refresh(new_street_view_camera)
    return new_street_view_camera

@router.get("/street-view-cameras/{camera_config_id}", response_model=StreetViewCameraResponse)
async def get_street_view_camera(camera_config_id: str, db: Session = Depends(get_db)):
    """Get a specific street view camera configuration"""
    camera_config = db.query(StreetViewCamera).filter(StreetViewCamera.id == camera_config_id).first()
    if not camera_config:
        raise HTTPException(status_code=404, detail="Street view camera configuration not found")
    return camera_config

@router.put("/street-view-cameras/{camera_config_id}", response_model=StreetViewCameraResponse)
async def update_street_view_camera(camera_config_id: str, camera_data: StreetViewCameraCreateRequest, db: Session = Depends(get_db)):
    """Update a street view camera configuration"""
    camera_config = db.query(StreetViewCamera).filter(StreetViewCamera.id == camera_config_id).first()
    if not camera_config:
        raise HTTPException(status_code=404, detail="Street view camera configuration not found")
    
    # Update fields
    for field, value in camera_data.dict(exclude_unset=True).items():
        if field != 'camera_id':  # Don't allow changing the camera reference
            setattr(camera_config, field, value)
    
    db.commit()
    db.refresh(camera_config)
    return camera_config

@router.delete("/street-view-cameras/{camera_config_id}")
async def delete_street_view_camera(camera_config_id: str, db: Session = Depends(get_db)):
    """Delete a street view camera configuration"""
    camera_config = db.query(StreetViewCamera).filter(StreetViewCamera.id == camera_config_id).first()
    if not camera_config:
        raise HTTPException(status_code=404, detail="Street view camera configuration not found")
    
    db.delete(camera_config)
    db.commit()
    return {"message": "Street view camera configuration deleted successfully"}

# ANALYTICS AND REPORTING ENDPOINTS

@router.get("/analytics/route-usage")
async def get_route_usage_analytics(
    site_id: Optional[str] = Query(None, description="Filter by site ID"),
    days: int = Query(30, description="Number of days to analyze"),
    db: Session = Depends(get_db)
):
    """Get route usage analytics"""
    date_threshold = datetime.utcnow() - timedelta(days=days)
    
    query = db.query(NavigationRoute)
    if site_id:
        query = query.filter(NavigationRoute.site_id == site_id)
    
    routes = query.all()
    
    analytics = []
    for route in routes:
        # Count sessions for this route within the date range
        session_count = db.query(NavigationSession).filter(
            and_(
                NavigationSession.route_id == route.id,
                NavigationSession.started_at >= date_threshold
            )
        ).count()
        
        # Calculate completion rate
        completed_sessions = db.query(NavigationSession).filter(
            and_(
                NavigationSession.route_id == route.id,
                NavigationSession.session_status == "completed",
                NavigationSession.started_at >= date_threshold
            )
        ).count()
        
        completion_rate = (completed_sessions / session_count * 100) if session_count > 0 else 0
        
        analytics.append({
            "route_id": route.id,
            "route_name": route.route_name,
            "route_type": route.route_type,
            "session_count": session_count,
            "completion_rate": completion_rate,
            "total_distance_meters": route.total_distance_meters,
            "estimated_duration_minutes": route.estimated_duration_minutes
        })
    
    return {
        "analytics_period_days": days,
        "total_routes_analyzed": len(analytics),
        "route_analytics": analytics
    }

@router.get("/analytics/session-performance")
async def get_session_performance_analytics(
    route_id: Optional[str] = Query(None, description="Filter by route ID"),
    days: int = Query(30, description="Number of days to analyze"),
    db: Session = Depends(get_db)
):
    """Get navigation session performance analytics"""
    date_threshold = datetime.utcnow() - timedelta(days=days)
    
    query = db.query(NavigationSession).filter(NavigationSession.started_at >= date_threshold)
    if route_id:
        query = query.filter(NavigationSession.route_id == route_id)
    
    sessions = query.all()
    
    if not sessions:
        return {
            "analytics_period_days": days,
            "total_sessions": 0,
            "performance_metrics": {}
        }
    
    # Calculate performance metrics
    total_sessions = len(sessions)
    completed_sessions = len([s for s in sessions if s.session_status == "completed"])
    avg_completion_rate = sum([s.completion_percentage or 0 for s in sessions]) / total_sessions
    avg_duration = sum([s.total_duration_minutes or 0 for s in sessions if s.total_duration_minutes]) / len([s for s in sessions if s.total_duration_minutes])
    safety_incidents = sum([s.safety_incidents for s in sessions])
    
    return {
        "analytics_period_days": days,
        "total_sessions": total_sessions,
        "performance_metrics": {
            "completion_rate_percentage": (completed_sessions / total_sessions * 100) if total_sessions > 0 else 0,
            "average_completion_percentage": avg_completion_rate,
            "average_duration_minutes": avg_duration,
            "total_safety_incidents": safety_incidents,
            "incident_rate_per_session": safety_incidents / total_sessions if total_sessions > 0 else 0
        }
    }