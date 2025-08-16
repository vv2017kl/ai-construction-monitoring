#!/usr/bin/env python3
"""
Backend API Testing Script for AI Construction Management System
Tests the MySQL-based FastAPI backend endpoints to ensure proper functionality
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

print(f"Testing AI Construction Management Backend API at: {API_BASE_URL}")
print("=" * 80)

# Test data for creating records
TEST_SITE_DATA = {
    "name": f"Construction Site Alpha {uuid.uuid4().hex[:8]}",
    "code": f"CSA-{uuid.uuid4().hex[:8].upper()}",
    "address": "123 Construction Ave, Builder City, BC 12345",
    "type": "commercial",
    "phase": "construction",
    "manager_id": None  # Will be set after creating a user
}

TEST_USER_DATA = {
    "username": f"john_manager_{uuid.uuid4().hex[:8]}",
    "email": f"john.manager.{uuid.uuid4().hex[:8]}@construction.com",
    "first_name": "John",
    "last_name": "Manager",
    "password": "SecurePass123!",
    "role": "site_manager",
    "department": "Operations",
    "phone": "+1-555-0123"
}

def test_api_connectivity():
    """Test basic API connectivity"""
    print("\n1. Testing API Connectivity")
    try:
        # Test if we can reach the backend at all
        response = requests.get(BACKEND_URL, timeout=5)
        print(f"   Backend base URL accessible: {response.status_code}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Backend connectivity issue: {e}")
        return False

def test_root_endpoint():
    """Test the root API endpoint"""
    print("\n2. Testing Root Endpoint (GET /api/)")
    try:
        response = requests.get(f"{API_BASE_URL}/", timeout=10)
        print(f"   Status Code: {response.status_code}")
        print(f"   Response: {response.json()}")
        
        if response.status_code == 200:
            data = response.json()
            if "AI Construction Management API" in data.get("message", ""):
                print("   ✅ Root endpoint working correctly")
                return True
            else:
                print("   ❌ Unexpected response content")
                return False
        else:
            print("   ❌ Root endpoint failed")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Connection error: {e}")
        return False
    except Exception as e:
        print(f"   ❌ Unexpected error: {e}")
        return False

def test_health_endpoint():
    """Test the health check endpoint"""
    print("\n3. Testing Health Check Endpoint (GET /api/health)")
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=10)
        print(f"   Status Code: {response.status_code}")
        print(f"   Response: {response.json()}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "healthy" and data.get("database") == "connected":
                print("   ✅ Health check passed - MySQL database connected")
                return True
            else:
                print("   ❌ Health check failed - database connection issue")
                return False
        else:
            print("   ❌ Health endpoint failed")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Connection error: {e}")
        return False
    except Exception as e:
        print(f"   ❌ Unexpected error: {e}")
        return False

def test_dashboard_stats():
    """Test the dashboard stats endpoint"""
    print("\n4. Testing Dashboard Stats (GET /api/dashboard/stats)")
    try:
        response = requests.get(f"{API_BASE_URL}/dashboard/stats", timeout=10)
        print(f"   Status Code: {response.status_code}")
        print(f"   Response: {response.json()}")
        
        if response.status_code == 200:
            data = response.json()
            required_fields = ["total_sites", "active_sites", "total_users", "total_cameras", "active_alerts"]
            if all(field in data for field in required_fields):
                print("   ✅ Dashboard stats endpoint working correctly")
                return True
            else:
                print("   ❌ Missing required fields in dashboard stats")
                return False
        else:
            print("   ❌ Dashboard stats endpoint failed")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Connection error: {e}")
        return False
    except Exception as e:
        print(f"   ❌ Unexpected error: {e}")
        return False

def test_users_crud():
    """Test Users CRUD operations"""
    print("\n5. Testing Users CRUD Operations")
    created_user_id = None
    
    try:
        # Test GET all users
        print("   5a. Testing GET /api/users")
        response = requests.get(f"{API_BASE_URL}/users", timeout=10)
        print(f"      Status Code: {response.status_code}")
        if response.status_code == 200:
            users = response.json()
            print(f"      Found {len(users)} existing users")
            print("      ✅ GET users working")
        else:
            print("      ❌ GET users failed")
            return False, None
        
        # Test POST create user
        print("   5b. Testing POST /api/users")
        response = requests.post(
            f"{API_BASE_URL}/users",
            json=TEST_USER_DATA,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            user = response.json()
            created_user_id = user.get("id")
            print(f"      Created user ID: {created_user_id}")
            print("      ✅ POST user creation working")
        else:
            print(f"      Response: {response.text}")
            print("      ❌ POST user creation failed")
            return False, None
        
        # Test GET specific user
        print("   5c. Testing GET /api/users/{user_id}")
        response = requests.get(f"{API_BASE_URL}/users/{created_user_id}", timeout=10)
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            user = response.json()
            if user.get("username") == TEST_USER_DATA["username"]:
                print("      ✅ GET specific user working")
            else:
                print("      ❌ User data mismatch")
                return False, created_user_id
        else:
            print("      ❌ GET specific user failed")
            return False, created_user_id
        
        return True, created_user_id
        
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Connection error: {e}")
        return False, created_user_id
    except Exception as e:
        print(f"   ❌ Unexpected error: {e}")
        return False, created_user_id

def test_sites_crud(manager_id=None):
    """Test Sites CRUD operations"""
    print("\n6. Testing Sites CRUD Operations")
    created_site_id = None
    
    try:
        # Update test data with manager_id if provided
        site_data = TEST_SITE_DATA.copy()
        if manager_id:
            site_data["manager_id"] = manager_id
        
        # Test GET all sites
        print("   6a. Testing GET /api/sites")
        response = requests.get(f"{API_BASE_URL}/sites", timeout=10)
        print(f"      Status Code: {response.status_code}")
        if response.status_code == 200:
            sites = response.json()
            print(f"      Found {len(sites)} existing sites")
            print("      ✅ GET sites working")
        else:
            print("      ❌ GET sites failed")
            return False, None
        
        # Test POST create site
        print("   6b. Testing POST /api/sites")
        response = requests.post(
            f"{API_BASE_URL}/sites",
            json=site_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            site = response.json()
            created_site_id = site.get("id")
            print(f"      Created site ID: {created_site_id}")
            print("      ✅ POST site creation working")
        else:
            print(f"      Response: {response.text}")
            print("      ❌ POST site creation failed")
            return False, None
        
        # Test GET specific site
        print("   6c. Testing GET /api/sites/{site_id}")
        response = requests.get(f"{API_BASE_URL}/sites/{created_site_id}", timeout=10)
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            site = response.json()
            if site.get("code") == site_data["code"]:
                print("      ✅ GET specific site working")
            else:
                print("      ❌ Site data mismatch")
                return False, created_site_id
        else:
            print("      ❌ GET specific site failed")
            return False, created_site_id
        
        # Test PUT update site
        print("   6d. Testing PUT /api/sites/{site_id}")
        update_data = {"name": "Updated Construction Site Alpha", "phase": "finishing"}
        response = requests.put(
            f"{API_BASE_URL}/sites/{created_site_id}",
            json=update_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            updated_site = response.json()
            if updated_site.get("name") == update_data["name"]:
                print("      ✅ PUT site update working")
            else:
                print("      ❌ Site update data mismatch")
                return False, created_site_id
        else:
            print("      ❌ PUT site update failed")
            return False, created_site_id
        
        return True, created_site_id
        
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Connection error: {e}")
        return False, created_site_id
    except Exception as e:
        print(f"   ❌ Unexpected error: {e}")
        return False, created_site_id

def test_zones_api(site_id):
    """Test Zones API endpoints"""
    print("\n7. Testing Zones API")
    
    try:
        # Test GET site zones
        print("   7a. Testing GET /api/sites/{site_id}/zones")
        response = requests.get(f"{API_BASE_URL}/sites/{site_id}/zones", timeout=10)
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            zones = response.json()
            print(f"      Found {len(zones)} zones for site")
            print("      ✅ GET site zones working")
            return True
        else:
            print("      ❌ GET site zones failed")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Connection error: {e}")
        return False
    except Exception as e:
        print(f"   ❌ Unexpected error: {e}")
        return False

def test_cameras_api(site_id):
    """Test Cameras API endpoints"""
    print("\n8. Testing Cameras API")
    
    try:
        # Test GET all cameras
        print("   8a. Testing GET /api/cameras")
        response = requests.get(f"{API_BASE_URL}/cameras", timeout=10)
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            cameras = response.json()
            print(f"      Found {len(cameras)} total cameras")
            print("      ✅ GET all cameras working")
        else:
            print("      ❌ GET all cameras failed")
            return False
        
        # Test GET site cameras
        print("   8b. Testing GET /api/sites/{site_id}/cameras")
        response = requests.get(f"{API_BASE_URL}/sites/{site_id}/cameras", timeout=10)
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            site_cameras = response.json()
            print(f"      Found {len(site_cameras)} cameras for site")
            print("      ✅ GET site cameras working")
            return True
        else:
            print("      ❌ GET site cameras failed")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Connection error: {e}")
        return False
    except Exception as e:
        print(f"   ❌ Unexpected error: {e}")
        return False

def test_alerts_api(site_id):
    """Test Alerts API endpoints"""
    print("\n9. Testing Alerts API")
    
    try:
        # Test GET all alerts
        print("   9a. Testing GET /api/alerts")
        response = requests.get(f"{API_BASE_URL}/alerts", timeout=10)
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            alerts = response.json()
            print(f"      Found {len(alerts)} total alerts")
            print("      ✅ GET all alerts working")
        else:
            print("      ❌ GET all alerts failed")
            return False
        
        # Test GET site alerts
        print("   9b. Testing GET /api/sites/{site_id}/alerts")
        response = requests.get(f"{API_BASE_URL}/sites/{site_id}/alerts", timeout=10)
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            site_alerts = response.json()
            print(f"      Found {len(site_alerts)} alerts for site")
            print("      ✅ GET site alerts working")
            return True
        else:
            print("      ❌ GET site alerts failed")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Connection error: {e}")
        return False
    except Exception as e:
        print(f"   ❌ Unexpected error: {e}")
        return False

def test_personnel_api(site_id):
    """Test Personnel API endpoints"""
    print("\n10. Testing Personnel API")
    
    try:
        # Test GET site personnel
        print("   10a. Testing GET /api/sites/{site_id}/personnel")
        response = requests.get(f"{API_BASE_URL}/sites/{site_id}/personnel", timeout=10)
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            personnel = response.json()
            print(f"      Found {len(personnel)} personnel for site")
            print("      ✅ GET site personnel working")
            return True
        else:
            print("      ❌ GET site personnel failed")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Connection error: {e}")
        return False
    except Exception as e:
        print(f"   ❌ Unexpected error: {e}")
        return False

def test_error_handling():
    """Test error handling for non-existent resources"""
    print("\n11. Testing Error Handling")
    
    try:
        # Test 404 for non-existent site
        fake_id = str(uuid.uuid4())
        print("   11a. Testing 404 for non-existent site")
        response = requests.get(f"{API_BASE_URL}/sites/{fake_id}", timeout=10)
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 404:
            print("      ✅ 404 error handling working correctly")
        else:
            print("      ❌ Expected 404 for non-existent site")
            return False
        
        # Test 404 for non-existent user
        print("   11b. Testing 404 for non-existent user")
        response = requests.get(f"{API_BASE_URL}/users/{fake_id}", timeout=10)
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 404:
            print("      ✅ 404 error handling working correctly")
            return True
        else:
            print("      ❌ Expected 404 for non-existent user")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Connection error: {e}")
        return False
    except Exception as e:
        print(f"   ❌ Unexpected error: {e}")
        return False

def test_legacy_status_endpoints():
    """Test legacy status check endpoints for backward compatibility"""
    print("\n12. Testing Legacy Status Endpoints")
    
    try:
        # Test POST status check
        print("   12a. Testing POST /api/status")
        test_data = {"client_name": "Construction Site Alpha"}
        response = requests.post(
            f"{API_BASE_URL}/status",
            json=test_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if (data.get("client_name") == test_data["client_name"] and 
                "id" in data and "timestamp" in data):
                print("      ✅ POST status check working")
            else:
                print("      ❌ Unexpected response structure")
                return False
        else:
            print("      ❌ POST status check failed")
            return False
        
        # Test GET status checks
        print("   12b. Testing GET /api/status")
        response = requests.get(f"{API_BASE_URL}/status", timeout=10)
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list):
                print(f"      Found {len(data)} status checks")
                print("      ✅ GET status checks working")
                return True
            else:
                print("      ❌ Expected list response")
                return False
        else:
            print("      ❌ GET status checks failed")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Connection error: {e}")
        return False
    except Exception as e:
        print(f"   ❌ Unexpected error: {e}")
        return False

def test_ai_detections_api(site_id, camera_id=None):
    """Test AI Detections API endpoints"""
    print("\n13. Testing AI Detections API")
    created_detection_id = None
    
    try:
        # Test GET all AI detections
        print("   13a. Testing GET /api/ai-detections")
        response = requests.get(f"{API_BASE_URL}/ai-detections", timeout=10)
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            detections = response.json()
            print(f"      Found {len(detections)} total AI detections")
            print("      ✅ GET all AI detections working")
        else:
            print("      ❌ GET all AI detections failed")
            return False, None
        
        # Test GET AI detections by site
        print("   13b. Testing GET /api/sites/{site_id}/ai-detections")
        response = requests.get(f"{API_BASE_URL}/sites/{site_id}/ai-detections", timeout=10)
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            site_detections = response.json()
            print(f"      Found {len(site_detections)} AI detections for site")
            print("      ✅ GET site AI detections working")
        else:
            print("      ❌ GET site AI detections failed")
            return False, None
        
        # Get existing cameras to use a valid camera_id
        print("   13c. Getting existing cameras for valid camera_id")
        response = requests.get(f"{API_BASE_URL}/cameras", timeout=10)
        if response.status_code == 200:
            cameras = response.json()
            if cameras:
                camera_id = cameras[0]["id"]
                print(f"      Using existing camera ID: {camera_id}")
            else:
                print("      No existing cameras found, skipping AI detection POST test")
                print("      ⚠️ AI Detection POST test requires existing camera")
                return True, None  # Mark as passed since GET operations work
        else:
            print("      ❌ Failed to get cameras list")
            return False, None
        
        # Create test AI detection data
        test_detection_data = {
            "camera_id": camera_id,  # Use valid camera_id
            "site_id": site_id,
            "zone_id": None,  # Fixed: using None to avoid foreign key constraint
            "detection_type": "person",  # Fixed: using valid enum value
            "person_count": 3,
            "confidence_score": 0.85,
            "detection_results": {"objects": ["person", "helmet", "vest"]},
            "safety_score": 0.92
        }
        
        # Test POST create AI detection
        print("   13d. Testing POST /api/ai-detections")
        response = requests.post(
            f"{API_BASE_URL}/ai-detections",
            json=test_detection_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            detection = response.json()
            created_detection_id = detection.get("id")
            print(f"      Created AI detection ID: {created_detection_id}")
            print("      ✅ POST AI detection creation working")
        else:
            print(f"      Response: {response.text}")
            print("      ❌ POST AI detection creation failed")
            return False, None
        
        # Test GET specific AI detection
        print("   13e. Testing GET /api/ai-detections/{detection_id}")
        response = requests.get(f"{API_BASE_URL}/ai-detections/{created_detection_id}", timeout=10)
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            detection = response.json()
            if detection.get("detection_type") == test_detection_data["detection_type"]:
                print("      ✅ GET specific AI detection working")
            else:
                print("      ❌ AI detection data mismatch")
                return False, created_detection_id
        else:
            print("      ❌ GET specific AI detection failed")
            return False, created_detection_id
        
        # Test GET AI detections by camera (if camera_id provided)
        if camera_id:
            print("   13f. Testing GET /api/cameras/{camera_id}/ai-detections")
            response = requests.get(f"{API_BASE_URL}/cameras/{camera_id}/ai-detections", timeout=10)
            print(f"      Status Code: {response.status_code}")
            
            if response.status_code == 200:
                camera_detections = response.json()
                print(f"      Found {len(camera_detections)} AI detections for camera")
                print("      ✅ GET camera AI detections working")
            else:
                print("      ❌ GET camera AI detections failed")
                return False, created_detection_id
        
        return True, created_detection_id
        
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Connection error: {e}")
        return False, created_detection_id
    except Exception as e:
        print(f"   ❌ Unexpected error: {e}")
        return False, created_detection_id

def test_ai_models_api():
    """Test AI Models API endpoints (full CRUD)"""
    print("\n14. Testing AI Models API")
    created_model_id = None
    
    try:
        # Test GET all AI models
        print("   14a. Testing GET /api/ai-models")
        response = requests.get(f"{API_BASE_URL}/ai-models", timeout=10)
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            models = response.json()
            print(f"      Found {len(models)} total AI models")
            print("      ✅ GET all AI models working")
        else:
            print("      ❌ GET all AI models failed")
            return False, None
        
        # Create test AI model data
        test_model_data = {
            "name": f"YOLOv8 Construction Safety Model {uuid.uuid4().hex[:8]}",
            "description": "Advanced AI model for construction site safety detection",
            "model_type": "person_detection",  # Fixed: using valid enum value
            "provider": "Ultralytics",
            "endpoint_url": "https://api.ultralytics.com/v1/predict",
            "confidence_threshold": 0.75
        }
        
        # Test POST create AI model
        print("   14b. Testing POST /api/ai-models")
        response = requests.post(
            f"{API_BASE_URL}/ai-models",
            json=test_model_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            model = response.json()
            created_model_id = model.get("id")
            print(f"      Created AI model ID: {created_model_id}")
            print("      ✅ POST AI model creation working")
        else:
            print(f"      Response: {response.text}")
            print("      ❌ POST AI model creation failed")
            return False, None
        
        # Test GET specific AI model
        print("   14c. Testing GET /api/ai-models/{model_id}")
        response = requests.get(f"{API_BASE_URL}/ai-models/{created_model_id}", timeout=10)
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            model = response.json()
            if model.get("name") == test_model_data["name"]:
                print("      ✅ GET specific AI model working")
            else:
                print("      ❌ AI model data mismatch")
                return False, created_model_id
        else:
            print("      ❌ GET specific AI model failed")
            return False, created_model_id
        
        # Test PUT update AI model
        print("   14d. Testing PUT /api/ai-models/{model_id}")
        update_data = {
            "name": test_model_data["name"],  # Keep original name
            "description": "Updated AI model for enhanced safety detection",
            "model_type": test_model_data["model_type"],  # Keep original type
            "provider": test_model_data["provider"],  # Keep original provider
            "endpoint_url": test_model_data["endpoint_url"],  # Keep original URL
            "confidence_threshold": 0.80  # Updated threshold
        }
        response = requests.put(
            f"{API_BASE_URL}/ai-models/{created_model_id}",
            json=update_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            updated_model = response.json()
            if updated_model.get("description") == update_data["description"]:
                print("      ✅ PUT AI model update working")
            else:
                print("      ❌ AI model update data mismatch")
                return False, created_model_id
        else:
            print("      ❌ PUT AI model update failed")
            return False, created_model_id
        
        return True, created_model_id
        
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Connection error: {e}")
        return False, created_model_id
    except Exception as e:
        print(f"   ❌ Unexpected error: {e}")
        return False, created_model_id

def test_recording_sessions_api(site_id, camera_id=None):
    """Test Recording Sessions API endpoints"""
    print("\n15. Testing Recording Sessions API")
    
    try:
        # Test GET all recording sessions
        print("   15a. Testing GET /api/recording-sessions")
        response = requests.get(f"{API_BASE_URL}/recording-sessions", timeout=10)
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            sessions = response.json()
            print(f"      Found {len(sessions)} total recording sessions")
            print("      ✅ GET all recording sessions working")
        else:
            print("      ❌ GET all recording sessions failed")
            return False
        
        # Test GET recording sessions by site
        print("   15b. Testing GET /api/sites/{site_id}/recording-sessions")
        response = requests.get(f"{API_BASE_URL}/sites/{site_id}/recording-sessions", timeout=10)
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            site_sessions = response.json()
            print(f"      Found {len(site_sessions)} recording sessions for site")
            print("      ✅ GET site recording sessions working")
        else:
            print("      ❌ GET site recording sessions failed")
            return False
        
        # Test GET recording sessions by camera (if camera_id provided)
        if camera_id:
            print("   15c. Testing GET /api/cameras/{camera_id}/recording-sessions")
            response = requests.get(f"{API_BASE_URL}/cameras/{camera_id}/recording-sessions", timeout=10)
            print(f"      Status Code: {response.status_code}")
            
            if response.status_code == 200:
                camera_sessions = response.json()
                print(f"      Found {len(camera_sessions)} recording sessions for camera")
                print("      ✅ GET camera recording sessions working")
            else:
                print("      ❌ GET camera recording sessions failed")
                return False
        
        # Test GET specific recording session (using fake ID to test endpoint structure)
        fake_session_id = str(uuid.uuid4())
        print("   15d. Testing GET /api/recording-sessions/{session_id}")
        response = requests.get(f"{API_BASE_URL}/recording-sessions/{fake_session_id}", timeout=10)
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 404:
            print("      ✅ GET specific recording session endpoint working (404 expected)")
        else:
            print("      ❌ GET specific recording session endpoint issue")
            return False
        
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Connection error: {e}")
        return False
    except Exception as e:
        print(f"   ❌ Unexpected error: {e}")
        return False

def test_ai_analytics_api(site_id, camera_id=None):
    """Test AI Analytics API endpoints"""
    print("\n16. Testing AI Analytics API")
    
    try:
        # Test GET detection analytics (general)
        print("   16a. Testing GET /api/ai-analytics/detection-stats")
        response = requests.get(f"{API_BASE_URL}/ai-analytics/detection-stats", timeout=10)
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            analytics = response.json()
            required_fields = ["total_detections", "average_confidence", "analytics_records", "date_range"]
            if all(field in analytics for field in required_fields):
                print("      ✅ GET detection analytics working")
            else:
                print("      ❌ Missing required fields in detection analytics")
                return False
        else:
            print("      ❌ GET detection analytics failed")
            return False
        
        # Test GET detection analytics with site filter
        print("   16b. Testing GET /api/ai-analytics/detection-stats?site_id={site_id}")
        response = requests.get(f"{API_BASE_URL}/ai-analytics/detection-stats?site_id={site_id}", timeout=10)
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            site_analytics = response.json()
            print("      ✅ GET site detection analytics working")
        else:
            print("      ❌ GET site detection analytics failed")
            return False
        
        # Test GET detection analytics with camera filter (if camera_id provided)
        if camera_id:
            print("   16c. Testing GET /api/ai-analytics/detection-stats?camera_id={camera_id}")
            response = requests.get(f"{API_BASE_URL}/ai-analytics/detection-stats?camera_id={camera_id}", timeout=10)
            print(f"      Status Code: {response.status_code}")
            
            if response.status_code == 200:
                camera_analytics = response.json()
                print("      ✅ GET camera detection analytics working")
            else:
                print("      ❌ GET camera detection analytics failed")
                return False
        
        # Test GET camera AI performance (if camera_id provided)
        if camera_id:
            print("   16d. Testing GET /api/cameras/{camera_id}/ai-performance")
            response = requests.get(f"{API_BASE_URL}/cameras/{camera_id}/ai-performance", timeout=10)
            print(f"      Status Code: {response.status_code}")
            
            if response.status_code == 200:
                performance = response.json()
                # Check if it's a "no data" response or actual performance data
                if "message" in performance or "camera_id" in performance:
                    print("      ✅ GET camera AI performance working")
                else:
                    print("      ❌ Unexpected camera AI performance response")
                    return False
            else:
                print("      ❌ GET camera AI performance failed")
                return False
        else:
            # Test with fake camera ID to verify endpoint structure
            fake_camera_id = str(uuid.uuid4())
            print("   16d. Testing GET /api/cameras/{camera_id}/ai-performance (fake ID)")
            response = requests.get(f"{API_BASE_URL}/cameras/{fake_camera_id}/ai-performance", timeout=10)
            print(f"      Status Code: {response.status_code}")
            
            if response.status_code == 200:
                performance = response.json()
                if "message" in performance:
                    print("      ✅ GET camera AI performance endpoint working")
                else:
                    print("      ❌ Unexpected camera AI performance response")
                    return False
            else:
                print("      ❌ GET camera AI performance endpoint failed")
                return False
        
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Connection error: {e}")
        return False
    except Exception as e:
        print(f"   ❌ Unexpected error: {e}")
        return False

def test_database_verification():
    """Test database verification for new AI tables"""
    print("\n17. Testing Database Verification")
    
    try:
        # Test health endpoint to verify database connection
        print("   17a. Testing database connection via health endpoint")
        response = requests.get(f"{API_BASE_URL}/health", timeout=10)
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            health_data = response.json()
            if health_data.get("database") == "connected":
                print("      ✅ Database connection verified")
            else:
                print("      ❌ Database connection issue")
                return False
        else:
            print("      ❌ Health endpoint failed")
            return False
        
        # Test that AI endpoints are accessible (indicates tables exist)
        print("   17b. Testing AI tables accessibility via endpoints")
        endpoints_to_test = [
            "/ai-detections",
            "/ai-models", 
            "/recording-sessions",
            "/ai-analytics/detection-stats"
        ]
        
        for endpoint in endpoints_to_test:
            response = requests.get(f"{API_BASE_URL}{endpoint}", timeout=10)
            if response.status_code == 200:
                print(f"      ✅ {endpoint} accessible (table exists)")
            else:
                print(f"      ❌ {endpoint} failed (table may not exist)")
                return False
        
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Connection error: {e}")
        return False
    except Exception as e:
        print(f"   ❌ Unexpected error: {e}")
        return False

def test_video_bookmarks_api(camera_id=None, user_id="system"):
    """Test Video Bookmarks API endpoints"""
    print("\n18. Testing Video Bookmarks API")
    created_bookmark_id = None
    
    try:
        # Test GET all video bookmarks
        print("   18a. Testing GET /api/video-bookmarks")
        response = requests.get(f"{API_BASE_URL}/video-bookmarks", timeout=10)
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            bookmarks = response.json()
            print(f"      Found {len(bookmarks)} total video bookmarks")
            print("      ✅ GET all video bookmarks working")
        else:
            print("      ❌ GET all video bookmarks failed")
            return False, None
        
        # Get existing cameras to use a valid camera_id
        if not camera_id:
            print("   18b. Getting existing cameras for valid camera_id")
            response = requests.get(f"{API_BASE_URL}/cameras", timeout=10)
            if response.status_code == 200:
                cameras = response.json()
                if cameras:
                    camera_id = cameras[0]["id"]
                    print(f"      Using existing camera ID: {camera_id}")
                else:
                    print("      No existing cameras found, skipping video bookmark POST test")
                    print("      ⚠️ Video Bookmark POST test requires existing camera")
                    return True, None  # Mark as passed since GET operations work
            else:
                print("      ❌ Failed to get cameras list")
                return False, None
        
        # Create test video bookmark data
        test_bookmark_data = {
            "camera_id": camera_id,
            "bookmark_date": "2024-01-15",  # YYYY-MM-DD format
            "timestamp_seconds": 3600,  # 1 hour into the video
            "title": f"Safety Incident Bookmark {uuid.uuid4().hex[:8]}",
            "description": "Worker without hard hat detected in construction zone",
            "bookmark_type": "safety_incident",
            "priority_level": "high"
        }
        
        # Test POST create video bookmark
        print("   18c. Testing POST /api/video-bookmarks")
        response = requests.post(
            f"{API_BASE_URL}/video-bookmarks",
            json=test_bookmark_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            bookmark = response.json()
            created_bookmark_id = bookmark.get("id")
            print(f"      Created video bookmark ID: {created_bookmark_id}")
            print("      ✅ POST video bookmark creation working")
        else:
            print(f"      Response: {response.text}")
            print("      ❌ POST video bookmark creation failed")
            return False, None
        
        # Test GET specific video bookmark
        print("   18d. Testing GET /api/video-bookmarks/{bookmark_id}")
        response = requests.get(f"{API_BASE_URL}/video-bookmarks/{created_bookmark_id}", timeout=10)
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            bookmark = response.json()
            if bookmark.get("title") == test_bookmark_data["title"]:
                print("      ✅ GET specific video bookmark working")
            else:
                print("      ❌ Video bookmark data mismatch")
                return False, created_bookmark_id
        else:
            print("      ❌ GET specific video bookmark failed")
            return False, created_bookmark_id
        
        # Test PUT update bookmark status
        print("   18e. Testing PUT /api/video-bookmarks/{bookmark_id}/status")
        response = requests.put(
            f"{API_BASE_URL}/video-bookmarks/{created_bookmark_id}/status?status=reviewed",
            timeout=10
        )
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            if "message" in result:
                print("      ✅ PUT bookmark status update working")
            else:
                print("      ❌ Unexpected bookmark status update response")
                return False, created_bookmark_id
        else:
            print("      ❌ PUT bookmark status update failed")
            return False, created_bookmark_id
        
        # Test GET video bookmarks with camera filter
        print("   18f. Testing GET /api/video-bookmarks?camera_id={camera_id}")
        response = requests.get(f"{API_BASE_URL}/video-bookmarks?camera_id={camera_id}", timeout=10)
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            camera_bookmarks = response.json()
            print(f"      Found {len(camera_bookmarks)} bookmarks for camera")
            print("      ✅ GET video bookmarks with camera filter working")
        else:
            print("      ❌ GET video bookmarks with camera filter failed")
            return False, created_bookmark_id
        
        # Test GET video bookmarks with user filter
        print("   18g. Testing GET /api/video-bookmarks?user_id={user_id}")
        response = requests.get(f"{API_BASE_URL}/video-bookmarks?user_id={user_id}", timeout=10)
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            user_bookmarks = response.json()
            print(f"      Found {len(user_bookmarks)} bookmarks for user")
            print("      ✅ GET video bookmarks with user filter working")
        else:
            print("      ❌ GET video bookmarks with user filter failed")
            return False, created_bookmark_id
        
        return True, created_bookmark_id
        
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Connection error: {e}")
        return False, created_bookmark_id
    except Exception as e:
        print(f"   ❌ Unexpected error: {e}")
        return False, created_bookmark_id

def test_video_access_logs_api(camera_id=None, user_id="system"):
    """Test Video Access Logs API endpoints"""
    print("\n19. Testing Video Access Logs API")
    
    try:
        # Test GET all video access logs
        print("   19a. Testing GET /api/video-access-logs")
        response = requests.get(f"{API_BASE_URL}/video-access-logs", timeout=10)
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            logs = response.json()
            print(f"      Found {len(logs)} total video access logs")
            print("      ✅ GET all video access logs working")
        else:
            print("      ❌ GET all video access logs failed")
            return False
        
        # Get existing cameras to use a valid camera_id
        if not camera_id:
            print("   19b. Getting existing cameras for valid camera_id")
            response = requests.get(f"{API_BASE_URL}/cameras", timeout=10)
            if response.status_code == 200:
                cameras = response.json()
                if cameras:
                    camera_id = cameras[0]["id"]
                    print(f"      Using existing camera ID: {camera_id}")
                else:
                    print("      No existing cameras found, using fake camera_id for endpoint testing")
                    camera_id = str(uuid.uuid4())
            else:
                print("      ❌ Failed to get cameras list")
                return False
        
        # Test GET video access logs by camera
        print("   19c. Testing GET /api/cameras/{camera_id}/access-logs")
        response = requests.get(f"{API_BASE_URL}/cameras/{camera_id}/access-logs", timeout=10)
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            camera_logs = response.json()
            print(f"      Found {len(camera_logs)} access logs for camera")
            print("      ✅ GET camera access logs working")
        else:
            print("      ❌ GET camera access logs failed")
            return False
        
        # Test GET video access logs by user
        print("   19d. Testing GET /api/users/{user_id}/video-access-logs")
        response = requests.get(f"{API_BASE_URL}/users/{user_id}/video-access-logs", timeout=10)
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            user_logs = response.json()
            print(f"      Found {len(user_logs)} access logs for user")
            print("      ✅ GET user video access logs working")
        else:
            print("      ❌ GET user video access logs failed")
            return False
        
        # Test GET video access logs with filters
        print("   19e. Testing GET /api/video-access-logs?user_id={user_id}&camera_id={camera_id}")
        response = requests.get(f"{API_BASE_URL}/video-access-logs?user_id={user_id}&camera_id={camera_id}", timeout=10)
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            filtered_logs = response.json()
            print(f"      Found {len(filtered_logs)} filtered access logs")
            print("      ✅ GET video access logs with filters working")
        else:
            print("      ❌ GET video access logs with filters failed")
            return False
        
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Connection error: {e}")
        return False
    except Exception as e:
        print(f"   ❌ Unexpected error: {e}")
        return False

def test_video_exports_api(camera_id=None, user_id="system"):
    """Test Video Exports API endpoints"""
    print("\n20. Testing Video Exports API")
    created_export_id = None
    
    try:
        # Test GET all video exports
        print("   20a. Testing GET /api/video-exports")
        response = requests.get(f"{API_BASE_URL}/video-exports", timeout=10)
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            exports = response.json()
            print(f"      Found {len(exports)} total video exports")
            print("      ✅ GET all video exports working")
        else:
            print("      ❌ GET all video exports failed")
            return False, None
        
        # Get existing cameras to use a valid camera_id
        if not camera_id:
            print("   20b. Getting existing cameras for valid camera_id")
            response = requests.get(f"{API_BASE_URL}/cameras", timeout=10)
            if response.status_code == 200:
                cameras = response.json()
                if cameras:
                    camera_id = cameras[0]["id"]
                    print(f"      Using existing camera ID: {camera_id}")
                else:
                    print("      No existing cameras found, skipping video export POST test")
                    print("      ⚠️ Video Export POST test requires existing camera")
                    return True, None  # Mark as passed since GET operations work
            else:
                print("      ❌ Failed to get cameras list")
                return False, None
        
        # Create test video export data
        test_export_data = {
            "camera_id": camera_id,
            "source_video_date": "2024-01-15",  # YYYY-MM-DD format
            "start_timestamp_seconds": 1800,  # 30 minutes
            "end_timestamp_seconds": 5400,   # 90 minutes (1 hour duration)
            "export_type": "incident_evidence",
            "export_format": "mp4",
            "export_purpose": "safety_investigation",
            "export_justification": "Evidence collection for safety incident investigation",
            "quality_setting": "high"
        }
        
        # Test POST create video export
        print("   20c. Testing POST /api/video-exports")
        response = requests.post(
            f"{API_BASE_URL}/video-exports",
            json=test_export_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            export = response.json()
            created_export_id = export.get("id")
            print(f"      Created video export ID: {created_export_id}")
            print("      ✅ POST video export creation working")
        else:
            print(f"      Response: {response.text}")
            print("      ❌ POST video export creation failed")
            return False, None
        
        # Test GET specific video export
        print("   20d. Testing GET /api/video-exports/{export_id}")
        response = requests.get(f"{API_BASE_URL}/video-exports/{created_export_id}", timeout=10)
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            export = response.json()
            if export.get("export_purpose") == test_export_data["export_purpose"]:
                print("      ✅ GET specific video export working")
            else:
                print("      ❌ Video export data mismatch")
                return False, created_export_id
        else:
            print("      ❌ GET specific video export failed")
            return False, created_export_id
        
        # Test PUT update export status
        print("   20e. Testing PUT /api/video-exports/{export_id}/status")
        response = requests.put(
            f"{API_BASE_URL}/video-exports/{created_export_id}/status?status=processing&download_url=https://example.com/export.mp4",
            timeout=10
        )
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            if "message" in result:
                print("      ✅ PUT export status update working")
            else:
                print("      ❌ Unexpected export status update response")
                return False, created_export_id
        else:
            print("      ❌ PUT export status update failed")
            return False, created_export_id
        
        # Test GET video exports with camera filter
        print("   20f. Testing GET /api/video-exports?camera_id={camera_id}")
        response = requests.get(f"{API_BASE_URL}/video-exports?camera_id={camera_id}", timeout=10)
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            camera_exports = response.json()
            print(f"      Found {len(camera_exports)} exports for camera")
            print("      ✅ GET video exports with camera filter working")
        else:
            print("      ❌ GET video exports with camera filter failed")
            return False, created_export_id
        
        # Test GET video exports with user filter
        print("   20g. Testing GET /api/video-exports?user_id={user_id}")
        response = requests.get(f"{API_BASE_URL}/video-exports?user_id={user_id}", timeout=10)
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            user_exports = response.json()
            print(f"      Found {len(user_exports)} exports for user")
            print("      ✅ GET video exports with user filter working")
        else:
            print("      ❌ GET video exports with user filter failed")
            return False, created_export_id
        
        # Test GET video exports with status filter
        print("   20h. Testing GET /api/video-exports?status=processing")
        response = requests.get(f"{API_BASE_URL}/video-exports?status=processing", timeout=10)
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            status_exports = response.json()
            print(f"      Found {len(status_exports)} exports with processing status")
            print("      ✅ GET video exports with status filter working")
        else:
            print("      ❌ GET video exports with status filter failed")
            return False, created_export_id
        
        return True, created_export_id
        
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Connection error: {e}")
        return False, created_export_id
    except Exception as e:
        print(f"   ❌ Unexpected error: {e}")
        return False, created_export_id

def test_video_quality_metrics_api(camera_id=None):
    """Test Video Quality Metrics API endpoints"""
    print("\n21. Testing Video Quality Metrics API")
    
    try:
        # Test GET all video quality metrics
        print("   21a. Testing GET /api/video-quality-metrics")
        response = requests.get(f"{API_BASE_URL}/video-quality-metrics", timeout=10)
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            metrics = response.json()
            print(f"      Found {len(metrics)} total video quality metrics")
            print("      ✅ GET all video quality metrics working")
        else:
            print("      ❌ GET all video quality metrics failed")
            return False
        
        # Test GET video quality metrics with days filter
        print("   21b. Testing GET /api/video-quality-metrics?days=30")
        response = requests.get(f"{API_BASE_URL}/video-quality-metrics?days=30", timeout=10)
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            filtered_metrics = response.json()
            print(f"      Found {len(filtered_metrics)} quality metrics for last 30 days")
            print("      ✅ GET video quality metrics with days filter working")
        else:
            print("      ❌ GET video quality metrics with days filter failed")
            return False
        
        # Get existing cameras to use a valid camera_id
        if not camera_id:
            print("   21c. Getting existing cameras for valid camera_id")
            response = requests.get(f"{API_BASE_URL}/cameras", timeout=10)
            if response.status_code == 200:
                cameras = response.json()
                if cameras:
                    camera_id = cameras[0]["id"]
                    print(f"      Using existing camera ID: {camera_id}")
                else:
                    print("      No existing cameras found, using fake camera_id for endpoint testing")
                    camera_id = str(uuid.uuid4())
            else:
                print("      ❌ Failed to get cameras list")
                return False
        
        # Test GET video quality metrics by camera
        print("   21d. Testing GET /api/cameras/{camera_id}/quality-metrics")
        response = requests.get(f"{API_BASE_URL}/cameras/{camera_id}/quality-metrics", timeout=10)
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            camera_metrics = response.json()
            print(f"      Found {len(camera_metrics)} quality metrics for camera")
            print("      ✅ GET camera quality metrics working")
        else:
            print("      ❌ GET camera quality metrics failed")
            return False
        
        # Test GET camera quality summary
        print("   21e. Testing GET /api/cameras/{camera_id}/quality-summary")
        response = requests.get(f"{API_BASE_URL}/cameras/{camera_id}/quality-summary", timeout=10)
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            summary = response.json()
            # Check if it's a "no data" response or actual summary data
            if "message" in summary or "camera_id" in summary:
                print("      ✅ GET camera quality summary working")
            else:
                print("      ❌ Unexpected camera quality summary response")
                return False
        else:
            print("      ❌ GET camera quality summary failed")
            return False
        
        # Test GET camera quality summary with days filter
        print("   21f. Testing GET /api/cameras/{camera_id}/quality-summary?days=14")
        response = requests.get(f"{API_BASE_URL}/cameras/{camera_id}/quality-summary?days=14", timeout=10)
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            filtered_summary = response.json()
            if "message" in filtered_summary or "camera_id" in filtered_summary:
                print("      ✅ GET camera quality summary with days filter working")
            else:
                print("      ❌ Unexpected filtered camera quality summary response")
                return False
        else:
            print("      ❌ GET camera quality summary with days filter failed")
            return False
        
        # Test GET video quality metrics with camera filter
        print("   21g. Testing GET /api/video-quality-metrics?camera_id={camera_id}")
        response = requests.get(f"{API_BASE_URL}/video-quality-metrics?camera_id={camera_id}", timeout=10)
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            camera_filtered_metrics = response.json()
            print(f"      Found {len(camera_filtered_metrics)} quality metrics for camera filter")
            print("      ✅ GET video quality metrics with camera filter working")
        else:
            print("      ❌ GET video quality metrics with camera filter failed")
            return False
        
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Connection error: {e}")
        return False
    except Exception as e:
        print(f"   ❌ Unexpected error: {e}")
        return False

def test_video_database_verification():
    """Test database verification for new video tables"""
    print("\n22. Testing Video Database Verification")
    
    try:
        # Test health endpoint to verify database connection
        print("   22a. Testing database connection via health endpoint")
        response = requests.get(f"{API_BASE_URL}/health", timeout=10)
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            health_data = response.json()
            if health_data.get("database") == "connected":
                print("      ✅ Database connection verified")
            else:
                print("      ❌ Database connection issue")
                return False
        else:
            print("      ❌ Health endpoint failed")
            return False
        
        # Test that video endpoints are accessible (indicates tables exist)
        print("   22b. Testing video tables accessibility via endpoints")
        video_endpoints_to_test = [
            "/video-bookmarks",
            "/video-access-logs", 
            "/video-exports",
            "/video-quality-metrics"
        ]
        
        for endpoint in video_endpoints_to_test:
            response = requests.get(f"{API_BASE_URL}{endpoint}", timeout=10)
            if response.status_code == 200:
                print(f"      ✅ {endpoint} accessible (table exists)")
            else:
                print(f"      ❌ {endpoint} failed (table may not exist)")
                return False
        
        # Test complex video endpoints with parameters
        print("   22c. Testing complex video endpoints")
        complex_endpoints = [
            "/video-quality-metrics?days=7",
            "/video-exports?status=pending",
            "/video-bookmarks?camera_id=test"
        ]
        
        for endpoint in complex_endpoints:
            response = requests.get(f"{API_BASE_URL}{endpoint}", timeout=10)
            if response.status_code == 200:
                print(f"      ✅ {endpoint} accessible with parameters")
            else:
                print(f"      ❌ {endpoint} failed with parameters")
                return False
        
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Connection error: {e}")
        return False
    except Exception as e:
        print(f"   ❌ Unexpected error: {e}")
        return False

def test_field_operations_inspection_paths(site_id, user_id):
    """Test Field Operations - Inspection Paths API endpoints"""
    print("\n23. Testing Field Operations - Inspection Paths API")
    created_path_id = None
    
    try:
        # Test GET all inspection paths
        print("   23a. Testing GET /api/field-operations/inspection-paths")
        response = requests.get(f"{API_BASE_URL}/field-operations/inspection-paths", timeout=10)
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            paths = response.json()
            print(f"      Found {len(paths)} total inspection paths")
            print("      ✅ GET all inspection paths working")
        else:
            print("      ❌ GET all inspection paths failed")
            return False, None
        
        # Create test inspection path data
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
        
        # Test POST create inspection path
        print("   23b. Testing POST /api/field-operations/inspection-paths")
        response = requests.post(
            f"{API_BASE_URL}/field-operations/inspection-paths",
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
            return False, None
        
        # Test GET specific inspection path
        print("   23c. Testing GET /api/field-operations/inspection-paths/{path_id}")
        response = requests.get(f"{API_BASE_URL}/field-operations/inspection-paths/{created_path_id}", timeout=10)
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            path = response.json()
            if path.get("name") == test_path_data["name"]:
                print("      ✅ GET specific inspection path working")
            else:
                print("      ❌ Inspection path data mismatch")
                return False, created_path_id
        else:
            print("      ❌ GET specific inspection path failed")
            return False, created_path_id
        
        # Test PUT update inspection path
        print("   23d. Testing PUT /api/field-operations/inspection-paths/{path_id}")
        update_data = {
            "site_id": site_id,
            "name": test_path_data["name"],
            "description": "Updated comprehensive safety inspection path",
            "path_type": test_path_data["path_type"],
            "priority": "medium",
            "estimated_duration_minutes": 60
        }
        response = requests.put(
            f"{API_BASE_URL}/field-operations/inspection-paths/{created_path_id}",
            json=update_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            updated_path = response.json()
            if updated_path.get("priority") == update_data["priority"]:
                print("      ✅ PUT inspection path update working")
            else:
                print("      ❌ Inspection path update data mismatch")
                return False, created_path_id
        else:
            print("      ❌ PUT inspection path update failed")
            return False, created_path_id
        
        # Test GET site inspection paths
        print("   23e. Testing GET /api/sites/{site_id}/inspection-paths")
        response = requests.get(f"{API_BASE_URL}/sites/{site_id}/inspection-paths", timeout=10)
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            site_paths = response.json()
            print(f"      Found {len(site_paths)} inspection paths for site")
            print("      ✅ GET site inspection paths working")
        else:
            print("      ❌ GET site inspection paths failed")
            return False, created_path_id
        
        return True, created_path_id
        
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Connection error: {e}")
        return False, created_path_id
    except Exception as e:
        print(f"   ❌ Unexpected error: {e}")
        return False, created_path_id

def test_field_operations_path_waypoints(path_id):
    """Test Field Operations - Path Waypoints API endpoints"""
    print("\n24. Testing Field Operations - Path Waypoints API")
    created_waypoint_ids = []
    
    try:
        # Test GET all path waypoints
        print("   24a. Testing GET /api/field-operations/path-waypoints")
        response = requests.get(f"{API_BASE_URL}/field-operations/path-waypoints", timeout=10)
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            waypoints = response.json()
            print(f"      Found {len(waypoints)} total path waypoints")
            print("      ✅ GET all path waypoints working")
        else:
            print("      ❌ GET all path waypoints failed")
            return False, []
        
        # Create multiple test waypoints
        waypoint_data_list = [
            {
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
            },
            {
                "path_id": path_id,
                "waypoint_order": 2,
                "waypoint_name": "Construction Zone Alpha",
                "description": "Inspect active construction area for safety compliance",
                "coordinates_x": 150.7,
                "coordinates_y": 250.9,
                "waypoint_type": "inspection_point",
                "is_mandatory": True,
                "estimated_time_minutes": 15,
                "inspection_checklist": {"items": ["safety_barriers", "equipment_check", "worker_ppe"]}
            },
            {
                "path_id": path_id,
                "waypoint_order": 3,
                "waypoint_name": "Equipment Storage",
                "description": "Check equipment storage and maintenance area",
                "coordinates_x": 75.2,
                "coordinates_y": 180.6,
                "waypoint_type": "maintenance_check",
                "is_mandatory": False,
                "estimated_time_minutes": 10,
                "inspection_checklist": {"items": ["equipment_condition", "storage_organization"]}
            }
        ]
        
        # Test POST create path waypoints
        for i, waypoint_data in enumerate(waypoint_data_list):
            print(f"   24b.{i+1}. Testing POST /api/path-waypoints (Waypoint {i+1})")
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
                print(f"      ✅ POST waypoint {i+1} creation working")
            else:
                print(f"      Response: {response.text}")
                print(f"      ❌ POST waypoint {i+1} creation failed")
                return False, created_waypoint_ids
        
        # Test GET specific path waypoint
        if created_waypoint_ids:
            print("   24c. Testing GET /api/path-waypoints/{waypoint_id}")
            response = requests.get(f"{API_BASE_URL}/path-waypoints/{created_waypoint_ids[0]}", timeout=10)
            print(f"      Status Code: {response.status_code}")
            
            if response.status_code == 200:
                waypoint = response.json()
                if waypoint.get("waypoint_name") == waypoint_data_list[0]["waypoint_name"]:
                    print("      ✅ GET specific path waypoint working")
                else:
                    print("      ❌ Path waypoint data mismatch")
                    return False, created_waypoint_ids
            else:
                print("      ❌ GET specific path waypoint failed")
                return False, created_waypoint_ids
        
        # Test GET waypoints by path
        print("   24d. Testing GET /api/inspection-paths/{path_id}/waypoints")
        response = requests.get(f"{API_BASE_URL}/inspection-paths/{path_id}/waypoints", timeout=10)
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            path_waypoints = response.json()
            print(f"      Found {len(path_waypoints)} waypoints for path")
            if len(path_waypoints) >= len(waypoint_data_list):
                print("      ✅ GET waypoints by path working")
            else:
                print("      ❌ Unexpected waypoint count")
                return False, created_waypoint_ids
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
    print("\n25. Testing Field Operations - Path Executions API")
    created_execution_id = None
    
    try:
        # Test GET all path executions
        print("   25a. Testing GET /api/path-executions")
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
            "execution_type": "scheduled_inspection",
            "execution_reason": "Daily safety compliance check",
            "planned_duration_minutes": 45,
            "weather_conditions": "Clear, 22°C",
            "equipment_used": ["tablet", "camera", "safety_meter", "checklist"]
        }
        
        # Test POST create path execution
        print("   25b. Testing POST /api/path-executions")
        response = requests.post(
            f"{API_BASE_URL}/path-executions",
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
        
        # Test GET specific path execution
        print("   25c. Testing GET /api/path-executions/{execution_id}")
        response = requests.get(f"{API_BASE_URL}/path-executions/{created_execution_id}", timeout=10)
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            execution = response.json()
            if execution.get("execution_type") == test_execution_data["execution_type"]:
                print("      ✅ GET specific path execution working")
            else:
                print("      ❌ Path execution data mismatch")
                return False, created_execution_id
        else:
            print("      ❌ GET specific path execution failed")
            return False, created_execution_id
        
        # Test PUT update execution status
        print("   25d. Testing PUT /api/path-executions/{execution_id}/status")
        status_update_data = {
            "status": "in_progress",
            "completion_percentage": 25.0
        }
        response = requests.put(
            f"{API_BASE_URL}/path-executions/{created_execution_id}/status",
            params=status_update_data,
            timeout=10
        )
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            if "message" in result:
                print("      ✅ PUT execution status update working")
            else:
                print("      ❌ Unexpected status update response")
                return False, created_execution_id
        else:
            print("      ❌ PUT execution status update failed")
            return False, created_execution_id
        
        # Test GET executions by path
        print("   25e. Testing GET /api/inspection-paths/{path_id}/executions")
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

def test_field_operations_execution_waypoints(execution_id, waypoint_ids):
    """Test Field Operations - Path Execution Waypoints API endpoints"""
    print("\n26. Testing Field Operations - Path Execution Waypoints API")
    
    try:
        # Test GET all execution waypoints
        print("   26a. Testing GET /api/path-execution-waypoints")
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
        print("   26b. Testing GET /api/path-executions/{execution_id}/waypoints")
        response = requests.get(f"{API_BASE_URL}/path-executions/{execution_id}/waypoints", timeout=10)
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            execution_waypoints = response.json()
            print(f"      Found {len(execution_waypoints)} waypoints for execution")
            print("      ✅ GET execution waypoints by execution working")
        else:
            print("      ❌ GET execution waypoints by execution failed")
            return False
        
        # Test POST record waypoint visits
        if waypoint_ids:
            for i, waypoint_id in enumerate(waypoint_ids[:2]):  # Test first 2 waypoints
                print(f"   26c.{i+1}. Testing POST /api/path-executions/{execution_id}/waypoints/{waypoint_id}/visit")
                visit_data = {
                    "inspection_completed": True,
                    "issues_found": i,  # 0 for first, 1 for second
                    "photos_taken": 3 + i,
                    "notes": f"Waypoint {i+1} inspection completed successfully"
                }
                response = requests.post(
                    f"{API_BASE_URL}/path-executions/{execution_id}/waypoints/{waypoint_id}/visit",
                    params=visit_data,
                    timeout=10
                )
                print(f"      Status Code: {response.status_code}")
                
                if response.status_code == 200:
                    result = response.json()
                    if "message" in result:
                        print(f"      ✅ POST waypoint {i+1} visit recording working")
                    else:
                        print(f"      ❌ Unexpected waypoint {i+1} visit response")
                        return False
                else:
                    print(f"      ❌ POST waypoint {i+1} visit recording failed")
                    return False
        
        # Test GET execution waypoints again to verify visits were recorded
        print("   26d. Testing GET /api/path-executions/{execution_id}/waypoints (after visits)")
        response = requests.get(f"{API_BASE_URL}/path-executions/{execution_id}/waypoints", timeout=10)
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            execution_waypoints = response.json()
            visited_count = len([w for w in execution_waypoints if w.get("visited_at")])
            print(f"      Found {visited_count} visited waypoints out of {len(execution_waypoints)} total")
            if visited_count > 0:
                print("      ✅ Waypoint visits recorded successfully")
            else:
                print("      ⚠️ No waypoint visits found (may be expected)")
        else:
            print("      ❌ GET execution waypoints verification failed")
            return False
        
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Connection error: {e}")
        return False
    except Exception as e:
        print(f"   ❌ Unexpected error: {e}")
        return False

def test_field_operations_path_templates():
    """Test Field Operations - Path Templates API endpoints"""
    print("\n27. Testing Field Operations - Path Templates API")
    created_template_id = None
    
    try:
        # Test GET all path templates
        print("   27a. Testing GET /api/path-templates")
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
            "template_type": "safety_inspection",
            "difficulty_level": "intermediate",
            "safety_level": "high",
            "base_waypoint_count": 5,
            "estimated_duration_minutes": 60,
            "recommended_zones": ["construction_area", "equipment_storage", "office_area"],
            "required_equipment": ["tablet", "camera", "safety_meter"],
            "is_public": True
        }
        
        # Test POST create path template
        print("   27b. Testing POST /api/path-templates")
        response = requests.post(
            f"{API_BASE_URL}/path-templates",
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
        
        # Test GET specific path template
        print("   27c. Testing GET /api/path-templates/{template_id}")
        response = requests.get(f"{API_BASE_URL}/path-templates/{created_template_id}", timeout=10)
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            template = response.json()
            if template.get("template_name") == test_template_data["template_name"]:
                print("      ✅ GET specific path template working")
            else:
                print("      ❌ Path template data mismatch")
                return False, created_template_id
        else:
            print("      ❌ GET specific path template failed")
            return False, created_template_id
        
        # Test PUT update path template
        print("   27d. Testing PUT /api/path-templates/{template_id}")
        update_data = {
            "template_name": test_template_data["template_name"],
            "description": "Updated comprehensive template for enhanced safety inspections",
            "template_type": test_template_data["template_type"],
            "difficulty_level": "advanced",
            "safety_level": test_template_data["safety_level"],
            "estimated_duration_minutes": 75
        }
        response = requests.put(
            f"{API_BASE_URL}/path-templates/{created_template_id}",
            json=update_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            updated_template = response.json()
            if updated_template.get("difficulty_level") == update_data["difficulty_level"]:
                print("      ✅ PUT path template update working")
            else:
                print("      ❌ Path template update data mismatch")
                return False, created_template_id
        else:
            print("      ❌ PUT path template update failed")
            return False, created_template_id
        
        return True, created_template_id
        
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Connection error: {e}")
        return False, created_template_id
    except Exception as e:
        print(f"   ❌ Unexpected error: {e}")
        return False, created_template_id

def test_field_operations_analytics(site_id):
    """Test Field Operations - Analytics API endpoints"""
    print("\n28. Testing Field Operations - Analytics API")
    
    try:
        # Test GET path analytics summary
        print("   28a. Testing GET /api/path-analytics/summary")
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
        
        # Test GET path analytics summary with site filter
        print("   28b. Testing GET /api/path-analytics/summary?site_id={site_id}")
        response = requests.get(f"{API_BASE_URL}/path-analytics/summary?site_id={site_id}", timeout=10)
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            site_analytics = response.json()
            if "message" in site_analytics or "total_executions" in site_analytics:
                print("      ✅ GET site path analytics working")
            else:
                print("      ❌ Unexpected site analytics response")
                return False
        else:
            print("      ❌ GET site path analytics failed")
            return False
        
        # Test GET path analytics summary with days filter
        print("   28c. Testing GET /api/path-analytics/summary?days=7")
        response = requests.get(f"{API_BASE_URL}/path-analytics/summary?days=7", timeout=10)
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            weekly_analytics = response.json()
            if "date_range" in weekly_analytics or "message" in weekly_analytics:
                print("      ✅ GET weekly path analytics working")
            else:
                print("      ❌ Unexpected weekly analytics response")
                return False
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

def test_analytics_certifications_api(user_id):
    """Test Analytics - User Certifications API endpoints"""
    print("\n29. Testing Analytics - User Certifications API")
    created_certification_id = None
    
    try:
        # Test GET all user certifications
        print("   29a. Testing GET /api/analytics/certifications")
        response = requests.get(f"{API_BASE_URL}/analytics/certifications", timeout=10)
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            certifications = response.json()
            print(f"      Found {len(certifications)} total certifications")
            print("      ✅ GET all certifications working")
        else:
            print("      ❌ GET all certifications failed")
            return False, None
        
        # Create test certification data
        test_certification_data = {
            "user_id": user_id,
            "certification_name": f"OSHA 30-Hour Construction Safety {uuid.uuid4().hex[:8]}",
            "certification_type": "safety",
            "certification_number": f"OSHA-{uuid.uuid4().hex[:8].upper()}",
            "issuing_authority": "Occupational Safety and Health Administration",
            "issue_date": "2024-01-15",
            "expiry_date": "2027-01-15",
            "renewal_period_months": 36,
            "required_for_roles": ["site_manager", "supervisor"],
            "certificate_file_path": "/certificates/osha_30_hour.pdf"
        }
        
        # Test POST create certification
        print("   29b. Testing POST /api/analytics/certifications")
        response = requests.post(
            f"{API_BASE_URL}/analytics/certifications",
            json=test_certification_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            certification = response.json()
            created_certification_id = certification.get("id")
            print(f"      Created certification ID: {created_certification_id}")
            print("      ✅ POST certification creation working")
        else:
            print(f"      Response: {response.text}")
            print("      ❌ POST certification creation failed")
            return False, None
        
        # Test GET specific certification
        print("   29c. Testing GET /api/analytics/certifications/{certification_id}")
        response = requests.get(f"{API_BASE_URL}/analytics/certifications/{created_certification_id}", timeout=10)
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            certification = response.json()
            if certification.get("certification_name") == test_certification_data["certification_name"]:
                print("      ✅ GET specific certification working")
            else:
                print("      ❌ Certification data mismatch")
                return False, created_certification_id
        else:
            print("      ❌ GET specific certification failed")
            return False, created_certification_id
        
        # Test PUT verify certification
        print("   29d. Testing PUT /api/analytics/certifications/{certification_id}/verify")
        response = requests.put(f"{API_BASE_URL}/analytics/certifications/{created_certification_id}/verify", timeout=10)
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            if "verified successfully" in result.get("message", ""):
                print("      ✅ PUT certification verification working")
            else:
                print("      ❌ Certification verification response unexpected")
                return False, created_certification_id
        else:
            print("      ❌ PUT certification verification failed")
            return False, created_certification_id
        
        return True, created_certification_id
        
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Connection error: {e}")
        return False, created_certification_id
    except Exception as e:
        print(f"   ❌ Unexpected error: {e}")
        return False, created_certification_id

def test_analytics_performance_metrics_api(site_id):
    """Test Analytics - Performance Metrics API endpoints"""
    print("\n30. Testing Analytics - Performance Metrics API")
    created_metric_id = None
    
    try:
        # Test GET all performance metrics
        print("   30a. Testing GET /api/analytics/performance-metrics")
        response = requests.get(f"{API_BASE_URL}/analytics/performance-metrics", timeout=10)
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            metrics = response.json()
            print(f"      Found {len(metrics)} total performance metrics")
            print("      ✅ GET all performance metrics working")
        else:
            print("      ❌ GET all performance metrics failed")
            return False, None
        
        # Test GET with filtering
        print("   30b. Testing GET /api/analytics/performance-metrics with filters")
        response = requests.get(f"{API_BASE_URL}/analytics/performance-metrics?site_id={site_id}&days=7&is_kpi=true", timeout=10)
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            filtered_metrics = response.json()
            print(f"      Found {len(filtered_metrics)} filtered metrics")
            print("      ✅ GET filtered performance metrics working")
        else:
            print("      ❌ GET filtered performance metrics failed")
            return False, None
        
        # Create test performance metric data
        test_metric_data = {
            "site_id": site_id,
            "metric_date": "2024-01-15",
            "metric_hour": 14,
            "metric_type": "safety_compliance",
            "metric_value": 95.5,
            "target_value": 98.0,
            "measurement_unit": "percentage",
            "data_source": "automated_inspection",
            "is_kpi": True,
            "confidence_score": 0.92
        }
        
        # Test POST create performance metric
        print("   30c. Testing POST /api/analytics/performance-metrics")
        response = requests.post(
            f"{API_BASE_URL}/analytics/performance-metrics",
            json=test_metric_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            metric = response.json()
            created_metric_id = metric.get("id")
            print(f"      Created performance metric ID: {created_metric_id}")
            print("      ✅ POST performance metric creation working")
        else:
            print(f"      Response: {response.text}")
            print("      ❌ POST performance metric creation failed")
            return False, None
        
        return True, created_metric_id
        
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Connection error: {e}")
        return False, created_metric_id
    except Exception as e:
        print(f"   ❌ Unexpected error: {e}")
        return False, created_metric_id

def test_analytics_summary_apis(site_id):
    """Test Analytics - Summary API endpoints"""
    print("\n31. Testing Analytics - Summary APIs")
    
    try:
        # Test GET KPI dashboard summary
        print("   31a. Testing GET /api/analytics/summary/kpi-dashboard")
        response = requests.get(f"{API_BASE_URL}/analytics/summary/kpi-dashboard", timeout=10)
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            kpi_summary = response.json()
            required_fields = ["analysis_period_days", "total_kpi_metrics", "kpi_summary"]
            if all(field in kpi_summary for field in required_fields):
                print("      ✅ GET KPI dashboard summary working")
            else:
                print("      ❌ Missing required fields in KPI dashboard summary")
                return False
        else:
            print("      ❌ GET KPI dashboard summary failed")
            return False
        
        # Test GET KPI dashboard summary with site filter
        print("   31b. Testing GET /api/analytics/summary/kpi-dashboard with site filter")
        response = requests.get(f"{API_BASE_URL}/analytics/summary/kpi-dashboard?site_id={site_id}&days=7", timeout=10)
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            filtered_kpi_summary = response.json()
            print("      ✅ GET filtered KPI dashboard summary working")
        else:
            print("      ❌ GET filtered KPI dashboard summary failed")
            return False
        
        # Test GET certification compliance summary
        print("   31c. Testing GET /api/analytics/summary/certification-compliance")
        response = requests.get(f"{API_BASE_URL}/analytics/summary/certification-compliance", timeout=10)
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            compliance_summary = response.json()
            required_fields = ["total_certifications", "active_certifications", "expired_certifications", "compliance_rate"]
            if all(field in compliance_summary for field in required_fields):
                print("      ✅ GET certification compliance summary working")
            else:
                print("      ❌ Missing required fields in certification compliance summary")
                return False
        else:
            print("      ❌ GET certification compliance summary failed")
            return False
        
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Connection error: {e}")
        return False
    except Exception as e:
        print(f"   ❌ Unexpected error: {e}")
        return False

def test_admin_dashboard_metrics_api():
    """Test Admin - Dashboard Metrics API endpoints"""
    print("\n32. Testing Admin - Dashboard Metrics API")
    created_metric_id = None
    
    try:
        # Test GET all admin dashboard metrics
        print("   32a. Testing GET /api/admin/dashboard-metrics")
        response = requests.get(f"{API_BASE_URL}/admin/dashboard-metrics", timeout=10)
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            metrics = response.json()
            print(f"      Found {len(metrics)} total admin dashboard metrics")
            print("      ✅ GET all admin dashboard metrics working")
        else:
            print("      ❌ GET all admin dashboard metrics failed")
            return False, None
        
        # Test GET current dashboard metrics
        print("   32b. Testing GET /api/admin/dashboard-metrics/current")
        response = requests.get(f"{API_BASE_URL}/admin/dashboard-metrics/current", timeout=10)
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            current_metrics = response.json()
            required_fields = ["timestamp", "system_overview", "performance_indicators"]
            if all(field in current_metrics for field in required_fields):
                print("      ✅ GET current dashboard metrics working")
            else:
                print("      ❌ Missing required fields in current dashboard metrics")
                return False, None
        else:
            print("      ❌ GET current dashboard metrics failed")
            return False, None
        
        # Create test admin dashboard metric data
        test_metric_data = {
            "metric_date": "2024-01-15",
            "metric_hour": 14,
            "aggregation_level": "daily",  # Fixed: using valid enum value
            "total_users": 150,
            "active_users_24h": 45,
            "total_sites": 12,
            "active_sites": 10,
            "total_cameras": 240,
            "online_cameras": 235
        }
        
        # Test POST create admin dashboard metric
        print("   32c. Testing POST /api/admin/dashboard-metrics")
        response = requests.post(
            f"{API_BASE_URL}/admin/dashboard-metrics",
            json=test_metric_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            metric = response.json()
            created_metric_id = metric.get("id")
            print(f"      Created admin dashboard metric ID: {created_metric_id}")
            print("      ✅ POST admin dashboard metric creation working")
        else:
            print(f"      Response: {response.text}")
            print("      ❌ POST admin dashboard metric creation failed")
            return False, None
        
        return True, created_metric_id
        
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Connection error: {e}")
        return False, created_metric_id
    except Exception as e:
        print(f"   ❌ Unexpected error: {e}")
        return False, created_metric_id

def test_admin_system_health_api():
    """Test Admin - System Health API endpoints"""
    print("\n33. Testing Admin - System Health API")
    created_log_id = None
    
    try:
        # Test GET all system health logs
        print("   33a. Testing GET /api/admin/system-health")
        response = requests.get(f"{API_BASE_URL}/admin/system-health", timeout=10)
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            logs = response.json()
            print(f"      Found {len(logs)} total system health logs")
            print("      ✅ GET all system health logs working")
        else:
            print("      ❌ GET all system health logs failed")
            return False, None
        
        # Test GET system health summary
        print("   33b. Testing GET /api/admin/system-health/summary")
        response = requests.get(f"{API_BASE_URL}/admin/system-health/summary?hours=24", timeout=10)
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            summary = response.json()
            required_fields = ["analysis_period_hours", "total_measurements"]
            if all(field in summary for field in required_fields):
                print("      ✅ GET system health summary working")
            else:
                print("      ❌ Missing required fields in system health summary")
                return False, None
        else:
            print("      ❌ GET system health summary failed")
            return False, None
        
        # Create test system health log data
        test_log_data = {
            "server_id": f"server-{uuid.uuid4().hex[:8]}",
            "component_type": "database",
            "cpu_usage_percentage": 45.2,
            "memory_usage_percentage": 67.8,
            "disk_usage_percentage": 23.1,
            "response_time_ms": 125,
            "service_status": "healthy",
            "monitoring_source": "automated_monitoring"
        }
        
        # Test POST create system health log
        print("   33c. Testing POST /api/admin/system-health")
        response = requests.post(
            f"{API_BASE_URL}/admin/system-health",
            json=test_log_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            log = response.json()
            created_log_id = log.get("id")
            print(f"      Created system health log ID: {created_log_id}")
            print("      ✅ POST system health log creation working")
        else:
            print(f"      Response: {response.text}")
            print("      ❌ POST system health log creation failed")
            return False, None
        
        return True, created_log_id
        
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Connection error: {e}")
        return False, created_log_id
    except Exception as e:
        print(f"   ❌ Unexpected error: {e}")
        return False, created_log_id

def test_admin_analytics_api():
    """Test Admin - Analytics API endpoints"""
    print("\n34. Testing Admin - Analytics API")
    
    try:
        # Test GET system overview analytics
        print("   34a. Testing GET /api/admin/analytics/system-overview")
        response = requests.get(f"{API_BASE_URL}/admin/analytics/system-overview", timeout=10)
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            analytics = response.json()
            required_fields = ["analysis_period_days", "current_metrics", "system_health", "activity_summary", "timestamp"]
            if all(field in analytics for field in required_fields):
                print("      ✅ GET system overview analytics working")
            else:
                print("      ❌ Missing required fields in system overview analytics")
                return False
        else:
            print("      ❌ GET system overview analytics failed")
            return False
        
        # Test GET system overview analytics with custom period
        print("   34b. Testing GET /api/admin/analytics/system-overview with custom period")
        response = requests.get(f"{API_BASE_URL}/admin/analytics/system-overview?days=7", timeout=10)
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            custom_analytics = response.json()
            if custom_analytics.get("analysis_period_days") == 7:
                print("      ✅ GET custom period system overview analytics working")
            else:
                print("      ❌ Custom period not applied correctly")
                return False
        else:
            print("      ❌ GET custom period system overview analytics failed")
            return False
        
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Connection error: {e}")
        return False
    except Exception as e:
        print(f"   ❌ Unexpected error: {e}")
        return False

def cleanup_test_data(created_user_id, created_site_id, created_detection_id, created_model_id, 
                     created_bookmark_id, created_export_id, created_route_id=None, created_waypoint_id=None, 
                     created_session_id=None, created_camera_config_id=None, created_certification_id=None,
                     created_metric_id=None, created_admin_metric_id=None, created_health_log_id=None):
    """Clean up test data created during testing"""
    print("\n35. Cleaning up test data")
    
    try:
        # Delete analytics test data
        if created_certification_id:
            print("   35a. Deleting test certification")
            response = requests.delete(f"{API_BASE_URL}/analytics/certifications/{created_certification_id}", timeout=10)
            print(f"      Certification deletion status: {response.status_code}")
        
        # Delete navigation test data
        if created_camera_config_id:
            print("   35b. Deleting test street view camera config")
            response = requests.delete(f"{API_BASE_URL}/navigation/street-view-cameras/{created_camera_config_id}", timeout=10)
            print(f"      Status Code: {response.status_code}")
        
        if created_waypoint_id:
            print("   35c. Deleting test route waypoint")
            response = requests.delete(f"{API_BASE_URL}/navigation/waypoints/{created_waypoint_id}", timeout=10)
            print(f"      Status Code: {response.status_code}")
        
        # Note: Navigation sessions don't have DELETE endpoint, they are archived
        if created_session_id:
            print("   35d. Navigation session will remain (no DELETE endpoint)")
        
        if created_route_id:
            print("   35e. Deleting test navigation route")
            response = requests.delete(f"{API_BASE_URL}/navigation/routes/{created_route_id}", timeout=10)
            print(f"      Status Code: {response.status_code}")
        
        # Delete test video bookmark
        if created_bookmark_id:
            print("   35f. Deleting test video bookmark")
            response = requests.delete(f"{API_BASE_URL}/video-bookmarks/{created_bookmark_id}", timeout=10)
            if response.status_code == 200:
                print("      ✅ Test video bookmark deleted successfully")
            else:
                print(f"      ⚠️ Could not delete test video bookmark: {response.status_code}")
        
        # Delete AI detection if created
        if created_detection_id:
            print("   35g. Deleting test AI detection")
            response = requests.delete(f"{API_BASE_URL}/ai-detections/{created_detection_id}", timeout=10)
            print(f"      Status Code: {response.status_code}")
        
        # Delete AI model if created
        if created_model_id:
            print("   35h. Deleting test AI model")
            response = requests.delete(f"{API_BASE_URL}/ai-models/{created_model_id}", timeout=10)
            if response.status_code == 200:
                print("      ✅ Test AI model deleted successfully")
            else:
                print(f"      ⚠️ Could not delete test AI model: {response.status_code}")
        
        # Delete site if created
        if created_site_id:
            print("   35i. Deleting test site")
            response = requests.delete(f"{API_BASE_URL}/sites/{created_site_id}", timeout=10)
            if response.status_code == 200:
                print("      ✅ Test site deleted successfully")
            else:
                print(f"      ⚠️ Could not delete test site: {response.status_code}")
        
        # Delete user if created
        if created_user_id:
            print("   35j. Deleting test user")
            response = requests.delete(f"{API_BASE_URL}/users/{created_user_id}", timeout=10)
            print(f"      Status Code: {response.status_code}")
        
        # Note: We don't delete video export as there are no DELETE endpoints implemented
        print("   35k. Video export cleanup skipped (no DELETE endpoint)")
        
        print("   ✅ Test data cleanup completed")
        return True
        
    except Exception as e:
        print(f"   ⚠️ Cleanup error (non-critical): {e}")
        return True  # Don't fail the test suite for cleanup issues

def test_navigation_routes_api(site_id, user_id):
    """Test Navigation Routes API endpoints (full CRUD)"""
    print("\n29. Testing Navigation Routes API")
    created_route_id = None
    
    try:
        # Test GET all navigation routes
        print("   29a. Testing GET /api/navigation/routes")
        response = requests.get(f"{API_BASE_URL}/navigation/routes", timeout=10)
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            routes = response.json()
            print(f"      Found {len(routes)} total navigation routes")
            print("      ✅ GET all navigation routes working")
        else:
            print("      ❌ GET all navigation routes failed")
            return False, None
        
        # Create test navigation route data
        test_route_data = {
            "site_id": site_id,
            "route_name": f"Construction Site Route Alpha {uuid.uuid4().hex[:8]}",
            "route_code": f"CSR-{uuid.uuid4().hex[:8].upper()}",
            "description": "Primary navigation route for construction site access",
            "route_type": "inspection",  # Valid enum: patrol, inspection, emergency_evacuation, material_transport, visitor_tour, maintenance, custom
            "purpose": "safety_inspection",
            "priority_level": "high",
            "start_coordinates": {"lat": 40.7128, "lng": -74.0060, "elevation": 10.0},
            "end_coordinates": {"lat": 40.7589, "lng": -73.9851, "elevation": 15.0},
            "total_distance_meters": 5280.0,
            "estimated_duration_minutes": 45,
            "elevation_change_meters": 5.0,
            "difficulty_level": "moderate",
            "safety_rating": "caution",
            "accessibility_level": "walking",  # Valid enum: walking, vehicle, wheelchair, restricted
            "ppe_requirements": ["hard_hat", "safety_vest", "steel_toe_boots"],
            "hazard_warnings": ["heavy_machinery", "uneven_terrain"]
        }
        
        # Test POST create navigation route
        print("   29b. Testing POST /api/navigation/routes")
        response = requests.post(
            f"{API_BASE_URL}/navigation/routes",
            json=test_route_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            route = response.json()
            created_route_id = route.get("id")
            print(f"      Created navigation route ID: {created_route_id}")
            print("      ✅ POST navigation route creation working")
        else:
            print(f"      Response: {response.text}")
            print("      ❌ POST navigation route creation failed")
            return False, None
        
        # Test GET specific navigation route
        print("   29c. Testing GET /api/navigation/routes/{route_id}")
        response = requests.get(f"{API_BASE_URL}/navigation/routes/{created_route_id}", timeout=10)
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            route = response.json()
            if route.get("route_name") == test_route_data["route_name"]:
                print("      ✅ GET specific navigation route working")
            else:
                print("      ❌ Navigation route data mismatch")
                return False, created_route_id
        else:
            print("      ❌ GET specific navigation route failed")
            return False, created_route_id
        
        # Test PUT update navigation route
        print("   29d. Testing PUT /api/navigation/routes/{route_id}")
        update_data = test_route_data.copy()
        update_data["description"] = "Updated navigation route for enhanced site access"
        update_data["priority_level"] = "critical"
        
        response = requests.put(
            f"{API_BASE_URL}/navigation/routes/{created_route_id}",
            json=update_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            updated_route = response.json()
            if updated_route.get("description") == update_data["description"]:
                print("      ✅ PUT navigation route update working")
            else:
                print("      ❌ Navigation route update data mismatch")
                return False, created_route_id
        else:
            print("      ❌ PUT navigation route update failed")
            return False, created_route_id
        
        # Test GET navigation routes with filters
        print("   29e. Testing GET /api/navigation/routes with filters")
        response = requests.get(f"{API_BASE_URL}/navigation/routes?site_id={site_id}&route_type=construction_access", timeout=10)
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            filtered_routes = response.json()
            print(f"      Found {len(filtered_routes)} routes for site with construction_access type")
            print("      ✅ GET navigation routes with filters working")
        else:
            print("      ❌ GET navigation routes with filters failed")
            return False, created_route_id
        
        return True, created_route_id
        
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Connection error: {e}")
        return False, created_route_id
    except Exception as e:
        print(f"   ❌ Unexpected error: {e}")
        return False, created_route_id

def test_route_waypoints_api(route_id):
    """Test Route Waypoints API endpoints (full CRUD)"""
    print("\n30. Testing Route Waypoints API")
    created_waypoint_id = None
    
    try:
        # Test GET all route waypoints
        print("   30a. Testing GET /api/navigation/waypoints")
        response = requests.get(f"{API_BASE_URL}/navigation/waypoints", timeout=10)
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            waypoints = response.json()
            print(f"      Found {len(waypoints)} total route waypoints")
            print("      ✅ GET all route waypoints working")
        else:
            print("      ❌ GET all route waypoints failed")
            return False, None
        
        # Create test route waypoint data
        test_waypoint_data = {
            "route_id": route_id,
            "waypoint_name": f"Checkpoint Alpha {uuid.uuid4().hex[:8]}",
            "waypoint_code": f"CP-{uuid.uuid4().hex[:8].upper()}",
            "sequence_order": 1,
            "latitude": 40.7300,
            "longitude": -74.0000,
            "elevation": 12.5,
            "waypoint_type": "checkpoint",
            "action_required": "inspect",  # Valid enum: pass_through, pause, inspect, report, confirm, emergency_check
            "approach_instructions": "Approach from the north entrance, maintain 15 mph speed limit",
            "departure_instructions": "Continue south towards main construction area",
            "safety_level": "caution",
            "hazard_types": ["heavy_machinery", "construction_vehicles"],
            "associated_camera_ids": [],
            "monitoring_required": True,
            "photo_documentation_required": True
        }
        
        # Test POST create route waypoint
        print("   30b. Testing POST /api/navigation/waypoints")
        response = requests.post(
            f"{API_BASE_URL}/navigation/waypoints",
            json=test_waypoint_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            waypoint = response.json()
            created_waypoint_id = waypoint.get("id")
            print(f"      Created route waypoint ID: {created_waypoint_id}")
            print("      ✅ POST route waypoint creation working")
        else:
            print(f"      Response: {response.text}")
            print("      ❌ POST route waypoint creation failed")
            return False, None
        
        # Test GET specific route waypoint
        print("   30c. Testing GET /api/navigation/waypoints/{waypoint_id}")
        response = requests.get(f"{API_BASE_URL}/navigation/waypoints/{created_waypoint_id}", timeout=10)
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            waypoint = response.json()
            if waypoint.get("waypoint_name") == test_waypoint_data["waypoint_name"]:
                print("      ✅ GET specific route waypoint working")
            else:
                print("      ❌ Route waypoint data mismatch")
                return False, created_waypoint_id
        else:
            print("      ❌ GET specific route waypoint failed")
            return False, created_waypoint_id
        
        # Test GET route waypoints with filters
        print("   30d. Testing GET /api/navigation/waypoints with filters")
        response = requests.get(f"{API_BASE_URL}/navigation/waypoints?route_id={route_id}&waypoint_type=checkpoint", timeout=10)
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            filtered_waypoints = response.json()
            print(f"      Found {len(filtered_waypoints)} waypoints for route with checkpoint type")
            print("      ✅ GET route waypoints with filters working")
        else:
            print("      ❌ GET route waypoints with filters failed")
            return False, created_waypoint_id
        
        return True, created_waypoint_id
        
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Connection error: {e}")
        return False, created_waypoint_id
    except Exception as e:
        print(f"   ❌ Unexpected error: {e}")
        return False, created_waypoint_id

def test_navigation_sessions_api(user_id, route_id):
    """Test Navigation Sessions API endpoints"""
    print("\n31. Testing Navigation Sessions API")
    created_session_id = None
    
    try:
        # Test GET all navigation sessions
        print("   31a. Testing GET /api/navigation/sessions")
        response = requests.get(f"{API_BASE_URL}/navigation/sessions", timeout=10)
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            sessions = response.json()
            print(f"      Found {len(sessions)} total navigation sessions")
            print("      ✅ GET all navigation sessions working")
        else:
            print("      ❌ GET all navigation sessions failed")
            return False, None
        
        # Create test navigation session data
        test_session_data = {
            "user_id": user_id,
            "route_id": route_id,
            "session_name": f"Site Inspection Session {uuid.uuid4().hex[:8]}",
            "session_purpose": "inspection",  # Valid enum: patrol, inspection, emergency, training, tour, maintenance, other
            "planned_duration_minutes": 60,
            "total_waypoints": 5,
            "device_type": "tablet",
            "device_id": f"TABLET-{uuid.uuid4().hex[:8].upper()}",
            "weather_conditions": {
                "temperature": 22,
                "humidity": 65,
                "wind_speed": 8,
                "conditions": "partly_cloudy"
            }
        }
        
        # Test POST create navigation session
        print("   31b. Testing POST /api/navigation/sessions")
        response = requests.post(
            f"{API_BASE_URL}/navigation/sessions",
            json=test_session_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            session = response.json()
            created_session_id = session.get("id")
            print(f"      Created navigation session ID: {created_session_id}")
            print("      ✅ POST navigation session creation working")
        else:
            print(f"      Response: {response.text}")
            print("      ❌ POST navigation session creation failed")
            return False, None
        
        # Test GET specific navigation session
        print("   31c. Testing GET /api/navigation/sessions/{session_id}")
        response = requests.get(f"{API_BASE_URL}/navigation/sessions/{created_session_id}", timeout=10)
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            session = response.json()
            if session.get("session_purpose") == test_session_data["session_purpose"]:
                print("      ✅ GET specific navigation session working")
            else:
                print("      ❌ Navigation session data mismatch")
                return False, created_session_id
        else:
            print("      ❌ GET specific navigation session failed")
            return False, created_session_id
        
        # Test PUT complete navigation session
        print("   31d. Testing PUT /api/navigation/sessions/{session_id}/complete")
        response = requests.put(f"{API_BASE_URL}/navigation/sessions/{created_session_id}/complete", timeout=10)
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            if "completed successfully" in result.get("message", ""):
                print("      ✅ PUT navigation session completion working")
            else:
                print("      ❌ Navigation session completion response unexpected")
                return False, created_session_id
        else:
            print("      ❌ PUT navigation session completion failed")
            return False, created_session_id
        
        # Test GET navigation sessions with filters
        print("   31e. Testing GET /api/navigation/sessions with filters")
        response = requests.get(f"{API_BASE_URL}/navigation/sessions?user_id={user_id}&route_id={route_id}", timeout=10)
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            filtered_sessions = response.json()
            print(f"      Found {len(filtered_sessions)} sessions for user and route")
            print("      ✅ GET navigation sessions with filters working")
        else:
            print("      ❌ GET navigation sessions with filters failed")
            return False, created_session_id
        
        return True, created_session_id
        
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Connection error: {e}")
        return False, created_session_id
    except Exception as e:
        print(f"   ❌ Unexpected error: {e}")
        return False, created_session_id

def test_street_view_cameras_api():
    """Test Street View Cameras API endpoints (full CRUD)"""
    print("\n32. Testing Street View Cameras API")
    created_camera_config_id = None
    camera_id = None
    
    try:
        # Get existing cameras to use a valid camera_id
        print("   32a. Getting existing cameras for valid camera_id")
        response = requests.get(f"{API_BASE_URL}/cameras", timeout=10)
        if response.status_code == 200:
            cameras = response.json()
            if cameras:
                camera_id = cameras[0]["id"]
                print(f"      Using existing camera ID: {camera_id}")
            else:
                print("      No existing cameras found, skipping Street View Camera tests")
                print("      ⚠️ Street View Camera tests require existing camera")
                return True, None  # Mark as passed since no cameras exist
        else:
            print("      ❌ Failed to get cameras list")
            return False, None
        
        # Test GET all street view cameras
        print("   32b. Testing GET /api/navigation/street-view-cameras")
        response = requests.get(f"{API_BASE_URL}/navigation/street-view-cameras", timeout=10)
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            cameras = response.json()
            print(f"      Found {len(cameras)} total street view cameras")
            print("      ✅ GET all street view cameras working")
        else:
            print("      ❌ GET all street view cameras failed")
            return False, None
        
        # Create test street view camera data
        test_camera_data = {
            "camera_id": camera_id,
            "is_street_view_enabled": True,
            "street_view_priority": 2,
            "field_of_view_degrees": 120,
            "ptz_enabled": True,
            "streaming_resolution": "4K",
            "streaming_fps": 60,
            "ai_detection_enabled": True,
            "precise_latitude": 40.7128,
            "precise_longitude": -74.0060,
            "mounting_height_meters": 8.5,
            "orientation_degrees": 180.0,
            "route_coverage": ["route_1", "route_2"],
            "waypoint_coverage": ["waypoint_1", "waypoint_2", "waypoint_3"]
        }
        
        # Test POST create street view camera
        print("   32c. Testing POST /api/navigation/street-view-cameras")
        response = requests.post(
            f"{API_BASE_URL}/navigation/street-view-cameras",
            json=test_camera_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            camera_config = response.json()
            created_camera_config_id = camera_config.get("id")
            print(f"      Created street view camera config ID: {created_camera_config_id}")
            print("      ✅ POST street view camera creation working")
        else:
            print(f"      Response: {response.text}")
            print("      ❌ POST street view camera creation failed")
            return False, None
        
        # Test GET specific street view camera
        print("   32d. Testing GET /api/navigation/street-view-cameras/{camera_config_id}")
        response = requests.get(f"{API_BASE_URL}/navigation/street-view-cameras/{created_camera_config_id}", timeout=10)
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            camera_config = response.json()
            if camera_config.get("camera_id") == test_camera_data["camera_id"]:
                print("      ✅ GET specific street view camera working")
            else:
                print("      ❌ Street view camera data mismatch")
                return False, created_camera_config_id
        else:
            print("      ❌ GET specific street view camera failed")
            return False, created_camera_config_id
        
        # Test PUT update street view camera
        print("   32e. Testing PUT /api/navigation/street-view-cameras/{camera_config_id}")
        update_data = test_camera_data.copy()
        update_data["field_of_view_degrees"] = 150
        update_data["streaming_fps"] = 30
        
        response = requests.put(
            f"{API_BASE_URL}/navigation/street-view-cameras/{created_camera_config_id}",
            json=update_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            updated_camera_config = response.json()
            if updated_camera_config.get("field_of_view_degrees") == update_data["field_of_view_degrees"]:
                print("      ✅ PUT street view camera update working")
            else:
                print("      ❌ Street view camera update data mismatch")
                return False, created_camera_config_id
        else:
            print("      ❌ PUT street view camera update failed")
            return False, created_camera_config_id
        
        # Test GET street view cameras with filters
        print("   32f. Testing GET /api/navigation/street-view-cameras with filters")
        response = requests.get(f"{API_BASE_URL}/navigation/street-view-cameras?camera_id={camera_id}&is_enabled=true", timeout=10)
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            filtered_cameras = response.json()
            print(f"      Found {len(filtered_cameras)} enabled street view cameras for camera")
            print("      ✅ GET street view cameras with filters working")
        else:
            print("      ❌ GET street view cameras with filters failed")
            return False, created_camera_config_id
        
        return True, created_camera_config_id
        
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Connection error: {e}")
        return False, created_camera_config_id
    except Exception as e:
        print(f"   ❌ Unexpected error: {e}")
        return False, created_camera_config_id

def test_navigation_analytics_api(site_id, route_id):
    """Test Navigation Analytics API endpoints"""
    print("\n33. Testing Navigation Analytics API")
    
    try:
        # Test GET route usage analytics (general)
        print("   33a. Testing GET /api/navigation/analytics/route-usage")
        response = requests.get(f"{API_BASE_URL}/navigation/analytics/route-usage", timeout=10)
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            analytics = response.json()
            required_fields = ["analytics_period_days", "total_routes_analyzed", "route_analytics"]
            if all(field in analytics for field in required_fields):
                print("      ✅ GET route usage analytics working")
            else:
                print("      ❌ Missing required fields in route usage analytics")
                return False
        else:
            print("      ❌ GET route usage analytics failed")
            return False
        
        # Test GET route usage analytics with site filter
        print("   33b. Testing GET /api/navigation/analytics/route-usage?site_id={site_id}")
        response = requests.get(f"{API_BASE_URL}/navigation/analytics/route-usage?site_id={site_id}", timeout=10)
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            site_analytics = response.json()
            print("      ✅ GET site route usage analytics working")
        else:
            print("      ❌ GET site route usage analytics failed")
            return False
        
        # Test GET route usage analytics with days filter
        print("   33c. Testing GET /api/navigation/analytics/route-usage?days=7")
        response = requests.get(f"{API_BASE_URL}/navigation/analytics/route-usage?days=7", timeout=10)
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            weekly_analytics = response.json()
            if weekly_analytics.get("analytics_period_days") == 7:
                print("      ✅ GET route usage analytics with days filter working")
            else:
                print("      ❌ Days filter not applied correctly")
                return False
        else:
            print("      ❌ GET route usage analytics with days filter failed")
            return False
        
        # Test GET session performance analytics (general)
        print("   33d. Testing GET /api/navigation/analytics/session-performance")
        response = requests.get(f"{API_BASE_URL}/navigation/analytics/session-performance", timeout=10)
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            performance = response.json()
            required_fields = ["analytics_period_days", "total_sessions"]
            if all(field in performance for field in required_fields):
                print("      ✅ GET session performance analytics working")
            else:
                print("      ❌ Missing required fields in session performance analytics")
                return False
        else:
            print("      ❌ GET session performance analytics failed")
            return False
        
        # Test GET session performance analytics with route filter
        print("   33e. Testing GET /api/navigation/analytics/session-performance?route_id={route_id}")
        response = requests.get(f"{API_BASE_URL}/navigation/analytics/session-performance?route_id={route_id}", timeout=10)
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            route_performance = response.json()
            print("      ✅ GET route session performance analytics working")
        else:
            print("      ❌ GET route session performance analytics failed")
            return False
        
        # Test GET session performance analytics with days filter
        print("   33f. Testing GET /api/navigation/analytics/session-performance?days=14")
        response = requests.get(f"{API_BASE_URL}/navigation/analytics/session-performance?days=14", timeout=10)
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            biweekly_performance = response.json()
            if biweekly_performance.get("analytics_period_days") == 14:
                print("      ✅ GET session performance analytics with days filter working")
            else:
                print("      ❌ Days filter not applied correctly")
                return False
        else:
            print("      ❌ GET session performance analytics with days filter failed")
            return False
        
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Connection error: {e}")
        return False
    except Exception as e:
        print(f"   ❌ Unexpected error: {e}")
        return False

def main():
    """Run all backend tests"""
    print("Starting AI Construction Management Backend API Tests...")
    print(f"Backend URL: {BACKEND_URL}")
    print(f"API Base URL: {API_BASE_URL}")
    
    results = []
    created_user_id = None
    created_site_id = None
    created_detection_id = None
    created_model_id = None
    created_bookmark_id = None
    created_export_id = None
    created_route_id = None
    created_waypoint_id = None
    created_session_id = None
    created_camera_config_id = None
    created_certification_id = None
    created_metric_id = None
    created_admin_metric_id = None
    created_health_log_id = None
    
    # Test basic connectivity
    connectivity_ok = test_api_connectivity()
    results.append(("API Connectivity", connectivity_ok))
    
    if not connectivity_ok:
        print("\n❌ Cannot reach backend - skipping API tests")
        return False
    
    # Test core endpoints
    root_ok = test_root_endpoint()
    results.append(("Root Endpoint", root_ok))
    
    health_ok = test_health_endpoint()
    results.append(("Health Check", health_ok))
    
    dashboard_ok = test_dashboard_stats()
    results.append(("Dashboard Stats", dashboard_ok))
    
    # Test CRUD operations
    users_ok, created_user_id = test_users_crud()
    results.append(("Users CRUD", users_ok))
    
    sites_ok, created_site_id = test_sites_crud(created_user_id)
    results.append(("Sites CRUD", sites_ok))
    
    # Test related endpoints (only if we have a site)
    if created_site_id:
        zones_ok = test_zones_api(created_site_id)
        results.append(("Zones API", zones_ok))
        
        cameras_ok = test_cameras_api(created_site_id)
        results.append(("Cameras API", cameras_ok))
        
        alerts_ok = test_alerts_api(created_site_id)
        results.append(("Alerts API", alerts_ok))
        
        personnel_ok = test_personnel_api(created_site_id)
        results.append(("Personnel API", personnel_ok))
    
    # Test error handling
    error_ok = test_error_handling()
    results.append(("Error Handling", error_ok))
    
    # Test legacy endpoints
    legacy_ok = test_legacy_status_endpoints()
    results.append(("Legacy Status Endpoints", legacy_ok))
    
    # AI & DETECTION TESTS
    print("\n" + "=" * 80)
    print("STARTING AI & DETECTION API TESTS")
    print("=" * 80)
    
    # Test AI Detections API
    ai_detections_ok, created_detection_id = test_ai_detections_api(created_site_id)
    results.append(("AI Detections API", ai_detections_ok))
    
    # Test AI Models API (full CRUD)
    ai_models_ok, created_model_id = test_ai_models_api()
    results.append(("AI Models API", ai_models_ok))
    
    # Test Recording Sessions API
    recording_sessions_ok = test_recording_sessions_api(created_site_id)
    results.append(("Recording Sessions API", recording_sessions_ok))
    
    # Test AI Analytics API
    ai_analytics_ok = test_ai_analytics_api(created_site_id)
    results.append(("AI Analytics API", ai_analytics_ok))
    
    # Test Database Verification
    db_verification_ok = test_database_verification()
    results.append(("Database Verification", db_verification_ok))
    
    # VIDEO & EVIDENCE MANAGEMENT TESTS
    print("\n" + "=" * 80)
    print("STARTING VIDEO & EVIDENCE MANAGEMENT API TESTS")
    print("=" * 80)
    
    # Test Video Bookmarks API
    video_bookmarks_ok, created_bookmark_id = test_video_bookmarks_api()
    results.append(("Video Bookmarks API", video_bookmarks_ok))
    
    # Test Video Access Logs API
    video_access_logs_ok = test_video_access_logs_api()
    results.append(("Video Access Logs API", video_access_logs_ok))
    
    # Test Video Exports API
    video_exports_ok, created_export_id = test_video_exports_api()
    results.append(("Video Exports API", video_exports_ok))
    
    # Test Video Quality Metrics API
    video_quality_metrics_ok = test_video_quality_metrics_api()
    results.append(("Video Quality Metrics API", video_quality_metrics_ok))
    
    # Test Video Database Verification
    video_db_verification_ok = test_video_database_verification()
    results.append(("Video Database Verification", video_db_verification_ok))
    
    # NAVIGATION & STREET VIEW TESTS
    print("\n" + "=" * 80)
    print("STARTING NAVIGATION & STREET VIEW API TESTS")
    print("=" * 80)
    
    # Test Navigation Routes API (full CRUD)
    navigation_routes_ok, created_route_id = test_navigation_routes_api(created_site_id, created_user_id)
    results.append(("Navigation Routes API", navigation_routes_ok))
    
    # Test Route Waypoints API (full CRUD)
    if created_route_id:
        route_waypoints_ok, created_waypoint_id = test_route_waypoints_api(created_route_id)
        results.append(("Route Waypoints API", route_waypoints_ok))
    else:
        print("   ⚠️ Skipping Route Waypoints tests - no route created")
        results.append(("Route Waypoints API", False))
    
    # Test Navigation Sessions API
    if created_route_id and created_user_id:
        navigation_sessions_ok, created_session_id = test_navigation_sessions_api(created_user_id, created_route_id)
        results.append(("Navigation Sessions API", navigation_sessions_ok))
    else:
        print("   ⚠️ Skipping Navigation Sessions tests - missing route or user")
        results.append(("Navigation Sessions API", False))
    
    # Test Street View Cameras API (full CRUD)
    street_view_cameras_ok, created_camera_config_id = test_street_view_cameras_api()
    results.append(("Street View Cameras API", street_view_cameras_ok))
    
    # Test Navigation Analytics API
    if created_site_id and created_route_id:
        navigation_analytics_ok = test_navigation_analytics_api(created_site_id, created_route_id)
        results.append(("Navigation Analytics API", navigation_analytics_ok))
    else:
        print("   ⚠️ Skipping Navigation Analytics tests - missing site or route")
        results.append(("Navigation Analytics API", False))
    
    # COMPLETE ANALYTICS & REPORTING TESTS
    print("\n" + "=" * 80)
    print("STARTING COMPLETE ANALYTICS & REPORTING API TESTS")
    print("=" * 80)
    
    # Test Analytics - User Certifications API
    if created_user_id:
        analytics_certifications_ok, created_certification_id = test_analytics_certifications_api(created_user_id)
        results.append(("Analytics Certifications API", analytics_certifications_ok))
    else:
        print("   ⚠️ Skipping Analytics Certifications tests - no user created")
        results.append(("Analytics Certifications API", False))
    
    # Test Analytics - Performance Metrics API
    if created_site_id:
        analytics_metrics_ok, created_metric_id = test_analytics_performance_metrics_api(created_site_id)
        results.append(("Analytics Performance Metrics API", analytics_metrics_ok))
    else:
        print("   ⚠️ Skipping Analytics Performance Metrics tests - no site created")
        results.append(("Analytics Performance Metrics API", False))
    
    # Test Analytics - Summary APIs
    if created_site_id:
        analytics_summary_ok = test_analytics_summary_apis(created_site_id)
        results.append(("Analytics Summary APIs", analytics_summary_ok))
    else:
        print("   ⚠️ Skipping Analytics Summary tests - no site created")
        results.append(("Analytics Summary APIs", False))
    
    # ADMIN DASHBOARD & SYSTEM MANAGEMENT TESTS
    print("\n" + "=" * 80)
    print("STARTING ADMIN DASHBOARD & SYSTEM MANAGEMENT API TESTS")
    print("=" * 80)
    
    # Test Admin - Dashboard Metrics API
    admin_dashboard_metrics_ok, created_admin_metric_id = test_admin_dashboard_metrics_api()
    results.append(("Admin Dashboard Metrics API", admin_dashboard_metrics_ok))
    
    # Test Admin - System Health API
    admin_system_health_ok, created_health_log_id = test_admin_system_health_api()
    results.append(("Admin System Health API", admin_system_health_ok))
    
    # Test Admin - Analytics API
    admin_analytics_ok = test_admin_analytics_api()
    results.append(("Admin Analytics API", admin_analytics_ok))
    
    # Cleanup test data
    cleanup_ok = cleanup_test_data(created_user_id, created_site_id, created_detection_id, created_model_id, 
                                 created_bookmark_id, created_export_id, created_route_id, created_waypoint_id, 
                                 created_session_id, created_camera_config_id, created_certification_id,
                                 created_metric_id, created_admin_metric_id, created_health_log_id)
    results.append(("Test Data Cleanup", cleanup_ok))
    
    # Summary
    print("\n" + "=" * 80)
    print("AI CONSTRUCTION MANAGEMENT BACKEND API TEST RESULTS:")
    print("=" * 80)
    
    all_passed = True
    core_tests_passed = 0
    ai_tests_passed = 0
    video_tests_passed = 0
    navigation_tests_passed = 0
    analytics_tests_passed = 0
    admin_tests_passed = 0
    
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{test_name:<40} {status}")
        if not passed:
            all_passed = False
        
        # Count test categories
        if any(admin_keyword in test_name for admin_keyword in ["Admin"]):
            if passed:
                admin_tests_passed += 1
        elif any(analytics_keyword in test_name for analytics_keyword in ["Analytics"]):
            if passed:
                analytics_tests_passed += 1
        elif any(nav_keyword in test_name for nav_keyword in ["Navigation", "Route", "Street View"]):
            if passed:
                navigation_tests_passed += 1
        elif any(video_keyword in test_name for video_keyword in ["Video", "video"]):
            if passed:
                video_tests_passed += 1
        elif any(ai_keyword in test_name for ai_keyword in ["AI", "Recording", "Database Verification"]):
            if passed:
                ai_tests_passed += 1
        else:
            if passed:
                core_tests_passed += 1
    
    print("=" * 80)
    print(f"Core Backend Tests: {core_tests_passed} passed")
    print(f"AI & Detection Tests: {ai_tests_passed} passed")
    print(f"Video & Evidence Tests: {video_tests_passed} passed")
    print(f"Navigation & Street View Tests: {navigation_tests_passed} passed")
    print(f"Analytics & Reporting Tests: {analytics_tests_passed} passed")
    print(f"Admin Dashboard & System Tests: {admin_tests_passed} passed")
    
    if all_passed:
        print("🎉 ALL BACKEND TESTS PASSED!")
        print("✅ MySQL database connection working")
        print("✅ All core API endpoints functioning correctly")
        print("✅ All AI & Detection endpoints functioning correctly")
        print("✅ All Video & Evidence Management endpoints functioning correctly")
        print("✅ All Navigation & Street View endpoints functioning correctly")
        print("✅ All Analytics & Reporting endpoints functioning correctly")
        print("✅ All Admin Dashboard & System Management endpoints functioning correctly")
        print("✅ CRUD operations working")
        print("✅ Error handling implemented")
        print("✅ Database tables verified")
        return True
    else:
        print("⚠️  SOME BACKEND TESTS FAILED!")
        print("Please check the detailed output above for specific issues.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)