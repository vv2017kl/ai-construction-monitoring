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
        
        # Create test AI detection data
        test_detection_data = {
            "camera_id": camera_id or str(uuid.uuid4()),
            "site_id": site_id,
            "zone_id": None,  # Fixed: using None to avoid foreign key constraint
            "detection_type": "person",  # Fixed: using valid enum value
            "person_count": 3,
            "confidence_score": 0.85,
            "detection_results": {"objects": ["person", "helmet", "vest"]},
            "safety_score": 0.92
        }
        
        # Test POST create AI detection
        print("   13c. Testing POST /api/ai-detections")
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
        print("   13d. Testing GET /api/ai-detections/{detection_id}")
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
            print("   13e. Testing GET /api/cameras/{camera_id}/ai-detections")
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

def cleanup_test_data(site_id, user_id, detection_id=None, model_id=None):
    """Clean up test data created during testing"""
    print("\n18. Cleaning up test data")
    
    try:
        # Delete test AI model
        if model_id:
            print("   18a. Deleting test AI model")
            response = requests.delete(f"{API_BASE_URL}/ai-models/{model_id}", timeout=10)
            if response.status_code == 200:
                print("      ✅ Test AI model deleted successfully")
            else:
                print(f"      ⚠️ Could not delete test AI model: {response.status_code}")
        
        # Delete test site
        if site_id:
            print("   18b. Deleting test site")
            response = requests.delete(f"{API_BASE_URL}/sites/{site_id}", timeout=10)
            if response.status_code == 200:
                print("      ✅ Test site deleted successfully")
            else:
                print(f"      ⚠️ Could not delete test site: {response.status_code}")
        
        # Note: We don't delete the user or AI detection as there are no DELETE endpoints implemented
        # This is acceptable for testing purposes
        print("   18c. Test user and AI detection cleanup skipped (no DELETE endpoints)")
        
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"   ⚠️ Cleanup connection error: {e}")
        return False
    except Exception as e:
        print(f"   ⚠️ Cleanup error: {e}")
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
    
    # NEW AI & DETECTION TESTS
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
    
    # Cleanup test data
    cleanup_ok = cleanup_test_data(created_site_id, created_user_id, created_detection_id, created_model_id)
    results.append(("Test Data Cleanup", cleanup_ok))
    
    # Summary
    print("\n" + "=" * 80)
    print("AI CONSTRUCTION MANAGEMENT BACKEND API TEST RESULTS:")
    print("=" * 80)
    
    all_passed = True
    core_tests_passed = 0
    ai_tests_passed = 0
    
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{test_name:<30} {status}")
        if not passed:
            all_passed = False
        
        # Count AI-specific tests
        if any(ai_keyword in test_name for ai_keyword in ["AI", "Recording", "Analytics", "Database Verification"]):
            if passed:
                ai_tests_passed += 1
        else:
            if passed:
                core_tests_passed += 1
    
    print("=" * 80)
    print(f"Core Backend Tests: {core_tests_passed} passed")
    print(f"AI & Detection Tests: {ai_tests_passed} passed")
    
    if all_passed:
        print("🎉 ALL BACKEND TESTS PASSED!")
        print("✅ MySQL database connection working")
        print("✅ All core API endpoints functioning correctly")
        print("✅ All AI & Detection endpoints functioning correctly")
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