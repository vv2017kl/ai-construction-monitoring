"""
RTSP Stream Simulator for Construction Site Mock Data
===================================================

Simulates realistic RTSP streams with construction site activities.
"""

import asyncio
import random
from datetime import datetime
from typing import Dict, List, Optional

class RTSPStreamSimulator:
    """
    Simulates RTSP streams with realistic construction site content.
    
    Features:
    - Multiple camera angles and types
    - Dynamic construction activities
    - Weather and lighting variations
    - Time-based scenario changes
    """

    def __init__(self, port: int = 8554):
        self.port = port
        self.active_streams: Dict[str, Dict] = {}
        self.server_running = False
        
        # Construction activity scenarios
        self.scenarios = {
            "morning_briefing": {
                "description": "Daily safety briefing with workers gathered",
                "activity_level": "high",
                "personnel_count": (15, 25),
                "equipment_active": False,
                "time_range": (7, 9)
            },
            "concrete_pour": {
                "description": "Active concrete pouring operation",
                "activity_level": "very_high", 
                "personnel_count": (8, 12),
                "equipment_active": True,
                "equipment_types": ["concrete_mixer", "crane"],
                "time_range": (9, 15)
            },
            "steel_erection": {
                "description": "Structural steel installation",
                "activity_level": "high",
                "personnel_count": (6, 10),
                "equipment_active": True,
                "equipment_types": ["crane", "forklift"],
                "time_range": (8, 16)
            },
            "material_delivery": {
                "description": "Material delivery and unloading",
                "activity_level": "medium",
                "personnel_count": (4, 8),
                "equipment_active": True,
                "equipment_types": ["forklift", "delivery_truck"],
                "time_range": (6, 18)
            },
            "safety_inspection": {
                "description": "Safety inspection walkthrough",
                "activity_level": "low",
                "personnel_count": (2, 4),
                "equipment_active": False,
                "time_range": (10, 14)
            },
            "end_of_shift": {
                "description": "Workers leaving construction site",
                "activity_level": "medium",
                "personnel_count": (20, 40),
                "equipment_active": False,
                "time_range": (16, 18)
            },
            "night_security": {
                "description": "Night time security monitoring",
                "activity_level": "very_low",
                "personnel_count": (1, 2),
                "equipment_active": False,
                "time_range": (18, 7)
            }
        }

    async def start_server(self):
        """Start the RTSP simulation server"""
        if self.server_running:
            return
            
        print(f"📡 Starting RTSP Simulator on port {self.port}")
        self.server_running = True
        
        # Start background scenario generator
        asyncio.create_task(self._scenario_generator())
        
        print(f"✅ RTSP Simulator started - simulating construction site feeds")

    async def stop_server(self):
        """Stop the RTSP simulation server"""
        self.server_running = False
        self.active_streams.clear()
        print(f"🛑 RTSP Simulator stopped")

    def register_camera_stream(self, camera_id: str, camera_info: Dict):
        """Register a camera for stream simulation"""
        stream_path = self._generate_stream_path(camera_id, camera_info)
        
        self.active_streams[camera_id] = {
            "camera_id": camera_id,
            "camera_type": camera_info.get("camera_type", "fixed_security"),
            "site_id": camera_info.get("site_id"),
            "location": camera_info.get("location_description", "Unknown"),
            "stream_path": stream_path,
            "rtsp_url": f"rtsp://mock-rtsp-server:{self.port}{stream_path}",
            "http_url": f"http://mock-server:8555{stream_path.replace('/rtsp/', '/http/')}",
            "current_scenario": None,
            "last_activity_change": datetime.now(),
            "viewer_count": 0,
            "stream_quality": {
                "resolution": "1920x1080",
                "fps": 30,
                "bitrate": "2.5 Mbps",
                "codec": "H.264"
            }
        }
        
        print(f"📹 Registered stream: {camera_info.get('name', camera_id)}")
        print(f"   📍 RTSP: {self.active_streams[camera_id]['rtsp_url']}")

    def _generate_stream_path(self, camera_id: str, camera_info: Dict) -> str:
        """Generate appropriate stream path based on camera type"""
        camera_type = camera_info.get("camera_type", "fixed_security")
        site_id = camera_info.get("site_id", "default")
        
        path_mapping = {
            "fixed_security": f"/rtsp/security/{site_id}/{camera_id}",
            "ptz_monitoring": f"/rtsp/ptz/{site_id}/{camera_id}",
            "mobile_inspection": f"/rtsp/mobile/{site_id}/{camera_id}",
            "timelapse": f"/rtsp/timelapse/{site_id}/{camera_id}",
            "drone_aerial": f"/rtsp/drone/{site_id}/{camera_id}"
        }
        
        return path_mapping.get(camera_type, f"/rtsp/general/{site_id}/{camera_id}")

    async def _scenario_generator(self):
        """Generate realistic construction scenarios for all active streams"""
        while self.server_running:
            current_hour = datetime.now().hour
            
            # Update scenarios for all active streams
            for camera_id, stream_info in self.active_streams.items():
                # Determine appropriate scenario based on time and camera type
                scenario = self._select_scenario_for_camera(
                    stream_info["camera_type"], 
                    current_hour,
                    stream_info["location"]
                )
                
                if scenario != stream_info.get("current_scenario"):
                    stream_info["current_scenario"] = scenario
                    stream_info["last_activity_change"] = datetime.now()
                    
                    print(f"🎬 {stream_info.get('location', camera_id)}: {scenario['description']}")
            
            # Wait before next scenario update
            await asyncio.sleep(random.randint(300, 900))  # 5-15 minutes

    def _select_scenario_for_camera(self, camera_type: str, current_hour: int, location: str) -> Dict:
        """Select appropriate scenario based on camera type, time, and location"""
        
        # Filter scenarios by time
        available_scenarios = []
        for scenario_name, scenario in self.scenarios.items():
            time_range = scenario["time_range"]
            if time_range[0] <= current_hour <= time_range[1]:
                available_scenarios.append((scenario_name, scenario))
        
        # If no time-appropriate scenarios, use night security
        if not available_scenarios:
            available_scenarios = [("night_security", self.scenarios["night_security"])]
        
        # Weight scenarios based on camera type and location
        weighted_scenarios = []
        for scenario_name, scenario in available_scenarios:
            weight = self._calculate_scenario_weight(camera_type, location, scenario_name)
            weighted_scenarios.append((scenario_name, scenario, weight))
        
        # Select scenario based on weights
        total_weight = sum(weight for _, _, weight in weighted_scenarios)
        if total_weight == 0:
            return available_scenarios[0][1]  # Fallback to first available
        
        rand_val = random.uniform(0, total_weight)
        cumulative = 0
        
        for scenario_name, scenario, weight in weighted_scenarios:
            cumulative += weight
            if rand_val <= cumulative:
                scenario_copy = scenario.copy()
                scenario_copy["name"] = scenario_name
                return scenario_copy
        
        return available_scenarios[0][1]  # Fallback

    def _calculate_scenario_weight(self, camera_type: str, location: str, scenario_name: str) -> float:
        """Calculate probability weight for scenario based on camera context"""
        
        # Base weights for camera types
        camera_weights = {
            "fixed_security": {
                "morning_briefing": 0.8,
                "material_delivery": 0.9,
                "safety_inspection": 0.7,
                "end_of_shift": 0.9,
                "night_security": 1.0,
                "concrete_pour": 0.3,
                "steel_erection": 0.4
            },
            "ptz_monitoring": {
                "concrete_pour": 1.0,
                "steel_erection": 1.0,
                "material_delivery": 0.8,
                "morning_briefing": 0.6,
                "safety_inspection": 0.9,
                "end_of_shift": 0.5,
                "night_security": 0.3
            },
            "mobile_inspection": {
                "safety_inspection": 1.0,
                "concrete_pour": 0.7,
                "steel_erection": 0.8,
                "morning_briefing": 0.4,
                "material_delivery": 0.3,
                "end_of_shift": 0.2,
                "night_security": 0.1
            },
            "timelapse": {
                "concrete_pour": 1.0,
                "steel_erection": 1.0,
                "material_delivery": 0.6,
                "morning_briefing": 0.3,
                "safety_inspection": 0.4,
                "end_of_shift": 0.3,
                "night_security": 0.8
            },
            "drone_aerial": {
                "concrete_pour": 0.9,
                "steel_erection": 0.9,
                "safety_inspection": 1.0,
                "morning_briefing": 0.7,
                "material_delivery": 0.5,
                "end_of_shift": 0.6,
                "night_security": 0.2
            }
        }
        
        # Location-based modifiers
        location_modifiers = {
            "gate": {"material_delivery": 1.5, "end_of_shift": 1.3},
            "office": {"morning_briefing": 1.4, "safety_inspection": 1.2},
            "crane": {"steel_erection": 1.5, "concrete_pour": 1.3},
            "storage": {"material_delivery": 1.4},
            "foundation": {"concrete_pour": 1.5},
            "perimeter": {"night_security": 1.4},
            "overview": {"steel_erection": 1.2, "concrete_pour": 1.2}
        }
        
        base_weight = camera_weights.get(camera_type, {}).get(scenario_name, 0.5)
        
        # Apply location modifiers
        location_lower = location.lower()
        for loc_key, modifiers in location_modifiers.items():
            if loc_key in location_lower:
                modifier = modifiers.get(scenario_name, 1.0)
                base_weight *= modifier
                break
        
        return base_weight

    def get_stream_info(self, camera_id: str) -> Optional[Dict]:
        """Get current stream information for a camera"""
        if camera_id in self.active_streams:
            stream_info = self.active_streams[camera_id].copy()
            
            # Add current scenario details
            scenario = stream_info.get("current_scenario") or {}
            stream_info["current_activity"] = {
                "scenario": scenario.get("name", "unknown"),
                "description": scenario.get("description", "No activity"),
                "activity_level": scenario.get("activity_level", "low"),
                "estimated_personnel": random.randint(
                    *scenario.get("personnel_count", (0, 1))
                ) if scenario.get("personnel_count") else 0,
                "equipment_active": scenario.get("equipment_active", False),
                "equipment_types": scenario.get("equipment_types", [])
            }
            
            return stream_info
        return None

    def get_all_streams(self) -> Dict[str, Dict]:
        """Get information for all active streams"""
        return {
            camera_id: self.get_stream_info(camera_id) 
            for camera_id in self.active_streams.keys()
        }

    def simulate_viewer_activity(self, camera_id: str, action: str = "connect"):
        """Simulate viewer connecting/disconnecting from stream"""
        if camera_id in self.active_streams:
            if action == "connect":
                self.active_streams[camera_id]["viewer_count"] += 1
            elif action == "disconnect" and self.active_streams[camera_id]["viewer_count"] > 0:
                self.active_streams[camera_id]["viewer_count"] -= 1

    def get_server_statistics(self) -> Dict:
        """Get overall server statistics"""
        total_streams = len(self.active_streams)
        total_viewers = sum(stream["viewer_count"] for stream in self.active_streams.values())
        active_scenarios = len(set(
            stream.get("current_scenario", {}).get("name", "none") 
            for stream in self.active_streams.values()
        ))
        
        return {
            "server_running": self.server_running,
            "port": self.port,
            "total_active_streams": total_streams,
            "total_viewers": total_viewers,
            "active_scenarios": active_scenarios,
            "uptime_minutes": 0,  # Would calculate from start time
            "streams_by_type": {
                camera_type: len([
                    s for s in self.active_streams.values() 
                    if s["camera_type"] == camera_type
                ])
                for camera_type in ["fixed_security", "ptz_monitoring", "mobile_inspection", "timelapse", "drone_aerial"]
            }
        }

# Global RTSP simulator instance
rtsp_simulator = RTSPStreamSimulator()

async def initialize_rtsp_simulator(cameras: List[Dict]):
    """Initialize RTSP simulator with camera list"""
    await rtsp_simulator.start_server()
    
    for camera in cameras:
        rtsp_simulator.register_camera_stream(
            camera.get("camera_id", camera.get("id")),
            camera
        )
    
    return rtsp_simulator

async def shutdown_rtsp_simulator():
    """Shutdown RTSP simulator"""
    await rtsp_simulator.stop_server()