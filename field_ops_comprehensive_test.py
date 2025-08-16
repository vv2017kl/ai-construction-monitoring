#!/usr/bin/env python3
"""
Comprehensive Field Operations & Assessment API Testing Script
Tests all Field Operations APIs as requested in the review
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

def test_inspection_paths_api():
    """Test Inspection Paths API - CRUD operations"""
    print("\n1. Testing Inspection Paths API (CRUD Operations)")
    
    # Create test site and user first
    test_site_data = {
        "name": f"Field Ops Test Site {uuid.uuid4().hex[:8]}",
        "code": f"FOTS-{uuid.uuid4().hex[:8].upper()}",
        "address": "123 Field Operations Test Ave, Test City, TC 12345",
        "type": "commercial",
        "phase": "construction"
    }
    
    site_response = requests.post(f"{API_BASE_URL}/sites", json=test_site_data, headers={"Content-Type": "application/json"}, timeout=10)
    if site_response.status_code != 200:
        print(f"❌ Failed to create test site: {site_response.text}")
        return False, None, None
    
    site_id = site_response.json().get("id")
    print(f"   Created test site ID: {site_id}")
    
    test_user_data = {
        "username": f"field_ops_tester_{uuid.uuid4().hex[:8]}",
        "email": f"field.ops.tester.{uuid.uuid4().hex[:8]}@construction.com",
        "first_name": "Field",
        "last_name": "Tester",
        "password": "SecurePass123!",
        "role": "supervisor",
        "department": "Field Operations"
    }
    
    user_response = requests.post(f"{API_BASE_URL}/users", json=test_user_data, headers={"Content-Type": "application/json"}, timeout=10)
    if user_response.status_code != 200:
        print(f"❌ Failed to create test user: {user_response.text}")
        return False, site_id, None
    
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
            return False, site_id, user_id
        
        # Test POST create inspection path
        test_path_data = {
            "site_id": site_id,
            "name": f"Safety Inspection Route {uuid.uuid4().hex[:8]}",
            "description": "Comprehensive safety inspection path for construction site",
            "path_type": "inspection",
            "priority": "high",
            "assigned_to": user_id,
            "estimated_duration_minutes": 45,
            "zone_coverage": ["zone1", "zone2", "zone3"],
            "is_scheduled": True,
            "schedule_frequency": "daily"
        }
        
        print("   1b. Testing POST /api/inspection-paths")
        response = requests.post(f"{API_BASE_URL}/inspection-paths", json=test_path_data, headers={"Content-Type": "application/json"}, timeout=10)
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            path = response.json()
            path_id = path.get("id")
            print(f"      Created inspection path ID: {path_id}")
            print("      ✅ POST inspection path creation working")
        else:
            print(f"      Response: {response.text}")
            print("      ❌ POST inspection path creation failed")
            return False, site_id, user_id
        
        # Test GET specific inspection path
        print("   1c. Testing GET /api/inspection-paths/{path_id}")
        response = requests.get(f"{API_BASE_URL}/inspection-paths/{path_id}", timeout=10)
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            path = response.json()
            if path.get("name") == test_path_data["name"]:
                print("      ✅ GET specific inspection path working")
            else:
                print("      ❌ Inspection path data mismatch")
                return False, site_id, user_id
        else:
            print("      ❌ GET specific inspection path failed")
            return False, site_id, user_id
        
        # Test DELETE inspection path
        print("   1d. Testing DELETE /api/inspection-paths/{path_id}")
        response = requests.delete(f"{API_BASE_URL}/inspection-paths/{path_id}", timeout=10)
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("      ✅ DELETE inspection path working")
        else:
            print("      ❌ DELETE inspection path failed")
            return False, site_id, user_id
        
        return True, site_id, user_id
        
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Connection error: {e}")
        return False, site_id, user_id
    except Exception as e:
        print(f"   ❌ Unexpected error: {e}")
        return False, site_id, user_id

def test_path_waypoints_api(site_id, user_id):
    """Test Path Waypoints API - CRUD operations"""
    print("\n2. Testing Path Waypoints API (CRUD Operations)")
    
    # First create an inspection path
    test_path_data = {
        "site_id": site_id,
        "name": f"Waypoint Test Path {uuid.uuid4().hex[:8]}",
        "description": "Test path for waypoint operations",
        "path_type": "inspection",
        "priority": "medium",
        "assigned_to": user_id,
        "estimated_duration_minutes": 30
    }
    
    path_response = requests.post(f"{API_BASE_URL}/inspection-paths", json=test_path_data, headers={"Content-Type": "application/json"}, timeout=10)
    if path_response.status_code != 200:
        print(f"❌ Failed to create test path: {path_response.text}")
        return False
    
    path_id = path_response.json().get("id")
    print(f"   Created test path ID: {path_id}")
    
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
            return False
        
        # Test POST create path waypoint
        test_waypoint_data = {
            "path_id": path_id,
            "waypoint_order": 1,
            "waypoint_name": "Entry Gate Checkpoint",
            "description": "Main entry point safety verification",
            "coordinates_x": 100.5,
            "coordinates_y": 200.3,
            "waypoint_type": "checkpoint",
            "is_mandatory": True,
            "estimated_time_minutes": 5,
            "inspection_checklist": {"ppe_check": True, "id_verification": True}
        }
        
        print("   2b. Testing POST /api/path-waypoints")
        response = requests.post(f"{API_BASE_URL}/path-waypoints", json=test_waypoint_data, headers={"Content-Type": "application/json"}, timeout=10)
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            waypoint = response.json()
            waypoint_id = waypoint.get("id")
            print(f"      Created waypoint ID: {waypoint_id}")
            print("      ✅ POST path waypoint creation working")
        else:
            print(f"      Response: {response.text}")
            print("      ❌ POST path waypoint creation failed")
            return False
        
        # Test GET waypoints by path
        print("   2c. Testing GET /api/inspection-paths/{path_id}/waypoints")
        response = requests.get(f"{API_BASE_URL}/inspection-paths/{path_id}/waypoints", timeout=10)
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            path_waypoints = response.json()
            print(f"      Found {len(path_waypoints)} waypoints for path")
            print("      ✅ GET path waypoints working")
        else:
            print("      ❌ GET path waypoints failed")
            return False
        
        # Test DELETE waypoint
        print("   2d. Testing DELETE /api/path-waypoints/{waypoint_id}")
        response = requests.delete(f"{API_BASE_URL}/path-waypoints/{waypoint_id}", timeout=10)
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("      ✅ DELETE path waypoint working")
        else:
            print("      ❌ DELETE path waypoint failed")
            return False
        
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Connection error: {e}")
        return False
    except Exception as e:
        print(f"   ❌ Unexpected error: {e}")
        return False

def test_path_executions_api(site_id, user_id):
    """Test Path Executions API - execution workflow"""
    print("\n3. Testing Path Executions API (Execution Workflow)")
    
    # First create an inspection path
    test_path_data = {
        "site_id": site_id,
        "name": f"Execution Test Path {uuid.uuid4().hex[:8]}",
        "description": "Test path for execution operations",
        "path_type": "inspection",
        "priority": "medium",
        "assigned_to": user_id,
        "estimated_duration_minutes": 30
    }
    
    path_response = requests.post(f"{API_BASE_URL}/inspection-paths", json=test_path_data, headers={"Content-Type": "application/json"}, timeout=10)
    if path_response.status_code != 200:
        print(f"❌ Failed to create test path: {path_response.text}")
        return False
    
    path_id = path_response.json().get("id")
    print(f"   Created test path ID: {path_id}")
    
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
            return False
        
        # Test POST create path execution
        test_execution_data = {
            "path_id": path_id,
            "execution_type": "scheduled",
            "execution_reason": "Daily safety inspection routine",
            "planned_duration_minutes": 30,
            "weather_conditions": "Clear, 22°C, Light breeze",
            "equipment_used": ["tablet", "camera", "safety_checklist"]
        }
        
        print("   3b. Testing POST /api/path-executions")
        response = requests.post(f"{API_BASE_URL}/path-executions", json=test_execution_data, headers={"Content-Type": "application/json"}, timeout=10)
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            execution = response.json()
            execution_id = execution.get("id")
            print(f"      Created path execution ID: {execution_id}")
            print("      ✅ POST path execution creation working")
        else:
            print(f"      Response: {response.text}")
            print("      ❌ POST path execution creation failed")
            return False
        
        # Test GET executions by path
        print("   3c. Testing GET /api/inspection-paths/{path_id}/executions")
        response = requests.get(f"{API_BASE_URL}/inspection-paths/{path_id}/executions", timeout=10)
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            path_executions = response.json()
            print(f"      Found {len(path_executions)} executions for path")
            print("      ✅ GET path executions working")
        else:
            print("      ❌ GET path executions failed")
            return False
        
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Connection error: {e}")
        return False
    except Exception as e:
        print(f"   ❌ Unexpected error: {e}")
        return False

def test_path_execution_waypoints_api(site_id, user_id):
    """Test Path Execution Waypoints API - visit recording"""
    print("\n4. Testing Path Execution Waypoints API (Visit Recording)")
    
    # Create path, waypoint, and execution
    test_path_data = {
        "site_id": site_id,
        "name": f"Visit Test Path {uuid.uuid4().hex[:8]}",
        "description": "Test path for visit recording",
        "path_type": "inspection",
        "priority": "medium",
        "assigned_to": user_id,
        "estimated_duration_minutes": 20
    }
    
    path_response = requests.post(f"{API_BASE_URL}/inspection-paths", json=test_path_data, headers={"Content-Type": "application/json"}, timeout=10)
    if path_response.status_code != 200:
        print(f"❌ Failed to create test path: {path_response.text}")
        return False
    
    path_id = path_response.json().get("id")
    
    # Create waypoint
    test_waypoint_data = {
        "path_id": path_id,
        "waypoint_order": 1,
        "waypoint_name": "Test Checkpoint",
        "description": "Test waypoint for visit recording",
        "coordinates_x": 100.0,
        "coordinates_y": 200.0,
        "waypoint_type": "checkpoint",
        "is_mandatory": True,
        "estimated_time_minutes": 5
    }
    
    waypoint_response = requests.post(f"{API_BASE_URL}/path-waypoints", json=test_waypoint_data, headers={"Content-Type": "application/json"}, timeout=10)
    if waypoint_response.status_code != 200:
        print(f"❌ Failed to create test waypoint: {waypoint_response.text}")
        return False
    
    waypoint_id = waypoint_response.json().get("id")
    
    # Create execution
    test_execution_data = {
        "path_id": path_id,
        "execution_type": "on_demand",
        "execution_reason": "Test visit recording",
        "planned_duration_minutes": 20
    }
    
    execution_response = requests.post(f"{API_BASE_URL}/path-executions", json=test_execution_data, headers={"Content-Type": "application/json"}, timeout=10)
    if execution_response.status_code != 200:
        print(f"❌ Failed to create test execution: {execution_response.text}")
        return False
    
    execution_id = execution_response.json().get("id")
    print(f"   Created test execution ID: {execution_id}")
    
    try:
        # Test GET all execution waypoints
        print("   4a. Testing GET /api/path-execution-waypoints")
        response = requests.get(f"{API_BASE_URL}/path-execution-waypoints", timeout=10)
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            execution_waypoints = response.json()
            print(f"      Found {len(execution_waypoints)} total execution waypoints")
            print("      ✅ GET all execution waypoints working")
        else:
            print("      ❌ GET all execution waypoints failed")
            return False
        
        # Test GET execution waypoints by execution
        print("   4b. Testing GET /api/path-executions/{execution_id}/waypoints")
        response = requests.get(f"{API_BASE_URL}/path-executions/{execution_id}/waypoints", timeout=10)
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            execution_waypoints = response.json()
            print(f"      Found {len(execution_waypoints)} waypoints for execution")
            print("      ✅ GET execution waypoints working")
        else:
            print("      ❌ GET execution waypoints failed")
            return False
        
        # Test POST record waypoint visit
        print("   4c. Testing POST /api/path-executions/{execution_id}/waypoints/{waypoint_id}/visit")
        visit_params = {
            "inspection_completed": True,
            "issues_found": 0,
            "photos_taken": 2,
            "notes": "Waypoint inspection completed successfully. No issues found."
        }
        
        response = requests.post(f"{API_BASE_URL}/path-executions/{execution_id}/waypoints/{waypoint_id}/visit", params=visit_params, timeout=10)
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("      ✅ POST waypoint visit recording working")
        else:
            print(f"      Response: {response.text}")
            print("      ❌ POST waypoint visit recording failed")
            return False
        
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Connection error: {e}")
        return False
    except Exception as e:
        print(f"   ❌ Unexpected error: {e}")
        return False

def test_path_templates_api():
    """Test Path Templates API - template management"""
    print("\n5. Testing Path Templates API (Template Management)")
    
    try:
        # Test GET all path templates
        print("   5a. Testing GET /api/path-templates")
        response = requests.get(f"{API_BASE_URL}/path-templates", timeout=10)
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            templates = response.json()
            print(f"      Found {len(templates)} total path templates")
            print("      ✅ GET all path templates working")
        else:
            print("      ❌ GET all path templates failed")
            return False
        
        # Test POST create path template
        test_template_data = {
            "template_name": f"Standard Safety Template {uuid.uuid4().hex[:8]}",
            "description": "Comprehensive template for daily safety inspections",
            "template_type": "inspection",
            "difficulty_level": "intermediate",
            "safety_level": "high",
            "base_waypoint_count": 5,
            "estimated_duration_minutes": 60,
            "recommended_zones": ["construction", "safety", "office"],
            "required_equipment": ["tablet", "camera", "safety_checklist"],
            "is_public": True
        }
        
        print("   5b. Testing POST /api/path-templates")
        response = requests.post(f"{API_BASE_URL}/path-templates", json=test_template_data, headers={"Content-Type": "application/json"}, timeout=10)
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            template = response.json()
            template_id = template.get("id")
            print(f"      Created path template ID: {template_id}")
            print("      ✅ POST path template creation working")
        else:
            print(f"      Response: {response.text}")
            print("      ❌ POST path template creation failed")
            return False
        
        # Test GET specific path template
        print("   5c. Testing GET /api/path-templates/{template_id}")
        response = requests.get(f"{API_BASE_URL}/path-templates/{template_id}", timeout=10)
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            template = response.json()
            if template.get("template_name") == test_template_data["template_name"]:
                print("      ✅ GET specific path template working")
            else:
                print("      ❌ Path template data mismatch")
                return False
        else:
            print("      ❌ GET specific path template failed")
            return False
        
        # Test PUT update path template
        print("   5d. Testing PUT /api/path-templates/{template_id}")
        update_data = {
            "template_name": test_template_data["template_name"],
            "description": "Updated comprehensive template for enhanced safety inspections",
            "template_type": test_template_data["template_type"],
            "difficulty_level": "advanced",
            "safety_level": "critical",
            "base_waypoint_count": 7,
            "estimated_duration_minutes": 90,
            "recommended_zones": test_template_data["recommended_zones"],
            "required_equipment": test_template_data["required_equipment"] + ["gas_detector"],
            "is_public": True
        }
        
        response = requests.put(f"{API_BASE_URL}/path-templates/{template_id}", json=update_data, headers={"Content-Type": "application/json"}, timeout=10)
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            updated_template = response.json()
            if updated_template.get("difficulty_level") == update_data["difficulty_level"]:
                print("      ✅ PUT path template update working")
            else:
                print("      ❌ Path template update data mismatch")
                return False
        else:
            print("      ❌ PUT path template update failed")
            return False
        
        # Test DELETE path template
        print("   5e. Testing DELETE /api/path-templates/{template_id}")
        response = requests.delete(f"{API_BASE_URL}/path-templates/{template_id}", timeout=10)
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("      ✅ DELETE path template working")
        else:
            print("      ❌ DELETE path template failed")
            return False
        
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Connection error: {e}")
        return False
    except Exception as e:
        print(f"   ❌ Unexpected error: {e}")
        return False

def test_analytics_api(site_id):
    """Test Analytics API - path execution analytics"""
    print("\n6. Testing Analytics API (Path Execution Analytics)")
    
    try:
        # Test GET path analytics summary
        print("   6a. Testing GET /api/path-analytics/summary")
        response = requests.get(f"{API_BASE_URL}/path-analytics/summary", timeout=10)
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            analytics = response.json()
            print(f"      Analytics response keys: {list(analytics.keys()) if isinstance(analytics, dict) else 'Not a dict'}")
            print("      ✅ GET path analytics summary working")
        else:
            print("      ❌ GET path analytics summary failed")
            return False
        
        # Test GET path analytics with site filter
        print("   6b. Testing GET /api/path-analytics/summary?site_id={site_id}")
        response = requests.get(f"{API_BASE_URL}/path-analytics/summary?site_id={site_id}", timeout=10)
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            site_analytics = response.json()
            print("      ✅ GET site path analytics working")
        else:
            print("      ❌ GET site path analytics failed")
            return False
        
        # Test GET path analytics with days filter
        print("   6c. Testing GET /api/path-analytics/summary?days=7")
        response = requests.get(f"{API_BASE_URL}/path-analytics/summary?days=7", timeout=10)
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            weekly_analytics = response.json()
            print("      ✅ GET weekly path analytics working")
        else:
            print("      ❌ GET weekly path analytics failed")
            return False
        
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Connection error: {e}")
        return False
    except Exception as e:
        print(f"   ❌ Unexpected error: {e}")
        return False

def run_comprehensive_field_operations_tests():
    """Run all Field Operations & Assessment API tests"""
    print("Starting Comprehensive Field Operations & Assessment API Tests...")
    
    test_results = []
    site_id = None
    user_id = None
    
    # Test 1: Inspection Paths API
    success, site_id, user_id = test_inspection_paths_api()
    test_results.append(("Inspection Paths API", success))
    
    if not success or not site_id or not user_id:
        print("❌ Cannot continue without valid site and user")
        return False
    
    # Test 2: Path Waypoints API
    success = test_path_waypoints_api(site_id, user_id)
    test_results.append(("Path Waypoints API", success))
    
    # Test 3: Path Executions API
    success = test_path_executions_api(site_id, user_id)
    test_results.append(("Path Executions API", success))
    
    # Test 4: Path Execution Waypoints API
    success = test_path_execution_waypoints_api(site_id, user_id)
    test_results.append(("Path Execution Waypoints API", success))
    
    # Test 5: Path Templates API
    success = test_path_templates_api()
    test_results.append(("Path Templates API", success))
    
    # Test 6: Analytics API
    success = test_analytics_api(site_id)
    test_results.append(("Analytics API", success))
    
    # Print summary
    print("\n" + "=" * 80)
    print("FIELD OPERATIONS & ASSESSMENT API TEST SUMMARY")
    print("=" * 80)
    
    passed = 0
    total = len(test_results)
    
    for test_name, success in test_results:
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{test_name:<40} {status}")
        if success:
            passed += 1
    
    print(f"\nOverall Result: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL FIELD OPERATIONS & ASSESSMENT API TESTS PASSED!")
        return True
    else:
        print("❌ Some Field Operations & Assessment API tests failed")
        return False

if __name__ == "__main__":
    success = run_comprehensive_field_operations_tests()
    sys.exit(0 if success else 1)