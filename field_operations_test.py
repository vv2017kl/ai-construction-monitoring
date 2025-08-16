#!/usr/bin/env python3
"""
Field Operations & Assessment API Testing Script
Tests the newly implemented Field Operations APIs
"""

import requests
import json
import sys
from datetime import datetime
import os
from dotenv import load_dotenv
import uuid

# Load environment variables
load_dotenv('/app/frontend/.env')

# Get the backend URL from environment
BACKEND_URL = os.getenv('REACT_APP_BACKEND_URL')
API_BASE_URL = f"{BACKEND_URL}/api"

print(f"Testing Field Operations & Assessment APIs at: {API_BASE_URL}")
print("=" * 80)

def test_field_operations_inspection_paths():
    """Test Field Operations - Inspection Paths API endpoints"""
    print("\n1. Testing Field Operations - Inspection Paths API")
    created_path_id = None
    
    # First create a site and user for testing
    site_data = {
        "name": f"Test Construction Site {uuid.uuid4().hex[:8]}",
        "code": f"TCS-{uuid.uuid4().hex[:8].upper()}",
        "address": "123 Test Ave, Test City, TC 12345",
        "type": "commercial",
        "phase": "construction"
    }
    
    user_data = {
        "username": f"test_supervisor_{uuid.uuid4().hex[:8]}",
        "email": f"supervisor.{uuid.uuid4().hex[:8]}@test.com",
        "first_name": "Test",
        "last_name": "Supervisor",
        "password": "TestPass123!",
        "role": "supervisor",  # Fixed: using valid enum value
        "department": "Safety"
    }
    
    # Create test site
    site_response = requests.post(f"{API_BASE_URL}/sites", json=site_data, headers={"Content-Type": "application/json"})
    if site_response.status_code != 200:
        print(f"   ❌ Failed to create test site: {site_response.status_code}")
        return False, None, None, None
    
    site_id = site_response.json().get("id")
    print(f"   Created test site ID: {site_id}")
    
    # Create test user
    user_response = requests.post(f"{API_BASE_URL}/users", json=user_data, headers={"Content-Type": "application/json"})
    if user_response.status_code != 200:
        print(f"   ❌ Failed to create test user: {user_response.status_code}")
        return False, site_id, None, None
    
    user_id = user_response.json().get("id")
    print(f"   Created test user ID: {user_id}")
    
    try:
        # Test GET all inspection paths
        print("   1a. Testing GET /api/inspection-paths")
        response = requests.get(f"{API_BASE_URL}/inspection-paths", timeout=10)
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            paths = response.json()
            print(f"      Found {len(paths)} total inspection paths")
            print("      ✅ GET all inspection paths working")
        else:
            print("      ❌ GET all inspection paths failed")
            return False, site_id, user_id, None
        
        # Create test inspection path data
        test_path_data = {
            "site_id": site_id,
            "name": f"Safety Inspection Route {uuid.uuid4().hex[:8]}",
            "description": "Comprehensive safety inspection path for construction site",
            "path_type": "inspection",  # Fixed: using valid enum value
            "priority": "high",
            "assigned_to": user_id,
            "estimated_duration_minutes": 45,
            "zone_coverage": ["zone1", "zone2", "zone3"],
            "is_scheduled": True,
            "schedule_frequency": "daily"
        }
        
        # Test POST create inspection path (with user_id as query param)
        print("   1b. Testing POST /api/inspection-paths")
        response = requests.post(
            f"{API_BASE_URL}/inspection-paths?current_user_id={user_id}",
            json=test_path_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            path = response.json()
            created_path_id = path.get("id")
            print(f"      Created inspection path ID: {created_path_id}")
            print("      ✅ POST inspection path creation working")
        else:
            print(f"      Response: {response.text}")
            print("      ❌ POST inspection path creation failed")
            return False, site_id, user_id, None
        
        # Test GET specific inspection path
        print("   1c. Testing GET /api/inspection-paths/{path_id}")
        response = requests.get(f"{API_BASE_URL}/inspection-paths/{created_path_id}", timeout=10)
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            path = response.json()
            if path.get("name") == test_path_data["name"]:
                print("      ✅ GET specific inspection path working")
            else:
                print("      ❌ Inspection path data mismatch")
                return False, site_id, user_id, created_path_id
        else:
            print("      ❌ GET specific inspection path failed")
            return False, site_id, user_id, created_path_id
        
        # Test GET site inspection paths
        print("   1d. Testing GET /api/sites/{site_id}/inspection-paths")
        response = requests.get(f"{API_BASE_URL}/sites/{site_id}/inspection-paths", timeout=10)
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            site_paths = response.json()
            print(f"      Found {len(site_paths)} inspection paths for site")
            print("      ✅ GET site inspection paths working")
        else:
            print("      ❌ GET site inspection paths failed")
            return False, site_id, user_id, created_path_id
        
        return True, site_id, user_id, created_path_id
        
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Connection error: {e}")
        return False, site_id, user_id, created_path_id
    except Exception as e:
        print(f"   ❌ Unexpected error: {e}")
        return False, site_id, user_id, created_path_id

def test_field_operations_path_waypoints(path_id):
    """Test Field Operations - Path Waypoints API endpoints"""
    print("\n2. Testing Field Operations - Path Waypoints API")
    created_waypoint_ids = []
    
    try:
        # Test GET all path waypoints
        print("   2a. Testing GET /api/path-waypoints")
        response = requests.get(f"{API_BASE_URL}/path-waypoints", timeout=10)
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            waypoints = response.json()
            print(f"      Found {len(waypoints)} total path waypoints")
            print("      ✅ GET all path waypoints working")
        else:
            print("      ❌ GET all path waypoints failed")
            return False, []
        
        # Create test waypoint data
        waypoint_data = {
            "path_id": path_id,
            "waypoint_order": 1,
            "waypoint_name": "Main Entrance Check",
            "description": "Verify security and safety protocols at main entrance",
            "coordinates_x": 100.5,
            "coordinates_y": 200.3,
            "waypoint_type": "checkpoint",
            "is_mandatory": True,
            "estimated_time_minutes": 5,
            "inspection_checklist": {"items": ["security_check", "ppe_verification"]}
        }
        
        # Test POST create path waypoint
        print("   2b. Testing POST /api/path-waypoints")
        response = requests.post(
            f"{API_BASE_URL}/path-waypoints",
            json=waypoint_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            waypoint = response.json()
            waypoint_id = waypoint.get("id")
            created_waypoint_ids.append(waypoint_id)
            print(f"      Created waypoint ID: {waypoint_id}")
            print("      ✅ POST waypoint creation working")
        else:
            print(f"      Response: {response.text}")
            print("      ❌ POST waypoint creation failed")
            return False, []
        
        # Test GET waypoints by path
        print("   2c. Testing GET /api/inspection-paths/{path_id}/waypoints")
        response = requests.get(f"{API_BASE_URL}/inspection-paths/{path_id}/waypoints", timeout=10)
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            path_waypoints = response.json()
            print(f"      Found {len(path_waypoints)} waypoints for path")
            print("      ✅ GET waypoints by path working")
        else:
            print("      ❌ GET waypoints by path failed")
            return False, created_waypoint_ids
        
        return True, created_waypoint_ids
        
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Connection error: {e}")
        return False, created_waypoint_ids
    except Exception as e:
        print(f"   ❌ Unexpected error: {e}")
        return False, created_waypoint_ids

def test_field_operations_path_executions(path_id, user_id):
    """Test Field Operations - Path Executions API endpoints"""
    print("\n3. Testing Field Operations - Path Executions API")
    created_execution_id = None
    
    try:
        # Test GET all path executions
        print("   3a. Testing GET /api/path-executions")
        response = requests.get(f"{API_BASE_URL}/path-executions", timeout=10)
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            executions = response.json()
            print(f"      Found {len(executions)} total path executions")
            print("      ✅ GET all path executions working")
        else:
            print("      ❌ GET all path executions failed")
            return False, None
        
        # Create test path execution data
        test_execution_data = {
            "path_id": path_id,
            "execution_type": "scheduled",  # Fixed: using valid enum value
            "execution_reason": "Daily safety compliance check",
            "planned_duration_minutes": 45,
            "weather_conditions": "Clear, 22°C",
            "equipment_used": ["tablet", "camera", "safety_meter", "checklist"]
        }
        
        # Test POST create path execution (with user_id as query param)
        print("   3b. Testing POST /api/path-executions")
        response = requests.post(
            f"{API_BASE_URL}/path-executions?current_user_id={user_id}",
            json=test_execution_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            execution = response.json()
            created_execution_id = execution.get("id")
            print(f"      Created path execution ID: {created_execution_id}")
            print("      ✅ POST path execution creation working")
        else:
            print(f"      Response: {response.text}")
            print("      ❌ POST path execution creation failed")
            return False, None
        
        # Test GET executions by path
        print("   3c. Testing GET /api/inspection-paths/{path_id}/executions")
        response = requests.get(f"{API_BASE_URL}/inspection-paths/{path_id}/executions", timeout=10)
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            path_executions = response.json()
            print(f"      Found {len(path_executions)} executions for path")
            print("      ✅ GET executions by path working")
        else:
            print("      ❌ GET executions by path failed")
            return False, created_execution_id
        
        return True, created_execution_id
        
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Connection error: {e}")
        return False, created_execution_id
    except Exception as e:
        print(f"   ❌ Unexpected error: {e}")
        return False, created_execution_id

def test_field_operations_path_templates(user_id):
    """Test Field Operations - Path Templates API endpoints"""
    print("\n4. Testing Field Operations - Path Templates API")
    created_template_id = None
    
    try:
        # Test GET all path templates
        print("   4a. Testing GET /api/path-templates")
        response = requests.get(f"{API_BASE_URL}/path-templates", timeout=10)
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            templates = response.json()
            print(f"      Found {len(templates)} total path templates")
            print("      ✅ GET all path templates working")
        else:
            print("      ❌ GET all path templates failed")
            return False, None
        
        # Create test path template data
        test_template_data = {
            "template_name": f"Standard Safety Inspection Template {uuid.uuid4().hex[:8]}",
            "description": "Comprehensive template for daily safety inspections",
            "template_type": "inspection",  # Fixed: using valid enum value
            "difficulty_level": "intermediate",
            "safety_level": "high",
            "base_waypoint_count": 5,
            "estimated_duration_minutes": 60,
            "recommended_zones": ["construction_area", "equipment_storage", "office_area"],
            "required_equipment": ["tablet", "camera", "safety_meter"],
            "is_public": True
        }
        
        # Test POST create path template (with user_id as query param)
        print("   4b. Testing POST /api/path-templates")
        response = requests.post(
            f"{API_BASE_URL}/path-templates?current_user_id={user_id}",
            json=test_template_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            template = response.json()
            created_template_id = template.get("id")
            print(f"      Created path template ID: {created_template_id}")
            print("      ✅ POST path template creation working")
        else:
            print(f"      Response: {response.text}")
            print("      ❌ POST path template creation failed")
            return False, None
        
        return True, created_template_id
        
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Connection error: {e}")
        return False, created_template_id
    except Exception as e:
        print(f"   ❌ Unexpected error: {e}")
        return False, created_template_id

def test_field_operations_analytics(site_id):
    """Test Field Operations - Analytics API endpoints"""
    print("\n5. Testing Field Operations - Analytics API")
    
    try:
        # Test GET path analytics summary
        print("   5a. Testing GET /api/path-analytics/summary")
        response = requests.get(f"{API_BASE_URL}/path-analytics/summary", timeout=10)
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            analytics = response.json()
            if "message" in analytics or "total_executions" in analytics:
                print("      ✅ GET path analytics summary working")
            else:
                print("      ❌ Unexpected analytics response structure")
                return False
        else:
            print("      ❌ GET path analytics summary failed")
            return False
        
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Connection error: {e}")
        return False
    except Exception as e:
        print(f"   ❌ Unexpected error: {e}")
        return False

def cleanup_test_data(site_id, user_id, path_id, waypoint_ids, execution_id, template_id):
    """Clean up test data"""
    print("\n6. Cleaning up test data")
    
    try:
        # Delete template
        if template_id:
            response = requests.delete(f"{API_BASE_URL}/path-templates/{template_id}")
            print(f"   Template deletion: {response.status_code}")
        
        # Delete waypoints
        if waypoint_ids:
            for waypoint_id in waypoint_ids:
                response = requests.delete(f"{API_BASE_URL}/path-waypoints/{waypoint_id}")
                print(f"   Waypoint deletion: {response.status_code}")
        
        # Delete path
        if path_id:
            response = requests.delete(f"{API_BASE_URL}/inspection-paths/{path_id}")
            print(f"   Path deletion: {response.status_code}")
        
        # Delete site
        if site_id:
            response = requests.delete(f"{API_BASE_URL}/sites/{site_id}")
            print(f"   Site deletion: {response.status_code}")
        
        print("   ✅ Cleanup completed")
        
    except Exception as e:
        print(f"   ⚠️ Cleanup error: {e}")

def main():
    """Run Field Operations tests"""
    print("Starting Field Operations & Assessment API Tests...")
    
    # Test inspection paths
    paths_ok, site_id, user_id, path_id = test_field_operations_inspection_paths()
    
    waypoint_ids = []
    execution_id = None
    template_id = None
    
    if paths_ok and path_id:
        # Test waypoints
        waypoints_ok, waypoint_ids = test_field_operations_path_waypoints(path_id)
        
        # Test executions
        executions_ok, execution_id = test_field_operations_path_executions(path_id, user_id)
    
    # Test templates
    templates_ok, template_id = test_field_operations_path_templates()
    
    # Test analytics
    if site_id:
        analytics_ok = test_field_operations_analytics(site_id)
    
    # Cleanup
    cleanup_test_data(site_id, user_id, path_id, waypoint_ids, execution_id, template_id)
    
    print("\n" + "=" * 80)
    print("FIELD OPERATIONS & ASSESSMENT API TEST RESULTS:")
    print("=" * 80)
    print(f"Inspection Paths API:        {'✅ PASS' if paths_ok else '❌ FAIL'}")
    if paths_ok and path_id:
        print(f"Path Waypoints API:          {'✅ PASS' if waypoints_ok else '❌ FAIL'}")
        print(f"Path Executions API:         {'✅ PASS' if executions_ok else '❌ FAIL'}")
    print(f"Path Templates API:          {'✅ PASS' if templates_ok else '❌ FAIL'}")
    if site_id:
        print(f"Analytics API:               {'✅ PASS' if analytics_ok else '❌ FAIL'}")
    
    return paths_ok and (not path_id or (waypoints_ok and executions_ok)) and templates_ok

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)