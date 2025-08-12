# 🚨 Screen Analysis #04: Alert Center (/alert-center)

## 📋 **Document Information**
- **Screen Path**: `/alert-center`
- **Menu Location**: Safety & Alerts → Alert Center
- **Portal**: Solution User Portal
- **Priority**: CRITICAL (Safety management)
- **Status**: ✅ Implemented and Functional

---

## 🎯 **Functional Analysis**

### **Primary Purpose**
Centralized alert management system for monitoring, investigating, and resolving safety violations, equipment issues, and access violations detected through AI monitoring and manual reporting across construction sites.

### **Core Features & User Workflows**

#### **1. Alert Dashboard & Statistics**
- **Real-time Alert Metrics**:
  - Total alerts count with live updates
  - Critical alerts requiring immediate action
  - Open alerts pending investigation
  - In-progress investigations with assignee tracking
  - Average response time analytics

- **Statistical Overview Cards**:
  - Clickable stat cards for quick filtering
  - Color-coded priority indicators (red=critical, orange=high, yellow=medium, blue=low)
  - Trend indicators showing comparison metrics
  - Real-time status updates with animated indicators

#### **2. Advanced Filtering & Search System**
- **Multi-dimensional Filtering**:
  - **Status Filtering**: All, Open, Investigating, Resolved, Acknowledged
  - **Priority Filtering**: All, Critical, High, Medium, Low
  - **Type Filtering**: Safety Violation, Equipment Violation, Access Violation, System Alert
  - **Text Search**: Title, message, location, and camera name search

- **Sorting Options**:
  - Latest first (timestamp)
  - Priority-based sorting (critical → low)
  - Status-based grouping
  - Location-based organization

#### **3. Alert List Management**
- **Comprehensive Alert Cards**:
  - Priority indicators with visual icons and color coding
  - Status badges with workflow tracking
  - Location and camera information
  - Timestamp and assigned personnel display
  - Response time tracking for resolved alerts
  - Evidence attachment counts with preview access

- **Bulk Operations**:
  - Multi-select functionality with checkboxes
  - Bulk status updates (investigate, resolve, archive)
  - Bulk assignment to personnel
  - Select all/clear selection controls
  - Bulk actions toolbar with confirmation

#### **4. Alert Detail Management**
- **Comprehensive Alert Information**:
  - Complete alert metadata (ID, type, location, camera, timestamp)
  - Current assignment and response time tracking
  - Priority and status with visual indicators
  - Evidence gallery with preview and download options
  - Response timeline with status change history

- **Quick Action Controls**:
  - Investigate button with status update
  - Resolve button with completion tracking
  - View camera button for live feed access
  - Add comment functionality for collaboration
  - Direct navigation to related screens

#### **5. Evidence Management System**
- **Evidence Viewer Modal**:
  - Image evidence preview with full-screen capability
  - Video evidence playback with controls
  - Download functionality for compliance documentation
  - Evidence metadata and timestamp information
  - Integration with AI detection snapshots

- **Evidence Organization**:
  - Automatic evidence attachment from AI detections
  - Manual evidence upload capability
  - Evidence categorization by type (screenshot, video, manual)
  - Evidence audit trail with timestamp tracking

#### **6. Collaboration & Communication**
- **Comment System**:
  - Comment threads for each alert
  - User attribution with avatar and timestamp
  - Real-time comment updates
  - Comment history preservation
  - Mention functionality for team coordination

- **Assignment Management**:
  - Personnel assignment with role-based access
  - Assignment history tracking
  - Notification system for assigned personnel
  - Workload distribution analytics

#### **7. Real-time Updates & Notifications**
- **Live Alert Feed**:
  - Automatic new alert generation simulation
  - Real-time status change updates
  - Live statistics refresh
  - Push notifications for critical alerts
  - WebSocket-based real-time data synchronization

### **Interactive Elements**
- **Alert Card Interactions**: Click to view details, hover for preview
- **Bulk Selection**: Multi-select with checkboxes and keyboard shortcuts
- **Modal Windows**: Detail view, evidence viewer, comment system, assignment
- **Export Functionality**: JSON export for compliance and reporting
- **Real-time Refresh**: Manual and automatic data refresh controls

---

## 🗃️ **Database Requirements**

### **📚 Database Schema Reference**
👉 **See Master Database Schema**: [MASTER_DATABASE_SCHEMA.md](./MASTER_DATABASE_SCHEMA.md)

### **Required Tables for Alert Center**

#### **Core Tables Used:**
1. **`alerts`** - Primary alert data with workflow management
2. **`users`** - Personnel assignment and comment attribution
3. **`cameras`** - Camera information for alert source context
4. **`sites`** - Site context and location information
5. **`zones`** - Zone-specific alert categorization
6. **`ai_detections`** - AI detection data linked to alerts
7. **`alert_comments`** - Comment system for collaboration (new table needed)
8. **`alert_evidence`** - Evidence management system (new table needed)
9. **`alert_assignments`** - Assignment history and tracking (new table needed)

#### **Alert Center-Specific Data Requirements**

##### **Alert Management with Workflow:**
```sql
-- Enhanced alert query with full workflow data
SELECT 
    a.id, a.title, a.description, a.priority, a.status,
    a.alert_type, a.timestamp, a.confidence_score,
    a.severity_score, a.estimated_risk_level,
    
    -- Source information
    a.site_id, s.name as site_name,
    a.camera_id, c.name as camera_name,
    a.zone_id, z.name as zone_name, z.safety_level,
    
    -- Assignment and workflow
    a.acknowledged_by, a.acknowledged_at,
    a.investigating_by, a.investigating_started_at,
    a.resolved_by, a.resolved_at,
    a.resolution_type, a.resolution_notes,
    
    -- Response time calculation
    CASE 
        WHEN a.resolved_at IS NOT NULL THEN
            TIMESTAMPDIFF(MINUTE, a.timestamp, a.resolved_at)
        WHEN a.acknowledged_at IS NOT NULL THEN
            TIMESTAMPDIFF(MINUTE, a.timestamp, a.acknowledged_at)
        ELSE NULL
    END as response_time_minutes,
    
    -- Evidence counts
    COUNT(ae.id) as evidence_count,
    
    -- Comment counts
    COUNT(ac.id) as comment_count,
    
    -- Personnel information
    u1.display_name as acknowledged_by_name,
    u2.display_name as investigating_by_name,
    u3.display_name as resolved_by_name,
    
    -- AI detection correlation
    ad.person_count, ad.ppe_compliance_data,
    ad.safety_violations, ad.snapshot_image_url

FROM alerts a
LEFT JOIN sites s ON a.site_id = s.id
LEFT JOIN cameras c ON a.camera_id = c.id
LEFT JOIN zones z ON a.zone_id = z.id
LEFT JOIN users u1 ON a.acknowledged_by = u1.id
LEFT JOIN users u2 ON a.investigating_by = u2.id
LEFT JOIN users u3 ON a.resolved_by = u3.id
LEFT JOIN ai_detections ad ON a.detection_id = ad.id
LEFT JOIN alert_evidence ae ON a.id = ae.alert_id
LEFT JOIN alert_comments ac ON a.id = ac.alert_id
WHERE a.site_id = ?
GROUP BY a.id
ORDER BY 
    CASE a.priority 
        WHEN 'critical' THEN 1 
        WHEN 'high' THEN 2 
        WHEN 'medium' THEN 3 
        WHEN 'low' THEN 4 
    END, 
    a.timestamp DESC;
```

##### **Alert Statistics and Analytics:**
```sql
-- Alert statistics for dashboard
SELECT 
    -- Overall counts
    COUNT(*) as total_alerts,
    COUNT(CASE WHEN priority = 'critical' THEN 1 END) as critical_alerts,
    COUNT(CASE WHEN priority = 'high' THEN 1 END) as high_alerts,
    COUNT(CASE WHEN priority = 'medium' THEN 1 END) as medium_alerts,
    COUNT(CASE WHEN priority = 'low' THEN 1 END) as low_alerts,
    
    -- Status counts
    COUNT(CASE WHEN status = 'open' THEN 1 END) as open_alerts,
    COUNT(CASE WHEN status = 'investigating' THEN 1 END) as investigating_alerts,
    COUNT(CASE WHEN status = 'acknowledged' THEN 1 END) as acknowledged_alerts,
    COUNT(CASE WHEN status = 'resolved' THEN 1 END) as resolved_alerts,
    
    -- Response time analytics
    AVG(CASE 
        WHEN resolved_at IS NOT NULL THEN 
            TIMESTAMPDIFF(MINUTE, timestamp, resolved_at)
    END) as avg_resolution_time_minutes,
    
    AVG(CASE 
        WHEN acknowledged_at IS NOT NULL THEN 
            TIMESTAMPDIFF(MINUTE, timestamp, acknowledged_at)
    END) as avg_acknowledgment_time_minutes,
    
    -- Recent activity
    COUNT(CASE 
        WHEN timestamp >= DATE_SUB(NOW(), INTERVAL 1 HOUR) THEN 1 
    END) as alerts_last_hour,
    
    COUNT(CASE 
        WHEN timestamp >= DATE_SUB(NOW(), INTERVAL 24 HOUR) THEN 1 
    END) as alerts_last_24h,
    
    -- Performance metrics
    COUNT(CASE 
        WHEN status = 'resolved' 
        AND TIMESTAMPDIFF(MINUTE, timestamp, resolved_at) <= 30 
        THEN 1 
    END) as resolved_within_30_min,
    
    -- Alert types breakdown
    COUNT(CASE WHEN alert_type = 'safety_violation' THEN 1 END) as safety_violations,
    COUNT(CASE WHEN alert_type = 'equipment_violation' THEN 1 END) as equipment_violations,
    COUNT(CASE WHEN alert_type = 'access_violation' THEN 1 END) as access_violations,
    COUNT(CASE WHEN alert_type = 'system_alert' THEN 1 END) as system_alerts

FROM alerts 
WHERE site_id = ?
    AND timestamp >= DATE_SUB(NOW(), INTERVAL 30 DAY);
```

##### **Alert Assignment and Personnel Workload:**
```sql
-- Personnel workload and assignment analytics
SELECT 
    u.id as user_id,
    u.display_name, u.role,
    
    -- Current assignments
    COUNT(CASE 
        WHEN a.status IN ('investigating', 'acknowledged') 
        AND a.investigating_by = u.id 
        THEN 1 
    END) as active_assignments,
    
    -- Assignment history
    COUNT(CASE 
        WHEN a.investigating_by = u.id 
        AND a.investigating_started_at >= DATE_SUB(NOW(), INTERVAL 7 DAY)
        THEN 1 
    END) as assignments_last_week,
    
    -- Performance metrics
    COUNT(CASE 
        WHEN a.resolved_by = u.id 
        AND a.resolved_at >= DATE_SUB(NOW(), INTERVAL 30 DAY)
        THEN 1 
    END) as resolved_last_month,
    
    AVG(CASE 
        WHEN a.resolved_by = u.id 
        AND a.resolved_at IS NOT NULL
        THEN TIMESTAMPDIFF(MINUTE, a.investigating_started_at, a.resolved_at)
    END) as avg_resolution_time_minutes,
    
    -- Alert priority distribution
    COUNT(CASE 
        WHEN a.investigating_by = u.id 
        AND a.priority = 'critical' 
        THEN 1 
    END) as critical_assignments,
    
    -- Availability status
    CASE 
        WHEN COUNT(CASE WHEN a.status IN ('investigating', 'acknowledged') AND a.investigating_by = u.id THEN 1 END) >= 5 
        THEN 'overloaded'
        WHEN COUNT(CASE WHEN a.status IN ('investigating', 'acknowledged') AND a.investigating_by = u.id THEN 1 END) >= 3 
        THEN 'busy'
        ELSE 'available'
    END as availability_status

FROM users u
LEFT JOIN alerts a ON (a.investigating_by = u.id OR a.acknowledged_by = u.id OR a.resolved_by = u.id)
WHERE u.status = 'active' 
    AND u.role IN ('site_manager', 'supervisor', 'safety_officer', 'security')
GROUP BY u.id
ORDER BY active_assignments DESC, u.display_name;
```

#### **Critical Database Relationships for Alert Center:**
- **Alerts ← Users**: Multi-level assignment (acknowledged_by, investigating_by, resolved_by)
- **Alerts → AI_Detections**: Alert source correlation with AI detection data
- **Alerts ← Cameras**: Alert source identification and live camera access
- **Alerts ← Sites**: Site context and location information
- **Alerts ← Zones**: Zone-specific alert categorization and safety requirements

---

## 📹 **ZoneMinder Integration**

### **Alert-Triggered Evidence Capture**

#### **1. Automatic Evidence Generation from ZoneMinder**
```sql
-- Correlation between alerts and ZoneMinder events
SELECT 
    a.id as alert_id,
    a.timestamp as alert_time,
    a.camera_id,
    
    -- ZoneMinder event correlation
    e.Id as zm_event_id,
    e.StartTime, e.EndTime, e.Length,
    e.Frames, e.AlarmFrames, e.Score,
    e.Notes,
    
    -- Evidence file paths
    CONCAT('/zm/events/', DATE(e.StartTime), '/', e.MonitorId, '/', e.Id, '/') as event_path,
    CONCAT('/zm/events/', DATE(e.StartTime), '/', e.MonitorId, '/', e.Id, '/snapshot.jpg') as snapshot_url,
    
    -- Alert correlation strength
    ABS(TIMESTAMPDIFF(SECOND, a.timestamp, e.StartTime)) as time_diff_seconds,
    CASE 
        WHEN ABS(TIMESTAMPDIFF(SECOND, a.timestamp, e.StartTime)) <= 30 THEN 'direct'
        WHEN ABS(TIMESTAMPDIFF(SECOND, a.timestamp, e.StartTime)) <= 120 THEN 'related'
        ELSE 'distant'
    END as correlation_strength

FROM alerts a
LEFT JOIN site_cameras sc ON a.camera_id = sc.camera_id
LEFT JOIN Events e ON sc.zoneminder_monitor_id = e.MonitorId
    AND e.StartTime BETWEEN DATE_SUB(a.timestamp, INTERVAL 2 MINUTE) 
                        AND DATE_ADD(a.timestamp, INTERVAL 2 MINUTE)
WHERE a.site_id = ?
    AND a.timestamp >= DATE_SUB(NOW(), INTERVAL 24 HOUR)
ORDER BY a.timestamp DESC, time_diff_seconds ASC;
```

#### **2. Evidence File Management with ZoneMinder**
```javascript
class AlertEvidenceManager {
    constructor(zmBaseUrl, authToken) {
        this.zmBaseUrl = zmBaseUrl;
        this.authToken = authToken;
    }
    
    async generateEvidenceForAlert(alertId, alertData) {
        try {
            const camera = await this.getCameraForAlert(alertData.camera_id);
            if (!camera || !camera.zoneminder_monitor_id) {
                throw new Error('Camera not found or not integrated with ZoneMinder');
            }
            
            // Find related ZoneMinder events
            const relatedEvents = await this.findEventsNearAlert(
                camera.zoneminder_monitor_id,
                alertData.timestamp
            );
            
            const evidenceFiles = [];
            
            // Generate snapshot from live stream
            const snapshotUrl = await this.captureAlertSnapshot(camera.zoneminder_monitor_id);
            if (snapshotUrl) {
                evidenceFiles.push({
                    type: 'snapshot',
                    url: snapshotUrl,
                    timestamp: alertData.timestamp,
                    source: 'live_capture'
                });
            }
            
            // Include related event recordings
            for (const event of relatedEvents) {
                const eventEvidence = await this.processZMEventForAlert(event);
                evidenceFiles.push(...eventEvidence);
            }
            
            // Store evidence records in database
            for (const evidence of evidenceFiles) {
                await this.storeAlertEvidence(alertId, evidence);
            }
            
            return evidenceFiles;
            
        } catch (error) {
            console.error(`Evidence generation failed for alert ${alertId}:`, error);
            return [];
        }
    }
    
    async captureAlertSnapshot(monitorId) {
        try {
            const snapshotUrl = `${this.zmBaseUrl}/zm/cgi-bin/zms?mode=single&monitor=${monitorId}&scale=100&timestamp=${Date.now()}`;
            
            const response = await fetch(snapshotUrl, {
                headers: { 'Authorization': `Bearer ${this.authToken}` }
            });
            
            if (response.ok) {
                // Store snapshot file
                const snapshotBuffer = await response.arrayBuffer();
                const fileName = `alert_snapshot_${Date.now()}.jpg`;
                const filePath = await this.storeEvidenceFile(fileName, snapshotBuffer);
                
                return {
                    url: `/api/evidence/${fileName}`,
                    file_path: filePath,
                    file_size: snapshotBuffer.byteLength
                };
            }
            
            return null;
            
        } catch (error) {
            console.error(`Snapshot capture failed for monitor ${monitorId}:`, error);
            return null;
        }
    }
    
    async findEventsNearAlert(monitorId, alertTimestamp) {
        try {
            const startTime = new Date(alertTimestamp);
            startTime.setMinutes(startTime.getMinutes() - 2);
            
            const endTime = new Date(alertTimestamp);
            endTime.setMinutes(endTime.getMinutes() + 2);
            
            const eventsUrl = `${this.zmBaseUrl}/zm/api/events.json?MonitorId=${monitorId}&StartTime>=${startTime.toISOString()}&EndTime<=${endTime.toISOString()}`;
            
            const response = await fetch(eventsUrl, {
                headers: { 'Authorization': `Bearer ${this.authToken}` }
            });
            
            if (response.ok) {
                const eventsData = await response.json();
                return eventsData.events || [];
            }
            
            return [];
            
        } catch (error) {
            console.error(`Event search failed:`, error);
            return [];
        }
    }
}
```

---

## 🤖 **AI/YOLO Integration (Roboflow)**

### **Alert Generation from AI Detections**

#### **1. AI Detection to Alert Conversion**
```python
class AlertGenerationService:
    def __init__(self, db_connection, notification_service):
        self.db = db_connection
        self.notifications = notification_service
        
    async def process_ai_detection_for_alerts(self, detection_data):
        """Convert AI detection results into actionable alerts"""
        try:
            # Analyze detection for alert-worthy conditions
            alert_triggers = self.analyze_detection_for_alerts(detection_data)
            
            if not alert_triggers:
                return []
            
            generated_alerts = []
            
            for trigger in alert_triggers:
                # Create alert from trigger
                alert_data = await self.create_alert_from_trigger(detection_data, trigger)
                
                # Determine alert priority and urgency
                alert_data = self.calculate_alert_priority(alert_data, detection_data)
                
                # Generate evidence automatically
                alert_data["evidence"] = await self.generate_detection_evidence(detection_data)
                
                # Store alert in database
                alert_id = await self.store_alert(alert_data)
                alert_data["id"] = alert_id
                
                # Generate real-time notifications
                await self.send_alert_notifications(alert_data)
                
                generated_alerts.append(alert_data)
                
            return generated_alerts
            
        except Exception as e:
            logger.error(f"Alert generation failed: {str(e)}")
            return []
    
    def analyze_detection_for_alerts(self, detection_data):
        """Analyze detection data for alert triggers"""
        alert_triggers = []
        
        # PPE Violation Analysis
        if detection_data.get("overall_ppe_compliance", 100) < 75:
            severity = self.calculate_ppe_violation_severity(detection_data["ppe_compliance_data"])
            alert_triggers.append({
                "type": "safety_violation",
                "subtype": "ppe_violation",
                "severity": severity,
                "description": self.generate_ppe_violation_description(detection_data["ppe_compliance_data"]),
                "affected_personnel": detection_data["person_count"],
                "confidence": detection_data["confidence_score"]
            })
        
        # Unauthorized Access
        restricted_zones = detection_data.get("zone_violations", [])
        if restricted_zones:
            alert_triggers.append({
                "type": "access_violation", 
                "subtype": "unauthorized_zone_access",
                "severity": "high" if any(z.get("safety_level") == "critical" for z in restricted_zones) else "medium",
                "description": f"Personnel detected in {len(restricted_zones)} restricted zone(s)",
                "affected_zones": [z["zone_name"] for z in restricted_zones],
                "confidence": detection_data["confidence_score"]
            })
        
        # Equipment Safety Violations
        equipment_violations = detection_data.get("equipment_safety_violations", [])
        if equipment_violations:
            alert_triggers.append({
                "type": "equipment_violation",
                "subtype": "unsafe_equipment_operation",
                "severity": "high",
                "description": f"Unsafe equipment operation detected: {', '.join([v['type'] for v in equipment_violations])}",
                "equipment_involved": [v['equipment_type'] for v in equipment_violations],
                "confidence": detection_data["confidence_score"]
            })
        
        # High-Risk Activity Detection
        if detection_data.get("risk_assessment") in ["high", "critical"]:
            alert_triggers.append({
                "type": "safety_violation",
                "subtype": "high_risk_activity",
                "severity": "critical" if detection_data.get("risk_assessment") == "critical" else "high",
                "description": f"High-risk activity detected with {detection_data['person_count']} personnel involved",
                "risk_factors": detection_data.get("risk_factors", []),
                "confidence": detection_data["confidence_score"]
            })
        
        return alert_triggers
    
    async def create_alert_from_trigger(self, detection_data, trigger):
        """Create alert record from trigger data"""
        return {
            "site_id": detection_data["site_id"],
            "camera_id": detection_data["camera_id"],
            "zone_id": detection_data.get("zone_id"),
            "detection_id": detection_data["detection_id"],
            
            "alert_type": trigger["type"],
            "title": self.generate_alert_title(trigger),
            "description": trigger["description"],
            
            "priority": self.map_severity_to_priority(trigger["severity"]),
            "status": "open",
            "estimated_risk_level": trigger["severity"],
            
            "confidence_score": trigger["confidence"],
            "ai_model_used": detection_data.get("model_version"),
            
            "timestamp": detection_data["timestamp"],
            "detection_data": detection_data,
            
            "requires_immediate_action": trigger["severity"] in ["critical", "high"],
            "affected_personnel_count": detection_data.get("person_count", 0),
            
            # Evidence URLs from AI detection
            "primary_image_url": detection_data.get("snapshot_image_url"),
            "annotated_evidence_url": detection_data.get("annotated_image_url"),
            
            # Recommended actions based on trigger type
            "recommended_actions": self.generate_recommended_actions(trigger, detection_data)
        }
```

#### **2. AI Detection Evidence Processing**
```json
{
  "alert_from_ai_detection": {
    "alert_id": "alert_123456789",
    "detection_correlation": {
      "detection_id": "det_987654321", 
      "camera_id": "cam_001",
      "camera_name": "Main Entrance Gate",
      "zone_name": "Entry Control Zone",
      "timestamp": "2025-01-12T14:30:15Z"
    },
    
    "violation_analysis": {
      "type": "safety_violation",
      "subtype": "ppe_violation",
      "severity": "high",
      "confidence": 94.2,
      "affected_personnel": 2,
      
      "ppe_analysis": [
        {
          "person_id": 1,
          "compliance_score": 45.2,
          "missing_items": ["hardhat", "safety_vest"],
          "present_items": ["boots"],
          "violation_severity": "critical"
        },
        {
          "person_id": 2,
          "compliance_score": 78.5,
          "missing_items": ["safety_vest"],
          "present_items": ["hardhat", "boots"],
          "violation_severity": "medium"
        }
      ]
    },
    
    "evidence_package": {
      "primary_evidence": {
        "type": "annotated_image",
        "url": "/api/evidence/alert_123456789_primary.jpg",
        "annotations": [
          {
            "type": "person_bbox",
            "coordinates": [320, 150, 450, 600],
            "person_id": 1,
            "violation_overlay": true,
            "missing_ppe_highlighted": ["hardhat", "safety_vest"]
          }
        ]
      },
      
      "supporting_evidence": [
        {
          "type": "raw_detection_image",
          "url": "/api/evidence/alert_123456789_raw.jpg",
          "timestamp": "2025-01-12T14:30:15Z"
        },
        {
          "type": "detection_data",
          "url": "/api/evidence/alert_123456789_data.json",
          "content": "complete AI detection results"
        }
      ],
      
      "related_evidence": [
        {
          "type": "previous_detection",
          "url": "/api/evidence/related_det_123.jpg",
          "timestamp": "2025-01-12T14:25:00Z",
          "relation": "same_person_track"
        }
      ]
    },
    
    "recommended_response": {
      "immediate_actions": [
        "Stop work in affected area",
        "Dispatch safety supervisor to Entry Control Zone",
        "Provide required PPE to personnel",
        "Document incident for compliance reporting"
      ],
      "follow_up_actions": [
        "Review PPE training records for affected personnel",
        "Increase PPE compliance monitoring in zone",
        "Schedule safety refresher training"
      ],
      "estimated_response_time": "5 minutes",
      "escalation_required": true
    }
  }
}
```

---

## 🔗 **Backend API Requirements**

### **Required Endpoints**

#### **1. Alert Management API**
```http
GET /api/alerts?site_id={site_id}&status={status}&priority={priority}&type={type}&search={search}&sort={sort}&page={page}&limit={limit}

Response:
{
  "alerts": [
    {
      "id": "alert_001",
      "title": "PPE Violation - Missing Hard Hat",
      "description": "Worker detected without required safety helmet in Zone A",
      "type": "safety_violation",
      "priority": "critical",
      "status": "open",
      "timestamp": "2025-01-12T14:25:00Z",
      
      "location": {
        "site_id": "site_001",
        "site_name": "Downtown Plaza Project", 
        "camera_id": "cam_001",
        "camera_name": "Loading Zone Alpha",
        "zone_id": "zone_001",
        "zone_name": "Loading Area Zone A"
      },
      
      "assignment": {
        "acknowledged_by": null,
        "acknowledged_at": null,
        "investigating_by": null,
        "investigating_started_at": null,
        "resolved_by": null,
        "resolved_at": null
      },
      
      "metrics": {
        "confidence_score": 96.8,
        "severity_score": 9.2,
        "estimated_risk_level": "critical",
        "response_time_minutes": null,
        "affected_personnel_count": 1
      },
      
      "evidence": {
        "count": 2,
        "primary_image": "/api/evidence/alert_001_primary.jpg",
        "annotated_image": "/api/evidence/alert_001_annotated.jpg",
        "additional": [
          {
            "type": "video",
            "url": "/api/evidence/alert_001_video.mp4",
            "duration_seconds": 30
          }
        ]
      },
      
      "workflow": {
        "can_acknowledge": true,
        "can_investigate": true,
        "can_resolve": false,
        "requires_escalation": true,
        "auto_resolve_available": false
      },
      
      "comments_count": 2,
      "last_activity": "2025-01-12T14:28:00Z"
    }
  ],
  
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 45,
    "total_pages": 3,
    "has_next": true,
    "has_previous": false
  },
  
  "statistics": {
    "total": 45,
    "critical": 3,
    "high": 12,
    "medium": 18,
    "low": 12,
    "open": 15,
    "investigating": 8,
    "resolved": 22,
    "avg_response_time_minutes": 18.5
  }
}
```

#### **2. Alert Detail API**
```http
GET /api/alerts/{alert_id}?include=evidence,comments,timeline,related

Response:
{
  "alert": {
    "id": "alert_001",
    "title": "PPE Violation - Missing Hard Hat",
    "description": "Worker detected without required safety helmet in high-risk construction zone",
    "type": "safety_violation",
    "priority": "critical",
    "status": "open",
    "timestamp": "2025-01-12T14:25:00Z",
    
    "ai_detection": {
      "detection_id": "det_789456123",
      "confidence": 96.8,
      "person_count": 1,
      "ppe_violations": ["missing_hardhat"],
      "risk_assessment": "critical",
      "model_version": "ppe-detection-v4.2"
    },
    
    "location_context": {
      "site_name": "Downtown Plaza Project",
      "camera_name": "Zone 3 Safety Camera", 
      "zone_name": "High Risk Construction Area",
      "zone_safety_level": "critical",
      "required_ppe": ["hardhat", "safety_vest", "boots", "safety_harness"]
    },
    
    "workflow_history": [
      {
        "action": "alert_created",
        "timestamp": "2025-01-12T14:25:00Z",
        "user": "System (AI Detection)",
        "details": "Alert automatically generated from AI detection"
      }
    ],
    
    "evidence": [
      {
        "id": "evidence_001",
        "type": "annotated_image",
        "url": "/api/evidence/alert_001_annotated.jpg",
        "thumbnail_url": "/api/evidence/alert_001_annotated_thumb.jpg",
        "timestamp": "2025-01-12T14:25:00Z",
        "file_size_kb": 245,
        "annotations": {
          "violation_areas": [
            {
              "type": "missing_hardhat",
              "bbox": [320, 150, 450, 280],
              "confidence": 96.8
            }
          ]
        }
      },
      {
        "id": "evidence_002", 
        "type": "raw_image",
        "url": "/api/evidence/alert_001_raw.jpg",
        "timestamp": "2025-01-12T14:25:00Z",
        "file_size_kb": 180
      }
    ],
    
    "comments": [
      {
        "id": "comment_001",
        "author": {
          "id": "user_001",
          "name": "James Wilson",
          "avatar": "/api/avatars/user_001.jpg"
        },
        "text": "Supervisor dispatched to location immediately",
        "timestamp": "2025-01-12T14:28:00Z",
        "edited": false
      }
    ],
    
    "recommended_actions": [
      "Stop work in affected zone immediately",
      "Dispatch safety supervisor to High Risk Construction Area", 
      "Provide required safety helmet to worker",
      "Document violation for compliance reporting",
      "Review worker safety training records"
    ],
    
    "related_alerts": [
      {
        "id": "alert_045",
        "title": "PPE Violation - Same Zone",
        "timestamp": "2025-01-12T11:15:00Z",
        "status": "resolved",
        "relation": "same_zone_similar_violation"
      }
    ]
  }
}
```

#### **3. Alert Actions API**
```http
POST /api/alerts/{alert_id}/actions

Request:
{
  "action": "investigate",
  "user_id": "user_001",
  "notes": "Dispatching safety supervisor to location",
  "estimated_resolution_time_minutes": 15
}

Response:
{
  "success": true,
  "alert_id": "alert_001",
  "action_taken": "investigate",
  "status_updated_to": "investigating",
  "timestamp": "2025-01-12T14:30:00Z",
  "assigned_to": {
    "id": "user_001",
    "name": "James Wilson",
    "role": "Site Manager"
  },
  "workflow_updated": true
}

POST /api/alerts/{alert_id}/resolve

Request:
{
  "resolution_type": "corrective_action_taken",
  "resolution_notes": "Worker provided with safety helmet and reminded of PPE requirements. Work resumed after verification of compliance.",
  "evidence_urls": ["/api/evidence/resolution_photo_001.jpg"],
  "follow_up_required": true,
  "follow_up_actions": ["Schedule PPE refresher training", "Increase zone monitoring"]
}

Response:
{
  "success": true,
  "alert_id": "alert_001", 
  "status_updated_to": "resolved",
  "resolution_time_minutes": 12,
  "resolved_at": "2025-01-12T14:37:00Z",
  "performance_metrics": {
    "response_time_minutes": 12,
    "within_target": true,
    "target_time_minutes": 15
  }
}
```

#### **4. Bulk Operations API**
```http
POST /api/alerts/bulk-actions

Request:
{
  "action": "assign",
  "alert_ids": ["alert_001", "alert_002", "alert_003"],
  "assign_to": "user_002",
  "bulk_notes": "Assigning all high priority PPE violations to senior safety officer"
}

Response:
{
  "success": true,
  "processed_alerts": 3,
  "results": [
    {
      "alert_id": "alert_001",
      "success": true,
      "status": "investigating",
      "assigned_to": "user_002"
    },
    {
      "alert_id": "alert_002", 
      "success": true,
      "status": "investigating",
      "assigned_to": "user_002"
    },
    {
      "alert_id": "alert_003",
      "success": true,
      "status": "investigating", 
      "assigned_to": "user_002"
    }
  ],
  "notifications_sent": 4,
  "bulk_action_id": "bulk_action_123"
}
```

#### **5. Comment System API**
```http
GET /api/alerts/{alert_id}/comments

Response:
{
  "comments": [
    {
      "id": "comment_001",
      "author": {
        "id": "user_001",
        "name": "James Wilson",
        "avatar": "/api/avatars/user_001.jpg",
        "role": "Site Manager"
      },
      "text": "Supervisor dispatched to location immediately. ETA 5 minutes.",
      "timestamp": "2025-01-12T14:28:00Z",
      "edited": false,
      "mentions": [],
      "attachments": []
    }
  ],
  "total_comments": 3,
  "can_add_comment": true
}

POST /api/alerts/{alert_id}/comments

Request:
{
  "text": "PPE provided to worker. Work can resume with proper safety equipment.",
  "mentions": ["@user_002"],
  "attachments": ["/api/uploads/ppe_compliance_photo.jpg"]
}

Response:
{
  "success": true,
  "comment": {
    "id": "comment_002",
    "author": {
      "id": "user_001",
      "name": "James Wilson",
      "avatar": "/api/avatars/user_001.jpg"
    },
    "text": "PPE provided to worker. Work can resume with proper safety equipment.",
    "timestamp": "2025-01-12T14:32:00Z",
    "edited": false,
    "mentions": ["user_002"],
    "attachments": ["/api/uploads/ppe_compliance_photo.jpg"]
  },
  "notifications_sent": 1
}
```

#### **6. Export and Reporting API**
```http
GET /api/alerts/export?format=csv&filters={filters}&date_range={range}

Response:
{
  "export_id": "export_123456789",
  "format": "csv",
  "status": "processing",
  "estimated_completion": "2025-01-12T14:35:00Z",
  "download_url": null,
  "records_count": 1247
}

GET /api/alerts/export/{export_id}/download

Response: (CSV File)
Alert ID,Title,Type,Priority,Status,Location,Camera,Timestamp,Assigned To,Response Time,Resolution
alert_001,PPE Violation - Missing Hard Hat,safety_violation,critical,resolved,Zone A,Loading Zone Alpha,2025-01-12T14:25:00Z,James Wilson,12,corrective_action_taken
...
```

---

## ⚠️ **Identified Defects & Missing Features**

### **Database Gaps**
1. **Alert Comments Table**: Missing dedicated table for comment system with threading
2. **Alert Evidence Table**: No structured evidence management with metadata
3. **Alert Assignments Table**: Missing assignment history tracking and workload analytics
4. **Alert Templates**: No predefined alert templates for common violations
5. **Escalation Rules**: Missing automatic escalation based on time and priority

### **Workflow Management Gaps**
1. **SLA Tracking**: No service level agreement tracking for response times
2. **Automatic Assignment**: Missing intelligent assignment based on workload and expertise
3. **Escalation Automation**: No automatic escalation for overdue alerts
4. **Approval Workflows**: Missing approval requirements for certain resolution types

### **Integration Gaps**
1. **Real-time Notifications**: Limited push notification system for mobile devices
2. **External System Integration**: No integration with OSHA reporting or compliance systems
3. **Calendar Integration**: Missing calendar integration for scheduled inspections and follow-ups
4. **Mobile App Support**: Limited mobile-optimized alert management capabilities

---

## 🔧 **COMPLETE FIXED ALERT CENTER INTEGRATION**

### **1. ✅ FIXED: Alert Comments System**

#### **New alert_comments Table**
```sql
CREATE TABLE alert_comments (
    id UUID PRIMARY KEY,
    alert_id UUID NOT NULL,
    author_id UUID NOT NULL,
    
    -- Comment content
    comment_text TEXT NOT NULL,
    comment_type ENUM('note', 'status_update', 'evidence', 'resolution', 'escalation') DEFAULT 'note',
    
    -- Threading support
    parent_comment_id UUID NULL, -- For reply threading
    thread_level INT DEFAULT 0,
    
    -- Mentions and notifications
    mentioned_users JSON, -- Array of user IDs mentioned
    notifications_sent JSON, -- Notification delivery tracking
    
    -- Attachments
    attachment_urls JSON, -- Array of attachment URLs
    attachment_metadata JSON, -- File names, sizes, types
    
    -- Status and visibility
    is_internal BOOLEAN DEFAULT FALSE, -- Internal vs external comments
    is_edited BOOLEAN DEFAULT FALSE,
    edit_history JSON, -- Edit tracking
    visibility_level ENUM('public', 'team', 'management', 'admin') DEFAULT 'team',
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (alert_id) REFERENCES alerts(id) ON DELETE CASCADE,
    FOREIGN KEY (author_id) REFERENCES users(id),
    FOREIGN KEY (parent_comment_id) REFERENCES alert_comments(id),
    
    INDEX idx_alert_comments_alert (alert_id, created_at DESC),
    INDEX idx_alert_comments_author (author_id),
    INDEX idx_alert_comments_thread (parent_comment_id, thread_level),
    INDEX idx_alert_comments_mentions (mentioned_users),
    FULLTEXT INDEX idx_alert_comments_search (comment_text)
);
```

#### **Enhanced Alert Evidence Management**
```sql
CREATE TABLE alert_evidence (
    id UUID PRIMARY KEY,
    alert_id UUID NOT NULL,
    
    -- Evidence source
    source_type ENUM('ai_detection', 'manual_upload', 'zoneminder_event', 'camera_snapshot', 'document') NOT NULL,
    source_reference_id VARCHAR(255), -- Reference to source (detection_id, event_id, etc.)
    
    -- File information
    evidence_type ENUM('image', 'video', 'document', 'audio', 'data') NOT NULL,
    file_name VARCHAR(255) NOT NULL,
    original_file_name VARCHAR(255),
    file_path VARCHAR(500) NOT NULL,
    file_size_bytes BIGINT,
    file_format VARCHAR(50), -- jpg, mp4, pdf, json, etc.
    
    -- Content metadata
    duration_seconds INT NULL, -- For videos/audio
    image_width INT NULL,
    image_height INT NULL,
    thumbnail_path VARCHAR(500),
    
    -- Evidence details
    title VARCHAR(255),
    description TEXT,
    evidence_timestamp TIMESTAMP, -- When evidence was captured (vs when added)
    location_metadata JSON, -- Camera position, GPS, etc.
    
    -- AI Analysis metadata
    ai_annotations JSON, -- Bounding boxes, detections, etc.
    analysis_metadata JSON, -- Confidence scores, model versions, etc.
    
    -- Access and workflow
    uploaded_by UUID NOT NULL,
    is_primary_evidence BOOLEAN DEFAULT FALSE,
    evidence_chain_verified BOOLEAN DEFAULT FALSE,
    access_permissions JSON, -- Who can view this evidence
    
    -- Status
    status ENUM('processing', 'available', 'archived', 'deleted') DEFAULT 'available',
    retention_date DATE, -- When evidence expires
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (alert_id) REFERENCES alerts(id) ON DELETE CASCADE,
    FOREIGN KEY (uploaded_by) REFERENCES users(id),
    
    INDEX idx_alert_evidence_alert (alert_id, evidence_timestamp DESC),
    INDEX idx_alert_evidence_type (evidence_type, source_type),
    INDEX idx_alert_evidence_uploader (uploaded_by),
    INDEX idx_alert_evidence_primary (is_primary_evidence),
    INDEX idx_alert_evidence_retention (retention_date)
);
```

### **2. ✅ FIXED: Alert Assignment and Workload Management**
```sql
CREATE TABLE alert_assignments (
    id UUID PRIMARY KEY,
    alert_id UUID NOT NULL,
    
    -- Assignment details
    assigned_to UUID NOT NULL,
    assigned_by UUID NOT NULL,
    assignment_type ENUM('manual', 'automatic', 'escalation', 'reassignment') DEFAULT 'manual',
    
    -- Timing
    assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    accepted_at TIMESTAMP NULL,
    started_work_at TIMESTAMP NULL,
    estimated_completion TIMESTAMP NULL,
    actual_completion TIMESTAMP NULL,
    
    -- Assignment metadata
    assignment_reason TEXT,
    priority_override ENUM('critical', 'high', 'medium', 'low') NULL,
    skill_requirements JSON, -- Required skills/certifications
    assignment_notes TEXT,
    
    -- Status tracking
    status ENUM('assigned', 'accepted', 'in_progress', 'completed', 'reassigned', 'declined') DEFAULT 'assigned',
    completion_percentage INT DEFAULT 0,
    
    -- Performance metrics
    response_time_minutes INT, -- Time to start work
    resolution_time_minutes INT, -- Total time to complete
    quality_score DECIMAL(3,1), -- 1-10 quality rating
    
    -- Workload context
    concurrent_assignments INT, -- How many other active assignments at time of assignment
    workload_score DECIMAL(5,2), -- Calculated workload at assignment time
    
    -- Status changes
    status_changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status_changed_by UUID,
    
    FOREIGN KEY (alert_id) REFERENCES alerts(id) ON DELETE CASCADE,
    FOREIGN KEY (assigned_to) REFERENCES users(id),
    FOREIGN KEY (assigned_by) REFERENCES users(id),
    FOREIGN KEY (status_changed_by) REFERENCES users(id),
    
    INDEX idx_alert_assignments_alert (alert_id, assigned_at DESC),
    INDEX idx_alert_assignments_user (assigned_to, status, assigned_at DESC),
    INDEX idx_alert_assignments_performance (resolution_time_minutes, quality_score),
    INDEX idx_alert_assignments_workload (workload_score, concurrent_assignments)
);
```

### **3. ✅ FIXED: Real-time Alert Management**
```python
class AlertCenterWebSocketManager:
    def __init__(self):
        self.connections = {}  # site_id -> [websocket connections]
        self.user_connections = {}  # user_id -> [websocket connections]
        
    async def handle_alert_center_connection(self, websocket, user_id, site_id):
        """Handle WebSocket connection for real-time alert updates"""
        connection_id = str(uuid.uuid4())
        
        try:
            # Register connection for both site and user updates
            if site_id not in self.connections:
                self.connections[site_id] = {}
            self.connections[site_id][connection_id] = {
                "websocket": websocket,
                "user_id": user_id,
                "connected_at": datetime.utcnow(),
                "filters": {}, # User-specific filters
                "last_activity": datetime.utcnow()
            }
            
            if user_id not in self.user_connections:
                self.user_connections[user_id] = {}
            self.user_connections[user_id][connection_id] = websocket
            
            # Send initial alert state
            initial_data = await self.get_initial_alert_state(site_id, user_id)
            await websocket.send_json({
                "type": "initial_state",
                "data": initial_data
            })
            
            # Handle incoming messages (filter updates, actions)
            async for message in websocket.iter_json():
                await self.handle_alert_center_message(websocket, site_id, user_id, message)
                
        except WebSocketDisconnect:
            # Clean up connections
            if site_id in self.connections and connection_id in self.connections[site_id]:
                del self.connections[site_id][connection_id]
            if user_id in self.user_connections and connection_id in self.user_connections[user_id]:
                del self.user_connections[user_id][connection_id]
    
    async def broadcast_new_alert(self, alert_data):
        """Broadcast new alert to relevant users"""
        site_id = alert_data["site_id"]
        
        if site_id in self.connections:
            disconnected = []
            
            for connection_id, connection_info in self.connections[site_id].items():
                try:
                    # Check if user should receive this alert based on filters/permissions
                    if await self.should_user_receive_alert(connection_info["user_id"], alert_data):
                        await connection_info["websocket"].send_json({
                            "type": "new_alert",
                            "timestamp": datetime.utcnow().isoformat(),
                            "data": {
                                "alert": alert_data,
                                "requires_attention": alert_data["priority"] in ["critical", "high"],
                                "audio_notification": alert_data["priority"] == "critical",
                                "flash_notification": True
                            }
                        })
                except:
                    disconnected.append(connection_id)
            
            # Clean up disconnected
            for conn_id in disconnected:
                del self.connections[site_id][conn_id]
    
    async def broadcast_alert_status_change(self, alert_id, status_change_data):
        """Broadcast alert status changes to relevant users"""
        alert = await self.get_alert_by_id(alert_id)
        if not alert:
            return
            
        site_id = alert["site_id"]
        
        # Notify site connections
        await self.broadcast_to_site(site_id, {
            "type": "alert_status_change",
            "alert_id": alert_id,
            "timestamp": datetime.utcnow().isoformat(),
            "data": status_change_data
        })
        
        # Notify assigned user specifically
        if alert.get("investigating_by"):
            await self.notify_user_directly(alert["investigating_by"], {
                "type": "assignment_update", 
                "alert_id": alert_id,
                "data": status_change_data
            })
    
    async def broadcast_bulk_action_result(self, user_id, bulk_action_data):
        """Notify user about bulk action completion"""
        if user_id in self.user_connections:
            for websocket in self.user_connections[user_id].values():
                try:
                    await websocket.send_json({
                        "type": "bulk_action_complete",
                        "timestamp": datetime.utcnow().isoformat(),
                        "data": bulk_action_data
                    })
                except:
                    pass  # Connection will be cleaned up later
```

---

## 📈 **Success Metrics**

- **Alert Response Time**: Average response time < 15 minutes for high priority alerts
- **Resolution Rate**: 95% of alerts resolved within defined SLA timeframes
- **User Engagement**: Average session time > 8 minutes with active alert management
- **Real-time Performance**: Alert updates delivered within 2 seconds
- **Evidence Access**: 99% evidence availability with < 3 second load times
- **Bulk Operations**: Support for 100+ alerts in single bulk action
- **Mobile Compatibility**: 90% of alert management functions available on mobile

---

**Document Created**: 2025-01-12  
**Next Screen**: Site Overview (/site-overview)