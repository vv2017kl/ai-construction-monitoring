"""
ZoneMinder Connector Library for AI-Construction Platform
========================================================

This connector provides seamless abstraction between the AI-Construction platform 
and ZoneMinder, supporting both mock and real implementations.

Features:
- Abstract connector interface for easy mode switching
- Rich construction industry mock data
- RTSP stream simulation
- Real ZoneMinder integration (when ready)
- No frontend changes required when switching modes
"""

from .base_connector import ZoneMinderConnector
from .mock_connector import MockZoneMinderConnector
from .real_connector import RealZoneMinderConnector
from .config.settings import get_connector

# Factory function for easy connector instantiation
def get_zoneminder_connector() -> ZoneMinderConnector:
    """
    Factory function to get the appropriate ZoneMinder connector
    based on configuration settings.
    
    Returns:
        ZoneMinderConnector: Configured connector instance
    """
    return get_connector()

__version__ = "1.0.0"
__all__ = [
    "ZoneMinderConnector",
    "MockZoneMinderConnector", 
    "RealZoneMinderConnector",
    "get_zoneminder_connector"
]