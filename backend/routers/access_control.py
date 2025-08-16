"""
Access Control & Security Management API Router
Handles roles, permissions, security policies, and audit logs
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc, func
from typing import List, Optional
from datetime import datetime, timedelta
import uuid

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import get_db
from models import (
    AccessControlRole, SystemPermission, RolePermissionAssignment, 
    SecurityPolicy, AccessControlAuditLog, User, Site
)
from schemas import (
    AccessControlRoleResponse, AccessControlRoleCreateRequest,
    SystemPermissionResponse, SystemPermissionCreateRequest,
    SecurityPolicyResponse, SecurityPolicyCreateRequest,
    AccessControlAuditLogResponse, AccessControlAuditLogCreateRequest
)

router = APIRouter(prefix="/access-control", tags=["Access Control & Security Management"])

# ACCESS CONTROL ROLES ENDPOINTS

@router.get("/roles", response_model=List[AccessControlRoleResponse])
async def get_access_control_roles(
    role_level: Optional[str] = Query(None, description="Filter by role level"),
    risk_level: Optional[str] = Query(None, description="Filter by risk level"),
    is_active: Optional[bool] = Query(True, description="Filter by active status"),
    parent_role_id: Optional[str] = Query(None, description="Filter by parent role"),
    db: Session = Depends(get_db)
):
    """Get all access control roles with filtering"""
    query = db.query(AccessControlRole)
    
    if role_level:
        query = query.filter(AccessControlRole.role_level == role_level)
    if risk_level:
        query = query.filter(AccessControlRole.risk_level == risk_level)
    if is_active is not None:
        query = query.filter(AccessControlRole.is_active == is_active)
    if parent_role_id:
        query = query.filter(AccessControlRole.parent_role_id == parent_role_id)
    
    roles = query.order_by(AccessControlRole.role_level, AccessControlRole.role_name).all()
    return roles

@router.post("/roles", response_model=AccessControlRoleResponse)
async def create_access_control_role(role_data: AccessControlRoleCreateRequest, db: Session = Depends(get_db)):
    """Create a new access control role"""
    # Find a valid user to use as created_by
    existing_user = db.query(User).first()
    if not existing_user:
        raise HTTPException(status_code=400, detail="No users found in system")
    
    # Verify parent role exists if provided
    if role_data.parent_role_id:
        parent_role = db.query(AccessControlRole).filter(AccessControlRole.id == role_data.parent_role_id).first()
        if not parent_role:
            raise HTTPException(status_code=404, detail="Parent role not found")
    
    new_role = AccessControlRole(
        role_name=role_data.role_name,
        role_code=role_data.role_code,
        description=role_data.description,
        role_level=role_data.role_level,
        risk_level=role_data.risk_level,
        color_code=role_data.color_code,
        parent_role_id=role_data.parent_role_id,
        site_access_type=role_data.site_access_type,
        default_site_assignments=role_data.default_site_assignments,
        is_assignable=role_data.is_assignable,
        created_by=existing_user.id
    )
    
    db.add(new_role)
    db.commit()
    db.refresh(new_role)
    return new_role

@router.get("/roles/{role_id}", response_model=AccessControlRoleResponse)
async def get_access_control_role(role_id: str, db: Session = Depends(get_db)):
    """Get a specific access control role"""
    role = db.query(AccessControlRole).filter(AccessControlRole.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Access control role not found")
    return role

@router.put("/roles/{role_id}", response_model=AccessControlRoleResponse)
async def update_access_control_role(role_id: str, role_data: AccessControlRoleCreateRequest, db: Session = Depends(get_db)):
    """Update an access control role"""
    role = db.query(AccessControlRole).filter(AccessControlRole.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Access control role not found")
    
    # Find a valid user to use as updated_by
    existing_user = db.query(User).first()
    
    # Update fields
    for field, value in role_data.dict(exclude_unset=True).items():
        setattr(role, field, value)
    
    if existing_user:
        role.updated_by = existing_user.id
    
    db.commit()
    db.refresh(role)
    return role

@router.delete("/roles/{role_id}")
async def delete_access_control_role(role_id: str, db: Session = Depends(get_db)):
    """Delete an access control role"""
    role = db.query(AccessControlRole).filter(AccessControlRole.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Access control role not found")
    
    # Check for dependencies
    permissions_count = db.query(RolePermissionAssignment).filter(RolePermissionAssignment.role_id == role_id).count()
    if permissions_count > 0:
        raise HTTPException(status_code=400, detail="Cannot delete role that has permission assignments")
    
    db.delete(role)
    db.commit()
    return {"message": "Access control role deleted successfully"}

# SYSTEM PERMISSIONS ENDPOINTS

@router.get("/permissions", response_model=List[SystemPermissionResponse])
async def get_system_permissions(
    category: Optional[str] = Query(None, description="Filter by category"),
    resource_scope: Optional[str] = Query(None, description="Filter by resource scope"),
    operation_type: Optional[str] = Query(None, description="Filter by operation type"),
    risk_level: Optional[str] = Query(None, description="Filter by risk level"),
    is_assignable: Optional[bool] = Query(True, description="Filter by assignable status"),
    db: Session = Depends(get_db)
):
    """Get all system permissions with filtering"""
    query = db.query(SystemPermission)
    
    if category:
        query = query.filter(SystemPermission.category == category)
    if resource_scope:
        query = query.filter(SystemPermission.resource_scope == resource_scope)
    if operation_type:
        query = query.filter(SystemPermission.operation_type == operation_type)
    if risk_level:
        query = query.filter(SystemPermission.risk_level == risk_level)
    if is_assignable is not None:
        query = query.filter(SystemPermission.is_assignable == is_assignable)
    
    permissions = query.order_by(SystemPermission.category, SystemPermission.permission_name).all()
    return permissions

@router.post("/permissions", response_model=SystemPermissionResponse)
async def create_system_permission(permission_data: SystemPermissionCreateRequest, db: Session = Depends(get_db)):
    """Create a new system permission"""
    # Find a valid user to use as created_by
    existing_user = db.query(User).first()
    if not existing_user:
        raise HTTPException(status_code=400, detail="No users found in system")
    
    new_permission = SystemPermission(
        permission_name=permission_data.permission_name,
        permission_code=permission_data.permission_code,
        description=permission_data.description,
        category=permission_data.category,
        subcategory=permission_data.subcategory,
        risk_level=permission_data.risk_level,
        resource_scope=permission_data.resource_scope,
        operation_type=permission_data.operation_type,
        is_assignable=permission_data.is_assignable,
        requires_mfa=permission_data.requires_mfa,
        created_by=existing_user.id
    )
    
    db.add(new_permission)
    db.commit()
    db.refresh(new_permission)
    return new_permission

@router.get("/permissions/{permission_id}", response_model=SystemPermissionResponse)
async def get_system_permission(permission_id: str, db: Session = Depends(get_db)):
    """Get a specific system permission"""
    permission = db.query(SystemPermission).filter(SystemPermission.id == permission_id).first()
    if not permission:
        raise HTTPException(status_code=404, detail="System permission not found")
    return permission

# ROLE PERMISSION ASSIGNMENTS ENDPOINTS

@router.post("/roles/{role_id}/permissions/{permission_id}")
async def assign_permission_to_role(
    role_id: str, 
    permission_id: str,
    assignment_type: Optional[str] = Query("direct", description="Assignment type"),
    db: Session = Depends(get_db)
):
    """Assign a permission to a role"""
    # Verify role exists
    role = db.query(AccessControlRole).filter(AccessControlRole.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    
    # Verify permission exists
    permission = db.query(SystemPermission).filter(SystemPermission.id == permission_id).first()
    if not permission:
        raise HTTPException(status_code=404, detail="Permission not found")
    
    # Check if assignment already exists
    existing = db.query(RolePermissionAssignment).filter(
        and_(
            RolePermissionAssignment.role_id == role_id,
            RolePermissionAssignment.permission_id == permission_id,
            RolePermissionAssignment.assignment_type == assignment_type
        )
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Permission already assigned to role")
    
    # Find a valid user to use as granted_by
    existing_user = db.query(User).first()
    if not existing_user:
        raise HTTPException(status_code=400, detail="No users found in system")
    
    new_assignment = RolePermissionAssignment(
        role_id=role_id,
        permission_id=permission_id,
        assignment_type=assignment_type,
        granted_by=existing_user.id
    )
    
    db.add(new_assignment)
    db.commit()
    db.refresh(new_assignment)
    
    return {"message": "Permission assigned to role successfully", "assignment_id": new_assignment.id}

@router.delete("/roles/{role_id}/permissions/{permission_id}")
async def revoke_permission_from_role(role_id: str, permission_id: str, db: Session = Depends(get_db)):
    """Revoke a permission from a role"""
    assignment = db.query(RolePermissionAssignment).filter(
        and_(
            RolePermissionAssignment.role_id == role_id,
            RolePermissionAssignment.permission_id == permission_id,
            RolePermissionAssignment.is_active == True
        )
    ).first()
    
    if not assignment:
        raise HTTPException(status_code=404, detail="Permission assignment not found")
    
    assignment.is_active = False
    db.commit()
    
    return {"message": "Permission revoked from role successfully"}

@router.get("/roles/{role_id}/permissions")
async def get_role_permissions(role_id: str, db: Session = Depends(get_db)):
    """Get all permissions assigned to a role"""
    # Verify role exists
    role = db.query(AccessControlRole).filter(AccessControlRole.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    
    # Get all active permission assignments for the role
    assignments = db.query(RolePermissionAssignment).filter(
        and_(
            RolePermissionAssignment.role_id == role_id,
            RolePermissionAssignment.is_active == True
        )
    ).all()
    
    # Get permission details
    permissions = []
    for assignment in assignments:
        permission = db.query(SystemPermission).filter(SystemPermission.id == assignment.permission_id).first()
        if permission:
            permissions.append({
                "assignment_id": assignment.id,
                "assignment_type": assignment.assignment_type,
                "permission": {
                    "id": permission.id,
                    "permission_name": permission.permission_name,
                    "permission_code": permission.permission_code,
                    "category": permission.category,
                    "resource_scope": permission.resource_scope,
                    "operation_type": permission.operation_type,
                    "risk_level": permission.risk_level
                },
                "granted_at": assignment.granted_at
            })
    
    return {
        "role_id": role_id,
        "role_name": role.role_name,
        "permissions_count": len(permissions),
        "permissions": permissions
    }

# SECURITY POLICIES ENDPOINTS

@router.get("/policies", response_model=List[SecurityPolicyResponse])
async def get_security_policies(
    category: Optional[str] = Query(None, description="Filter by category"),
    policy_type: Optional[str] = Query(None, description="Filter by policy type"),
    is_active: Optional[bool] = Query(True, description="Filter by active status"),
    enforcement_level: Optional[str] = Query(None, description="Filter by enforcement level"),
    db: Session = Depends(get_db)
):
    """Get all security policies with filtering"""
    query = db.query(SecurityPolicy)
    
    if category:
        query = query.filter(SecurityPolicy.category == category)
    if policy_type:
        query = query.filter(SecurityPolicy.policy_type == policy_type)
    if is_active is not None:
        query = query.filter(SecurityPolicy.is_active == is_active)
    if enforcement_level:
        query = query.filter(SecurityPolicy.enforcement_level == enforcement_level)
    
    policies = query.order_by(SecurityPolicy.category, SecurityPolicy.policy_name).all()
    return policies

@router.post("/policies", response_model=SecurityPolicyResponse)
async def create_security_policy(policy_data: SecurityPolicyCreateRequest, db: Session = Depends(get_db)):
    """Create a new security policy"""
    # Find a valid user to use as created_by
    existing_user = db.query(User).first()
    if not existing_user:
        raise HTTPException(status_code=400, detail="No users found in system")
    
    new_policy = SecurityPolicy(
        policy_name=policy_data.policy_name,
        policy_code=policy_data.policy_code,
        description=policy_data.description,
        category=policy_data.category,
        policy_type=policy_data.policy_type,
        policy_rules=policy_data.policy_rules,
        enforcement_level=policy_data.enforcement_level,
        is_mandatory=policy_data.is_mandatory,
        applies_to_roles=policy_data.applies_to_roles,
        created_by=existing_user.id
    )
    
    db.add(new_policy)
    db.commit()
    db.refresh(new_policy)
    return new_policy

@router.get("/policies/{policy_id}", response_model=SecurityPolicyResponse)
async def get_security_policy(policy_id: str, db: Session = Depends(get_db)):
    """Get a specific security policy"""
    policy = db.query(SecurityPolicy).filter(SecurityPolicy.id == policy_id).first()
    if not policy:
        raise HTTPException(status_code=404, detail="Security policy not found")
    return policy

@router.put("/policies/{policy_id}/activate")
async def activate_security_policy(policy_id: str, db: Session = Depends(get_db)):
    """Activate a security policy"""
    policy = db.query(SecurityPolicy).filter(SecurityPolicy.id == policy_id).first()
    if not policy:
        raise HTTPException(status_code=404, detail="Security policy not found")
    
    policy.is_active = True
    db.commit()
    db.refresh(policy)
    
    return {"message": "Security policy activated successfully"}

@router.put("/policies/{policy_id}/deactivate")
async def deactivate_security_policy(policy_id: str, db: Session = Depends(get_db)):
    """Deactivate a security policy"""
    policy = db.query(SecurityPolicy).filter(SecurityPolicy.id == policy_id).first()
    if not policy:
        raise HTTPException(status_code=404, detail="Security policy not found")
    
    policy.is_active = False
    db.commit()
    db.refresh(policy)
    
    return {"message": "Security policy deactivated successfully"}

# ACCESS CONTROL AUDIT LOG ENDPOINTS

@router.get("/audit-logs", response_model=List[AccessControlAuditLogResponse])
async def get_audit_logs(
    event_type: Optional[str] = Query(None, description="Filter by event type"),
    event_category: Optional[str] = Query(None, description="Filter by event category"),
    user_id: Optional[str] = Query(None, description="Filter by user ID"),
    violation_severity: Optional[str] = Query(None, description="Filter by violation severity"),
    hours: int = Query(24, description="Number of hours to retrieve"),
    db: Session = Depends(get_db)
):
    """Get access control audit logs with filtering"""
    time_threshold = datetime.utcnow() - timedelta(hours=hours)
    
    query = db.query(AccessControlAuditLog).filter(AccessControlAuditLog.event_timestamp >= time_threshold)
    
    if event_type:
        query = query.filter(AccessControlAuditLog.event_type == event_type)
    if event_category:
        query = query.filter(AccessControlAuditLog.event_category == event_category)
    if user_id:
        query = query.filter(AccessControlAuditLog.user_id == user_id)
    if violation_severity:
        query = query.filter(AccessControlAuditLog.violation_severity == violation_severity)
    
    logs = query.order_by(desc(AccessControlAuditLog.event_timestamp)).all()
    return logs

@router.post("/audit-logs", response_model=AccessControlAuditLogResponse)
async def create_audit_log(log_data: AccessControlAuditLogCreateRequest, db: Session = Depends(get_db)):
    """Create a new access control audit log entry"""
    new_log = AccessControlAuditLog(
        event_type=log_data.event_type,
        event_category=log_data.event_category,
        user_id=log_data.user_id,
        target_user_id=log_data.target_user_id,
        action_performed=log_data.action_performed,
        resource_type=log_data.resource_type,
        site_id=log_data.site_id,
        access_granted=log_data.access_granted,
        denial_reason=log_data.denial_reason,
        ip_address=log_data.ip_address
    )
    
    db.add(new_log)
    db.commit()
    db.refresh(new_log)
    return new_log

# ACCESS CONTROL ANALYTICS ENDPOINTS

@router.get("/analytics/security-overview")
async def get_security_overview(
    days: int = Query(7, description="Number of days for analysis"),
    db: Session = Depends(get_db)
):
    """Get comprehensive security overview analytics"""
    date_threshold = datetime.utcnow() - timedelta(days=days)
    
    # Get audit logs from the period
    audit_logs = db.query(AccessControlAuditLog).filter(
        AccessControlAuditLog.event_timestamp >= date_threshold
    ).all()
    
    # Calculate metrics
    total_events = len(audit_logs)
    violations = len([log for log in audit_logs if log.violation_severity])
    denied_access = len([log for log in audit_logs if log.access_granted == False])
    
    # Group by event category
    event_categories = {}
    violation_severities = {}
    
    for log in audit_logs:
        cat = log.event_category.value if hasattr(log.event_category, 'value') else log.event_category
        event_categories[cat] = event_categories.get(cat, 0) + 1
        
        if log.violation_severity:
            sev = log.violation_severity.value if hasattr(log.violation_severity, 'value') else log.violation_severity
            violation_severities[sev] = violation_severities.get(sev, 0) + 1
    
    # Count active roles and permissions
    active_roles = db.query(AccessControlRole).filter(AccessControlRole.is_active == True).count()
    active_permissions = db.query(SystemPermission).filter(SystemPermission.is_assignable == True).count()
    active_policies = db.query(SecurityPolicy).filter(SecurityPolicy.is_active == True).count()
    
    return {
        "analysis_period_days": days,
        "security_metrics": {
            "total_security_events": total_events,
            "security_violations": violations,
            "denied_access_attempts": denied_access,
            "violation_rate": (violations / total_events * 100) if total_events > 0 else 0
        },
        "access_control_summary": {
            "active_roles": active_roles,
            "active_permissions": active_permissions,
            "active_policies": active_policies
        },
        "event_distribution": event_categories,
        "violation_severity_distribution": violation_severities
    }

@router.get("/analytics/role-utilization")
async def get_role_utilization_analytics(db: Session = Depends(get_db)):
    """Get role utilization analytics"""
    roles = db.query(AccessControlRole).all()
    
    role_analytics = []
    for role in roles:
        # Count permission assignments
        permission_count = db.query(RolePermissionAssignment).filter(
            and_(
                RolePermissionAssignment.role_id == role.id,
                RolePermissionAssignment.is_active == True
            )
        ).count()
        
        role_analytics.append({
            "role_id": role.id,
            "role_name": role.role_name,
            "role_level": role.role_level,
            "risk_level": role.risk_level,
            "user_count": role.user_count,
            "permission_count": permission_count,
            "is_active": role.is_active,
            "utilization_score": role.user_count * permission_count if role.user_count and permission_count else 0
        })
    
    # Sort by utilization score
    role_analytics.sort(key=lambda x: x["utilization_score"], reverse=True)
    
    return {
        "total_roles": len(roles),
        "active_roles": len([r for r in roles if r.is_active]),
        "role_utilization": role_analytics[:10],  # Top 10 most utilized roles
        "average_permissions_per_role": sum([ra["permission_count"] for ra in role_analytics]) / len(role_analytics) if role_analytics else 0
    }