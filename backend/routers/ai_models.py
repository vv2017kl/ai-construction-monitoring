"""
AI Model Management & Deployment API Router
Handles AI models, deployments, training jobs, and evaluation results
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
    AIModel, ModelDeployment, ModelPerformanceMetric, ModelTrainingJob,
    ModelEvaluationResult, Site, User
)
from schemas import (
    AIModelResponse, AIModelCreateRequest,
    ModelDeploymentResponse, ModelDeploymentCreateRequest,
    ModelTrainingJobResponse, ModelTrainingJobCreateRequest,
    ModelEvaluationResultResponse, ModelEvaluationResultCreateRequest
)

router = APIRouter(prefix="/ai-models", tags=["AI Model Management & Deployment"])

# AI MODELS ENDPOINTS

@router.get("/", response_model=List[AIModelResponse])
async def get_ai_models(
    model_type: Optional[str] = Query(None, description="Filter by model type"),
    category: Optional[str] = Query(None, description="Filter by category"),
    status: Optional[str] = Query(None, description="Filter by status"),
    lifecycle_stage: Optional[str] = Query(None, description="Filter by lifecycle stage"),
    approval_status: Optional[str] = Query(None, description="Filter by approval status"),
    db: Session = Depends(get_db)
):
    """Get all AI models with filtering"""
    query = db.query(AIModel)
    
    if model_type:
        query = query.filter(AIModel.model_type == model_type)
    if category:
        query = query.filter(AIModel.category == category)
    if status:
        query = query.filter(AIModel.status == status)
    if lifecycle_stage:
        query = query.filter(AIModel.lifecycle_stage == lifecycle_stage)
    if approval_status:
        query = query.filter(AIModel.approval_status == approval_status)
    
    models = query.order_by(desc(AIModel.created_at)).all()
    return models

@router.post("/", response_model=AIModelResponse)
async def create_ai_model(model_data: AIModelCreateRequest, db: Session = Depends(get_db)):
    """Create a new AI model"""
    # Find a valid user to use as created_by and last_modified_by
    existing_user = db.query(User).first()
    if not existing_user:
        raise HTTPException(status_code=400, detail="No users found in system")
    
    new_model = AIModel(
        name=model_data.name,
        model_type=model_data.model_type,
        category=model_data.category,
        version=model_data.version,
        description=model_data.description,
        framework=model_data.framework,
        model_file_path=model_data.model_file_path,
        training_dataset_info=model_data.training_dataset_info,
        baseline_accuracy=model_data.baseline_accuracy,
        license_type=model_data.license_type,
        created_by=existing_user.id,
        last_modified_by=existing_user.id
    )
    
    db.add(new_model)
    db.commit()
    db.refresh(new_model)
    return new_model

@router.get("/{model_id}", response_model=AIModelResponse)
async def get_ai_model(model_id: str, db: Session = Depends(get_db)):
    """Get a specific AI model"""
    model = db.query(AIModel).filter(AIModel.id == model_id).first()
    if not model:
        raise HTTPException(status_code=404, detail="AI model not found")
    return model

@router.put("/{model_id}", response_model=AIModelResponse)
async def update_ai_model(model_id: str, model_data: AIModelCreateRequest, db: Session = Depends(get_db)):
    """Update an AI model"""
    model = db.query(AIModel).filter(AIModel.id == model_id).first()
    if not model:
        raise HTTPException(status_code=404, detail="AI model not found")
    
    # Find a valid user to use as last_modified_by
    existing_user = db.query(User).first()
    
    # Update fields
    for field, value in model_data.dict(exclude_unset=True).items():
        setattr(model, field, value)
    
    if existing_user:
        model.last_modified_by = existing_user.id
    
    db.commit()
    db.refresh(model)
    return model

@router.put("/{model_id}/approve")
async def approve_ai_model(model_id: str, db: Session = Depends(get_db)):
    """Approve an AI model for deployment"""
    model = db.query(AIModel).filter(AIModel.id == model_id).first()
    if not model:
        raise HTTPException(status_code=404, detail="AI model not found")
    
    # Find a valid user to use as approved_by
    existing_user = db.query(User).first()
    
    model.approval_status = "approved"
    model.approved_at = datetime.utcnow()
    if existing_user:
        model.approved_by = existing_user.id
    
    db.commit()
    db.refresh(model)
    
    return {"message": "AI model approved successfully"}

@router.delete("/{model_id}")
async def delete_ai_model(model_id: str, db: Session = Depends(get_db)):
    """Delete an AI model"""
    model = db.query(AIModel).filter(AIModel.id == model_id).first()
    if not model:
        raise HTTPException(status_code=404, detail="AI model not found")
    
    # Check for active deployments
    active_deployments = db.query(ModelDeployment).filter(
        and_(
            ModelDeployment.model_id == model_id,
            ModelDeployment.deployment_status == "active"
        )
    ).count()
    
    if active_deployments > 0:
        raise HTTPException(status_code=400, detail="Cannot delete model with active deployments")
    
    db.delete(model)
    db.commit()
    return {"message": "AI model deleted successfully"}

# MODEL DEPLOYMENTS ENDPOINTS

@router.get("/deployments", response_model=List[ModelDeploymentResponse])
async def get_model_deployments(
    model_id: Optional[str] = Query(None, description="Filter by model ID"),
    site_id: Optional[str] = Query(None, description="Filter by site ID"),
    deployment_status: Optional[str] = Query(None, description="Filter by deployment status"),
    deployment_type: Optional[str] = Query(None, description="Filter by deployment type"),
    db: Session = Depends(get_db)
):
    """Get all model deployments with filtering"""
    query = db.query(ModelDeployment)
    
    if model_id:
        query = query.filter(ModelDeployment.model_id == model_id)
    if site_id:
        query = query.filter(ModelDeployment.site_id == site_id)
    if deployment_status:
        query = query.filter(ModelDeployment.deployment_status == deployment_status)
    if deployment_type:
        query = query.filter(ModelDeployment.deployment_type == deployment_type)
    
    deployments = query.order_by(desc(ModelDeployment.created_at)).all()
    return deployments

@router.post("/deployments", response_model=ModelDeploymentResponse)
async def create_model_deployment(deployment_data: ModelDeploymentCreateRequest, db: Session = Depends(get_db)):
    """Create a new model deployment"""
    # Verify model exists and is approved
    model = db.query(AIModel).filter(AIModel.id == deployment_data.model_id).first()
    if not model:
        raise HTTPException(status_code=404, detail="AI model not found")
    
    if model.approval_status != "approved":
        raise HTTPException(status_code=400, detail="Model must be approved before deployment")
    
    # Verify site exists
    site = db.query(Site).filter(Site.id == deployment_data.site_id).first()
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    
    # Find a valid user to use as deployed_by
    existing_user = db.query(User).first()
    if not existing_user:
        raise HTTPException(status_code=400, detail="No users found in system")
    
    new_deployment = ModelDeployment(
        model_id=deployment_data.model_id,
        site_id=deployment_data.site_id,
        deployment_name=deployment_data.deployment_name,
        deployment_type=deployment_data.deployment_type,
        confidence_threshold=deployment_data.confidence_threshold,
        batch_size=deployment_data.batch_size,
        processing_interval_seconds=deployment_data.processing_interval_seconds,
        auto_scaling_enabled=deployment_data.auto_scaling_enabled,
        monitoring_enabled=deployment_data.monitoring_enabled,
        deployed_by=existing_user.id
    )
    
    db.add(new_deployment)
    db.commit()
    db.refresh(new_deployment)
    return new_deployment

@router.get("/deployments/{deployment_id}", response_model=ModelDeploymentResponse)
async def get_model_deployment(deployment_id: str, db: Session = Depends(get_db)):
    """Get a specific model deployment"""
    deployment = db.query(ModelDeployment).filter(ModelDeployment.id == deployment_id).first()
    if not deployment:
        raise HTTPException(status_code=404, detail="Model deployment not found")
    return deployment

@router.put("/deployments/{deployment_id}/start")
async def start_deployment(deployment_id: str, db: Session = Depends(get_db)):
    """Start a model deployment"""
    deployment = db.query(ModelDeployment).filter(ModelDeployment.id == deployment_id).first()
    if not deployment:
        raise HTTPException(status_code=404, detail="Model deployment not found")
    
    deployment.deployment_status = "active"
    deployment.deployed_at = datetime.utcnow()
    
    db.commit()
    db.refresh(deployment)
    
    return {"message": "Model deployment started successfully"}

@router.put("/deployments/{deployment_id}/stop")
async def stop_deployment(deployment_id: str, db: Session = Depends(get_db)):
    """Stop a model deployment"""
    deployment = db.query(ModelDeployment).filter(ModelDeployment.id == deployment_id).first()
    if not deployment:
        raise HTTPException(status_code=404, detail="Model deployment not found")
    
    deployment.deployment_status = "terminated"
    
    db.commit()
    db.refresh(deployment)
    
    return {"message": "Model deployment stopped successfully"}

# MODEL TRAINING JOBS ENDPOINTS

@router.get("/training-jobs", response_model=List[ModelTrainingJobResponse])
async def get_training_jobs(
    model_id: Optional[str] = Query(None, description="Filter by model ID"),
    job_status: Optional[str] = Query(None, description="Filter by job status"),
    training_type: Optional[str] = Query(None, description="Filter by training type"),
    db: Session = Depends(get_db)
):
    """Get all model training jobs with filtering"""
    query = db.query(ModelTrainingJob)
    
    if model_id:
        query = query.filter(ModelTrainingJob.model_id == model_id)
    if job_status:
        query = query.filter(ModelTrainingJob.job_status == job_status)
    if training_type:
        query = query.filter(ModelTrainingJob.training_type == training_type)
    
    jobs = query.order_by(desc(ModelTrainingJob.created_at)).all()
    return jobs

@router.post("/training-jobs", response_model=ModelTrainingJobResponse)
async def create_training_job(job_data: ModelTrainingJobCreateRequest, db: Session = Depends(get_db)):
    """Create a new model training job"""
    # Verify model exists
    model = db.query(AIModel).filter(AIModel.id == job_data.model_id).first()
    if not model:
        raise HTTPException(status_code=404, detail="AI model not found")
    
    # Verify base model exists if provided
    if job_data.base_model_id:
        base_model = db.query(AIModel).filter(AIModel.id == job_data.base_model_id).first()
        if not base_model:
            raise HTTPException(status_code=404, detail="Base model not found")
    
    # Find a valid user to use as created_by
    existing_user = db.query(User).first()
    if not existing_user:
        raise HTTPException(status_code=400, detail="No users found in system")
    
    new_job = ModelTrainingJob(
        model_id=job_data.model_id,
        job_name=job_data.job_name,
        training_type=job_data.training_type,
        job_description=job_data.job_description,
        base_model_id=job_data.base_model_id,
        epochs=job_data.epochs,
        batch_size=job_data.batch_size,
        learning_rate=job_data.learning_rate,
        cost_budget_limit=job_data.cost_budget_limit,
        created_by=existing_user.id
    )
    
    db.add(new_job)
    db.commit()
    db.refresh(new_job)
    return new_job

@router.get("/training-jobs/{job_id}", response_model=ModelTrainingJobResponse)
async def get_training_job(job_id: str, db: Session = Depends(get_db)):
    """Get a specific model training job"""
    job = db.query(ModelTrainingJob).filter(ModelTrainingJob.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Model training job not found")
    return job

@router.put("/training-jobs/{job_id}/start")
async def start_training_job(job_id: str, db: Session = Depends(get_db)):
    """Start a model training job"""
    job = db.query(ModelTrainingJob).filter(ModelTrainingJob.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Model training job not found")
    
    job.job_status = "running"
    job.started_at = datetime.utcnow()
    
    db.commit()
    db.refresh(job)
    
    return {"message": "Model training job started successfully"}

@router.put("/training-jobs/{job_id}/complete")
async def complete_training_job(job_id: str, db: Session = Depends(get_db)):
    """Mark a model training job as completed"""
    job = db.query(ModelTrainingJob).filter(ModelTrainingJob.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Model training job not found")
    
    job.job_status = "completed"
    job.completed_at = datetime.utcnow()
    job.actual_completion_time = datetime.utcnow()
    job.progress_percentage = 100.0
    
    db.commit()
    db.refresh(job)
    
    return {"message": "Model training job completed successfully"}

# MODEL EVALUATION RESULTS ENDPOINTS

@router.get("/evaluations", response_model=List[ModelEvaluationResultResponse])
async def get_evaluation_results(
    model_id: Optional[str] = Query(None, description="Filter by model ID"),
    evaluation_type: Optional[str] = Query(None, description="Filter by evaluation type"),
    review_status: Optional[str] = Query(None, description="Filter by review status"),
    approval_for_production: Optional[bool] = Query(None, description="Filter by production approval"),
    db: Session = Depends(get_db)
):
    """Get all model evaluation results with filtering"""
    query = db.query(ModelEvaluationResult)
    
    if model_id:
        query = query.filter(ModelEvaluationResult.model_id == model_id)
    if evaluation_type:
        query = query.filter(ModelEvaluationResult.evaluation_type == evaluation_type)
    if review_status:
        query = query.filter(ModelEvaluationResult.review_status == review_status)
    if approval_for_production is not None:
        query = query.filter(ModelEvaluationResult.approval_for_production == approval_for_production)
    
    evaluations = query.order_by(desc(ModelEvaluationResult.evaluation_date)).all()
    return evaluations

@router.post("/evaluations", response_model=ModelEvaluationResultResponse)
async def create_evaluation_result(evaluation_data: ModelEvaluationResultCreateRequest, db: Session = Depends(get_db)):
    """Create a new model evaluation result"""
    # Verify model exists
    model = db.query(AIModel).filter(AIModel.id == evaluation_data.model_id).first()
    if not model:
        raise HTTPException(status_code=404, detail="AI model not found")
    
    # Find a valid user to use as evaluated_by
    existing_user = db.query(User).first()
    if not existing_user:
        raise HTTPException(status_code=400, detail="No users found in system")
    
    new_evaluation = ModelEvaluationResult(
        model_id=evaluation_data.model_id,
        evaluation_name=evaluation_data.evaluation_name,
        evaluation_type=evaluation_data.evaluation_type,
        dataset_size=evaluation_data.dataset_size,
        overall_accuracy=evaluation_data.overall_accuracy,
        overall_precision=evaluation_data.overall_precision,
        overall_recall=evaluation_data.overall_recall,
        overall_f1_score=evaluation_data.overall_f1_score,
        business_accuracy_score=evaluation_data.business_accuracy_score,
        evaluated_by=existing_user.id
    )
    
    db.add(new_evaluation)
    db.commit()
    db.refresh(new_evaluation)
    return new_evaluation

@router.get("/evaluations/{evaluation_id}", response_model=ModelEvaluationResultResponse)
async def get_evaluation_result(evaluation_id: str, db: Session = Depends(get_db)):
    """Get a specific model evaluation result"""
    evaluation = db.query(ModelEvaluationResult).filter(ModelEvaluationResult.id == evaluation_id).first()
    if not evaluation:
        raise HTTPException(status_code=404, detail="Model evaluation result not found")
    return evaluation

@router.put("/evaluations/{evaluation_id}/approve")
async def approve_evaluation_for_production(evaluation_id: str, db: Session = Depends(get_db)):
    """Approve model evaluation for production deployment"""
    evaluation = db.query(ModelEvaluationResult).filter(ModelEvaluationResult.id == evaluation_id).first()
    if not evaluation:
        raise HTTPException(status_code=404, detail="Model evaluation result not found")
    
    # Find a valid user to use as reviewed_by
    existing_user = db.query(User).first()
    
    evaluation.review_status = "approved"
    evaluation.approval_for_production = True
    evaluation.review_date = datetime.utcnow()
    if existing_user:
        evaluation.reviewed_by = existing_user.id
    
    db.commit()
    db.refresh(evaluation)
    
    return {"message": "Model evaluation approved for production successfully"}

# AI MODEL ANALYTICS ENDPOINTS

@router.get("/analytics/model-overview")
async def get_model_overview_analytics(db: Session = Depends(get_db)):
    """Get comprehensive AI model analytics overview"""
    # Count models by status
    models = db.query(AIModel).all()
    
    status_counts = {}
    lifecycle_counts = {}
    type_counts = {}
    
    for model in models:
        status = model.status.value if hasattr(model.status, 'value') else model.status
        lifecycle = model.lifecycle_stage.value if hasattr(model.lifecycle_stage, 'value') else model.lifecycle_stage
        model_type = model.model_type.value if hasattr(model.model_type, 'value') else model.model_type
        
        status_counts[status] = status_counts.get(status, 0) + 1
        lifecycle_counts[lifecycle] = lifecycle_counts.get(lifecycle, 0) + 1
        type_counts[model_type] = type_counts.get(model_type, 0) + 1
    
    # Count deployments
    active_deployments = db.query(ModelDeployment).filter(ModelDeployment.deployment_status == "active").count()
    total_deployments = db.query(ModelDeployment).count()
    
    # Count training jobs
    running_jobs = db.query(ModelTrainingJob).filter(ModelTrainingJob.job_status == "running").count()
    completed_jobs = db.query(ModelTrainingJob).filter(ModelTrainingJob.job_status == "completed").count()
    
    # Count evaluations
    pending_evaluations = db.query(ModelEvaluationResult).filter(ModelEvaluationResult.review_status == "pending").count()
    approved_evaluations = db.query(ModelEvaluationResult).filter(ModelEvaluationResult.approval_for_production == True).count()
    
    return {
        "model_inventory": {
            "total_models": len(models),
            "models_by_status": status_counts,
            "models_by_lifecycle": lifecycle_counts,
            "models_by_type": type_counts
        },
        "deployment_metrics": {
            "active_deployments": active_deployments,
            "total_deployments": total_deployments,
            "deployment_utilization": (active_deployments / total_deployments * 100) if total_deployments > 0 else 0
        },
        "training_metrics": {
            "running_training_jobs": running_jobs,
            "completed_training_jobs": completed_jobs,
            "training_success_rate": (completed_jobs / (running_jobs + completed_jobs) * 100) if (running_jobs + completed_jobs) > 0 else 0
        },
        "evaluation_metrics": {
            "pending_evaluations": pending_evaluations,
            "production_approved": approved_evaluations,
            "approval_rate": (approved_evaluations / (pending_evaluations + approved_evaluations) * 100) if (pending_evaluations + approved_evaluations) > 0 else 0
        }
    }

@router.get("/analytics/deployment-performance")
async def get_deployment_performance_analytics(
    days: int = Query(30, description="Number of days for analysis"),
    db: Session = Depends(get_db)
):
    """Get deployment performance analytics"""
    date_threshold = datetime.utcnow() - timedelta(days=days)
    
    # Get deployment performance metrics
    metrics = db.query(ModelPerformanceMetric).filter(
        ModelPerformanceMetric.metric_timestamp >= date_threshold
    ).all()
    
    if not metrics:
        return {
            "analysis_period_days": days,
            "performance_summary": "No performance data available",
            "deployment_count": 0
        }
    
    # Calculate average performance metrics
    avg_accuracy = sum([m.accuracy_percentage for m in metrics if m.accuracy_percentage]) / len([m for m in metrics if m.accuracy_percentage]) if any(m.accuracy_percentage for m in metrics) else 0
    avg_f1_score = sum([m.f1_score for m in metrics if m.f1_score]) / len([m for m in metrics if m.f1_score]) if any(m.f1_score for m in metrics) else 0
    avg_inference_time = sum([m.inference_time_avg_ms for m in metrics if m.inference_time_avg_ms]) / len([m for m in metrics if m.inference_time_avg_ms]) if any(m.inference_time_avg_ms for m in metrics) else 0
    avg_throughput = sum([m.throughput_fps for m in metrics if m.throughput_fps]) / len([m for m in metrics if m.throughput_fps]) if any(m.throughput_fps for m in metrics) else 0
    
    # Calculate resource utilization
    avg_cpu = sum([m.cpu_utilization_avg for m in metrics if m.cpu_utilization_avg]) / len([m for m in metrics if m.cpu_utilization_avg]) if any(m.cpu_utilization_avg for m in metrics) else 0
    avg_gpu = sum([m.gpu_utilization_avg for m in metrics if m.gpu_utilization_avg]) / len([m for m in metrics if m.gpu_utilization_avg]) if any(m.gpu_utilization_avg for m in metrics) else 0
    
    # Count unique deployments
    unique_deployments = len(set([m.deployment_id for m in metrics]))
    
    return {
        "analysis_period_days": days,
        "deployment_count": unique_deployments,
        "performance_metrics": {
            "average_accuracy_percentage": avg_accuracy,
            "average_f1_score": avg_f1_score,
            "average_inference_time_ms": avg_inference_time,
            "average_throughput_fps": avg_throughput
        },
        "resource_utilization": {
            "average_cpu_utilization": avg_cpu,
            "average_gpu_utilization": avg_gpu
        },
        "total_metrics_collected": len(metrics)
    }