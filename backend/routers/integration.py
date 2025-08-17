"""
Integration & User Experience API Router
Handles third-party integrations, user profile settings, application settings, help articles, and user feedback
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
    ThirdPartyIntegration, UserProfileSetting, UserApplicationSetting,
    HelpArticle, UserFeedback, User
)
from schemas import (
    ThirdPartyIntegrationResponse, ThirdPartyIntegrationCreateRequest,
    UserProfileSettingResponse, UserProfileSettingCreateRequest,
    UserApplicationSettingResponse, UserApplicationSettingCreateRequest,
    HelpArticleResponse, HelpArticleCreateRequest,
    UserFeedbackResponse, UserFeedbackCreateRequest
)

router = APIRouter(prefix="/integration", tags=["Integration & User Experience"])

# THIRD PARTY INTEGRATIONS ENDPOINTS

@router.get("/third-party", response_model=List[ThirdPartyIntegrationResponse])
async def get_third_party_integrations(
    integration_type: Optional[str] = Query(None, description="Filter by integration type"),
    provider_name: Optional[str] = Query(None, description="Filter by provider name"),
    status: Optional[str] = Query(None, description="Filter by status"),
    db: Session = Depends(get_db)
):
    """Get all third-party integrations with filtering"""
    query = db.query(ThirdPartyIntegration)
    
    if integration_type:
        query = query.filter(ThirdPartyIntegration.integration_type == integration_type)
    if provider_name:
        query = query.filter(ThirdPartyIntegration.provider_name == provider_name)
    if status:
        query = query.filter(ThirdPartyIntegration.status == status)
    
    integrations = query.order_by(desc(ThirdPartyIntegration.created_at)).all()
    return integrations

@router.post("/third-party", response_model=ThirdPartyIntegrationResponse)
async def create_third_party_integration(integration_data: ThirdPartyIntegrationCreateRequest, db: Session = Depends(get_db)):
    """Create a new third-party integration"""
    # Find a valid user to use as created_by
    existing_user = db.query(User).first()
    if not existing_user:
        raise HTTPException(status_code=400, detail="No users found in system")
    
    new_integration = ThirdPartyIntegration(
        integration_name=integration_data.integration_name,
        integration_type=integration_data.integration_type,
        provider_name=integration_data.provider_name,
        description=integration_data.description,
        configuration=integration_data.configuration,
        endpoints=integration_data.endpoints,
        rate_limits=integration_data.rate_limits,
        monthly_limit=integration_data.monthly_limit,
        created_by=existing_user.id
    )
    
    db.add(new_integration)
    db.commit()
    db.refresh(new_integration)
    return new_integration

@router.get("/third-party/{integration_id}", response_model=ThirdPartyIntegrationResponse)
async def get_third_party_integration(integration_id: str, db: Session = Depends(get_db)):
    """Get a specific third-party integration"""
    integration = db.query(ThirdPartyIntegration).filter(ThirdPartyIntegration.id == integration_id).first()
    if not integration:
        raise HTTPException(status_code=404, detail="Third-party integration not found")
    return integration

@router.put("/third-party/{integration_id}", response_model=ThirdPartyIntegrationResponse)
async def update_third_party_integration(integration_id: str, integration_data: ThirdPartyIntegrationCreateRequest, db: Session = Depends(get_db)):
    """Update a third-party integration"""
    integration = db.query(ThirdPartyIntegration).filter(ThirdPartyIntegration.id == integration_id).first()
    if not integration:
        raise HTTPException(status_code=404, detail="Third-party integration not found")
    
    # Update fields
    for field, value in integration_data.dict(exclude_unset=True).items():
        setattr(integration, field, value)
    
    db.commit()
    db.refresh(integration)
    return integration

@router.put("/third-party/{integration_id}/activate")
async def activate_integration(integration_id: str, db: Session = Depends(get_db)):
    """Activate a third-party integration"""
    integration = db.query(ThirdPartyIntegration).filter(ThirdPartyIntegration.id == integration_id).first()
    if not integration:
        raise HTTPException(status_code=404, detail="Third-party integration not found")
    
    integration.status = "active"
    integration.last_health_check = datetime.utcnow()
    
    db.commit()
    db.refresh(integration)
    return {"message": "Integration activated successfully"}

@router.put("/third-party/{integration_id}/deactivate")
async def deactivate_integration(integration_id: str, db: Session = Depends(get_db)):
    """Deactivate a third-party integration"""
    integration = db.query(ThirdPartyIntegration).filter(ThirdPartyIntegration.id == integration_id).first()
    if not integration:
        raise HTTPException(status_code=404, detail="Third-party integration not found")
    
    integration.status = "inactive"
    
    db.commit()
    db.refresh(integration)
    return {"message": "Integration deactivated successfully"}

# USER PROFILE SETTINGS ENDPOINTS

@router.get("/user-profile-settings", response_model=List[UserProfileSettingResponse])
async def get_user_profile_settings(
    user_id: Optional[str] = Query(None, description="Filter by user ID"),
    db: Session = Depends(get_db)
):
    """Get all user profile settings with filtering"""
    query = db.query(UserProfileSetting)
    
    if user_id:
        query = query.filter(UserProfileSetting.user_id == user_id)
    
    profile_settings = query.order_by(desc(UserProfileSetting.created_at)).all()
    return profile_settings

@router.post("/user-profile-settings", response_model=UserProfileSettingResponse)
async def create_user_profile_setting(profile_data: UserProfileSettingCreateRequest, db: Session = Depends(get_db)):
    """Create new user profile settings"""
    # Verify user exists
    user = db.query(User).filter(User.id == profile_data.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check if profile settings already exist for this user
    existing = db.query(UserProfileSetting).filter(UserProfileSetting.user_id == profile_data.user_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Profile settings already exist for this user")
    
    new_profile_setting = UserProfileSetting(
        user_id=profile_data.user_id,
        profile_picture_url=profile_data.profile_picture_url,
        bio=profile_data.bio,
        preferences=profile_data.preferences,
        notification_settings=profile_data.notification_settings,
        dashboard_config=profile_data.dashboard_config,
        theme_settings=profile_data.theme_settings
    )
    
    db.add(new_profile_setting)
    db.commit()
    db.refresh(new_profile_setting)
    return new_profile_setting

@router.get("/user-profile-settings/{user_id}", response_model=UserProfileSettingResponse)
async def get_user_profile_setting(user_id: str, db: Session = Depends(get_db)):
    """Get user profile settings by user ID"""
    profile_setting = db.query(UserProfileSetting).filter(UserProfileSetting.user_id == user_id).first()
    if not profile_setting:
        raise HTTPException(status_code=404, detail="User profile settings not found")
    return profile_setting

@router.put("/user-profile-settings/{user_id}", response_model=UserProfileSettingResponse)
async def update_user_profile_setting(user_id: str, profile_data: UserProfileSettingCreateRequest, db: Session = Depends(get_db)):
    """Update user profile settings"""
    profile_setting = db.query(UserProfileSetting).filter(UserProfileSetting.user_id == user_id).first()
    if not profile_setting:
        raise HTTPException(status_code=404, detail="User profile settings not found")
    
    # Update fields
    for field, value in profile_data.dict(exclude_unset=True).items():
        if field != 'user_id':  # Don't allow changing user reference
            setattr(profile_setting, field, value)
    
    db.commit()
    db.refresh(profile_setting)
    return profile_setting

# USER APPLICATION SETTINGS ENDPOINTS

@router.get("/user-app-settings", response_model=List[UserApplicationSettingResponse])
async def get_user_application_settings(
    user_id: Optional[str] = Query(None, description="Filter by user ID"),
    db: Session = Depends(get_db)
):
    """Get all user application settings with filtering"""
    query = db.query(UserApplicationSetting)
    
    if user_id:
        query = query.filter(UserApplicationSetting.user_id == user_id)
    
    app_settings = query.order_by(desc(UserApplicationSetting.created_at)).all()
    return app_settings

@router.post("/user-app-settings", response_model=UserApplicationSettingResponse)
async def create_user_application_setting(app_data: UserApplicationSettingCreateRequest, db: Session = Depends(get_db)):
    """Create new user application settings"""
    # Verify user exists
    user = db.query(User).filter(User.id == app_data.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check if application settings already exist for this user
    existing = db.query(UserApplicationSetting).filter(UserApplicationSetting.user_id == app_data.user_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Application settings already exist for this user")
    
    new_app_setting = UserApplicationSetting(
        user_id=app_data.user_id,
        language=app_data.language,
        timezone=app_data.timezone,
        time_format=app_data.time_format,
        theme=app_data.theme,
        font_size=app_data.font_size,
        notifications_enabled=app_data.notifications_enabled,
        email_notifications=app_data.email_notifications,
        quiet_hours_enabled=app_data.quiet_hours_enabled
    )
    
    db.add(new_app_setting)
    db.commit()
    db.refresh(new_app_setting)
    return new_app_setting

@router.get("/user-app-settings/{user_id}", response_model=UserApplicationSettingResponse)
async def get_user_application_setting(user_id: str, db: Session = Depends(get_db)):
    """Get user application settings by user ID"""
    app_setting = db.query(UserApplicationSetting).filter(UserApplicationSetting.user_id == user_id).first()
    if not app_setting:
        raise HTTPException(status_code=404, detail="User application settings not found")
    return app_setting

@router.put("/user-app-settings/{user_id}", response_model=UserApplicationSettingResponse)
async def update_user_application_setting(user_id: str, app_data: UserApplicationSettingCreateRequest, db: Session = Depends(get_db)):
    """Update user application settings"""
    app_setting = db.query(UserApplicationSetting).filter(UserApplicationSetting.user_id == user_id).first()
    if not app_setting:
        raise HTTPException(status_code=404, detail="User application settings not found")
    
    # Update fields
    for field, value in app_data.dict(exclude_unset=True).items():
        if field != 'user_id':  # Don't allow changing user reference
            setattr(app_setting, field, value)
    
    db.commit()
    db.refresh(app_setting)
    return app_setting

# HELP ARTICLES ENDPOINTS

@router.get("/help-articles", response_model=List[HelpArticleResponse])
async def get_help_articles(
    category: Optional[str] = Query(None, description="Filter by category"),
    subcategory: Optional[str] = Query(None, description="Filter by subcategory"),
    is_published: Optional[bool] = Query(True, description="Filter by published status"),
    author_id: Optional[str] = Query(None, description="Filter by author"),
    db: Session = Depends(get_db)
):
    """Get all help articles with filtering"""
    query = db.query(HelpArticle)
    
    if category:
        query = query.filter(HelpArticle.category == category)
    if subcategory:
        query = query.filter(HelpArticle.subcategory == subcategory)
    if is_published is not None:
        query = query.filter(HelpArticle.is_published == is_published)
    if author_id:
        query = query.filter(HelpArticle.author_id == author_id)
    
    articles = query.order_by(desc(HelpArticle.view_count), desc(HelpArticle.created_at)).all()
    return articles

@router.post("/help-articles", response_model=HelpArticleResponse)
async def create_help_article(article_data: HelpArticleCreateRequest, db: Session = Depends(get_db)):
    """Create a new help article"""
    # Find a valid user to use as author_id
    existing_user = db.query(User).first()
    if not existing_user:
        raise HTTPException(status_code=400, detail="No users found in system")
    
    new_article = HelpArticle(
        title=article_data.title,
        content=article_data.content,
        category=article_data.category,
        subcategory=article_data.subcategory,
        tags=article_data.tags,
        is_published=article_data.is_published,
        search_keywords=article_data.search_keywords,
        author_id=existing_user.id
    )
    
    db.add(new_article)
    db.commit()
    db.refresh(new_article)
    return new_article

@router.get("/help-articles/{article_id}", response_model=HelpArticleResponse)
async def get_help_article(article_id: str, db: Session = Depends(get_db)):
    """Get a specific help article"""
    article = db.query(HelpArticle).filter(HelpArticle.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Help article not found")
    
    # Increment view count
    article.view_count += 1
    db.commit()
    
    return article

@router.put("/help-articles/{article_id}", response_model=HelpArticleResponse)
async def update_help_article(article_id: str, article_data: HelpArticleCreateRequest, db: Session = Depends(get_db)):
    """Update a help article"""
    article = db.query(HelpArticle).filter(HelpArticle.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Help article not found")
    
    # Update fields
    for field, value in article_data.dict(exclude_unset=True).items():
        setattr(article, field, value)
    
    db.commit()
    db.refresh(article)
    return article

@router.put("/help-articles/{article_id}/publish")
async def publish_help_article(article_id: str, db: Session = Depends(get_db)):
    """Publish a help article"""
    article = db.query(HelpArticle).filter(HelpArticle.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Help article not found")
    
    article.is_published = True
    db.commit()
    db.refresh(article)
    
    return {"message": "Help article published successfully"}

@router.put("/help-articles/{article_id}/helpful")
async def mark_article_helpful(article_id: str, helpful: bool = True, db: Session = Depends(get_db)):
    """Mark a help article as helpful or not helpful"""
    article = db.query(HelpArticle).filter(HelpArticle.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Help article not found")
    
    if helpful:
        article.helpful_count += 1
    else:
        article.unhelpful_count += 1
    
    db.commit()
    db.refresh(article)
    
    return {"message": f"Article marked as {'helpful' if helpful else 'not helpful'}"}

# USER FEEDBACK ENDPOINTS

@router.get("/user-feedback", response_model=List[UserFeedbackResponse])
async def get_user_feedback(
    user_id: Optional[str] = Query(None, description="Filter by user ID"),
    feedback_type: Optional[str] = Query(None, description="Filter by feedback type"),
    status: Optional[str] = Query(None, description="Filter by status"),
    priority: Optional[str] = Query(None, description="Filter by priority"),
    db: Session = Depends(get_db)
):
    """Get all user feedback with filtering"""
    query = db.query(UserFeedback)
    
    if user_id:
        query = query.filter(UserFeedback.user_id == user_id)
    if feedback_type:
        query = query.filter(UserFeedback.feedback_type == feedback_type)
    if status:
        query = query.filter(UserFeedback.status == status)
    if priority:
        query = query.filter(UserFeedback.priority == priority)
    
    feedback = query.order_by(desc(UserFeedback.created_at)).all()
    return feedback

@router.post("/user-feedback", response_model=UserFeedbackResponse)
async def create_user_feedback(feedback_data: UserFeedbackCreateRequest, db: Session = Depends(get_db)):
    """Create new user feedback"""
    # Verify user exists
    user = db.query(User).filter(User.id == feedback_data.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    new_feedback = UserFeedback(
        user_id=feedback_data.user_id,
        feedback_type=feedback_data.feedback_type,
        title=feedback_data.title,
        description=feedback_data.description,
        priority=feedback_data.priority,
        category=feedback_data.category,
        attachments=feedback_data.attachments
    )
    
    db.add(new_feedback)
    db.commit()
    db.refresh(new_feedback)
    return new_feedback

@router.get("/user-feedback/{feedback_id}", response_model=UserFeedbackResponse)
async def get_user_feedback_item(feedback_id: str, db: Session = Depends(get_db)):
    """Get a specific user feedback item"""
    feedback = db.query(UserFeedback).filter(UserFeedback.id == feedback_id).first()
    if not feedback:
        raise HTTPException(status_code=404, detail="User feedback not found")
    return feedback

@router.put("/user-feedback/{feedback_id}/respond")
async def respond_to_feedback(feedback_id: str, response: str, db: Session = Depends(get_db)):
    """Respond to user feedback"""
    feedback = db.query(UserFeedback).filter(UserFeedback.id == feedback_id).first()
    if not feedback:
        raise HTTPException(status_code=404, detail="User feedback not found")
    
    # Find a valid user to use as responded_by
    existing_user = db.query(User).first()
    
    feedback.admin_response = response
    feedback.responded_at = datetime.utcnow()
    feedback.status = "resolved"
    if existing_user:
        feedback.responded_by = existing_user.id
    
    db.commit()
    db.refresh(feedback)
    
    return {"message": "Response added successfully"}

@router.put("/user-feedback/{feedback_id}/upvote")
async def upvote_feedback(feedback_id: str, db: Session = Depends(get_db)):
    """Upvote user feedback"""
    feedback = db.query(UserFeedback).filter(UserFeedback.id == feedback_id).first()
    if not feedback:
        raise HTTPException(status_code=404, detail="User feedback not found")
    
    feedback.upvote_count += 1
    db.commit()
    db.refresh(feedback)
    
    return {"message": "Feedback upvoted successfully", "upvote_count": feedback.upvote_count}

# INTEGRATION ANALYTICS ENDPOINTS

@router.get("/analytics/integration-overview")
async def get_integration_overview_analytics(db: Session = Depends(get_db)):
    """Get integration overview analytics"""
    integrations = db.query(ThirdPartyIntegration).all()
    
    # Group by status and type
    status_counts = {}
    type_counts = {}
    
    total_usage = 0
    total_errors = 0
    
    for integration in integrations:
        status = integration.status.value if hasattr(integration.status, 'value') else integration.status
        int_type = integration.integration_type.value if hasattr(integration.integration_type, 'value') else integration.integration_type
        
        status_counts[status] = status_counts.get(status, 0) + 1
        type_counts[int_type] = type_counts.get(int_type, 0) + 1
        
        total_usage += integration.monthly_usage
        total_errors += integration.error_rate or 0
    
    active_integrations = status_counts.get("active", 0)
    avg_error_rate = total_errors / len(integrations) if integrations else 0
    
    return {
        "total_integrations": len(integrations),
        "active_integrations": active_integrations,
        "integration_health": (active_integrations / len(integrations) * 100) if integrations else 0,
        "integrations_by_status": status_counts,
        "integrations_by_type": type_counts,
        "usage_metrics": {
            "total_monthly_usage": total_usage,
            "average_error_rate": avg_error_rate
        }
    }

@router.get("/analytics/user-engagement")
async def get_user_engagement_analytics(
    days: int = Query(30, description="Number of days for analysis"),
    db: Session = Depends(get_db)
):
    """Get user engagement analytics"""
    date_threshold = datetime.utcnow() - timedelta(days=days)
    
    # Get recent feedback
    recent_feedback = db.query(UserFeedback).filter(
        UserFeedback.created_at >= date_threshold
    ).all()
    
    # Get help article views (using created_at as proxy for recent views)
    help_articles = db.query(HelpArticle).filter(HelpArticle.is_published == True).all()
    
    # Group feedback by type and status
    feedback_types = {}
    feedback_status = {}
    
    for feedback in recent_feedback:
        f_type = feedback.feedback_type.value if hasattr(feedback.feedback_type, 'value') else feedback.feedback_type
        f_status = feedback.status.value if hasattr(feedback.status, 'value') else feedback.status
        
        feedback_types[f_type] = feedback_types.get(f_type, 0) + 1
        feedback_status[f_status] = feedback_status.get(f_status, 0) + 1
    
    # Calculate help article metrics
    total_article_views = sum([article.view_count for article in help_articles])
    helpful_votes = sum([article.helpful_count for article in help_articles])
    unhelpful_votes = sum([article.unhelpful_count for article in help_articles])
    
    return {
        "analysis_period_days": days,
        "feedback_metrics": {
            "total_feedback": len(recent_feedback),
            "feedback_by_type": feedback_types,
            "feedback_by_status": feedback_status,
            "resolved_feedback": feedback_status.get("resolved", 0)
        },
        "help_system_metrics": {
            "total_articles": len(help_articles),
            "total_article_views": total_article_views,
            "helpful_votes": helpful_votes,
            "unhelpful_votes": unhelpful_votes,
            "helpfulness_ratio": (helpful_votes / (helpful_votes + unhelpful_votes) * 100) if (helpful_votes + unhelpful_votes) > 0 else 0
        },
        "engagement_score": (len(recent_feedback) + total_article_views) / days if days > 0 else 0
    }