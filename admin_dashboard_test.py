#!/usr/bin/env python3
"""
Admin Dashboard API Testing Script
Focused testing for admin dashboard integration and data flow analysis
"""

import requests
import json
import sys
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('/app/frontend/.env')

# Get the backend URL from environment
BACKEND_URL = os.getenv('REACT_APP_BACKEND_URL')
API_BASE_URL = f"{BACKEND_URL}/api"

print(f"🎯 ADMIN DASHBOARD API INTEGRATION TESTING")
print(f"Testing Admin Dashboard APIs at: {API_BASE_URL}")
print("=" * 80)

def test_admin_dashboard_apis():
    """Test Admin Dashboard API endpoints specifically for admin dashboard integration"""
    print("\n🔧 ADMIN DASHBOARD API INTEGRATION TESTING")
    print("=" * 80)
    
    admin_tests_passed = 0
    admin_tests_total = 0
    
    # Test 1: Admin Dashboard Metrics API
    print("\n1. Testing Admin Dashboard Metrics API")
    admin_tests_total += 1
    try:
        # Test GET dashboard metrics
        print("   1a. Testing GET /api/admin/dashboard-metrics")
        response = requests.get(f"{API_BASE_URL}/admin/dashboard-metrics", timeout=10)
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            metrics = response.json()
            print(f"      Found {len(metrics)} dashboard metrics")
            print("      ✅ Admin dashboard metrics API working")
            admin_tests_passed += 1
        else:
            print(f"      ❌ Admin dashboard metrics API failed: {response.text}")
    except Exception as e:
        print(f"      ❌ Admin dashboard metrics API error: {e}")
    
    # Test 2: Current Dashboard Metrics API
    print("\n2. Testing Current Dashboard Metrics API")
    admin_tests_total += 1
    try:
        print("   2a. Testing GET /api/admin/dashboard-metrics/current")
        response = requests.get(f"{API_BASE_URL}/admin/dashboard-metrics/current", timeout=10)
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            current_metrics = response.json()
            print(f"      Current metrics response: {json.dumps(current_metrics, indent=2)}")
            
            # Check for required fields
            required_fields = ["system_overview", "performance_indicators", "alerts_summary"]
            if all(field in current_metrics for field in required_fields):
                print("      ✅ Current dashboard metrics API working with proper structure")
                admin_tests_passed += 1
            else:
                print("      ❌ Current dashboard metrics missing required fields")
        else:
            print(f"      ❌ Current dashboard metrics API failed: {response.text}")
    except Exception as e:
        print(f"      ❌ Current dashboard metrics API error: {e}")
    
    # Test 3: System Health API
    print("\n3. Testing System Health API")
    admin_tests_total += 1
    try:
        print("   3a. Testing GET /api/admin/system-health")
        response = requests.get(f"{API_BASE_URL}/admin/system-health", timeout=10)
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            health_logs = response.json()
            print(f"      Found {len(health_logs)} system health logs")
            print("      ✅ System health API working")
            admin_tests_passed += 1
        else:
            print(f"      ❌ System health API failed: {response.text}")
    except Exception as e:
        print(f"      ❌ System health API error: {e}")
    
    # Test 4: Sites API for Admin View
    print("\n4. Testing Sites API for Admin Dashboard")
    admin_tests_total += 1
    try:
        print("   4a. Testing GET /api/sites (admin view)")
        response = requests.get(f"{API_BASE_URL}/sites", timeout=10)
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            sites = response.json()
            print(f"      Found {len(sites)} sites for admin dashboard")
            if sites:
                print(f"      Sample site data: {json.dumps(sites[0], indent=2)}")
            print("      ✅ Sites API for admin working")
            admin_tests_passed += 1
        else:
            print(f"      ❌ Sites API failed: {response.text}")
    except Exception as e:
        print(f"      ❌ Sites API error: {e}")
    
    # Test 5: Users API for Admin View
    print("\n5. Testing Users API for Admin Dashboard")
    admin_tests_total += 1
    try:
        print("   5a. Testing GET /api/users (admin view)")
        response = requests.get(f"{API_BASE_URL}/users", timeout=10)
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            users = response.json()
            print(f"      Found {len(users)} users for admin dashboard")
            if users:
                print(f"      Sample user data: {json.dumps(users[0], indent=2)}")
            print("      ✅ Users API for admin working")
            admin_tests_passed += 1
        else:
            print(f"      ❌ Users API failed: {response.text}")
    except Exception as e:
        print(f"      ❌ Users API error: {e}")
    
    return admin_tests_passed, admin_tests_total

def test_zoneminder_system_apis():
    """Test ZoneMinder System APIs for admin dashboard integration"""
    print("\n🎯 ZONEMINDER SYSTEM API INTEGRATION TESTING")
    print("=" * 80)
    
    zm_tests_passed = 0
    zm_tests_total = 0
    
    # Test 1: ZoneMinder Status API
    print("\n1. Testing ZoneMinder Status API")
    zm_tests_total += 1
    try:
        print("   1a. Testing GET /api/zoneminder/status")
        response = requests.get(f"{API_BASE_URL}/zoneminder/status", timeout=10)
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            status = response.json()
            print(f"      ZoneMinder status: {json.dumps(status, indent=2)}")
            
            # Check for required fields
            required_fields = ["status", "system_health", "storage_info"]
            if all(field in status for field in required_fields):
                print("      ✅ ZoneMinder status API working with proper structure")
                zm_tests_passed += 1
            else:
                print("      ❌ ZoneMinder status missing required fields")
        else:
            print(f"      ❌ ZoneMinder status API failed: {response.text}")
    except Exception as e:
        print(f"      ❌ ZoneMinder status API error: {e}")
    
    # Test 2: ZoneMinder Cameras API
    print("\n2. Testing ZoneMinder Cameras API")
    zm_tests_total += 1
    try:
        print("   2a. Testing GET /api/zoneminder/cameras")
        response = requests.get(f"{API_BASE_URL}/zoneminder/cameras", timeout=10)
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            cameras_data = response.json()
            cameras = cameras_data.get("cameras", [])
            print(f"      Found {len(cameras)} ZoneMinder cameras")
            if cameras:
                print(f"      Sample camera: {json.dumps(cameras[0], indent=2)}")
            print("      ✅ ZoneMinder cameras API working")
            zm_tests_passed += 1
        else:
            print(f"      ❌ ZoneMinder cameras API failed: {response.text}")
    except Exception as e:
        print(f"      ❌ ZoneMinder cameras API error: {e}")
    
    # Test 3: ZoneMinder Events API
    print("\n3. Testing ZoneMinder Events API")
    zm_tests_total += 1
    try:
        print("   3a. Testing GET /api/zoneminder/events")
        response = requests.get(f"{API_BASE_URL}/zoneminder/events?limit=10", timeout=10)
        print(f"      Status Code: {response.status_code}")
        
        if response.status_code == 200:
            events_data = response.json()
            events = events_data.get("events", [])
            print(f"      Found {len(events)} ZoneMinder events")
            if events:
                print(f"      Sample event: {json.dumps(events[0], indent=2)}")
            print("      ✅ ZoneMinder events API working")
            zm_tests_passed += 1
        else:
            print(f"      ❌ ZoneMinder events API failed: {response.text}")
    except Exception as e:
        print(f"      ❌ ZoneMinder events API error: {e}")
    
    return zm_tests_passed, zm_tests_total

def analyze_admin_dashboard_data_flow():
    """Analyze the data flow for admin dashboard to identify why it might appear empty"""
    print("\n📊 ADMIN DASHBOARD DATA FLOW ANALYSIS")
    print("=" * 80)
    
    analysis_results = {
        "dashboard_stats": None,
        "current_metrics": None,
        "zoneminder_status": None,
        "zoneminder_cameras": None,
        "zoneminder_events": None,
        "sites_data": None,
        "users_data": None,
        "issues_found": []
    }
    
    # Analyze Dashboard Stats
    print("\n1. Analyzing Dashboard Stats Data")
    try:
        response = requests.get(f"{API_BASE_URL}/dashboard/stats", timeout=10)
        if response.status_code == 200:
            stats = response.json()
            analysis_results["dashboard_stats"] = stats
            print(f"   Dashboard Stats: {json.dumps(stats, indent=2)}")
            
            # Check for empty data
            if stats.get("total_sites", 0) == 0:
                analysis_results["issues_found"].append("No sites in database - dashboard will show 0 sites")
            if stats.get("total_users", 0) == 0:
                analysis_results["issues_found"].append("No users in database - dashboard will show 0 users")
            if stats.get("total_cameras", 0) == 0:
                analysis_results["issues_found"].append("No cameras in database - dashboard will show 0 cameras")
        else:
            analysis_results["issues_found"].append(f"Dashboard stats API failed: {response.status_code}")
    except Exception as e:
        analysis_results["issues_found"].append(f"Dashboard stats API error: {e}")
    
    # Analyze Current Metrics
    print("\n2. Analyzing Current Metrics Data")
    try:
        response = requests.get(f"{API_BASE_URL}/admin/dashboard-metrics/current", timeout=10)
        if response.status_code == 200:
            metrics = response.json()
            analysis_results["current_metrics"] = metrics
            print(f"   Current Metrics: {json.dumps(metrics, indent=2)}")
        else:
            analysis_results["issues_found"].append(f"Current metrics API failed: {response.status_code}")
    except Exception as e:
        analysis_results["issues_found"].append(f"Current metrics API error: {e}")
    
    # Analyze ZoneMinder Data
    print("\n3. Analyzing ZoneMinder Data")
    try:
        # ZoneMinder Status
        response = requests.get(f"{API_BASE_URL}/zoneminder/status", timeout=10)
        if response.status_code == 200:
            zm_status = response.json()
            analysis_results["zoneminder_status"] = zm_status
            print(f"   ZoneMinder Status: {json.dumps(zm_status, indent=2)}")
        else:
            analysis_results["issues_found"].append(f"ZoneMinder status API failed: {response.status_code}")
        
        # ZoneMinder Cameras
        response = requests.get(f"{API_BASE_URL}/zoneminder/cameras", timeout=10)
        if response.status_code == 200:
            zm_cameras = response.json()
            analysis_results["zoneminder_cameras"] = zm_cameras
            camera_count = len(zm_cameras.get("cameras", []))
            print(f"   ZoneMinder Cameras: {camera_count} cameras found")
            
            if camera_count == 0:
                analysis_results["issues_found"].append("No ZoneMinder cameras available - dashboard camera data will be empty")
        else:
            analysis_results["issues_found"].append(f"ZoneMinder cameras API failed: {response.status_code}")
        
        # ZoneMinder Events
        response = requests.get(f"{API_BASE_URL}/zoneminder/events?limit=5", timeout=10)
        if response.status_code == 200:
            zm_events = response.json()
            analysis_results["zoneminder_events"] = zm_events
            event_count = len(zm_events.get("events", []))
            print(f"   ZoneMinder Events: {event_count} recent events found")
            
            if event_count == 0:
                analysis_results["issues_found"].append("No ZoneMinder events available - dashboard activity feed will be empty")
        else:
            analysis_results["issues_found"].append(f"ZoneMinder events API failed: {response.status_code}")
            
    except Exception as e:
        analysis_results["issues_found"].append(f"ZoneMinder API error: {e}")
    
    # Analyze Sites and Users Data
    print("\n4. Analyzing Sites and Users Data")
    try:
        # Sites
        response = requests.get(f"{API_BASE_URL}/sites", timeout=10)
        if response.status_code == 200:
            sites = response.json()
            analysis_results["sites_data"] = sites
            print(f"   Sites: {len(sites)} sites found")
            
            if len(sites) == 0:
                analysis_results["issues_found"].append("No sites in database - admin dashboard site overview will be empty")
        else:
            analysis_results["issues_found"].append(f"Sites API failed: {response.status_code}")
        
        # Users
        response = requests.get(f"{API_BASE_URL}/users", timeout=10)
        if response.status_code == 200:
            users = response.json()
            analysis_results["users_data"] = users
            print(f"   Users: {len(users)} users found")
            
            if len(users) == 0:
                analysis_results["issues_found"].append("No users in database - admin dashboard user management will be empty")
        else:
            analysis_results["issues_found"].append(f"Users API failed: {response.status_code}")
            
    except Exception as e:
        analysis_results["issues_found"].append(f"Sites/Users API error: {e}")
    
    # Summary
    print("\n5. Data Flow Analysis Summary")
    print("   Issues Found:")
    if analysis_results["issues_found"]:
        for i, issue in enumerate(analysis_results["issues_found"], 1):
            print(f"      {i}. {issue}")
    else:
        print("      No critical issues found - admin dashboard should have data")
    
    return analysis_results

def main():
    """Main testing function for admin dashboard"""
    
    # Test Admin Dashboard APIs
    admin_passed, admin_total = test_admin_dashboard_apis()
    
    # Test ZoneMinder System APIs
    zm_passed, zm_total = test_zoneminder_system_apis()
    
    # Analyze Admin Dashboard Data Flow
    analysis_results = analyze_admin_dashboard_data_flow()
    
    # Summary
    print("\n" + "="*80)
    print("🎯 ADMIN DASHBOARD TESTING SUMMARY")
    print("="*80)
    
    print(f"\n📊 Test Results:")
    print(f"   Admin Dashboard APIs: {admin_passed}/{admin_total} passed")
    print(f"   ZoneMinder System APIs: {zm_passed}/{zm_total} passed")
    print(f"   Data Flow Issues Found: {len(analysis_results['issues_found'])}")
    
    # Determine overall status
    total_passed = admin_passed + zm_passed
    total_tests = admin_total + zm_total
    
    if total_passed == total_tests and len(analysis_results["issues_found"]) == 0:
        print(f"\n✅ ADMIN DASHBOARD INTEGRATION: ALL TESTS PASSED")
        print("   Admin dashboard should be working properly with data")
    elif total_passed == total_tests:
        print(f"\n⚠️ ADMIN DASHBOARD INTEGRATION: APIs WORKING BUT DATA ISSUES FOUND")
        print("   Admin dashboard APIs are functional but may appear empty due to data issues")
    else:
        print(f"\n❌ ADMIN DASHBOARD INTEGRATION: CRITICAL API FAILURES")
        print("   Admin dashboard will not work properly due to API failures")
    
    return total_passed == total_tests and len(analysis_results["issues_found"]) == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)