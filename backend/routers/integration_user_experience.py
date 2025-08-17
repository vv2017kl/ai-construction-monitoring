"""
Integration & User Experience API Routes
Handles third-party integrations, user profile settings, application settings, help articles, and user feedback
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_
from typing import List, Optional
from datetime import datetime, timedelta

from database import get_db
from models import (
    ThirdPartyIntegration, UserProfileSetting, UserApplicationSetting, 
    HelpArticle, UserFeedback, User,
    IntegrationType, IntegrationStatus, FeedbackType, FeedbackStatus
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

@router.get("/integrations", response_model=List[ThirdPartyIntegrationResponse])
def get_all_integrations(
    integration_type: Optional[str] = Query(None, description="Filter by integration type"),
    status: Optional[str] = Query(None, description="Filter by status"),
    provider: Optional[str] = Query(None, description="Filter by provider name"),
    db: Session = Depends(get_db)
):
    """Get all third-party integrations with optional filtering"""
    query = db.query(ThirdPartyIntegration)
    
    if integration_type:
        try:
            type_enum = IntegrationType(integration_type)
            query = query.filter(ThirdPartyIntegration.integration_type == type_enum)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid integration type: {integration_type}")
    
    if status:
        try:
            status_enum = IntegrationStatus(status)
            query = query.filter(ThirdPartyIntegration.status == status_enum)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid status: {status}")
    
    if provider:
        query = query.filter(ThirdPartyIntegration.provider_name.ilike(f"%{provider}%"))
    
    return query.all()

@router.post("/integrations", response_model=ThirdPartyIntegrationResponse)
def create_integration(
    integration: ThirdPartyIntegrationCreateRequest,
    created_by: str = Query(..., description="User ID creating the integration"),
    db: Session = Depends(get_db)
):
    """Create a new third-party integration"""
    # Verify user exists
    user = db.query(User).filter(User.id == created_by).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Validate integration type
    try:
        IntegrationType(integration.integration_type)
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid integration type: {integration.integration_type}")
    
    db_integration = ThirdPartyIntegration(
        integration_name=integration.integration_name,
        integration_type=integration.integration_type,
        provider_name=integration.provider_name,
        description=integration.description,
        configuration=integration.configuration,
        endpoints=integration.endpoints,
        rate_limits=integration.rate_limits,
        monthly_limit=integration.monthly_limit,
        created_by=created_by
    )
    
    db.add(db_integration)
    db.commit()
    db.refresh(db_integration)
    
    return db_integration

@router.get("/integrations/{integration_id}", response_model=ThirdPartyIntegrationResponse)
def get_integration(integration_id: str, db: Session = Depends(get_db)):
    """Get a specific third-party integration"""
    integration = db.query(ThirdPartyIntegration).filter(ThirdPartyIntegration.id == integration_id).first()
    if not integration:
        raise HTTPException(status_code=404, detail="Integration not found")
    return integration

@router.put("/integrations/{integration_id}", response_model=ThirdPartyIntegrationResponse)
def update_integration(
    integration_id: str,
    integration_data: dict,
    db: Session = Depends(get_db)
):
    """Update a third-party integration"""
    integration = db.query(ThirdPartyIntegration).filter(ThirdPartyIntegration.id == integration_id).first()
    if not integration:
        raise HTTPException(status_code=404, detail="Integration not found")
    
    for key, value in integration_data.items():
        if hasattr(integration, key):
            setattr(integration, key, value)
    
    db.commit()
    db.refresh(integration)
    return integration

@router.delete("/integrations/{integration_id}")
def delete_integration(integration_id: str, db: Session = Depends(get_db)):
    """Delete a third-party integration"""
    integration = db.query(ThirdPartyIntegration).filter(ThirdPartyIntegration.id == integration_id).first()
    if not integration:
        raise HTTPException(status_code=404, detail="Integration not found")
    
    db.delete(integration)
    db.commit()
    return {"message": "Integration deleted successfully"}

@router.get("/integrations/analytics/health-summary")
def get_integration_health_summary(db: Session = Depends(get_db)):
    """Get integration health summary analytics"""
    total = db.query(ThirdPartyIntegration).count()
    active = db.query(ThirdPartyIntegration).filter(ThirdPartyIntegration.status == IntegrationStatus.active).count()
    error = db.query(ThirdPartyIntegration).filter(ThirdPartyIntegration.status == IntegrationStatus.error).count()
    
    avg_health = db.query(func.avg(ThirdPartyIntegration.health_score)).scalar() or 0
    avg_response_time = db.query(func.avg(ThirdPartyIntegration.avg_response_time_ms)).scalar() or 0
    
    return {
        "total_integrations": total,
        "active_integrations": active,
        "error_integrations": error,
        "health_rate": (active / total * 100) if total > 0 else 0,
        "average_health_score": float(avg_health),
        "average_response_time_ms": float(avg_response_time)
    }

# USER PROFILE SETTINGS ENDPOINTS

@router.get("/profile-settings", response_model=List[UserProfileSettingResponse])
def get_all_profile_settings(
    user_id: Optional[str] = Query(None, description="Filter by user ID"),
    db: Session = Depends(get_db)
):
    """Get all user profile settings"""
    query = db.query(UserProfileSetting)
    
    if user_id:
        query = query.filter(UserProfileSetting.user_id == user_id)
    
    return query.all()

@router.post("/profile-settings", response_model=UserProfileSettingResponse)
def create_profile_setting(
    profile_setting: UserProfileSettingCreateRequest,
    db: Session = Depends(get_db)
):
    """Create user profile settings"""
    # Verify user exists
    user = db.query(User).filter(User.id == profile_setting.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check if profile settings already exist for user
    existing = db.query(UserProfileSetting).filter(UserProfileSetting.user_id == profile_setting.user_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Profile settings already exist for this user")
    
    db_setting = UserProfileSetting(**profile_setting.model_dump())
    db.add(db_setting)
    db.commit()
    db.refresh(db_setting)
    
    return db_setting

@router.get("/profile-settings/{user_id}", response_model=UserProfileSettingResponse)
def get_user_profile_settings(user_id: str, db: Session = Depends(get_db)):
    """Get user profile settings by user ID"""
    setting = db.query(UserProfileSetting).filter(UserProfileSetting.user_id == user_id).first()
    if not setting:
        raise HTTPException(status_code=404, detail="Profile settings not found")
    return setting

@router.put("/profile-settings/{user_id}", response_model=UserProfileSettingResponse)
def update_profile_settings(
    user_id: str,
    profile_data: dict,
    db: Session = Depends(get_db)
):
    """Update user profile settings"""
    setting = db.query(UserProfileSetting).filter(UserProfileSetting.user_id == user_id).first()
    if not setting:
        raise HTTPException(status_code=404, detail="Profile settings not found")
    
    for key, value in profile_data.items():
        if hasattr(setting, key):
            setattr(setting, key, value)
    
    db.commit()
    db.refresh(setting)
    return setting

# USER APPLICATION SETTINGS ENDPOINTS

@router.get("/app-settings", response_model=List[UserApplicationSettingResponse])
def get_all_app_settings(
    user_id: Optional[str] = Query(None, description="Filter by user ID"),
    db: Session = Depends(get_db)
):
    """Get all user application settings"""
    query = db.query(UserApplicationSetting)
    
    if user_id:
        query = query.filter(UserApplicationSetting.user_id == user_id)
    
    return query.all()

@router.post("/app-settings", response_model=UserApplicationSettingResponse)
def create_app_setting(
    app_setting: UserApplicationSettingCreateRequest,
    db: Session = Depends(get_db)
):
    """Create user application settings"""
    # Verify user exists
    user = db.query(User).filter(User.id == app_setting.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check if app settings already exist for user
    existing = db.query(UserApplicationSetting).filter(UserApplicationSetting.user_id == app_setting.user_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Application settings already exist for this user")
    
    db_setting = UserApplicationSetting(**app_setting.model_dump())
    db.add(db_setting)
    db.commit()
    db.refresh(db_setting)
    
    return db_setting

@router.get("/app-settings/{user_id}", response_model=UserApplicationSettingResponse)
def get_user_app_settings(user_id: str, db: Session = Depends(get_db)):
    """Get user application settings by user ID"""
    setting = db.query(UserApplicationSetting).filter(UserApplicationSetting.user_id == user_id).first()
    if not setting:
        raise HTTPException(status_code=404, detail="Application settings not found")
    return setting

@router.put("/app-settings/{user_id}", response_model=UserApplicationSettingResponse)
def update_app_settings(
    user_id: str,
    app_data: dict,
    db: Session = Depends(get_db)
):
    """Update user application settings"""
    setting = db.query(UserApplicationSetting).filter(UserApplicationSetting.user_id == user_id).first()
    if not setting:
        raise HTTPException(status_code=404, detail="Application settings not found")
    
    for key, value in app_data.items():
        if hasattr(setting, key):
            setattr(setting, key, value)
    
    db.commit()
    db.refresh(setting)
    return setting

# HELP ARTICLES ENDPOINTS

@router.get("/help/articles", response_model=List[HelpArticleResponse])
def get_all_help_articles(
    category: Optional[str] = Query(None, description="Filter by category"),
    subcategory: Optional[str] = Query(None, description="Filter by subcategory"),
    published_only: bool = Query(True, description="Show only published articles"),
    search: Optional[str] = Query(None, description="Search in title and content"),
    db: Session = Depends(get_db)
):
    """Get all help articles with optional filtering and search"""
    query = db.query(HelpArticle)
    
    if published_only:
        query = query.filter(HelpArticle.is_published == True)
    
    if category:
        query = query.filter(HelpArticle.category.ilike(f"%{category}%"))
    
    if subcategory:
        query = query.filter(HelpArticle.subcategory.ilike(f"%{subcategory}%"))
    
    if search:
        query = query.filter(
            or_(
                HelpArticle.title.ilike(f"%{search}%"),
                HelpArticle.content.ilike(f"%{search}%"),
                HelpArticle.search_keywords.ilike(f"%{search}%")
            )
        )
    
    return query.order_by(HelpArticle.view_count.desc()).all()

@router.post("/help/articles", response_model=HelpArticleResponse)
def create_help_article(
    article: HelpArticleCreateRequest,
    author_id: str = Query(..., description="Author user ID"),
    db: Session = Depends(get_db)
):
    """Create a new help article"""
    # Verify author exists
    author = db.query(User).filter(User.id == author_id).first()
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    
    db_article = HelpArticle(
        title=article.title,
        content=article.content,
        category=article.category,
        subcategory=article.subcategory,
        tags=article.tags,
        author_id=author_id,
        is_published=article.is_published,
        search_keywords=article.search_keywords
    )
    
    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    
    return db_article

@router.get("/help/articles/{article_id}", response_model=HelpArticleResponse)
def get_help_article(article_id: str, db: Session = Depends(get_db)):
    """Get a specific help article and increment view count"""
    article = db.query(HelpArticle).filter(HelpArticle.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    
    # Increment view count
    article.view_count += 1
    db.commit()
    
    return article

@router.put("/help/articles/{article_id}", response_model=HelpArticleResponse)
def update_help_article(
    article_id: str,
    article_data: dict,
    db: Session = Depends(get_db)
):
    """Update a help article"""
    article = db.query(HelpArticle).filter(HelpArticle.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    
    for key, value in article_data.items():
        if hasattr(article, key):
            setattr(article, key, value)
    
    db.commit()
    db.refresh(article)
    return article

@router.delete("/help/articles/{article_id}")
def delete_help_article(article_id: str, db: Session = Depends(get_db)):
    """Delete a help article"""
    article = db.query(HelpArticle).filter(HelpArticle.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    
    db.delete(article)
    db.commit()
    return {"message": "Article deleted successfully"}

@router.post("/help/articles/{article_id}/helpful")
def mark_article_helpful(
    article_id: str,
    helpful: bool = Query(..., description="True for helpful, False for unhelpful"),
    db: Session = Depends(get_db)
):
    """Mark article as helpful or unhelpful"""
    article = db.query(HelpArticle).filter(HelpArticle.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    
    if helpful:
        article.helpful_count += 1
    else:
        article.unhelpful_count += 1
    
    db.commit()
    
    return {
        "message": f"Article marked as {'helpful' if helpful else 'unhelpful'}",
        "helpful_count": article.helpful_count,
        "unhelpful_count": article.unhelpful_count
    }

@router.get("/help/analytics/categories")
def get_help_categories_analytics(db: Session = Depends(get_db)):
    """Get help articles analytics by category"""
    categories = db.query(
        HelpArticle.category,
        func.count(HelpArticle.id).label('article_count'),
        func.sum(HelpArticle.view_count).label('total_views'),
        func.avg(HelpArticle.helpful_count).label('avg_helpful')
    ).group_by(HelpArticle.category).all()
    
    return [
        {
            "category": cat.category,
            "article_count": cat.article_count,
            "total_views": cat.total_views or 0,
            "avg_helpful": float(cat.avg_helpful or 0)
        }
        for cat in categories
    ]

# USER FEEDBACK ENDPOINTS

@router.get("/feedback", response_model=List[UserFeedbackResponse])
def get_all_feedback(
    feedback_type: Optional[str] = Query(None, description="Filter by feedback type"),
    status: Optional[str] = Query(None, description="Filter by status"),
    priority: Optional[str] = Query(None, description="Filter by priority"),
    user_id: Optional[str] = Query(None, description="Filter by user ID"),
    days: Optional[int] = Query(None, description="Filter by days back"),
    db: Session = Depends(get_db)
):
    """Get all user feedback with optional filtering"""
    query = db.query(UserFeedback)
    
    if feedback_type:
        try:
            type_enum = FeedbackType(feedback_type)
            query = query.filter(UserFeedback.feedback_type == type_enum)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid feedback type: {feedback_type}")
    
    if status:
        try:
            status_enum = FeedbackStatus(status)
            query = query.filter(UserFeedback.status == status_enum)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid status: {status}")
    
    if priority:
        query = query.filter(UserFeedback.priority == priority)
    
    if user_id:
        query = query.filter(UserFeedback.user_id == user_id)
    
    if days:
        cutoff_date = datetime.now() - timedelta(days=days)
        query = query.filter(UserFeedback.created_at >= cutoff_date)
    
    return query.order_by(UserFeedback.created_at.desc()).all()

@router.post("/feedback", response_model=UserFeedbackResponse)
def create_feedback(
    feedback: UserFeedbackCreateRequest,
    db: Session = Depends(get_db)
):
    """Create new user feedback"""
    # Verify user exists
    user = db.query(User).filter(User.id == feedback.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Validate feedback type
    try:
        FeedbackType(feedback.feedback_type)
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid feedback type: {feedback.feedback_type}")
    
    db_feedback = UserFeedback(**feedback.model_dump())
    db.add(db_feedback)
    db.commit()
    db.refresh(db_feedback)
    
    return db_feedback

@router.get("/feedback/{feedback_id}", response_model=UserFeedbackResponse)
def get_feedback(feedback_id: str, db: Session = Depends(get_db)):
    """Get a specific feedback item"""
    feedback = db.query(UserFeedback).filter(UserFeedback.id == feedback_id).first()
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")
    return feedback

@router.put("/feedback/{feedback_id}", response_model=UserFeedbackResponse)
def update_feedback(
    feedback_id: str,
    feedback_data: dict,
    db: Session = Depends(get_db)
):
    """Update feedback (typically for admin responses)"""
    feedback = db.query(UserFeedback).filter(UserFeedback.id == feedback_id).first()
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")
    
    # If admin response is being added, set responded_at timestamp
    if "admin_response" in feedback_data and feedback_data["admin_response"]:
        feedback_data["responded_at"] = datetime.now()
    
    for key, value in feedback_data.items():
        if hasattr(feedback, key):
            setattr(feedback, key, value)
    
    db.commit()
    db.refresh(feedback)
    return feedback

@router.post("/feedback/{feedback_id}/upvote")
def upvote_feedback(feedback_id: str, db: Session = Depends(get_db)):
    """Upvote a feedback item"""
    feedback = db.query(UserFeedback).filter(UserFeedback.id == feedback_id).first()
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")
    
    feedback.upvote_count += 1
    db.commit()
    
    return {
        "message": "Feedback upvoted successfully",
        "upvote_count": feedback.upvote_count
    }

@router.get("/feedback/analytics/summary")
def get_feedback_analytics_summary(
    days: Optional[int] = Query(None, description="Analytics period in days"),
    db: Session = Depends(get_db)
):
    """Get feedback analytics summary"""
    query = db.query(UserFeedback)
    
    if days:
        cutoff_date = datetime.now() - timedelta(days=days)
        query = query.filter(UserFeedback.created_at >= cutoff_date)
    
    total = query.count()
    by_type = query.with_entities(
        UserFeedback.feedback_type,
        func.count(UserFeedback.id).label('count')
    ).group_by(UserFeedback.feedback_type).all()
    
    by_status = query.with_entities(
        UserFeedback.status,
        func.count(UserFeedback.id).label('count')
    ).group_by(UserFeedback.status).all()
    
    resolved = query.filter(UserFeedback.status == FeedbackStatus.resolved).count()
    
    return {
        "total_feedback": total,
        "resolution_rate": (resolved / total * 100) if total > 0 else 0,
        "by_type": [{"type": item.feedback_type.value, "count": item.count} for item in by_type],
        "by_status": [{"status": item.status.value, "count": item.count} for item in by_status],
        "period_days": days or "all_time"
    }