# 🧠 SCREEN ANALYSIS #07: AI Analytics & Insights

## 📋 **Document Information**
- **Screen Name**: AI Analytics & Insights
- **Route**: `/ai-analytics`
- **Screen Type**: User Portal - Analytics Dashboard
- **Analysis Date**: 2025-01-12
- **Priority**: HIGH (TIER 1: Critical Operations)
- **Implementation Status**: ✅ Frontend Complete, ⏳ Backend Required

---

## 🎯 **Screen Purpose**
The AI Analytics screen provides comprehensive monitoring and analysis of AI model performance, detection accuracy, safety metrics tracking, and trend analysis for the construction site. It serves as the central hub for AI-driven insights and model optimization.

---

## 🖥️ **FRONTEND ANALYSIS**

### **Current Implementation Status: ✅ COMPLETE**
The frontend is fully implemented with comprehensive interactive features.

### **Core Components Implemented:**
1. **Analytics Dashboard Header** - Time range selectors, chart type controls, real-time toggle
2. **Key Performance Metrics Cards** - AI Confidence, PPE Compliance, Processing Speed, Safety Score
3. **Interactive Chart System** - Personnel detection trends, PPE compliance breakdown
4. **Model Performance Panel** - Detection accuracy, false positive rates, model versioning
5. **Safety Incident Tracking** - Real-time incidents and near-miss monitoring
6. **Camera Performance Table** - Individual camera analytics with sorting and filtering
7. **Export System** - CSV/JSON export with data preview
8. **Real-time Updates** - Live data refresh simulation
9. **Comparison Mode** - Period-over-period analysis capabilities

### **Interactive Features:**
- ✅ Time range selection (1h, 24h, 7d, 30d)
- ✅ Chart type switching (bar, line, pie)
- ✅ Real-time data toggle with auto-refresh
- ✅ Comparison mode for trend analysis
- ✅ Camera performance table with search/sort/filter
- ✅ Export modal with format selection
- ✅ Chart data detail exploration
- ✅ Quick action navigation links

---

## 📊 **FUNCTIONAL REQUIREMENTS**

### **F01: AI Model Performance Monitoring**
- **Track Model Metrics**: Detection accuracy, confidence scores, processing times
- **Model Versioning**: Track model updates and performance changes
- **Performance Comparison**: Compare current vs previous model versions
- **Accuracy Trending**: Historical accuracy tracking and trend analysis
- **False Positive Analysis**: Monitor and track false positive rates

### **F02: Detection Analytics Dashboard**
- **Real-time Detection Counts**: Live detection statistics per camera/zone
- **Detection Type Analysis**: Break down by person, PPE, vehicle, safety violations
- **Hourly/Daily Trends**: Time-series analysis of detection patterns
- **Confidence Score Distribution**: Analysis of AI confidence levels
- **Detection Success Rates**: Monitor detection success vs manual validation

### **F03: Safety Metrics Intelligence**
- **PPE Compliance Tracking**: Real-time and historical PPE compliance rates
- **Safety Score Calculation**: Composite safety scores based on AI detections
- **Incident Correlation**: Link AI detections to safety incidents
- **Risk Assessment**: AI-driven risk level assessments
- **Safety Trend Analysis**: Long-term safety performance trends

### **F04: Camera Performance Analytics**
- **Individual Camera Metrics**: Detection rates, accuracy, uptime per camera
- **Camera Comparison**: Side-by-side camera performance analysis
- **Performance Optimization**: Identify under-performing cameras
- **Coverage Analysis**: Analyze detection coverage by camera and zone
- **Health Monitoring**: Camera health scores based on performance

### **F05: Advanced Analytics & Reporting**
- **Time-range Flexibility**: Support 1h, 24h, 7d, 30d, custom ranges
- **Multi-dimensional Analysis**: Cross-analyze by time, location, camera, detection type
- **Export Capabilities**: CSV/JSON/PDF export with customizable data sets
- **Real-time Dashboard**: Live updates with configurable refresh rates
- **Comparison Tools**: Period-over-period and model-over-model comparisons

### **F06: AI Model Management Integration**
- **Model Performance Tracking**: Monitor active model performance
- **Model Deployment Analytics**: Track model rollout success
- **Training Data Insights**: Analyze training data effectiveness
- **Model Optimization Recommendations**: AI-driven model improvement suggestions
- **A/B Testing Support**: Compare different model versions in real-time

---

## 🗃️ **DATABASE REQUIREMENTS**

### **Primary Tables (Existing in Schema):**
All required tables already exist in `MASTER_DATABASE_SCHEMA.md`:

1. **`ai_detections`** - Core AI detection records with confidence scores
2. **`ai_models`** - AI model versions and performance metrics
3. **`cameras`** - Camera information and specifications
4. **`site_cameras`** - Site-specific camera configurations
5. **`alerts`** - Safety alerts generated from AI detections
6. **`safety_metrics`** - Historical safety performance data
7. **`analytics_cache`** - Cached analytics calculations for performance

### **New Tables Required:**

#### **`ai_model_performance_logs`**
```sql
CREATE TABLE ai_model_performance_logs (
    id UUID PRIMARY KEY,
    model_id UUID NOT NULL,
    
    -- Performance metrics
    evaluation_date DATE NOT NULL,
    evaluation_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    accuracy_score DECIMAL(5,2) NOT NULL,
    precision_score DECIMAL(5,2) NOT NULL,
    recall_score DECIMAL(5,2) NOT NULL,
    f1_score DECIMAL(5,2) NOT NULL,
    
    -- Processing performance
    avg_processing_time_ms INT NOT NULL,
    median_processing_time_ms INT,
    max_processing_time_ms INT,
    min_processing_time_ms INT,
    
    -- Detection statistics
    total_detections_processed INT DEFAULT 0,
    true_positives INT DEFAULT 0,
    false_positives INT DEFAULT 0,
    false_negatives INT DEFAULT 0,
    confidence_score_avg DECIMAL(5,2),
    confidence_score_std DECIMAL(5,2),
    
    -- Context information
    test_dataset_id UUID,
    site_id UUID,
    camera_subset JSON, -- Array of camera IDs used for evaluation
    
    -- Evaluation metadata
    evaluation_type ENUM('automated', 'manual', 'field_test', 'benchmark') DEFAULT 'automated',
    evaluated_by UUID,
    evaluation_notes TEXT,
    
    -- Comparison data
    compared_to_model_id UUID,
    performance_change_percentage DECIMAL(6,2),
    
    FOREIGN KEY (model_id) REFERENCES ai_models(id),
    FOREIGN KEY (site_id) REFERENCES sites(id),
    FOREIGN KEY (evaluated_by) REFERENCES users(id),
    FOREIGN KEY (compared_to_model_id) REFERENCES ai_models(id),
    
    INDEX idx_model_performance_model_date (model_id, evaluation_date DESC),
    INDEX idx_model_performance_accuracy (accuracy_score DESC),
    INDEX idx_model_performance_processing (avg_processing_time_ms),
    INDEX idx_model_performance_site (site_id, evaluation_date DESC)
);
```

#### **`ai_detection_analytics`**
```sql
CREATE TABLE ai_detection_analytics (
    id UUID PRIMARY KEY,
    
    -- Time and scope
    analysis_date DATE NOT NULL,
    analysis_hour INT, -- 0-23 for hourly granularity
    site_id UUID NOT NULL,
    camera_id UUID,
    zone_id UUID,
    
    -- Detection counts by type
    person_detections INT DEFAULT 0,
    ppe_detections INT DEFAULT 0,
    vehicle_detections INT DEFAULT 0,
    safety_violation_detections INT DEFAULT 0,
    equipment_detections INT DEFAULT 0,
    activity_detections INT DEFAULT 0,
    
    -- Quality metrics
    total_detections INT DEFAULT 0,
    high_confidence_detections INT DEFAULT 0, -- confidence > 0.8
    medium_confidence_detections INT DEFAULT 0, -- confidence 0.6-0.8
    low_confidence_detections INT DEFAULT 0, -- confidence < 0.6
    avg_confidence_score DECIMAL(5,2),
    
    -- Performance metrics
    avg_processing_time_ms INT,
    total_processing_time_ms BIGINT,
    failed_processing_count INT DEFAULT 0,
    
    -- Safety analysis
    safety_violations_detected INT DEFAULT 0,
    ppe_compliance_rate DECIMAL(5,2),
    risk_level_high_count INT DEFAULT 0,
    risk_level_medium_count INT DEFAULT 0,
    risk_level_low_count INT DEFAULT 0,
    
    -- Trend indicators
    detection_trend ENUM('increasing', 'stable', 'decreasing'),
    accuracy_trend ENUM('improving', 'stable', 'declining'),
    
    -- Model information
    primary_model_id UUID,
    model_version VARCHAR(50),
    
    calculated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (site_id) REFERENCES sites(id),
    FOREIGN KEY (camera_id) REFERENCES cameras(id),
    FOREIGN KEY (zone_id) REFERENCES zones(id),
    FOREIGN KEY (primary_model_id) REFERENCES ai_models(id),
    
    UNIQUE KEY unique_analytics_scope (site_id, camera_id, zone_id, analysis_date, analysis_hour),
    INDEX idx_detection_analytics_site_date (site_id, analysis_date DESC),
    INDEX idx_detection_analytics_camera_date (camera_id, analysis_date DESC),
    INDEX idx_detection_analytics_confidence (avg_confidence_score DESC),
    INDEX idx_detection_analytics_performance (avg_processing_time_ms)
);
```

#### **`camera_ai_performance`**
```sql
CREATE TABLE camera_ai_performance (
    id UUID PRIMARY KEY,
    camera_id UUID NOT NULL,
    analysis_date DATE NOT NULL,
    
    -- Detection performance
    total_detections INT DEFAULT 0,
    successful_detections INT DEFAULT 0,
    failed_detections INT DEFAULT 0,
    detection_success_rate DECIMAL(5,2),
    
    -- Accuracy metrics
    validated_detections INT DEFAULT 0,
    confirmed_true_positives INT DEFAULT 0,
    confirmed_false_positives INT DEFAULT 0,
    accuracy_rate DECIMAL(5,2),
    
    -- Processing performance
    avg_processing_time_ms INT,
    max_processing_time_ms INT,
    min_processing_time_ms INT,
    timeout_count INT DEFAULT 0,
    
    -- Quality scores
    image_quality_score DECIMAL(5,2), -- Based on resolution, lighting, etc.
    detection_quality_score DECIMAL(5,2), -- Based on detection success
    overall_performance_score DECIMAL(5,2),
    
    -- Camera health indicators
    uptime_percentage DECIMAL(5,2),
    connection_issues_count INT DEFAULT 0,
    stream_quality_issues_count INT DEFAULT 0,
    
    -- Detection type breakdown
    person_detection_rate DECIMAL(5,2),
    ppe_detection_rate DECIMAL(5,2),
    vehicle_detection_rate DECIMAL(5,2),
    equipment_detection_rate DECIMAL(5,2),
    
    -- Comparative ranking
    site_ranking INT, -- Rank among cameras at the site
    performance_tier ENUM('excellent', 'good', 'average', 'poor', 'critical'),
    
    -- Environment factors
    lighting_conditions_avg DECIMAL(5,2), -- 0-10 scale
    weather_impact_score DECIMAL(5,2), -- Weather effect on performance
    
    calculated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (camera_id) REFERENCES cameras(id),
    
    UNIQUE KEY unique_camera_date (camera_id, analysis_date),
    INDEX idx_camera_performance_date (analysis_date DESC),
    INDEX idx_camera_performance_score (overall_performance_score DESC),
    INDEX idx_camera_performance_accuracy (accuracy_rate DESC),
    INDEX idx_camera_performance_tier (performance_tier, overall_performance_score DESC)
);
```

### **Schema Updates Required:**
None - all existing tables support the AI Analytics requirements.

---

## 🎥 **ZONEMINDER INTEGRATION**

### **ZM01: Event Correlation for AI Performance**
**Purpose**: Correlate ZoneMinder events with AI detection performance
**Integration Points**:
- Link AI detections to ZM events via `event_correlations` table
- Analyze detection accuracy against manual ZM event validation
- Use ZM event data for AI model performance evaluation

### **ZM02: Video Analytics Performance**
**Purpose**: Analyze AI model performance on ZM recorded video
**Requirements**:
```python
# ZoneMinder Event Analysis
def analyze_zm_event_ai_performance(event_id, model_id):
    """
    Analyze AI model performance on specific ZM event
    Returns accuracy metrics and processing performance
    """
    return {
        'detection_accuracy': float,
        'processing_time': int,  # milliseconds
        'confidence_scores': [float],
        'detection_success': bool
    }
```

### **ZM03: Historical Video Re-analysis**
**Purpose**: Re-analyze historical ZM footage with new AI models
**Process**:
1. Query ZM database for historical events
2. Re-run AI analysis on stored footage
3. Compare results with original detections
4. Generate model improvement metrics

### **ZM04: Real-time Performance Monitoring**
**Purpose**: Monitor AI detection performance on live ZM streams
**Implementation**:
- Monitor processing latency for live detections
- Track detection success rates per camera
- Analyze correlation between ZM motion detection and AI detections

---

## 🤖 **ROBOFLOW AI INTEGRATION**

### **RF01: Model Performance API Integration**
**Purpose**: Integrate with Roboflow for model performance analytics
**API Endpoints Required**:
```python
# Roboflow Model Performance API
POST /api/roboflow/model-analytics
{
    "model_id": "construction-safety-v8",
    "time_range": "24h",
    "metrics": ["accuracy", "processing_time", "confidence"]
}
```

### **RF02: Detection Quality Analysis**
**Purpose**: Analyze detection quality and confidence distributions
**Implementation**:
- Batch analyze recent detections for quality metrics
- Calculate confidence score distributions
- Identify patterns in false positives/negatives
- Generate model optimization recommendations

### **RF03: Model Comparison Framework**
**Purpose**: Compare different Roboflow model versions
**Features**:
- A/B test different model versions
- Compare accuracy metrics across models
- Analyze processing performance differences
- Generate model deployment recommendations

### **RF04: Training Data Feedback Loop**
**Purpose**: Provide feedback to improve model training
**Process**:
1. Identify low-confidence detections
2. Flag false positives/negatives for manual review
3. Export training data suggestions to Roboflow
4. Track model improvement after retraining

### **RF05: Custom Model Analytics**
**Purpose**: Analytics for site-specific custom models
**Requirements**:
- Track custom model performance vs base models
- Analyze site-specific detection patterns
- Monitor custom model degradation over time
- Provide retraining recommendations

---

## 🔌 **BACKEND API REQUIREMENTS**

### **API01: Analytics Data Endpoints**

#### **GET /api/ai-analytics/overview**
```python
@app.get("/api/ai-analytics/overview")
async def get_analytics_overview(
    site_id: str,
    time_range: str = "24h",  # 1h, 24h, 7d, 30d
    db: Session = Depends(get_database)
):
    """Get AI analytics overview for dashboard"""
    return {
        "ai_performance": {
            "detection_count": int,
            "average_confidence": float,
            "processing_time_avg": int,  # ms
            "model_accuracy": float,
            "false_positive_rate": float
        },
        "safety_metrics": {
            "ppe_compliance_rate": float,
            "safety_score": float,
            "incident_count": int,
            "near_miss_count": int,
            "trend_direction": str
        },
        "camera_stats": {
            "total_cameras": int,
            "active_cameras": int,
            "avg_performance_score": float
        }
    }
```

#### **GET /api/ai-analytics/detections/trends**
```python
@app.get("/api/ai-analytics/detections/trends")
async def get_detection_trends(
    site_id: str,
    time_range: str = "24h",
    granularity: str = "hourly",  # hourly, daily
    detection_types: List[str] = Query(default=None),
    camera_ids: List[str] = Query(default=None)
):
    """Get detection trend data for charts"""
    return {
        "timeline": [
            {
                "timestamp": str,
                "detection_counts": {
                    "person": int,
                    "ppe": int,
                    "vehicle": int,
                    "violation": int
                },
                "confidence_avg": float,
                "processing_time_avg": int
            }
        ]
    }
```

### **API02: Model Performance Endpoints**

#### **GET /api/ai-analytics/models/performance**
```python
@app.get("/api/ai-analytics/models/performance")
async def get_model_performance(
    model_id: str = None,
    site_id: str = None,
    date_range: str = "7d"
):
    """Get AI model performance metrics"""
    return {
        "models": [
            {
                "model_id": str,
                "model_name": str,
                "version": str,
                "accuracy_metrics": {
                    "accuracy": float,
                    "precision": float,
                    "recall": float,
                    "f1_score": float
                },
                "performance_metrics": {
                    "avg_processing_time": int,
                    "total_detections": int,
                    "success_rate": float
                },
                "trend": {
                    "accuracy_change": float,
                    "performance_change": float,
                    "trend_direction": str
                }
            }
        ]
    }
```

#### **POST /api/ai-analytics/models/evaluate**
```python
@app.post("/api/ai-analytics/models/evaluate")
async def evaluate_model_performance(
    model_id: str,
    evaluation_config: dict
):
    """Trigger model performance evaluation"""
    return {
        "evaluation_id": str,
        "status": "started",
        "estimated_completion": str
    }
```

### **API03: Camera Analytics Endpoints**

#### **GET /api/ai-analytics/cameras/performance**
```python
@app.get("/api/ai-analytics/cameras/performance")
async def get_camera_performance(
    site_id: str,
    time_range: str = "24h",
    sort_by: str = "performance_score",
    sort_order: str = "desc"
):
    """Get camera performance analytics"""
    return {
        "cameras": [
            {
                "camera_id": str,
                "camera_name": str,
                "location": str,
                "performance_metrics": {
                    "detection_count": int,
                    "accuracy_rate": float,
                    "uptime_percentage": float,
                    "avg_processing_time": int,
                    "performance_score": float
                },
                "health_indicators": {
                    "connection_stability": float,
                    "image_quality": float,
                    "detection_success_rate": float
                },
                "ranking": {
                    "site_rank": int,
                    "performance_tier": str
                }
            }
        ]
    }
```

### **API04: Safety Analytics Endpoints**

#### **GET /api/ai-analytics/safety/metrics**
```python
@app.get("/api/ai-analytics/safety/metrics")
async def get_safety_analytics(
    site_id: str,
    time_range: str = "24h",
    include_predictions: bool = True
):
    """Get safety analytics and metrics"""
    return {
        "current_metrics": {
            "safety_score": float,
            "ppe_compliance_rate": float,
            "incident_count": int,
            "near_miss_count": int,
            "risk_level": str
        },
        "breakdown": {
            "ppe_compliance": {
                "hardhat": float,
                "vest": float,
                "boots": float,
                "gloves": float,
                "eye_protection": float
            },
            "violation_types": [
                {
                    "type": str,
                    "count": int,
                    "severity": str,
                    "trend": str
                }
            ]
        },
        "predictions": {
            "safety_trend": str,
            "risk_forecast": str,
            "recommendations": [str]
        }
    }
```

### **API05: Export and Reporting Endpoints**

#### **POST /api/ai-analytics/export**
```python
@app.post("/api/ai-analytics/export")
async def export_analytics_data(
    export_config: dict
):
    """Export analytics data in various formats"""
    # export_config includes: format, data_types, time_range, filters
    return {
        "export_id": str,
        "download_url": str,
        "expires_at": str,
        "file_size": int
    }
```

---

## 📈 **ADVANCED FEATURES**

### **AF01: Real-time Analytics Dashboard**
- Live data updates with WebSocket connections
- Real-time detection count updates
- Live performance metric streaming
- Dynamic threshold alerting

### **AF02: Predictive Analytics**
- Safety incident prediction based on AI trends
- Camera maintenance prediction using performance data
- Model performance degradation prediction
- Optimal deployment timing for model updates

### **AF03: Comparative Analysis Tools**
- Site-to-site performance comparisons
- Model version A/B testing results
- Historical performance comparisons
- Benchmark against industry standards

### **AF04: AI Model Optimization Recommendations**
- Automated model performance analysis
- Training data quality recommendations
- Model deployment optimization suggestions
- Performance tuning recommendations

---

## 🔄 **REAL-TIME REQUIREMENTS**

### **RT01: Live Data Streaming**
- WebSocket connection for real-time metrics
- 30-second refresh intervals for dashboard
- Live detection count updates
- Real-time performance alerts

### **RT02: Performance Monitoring**
- Continuous model performance tracking
- Real-time accuracy degradation alerts
- Live processing latency monitoring
- Automatic performance reporting

---

## 🎯 **SUCCESS CRITERIA**

### **Functional Success:**
- ✅ Real-time AI performance monitoring operational
- ✅ Historical trend analysis with 90%+ accuracy
- ✅ Camera performance ranking and optimization
- ✅ Export functionality for all data types
- ✅ Model comparison and evaluation tools

### **Performance Success:**
- Dashboard loads in <2 seconds
- Real-time updates with <5 second latency
- Export generation in <30 seconds
- Analytics calculations optimized with caching

### **Integration Success:**
- Full ZoneMinder event correlation
- Complete Roboflow model performance integration
- Seamless database analytics queries
- Real-time data pipeline operational

---

## 📋 **IMPLEMENTATION PRIORITY**

### **Phase 1: Core Analytics (Week 1)**
1. Database schema implementation (new tables)
2. Basic API endpoints for overview and trends
3. Model performance tracking setup
4. Camera analytics foundation

### **Phase 2: Advanced Features (Week 2)**
1. Real-time data pipeline setup
2. Export functionality implementation
3. Comparative analysis tools
4. Performance optimization features

### **Phase 3: AI Integration (Week 3)**
1. Complete Roboflow integration
2. ZoneMinder correlation system
3. Predictive analytics implementation
4. Advanced reporting capabilities

---

**Document Status**: ✅ Analysis Complete  
**Next Screen**: Video Review (`/video-review`)  
**Database Schema**: Update required - 3 new tables  
**Estimated Backend Development**: 2-3 weeks