"""
ZoneMinder Connector Configuration
=================================

Configuration management for both mock and real ZoneMinder connections.
"""

import os
from typing import Dict, Any, Optional
from enum import Enum

class ConnectorMode(Enum):
    MOCK = "mock"
    REAL = "real"
    
class ZoneMinderConfig:
    """Configuration class for ZoneMinder connector"""
    
    def __init__(self):
        # Determine mode from environment variable
        self.mode = ConnectorMode(os.getenv("ZONEMINDER_MODE", "mock"))
        
        # Common configuration
        self.debug = os.getenv("ZONEMINDER_DEBUG", "false").lower() == "true"
        self.log_level = os.getenv("ZONEMINDER_LOG_LEVEL", "INFO")
        
        # Mock configuration
        self.mock_config = {
            "stream_simulation": True,
            "rtsp_port": int(os.getenv("MOCK_RTSP_PORT", "8554")),
            "http_port": int(os.getenv("MOCK_HTTP_PORT", "8555")),
            "sites_count": int(os.getenv("MOCK_SITES_COUNT", "3")),
            "cameras_per_site": int(os.getenv("MOCK_CAMERAS_PER_SITE", "8")),
            "events_per_day": int(os.getenv("MOCK_EVENTS_PER_DAY", "25")),
            "zones_per_camera": int(os.getenv("MOCK_ZONES_PER_CAMERA", "2")),
            "enable_realtime_simulation": True,
            "event_generation_interval": int(os.getenv("MOCK_EVENT_INTERVAL", "30")),  # seconds
            "camera_status_change_probability": 0.02,  # 2% chance per check
            "seasonal_variations": True,
            "weather_integration": True,
            # Construction industry specific settings
            "construction_types": [
                "high_rise_building",
                "residential_complex", 
                "commercial_mall",
                "infrastructure_highway",
                "industrial_facility",
                "renovation_project"
            ],
            "peak_activity_hours": {
                "start": 7,  # 7 AM
                "end": 18    # 6 PM
            },
            "weekend_activity_reduction": 0.3,  # 70% reduction on weekends
            "night_activity_reduction": 0.1,   # 90% reduction at night
        }
        
        # Real ZoneMinder configuration
        self.real_config = {
            "host": os.getenv("ZONEMINDER_HOST", "localhost"),
            "port": int(os.getenv("ZONEMINDER_PORT", "80")),
            "username": os.getenv("ZONEMINDER_USER", "admin"),
            "password": os.getenv("ZONEMINDER_PASS", "admin"),
            "ssl": os.getenv("ZONEMINDER_SSL", "false").lower() == "true",
            "api_version": os.getenv("ZONEMINDER_API_VERSION", "v1"),
            "timeout": int(os.getenv("ZONEMINDER_TIMEOUT", "30")),
            "max_retries": int(os.getenv("ZONEMINDER_MAX_RETRIES", "3")),
            "retry_delay": int(os.getenv("ZONEMINDER_RETRY_DELAY", "5")),
            "connection_pool_size": int(os.getenv("ZONEMINDER_POOL_SIZE", "10")),
        }
        
    def get_config(self) -> Dict[str, Any]:
        """Get configuration based on current mode"""
        base_config = {
            "mode": self.mode.value,
            "debug": self.debug,
            "log_level": self.log_level
        }
        
        if self.mode == ConnectorMode.MOCK:
            base_config.update(self.mock_config)
        else:
            base_config.update(self.real_config)
            
        return base_config
    
    def is_mock_mode(self) -> bool:
        """Check if running in mock mode"""
        return self.mode == ConnectorMode.MOCK
    
    def is_real_mode(self) -> bool:
        """Check if running in real mode"""
        return self.mode == ConnectorMode.REAL

# Global configuration instance
_config = ZoneMinderConfig()

def get_config() -> Dict[str, Any]:
    """Get the current configuration"""
    return _config.get_config()

def get_connector():
    """Factory function to get appropriate connector based on configuration"""
    from ..mock_connector import MockZoneMinderConnector
    
    config = get_config()
    
    if _config.is_mock_mode():
        print("🎭 Using Mock ZoneMinder Connector")
        return MockZoneMinderConnector(config)
    else:
        print("🔗 Using Real ZoneMinder Connector")
        try:
            from ..real_connector import RealZoneMinderConnector
            return RealZoneMinderConnector(config)
        except ImportError as e:
            print(f"⚠️ Real connector dependencies not available: {e}")
            print("🎭 Falling back to Mock ZoneMinder Connector")
            return MockZoneMinderConnector(config)

def set_mode(mode: str):
    """Set the connector mode (for testing purposes)"""
    global _config 
    _config.mode = ConnectorMode(mode)
    
def get_mode() -> str:
    """Get current connector mode"""
    return _config.mode.value

# Configuration presets for different environments
DEVELOPMENT_CONFIG = {
    "mode": "mock",
    "debug": True,
    "sites_count": 2,
    "cameras_per_site": 4,
    "events_per_day": 15,
    "enable_realtime_simulation": True
}

TESTING_CONFIG = {
    "mode": "mock", 
    "debug": False,
    "sites_count": 1,
    "cameras_per_site": 2,
    "events_per_day": 5,
    "enable_realtime_simulation": False
}

PRODUCTION_CONFIG = {
    "mode": "real",
    "debug": False,
    "max_retries": 5,
    "timeout": 60,
    "connection_pool_size": 20
}

def load_preset(preset_name: str):
    """Load a configuration preset"""
    presets = {
        "development": DEVELOPMENT_CONFIG,
        "testing": TESTING_CONFIG,
        "production": PRODUCTION_CONFIG
    }
    
    if preset_name not in presets:
        raise ValueError(f"Unknown preset: {preset_name}")
    
    preset = presets[preset_name]
    for key, value in preset.items():
        os.environ[f"ZONEMINDER_{key.upper()}"] = str(value)
    
    # Reinitialize configuration
    global _config
    _config = ZoneMinderConfig()