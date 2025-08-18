"""
Configuration Settings for ZoneMinder Connector
==============================================

Manages configuration and factory method for connector instantiation.
"""

import os
from typing import Optional

# Configuration constants
ZONEMINDER_MODE = os.getenv("ZONEMINDER_MODE", "mock").lower()  # "mock" or "real"
MOCK_DATA_QUALITY = os.getenv("MOCK_DATA_QUALITY", "high").lower()  # "low", "medium", "high"
STREAM_SIMULATION = os.getenv("STREAM_SIMULATION", "true").lower() == "true"
REALISTIC_TIMING = os.getenv("REALISTIC_TIMING", "true").lower() == "true"
MOCK_RTSP_PORT = int(os.getenv("MOCK_RTSP_PORT", "8554"))
MOCK_HTTP_PORT = int(os.getenv("MOCK_HTTP_PORT", "8555"))

# Real ZoneMinder settings (for when switching to real mode)
ZONEMINDER_HOST = os.getenv("ZONEMINDER_HOST", "localhost")
ZONEMINDER_PORT = int(os.getenv("ZONEMINDER_PORT", "80"))
ZONEMINDER_USERNAME = os.getenv("ZONEMINDER_USERNAME", "admin")
ZONEMINDER_PASSWORD = os.getenv("ZONEMINDER_PASSWORD", "admin")
ZONEMINDER_API_URL = f"http://{ZONEMINDER_HOST}:{ZONEMINDER_PORT}/zm/api"

# Mock data configuration
MOCK_CONFIG = {
    "sites_count": 5,
    "cameras_per_site": 8,
    "events_per_day": 50,
    "data_quality": MOCK_DATA_QUALITY,
    "stream_simulation": STREAM_SIMULATION,
    "realistic_timing": REALISTIC_TIMING,
    "construction_scenarios": [
        "high_rise_building",
        "infrastructure_project", 
        "residential_development",
        "industrial_facility",
        "renovation_project"
    ],
    "rtsp_port": MOCK_RTSP_PORT,
    "http_port": MOCK_HTTP_PORT
}

def get_connector():
    """
    Factory function to get the appropriate connector based on configuration
    """
    if ZONEMINDER_MODE == "mock":
        from ..mock_connector import MockZoneMinderConnector
        return MockZoneMinderConnector(MOCK_CONFIG)
    elif ZONEMINDER_MODE == "real":
        from ..real_connector import RealZoneMinderConnector
        return RealZoneMinderConnector({
            "host": ZONEMINDER_HOST,
            "port": ZONEMINDER_PORT,
            "username": ZONEMINDER_USERNAME,
            "password": ZONEMINDER_PASSWORD,
            "api_url": ZONEMINDER_API_URL
        })
    else:
        raise ValueError(f"Invalid ZONEMINDER_MODE: {ZONEMINDER_MODE}. Must be 'mock' or 'real'")

def switch_mode(new_mode: str) -> None:
    """
    Switch connector mode at runtime
    """
    global ZONEMINDER_MODE
    if new_mode.lower() not in ["mock", "real"]:
        raise ValueError(f"Invalid mode: {new_mode}. Must be 'mock' or 'real'")
    
    ZONEMINDER_MODE = new_mode.lower()
    os.environ["ZONEMINDER_MODE"] = ZONEMINDER_MODE

def get_current_mode() -> str:
    """Get the current connector mode"""
    return ZONEMINDER_MODE

def is_mock_mode() -> bool:
    """Check if currently in mock mode"""
    return ZONEMINDER_MODE == "mock"

def is_real_mode() -> bool:
    """Check if currently in real mode"""
    return ZONEMINDER_MODE == "real"