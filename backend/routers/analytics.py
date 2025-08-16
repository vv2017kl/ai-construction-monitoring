"""
Complete Analytics & Reporting API Router
Handles analytics, reporting, certifications, performance metrics, and dashboard widgets
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
    UserCertification, PerformanceMetric, TrendAnalysis, ReportTemplate, DashboardWidget,
    Site, User, Report, AnalyticsCache
)
from schemas import (
    UserCertificationResponse, UserCertificationCreateRequest,
    PerformanceMetricResponse, PerformanceMetricCreateRequest,
    TrendAnalysisResponse, TrendAnalysisCreateRequest,
    ReportTemplateResponse, ReportTemplateCreateRequest,
    DashboardWidgetResponse, DashboardWidgetCreateRequest,
    ReportResponse, ReportCreateRequest
)

router = APIRouter(prefix="/analytics", tags=["Complete Analytics & Reporting"])

# USER CERTIFICATIONS ENDPOINTS

@router.get("/certifications", response_model=List[UserCertificationResponse])
async def get_user_certifications(
    user_id: Optional[str] = Query(None, description="Filter by user ID"),
    certification_type: Optional[str] = Query(None, description="Filter by certification type"),
    status: Optional[str] = Query(None, description="Filter by certification status"),
    expiring_within_days: Optional[int] = Query(None, description="Show certifications expiring within X days"),
    db: Session = Depends(get_db)
):
    """Get all user certifications with filtering options"""
    query = db.query(UserCertification)
    
    if user_id:
        query = query.filter(UserCertification.user_id == user_id)
    if certification_type:
        query = query.filter(UserCertification.certification_type == certification_type)
    if status:
        query = query.filter(UserCertification.status == status)
    if expiring_within_days:
        expiry_threshold = datetime.utcnow().date() + timedelta(days=expiring_within_days)
        query = query.filter(
            and_(
                UserCertification.expiry_date.isnot(None),
                UserCertification.expiry_date <= expiry_threshold
            )
        )
    
    certifications = query.order_by(desc(UserCertification.created_at)).all()
    return certifications

@router.post("/certifications", response_model=UserCertificationResponse)
async def create_user_certification(cert_data: UserCertificationCreateRequest, db: Session = Depends(get_db)):
    """Create a new user certification"""
    # Verify user exists
    user = db.query(User).filter(User.id == cert_data.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Find a valid user to use as created_by
    existing_user = db.query(User).first()
    if not existing_user:
        raise HTTPException(status_code=400, detail="No users found in system")
    
    # Parse dates
    issue_date = datetime.strptime(cert_data.issue_date, "%Y-%m-%d").date()
    expiry_date = None
    if cert_data.expiry_date:
        expiry_date = datetime.strptime(cert_data.expiry_date, "%Y-%m-%d").date()
    
    new_certification = UserCertification(
        user_id=cert_data.user_id,
        certification_name=cert_data.certification_name,
        certification_type=cert_data.certification_type,
        certification_number=cert_data.certification_number,
        issuing_authority=cert_data.issuing_authority,
        issue_date=issue_date,
        expiry_date=expiry_date,
        renewal_period_months=cert_data.renewal_period_months,
        required_for_roles=cert_data.required_for_roles,
        certificate_file_path=cert_data.certificate_file_path,
        created_by=existing_user.id
    )
    
    db.add(new_certification)
    db.commit()
    db.refresh(new_certification)
    return new_certification

@router.get("/certifications/{certification_id}", response_model=UserCertificationResponse)
async def get_user_certification(certification_id: str, db: Session = Depends(get_db)):
    """Get a specific user certification"""
    certification = db.query(UserCertification).filter(UserCertification.id == certification_id).first()
    if not certification:
        raise HTTPException(status_code=404, detail="User certification not found")
    return certification

@router.put("/certifications/{certification_id}/verify")
async def verify_certification(certification_id: str, db: Session = Depends(get_db)):
    """Mark a certification as verified"""
    certification = db.query(UserCertification).filter(UserCertification.id == certification_id).first()
    if not certification:
        raise HTTPException(status_code=404, detail="User certification not found")
    
    certification.verification_status = "verified"
    certification.last_verification_check = datetime.utcnow().date()
    
    db.commit()
    db.refresh(certification)
    return {"message": "Certification verified successfully"}

# PERFORMANCE METRICS ENDPOINTS

@router.get("/performance-metrics", response_model=List[PerformanceMetricResponse])
async def get_performance_metrics(
    site_id: Optional[str] = Query(None, description="Filter by site ID"),
    metric_type: Optional[str] = Query(None, description="Filter by metric type"),
    days: int = Query(30, description="Number of days to retrieve"),
    is_kpi: Optional[bool] = Query(None, description="Filter by KPI status"),
    db: Session = Depends(get_db)
):
    """Get performance metrics with filtering"""
    date_threshold = datetime.utcnow().date() - timedelta(days=days)
    
    query = db.query(PerformanceMetric).filter(PerformanceMetric.metric_date >= date_threshold)
    
    if site_id:
        query = query.filter(PerformanceMetric.site_id == site_id)
    if metric_type:
        query = query.filter(PerformanceMetric.metric_type == metric_type)
    if is_kpi is not None:
        query = query.filter(PerformanceMetric.is_kpi == is_kpi)
    
    metrics = query.order_by(desc(PerformanceMetric.metric_date), desc(PerformanceMetric.metric_hour)).all()
    return metrics

@router.post("/performance-metrics", response_model=PerformanceMetricResponse)
async def create_performance_metric(metric_data: PerformanceMetricCreateRequest, db: Session = Depends(get_db)):
    """Create a new performance metric"""
    # Verify site exists
    site = db.query(Site).filter(Site.id == metric_data.site_id).first()
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    
    # Find a valid user to use as calculated_by
    existing_user = db.query(User).first()
    
    # Parse date
    metric_date = datetime.strptime(metric_data.metric_date, "%Y-%m-%d").date()
    
    new_metric = PerformanceMetric(
        site_id=metric_data.site_id,
        metric_date=metric_date,
        metric_hour=metric_data.metric_hour,
        metric_type=metric_data.metric_type,
        metric_value=metric_data.metric_value,
        target_value=metric_data.target_value,
        measurement_unit=metric_data.measurement_unit,
        data_source=metric_data.data_source,
        is_kpi=metric_data.is_kpi,
        confidence_score=metric_data.confidence_score,
        calculated_by=existing_user.id if existing_user else None
    )
    
    db.add(new_metric)
    db.commit()
    db.refresh(new_metric)
    return new_metric

# TREND ANALYSIS ENDPOINTS

@router.get("/trend-analyses", response_model=List[TrendAnalysisResponse])
async def get_trend_analyses(
    site_id: Optional[str] = Query(None, description="Filter by site ID"),
    analysis_type: Optional[str] = Query(None, description="Filter by analysis type"),
    days: int = Query(90, description="Number of days to look back"),
    db: Session = Depends(get_db)
):
    """Get trend analyses with filtering"""
    date_threshold = datetime.utcnow().date() - timedelta(days=days)
    
    query = db.query(TrendAnalysis).filter(TrendAnalysis.start_date >= date_threshold)
    
    if site_id:
        query = query.filter(TrendAnalysis.site_id == site_id)
    if analysis_type:
        query = query.filter(TrendAnalysis.analysis_type == analysis_type)
    
    analyses = query.order_by(desc(TrendAnalysis.created_at)).all()
    return analyses

@router.post("/trend-analyses", response_model=TrendAnalysisResponse)
async def create_trend_analysis(analysis_data: TrendAnalysisCreateRequest, db: Session = Depends(get_db)):
    """Create a new trend analysis"""
    # Verify site exists if provided
    if analysis_data.site_id:
        site = db.query(Site).filter(Site.id == analysis_data.site_id).first()
        if not site:
            raise HTTPException(status_code=404, detail="Site not found")
    
    # Find a valid user to use as created_by
    existing_user = db.query(User).first()
    if not existing_user:
        raise HTTPException(status_code=400, detail="No users found in system")
    
    # Parse dates
    start_date = datetime.strptime(analysis_data.start_date, "%Y-%m-%d").date()
    end_date = datetime.strptime(analysis_data.end_date, "%Y-%m-%d").date()
    
    # Calculate period days
    analysis_period_days = (end_date - start_date).days
    
    new_analysis = TrendAnalysis(
        site_id=analysis_data.site_id,
        analysis_name=analysis_data.analysis_name,
        analysis_type=analysis_data.analysis_type,
        start_date=start_date,
        end_date=end_date,
        analysis_period_days=analysis_period_days,
        analysis_algorithm=analysis_data.analysis_algorithm,
        forecast_horizon_days=analysis_data.forecast_horizon_days,
        created_by=existing_user.id
    )
    
    db.add(new_analysis)
    db.commit()
    db.refresh(new_analysis)
    return new_analysis

# REPORT TEMPLATES ENDPOINTS

@router.get("/report-templates", response_model=List[ReportTemplateResponse])
async def get_report_templates(
    template_type: Optional[str] = Query(None, description="Filter by template type"),
    is_active: Optional[bool] = Query(True, description="Filter by active status"),
    is_public: Optional[bool] = Query(None, description="Filter by public status"),
    db: Session = Depends(get_db)
):
    """Get report templates with filtering"""
    query = db.query(ReportTemplate)
    
    if template_type:
        query = query.filter(ReportTemplate.template_type == template_type)
    if is_active is not None:
        query = query.filter(ReportTemplate.is_active == is_active)
    if is_public is not None:
        query = query.filter(ReportTemplate.is_public == is_public)
    
    templates = query.order_by(desc(ReportTemplate.usage_count), desc(ReportTemplate.created_at)).all()
    return templates

@router.post("/report-templates", response_model=ReportTemplateResponse)
async def create_report_template(template_data: ReportTemplateCreateRequest, db: Session = Depends(get_db)):
    """Create a new report template"""
    # Find a valid user to use as created_by
    existing_user = db.query(User).first()
    if not existing_user:
        raise HTTPException(status_code=400, detail="No users found in system")
    
    new_template = ReportTemplate(
        template_name=template_data.template_name,
        template_type=template_data.template_type,
        description=template_data.description,
        template_structure=template_data.template_structure,
        default_parameters=template_data.default_parameters,
        required_parameters=template_data.required_parameters,
        supported_formats=template_data.supported_formats,
        is_public=template_data.is_public,
        created_by=existing_user.id
    )
    
    db.add(new_template)
    db.commit()
    db.refresh(new_template)
    return new_template

# DASHBOARD WIDGETS ENDPOINTS

@router.get("/dashboard-widgets", response_model=List[DashboardWidgetResponse])
async def get_dashboard_widgets(
    user_id: Optional[str] = Query(None, description="Filter by user ID"),
    dashboard_tab: Optional[str] = Query(None, description="Filter by dashboard tab"),
    widget_type: Optional[str] = Query(None, description="Filter by widget type"),
    db: Session = Depends(get_db)
):
    """Get dashboard widgets with filtering"""
    query = db.query(DashboardWidget)
    
    if user_id:
        query = query.filter(DashboardWidget.user_id == user_id)
    if dashboard_tab:
        query = query.filter(DashboardWidget.dashboard_tab == dashboard_tab)
    if widget_type:
        query = query.filter(DashboardWidget.widget_type == widget_type)
    
    widgets = query.filter(DashboardWidget.is_visible == True).order_by(
        DashboardWidget.dashboard_tab,
        DashboardWidget.position_y,
        DashboardWidget.position_x
    ).all()
    return widgets

@router.post("/dashboard-widgets", response_model=DashboardWidgetResponse)
async def create_dashboard_widget(widget_data: DashboardWidgetCreateRequest, db: Session = Depends(get_db)):
    """Create a new dashboard widget"""
    # Verify user exists
    user = db.query(User).filter(User.id == widget_data.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    new_widget = DashboardWidget(
        user_id=widget_data.user_id,
        widget_name=widget_data.widget_name,
        widget_type=widget_data.widget_type,
        widget_config=widget_data.widget_config,
        data_source=widget_data.data_source,
        dashboard_tab=widget_data.dashboard_tab,
        position_x=widget_data.position_x,
        position_y=widget_data.position_y,
        width=widget_data.width,
        height=widget_data.height,
        refresh_interval_minutes=widget_data.refresh_interval_minutes
    )
    
    db.add(new_widget)
    db.commit()
    db.refresh(new_widget)
    return new_widget

@router.put("/dashboard-widgets/{widget_id}", response_model=DashboardWidgetResponse)
async def update_dashboard_widget(widget_id: str, widget_data: DashboardWidgetCreateRequest, db: Session = Depends(get_db)):
    """Update a dashboard widget"""
    widget = db.query(DashboardWidget).filter(DashboardWidget.id == widget_id).first()
    if not widget:
        raise HTTPException(status_code=404, detail="Dashboard widget not found")
    
    # Update fields
    for field, value in widget_data.dict(exclude_unset=True).items():
        if field != 'user_id':  # Don't allow changing the user
            setattr(widget, field, value)
    
    db.commit()
    db.refresh(widget)
    return widget

@router.delete("/dashboard-widgets/{widget_id}")
async def delete_dashboard_widget(widget_id: str, db: Session = Depends(get_db)):
    """Delete a dashboard widget"""
    widget = db.query(DashboardWidget).filter(DashboardWidget.id == widget_id).first()
    if not widget:
        raise HTTPException(status_code=404, detail="Dashboard widget not found")
    
    db.delete(widget)
    db.commit()
    return {"message": "Dashboard widget deleted successfully"}

# ANALYTICS SUMMARY ENDPOINTS

@router.get("/summary/kpi-dashboard")
async def get_kpi_dashboard(
    site_id: Optional[str] = Query(None, description="Filter by site ID"),
    days: int = Query(30, description="Number of days for analysis"),
    db: Session = Depends(get_db)
):
    """Get KPI dashboard summary"""
    date_threshold = datetime.utcnow().date() - timedelta(days=days)
    
    query = db.query(PerformanceMetric).filter(
        and_(
            PerformanceMetric.is_kpi == True,
            PerformanceMetric.metric_date >= date_threshold
        )
    )
    
    if site_id:
        query = query.filter(PerformanceMetric.site_id == site_id)
    
    kpi_metrics = query.all()
    
    # Group by metric type and calculate summary
    kpi_summary = {}
    for metric in kpi_metrics:
        if metric.metric_type not in kpi_summary:
            kpi_summary[metric.metric_type] = {
                "metric_type": metric.metric_type,
                "current_value": metric.metric_value,
                "target_value": metric.target_value,
                "measurement_unit": metric.measurement_unit,
                "performance_grade": metric.performance_grade,
                "data_points": 1,
                "latest_date": metric.metric_date.isoformat()
            }
        else:
            # Keep the most recent value
            if metric.metric_date > datetime.strptime(kpi_summary[metric.metric_type]["latest_date"], "%Y-%m-%d").date():
                kpi_summary[metric.metric_type]["current_value"] = metric.metric_value
                kpi_summary[metric.metric_type]["latest_date"] = metric.metric_date.isoformat()
            kpi_summary[metric.metric_type]["data_points"] += 1
    
    return {
        "analysis_period_days": days,
        "total_kpi_metrics": len(kpi_summary),
        "kpi_summary": list(kpi_summary.values())
    }

@router.get("/summary/certification-compliance")
async def get_certification_compliance_summary(
    site_id: Optional[str] = Query(None, description="Filter by site ID"),
    db: Session = Depends(get_db)
):
    """Get certification compliance summary"""
    query = db.query(UserCertification)
    
    # If site filtering is needed, we'd need to join with user-site relationships
    # For now, get all certifications
    
    certifications = query.all()
    
    total_certifications = len(certifications)
    active_certifications = len([c for c in certifications if c.status == "active"])
    expired_certifications = len([c for c in certifications if c.status == "expired"])
    expiring_soon = len([c for c in certifications if c.expiry_date and c.expiry_date <= datetime.utcnow().date() + timedelta(days=30)])
    
    # Group by certification type
    type_summary = {}
    for cert in certifications:
        cert_type = cert.certification_type.value
        if cert_type not in type_summary:
            type_summary[cert_type] = {"total": 0, "active": 0, "expired": 0}
        
        type_summary[cert_type]["total"] += 1
        if cert.status == "active":
            type_summary[cert_type]["active"] += 1
        elif cert.status == "expired":
            type_summary[cert_type]["expired"] += 1
    
    return {
        "total_certifications": total_certifications,
        "active_certifications": active_certifications,
        "expired_certifications": expired_certifications,
        "expiring_within_30_days": expiring_soon,
        "compliance_rate": (active_certifications / total_certifications * 100) if total_certifications > 0 else 100,
        "certification_types": type_summary
    }