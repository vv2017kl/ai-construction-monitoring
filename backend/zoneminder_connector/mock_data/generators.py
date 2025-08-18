"""
Comprehensive Mock Data Generators for Construction Industry
==========================================================

Generates realistic construction site monitoring data for development and testing.
"""

import random
import uuid
from datetime import datetime, timedelta, date, time
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import asdict
import json

from ..base_connector import (
    CameraInfo, DetectionEvent, MonitoringZone, CameraType, 
    CameraStatus, DetectionType, StreamQuality
)

class ConstructionDataGenerator:
    """Main generator class that orchestrates all construction industry mock data"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.sites_count = config.get("sites_count", 3)
        self.cameras_per_site = config.get("cameras_per_site", 8)
        self.events_per_day = config.get("events_per_day", 25)
        self.zones_per_camera = config.get("zones_per_camera", 2)
        
        # Initialize sub-generators
        self.site_generator = SiteDataGenerator(config)
        self.camera_generator = CameraDataGenerator(config)
        self.event_generator = EventDataGenerator(config)
        self.analytics_generator = AnalyticsDataGenerator(config)
        
        # Generate base site data
        self.sites_data = self.site_generator.generate_sites(self.sites_count)
        
        print(f"🏗️ Construction Data Generator initialized:")
        print(f"   🏢 Sites: {len(self.sites_data)}")
        print(f"   📹 Cameras per site: {self.cameras_per_site}")
        print(f"   🎯 Events per day: {self.events_per_day}")
        
    def generate_cameras(self) -> List[CameraInfo]:
        """Generate cameras for all construction sites"""
        all_cameras = []
        
        for site_data in self.sites_data:
            site_cameras = self.camera_generator.generate_site_cameras(
                site_data, self.cameras_per_site
            )
            all_cameras.extend(site_cameras)
            
        print(f"📹 Generated {len(all_cameras)} cameras across {len(self.sites_data)} construction sites")
        return all_cameras
    
    def generate_events(self, cameras: List[CameraInfo], days_back: int = 30) -> List[DetectionEvent]:
        """Generate detection events for the past N days"""
        all_events = []
        
        # Calculate total events needed
        total_events = self.events_per_day * days_back
        
        for day_offset in range(days_back):
            event_date = datetime.now() - timedelta(days=day_offset)
            daily_events = self.event_generator.generate_daily_events(
                cameras, self.sites_data, event_date, self.events_per_day
            )
            all_events.extend(daily_events)
        
        # Sort by timestamp (newest first)
        all_events.sort(key=lambda x: x.timestamp, reverse=True)
        
        print(f"🎯 Generated {len(all_events)} detection events over {days_back} days")
        return all_events
    
    def generate_monitoring_zones(self, cameras: List[CameraInfo]) -> List[MonitoringZone]:
        """Generate monitoring zones for cameras"""
        all_zones = []
        
        for camera in cameras:
            camera_zones = self.camera_generator.generate_camera_zones(
                camera, self.zones_per_camera
            )
            all_zones.extend(camera_zones)
            
        print(f"🔍 Generated {len(all_zones)} monitoring zones")
        return all_zones
    
    def get_site_analytics(self, site_id: str, start_date: date, end_date: date) -> Dict[str, Any]:
        """Generate comprehensive site analytics"""
        site_data = next((s for s in self.sites_data if s["site_id"] == site_id), None)
        if not site_data:
            raise ValueError(f"Site {site_id} not found")
            
        return self.analytics_generator.generate_site_analytics(
            site_data, start_date, end_date
        )
    
    def _create_detection_event(self, camera: CameraInfo, site_data: Dict[str, Any], timestamp: datetime) -> DetectionEvent:
        """Create a single detection event (used by mock connector for real-time events)"""
        return self.event_generator.create_single_event(camera, site_data, timestamp)

class SiteDataGenerator:
    """Generates construction site data and metadata"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.construction_types = config.get("construction_types", [
            "high_rise_building", "residential_complex", "commercial_mall",
            "infrastructure_highway", "industrial_facility", "renovation_project"
        ])
        
    def generate_sites(self, count: int) -> List[Dict[str, Any]]:
        """Generate diverse construction sites"""
        sites = []
        
        # Real construction site templates
        site_templates = [
            {
                "name": "Downtown Tower Complex",
                "type": "high_rise_building",
                "location": "Downtown Seattle",
                "coordinates": (47.6062, -122.3321),
                "description": "42-story mixed-use tower with retail, office, and residential spaces",
                "contractor": "Turner Construction",
                "project_value": 285000000,
                "start_date": "2024-03-15",
                "expected_completion": "2026-11-30",
                "current_phase": "Foundation and Structure",
                "workers_count": 120,
                "hazard_level": "high",
                "weather_sensitive": True,
                "working_hours": "6:00-18:00",
                "security_level": "maximum"
            },
            {
                "name": "Riverside Residential Village", 
                "type": "residential_complex",
                "location": "Bellevue, WA",
                "coordinates": (47.6101, -122.2015),
                "description": "350-unit luxury apartment complex with amenities",
                "contractor": "Lennar Corporation",
                "project_value": 125000000,
                "start_date": "2024-01-08",
                "expected_completion": "2025-12-15",
                "current_phase": "Building Envelope",
                "workers_count": 85,
                "hazard_level": "medium",
                "weather_sensitive": False,
                "working_hours": "7:00-17:00",
                "security_level": "standard"
            },
            {
                "name": "Pacific Northwest Mall Expansion",
                "type": "commercial_mall", 
                "location": "Tacoma, WA",
                "coordinates": (47.2529, -122.4443),
                "description": "200,000 sq ft mall expansion with new anchor stores",
                "contractor": "Skanska USA",
                "project_value": 68000000,
                "start_date": "2024-05-20",
                "expected_completion": "2025-08-31",
                "current_phase": "Interior Fit-out",
                "workers_count": 65,
                "hazard_level": "medium",
                "weather_sensitive": False,
                "working_hours": "8:00-16:00",
                "security_level": "standard"
            },
            {
                "name": "I-405 Bridge Modernization",
                "type": "infrastructure_highway",
                "location": "Renton, WA", 
                "coordinates": (47.4829, -122.2171),
                "description": "Major highway bridge replacement and lane expansion",
                "contractor": "WSDOT & Granite Construction",
                "project_value": 180000000,
                "start_date": "2023-09-01",
                "expected_completion": "2025-06-30",
                "current_phase": "Bridge Construction",
                "workers_count": 150,
                "hazard_level": "critical",
                "weather_sensitive": True,
                "working_hours": "24/7",
                "security_level": "maximum"
            },
            {
                "name": "GreenTech Manufacturing Facility",
                "type": "industrial_facility",
                "location": "Kent, WA",
                "coordinates": (47.3809, -122.2348),
                "description": "450,000 sq ft clean energy component manufacturing plant",
                "contractor": "McCarthy Building Companies",
                "project_value": 95000000,
                "start_date": "2024-02-12",
                "expected_completion": "2025-10-15",
                "current_phase": "Equipment Installation",
                "workers_count": 95,
                "hazard_level": "high",
                "weather_sensitive": False,
                "working_hours": "6:00-18:00",
                "security_level": "high"
            }
        ]
        
        for i in range(count):
            if i < len(site_templates):
                # Use predefined template
                site = site_templates[i].copy()
                site["site_id"] = f"site_{i+1:03d}"
            else:
                # Generate additional sites
                site = self._generate_generic_site(i)
                
            # Add common fields
            site.update({
                "active_zones": random.randint(4, 12),
                "total_area_sqft": random.randint(50000, 2000000),
                "safety_incidents_mtd": random.randint(0, 3),
                "compliance_score": random.uniform(85, 98),
                "environmental_permits": random.choice([True, False]),
                "noise_restrictions": random.choice([True, False]),
                "emergency_contacts": self._generate_emergency_contacts(),
                "equipment_inventory": self._generate_equipment_list(),
                "safety_protocols": self._generate_safety_protocols(),
                "progress_milestones": self._generate_milestones(),
                "weather_impact_days": random.randint(5, 25),
                "last_inspection": (datetime.now() - timedelta(days=random.randint(1, 14))).isoformat()
            })
            
            sites.append(site)
            
        return sites
    
    def _generate_generic_site(self, index: int) -> Dict[str, Any]:
        """Generate a generic construction site"""
        construction_type = random.choice(self.construction_types)
        
        return {
            "site_id": f"site_{index+1:03d}",
            "name": f"{random.choice(['Metro', 'Central', 'North', 'South', 'East', 'West'])} {construction_type.replace('_', ' ').title()} Project",
            "type": construction_type,
            "location": f"{random.choice(['Seattle', 'Bellevue', 'Tacoma', 'Redmond', 'Kirkland'])}, WA",
            "coordinates": (
                47.6062 + random.uniform(-0.2, 0.2),
                -122.3321 + random.uniform(-0.2, 0.2)
            ),
            "description": f"Construction project: {construction_type.replace('_', ' ')}",
            "contractor": random.choice([
                "Turner Construction", "Skanska USA", "Lennar Corporation",
                "McCarthy Building", "Granite Construction", "DPR Construction"
            ]),
            "project_value": random.randint(15000000, 300000000),
            "start_date": (datetime.now() - timedelta(days=random.randint(30, 365))).strftime("%Y-%m-%d"),
            "expected_completion": (datetime.now() + timedelta(days=random.randint(180, 730))).strftime("%Y-%m-%d"),
            "current_phase": random.choice([
                "Site Preparation", "Foundation", "Structure", "Building Envelope",
                "MEP Systems", "Interior Fit-out", "Final Inspections"
            ]),
            "workers_count": random.randint(25, 200),
            "hazard_level": random.choice(["low", "medium", "high", "critical"]),
            "weather_sensitive": random.choice([True, False]),
            "working_hours": random.choice(["6:00-18:00", "7:00-17:00", "8:00-16:00", "24/7"]),
            "security_level": random.choice(["standard", "high", "maximum"])
        }
    
    def _generate_emergency_contacts(self) -> List[Dict[str, str]]:
        """Generate emergency contact information"""
        return [
            {
                "role": "Site Supervisor",
                "name": random.choice(["Mike Johnson", "Sarah Wilson", "David Chen", "Lisa Rodriguez"]),
                "phone": f"({random.randint(200,999)}) {random.randint(200,999)}-{random.randint(1000,9999)}",
                "email": f"supervisor{random.randint(1,99)}@construction.com"
            },
            {
                "role": "Safety Manager", 
                "name": random.choice(["Robert Taylor", "Amanda Davis", "Carlos Martinez", "Jennifer Lee"]),
                "phone": f"({random.randint(200,999)}) {random.randint(200,999)}-{random.randint(1000,9999)}",
                "email": f"safety{random.randint(1,99)}@construction.com"
            },
            {
                "role": "Emergency Services",
                "name": "911 / Site Security",
                "phone": "911",
                "email": "security@construction.com"
            }
        ]
    
    def _generate_equipment_list(self) -> List[Dict[str, Any]]:
        """Generate construction equipment inventory"""
        equipment_types = [
            "Tower Crane", "Mobile Crane", "Excavator", "Bulldozer", "Concrete Mixer",
            "Dump Truck", "Loader", "Forklift", "Generator", "Concrete Pump",
            "Scaffolding System", "Welding Equipment", "Compressor"
        ]
        
        equipment = []
        for _ in range(random.randint(5, 15)):
            equipment.append({
                "type": random.choice(equipment_types),
                "model": f"Model-{random.randint(100, 999)}",
                "status": random.choice(["operational", "maintenance", "repair", "standby"]),
                "location": f"Zone {random.randint(1, 8)}",
                "operator": random.choice(["John Smith", "Maria Garcia", "Kevin Brown", "Unassigned"]),
                "last_maintenance": (datetime.now() - timedelta(days=random.randint(1, 90))).strftime("%Y-%m-%d"),
                "hours_used": random.randint(50, 2000)
            })
            
        return equipment
    
    def _generate_safety_protocols(self) -> List[str]:
        """Generate safety protocols for the site"""
        return random.sample([
            "Hard Hat Required at All Times",
            "Safety Vest Must Be Worn",
            "Steel-toed Boots Mandatory", 
            "Fall Protection Above 6 Feet",
            "Lockout/Tagout Procedures",
            "Hot Work Permits Required",
            "Confined Space Entry Protocols",
            "Crane Operation Safety Zones",
            "Daily Safety Briefings",
            "Equipment Pre-use Inspections",
            "Emergency Evacuation Routes Posted",
            "First Aid Stations Marked",
            "Fire Extinguisher Locations",
            "Eye Wash Stations Available"
        ], k=random.randint(6, 10))
    
    def _generate_milestones(self) -> List[Dict[str, Any]]:
        """Generate project milestones"""
        milestones = [
            {"name": "Site Preparation Complete", "status": "completed", "date": "2024-04-15"},
            {"name": "Foundation Pour", "status": "completed", "date": "2024-06-30"},
            {"name": "Structure Topping Out", "status": "in_progress", "date": "2024-12-15"},
            {"name": "Building Envelope", "status": "pending", "date": "2025-03-31"},
            {"name": "MEP Rough-in", "status": "pending", "date": "2025-06-30"},
            {"name": "Final Inspections", "status": "pending", "date": "2025-11-15"}
        ]
        
        return random.sample(milestones, k=random.randint(3, 6))

class CameraDataGenerator:
    """Generates construction-focused camera configurations and monitoring zones"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.rtsp_port = config.get("rtsp_port", 8554)
        
    def generate_site_cameras(self, site_data: Dict[str, Any], count: int) -> List[CameraInfo]:
        """Generate realistic cameras for a construction site"""
        cameras = []
        site_id = site_data["site_id"]
        site_type = site_data["type"]
        
        # Camera placement strategies based on site type
        if site_type == "high_rise_building":
            camera_locations = [
                "Main Entrance Gate", "Construction Elevator", "Tower Crane Base",
                "Material Hoist Area", "Concrete Pour Zone", "Rebar Storage",
                "Worker Break Area", "Equipment Staging", "Perimeter North",
                "Perimeter South", "Loading Dock", "Site Office Entrance"
            ]
        elif site_type == "infrastructure_highway":
            camera_locations = [
                "Bridge Deck Work Zone", "Traffic Control Point", "Heavy Equipment Area",
                "Material Storage Yard", "Concrete Batch Plant", "Worker Safety Zone",
                "Environmental Monitoring", "Public Access Control", "Emergency Vehicle Access",
                "Crane Operation Zone", "Utility Relocation", "Quality Control Lab"
            ]
        else:
            camera_locations = [
                "Main Site Entrance", "Material Storage", "Equipment Yard", 
                "Worker Assembly Area", "Quality Control Zone", "Waste Management",
                "Perimeter Security", "Emergency Assembly Point", "Delivery Area",
                "Supervisor Office", "Safety Equipment Station", "Vehicle Parking"
            ]
        
        # Ensure we have enough locations
        while len(camera_locations) < count:
            camera_locations.extend([
                f"Zone {chr(65+len(camera_locations))}", 
                f"Monitoring Point {len(camera_locations)+1}"
            ])
        
        for i in range(count):
            camera = self._create_camera(site_data, i+1, camera_locations[i % len(camera_locations)])
            cameras.append(camera)
            
        return cameras
    
    def _create_camera(self, site_data: Dict[str, Any], camera_num: int, location: str) -> CameraInfo:
        """Create a single camera with realistic construction site characteristics"""
        site_id = site_data["site_id"]
        camera_id = f"{site_id}_cam_{camera_num:02d}"
        
        # Determine camera type based on location and site characteristics
        camera_type = self._determine_camera_type(location, site_data)
        
        # Generate realistic coordinates around the site
        base_lat, base_lon = site_data["coordinates"]
        lat_offset = random.uniform(-0.001, 0.001)  # ~100m radius
        lon_offset = random.uniform(-0.001, 0.001)
        
        # Camera status based on site activity and time
        status = self._determine_camera_status(site_data)
        
        # Stream configuration
        stream_url = f"rtsp://mock-rtsp-server:{self.rtsp_port}/{site_id}/{camera_id}"
        
        # Camera capabilities based on type and location
        ptz_capable = camera_type in [CameraType.PTZ_MONITORING, CameraType.MOBILE_INSPECTION]
        night_vision = location.lower() in ["perimeter", "security", "entrance", "gate"]
        resolution = self._determine_resolution(camera_type)
        
        camera = CameraInfo(
            camera_id=camera_id,
            name=f"{site_data['name']} - {location}",
            camera_type=camera_type,
            status=status,
            site_id=site_id,
            location_description=location,
            coordinates=(base_lat + lat_offset, base_lon + lon_offset),
            stream_url=stream_url,
            recording_enabled=True,
            motion_detection=True,
            night_vision=night_vision,
            ptz_capable=ptz_capable,
            zoom_level=random.uniform(1.0, 3.0) if ptz_capable else None,
            resolution=resolution,
            created_at=datetime.now() - timedelta(days=random.randint(1, 180)),
            last_seen=datetime.now() - timedelta(minutes=random.randint(0, 30)),
            metadata={
                "installation_date": (datetime.now() - timedelta(days=random.randint(30, 365))).isoformat(),
                "maintenance_schedule": random.choice(["weekly", "bi-weekly", "monthly"]),
                "weather_rating": random.choice(["IP65", "IP66", "IP67"]),
                "mounting_height": f"{random.randint(8, 25)} feet",
                "coverage_angle": f"{random.randint(60, 120)} degrees",
                "recording_retention": f"{random.randint(7, 30)} days",
                "ai_features": random.sample([
                    "person_detection", "vehicle_detection", "ppe_detection",
                    "fall_detection", "crowd_detection", "object_tracking"
                ], k=random.randint(2, 4)),
                "vendor": random.choice(["Hikvision", "Axis", "Dahua", "Bosch", "Hanwha"]),
                "model": f"Model-{random.randint(1000, 9999)}",
                "firmware_version": f"v{random.randint(1,5)}.{random.randint(0,9)}.{random.randint(0,9)}",
                "bandwidth_usage": f"{random.randint(2, 8)} Mbps",
                "storage_allocated": f"{random.randint(50, 500)} GB"
            }
        )
        
        return camera
    
    def _determine_camera_type(self, location: str, site_data: Dict[str, Any]) -> CameraType:
        """Determine appropriate camera type based on location and site"""
        location_lower = location.lower()
        
        if "crane" in location_lower or "equipment" in location_lower:
            return CameraType.PTZ_MONITORING
        elif "entrance" in location_lower or "gate" in location_lower:
            return CameraType.FIXED_SECURITY
        elif "mobile" in location_lower or "inspection" in location_lower:
            return CameraType.MOBILE_INSPECTION
        elif "drone" in location_lower or "aerial" in location_lower:
            return CameraType.DRONE_AERIAL
        elif "progress" in location_lower or "timelapse" in location_lower:
            return CameraType.TIMELAPSE
        else:
            # Default distribution
            return random.choices([
                CameraType.FIXED_SECURITY,
                CameraType.PTZ_MONITORING,
                CameraType.MOBILE_INSPECTION,
                CameraType.TIMELAPSE
            ], weights=[40, 30, 20, 10])[0]
    
    def _determine_camera_status(self, site_data: Dict[str, Any]) -> CameraStatus:
        """Determine camera status based on site conditions"""
        # Higher chance of issues during bad weather or high-hazard sites
        base_online_probability = 0.85
        
        if site_data.get("weather_sensitive", False):
            base_online_probability -= 0.1
            
        if site_data.get("hazard_level") == "critical":
            base_online_probability -= 0.05
        
        # Weekend and night adjustments
        now = datetime.now()
        if now.weekday() >= 5:  # Weekend
            base_online_probability -= 0.05
        
        if now.hour < 6 or now.hour > 22:  # Night hours
            base_online_probability -= 0.1
            
        rand = random.random()
        if rand < base_online_probability:
            return CameraStatus.ONLINE
        elif rand < base_online_probability + 0.08:
            return CameraStatus.MAINTENANCE
        elif rand < base_online_probability + 0.12:
            return CameraStatus.ERROR
        else:
            return CameraStatus.OFFLINE
    
    def _determine_resolution(self, camera_type: CameraType) -> StreamQuality:
        """Determine appropriate resolution based on camera type"""
        if camera_type == CameraType.DRONE_AERIAL:
            return random.choice([StreamQuality.HIGH, StreamQuality.ULTRA])
        elif camera_type == CameraType.TIMELAPSE:
            return random.choice([StreamQuality.HIGH, StreamQuality.ULTRA])
        elif camera_type == CameraType.PTZ_MONITORING:
            return random.choice([StreamQuality.MEDIUM, StreamQuality.HIGH])
        else:
            return random.choices([
                StreamQuality.MEDIUM, StreamQuality.HIGH, StreamQuality.LOW
            ], weights=[50, 40, 10])[0]
    
    def generate_camera_zones(self, camera: CameraInfo, zones_count: int) -> List[MonitoringZone]:
        """Generate monitoring zones for a camera"""
        zones = []
        
        # Zone types appropriate for construction sites
        zone_types = ["safety", "progress", "equipment", "restricted"]
        
        for i in range(zones_count):
            zone_type = random.choice(zone_types)
            zone = self._create_monitoring_zone(camera, i+1, zone_type)
            zones.append(zone)
            
        return zones
    
    def _create_monitoring_zone(self, camera: CameraInfo, zone_num: int, zone_type: str) -> MonitoringZone:
        """Create a monitoring zone for a camera"""
        zone_id = f"{camera.camera_id}_zone_{zone_num}"
        
        # Generate realistic zone names based on type
        zone_names = {
            "safety": ["Hard Hat Zone", "Safety Vest Area", "Fall Protection Zone", "PPE Required Area"],
            "progress": ["Pour Progress", "Installation Zone", "Quality Check Area", "Milestone Area"],
            "equipment": ["Crane Operation", "Heavy Machinery", "Vehicle Traffic", "Equipment Storage"],
            "restricted": ["Authorized Personnel Only", "Danger Zone", "No Entry Area", "Executive Area"]
        }
        
        zone_name = random.choice(zone_names.get(zone_type, ["Monitoring Zone"]))
        
        # Generate polygon coordinates (relative to camera view)
        # Simulate different zone shapes and sizes
        base_coords = self._generate_zone_coordinates(zone_type)
        
        # Sensitivity and thresholds based on zone type
        sensitivity_map = {
            "safety": 0.9,      # High sensitivity for safety zones
            "restricted": 0.95,  # Very high for restricted areas
            "equipment": 0.7,    # Medium for equipment zones
            "progress": 0.6      # Lower for progress monitoring
        }
        
        threshold_map = {
            "safety": 1,        # Immediate alert for safety
            "restricted": 1,    # Immediate alert for restricted access
            "equipment": 3,     # Allow some movement for equipment zones
            "progress": 5       # More tolerance for progress zones
        }
        
        zone = MonitoringZone(
            zone_id=zone_id,
            camera_id=camera.camera_id,
            name=f"{camera.name} - {zone_name}",
            zone_type=zone_type,
            coordinates=base_coords,
            detection_enabled=True,
            sensitivity=sensitivity_map.get(zone_type, 0.8),
            alert_threshold=threshold_map.get(zone_type, 2),
            description=f"{zone_type.title()} monitoring zone for construction site safety and compliance",
            created_at=datetime.now() - timedelta(days=random.randint(1, 90))
        )
        
        return zone
    
    def _generate_zone_coordinates(self, zone_type: str) -> List[Tuple[int, int]]:
        """Generate zone polygon coordinates based on type"""
        # Different zone shapes for different purposes
        if zone_type == "safety":
            # Rectangular safety zones
            x1, y1 = random.randint(50, 200), random.randint(50, 200)
            width, height = random.randint(100, 300), random.randint(80, 200)
            return [(x1, y1), (x1 + width, y1), (x1 + width, y1 + height), (x1, y1 + height)]
        
        elif zone_type == "restricted":
            # Smaller, more focused restricted areas
            x1, y1 = random.randint(100, 300), random.randint(100, 300)
            width, height = random.randint(50, 150), random.randint(50, 150)
            return [(x1, y1), (x1 + width, y1), (x1 + width, y1 + height), (x1, y1 + height)]
        
        elif zone_type == "equipment":
            # Larger equipment zones with more complex shapes
            center_x, center_y = random.randint(200, 600), random.randint(200, 400)
            radius = random.randint(80, 150)
            # Generate hexagonal zone
            points = []
            for i in range(6):
                angle = i * 60 * 3.14159 / 180
                x = center_x + radius * math.cos(angle)
                y = center_y + radius * math.sin(angle)
                points.append((int(x), int(y)))
            return points
        
        else:  # progress zones
            # Variable-sized progress monitoring areas
            x1, y1 = random.randint(100, 400), random.randint(100, 300)
            width, height = random.randint(150, 400), random.randint(100, 250)
            return [(x1, y1), (x1 + width, y1), (x1 + width, y1 + height), (x1, y1 + height)]

import math  # Import needed for zone coordinate generation

class EventDataGenerator:
    """Generates realistic construction site detection events"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.peak_hours = config.get("peak_activity_hours", {"start": 7, "end": 18})
        self.weekend_reduction = config.get("weekend_activity_reduction", 0.3)
        self.night_reduction = config.get("night_activity_reduction", 0.1)
        self.seasonal_variations = config.get("seasonal_variations", True)
        
    def generate_daily_events(
        self, 
        cameras: List[CameraInfo], 
        sites_data: List[Dict[str, Any]], 
        event_date: datetime, 
        target_count: int
    ) -> List[DetectionEvent]:
        """Generate events for a specific day"""
        events = []
        
        # Adjust event count based on day of week and time factors
        adjusted_count = self._adjust_event_count_for_day(target_count, event_date)
        
        # Generate events throughout the day
        for _ in range(adjusted_count):
            # Select random camera and corresponding site
            camera = random.choice(cameras)
            site_data = next(s for s in sites_data if s["site_id"] == camera.site_id)
            
            # Generate random time during the day with realistic distribution
            event_time = self._generate_realistic_event_time(event_date)
            
            event = self.create_single_event(camera, site_data, event_time)
            events.append(event)
            
        return events
    
    def create_single_event(self, camera: CameraInfo, site_data: Dict[str, Any], timestamp: datetime) -> DetectionEvent:
        """Create a single realistic detection event"""
        event_id = f"evt_{uuid.uuid4().hex[:12]}"
        
        # Determine detection type based on camera type, location, and site characteristics
        detection_type = self._determine_detection_type(camera, site_data, timestamp)
        
        # Generate event details based on detection type
        event_details = self._generate_event_details(detection_type, camera, site_data, timestamp)
        
        event = DetectionEvent(
            event_id=event_id,
            camera_id=camera.camera_id,
            detection_type=detection_type,
            timestamp=timestamp,
            confidence_score=event_details["confidence"],
            bounding_boxes=event_details["bounding_boxes"],
            description=event_details["description"],
            severity=event_details["severity"],
            location=camera.location_description,
            personnel_involved=event_details.get("personnel", []),
            equipment_involved=event_details.get("equipment", []),
            image_url=f"http://mock-server:8555/events/{event_id}/image.jpg",
            video_clip_url=f"http://mock-server:8555/events/{event_id}/clip.mp4",
            acknowledged=random.random() < 0.3,  # 30% chance already acknowledged
            resolved=random.random() < 0.15,      # 15% chance already resolved
            metadata=event_details.get("metadata", {})
        )
        
        return event
    
    def _adjust_event_count_for_day(self, base_count: int, event_date: datetime) -> int:
        """Adjust event count based on day characteristics"""
        adjusted_count = base_count
        
        # Weekend reduction
        if event_date.weekday() >= 5:  # Saturday = 5, Sunday = 6
            adjusted_count = int(adjusted_count * (1 - self.weekend_reduction))
        
        # Seasonal variations
        if self.seasonal_variations:
            month = event_date.month
            # Winter months have fewer events due to weather
            if month in [12, 1, 2]:
                adjusted_count = int(adjusted_count * 0.8)
            # Spring/Summer peak activity
            elif month in [4, 5, 6, 7, 8]:
                adjusted_count = int(adjusted_count * 1.2)
        
        return max(1, adjusted_count)  # Ensure at least 1 event
    
    def _generate_realistic_event_time(self, base_date: datetime) -> datetime:
        """Generate realistic event time with higher probability during work hours"""
        # Work hours have 70% of events, off-hours have 30%
        if random.random() < 0.7:
            # During work hours (peak activity)
            hour = random.randint(self.peak_hours["start"], self.peak_hours["end"])
        else:
            # Off hours (security, maintenance, etc.)
            off_hours = list(range(0, self.peak_hours["start"])) + list(range(self.peak_hours["end"]+1, 24))
            hour = random.choice(off_hours)
        
        minute = random.randint(0, 59)
        second = random.randint(0, 59)
        
        return base_date.replace(hour=hour, minute=minute, second=second)
    
    def _determine_detection_type(self, camera: CameraInfo, site_data: Dict[str, Any], timestamp: datetime) -> DetectionType:
        """Determine appropriate detection type based on context"""
        location = camera.location_description.lower()
        camera_type = camera.camera_type
        site_type = site_data["type"]
        hour = timestamp.hour
        
        # Detection type probabilities based on context
        if "entrance" in location or "gate" in location:
            return random.choices([
                DetectionType.PERSONNEL_COUNT,
                DetectionType.RESTRICTED_ACCESS,
                DetectionType.PPE_VIOLATION,
                DetectionType.EQUIPMENT_OPERATION
            ], weights=[40, 30, 20, 10])[0]
        
        elif "crane" in location or "equipment" in location:
            return random.choices([
                DetectionType.EQUIPMENT_OPERATION,
                DetectionType.SAFETY_HAZARD,
                DetectionType.PPE_VIOLATION,
                DetectionType.PERSONNEL_COUNT
            ], weights=[50, 25, 15, 10])[0]
        
        elif "safety" in location or "ppe" in location:
            return random.choices([
                DetectionType.PPE_VIOLATION,
                DetectionType.SAFETY_HAZARD,
                DetectionType.PERSONNEL_COUNT
            ], weights=[60, 30, 10])[0]
        
        elif camera_type == CameraType.TIMELAPSE:
            return DetectionType.PROGRESS_MILESTONE
        
        elif hour < 6 or hour > 22:  # Night hours
            return random.choices([
                DetectionType.RESTRICTED_ACCESS,
                DetectionType.SAFETY_HAZARD,
                DetectionType.EQUIPMENT_OPERATION
            ], weights=[60, 25, 15])[0]
        
        else:
            # General construction site activities
            return random.choices([
                DetectionType.PPE_VIOLATION,
                DetectionType.EQUIPMENT_OPERATION,
                DetectionType.PERSONNEL_COUNT,
                DetectionType.SAFETY_HAZARD,
                DetectionType.PROGRESS_MILESTONE,
                DetectionType.RESTRICTED_ACCESS,
                DetectionType.WEATHER_ALERT
            ], weights=[25, 20, 20, 15, 10, 7, 3])[0]
    
    def _generate_event_details(
        self, 
        detection_type: DetectionType, 
        camera: CameraInfo, 
        site_data: Dict[str, Any], 
        timestamp: datetime
    ) -> Dict[str, Any]:
        """Generate detailed event information based on detection type"""
        
        if detection_type == DetectionType.PPE_VIOLATION:
            return {
                "confidence": random.uniform(0.82, 0.97),
                "severity": random.choices(["medium", "high"], weights=[70, 30])[0],
                "description": random.choice([
                    "Worker detected without hard hat in construction zone",
                    "Personnel not wearing safety vest in designated area",
                    "Missing safety harness at elevated work location",
                    "Worker without steel-toed boots in heavy equipment zone",
                    "Eye protection required but not worn during welding activity",
                    "High-visibility clothing not worn in vehicle traffic area"
                ]),
                "bounding_boxes": [self._generate_person_bounding_box()],
                "personnel": [self._generate_worker_id()],
                "metadata": {
                    "violation_type": random.choice(["hard_hat", "safety_vest", "harness", "boots", "eye_protection"]),
                    "compliance_score_impact": -random.randint(2, 8),
                    "supervisor_notified": random.choice([True, False]),
                    "training_required": True,
                    "incident_category": "safety_violation"
                }
            }
        
        elif detection_type == DetectionType.EQUIPMENT_OPERATION:
            equipment_type = random.choice([
                "Tower Crane", "Mobile Crane", "Excavator", "Concrete Mixer", 
                "Forklift", "Bulldozer", "Concrete Pump", "Welding Equipment"
            ])
            return {
                "confidence": random.uniform(0.88, 0.96),
                "severity": "low",
                "description": f"{equipment_type} operation detected in {camera.location_description}",
                "bounding_boxes": [self._generate_vehicle_bounding_box()],
                "equipment": [equipment_type],
                "personnel": [self._generate_worker_id()] if random.random() < 0.8 else [],
                "metadata": {
                    "equipment_type": equipment_type,
                    "operation_duration_minutes": random.randint(5, 120),
                    "operator_certified": random.choice([True, False]),
                    "maintenance_due": random.choice([True, False]),
                    "fuel_level": f"{random.randint(20, 100)}%",
                    "efficiency_score": random.uniform(75, 95)
                }
            }
        
        elif detection_type == DetectionType.SAFETY_HAZARD:
            hazard_types = [
                "Unsecured materials detected at height",
                "Spill or debris blocking emergency exit",
                "Improper scaffolding configuration identified",
                "Electrical hazard - exposed wiring detected",
                "Fall hazard - missing guardrails observed",
                "Fire hazard - improper storage of flammable materials",
                "Structural instability warning - temporary supports",
                "Confined space entry without proper protocols"
            ]
            return {
                "confidence": random.uniform(0.75, 0.92),
                "severity": random.choices(["high", "critical"], weights=[75, 25])[0],
                "description": random.choice(hazard_types),
                "bounding_boxes": [self._generate_hazard_bounding_box()],
                "metadata": {
                    "hazard_category": random.choice([
                        "fall_risk", "electrical", "structural", "chemical", 
                        "fire_risk", "confined_space", "material_handling"
                    ]),
                    "immediate_action_required": True,
                    "evacuation_recommended": random.choice([True, False]),
                    "regulatory_violation": random.choice([True, False]),
                    "estimated_risk_level": random.randint(6, 10),
                    "response_time_minutes": random.randint(2, 15)
                }
            }
        
        elif detection_type == DetectionType.PERSONNEL_COUNT:
            count = random.randint(1, 15)
            return {
                "confidence": random.uniform(0.85, 0.95),
                "severity": "low",
                "description": f"{count} personnel detected in {camera.location_description}",
                "bounding_boxes": [self._generate_person_bounding_box() for _ in range(min(count, 5))],
                "personnel": [self._generate_worker_id() for _ in range(count)],
                "metadata": {
                    "count": count,
                    "expected_capacity": random.randint(count, count + 10),
                    "shift": self._determine_shift(timestamp),
                    "activity_level": random.choice(["low", "medium", "high"]),
                    "density_per_sqm": round(count / random.uniform(50, 200), 2),
                    "average_duration_minutes": random.randint(10, 180)
                }
            }
        
        elif detection_type == DetectionType.RESTRICTED_ACCESS:
            return {
                "confidence": random.uniform(0.90, 0.98),
                "severity": "high",
                "description": random.choice([
                    "Unauthorized personnel detected in restricted area",
                    "Access attempted outside of authorized hours",
                    "Entry without proper credentials or escort",
                    "Vehicle access in pedestrian-only zone",
                    "Visitor in hard-hat required area without PPE"
                ]),
                "bounding_boxes": [self._generate_person_bounding_box()],
                "personnel": [self._generate_worker_id()],
                "metadata": {
                    "access_level_required": random.choice(["level_1", "level_2", "level_3", "executive"]),
                    "badge_scan_failed": random.choice([True, False]),
                    "security_response_time": random.randint(1, 10),
                    "previous_violations": random.randint(0, 3),
                    "area_classification": random.choice([
                        "executive", "high_voltage", "chemical_storage", 
                        "equipment_maintenance", "structural_danger"
                    ])
                }
            }
        
        elif detection_type == DetectionType.PROGRESS_MILESTONE:
            return {
                "confidence": random.uniform(0.70, 0.88),
                "severity": "low",
                "description": random.choice([
                    "Concrete pour completion milestone achieved",
                    "Structural framework installation progress",
                    "Equipment installation phase milestone",
                    "Quality inspection checkpoint reached",
                    "Safety training completion milestone",
                    "Material delivery and staging complete"
                ]),
                "bounding_boxes": [self._generate_progress_bounding_box()],
                "metadata": {
                    "milestone_type": random.choice([
                        "concrete_pour", "structural", "equipment", "inspection", 
                        "training", "delivery", "quality_check"
                    ]),
                    "completion_percentage": random.randint(70, 100),
                    "schedule_status": random.choice(["on_time", "ahead", "delayed"]),
                    "quality_score": random.uniform(85, 98),
                    "next_milestone_days": random.randint(3, 21),
                    "project_impact": random.choice(["positive", "neutral", "concerning"])
                }
            }
        
        elif detection_type == DetectionType.WEATHER_ALERT:
            weather_conditions = [
                "High wind conditions affecting crane operations",
                "Heavy precipitation impacting concrete work",
                "Low visibility due to fog or dust",
                "Temperature below safe working conditions",
                "Lightning detected - outdoor work suspension",
                "Ice formation creating slip hazards"
            ]
            return {
                "confidence": random.uniform(0.95, 0.99),
                "severity": random.choices(["medium", "high", "critical"], weights=[50, 35, 15])[0],
                "description": random.choice(weather_conditions),
                "bounding_boxes": [],  # Weather events don't have bounding boxes
                "metadata": {
                    "weather_type": random.choice([
                        "wind", "precipitation", "visibility", "temperature", 
                        "lightning", "ice", "extreme_heat"
                    ]),
                    "measurement_value": random.uniform(10, 100),
                    "measurement_unit": random.choice(["mph", "mm/hr", "meters", "°F", "strikes/hr"]),
                    "work_suspension_required": random.choice([True, False]),
                    "estimated_duration_hours": random.randint(1, 24),
                    "safety_protocols_activated": True,
                    "national_weather_service_alert": random.choice([True, False])
                }
            }
        
        else:
            # Default/fallback event details
            return {
                "confidence": random.uniform(0.70, 0.90),
                "severity": "medium",
                "description": f"Construction activity detected in {camera.location_description}",
                "bounding_boxes": [self._generate_generic_bounding_box()],
                "metadata": {
                    "event_category": "general_activity",
                    "automated_detection": True
                }
            }
    
    def _generate_person_bounding_box(self) -> Dict[str, float]:
        """Generate realistic bounding box for a person"""
        x1 = random.uniform(0.1, 0.7)
        y1 = random.uniform(0.2, 0.6)
        width = random.uniform(0.08, 0.15)
        height = random.uniform(0.2, 0.4)
        return {
            "x1": x1,
            "y1": y1,
            "x2": min(x1 + width, 0.95),
            "y2": min(y1 + height, 0.95),
            "confidence": random.uniform(0.85, 0.98)
        }
    
    def _generate_vehicle_bounding_box(self) -> Dict[str, float]:
        """Generate realistic bounding box for equipment/vehicles"""
        x1 = random.uniform(0.05, 0.5)
        y1 = random.uniform(0.3, 0.7)
        width = random.uniform(0.2, 0.4)
        height = random.uniform(0.15, 0.3)
        return {
            "x1": x1,
            "y1": y1,
            "x2": min(x1 + width, 0.95),
            "y2": min(y1 + height, 0.95),
            "confidence": random.uniform(0.88, 0.96)
        }
    
    def _generate_hazard_bounding_box(self) -> Dict[str, float]:
        """Generate bounding box for hazard detection"""
        x1 = random.uniform(0.1, 0.6)
        y1 = random.uniform(0.1, 0.6)
        width = random.uniform(0.15, 0.3)
        height = random.uniform(0.1, 0.25)
        return {
            "x1": x1,
            "y1": y1,
            "x2": min(x1 + width, 0.9),
            "y2": min(y1 + height, 0.9),
            "confidence": random.uniform(0.75, 0.92)
        }
    
    def _generate_progress_bounding_box(self) -> Dict[str, float]:
        """Generate bounding box for progress milestone detection"""
        x1 = random.uniform(0.0, 0.3)
        y1 = random.uniform(0.0, 0.3)
        width = random.uniform(0.4, 0.7)
        height = random.uniform(0.4, 0.7)
        return {
            "x1": x1,
            "y1": y1,
            "x2": min(x1 + width, 1.0),
            "y2": min(y1 + height, 1.0),
            "confidence": random.uniform(0.70, 0.88)
        }
    
    def _generate_generic_bounding_box(self) -> Dict[str, float]:
        """Generate generic bounding box"""
        x1 = random.uniform(0.1, 0.5)
        y1 = random.uniform(0.1, 0.5)
        width = random.uniform(0.2, 0.4)
        height = random.uniform(0.2, 0.4)
        return {
            "x1": x1,
            "y1": y1,
            "x2": min(x1 + width, 0.9),
            "y2": min(y1 + height, 0.9),
            "confidence": random.uniform(0.70, 0.90)
        }
    
    def _generate_worker_id(self) -> str:
        """Generate realistic worker identifier"""
        return f"W{random.randint(1000, 9999)}"
    
    def _determine_shift(self, timestamp: datetime) -> str:
        """Determine work shift based on time"""
        hour = timestamp.hour
        if 6 <= hour < 14:
            return "day_shift"
        elif 14 <= hour < 22:
            return "evening_shift"
        else:
            return "night_shift"

class AnalyticsDataGenerator:
    """Generates comprehensive construction site analytics and insights"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
    def generate_site_analytics(
        self, 
        site_data: Dict[str, Any], 
        start_date: date, 
        end_date: date
    ) -> Dict[str, Any]:
        """Generate comprehensive site analytics for a date range"""
        total_days = (end_date - start_date).days + 1
        site_type = site_data["type"]
        
        return {
            "site_info": {
                "site_id": site_data["site_id"],
                "name": site_data["name"],
                "type": site_type,
                "analysis_period": {
                    "start_date": start_date.isoformat(),
                    "end_date": end_date.isoformat(),
                    "total_days": total_days
                }
            },
            "safety_metrics": self._generate_safety_analytics(site_data, total_days),
            "productivity_metrics": self._generate_productivity_analytics(site_data, total_days),
            "equipment_analytics": self._generate_equipment_analytics(site_data, total_days),
            "personnel_analytics": self._generate_personnel_analytics(site_data, total_days),
            "quality_metrics": self._generate_quality_analytics(site_data, total_days),
            "environmental_impact": self._generate_environmental_analytics(site_data, total_days),
            "cost_efficiency": self._generate_cost_analytics(site_data, total_days),
            "compliance_tracking": self._generate_compliance_analytics(site_data, total_days),
            "predictive_insights": self._generate_predictive_analytics(site_data, total_days),
            "benchmarking": self._generate_benchmarking_data(site_data, site_type, total_days)
        }
    
    def _generate_safety_analytics(self, site_data: Dict[str, Any], days: int) -> Dict[str, Any]:
        """Generate safety-focused analytics"""
        base_incidents = site_data.get("safety_incidents_mtd", random.randint(0, 5))
        
        return {
            "incident_summary": {
                "total_incidents": base_incidents + random.randint(0, 3),
                "near_misses": random.randint(5, 25),
                "safety_violations": random.randint(2, 15),
                "lost_time_incidents": random.randint(0, 2),
                "first_aid_cases": random.randint(1, 8)
            },
            "incident_trends": {
                "incidents_by_type": {
                    "ppe_violation": random.randint(30, 60),
                    "fall_risk": random.randint(5, 20),
                    "equipment_related": random.randint(8, 25),
                    "environmental": random.randint(2, 10),
                    "procedural": random.randint(10, 30)
                },
                "incidents_by_severity": {
                    "low": random.randint(40, 70),
                    "medium": random.randint(15, 35),
                    "high": random.randint(3, 12),
                    "critical": random.randint(0, 3)
                },
                "daily_average": round((base_incidents + random.randint(0, 3)) / max(days, 1), 2)
            },
            "safety_scores": {
                "overall_safety_rating": random.uniform(78, 94),
                "ppe_compliance_rate": random.uniform(85, 98),
                "training_completion_rate": random.uniform(92, 99),
                "hazard_identification_score": random.uniform(80, 95),
                "emergency_response_readiness": random.uniform(88, 97)
            },
            "leading_indicators": {
                "safety_meetings_held": random.randint(days//7, days//3),
                "inspections_completed": random.randint(days*2, days*5),
                "hazards_identified": random.randint(10, 50),
                "corrective_actions_taken": random.randint(8, 45),
                "safety_suggestions_submitted": random.randint(5, 25)
            }
        }
    
    def _generate_productivity_analytics(self, site_data: Dict[str, Any], days: int) -> Dict[str, Any]:
        """Generate productivity and progress analytics"""
        return {
            "progress_metrics": {
                "overall_completion": random.uniform(25, 85),
                "schedule_performance": random.uniform(85, 105),  # % of planned vs actual
                "milestone_completion_rate": random.uniform(80, 95),
                "critical_path_status": random.choice(["on_track", "at_risk", "delayed"]),
                "estimated_completion_date": (
                    datetime.now() + timedelta(days=random.randint(90, 550))
                ).strftime("%Y-%m-%d")
            },
            "work_efficiency": {
                "labor_productivity_index": random.uniform(85, 115),
                "equipment_utilization_rate": random.uniform(70, 90),
                "material_waste_percentage": random.uniform(3, 12),
                "rework_percentage": random.uniform(2, 8),
                "daily_production_rate": random.uniform(80, 120)  # % of target
            },
            "resource_utilization": {
                "peak_workforce_count": random.randint(80, 200),
                "average_daily_workforce": random.randint(60, 150),
                "overtime_hours_percentage": random.uniform(5, 25),
                "subcontractor_percentage": random.uniform(20, 60),
                "equipment_availability": random.uniform(85, 95)
            },
            "quality_indicators": {
                "first_pass_quality_rate": random.uniform(88, 96),
                "inspection_pass_rate": random.uniform(90, 98),
                "defect_density": random.uniform(0.5, 3.0),  # defects per 100 units
                "customer_satisfaction_score": random.uniform(4.2, 4.8),  # out of 5
                "warranty_claims": random.randint(0, 3)
            }
        }
    
    def _generate_equipment_analytics(self, site_data: Dict[str, Any], days: int) -> Dict[str, Any]:
        """Generate equipment performance analytics"""
        equipment_count = len(site_data.get("equipment_inventory", []))
        
        return {
            "fleet_overview": {
                "total_equipment_count": equipment_count,
                "operational_equipment": random.randint(int(equipment_count * 0.8), equipment_count),
                "under_maintenance": random.randint(0, int(equipment_count * 0.15)),
                "out_of_service": random.randint(0, int(equipment_count * 0.1)),
                "utilization_rate": random.uniform(65, 85)
            },
            "performance_metrics": {
                "average_uptime": random.uniform(85, 95),
                "maintenance_costs_per_hour": random.uniform(25, 85),
                "fuel_efficiency_rating": random.uniform(70, 90),
                "operator_efficiency_score": random.uniform(80, 95),
                "breakdown_frequency": random.uniform(0.02, 0.08)  # per operating hour
            },
            "maintenance_analytics": {
                "scheduled_maintenance_compliance": random.uniform(90, 98),
                "preventive_maintenance_ratio": random.uniform(75, 90),
                "mean_time_between_failures": random.randint(150, 500),  # hours
                "average_repair_time": random.uniform(2, 8),  # hours
                "parts_availability": random.uniform(85, 95)
            },
            "cost_analysis": {
                "total_operating_costs": random.randint(50000, 250000),
                "cost_per_operating_hour": random.uniform(45, 120),
                "maintenance_cost_ratio": random.uniform(15, 30),  # % of total costs
                "fuel_cost_percentage": random.uniform(25, 45),
                "depreciation_rate": random.uniform(8, 15)  # % per year
            }
        }
    
    def _generate_personnel_analytics(self, site_data: Dict[str, Any], days: int) -> Dict[str, Any]:
        """Generate workforce analytics"""
        worker_count = site_data.get("workers_count", random.randint(50, 200))
        
        return {
            "workforce_overview": {
                "total_personnel": worker_count,
                "direct_employees": random.randint(int(worker_count * 0.4), int(worker_count * 0.7)),
                "subcontractors": random.randint(int(worker_count * 0.3), int(worker_count * 0.6)),
                "average_daily_attendance": random.uniform(85, 95),
                "turnover_rate": random.uniform(8, 25)  # % annually
            },
            "productivity_metrics": {
                "labor_hours_per_day": random.randint(worker_count * 6, worker_count * 10),
                "productivity_index": random.uniform(90, 110),
                "skill_utilization_rate": random.uniform(75, 90),
                "cross_training_completion": random.uniform(60, 85),
                "performance_rating_average": random.uniform(3.8, 4.6)  # out of 5
            },
            "safety_performance": {
                "lost_time_injury_rate": random.uniform(0.5, 3.0),
                "safety_training_hours": random.randint(worker_count * 2, worker_count * 8),
                "safety_certification_compliance": random.uniform(90, 99),
                "incident_reporting_rate": random.uniform(85, 95),
                "ppe_compliance_score": random.uniform(88, 97)
            },
            "engagement_metrics": {
                "employee_satisfaction_score": random.uniform(3.5, 4.5),  # out of 5
                "suggestion_box_submissions": random.randint(5, 30),
                "training_participation_rate": random.uniform(85, 95),
                "communication_effectiveness": random.uniform(75, 90),
                "retention_rate": random.uniform(75, 92)
            }
        }
    
    def _generate_quality_analytics(self, site_data: Dict[str, Any], days: int) -> Dict[str, Any]:
        """Generate quality control analytics"""
        return {
            "quality_overview": {
                "overall_quality_score": random.uniform(85, 96),
                "inspection_pass_rate": random.uniform(88, 95),
                "rework_percentage": random.uniform(2, 8),
                "defect_rate": random.uniform(1, 5),  # % of work requiring correction
                "client_satisfaction": random.uniform(4.0, 4.8)  # out of 5
            },
            "inspection_metrics": {
                "total_inspections": random.randint(days * 3, days * 8),
                "passed_first_inspection": random.uniform(80, 92),
                "critical_defects": random.randint(0, 5),
                "minor_defects": random.randint(5, 25),
                "inspection_coverage": random.uniform(90, 98)  # % of work inspected
            },
            "material_quality": {
                "material_acceptance_rate": random.uniform(92, 98),
                "supplier_quality_rating": random.uniform(85, 95),
                "material_waste_percentage": random.uniform(3, 10),
                "specification_compliance": random.uniform(90, 98),
                "testing_pass_rate": random.uniform(88, 96)
            },
            "continuous_improvement": {
                "quality_improvement_initiatives": random.randint(3, 12),
                "process_optimization_suggestions": random.randint(5, 20),
                "best_practices_documented": random.randint(8, 25),
                "training_effectiveness_score": random.uniform(80, 95),
                "quality_cost_reduction": random.uniform(2, 12)  # % improvement
            }
        }
    
    def _generate_environmental_analytics(self, site_data: Dict[str, Any], days: int) -> Dict[str, Any]:
        """Generate environmental impact analytics"""
        return {
            "environmental_compliance": {
                "permit_compliance_rate": random.uniform(95, 99.5),
                "environmental_incidents": random.randint(0, 2),
                "regulatory_inspections_passed": random.randint(2, 8),
                "sustainability_score": random.uniform(70, 90),
                "carbon_footprint_rating": random.choice(["A", "B", "B+", "A-"])
            },
            "resource_consumption": {
                "water_usage_gallons": random.randint(10000, 50000),
                "electricity_consumption_kwh": random.randint(5000, 25000),
                "fuel_consumption_gallons": random.randint(2000, 15000),
                "waste_generated_tons": random.uniform(5, 30),
                "recycling_rate": random.uniform(60, 85)
            },
            "emission_metrics": {
                "co2_emissions_tons": random.uniform(10, 100),
                "particulate_matter_levels": random.uniform(20, 80),  # μg/m³
                "noise_level_average": random.uniform(65, 85),  # dB
                "dust_control_effectiveness": random.uniform(80, 95),
                "air_quality_index": random.randint(25, 75)
            },
            "conservation_efforts": {
                "water_conservation_percentage": random.uniform(10, 30),
                "energy_efficiency_improvements": random.uniform(5, 20),
                "material_recycling_tons": random.uniform(2, 15),
                "green_building_features": random.randint(3, 12),
                "biodiversity_protection_measures": random.randint(1, 6)
            }
        }
    
    def _generate_cost_analytics(self, site_data: Dict[str, Any], days: int) -> Dict[str, Any]:
        """Generate cost efficiency analytics"""
        total_value = site_data.get("project_value", random.randint(50000000, 500000000))
        
        return {
            "budget_performance": {
                "total_project_value": total_value,
                "spent_to_date": random.randint(int(total_value * 0.2), int(total_value * 0.8)),
                "budget_variance": random.uniform(-15, 10),  # % over/under budget
                "cost_performance_index": random.uniform(0.85, 1.15),
                "estimated_final_cost": random.randint(int(total_value * 0.9), int(total_value * 1.2))
            },
            "cost_breakdown": {
                "labor_costs_percentage": random.uniform(35, 50),
                "material_costs_percentage": random.uniform(25, 40),
                "equipment_costs_percentage": random.uniform(10, 20),
                "overhead_percentage": random.uniform(8, 15),
                "profit_margin": random.uniform(5, 12)
            },
            "efficiency_metrics": {
                "cost_per_square_foot": random.uniform(150, 400),
                "labor_cost_efficiency": random.uniform(85, 115),  # vs industry standard
                "material_cost_optimization": random.uniform(90, 110),
                "overhead_ratio": random.uniform(8, 18),
                "change_order_impact": random.uniform(-5, 15)  # % of original contract
            },
            "financial_health": {
                "cash_flow_status": random.choice(["positive", "neutral", "concerning"]),
                "payment_schedule_adherence": random.uniform(85, 98),
                "supplier_payment_terms": random.randint(30, 90),  # days
                "project_profitability": random.uniform(8, 20),
                "risk_reserve_utilization": random.uniform(10, 60)
            }
        }
    
    def _generate_compliance_analytics(self, site_data: Dict[str, Any], days: int) -> Dict[str, Any]:
        """Generate regulatory compliance analytics"""
        return {
            "regulatory_compliance": {
                "overall_compliance_score": random.uniform(90, 98),
                "permit_status": "current",
                "inspection_results": {
                    "passed": random.randint(8, 15),
                    "failed": random.randint(0, 2),
                    "pending": random.randint(0, 3)
                },
                "violations_count": random.randint(0, 3),
                "corrective_actions_completed": random.uniform(90, 100)
            },
            "safety_compliance": {
                "osha_compliance_score": random.uniform(92, 98),
                "safety_training_compliance": random.uniform(95, 99),
                "ppe_compliance_rate": random.uniform(88, 96),
                "incident_reporting_compliance": random.uniform(95, 100),
                "safety_meeting_attendance": random.uniform(85, 95)
            },
            "environmental_compliance": {
                "epa_compliance_rating": random.choice(["Excellent", "Good", "Satisfactory"]),
                "waste_disposal_compliance": random.uniform(95, 99),
                "emission_standards_adherence": random.uniform(90, 98),
                "water_quality_compliance": random.uniform(92, 99),
                "noise_ordinance_compliance": random.uniform(85, 95)
            },
            "documentation_compliance": {
                "permit_documentation_complete": random.uniform(95, 100),
                "inspection_records_current": random.uniform(90, 98),
                "training_records_compliance": random.uniform(92, 99),
                "incident_documentation_rate": random.uniform(95, 100),
                "audit_readiness_score": random.uniform(85, 95)
            }
        }
    
    def _generate_predictive_analytics(self, site_data: Dict[str, Any], days: int) -> Dict[str, Any]:
        """Generate predictive insights and forecasts"""
        return {
            "schedule_predictions": {
                "completion_probability_on_time": random.uniform(70, 90),
                "predicted_delay_days": random.randint(-14, 45),
                "critical_path_risks": random.randint(2, 8),
                "weather_impact_forecast": random.uniform(5, 20),  # days of delay
                "resource_constraint_risks": random.randint(1, 5)
            },
            "cost_forecasts": {
                "budget_overrun_probability": random.uniform(15, 40),
                "predicted_final_cost_variance": random.uniform(-5, 25),
                "material_cost_escalation": random.uniform(2, 12),
                "labor_cost_trends": random.uniform(-3, 15),
                "contingency_utilization_forecast": random.uniform(20, 80)
            },
            "safety_predictions": {
                "incident_risk_score": random.uniform(0.1, 0.8),  # probability of incident
                "high_risk_activities": random.randint(2, 8),
                "safety_training_needs": random.randint(10, 40),  # number of workers
                "ppe_replacement_forecast": random.randint(50, 200),  # units needed
                "safety_investment_recommendation": random.randint(5000, 25000)
            },
            "equipment_forecasts": {
                "maintenance_due_next_30_days": random.randint(3, 12),
                "equipment_replacement_needed": random.randint(0, 3),
                "utilization_optimization_potential": random.uniform(5, 20),
                "fuel_cost_projections": random.uniform(-10, 25),
                "downtime_risk_assessment": random.uniform(2, 12)  # hours per month
            }
        }
    
    def _generate_benchmarking_data(self, site_data: Dict[str, Any], site_type: str, days: int) -> Dict[str, Any]:
        """Generate industry benchmarking data"""
        return {
            "industry_comparisons": {
                "safety_performance_vs_industry": random.uniform(95, 125),  # % of industry average
                "productivity_vs_peers": random.uniform(85, 115),
                "cost_efficiency_ranking": random.choice(["Top 10%", "Top 25%", "Average", "Below Average"]),
                "schedule_performance_percentile": random.randint(25, 90),
                "quality_score_vs_benchmark": random.uniform(90, 110)
            },
            "regional_comparisons": {
                "vs_regional_average_cost": random.uniform(90, 120),
                "vs_regional_safety_record": random.uniform(85, 115),
                "vs_regional_completion_time": random.uniform(80, 110),
                "regional_ranking": f"#{random.randint(1, 50)} of {random.randint(50, 150)} projects",
                "market_position": random.choice(["Leader", "Strong", "Average", "Developing"])
            },
            "best_practices_comparison": {
                "innovation_adoption_score": random.uniform(60, 95),
                "technology_utilization_rate": random.uniform(70, 90),
                "sustainability_practices_score": random.uniform(65, 85),
                "workforce_development_rating": random.uniform(75, 95),
                "client_satisfaction_vs_industry": random.uniform(95, 115)
            },
            "improvement_opportunities": {
                "cost_reduction_potential": random.uniform(3, 15),  # % potential savings
                "schedule_compression_potential": random.uniform(5, 20),  # % time reduction
                "safety_improvement_areas": random.randint(2, 6),
                "quality_enhancement_opportunities": random.randint(1, 4),
                "efficiency_optimization_score": random.uniform(70, 90)
            }
        }