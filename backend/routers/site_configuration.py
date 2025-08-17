"""
Site Configuration & Infrastructure API Router
Handles site configurations, infrastructure, zone configurations, performance tracking, and compliance
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
    SiteConfiguration, SiteInfrastructure, SiteZoneConfiguration, 
    SitePerformanceTracking, SiteComplianceTracking, Site, User, Zone
)
from schemas import (
    SiteConfigurationResponse, SiteConfigurationCreateRequest,
    SiteInfrastructureResponse, SiteInfrastructureCreateRequest,
    SiteZoneConfigurationResponse, SiteZoneConfigurationCreateRequest,
    SitePerformanceTrackingResponse, SitePerformanceTrackingCreateRequest,
    SiteComplianceTrackingResponse, SiteComplianceTrackingCreateRequest
)

router = APIRouter(prefix="/site-configuration", tags=["Site Configuration & Infrastructure"])

# SITE CONFIGURATIONS ENDPOINTS

@router.get("/configurations", response_model=List[SiteConfigurationResponse])
async def get_site_configurations(
    site_id: Optional[str] = Query(None, description="Filter by site ID"),
    safety_level: Optional[str] = Query(None, description="Filter by safety level"),
    ai_detection_enabled: Optional[bool] = Query(None, description="Filter by AI detection status"),
    db: Session = Depends(get_db)
):
    """Get all site configurations with filtering"""
    query = db.query(SiteConfiguration)
    
    if site_id:
        query = query.filter(SiteConfiguration.site_id == site_id)
    if safety_level:
        query = query.filter(SiteConfiguration.safety_level == safety_level)
    if ai_detection_enabled is not None:
        query = query.filter(SiteConfiguration.ai_detection_enabled == ai_detection_enabled)
    
    configurations = query.order_by(desc(SiteConfiguration.created_at)).all()
    return configurations

@router.post("/configurations", response_model=SiteConfigurationResponse)
async def create_site_configuration(config_data: SiteConfigurationCreateRequest, db: Session = Depends(get_db)):
    """Create a new site configuration"""
    # Verify site exists
    site = db.query(Site).filter(Site.id == config_data.site_id).first()
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    
    # Check if configuration already exists for this site
    existing = db.query(SiteConfiguration).filter(SiteConfiguration.site_id == config_data.site_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Site configuration already exists for this site")
    
    # Find a valid user to use as configured_by and last_modified_by
    existing_user = db.query(User).first()
    if not existing_user:
        raise HTTPException(status_code=400, detail="No users found in system")
    
    new_config = SiteConfiguration(
        site_id=config_data.site_id,
        timezone=config_data.timezone,
        working_hours_start=config_data.working_hours_start,
        working_hours_end=config_data.working_hours_end,
        max_occupancy=config_data.max_occupancy,
        safety_level=config_data.safety_level,
        ai_detection_enabled=config_data.ai_detection_enabled,
        ai_sensitivity_level=config_data.ai_sensitivity_level,
        recording_retention_days=config_data.recording_retention_days,
        recording_quality=config_data.recording_quality,
        alert_notifications_enabled=config_data.alert_notifications_enabled,
        access_control_type=config_data.access_control_type,
        emergency_contacts=config_data.emergency_contacts,
        safety_protocols=config_data.safety_protocols,
        configured_by=existing_user.id,
        last_modified_by=existing_user.id
    )
    
    db.add(new_config)
    db.commit()
    db.refresh(new_config)
    return new_config

@router.get("/configurations/{config_id}", response_model=SiteConfigurationResponse)
async def get_site_configuration(config_id: str, db: Session = Depends(get_db)):
    """Get a specific site configuration"""
    config = db.query(SiteConfiguration).filter(SiteConfiguration.id == config_id).first()
    if not config:
        raise HTTPException(status_code=404, detail="Site configuration not found")
    return config

@router.put("/configurations/{config_id}", response_model=SiteConfigurationResponse)
async def update_site_configuration(config_id: str, config_data: SiteConfigurationCreateRequest, db: Session = Depends(get_db)):
    """Update a site configuration"""
    config = db.query(SiteConfiguration).filter(SiteConfiguration.id == config_id).first()
    if not config:
        raise HTTPException(status_code=404, detail="Site configuration not found")
    
    # Find a valid user to use as last_modified_by
    existing_user = db.query(User).first()
    
    # Update fields
    for field, value in config_data.dict(exclude_unset=True).items():
        if field != 'site_id':  # Don't allow changing site reference
            setattr(config, field, value)
    
    if existing_user:
        config.last_modified_by = existing_user.id
    
    db.commit()
    db.refresh(config)
    return config

# SITE INFRASTRUCTURE ENDPOINTS

@router.get("/infrastructure", response_model=List[SiteInfrastructureResponse])
async def get_site_infrastructure(
    site_id: Optional[str] = Query(None, description="Filter by site ID"),
    network_status: Optional[str] = Query(None, description="Filter by network status"),
    power_status: Optional[str] = Query(None, description="Filter by power status"),
    db: Session = Depends(get_db)
):
    """Get all site infrastructure records with filtering"""
    query = db.query(SiteInfrastructure)
    
    if site_id:
        query = query.filter(SiteInfrastructure.site_id == site_id)
    if network_status:
        query = query.filter(SiteInfrastructure.network_status == network_status)
    if power_status:
        query = query.filter(SiteInfrastructure.power_status == power_status)
    
    infrastructure = query.order_by(desc(SiteInfrastructure.created_at)).all()
    return infrastructure

@router.post("/infrastructure", response_model=SiteInfrastructureResponse)
async def create_site_infrastructure(infra_data: SiteInfrastructureCreateRequest, db: Session = Depends(get_db)):
    """Create a new site infrastructure record"""
    # Verify site exists
    site = db.query(Site).filter(Site.id == infra_data.site_id).first()
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    
    # Check if infrastructure record already exists for this site
    existing = db.query(SiteInfrastructure).filter(SiteInfrastructure.site_id == infra_data.site_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Site infrastructure record already exists for this site")
    
    new_infrastructure = SiteInfrastructure(
        site_id=infra_data.site_id,
        network_status=infra_data.network_status,
        internet_speed_mbps=infra_data.internet_speed_mbps,
        network_provider=infra_data.network_provider,
        power_status=infra_data.power_status,
        backup_power_available=infra_data.backup_power_available,
        cellular_coverage=infra_data.cellular_coverage,
        storage_capacity_tb=infra_data.storage_capacity_tb,
        cloud_storage_enabled=infra_data.cloud_storage_enabled,
        environmental_sensors=infra_data.environmental_sensors
    )
    
    db.add(new_infrastructure)
    db.commit()
    db.refresh(new_infrastructure)
    return new_infrastructure

@router.get("/infrastructure/{infra_id}", response_model=SiteInfrastructureResponse)
async def get_site_infrastructure_record(infra_id: str, db: Session = Depends(get_db)):
    """Get a specific site infrastructure record"""
    infrastructure = db.query(SiteInfrastructure).filter(SiteInfrastructure.id == infra_id).first()
    if not infrastructure:
        raise HTTPException(status_code=404, detail="Site infrastructure record not found")
    return infrastructure

# ZONE CONFIGURATIONS ENDPOINTS

@router.get("/zone-configurations", response_model=List[SiteZoneConfigurationResponse])
async def get_zone_configurations(
    site_id: Optional[str] = Query(None, description="Filter by site ID"),
    zone_id: Optional[str] = Query(None, description="Filter by zone ID"),
    monitoring_level: Optional[str] = Query(None, description="Filter by monitoring level"),
    zone_status: Optional[str] = Query(None, description="Filter by zone status"),
    db: Session = Depends(get_db)
):
    """Get all zone configurations with filtering"""
    query = db.query(SiteZoneConfiguration)
    
    if site_id:
        query = query.filter(SiteZoneConfiguration.site_id == site_id)
    if zone_id:
        query = query.filter(SiteZoneConfiguration.zone_id == zone_id)
    if monitoring_level:
        query = query.filter(SiteZoneConfiguration.monitoring_level == monitoring_level)
    if zone_status:
        query = query.filter(SiteZoneConfiguration.zone_status == zone_status)
    
    configurations = query.order_by(desc(SiteZoneConfiguration.created_at)).all()
    return configurations

@router.post("/zone-configurations", response_model=SiteZoneConfigurationResponse)
async def create_zone_configuration(zone_config_data: SiteZoneConfigurationCreateRequest, db: Session = Depends(get_db)):
    """Create a new zone configuration"""
    # Verify site exists
    site = db.query(Site).filter(Site.id == zone_config_data.site_id).first()
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    
    # Verify zone exists
    zone = db.query(Zone).filter(Zone.id == zone_config_data.zone_id).first()
    if not zone:
        raise HTTPException(status_code=404, detail="Zone not found")
    
    # Check if configuration already exists for this site-zone combination
    existing = db.query(SiteZoneConfiguration).filter(
        and_(
            SiteZoneConfiguration.site_id == zone_config_data.site_id,
            SiteZoneConfiguration.zone_id == zone_config_data.zone_id
        )
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Zone configuration already exists for this site-zone combination")
    
    # Find a valid user to use as configured_by
    existing_user = db.query(User).first()
    if not existing_user:
        raise HTTPException(status_code=400, detail="No users found in system")
    
    new_zone_config = SiteZoneConfiguration(
        site_id=zone_config_data.site_id,
        zone_id=zone_config_data.zone_id,
        monitoring_level=zone_config_data.monitoring_level,
        max_personnel=zone_config_data.max_personnel,
        authorized_roles=zone_config_data.authorized_roles,
        ppe_requirements=zone_config_data.ppe_requirements,
        detection_sensitivity=zone_config_data.detection_sensitivity,
        safety_requirements=zone_config_data.safety_requirements,
        configured_by=existing_user.id
    )
    
    db.add(new_zone_config)
    db.commit()
    db.refresh(new_zone_config)
    return new_zone_config

# PERFORMANCE TRACKING ENDPOINTS

@router.get("/performance-tracking", response_model=List[SitePerformanceTrackingResponse])
async def get_performance_tracking(
    site_id: Optional[str] = Query(None, description="Filter by site ID"),
    tracking_period: Optional[str] = Query(None, description="Filter by tracking period"),
    days: int = Query(30, description="Number of days to retrieve"),
    db: Session = Depends(get_db)
):
    """Get site performance tracking records with filtering"""
    date_threshold = datetime.utcnow().date() - timedelta(days=days)
    
    query = db.query(SitePerformanceTracking).filter(SitePerformanceTracking.tracking_date >= date_threshold)
    
    if site_id:
        query = query.filter(SitePerformanceTracking.site_id == site_id)
    if tracking_period:
        query = query.filter(SitePerformanceTracking.tracking_period == tracking_period)
    
    tracking_records = query.order_by(desc(SitePerformanceTracking.tracking_date)).all()
    return tracking_records

@router.post("/performance-tracking", response_model=SitePerformanceTrackingResponse)
async def create_performance_tracking(tracking_data: SitePerformanceTrackingCreateRequest, db: Session = Depends(get_db)):
    """Create a new performance tracking record"""
    # Verify site exists
    site = db.query(Site).filter(Site.id == tracking_data.site_id).first()
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    
    # Find a valid user to use as analyst_id
    existing_user = db.query(User).first()
    
    # Parse tracking date
    tracking_date = datetime.strptime(tracking_data.tracking_date, "%Y-%m-%d").date()
    
    new_tracking = SitePerformanceTracking(
        site_id=tracking_data.site_id,
        tracking_date=tracking_date,
        tracking_period=tracking_data.tracking_period,
        system_health_score=tracking_data.system_health_score,
        uptime_percentage=tracking_data.uptime_percentage,
        safety_incident_count=tracking_data.safety_incident_count,
        compliance_score=tracking_data.compliance_score,
        performance_notes=tracking_data.performance_notes,
        analyst_id=existing_user.id if existing_user else None
    )
    
    db.add(new_tracking)
    db.commit()
    db.refresh(new_tracking)
    return new_tracking

# COMPLIANCE TRACKING ENDPOINTS

@router.get("/compliance-tracking", response_model=List[SiteComplianceTrackingResponse])
async def get_compliance_tracking(
    site_id: Optional[str] = Query(None, description="Filter by site ID"),
    compliance_framework: Optional[str] = Query(None, description="Filter by compliance framework"),
    compliance_status: Optional[str] = Query(None, description="Filter by compliance status"),
    audit_type: Optional[str] = Query(None, description="Filter by audit type"),
    days: int = Query(90, description="Number of days to retrieve"),
    db: Session = Depends(get_db)
):
    """Get compliance tracking records with filtering"""
    date_threshold = datetime.utcnow().date() - timedelta(days=days)
    
    query = db.query(SiteComplianceTracking).filter(SiteComplianceTracking.compliance_date >= date_threshold)
    
    if site_id:
        query = query.filter(SiteComplianceTracking.site_id == site_id)
    if compliance_framework:
        query = query.filter(SiteComplianceTracking.compliance_framework == compliance_framework)
    if compliance_status:
        query = query.filter(SiteComplianceTracking.compliance_status == compliance_status)
    if audit_type:
        query = query.filter(SiteComplianceTracking.audit_type == audit_type)
    
    compliance_records = query.order_by(desc(SiteComplianceTracking.compliance_date)).all()
    return compliance_records

@router.post("/compliance-tracking", response_model=SiteComplianceTrackingResponse)
async def create_compliance_tracking(compliance_data: SiteComplianceTrackingCreateRequest, db: Session = Depends(get_db)):
    """Create a new compliance tracking record"""
    # Verify site exists
    site = db.query(Site).filter(Site.id == compliance_data.site_id).first()
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    
    # Find a valid user to use as reported_by
    existing_user = db.query(User).first()
    if not existing_user:
        raise HTTPException(status_code=400, detail="No users found in system")
    
    # Parse dates
    compliance_date = datetime.strptime(compliance_data.compliance_date, "%Y-%m-%d").date()
    audit_date = datetime.strptime(compliance_data.audit_date, "%Y-%m-%d").date()
    
    new_compliance = SiteComplianceTracking(
        site_id=compliance_data.site_id,
        compliance_framework=compliance_data.compliance_framework,
        compliance_date=compliance_date,
        overall_compliance_score=compliance_data.overall_compliance_score,
        audit_type=compliance_data.audit_type,
        audit_date=audit_date,
        auditor_name=compliance_data.auditor_name,
        total_findings=compliance_data.total_findings,
        safety_compliance_score=compliance_data.safety_compliance_score,
        reported_by=existing_user.id
    )
    
    db.add(new_compliance)
    db.commit()
    db.refresh(new_compliance)
    return new_compliance

# ANALYTICS ENDPOINTS

@router.get("/analytics/site-overview")
async def get_site_overview_analytics(
    site_id: Optional[str] = Query(None, description="Filter by site ID"),
    days: int = Query(30, description="Number of days for analysis"),
    db: Session = Depends(get_db)
):
    """Get comprehensive site overview analytics"""
    date_threshold = datetime.utcnow().date() - timedelta(days=days)
    
    # Get site configurations
    config_query = db.query(SiteConfiguration)
    if site_id:
        config_query = config_query.filter(SiteConfiguration.site_id == site_id)
    
    configurations = config_query.all()
    
    # Get performance data
    perf_query = db.query(SitePerformanceTracking).filter(
        SitePerformanceTracking.tracking_date >= date_threshold
    )
    if site_id:
        perf_query = perf_query.filter(SitePerformanceTracking.site_id == site_id)
    
    performance_records = perf_query.all()
    
    # Calculate metrics
    total_sites = len(configurations)
    ai_enabled_sites = len([c for c in configurations if c.ai_detection_enabled])
    
    avg_health_score = 0
    avg_compliance_score = 0
    total_incidents = 0
    
    if performance_records:
        health_scores = [p.system_health_score for p in performance_records if p.system_health_score]
        compliance_scores = [p.compliance_score for p in performance_records if p.compliance_score]
        total_incidents = sum([p.safety_incident_count for p in performance_records])
        
        if health_scores:
            avg_health_score = sum(health_scores) / len(health_scores)
        if compliance_scores:
            avg_compliance_score = sum(compliance_scores) / len(compliance_scores)
    
    return {
        "analysis_period_days": days,
        "site_summary": {
            "total_sites_configured": total_sites,
            "ai_enabled_sites": ai_enabled_sites,
            "ai_adoption_rate": (ai_enabled_sites / total_sites * 100) if total_sites > 0 else 0
        },
        "performance_summary": {
            "average_health_score": avg_health_score,
            "average_compliance_score": avg_compliance_score,
            "total_safety_incidents": total_incidents,
            "performance_records_analyzed": len(performance_records)
        }
    }

@router.get("/analytics/compliance-summary")
async def get_compliance_summary_analytics(
    site_id: Optional[str] = Query(None, description="Filter by site ID"),
    days: int = Query(90, description="Number of days for analysis"),
    db: Session = Depends(get_db)
):
    """Get compliance analytics summary"""
    date_threshold = datetime.utcnow().date() - timedelta(days=days)
    
    query = db.query(SiteComplianceTracking).filter(
        SiteComplianceTracking.compliance_date >= date_threshold
    )
    if site_id:
        query = query.filter(SiteComplianceTracking.site_id == site_id)
    
    compliance_records = query.all()
    
    if not compliance_records:
        return {
            "analysis_period_days": days,
            "compliance_summary": "No compliance data available",
            "records_analyzed": 0
        }
    
    # Group by status and framework
    status_counts = {}
    framework_counts = {}
    audit_type_counts = {}
    
    total_findings = 0
    avg_compliance_score = 0
    
    for record in compliance_records:
        status = record.compliance_status.value if hasattr(record.compliance_status, 'value') else record.compliance_status
        framework = record.compliance_framework
        audit_type = record.audit_type.value if hasattr(record.audit_type, 'value') else record.audit_type
        
        status_counts[status] = status_counts.get(status, 0) + 1
        framework_counts[framework] = framework_counts.get(framework, 0) + 1
        audit_type_counts[audit_type] = audit_type_counts.get(audit_type, 0) + 1
        
        total_findings += record.total_findings
        avg_compliance_score += record.overall_compliance_score
    
    avg_compliance_score = avg_compliance_score / len(compliance_records)
    
    return {
        "analysis_period_days": days,
        "records_analyzed": len(compliance_records),
        "compliance_metrics": {
            "average_compliance_score": avg_compliance_score,
            "total_findings": total_findings,
            "compliance_by_status": status_counts,
            "compliance_by_framework": framework_counts,
            "audits_by_type": audit_type_counts
        },
        "compliance_rate": (status_counts.get("compliant", 0) / len(compliance_records) * 100) if compliance_records else 0
    }