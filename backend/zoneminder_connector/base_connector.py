"""
Abstract Base Connector for ZoneMinder Integration
=================================================

Defines the interface that both mock and real ZoneMinder connectors must implement.
This ensures seamless switching between modes without frontend changes.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Any, AsyncGenerator
from datetime import datetime, date
from dataclasses import dataclass
from enum import Enum

class CameraStatus(Enum):
    ONLINE = "online"
    OFFLINE = "offline"
    ERROR = "error"
    MAINTENANCE = "maintenance"

class CameraType(Enum):
    FIXED_SECURITY = "fixed_security"
    PTZ_MONITORING = "ptz_monitoring"
    MOBILE_INSPECTION = "mobile_inspection"
    DRONE_AERIAL = "drone_aerial"
    TIMELAPSE = "timelapse"

class DetectionType(Enum):
    PPE_VIOLATION = "ppe_violation"
    RESTRICTED_ACCESS = "restricted_access"
    EQUIPMENT_OPERATION = "equipment_operation"
    PERSONNEL_COUNT = "personnel_count"
    SAFETY_HAZARD = "safety_hazard"
    PROGRESS_MILESTONE = "progress_milestone"
    WEATHER_ALERT = "weather_alert"

class StreamQuality(Enum):
    LOW = "480p"
    MEDIUM = "720p"
    HIGH = "1080p"
    ULTRA = "4K"

@dataclass
class CameraInfo:
    """Camera information structure"""
    camera_id: str
    name: str
    camera_type: CameraType
    status: CameraStatus
    site_id: str
    location_description: str
    coordinates: tuple[float, float]  # (latitude, longitude)
    stream_url: str
    recording_enabled: bool
    motion_detection: bool
    night_vision: bool
    ptz_capable: bool
    zoom_level: Optional[float] = None
    resolution: StreamQuality = StreamQuality.HIGH
    created_at: datetime = None
    last_seen: datetime = None
    metadata: Dict[str, Any] = None

@dataclass  
class DetectionEvent:
    """AI detection event structure"""
    event_id: str
    camera_id: str
    detection_type: DetectionType
    timestamp: datetime
    confidence_score: float
    bounding_boxes: List[Dict[str, float]]  # [{"x1": 0.1, "y1": 0.1, "x2": 0.9, "y2": 0.9}]
    description: str
    severity: str  # "low", "medium", "high", "critical"
    location: str
    personnel_involved: Optional[List[str]] = None
    equipment_involved: Optional[List[str]] = None
    image_url: Optional[str] = None
    video_clip_url: Optional[str] = None
    acknowledged: bool = False
    resolved: bool = False
    metadata: Dict[str, Any] = None

@dataclass
class MonitoringZone:
    """Camera monitoring zone definition"""
    zone_id: str
    camera_id: str
    name: str
    zone_type: str  # "safety", "progress", "equipment", "restricted"
    coordinates: List[tuple[int, int]]  # Polygon points
    detection_enabled: bool
    sensitivity: float  # 0.0 to 1.0
    alert_threshold: int
    description: str
    created_at: datetime = None

@dataclass
class StreamMetadata:
    """Live stream metadata"""
    camera_id: str
    stream_url: str
    backup_url: Optional[str]
    quality: StreamQuality
    fps: int
    codec: str
    bitrate: int
    is_live: bool
    viewer_count: int = 0
    uptime_seconds: int = 0

class ZoneMinderConnector(ABC):
    """
    Abstract base class for ZoneMinder connectors.
    
    This interface ensures that both mock and real implementations
    provide the same API, enabling seamless switching.
    """

    @abstractmethod
    async def initialize(self) -> bool:
        """Initialize the connector and verify connectivity"""
        pass

    @abstractmethod
    async def shutdown(self) -> None:
        """Clean shutdown of the connector"""
        pass

    # Camera Management
    @abstractmethod
    async def get_cameras(self, site_id: Optional[str] = None) -> List[CameraInfo]:
        """Get all cameras or cameras for a specific site"""
        pass

    @abstractmethod
    async def get_camera(self, camera_id: str) -> Optional[CameraInfo]:
        """Get specific camera information"""
        pass

    @abstractmethod
    async def create_camera(self, camera_data: Dict[str, Any]) -> CameraInfo:
        """Create a new camera configuration"""
        pass

    @abstractmethod
    async def update_camera(self, camera_id: str, updates: Dict[str, Any]) -> CameraInfo:
        """Update camera settings"""
        pass

    @abstractmethod
    async def delete_camera(self, camera_id: str) -> bool:
        """Delete a camera configuration"""
        pass

    # Stream Management
    @abstractmethod
    async def get_live_stream(self, camera_id: str, quality: StreamQuality = StreamQuality.HIGH) -> StreamMetadata:
        """Get live stream URL and metadata for a camera"""
        pass

    @abstractmethod
    async def get_stream_snapshot(self, camera_id: str) -> str:
        """Get current snapshot image URL from camera"""
        pass

    @abstractmethod
    async def start_recording(self, camera_id: str, duration_minutes: Optional[int] = None) -> str:
        """Start recording from a camera, returns recording_id"""
        pass

    @abstractmethod
    async def stop_recording(self, camera_id: str, recording_id: str) -> bool:
        """Stop an active recording"""
        pass

    # Detection Events
    @abstractmethod
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
        pass

    @abstractmethod
    async def get_event(self, event_id: str) -> Optional[DetectionEvent]:
        """Get specific detection event details"""
        pass

    @abstractmethod
    async def acknowledge_event(self, event_id: str, user_id: str) -> bool:
        """Acknowledge a detection event"""
        pass

    @abstractmethod
    async def resolve_event(self, event_id: str, user_id: str, resolution_notes: str) -> bool:
        """Mark an event as resolved"""
        pass

    # Monitoring Zones
    @abstractmethod
    async def get_zones(self, camera_id: Optional[str] = None) -> List[MonitoringZone]:
        """Get monitoring zones for camera(s)"""
        pass

    @abstractmethod
    async def create_zone(self, zone_data: Dict[str, Any]) -> MonitoringZone:
        """Create a new monitoring zone"""
        pass

    @abstractmethod
    async def update_zone(self, zone_id: str, updates: Dict[str, Any]) -> MonitoringZone:
        """Update monitoring zone settings"""
        pass

    @abstractmethod
    async def delete_zone(self, zone_id: str) -> bool:
        """Delete a monitoring zone"""
        pass

    # Analytics and Statistics
    @abstractmethod
    async def get_camera_statistics(
        self, 
        camera_id: str, 
        start_date: date, 
        end_date: date
    ) -> Dict[str, Any]:
        """Get camera performance and detection statistics"""
        pass

    @abstractmethod
    async def get_site_analytics(
        self, 
        site_id: str, 
        start_date: date, 
        end_date: date
    ) -> Dict[str, Any]:
        """Get site-wide analytics and insights"""
        pass

    # Real-time Event Streaming (for websockets)
    @abstractmethod
    async def stream_events(self, camera_ids: Optional[List[str]] = None) -> AsyncGenerator[DetectionEvent, None]:
        """Stream real-time detection events"""
        pass

    # System Health
    @abstractmethod
    async def get_system_health(self) -> Dict[str, Any]:
        """Get ZoneMinder system health status"""
        pass

    @abstractmethod
    async def get_storage_info(self) -> Dict[str, Any]:
        """Get storage usage and capacity information"""
        pass