"""
User Management & Administration API Router
Handles user profiles, role assignments, session management, activity tracking, and permissions
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc, func
from typing import List, Optional
from datetime import datetime, timedelta, date
import uuid

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import get_db
from models import (
    UserManagementProfile, UserRoleAssignment, UserSessionManagement, 
    UserActivityTracking, UserPermissionsMatrix, User, Site
)
from schemas import (
    UserManagementProfileResponse, UserManagementProfileCreateRequest,
    UserRoleAssignmentResponse, UserRoleAssignmentCreateRequest,
    UserSessionManagementResponse, UserSessionManagementCreateRequest,
    UserActivityTrackingResponse, UserActivityTrackingCreateRequest
)

router = APIRouter(prefix="/user-management", tags=["User Management & Administration"])

# USER MANAGEMENT PROFILES ENDPOINTS

@router.get("/profiles", response_model=List[UserManagementProfileResponse])
async def get_user_profiles(
    employment_status: Optional[str] = Query(None, description="Filter by employment status"),
    position_level: Optional[str] = Query(None, description="Filter by position level"),
    department_id: Optional[str] = Query(None, description="Filter by department"),
    db: Session = Depends(get_db)
):
    """Get all user management profiles with filtering"""
    query = db.query(UserManagementProfile)
    
    if employment_status:
        query = query.filter(UserManagementProfile.employment_status == employment_status)
    if position_level:
        query = query.filter(UserManagementProfile.position_level == position_level)
    
    profiles = query.order_by(desc(UserManagementProfile.created_at)).all()
    return profiles

@router.post("/profiles", response_model=UserManagementProfileResponse)
async def create_user_profile(profile_data: UserManagementProfileCreateRequest, db: Session = Depends(get_db)):
    """Create a new user management profile"""
    # Verify user exists
    user = db.query(User).filter(User.id == profile_data.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check if profile already exists
    existing = db.query(UserManagementProfile).filter(UserManagementProfile.user_id == profile_data.user_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="User management profile already exists for this user")
    
    # Parse start date
    start_date = datetime.strptime(profile_data.start_date, "%Y-%m-%d").date()
    
    new_profile = UserManagementProfile(
        user_id=profile_data.user_id,
        employee_number=profile_data.employee_number,
        badge_number=profile_data.badge_number,
        position_title=profile_data.position_title,
        position_level=profile_data.position_level,
        employment_type=profile_data.employment_type,
        employment_status=profile_data.employment_status,
        start_date=start_date,
        skills=profile_data.skills,
        notification_preferences=profile_data.notification_preferences
    )
    
    db.add(new_profile)
    db.commit()
    db.refresh(new_profile)
    return new_profile

@router.get("/profiles/{profile_id}", response_model=UserManagementProfileResponse)
async def get_user_profile(profile_id: str, db: Session = Depends(get_db)):
    """Get a specific user management profile"""
    profile = db.query(UserManagementProfile).filter(UserManagementProfile.id == profile_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="User management profile not found")
    return profile

@router.get("/profiles/user/{user_id}", response_model=UserManagementProfileResponse)
async def get_user_profile_by_user_id(user_id: str, db: Session = Depends(get_db)):
    """Get user management profile by user ID"""
    profile = db.query(UserManagementProfile).filter(UserManagementProfile.user_id == user_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="User management profile not found")
    return profile

@router.put("/profiles/{profile_id}", response_model=UserManagementProfileResponse)
async def update_user_profile(profile_id: str, profile_data: UserManagementProfileCreateRequest, db: Session = Depends(get_db)):
    """Update a user management profile"""
    profile = db.query(UserManagementProfile).filter(UserManagementProfile.id == profile_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="User management profile not found")
    
    # Update fields
    for field, value in profile_data.dict(exclude_unset=True).items():
        if field == 'start_date' and value:
            setattr(profile, field, datetime.strptime(value, "%Y-%m-%d").date())
        elif field != 'user_id':  # Don't allow changing user reference
            setattr(profile, field, value)
    
    db.commit()
    db.refresh(profile)
    return profile

# USER ROLE ASSIGNMENTS ENDPOINTS

@router.get("/role-assignments", response_model=List[UserRoleAssignmentResponse])
async def get_role_assignments(
    user_id: Optional[str] = Query(None, description="Filter by user ID"),
    role_type: Optional[str] = Query(None, description="Filter by role type"),
    assignment_status: Optional[str] = Query(None, description="Filter by assignment status"),
    site_id: Optional[str] = Query(None, description="Filter by site ID"),
    db: Session = Depends(get_db)
):
    """Get all user role assignments with filtering"""
    query = db.query(UserRoleAssignment)
    
    if user_id:
        query = query.filter(UserRoleAssignment.user_id == user_id)
    if role_type:
        query = query.filter(UserRoleAssignment.role_type == role_type)
    if assignment_status:
        query = query.filter(UserRoleAssignment.assignment_status == assignment_status)
    if site_id:
        query = query.filter(UserRoleAssignment.site_id == site_id)
    
    assignments = query.order_by(desc(UserRoleAssignment.created_at)).all()
    return assignments

@router.post("/role-assignments", response_model=UserRoleAssignmentResponse)
async def create_role_assignment(assignment_data: UserRoleAssignmentCreateRequest, db: Session = Depends(get_db)):
    """Create a new user role assignment"""
    # Verify user exists
    user = db.query(User).filter(User.id == assignment_data.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Verify site exists if provided
    if assignment_data.site_id:
        site = db.query(Site).filter(Site.id == assignment_data.site_id).first()
        if not site:
            raise HTTPException(status_code=404, detail="Site not found")
    
    # Find a valid user to use as assigned_by
    existing_user = db.query(User).first()
    if not existing_user:
        raise HTTPException(status_code=400, detail="No users found in system")
    
    # Parse dates
    effective_from = datetime.strptime(assignment_data.effective_from, "%Y-%m-%d").date()
    effective_until = None
    if assignment_data.effective_until:
        effective_until = datetime.strptime(assignment_data.effective_until, "%Y-%m-%d").date()
    
    new_assignment = UserRoleAssignment(
        user_id=assignment_data.user_id,
        role_type=assignment_data.role_type,
        role_name=assignment_data.role_name,
        role_description=assignment_data.role_description,
        site_id=assignment_data.site_id,
        access_level=assignment_data.access_level,
        effective_from=effective_from,
        effective_until=effective_until,
        permissions=assignment_data.permissions,
        is_primary_role=assignment_data.is_primary_role,
        assigned_by=existing_user.id
    )
    
    db.add(new_assignment)
    db.commit()
    db.refresh(new_assignment)
    return new_assignment

@router.get("/role-assignments/{assignment_id}", response_model=UserRoleAssignmentResponse)
async def get_role_assignment(assignment_id: str, db: Session = Depends(get_db)):
    """Get a specific user role assignment"""
    assignment = db.query(UserRoleAssignment).filter(UserRoleAssignment.id == assignment_id).first()
    if not assignment:
        raise HTTPException(status_code=404, detail="User role assignment not found")
    return assignment

@router.put("/role-assignments/{assignment_id}/revoke")
async def revoke_role_assignment(assignment_id: str, db: Session = Depends(get_db)):
    """Revoke a user role assignment"""
    assignment = db.query(UserRoleAssignment).filter(UserRoleAssignment.id == assignment_id).first()
    if not assignment:
        raise HTTPException(status_code=404, detail="User role assignment not found")
    
    assignment.assignment_status = "revoked"
    assignment.revoked_at = datetime.utcnow()
    
    db.commit()
    db.refresh(assignment)
    return {"message": "Role assignment revoked successfully"}

# USER SESSION MANAGEMENT ENDPOINTS

@router.get("/sessions", response_model=List[UserSessionManagementResponse])
async def get_user_sessions(
    user_id: Optional[str] = Query(None, description="Filter by user ID"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    access_method: Optional[str] = Query(None, description="Filter by access method"),
    hours: int = Query(24, description="Number of hours to retrieve"),
    db: Session = Depends(get_db)
):
    """Get user sessions with filtering"""
    time_threshold = datetime.utcnow() - timedelta(hours=hours)
    
    query = db.query(UserSessionManagement).filter(UserSessionManagement.login_timestamp >= time_threshold)
    
    if user_id:
        query = query.filter(UserSessionManagement.user_id == user_id)
    if is_active is not None:
        query = query.filter(UserSessionManagement.is_active == is_active)
    if access_method:
        query = query.filter(UserSessionManagement.access_method == access_method)
    
    sessions = query.order_by(desc(UserSessionManagement.login_timestamp)).all()
    return sessions

@router.post("/sessions", response_model=UserSessionManagementResponse)
async def create_user_session(session_data: UserSessionManagementCreateRequest, db: Session = Depends(get_db)):
    """Create a new user session"""
    # Verify user exists
    user = db.query(User).filter(User.id == session_data.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    new_session = UserSessionManagement(
        user_id=session_data.user_id,
        session_id=session_data.session_id,
        session_token=session_data.session_token,
        ip_address=session_data.ip_address,
        access_method=session_data.access_method,
        authentication_method=session_data.authentication_method,
        device_info=session_data.device_info,
        browser_info=session_data.browser_info
    )
    
    db.add(new_session)
    db.commit()
    db.refresh(new_session)
    return new_session

@router.put("/sessions/{session_id}/logout")
async def logout_session(session_id: str, db: Session = Depends(get_db)):
    """Log out a user session"""
    session = db.query(UserSessionManagement).filter(UserSessionManagement.session_id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session.is_active = False
    session.logout_timestamp = datetime.utcnow()
    if session.login_timestamp:
        duration = datetime.utcnow() - session.login_timestamp
        session.session_duration_seconds = int(duration.total_seconds())
    
    db.commit()
    db.refresh(session)
    return {"message": "Session logged out successfully"}

# USER ACTIVITY TRACKING ENDPOINTS

@router.get("/activity", response_model=List[UserActivityTrackingResponse])
async def get_user_activity(
    user_id: Optional[str] = Query(None, description="Filter by user ID"),
    activity_type: Optional[str] = Query(None, description="Filter by activity type"),
    site_id: Optional[str] = Query(None, description="Filter by site ID"),
    security_level: Optional[str] = Query(None, description="Filter by security level"),
    hours: int = Query(24, description="Number of hours to retrieve"),
    db: Session = Depends(get_db)
):
    """Get user activity tracking records with filtering"""
    time_threshold = datetime.utcnow() - timedelta(hours=hours)
    
    query = db.query(UserActivityTracking).filter(UserActivityTracking.activity_timestamp >= time_threshold)
    
    if user_id:
        query = query.filter(UserActivityTracking.user_id == user_id)
    if activity_type:
        query = query.filter(UserActivityTracking.activity_type == activity_type)
    if site_id:
        query = query.filter(UserActivityTracking.site_id == site_id)
    if security_level:
        query = query.filter(UserActivityTracking.security_level == security_level)
    
    activities = query.order_by(desc(UserActivityTracking.activity_timestamp)).all()
    return activities

@router.post("/activity", response_model=UserActivityTrackingResponse)
async def create_activity_record(activity_data: UserActivityTrackingCreateRequest, db: Session = Depends(get_db)):
    """Create a new user activity tracking record"""
    # Verify user exists
    user = db.query(User).filter(User.id == activity_data.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Verify session exists
    session = db.query(UserSessionManagement).filter(UserSessionManagement.id == activity_data.session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    new_activity = UserActivityTracking(
        user_id=activity_data.user_id,
        session_id=activity_data.session_id,
        activity_type=activity_data.activity_type,
        activity_description=activity_data.activity_description,
        activity_category=activity_data.activity_category,
        resource_type=activity_data.resource_type,
        resource_id=activity_data.resource_id,
        site_id=activity_data.site_id,
        request_method=activity_data.request_method,
        security_level=activity_data.security_level
    )
    
    db.add(new_activity)
    db.commit()
    db.refresh(new_activity)
    return new_activity

# USER MANAGEMENT ANALYTICS ENDPOINTS

@router.get("/analytics/active-users")
async def get_active_users_analytics(
    days: int = Query(30, description="Number of days for analysis"),
    db: Session = Depends(get_db)
):
    """Get active users analytics"""
    date_threshold = datetime.utcnow() - timedelta(days=days)
    
    # Get active sessions in the period
    active_sessions = db.query(UserSessionManagement).filter(
        UserSessionManagement.login_timestamp >= date_threshold
    ).all()
    
    # Calculate metrics
    unique_users = len(set([session.user_id for session in active_sessions]))
    total_sessions = len(active_sessions)
    avg_session_duration = 0
    
    if active_sessions:
        durations = [session.session_duration_seconds for session in active_sessions if session.session_duration_seconds]
        if durations:
            avg_session_duration = sum(durations) / len(durations) / 60  # Convert to minutes
    
    # Group by access method
    access_methods = {}
    for session in active_sessions:
        method = session.access_method.value if hasattr(session.access_method, 'value') else session.access_method
        access_methods[method] = access_methods.get(method, 0) + 1
    
    return {
        "analysis_period_days": days,
        "unique_active_users": unique_users,
        "total_sessions": total_sessions,
        "average_session_duration_minutes": avg_session_duration,
        "access_methods": access_methods,
        "sessions_per_user": total_sessions / unique_users if unique_users > 0 else 0
    }

@router.get("/analytics/role-assignments-summary")
async def get_role_assignments_summary(db: Session = Depends(get_db)):
    """Get role assignments summary analytics"""
    assignments = db.query(UserRoleAssignment).all()
    
    # Group by role type and status
    role_types = {}
    statuses = {}
    
    for assignment in assignments:
        role_type = assignment.role_type.value if hasattr(assignment.role_type, 'value') else assignment.role_type
        status = assignment.assignment_status.value if hasattr(assignment.assignment_status, 'value') else assignment.assignment_status
        
        role_types[role_type] = role_types.get(role_type, 0) + 1
        statuses[status] = statuses.get(status, 0) + 1
    
    # Count primary roles
    primary_roles = db.query(UserRoleAssignment).filter(UserRoleAssignment.is_primary_role == True).count()
    
    # Count active assignments
    active_assignments = db.query(UserRoleAssignment).filter(UserRoleAssignment.assignment_status == "active").count()
    
    return {
        "total_assignments": len(assignments),
        "active_assignments": active_assignments,
        "primary_roles_count": primary_roles,
        "assignments_by_type": role_types,
        "assignments_by_status": statuses,
        "assignment_effectiveness": (active_assignments / len(assignments) * 100) if assignments else 0
    }

@router.get("/analytics/user-activity-summary")
async def get_user_activity_summary(
    hours: int = Query(24, description="Number of hours for analysis"),
    db: Session = Depends(get_db)
):
    """Get user activity summary analytics"""
    time_threshold = datetime.utcnow() - timedelta(hours=hours)
    
    activities = db.query(UserActivityTracking).filter(
        UserActivityTracking.activity_timestamp >= time_threshold
    ).all()
    
    # Group by activity type and security level
    activity_types = {}
    security_levels = {}
    
    for activity in activities:
        act_type = activity.activity_type.value if hasattr(activity.activity_type, 'value') else activity.activity_type
        sec_level = activity.security_level.value if hasattr(activity.security_level, 'value') else activity.security_level
        
        activity_types[act_type] = activity_types.get(act_type, 0) + 1
        security_levels[sec_level] = security_levels.get(sec_level, 0) + 1
    
    # Count high security activities
    high_security_count = len([a for a in activities if 
                              (hasattr(a.security_level, 'value') and a.security_level.value in ['confidential', 'restricted']) or
                              (isinstance(a.security_level, str) and a.security_level in ['confidential', 'restricted'])])
    
    return {
        "analysis_period_hours": hours,
        "total_activities": len(activities),
        "unique_users": len(set([activity.user_id for activity in activities])),
        "activities_by_type": activity_types,
        "activities_by_security_level": security_levels,
        "high_security_activities": high_security_count,
        "activities_per_hour": len(activities) / hours if hours > 0 else 0
    }