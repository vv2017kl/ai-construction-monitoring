# 🏗️ Screen Analysis #05: Site Overview (/site-overview)

## 📋 **Document Information**
- **Screen Path**: `/site-overview`
- **Menu Location**: Site Management → Site Overview
- **Portal**: Solution User Portal
- **Priority**: CRITICAL (Central management hub)
- **Status**: ✅ Implemented and Functional

---

## 🎯 **Functional Analysis**

### **Primary Purpose**
Comprehensive site management dashboard providing interactive 2D/blueprint-style site visualization with real-time monitoring of cameras, personnel, equipment, zones, and safety conditions for operational control and situational awareness.

### **Core Features & User Workflows**

#### **1. Interactive Site Map System**
- **Multi-View Map Modes**:
  - **Satellite View**: Aerial imagery simulation with realistic terrain
  - **Blueprint View**: Technical blueprint with grid overlay and measurements
  - **Hybrid View**: Combination of satellite imagery with blueprint grid overlay
  - **Dynamic Zoom Control**: 50% to 200% zoom levels with smooth scaling
  - **Pan Control**: Interactive map navigation with center point tracking

- **Real-time Layer Management**:
  - **Camera Layer**: Live camera positions with status indicators and field-of-view cones
  - **Zone Layer**: Safety zones, work areas, restricted areas with color coding
  - **Personnel Layer**: Real-time personnel positions with PPE compliance indicators
  - **Equipment Layer**: Heavy equipment tracking with operational status
  - **Alert Layer**: Safety alert overlays with severity-based visual indicators

#### **2. Advanced Zone Management System**
- **Interactive Zone Creation**:
  - **Drawing Tools**: Rectangle, circle, and polygon zone creation with real-time preview
  - **Click-and-Drag Interface**: Intuitive zone boundary definition
  - **Multi-point Polygon**: Complex zone shapes with point-by-point creation
  - **Visual Feedback**: Real-time drawing guides with snap-to-grid functionality

- **Zone Configuration Management**:
  - **Zone Types**: Work areas, safety zones, restricted areas, equipment zones, hazardous areas
  - **Safety Level Assignment**: Low, medium, high, critical safety classifications
  - **Occupancy Controls**: Maximum personnel limits with real-time tracking
  - **PPE Requirements**: Mandatory safety equipment specifications
  - **Access Control Integration**: Permission-based zone restrictions

#### **3. Multi-Entity Selection and Bulk Operations**
- **Advanced Selection System**:
  - **Individual Selection**: Click-to-select cameras, zones, personnel, equipment
  - **Multi-select Mode**: Checkbox-based bulk selection with visual feedback
  - **Select All Functions**: Bulk selection by entity type (all cameras, all zones)
  - **Selection Persistence**: Maintain selections across view changes and operations

- **Bulk Action Capabilities**:
  - **Monitoring Operations**: Bulk enable/disable monitoring for selected cameras
  - **Configuration Updates**: Batch configuration changes for multiple entities
  - **Data Export**: Comprehensive site data export with selection filtering
  - **Status Updates**: Bulk status changes and operational control

#### **4. Real-time Personnel and Equipment Tracking**
- **Live Personnel Monitoring**:
  - **Position Tracking**: Real-time personnel location updates with smooth movement animation
  - **PPE Compliance Indicators**: Color-coded personnel markers based on compliance scores
  - **Status Tracking**: Working, moving, break, inspection status indicators
  - **Zone Occupancy Monitoring**: Real-time zone capacity tracking and alerts

- **Equipment Position Management**:
  - **Heavy Equipment Tracking**: Excavators, cranes, trucks with operational status
  - **Status Visualization**: Active, idle, loading, maintenance status indicators
  - **Movement Patterns**: Historical movement tracking for optimization analysis
  - **Safety Zone Integration**: Equipment proximity alerts and zone violations

#### **5. Camera Management and Live Preview**
- **Interactive Camera Controls**:
  - **Camera Status Visualization**: Online/offline status with health indicators
  - **Alert Correlation**: Camera-specific alert counts with severity indicators
  - **Field of View Display**: Camera coverage area visualization with adjustable cones
  - **Quick Preview Modal**: Instant camera feed preview without navigation

- **Camera Integration Features**:
  - **Live Feed Access**: Direct navigation to live monitoring interface
  - **Alert Management**: Quick access to camera-specific alert management
  - **Configuration Access**: Camera settings and configuration management
  - **Performance Monitoring**: Camera health and performance indicators

#### **6. Environmental and Site Condition Monitoring**
- **Weather Integration**:
  - **Real-time Conditions**: Temperature, wind speed, weather condition display
  - **Safety Impact Assessment**: Weather-based work condition evaluation
  - **Historical Tracking**: Weather trend analysis for planning optimization
  - **Alert Integration**: Weather-based safety alerts and recommendations

- **Site Status Dashboard**:
  - **Activity Overview**: Personnel count, camera status, zone occupancy
  - **Safety Metrics**: Overall site safety score and compliance indicators
  - **Operational Status**: Equipment utilization and site activity levels

#### **7. Navigation Integration and Quick Actions**
- **Integrated Navigation**:
  - **Live View Access**: Direct navigation to multi-camera monitoring
  - **Street View Integration**: GPS-guided site inspection workflows
  - **Path Administration**: Route planning and inspection path creation
  - **Alert Center Access**: Quick access to alert management systems

### **Interactive Elements**
- **Map Interaction**: Click, drag, zoom, select with multi-touch support
- **Entity Selection**: Individual and bulk selection with visual feedback
- **Drawing Tools**: Interactive zone creation with real-time preview
- **Modal Systems**: Camera preview, zone management, configuration dialogs
- **Layer Controls**: Toggle visibility and manage display options
- **Quick Actions**: Context-sensitive actions based on selected entities

---

## 🗃️ **Database Requirements**

### **📚 Database Schema Reference**
👉 **See Master Database Schema**: [MASTER_DATABASE_SCHEMA.md](./MASTER_DATABASE_SCHEMA.md)

### **Required Tables for Site Overview**

#### **Core Tables Used:**
1. **`sites`** - Site information, weather conditions, operational metrics
2. **`cameras`** - Camera specifications and capabilities
3. **`site_cameras`** - Camera positioning, field of view, status tracking
4. **`zones`** - Zone definitions, boundaries, safety requirements
5. **`users`** - Personnel information and access permissions
6. **`site_personnel`** - Real-time personnel tracking and status
7. **`equipment`** - Heavy equipment tracking and management (new table needed)
8. **`zone_occupancy`** - Real-time zone occupancy tracking (new table needed)

#### **Site Overview-Specific Data Requirements**

##### **Interactive Map Data with Real-time Updates:**
```sql
-- Comprehensive site overview data
SELECT 
    -- Site information
    s.id, s.name, s.code, s.address,
    s.coordinates as site_coordinates,
    s.weather_condition, s.weather_temp, s.weather_wind,
    s.last_weather_update,
    
    -- Site operational metrics
    s.total_cameras, s.active_cameras, s.offline_cameras,
    s.construction_stage, s.completion_percent,
    s.last_activity_timestamp,
    
    -- Site boundaries for map display
    s.site_boundary_coordinates,
    
    -- Real-time personnel count
    COUNT(DISTINCT sp.id) as current_personnel_count,
    
    -- Active alerts summary
    COUNT(DISTINCT CASE WHEN a.priority = 'critical' AND a.status = 'open' THEN a.id END) as critical_alerts,
    COUNT(DISTINCT CASE WHEN a.priority = 'high' AND a.status = 'open' THEN a.id END) as high_alerts,
    
    -- Equipment summary
    COUNT(DISTINCT e.id) as total_equipment,
    COUNT(DISTINCT CASE WHEN e.status = 'active' THEN e.id END) as active_equipment,
    
    -- Zone summary
    COUNT(DISTINCT z.id) as total_zones,
    COUNT(DISTINCT CASE WHEN zo.current_occupancy >= z.max_occupancy THEN z.id END) as zones_at_capacity

FROM sites s
LEFT JOIN site_personnel sp ON s.id = sp.site_id AND sp.status = 'active'
LEFT JOIN alerts a ON s.id = a.site_id AND a.status = 'open'
LEFT JOIN equipment e ON s.id = e.site_id
LEFT JOIN zones z ON s.id = z.site_id AND z.status = 'active'
LEFT JOIN zone_occupancy zo ON z.id = zo.zone_id
WHERE s.id = ?
GROUP BY s.id;
```

##### **Real-time Camera Positioning and Status:**
```sql
-- Camera overlay data for interactive map
SELECT 
    c.id as camera_id, c.name, c.camera_type,
    c.resolution, c.status as camera_status,
    
    -- Positioning data for map display
    sc.coordinates, sc.elevation,
    sc.orientation_angle, sc.tilt_angle,
    sc.field_of_view, sc.detection_range,
    sc.health_score, sc.last_online,
    
    -- Zone coverage for map overlay
    sc.zone_coverage,
    sc.primary_zone_id,
    z.name as primary_zone_name,
    z.zone_type, z.safety_level,
    
    -- Alert correlation for visual indicators
    COUNT(a.id) as active_alerts_count,
    MAX(CASE 
        WHEN a.priority = 'critical' THEN 4
        WHEN a.priority = 'high' THEN 3  
        WHEN a.priority = 'medium' THEN 2
        WHEN a.priority = 'low' THEN 1
        ELSE 0
    END) as highest_alert_priority,
    
    -- Recent AI detection activity
    COUNT(ad.id) as detections_last_hour,
    AVG(ad.confidence_score) as avg_detection_confidence,
    
    -- Stream availability for preview
    sc.recording_active,
    sc.stream_quality,
    
    -- Field of view calculation for map overlay
    CASE 
        WHEN c.camera_type = 'ptz' THEN 
            JSON_OBJECT(
                'type', 'adjustable',
                'current_angle', sc.orientation_angle,
                'fov_degrees', sc.field_of_view,
                'range_meters', sc.detection_range
            )
        ELSE 
            JSON_OBJECT(
                'type', 'fixed',
                'angle', sc.orientation_angle,
                'fov_degrees', sc.field_of_view,
                'range_meters', sc.detection_range
            )
    END as fov_data

FROM cameras c
JOIN site_cameras sc ON c.id = sc.camera_id
LEFT JOIN zones z ON sc.primary_zone_id = z.id
LEFT JOIN alerts a ON c.id = a.camera_id AND a.status = 'open'
LEFT JOIN ai_detections ad ON c.id = ad.camera_id 
    AND ad.timestamp >= DATE_SUB(NOW(), INTERVAL 1 HOUR)
WHERE sc.site_id = ?
GROUP BY c.id, sc.id, z.id
ORDER BY sc.primary_zone_id, c.name;
```

##### **Zone Management and Occupancy Tracking:**
```sql
-- Zone overlay data with real-time occupancy
SELECT 
    z.id as zone_id, z.name, z.zone_type, z.safety_level,
    z.max_occupancy, z.requires_ppe, z.status,
    z.zone_coordinates, z.access_restrictions,
    
    -- Real-time occupancy data
    COALESCE(zo.current_occupancy, 0) as current_occupancy,
    zo.last_updated as occupancy_last_updated,
    
    -- Personnel breakdown in zone
    COUNT(DISTINCT CASE WHEN sp.current_zone_id = z.id THEN sp.id END) as personnel_in_zone,
    AVG(CASE WHEN sp.current_zone_id = z.id THEN sp.ppe_compliance_score END) as avg_ppe_compliance,
    
    -- Equipment in zone
    COUNT(DISTINCT CASE WHEN e.current_zone_id = z.id THEN e.id END) as equipment_in_zone,
    
    -- Safety metrics
    COUNT(DISTINCT CASE WHEN a.zone_id = z.id AND a.status = 'open' THEN a.id END) as zone_alerts,
    MAX(CASE 
        WHEN a.zone_id = z.id AND a.priority = 'critical' THEN 4
        WHEN a.zone_id = z.id AND a.priority = 'high' THEN 3
        WHEN a.zone_id = z.id AND a.priority = 'medium' THEN 2  
        WHEN a.zone_id = z.id AND a.priority = 'low' THEN 1
        ELSE 0
    END) as highest_zone_alert_priority,
    
    -- Zone coverage by cameras
    COUNT(DISTINCT sc.camera_id) as monitoring_cameras,
    
    -- Access control
    CASE 
        WHEN z.access_restrictions IS NOT NULL THEN
            JSON_EXTRACT(z.access_restrictions, '$.restricted_roles')
        ELSE NULL
    END as restricted_roles,
    
    -- Capacity status
    CASE 
        WHEN COALESCE(zo.current_occupancy, 0) >= z.max_occupancy THEN 'at_capacity'
        WHEN COALESCE(zo.current_occupancy, 0) >= (z.max_occupancy * 0.8) THEN 'near_capacity'
        ELSE 'available'
    END as capacity_status

FROM zones z
LEFT JOIN zone_occupancy zo ON z.id = zo.zone_id
LEFT JOIN site_personnel sp ON z.id = sp.current_zone_id AND sp.status = 'active'
LEFT JOIN equipment e ON z.id = e.current_zone_id
LEFT JOIN alerts a ON z.id = a.zone_id AND a.status = 'open'
LEFT JOIN site_cameras sc ON JSON_CONTAINS(sc.zone_coverage, CAST(z.id AS JSON), '$')
WHERE z.site_id = ? AND z.status = 'active'
GROUP BY z.id, zo.current_occupancy, zo.last_updated
ORDER BY z.zone_type, z.name;
```

##### **Real-time Personnel and Equipment Tracking:**
```sql
-- Personnel positioning for map overlay
SELECT 
    sp.id as personnel_id, sp.user_id,
    u.display_name, u.role, u.avatar_url,
    
    -- Current position and status
    sp.current_coordinates, sp.last_position_update,
    sp.status, sp.shift_start_time,
    sp.ppe_compliance_score, sp.last_ppe_check,
    
    -- Zone context
    sp.current_zone_id, z.name as zone_name,
    z.zone_type, z.safety_level, z.requires_ppe,
    
    -- Safety and compliance
    sp.safety_violations_today, sp.safety_score,
    sp.certifications_valid, sp.training_expiry_date,
    
    -- Activity tracking
    sp.hours_worked_today, sp.break_time_remaining,
    sp.last_activity_type, sp.activity_timestamp,
    
    -- Alert correlation
    COUNT(a.id) as personal_alerts_today,
    
    -- PPE status breakdown
    JSON_OBJECT(
        'hardhat', IF(JSON_EXTRACT(sp.current_ppe_status, '$.hardhat') = true, 1, 0),
        'safety_vest', IF(JSON_EXTRACT(sp.current_ppe_status, '$.safety_vest') = true, 1, 0),
        'boots', IF(JSON_EXTRACT(sp.current_ppe_status, '$.boots') = true, 1, 0),
        'gloves', IF(JSON_EXTRACT(sp.current_ppe_status, '$.gloves') = true, 1, 0),
        'compliance_percentage', sp.ppe_compliance_score
    ) as ppe_detail,
    
    -- Movement tracking
    sp.distance_traveled_today, sp.zones_visited_today

FROM site_personnel sp
JOIN users u ON sp.user_id = u.id
LEFT JOIN zones z ON sp.current_zone_id = z.id
LEFT JOIN alerts a ON sp.user_id = a.investigating_by 
    AND DATE(a.timestamp) = CURRENT_DATE
WHERE sp.site_id = ? 
    AND sp.status = 'active'
    AND sp.last_position_update >= DATE_SUB(NOW(), INTERVAL 30 MINUTE)
GROUP BY sp.id
ORDER BY sp.last_position_update DESC;

-- Equipment positioning for map overlay  
SELECT 
    e.id as equipment_id, e.name, e.equipment_type,
    e.make, e.model, e.serial_number,
    
    -- Current position and status
    e.current_coordinates, e.last_position_update,
    e.status, e.operational_hours_today,
    
    -- Zone context
    e.current_zone_id, z.name as zone_name,
    z.zone_type, z.safety_level,
    
    -- Operational data
    e.fuel_level, e.maintenance_due_date,
    e.operator_id, op.display_name as operator_name,
    
    -- Safety and compliance
    e.safety_inspections_current, e.last_inspection_date,
    e.violation_count_today,
    
    -- Performance metrics
    e.utilization_percentage_today, e.idle_time_today,
    e.distance_moved_today, e.zones_operated_today,
    
    -- Alert correlation
    COUNT(a.id) as equipment_alerts_today

FROM equipment e
LEFT JOIN zones z ON e.current_zone_id = z.id  
LEFT JOIN users op ON e.operator_id = op.id
LEFT JOIN alerts a ON e.id = a.equipment_id 
    AND DATE(a.timestamp) = CURRENT_DATE
WHERE e.site_id = ?
    AND e.status != 'decommissioned'
    AND e.last_position_update >= DATE_SUB(NOW(), INTERVAL 1 HOUR)
GROUP BY e.id
ORDER BY e.equipment_type, e.name;
```

#### **Critical Database Relationships for Site Overview:**
- **Sites ← Site_Cameras**: Camera positioning and field of view visualization
- **Sites ← Zones**: Zone management and safety area definition
- **Sites ← Site_Personnel**: Real-time personnel tracking and safety monitoring
- **Sites ← Equipment**: Heavy equipment tracking and operational status
- **Zones ← Zone_Occupancy**: Real-time capacity monitoring and alerts
- **Users ← Site_Personnel**: Personnel identification and role-based access

---

## 📹 **ZoneMinder Integration**

### **Enhanced Camera Field of View Integration**

#### **1. Camera FOV Visualization with ZoneMinder Data**
```sql
-- Camera field of view calculation with ZoneMinder integration
SELECT 
    m.Id as monitor_id, m.Name, 
    m.Width as resolution_width, m.Height as resolution_height,
    m.Enabled, m.Function,
    
    -- Our camera positioning
    sc.camera_id, sc.coordinates, sc.elevation,
    sc.orientation_angle, sc.tilt_angle, sc.field_of_view,
    
    -- Calculate FOV boundaries for map overlay
    sc.coordinates[0] as center_x,
    sc.coordinates[1] as center_y,
    
    -- FOV polygon calculation (simplified)
    JSON_ARRAY(
        JSON_ARRAY(
            sc.coordinates[0] + (sc.detection_range * COS(RADIANS(sc.orientation_angle - sc.field_of_view/2)) / 111320),
            sc.coordinates[1] + (sc.detection_range * SIN(RADIANS(sc.orientation_angle - sc.field_of_view/2)) / 110540)
        ),
        JSON_ARRAY(
            sc.coordinates[0] + (sc.detection_range * COS(RADIANS(sc.orientation_angle + sc.field_of_view/2)) / 111320), 
            sc.coordinates[1] + (sc.detection_range * SIN(RADIANS(sc.orientation_angle + sc.field_of_view/2)) / 110540)
        ),
        sc.coordinates
    ) as fov_polygon_coordinates,
    
    -- Live stream availability
    CASE 
        WHEN m.Enabled = 1 AND m.Function != 'None' THEN
            CONCAT('${zmBaseUrl}/zm/cgi-bin/nph-zms?mode=jpeg&scale=50&maxfps=5&monitor=', m.Id)
        ELSE NULL
    END as preview_stream_url,
    
    -- Recent activity from ZoneMinder
    COUNT(e.Id) as events_last_hour,
    MAX(e.Score) as highest_event_score,
    MAX(e.StartTime) as last_event_time

FROM Monitors m
JOIN site_cameras sc ON m.Id = sc.zoneminder_monitor_id
LEFT JOIN Events e ON m.Id = e.MonitorId 
    AND e.StartTime >= DATE_SUB(NOW(), INTERVAL 1 HOUR)
WHERE sc.site_id = ?
GROUP BY m.Id, sc.id
ORDER BY sc.primary_zone_id, m.Name;
```

#### **2. Live Stream Preview Integration**
```javascript
class SiteOverviewZMIntegration {
    constructor(zmBaseUrl, authToken) {
        this.zmBaseUrl = zmBaseUrl;
        this.authToken = authToken;
        this.activePreviewStreams = new Map();
    }
    
    async initializeCameraPreviewModal(cameraId) {
        try {
            // Get camera and monitor information
            const cameraData = await this.getCameraData(cameraId);
            if (!cameraData.zoneminder_monitor_id) {
                throw new Error('Camera not integrated with ZoneMinder');
            }
            
            // Generate preview stream URLs
            const streamUrls = {
                low_quality: `${this.zmBaseUrl}/zm/cgi-bin/nph-zms?mode=jpeg&scale=25&maxfps=5&monitor=${cameraData.zoneminder_monitor_id}`,
                medium_quality: `${this.zmBaseUrl}/zm/cgi-bin/nph-zms?mode=jpeg&scale=50&maxfps=10&monitor=${cameraData.zoneminder_monitor_id}`,
                high_quality: `${this.zmBaseUrl}/zm/cgi-bin/nph-zms?mode=jpeg&scale=100&maxfps=15&monitor=${cameraData.zoneminder_monitor_id}`,
                snapshot: `${this.zmBaseUrl}/zm/cgi-bin/zms?mode=single&monitor=${cameraData.zoneminder_monitor_id}&scale=100`
            };
            
            // Create preview modal with live stream
            const previewModal = this.createPreviewModal(cameraData, streamUrls);
            
            // Start stream monitoring
            this.activePreviewStreams.set(cameraId, {
                monitorId: cameraData.zoneminder_monitor_id,
                streamUrl: streamUrls.medium_quality,
                startTime: Date.now()
            });
            
            return previewModal;
            
        } catch (error) {
            console.error(`Camera preview initialization failed: ${error.message}`);
            return null;
        }
    }
    
    async updateCameraStatusOnMap() {
        try {
            // Get all monitor statuses from ZoneMinder
            const monitorsResponse = await fetch(`${this.zmBaseUrl}/zm/api/monitors.json`, {
                headers: { 'Authorization': `Bearer ${this.authToken}` }
            });
            
            if (!monitorsResponse.ok) {
                throw new Error('Failed to fetch monitor statuses');
            }
            
            const monitorsData = await monitorsResponse.json();
            const statusUpdates = {};
            
            // Process each monitor status
            monitorsData.monitors.forEach(monitor => {
                const lastWriteTime = new Date(monitor.LastWrite);
                const timeSinceLastWrite = (Date.now() - lastWriteTime.getTime()) / 1000;
                
                let status = 'offline';
                if (monitor.Enabled && timeSinceLastWrite < 60) {
                    status = 'online';
                } else if (monitor.Enabled && timeSinceLastWrite < 300) {
                    status = 'degraded';
                } else if (!monitor.Enabled) {
                    status = 'disabled';
                }
                
                statusUpdates[monitor.Id] = {
                    status: status,
                    lastActivity: monitor.LastWrite,
                    function: monitor.Function,
                    enabled: monitor.Enabled
                };
            });
            
            // Update camera markers on map
            await this.broadcastCameraStatusUpdates(statusUpdates);
            
            return statusUpdates;
            
        } catch (error) {
            console.error(`Camera status update failed: ${error.message}`);
            return {};
        }
    }
    
    async generateFOVOverlayData(siteId) {
        try {
            // Get all cameras for site with FOV data
            const cameras = await this.getSiteCamerasWithFOV(siteId);
            const fovOverlays = [];
            
            for (const camera of cameras) {
                // Calculate field of view polygon
                const fovPolygon = this.calculateFOVPolygon(
                    camera.coordinates,
                    camera.orientation_angle,
                    camera.field_of_view,
                    camera.detection_range
                );
                
                fovOverlays.push({
                    camera_id: camera.camera_id,
                    camera_name: camera.name,
                    fov_polygon: fovPolygon,
                    coverage_color: this.getFOVColor(camera.camera_type, camera.status),
                    coverage_opacity: camera.status === 'online' ? 0.3 : 0.1,
                    show_fov: camera.status === 'online'
                });
            }
            
            return fovOverlays;
            
        } catch (error) {
            console.error(`FOV overlay generation failed: ${error.message}`);
            return [];
        }
    }
    
    calculateFOVPolygon(centerCoords, orientation, fovDegrees, range) {
        const centerLon = centerCoords[0];
        const centerLat = centerCoords[1];
        
        // Convert range from meters to approximate degrees
        const rangeDegLon = range / 111320; // meters to degrees longitude
        const rangeDegLat = range / 110540; // meters to degrees latitude
        
        // Calculate FOV boundary points
        const halfFOV = fovDegrees / 2;
        const leftAngle = orientation - halfFOV;
        const rightAngle = orientation + halfFOV;
        
        const leftPoint = [
            centerLon + (rangeDegLon * Math.cos(this.degreesToRadians(leftAngle))),
            centerLat + (rangeDegLat * Math.sin(this.degreesToRadians(leftAngle)))
        ];
        
        const rightPoint = [
            centerLon + (rangeDegLon * Math.cos(this.degreesToRadians(rightAngle))),
            centerLat + (rangeDegLat * Math.sin(this.degreesToRadians(rightAngle)))
        ];
        
        return [centerCoords, leftPoint, rightPoint, centerCoords];
    }
}
```

---

## 🤖 **AI/YOLO Integration (Roboflow)**

### **Real-time Site Activity Analysis**

#### **1. Site-Wide AI Monitoring Integration**
```python
class SiteOverviewAIIntegration:
    def __init__(self, person_detector, equipment_detector, db_connection):
        self.person_detector = person_detector
        self.equipment_detector = equipment_detector
        self.db = db_connection
        
    async def process_site_overview_ai_updates(self, site_id):
        """Generate real-time AI data for site overview map"""
        try:
            # Get all active cameras for site
            cameras = await self.get_active_site_cameras(site_id)
            
            site_ai_overview = {
                "site_id": site_id,
                "timestamp": datetime.utcnow().isoformat(),
                "camera_analysis": [],
                "zone_analysis": {},
                "personnel_tracking": [],
                "equipment_tracking": [],
                "safety_overview": {
                    "total_personnel": 0,
                    "ppe_compliant_personnel": 0,
                    "safety_violations": 0,
                    "zones_at_risk": [],
                    "overall_safety_score": 100
                }
            }
            
            # Process each active camera
            for camera in cameras:
                camera_ai_data = await self.process_camera_for_overview(camera)
                if camera_ai_data:
                    site_ai_overview["camera_analysis"].append(camera_ai_data)
                    
                    # Aggregate personnel data for map overlay
                    for person in camera_ai_data.get("personnel_detected", []):
                        site_ai_overview["personnel_tracking"].append({
                            "person_id": person["track_id"],
                            "camera_id": camera["camera_id"],
                            "position_estimate": self.estimate_world_coordinates(
                                person["bbox"], camera["coordinates"], camera["field_of_view"]
                            ),
                            "ppe_compliance": person["ppe_compliance"],
                            "zone_id": camera["primary_zone_id"],
                            "confidence": person["confidence"]
                        })
                    
                    # Aggregate equipment data
                    for equipment in camera_ai_data.get("equipment_detected", []):
                        site_ai_overview["equipment_tracking"].append({
                            "equipment_id": equipment["track_id"],
                            "equipment_type": equipment["type"],
                            "camera_id": camera["camera_id"],
                            "position_estimate": self.estimate_world_coordinates(
                                equipment["bbox"], camera["coordinates"], camera["field_of_view"]
                            ),
                            "zone_id": camera["primary_zone_id"],
                            "operational_status": equipment["status"],
                            "confidence": equipment["confidence"]
                        })
            
            # Generate zone-level analysis
            site_ai_overview["zone_analysis"] = await self.analyze_zones_with_ai_data(
                site_id, site_ai_overview["personnel_tracking"], site_ai_overview["equipment_tracking"]
            )
            
            # Calculate overall safety metrics
            site_ai_overview["safety_overview"] = self.calculate_site_safety_overview(site_ai_overview)
            
            # Update real-time tracking tables
            await self.update_personnel_positions(site_ai_overview["personnel_tracking"])
            await self.update_equipment_positions(site_ai_overview["equipment_tracking"])
            await self.update_zone_occupancy(site_ai_overview["zone_analysis"])
            
            # Broadcast to site overview interface
            await self.broadcast_site_overview_update(site_ai_overview)
            
            return site_ai_overview
            
        except Exception as e:
            logger.error(f"Site overview AI processing failed: {str(e)}")
            return None
    
    async def process_camera_for_overview(self, camera):
        """Process individual camera for site overview integration"""
        try:
            # Get latest frame
            frame = await self.get_camera_frame(camera["camera_id"])
            if frame is None:
                return None
            
            # Run AI detection optimized for overview
            person_results = await self.person_detector.detect_persons(
                frame,
                confidence_threshold=0.75,  # Higher threshold for reliability
                enable_tracking=True  # Enable person tracking
            )
            
            equipment_results = await self.equipment_detector.detect_equipment(
                frame,
                equipment_types=['excavator', 'crane', 'truck', 'forklift'],
                confidence_threshold=0.7
            )
            
            # PPE analysis for detected persons
            ppe_analysis = []
            if person_results["person_count"] > 0:
                person_crops = self.extract_person_crops(frame, person_results["bounding_boxes"])
                ppe_analysis = await self.ppe_detector.detect_ppe_compliance(person_crops)
            
            return {
                "camera_id": camera["camera_id"],
                "camera_name": camera["name"],
                "zone_id": camera["primary_zone_id"],
                "timestamp": datetime.utcnow().isoformat(),
                
                # Personnel detection for map overlay
                "personnel_detected": [
                    {
                        "track_id": f"person_{i}_{camera['camera_id']}",
                        "bbox": bbox,
                        "confidence": bbox["confidence"],
                        "ppe_compliance": ppe_analysis[i]["compliance_score"] if i < len(ppe_analysis) else 0,
                        "ppe_violations": ppe_analysis[i]["violations"] if i < len(ppe_analysis) else [],
                        "activity": self.classify_person_activity(bbox, frame)
                    }
                    for i, bbox in enumerate(person_results["bounding_boxes"])
                ],
                
                # Equipment detection for map overlay
                "equipment_detected": [
                    {
                        "track_id": f"equipment_{i}_{camera['camera_id']}",
                        "type": equipment_results["equipment_types"][i] if i < len(equipment_results["equipment_types"]) else "unknown",
                        "bbox": bbox,
                        "confidence": bbox["confidence"],
                        "status": self.classify_equipment_status(bbox, frame)
                    }
                    for i, bbox in enumerate(equipment_results["bounding_boxes"])
                ],
                
                # Zone context
                "zone_safety_assessment": self.assess_zone_safety(
                    person_results, equipment_results, ppe_analysis, camera
                )
            }
            
        except Exception as e:
            logger.error(f"Camera AI processing failed for {camera['camera_id']}: {str(e)}")
            return None
    
    def estimate_world_coordinates(self, bbox, camera_coords, camera_fov):
        """Estimate real-world coordinates from camera detection"""
        # Simplified coordinate estimation (would need camera calibration in production)
        bbox_center_x = (bbox["x"] + bbox["width"] / 2) / 100  # Normalize to 0-1
        bbox_center_y = (bbox["y"] + bbox["height"] / 2) / 100
        
        # Estimate position relative to camera
        # This is a simplified calculation - real implementation would need:
        # - Camera calibration matrix
        # - Ground plane detection
        # - Stereo vision or depth estimation
        
        estimated_distance = 50  # meters (would be calculated from bbox size)
        angle_offset = (bbox_center_x - 0.5) * camera_fov  # Horizontal angle from center
        
        # Convert to approximate world coordinates
        estimated_coords = [
            camera_coords[0] + (estimated_distance * math.cos(math.radians(angle_offset)) / 111320),
            camera_coords[1] + (estimated_distance * math.sin(math.radians(angle_offset)) / 110540)
        ]
        
        return estimated_coords
```

#### **2. Zone-Level AI Analysis**
```json
{
  "zone_ai_analysis": {
    "zone_id": "zone_001",
    "zone_name": "Main Construction Area",
    "analysis_timestamp": "2025-01-12T14:30:15Z",
    
    "occupancy_analysis": {
      "current_personnel": 8,
      "max_capacity": 12,
      "capacity_utilization": 67,
      "personnel_distribution": [
        {
          "person_track_id": "person_1_cam_001",
          "estimated_position": [55.2744, 25.1972],
          "ppe_compliance": 92.5,
          "activity": "working",
          "zone_entry_time": "2025-01-12T14:15:00Z"
        }
      ]
    },
    
    "equipment_presence": {
      "active_equipment": 2,
      "equipment_list": [
        {
          "equipment_track_id": "equipment_1_cam_002", 
          "equipment_type": "excavator",
          "estimated_position": [55.2746, 25.1973],
          "operational_status": "active",
          "safety_clearance": "adequate"
        }
      ]
    },
    
    "safety_assessment": {
      "overall_risk_level": "medium",
      "ppe_compliance_rate": 87.5,
      "safety_violations": [
        {
          "violation_type": "missing_hardhat",
          "person_id": "person_3_cam_001",
          "severity": "high",
          "position": [55.2745, 25.1971]
        }
      ],
      "equipment_safety": {
        "proximity_warnings": 1,
        "operational_violations": 0
      }
    },
    
    "productivity_metrics": {
      "activity_level": "high",
      "personnel_utilization": 85,
      "equipment_utilization": 90,
      "estimated_progress": "on_schedule"
    },
    
    "recommendations": [
      "Deploy supervisor to address PPE violation",
      "Monitor equipment proximity to personnel", 
      "Zone capacity allows for 4 additional personnel"
    ]
  }
}
```

---

## 🔗 **Backend API Requirements**

### **Required Endpoints**

#### **1. Site Overview Data API**
```http
GET /api/site-overview/{site_id}?include=cameras,zones,personnel,equipment,weather

Response:
{
  "site": {
    "id": "site_001",
    "name": "Downtown Plaza Project",
    "code": "DTP-001",
    "coordinates": [55.2744, 25.1972],
    "site_boundary": {
      "type": "Polygon",
      "coordinates": [[[55.2740, 25.1970], [55.2748, 25.1970], [55.2748, 25.1975], [55.2740, 25.1975], [55.2740, 25.1970]]]
    },
    
    "operational_status": {
      "total_cameras": 12,
      "active_cameras": 11,
      "offline_cameras": 1,
      "total_zones": 8,
      "zones_at_capacity": 0,
      "current_personnel": 45,
      "total_equipment": 6,
      "active_equipment": 5
    },
    
    "weather_conditions": {
      "temperature": 72,
      "wind_speed": "8 mph",
      "condition": "Partly Cloudy",
      "visibility": "Good",
      "work_suitability": "Optimal",
      "last_updated": "2025-01-12T14:25:00Z"
    },
    
    "safety_summary": {
      "active_alerts": 3,
      "critical_alerts": 1,
      "overall_safety_score": 87.5,
      "ppe_compliance_rate": 92.0,
      "zones_with_violations": 2
    }
  },
  
  "cameras": [
    {
      "id": "cam_001",
      "name": "Main Entrance Gate",
      "type": "fixed",
      "status": "online",
      "coordinates": [55.2744, 25.1972],
      "field_of_view": {
        "angle": 65,
        "orientation": 45,
        "range": 100,
        "fov_polygon": [[55.2744, 25.1972], [55.2750, 25.1975], [55.2750, 25.1968], [55.2744, 25.1972]]
      },
      "zone_coverage": ["zone_001", "zone_002"],
      "active_alerts": 2,
      "preview_available": true,
      "health_score": 9.2
    }
  ],
  
  "zones": [
    {
      "id": "zone_001",
      "name": "Main Construction Area",
      "type": "work_area", 
      "safety_level": "medium",
      "zone_coordinates": [[55.2742, 25.1970], [55.2746, 25.1970], [55.2746, 25.1974], [55.2742, 25.1974]],
      "occupancy": {
        "current": 8,
        "maximum": 12,
        "capacity_status": "available"
      },
      "requires_ppe": true,
      "monitoring_cameras": 3,
      "active_alerts": 1
    }
  ],
  
  "personnel": [
    {
      "id": "person_001",
      "name": "John Mitchell", 
      "role": "Site Supervisor",
      "current_position": [55.2745, 25.1973],
      "current_zone": "zone_001",
      "status": "working",
      "ppe_compliance": 95,
      "safety_score": 9.8,
      "last_position_update": "2025-01-12T14:29:00Z"
    }
  ],
  
  "equipment": [
    {
      "id": "equipment_001",
      "name": "EX-001",
      "type": "excavator",
      "current_position": [55.2747, 25.1971],
      "current_zone": "zone_002", 
      "status": "active",
      "operator": "Mike Rodriguez",
      "fuel_level": 75,
      "last_position_update": "2025-01-12T14:28:30Z"
    }
  ]
}
```

#### **2. Interactive Zone Management API**
```http
POST /api/site-overview/{site_id}/zones

Request:
{
  "name": "New Safety Zone",
  "type": "safety",
  "safety_level": "high",
  "max_occupancy": 6,
  "requires_ppe": true,
  "zone_coordinates": [
    [55.2743, 25.1971],
    [55.2747, 25.1971], 
    [55.2747, 25.1975],
    [55.2743, 25.1975]
  ],
  "access_restrictions": {
    "restricted_roles": ["visitor", "contractor"],
    "time_restrictions": ["night_shift"]
  },
  "required_ppe": ["hardhat", "safety_vest", "boots"]
}

Response:
{
  "success": true,
  "zone": {
    "id": "zone_009",
    "name": "New Safety Zone",
    "type": "safety",
    "safety_level": "high",
    "status": "active",
    "created_at": "2025-01-12T14:30:15Z",
    "zone_area_sqm": 450,
    "monitoring_cameras": [],
    "initial_occupancy": 0
  },
  "map_update": {
    "zone_overlay_data": {
      "coordinates": [...],
      "color": "#fbbf24",
      "border_color": "#f59e0b",
      "opacity": 0.3
    }
  }
}

PUT /api/site-overview/zones/{zone_id}

Request:
{
  "name": "Updated Zone Name",
  "max_occupancy": 8,
  "zone_coordinates": [...]
}

Response:
{
  "success": true,
  "zone": {...},
  "map_update": {...}
}

DELETE /api/site-overview/zones/{zone_id}

Response:
{
  "success": true,
  "message": "Zone deleted successfully",
  "affected_cameras": ["cam_001", "cam_002"],
  "personnel_relocated": 3
}
```

#### **3. Real-time Position Tracking API**
```http
GET /api/site-overview/{site_id}/live-positions?types=personnel,equipment&last_update={timestamp}

Response:
{
  "position_updates": [
    {
      "entity_type": "personnel",
      "entity_id": "person_001",
      "position": [55.2745, 25.1973],
      "zone_id": "zone_001",
      "timestamp": "2025-01-12T14:30:15Z",
      "movement_vector": {
        "speed": 1.2,
        "direction": 45,
        "destination_estimate": "zone_002"
      },
      "status_change": {
        "previous_status": "moving",
        "current_status": "working",
        "change_timestamp": "2025-01-12T14:29:45Z"
      }
    },
    {
      "entity_type": "equipment", 
      "entity_id": "equipment_001",
      "position": [55.2747, 25.1971],
      "zone_id": "zone_002",
      "timestamp": "2025-01-12T14:30:10Z",
      "operational_data": {
        "fuel_level": 74,
        "engine_hours": 3.2,
        "operator_id": "person_003"
      }
    }
  ],
  "zone_occupancy_changes": [
    {
      "zone_id": "zone_001",
      "previous_count": 7,
      "current_count": 8,
      "capacity_status": "available",
      "last_entry": {
        "entity_id": "person_005",
        "entry_time": "2025-01-12T14:29:30Z"
      }
    }
  ],
  "next_update_eta": 30
}

POST /api/site-overview/{site_id}/bulk-actions

Request:
{
  "action_type": "monitor_selected",
  "entity_selections": [
    {"type": "camera", "ids": ["cam_001", "cam_002", "cam_003"]},
    {"type": "zone", "ids": ["zone_001", "zone_002"]}
  ],
  "action_parameters": {
    "monitoring_priority": "high",
    "alert_threshold": "medium",
    "notification_enabled": true
  }
}

Response:
{
  "success": true,
  "actions_processed": 5,
  "results": [
    {
      "entity_type": "camera",
      "entity_id": "cam_001", 
      "action_result": "monitoring_enabled",
      "new_status": "high_priority_monitoring"
    }
  ],
  "monitoring_session_id": "monitor_session_123"
}
```

#### **4. Map Interaction API**
```http
GET /api/site-overview/{site_id}/map-layers?view_mode=satellite&zoom_level=100&bbox=[lon1,lat1,lon2,lat2]

Response:
{
  "base_layer": {
    "type": "satellite",
    "imagery_url": "/api/map-tiles/satellite/{z}/{x}/{y}.jpg",
    "last_updated": "2025-01-12T14:00:00Z"
  },
  
  "camera_layer": {
    "markers": [
      {
        "camera_id": "cam_001",
        "position": [55.2744, 25.1972],
        "marker_type": "camera_online",
        "marker_color": "#10b981",
        "fov_display": true,
        "fov_polygon": [...],
        "popup_data": {
          "title": "Main Entrance Gate",
          "status": "Online",
          "alerts": 2,
          "preview_url": "/api/camera/cam_001/preview"
        }
      }
    ]
  },
  
  "zone_layer": {
    "overlays": [
      {
        "zone_id": "zone_001",
        "polygon": [...],
        "fill_color": "rgba(59, 130, 246, 0.3)",
        "border_color": "#3b82f6",
        "interactive": true,
        "popup_data": {
          "title": "Main Construction Area",
          "occupancy": "8/12",
          "safety_level": "medium"
        }
      }
    ]
  },
  
  "personnel_layer": {
    "markers": [...] 
  },
  
  "equipment_layer": {
    "markers": [...]
  }
}

POST /api/site-overview/{site_id}/export

Request:
{
  "export_format": "json",
  "include_layers": ["cameras", "zones", "personnel", "equipment"],
  "date_range": {
    "start": "2025-01-12T00:00:00Z",
    "end": "2025-01-12T23:59:59Z"
  },
  "export_options": {
    "include_position_history": true,
    "include_zone_boundaries": true,
    "include_camera_fov": true
  }
}

Response:
{
  "export_id": "export_123456789",
  "status": "processing",
  "estimated_completion": "2025-01-12T14:35:00Z", 
  "file_size_estimate": "15.2 MB",
  "download_url": null
}
```

---

## ⚠️ **Identified Defects & Missing Features**

### **Database Gaps**
1. **Equipment Tracking Table**: Missing dedicated `equipment` table for heavy equipment positioning
2. **Zone Occupancy Table**: Missing `zone_occupancy` table for real-time capacity tracking
3. **Position History**: No historical position tracking for personnel and equipment movement analysis
4. **Zone Access Control**: Missing granular access control and time-based restrictions
5. **Equipment Maintenance**: No maintenance tracking integration with positioning data

### **Real-time Integration Gaps**  
1. **Position Accuracy**: No GPS/beacon integration for precise personnel positioning
2. **Movement Prediction**: Missing predictive algorithms for personnel and equipment movement
3. **Collision Detection**: No proximity warning system for personnel and equipment safety
4. **Zone Boundary Enforcement**: Missing automated zone violation detection and alerts

### **Visualization and UX Gaps**
1. **Mobile Optimization**: Limited mobile device support for field operations
2. **Offline Capability**: No offline map functionality for network-limited environments
3. **AR Integration**: Missing augmented reality overlay capabilities for field inspections
4. **Custom Map Tiles**: No support for custom site blueprints and engineering drawings

---

## 🔧 **COMPLETE FIXED SITE OVERVIEW INTEGRATION**

### **1. ✅ FIXED: Equipment Tracking System**

#### **New equipment Table**
```sql
CREATE TABLE equipment (
    id UUID PRIMARY KEY,
    site_id UUID NOT NULL,
    
    -- Equipment identification
    name VARCHAR(255) NOT NULL,
    equipment_type ENUM('excavator', 'crane', 'truck', 'forklift', 'bulldozer', 'loader', 'compactor', 'generator') NOT NULL,
    make VARCHAR(100),
    model VARCHAR(100),
    serial_number VARCHAR(100),
    asset_tag VARCHAR(50),
    
    -- Current status and position
    status ENUM('active', 'idle', 'maintenance', 'offline', 'decommissioned') DEFAULT 'idle',
    current_coordinates POINT,
    current_zone_id UUID,
    last_position_update TIMESTAMP,
    
    -- Operational data
    operator_id UUID, -- Current operator
    fuel_level DECIMAL(5,2), -- Percentage
    engine_hours_total DECIMAL(10,2),
    engine_hours_today DECIMAL(8,2),
    operational_hours_today DECIMAL(8,2),
    
    -- Maintenance and compliance
    last_inspection_date DATE,
    maintenance_due_date DATE,
    safety_inspections_current BOOLEAN DEFAULT TRUE,
    certification_expiry_date DATE,
    
    -- Performance metrics
    utilization_percentage_today DECIMAL(5,2),
    idle_time_today DECIMAL(8,2),
    distance_moved_today DECIMAL(10,2), -- In meters
    zones_operated_today JSON, -- Array of zone IDs
    
    -- Safety tracking
    violation_count_today INT DEFAULT 0,
    safety_score DECIMAL(3,1), -- 1-10 rating
    proximity_alerts_today INT DEFAULT 0,
    
    -- Technical specifications
    specifications JSON, -- Weight, dimensions, capacity, etc.
    
    FOREIGN KEY (site_id) REFERENCES sites(id),
    FOREIGN KEY (current_zone_id) REFERENCES zones(id),
    FOREIGN KEY (operator_id) REFERENCES users(id),
    
    INDEX idx_equipment_site_status (site_id, status),
    INDEX idx_equipment_zone (current_zone_id),
    INDEX idx_equipment_operator (operator_id),
    INDEX idx_equipment_position_update (last_position_update DESC),
    SPATIAL INDEX idx_equipment_coordinates (current_coordinates)
);
```

#### **Enhanced Zone Occupancy Tracking**
```sql
CREATE TABLE zone_occupancy (
    id UUID PRIMARY KEY,
    zone_id UUID NOT NULL,
    
    -- Current occupancy data
    current_occupancy INT DEFAULT 0,
    personnel_count INT DEFAULT 0,
    equipment_count INT DEFAULT 0,
    visitor_count INT DEFAULT 0,
    
    -- Capacity status
    max_capacity INT,
    capacity_utilization_percentage DECIMAL(5,2),
    capacity_status ENUM('available', 'near_capacity', 'at_capacity', 'over_capacity') DEFAULT 'available',
    
    -- Safety metrics
    avg_ppe_compliance DECIMAL(5,2),
    safety_violations_active INT DEFAULT 0,
    emergency_exits_clear BOOLEAN DEFAULT TRUE,
    
    -- Activity tracking
    entry_count_today INT DEFAULT 0,
    exit_count_today INT DEFAULT 0,
    peak_occupancy_today INT DEFAULT 0,
    peak_occupancy_time TIME,
    
    -- Time tracking
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_entry_time TIMESTAMP,
    last_exit_time TIMESTAMP,
    
    -- Detailed occupancy breakdown
    occupancy_details JSON, -- Detailed breakdown by role, equipment type, etc.
    
    FOREIGN KEY (zone_id) REFERENCES zones(id),
    
    UNIQUE KEY unique_zone_occupancy (zone_id),
    INDEX idx_zone_occupancy_capacity (capacity_status),
    INDEX idx_zone_occupancy_updated (last_updated DESC)
);
```

### **2. ✅ FIXED: Real-time Position Tracking**
```python
class SiteOverviewPositionTracker:
    def __init__(self, db_connection, websocket_manager):
        self.db = db_connection
        self.websocket = websocket_manager
        self.position_cache = {}
        
    async def update_personnel_position(self, site_id, personnel_updates):
        """Update personnel positions with zone detection"""
        try:
            for update in personnel_updates:
                personnel_id = update["personnel_id"]
                new_position = update["position"]
                timestamp = update["timestamp"]
                
                # Determine current zone
                current_zone = await self.detect_zone_from_position(site_id, new_position)
                previous_zone = self.position_cache.get(f"personnel_{personnel_id}", {}).get("zone_id")
                
                # Update personnel position
                await self.db.execute("""
                    UPDATE site_personnel 
                    SET current_coordinates = POINT(?, ?),
                        current_zone_id = ?,
                        last_position_update = ?,
                        status = ?,
                        distance_traveled_today = distance_traveled_today + ?
                    WHERE id = ? AND site_id = ?
                """, [
                    new_position[0], new_position[1],
                    current_zone["zone_id"] if current_zone else None,
                    timestamp,
                    update.get("status", "active"),
                    self.calculate_distance_moved(personnel_id, new_position),
                    personnel_id, site_id
                ])
                
                # Handle zone transitions
                if current_zone and current_zone["zone_id"] != previous_zone:
                    await self.handle_zone_transition(
                        "personnel", personnel_id, previous_zone, current_zone["zone_id"]
                    )
                
                # Update cache
                self.position_cache[f"personnel_{personnel_id}"] = {
                    "position": new_position,
                    "zone_id": current_zone["zone_id"] if current_zone else None,
                    "timestamp": timestamp
                }
                
                # Broadcast real-time update
                await self.websocket.broadcast_position_update(site_id, {
                    "type": "personnel_position",
                    "personnel_id": personnel_id,
                    "position": new_position,
                    "zone": current_zone,
                    "timestamp": timestamp
                })
                
        except Exception as e:
            logger.error(f"Personnel position update failed: {str(e)}")
    
    async def update_equipment_position(self, site_id, equipment_updates):
        """Update equipment positions with operational tracking"""
        try:
            for update in equipment_updates:
                equipment_id = update["equipment_id"]
                new_position = update["position"]
                timestamp = update["timestamp"]
                operational_data = update.get("operational_data", {})
                
                # Determine current zone
                current_zone = await self.detect_zone_from_position(site_id, new_position)
                
                # Update equipment position and operational data
                await self.db.execute("""
                    UPDATE equipment 
                    SET current_coordinates = POINT(?, ?),
                        current_zone_id = ?,
                        last_position_update = ?,
                        fuel_level = COALESCE(?, fuel_level),
                        engine_hours_today = COALESCE(?, engine_hours_today),
                        operational_hours_today = COALESCE(?, operational_hours_today),
                        distance_moved_today = distance_moved_today + ?
                    WHERE id = ? AND site_id = ?
                """, [
                    new_position[0], new_position[1],
                    current_zone["zone_id"] if current_zone else None,
                    timestamp,
                    operational_data.get("fuel_level"),
                    operational_data.get("engine_hours"),
                    operational_data.get("operational_hours"),
                    self.calculate_distance_moved(f"equipment_{equipment_id}", new_position),
                    equipment_id, site_id
                ])
                
                # Check for proximity alerts
                await self.check_equipment_proximity_alerts(site_id, equipment_id, new_position)
                
                # Broadcast real-time update
                await self.websocket.broadcast_position_update(site_id, {
                    "type": "equipment_position",
                    "equipment_id": equipment_id,
                    "position": new_position,
                    "zone": current_zone,
                    "operational_data": operational_data,
                    "timestamp": timestamp
                })
                
        except Exception as e:
            logger.error(f"Equipment position update failed: {str(e)}")
    
    async def update_zone_occupancy(self, site_id):
        """Update all zone occupancy counts"""
        try:
            zones_data = await self.db.fetch_all("""
                SELECT 
                    z.id as zone_id, z.max_occupancy,
                    COUNT(DISTINCT sp.id) as personnel_count,
                    COUNT(DISTINCT e.id) as equipment_count,
                    AVG(sp.ppe_compliance_score) as avg_ppe_compliance
                FROM zones z
                LEFT JOIN site_personnel sp ON z.id = sp.current_zone_id 
                    AND sp.status = 'active'
                LEFT JOIN equipment e ON z.id = e.current_zone_id 
                    AND e.status IN ('active', 'idle')
                WHERE z.site_id = ? AND z.status = 'active'
                GROUP BY z.id
            """, [site_id])
            
            occupancy_updates = []
            
            for zone_data in zones_data:
                total_occupancy = zone_data["personnel_count"] + zone_data["equipment_count"]
                utilization = (total_occupancy / zone_data["max_occupancy"]) * 100 if zone_data["max_occupancy"] > 0 else 0
                
                capacity_status = "available"
                if utilization >= 100:
                    capacity_status = "at_capacity"
                elif utilization >= 80:
                    capacity_status = "near_capacity"
                
                # Update zone occupancy
                await self.db.execute("""
                    INSERT INTO zone_occupancy (
                        zone_id, current_occupancy, personnel_count, equipment_count,
                        capacity_utilization_percentage, capacity_status, avg_ppe_compliance,
                        last_updated
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, NOW())
                    ON DUPLICATE KEY UPDATE
                        current_occupancy = VALUES(current_occupancy),
                        personnel_count = VALUES(personnel_count),
                        equipment_count = VALUES(equipment_count),
                        capacity_utilization_percentage = VALUES(capacity_utilization_percentage),
                        capacity_status = VALUES(capacity_status),
                        avg_ppe_compliance = VALUES(avg_ppe_compliance),
                        last_updated = VALUES(last_updated)
                """, [
                    zone_data["zone_id"], total_occupancy, zone_data["personnel_count"],
                    zone_data["equipment_count"], utilization, capacity_status,
                    zone_data["avg_ppe_compliance"]
                ])
                
                occupancy_updates.append({
                    "zone_id": zone_data["zone_id"],
                    "current_occupancy": total_occupancy,
                    "capacity_status": capacity_status,
                    "utilization_percentage": utilization
                })
            
            # Broadcast occupancy updates
            await self.websocket.broadcast_zone_occupancy_update(site_id, occupancy_updates)
            
        except Exception as e:
            logger.error(f"Zone occupancy update failed: {str(e)}")
```

### **3. ✅ FIXED: Enhanced Zone Management**
```sql
-- Enhanced zones table with additional fields
ALTER TABLE zones ADD COLUMN zone_coordinates POLYGON;
ALTER TABLE zones ADD COLUMN access_restrictions JSON;
ALTER TABLE zones ADD COLUMN required_certifications JSON;
ALTER TABLE zones ADD COLUMN time_restrictions JSON;
ALTER TABLE zones ADD COLUMN emergency_exits JSON;

-- Add spatial index for zone boundary queries
CREATE SPATIAL INDEX idx_zones_coordinates ON zones(zone_coordinates);

-- Zone access permissions table
CREATE TABLE zone_access_permissions (
    id UUID PRIMARY KEY,
    zone_id UUID NOT NULL,
    user_id UUID NOT NULL,
    
    -- Permission details
    access_level ENUM('denied', 'restricted', 'full') DEFAULT 'restricted',
    granted_by UUID NOT NULL,
    granted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NULL,
    
    -- Time-based restrictions
    allowed_hours JSON, -- Array of time ranges
    allowed_days JSON, -- Array of weekdays
    
    -- Condition-based access
    required_escort BOOLEAN DEFAULT FALSE,
    escort_user_id UUID,
    ppe_requirements JSON,
    
    -- Audit trail
    last_access_attempt TIMESTAMP,
    access_violations INT DEFAULT 0,
    
    FOREIGN KEY (zone_id) REFERENCES zones(id),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (granted_by) REFERENCES users(id),
    FOREIGN KEY (escort_user_id) REFERENCES users(id),
    
    UNIQUE KEY unique_zone_user_access (zone_id, user_id),
    INDEX idx_zone_access_user (user_id),
    INDEX idx_zone_access_expires (expires_at)
);
```

---

## 📈 **Success Metrics**

- **Real-time Updates**: Position updates delivered within 5 seconds of actual movement
- **Zone Management**: Zone creation and modification completed within 10 seconds
- **Map Performance**: Interactive map responds to user actions within 200ms
- **Data Accuracy**: Personnel and equipment positions accurate within 2 meters
- **Concurrent Users**: Support 20+ simultaneous site overview sessions
- **Zone Occupancy**: Real-time occupancy tracking with 99% accuracy
- **Export Performance**: Site data export completed within 30 seconds for full dataset

---

**Document Created**: 2025-01-12  
**Next Screen**: Personnel Management (/personnel)