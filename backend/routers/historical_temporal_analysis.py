"""
Historical Data & Temporal Analysis API Routes
Handles historical data snapshots, temporal analysis jobs, performance benchmarks, and predictive models
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_
from typing import List, Optional
from datetime import datetime, timedelta, date, time

from database import get_db
from models import (
    HistoricalDataSnapshot, TemporalAnalysisJob, PerformanceBenchmark, 
    PredictiveModel, PredictiveModelPrediction, User, Site,
    DataAnalysisType, AggregationPeriod, DataSourceType, AnalysisAlgorithm,
    JobStatus, TrendDirection, ModelStatus
)
from schemas import (
    HistoricalDataSnapshotResponse, HistoricalDataSnapshotCreateRequest,
    TemporalAnalysisJobResponse, TemporalAnalysisJobCreateRequest,
    PerformanceBenchmarkResponse, PerformanceBenchmarkCreateRequest,
    PredictiveModelResponse, PredictiveModelCreateRequest,
    PredictiveModelPredictionResponse, PredictiveModelPredictionCreateRequest
)

router = APIRouter(prefix="/historical-analysis", tags=["Historical Data & Temporal Analysis"])

# HISTORICAL DATA SNAPSHOTS ENDPOINTS

@router.get("/snapshots", response_model=List[HistoricalDataSnapshotResponse])
def get_all_snapshots(
    site_id: Optional[str] = Query(None, description="Filter by site ID"),
    data_source_type: Optional[str] = Query(None, description="Filter by data source type"),
    source_entity_id: Optional[str] = Query(None, description="Filter by source entity ID"),
    date_from: Optional[str] = Query(None, description="Filter from date (YYYY-MM-DD)"),
    date_to: Optional[str] = Query(None, description="Filter to date (YYYY-MM-DD)"),
    quality_threshold: Optional[float] = Query(None, description="Minimum data quality score"),
    db: Session = Depends(get_db)
):
    """Get all historical data snapshots with optional filtering"""
    query = db.query(HistoricalDataSnapshot)
    
    if site_id:
        query = query.filter(HistoricalDataSnapshot.site_id == site_id)
    
    if data_source_type:
        try:
            source_enum = DataSourceType(data_source_type)
            query = query.filter(HistoricalDataSnapshot.data_source_type == source_enum)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid data source type: {data_source_type}")
    
    if source_entity_id:
        query = query.filter(HistoricalDataSnapshot.source_entity_id == source_entity_id)
    
    if date_from:
        try:
            from_date = datetime.strptime(date_from, "%Y-%m-%d").date()
            query = query.filter(HistoricalDataSnapshot.snapshot_date >= from_date)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date_from format. Use YYYY-MM-DD")
    
    if date_to:
        try:
            to_date = datetime.strptime(date_to, "%Y-%m-%d").date()
            query = query.filter(HistoricalDataSnapshot.snapshot_date <= to_date)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date_to format. Use YYYY-MM-DD")
    
    if quality_threshold:
        query = query.filter(HistoricalDataSnapshot.data_accuracy_score >= quality_threshold)
    
    return query.order_by(HistoricalDataSnapshot.snapshot_date.desc(), HistoricalDataSnapshot.snapshot_time.desc()).all()

@router.post("/snapshots", response_model=HistoricalDataSnapshotResponse)
def create_snapshot(
    snapshot: HistoricalDataSnapshotCreateRequest,
    created_by: str = Query(..., description="User ID creating the snapshot"),
    db: Session = Depends(get_db)
):
    """Create a new historical data snapshot"""
    # Verify user exists
    user = db.query(User).filter(User.id == created_by).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Verify site exists
    site = db.query(Site).filter(Site.id == snapshot.site_id).first()
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    
    # Validate data source type
    try:
        DataSourceType(snapshot.data_source_type)
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid data source type: {snapshot.data_source_type}")
    
    # Parse date and time
    try:
        snapshot_date = datetime.strptime(snapshot.snapshot_date, "%Y-%m-%d").date()
        snapshot_time = datetime.strptime(snapshot.snapshot_time, "%H:%M:%S").time()
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date/time format. Use YYYY-MM-DD for date and HH:MM:SS for time")
    
    db_snapshot = HistoricalDataSnapshot(
        site_id=snapshot.site_id,
        snapshot_date=snapshot_date,
        snapshot_time=snapshot_time,
        data_source_type=snapshot.data_source_type,
        source_entity_id=snapshot.source_entity_id,
        source_entity_name=snapshot.source_entity_name,
        data_payload=snapshot.data_payload,
        data_metadata=snapshot.data_metadata,
        data_completeness_percentage=snapshot.data_completeness_percentage,
        data_accuracy_score=snapshot.data_accuracy_score,
        created_by=created_by
    )
    
    db.add(db_snapshot)
    db.commit()
    db.refresh(db_snapshot)
    
    return db_snapshot

@router.get("/snapshots/{snapshot_id}", response_model=HistoricalDataSnapshotResponse)
def get_snapshot(snapshot_id: str, db: Session = Depends(get_db)):
    """Get a specific historical data snapshot"""
    snapshot = db.query(HistoricalDataSnapshot).filter(HistoricalDataSnapshot.id == snapshot_id).first()
    if not snapshot:
        raise HTTPException(status_code=404, detail="Snapshot not found")
    return snapshot

@router.get("/snapshots/analytics/data-quality")
def get_data_quality_analytics(
    site_id: Optional[str] = Query(None, description="Filter by site ID"),
    days: Optional[int] = Query(None, description="Analytics period in days"),
    db: Session = Depends(get_db)
):
    """Get data quality analytics for snapshots"""
    query = db.query(HistoricalDataSnapshot)
    
    if site_id:
        query = query.filter(HistoricalDataSnapshot.site_id == site_id)
    
    if days:
        cutoff_date = datetime.now() - timedelta(days=days)
        query = query.filter(HistoricalDataSnapshot.processing_timestamp >= cutoff_date)
    
    total_snapshots = query.count()
    avg_completeness = query.with_entities(func.avg(HistoricalDataSnapshot.data_completeness_percentage)).scalar() or 0
    avg_accuracy = query.with_entities(func.avg(HistoricalDataSnapshot.data_accuracy_score)).scalar() or 0
    
    by_source = query.with_entities(
        HistoricalDataSnapshot.data_source_type,
        func.count(HistoricalDataSnapshot.id).label('count'),
        func.avg(HistoricalDataSnapshot.data_accuracy_score).label('avg_accuracy')
    ).group_by(HistoricalDataSnapshot.data_source_type).all()
    
    return {
        "total_snapshots": total_snapshots,
        "average_completeness": float(avg_completeness),
        "average_accuracy": float(avg_accuracy),
        "by_source": [
            {
                "source_type": item.data_source_type.value,
                "count": item.count,
                "average_accuracy": float(item.avg_accuracy or 0)
            }
            for item in by_source
        ],
        "period_days": days or "all_time"
    }

# TEMPORAL ANALYSIS JOBS ENDPOINTS

@router.get("/analysis-jobs", response_model=List[TemporalAnalysisJobResponse])
def get_all_analysis_jobs(
    site_id: Optional[str] = Query(None, description="Filter by site ID"),
    analysis_type: Optional[str] = Query(None, description="Filter by analysis type"),
    status: Optional[str] = Query(None, description="Filter by job status"),
    db: Session = Depends(get_db)
):
    """Get all temporal analysis jobs with optional filtering"""
    query = db.query(TemporalAnalysisJob)
    
    if site_id:
        query = query.filter(TemporalAnalysisJob.site_id == site_id)
    
    if analysis_type:
        try:
            type_enum = DataAnalysisType(analysis_type)
            query = query.filter(TemporalAnalysisJob.analysis_type == type_enum)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid analysis type: {analysis_type}")
    
    if status:
        try:
            status_enum = JobStatus(status)
            query = query.filter(TemporalAnalysisJob.status == status_enum)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid status: {status}")
    
    return query.order_by(TemporalAnalysisJob.created_at.desc()).all()

@router.post("/analysis-jobs", response_model=TemporalAnalysisJobResponse)
def create_analysis_job(
    job: TemporalAnalysisJobCreateRequest,
    created_by: str = Query(..., description="User ID creating the job"),
    db: Session = Depends(get_db)
):
    """Create a new temporal analysis job"""
    # Verify user exists
    user = db.query(User).filter(User.id == created_by).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Verify site exists
    site = db.query(Site).filter(Site.id == job.site_id).first()
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    
    # Validate enums
    try:
        DataAnalysisType(job.analysis_type)
        AggregationPeriod(job.aggregation_period)
        AnalysisAlgorithm(job.algorithm)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid enum value: {str(e)}")
    
    # Parse dates
    try:
        start_date = datetime.strptime(job.start_date, "%Y-%m-%d").date()
        end_date = datetime.strptime(job.end_date, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")
    
    if start_date >= end_date:
        raise HTTPException(status_code=400, detail="Start date must be before end date")
    
    db_job = TemporalAnalysisJob(
        site_id=job.site_id,
        job_name=job.job_name,
        analysis_type=job.analysis_type,
        aggregation_period=job.aggregation_period,
        algorithm=job.algorithm,
        start_date=start_date,
        end_date=end_date,
        include_weekends=job.include_weekends,
        include_holidays=job.include_holidays,
        data_sources=job.data_sources,
        filter_criteria=job.filter_criteria,
        scheduled_at=job.scheduled_at,
        created_by=created_by
    )
    
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    
    return db_job

@router.get("/analysis-jobs/{job_id}", response_model=TemporalAnalysisJobResponse)
def get_analysis_job(job_id: str, db: Session = Depends(get_db)):
    """Get a specific temporal analysis job"""
    job = db.query(TemporalAnalysisJob).filter(TemporalAnalysisJob.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Analysis job not found")
    return job

@router.put("/analysis-jobs/{job_id}", response_model=TemporalAnalysisJobResponse)
def update_analysis_job(
    job_id: str,
    job_data: dict,
    db: Session = Depends(get_db)
):
    """Update a temporal analysis job (typically for status and results)"""
    job = db.query(TemporalAnalysisJob).filter(TemporalAnalysisJob.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Analysis job not found")
    
    # Set completion time if status changed to completed
    if "status" in job_data and job_data["status"] == "completed" and not job.completed_at:
        job_data["completed_at"] = datetime.now()
        if job.started_at:
            job_data["execution_duration_seconds"] = int((datetime.now() - job.started_at).total_seconds())
    
    for key, value in job_data.items():
        if hasattr(job, key):
            setattr(job, key, value)
    
    db.commit()
    db.refresh(job)
    return job

# PERFORMANCE BENCHMARKS ENDPOINTS

@router.get("/benchmarks", response_model=List[PerformanceBenchmarkResponse])
def get_all_benchmarks(
    site_id: Optional[str] = Query(None, description="Filter by site ID"),
    benchmark_category: Optional[str] = Query(None, description="Filter by benchmark category"),
    date_from: Optional[str] = Query(None, description="Filter from date (YYYY-MM-DD)"),
    date_to: Optional[str] = Query(None, description="Filter to date (YYYY-MM-DD)"),
    db: Session = Depends(get_db)
):
    """Get all performance benchmarks with optional filtering"""
    query = db.query(PerformanceBenchmark)
    
    if site_id:
        query = query.filter(PerformanceBenchmark.site_id == site_id)
    
    if benchmark_category:
        query = query.filter(PerformanceBenchmark.benchmark_category.ilike(f"%{benchmark_category}%"))
    
    if date_from:
        try:
            from_date = datetime.strptime(date_from, "%Y-%m-%d").date()
            query = query.filter(PerformanceBenchmark.measurement_date >= from_date)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date_from format. Use YYYY-MM-DD")
    
    if date_to:
        try:
            to_date = datetime.strptime(date_to, "%Y-%m-%d").date()
            query = query.filter(PerformanceBenchmark.measurement_date <= to_date)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date_to format. Use YYYY-MM-DD")
    
    return query.order_by(PerformanceBenchmark.measurement_date.desc()).all()

@router.post("/benchmarks", response_model=PerformanceBenchmarkResponse)
def create_benchmark(
    benchmark: PerformanceBenchmarkCreateRequest,
    created_by: str = Query(..., description="User ID creating the benchmark"),
    db: Session = Depends(get_db)
):
    """Create a new performance benchmark"""
    # Verify user exists
    user = db.query(User).filter(User.id == created_by).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Verify site exists
    site = db.query(Site).filter(Site.id == benchmark.site_id).first()
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    
    # Parse measurement date
    try:
        measurement_date = datetime.strptime(benchmark.measurement_date, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid measurement_date format. Use YYYY-MM-DD")
    
    # Calculate performance percentages
    performance_percentage = None
    improvement_percentage = None
    variance_percentage = None
    
    if benchmark.target_value and benchmark.target_value != 0:
        performance_percentage = (benchmark.current_value / benchmark.target_value) * 100
    
    if benchmark.baseline_value and benchmark.baseline_value != 0:
        improvement_percentage = ((benchmark.current_value - benchmark.baseline_value) / benchmark.baseline_value) * 100
    
    if benchmark.industry_average and benchmark.industry_average != 0:
        variance_percentage = ((benchmark.current_value - benchmark.industry_average) / benchmark.industry_average) * 100
    
    db_benchmark = PerformanceBenchmark(
        site_id=benchmark.site_id,
        benchmark_name=benchmark.benchmark_name,
        benchmark_category=benchmark.benchmark_category,
        measurement_date=measurement_date,
        current_value=benchmark.current_value,
        target_value=benchmark.target_value,
        baseline_value=benchmark.baseline_value,
        industry_average=benchmark.industry_average,
        performance_percentage=performance_percentage,
        improvement_percentage=improvement_percentage,
        variance_percentage=variance_percentage,
        measurement_method=benchmark.measurement_method,
        data_source_entities=benchmark.data_source_entities,
        external_factors=benchmark.external_factors,
        confidence_level=benchmark.confidence_level,
        sample_size=benchmark.sample_size,
        created_by=created_by
    )
    
    db.add(db_benchmark)
    db.commit()
    db.refresh(db_benchmark)
    
    return db_benchmark

@router.get("/benchmarks/{benchmark_id}", response_model=PerformanceBenchmarkResponse)
def get_benchmark(benchmark_id: str, db: Session = Depends(get_db)):
    """Get a specific performance benchmark"""
    benchmark = db.query(PerformanceBenchmark).filter(PerformanceBenchmark.id == benchmark_id).first()
    if not benchmark:
        raise HTTPException(status_code=404, detail="Benchmark not found")
    return benchmark

@router.get("/benchmarks/analytics/performance-summary")
def get_performance_analytics_summary(
    site_id: Optional[str] = Query(None, description="Filter by site ID"),
    category: Optional[str] = Query(None, description="Filter by category"),
    days: Optional[int] = Query(None, description="Analytics period in days"),
    db: Session = Depends(get_db)
):
    """Get performance benchmarks analytics summary"""
    query = db.query(PerformanceBenchmark)
    
    if site_id:
        query = query.filter(PerformanceBenchmark.site_id == site_id)
    
    if category:
        query = query.filter(PerformanceBenchmark.benchmark_category.ilike(f"%{category}%"))
    
    if days:
        cutoff_date = datetime.now() - timedelta(days=days)
        query = query.filter(PerformanceBenchmark.measurement_date >= cutoff_date.date())
    
    total_benchmarks = query.count()
    avg_performance = query.with_entities(func.avg(PerformanceBenchmark.performance_percentage)).scalar() or 0
    avg_improvement = query.with_entities(func.avg(PerformanceBenchmark.improvement_percentage)).scalar() or 0
    
    # Count benchmarks above target (performance > 100%)
    above_target = query.filter(PerformanceBenchmark.performance_percentage > 100).count()
    
    by_category = query.with_entities(
        PerformanceBenchmark.benchmark_category,
        func.count(PerformanceBenchmark.id).label('count'),
        func.avg(PerformanceBenchmark.performance_percentage).label('avg_performance')
    ).group_by(PerformanceBenchmark.benchmark_category).all()
    
    return {
        "total_benchmarks": total_benchmarks,
        "average_performance_percentage": float(avg_performance),
        "average_improvement_percentage": float(avg_improvement),
        "benchmarks_above_target": above_target,
        "target_achievement_rate": (above_target / total_benchmarks * 100) if total_benchmarks > 0 else 0,
        "by_category": [
            {
                "category": item.benchmark_category,
                "count": item.count,
                "average_performance": float(item.avg_performance or 0)
            }
            for item in by_category
        ],
        "period_days": days or "all_time"
    }

# PREDICTIVE MODELS ENDPOINTS

@router.get("/models", response_model=List[PredictiveModelResponse])
def get_all_models(
    site_id: Optional[str] = Query(None, description="Filter by site ID"),
    model_type: Optional[str] = Query(None, description="Filter by model type"),
    status: Optional[str] = Query(None, description="Filter by model status"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    db: Session = Depends(get_db)
):
    """Get all predictive models with optional filtering"""
    query = db.query(PredictiveModel)
    
    if site_id:
        query = query.filter(PredictiveModel.site_id == site_id)
    
    if model_type:
        query = query.filter(PredictiveModel.model_type.ilike(f"%{model_type}%"))
    
    if status:
        try:
            status_enum = ModelStatus(status)
            query = query.filter(PredictiveModel.status == status_enum)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid status: {status}")
    
    if is_active is not None:
        query = query.filter(PredictiveModel.is_active == is_active)
    
    return query.order_by(PredictiveModel.created_at.desc()).all()

@router.post("/models", response_model=PredictiveModelResponse)
def create_model(
    model: PredictiveModelCreateRequest,
    created_by: str = Query(..., description="User ID creating the model"),
    db: Session = Depends(get_db)
):
    """Create a new predictive model"""
    # Verify user exists
    user = db.query(User).filter(User.id == created_by).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Verify site exists
    site = db.query(Site).filter(Site.id == model.site_id).first()
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    
    # Validate enums
    try:
        AnalysisAlgorithm(model.algorithm)
        AggregationPeriod(model.prediction_frequency)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid enum value: {str(e)}")
    
    # Parse training dates
    try:
        training_start_date = datetime.strptime(model.training_start_date, "%Y-%m-%d").date()
        training_end_date = datetime.strptime(model.training_end_date, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")
    
    if training_start_date >= training_end_date:
        raise HTTPException(status_code=400, detail="Training start date must be before end date")
    
    db_model = PredictiveModel(
        site_id=model.site_id,
        model_name=model.model_name,
        model_type=model.model_type,
        prediction_target=model.prediction_target,
        algorithm=model.algorithm,
        input_features=model.input_features,
        hyperparameters=model.hyperparameters,
        training_data_period_days=model.training_data_period_days,
        training_start_date=training_start_date,
        training_end_date=training_end_date,
        prediction_horizon_days=model.prediction_horizon_days,
        prediction_frequency=model.prediction_frequency,
        confidence_threshold=model.confidence_threshold,
        version=model.version,
        created_by=created_by
    )
    
    db.add(db_model)
    db.commit()
    db.refresh(db_model)
    
    return db_model

@router.get("/models/{model_id}", response_model=PredictiveModelResponse)
def get_model(model_id: str, db: Session = Depends(get_db)):
    """Get a specific predictive model"""
    model = db.query(PredictiveModel).filter(PredictiveModel.id == model_id).first()
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")
    return model

@router.put("/models/{model_id}", response_model=PredictiveModelResponse)
def update_model(
    model_id: str,
    model_data: dict,
    db: Session = Depends(get_db)
):
    """Update a predictive model (typically for performance metrics and deployment)"""
    model = db.query(PredictiveModel).filter(PredictiveModel.id == model_id).first()
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")
    
    # Set deployment date if model is being activated
    if "is_active" in model_data and model_data["is_active"] and not model.deployment_date:
        model_data["deployment_date"] = datetime.now().date()
    
    for key, value in model_data.items():
        if hasattr(model, key):
            setattr(model, key, value)
    
    db.commit()
    db.refresh(model)
    return model

# PREDICTIVE MODEL PREDICTIONS ENDPOINTS

@router.get("/predictions", response_model=List[PredictiveModelPredictionResponse])
def get_all_predictions(
    model_id: Optional[str] = Query(None, description="Filter by model ID"),
    site_id: Optional[str] = Query(None, description="Filter by site ID"),
    target_date: Optional[str] = Query(None, description="Filter by target date (YYYY-MM-DD)"),
    validated: Optional[bool] = Query(None, description="Filter by validation status"),
    db: Session = Depends(get_db)
):
    """Get all predictive model predictions with optional filtering"""
    query = db.query(PredictiveModelPrediction)
    
    if model_id:
        query = query.filter(PredictiveModelPrediction.model_id == model_id)
    
    if site_id:
        query = query.filter(PredictiveModelPrediction.site_id == site_id)
    
    if target_date:
        try:
            target_dt = datetime.strptime(target_date, "%Y-%m-%d").date()
            query = query.filter(PredictiveModelPrediction.target_date == target_dt)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid target_date format. Use YYYY-MM-DD")
    
    if validated is not None:
        if validated:
            query = query.filter(PredictiveModelPrediction.actual_value.isnot(None))
        else:
            query = query.filter(PredictiveModelPrediction.actual_value.is_(None))
    
    return query.order_by(PredictiveModelPrediction.created_at.desc()).all()

@router.post("/predictions", response_model=PredictiveModelPredictionResponse)
def create_prediction(
    prediction: PredictiveModelPredictionCreateRequest,
    db: Session = Depends(get_db)
):
    """Create a new predictive model prediction"""
    # Verify model exists
    model = db.query(PredictiveModel).filter(PredictiveModel.id == prediction.model_id).first()
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")
    
    # Verify site exists
    site = db.query(Site).filter(Site.id == prediction.site_id).first()
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    
    # Parse dates
    try:
        prediction_date = datetime.strptime(prediction.prediction_date, "%Y-%m-%d").date()
        target_date = datetime.strptime(prediction.target_date, "%Y-%m-%d").date()
        target_time_obj = None
        if prediction.target_time:
            target_time_obj = datetime.strptime(prediction.target_time, "%H:%M:%S").time()
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date/time format. Use YYYY-MM-DD for dates and HH:MM:SS for time")
    
    db_prediction = PredictiveModelPrediction(
        model_id=prediction.model_id,
        site_id=prediction.site_id,
        prediction_date=prediction_date,
        target_date=target_date,
        target_time=target_time_obj,
        predicted_value=prediction.predicted_value,
        confidence_score=prediction.confidence_score,
        prediction_interval_lower=prediction.prediction_interval_lower,
        prediction_interval_upper=prediction.prediction_interval_upper,
        input_features_snapshot=prediction.input_features_snapshot,
        feature_values=prediction.feature_values,
        prediction_context=prediction.prediction_context
    )
    
    db.add(db_prediction)
    db.commit()
    db.refresh(db_prediction)
    
    return db_prediction

@router.get("/predictions/{prediction_id}", response_model=PredictiveModelPredictionResponse)
def get_prediction(prediction_id: str, db: Session = Depends(get_db)):
    """Get a specific predictive model prediction"""
    prediction = db.query(PredictiveModelPrediction).filter(PredictiveModelPrediction.id == prediction_id).first()
    if not prediction:
        raise HTTPException(status_code=404, detail="Prediction not found")
    return prediction

@router.put("/predictions/{prediction_id}/validate", response_model=PredictiveModelPredictionResponse)
def validate_prediction(
    prediction_id: str,
    actual_value: float = Query(..., description="The actual observed value"),
    db: Session = Depends(get_db)
):
    """Validate a prediction with actual observed value"""
    prediction = db.query(PredictiveModelPrediction).filter(PredictiveModelPrediction.id == prediction_id).first()
    if not prediction:
        raise HTTPException(status_code=404, detail="Prediction not found")
    
    # Calculate prediction metrics
    prediction_error = actual_value - prediction.predicted_value
    absolute_error = abs(prediction_error)
    percentage_error = (prediction_error / actual_value * 100) if actual_value != 0 else 0
    
    # Get model confidence threshold to determine accuracy
    model = db.query(PredictiveModel).filter(PredictiveModel.id == prediction.model_id).first()
    confidence_threshold = model.confidence_threshold if model else 80.0
    
    is_accurate = prediction.confidence_score >= confidence_threshold and abs(percentage_error) <= 20.0
    
    # Update prediction with validation data
    prediction.actual_value = actual_value
    prediction.prediction_error = prediction_error
    prediction.absolute_error = absolute_error
    prediction.percentage_error = percentage_error
    prediction.is_accurate = is_accurate
    prediction.validated_at = datetime.now()
    
    db.commit()
    db.refresh(prediction)
    
    return prediction

@router.get("/predictions/analytics/model-performance")
def get_model_performance_analytics(
    model_id: Optional[str] = Query(None, description="Filter by model ID"),
    days: Optional[int] = Query(None, description="Analytics period in days"),
    db: Session = Depends(get_db)
):
    """Get predictive model performance analytics"""
    query = db.query(PredictiveModelPrediction).filter(PredictiveModelPrediction.actual_value.isnot(None))
    
    if model_id:
        query = query.filter(PredictiveModelPrediction.model_id == model_id)
    
    if days:
        cutoff_date = datetime.now() - timedelta(days=days)
        query = query.filter(PredictiveModelPrediction.created_at >= cutoff_date)
    
    total_predictions = query.count()
    accurate_predictions = query.filter(PredictiveModelPrediction.is_accurate == True).count()
    avg_confidence = query.with_entities(func.avg(PredictiveModelPrediction.confidence_score)).scalar() or 0
    avg_absolute_error = query.with_entities(func.avg(PredictiveModelPrediction.absolute_error)).scalar() or 0
    avg_percentage_error = query.with_entities(func.avg(func.abs(PredictiveModelPrediction.percentage_error))).scalar() or 0
    
    return {
        "total_validated_predictions": total_predictions,
        "accurate_predictions": accurate_predictions,
        "accuracy_rate": (accurate_predictions / total_predictions * 100) if total_predictions > 0 else 0,
        "average_confidence_score": float(avg_confidence),
        "average_absolute_error": float(avg_absolute_error),
        "average_percentage_error": float(avg_percentage_error),
        "period_days": days or "all_time"
    }