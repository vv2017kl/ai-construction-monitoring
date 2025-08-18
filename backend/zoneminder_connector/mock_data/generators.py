"""
Mock Data Generators for Construction Industry ZoneMinder Simulation
===================================================================

Generates realistic construction site data including cameras, events, and scenarios.
"""

import random
import uuid
from datetime import datetime, timedelta, date
from typing import List, Dict, Any, Optional
from faker import Faker

from ..base_connector import (
    CameraInfo, DetectionEvent, MonitoringZone, CameraType, CameraStatus, 
    DetectionType, StreamQuality
)

fake = Faker()

class ConstructionDataGenerator:
    """Generates realistic construction industry mock data"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.sites_data = self._generate_construction_sites()
        
    def _generate_construction_sites(self) -> List[Dict[str, Any]]:
        """Generate construction site configurations"""
        sites = []
        
        site_types = [
            {
                "type": "high_rise_building",
                "name": "Metropolitan Tower Construction",
                "description": "30-story residential/commercial high-rise",
                "camera_types": ["fixed_security", "ptz_monitoring", "timelapse"],
                "typical_events": ["ppe_violation", "equipment_operation", "progress_milestone"]
            },
            {
                "type": "infrastructure_project", 
                "name": "Downtown Bridge Expansion",
                "description": "Major bridge infrastructure upgrade",
                "camera_types": ["fixed_security", "mobile_inspection", "drone_aerial"],
                "typical_events": ["safety_hazard", "equipment_operation", "weather_alert"]
            },
            {
                "type": "residential_development",
                "name": "Riverside Housing Development", 
                "description": "120-unit residential community",
                "camera_types": ["fixed_security", "ptz_monitoring"],
                "typical_events": ["restricted_access", "personnel_count", "progress_milestone"]
            },
            {
                "type": "industrial_facility",
                "name": "Advanced Manufacturing Plant",
                "description": "State-of-the-art production facility",
                "camera_types": ["fixed_security", "ptz_monitoring", "mobile_inspection"],
                "typical_events": ["safety_hazard", "equipment_operation", "ppe_violation"]
            },
            {
                "type": "renovation_project",
                "name": "Historic Building Restoration",
                "description": "19th century landmark renovation",
                "camera_types": ["fixed_security", "timelapse"],
                "typical_events": ["progress_milestone", "safety_hazard", "restricted_access"]
            }
        ]
        
        for i, site_type in enumerate(site_types[:self.config.get("sites_count", 5)]):
            site = {
                "site_id": str(uuid.uuid4()),
                "name": site_type["name"],
                "type": site_type["type"],
                "description": site_type["description"],
                "address": fake.address(),
                "coordinates": (fake.latitude(), fake.longitude()),
                "project_manager": fake.name(),
                "start_date": fake.date_between(start_date="-2y", end_date="-6m"),
                "expected_completion": fake.date_between(start_date="6m", end_date="2y"),
                "camera_types": site_type["camera_types"],
                "typical_events": site_type["typical_events"],
                "active_cameras": [],
                "monitoring_zones": []
            }
            sites.append(site)
            
        return sites

    def generate_cameras(self) -> List[CameraInfo]:
        """Generate realistic construction site cameras"""
        cameras = []
        
        for site in self.sites_data:
            cameras_per_site = self.config.get("cameras_per_site", 8)
            
            for i in range(cameras_per_site):
                camera_type = random.choice(site["camera_types"])
                camera = self._create_camera(site, i, camera_type)
                cameras.append(camera)
                site["active_cameras"].append(camera.camera_id)
                
        return cameras

    def _create_camera(self, site: Dict, index: int, camera_type_str: str) -> CameraInfo:
        """Create individual camera with realistic construction site positioning"""
        camera_type = CameraType(camera_type_str)
        
        # Realistic camera positioning based on construction site layout
        camera_locations = {
            "fixed_security": [
                "Main Gate Entrance", "Construction Office", "Material Storage Area",
                "Equipment Parking", "Site Perimeter - North", "Site Perimeter - South"
            ],
            "ptz_monitoring": [
                "Central Command Tower", "Crane Operation Zone", "High Activity Area",
                "Safety Critical Zone", "Main Work Area Overview"
            ],
            "mobile_inspection": [
                "Foundation Level", "Floor 5 Inspection", "Structural Check Point",
                "Quality Control Station", "Safety Audit Point"
            ],
            "timelapse": [
                "Building Progress - East View", "Building Progress - West View",
                "Construction Overview", "Site Development Timelapse"
            ],
            "drone_aerial": [
                "Aerial Site Overview", "Progress Documentation", "Safety Monitoring",
                "Environmental Assessment"
            ]
        }
        
        locations = camera_locations.get(camera_type_str, ["General Monitoring"])
        location = locations[index % len(locations)]
        
        # Generate realistic stream URL based on camera type
        stream_urls = {
            "fixed_security": f"rtsp://mock-rtsp-server:8554/security/{site['site_id']}/cam{index+1}",
            "ptz_monitoring": f"rtsp://mock-rtsp-server:8554/ptz/{site['site_id']}/cam{index+1}",
            "mobile_inspection": f"rtsp://mock-rtsp-server:8554/mobile/{site['site_id']}/cam{index+1}",
            "timelapse": f"rtsp://mock-rtsp-server:8554/timelapse/{site['site_id']}/cam{index+1}",
            "drone_aerial": f"rtsp://mock-rtsp-server:8554/drone/{site['site_id']}/cam{index+1}"
        }
        
        return CameraInfo(
            camera_id=str(uuid.uuid4()),
            name=f"{site['name']} - {location}",
            camera_type=camera_type,
            status=random.choices(
                [CameraStatus.ONLINE, CameraStatus.OFFLINE, CameraStatus.ERROR],
                weights=[85, 10, 5]
            )[0],
            site_id=site["site_id"],
            location_description=location,
            coordinates=(
                float(site["coordinates"][0]) + random.uniform(-0.001, 0.001),
                float(site["coordinates"][1]) + random.uniform(-0.001, 0.001)
            ),
            stream_url=stream_urls.get(camera_type_str, f"rtsp://mock-rtsp-server:8554/general/{site['site_id']}/cam{index+1}"),
            recording_enabled=True,
            motion_detection=camera_type != CameraType.TIMELAPSE,
            night_vision=camera_type in [CameraType.FIXED_SECURITY, CameraType.PTZ_MONITORING],
            ptz_capable=camera_type == CameraType.PTZ_MONITORING,
            zoom_level=random.uniform(1.0, 4.0) if camera_type == CameraType.PTZ_MONITORING else None,
            resolution=random.choice([StreamQuality.HIGH, StreamQuality.ULTRA]),
            created_at=fake.date_time_between(start_date=site["start_date"], end_date="now"),
            last_seen=fake.date_time_between(start_date="-1h", end_date="now"),
            metadata={
                "installation_height": f"{random.randint(3, 15)}m",
                "viewing_angle": f"{random.randint(45, 180)}°",
                "weather_resistant": True,
                "night_vision_range": f"{random.randint(20, 100)}m" if camera_type != CameraType.TIMELAPSE else None
            }
        )

    def generate_events(self, cameras: List[CameraInfo], days_back: int = 30) -> List[DetectionEvent]:
        """Generate realistic construction site detection events"""
        events = []
        events_per_day = self.config.get("events_per_day", 50)
        
        for day in range(days_back):
            event_date = datetime.now() - timedelta(days=day)
            daily_events = random.randint(events_per_day - 20, events_per_day + 20)
            
            for _ in range(daily_events):
                camera = random.choice(cameras)
                site_data = next(site for site in self.sites_data if site["site_id"] == camera.site_id)
                
                event = self._create_detection_event(camera, site_data, event_date)
                events.append(event)
                
        return sorted(events, key=lambda x: x.timestamp, reverse=True)

    def _create_detection_event(self, camera: CameraInfo, site_data: Dict, base_date: datetime) -> DetectionEvent:
        """Create realistic detection event based on camera type and site"""
        
        # Event types based on camera type and site type
        event_probabilities = {
            CameraType.FIXED_SECURITY: {
                DetectionType.RESTRICTED_ACCESS: 0.3,
                DetectionType.PPE_VIOLATION: 0.25,
                DetectionType.PERSONNEL_COUNT: 0.2,
                DetectionType.SAFETY_HAZARD: 0.15,
                DetectionType.EQUIPMENT_OPERATION: 0.1
            },
            CameraType.PTZ_MONITORING: {
                DetectionType.EQUIPMENT_OPERATION: 0.35,
                DetectionType.SAFETY_HAZARD: 0.25,
                DetectionType.PPE_VIOLATION: 0.2,
                DetectionType.PROGRESS_MILESTONE: 0.15,
                DetectionType.PERSONNEL_COUNT: 0.05
            },
            CameraType.MOBILE_INSPECTION: {
                DetectionType.PROGRESS_MILESTONE: 0.4,
                DetectionType.SAFETY_HAZARD: 0.3,
                DetectionType.PPE_VIOLATION: 0.2,
                DetectionType.EQUIPMENT_OPERATION: 0.1
            },
            CameraType.TIMELAPSE: {
                DetectionType.PROGRESS_MILESTONE: 0.6,
                DetectionType.WEATHER_ALERT: 0.25,
                DetectionType.EQUIPMENT_OPERATION: 0.15
            },
            CameraType.DRONE_AERIAL: {
                DetectionType.PROGRESS_MILESTONE: 0.4,
                DetectionType.SAFETY_HAZARD: 0.3,
                DetectionType.WEATHER_ALERT: 0.2,
                DetectionType.PERSONNEL_COUNT: 0.1
            }
        }
        
        probabilities = event_probabilities.get(camera.camera_type, {
            DetectionType.PPE_VIOLATION: 0.3,
            DetectionType.SAFETY_HAZARD: 0.3,
            DetectionType.EQUIPMENT_OPERATION: 0.4
        })
        
        detection_type = random.choices(
            list(probabilities.keys()),
            weights=list(probabilities.values())
        )[0]
        
        # Generate realistic event details
        event_details = self._get_event_details(detection_type, camera.camera_type, site_data)
        
        # Realistic timing during work hours
        work_hour = random.randint(7, 18)
        work_minute = random.randint(0, 59)
        event_time = base_date.replace(hour=work_hour, minute=work_minute, second=random.randint(0, 59))
        
        return DetectionEvent(
            event_id=str(uuid.uuid4()),
            camera_id=camera.camera_id,
            detection_type=detection_type,
            timestamp=event_time,
            confidence_score=random.uniform(0.7, 0.99),
            bounding_boxes=self._generate_bounding_boxes(detection_type),
            description=event_details["description"],
            severity=event_details["severity"],
            location=camera.location_description,
            personnel_involved=event_details.get("personnel"),
            equipment_involved=event_details.get("equipment"),
            image_url=f"http://mock-server:8555/images/events/{uuid.uuid4()}.jpg",
            video_clip_url=f"http://mock-server:8555/videos/events/{uuid.uuid4()}.mp4",
            acknowledged=random.choice([True, False]) if random.random() > 0.3 else False,
            resolved=random.choice([True, False]) if random.random() > 0.7 else False,
            metadata={
                "weather_conditions": random.choice(["clear", "cloudy", "light_rain", "heavy_rain"]),
                "work_shift": "day" if 7 <= work_hour <= 15 else "evening",
                "site_activity_level": random.choice(["low", "medium", "high"]),
                "detected_objects": event_details.get("objects", [])
            }
        )

    def _get_event_details(self, detection_type: DetectionType, camera_type: CameraType, site_data: Dict) -> Dict[str, Any]:
        """Generate detailed event information based on detection type"""
        
        event_templates = {
            DetectionType.PPE_VIOLATION: {
                "descriptions": [
                    "Worker without hard hat detected in construction zone",
                    "Missing safety vest in high-visibility area", 
                    "Improper safety footwear on construction site",
                    "Worker without safety harness at elevation",
                    "Missing eye protection in welding area"
                ],
                "severity": random.choice(["medium", "high"]),
                "personnel": [fake.name() for _ in range(random.randint(1, 3))],
                "objects": ["person", "hard_hat", "safety_vest"]
            },
            DetectionType.RESTRICTED_ACCESS: {
                "descriptions": [
                    "Unauthorized personnel in restricted construction area",
                    "Vehicle access violation in pedestrian zone",
                    "After-hours access without proper authorization",
                    "Visitor in hard-hat required area without PPE"
                ],
                "severity": random.choice(["medium", "high", "critical"]),
                "personnel": [fake.name() for _ in range(random.randint(1, 2))],
                "objects": ["person", "restricted_zone", "access_barrier"]
            },
            DetectionType.EQUIPMENT_OPERATION: {
                "descriptions": [
                    "Crane operation detected - load lifting in progress",
                    "Excavator movement in designated work zone",
                    "Concrete mixer truck positioning for pour",
                    "Forklift operation in material storage area",
                    "Heavy machinery startup sequence initiated"
                ],
                "severity": "low",
                "equipment": [
                    random.choice(["crane", "excavator", "concrete_mixer", "forklift", "bulldozer"])
                ],
                "objects": ["heavy_equipment", "operator", "work_zone"]
            },
            DetectionType.PERSONNEL_COUNT: {
                "descriptions": [
                    f"Personnel count: {random.randint(15, 45)} workers detected on site",
                    "Shift change detected - personnel movement",
                    "Safety briefing gathering identified",
                    "Work crew assembly in designated area"
                ],
                "severity": "low",
                "personnel": [fake.name() for _ in range(random.randint(5, 15))],
                "objects": ["person", "work_area", "assembly_point"]
            },
            DetectionType.SAFETY_HAZARD: {
                "descriptions": [
                    "Potential fall hazard - unguarded edge detected",
                    "Electrical hazard - exposed wiring identified",
                    "Fire safety concern - blocked emergency exit", 
                    "Material handling hazard - unstable stack",
                    "Slip hazard - wet surface in work area"
                ],
                "severity": random.choice(["high", "critical"]),
                "objects": ["hazard", "safety_barrier", "warning_sign"]
            },
            DetectionType.PROGRESS_MILESTONE: {
                "descriptions": [
                    "Foundation pouring milestone completed",
                    "Structural steel installation phase initiated",
                    "Floor slab completion detected",
                    "Roofing installation milestone reached",
                    "Exterior facade installation progress"
                ],
                "severity": "low",
                "objects": ["construction_progress", "milestone_marker", "completed_work"]
            },
            DetectionType.WEATHER_ALERT: {
                "descriptions": [
                    "Heavy rain detected - work stoppage recommended",
                    "High wind conditions - crane operation suspended",
                    "Lightning alert - outdoor work cessation",
                    "Temperature extreme - worker safety protocol"
                ],
                "severity": random.choice(["medium", "high"]),
                "objects": ["weather_conditions", "safety_protocol"]
            }
        }
        
        template = event_templates.get(detection_type, {
            "descriptions": ["General detection event"],
            "severity": "medium",
            "objects": ["general_object"]
        })
        
        return {
            "description": random.choice(template["descriptions"]),
            "severity": template["severity"],
            "personnel": template.get("personnel"),
            "equipment": template.get("equipment"),
            "objects": template.get("objects", [])
        }

    def _generate_bounding_boxes(self, detection_type: DetectionType) -> List[Dict[str, float]]:
        """Generate realistic bounding boxes for detection events"""
        box_count = {
            DetectionType.PPE_VIOLATION: random.randint(1, 3),
            DetectionType.RESTRICTED_ACCESS: random.randint(1, 2), 
            DetectionType.EQUIPMENT_OPERATION: 1,
            DetectionType.PERSONNEL_COUNT: random.randint(3, 12),
            DetectionType.SAFETY_HAZARD: 1,
            DetectionType.PROGRESS_MILESTONE: random.randint(1, 3),
            DetectionType.WEATHER_ALERT: 0
        }.get(detection_type, 1)
        
        boxes = []
        for _ in range(box_count):
            x1 = random.uniform(0.1, 0.7)
            y1 = random.uniform(0.1, 0.7)
            x2 = x1 + random.uniform(0.1, 0.3)
            y2 = y1 + random.uniform(0.1, 0.3)
            
            boxes.append({
                "x1": min(x1, 1.0),
                "y1": min(y1, 1.0), 
                "x2": min(x2, 1.0),
                "y2": min(y2, 1.0),
                "confidence": random.uniform(0.7, 0.99)
            })
            
        return boxes

    def generate_monitoring_zones(self, cameras: List[CameraInfo]) -> List[MonitoringZone]:
        """Generate realistic monitoring zones for cameras"""
        zones = []
        
        for camera in cameras:
            # Number of zones per camera type
            zone_counts = {
                CameraType.FIXED_SECURITY: random.randint(2, 4),
                CameraType.PTZ_MONITORING: random.randint(3, 6),
                CameraType.MOBILE_INSPECTION: random.randint(1, 3),
                CameraType.TIMELAPSE: random.randint(1, 2),
                CameraType.DRONE_AERIAL: random.randint(2, 4)
            }
            
            zone_count = zone_counts.get(camera.camera_type, 2)
            
            for i in range(zone_count):
                zone = self._create_monitoring_zone(camera, i)
                zones.append(zone)
                
        return zones

    def _create_monitoring_zone(self, camera: CameraInfo, index: int) -> MonitoringZone:
        """Create individual monitoring zone"""
        zone_types_by_camera = {
            CameraType.FIXED_SECURITY: ["safety", "restricted", "equipment"],
            CameraType.PTZ_MONITORING: ["progress", "equipment", "safety"],
            CameraType.MOBILE_INSPECTION: ["progress", "safety"],
            CameraType.TIMELAPSE: ["progress"],
            CameraType.DRONE_AERIAL: ["progress", "safety", "equipment"]
        }
        
        available_types = zone_types_by_camera.get(camera.camera_type, ["safety"])
        zone_type = random.choice(available_types)
        
        # Generate polygon coordinates for the zone
        center_x = random.randint(200, 600)
        center_y = random.randint(150, 450)
        size = random.randint(50, 150)
        
        coordinates = [
            (center_x - size, center_y - size),
            (center_x + size, center_y - size),
            (center_x + size, center_y + size),
            (center_x - size, center_y + size)
        ]
        
        zone_names = {
            "safety": f"Safety Zone {index + 1}",
            "restricted": f"Restricted Area {index + 1}",
            "equipment": f"Equipment Zone {index + 1}",
            "progress": f"Progress Monitor {index + 1}"
        }
        
        return MonitoringZone(
            zone_id=str(uuid.uuid4()),
            camera_id=camera.camera_id,
            name=zone_names.get(zone_type, f"Zone {index + 1}"),
            zone_type=zone_type,
            coordinates=coordinates,
            detection_enabled=True,
            sensitivity=random.uniform(0.6, 0.9),
            alert_threshold=random.randint(1, 5),
            description=f"{zone_type.title()} monitoring zone for {camera.location_description}",
            created_at=fake.date_time_between(start_date=camera.created_at, end_date="now")
        )

    def get_site_analytics(self, site_id: str, start_date: date, end_date: date) -> Dict[str, Any]:
        """Generate realistic site analytics"""
        return {
            "site_id": site_id,
            "analysis_period": {
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat(),
                "total_days": (end_date - start_date).days
            },
            "detection_summary": {
                "total_events": random.randint(150, 500),
                "ppe_violations": random.randint(15, 45),
                "safety_hazards": random.randint(8, 25),
                "equipment_operations": random.randint(80, 200),
                "progress_milestones": random.randint(5, 15),
                "personnel_alerts": random.randint(20, 60)
            },
            "camera_performance": {
                "total_cameras": len([c for c in self.sites_data if c["site_id"] == site_id]),
                "online_cameras": random.randint(6, 8),
                "offline_cameras": random.randint(0, 2),
                "average_uptime": random.uniform(94, 99),
                "total_recording_hours": random.randint(1000, 3000)
            },
            "safety_metrics": {
                "safety_score": random.uniform(85, 98),
                "incident_rate": random.uniform(0.1, 2.5),
                "compliance_rate": random.uniform(88, 97),
                "training_completion": random.uniform(85, 100)
            },
            "productivity_insights": {
                "active_work_hours": random.randint(8, 12),
                "peak_activity_time": f"{random.randint(9, 11)}:00 AM",
                "equipment_utilization": random.uniform(65, 85),
                "weather_impact_days": random.randint(0, 5)
            }
        }