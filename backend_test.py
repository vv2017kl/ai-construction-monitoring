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
    "name": "Construction Site Alpha",
    "code": "CSA-001",
    "address": "123 Construction Ave, Builder City, BC 12345",
    "type": "commercial",
    "phase": "construction",
    "manager_id": None  # Will be set after creating a user
}

TEST_USER_DATA = {
    "username": "john_manager",
    "email": "john.manager@construction.com",
    "first_name": "John",
    "last_name": "Manager",
    "password": "SecurePass123!",
    "role": "site_manager",
    "department": "Operations",
    "phone": "+1-555-0123"
}

def test_root_endpoint():
    """Test the root API endpoint"""
    print("\n1. Testing Root Endpoint (GET /api/)")
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
    print("\n2. Testing Health Check Endpoint (GET /api/health)")
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
    print("\n3. Testing Dashboard Stats (GET /api/dashboard/stats)")
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

def test_create_status_check():
    """Test creating a status check"""
    print("\n2. Testing Create Status Check (POST /api/status)")
    try:
        test_data = {
            "client_name": "Construction Site Alpha"
        }
        
        response = requests.post(
            f"{API_BASE_URL}/status", 
            json=test_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        print(f"   Status Code: {response.status_code}")
        print(f"   Response: {response.json()}")
        
        if response.status_code == 200:
            data = response.json()
            if (data.get("client_name") == test_data["client_name"] and 
                "id" in data and "timestamp" in data):
                print("   ✅ Status check creation working correctly")
                return True, data.get("id")
            else:
                print("   ❌ Unexpected response structure")
                return False, None
        else:
            print("   ❌ Status check creation failed")
            return False, None
            
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Connection error: {e}")
        return False, None
    except Exception as e:
        print(f"   ❌ Unexpected error: {e}")
        return False, None

def test_get_status_checks():
    """Test retrieving status checks"""
    print("\n3. Testing Get Status Checks (GET /api/status)")
    try:
        response = requests.get(f"{API_BASE_URL}/status", timeout=10)
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   Found {len(data)} status check(s)")
            
            if isinstance(data, list):
                if len(data) > 0:
                    print(f"   Sample record: {data[0]}")
                print("   ✅ Status checks retrieval working correctly")
                return True
            else:
                print("   ❌ Expected list response")
                return False
        else:
            print("   ❌ Status checks retrieval failed")
            print(f"   Response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Connection error: {e}")
        return False
    except Exception as e:
        print(f"   ❌ Unexpected error: {e}")
        return False

def test_api_connectivity():
    """Test basic API connectivity"""
    print("\n4. Testing API Connectivity")
    try:
        # Test if we can reach the backend at all
        response = requests.get(BACKEND_URL, timeout=5)
        print(f"   Backend base URL accessible: {response.status_code}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Backend connectivity issue: {e}")
        return False

def main():
    """Run all backend tests"""
    print("Starting Backend API Tests...")
    print(f"Backend URL: {BACKEND_URL}")
    print(f"API Base URL: {API_BASE_URL}")
    
    results = []
    
    # Test basic connectivity
    connectivity_ok = test_api_connectivity()
    results.append(("API Connectivity", connectivity_ok))
    
    if not connectivity_ok:
        print("\n❌ Cannot reach backend - skipping API tests")
        return False
    
    # Test root endpoint
    root_ok = test_root_endpoint()
    results.append(("Root Endpoint", root_ok))
    
    # Test status check creation
    create_ok, created_id = test_create_status_check()
    results.append(("Create Status Check", create_ok))
    
    # Test status check retrieval
    get_ok = test_get_status_checks()
    results.append(("Get Status Checks", get_ok))
    
    # Summary
    print("\n" + "=" * 60)
    print("BACKEND API TEST RESULTS:")
    print("=" * 60)
    
    all_passed = True
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{test_name:<25} {status}")
        if not passed:
            all_passed = False
    
    print("=" * 60)
    if all_passed:
        print("🎉 ALL BACKEND TESTS PASSED!")
        return True
    else:
        print("⚠️  SOME BACKEND TESTS FAILED!")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)