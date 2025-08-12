# 🚜 SCREEN ANALYSIS #12: Equipment Dashboard

## 📋 **Document Information**
- **Screen Name**: Equipment Dashboard
- **Route**: `/equipment`
- **Screen Type**: User Portal - Equipment Management & Monitoring
- **Analysis Date**: 2025-01-12
- **Priority**: MEDIUM-HIGH (TIER 2: Enhanced Operations - Phase 2)
- **Implementation Status**: ⏳ Frontend Required, ⏳ Backend Required

---

## 🎯 **Screen Purpose**
The Equipment Dashboard provides comprehensive equipment monitoring, utilization tracking, and maintenance oversight for construction sites. It serves as the central interface for equipment operators, supervisors, and managers to monitor equipment performance, schedule maintenance, track utilization, and manage IoT-connected construction machinery and tools.

---

## 🖥️ **FRONTEND ANALYSIS**

### **Current Implementation Status: ⏳ PARTIALLY IMPLEMENTED**
Admin equipment management exists but user-facing equipment dashboard needs to be created.

### **Required Components for User Dashboard:**
1. **Real-Time Equipment Status Board** - Live status monitoring with health indicators and alerts
2. **Equipment Utilization Analytics** - Real-time and historical utilization tracking and optimization
3. **IoT Sensor Integration Panel** - Live sensor data from connected equipment (fuel, temperature, vibration)
4. **Maintenance Scheduling Interface** - Preventive maintenance tracking and scheduling system
5. **Equipment Location Tracking** - GPS-based equipment location and movement monitoring
6. **Performance Metrics Dashboard** - Efficiency, productivity, and cost analysis
7. **Operator Assignment System** - Equipment assignment and operator management
8. **Alert & Notification Center** - Equipment-related alerts and maintenance notifications

### **Interactive Features Needed:**
- ✅ Real-time equipment health monitoring with color-coded status indicators
- ✅ Interactive equipment location mapping with live GPS tracking
- ✅ Maintenance scheduling with drag-and-drop calendar interface
- ✅ IoT sensor data visualization with charts and trend analysis
- ✅ Equipment reservation and assignment system
- ✅ Mobile-optimized interface for field operators
- ✅ QR code scanning for equipment identification and status updates
- ✅ Voice command integration for hands-free operation updates

### **Key Differences from Admin Screen:**
- **User Focus**: Operational monitoring vs administrative management
- **Real-Time Priority**: Live data and immediate alerts vs historical reporting
- **Field Optimization**: Mobile-first design for on-site use
- **Operator Workflow**: Equipment-centric workflows vs management oversight

---

## 📊 **FUNCTIONAL REQUIREMENTS**

### **F01: Real-Time Equipment Monitoring**
- **Live Status Dashboard**: Real-time equipment status with health indicators and operational state
- **IoT Sensor Integration**: Live data from fuel levels, engine temperature, hydraulic pressure, and vibration sensors
- **Performance Monitoring**: Real-time efficiency tracking, fuel consumption, and operational metrics
- **Alert Management**: Instant notifications for equipment issues, maintenance needs, and safety concerns
- **Geographic Tracking**: GPS-based location tracking with geofencing and movement alerts

### **F02: Equipment Utilization Analytics**
- **Usage Tracking**: Real-time and historical equipment utilization rates and patterns
- **Productivity Analysis**: Equipment productivity metrics, output tracking, and efficiency scoring
- **Cost Management**: Operating cost tracking, fuel consumption analysis, and ROI calculations
- **Comparative Analytics**: Equipment performance comparison and benchmarking
- **Predictive Analytics**: AI-powered usage forecasting and optimization recommendations

### **F03: Maintenance Management System**
- **Preventive Maintenance**: Scheduled maintenance tracking with automated reminders and notifications
- **Work Order Management**: Maintenance request creation, assignment, and tracking
- **Parts Inventory Integration**: Parts availability tracking and automatic reordering
- **Maintenance History**: Complete maintenance records and service documentation
- **Predictive Maintenance**: AI-driven predictive maintenance recommendations based on usage patterns

### **F04: Equipment Assignment & Reservation**
- **Operator Assignment**: Equipment assignment to certified operators with skill verification
- **Reservation System**: Equipment booking and scheduling system with conflict resolution
- **Availability Tracking**: Real-time equipment availability and reservation status
- **Skill Matching**: Automatic matching of equipment with qualified operators
- **Shift Management**: Equipment handover tracking and shift change documentation

### **F05: Field Operations Support**
- **Mobile Interface**: Optimized mobile interface for field operators and supervisors
- **QR Code Integration**: QR code scanning for equipment identification and status updates
- **Voice Commands**: Voice-activated status updates and equipment control
- **Offline Capability**: Offline data collection with sync when connectivity returns
- **Emergency Protocols**: Emergency stop procedures and incident reporting

### **F06: Integration & Automation**
- **IoT Device Management**: Integration with telematics systems and IoT sensors
- **Fleet Management**: Integration with fleet management systems and GPS tracking
- **ERP Integration**: Connection with enterprise resource planning and asset management systems
- **Safety System Integration**: Integration with safety monitoring and compliance systems
- **Third-Party APIs**: Integration with manufacturer APIs and diagnostic systems

---

## 🗃️ **DATABASE REQUIREMENTS**

### **Primary Tables (Existing in Schema):**
Some required tables already exist in `MASTER_DATABASE_SCHEMA.md`:

1. **`users`** - User information for equipment operators and managers
2. **`sites`** - Site information for equipment deployment
3. **`zones`** - Site zones for equipment location and movement tracking

### **New Tables Required:**

#### **`equipment`**
```sql
CREATE TABLE equipment (
    id UUID PRIMARY KEY,
    
    -- Basic equipment information
    equipment_name VARCHAR(255) NOT NULL,
    equipment_code VARCHAR(50) UNIQUE NOT NULL,
    serial_number VARCHAR(100) UNIQUE,
    asset_tag VARCHAR(50) UNIQUE,
    
    -- Classification and categorization
    equipment_type ENUM('excavator', 'crane', 'bulldozer', 'loader', 'dump_truck', 'concrete_mixer', 'generator', 'compressor', 'welding_equipment', 'safety_equipment', 'survey_equipment', 'other') NOT NULL,
    equipment_category VARCHAR(100), -- Heavy Machinery, Power Tools, Safety Equipment
    subcategory VARCHAR(100),
    
    -- Manufacturer and model information
    manufacturer VARCHAR(255) NOT NULL,
    model VARCHAR(255) NOT NULL,
    model_year INT,
    specifications JSON, -- Technical specifications
    
    -- Purchase and ownership
    purchase_date DATE,
    purchase_price DECIMAL(12,2),
    purchase_order_number VARCHAR(100),
    vendor VARCHAR(255),
    
    -- Warranty information
    warranty_start_date DATE,
    warranty_end_date DATE,
    warranty_type ENUM('manufacturer', 'extended', 'service_contract') DEFAULT 'manufacturer',
    warranty_terms TEXT,
    
    -- Current status and location
    current_status ENUM('operational', 'maintenance', 'repair', 'idle', 'retired', 'lost_damaged') DEFAULT 'operational',
    current_site_id UUID,
    current_zone_id UUID,
    current_location_gps JSON, -- {latitude: float, longitude: float, elevation: float}
    
    -- Operator information
    assigned_operator_id UUID,
    certified_operators JSON, -- Array of user IDs certified to operate this equipment
    requires_certification BOOLEAN DEFAULT TRUE,
    certification_level_required ENUM('basic', 'intermediate', 'advanced', 'expert') DEFAULT 'basic',
    
    -- Utilization and performance tracking
    total_operating_hours DECIMAL(10,2) DEFAULT 0,
    operating_hours_limit DECIMAL(10,2), -- Maximum operating hours before major service
    last_operating_date DATE,
    utilization_target_hours_per_day DECIMAL(5,2) DEFAULT 8,
    
    -- Condition and health
    condition_rating ENUM('excellent', 'good', 'fair', 'poor', 'critical') DEFAULT 'good',
    health_score DECIMAL(3,1) DEFAULT 10.0, -- 0-10 health score
    last_inspection_date DATE,
    next_inspection_due DATE,
    
    -- Maintenance scheduling
    maintenance_schedule_type ENUM('hours_based', 'calendar_based', 'condition_based', 'predictive') DEFAULT 'hours_based',
    maintenance_interval_hours DECIMAL(8,2),
    maintenance_interval_days INT,
    last_maintenance_date DATE,
    next_maintenance_due DATE,
    maintenance_overdue_flag BOOLEAN DEFAULT FALSE,
    
    -- Financial tracking
    current_value DECIMAL(12,2),
    depreciation_rate DECIMAL(5,2) DEFAULT 10.00, -- Annual depreciation percentage
    total_maintenance_cost DECIMAL(12,2) DEFAULT 0,
    total_repair_cost DECIMAL(12,2) DEFAULT 0,
    insurance_value DECIMAL(12,2),
    
    -- IoT and connectivity
    iot_device_id VARCHAR(255),
    telematics_enabled BOOLEAN DEFAULT FALSE,
    gps_tracking_enabled BOOLEAN DEFAULT TRUE,
    remote_monitoring_enabled BOOLEAN DEFAULT FALSE,
    connectivity_status ENUM('connected', 'disconnected', 'intermittent') DEFAULT 'disconnected',
    
    -- Safety and compliance
    safety_features JSON, -- Array of safety features
    compliance_certifications JSON, -- Required certifications and inspections
    safety_rating ENUM('high', 'medium', 'low') DEFAULT 'high',
    accident_history_count INT DEFAULT 0,
    
    -- Environmental impact
    fuel_type ENUM('diesel', 'gasoline', 'electric', 'hybrid', 'propane', 'natural_gas') DEFAULT 'diesel',
    emissions_rating VARCHAR(50),
    environmental_compliance JSON,
    
    -- Lifecycle management
    lifecycle_stage ENUM('new', 'active', 'aging', 'end_of_life', 'disposed') DEFAULT 'active',
    replacement_plan_date DATE,
    disposal_date DATE,
    disposal_method VARCHAR(255),
    
    -- Status and metadata
    status ENUM('active', 'inactive', 'archived', 'deleted') DEFAULT 'active',
    notes TEXT,
    created_by UUID NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (current_site_id) REFERENCES sites(id),
    FOREIGN KEY (current_zone_id) REFERENCES zones(id),
    FOREIGN KEY (assigned_operator_id) REFERENCES users(id),
    FOREIGN KEY (created_by) REFERENCES users(id),
    
    INDEX idx_equipment_type_status (equipment_type, current_status),
    INDEX idx_equipment_site_zone (current_site_id, current_zone_id),
    INDEX idx_equipment_operator (assigned_operator_id, current_status),
    INDEX idx_equipment_maintenance (next_maintenance_due, maintenance_overdue_flag),
    INDEX idx_equipment_condition (condition_rating, health_score DESC),
    INDEX idx_equipment_utilization (total_operating_hours DESC, utilization_target_hours_per_day),
    UNIQUE KEY unique_equipment_code (equipment_code),
    UNIQUE KEY unique_serial_number (serial_number),
    UNIQUE KEY unique_asset_tag (asset_tag)
);
```

#### **`equipment_iot_data`**
```sql
CREATE TABLE equipment_iot_data (
    id UUID PRIMARY KEY,
    equipment_id UUID NOT NULL,
    
    -- Data collection information
    timestamp_recorded TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_source VARCHAR(100), -- sensor, telematics, manual, api
    device_id VARCHAR(255),
    
    -- Location data
    gps_latitude DECIMAL(10,7),
    gps_longitude DECIMAL(10,7),
    gps_elevation DECIMAL(6,2),
    gps_accuracy_meters DECIMAL(5,2),
    heading_degrees DECIMAL(6,2), -- 0-360 degrees
    speed_kmh DECIMAL(6,2),
    
    -- Engine and performance data
    engine_hours DECIMAL(8,2),
    engine_rpm INT,
    engine_temperature_celsius DECIMAL(5,2),
    coolant_temperature_celsius DECIMAL(5,2),
    oil_pressure_psi DECIMAL(6,2),
    oil_temperature_celsius DECIMAL(5,2),
    
    -- Fuel and power data
    fuel_level_percentage DECIMAL(5,2), -- 0-100%
    fuel_consumption_rate_lph DECIMAL(6,2), -- Liters per hour
    battery_voltage_volts DECIMAL(6,2),
    alternator_output_volts DECIMAL(6,2),
    
    -- Hydraulic system data
    hydraulic_pressure_psi DECIMAL(8,2),
    hydraulic_oil_temperature_celsius DECIMAL(5,2),
    hydraulic_flow_rate_lpm DECIMAL(8,2), -- Liters per minute
    
    -- Operational data
    operational_status ENUM('idle', 'working', 'traveling', 'maintenance', 'error') DEFAULT 'idle',
    load_percentage DECIMAL(5,2), -- 0-100% current load
    productivity_metric DECIMAL(8,2), -- Equipment-specific productivity measure
    
    -- Environmental data
    ambient_temperature_celsius DECIMAL(5,2),
    humidity_percentage DECIMAL(5,2),
    atmospheric_pressure_hpa DECIMAL(7,2),
    
    -- Vibration and condition monitoring
    vibration_level_mm_s DECIMAL(6,3), -- Vibration in mm/s
    noise_level_db DECIMAL(5,1),
    bearing_temperature_celsius DECIMAL(5,2),
    
    -- Safety and alerts
    safety_systems_status JSON, -- Status of various safety systems
    active_fault_codes JSON, -- Array of active diagnostic fault codes
    warning_lights JSON, -- Status of warning indicators
    
    -- Usage and productivity
    work_cycles_count INT DEFAULT 0, -- Number of work cycles (e.g., bucket loads)
    distance_traveled_km DECIMAL(8,3),
    fuel_consumed_liters DECIMAL(8,3),
    
    -- Data quality and reliability
    data_quality_score DECIMAL(3,1) DEFAULT 10.0, -- 0-10 data quality assessment
    signal_strength_percentage DECIMAL(5,2), -- Connectivity signal strength
    data_completeness_percentage DECIMAL(5,2), -- Percentage of expected data received
    
    -- Processing and analysis
    anomaly_detected BOOLEAN DEFAULT FALSE,
    anomaly_type VARCHAR(100),
    anomaly_confidence DECIMAL(5,2),
    processed_by_ai BOOLEAN DEFAULT FALSE,
    ai_analysis_results JSON,
    
    FOREIGN KEY (equipment_id) REFERENCES equipment(id) ON DELETE CASCADE,
    
    INDEX idx_equipment_iot_equipment_time (equipment_id, timestamp_recorded DESC),
    INDEX idx_equipment_iot_timestamp (timestamp_recorded DESC),
    INDEX idx_equipment_iot_status (operational_status, timestamp_recorded DESC),
    INDEX idx_equipment_iot_location (gps_latitude, gps_longitude, timestamp_recorded DESC),
    INDEX idx_equipment_iot_anomaly (anomaly_detected, anomaly_type),
    INDEX idx_equipment_iot_data_quality (data_quality_score DESC, signal_strength_percentage DESC)
);
```

#### **`maintenance_schedules`**
```sql
CREATE TABLE maintenance_schedules (
    id UUID PRIMARY KEY,
    equipment_id UUID NOT NULL,
    
    -- Schedule identification
    schedule_name VARCHAR(255) NOT NULL,
    schedule_type ENUM('preventive', 'predictive', 'corrective', 'emergency', 'regulatory') NOT NULL,
    maintenance_category ENUM('routine', 'major_service', 'overhaul', 'inspection', 'repair', 'calibration') NOT NULL,
    
    -- Scheduling criteria
    trigger_type ENUM('hours_based', 'calendar_based', 'condition_based', 'usage_based', 'manual') NOT NULL,
    trigger_value DECIMAL(10,2), -- Hours, days, cycles, etc.
    trigger_units ENUM('hours', 'days', 'weeks', 'months', 'cycles', 'kilometers', 'custom') NOT NULL,
    
    -- Timing information
    last_performed TIMESTAMP,
    next_due_date DATE NOT NULL,
    estimated_duration_hours DECIMAL(5,2) DEFAULT 4,
    
    -- Work description
    work_description TEXT NOT NULL,
    required_parts JSON, -- Array of parts with quantities
    required_tools JSON, -- Array of required tools and equipment
    required_skills JSON, -- Array of required technician skills
    
    -- Resource requirements
    estimated_labor_hours DECIMAL(6,2) DEFAULT 4,
    estimated_cost DECIMAL(10,2),
    priority_level ENUM('low', 'medium', 'high', 'critical', 'emergency') DEFAULT 'medium',
    
    -- Safety and compliance
    safety_requirements JSON, -- Required safety procedures and PPE
    regulatory_requirements JSON, -- Compliance and certification requirements
    environmental_considerations TEXT,
    
    -- Scheduling constraints
    requires_downtime BOOLEAN DEFAULT TRUE,
    max_delay_days INT DEFAULT 7, -- Maximum acceptable delay
    seasonal_restrictions JSON, -- Weather or seasonal limitations
    site_constraints JSON, -- Site-specific scheduling constraints
    
    -- Automation and notifications
    auto_create_work_orders BOOLEAN DEFAULT TRUE,
    notification_advance_days INT DEFAULT 7,
    notification_recipients JSON, -- User IDs to notify
    escalation_rules JSON, -- Escalation procedures for overdue maintenance
    
    -- Performance tracking
    completion_rate DECIMAL(5,2) DEFAULT 100.00,
    average_actual_duration_hours DECIMAL(6,2),
    average_actual_cost DECIMAL(10,2),
    effectiveness_score DECIMAL(3,1), -- 0-10 maintenance effectiveness
    
    -- Vendor and contractor information
    preferred_vendor VARCHAR(255),
    vendor_contact_info JSON,
    requires_external_service BOOLEAN DEFAULT FALSE,
    
    -- Documentation requirements
    documentation_required BOOLEAN DEFAULT TRUE,
    photo_documentation_required BOOLEAN DEFAULT TRUE,
    certification_required BOOLEAN DEFAULT FALSE,
    
    -- Status and lifecycle
    status ENUM('active', 'suspended', 'completed', 'cancelled', 'archived') DEFAULT 'active',
    created_by UUID NOT NULL,
    approved_by UUID,
    approved_at TIMESTAMP,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (equipment_id) REFERENCES equipment(id) ON DELETE CASCADE,
    FOREIGN KEY (created_by) REFERENCES users(id),
    FOREIGN KEY (approved_by) REFERENCES users(id),
    
    INDEX idx_maintenance_schedules_equipment (equipment_id, status),
    INDEX idx_maintenance_schedules_due_date (next_due_date, priority_level),
    INDEX idx_maintenance_schedules_type (schedule_type, maintenance_category),
    INDEX idx_maintenance_schedules_trigger (trigger_type, trigger_value),
    INDEX idx_maintenance_schedules_priority (priority_level, next_due_date)
);
```

#### **`equipment_work_orders`**
```sql
CREATE TABLE equipment_work_orders (
    id UUID PRIMARY KEY,
    equipment_id UUID NOT NULL,
    maintenance_schedule_id UUID, -- Links to scheduled maintenance
    
    -- Work order identification
    work_order_number VARCHAR(100) UNIQUE NOT NULL,
    work_order_title VARCHAR(255) NOT NULL,
    work_order_type ENUM('preventive', 'corrective', 'emergency', 'inspection', 'installation', 'modification') NOT NULL,
    
    -- Work description and requirements
    description TEXT NOT NULL,
    work_instructions TEXT,
    safety_instructions TEXT,
    parts_required JSON, -- Array of parts with quantities and part numbers
    tools_required JSON, -- Array of required tools
    
    -- Scheduling and assignment
    requested_by UUID NOT NULL,
    assigned_technician_id UUID,
    assigned_team JSON, -- Array of team member IDs
    priority ENUM('low', 'medium', 'high', 'critical', 'emergency') NOT NULL DEFAULT 'medium',
    
    -- Timing information
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    requested_completion_date DATE,
    scheduled_start_date DATE,
    actual_start_date DATE,
    scheduled_end_date DATE,
    actual_end_date DATE,
    
    -- Status tracking
    status ENUM('created', 'assigned', 'parts_ordered', 'ready', 'in_progress', 'waiting_parts', 'on_hold', 'completed', 'cancelled', 'rejected') DEFAULT 'created',
    completion_percentage DECIMAL(5,2) DEFAULT 0.00,
    
    -- Resource tracking
    estimated_labor_hours DECIMAL(6,2),
    actual_labor_hours DECIMAL(6,2),
    estimated_cost DECIMAL(10,2),
    actual_cost DECIMAL(10,2),
    parts_cost DECIMAL(10,2) DEFAULT 0,
    labor_cost DECIMAL(10,2) DEFAULT 0,
    
    -- Work performed
    work_performed TEXT,
    parts_used JSON, -- Array of parts actually used with quantities
    issues_encountered TEXT,
    resolution_notes TEXT,
    
    -- Quality and inspection
    quality_check_performed BOOLEAN DEFAULT FALSE,
    quality_check_passed BOOLEAN,
    quality_inspector_id UUID,
    inspection_notes TEXT,
    
    -- Documentation and evidence
    before_photos JSON, -- Array of photo file paths
    after_photos JSON, -- Array of photo file paths
    documentation_files JSON, -- Array of document file paths
    test_results JSON, -- Measurement and test results
    
    -- Follow-up and recommendations
    follow_up_required BOOLEAN DEFAULT FALSE,
    follow_up_date DATE,
    recommendations TEXT,
    next_maintenance_due DATE,
    
    -- Approval workflow
    requires_approval BOOLEAN DEFAULT FALSE,
    approved_by UUID,
    approved_at TIMESTAMP,
    approval_notes TEXT,
    
    -- Customer/requester feedback
    requester_satisfied BOOLEAN,
    feedback_rating DECIMAL(2,1), -- 1-5 star rating
    feedback_comments TEXT,
    
    -- Vendor and external service
    vendor_used VARCHAR(255),
    vendor_invoice_number VARCHAR(100),
    warranty_provided BOOLEAN DEFAULT FALSE,
    warranty_duration_days INT,
    
    FOREIGN KEY (equipment_id) REFERENCES equipment(id),
    FOREIGN KEY (maintenance_schedule_id) REFERENCES maintenance_schedules(id),
    FOREIGN KEY (requested_by) REFERENCES users(id),
    FOREIGN KEY (assigned_technician_id) REFERENCES users(id),
    FOREIGN KEY (quality_inspector_id) REFERENCES users(id),
    FOREIGN KEY (approved_by) REFERENCES users(id),
    
    INDEX idx_work_orders_equipment (equipment_id, status),
    INDEX idx_work_orders_technician (assigned_technician_id, status),
    INDEX idx_work_orders_status_priority (status, priority),
    INDEX idx_work_orders_dates (scheduled_start_date, scheduled_end_date),
    INDEX idx_work_orders_type (work_order_type, created_date DESC),
    UNIQUE KEY unique_work_order_number (work_order_number)
);
```

#### **`equipment_utilization_logs`**
```sql
CREATE TABLE equipment_utilization_logs (
    id UUID PRIMARY KEY,
    equipment_id UUID NOT NULL,
    operator_id UUID,
    
    -- Session information
    session_start TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    session_end TIMESTAMP,
    session_duration_hours DECIMAL(6,2),
    session_type ENUM('operational', 'training', 'testing', 'maintenance_run', 'transport') DEFAULT 'operational',
    
    -- Location and project context
    site_id UUID,
    zone_id UUID,
    project_id UUID,
    work_order_id UUID, -- Links to specific work being performed
    
    -- Usage metrics
    engine_hours_start DECIMAL(8,2),
    engine_hours_end DECIMAL(8,2),
    engine_hours_used DECIMAL(6,2),
    idle_time_hours DECIMAL(6,2) DEFAULT 0,
    productive_time_hours DECIMAL(6,2),
    
    -- Productivity measurements
    work_completed_units DECIMAL(10,2), -- Units depend on equipment type
    work_unit_type VARCHAR(50), -- cubic_meters, tons, cycles, etc.
    productivity_rate DECIMAL(8,2), -- Units per hour
    efficiency_percentage DECIMAL(5,2), -- Percentage of theoretical maximum
    
    -- Fuel and energy consumption
    fuel_consumed_liters DECIMAL(8,3),
    fuel_efficiency_lph DECIMAL(6,3), -- Liters per hour
    energy_consumed_kwh DECIMAL(8,3), -- For electric equipment
    
    -- Performance metrics
    average_load_percentage DECIMAL(5,2),
    peak_load_percentage DECIMAL(5,2),
    temperature_max_celsius DECIMAL(5,2),
    pressure_max_psi DECIMAL(8,2),
    
    -- Movement and distance
    distance_traveled_km DECIMAL(8,3),
    number_of_stops INT DEFAULT 0,
    geofence_violations INT DEFAULT 0,
    
    -- Operational conditions
    weather_conditions VARCHAR(100),
    ground_conditions VARCHAR(100),
    operational_difficulty ENUM('easy', 'moderate', 'difficult', 'extreme') DEFAULT 'moderate',
    
    -- Safety and incidents
    safety_incidents INT DEFAULT 0,
    near_miss_events INT DEFAULT 0,
    equipment_alerts INT DEFAULT 0,
    emergency_stops INT DEFAULT 0,
    
    -- Quality and compliance
    ppe_compliance_rate DECIMAL(5,2) DEFAULT 100.00,
    safety_protocol_adherence ENUM('full', 'partial', 'poor', 'violation') DEFAULT 'full',
    environmental_compliance BOOLEAN DEFAULT TRUE,
    
    -- Maintenance indicators
    maintenance_alerts_generated INT DEFAULT 0,
    diagnostic_codes_triggered JSON, -- Array of diagnostic codes
    performance_degradation_detected BOOLEAN DEFAULT FALSE,
    
    -- Session quality and validation
    data_completeness_percentage DECIMAL(5,2) DEFAULT 100.00,
    gps_tracking_quality ENUM('excellent', 'good', 'fair', 'poor') DEFAULT 'good',
    sensor_data_reliability DECIMAL(5,2) DEFAULT 100.00,
    
    -- Cost allocation
    hourly_operating_cost DECIMAL(8,2),
    total_session_cost DECIMAL(10,2),
    fuel_cost DECIMAL(8,2),
    maintenance_cost_allocation DECIMAL(8,2),
    
    -- Notes and observations
    operator_notes TEXT,
    supervisor_notes TEXT,
    issues_reported TEXT,
    recommendations TEXT,
    
    -- Status and validation
    session_validated BOOLEAN DEFAULT FALSE,
    validated_by UUID,
    validated_at TIMESTAMP,
    data_source ENUM('automatic', 'manual', 'hybrid') DEFAULT 'automatic',
    
    FOREIGN KEY (equipment_id) REFERENCES equipment(id),
    FOREIGN KEY (operator_id) REFERENCES users(id),
    FOREIGN KEY (site_id) REFERENCES sites(id),
    FOREIGN KEY (zone_id) REFERENCES zones(id),
    FOREIGN KEY (work_order_id) REFERENCES equipment_work_orders(id),
    FOREIGN KEY (validated_by) REFERENCES users(id),
    
    INDEX idx_utilization_equipment_time (equipment_id, session_start DESC),
    INDEX idx_utilization_operator (operator_id, session_start DESC),
    INDEX idx_utilization_site (site_id, session_start DESC),
    INDEX idx_utilization_productivity (productivity_rate DESC, efficiency_percentage DESC),
    INDEX idx_utilization_duration (session_duration_hours DESC),
    INDEX idx_utilization_validation (session_validated, validated_by)
);
```

### **Schema Updates Required:**
Enhance existing tables with equipment integration:
```sql
-- Add equipment tracking to zones table
ALTER TABLE zones 
ADD COLUMN equipment_count INT DEFAULT 0,
ADD COLUMN equipment_types JSON, -- Array of equipment types typically in this zone
ADD COLUMN equipment_restrictions JSON; -- Equipment access restrictions

-- Add equipment context to users table for operators
ALTER TABLE users
ADD COLUMN equipment_certifications JSON, -- Array of equipment certifications
ADD COLUMN current_equipment_assignment UUID,
ADD COLUMN equipment_operator_level ENUM('trainee', 'operator', 'senior_operator', 'supervisor') DEFAULT 'operator';
```

---

## 🔌 **BACKEND API REQUIREMENTS**

### **API01: Equipment Status & Monitoring**

#### **GET /api/equipment**
```python
@app.get("/api/equipment")
async def get_equipment_list(
    site_id: str = None,
    status: str = None,
    equipment_type: str = None,
    assigned_operator: str = None,
    include_iot_data: bool = False
):
    """Get equipment list with filtering options"""
    return {
        "equipment": [
            {
                "id": str,
                "name": str,
                "type": str,
                "model": str,
                "serial_number": str,
                "current_status": str,
                "location": {
                    "site_id": str,
                    "zone_id": str,
                    "gps_coordinates": dict,
                    "last_updated": str
                },
                "operator": {
                    "id": str,
                    "name": str,
                    "certification_level": str
                },
                "health_metrics": {
                    "health_score": float,
                    "condition_rating": str,
                    "active_alerts": int,
                    "maintenance_due": bool
                },
                "utilization": {
                    "current_utilization": float,
                    "today_hours": float,
                    "efficiency_score": float
                },
                "iot_data": dict  # If include_iot_data=true
            }
        ]
    }
```

#### **GET /api/equipment/{equipment_id}/status**
```python
@app.get("/api/equipment/{equipment_id}/status")
async def get_equipment_real_time_status(equipment_id: str):
    """Get real-time equipment status and metrics"""
    return {
        "equipment_id": str,
        "timestamp": str,
        "operational_status": str,
        "location": {
            "gps_coordinates": dict,
            "site": str,
            "zone": str,
            "heading": float,
            "speed": float
        },
        "engine_metrics": {
            "hours": float,
            "rpm": int,
            "temperature": float,
            "oil_pressure": float
        },
        "fuel_metrics": {
            "level_percentage": float,
            "consumption_rate": float,
            "estimated_remaining_hours": float
        },
        "performance": {
            "load_percentage": float,
            "productivity_score": float,
            "efficiency_rating": float
        },
        "alerts": [
            {
                "type": str,
                "severity": str,
                "message": str,
                "timestamp": str
            }
        ]
    }
```

### **API02: IoT Data Management**

#### **POST /api/equipment/{equipment_id}/iot-data**
```python
@app.post("/api/equipment/{equipment_id}/iot-data")
async def receive_iot_data(
    equipment_id: str,
    iot_data: EquipmentIoTDataRequest
):
    """Receive and process IoT data from equipment"""
    return {
        "received": bool,
        "processed": bool,
        "data_points": int,
        "anomalies_detected": int,
        "alerts_generated": int,
        "next_expected": str
    }
```

#### **GET /api/equipment/{equipment_id}/iot-data/history**
```python
@app.get("/api/equipment/{equipment_id}/iot-data/history")
async def get_iot_data_history(
    equipment_id: str,
    start_time: str,
    end_time: str,
    data_types: List[str] = Query(default=None),
    granularity: str = "hourly"
):
    """Get historical IoT data for equipment"""
    return {
        "equipment_id": str,
        "time_range": dict,
        "data_points": [
            {
                "timestamp": str,
                "engine_data": dict,
                "fuel_data": dict,
                "location_data": dict,
                "performance_data": dict,
                "environmental_data": dict,
                "alerts": [dict]
            }
        ],
        "aggregated_metrics": {
            "avg_fuel_consumption": float,
            "total_operating_hours": float,
            "avg_efficiency": float,
            "alert_frequency": float
        }
    }
```

### **API03: Maintenance Management**

#### **GET /api/equipment/{equipment_id}/maintenance**
```python
@app.get("/api/equipment/{equipment_id}/maintenance")
async def get_equipment_maintenance_schedule(equipment_id: str):
    """Get maintenance schedule and work orders for equipment"""
    return {
        "equipment_id": str,
        "next_maintenance": {
            "due_date": str,
            "type": str,
            "estimated_hours": float,
            "overdue": bool
        },
        "active_work_orders": [
            {
                "id": str,
                "work_order_number": str,
                "type": str,
                "priority": str,
                "status": str,
                "assigned_technician": str,
                "scheduled_date": str
            }
        ],
        "maintenance_history": [
            {
                "date": str,
                "type": str,
                "work_performed": str,
                "cost": float,
                "technician": str
            }
        ]
    }
```

#### **POST /api/equipment/{equipment_id}/maintenance/work-order**
```python
@app.post("/api/equipment/{equipment_id}/maintenance/work-order")
async def create_maintenance_work_order(
    equipment_id: str,
    work_order_data: MaintenanceWorkOrderRequest
):
    """Create new maintenance work order"""
    return {
        "work_order_id": str,
        "work_order_number": str,
        "status": "created",
        "estimated_completion": str,
        "assigned_technician": str
    }
```

### **API04: Utilization Analytics**

#### **GET /api/equipment/{equipment_id}/utilization**
```python
@app.get("/api/equipment/{equipment_id}/utilization")
async def get_equipment_utilization(
    equipment_id: str,
    time_range: str = "30d",
    include_productivity: bool = True
):
    """Get equipment utilization analytics"""
    return {
        "equipment_id": str,
        "time_range": str,
        "utilization_summary": {
            "total_hours": float,
            "productive_hours": float,
            "idle_hours": float,
            "utilization_rate": float,
            "efficiency_score": float
        },
        "daily_utilization": [
            {
                "date": str,
                "total_hours": float,
                "productive_hours": float,
                "efficiency": float,
                "fuel_consumed": float
            }
        ],
        "productivity_metrics": {
            "work_completed": float,
            "productivity_rate": float,
            "cost_per_hour": float,
            "revenue_generated": float
        } if include_productivity else None
    }
```

### **API05: Equipment Assignment & Reservation**

#### **GET /api/equipment/assignments**
```python
@app.get("/api/equipment/assignments")
async def get_equipment_assignments(
    site_id: str = None,
    operator_id: str = None,
    date: str = None
):
    """Get current equipment assignments and reservations"""
    return {
        "assignments": [
            {
                "equipment_id": str,
                "equipment_name": str,
                "operator_id": str,
                "operator_name": str,
                "assignment_start": str,
                "assignment_end": str,
                "status": str,
                "location": dict
            }
        ],
        "reservations": [
            {
                "equipment_id": str,
                "reserved_by": str,
                "reservation_start": str,
                "reservation_end": str,
                "purpose": str
            }
        ]
    }
```

#### **POST /api/equipment/{equipment_id}/assign**
```python
@app.post("/api/equipment/{equipment_id}/assign")
async def assign_equipment(
    equipment_id: str,
    assignment_data: EquipmentAssignmentRequest
):
    """Assign equipment to operator"""
    return {
        "assignment_id": str,
        "equipment_id": str,
        "operator_id": str,
        "assignment_confirmed": bool,
        "certification_verified": bool,
        "assignment_start": str
    }
```

---

## 📈 **ADVANCED FEATURES**

### **AF01: Predictive Maintenance AI**
- Machine learning models for predicting equipment failures
- Anomaly detection in IoT sensor data
- Optimal maintenance timing recommendations
- Parts inventory forecasting based on usage patterns

### **AF02: Fleet Optimization**
- AI-powered equipment allocation and scheduling
- Cross-site equipment sharing optimization
- Fuel efficiency and route optimization
- Cost-benefit analysis for equipment decisions

### **AF03: Mobile Field Applications**
- Equipment inspection mobile apps with photo capture
- QR code scanning for equipment identification
- Voice-activated status updates and work logging
- Offline capability with data synchronization

### **AF04: Integration Ecosystem**
- Telematics system integration (Caterpillar, Komatsu, etc.)
- Fleet management system APIs
- Parts supplier integration for automatic ordering
- Insurance and warranty claim automation

---

## 🔄 **REAL-TIME REQUIREMENTS**

### **RT01: Live Equipment Monitoring**
- Real-time IoT data streaming with <30 second latency
- Live equipment location tracking with GPS updates every 10 seconds
- Instant alert generation for equipment issues or safety violations
- Real-time utilization dashboard with auto-refresh every 60 seconds

### **RT02: Dynamic Resource Allocation**
- Real-time equipment availability tracking
- Instant operator assignment and conflict resolution
- Live workload balancing and equipment redistribution
- Emergency reallocation protocols for urgent needs

---

## 🎯 **SUCCESS CRITERIA**

### **Functional Success:**
- ✅ Real-time monitoring of all equipment with 95%+ uptime visibility
- ✅ Automated maintenance scheduling with 90%+ adherence rate
- ✅ IoT integration with 85%+ of compatible equipment
- ✅ Mobile interface supporting field operations
- ✅ Predictive maintenance reducing unplanned downtime by 40%

### **Performance Success:**
- Equipment status updates within 30 seconds of IoT data receipt
- Dashboard loads within 3 seconds with full equipment data
- Mobile app responds within 2 seconds for field operations
- Maintenance work order generation within 60 seconds
- Alert notifications delivered within 10 seconds

### **Integration Success:**
- Full IoT device integration with major equipment manufacturers
- Complete maintenance management workflow automation
- Seamless operator assignment and certification verification
- Real-time cost tracking and utilization optimization
- Cross-system data synchronization with 99%+ accuracy

---

## 📋 **IMPLEMENTATION PRIORITY**

### **Phase 1: Core Equipment Management (Week 1)**
1. Database schema implementation (5 new tables + enhancements)
2. Basic equipment monitoring dashboard and status tracking
3. Equipment assignment and reservation system
4. Mobile-optimized interface for field operations

### **Phase 2: IoT Integration & Analytics (Week 2)**
1. IoT data ingestion and processing pipeline
2. Real-time monitoring dashboard with live updates
3. Maintenance scheduling and work order management
4. Utilization analytics and performance tracking

### **Phase 3: Advanced Features & AI (Week 3)**
1. Predictive maintenance AI and anomaly detection
2. Fleet optimization and resource allocation algorithms
3. Advanced mobile features (QR codes, voice commands)
4. Third-party integrations and API connections

---

**Document Status**: ✅ Analysis Complete - Phase 2 Screen #02  
**Next Screen**: Time Comparison (`/time-comparison`)  
**Database Schema**: Update required - 5 new tables + 2 enhancements  
**Estimated Backend Development**: 4-5 weeks