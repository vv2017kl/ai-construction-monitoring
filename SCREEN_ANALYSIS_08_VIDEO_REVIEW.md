# 🎥 SCREEN ANALYSIS #08: Historical Video Review

## 📋 **Document Information**
- **Screen Name**: Historical Video Review
- **Route**: `/video-review`
- **Screen Type**: User Portal - Video Analysis & Forensics
- **Analysis Date**: 2025-01-12
- **Priority**: CRITICAL (TIER 1: Critical Operations)
- **Implementation Status**: ✅ Frontend Complete, ⏳ Backend Required

---

## 🎯 **Screen Purpose**
The Historical Video Review screen provides comprehensive video analysis capabilities for forensic investigation, incident review, compliance auditing, and evidence management. It serves as the primary interface for reviewing historical footage with advanced playback controls, timeline visualization, and evidence export capabilities.

---

## 🖥️ **FRONTEND ANALYSIS**

### **Current Implementation Status: ✅ COMPLETE**
The frontend is fully implemented with sophisticated video review and forensic analysis features.

### **Core Components Implemented:**
1. **Advanced Video Player** - Full-featured player with timestamp overlays and camera info
2. **Timeline Visualization** - Activity timeline with hourly granularity and incident markers
3. **Playback Controls** - Variable speed, seeking, bookmark management
4. **Date & Camera Selection** - Flexible video source selection interface
5. **Bookmark System** - Custom bookmarks with categorization and time-stamping
6. **Activity Analysis** - Visual activity intensity mapping across 24-hour periods
7. **Quick Actions Panel** - Navigation to related analysis tools
8. **Export Options** - Screenshot, video clip, and sharing capabilities

### **Interactive Features:**
- ✅ Variable playback speed (0.5x to 8x) with visual indicators
- ✅ Timeline seeking with activity visualization and incident markers
- ✅ Bookmark creation, categorization, and quick navigation
- ✅ Date and camera selection with historical data validation
- ✅ Activity timeline with hover tooltips and click-to-seek
- ✅ Export functionality for screenshots, clips, and share links
- ✅ Quick navigation to related analysis screens

### **Advanced Video Features:**
- Professional video player interface with overlay information
- Timeline scrubbing with visual activity indicators
- Bookmark system with type categorization (alert, safety, activity, custom)
- Activity intensity visualization with incident highlighting
- Real-time timestamp display with camera identification

---

## 📊 **FUNCTIONAL REQUIREMENTS**

### **F01: Historical Video Playback Management**
- **Multi-Date Video Access**: Browse and load video from any historical date
- **Multi-Camera Support**: Switch between different camera feeds for same time period
- **Advanced Playback Controls**: Variable speed (0.5x-8x), precise seeking, frame-by-frame
- **Timeline Navigation**: Visual timeline with activity indicators and incident markers
- **Continuous Playback**: Support for 24-hour continuous video review sessions

### **F02: Forensic Investigation Tools**
- **Timestamp Verification**: Precise timestamp display with timezone awareness
- **Evidence Marking**: Bookmark critical moments with detailed annotations
- **Incident Correlation**: Link video segments to alerts and safety incidents
- **Chain of Custody**: Maintain evidence integrity for legal compliance
- **Quality Analysis**: Video quality assessment and enhancement options

### **F03: Activity Pattern Analysis**
- **Timeline Visualization**: 24-hour activity intensity mapping
- **Incident Highlighting**: Visual markers for safety violations and alerts
- **Pattern Recognition**: Identify unusual activity patterns or anomalies
- **Multi-Camera Correlation**: Compare activity across multiple camera feeds
- **Statistical Insights**: Activity metrics and peak hour identification

### **F04: Bookmark & Annotation System**
- **Smart Bookmarking**: Automated bookmarks for AI-detected incidents
- **Custom Annotations**: User-created bookmarks with detailed descriptions
- **Bookmark Categories**: Classification by type (safety, incident, activity, custom)
- **Quick Navigation**: Jump to bookmarked moments instantly
- **Bookmark Export**: Export bookmark data for reporting and analysis

### **F05: Evidence Export & Sharing**
- **Video Clip Export**: Extract specific time ranges as video files
- **Screenshot Capture**: High-quality frame extraction at any timestamp
- **Evidence Packages**: Comprehensive evidence exports with metadata
- **Share Links**: Generate secure links for video review sharing
- **Format Options**: Multiple export formats (MP4, images, reports)

### **F06: Compliance & Audit Support**
- **Audit Trail**: Complete viewing history and user activity logs
- **Retention Management**: Automated video retention and archival
- **Compliance Reports**: Generate regulatory compliance documentation
- **Access Control**: Role-based permissions for sensitive footage
- **Legal Export**: Evidence exports formatted for legal proceedings

---

## 🗃️ **DATABASE REQUIREMENTS**

### **Primary Tables (Existing in Schema):**
Most required tables already exist in `MASTER_DATABASE_SCHEMA.md`:

1. **`cameras`** - Camera hardware and configuration information
2. **`site_cameras`** - Site-specific camera deployments and settings
3. **`recording_sessions`** - Recording session metadata and file information
4. **`alerts`** - Safety alerts and incidents linked to video footage
5. **`ai_detections`** - AI detection results correlated with video timestamps
6. **`users`** - User information for access control and audit trails
7. **`audit_logs`** - System activity logging for compliance

### **New Tables Required:**

#### **`video_bookmarks`**
```sql
CREATE TABLE video_bookmarks (
    id UUID PRIMARY KEY,
    camera_id UUID NOT NULL,
    user_id UUID NOT NULL,
    
    -- Temporal information
    bookmark_date DATE NOT NULL,
    timestamp_seconds INT NOT NULL, -- Seconds from start of day
    duration_seconds INT DEFAULT 10, -- Bookmark duration for clips
    
    -- Bookmark details
    title VARCHAR(255) NOT NULL,
    description TEXT,
    bookmark_type ENUM('safety_incident', 'ppe_violation', 'equipment_issue', 'person_activity', 'vehicle_activity', 'custom', 'alert_related', 'compliance_check') NOT NULL,
    
    -- Classification and priority
    priority_level ENUM('low', 'medium', 'high', 'critical') DEFAULT 'medium',
    severity ENUM('info', 'warning', 'error', 'critical') DEFAULT 'info',
    
    -- Evidence and correlation
    related_alert_id UUID,
    related_detection_id UUID,
    evidence_quality ENUM('poor', 'fair', 'good', 'excellent') DEFAULT 'good',
    
    -- User interaction
    is_shared BOOLEAN DEFAULT FALSE,
    share_permissions JSON, -- Array of user IDs or roles with access
    
    -- Visual markers
    thumbnail_timestamp INT, -- Best representative frame
    color_code VARCHAR(7) DEFAULT '#FFA500', -- Hex color for timeline display
    
    -- Metadata
    video_quality_at_time VARCHAR(50), -- Resolution/quality at bookmark time
    weather_conditions VARCHAR(100),
    lighting_conditions ENUM('excellent', 'good', 'fair', 'poor', 'very_poor'),
    
    -- Workflow status
    status ENUM('active', 'reviewed', 'resolved', 'archived') DEFAULT 'active',
    reviewed_by UUID,
    reviewed_at TIMESTAMP,
    review_notes TEXT,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (camera_id) REFERENCES cameras(id),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (related_alert_id) REFERENCES alerts(id),
    FOREIGN KEY (related_detection_id) REFERENCES ai_detections(id),
    FOREIGN KEY (reviewed_by) REFERENCES users(id),
    
    INDEX idx_video_bookmarks_camera_date (camera_id, bookmark_date DESC),
    INDEX idx_video_bookmarks_user (user_id, created_at DESC),
    INDEX idx_video_bookmarks_type (bookmark_type, priority_level),
    INDEX idx_video_bookmarks_timestamp (bookmark_date, timestamp_seconds),
    INDEX idx_video_bookmarks_status (status, created_at DESC),
    INDEX idx_video_bookmarks_shared (is_shared),
    UNIQUE KEY unique_user_camera_timestamp (user_id, camera_id, bookmark_date, timestamp_seconds)
);
```

#### **`video_access_logs`**
```sql
CREATE TABLE video_access_logs (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL,
    camera_id UUID NOT NULL,
    
    -- Access session details
    session_id UUID NOT NULL,
    access_start TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    access_end TIMESTAMP,
    session_duration_minutes INT,
    
    -- Video details accessed
    video_date DATE NOT NULL,
    start_timestamp_seconds INT NOT NULL, -- Start time in video
    end_timestamp_seconds INT, -- End time (if session completed)
    total_video_watched_seconds INT DEFAULT 0,
    
    -- Access method and context
    access_method ENUM('web_browser', 'mobile_app', 'api', 'export') DEFAULT 'web_browser',
    access_reason ENUM('routine_review', 'incident_investigation', 'compliance_audit', 'training', 'maintenance', 'legal_request') NOT NULL,
    
    -- User activity during session
    bookmarks_created INT DEFAULT 0,
    screenshots_taken INT DEFAULT 0,
    clips_exported INT DEFAULT 0,
    playback_speed_changes INT DEFAULT 0,
    
    -- Technical details
    ip_address INET,
    user_agent TEXT,
    browser_info JSON,
    
    -- Legal and compliance
    legal_hold_flag BOOLEAN DEFAULT FALSE,
    audit_flag BOOLEAN DEFAULT FALSE,
    retention_period_override INT, -- Days to retain this access record
    
    -- Performance metrics
    initial_load_time_ms INT,
    average_seek_time_ms INT,
    total_pause_time_seconds INT DEFAULT 0,
    
    -- Access outcome
    session_complete BOOLEAN DEFAULT FALSE,
    premature_termination_reason ENUM('user_logout', 'session_timeout', 'technical_error', 'policy_violation', 'system_maintenance'),
    
    -- Data export tracking
    export_count INT DEFAULT 0,
    export_details JSON, -- Details of any exports performed
    
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (camera_id) REFERENCES cameras(id),
    
    INDEX idx_video_access_user_time (user_id, access_start DESC),
    INDEX idx_video_access_camera_date (camera_id, video_date DESC),
    INDEX idx_video_access_session (session_id),
    INDEX idx_video_access_legal (legal_hold_flag, audit_flag),
    INDEX idx_video_access_reason (access_reason, access_start DESC)
);
```

#### **`video_exports`**
```sql
CREATE TABLE video_exports (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL,
    camera_id UUID NOT NULL,
    
    -- Export source details
    source_video_date DATE NOT NULL,
    start_timestamp_seconds INT NOT NULL,
    end_timestamp_seconds INT NOT NULL,
    export_duration_seconds INT NOT NULL,
    
    -- Export configuration
    export_type ENUM('video_clip', 'screenshot', 'evidence_package', 'compliance_report', 'share_link') NOT NULL,
    export_format VARCHAR(20) NOT NULL, -- mp4, jpg, png, pdf, zip
    resolution VARCHAR(20), -- Original, 1080p, 720p, 480p
    quality_setting ENUM('high', 'medium', 'low') DEFAULT 'high',
    include_audio BOOLEAN DEFAULT TRUE,
    
    -- Evidence and legal
    export_purpose ENUM('evidence', 'training', 'analysis', 'compliance', 'documentation', 'legal_proceeding') NOT NULL,
    chain_of_custody JSON, -- Evidence handling chain
    hash_verification VARCHAR(128), -- File integrity hash
    digital_signature VARCHAR(512), -- Legal authentication
    
    -- File information
    original_filename VARCHAR(255),
    stored_filename VARCHAR(255),
    file_path VARCHAR(500),
    file_size_bytes BIGINT,
    
    -- Processing status
    export_status ENUM('requested', 'processing', 'completed', 'failed', 'expired') DEFAULT 'requested',
    processing_started_at TIMESTAMP,
    processing_completed_at TIMESTAMP,
    processing_time_seconds INT,
    error_message TEXT,
    
    -- Access and sharing
    download_url VARCHAR(500),
    share_token VARCHAR(255) UNIQUE,
    download_expires_at TIMESTAMP,
    download_count INT DEFAULT 0,
    max_download_count INT DEFAULT 5,
    
    -- Metadata preservation
    original_metadata JSON, -- Camera settings, weather, etc.
    bookmark_data JSON, -- Any bookmarks within the export timeframe
    incident_data JSON, -- Related alerts and detections
    
    -- Audit and compliance
    export_justification TEXT NOT NULL,
    approval_required BOOLEAN DEFAULT FALSE,
    approved_by UUID,
    approved_at TIMESTAMP,
    legal_hold_applied BOOLEAN DEFAULT FALSE,
    retention_period_days INT DEFAULT 90,
    
    -- Performance tracking
    compression_ratio DECIMAL(5,2), -- Original size vs final size
    processing_efficiency_score DECIMAL(3,1), -- 1-10 efficiency rating
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (camera_id) REFERENCES cameras(id),
    FOREIGN KEY (approved_by) REFERENCES users(id),
    
    INDEX idx_video_exports_user_date (user_id, created_at DESC),
    INDEX idx_video_exports_camera (camera_id, source_video_date DESC),
    INDEX idx_video_exports_status (export_status, created_at DESC),
    INDEX idx_video_exports_purpose (export_purpose, created_at DESC),
    INDEX idx_video_exports_legal (legal_hold_applied, retention_period_days),
    INDEX idx_video_exports_share (share_token, download_expires_at)
);
```

#### **`video_quality_metrics`**
```sql
CREATE TABLE video_quality_metrics (
    id UUID PRIMARY KEY,
    camera_id UUID NOT NULL,
    analysis_date DATE NOT NULL,
    analysis_hour INT DEFAULT 0, -- 0-23 for hourly analysis
    
    -- Technical quality metrics
    average_bitrate_kbps INT,
    average_fps DECIMAL(5,2),
    resolution_width INT,
    resolution_height INT,
    
    -- Visual quality assessment
    sharpness_score DECIMAL(5,2), -- 0-10 scale
    brightness_score DECIMAL(5,2), -- 0-10 scale
    contrast_score DECIMAL(5,2), -- 0-10 scale
    color_accuracy_score DECIMAL(5,2), -- 0-10 scale
    noise_level_score DECIMAL(5,2), -- 0-10 scale (lower is better)
    
    -- Environmental factors
    lighting_condition ENUM('excellent', 'good', 'fair', 'poor', 'very_poor'),
    weather_impact ENUM('none', 'minimal', 'moderate', 'significant', 'severe'),
    obstruction_detected BOOLEAN DEFAULT FALSE,
    camera_shake_detected BOOLEAN DEFAULT FALSE,
    
    -- Usability for analysis
    forensic_quality_rating ENUM('excellent', 'good', 'acceptable', 'poor', 'unusable'),
    person_identification_viability ENUM('clear', 'good', 'limited', 'poor', 'impossible'),
    activity_recognition_viability ENUM('clear', 'good', 'limited', 'poor', 'impossible'),
    
    -- Storage and compression
    compression_efficiency DECIMAL(5,2),
    storage_size_mb DECIMAL(10,2),
    file_corruption_detected BOOLEAN DEFAULT FALSE,
    
    -- Recording continuity
    recording_gaps_detected BOOLEAN DEFAULT FALSE,
    total_gap_duration_seconds INT DEFAULT 0,
    frame_drops_count INT DEFAULT 0,
    sync_issues_detected BOOLEAN DEFAULT FALSE,
    
    -- Analysis metadata
    analysis_method ENUM('automated', 'manual', 'hybrid') DEFAULT 'automated',
    analysis_tool VARCHAR(100),
    analysis_confidence DECIMAL(5,2), -- Confidence in the quality assessment
    
    -- Improvement recommendations
    recommended_adjustments JSON, -- Settings adjustments to improve quality
    maintenance_flags JSON, -- Issues requiring camera maintenance
    
    calculated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (camera_id) REFERENCES cameras(id),
    
    UNIQUE KEY unique_camera_datetime (camera_id, analysis_date, analysis_hour),
    INDEX idx_video_quality_camera_date (camera_id, analysis_date DESC),
    INDEX idx_video_quality_forensic (forensic_quality_rating, camera_id),
    INDEX idx_video_quality_overall (sharpness_score, brightness_score, contrast_score),
    INDEX idx_video_quality_issues (file_corruption_detected, recording_gaps_detected),
    INDEX idx_video_quality_lighting (lighting_condition, analysis_date DESC)
);
```

### **Schema Updates Required:**
None - existing tables support core video review functionality.

---

## 🎥 **ZONEMINDER INTEGRATION**

### **ZM01: Historical Video Retrieval**
**Purpose**: Retrieve and stream historical video footage from ZoneMinder storage
**Integration Points**:
- Query ZM database for available recordings by date and camera
- Stream video files directly from ZM storage with proper authentication
- Support for multiple video formats and compression levels

**Implementation**:
```python
# ZoneMinder Historical Video API
def get_historical_video(camera_id, date, start_hour, end_hour):
    """
    Retrieve historical video from ZoneMinder storage
    Returns video stream URL and metadata
    """
    zm_query = f"""
    SELECT e.Id, e.Name, e.StartTime, e.EndTime, e.Length,
           e.Frames, e.AlarmFrames, e.DiskSpace, e.Path
    FROM Events e 
    WHERE e.MonitorId = {zm_monitor_id}
    AND DATE(e.StartTime) = '{date}'
    AND HOUR(e.StartTime) BETWEEN {start_hour} AND {end_hour}
    ORDER BY e.StartTime
    """
    return {
        'video_segments': [zm_events],
        'total_duration': int,
        'stream_urls': [urls],
        'quality_info': dict
    }
```

### **ZM02: Event Timeline Correlation**
**Purpose**: Correlate ZoneMinder motion events with video timeline
**Requirements**:
```python
# ZoneMinder Event Timeline Integration
def get_event_timeline(camera_id, date):
    """
    Get ZoneMinder events for timeline visualization
    """
    return {
        'events': [
            {
                'start_time': datetime,
                'end_time': datetime,
                'event_type': str,  # motion, alarm, continuous
                'alarm_frames': int,
                'score': int,  # Event score from ZM
                'thumbnail': str  # Thumbnail URL
            }
        ],
        'activity_intensity': [hourly_data]
    }
```

### **ZM03: Video Quality Assessment**
**Purpose**: Assess video quality using ZoneMinder metadata
**Process**:
1. Extract video quality metrics from ZM event data
2. Analyze frame rates, resolution, and compression
3. Identify recording gaps and quality issues
4. Generate quality reports for forensic analysis

### **ZM04: Export Integration**
**Purpose**: Export video segments using ZoneMinder's export capabilities
**Implementation**:
- Use ZM's video export API for clip generation
- Maintain ZM metadata in exported files
- Support for multiple export formats and qualities
- Preserve ZM event correlation in exports

---

## 🤖 **ROBOFLOW AI INTEGRATION**

### **RF01: AI Detection Overlay in Video**
**Purpose**: Display AI detection results overlaid on historical video
**API Integration**:
```python
# Roboflow Detection History API
POST /api/roboflow/detection-history
{
    "camera_id": "cam_001",
    "date": "2025-01-12",
    "start_time": "08:00:00",
    "end_time": "17:00:00",
    "include_bounding_boxes": true,
    "detection_types": ["person", "ppe", "vehicle"]
}
```

**Implementation**:
- Overlay bounding boxes on video at corresponding timestamps
- Display confidence scores and detection classifications
- Enable/disable overlay display for cleaner video review
- Color-code different detection types

### **RF02: Forensic Analysis Enhancement**
**Purpose**: Use AI to enhance video for forensic analysis
**Features**:
- Image enhancement for person identification
- Activity recognition and classification
- Anomaly detection in historical footage
- Evidence quality assessment

### **RF03: Automated Bookmark Generation**
**Purpose**: Automatically create bookmarks for significant AI detections
**Process**:
1. Analyze historical AI detection data for the selected video
2. Identify high-confidence or unusual detections
3. Generate bookmarks with AI-suggested labels
4. Allow user to accept, modify, or reject AI-generated bookmarks

### **RF04: Pattern Analysis**
**Purpose**: AI-powered pattern recognition in historical footage
**Capabilities**:
- Detect recurring safety violations
- Identify unusual activity patterns
- Personnel behavior analysis
- Equipment usage patterns

---

## 🔌 **BACKEND API REQUIREMENTS**

### **API01: Video Retrieval Endpoints**

#### **GET /api/video-review/available-dates**
```python
@app.get("/api/video-review/available-dates")
async def get_available_video_dates(
    camera_id: str,
    start_date: str = None,
    end_date: str = None
):
    """Get dates with available video footage for a camera"""
    return {
        "camera_id": str,
        "available_dates": [
            {
                "date": "2025-01-12",
                "total_duration_hours": float,
                "quality_rating": str,
                "events_count": int,
                "alerts_count": int,
                "gaps_detected": bool
            }
        ]
    }
```

#### **GET /api/video-review/stream**
```python
@app.get("/api/video-review/stream")
async def get_video_stream(
    camera_id: str,
    date: str,
    start_time: str = "00:00:00",
    end_time: str = "23:59:59",
    quality: str = "original"  # original, high, medium, low
):
    """Get video stream URL for specified time range"""
    return {
        "stream_url": str,
        "stream_type": str,  # hls, mp4, webm
        "duration_seconds": int,
        "resolution": str,
        "bitrate": int,
        "metadata": {
            "camera_info": dict,
            "weather_conditions": dict,
            "recording_quality": str
        }
    }
```

### **API02: Bookmark Management Endpoints**

#### **POST /api/video-review/bookmarks**
```python
@app.post("/api/video-review/bookmarks")
async def create_bookmark(
    bookmark_data: BookmarkCreate
):
    """Create a new video bookmark"""
    return {
        "bookmark_id": str,
        "status": "created",
        "bookmark_details": {
            "title": str,
            "timestamp": str,
            "type": str,
            "thumbnail_url": str
        }
    }
```

#### **GET /api/video-review/bookmarks**
```python
@app.get("/api/video-review/bookmarks")
async def get_bookmarks(
    camera_id: str,
    date: str,
    bookmark_type: str = None,
    user_id: str = None
):
    """Get bookmarks for specific video"""
    return {
        "bookmarks": [
            {
                "id": str,
                "title": str,
                "description": str,
                "timestamp_seconds": int,
                "bookmark_type": str,
                "priority_level": str,
                "created_by": str,
                "created_at": str,
                "thumbnail_url": str,
                "related_alert_id": str
            }
        ]
    }
```

### **API03: Timeline Analytics Endpoints**

#### **GET /api/video-review/timeline**
```python
@app.get("/api/video-review/timeline")
async def get_video_timeline(
    camera_id: str,
    date: str,
    granularity: str = "hourly"  # hourly, 15min, 5min
):
    """Get activity timeline for video review"""
    return {
        "timeline_data": [
            {
                "time_period": str,
                "activity_level": float,  # 0-100
                "incident_count": int,
                "detection_count": int,
                "quality_score": float,
                "events": [
                    {
                        "event_type": str,
                        "start_time": str,
                        "confidence": float,
                        "description": str
                    }
                ]
            }
        ],
        "summary": {
            "peak_activity_hour": int,
            "total_incidents": int,
            "average_quality": float
        }
    }
```

### **API04: Export Management Endpoints**

#### **POST /api/video-review/export**
```python
@app.post("/api/video-review/export")
async def create_video_export(
    export_request: VideoExportRequest
):
    """Create video export job"""
    return {
        "export_id": str,
        "status": "processing",
        "estimated_completion": str,
        "export_type": str,
        "file_size_estimate": int
    }
```

#### **GET /api/video-review/export/{export_id}/status**
```python
@app.get("/api/video-review/export/{export_id}/status")
async def get_export_status(export_id: str):
    """Get export job status"""
    return {
        "export_id": str,
        "status": str,  # processing, completed, failed
        "progress_percentage": int,
        "download_url": str,
        "expires_at": str,
        "file_info": {
            "filename": str,
            "size_bytes": int,
            "format": str,
            "duration_seconds": int
        }
    }
```

### **API05: Quality Assessment Endpoints**

#### **GET /api/video-review/quality-assessment**
```python
@app.get("/api/video-review/quality-assessment")
async def get_video_quality_assessment(
    camera_id: str,
    date: str,
    detailed: bool = False
):
    """Get video quality assessment for forensic analysis"""
    return {
        "overall_quality": {
            "forensic_rating": str,
            "technical_score": float,
            "usability_score": float
        },
        "detailed_metrics": {
            "resolution": str,
            "bitrate": int,
            "frame_rate": float,
            "sharpness_score": float,
            "lighting_score": float,
            "stability_score": float
        },
        "issues_detected": [
            {
                "issue_type": str,
                "severity": str,
                "time_range": str,
                "description": str,
                "impact_on_analysis": str
            }
        ],
        "recommendations": [str]
    }
```

---

## 📈 **ADVANCED FEATURES**

### **AF01: Multi-Camera Synchronization**
- Synchronized playback across multiple cameras
- Timeline correlation between different camera views
- Side-by-side comparison for incident analysis
- Cross-camera activity correlation

### **AF02: AI-Enhanced Video Analysis**
- Automated incident detection in historical footage
- Person tracking across multiple camera views
- Activity pattern recognition and anomaly detection
- Enhanced forensic capabilities with AI assistance

### **AF03: Legal Evidence Management**
- Chain of custody maintenance for exported evidence
- Digital signatures and hash verification
- Legal compliance reporting and documentation
- Secure evidence sharing with external parties

### **AF04: Advanced Search Capabilities**
- Search by detected objects (person, vehicle, equipment)
- Search by activity patterns or behaviors
- Search by time ranges with specific conditions
- Search by bookmark content and annotations

---

## 🔄 **REAL-TIME REQUIREMENTS**

### **RT01: Video Streaming Performance**
- Smooth video streaming with minimal buffering
- Adaptive quality based on network conditions
- Fast seeking with thumbnail previews
- Efficient caching for frequently accessed footage

### **RT02: Timeline Responsiveness**
- Real-time timeline updates as user navigates
- Smooth activity visualization updates
- Instant bookmark creation and display
- Responsive timeline scrubbing and seeking

---

## 🎯 **SUCCESS CRITERIA**

### **Functional Success:**
- ✅ Comprehensive historical video access with multi-camera support
- ✅ Advanced timeline visualization with activity and incident mapping
- ✅ Robust bookmark system with categorization and sharing
- ✅ Professional export capabilities for evidence and compliance
- ✅ Full ZoneMinder integration for seamless video retrieval

### **Performance Success:**
- Video streams load within 3 seconds
- Timeline navigation responds within 500ms
- Export generation completes within 2 minutes for 1-hour clips
- Search operations return results within 5 seconds

### **Integration Success:**
- Full ZoneMinder historical video access
- Complete AI detection overlay capabilities
- Seamless bookmark synchronization across users
- Reliable export functionality with metadata preservation

---

## 📋 **IMPLEMENTATION PRIORITY**

### **Phase 1: Core Video Review (Week 1)**
1. ZoneMinder integration for historical video access
2. Basic playback controls and timeline visualization
3. Bookmark creation and management system
4. Database schema implementation (4 new tables)

### **Phase 2: Advanced Analysis (Week 2)**
1. AI detection overlay system
2. Video quality assessment integration
3. Export functionality with evidence management
4. Multi-camera synchronization capabilities

### **Phase 3: Forensic & Compliance (Week 3)**
1. Legal evidence management and chain of custody
2. Advanced search and pattern recognition
3. Compliance reporting and audit trail
4. Performance optimization and caching

---

**Document Status**: ✅ Analysis Complete  
**Next Screen**: Reports Center (`/reports`)  
**Database Schema**: Update required - 4 new tables  
**Estimated Backend Development**: 3-4 weeks