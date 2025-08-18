"""
Real ZoneMinder Connector Implementation
======================================

Production implementation for connecting to actual ZoneMinder systems.
This will be used when switching from mock to real mode.
"""

import asyncio
import aiohttp
from datetime import datetime, timedelta, date
from typing import List, Dict, Optional, Any, AsyncGenerator

from .base_connector import (
    ZoneMinderConnector, CameraInfo, DetectionEvent, MonitoringZone, 
    StreamMetadata, CameraType, CameraStatus, DetectionType, StreamQuality
)

class RealZoneMinderConnector(ZoneMinderConnector):
    """
    Real ZoneMinder connector for production use.
    
    This implementation will connect to actual ZoneMinder APIs and database
    when the real system is ready.
    """

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.host = config.get("host", "localhost")
        self.port = config.get("port", 80)
        self.username = config.get("username", "admin")
        self.password = config.get("password", "admin") 
        self.api_url = config.get("api_url", f"http://{self.host}:{self.port}/zm/api")
        
        self.session: Optional[aiohttp.ClientSession] = None
        self.auth_token: Optional[str] = None
        self.is_initialized = False

    async def initialize(self) -> bool:
        """Initialize connection to real ZoneMinder"""
        try:
            print("🔗 Connecting to Real ZoneMinder...")
            print(f"   📍 Host: {self.host}:{self.port}")
            print(f"   🔐 User: {self.username}")
            
            # Create HTTP session
            self.session = aiohttp.ClientSession()
            
            # Authenticate with ZoneMinder
            auth_success = await self._authenticate()
            if not auth_success:
                print("❌ Authentication failed")
                return False
            
            # Verify connection
            system_info = await self._get_system_info()
            if not system_info:
                print("❌ Failed to get system information")
                return False
                
            self.is_initialized = True
            
            print("✅ Real ZoneMinder connected successfully:")
            print(f"   📊 Version: {system_info.get('version', 'Unknown')}")
            print(f"   📹 Cameras: {system_info.get('camera_count', 0)}")
            print(f"   💾 Storage: {system_info.get('storage_gb', 'Unknown')} GB")
            
            return True
        except Exception as e:
            print(f"❌ Failed to connect to ZoneMinder: {e}")
            return False

    async def shutdown(self) -> None:
        """Clean shutdown of real connector"""
        print("🛑 Disconnecting from Real ZoneMinder...")
        if self.session:
            await self.session.close()
        self.is_initialized = False

    async def _authenticate(self) -> bool:
        """Authenticate with ZoneMinder API"""
        try:
            auth_url = f"{self.api_url}/host/login.json"
            auth_data = {
                "user": self.username,
                "pass": self.password
            }
            
            async with self.session.post(auth_url, json=auth_data) as response:
                if response.status == 200:
                    result = await response.json()
                    self.auth_token = result.get("access_token")
                    return self.auth_token is not None
                return False
        except Exception as e:
            print(f"Authentication error: {e}")
            return False

    async def _get_system_info(self) -> Dict[str, Any]:
        """Get ZoneMinder system information"""
        try:
            headers = {"Authorization": f"Bearer {self.auth_token}"}
            info_url = f"{self.api_url}/host/getVersion.json"
            
            async with self.session.get(info_url, headers=headers) as response:
                if response.status == 200:
                    return await response.json()
                return {}
        except Exception as e:
            print(f"System info error: {e}")
            return {}

    # Camera Management
    async def get_cameras(self, site_id: Optional[str] = None) -> List[CameraInfo]:
        """Get cameras from ZoneMinder"""
        if not self.is_initialized:
            raise RuntimeError("Connector not initialized")
        
        try:
            headers = {"Authorization": f"Bearer {self.auth_token}"}
            cameras_url = f"{self.api_url}/monitors.json"
            
            async with self.session.get(cameras_url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    cameras = []
                    
                    for monitor in data.get("monitors", []):
                        camera = self._convert_monitor_to_camera(monitor, site_id)
                        if camera and (not site_id or camera.site_id == site_id):
                            cameras.append(camera)
                    
                    return cameras
                else:
                    print(f"Failed to get cameras: HTTP {response.status}")
                    return []
                    
        except Exception as e:
            print(f"Error getting cameras: {e}")
            return []

    async def get_camera(self, camera_id: str) -> Optional[CameraInfo]:
        """Get specific camera from ZoneMinder"""
        cameras = await self.get_cameras()
        for camera in cameras:
            if camera.camera_id == camera_id:
                return camera
        return None

    async def create_camera(self, camera_data: Dict[str, Any]) -> CameraInfo:
        """Create new monitor in ZoneMinder"""
        if not self.is_initialized:
            raise RuntimeError("Connector not initialized")
        
        # Convert camera_data to ZoneMinder monitor format
        monitor_data = self._convert_camera_to_monitor(camera_data)
        
        try:
            headers = {"Authorization": f"Bearer {self.auth_token}"}
            create_url = f"{self.api_url}/monitors.json"
            
            async with self.session.post(create_url, json=monitor_data, headers=headers) as response:
                if response.status == 201:
                    result = await response.json()
                    return self._convert_monitor_to_camera(result["monitor"])
                else:
                    raise Exception(f"Failed to create camera: HTTP {response.status}")
                    
        except Exception as e:
            print(f"Error creating camera: {e}")
            raise

    async def update_camera(self, camera_id: str, updates: Dict[str, Any]) -> CameraInfo:
        """Update monitor in ZoneMinder"""
        if not self.is_initialized:
            raise RuntimeError("Connector not initialized")
        
        try:
            headers = {"Authorization": f"Bearer {self.auth_token}"}
            update_url = f"{self.api_url}/monitors/{camera_id}.json"
            
            # Convert updates to ZoneMinder format
            monitor_updates = self._convert_camera_updates(updates)
            
            async with self.session.put(update_url, json=monitor_updates, headers=headers) as response:
                if response.status == 200:
                    return await self.get_camera(camera_id)
                else:
                    raise Exception(f"Failed to update camera: HTTP {response.status}")
                    
        except Exception as e:
            print(f"Error updating camera: {e}")
            raise

    async def delete_camera(self, camera_id: str) -> bool:
        """Delete monitor from ZoneMinder"""
        if not self.is_initialized:
            raise RuntimeError("Connector not initialized")
        
        try:
            headers = {"Authorization": f"Bearer {self.auth_token}"}
            delete_url = f"{self.api_url}/monitors/{camera_id}.json"
            
            async with self.session.delete(delete_url, headers=headers) as response:
                return response.status == 200
                
        except Exception as e:
            print(f"Error deleting camera: {e}")
            return False

    # Stream Management
    async def get_live_stream(self, camera_id: str, quality: StreamQuality = StreamQuality.HIGH) -> StreamMetadata:
        """Get live stream from ZoneMinder"""
        camera = await self.get_camera(camera_id)
        if not camera:
            raise ValueError(f"Camera {camera_id} not found")
        
        # Generate ZoneMinder stream URL
        stream_url = f"rtmp://{self.host}:{self.port}/zm/cgi-bin/nph-zms"
        stream_params = f"?mode=jpeg&monitor={camera_id}&scale=100&maxfps=30"
        
        quality_settings = {
            StreamQuality.LOW: {"scale": 50, "maxfps": 15},
            StreamQuality.MEDIUM: {"scale": 75, "maxfps": 24},
            StreamQuality.HIGH: {"scale": 100, "maxfps": 30},
            StreamQuality.ULTRA: {"scale": 100, "maxfps": 60}
        }
        
        settings = quality_settings.get(quality, quality_settings[StreamQuality.HIGH])
        stream_params = f"?mode=jpeg&monitor={camera_id}&scale={settings['scale']}&maxfps={settings['maxfps']}"
        
        return StreamMetadata(
            camera_id=camera_id,
            stream_url=stream_url + stream_params,
            backup_url=None,
            quality=quality,
            fps=settings['maxfps'],
            codec="MJPEG",
            bitrate=2000,  # Estimated
            is_live=camera.status == CameraStatus.ONLINE,
            viewer_count=0,  # ZoneMinder doesn't typically track this
            uptime_seconds=0  # Would need to calculate from monitor stats
        )

    async def get_stream_snapshot(self, camera_id: str) -> str:
        """Get snapshot from ZoneMinder camera"""
        snapshot_url = f"http://{self.host}:{self.port}/zm/cgi-bin/nph-zms"
        snapshot_params = f"?mode=single&monitor={camera_id}&scale=100"
        
        return snapshot_url + snapshot_params

    async def start_recording(self, camera_id: str, duration_minutes: Optional[int] = None) -> str:
        """Start recording in ZoneMinder"""
        try:
            headers = {"Authorization": f"Bearer {self.auth_token}"}
            record_url = f"{self.api_url}/monitors/alarm/id:{camera_id}/command:on.json"
            
            async with self.session.post(record_url, headers=headers) as response:
                if response.status == 200:
                    recording_id = f"zm_recording_{camera_id}_{int(datetime.now().timestamp())}"
                    return recording_id
                else:
                    raise Exception(f"Failed to start recording: HTTP {response.status}")
                    
        except Exception as e:
            print(f"Error starting recording: {e}")
            raise

    async def stop_recording(self, camera_id: str, recording_id: str) -> bool:
        """Stop recording in ZoneMinder"""
        try:
            headers = {"Authorization": f"Bearer {self.auth_token}"}
            stop_url = f"{self.api_url}/monitors/alarm/id:{camera_id}/command:off.json"
            
            async with self.session.post(stop_url, headers=headers) as response:
                return response.status == 200
                
        except Exception as e:
            print(f"Error stopping recording: {e}")
            return False

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
        """Get events from ZoneMinder"""
        if not self.is_initialized:
            raise RuntimeError("Connector not initialized")
        
        try:
            headers = {"Authorization": f"Bearer {self.auth_token}"}
            events_url = f"{self.api_url}/events.json"
            
            # Build query parameters
            params = {"limit": limit}
            if camera_id:
                params["MonitorId"] = camera_id
            if start_date:
                params["StartDateTime"] = start_date.strftime("%Y-%m-%d %H:%M:%S")
            if end_date:
                params["EndDateTime"] = end_date.strftime("%Y-%m-%d %H:%M:%S")
            
            async with self.session.get(events_url, params=params, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    events = []
                    
                    for zm_event in data.get("events", []):
                        event = self._convert_zm_event_to_detection(zm_event)
                        if event:
                            events.append(event)
                    
                    return events
                else:
                    print(f"Failed to get events: HTTP {response.status}")
                    return []
                    
        except Exception as e:
            print(f"Error getting events: {e}")
            return []

    async def get_event(self, event_id: str) -> Optional[DetectionEvent]:
        """Get specific event from ZoneMinder"""
        events = await self.get_events(limit=1000)  # Get all events and filter
        for event in events:
            if event.event_id == event_id:
                return event
        return None

    async def acknowledge_event(self, event_id: str, user_id: str) -> bool:
        """Acknowledge event in ZoneMinder (may require custom implementation)"""
        # ZoneMinder doesn't have built-in acknowledgment, would need custom field
        print(f"Event {event_id} acknowledged by {user_id} (custom implementation needed)")
        return True

    async def resolve_event(self, event_id: str, user_id: str, resolution_notes: str) -> bool:
        """Resolve event in ZoneMinder (may require custom implementation)"""
        # ZoneMinder doesn't have built-in resolution, would need custom field
        print(f"Event {event_id} resolved by {user_id}: {resolution_notes}")
        return True

    # Monitoring Zones
    async def get_zones(self, camera_id: Optional[str] = None) -> List[MonitoringZone]:
        """Get zones from ZoneMinder"""
        if not self.is_initialized:
            raise RuntimeError("Connector not initialized")
        
        try:
            headers = {"Authorization": f"Bearer {self.auth_token}"}
            zones_url = f"{self.api_url}/zones.json"
            
            params = {}
            if camera_id:
                params["MonitorId"] = camera_id
            
            async with self.session.get(zones_url, params=params, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    zones = []
                    
                    for zm_zone in data.get("zones", []):
                        zone = self._convert_zm_zone_to_monitoring(zm_zone)
                        if zone:
                            zones.append(zone)
                    
                    return zones
                else:
                    print(f"Failed to get zones: HTTP {response.status}")
                    return []
                    
        except Exception as e:
            print(f"Error getting zones: {e}")
            return []

    async def create_zone(self, zone_data: Dict[str, Any]) -> MonitoringZone:
        """Create zone in ZoneMinder"""
        # Implementation for creating ZoneMinder zones
        raise NotImplementedError("Zone creation in real ZoneMinder needs implementation")

    async def update_zone(self, zone_id: str, updates: Dict[str, Any]) -> MonitoringZone:
        """Update zone in ZoneMinder"""
        # Implementation for updating ZoneMinder zones
        raise NotImplementedError("Zone updates in real ZoneMinder needs implementation")

    async def delete_zone(self, zone_id: str) -> bool:
        """Delete zone from ZoneMinder"""
        # Implementation for deleting ZoneMinder zones
        raise NotImplementedError("Zone deletion in real ZoneMinder needs implementation")

    # Analytics and Statistics
    async def get_camera_statistics(self, camera_id: str, start_date: date, end_date: date) -> Dict[str, Any]:
        """Get camera statistics from ZoneMinder"""
        # Implementation for ZoneMinder camera statistics
        return {
            "camera_id": camera_id,
            "note": "Real ZoneMinder statistics implementation needed",
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat()
        }

    async def get_site_analytics(self, site_id: str, start_date: date, end_date: date) -> Dict[str, Any]:
        """Get site analytics from ZoneMinder"""
        # Implementation for ZoneMinder site analytics
        return {
            "site_id": site_id,
            "note": "Real ZoneMinder site analytics implementation needed",
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat()
        }

    # Real-time Event Streaming
    async def stream_events(self, camera_ids: Optional[List[str]] = None) -> AsyncGenerator[DetectionEvent, None]:
        """Stream real-time events from ZoneMinder"""
        # Implementation for real-time ZoneMinder event streaming
        while True:
            await asyncio.sleep(10)  # Poll every 10 seconds
            events = await self.get_events(limit=10)  # Get recent events
            for event in events:
                if not event.acknowledged:  # Only yield new/unacknowledged events
                    yield event

    # System Health
    async def get_system_health(self) -> Dict[str, Any]:
        """Get ZoneMinder system health"""
        if not self.is_initialized:
            raise RuntimeError("Connector not initialized")
        
        # Implementation for ZoneMinder system health
        return {
            "system_status": "connected",
            "note": "Real ZoneMinder health monitoring implementation needed"
        }

    async def get_storage_info(self) -> Dict[str, Any]:
        """Get ZoneMinder storage information"""
        if not self.is_initialized:
            raise RuntimeError("Connector not initialized")
        
        # Implementation for ZoneMinder storage info
        return {
            "note": "Real ZoneMinder storage info implementation needed"
        }

    # Helper methods for data conversion
    def _convert_monitor_to_camera(self, monitor: Dict[str, Any], site_id: Optional[str] = None) -> Optional[CameraInfo]:
        """Convert ZoneMinder monitor to CameraInfo"""
        try:
            monitor_data = monitor.get("Monitor", monitor)
            
            return CameraInfo(
                camera_id=str(monitor_data.get("Id")),
                name=monitor_data.get("Name", "Unknown Camera"),
                camera_type=CameraType.FIXED_SECURITY,  # Default type
                status=CameraStatus.ONLINE if monitor_data.get("Function") != "None" else CameraStatus.OFFLINE,
                site_id=site_id or "default_site",
                location_description=monitor_data.get("Description", ""),
                coordinates=(0.0, 0.0),  # ZoneMinder doesn't store coordinates by default
                stream_url=f"rtmp://{self.host}/zm/monitor_{monitor_data.get('Id')}",
                recording_enabled=monitor_data.get("RecordAudio", "0") == "1",
                motion_detection=monitor_data.get("Function") == "Motion",
                night_vision=False,  # Not available in ZoneMinder by default
                ptz_capable=monitor_data.get("Controllable", "0") == "1",
                created_at=datetime.now(),  # ZoneMinder doesn't track creation time by default
                metadata={
                    "zm_id": monitor_data.get("Id"),
                    "zm_function": monitor_data.get("Function"),
                    "zm_enabled": monitor_data.get("Enabled")
                }
            )
        except Exception as e:
            print(f"Error converting monitor to camera: {e}")
            return None

    def _convert_camera_to_monitor(self, camera_data: Dict[str, Any]) -> Dict[str, Any]:
        """Convert CameraInfo to ZoneMinder monitor format"""
        return {
            "Name": camera_data.get("name", "New Camera"),
            "Description": camera_data.get("location_description", ""),
            "Function": "Motion",  # Default function
            "Enabled": "1",
            "RecordAudio": "1" if camera_data.get("recording_enabled") else "0",
            "Controllable": "1" if camera_data.get("ptz_capable") else "0"
        }

    def _convert_camera_updates(self, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Convert camera updates to ZoneMinder format"""
        zm_updates = {}
        
        if "name" in updates:
            zm_updates["Name"] = updates["name"]
        if "location_description" in updates:
            zm_updates["Description"] = updates["location_description"]
        if "recording_enabled" in updates:
            zm_updates["RecordAudio"] = "1" if updates["recording_enabled"] else "0"
        
        return zm_updates

    def _convert_zm_event_to_detection(self, zm_event: Dict[str, Any]) -> Optional[DetectionEvent]:
        """Convert ZoneMinder event to DetectionEvent"""
        try:
            event_data = zm_event.get("Event", zm_event)
            
            return DetectionEvent(
                event_id=str(event_data.get("Id")),
                camera_id=str(event_data.get("MonitorId")),
                detection_type=DetectionType.EQUIPMENT_OPERATION,  # Default type
                timestamp=datetime.fromisoformat(event_data.get("StartDateTime", datetime.now().isoformat())),
                confidence_score=0.8,  # Default confidence
                bounding_boxes=[],  # ZoneMinder doesn't provide bounding boxes by default
                description=event_data.get("Name", "ZoneMinder Event"),
                severity="medium",
                location=f"Monitor {event_data.get('MonitorId')}",
                image_url=f"http://{self.host}:{self.port}/zm/index.php?view=image&eid={event_data.get('Id')}",
                video_clip_url=f"http://{self.host}:{self.port}/zm/index.php?view=video&eid={event_data.get('Id')}",
                metadata={
                    "zm_event_id": event_data.get("Id"),
                    "zm_frames": event_data.get("Frames"),
                    "zm_alarm_frames": event_data.get("AlarmFrames"),
                    "zm_length": event_data.get("Length")
                }
            )
        except Exception as e:
            print(f"Error converting ZM event to detection: {e}")
            return None

    def _convert_zm_zone_to_monitoring(self, zm_zone: Dict[str, Any]) -> Optional[MonitoringZone]:
        """Convert ZoneMinder zone to MonitoringZone"""
        try:
            zone_data = zm_zone.get("Zone", zm_zone)
            
            # Parse ZoneMinder zone coordinates (typically stored as polygon string)
            coords_str = zone_data.get("Coords", "0,0 100,0 100,100 0,100")
            coordinates = []
            for coord_pair in coords_str.split():
                x, y = map(int, coord_pair.split(","))
                coordinates.append((x, y))
            
            return MonitoringZone(
                zone_id=str(zone_data.get("Id")),
                camera_id=str(zone_data.get("MonitorId")),
                name=zone_data.get("Name", "Unknown Zone"),
                zone_type="safety",  # Default type
                coordinates=coordinates,
                detection_enabled=zone_data.get("CheckMethod") != "Disabled",
                sensitivity=float(zone_data.get("MinAlarmPixels", 25)) / 100.0,
                alert_threshold=int(zone_data.get("MinFilterPixels", 25)),
                description=f"ZoneMinder zone {zone_data.get('Name')}",
                created_at=datetime.now()  # ZoneMinder doesn't track creation time
            )
        except Exception as e:
            print(f"Error converting ZM zone to monitoring zone: {e}")
            return None