"""
Admin Dashboard & System Management API Router
Handles admin metrics, site performance, system health, activity logs, and executive reports
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
    AdminDashboardMetric, SitePerformanceSummary, SystemHealthLog, AdminActivityLog, ExecutiveReport,
    Site, User, Camera, Alert
)
from schemas import (
    AdminDashboardMetricResponse, AdminDashboardMetricCreateRequest,
    SitePerformanceSummaryResponse, SitePerformanceSummaryCreateRequest,
    SystemHealthLogResponse, SystemHealthLogCreateRequest,
    AdminActivityLogResponse, AdminActivityLogCreateRequest,
    ExecutiveReportResponse, ExecutiveReportCreateRequest
)

router = APIRouter(prefix="/admin", tags=["Admin Dashboard & System Management"])

# ADMIN DASHBOARD METRICS ENDPOINTS

@router.get("/dashboard-metrics", response_model=List[AdminDashboardMetricResponse])
async def get_admin_dashboard_metrics(
    aggregation_level: Optional[str] = Query(None, description="Filter by aggregation level"),
    days: int = Query(30, description="Number of days to retrieve"),
    db: Session = Depends(get_db)
):
    """Get admin dashboard metrics"""
    date_threshold = datetime.utcnow().date() - timedelta(days=days)
    
    query = db.query(AdminDashboardMetric).filter(AdminDashboardMetric.metric_date >= date_threshold)
    
    if aggregation_level:
        query = query.filter(AdminDashboardMetric.aggregation_level == aggregation_level)
    
    metrics = query.order_by(desc(AdminDashboardMetric.metric_date), AdminDashboardMetric.metric_hour).all()
    return metrics

@router.post("/dashboard-metrics", response_model=AdminDashboardMetricResponse)
async def create_admin_dashboard_metric(metric_data: AdminDashboardMetricCreateRequest, db: Session = Depends(get_db)):
    """Create a new admin dashboard metric"""
    # Parse date
    metric_date = datetime.strptime(metric_data.metric_date, "%Y-%m-%d").date()
    
    new_metric = AdminDashboardMetric(
        metric_date=metric_date,
        metric_hour=metric_data.metric_hour,
        aggregation_level=metric_data.aggregation_level,
        total_users=metric_data.total_users,
        active_users_24h=metric_data.active_users_24h,
        total_sites=metric_data.total_sites,
        active_sites=metric_data.active_sites,
        total_cameras=metric_data.total_cameras,
        online_cameras=metric_data.online_cameras
    )
    
    db.add(new_metric)
    db.commit()
    db.refresh(new_metric)
    return new_metric

@router.get("/dashboard-metrics/current")
async def get_current_dashboard_metrics(db: Session = Depends(get_db)):
    """Get real-time dashboard metrics calculated from current data"""
    
    # Calculate current metrics from database
    total_users = db.query(User).count()
    total_sites = db.query(Site).count()
    active_sites = db.query(Site).filter(Site.status == "active").count()
    total_cameras = db.query(Camera).count()
    online_cameras = db.query(Camera).filter(Camera.status == "online").count()
    
    # Get recent activity (last 24 hours)
    yesterday = datetime.utcnow() - timedelta(hours=24)
    
    # For active users, we'd need session/login tracking - using a simplified approach
    active_users_24h = total_users  # Placeholder - would need proper session tracking
    
    # Calculate system health metrics
    camera_uptime = (online_cameras / total_cameras * 100) if total_cameras > 0 else 100
    site_availability = (active_sites / total_sites * 100) if total_sites > 0 else 100
    
    return {
        "timestamp": datetime.utcnow(),
        "system_overview": {
            "total_users": total_users,
            "active_users_24h": active_users_24h,
            "total_sites": total_sites,
            "active_sites": active_sites,
            "total_cameras": total_cameras,
            "online_cameras": online_cameras
        },
        "performance_indicators": {
            "camera_uptime_percentage": camera_uptime,
            "site_availability_percentage": site_availability,
            "system_health_score": min(camera_uptime, site_availability)
        },
        "alerts_summary": {
            "total_alerts_today": 0,  # Would calculate from alerts table
            "pending_alerts": 0,
            "resolved_alerts": 0
        }
    }

# SITE PERFORMANCE SUMMARY ENDPOINTS

@router.get("/site-performance", response_model=List[SitePerformanceSummaryResponse])
async def get_site_performance_summaries(
    site_id: Optional[str] = Query(None, description="Filter by site ID"),
    summary_period: Optional[str] = Query(None, description="Filter by summary period"),
    days: int = Query(30, description="Number of days to retrieve"),
    db: Session = Depends(get_db)
):
    """Get site performance summaries"""
    date_threshold = datetime.utcnow().date() - timedelta(days=days)
    
    query = db.query(SitePerformanceSummary).filter(SitePerformanceSummary.summary_date >= date_threshold)
    
    if site_id:
        query = query.filter(SitePerformanceSummary.site_id == site_id)
    if summary_period:
        query = query.filter(SitePerformanceSummary.summary_period == summary_period)
    
    summaries = query.order_by(desc(SitePerformanceSummary.summary_date)).all()
    return summaries

@router.post("/site-performance", response_model=SitePerformanceSummaryResponse)
async def create_site_performance_summary(summary_data: SitePerformanceSummaryCreateRequest, db: Session = Depends(get_db)):
    """Create a new site performance summary"""
    # Verify site exists
    site = db.query(Site).filter(Site.id == summary_data.site_id).first()
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    
    # Parse date
    summary_date = datetime.strptime(summary_data.summary_date, "%Y-%m-%d").date()
    
    new_summary = SitePerformanceSummary(
        site_id=summary_data.site_id,
        summary_date=summary_date,
        summary_period=summary_data.summary_period,
        personnel_count=summary_data.personnel_count,
        camera_count=summary_data.camera_count,
        online_cameras=summary_data.online_cameras,
        safety_score=summary_data.safety_score,
        notes=summary_data.notes
    )
    
    db.add(new_summary)
    db.commit()
    db.refresh(new_summary)
    return new_summary

@router.get("/site-performance/{site_id}/trend")
async def get_site_performance_trend(
    site_id: str,
    days: int = Query(90, description="Number of days for trend analysis"),
    db: Session = Depends(get_db)
):
    """Get site performance trend analysis"""
    # Verify site exists
    site = db.query(Site).filter(Site.id == site_id).first()
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    
    date_threshold = datetime.utcnow().date() - timedelta(days=days)
    
    summaries = db.query(SitePerformanceSummary).filter(
        and_(
            SitePerformanceSummary.site_id == site_id,
            SitePerformanceSummary.summary_date >= date_threshold
        )
    ).order_by(SitePerformanceSummary.summary_date).all()
    
    if not summaries:
        return {
            "site_id": site_id,
            "analysis_period_days": days,
            "trend_data": [],
            "trend_summary": "No data available"
        }
    
    # Calculate trend metrics
    trend_data = []
    for summary in summaries:
        trend_data.append({
            "date": summary.summary_date.isoformat(),
            "safety_score": summary.safety_score,
            "compliance_score": summary.compliance_score,
            "efficiency_score": summary.efficiency_score,
            "camera_uptime": (summary.online_cameras / summary.camera_count * 100) if summary.camera_count > 0 else 100
        })
    
    # Simple trend analysis
    recent_avg_safety = sum([d["safety_score"] for d in trend_data[-7:] if d["safety_score"]]) / 7
    early_avg_safety = sum([d["safety_score"] for d in trend_data[:7] if d["safety_score"]]) / 7
    
    safety_trend = "improving" if recent_avg_safety > early_avg_safety else "declining" if recent_avg_safety < early_avg_safety else "stable"
    
    return {
        "site_id": site_id,
        "site_name": site.name,
        "analysis_period_days": days,
        "trend_data": trend_data,
        "trend_summary": {
            "safety_trend": safety_trend,
            "average_safety_score": recent_avg_safety,
            "total_data_points": len(trend_data)
        }
    }

# SYSTEM HEALTH LOGS ENDPOINTS

@router.get("/system-health", response_model=List[SystemHealthLogResponse])
async def get_system_health_logs(
    server_id: Optional[str] = Query(None, description="Filter by server ID"),
    component_type: Optional[str] = Query(None, description="Filter by component type"),
    service_status: Optional[str] = Query(None, description="Filter by service status"),
    hours: int = Query(24, description="Number of hours to retrieve"),
    db: Session = Depends(get_db)
):
    """Get system health logs"""
    time_threshold = datetime.utcnow() - timedelta(hours=hours)
    
    query = db.query(SystemHealthLog).filter(SystemHealthLog.measurement_timestamp >= time_threshold)
    
    if server_id:
        query = query.filter(SystemHealthLog.server_id == server_id)
    if component_type:
        query = query.filter(SystemHealthLog.component_type == component_type)
    if service_status:
        query = query.filter(SystemHealthLog.service_status == service_status)
    
    logs = query.order_by(desc(SystemHealthLog.measurement_timestamp)).all()
    return logs

@router.post("/system-health", response_model=SystemHealthLogResponse)
async def create_system_health_log(health_data: SystemHealthLogCreateRequest, db: Session = Depends(get_db)):
    """Create a new system health log entry"""
    new_log = SystemHealthLog(
        server_id=health_data.server_id,
        component_type=health_data.component_type,
        cpu_usage_percentage=health_data.cpu_usage_percentage,
        memory_usage_percentage=health_data.memory_usage_percentage,
        disk_usage_percentage=health_data.disk_usage_percentage,
        response_time_ms=health_data.response_time_ms,
        service_status=health_data.service_status,
        monitoring_source=health_data.monitoring_source
    )
    
    db.add(new_log)
    db.commit()
    db.refresh(new_log)
    return new_log

@router.get("/system-health/summary")
async def get_system_health_summary(
    hours: int = Query(24, description="Number of hours for analysis"),
    db: Session = Depends(get_db)
):
    """Get system health summary"""
    time_threshold = datetime.utcnow() - timedelta(hours=hours)
    
    logs = db.query(SystemHealthLog).filter(SystemHealthLog.measurement_timestamp >= time_threshold).all()
    
    if not logs:
        return {
            "analysis_period_hours": hours,
            "total_measurements": 0,
            "system_health": "No data available"
        }
    
    # Calculate summary metrics
    total_logs = len(logs)
    healthy_logs = len([log for log in logs if log.service_status == "healthy"])
    degraded_logs = len([log for log in logs if log.service_status == "degraded"])
    unhealthy_logs = len([log for log in logs if log.service_status == "unhealthy"])
    
    avg_cpu = sum([log.cpu_usage_percentage for log in logs if log.cpu_usage_percentage]) / len([log for log in logs if log.cpu_usage_percentage]) if any(log.cpu_usage_percentage for log in logs) else 0
    avg_memory = sum([log.memory_usage_percentage for log in logs if log.memory_usage_percentage]) / len([log for log in logs if log.memory_usage_percentage]) if any(log.memory_usage_percentage for log in logs) else 0
    
    # Overall health score (percentage of healthy measurements)
    health_score = (healthy_logs / total_logs * 100) if total_logs > 0 else 100
    
    return {
        "analysis_period_hours": hours,
        "total_measurements": total_logs,
        "health_distribution": {
            "healthy": healthy_logs,
            "degraded": degraded_logs,
            "unhealthy": unhealthy_logs
        },
        "resource_utilization": {
            "average_cpu_percentage": avg_cpu,
            "average_memory_percentage": avg_memory
        },
        "overall_health_score": health_score,
        "status": "healthy" if health_score >= 90 else "degraded" if health_score >= 70 else "unhealthy"
    }

# ADMIN ACTIVITY LOGS ENDPOINTS

@router.get("/activity-logs", response_model=List[AdminActivityLogResponse])
async def get_admin_activity_logs(
    admin_user_id: Optional[str] = Query(None, description="Filter by admin user ID"),
    activity_type: Optional[str] = Query(None, description="Filter by activity type"),
    impact_level: Optional[str] = Query(None, description="Filter by impact level"),
    days: int = Query(30, description="Number of days to retrieve"),
    db: Session = Depends(get_db)
):
    """Get admin activity logs"""
    date_threshold = datetime.utcnow() - timedelta(days=days)
    
    query = db.query(AdminActivityLog).filter(AdminActivityLog.created_at >= date_threshold)
    
    if admin_user_id:
        query = query.filter(AdminActivityLog.admin_user_id == admin_user_id)
    if activity_type:
        query = query.filter(AdminActivityLog.activity_type == activity_type)
    if impact_level:
        query = query.filter(AdminActivityLog.impact_level == impact_level)
    
    logs = query.order_by(desc(AdminActivityLog.created_at)).all()
    return logs

@router.post("/activity-logs", response_model=AdminActivityLogResponse)
async def create_admin_activity_log(activity_data: AdminActivityLogCreateRequest, db: Session = Depends(get_db)):
    """Create a new admin activity log"""
    # Verify admin user exists
    admin_user = db.query(User).filter(User.id == activity_data.admin_user_id).first()
    if not admin_user:
        raise HTTPException(status_code=404, detail="Admin user not found")
    
    new_log = AdminActivityLog(
        admin_user_id=activity_data.admin_user_id,
        activity_type=activity_data.activity_type,
        action=activity_data.action,
        resource_type=activity_data.resource_type,
        resource_id=activity_data.resource_id,
        resource_name=activity_data.resource_name,
        old_values=activity_data.old_values,
        new_values=activity_data.new_values,
        change_summary=activity_data.change_summary,
        ip_address=activity_data.ip_address,
        impact_level=activity_data.impact_level
    )
    
    db.add(new_log)
    db.commit()
    db.refresh(new_log)
    return new_log

# EXECUTIVE REPORTS ENDPOINTS

@router.get("/executive-reports", response_model=List[ExecutiveReportResponse])
async def get_executive_reports(
    report_type: Optional[str] = Query(None, description="Filter by report type"),
    report_status: Optional[str] = Query(None, description="Filter by report status"),
    days: int = Query(90, description="Number of days to retrieve"),
    db: Session = Depends(get_db)
):
    """Get executive reports"""
    date_threshold = datetime.utcnow() - timedelta(days=days)
    
    query = db.query(ExecutiveReport).filter(ExecutiveReport.created_at >= date_threshold)
    
    if report_type:
        query = query.filter(ExecutiveReport.report_type == report_type)
    if report_status:
        query = query.filter(ExecutiveReport.report_status == report_status)
    
    reports = query.order_by(desc(ExecutiveReport.created_at)).all()
    return reports

@router.post("/executive-reports", response_model=ExecutiveReportResponse)
async def create_executive_report(report_data: ExecutiveReportCreateRequest, db: Session = Depends(get_db)):
    """Create a new executive report"""
    # Verify user exists
    user = db.query(User).filter(User.id == report_data.generated_by).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Parse dates
    start_date = datetime.strptime(report_data.reporting_period_start, "%Y-%m-%d").date()
    end_date = datetime.strptime(report_data.reporting_period_end, "%Y-%m-%d").date()
    
    new_report = ExecutiveReport(
        report_name=report_data.report_name,
        report_type=report_data.report_type,
        reporting_period_start=start_date,
        reporting_period_end=end_date,
        generated_by=report_data.generated_by,
        executive_summary=report_data.executive_summary,
        included_sites=report_data.included_sites,
        confidentiality_level=report_data.confidentiality_level,
        report_file_format=report_data.report_file_format
    )
    
    db.add(new_report)
    db.commit()
    db.refresh(new_report)
    return new_report

@router.get("/executive-reports/{report_id}", response_model=ExecutiveReportResponse)
async def get_executive_report(report_id: str, db: Session = Depends(get_db)):
    """Get a specific executive report"""
    report = db.query(ExecutiveReport).filter(ExecutiveReport.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Executive report not found")
    
    # Increment view count
    report.view_count += 1
    report.last_accessed = datetime.utcnow()
    db.commit()
    
    return report

@router.put("/executive-reports/{report_id}/complete")
async def complete_executive_report(report_id: str, db: Session = Depends(get_db)):
    """Mark an executive report as completed"""
    report = db.query(ExecutiveReport).filter(ExecutiveReport.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Executive report not found")
    
    report.report_status = "completed"
    report.generation_duration_seconds = int((datetime.utcnow() - report.generation_timestamp).total_seconds())
    
    db.commit()
    db.refresh(report)
    return {"message": "Executive report marked as completed"}

# ADMIN ANALYTICS ENDPOINTS

@router.get("/analytics/system-overview")
async def get_system_overview_analytics(
    days: int = Query(30, description="Number of days for analysis"),
    db: Session = Depends(get_db)
):
    """Get comprehensive system overview analytics for admin dashboard"""
    date_threshold = datetime.utcnow().date() - timedelta(days=days)
    
    # Get recent dashboard metrics
    recent_metrics = db.query(AdminDashboardMetric).filter(
        AdminDashboardMetric.metric_date >= date_threshold
    ).order_by(desc(AdminDashboardMetric.metric_date)).first()
    
    # Get system health summary
    health_logs = db.query(SystemHealthLog).filter(
        SystemHealthLog.measurement_timestamp >= datetime.utcnow() - timedelta(hours=24)
    ).all()
    
    healthy_systems = len([log for log in health_logs if log.service_status == "healthy"])
    total_systems = len(health_logs) if health_logs else 1
    system_health_percentage = (healthy_systems / total_systems * 100) if total_systems > 0 else 100
    
    # Get activity summary
    recent_activities = db.query(AdminActivityLog).filter(
        AdminActivityLog.created_at >= datetime.utcnow() - timedelta(days=7)
    ).count()
    
    critical_activities = db.query(AdminActivityLog).filter(
        and_(
            AdminActivityLog.created_at >= datetime.utcnow() - timedelta(days=7),
            AdminActivityLog.impact_level == "critical"
        )
    ).count()
    
    return {
        "analysis_period_days": days,
        "current_metrics": {
            "total_users": recent_metrics.total_users if recent_metrics else 0,
            "total_sites": recent_metrics.total_sites if recent_metrics else 0,
            "total_cameras": recent_metrics.total_cameras if recent_metrics else 0,
            "system_uptime_percentage": recent_metrics.system_uptime_percentage if recent_metrics else 100,
            "overall_safety_score": recent_metrics.overall_safety_score if recent_metrics else 100
        },
        "system_health": {
            "health_percentage": system_health_percentage,
            "status": "healthy" if system_health_percentage >= 90 else "degraded",
            "total_monitored_components": total_systems
        },
        "activity_summary": {
            "recent_admin_activities": recent_activities,
            "critical_activities_last_week": critical_activities
        },
        "timestamp": datetime.utcnow()
    }