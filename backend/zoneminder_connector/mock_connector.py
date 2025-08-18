"""
Mock ZoneMinder Connector Implementation
======================================

Provides rich, realistic construction industry mock data for development and testing.
"""

import asyncio
import random
from datetime import datetime, timedelta, date
from typing import List, Dict, Optional, Any, AsyncGenerator

from .base_connector import (
    ZoneMinderConnector, CameraInfo, DetectionEvent, MonitoringZone, 
    StreamMetadata, CameraType, CameraStatus, DetectionType, StreamQuality
)
from .mock_data.generators import ConstructionDataGenerator

class MockZoneMinderConnector(ZoneMinderConnector):
    """
    Mock implementation of ZoneMinder connector with rich construction industry data.
    
    Provides realistic simulation for development without requiring actual ZoneMinder installation.
    """

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.data_generator = ConstructionDataGenerator(config)
        self.cameras: List[CameraInfo] = []
        self.events: List[DetectionEvent] = []
        self.zones: List[MonitoringZone] = []
        self.is_initialized = False
        
        # Stream server configuration
        self.rtsp_port = config.get("rtsp_port", 8554)
        self.http_port = config.get("http_port", 8555)
        
    async def initialize(self) -> bool:
        """Initialize the mock connector with generated data"""
        try:
            print("🚀 Initializing Mock ZoneMinder Connector...")
            
            # Generate mock data
            print("📹 Generating construction site cameras...")
            self.cameras = self.data_generator.generate_cameras()
            
            print("🎯 Generating detection events...")
            self.events = self.data_generator.generate_events(self.cameras, days_back=30)
            
            print("🔍 Generating monitoring zones...")
            self.zones = self.data_generator.generate_monitoring_zones(self.cameras)
            
            # Start mock stream server (simulated)
            if self.config.get("stream_simulation", True):
                await self._start_stream_server()
            
            self.is_initialized = True
            
            print(f"✅ Mock ZoneMinder initialized successfully:")
            print(f"   📹 {len(self.cameras)} cameras across {len(self.data_generator.sites_data)} sites")
            print(f"   🎯 {len(self.events)} detection events")
            print(f"   🔍 {len(self.zones)} monitoring zones")
            print(f"   📡 RTSP streams available on port {self.rtsp_port}")
            
            return True
        except Exception as e:
            print(f"❌ Failed to initialize mock connector: {e}")
            return False

    async def shutdown(self) -> None:
        """Clean shutdown of the mock connector"""
        print("🛑 Shutting down Mock ZoneMinder Connector...")
        self.is_initialized = False

    # Camera Management
    async def get_cameras(self, site_id: Optional[str] = None) -> List[CameraInfo]:
        """Get all cameras or cameras for a specific site"""
        if not self.is_initialized:
            await self.initialize()
            
        if site_id:
            return [cam for cam in self.cameras if cam.site_id == site_id]
        return self.cameras.copy()

    async def get_camera(self, camera_id: str) -> Optional[CameraInfo]:
        """Get specific camera information"""
        if not self.is_initialized:
            await self.initialize()
            
        for camera in self.cameras:
            if camera.camera_id == camera_id:
                # Simulate real-time status updates
                if random.random() < 0.05:  # 5% chance of status change
                    camera.status = random.choice([CameraStatus.ONLINE, CameraStatus.OFFLINE])
                camera.last_seen = datetime.now()
                return camera
        return None

    async def create_camera(self, camera_data: Dict[str, Any]) -> CameraInfo:
        """Create a new camera configuration"""
        # Simulate camera creation
        camera = CameraInfo(
            camera_id=camera_data.get("camera_id", f"cam_{len(self.cameras)+1}"),
            name=camera_data.get("name", f"New Camera {len(self.cameras)+1}"),
            camera_type=CameraType(camera_data.get("camera_type", "fixed_security")),
            status=CameraStatus.ONLINE,
            site_id=camera_data.get("site_id"),
            location_description=camera_data.get("location_description", "New Location"),
            coordinates=tuple(camera_data.get("coordinates", [0.0, 0.0])),
            stream_url=f"rtsp://mock-rtsp-server:{self.rtsp_port}/new/{camera_data.get('camera_id', f'cam_{len(self.cameras)+1}')}",
            recording_enabled=camera_data.get("recording_enabled", True),
            motion_detection=camera_data.get("motion_detection", True),
            night_vision=camera_data.get("night_vision", False),
            ptz_capable=camera_data.get("ptz_capable", False),
            created_at=datetime.now()
        )
        
        self.cameras.append(camera)
        print(f"📹 Created new camera: {camera.name}")
        return camera

    async def update_camera(self, camera_id: str, updates: Dict[str, Any]) -> CameraInfo:
        """Update camera settings"""
        camera = await self.get_camera(camera_id)
        if not camera:
            raise ValueError(f"Camera {camera_id} not found")
        
        # Update camera properties
        for key, value in updates.items():
            if hasattr(camera, key):
                setattr(camera, key, value)
                
        print(f"📹 Updated camera: {camera.name}")
        return camera

    async def delete_camera(self, camera_id: str) -> bool:
        """Delete a camera configuration"""
        for i, camera in enumerate(self.cameras):
            if camera.camera_id == camera_id:
                self.cameras.pop(i)
                print(f"📹 Deleted camera: {camera.name}")
                return True
        return False

    # Stream Management
    async def get_live_stream(self, camera_id: str, quality: StreamQuality = StreamQuality.HIGH) -> StreamMetadata:
        """Get live stream URL and metadata for a camera"""
        camera = await self.get_camera(camera_id)
        if not camera:
            raise ValueError(f"Camera {camera_id} not found")
        
        # Generate realistic stream metadata
        return StreamMetadata(
            camera_id=camera_id,
            stream_url=camera.stream_url,
            backup_url=camera.stream_url.replace("rtsp://", "http://").replace(":8554", ":8555"),
            quality=quality,
            fps=random.choice([15, 24, 30]),
            codec="H.264",
            bitrate=random.randint(1000, 5000),
            is_live=camera.status == CameraStatus.ONLINE,
            viewer_count=random.randint(0, 5),
            uptime_seconds=random.randint(3600, 86400)
        )

    async def get_stream_snapshot(self, camera_id: str) -> str:
        """Get current snapshot image URL from camera"""
        camera = await self.get_camera(camera_id)
        if not camera:
            raise ValueError(f"Camera {camera_id} not found")
            
        # Return mock snapshot URL with timestamp for uniqueness
        timestamp = int(datetime.now().timestamp())
        return f"http://mock-server:{self.http_port}/snapshots/{camera_id}/{timestamp}.jpg"

    async def start_recording(self, camera_id: str, duration_minutes: Optional[int] = None) -> str:
        """Start recording from a camera, returns recording_id"""
        camera = await self.get_camera(camera_id)
        if not camera:
            raise ValueError(f"Camera {camera_id} not found")
            
        recording_id = f"rec_{camera_id}_{int(datetime.now().timestamp())}"
        print(f"🎬 Started recording {recording_id} for camera {camera.name}")
        return recording_id

    async def stop_recording(self, camera_id: str, recording_id: str) -> bool:
        """Stop an active recording"""
        print(f"⏹️ Stopped recording {recording_id}")
        return True

    # Detection Events
    async def get_events(
        self, 
        camera_id: Optional[str] = None,
        detection_type: Optional[DetectionType] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        severity: Optional[str] = None,
        limit: int = 100
    ) -> List[DetectionEvent]:
        """Get detection events with filtering options"""
        if not self.is_initialized:
            await self.initialize()
            
        filtered_events = self.events.copy()
        
        # Apply filters
        if camera_id:
            filtered_events = [e for e in filtered_events if e.camera_id == camera_id]
            
        if detection_type:
            filtered_events = [e for e in filtered_events if e.detection_type == detection_type]
            
        if start_date:
            filtered_events = [e for e in filtered_events if e.timestamp >= start_date]
            
        if end_date:
            filtered_events = [e for e in filtered_events if e.timestamp <= end_date]
            
        if severity:
            filtered_events = [e for e in filtered_events if e.severity == severity]
            
        # Simulate new events being added (5% chance)
        if random.random() < 0.05 and len(self.cameras) > 0:
            new_event = self.data_generator._create_detection_event(
                random.choice(self.cameras),
                random.choice(self.data_generator.sites_data),
                datetime.now()
            )
            self.events.insert(0, new_event)
            filtered_events.insert(0, new_event)
            
        return filtered_events[:limit]

    async def get_event(self, event_id: str) -> Optional[DetectionEvent]:
        """Get specific detection event details"""
        if not self.is_initialized:
            await self.initialize()
            
        for event in self.events:
            if event.event_id == event_id:
                return event
        return None

    async def acknowledge_event(self, event_id: str, user_id: str) -> bool:
        """Acknowledge a detection event"""
        event = await self.get_event(event_id)
        if event:
            event.acknowledged = True
            print(f"✅ Event {event_id} acknowledged by {user_id}")
            return True
        return False

    async def resolve_event(self, event_id: str, user_id: str, resolution_notes: str) -> bool:
        """Mark an event as resolved"""
        event = await self.get_event(event_id)
        if event:
            event.resolved = True
            event.metadata = event.metadata or {}
            event.metadata["resolved_by"] = user_id
            event.metadata["resolution_notes"] = resolution_notes
            event.metadata["resolved_at"] = datetime.now().isoformat()
            print(f"✅ Event {event_id} resolved by {user_id}")
            return True
        return False

    # Monitoring Zones
    async def get_zones(self, camera_id: Optional[str] = None) -> List[MonitoringZone]:
        """Get monitoring zones for camera(s)"""
        if not self.is_initialized:
            await self.initialize()
            
        if camera_id:
            return [zone for zone in self.zones if zone.camera_id == camera_id]
        return self.zones.copy()

    async def create_zone(self, zone_data: Dict[str, Any]) -> MonitoringZone:
        """Create a new monitoring zone"""
        zone = MonitoringZone(
            zone_id=zone_data.get("zone_id", f"zone_{len(self.zones)+1}"),
            camera_id=zone_data.get("camera_id"),
            name=zone_data.get("name", f"New Zone {len(self.zones)+1}"),
            zone_type=zone_data.get("zone_type", "safety"),
            coordinates=zone_data.get("coordinates", [(100, 100), (200, 100), (200, 200), (100, 200)]),
            detection_enabled=zone_data.get("detection_enabled", True),
            sensitivity=zone_data.get("sensitivity", 0.8),
            alert_threshold=zone_data.get("alert_threshold", 3),
            description=zone_data.get("description", "New monitoring zone"),
            created_at=datetime.now()
        )
        
        self.zones.append(zone)
        print(f"🔍 Created new monitoring zone: {zone.name}")
        return zone

    async def update_zone(self, zone_id: str, updates: Dict[str, Any]) -> MonitoringZone:
        """Update monitoring zone settings"""
        for zone in self.zones:
            if zone.zone_id == zone_id:
                for key, value in updates.items():
                    if hasattr(zone, key):
                        setattr(zone, key, value)
                print(f"🔍 Updated monitoring zone: {zone.name}")
                return zone
        
        raise ValueError(f"Zone {zone_id} not found")

    async def delete_zone(self, zone_id: str) -> bool:
        """Delete a monitoring zone"""
        for i, zone in enumerate(self.zones):
            if zone.zone_id == zone_id:
                self.zones.pop(i)
                print(f"🔍 Deleted monitoring zone: {zone.name}")
                return True
        return False

    # Analytics and Statistics
    async def get_camera_statistics(
        self, 
        camera_id: str, 
        start_date: date, 
        end_date: date
    ) -> Dict[str, Any]:
        """Get camera performance and detection statistics"""
        camera = await self.get_camera(camera_id)
        if not camera:
            raise ValueError(f"Camera {camera_id} not found")
        
        # Generate realistic camera statistics
        total_days = (end_date - start_date).days
        return {
            "camera_id": camera_id,
            "camera_name": camera.name,
            "analysis_period": {
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat(),
                "total_days": total_days
            },
            "performance_metrics": {
                "uptime_percentage": random.uniform(94, 99),
                "total_recording_hours": random.randint(total_days * 10, total_days * 24),
                "average_fps": random.randint(20, 30),
                "stream_interruptions": random.randint(0, 5),
                "maintenance_events": random.randint(0, 2)
            },
            "detection_statistics": {
                "total_events": random.randint(10, 100),
                "events_by_type": {
                    "ppe_violation": random.randint(2, 20),
                    "safety_hazard": random.randint(1, 15),
                    "equipment_operation": random.randint(5, 40),
                    "personnel_count": random.randint(1, 25)
                },
                "average_confidence": random.uniform(0.75, 0.95),
                "false_positive_rate": random.uniform(0.02, 0.08)
            },
            "storage_usage": {
                "total_gb": random.uniform(50, 500),
                "recordings_count": random.randint(total_days * 2, total_days * 10),
                "oldest_recording": (start_date - timedelta(days=random.randint(1, 30))).isoformat()
            }
        }

    async def get_site_analytics(
        self, 
        site_id: str, 
        start_date: date, 
        end_date: date
    ) -> Dict[str, Any]:
        """Get site-wide analytics and insights"""
        return self.data_generator.get_site_analytics(site_id, start_date, end_date)

    # Real-time Event Streaming
    async def stream_events(self, camera_ids: Optional[List[str]] = None) -> AsyncGenerator[DetectionEvent, None]:
        """Stream real-time detection events"""
        print("📡 Starting real-time event streaming...")
        
        while True:
            await asyncio.sleep(random.uniform(5, 30))  # Random interval between events
            
            # Generate new event
            if len(self.cameras) > 0:
                cameras_to_use = self.cameras
                if camera_ids:
                    cameras_to_use = [c for c in self.cameras if c.camera_id in camera_ids]
                
                if cameras_to_use:
                    camera = random.choice(cameras_to_use)
                    site_data = next(site for site in self.data_generator.sites_data if site["site_id"] == camera.site_id)
                    
                    event = self.data_generator._create_detection_event(camera, site_data, datetime.now())
                    self.events.insert(0, event)  # Add to beginning of events list
                    
                    yield event

    # System Health
    async def get_system_health(self) -> Dict[str, Any]:
        """Get ZoneMinder system health status"""
        return {
            "system_status": "operational",
            "version": "1.36.12 (Mock)",
            "uptime_hours": random.randint(100, 1000),
            "cpu_usage": random.uniform(15, 45),
            "memory_usage": random.uniform(30, 70),
            "disk_usage": random.uniform(40, 80),
            "database_status": "connected",
            "active_processes": random.randint(15, 30),
            "total_cameras": len(self.cameras),
            "online_cameras": len([c for c in self.cameras if c.status == CameraStatus.ONLINE]),
            "recording_cameras": len([c for c in self.cameras if c.recording_enabled]),
            "alerts_enabled": True,
            "motion_detection_enabled": True,
            "last_restart": (datetime.now() - timedelta(hours=random.randint(1, 72))).isoformat()
        }

    async def get_storage_info(self) -> Dict[str, Any]:
        """Get storage usage and capacity information"""
        return {
            "total_capacity_gb": random.randint(500, 2000),
            "used_space_gb": random.randint(200, 800),
            "available_space_gb": random.randint(300, 1200),
            "usage_percentage": random.uniform(30, 80),
            "retention_policy_days": random.choice([7, 14, 30, 60]),
            "oldest_recording": (datetime.now() - timedelta(days=random.randint(7, 60))).isoformat(),
            "newest_recording": datetime.now().isoformat(),
            "total_recordings": random.randint(1000, 5000),
            "cleanup_last_run": (datetime.now() - timedelta(hours=random.randint(1, 24))).isoformat(),
            "backup_status": "enabled",
            "compression_ratio": random.uniform(0.3, 0.7)
        }

    async def _start_stream_server(self):
        """Initialize mock stream server (simulated)"""
        print(f"📡 Mock RTSP server starting on port {self.rtsp_port}")
        print(f"🖼️ Mock HTTP media server starting on port {self.http_port}")
        
        # In a real implementation, this would start actual RTSP/HTTP servers
        # For now, we just simulate the initialization
        await asyncio.sleep(0.1)  # Simulate startup time
        
        print(f"✅ Mock stream servers initialized")

    def get_mock_statistics(self) -> Dict[str, Any]:
        """Get statistics about the mock data generated"""
        return {
            "total_sites": len(self.data_generator.sites_data),
            "total_cameras": len(self.cameras),
            "total_events": len(self.events),
            "total_zones": len(self.zones),
            "cameras_by_type": {
                camera_type.value: len([c for c in self.cameras if c.camera_type == camera_type])
                for camera_type in CameraType
            },
            "events_by_type": {
                event_type.value: len([e for e in self.events if e.detection_type == event_type])
                for event_type in DetectionType
            },
            "sites_info": [
                {
                    "site_id": site["site_id"],
                    "name": site["name"],
                    "type": site["type"],
                    "camera_count": len([c for c in self.cameras if c.site_id == site["site_id"]])
                }
                for site in self.data_generator.sites_data
            ]
        }