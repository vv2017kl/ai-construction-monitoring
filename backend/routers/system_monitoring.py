"""
System Monitoring & Infrastructure Health API Router
Handles system health monitoring, service metrics, infrastructure monitoring, alerts, and dashboards
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
    SystemHealthMonitoring, ServiceHealthMetric, InfrastructureMonitoring,
    SystemAlert, MonitoringDashboard, User
)
from schemas import (
    SystemHealthMonitoringResponse, SystemHealthMonitoringCreateRequest,
    ServiceHealthMetricResponse, ServiceHealthMetricCreateRequest,
    SystemAlertResponse, SystemAlertCreateRequest,
    MonitoringDashboardResponse, MonitoringDashboardCreateRequest
)

router = APIRouter(prefix="/system-monitoring", tags=["System Monitoring & Infrastructure Health"])

# SYSTEM HEALTH MONITORING ENDPOINTS

@router.get("/health", response_model=List[SystemHealthMonitoringResponse])
async def get_system_health_monitoring(
    system_status: Optional[str] = Query(None, description="Filter by system status"),
    health_trend: Optional[str] = Query(None, description="Filter by health trend"),
    hours: int = Query(24, description="Number of hours to retrieve"),
    db: Session = Depends(get_db)
):
    """Get system health monitoring records with filtering"""
    time_threshold = datetime.utcnow() - timedelta(hours=hours)
    
    query = db.query(SystemHealthMonitoring).filter(SystemHealthMonitoring.timestamp >= time_threshold)
    
    if system_status:
        query = query.filter(SystemHealthMonitoring.system_status == system_status)
    if health_trend:
        query = query.filter(SystemHealthMonitoring.health_trend == health_trend)
    
    health_records = query.order_by(desc(SystemHealthMonitoring.timestamp)).all()
    return health_records

@router.post("/health", response_model=SystemHealthMonitoringResponse)
async def create_system_health_monitoring(health_data: SystemHealthMonitoringCreateRequest, db: Session = Depends(get_db)):
    """Create a new system health monitoring record"""
    new_health_record = SystemHealthMonitoring(
        overall_health_score=health_data.overall_health_score,
        system_status=health_data.system_status,
        availability_percentage=health_data.availability_percentage,
        total_services_count=health_data.total_services_count,
        healthy_services_count=health_data.healthy_services_count,
        warning_services_count=health_data.warning_services_count,
        critical_services_count=health_data.critical_services_count,
        monitoring_interval_minutes=health_data.monitoring_interval_minutes
    )
    
    db.add(new_health_record)
    db.commit()
    db.refresh(new_health_record)
    return new_health_record

@router.get("/health/current")
async def get_current_system_health(db: Session = Depends(get_db)):
    """Get the most recent system health status"""
    latest_health = db.query(SystemHealthMonitoring).order_by(desc(SystemHealthMonitoring.timestamp)).first()
    
    if not latest_health:
        return {
            "message": "No health data available",
            "system_status": "unknown",
            "overall_health_score": 0
        }
    
    return {
        "timestamp": latest_health.timestamp,
        "overall_health_score": latest_health.overall_health_score,
        "system_status": latest_health.system_status,
        "availability_percentage": latest_health.availability_percentage,
        "total_services": latest_health.total_services_count,
        "healthy_services": latest_health.healthy_services_count,
        "warning_services": latest_health.warning_services_count,
        "critical_services": latest_health.critical_services_count,
        "health_trend": latest_health.health_trend,
        "performance_trend": latest_health.performance_trend
    }

# SERVICE HEALTH METRICS ENDPOINTS

@router.get("/services", response_model=List[ServiceHealthMetricResponse])
async def get_service_health_metrics(
    service_name: Optional[str] = Query(None, description="Filter by service name"),
    service_type: Optional[str] = Query(None, description="Filter by service type"),
    service_status: Optional[str] = Query(None, description="Filter by service status"),
    hours: int = Query(24, description="Number of hours to retrieve"),
    db: Session = Depends(get_db)
):
    """Get service health metrics with filtering"""
    time_threshold = datetime.utcnow() - timedelta(hours=hours)
    
    query = db.query(ServiceHealthMetric).filter(ServiceHealthMetric.timestamp >= time_threshold)
    
    if service_name:
        query = query.filter(ServiceHealthMetric.service_name == service_name)
    if service_type:
        query = query.filter(ServiceHealthMetric.service_type == service_type)
    if service_status:
        query = query.filter(ServiceHealthMetric.service_status == service_status)
    
    service_metrics = query.order_by(desc(ServiceHealthMetric.timestamp)).all()
    return service_metrics

@router.post("/services", response_model=ServiceHealthMetricResponse)
async def create_service_health_metric(service_data: ServiceHealthMetricCreateRequest, db: Session = Depends(get_db)):
    """Create a new service health metric record"""
    new_service_metric = ServiceHealthMetric(
        service_name=service_data.service_name,
        service_type=service_data.service_type,
        service_status=service_data.service_status,
        uptime_percentage=service_data.uptime_percentage,
        response_time_avg_ms=service_data.response_time_avg_ms,
        success_rate_percentage=service_data.success_rate_percentage,
        cpu_utilization_percentage=service_data.cpu_utilization_percentage,
        memory_utilization_percentage=service_data.memory_utilization_percentage
    )
    
    db.add(new_service_metric)
    db.commit()
    db.refresh(new_service_metric)
    return new_service_metric

@router.get("/services/{service_name}/status")
async def get_service_status(service_name: str, db: Session = Depends(get_db)):
    """Get current status of a specific service"""
    latest_metric = db.query(ServiceHealthMetric).filter(
        ServiceHealthMetric.service_name == service_name
    ).order_by(desc(ServiceHealthMetric.timestamp)).first()
    
    if not latest_metric:
        raise HTTPException(status_code=404, detail="Service not found")
    
    return {
        "service_name": latest_metric.service_name,
        "service_type": latest_metric.service_type,
        "service_status": latest_metric.service_status,
        "uptime_percentage": latest_metric.uptime_percentage,
        "response_time_avg_ms": latest_metric.response_time_avg_ms,
        "success_rate_percentage": latest_metric.success_rate_percentage,
        "last_updated": latest_metric.timestamp,
        "health_check_status": latest_metric.health_check_status
    }

# INFRASTRUCTURE MONITORING ENDPOINTS

@router.get("/infrastructure")
async def get_infrastructure_monitoring(
    component_name: Optional[str] = Query(None, description="Filter by component name"),
    component_type: Optional[str] = Query(None, description="Filter by component type"),
    component_status: Optional[str] = Query(None, description="Filter by component status"),
    hours: int = Query(24, description="Number of hours to retrieve"),
    db: Session = Depends(get_db)
):
    """Get infrastructure monitoring records with filtering"""
    time_threshold = datetime.utcnow() - timedelta(hours=hours)
    
    query = db.query(InfrastructureMonitoring).filter(InfrastructureMonitoring.timestamp >= time_threshold)
    
    if component_name:
        query = query.filter(InfrastructureMonitoring.component_name == component_name)
    if component_type:
        query = query.filter(InfrastructureMonitoring.component_type == component_type)
    if component_status:
        query = query.filter(InfrastructureMonitoring.component_status == component_status)
    
    infrastructure_records = query.order_by(desc(InfrastructureMonitoring.timestamp)).all()
    
    # Convert to dict format for response
    result = []
    for record in infrastructure_records:
        result.append({
            "id": record.id,
            "component_name": record.component_name,
            "component_type": record.component_type,
            "timestamp": record.timestamp,
            "component_status": record.component_status,
            "availability_percentage": record.availability_percentage,
            "capacity_utilization_percentage": record.capacity_utilization_percentage,
            "throughput_mbps": record.throughput_mbps,
            "latency_avg_ms": record.latency_avg_ms,
            "cpu_utilization_percentage": record.cpu_utilization_percentage,
            "memory_utilization_percentage": record.memory_utilization_percentage,
            "disk_utilization_percentage": record.disk_utilization_percentage,
            "error_count_24h": record.error_count_24h,
            "created_at": record.created_at
        })
    
    return result

@router.post("/infrastructure")
async def create_infrastructure_monitoring(component_data: dict, db: Session = Depends(get_db)):
    """Create a new infrastructure monitoring record"""
    new_infrastructure = InfrastructureMonitoring(
        component_name=component_data.get("component_name"),
        component_type=component_data.get("component_type"),
        component_status=component_data.get("component_status", "healthy"),
        availability_percentage=component_data.get("availability_percentage", 100.0),
        capacity_utilization_percentage=component_data.get("capacity_utilization_percentage"),
        throughput_mbps=component_data.get("throughput_mbps"),
        latency_avg_ms=component_data.get("latency_avg_ms"),
        cpu_utilization_percentage=component_data.get("cpu_utilization_percentage"),
        memory_utilization_percentage=component_data.get("memory_utilization_percentage"),
        disk_utilization_percentage=component_data.get("disk_utilization_percentage"),
        error_count_24h=component_data.get("error_count_24h", 0)
    )
    
    db.add(new_infrastructure)
    db.commit()
    db.refresh(new_infrastructure)
    
    return {
        "id": new_infrastructure.id,
        "component_name": new_infrastructure.component_name,
        "component_type": new_infrastructure.component_type,
        "component_status": new_infrastructure.component_status,
        "timestamp": new_infrastructure.timestamp,
        "created_at": new_infrastructure.created_at
    }

# SYSTEM ALERTS ENDPOINTS

@router.get("/alerts", response_model=List[SystemAlertResponse])
async def get_system_alerts(
    alert_level: Optional[str] = Query(None, description="Filter by alert level"),
    alert_category: Optional[str] = Query(None, description="Filter by alert category"),
    status: Optional[str] = Query(None, description="Filter by alert status"),
    assigned_to: Optional[str] = Query(None, description="Filter by assigned user"),
    hours: int = Query(24, description="Number of hours to retrieve"),
    db: Session = Depends(get_db)
):
    """Get system alerts with filtering"""
    time_threshold = datetime.utcnow() - timedelta(hours=hours)
    
    query = db.query(SystemAlert).filter(SystemAlert.triggered_at >= time_threshold)
    
    if alert_level:
        query = query.filter(SystemAlert.alert_level == alert_level)
    if alert_category:
        query = query.filter(SystemAlert.alert_category == alert_category)
    if status:
        query = query.filter(SystemAlert.status == status)
    if assigned_to:
        query = query.filter(SystemAlert.assigned_to == assigned_to)
    
    alerts = query.order_by(desc(SystemAlert.triggered_at)).all()
    return alerts

@router.post("/alerts", response_model=SystemAlertResponse)
async def create_system_alert(alert_data: SystemAlertCreateRequest, db: Session = Depends(get_db)):
    """Create a new system alert"""
    # Parse triggered_at if provided
    triggered_at = datetime.utcnow()
    if alert_data.triggered_at:
        try:
            triggered_at = datetime.fromisoformat(alert_data.triggered_at.replace('Z', '+00:00'))
        except:
            # If parsing fails, use current time
            pass
    
    new_alert = SystemAlert(
        alert_id=alert_data.alert_id,
        alert_level=alert_data.alert_level,
        alert_category=alert_data.alert_category,
        alert_type=alert_data.alert_type,
        alert_source=alert_data.alert_source,
        title=alert_data.title,
        message=alert_data.message,
        triggered_at=triggered_at,
        business_impact=alert_data.business_impact,
        detailed_description=alert_data.detailed_description,
        recommended_actions=alert_data.recommended_actions
    )
    
    db.add(new_alert)
    db.commit()
    db.refresh(new_alert)
    return new_alert

@router.put("/alerts/{alert_id}/acknowledge")
async def acknowledge_alert(alert_id: str, db: Session = Depends(get_db)):
    """Acknowledge a system alert"""
    alert = db.query(SystemAlert).filter(SystemAlert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    
    # Find a valid user to use as acknowledged_by
    existing_user = db.query(User).first()
    
    alert.status = "acknowledged"
    alert.acknowledged_at = datetime.utcnow()
    if existing_user:
        alert.acknowledged_by = existing_user.id
    
    db.commit()
    db.refresh(alert)
    return {"message": "Alert acknowledged successfully"}

@router.put("/alerts/{alert_id}/resolve")
async def resolve_alert(alert_id: str, resolution_notes: Optional[str] = None, db: Session = Depends(get_db)):
    """Resolve a system alert"""
    alert = db.query(SystemAlert).filter(SystemAlert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    
    # Find a valid user to use as resolved_by
    existing_user = db.query(User).first()
    
    alert.status = "resolved"
    alert.resolved_at = datetime.utcnow()
    alert.resolution_notes = resolution_notes
    if existing_user:
        alert.resolved_by = existing_user.id
    
    db.commit()
    db.refresh(alert)
    return {"message": "Alert resolved successfully"}

# MONITORING DASHBOARDS ENDPOINTS

@router.get("/dashboards", response_model=List[MonitoringDashboardResponse])
async def get_monitoring_dashboards(
    dashboard_type: Optional[str] = Query(None, description="Filter by dashboard type"),
    created_by: Optional[str] = Query(None, description="Filter by creator"),
    is_public: Optional[bool] = Query(None, description="Filter by public status"),
    db: Session = Depends(get_db)
):
    """Get monitoring dashboards with filtering"""
    query = db.query(MonitoringDashboard)
    
    if dashboard_type:
        query = query.filter(MonitoringDashboard.dashboard_type == dashboard_type)
    if created_by:
        query = query.filter(MonitoringDashboard.created_by == created_by)
    if is_public is not None:
        query = query.filter(MonitoringDashboard.is_public == is_public)
    
    dashboards = query.order_by(desc(MonitoringDashboard.created_at)).all()
    return dashboards

@router.post("/dashboards", response_model=MonitoringDashboardResponse)
async def create_monitoring_dashboard(dashboard_data: MonitoringDashboardCreateRequest, db: Session = Depends(get_db)):
    """Create a new monitoring dashboard"""
    # Verify user exists
    user = db.query(User).filter(User.id == dashboard_data.created_by).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    new_dashboard = MonitoringDashboard(
        dashboard_name=dashboard_data.dashboard_name,
        dashboard_type=dashboard_data.dashboard_type,
        created_by=dashboard_data.created_by,
        layout_config=dashboard_data.layout_config,
        refresh_interval_seconds=dashboard_data.refresh_interval_seconds,
        auto_refresh_enabled=dashboard_data.auto_refresh_enabled,
        is_public=dashboard_data.is_public,
        widgets=dashboard_data.widgets
    )
    
    # Set widget count if widgets provided
    if dashboard_data.widgets:
        new_dashboard.widget_count = len(dashboard_data.widgets)
    
    db.add(new_dashboard)
    db.commit()
    db.refresh(new_dashboard)
    return new_dashboard

@router.get("/dashboards/{dashboard_id}", response_model=MonitoringDashboardResponse)
async def get_monitoring_dashboard(dashboard_id: str, db: Session = Depends(get_db)):
    """Get a specific monitoring dashboard"""
    dashboard = db.query(MonitoringDashboard).filter(MonitoringDashboard.id == dashboard_id).first()
    if not dashboard:
        raise HTTPException(status_code=404, detail="Monitoring dashboard not found")
    
    # Increment view count
    dashboard.view_count += 1
    dashboard.last_viewed = datetime.utcnow()
    db.commit()
    
    return dashboard

# SYSTEM MONITORING ANALYTICS ENDPOINTS

@router.get("/analytics/system-overview")
async def get_system_monitoring_overview(
    hours: int = Query(24, description="Number of hours for analysis"),
    db: Session = Depends(get_db)
):
    """Get comprehensive system monitoring overview"""
    time_threshold = datetime.utcnow() - timedelta(hours=hours)
    
    # Get latest system health
    latest_health = db.query(SystemHealthMonitoring).order_by(desc(SystemHealthMonitoring.timestamp)).first()
    
    # Get service metrics
    service_metrics = db.query(ServiceHealthMetric).filter(
        ServiceHealthMetric.timestamp >= time_threshold
    ).all()
    
    # Get alerts
    alerts = db.query(SystemAlert).filter(
        SystemAlert.triggered_at >= time_threshold
    ).all()
    
    # Calculate service status distribution
    service_status_counts = {}
    if service_metrics:
        for metric in service_metrics:
            status = metric.service_status.value if hasattr(metric.service_status, 'value') else metric.service_status
            service_status_counts[status] = service_status_counts.get(status, 0) + 1
    
    # Calculate alert distribution
    alert_level_counts = {}
    active_alerts = 0
    if alerts:
        for alert in alerts:
            level = alert.alert_level.value if hasattr(alert.alert_level, 'value') else alert.alert_level
            alert_level_counts[level] = alert_level_counts.get(level, 0) + 1
            if alert.status == "active":
                active_alerts += 1
    
    return {
        "analysis_period_hours": hours,
        "system_health": {
            "overall_health_score": latest_health.overall_health_score if latest_health else 0,
            "system_status": latest_health.system_status if latest_health else "unknown",
            "availability_percentage": latest_health.availability_percentage if latest_health else 0,
            "last_updated": latest_health.timestamp if latest_health else None
        },
        "services_summary": {
            "total_services_monitored": len(set([m.service_name for m in service_metrics])),
            "service_status_distribution": service_status_counts,
            "metrics_collected": len(service_metrics)
        },
        "alerts_summary": {
            "total_alerts": len(alerts),
            "active_alerts": active_alerts,
            "alert_level_distribution": alert_level_counts,
            "alert_rate_per_hour": len(alerts) / hours if hours > 0 else 0
        },
        "timestamp": datetime.utcnow()
    }

@router.get("/analytics/service-performance")
async def get_service_performance_analytics(
    service_name: Optional[str] = Query(None, description="Filter by service name"),
    hours: int = Query(24, description="Number of hours for analysis"),
    db: Session = Depends(get_db)
):
    """Get service performance analytics"""
    time_threshold = datetime.utcnow() - timedelta(hours=hours)
    
    query = db.query(ServiceHealthMetric).filter(ServiceHealthMetric.timestamp >= time_threshold)
    if service_name:
        query = query.filter(ServiceHealthMetric.service_name == service_name)
    
    service_metrics = query.all()
    
    if not service_metrics:
        return {
            "analysis_period_hours": hours,
            "service_performance": "No service data available",
            "metrics_analyzed": 0
        }
    
    # Calculate performance metrics
    response_times = [m.response_time_avg_ms for m in service_metrics if m.response_time_avg_ms]
    success_rates = [m.success_rate_percentage for m in service_metrics if m.success_rate_percentage]
    uptime_percentages = [m.uptime_percentage for m in service_metrics if m.uptime_percentage]
    cpu_utilizations = [m.cpu_utilization_percentage for m in service_metrics if m.cpu_utilization_percentage]
    
    avg_response_time = sum(response_times) / len(response_times) if response_times else 0
    avg_success_rate = sum(success_rates) / len(success_rates) if success_rates else 0
    avg_uptime = sum(uptime_percentages) / len(uptime_percentages) if uptime_percentages else 0
    avg_cpu = sum(cpu_utilizations) / len(cpu_utilizations) if cpu_utilizations else 0
    
    # Group by service name
    service_summary = {}
    for metric in service_metrics:
        service = metric.service_name
        if service not in service_summary:
            service_summary[service] = {
                "service_name": service,
                "service_type": metric.service_type,
                "metrics_count": 0,
                "latest_status": None
            }
        service_summary[service]["metrics_count"] += 1
        service_summary[service]["latest_status"] = metric.service_status
    
    return {
        "analysis_period_hours": hours,
        "metrics_analyzed": len(service_metrics),
        "performance_summary": {
            "average_response_time_ms": avg_response_time,
            "average_success_rate": avg_success_rate,
            "average_uptime_percentage": avg_uptime,
            "average_cpu_utilization": avg_cpu
        },
        "services_analyzed": list(service_summary.values()),
        "unique_services_count": len(service_summary)
    }