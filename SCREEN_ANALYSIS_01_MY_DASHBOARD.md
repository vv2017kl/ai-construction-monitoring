# 📊 Screen Analysis #01: My Dashboard (/dashboard)

## 📋 **Document Information**
- **Screen Path**: `/dashboard`
- **Menu Location**: Dashboard → My Dashboard
- **Portal**: Solution User Portal
- **Priority**: HIGH (Main landing screen)
- **Status**: ✅ Implemented and Functional

---

## 🎯 **Functional Analysis**

### **Primary Purpose**
Main dashboard providing comprehensive overview of current construction site status, real-time activities, alerts, and quick access to key system functions.

### **Core Features & User Workflows**

#### **1. Welcome Header Section**
- **Personalized greeting** with time-based salutation
- **Current site display** with project type and progress
- **Circular progress indicator** showing completion percentage
- **Dynamic weather conditions** for current site

#### **2. Key Metrics Grid (4 StatCards)**
- **Active Personnel**: Live count with trend comparison
- **Camera Status**: Available/total cameras with maintenance alerts
- **Active Alerts**: Alert count with critical alert breakdown
- **Safety Score**: 0-10 rating with PPE compliance percentage

#### **3. Live Site Activity Feed**
- **Real-time detection display** from AI processing
- **Personnel counting** with PPE compliance indicators
- **Camera-specific activity** with confidence levels
- **Timestamp tracking** for each detection event
- **Modal expansion** for detailed activity viewing

#### **4. Priority Alerts Panel**
- **Critical/High priority alerts** display (top 3)
- **Alert categorization** with color coding
- **Quick acknowledge/investigate** actions
- **Full alert center navigation**

#### **5. Site Conditions Widget**
- **Real-time weather data** (temperature, wind)
- **Working conditions assessment**
- **Environmental indicators** for safety planning

#### **6. Quick Actions Grid**
- **Live Monitoring**: Direct access to camera feeds
- **Street View Tour**: GPS-guided site inspection
- **Generate Report**: AI analytics and reporting
- **Field Assessment**: Mobile inspection tools

### **Interactive Elements**
- **Clickable StatCards**: Navigate to relevant screens
- **Live Activity Modal**: Detailed activity breakdown
- **Priority Alerts Modal**: Comprehensive alert management
- **Quick Action Buttons**: Direct feature access
- **Real-time updates**: Live data refresh indicators

---

## 🗃️ **Database Requirements**

### **Required Tables & Relationships**

#### **1. Sites Table**
```sql
CREATE TABLE sites (
    id UUID PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    code VARCHAR(50) UNIQUE NOT NULL,
    address TEXT,
    coordinates POINT,
    status ENUM('active', 'inactive', 'maintenance') DEFAULT 'active',
    type ENUM('commercial', 'residential', 'industrial', 'infrastructure'),
    phase ENUM('planning', 'construction', 'finishing', 'completed'),
    progress_percentage DECIMAL(5,2) DEFAULT 0.00,
    budget DECIMAL(15,2),
    completion_date DATE,
    manager_id UUID,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Missing fields needed for dashboard:
    weather_temp INT,
    weather_condition VARCHAR(100),
    weather_wind_speed VARCHAR(50),
    last_activity_timestamp TIMESTAMP,
    
    FOREIGN KEY (manager_id) REFERENCES users(id)
);
```

#### **2. Site_Personnel Table**
```sql
CREATE TABLE site_personnel (
    id UUID PRIMARY KEY,
    site_id UUID NOT NULL,
    user_id UUID NOT NULL,
    role VARCHAR(100),
    status ENUM('active', 'inactive', 'break', 'offsite') DEFAULT 'active',
    check_in_time TIMESTAMP,
    check_out_time TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Missing fields for dashboard:
    current_zone VARCHAR(100),
    ppe_compliance_score DECIMAL(5,2),
    last_detection_timestamp TIMESTAMP,
    
    FOREIGN KEY (site_id) REFERENCES sites(id),
    FOREIGN KEY (user_id) REFERENCES users(id),
    UNIQUE KEY unique_site_user_active (site_id, user_id, status)
);
```

#### **3. Alerts Table** 
```sql
CREATE TABLE alerts (
    id UUID PRIMARY KEY,
    site_id UUID NOT NULL,
    camera_id UUID,
    zone_id UUID,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    priority ENUM('critical', 'high', 'medium', 'low', 'info') NOT NULL,
    status ENUM('open', 'acknowledged', 'investigating', 'resolved') DEFAULT 'open',
    alert_type VARCHAR(100),
    confidence_score DECIMAL(5,2),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    acknowledged_at TIMESTAMP NULL,
    acknowledged_by UUID NULL,
    resolved_at TIMESTAMP NULL,
    resolved_by UUID NULL,
    
    -- Missing fields for dashboard:
    detection_data JSON, -- Store AI detection results
    image_url VARCHAR(500),
    video_clip_url VARCHAR(500),
    
    FOREIGN KEY (site_id) REFERENCES sites(id),
    FOREIGN KEY (camera_id) REFERENCES cameras(id),
    FOREIGN KEY (zone_id) REFERENCES zones(id),
    FOREIGN KEY (acknowledged_by) REFERENCES users(id),
    FOREIGN KEY (resolved_by) REFERENCES users(id)
);
```

#### **4. AI_Detections Table**
```sql
CREATE TABLE ai_detections (
    id UUID PRIMARY KEY,
    camera_id UUID NOT NULL,
    zone_id UUID,
    detection_type ENUM('person', 'vehicle', 'ppe', 'safety_violation', 'equipment'),
    person_count INT DEFAULT 0,
    confidence_score DECIMAL(5,2),
    bounding_boxes JSON, -- Store detection coordinates
    ppe_compliance_data JSON, -- PPE detection results
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    processed BOOLEAN DEFAULT FALSE,
    alert_generated BOOLEAN DEFAULT FALSE,
    
    -- Missing fields for dashboard:
    zone_name VARCHAR(100),
    activity_summary TEXT,
    safety_score DECIMAL(5,2),
    
    FOREIGN KEY (camera_id) REFERENCES cameras(id),
    FOREIGN KEY (zone_id) REFERENCES zones(id)
);
```

#### **5. Safety_Metrics Table**
```sql
CREATE TABLE safety_metrics (
    id UUID PRIMARY KEY,
    site_id UUID NOT NULL,
    date DATE NOT NULL,
    safety_score DECIMAL(3,1), -- 0.0 to 10.0
    ppe_compliance_rate DECIMAL(5,2), -- Percentage
    incident_count INT DEFAULT 0,
    near_miss_count INT DEFAULT 0,
    personnel_violations INT DEFAULT 0,
    equipment_violations INT DEFAULT 0,
    
    -- Missing fields for dashboard trends:
    week_comparison DECIMAL(5,2), -- % change from last week
    month_comparison DECIMAL(5,2), -- % change from last month
    
    FOREIGN KEY (site_id) REFERENCES sites(id),
    UNIQUE KEY unique_site_date (site_id, date)
);
```

### **Critical Missing Database Fields**
1. **Sites table**: Weather integration fields
2. **AI_Detections**: Zone names and activity summaries
3. **Safety_Metrics**: Trend comparison calculations
4. **Alerts**: Rich media (images/videos) from detections
5. **Site_Personnel**: Real-time location and PPE status

---

## 📹 **ZoneMinder Integration**

### **Required ZoneMinder MySQL Tables**

#### **1. Monitors Table**
```sql
-- Query active cameras per site
SELECT COUNT(*) as active_cameras
FROM Monitors m
JOIN site_cameras sc ON m.Id = sc.monitor_id  
WHERE sc.site_id = ? AND m.Enabled = 1;

-- Query camera maintenance status
SELECT m.Id, m.Name, m.Enabled, m.Function
FROM Monitors m
JOIN site_cameras sc ON m.Id = sc.monitor_id
WHERE sc.site_id = ? AND (m.Enabled = 0 OR m.Function = 'None');
```

#### **2. Events Table** 
```sql
-- Query recent activity events for live feed
SELECT e.Id, e.Name, e.StartTime, e.EndTime, e.Length,
       e.Frames, e.AlarmFrames, e.Score, m.Name as MonitorName
FROM Events e
JOIN Monitors m ON e.MonitorId = m.Id
JOIN site_cameras sc ON m.Id = sc.monitor_id
WHERE sc.site_id = ? 
  AND e.StartTime >= DATE_SUB(NOW(), INTERVAL 1 HOUR)
ORDER BY e.StartTime DESC
LIMIT 20;
```

#### **3. Stats Table**
```sql
-- Query camera performance metrics
SELECT s.MonitorId, s.ZoneId, AVG(s.Score) as avg_score,
       COUNT(*) as event_count
FROM Stats s
JOIN Monitors m ON s.MonitorId = m.Id
JOIN site_cameras sc ON m.Id = sc.monitor_id
WHERE sc.site_id = ?
  AND s.DateTime >= DATE_SUB(NOW(), INTERVAL 24 HOUR)
GROUP BY s.MonitorId, s.ZoneId;
```

### **ZoneMinder API Endpoints Required**
1. **GET** `/zm/api/monitors.json` - Camera status and configuration
2. **GET** `/zm/api/events.json?MonitorId={id}&page=1&limit=20` - Recent events
3. **GET** `/zm/api/events/{eventId}.json` - Specific event details
4. **GET** `/zm/api/monitors/{id}/live` - Live stream URLs
5. **POST** `/zm/api/monitors/{id}/restart` - Camera restart functionality

### **Live Stream Integration**
```javascript
// WebRTC/HLS stream URLs for live camera feeds
const streamUrls = {
  hls: `${zmBaseUrl}/zm/cgi-bin/nph-zms?mode=jpeg&scale=100&maxfps=30&monitor=${monitorId}`,
  mjpeg: `${zmBaseUrl}/zm/cgi-bin/nph-zms?mode=single&monitor=${monitorId}&scale=100`,
  webrtc: `wss://${zmHost}/ws?monitor=${monitorId}` // If WebRTC enabled
};
```

---

## 🤖 **AI/YOLO Integration (Roboflow)**

### **Required Roboflow Models**

#### **1. Person Detection Model**
```json
{
  "model_endpoint": "https://detect.roboflow.com/construction-person-detection/1",
  "input_format": {
    "image": "base64_encoded_string",
    "confidence": 0.5,
    "overlap": 0.3
  },
  "output_format": {
    "predictions": [
      {
        "class": "person",
        "confidence": 0.87,
        "x": 320,
        "y": 240,
        "width": 150,
        "height": 400
      }
    ],
    "image": {
      "width": 1920,
      "height": 1080
    }
  }
}
```

#### **2. PPE Detection Model**
```json
{
  "model_endpoint": "https://detect.roboflow.com/ppe-detection-safety/2", 
  "input_format": {
    "image": "base64_encoded_string",
    "confidence": 0.6,
    "overlap": 0.2
  },
  "output_format": {
    "predictions": [
      {
        "class": "hardhat",
        "confidence": 0.92,
        "x": 340,
        "y": 180,
        "width": 80,
        "height": 60
      },
      {
        "class": "safety_vest",
        "confidence": 0.88,
        "x": 320,
        "y": 250,
        "width": 120,
        "height": 180
      }
    ],
    "compliance_score": 85.5
  }
}
```

### **AI Processing Pipeline**

#### **Real-time Detection Workflow**
```python
def process_dashboard_detections():
    # 1. Get latest frame from ZoneMinder
    frame = get_latest_frame_from_zm(camera_id)
    
    # 2. Run YOLO person detection
    person_results = roboflow_detect(frame, 'person-detection')
    
    # 3. Run PPE detection for each person
    ppe_results = []
    for person in person_results['predictions']:
        person_crop = crop_image(frame, person['bbox'])
        ppe_result = roboflow_detect(person_crop, 'ppe-detection')
        ppe_results.append(ppe_result)
    
    # 4. Calculate compliance metrics
    compliance_data = {
        'person_count': len(person_results['predictions']),
        'ppe_compliance_rate': calculate_ppe_compliance(ppe_results),
        'safety_violations': detect_violations(person_results, ppe_results),
        'confidence_score': avg([r['confidence'] for r in person_results['predictions']])
    }
    
    # 5. Store in database
    store_ai_detection(camera_id, compliance_data)
    
    # 6. Generate alerts if needed
    if compliance_data['ppe_compliance_rate'] < 75:
        create_alert('PPE Violation', 'high', compliance_data)
```

#### **Event/JSON Structure for Dashboard**
```json
{
  "detection_event": {
    "id": "det_123456789",
    "camera_id": "cam_001",
    "zone_name": "Main Entrance",
    "timestamp": "2025-01-12T14:30:15Z",
    "detection_results": {
      "person_count": 3,
      "confidence": 0.89,
      "ppe_compliance": {
        "overall_rate": 78.5,
        "hardhat_compliance": 100.0,
        "vest_compliance": 66.7,
        "boots_compliance": 88.9
      },
      "violations": [
        {
          "type": "missing_safety_vest",
          "person_id": 2,
          "confidence": 0.92
        }
      ],
      "bounding_boxes": [
        {
          "person_id": 1,
          "bbox": [300, 150, 450, 600],
          "ppe_items": ["hardhat", "safety_vest", "boots"]
        }
      ]
    },
    "alert_generated": true,
    "alert_id": "alert_789123"
  }
}
```

---

## 🔗 **Backend API Requirements**

### **Required Endpoints**

#### **1. Dashboard Data Endpoint**
```http
GET /api/dashboard/overview?site_id={site_id}

Response:
{
  "site_info": {
    "id": "site_001",
    "name": "Downtown Plaza Project", 
    "progress": 67,
    "weather": {
      "temp": 72,
      "condition": "Partly Cloudy",
      "wind": "8 mph"
    }
  },
  "metrics": {
    "active_personnel": 45,
    "personnel_trend": "+12%",
    "camera_status": {
      "active": 23,
      "total": 24,
      "maintenance": 1
    },
    "active_alerts": 3,
    "critical_alerts": 1,
    "safety_score": 8.5,
    "ppe_compliance_rate": 87.2
  },
  "recent_activity": [...],
  "priority_alerts": [...]
}
```

#### **2. Live Activity Feed Endpoint**
```http
GET /api/dashboard/live-activity?site_id={site_id}&limit=10

Response:
{
  "activities": [
    {
      "id": "activity_001",
      "timestamp": "2025-01-12T14:30:15Z",
      "type": "person_detection",
      "camera": "Main Entrance Cam",
      "zone": "Entry Zone",
      "person_count": 3,
      "ppe_compliance": 78.5,
      "confidence": 89.2,
      "alert_generated": true
    }
  ],
  "total_count": 156,
  "last_updated": "2025-01-12T14:30:30Z"
}
```

#### **3. Priority Alerts Endpoint**
```http
GET /api/alerts/priority?site_id={site_id}&priorities[]=critical&priorities[]=high&limit=10

Response:
{
  "alerts": [
    {
      "id": "alert_001",
      "title": "PPE Violation Detected",
      "description": "Worker without safety vest in restricted area",
      "priority": "high",
      "status": "open",
      "timestamp": "2025-01-12T14:25:00Z",
      "camera": "Zone 3 Camera",
      "zone": "Restricted Area",
      "confidence": 94.5,
      "image_url": "/api/alerts/alert_001/snapshot",
      "actions_available": ["acknowledge", "investigate", "resolve"]
    }
  ]
}
```

#### **4. Quick Actions Endpoints**
```http
GET /api/cameras/live-streams?site_id={site_id}
GET /api/street-view/start-tour?site_id={site_id}  
GET /api/reports/generate-safety?site_id={site_id}
GET /api/field-assessment/mobile-tool?site_id={site_id}
```

### **Real-time Updates**
- **WebSocket connection**: `/ws/dashboard/{site_id}`
- **Event types**: `detection_update`, `alert_created`, `camera_status_change`, `personnel_update`
- **Update frequency**: Every 30 seconds for metrics, real-time for critical alerts

---

## ⚠️ **Identified Defects & Missing Features**

### **Database Gaps**
1. **Weather integration**: No weather API integration or storage
2. **Trend calculations**: Missing week/month comparison logic
3. **Real-time personnel tracking**: No live location updates
4. **PPE compliance history**: No historical compliance tracking
5. **Zone-based activity**: Limited zone management capabilities

### **ZoneMinder Integration Gaps**
1. **Site-Camera relationship**: Need mapping table for sites to ZM monitors
2. **Event correlation**: No automated correlation between ZM events and AI detections
3. **Camera health monitoring**: Missing camera offline/online status tracking
4. **Storage management**: No integration with ZM storage quotas

### **AI/YOLO Integration Gaps**
1. **Model versioning**: No version control for deployed models
2. **Batch processing**: Only real-time processing implemented
3. **Training data feedback**: No mechanism to improve models
4. **Multi-model orchestration**: Limited coordination between detection models

### **Performance Considerations**
1. **Caching strategy**: Dashboard data should be cached for 30-60 seconds
2. **Pagination**: Activity feeds need proper pagination
3. **Image optimization**: Snapshot images need compression/CDN
4. **Database indexing**: Critical indexes missing on timestamp and site_id fields

---

## 📈 **Success Metrics**
- **Page load time**: < 2 seconds
- **Data freshness**: Real-time updates within 30 seconds
- **Alert response time**: Critical alerts visible within 10 seconds
- **User engagement**: Average session time > 5 minutes

---

**Document Created**: 2025-01-12
**Next Screen**: GeoSpatial View (/cesium-dashboard)