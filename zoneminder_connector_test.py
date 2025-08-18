#!/usr/bin/env python3
"""
ZoneMinder Connector Testing Script
==================================

Comprehensive testing for the ZoneMinder connector library including:
1. Connector Factory and Configuration
2. Mock Connector Functionality  
3. Mock Data Generators
4. RTSP Stream Simulator
5. Integration Testing
"""

import asyncio
import sys
import os
import json
from datetime import datetime, date, timedelta
from typing import Dict, List, Any

# Add backend directory to path
sys.path.append('/app/backend')

# Import ZoneMinder connector components
from zoneminder_connector.config.settings import (
    ZoneMinderConfig, ConnectorMode, get_config, get_connector, 
    set_mode, get_mode, load_preset
)
from zoneminder_connector.base_connector import (
    CameraType, CameraStatus, DetectionType, StreamQuality
)
from zoneminder_connector.mock_connector import MockZoneMinderConnector
from zoneminder_connector.mock_data.generators import ConstructionDataGenerator
from zoneminder_connector.stream_server.rtsp_simulator import RTSPStreamSimulator

class ZoneMinderConnectorTester:
    """Main test class for ZoneMinder connector functionality"""
    
    def __init__(self):
        self.test_results = []
        self.connector = None
        self.rtsp_simulator = None
        
    def log_test_result(self, test_name: str, success: bool, message: str = "", details: Dict = None):
        """Log test result"""
        result = {
            "test_name": test_name,
            "success": success,
            "message": message,
            "details": details or {},
            "timestamp": datetime.now().isoformat()
        }
        self.test_results.append(result)
        
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if message:
            print(f"    {message}")
        if not success and details:
            print(f"    Details: {details}")
    
    async def run_all_tests(self):
        """Run comprehensive ZoneMinder connector tests"""
        print("🎭 ZoneMinder Connector Comprehensive Testing")
        print("=" * 60)
        
        # Test 1: Configuration and Factory
        await self.test_configuration_management()
        await self.test_connector_factory()
        
        # Test 2: Mock Connector Core Functionality
        await self.test_mock_connector_initialization()
        await self.test_camera_management()
        await self.test_stream_management()
        await self.test_detection_events()
        await self.test_monitoring_zones()
        await self.test_analytics_functionality()
        await self.test_system_health()
        
        # Test 3: Mock Data Generators
        await self.test_construction_data_generator()
        await self.test_site_data_generation()
        await self.test_camera_data_generation()
        await self.test_event_data_generation()
        await self.test_analytics_data_generation()
        
        # Test 4: RTSP Stream Simulator
        await self.test_rtsp_simulator()
        await self.test_stream_scenarios()
        
        # Test 5: Integration Testing
        await self.test_end_to_end_integration()
        
        # Generate test report
        self.generate_test_report()
    
    async def test_configuration_management(self):
        """Test configuration loading and management"""
        print("\n📋 Testing Configuration Management")
        
        try:
            # Test default configuration
            config = get_config()
            self.log_test_result(
                "Configuration Loading",
                isinstance(config, dict) and "mode" in config,
                f"Loaded config with mode: {config.get('mode')}"
            )
            
            # Test mode switching
            original_mode = get_mode()
            set_mode("mock")
            mock_mode = get_mode()
            set_mode("real")
            real_mode = get_mode()
            set_mode(original_mode)  # Restore
            
            self.log_test_result(
                "Mode Switching",
                mock_mode == "mock" and real_mode == "real",
                f"Successfully switched modes: mock={mock_mode}, real={real_mode}"
            )
            
            # Test configuration presets
            load_preset("testing")
            testing_config = get_config()
            self.log_test_result(
                "Configuration Presets",
                testing_config.get("sites_count") == 1,
                f"Testing preset loaded with sites_count: {testing_config.get('sites_count')}"
            )
            
        except Exception as e:
            self.log_test_result("Configuration Management", False, str(e))
    
    async def test_connector_factory(self):
        """Test connector factory pattern"""
        print("\n🏭 Testing Connector Factory")
        
        try:
            # Test mock connector creation
            set_mode("mock")
            mock_connector = get_connector()
            self.log_test_result(
                "Mock Connector Factory",
                isinstance(mock_connector, MockZoneMinderConnector),
                f"Created mock connector: {type(mock_connector).__name__}"
            )
            
            # Test configuration injection
            config = mock_connector.config
            self.log_test_result(
                "Configuration Injection",
                isinstance(config, dict) and "mode" in config,
                f"Connector received config with {len(config)} parameters"
            )
            
        except Exception as e:
            self.log_test_result("Connector Factory", False, str(e))
    
    async def test_mock_connector_initialization(self):
        """Test mock connector initialization"""
        print("\n🚀 Testing Mock Connector Initialization")
        
        try:
            # Create and initialize connector
            set_mode("mock")
            self.connector = get_connector()
            
            # Test initialization
            init_success = await self.connector.initialize()
            self.log_test_result(
                "Connector Initialization",
                init_success and self.connector.is_initialized,
                f"Connector initialized with {len(self.connector.cameras)} cameras"
            )
            
            # Test data generation
            cameras_count = len(self.connector.cameras)
            events_count = len(self.connector.events)
            zones_count = len(self.connector.zones)
            
            self.log_test_result(
                "Mock Data Generation",
                cameras_count > 0 and events_count > 0 and zones_count > 0,
                f"Generated {cameras_count} cameras, {events_count} events, {zones_count} zones"
            )
            
        except Exception as e:
            self.log_test_result("Mock Connector Initialization", False, str(e))
    
    async def test_camera_management(self):
        """Test camera management operations"""
        print("\n📹 Testing Camera Management")
        
        if not self.connector:
            self.log_test_result("Camera Management", False, "Connector not initialized")
            return
        
        try:
            # Test get all cameras
            all_cameras = await self.connector.get_cameras()
            self.log_test_result(
                "Get All Cameras",
                len(all_cameras) > 0,
                f"Retrieved {len(all_cameras)} cameras"
            )
            
            if all_cameras:
                # Test get specific camera
                test_camera = all_cameras[0]
                camera = await self.connector.get_camera(test_camera.camera_id)
                self.log_test_result(
                    "Get Specific Camera",
                    camera is not None and camera.camera_id == test_camera.camera_id,
                    f"Retrieved camera: {camera.name if camera else 'None'}"
                )
                
                # Test get cameras by site
                site_cameras = await self.connector.get_cameras(test_camera.site_id)
                self.log_test_result(
                    "Get Cameras by Site",
                    len(site_cameras) > 0 and all(c.site_id == test_camera.site_id for c in site_cameras),
                    f"Retrieved {len(site_cameras)} cameras for site {test_camera.site_id}"
                )
                
                # Test camera creation
                new_camera_data = {
                    "camera_id": "test_cam_001",
                    "name": "Test Camera",
                    "camera_type": "fixed_security",
                    "site_id": test_camera.site_id,
                    "location_description": "Test Location",
                    "coordinates": [47.6062, -122.3321]
                }
                created_camera = await self.connector.create_camera(new_camera_data)
                self.log_test_result(
                    "Create Camera",
                    created_camera.camera_id == "test_cam_001",
                    f"Created camera: {created_camera.name}"
                )
                
                # Test camera update
                updates = {"name": "Updated Test Camera"}
                updated_camera = await self.connector.update_camera("test_cam_001", updates)
                self.log_test_result(
                    "Update Camera",
                    updated_camera.name == "Updated Test Camera",
                    f"Updated camera name to: {updated_camera.name}"
                )
                
                # Test camera deletion
                delete_success = await self.connector.delete_camera("test_cam_001")
                self.log_test_result(
                    "Delete Camera",
                    delete_success,
                    "Successfully deleted test camera"
                )
            
        except Exception as e:
            self.log_test_result("Camera Management", False, str(e))
    
    async def test_stream_management(self):
        """Test stream management operations"""
        print("\n📡 Testing Stream Management")
        
        if not self.connector:
            self.log_test_result("Stream Management", False, "Connector not initialized")
            return
        
        try:
            cameras = await self.connector.get_cameras()
            if not cameras:
                self.log_test_result("Stream Management", False, "No cameras available")
                return
            
            test_camera = cameras[0]
            
            # Test get live stream
            stream_metadata = await self.connector.get_live_stream(test_camera.camera_id)
            self.log_test_result(
                "Get Live Stream",
                stream_metadata.camera_id == test_camera.camera_id and stream_metadata.stream_url,
                f"Stream URL: {stream_metadata.stream_url[:50]}..."
            )
            
            # Test get stream snapshot
            snapshot_url = await self.connector.get_stream_snapshot(test_camera.camera_id)
            self.log_test_result(
                "Get Stream Snapshot",
                snapshot_url and "snapshots" in snapshot_url,
                f"Snapshot URL: {snapshot_url[:50]}..."
            )
            
            # Test start recording
            recording_id = await self.connector.start_recording(test_camera.camera_id, 5)
            self.log_test_result(
                "Start Recording",
                recording_id and recording_id.startswith("rec_"),
                f"Recording ID: {recording_id}"
            )
            
            # Test stop recording
            stop_success = await self.connector.stop_recording(test_camera.camera_id, recording_id)
            self.log_test_result(
                "Stop Recording",
                stop_success,
                "Successfully stopped recording"
            )
            
        except Exception as e:
            self.log_test_result("Stream Management", False, str(e))
    
    async def test_detection_events(self):
        """Test detection event operations"""
        print("\n🎯 Testing Detection Events")
        
        if not self.connector:
            self.log_test_result("Detection Events", False, "Connector not initialized")
            return
        
        try:
            # Test get all events
            all_events = await self.connector.get_events()
            self.log_test_result(
                "Get All Events",
                len(all_events) > 0,
                f"Retrieved {len(all_events)} events"
            )
            
            if all_events:
                # Test get specific event
                test_event = all_events[0]
                event = await self.connector.get_event(test_event.event_id)
                self.log_test_result(
                    "Get Specific Event",
                    event is not None and event.event_id == test_event.event_id,
                    f"Retrieved event: {event.description[:50] if event else 'None'}..."
                )
                
                # Test event filtering by camera
                cameras = await self.connector.get_cameras()
                if cameras:
                    camera_events = await self.connector.get_events(camera_id=cameras[0].camera_id)
                    self.log_test_result(
                        "Filter Events by Camera",
                        all(e.camera_id == cameras[0].camera_id for e in camera_events),
                        f"Retrieved {len(camera_events)} events for camera"
                    )
                
                # Test event filtering by detection type
                ppe_events = await self.connector.get_events(detection_type=DetectionType.PPE_VIOLATION)
                self.log_test_result(
                    "Filter Events by Type",
                    all(e.detection_type == DetectionType.PPE_VIOLATION for e in ppe_events),
                    f"Retrieved {len(ppe_events)} PPE violation events"
                )
                
                # Test event filtering by date range
                end_date = datetime.now()
                start_date = end_date - timedelta(days=7)
                recent_events = await self.connector.get_events(start_date=start_date, end_date=end_date)
                self.log_test_result(
                    "Filter Events by Date",
                    all(start_date <= e.timestamp <= end_date for e in recent_events),
                    f"Retrieved {len(recent_events)} events from last 7 days"
                )
                
                # Test acknowledge event
                ack_success = await self.connector.acknowledge_event(test_event.event_id, "test_user")
                self.log_test_result(
                    "Acknowledge Event",
                    ack_success,
                    f"Acknowledged event: {test_event.event_id}"
                )
                
                # Test resolve event
                resolve_success = await self.connector.resolve_event(
                    test_event.event_id, "test_user", "Test resolution"
                )
                self.log_test_result(
                    "Resolve Event",
                    resolve_success,
                    f"Resolved event: {test_event.event_id}"
                )
            
        except Exception as e:
            self.log_test_result("Detection Events", False, str(e))
    
    async def test_monitoring_zones(self):
        """Test monitoring zone operations"""
        print("\n🔍 Testing Monitoring Zones")
        
        if not self.connector:
            self.log_test_result("Monitoring Zones", False, "Connector not initialized")
            return
        
        try:
            # Test get all zones
            all_zones = await self.connector.get_zones()
            self.log_test_result(
                "Get All Zones",
                len(all_zones) > 0,
                f"Retrieved {len(all_zones)} zones"
            )
            
            if all_zones:
                # Test get zones by camera
                test_zone = all_zones[0]
                camera_zones = await self.connector.get_zones(test_zone.camera_id)
                self.log_test_result(
                    "Get Zones by Camera",
                    all(z.camera_id == test_zone.camera_id for z in camera_zones),
                    f"Retrieved {len(camera_zones)} zones for camera"
                )
                
                # Test create zone
                cameras = await self.connector.get_cameras()
                if cameras:
                    new_zone_data = {
                        "zone_id": "test_zone_001",
                        "camera_id": cameras[0].camera_id,
                        "name": "Test Safety Zone",
                        "zone_type": "safety",
                        "coordinates": [(100, 100), (200, 100), (200, 200), (100, 200)],
                        "detection_enabled": True,
                        "sensitivity": 0.8,
                        "alert_threshold": 2,
                        "description": "Test monitoring zone"
                    }
                    created_zone = await self.connector.create_zone(new_zone_data)
                    self.log_test_result(
                        "Create Zone",
                        created_zone.zone_id == "test_zone_001",
                        f"Created zone: {created_zone.name}"
                    )
                    
                    # Test update zone
                    updates = {"name": "Updated Test Zone", "sensitivity": 0.9}
                    updated_zone = await self.connector.update_zone("test_zone_001", updates)
                    self.log_test_result(
                        "Update Zone",
                        updated_zone.name == "Updated Test Zone" and updated_zone.sensitivity == 0.9,
                        f"Updated zone: {updated_zone.name}"
                    )
                    
                    # Test delete zone
                    delete_success = await self.connector.delete_zone("test_zone_001")
                    self.log_test_result(
                        "Delete Zone",
                        delete_success,
                        "Successfully deleted test zone"
                    )
            
        except Exception as e:
            self.log_test_result("Monitoring Zones", False, str(e))
    
    async def test_analytics_functionality(self):
        """Test analytics and statistics"""
        print("\n📊 Testing Analytics Functionality")
        
        if not self.connector:
            self.log_test_result("Analytics Functionality", False, "Connector not initialized")
            return
        
        try:
            cameras = await self.connector.get_cameras()
            if not cameras:
                self.log_test_result("Analytics Functionality", False, "No cameras available")
                return
            
            test_camera = cameras[0]
            start_date = date.today() - timedelta(days=30)
            end_date = date.today()
            
            # Test camera statistics
            camera_stats = await self.connector.get_camera_statistics(
                test_camera.camera_id, start_date, end_date
            )
            self.log_test_result(
                "Camera Statistics",
                "performance_metrics" in camera_stats and "detection_statistics" in camera_stats,
                f"Retrieved stats for camera: {camera_stats.get('camera_name', 'Unknown')}"
            )
            
            # Test site analytics
            site_analytics = await self.connector.get_site_analytics(
                test_camera.site_id, start_date, end_date
            )
            self.log_test_result(
                "Site Analytics",
                "site_info" in site_analytics and "safety_metrics" in site_analytics,
                f"Retrieved analytics for site: {site_analytics.get('site_info', {}).get('name', 'Unknown')}"
            )
            
        except Exception as e:
            self.log_test_result("Analytics Functionality", False, str(e))
    
    async def test_system_health(self):
        """Test system health monitoring"""
        print("\n🏥 Testing System Health")
        
        if not self.connector:
            self.log_test_result("System Health", False, "Connector not initialized")
            return
        
        try:
            # Test system health
            health_info = await self.connector.get_system_health()
            self.log_test_result(
                "System Health",
                "system_status" in health_info and "total_cameras" in health_info,
                f"System status: {health_info.get('system_status', 'Unknown')}"
            )
            
            # Test storage info
            storage_info = await self.connector.get_storage_info()
            self.log_test_result(
                "Storage Information",
                "total_capacity_gb" in storage_info and "used_space_gb" in storage_info,
                f"Storage usage: {storage_info.get('usage_percentage', 0):.1f}%"
            )
            
        except Exception as e:
            self.log_test_result("System Health", False, str(e))
    
    async def test_construction_data_generator(self):
        """Test construction data generator"""
        print("\n🏗️ Testing Construction Data Generator")
        
        try:
            # Test data generator initialization
            config = {"sites_count": 2, "cameras_per_site": 4, "events_per_day": 10}
            generator = ConstructionDataGenerator(config)
            
            self.log_test_result(
                "Data Generator Initialization",
                len(generator.sites_data) == 2,
                f"Generated {len(generator.sites_data)} construction sites"
            )
            
            # Test camera generation
            cameras = generator.generate_cameras()
            expected_cameras = 2 * 4  # sites * cameras_per_site
            self.log_test_result(
                "Camera Generation",
                len(cameras) == expected_cameras,
                f"Generated {len(cameras)} cameras (expected {expected_cameras})"
            )
            
            # Test event generation
            events = generator.generate_events(cameras, days_back=7)
            self.log_test_result(
                "Event Generation",
                len(events) > 0,
                f"Generated {len(events)} events over 7 days"
            )
            
            # Test monitoring zones generation
            zones = generator.generate_monitoring_zones(cameras)
            self.log_test_result(
                "Zone Generation",
                len(zones) > 0,
                f"Generated {len(zones)} monitoring zones"
            )
            
        except Exception as e:
            self.log_test_result("Construction Data Generator", False, str(e))
    
    async def test_site_data_generation(self):
        """Test site data generation"""
        print("\n🏢 Testing Site Data Generation")
        
        try:
            from zoneminder_connector.mock_data.generators import SiteDataGenerator
            
            config = {"construction_types": ["high_rise_building", "residential_complex"]}
            site_generator = SiteDataGenerator(config)
            
            # Test site generation
            sites = site_generator.generate_sites(3)
            self.log_test_result(
                "Site Data Generation",
                len(sites) == 3 and all("site_id" in site for site in sites),
                f"Generated {len(sites)} construction sites with complete data"
            )
            
            # Verify site data completeness
            test_site = sites[0]
            required_fields = ["name", "type", "location", "coordinates", "contractor", "workers_count"]
            has_required_fields = all(field in test_site for field in required_fields)
            
            self.log_test_result(
                "Site Data Completeness",
                has_required_fields,
                f"Site contains all required fields: {list(test_site.keys())[:5]}..."
            )
            
        except Exception as e:
            self.log_test_result("Site Data Generation", False, str(e))
    
    async def test_camera_data_generation(self):
        """Test camera data generation"""
        print("\n📹 Testing Camera Data Generation")
        
        try:
            from zoneminder_connector.mock_data.generators import CameraDataGenerator
            
            config = {"rtsp_port": 8554}
            camera_generator = CameraDataGenerator(config)
            
            # Create test site data
            site_data = {
                "site_id": "test_site_001",
                "name": "Test Construction Site",
                "type": "high_rise_building",
                "coordinates": (47.6062, -122.3321),
                "hazard_level": "high",
                "weather_sensitive": True
            }
            
            # Test camera generation for site
            cameras = camera_generator.generate_site_cameras(site_data, 6)
            self.log_test_result(
                "Camera Data Generation",
                len(cameras) == 6 and all(cam.site_id == "test_site_001" for cam in cameras),
                f"Generated {len(cameras)} cameras for construction site"
            )
            
            # Test camera type distribution
            camera_types = [cam.camera_type for cam in cameras]
            unique_types = set(camera_types)
            self.log_test_result(
                "Camera Type Diversity",
                len(unique_types) > 1,
                f"Generated {len(unique_types)} different camera types: {list(unique_types)}"
            )
            
            # Test zone generation for cameras
            test_camera = cameras[0]
            zones = camera_generator.generate_camera_zones(test_camera, 3)
            self.log_test_result(
                "Camera Zone Generation",
                len(zones) == 3 and all(zone.camera_id == test_camera.camera_id for zone in zones),
                f"Generated {len(zones)} monitoring zones for camera"
            )
            
        except Exception as e:
            self.log_test_result("Camera Data Generation", False, str(e))
    
    async def test_event_data_generation(self):
        """Test event data generation"""
        print("\n🎯 Testing Event Data Generation")
        
        try:
            from zoneminder_connector.mock_data.generators import EventDataGenerator
            
            config = {
                "peak_activity_hours": {"start": 7, "end": 18},
                "weekend_activity_reduction": 0.3,
                "seasonal_variations": True
            }
            event_generator = EventDataGenerator(config)
            
            # Create test data
            from zoneminder_connector.base_connector import CameraInfo, CameraType, CameraStatus
            
            test_camera = CameraInfo(
                camera_id="test_cam_001",
                name="Test Camera",
                camera_type=CameraType.FIXED_SECURITY,
                status=CameraStatus.ONLINE,
                site_id="test_site_001",
                location_description="Main Entrance",
                coordinates=(47.6062, -122.3321),
                stream_url="rtsp://test",
                recording_enabled=True,
                motion_detection=True,
                night_vision=True,
                ptz_capable=False
            )
            
            site_data = {
                "site_id": "test_site_001",
                "name": "Test Site",
                "type": "high_rise_building",
                "hazard_level": "high"
            }
            
            # Test single event creation
            event = event_generator.create_single_event(test_camera, site_data, datetime.now())
            self.log_test_result(
                "Single Event Generation",
                event.camera_id == "test_cam_001" and event.event_id,
                f"Generated event: {event.description[:50]}..."
            )
            
            # Test daily events generation
            cameras = [test_camera]
            sites_data = [site_data]
            daily_events = event_generator.generate_daily_events(
                cameras, sites_data, datetime.now(), 5
            )
            self.log_test_result(
                "Daily Events Generation",
                len(daily_events) > 0,
                f"Generated {len(daily_events)} events for today"
            )
            
        except Exception as e:
            self.log_test_result("Event Data Generation", False, str(e))
    
    async def test_analytics_data_generation(self):
        """Test analytics data generation"""
        print("\n📊 Testing Analytics Data Generation")
        
        try:
            from zoneminder_connector.mock_data.generators import AnalyticsDataGenerator
            
            config = {}
            analytics_generator = AnalyticsDataGenerator(config)
            
            # Test site data
            site_data = {
                "site_id": "test_site_001",
                "name": "Test Construction Site",
                "type": "high_rise_building",
                "workers_count": 120,
                "safety_incidents_mtd": 2,
                "equipment_inventory": [{"type": "crane"}, {"type": "excavator"}]
            }
            
            # Test analytics generation
            start_date = date.today() - timedelta(days=30)
            end_date = date.today()
            
            analytics = analytics_generator.generate_site_analytics(site_data, start_date, end_date)
            
            required_sections = [
                "site_info", "safety_metrics", "productivity_metrics", 
                "equipment_analytics", "personnel_analytics"
            ]
            has_all_sections = all(section in analytics for section in required_sections)
            
            self.log_test_result(
                "Analytics Data Generation",
                has_all_sections,
                f"Generated analytics with {len(analytics)} sections"
            )
            
            # Test safety metrics detail
            safety_metrics = analytics.get("safety_metrics", {})
            has_safety_details = "incident_summary" in safety_metrics and "safety_scores" in safety_metrics
            
            self.log_test_result(
                "Safety Analytics Detail",
                has_safety_details,
                f"Safety metrics include incident tracking and scoring"
            )
            
        except Exception as e:
            self.log_test_result("Analytics Data Generation", False, str(e))
    
    async def test_rtsp_simulator(self):
        """Test RTSP stream simulator"""
        print("\n📡 Testing RTSP Stream Simulator")
        
        try:
            # Initialize RTSP simulator
            self.rtsp_simulator = RTSPStreamSimulator(port=8554)
            
            # Test server start
            await self.rtsp_simulator.start_server()
            self.log_test_result(
                "RTSP Server Start",
                self.rtsp_simulator.server_running,
                f"RTSP simulator started on port {self.rtsp_simulator.port}"
            )
            
            # Test camera stream registration
            camera_info = {
                "camera_id": "test_cam_001",
                "name": "Test Camera",
                "camera_type": "fixed_security",
                "site_id": "test_site_001",
                "location_description": "Main Entrance"
            }
            
            self.rtsp_simulator.register_camera_stream("test_cam_001", camera_info)
            
            # Test stream info retrieval
            stream_info = self.rtsp_simulator.get_stream_info("test_cam_001")
            self.log_test_result(
                "Stream Registration",
                stream_info is not None and "rtsp_url" in stream_info,
                f"Registered stream: {stream_info.get('rtsp_url', 'None')[:50]}..."
            )
            
            # Test server statistics
            stats = self.rtsp_simulator.get_server_statistics()
            self.log_test_result(
                "Server Statistics",
                stats["total_active_streams"] == 1 and stats["server_running"],
                f"Server stats: {stats['total_active_streams']} streams active"
            )
            
            # Test viewer simulation
            self.rtsp_simulator.simulate_viewer_activity("test_cam_001", "connect")
            updated_info = self.rtsp_simulator.get_stream_info("test_cam_001")
            self.log_test_result(
                "Viewer Activity Simulation",
                updated_info["viewer_count"] == 1,
                f"Viewer count: {updated_info['viewer_count']}"
            )
            
        except Exception as e:
            self.log_test_result("RTSP Stream Simulator", False, str(e))
    
    async def test_stream_scenarios(self):
        """Test stream scenario generation"""
        print("\n🎬 Testing Stream Scenarios")
        
        if not self.rtsp_simulator:
            self.log_test_result("Stream Scenarios", False, "RTSP simulator not initialized")
            return
        
        try:
            # Wait for scenario generation
            await asyncio.sleep(2)
            
            # Test scenario assignment
            stream_info = self.rtsp_simulator.get_stream_info("test_cam_001")
            if stream_info:
                current_activity = stream_info.get("current_activity", {})
                self.log_test_result(
                    "Scenario Generation",
                    "scenario" in current_activity and "description" in current_activity,
                    f"Current scenario: {current_activity.get('scenario', 'None')}"
                )
                
                # Test scenario details
                has_activity_details = all(key in current_activity for key in [
                    "activity_level", "estimated_personnel", "equipment_active"
                ])
                self.log_test_result(
                    "Scenario Detail Generation",
                    has_activity_details,
                    f"Activity level: {current_activity.get('activity_level', 'Unknown')}"
                )
            
            # Test all streams info
            all_streams = self.rtsp_simulator.get_all_streams()
            self.log_test_result(
                "All Streams Information",
                len(all_streams) == 1,
                f"Retrieved info for {len(all_streams)} active streams"
            )
            
        except Exception as e:
            self.log_test_result("Stream Scenarios", False, str(e))
    
    async def test_end_to_end_integration(self):
        """Test complete end-to-end integration"""
        print("\n🔄 Testing End-to-End Integration")
        
        try:
            # Test complete workflow: Config -> Connector -> Data -> Streams
            
            # 1. Configuration
            set_mode("mock")
            config = get_config()
            
            # 2. Connector creation and initialization
            connector = get_connector()
            await connector.initialize()
            
            # 3. Data operations
            cameras = await connector.get_cameras()
            events = await connector.get_events(limit=5)
            zones = await connector.get_zones()
            
            # 4. Stream simulation
            rtsp_sim = RTSPStreamSimulator()
            await rtsp_sim.start_server()
            
            if cameras:
                rtsp_sim.register_camera_stream(cameras[0].camera_id, {
                    "camera_id": cameras[0].camera_id,
                    "name": cameras[0].name,
                    "camera_type": cameras[0].camera_type.value,
                    "site_id": cameras[0].site_id,
                    "location_description": cameras[0].location_description
                })
            
            # 5. Analytics
            if cameras:
                start_date = date.today() - timedelta(days=7)
                end_date = date.today()
                analytics = await connector.get_site_analytics(cameras[0].site_id, start_date, end_date)
            
            # 6. Real-time event streaming test (brief)
            event_stream = connector.stream_events()
            stream_started = False
            try:
                # Try to get one event from the stream
                async for event in event_stream:
                    stream_started = True
                    break
            except:
                pass  # Stream might not produce events immediately
            
            # Verify integration success
            integration_success = (
                len(cameras) > 0 and 
                len(events) > 0 and 
                len(zones) > 0 and
                rtsp_sim.server_running and
                "site_info" in analytics if cameras else True
            )
            
            self.log_test_result(
                "End-to-End Integration",
                integration_success,
                f"Complete workflow: {len(cameras)} cameras, {len(events)} events, {len(zones)} zones, RTSP active"
            )
            
            # Test mock statistics
            if hasattr(connector, 'get_mock_statistics'):
                mock_stats = connector.get_mock_statistics()
                self.log_test_result(
                    "Mock Statistics",
                    "total_sites" in mock_stats and "total_cameras" in mock_stats,
                    f"Mock data: {mock_stats.get('total_sites', 0)} sites, {mock_stats.get('total_cameras', 0)} cameras"
                )
            
            # Cleanup
            await rtsp_sim.stop_server()
            await connector.shutdown()
            
        except Exception as e:
            self.log_test_result("End-to-End Integration", False, str(e))
    
    def generate_test_report(self):
        """Generate comprehensive test report"""
        print("\n" + "=" * 60)
        print("🎭 ZONEMINDER CONNECTOR TEST REPORT")
        print("=" * 60)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result["success"])
        failed_tests = total_tests - passed_tests
        
        print(f"\n📊 SUMMARY:")
        print(f"   Total Tests: {total_tests}")
        print(f"   ✅ Passed: {passed_tests}")
        print(f"   ❌ Failed: {failed_tests}")
        print(f"   📈 Success Rate: {(passed_tests/total_tests*100):.1f}%")
        
        if failed_tests > 0:
            print(f"\n❌ FAILED TESTS:")
            for result in self.test_results:
                if not result["success"]:
                    print(f"   • {result['test_name']}: {result['message']}")
        
        print(f"\n✅ PASSED TESTS:")
        for result in self.test_results:
            if result["success"]:
                print(f"   • {result['test_name']}")
        
        # Test categories summary
        categories = {}
        for result in self.test_results:
            category = result["test_name"].split()[0] if " " in result["test_name"] else "General"
            if category not in categories:
                categories[category] = {"total": 0, "passed": 0}
            categories[category]["total"] += 1
            if result["success"]:
                categories[category]["passed"] += 1
        
        print(f"\n📋 BY CATEGORY:")
        for category, stats in categories.items():
            success_rate = (stats["passed"] / stats["total"] * 100) if stats["total"] > 0 else 0
            print(f"   {category}: {stats['passed']}/{stats['total']} ({success_rate:.1f}%)")
        
        print("\n" + "=" * 60)
        
        return {
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "failed_tests": failed_tests,
            "success_rate": passed_tests/total_tests*100 if total_tests > 0 else 0,
            "results": self.test_results
        }

async def main():
    """Main test execution function"""
    print("🎭 ZoneMinder Connector Comprehensive Testing Suite")
    print("=" * 60)
    
    tester = ZoneMinderConnectorTester()
    
    try:
        await tester.run_all_tests()
        
        # Final cleanup
        if tester.connector:
            await tester.connector.shutdown()
        if tester.rtsp_simulator:
            await tester.rtsp_simulator.stop_server()
            
    except KeyboardInterrupt:
        print("\n⚠️ Testing interrupted by user")
    except Exception as e:
        print(f"\n❌ Testing failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())