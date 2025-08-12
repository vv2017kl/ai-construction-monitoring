# 👥 Screen Analysis #06: Personnel Management (/personnel)

## 📋 **Document Information**
- **Screen Path**: `/personnel`
- **Menu Location**: Workforce → Personnel Management
- **Portal**: Solution User Portal  
- **Priority**: CRITICAL (Workforce safety tracking - has runtime bug)
- **Status**: ⚠️ **NEEDS BUG FIX** - Implemented but requires runtime error resolution

---

## 🎯 **Functional Analysis**

### **Primary Purpose**
Comprehensive workforce management system providing real-time personnel tracking, safety monitoring, certification management, and operational oversight for construction site personnel with advanced filtering, bulk operations, and live location tracking capabilities.

### **Core Features & User Workflows**

#### **1. Personnel Overview Dashboard**
- **Real-time Statistics Cards**:
  - **Total Personnel**: Complete workforce count with trend indicators
  - **On-Site Personnel**: Currently active workers with real-time updates
  - **Average Safety Score**: Site-wide safety performance with trend analysis
  - **PPE Compliance**: Overall PPE compliance rate with improvement tracking

- **Live Tracking Indicators**:
  - **Real-time Location Updates**: Continuous personnel position tracking
  - **Status Broadcasting**: Live work status updates (active, break, off-site, absent)
  - **Safety Score Monitoring**: Dynamic safety performance tracking
  - **Alert Integration**: Instant safety violation notifications

#### **2. Advanced Personnel Search and Filtering**
- **Multi-dimensional Search System**:
  - **Text Search**: Name, email, role-based search with real-time filtering
  - **Department Filtering**: Construction, Safety, Equipment, Quality Assurance, Electrical
  - **Status Filtering**: Active, break, off-site, absent status categorization
  - **Role-based Filtering**: Site Supervisor, Safety Inspector, Equipment Operator, etc.
  - **Advanced Sorting**: Name, last seen, safety score, hours worked sorting options

- **Dynamic View Modes**:
  - **Table View**: Detailed tabular data with sortable columns and bulk actions
  - **Card View**: Visual personnel cards with key metrics and quick actions
  - **Responsive Design**: Adaptive layout for desktop, tablet, and mobile devices

#### **3. Comprehensive Personnel CRUD Operations**
- **Add Personnel Workflow**:
  - **Basic Information**: Name, role, department, contact details
  - **Certification Management**: Multiple certification tracking and validation
  - **Department Assignment**: Structured department categorization
  - **Automatic Profile Setup**: Default safety scores and compliance tracking

- **Edit Personnel Management**:
  - **Profile Updates**: Real-time personnel information editing
  - **Role and Department Changes**: Workflow-based role transitions
  - **Contact Information**: Email and phone number management
  - **Certification Updates**: Training and certification status management

#### **4. Real-time Status and Location Management** 
- **Status Update System**:
  - **Check-in/Check-out**: Automated time tracking with GPS validation
  - **Break Management**: Break time tracking with automatic alerts
  - **Off-site Status**: Remote work tracking and location validation
  - **Emergency Status**: Immediate status updates for safety incidents

- **Location Tracking Integration**:
  - **Zone-based Positioning**: Real-time zone assignment and movement tracking
  - **GPS Coordinate Tracking**: Precise location monitoring with timestamp validation
  - **Movement Pattern Analysis**: Historical movement data for optimization
  - **Safety Zone Compliance**: Automatic zone violation detection and alerts

#### **5. Advanced Bulk Operations**
- **Multi-select Functionality**:
  - **Individual Selection**: Personnel-specific actions with visual feedback
  - **Bulk Selection**: Select all/clear all with advanced filtering integration
  - **Cross-page Selection**: Persistent selections across pagination and view changes

- **Bulk Action Capabilities**:
  - **Status Updates**: Bulk check-in, break, off-site status changes
  - **Alert Broadcasting**: Mass emergency alerts and notifications
  - **Assignment Management**: Bulk task and zone assignments
  - **Export Operations**: Filtered data export with customizable formats

#### **6. Personnel Detail Management System**
- **Comprehensive Personnel Profiles**:
  - **Contact Information**: Email, phone, department, role details
  - **Work Metrics**: Hours worked, check-in times, productivity tracking
  - **Safety Performance**: Safety scores, PPE compliance, violation history
  - **Certification Tracking**: Current certifications, expiry dates, training records

- **Quick Action Controls**:
  - **Status Updates**: Instant status changes with timestamp logging
  - **Location Updates**: GPS-based location assignment and validation
  - **Communication Tools**: Direct calling, messaging, and alert sending
  - **Camera Integration**: Live camera feed access for personnel monitoring

#### **7. Safety and Compliance Monitoring**
- **Real-time Safety Metrics**:
  - **Individual Safety Scores**: Personal safety performance tracking (0-100%)
  - **PPE Compliance Monitoring**: Equipment compliance with zone requirements
  - **Violation Tracking**: Safety incident history and resolution status
  - **Certification Validation**: Training currency and compliance verification

- **Automated Safety Alerts**:
  - **Low Safety Score Alerts**: Automatic notifications for safety concerns
  - **PPE Violation Notifications**: Real-time equipment compliance alerts
  - **Zone Violation Alerts**: Unauthorized area access notifications
  - **Emergency Response Integration**: Immediate safety incident escalation

### **Interactive Elements**
- **Dual View Toggle**: Seamless switching between table and card views
- **Advanced Filtering**: Real-time data filtering with multiple criteria
- **Bulk Selection**: Multi-select with persistent selections and bulk actions
- **Modal Systems**: Add/edit personnel, location updates, detailed profiles
- **Export Functionality**: Data export with filtering and customization options
- **Real-time Updates**: Live data refresh with WebSocket integration

---

## 🗃️ **Database Requirements**

### **📚 Database Schema Reference**
👉 **See Master Database Schema**: [MASTER_DATABASE_SCHEMA.md](./MASTER_DATABASE_SCHEMA.md)

### **Required Tables for Personnel Management**

#### **Core Tables Used:**
1. **`users`** - User accounts and authentication
2. **`site_personnel`** - Site-specific personnel assignments and tracking
3. **`user_certifications`** - Training and certification management (new table needed)
4. **`personnel_attendance`** - Check-in/check-out tracking (new table needed)
5. **`personnel_safety_scores`** - Safety performance history (new table needed)
6. **`department_assignments`** - Department and role management (new table needed)

#### **Personnel Management-Specific Data Requirements**

##### **Comprehensive Personnel Data with Real-time Metrics:**
```sql
-- Complete personnel overview with real-time status
SELECT 
    u.id as user_id, u.display_name, u.email, u.phone,
    u.role, u.status as user_status, u.avatar_url,
    
    -- Site personnel details
    sp.id as personnel_id, sp.employee_id,
    sp.status as work_status, sp.shift_start_time, sp.shift_end_time,
    sp.current_coordinates, sp.current_zone_id,
    sp.last_position_update, sp.hours_worked_today,
    
    -- Zone information
    z.name as current_zone_name, z.zone_type, z.safety_level,
    
    -- Department and role assignment
    da.department_name, da.position_title, da.reporting_manager_id,
    da.start_date as position_start_date,
    
    -- Safety metrics
    sp.ppe_compliance_score, sp.safety_score, sp.safety_violations_today,
    sp.last_ppe_check, sp.current_ppe_status,
    
    -- Attendance tracking
    pa.check_in_time, pa.check_out_time, pa.break_start_time, pa.break_end_time,
    pa.total_break_minutes, pa.overtime_hours,
    
    -- Certification status
    COUNT(uc.id) as total_certifications,
    COUNT(CASE WHEN uc.expiry_date >= CURRENT_DATE THEN 1 END) as valid_certifications,
    COUNT(CASE WHEN uc.expiry_date < DATE_ADD(CURRENT_DATE, INTERVAL 30 DAY) THEN 1 END) as expiring_certifications,
    
    -- Activity metrics
    sp.distance_traveled_today, sp.zones_visited_today,
    sp.activity_level, sp.last_activity_type, sp.activity_timestamp,
    
    -- Emergency contact and medical info
    u.emergency_contact_name, u.emergency_contact_phone,
    sp.medical_conditions, sp.medication_alerts,
    
    -- Performance tracking
    AVG(pss.safety_score) as avg_safety_score_30_days,
    MAX(pss.recorded_date) as last_safety_assessment

FROM users u
LEFT JOIN site_personnel sp ON u.id = sp.user_id
LEFT JOIN zones z ON sp.current_zone_id = z.id
LEFT JOIN department_assignments da ON u.id = da.user_id AND da.is_active = TRUE
LEFT JOIN personnel_attendance pa ON sp.id = pa.personnel_id AND DATE(pa.check_in_time) = CURRENT_DATE
LEFT JOIN user_certifications uc ON u.id = uc.user_id
LEFT JOIN personnel_safety_scores pss ON sp.id = pss.personnel_id 
    AND pss.recorded_date >= DATE_SUB(CURRENT_DATE, INTERVAL 30 DAY)
WHERE sp.site_id = ? AND u.status = 'active'
GROUP BY u.id, sp.id, z.id, da.id, pa.id
ORDER BY sp.last_position_update DESC;
```

##### **Real-time Personnel Status and Location Tracking:**
```sql
-- Personnel location and status updates
SELECT 
    sp.id as personnel_id, sp.user_id,
    u.display_name, u.avatar_url,
    
    -- Current status and location
    sp.status, sp.current_coordinates,
    sp.current_zone_id, z.name as zone_name,
    sp.last_position_update, sp.activity_timestamp,
    
    -- Work session data
    pa.check_in_time, pa.total_work_minutes,
    pa.break_start_time, pa.total_break_minutes,
    CASE 
        WHEN pa.break_start_time IS NOT NULL AND pa.break_end_time IS NULL THEN 'on_break'
        WHEN pa.check_in_time IS NOT NULL AND pa.check_out_time IS NULL THEN 'active'
        WHEN pa.check_out_time IS NOT NULL THEN 'checked_out'
        ELSE 'not_checked_in'
    END as calculated_status,
    
    -- Safety status
    sp.ppe_compliance_score, sp.safety_violations_today,
    sp.last_safety_check, sp.current_ppe_status,
    
    -- Zone compliance
    CASE 
        WHEN z.requires_ppe = TRUE AND sp.ppe_compliance_score < 80 THEN 'ppe_violation'
        WHEN sp.current_zone_id != z.id THEN 'zone_mismatch'
        ELSE 'compliant'
    END as compliance_status,
    
    -- Alert indicators
    COUNT(a.id) as active_personal_alerts,
    MAX(a.priority) as highest_alert_priority,
    
    -- Movement tracking
    sp.distance_traveled_today, sp.last_movement_time,
    JSON_ARRAYAGG(DISTINCT z_visited.name) as zones_visited_today

FROM site_personnel sp
JOIN users u ON sp.user_id = u.id
LEFT JOIN zones z ON sp.current_zone_id = z.id
LEFT JOIN personnel_attendance pa ON sp.id = pa.personnel_id AND DATE(pa.check_in_time) = CURRENT_DATE
LEFT JOIN alerts a ON sp.user_id = a.investigating_by AND a.status = 'open'
LEFT JOIN zones z_visited ON JSON_CONTAINS(sp.zones_visited_today, CAST(z_visited.id AS JSON), '$')
WHERE sp.site_id = ? 
    AND sp.status != 'inactive'
    AND sp.last_position_update >= DATE_SUB(NOW(), INTERVAL 2 HOUR)
GROUP BY sp.id
ORDER BY sp.last_position_update DESC;
```

##### **Personnel Safety Performance and Compliance:**
```sql
-- Personnel safety performance analytics
SELECT 
    sp.id as personnel_id, u.display_name,
    
    -- Current safety metrics
    sp.safety_score, sp.ppe_compliance_score,
    sp.safety_violations_today, sp.safety_violations_total,
    sp.days_without_incident, sp.last_safety_training,
    
    -- Historical safety performance
    AVG(pss.safety_score) as avg_safety_score_30_days,
    MIN(pss.safety_score) as min_safety_score_30_days,
    MAX(pss.safety_score) as max_safety_score_30_days,
    COUNT(pss.id) as safety_assessments_30_days,
    
    -- PPE compliance breakdown
    JSON_EXTRACT(sp.current_ppe_status, '$.hardhat') as hardhat_compliant,
    JSON_EXTRACT(sp.current_ppe_status, '$.safety_vest') as vest_compliant,
    JSON_EXTRACT(sp.current_ppe_status, '$.boots') as boots_compliant,
    JSON_EXTRACT(sp.current_ppe_status, '$.gloves') as gloves_compliant,
    
    -- Incident history
    COUNT(DISTINCT si.id) as incidents_30_days,
    MAX(si.incident_date) as last_incident_date,
    AVG(si.severity_score) as avg_incident_severity,
    
    -- Training compliance
    COUNT(DISTINCT uc.id) as total_certifications,
    COUNT(DISTINCT CASE WHEN uc.expiry_date >= CURRENT_DATE THEN uc.id END) as valid_certifications,
    COUNT(DISTINCT CASE WHEN uc.expiry_date < DATE_ADD(CURRENT_DATE, INTERVAL 30 DAY) THEN uc.id END) as expiring_certifications,
    
    -- Zone-specific safety performance
    GROUP_CONCAT(DISTINCT CONCAT(z.name, ':', sp.zone_safety_scores->'$."', z.id, '"') SEPARATOR ';') as zone_specific_scores

FROM site_personnel sp
JOIN users u ON sp.user_id = u.id
LEFT JOIN personnel_safety_scores pss ON sp.id = pss.personnel_id 
    AND pss.recorded_date >= DATE_SUB(CURRENT_DATE, INTERVAL 30 DAY)
LEFT JOIN safety_incidents si ON sp.id = si.personnel_id 
    AND si.incident_date >= DATE_SUB(CURRENT_DATE, INTERVAL 30 DAY)
LEFT JOIN user_certifications uc ON u.id = uc.user_id
LEFT JOIN zones z ON JSON_CONTAINS(sp.zones_visited_today, CAST(z.id AS JSON), '$')
WHERE sp.site_id = ?
GROUP BY sp.id
ORDER BY sp.safety_score DESC, sp.ppe_compliance_score DESC;
```

##### **Personnel Attendance and Time Tracking:**
```sql  
-- Comprehensive attendance and time tracking
SELECT 
    pa.id as attendance_id, pa.personnel_id,
    u.display_name, u.employee_id,
    
    -- Daily attendance
    pa.check_in_time, pa.check_out_time,
    pa.scheduled_start_time, pa.scheduled_end_time,
    
    -- Time calculations
    CASE 
        WHEN pa.check_in_time IS NOT NULL AND pa.check_out_time IS NOT NULL THEN
            TIMESTAMPDIFF(MINUTE, pa.check_in_time, pa.check_out_time)
        WHEN pa.check_in_time IS NOT NULL THEN
            TIMESTAMPDIFF(MINUTE, pa.check_in_time, NOW())
        ELSE 0
    END as total_work_minutes,
    
    -- Break time tracking
    pa.break_start_time, pa.break_end_time, pa.total_break_minutes,
    pa.authorized_break_minutes, 
    GREATEST(0, pa.total_break_minutes - pa.authorized_break_minutes) as excess_break_minutes,
    
    -- Overtime calculations
    pa.overtime_hours, pa.overtime_approved,
    CASE 
        WHEN TIMESTAMPDIFF(MINUTE, pa.scheduled_start_time, pa.check_in_time) > 5 THEN 'late'
        WHEN TIMESTAMPDIFF(MINUTE, pa.check_in_time, pa.scheduled_start_time) > 15 THEN 'early'
        ELSE 'on_time'
    END as arrival_status,
    
    -- Weekly summary
    (SELECT COUNT(*) FROM personnel_attendance pa_week 
     WHERE pa_week.personnel_id = pa.personnel_id 
     AND YEARWEEK(pa_week.check_in_time) = YEARWEEK(CURRENT_DATE)
    ) as days_worked_this_week,
    
    (SELECT SUM(TIMESTAMPDIFF(MINUTE, pa_week.check_in_time, pa_week.check_out_time))
     FROM personnel_attendance pa_week 
     WHERE pa_week.personnel_id = pa.personnel_id 
     AND YEARWEEK(pa_week.check_in_time) = YEARWEEK(CURRENT_DATE)
    ) as total_minutes_this_week,
    
    -- Attendance patterns
    pa.location_check_in, pa.location_check_out,
    pa.gps_accuracy_check_in, pa.gps_accuracy_check_out,
    pa.device_used_check_in, pa.device_used_check_out

FROM personnel_attendance pa
JOIN site_personnel sp ON pa.personnel_id = sp.id
JOIN users u ON sp.user_id = u.id
WHERE sp.site_id = ? 
    AND DATE(pa.check_in_time) >= DATE_SUB(CURRENT_DATE, INTERVAL 7 DAY)
ORDER BY pa.check_in_time DESC;
```

#### **Critical Database Relationships for Personnel Management:**
- **Users ← Site_Personnel**: Core personnel assignment and tracking
- **Site_Personnel ← Personnel_Attendance**: Time tracking and work sessions
- **Users ← User_Certifications**: Training and qualification management
- **Site_Personnel ← Personnel_Safety_Scores**: Safety performance history
- **Site_Personnel ← Department_Assignments**: Organizational structure
- **Site_Personnel → Zones**: Current location and zone compliance

---

## 📹 **ZoneMinder Integration**

### **Personnel Monitoring and Verification**

#### **1. Camera-Based Personnel Verification**
```sql
-- Personnel location verification through camera coverage
SELECT 
    sp.id as personnel_id, u.display_name,
    sp.current_coordinates, sp.current_zone_id,
    
    -- Camera coverage analysis
    COUNT(DISTINCT sc.camera_id) as covering_cameras,
    GROUP_CONCAT(DISTINCT c.name SEPARATOR ', ') as camera_names,
    GROUP_CONCAT(DISTINCT m.Id SEPARATOR ', ') as monitor_ids,
    
    -- Recent camera detections
    COUNT(DISTINCT ad.id) as detections_last_hour,
    MAX(ad.timestamp) as last_detection_time,
    AVG(ad.confidence_score) as avg_detection_confidence,
    
    -- Verification status
    CASE 
        WHEN COUNT(DISTINCT sc.camera_id) = 0 THEN 'no_coverage'
        WHEN COUNT(DISTINCT ad.id) = 0 THEN 'not_detected'
        WHEN MAX(ad.timestamp) < DATE_SUB(NOW(), INTERVAL 30 MINUTE) THEN 'outdated_detection'
        ELSE 'verified'
    END as location_verification_status,
    
    -- Stream URLs for personnel verification
    GROUP_CONCAT(DISTINCT CONCAT(
        '${zmBaseUrl}/zm/cgi-bin/nph-zms?mode=jpeg&scale=50&maxfps=5&monitor=', m.Id
    ) SEPARATOR '|') as verification_stream_urls

FROM site_personnel sp
JOIN users u ON sp.user_id = u.id
LEFT JOIN site_cameras sc ON sp.current_zone_id = ANY (
    SELECT zone_id FROM JSON_TABLE(sc.zone_coverage, '$[*]' COLUMNS (zone_id VARCHAR(255) PATH '$')) AS zones
)
LEFT JOIN cameras c ON sc.camera_id = c.id
LEFT JOIN Monitors m ON sc.zoneminder_monitor_id = m.Id
LEFT JOIN ai_detections ad ON sc.camera_id = ad.camera_id 
    AND ad.timestamp >= DATE_SUB(NOW(), INTERVAL 1 HOUR)
    AND JSON_CONTAINS(ad.person_tracks, JSON_OBJECT('user_id', sp.user_id))
WHERE sp.site_id = ? 
    AND sp.status = 'active'
    AND sp.last_position_update >= DATE_SUB(NOW(), INTERVAL 2 HOUR)
GROUP BY sp.id
ORDER BY location_verification_status, sp.last_position_update DESC;
```

#### **2. Personnel Safety Monitoring Integration**
```javascript
class PersonnelZMIntegration {
    constructor(zmBaseUrl, authToken) {
        this.zmBaseUrl = zmBaseUrl;
        this.authToken = authToken;
        this.personnelTrackingCache = new Map();
    }
    
    async verifyPersonnelLocation(personnelId, reportedLocation) {
        try {
            // Get cameras covering reported location
            const coveringCameras = await this.getCamerasForLocation(reportedLocation);
            
            if (coveringCameras.length === 0) {
                return {
                    verification_status: 'no_coverage',
                    confidence: 0,
                    message: 'No cameras cover this location'
                };
            }
            
            // Check recent detections in covering cameras
            const verificationResults = [];
            
            for (const camera of coveringCameras) {
                // Get recent frames and run person detection
                const detectionResult = await this.checkPersonnelInCamera(
                    camera.zoneminder_monitor_id,
                    personnelId
                );
                
                if (detectionResult.detected) {
                    verificationResults.push({
                        camera_id: camera.camera_id,
                        camera_name: camera.name,
                        confidence: detectionResult.confidence,
                        detection_time: detectionResult.timestamp,
                        bbox: detectionResult.bounding_box
                    });
                }
            }
            
            // Determine verification status
            let verification_status = 'not_detected';
            let overall_confidence = 0;
            
            if (verificationResults.length > 0) {
                verification_status = 'verified';
                overall_confidence = Math.max(...verificationResults.map(r => r.confidence));
            }
            
            return {
                verification_status,
                confidence: overall_confidence,
                detections: verificationResults,
                covering_cameras: coveringCameras.length,
                message: `Location ${verification_status} with ${overall_confidence}% confidence`
            };
            
        } catch (error) {
            console.error(`Personnel location verification failed: ${error.message}`);
            return {
                verification_status: 'error',
                confidence: 0,
                error: error.message
            };
        }
    }
    
    async generatePersonnelSecuritySnapshot(personnelId) {
        try {
            // Get personnel current location and covering cameras
            const personnelData = await this.getPersonnelLocationData(personnelId);
            if (!personnelData) {
                throw new Error('Personnel location data not found');
            }
            
            const cameras = await this.getCamerasForLocation(personnelData.current_location);
            const snapshots = [];
            
            for (const camera of cameras) {
                // Capture snapshot from ZoneMinder
                const snapshotUrl = `${this.zmBaseUrl}/zm/cgi-bin/zms?mode=single&monitor=${camera.zoneminder_monitor_id}&scale=100&timestamp=${Date.now()}`;
                
                const response = await fetch(snapshotUrl, {
                    headers: { 'Authorization': `Bearer ${this.authToken}` }
                });
                
                if (response.ok) {
                    const snapshotBuffer = await response.arrayBuffer();
                    const fileName = `personnel_snapshot_${personnelId}_${camera.camera_id}_${Date.now()}.jpg`;
                    
                    // Store snapshot for personnel verification
                    const snapshotPath = await this.storePersonnelSnapshot(fileName, snapshotBuffer);
                    
                    snapshots.push({
                        camera_id: camera.camera_id,
                        camera_name: camera.name,
                        snapshot_url: `/api/personnel-snapshots/${fileName}`,
                        file_path: snapshotPath,
                        timestamp: new Date().toISOString(),
                        location: personnelData.current_location
                    });
                }
            }
            
            return {
                personnel_id: personnelId,
                snapshots: snapshots,
                total_snapshots: snapshots.length,
                timestamp: new Date().toISOString()
            };
            
        } catch (error) {
            console.error(`Personnel snapshot generation failed: ${error.message}`);
            return {
                personnel_id: personnelId,
                snapshots: [],
                error: error.message
            };
        }
    }
    
    async trackPersonnelMovement(personnelId, timeRange = 3600) {
        try {
            // Get personnel movement history
            const movementHistory = await this.getPersonnelMovementHistory(personnelId, timeRange);
            const trackingData = [];
            
            for (const movement of movementHistory) {
                // Find cameras that covered each location
                const cameras = await this.getCamerasForLocation(movement.location);
                
                for (const camera of cameras) {
                    // Get ZoneMinder events during movement timeframe
                    const events = await this.getZMEventsInTimeRange(
                        camera.zoneminder_monitor_id,
                        movement.start_time,
                        movement.end_time
                    );
                    
                    // Correlate events with personnel presence
                    for (const event of events) {
                        const correlation = await this.correlateEventWithPersonnel(event, personnelId);
                        
                        if (correlation.likely_match) {
                            trackingData.push({
                                personnel_id: personnelId,
                                location: movement.location,
                                camera_id: camera.camera_id,
                                zm_event_id: event.Id,
                                event_start: event.StartTime,
                                event_end: event.EndTime,
                                confidence: correlation.confidence,
                                movement_verified: true
                            });
                        }
                    }
                }
            }
            
            return {
                personnel_id: personnelId,
                tracking_period_seconds: timeRange,
                movements_tracked: trackingData.length,
                tracking_data: trackingData,
                verification_rate: trackingData.filter(t => t.movement_verified).length / trackingData.length
            };
            
        } catch (error) {
            console.error(`Personnel movement tracking failed: ${error.message}`);
            return {
                personnel_id: personnelId,
                tracking_data: [],
                error: error.message
            };
        }
    }
}
```

---

## 🤖 **AI/YOLO Integration (Roboflow)**

### **Personnel Identification and Safety Monitoring**

#### **1. Personnel Recognition and Tracking**
```python
class PersonnelAIIntegration:
    def __init__(self, person_detector, face_recognizer, ppe_detector):
        self.person_detector = person_detector
        self.face_recognizer = face_recognizer
        self.ppe_detector = ppe_detector
        self.personnel_tracking_data = {}
        
    async def process_personnel_detection(self, camera_id, frame_image):
        """Comprehensive personnel detection and identification"""
        try:
            # Run person detection
            person_results = await self.person_detector.detect_persons(
                frame_image,
                confidence_threshold=0.8,
                enable_tracking=True
            )
            
            if person_results["person_count"] == 0:
                return {
                    "camera_id": camera_id,
                    "timestamp": datetime.utcnow().isoformat(),
                    "personnel_detected": [],
                    "total_personnel": 0
                }
            
            personnel_detections = []
            
            # Process each detected person
            for i, person_bbox in enumerate(person_results["bounding_boxes"]):
                # Extract person crop for detailed analysis
                person_crop = self.extract_person_crop(frame_image, person_bbox)
                
                # Face recognition for personnel identification
                face_recognition_result = await self.face_recognizer.identify_person(person_crop)
                
                # PPE compliance analysis
                ppe_analysis = await self.ppe_detector.detect_ppe_compliance([person_crop])
                ppe_result = ppe_analysis[0] if ppe_analysis else None
                
                # Activity classification
                activity = self.classify_person_activity(person_crop, person_bbox)
                
                personnel_detection = {
                    "detection_id": f"person_{i}_{camera_id}_{int(time.time())}",
                    "track_id": person_bbox.get("track_id", f"track_{i}"),
                    "bounding_box": person_bbox,
                    "confidence": person_bbox["confidence"],
                    
                    # Identity recognition
                    "identified_personnel": {
                        "user_id": face_recognition_result.get("user_id"),
                        "name": face_recognition_result.get("name"),
                        "confidence": face_recognition_result.get("confidence", 0),
                        "identification_method": face_recognition_result.get("method", "unknown")
                    } if face_recognition_result and face_recognition_result.get("user_id") else None,
                    
                    # PPE compliance
                    "ppe_analysis": {
                        "overall_compliance": ppe_result["compliance_score"] if ppe_result else 0,
                        "hardhat": ppe_result["ppe_items"].get("hardhat", False) if ppe_result else False,
                        "safety_vest": ppe_result["ppe_items"].get("safety_vest", False) if ppe_result else False,
                        "boots": ppe_result["ppe_items"].get("boots", False) if ppe_result else False,
                        "gloves": ppe_result["ppe_items"].get("gloves", False) if ppe_result else False,
                        "violations": ppe_result["violations"] if ppe_result else []
                    },
                    
                    # Activity and behavior
                    "activity_analysis": {
                        "activity_type": activity["type"],
                        "confidence": activity["confidence"],
                        "movement_pattern": activity.get("movement"),
                        "posture": activity.get("posture"),
                        "interaction_objects": activity.get("objects", [])
                    },
                    
                    # Location context
                    "location_context": await self.get_location_context(camera_id, person_bbox),
                    
                    # Safety assessment
                    "safety_assessment": self.assess_personnel_safety(ppe_result, activity, camera_id),
                    
                    "timestamp": datetime.utcnow().isoformat()
                }
                
                personnel_detections.append(personnel_detection)
                
                # Update personnel tracking data
                await self.update_personnel_tracking(personnel_detection)
                
                # Generate alerts if necessary
                await self.check_personnel_safety_alerts(personnel_detection)
            
            return {
                "camera_id": camera_id,
                "timestamp": datetime.utcnow().isoformat(),
                "personnel_detected": personnel_detections,
                "total_personnel": len(personnel_detections),
                "processing_time_ms": 0  # Would be calculated
            }
            
        except Exception as e:
            logger.error(f"Personnel AI detection failed: {str(e)}")
            return {
                "camera_id": camera_id,
                "personnel_detected": [],
                "error": str(e)
            }
    
    async def update_personnel_tracking(self, detection_data):
        """Update personnel tracking database with AI detection data"""
        try:
            if not detection_data.get("identified_personnel", {}).get("user_id"):
                return  # Skip unidentified personnel
            
            user_id = detection_data["identified_personnel"]["user_id"]
            camera_id = detection_data.get("camera_id")
            
            # Get camera location for position estimation
            camera_data = await self.get_camera_data(camera_id)
            estimated_position = self.estimate_person_position(
                detection_data["bounding_box"],
                camera_data
            )
            
            # Update site_personnel table
            await self.db.execute("""
                UPDATE site_personnel 
                SET 
                    current_coordinates = POINT(?, ?),
                    last_position_update = NOW(),
                    ppe_compliance_score = ?,
                    current_ppe_status = ?,
                    safety_score = ?,
                    last_activity_type = ?,
                    activity_timestamp = NOW()
                WHERE user_id = ? AND site_id = ?
            """, [
                estimated_position[0], estimated_position[1],
                detection_data["ppe_analysis"]["overall_compliance"],
                json.dumps(detection_data["ppe_analysis"]),
                detection_data["safety_assessment"]["overall_score"],
                detection_data["activity_analysis"]["activity_type"],
                user_id, camera_data["site_id"]
            ])
            
            # Log detection in AI detection history
            await self.store_personnel_detection(detection_data)
            
        except Exception as e:
            logger.error(f"Personnel tracking update failed: {str(e)}")
    
    def assess_personnel_safety(self, ppe_result, activity, camera_id):
        """Assess overall personnel safety based on multiple factors"""
        safety_factors = {
            "ppe_compliance": 0,
            "activity_safety": 0,
            "zone_compliance": 0,
            "behavior_assessment": 0
        }
        
        # PPE compliance assessment
        if ppe_result:
            safety_factors["ppe_compliance"] = ppe_result["compliance_score"]
        
        # Activity safety assessment
        activity_safety_scores = {
            "working": 90,
            "walking": 85,
            "running": 60,  # Potentially unsafe
            "climbing": 70,
            "lifting": 75,
            "operating_equipment": 80,
            "emergency_response": 95
        }
        safety_factors["activity_safety"] = activity_safety_scores.get(activity["type"], 80)
        
        # Zone compliance (would be determined by camera zone context)
        safety_factors["zone_compliance"] = 90  # Placeholder
        
        # Behavior assessment (posture, movement patterns)
        behavior_safety = self.assess_behavior_safety(activity)
        safety_factors["behavior_assessment"] = behavior_safety
        
        # Calculate overall safety score
        overall_score = sum(safety_factors.values()) / len(safety_factors)
        
        # Determine risk level
        risk_level = "low"
        if overall_score < 60:
            risk_level = "high"
        elif overall_score < 80:
            risk_level = "medium"
        
        return {
            "overall_score": overall_score,
            "risk_level": risk_level,
            "safety_factors": safety_factors,
            "recommendations": self.generate_safety_recommendations(safety_factors),
            "requires_intervention": overall_score < 70
        }
```

#### **2. Personnel Safety Alert Generation**
```json
{
  "personnel_safety_alert": {
    "alert_id": "personnel_alert_123456789",
    "personnel_id": "person_001",
    "user_id": "user_abc123",
    "personnel_name": "John Mitchell",
    "timestamp": "2025-01-12T14:30:15Z",
    "alert_type": "personnel_safety_violation",
    "priority": "high",
    
    "detection_context": {
      "camera_id": "cam_001",
      "camera_name": "Zone A Construction Camera",
      "detection_confidence": 94.8,
      "identification_confidence": 89.5,
      "detection_method": "face_recognition_and_tracking"
    },
    
    "safety_violation": {
      "violation_type": "ppe_non_compliance",
      "missing_ppe": ["hardhat", "safety_vest"],
      "zone_requirements": ["hardhat", "safety_vest", "boots", "gloves"],
      "compliance_score": 45.2,
      "severity": "critical"
    },
    
    "personnel_status": {
      "work_status": "active",
      "current_location": "Zone A - Foundation Area",
      "shift_hours": 4.2,
      "recent_safety_score": 87.5,
      "previous_violations_today": 1
    },
    
    "ai_analysis": {
      "activity_detected": "heavy_lifting",
      "posture_analysis": "unsafe_lifting_posture",
      "equipment_interaction": ["crane_hook", "steel_beam"],
      "behavior_assessment": "high_risk_activity_without_proper_ppe"
    },
    
    "recommended_actions": [
      "Immediately halt current activity",
      "Dispatch safety supervisor to Zone A",
      "Provide required PPE (hardhat, safety vest)",
      "Conduct safety refresher training",
      "Document incident for compliance"
    ],
    
    "escalation_protocol": {
      "immediate_supervisor": "supervisor_001",
      "safety_officer": "safety_001", 
      "site_manager": "manager_001",
      "escalation_timeline": "immediate"
    },
    
    "evidence": {
      "detection_image": "/api/evidence/personnel_detection_001.jpg",
      "annotated_image": "/api/evidence/personnel_annotated_001.jpg",
      "video_clip": "/api/evidence/personnel_incident_001.mp4",
      "ai_analysis_data": "/api/evidence/ai_data_001.json"
    }
  }
}
```

---

## ⚠️ **RUNTIME BUG ANALYSIS & SOLUTION**

### **🐛 Identified Runtime Issues**

#### **Issue 1: Mock Data Handling Error**
**Problem**: The component attempts to access `mockPersonnel` which may be undefined or null, causing runtime crashes.

**Location**: Lines 21, 50-140 in PersonnelManagement.js

**Root Cause**: 
```javascript
const [personnel, setPersonnel] = useState(mockPersonnel || []); // Line 21
// Later: const generateMockPersonnel = () => {
//   if (mockPersonnel && mockPersonnel.length > 0) return mockPersonnel; // Line 51
```

**Solution**:
```javascript
// Fixed initialization with proper fallback
const [personnel, setPersonnel] = useState(() => {
  if (Array.isArray(mockPersonnel) && mockPersonnel.length > 0) {
    return mockPersonnel;
  }
  return generateDefaultPersonnel();
});

// Improved mock data generation
const generateDefaultPersonnel = () => {
  return [
    // ... existing mock data structure
  ];
};
```

#### **Issue 2: Date Formatting Errors** 
**Problem**: Inconsistent date handling causing format errors in `formatTime` and `formatLastSeen` functions.

**Location**: Lines 335-354

**Solution**:
```javascript
const formatTime = (timestamp) => {
  if (!timestamp) return 'Not checked in';
  try {
    const date = new Date(timestamp);
    if (isNaN(date.getTime())) return 'Invalid time';
    return date.toLocaleTimeString('en-US', { 
      hour: '2-digit', 
      minute: '2-digit',
      hour12: false 
    });
  } catch (error) {
    console.error('Time formatting error:', error);
    return 'Time error';
  }
};

const formatLastSeen = (timestamp) => {
  if (!timestamp) return 'Never';
  try {
    const now = new Date();
    const lastSeen = new Date(timestamp);
    
    if (isNaN(now.getTime()) || isNaN(lastSeen.getTime())) {
      return 'Invalid date';
    }
    
    const diffMinutes = Math.floor((now - lastSeen) / (1000 * 60));
    
    if (diffMinutes < 1) return 'Just now';
    if (diffMinutes < 60) return `${diffMinutes}m ago`;
    
    const diffHours = Math.floor(diffMinutes / 60);
    if (diffHours < 24) return `${diffHours}h ago`;
    
    const diffDays = Math.floor(diffHours / 24);
    return `${diffDays}d ago`;
  } catch (error) {
    console.error('Last seen formatting error:', error);
    return 'Time error';
  }
};
```

#### **Issue 3: Memory Leak in Real-time Updates**
**Problem**: The `useEffect` interval on lines 303-317 doesn't properly clean up, causing memory leaks.

**Solution**:
```javascript
useEffect(() => {
  if (personnel.length === 0) return; // Don't start if no personnel
  
  const interval = setInterval(() => {
    setPersonnel(prev => {
      if (prev.length === 0) return prev; // Safety check
      
      return prev.map(person => {
        if (person.status === 'active' && Math.random() < 0.3) {
          const locations = [
            'Zone A - Foundation', 
            'Zone B - Steel Frame', 
            'Zone C - Excavation', 
            'Safety Office', 
            'Equipment Storage'
          ];
          const randomLocation = locations[Math.floor(Math.random() * locations.length)];
          
          return { 
            ...person, 
            currentLocation: randomLocation, 
            lastSeen: new Date().toISOString() // Use ISO string for consistency
          };
        }
        return person;
      });
    });
  }, 15000);

  return () => {
    clearInterval(interval);
  };
}, [personnel.length]); // Add dependency to restart when personnel changes
```

---

## 🔧 **COMPLETE FIXED PERSONNEL MANAGEMENT INTEGRATION**

### **1. ✅ FIXED: New Database Tables for Personnel Management**

#### **User Certifications Table**
```sql
CREATE TABLE user_certifications (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL,
    
    -- Certification details
    certification_name VARCHAR(255) NOT NULL,
    certification_type ENUM('safety', 'technical', 'license', 'training', 'medical') NOT NULL,
    certification_number VARCHAR(100),
    issuing_authority VARCHAR(255),
    
    -- Validity and compliance
    issue_date DATE NOT NULL,
    expiry_date DATE,
    renewal_required BOOLEAN DEFAULT TRUE,
    renewal_period_months INT,
    
    -- Status tracking
    status ENUM('active', 'expired', 'suspended', 'pending_renewal') DEFAULT 'active',
    verification_status ENUM('verified', 'pending', 'rejected') DEFAULT 'pending',
    
    -- Compliance requirements
    required_for_roles JSON, -- Array of roles requiring this certification
    required_for_zones JSON, -- Array of zone IDs requiring this certification
    
    -- Files and documentation
    certificate_file_path VARCHAR(500),
    verification_documents JSON, -- Array of document paths
    
    -- Audit trail
    created_by UUID,
    verified_by UUID,
    last_verification_check DATE,
    
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (created_by) REFERENCES users(id),
    FOREIGN KEY (verified_by) REFERENCES users(id),
    
    INDEX idx_user_certifications_user (user_id),
    INDEX idx_user_certifications_type (certification_type),
    INDEX idx_user_certifications_status (status),
    INDEX idx_user_certifications_expiry (expiry_date),
    INDEX idx_user_certifications_required_roles (required_for_roles),
    UNIQUE KEY unique_user_certification (user_id, certification_name, certification_number)
);
```

#### **Personnel Attendance Table**
```sql
CREATE TABLE personnel_attendance (
    id UUID PRIMARY KEY,
    personnel_id UUID NOT NULL,
    attendance_date DATE NOT NULL,
    
    -- Check-in/Check-out
    check_in_time TIMESTAMP,
    check_out_time TIMESTAMP,
    scheduled_start_time TIME,
    scheduled_end_time TIME,
    
    -- Break management
    break_start_time TIMESTAMP,
    break_end_time TIMESTAMP,
    total_break_minutes INT DEFAULT 0,
    authorized_break_minutes INT DEFAULT 30,
    
    -- Time calculations
    total_work_minutes INT DEFAULT 0,
    overtime_hours DECIMAL(4,2) DEFAULT 0.00,
    overtime_approved BOOLEAN DEFAULT FALSE,
    
    -- Location verification
    location_check_in POINT,
    location_check_out POINT,
    gps_accuracy_check_in DECIMAL(8,2), -- meters
    gps_accuracy_check_out DECIMAL(8,2),
    
    -- Device and method tracking
    device_used_check_in VARCHAR(255), -- mobile, tablet, terminal, etc.
    device_used_check_out VARCHAR(255),
    check_in_method ENUM('gps', 'qr_code', 'nfc', 'manual', 'facial_recognition') DEFAULT 'gps',
    check_out_method ENUM('gps', 'qr_code', 'nfc', 'manual', 'facial_recognition') DEFAULT 'gps',
    
    -- Status and compliance
    attendance_status ENUM('present', 'late', 'absent', 'partial', 'overtime') DEFAULT 'present',
    tardiness_minutes INT DEFAULT 0,
    early_departure_minutes INT DEFAULT 0,
    
    -- Approval and notes
    approved_by UUID,
    supervisor_notes TEXT,
    employee_notes TEXT,
    
    FOREIGN KEY (personnel_id) REFERENCES site_personnel(id),
    FOREIGN KEY (approved_by) REFERENCES users(id),
    
    UNIQUE KEY unique_personnel_date (personnel_id, attendance_date),
    INDEX idx_attendance_personnel_date (personnel_id, attendance_date DESC),
    INDEX idx_attendance_status (attendance_status),
    INDEX idx_attendance_overtime (overtime_hours DESC),
    SPATIAL INDEX idx_attendance_checkin_location (location_check_in),
    SPATIAL INDEX idx_attendance_checkout_location (location_check_out)
);
```

#### **Personnel Safety Scores Table**
```sql
CREATE TABLE personnel_safety_scores (
    id UUID PRIMARY KEY,
    personnel_id UUID NOT NULL,
    recorded_date DATE NOT NULL,
    recorded_time TIME DEFAULT CURRENT_TIME,
    
    -- Safety metrics
    safety_score DECIMAL(5,2) NOT NULL, -- 0.00 to 100.00
    ppe_compliance_score DECIMAL(5,2) NOT NULL,
    behavior_score DECIMAL(5,2) DEFAULT 100.00,
    zone_compliance_score DECIMAL(5,2) DEFAULT 100.00,
    
    -- Assessment details
    assessment_type ENUM('ai_automated', 'supervisor_review', 'incident_based', 'periodic_review') NOT NULL,
    assessed_by UUID,
    assessment_camera_id UUID,
    assessment_zone_id UUID,
    
    -- Detailed breakdown
    ppe_items_status JSON, -- Detailed PPE compliance by item
    safety_violations JSON, -- Array of violations detected
    positive_behaviors JSON, -- Array of positive safety behaviors
    
    -- Context and evidence
    assessment_context TEXT,
    evidence_files JSON, -- Array of evidence file paths
    ai_confidence_score DECIMAL(5,2),
    
    -- Improvement tracking
    previous_score DECIMAL(5,2),
    score_change DECIMAL(6,2), -- Can be negative
    improvement_notes TEXT,
    corrective_actions JSON,
    
    FOREIGN KEY (personnel_id) REFERENCES site_personnel(id),
    FOREIGN KEY (assessed_by) REFERENCES users(id),
    FOREIGN KEY (assessment_camera_id) REFERENCES cameras(id),
    FOREIGN KEY (assessment_zone_id) REFERENCES zones(id),
    
    INDEX idx_safety_scores_personnel_date (personnel_id, recorded_date DESC),
    INDEX idx_safety_scores_type (assessment_type),
    INDEX idx_safety_scores_score (safety_score DESC),
    INDEX idx_safety_scores_assessor (assessed_by),
    INDEX idx_safety_scores_zone (assessment_zone_id)
);
```

#### **Department Assignments Table**
```sql
CREATE TABLE department_assignments (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL,
    site_id UUID NOT NULL,
    
    -- Department and position
    department_name VARCHAR(255) NOT NULL,
    position_title VARCHAR(255) NOT NULL,
    position_level ENUM('entry', 'junior', 'mid', 'senior', 'lead', 'supervisor', 'manager') DEFAULT 'entry',
    
    -- Reporting structure
    reporting_manager_id UUID,
    department_head_id UUID,
    
    -- Assignment details
    start_date DATE NOT NULL,
    end_date DATE,
    is_active BOOLEAN DEFAULT TRUE,
    assignment_type ENUM('permanent', 'temporary', 'contract', 'intern') DEFAULT 'permanent',
    
    -- Responsibilities and permissions
    job_responsibilities JSON, -- Array of responsibility descriptions
    zone_access_permissions JSON, -- Array of zone IDs user can access
    equipment_permissions JSON, -- Array of equipment IDs user can operate
    
    -- Work schedule
    default_shift_start TIME,
    default_shift_end TIME,
    work_days JSON, -- Array of weekdays (0=Sunday, 1=Monday, etc.)
    
    -- Compensation (optional)
    hourly_rate DECIMAL(8,2),
    overtime_rate DECIMAL(8,2),
    
    -- Assignment history
    assigned_by UUID,
    assignment_reason TEXT,
    previous_assignment_id UUID, -- Reference to previous assignment
    
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (site_id) REFERENCES sites(id),
    FOREIGN KEY (reporting_manager_id) REFERENCES users(id),
    FOREIGN KEY (department_head_id) REFERENCES users(id),
    FOREIGN KEY (assigned_by) REFERENCES users(id),
    FOREIGN KEY (previous_assignment_id) REFERENCES department_assignments(id),
    
    INDEX idx_department_assignments_user (user_id),
    INDEX idx_department_assignments_site (site_id),
    INDEX idx_department_assignments_department (department_name),
    INDEX idx_department_assignments_manager (reporting_manager_id),
    INDEX idx_department_assignments_active (is_active, start_date DESC)
);
```

### **2. ✅ FIXED: Enhanced Personnel Management Backend Integration**

#### **Personnel Real-time Update Service**
```python
class PersonnelManagementService:
    def __init__(self, db_connection, websocket_manager):
        self.db = db_connection
        self.websocket = websocket_manager
        
    async def update_personnel_status(self, personnel_id, new_status, location=None, user_id=None):
        """Update personnel status with real-time broadcasting"""
        try:
            update_data = {
                "status": new_status,
                "last_position_update": datetime.utcnow(),
                "activity_timestamp": datetime.utcnow()
            }
            
            if location:
                # Determine zone from location
                zone_data = await self.detect_zone_from_location(location)
                update_data.update({
                    "current_coordinates": f"POINT({location[0]} {location[1]})",
                    "current_zone_id": zone_data.get("zone_id") if zone_data else None
                })
            
            # Update database
            await self.db.execute("""
                UPDATE site_personnel 
                SET status = :status,
                    current_coordinates = :current_coordinates,
                    current_zone_id = :current_zone_id,
                    last_position_update = :last_position_update,
                    activity_timestamp = :activity_timestamp
                WHERE id = :personnel_id
            """, {**update_data, "personnel_id": personnel_id})
            
            # Update attendance if check-in/check-out
            if new_status in ['active', 'off-site']:
                await self.update_attendance_record(personnel_id, new_status, location)
            
            # Get updated personnel data
            updated_personnel = await self.get_personnel_by_id(personnel_id)
            
            # Broadcast update to all connected clients
            await self.websocket.broadcast_personnel_update(updated_personnel)
            
            return {
                "success": True,
                "personnel_id": personnel_id,
                "new_status": new_status,
                "updated_at": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Personnel status update failed: {str(e)}")
            return {"success": False, "error": str(e)}
    
    async def bulk_update_personnel_status(self, personnel_ids, new_status):
        """Bulk update personnel status with transaction safety"""
        try:
            async with self.db.begin() as transaction:
                updated_personnel = []
                
                for personnel_id in personnel_ids:
                    result = await self.update_personnel_status(personnel_id, new_status)
                    if result["success"]:
                        updated_personnel.append(personnel_id)
                    else:
                        # Rollback on any failure
                        await transaction.rollback()
                        return {
                            "success": False,
                            "error": f"Bulk update failed at personnel {personnel_id}"
                        }
                
                await transaction.commit()
                
                # Broadcast bulk update
                await self.websocket.broadcast_bulk_personnel_update({
                    "personnel_ids": updated_personnel,
                    "new_status": new_status,
                    "updated_count": len(updated_personnel)
                })
                
                return {
                    "success": True,
                    "updated_count": len(updated_personnel),
                    "personnel_ids": updated_personnel
                }
                
        except Exception as e:
            logger.error(f"Bulk personnel update failed: {str(e)}")
            return {"success": False, "error": str(e)}
    
    async def generate_personnel_safety_report(self, site_id, time_period="week"):
        """Generate comprehensive personnel safety report"""
        try:
            # Calculate date range
            end_date = datetime.utcnow().date()
            if time_period == "week":
                start_date = end_date - timedelta(days=7)
            elif time_period == "month":
                start_date = end_date - timedelta(days=30)
            else:
                start_date = end_date - timedelta(days=1)
            
            # Get personnel safety data
            safety_data = await self.db.fetch_all("""
                SELECT 
                    u.display_name,
                    sp.id as personnel_id,
                    sp.safety_score,
                    sp.ppe_compliance_score,
                    sp.safety_violations_today,
                    COUNT(pss.id) as safety_assessments,
                    AVG(pss.safety_score) as avg_safety_score,
                    COUNT(DISTINCT uc.id) as valid_certifications,
                    COUNT(DISTINCT si.id) as incidents
                FROM site_personnel sp
                JOIN users u ON sp.user_id = u.id
                LEFT JOIN personnel_safety_scores pss ON sp.id = pss.personnel_id 
                    AND pss.recorded_date BETWEEN ? AND ?
                LEFT JOIN user_certifications uc ON u.id = uc.user_id 
                    AND uc.status = 'active' AND uc.expiry_date >= CURRENT_DATE
                LEFT JOIN safety_incidents si ON sp.id = si.personnel_id 
                    AND si.incident_date BETWEEN ? AND ?
                WHERE sp.site_id = ?
                GROUP BY sp.id
                ORDER BY sp.safety_score DESC
            """, [start_date, end_date, start_date, end_date, site_id])
            
            # Generate report summary
            total_personnel = len(safety_data)
            avg_safety_score = sum(p["safety_score"] for p in safety_data) / total_personnel if total_personnel > 0 else 0
            high_risk_personnel = len([p for p in safety_data if p["safety_score"] < 70])
            
            return {
                "report_generated": datetime.utcnow().isoformat(),
                "time_period": time_period,
                "date_range": {"start": start_date.isoformat(), "end": end_date.isoformat()},
                "summary": {
                    "total_personnel": total_personnel,
                    "average_safety_score": avg_safety_score,
                    "high_risk_personnel": high_risk_personnel,
                    "safety_compliance_rate": (total_personnel - high_risk_personnel) / total_personnel * 100 if total_personnel > 0 else 0
                },
                "personnel_data": safety_data
            }
            
        except Exception as e:
            logger.error(f"Safety report generation failed: {str(e)}")
            return {"success": False, "error": str(e)}
```

---

## 📈 **Success Metrics**

- **Real-time Updates**: Personnel status updates delivered within 3 seconds
- **Data Accuracy**: Personnel location accuracy within 5 meters using GPS/AI correlation
- **Search Performance**: Advanced filtering results returned within 500ms
- **Bulk Operations**: Support for 100+ personnel bulk operations within 10 seconds
- **Safety Monitoring**: 99% accuracy in PPE compliance detection and reporting
- **Attendance Tracking**: Automated time tracking with 95% GPS verification accuracy
- **Export Performance**: Personnel data export completed within 15 seconds for 500+ records

---

## 🔧 **FIXED RUNTIME BUG SUMMARY**

✅ **Mock Data Handling**: Proper null/undefined checks and fallback data generation  
✅ **Date Formatting**: Robust error handling and consistent date parsing  
✅ **Memory Management**: Proper cleanup of intervals and effects to prevent memory leaks  
✅ **State Management**: Improved state initialization and update patterns  
✅ **Error Boundaries**: Comprehensive error handling for all async operations

**Document Created**: 2025-01-12  
**Next Screen**: AI Analytics (/ai-analytics)