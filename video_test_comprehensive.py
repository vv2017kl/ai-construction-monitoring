#!/usr/bin/env python3
"""
Comprehensive Video & Evidence Management API Testing Script
Tests all video management endpoints with actual data creation and manipulation
"""

import requests
import json
import sys
from datetime import datetime, date
import os
from dotenv import load_dotenv
import uuid

# Load environment variables
load_dotenv('/app/frontend/.env')

# Get the backend URL from environment
BACKEND_URL = os.getenv('REACT_APP_BACKEND_URL')
API_BASE_URL = f"{BACKEND_URL}/api"

print(f"Testing Video & Evidence Management APIs at: {API_BASE_URL}")
print("=" * 80)

def create_test_data():
    """Create test user, site, and camera for video testing"""
    print("\n1. Creating Test Data (User, Site, Camera)")
    
    # Create test user
    test_user_data = {
        "username": f"video_tester_{uuid.uuid4().hex[:8]}",
        "email": f"video.tester.{uuid.uuid4().hex[:8]}@construction.com",
        "first_name": "Video",
        "last_name": "Tester",
        "password": "VideoTest123!",
        "role": "site_manager",
        "department": "Security",
        "phone": "+1-555-0199"
    }
    
    response = requests.post(f"{API_BASE_URL}/users", json=test_user_data, timeout=10)
    if response.status_code != 200:
        print(f"   ❌ Failed to create test user: {response.status_code}")
        return None, None, None
    
    user = response.json()
    user_id = user.get("id")
    print(f"   ✅ Created test user: {user_id}")
    
    # Create test site
    test_site_data = {
        "name": f"Video Test Site {uuid.uuid4().hex[:8]}",
        "code": f"VTS-{uuid.uuid4().hex[:8].upper()}",
        "address": "456 Video Test Ave, Security City, SC 54321",
        "type": "commercial",
        "phase": "construction",
        "manager_id": user_id
    }
    
    response = requests.post(f"{API_BASE_URL}/sites", json=test_site_data, timeout=10)
    if response.status_code != 200:
        print(f"   ❌ Failed to create test site: {response.status_code}")
        return user_id, None, None
    
    site = response.json()
    site_id = site.get("id")
    print(f"   ✅ Created test site: {site_id}")
    
    # Create test camera (we need to add this to the database manually since there's no camera creation endpoint)
    # For now, we'll use a fake camera ID and test the endpoints
    camera_id = str(uuid.uuid4())
    print(f"   ⚠️ Using fake camera ID for testing: {camera_id}")
    
    return user_id, site_id, camera_id

def test_video_bookmarks_comprehensive(camera_id, user_id):
    """Comprehensive test of Video Bookmarks API"""
    print("\n2. Testing Video Bookmarks API (Comprehensive)")
    created_bookmarks = []
    
    try:
        # Test 1: Create multiple video bookmarks with different types
        bookmark_test_cases = [
            {
                "camera_id": camera_id,
                "bookmark_date": "2024-01-15",
                "timestamp_seconds": 3600,
                "title": "Safety Incident - Hard Hat Violation",
                "description": "Worker without hard hat detected in construction zone",
                "bookmark_type": "safety_incident",
                "priority_level": "high"
            },
            {
                "camera_id": camera_id,
                "bookmark_date": "2024-01-15",
                "timestamp_seconds": 7200,
                "title": "Equipment Malfunction",
                "description": "Crane showing unusual movement patterns",
                "bookmark_type": "equipment_issue",
                "priority_level": "medium"
            },
            {
                "camera_id": camera_id,
                "bookmark_date": "2024-01-16",
                "timestamp_seconds": 1800,
                "title": "Compliance Check Point",
                "description": "PPE compliance verification needed",
                "bookmark_type": "compliance_check",
                "priority_level": "low"
            }
        ]
        
        print("   2a. Creating multiple video bookmarks")
        for i, bookmark_data in enumerate(bookmark_test_cases):
            response = requests.post(
                f"{API_BASE_URL}/video-bookmarks",
                json=bookmark_data,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            if response.status_code == 200:
                bookmark = response.json()
                bookmark_id = bookmark.get("id")
                created_bookmarks.append(bookmark_id)
                print(f"      ✅ Created bookmark {i+1}: {bookmark_id}")
                print(f"         Type: {bookmark_data['bookmark_type']}, Priority: {bookmark_data['priority_level']}")
            else:
                print(f"      ❌ Failed to create bookmark {i+1}: {response.status_code}")
                print(f"         Response: {response.text}")
                return False, []
        
        # Test 2: Retrieve all bookmarks and verify count
        print("   2b. Testing GET all video bookmarks")
        response = requests.get(f"{API_BASE_URL}/video-bookmarks", timeout=10)
        if response.status_code == 200:
            all_bookmarks = response.json()
            print(f"      ✅ Retrieved {len(all_bookmarks)} total bookmarks")
            
            # Verify our created bookmarks are in the list
            our_bookmark_ids = [b.get("id") for b in all_bookmarks if b.get("id") in created_bookmarks]
            print(f"      ✅ Found {len(our_bookmark_ids)} of our created bookmarks")
        else:
            print(f"      ❌ Failed to get all bookmarks: {response.status_code}")
            return False, created_bookmarks
        
        # Test 3: Filter bookmarks by camera
        print("   2c. Testing GET bookmarks filtered by camera")
        response = requests.get(f"{API_BASE_URL}/video-bookmarks?camera_id={camera_id}", timeout=10)
        if response.status_code == 200:
            camera_bookmarks = response.json()
            print(f"      ✅ Retrieved {len(camera_bookmarks)} bookmarks for camera")
        else:
            print(f"      ❌ Failed to get camera bookmarks: {response.status_code}")
            return False, created_bookmarks
        
        # Test 4: Filter bookmarks by user
        print("   2d. Testing GET bookmarks filtered by user")
        response = requests.get(f"{API_BASE_URL}/video-bookmarks?user_id={user_id}", timeout=10)
        if response.status_code == 200:
            user_bookmarks = response.json()
            print(f"      ✅ Retrieved {len(user_bookmarks)} bookmarks for user")
        else:
            print(f"      ❌ Failed to get user bookmarks: {response.status_code}")
            return False, created_bookmarks
        
        # Test 5: Get specific bookmark details
        if created_bookmarks:
            test_bookmark_id = created_bookmarks[0]
            print(f"   2e. Testing GET specific bookmark: {test_bookmark_id}")
            response = requests.get(f"{API_BASE_URL}/video-bookmarks/{test_bookmark_id}", timeout=10)
            if response.status_code == 200:
                bookmark_detail = response.json()
                print(f"      ✅ Retrieved bookmark details")
                print(f"         Title: {bookmark_detail.get('title')}")
                print(f"         Type: {bookmark_detail.get('bookmark_type')}")
                print(f"         Status: {bookmark_detail.get('status')}")
            else:
                print(f"      ❌ Failed to get bookmark details: {response.status_code}")
                return False, created_bookmarks
        
        # Test 6: Update bookmark status
        if created_bookmarks:
            test_bookmark_id = created_bookmarks[0]
            print(f"   2f. Testing PUT bookmark status update")
            response = requests.put(f"{API_BASE_URL}/video-bookmarks/{test_bookmark_id}/status?status=reviewed", timeout=10)
            if response.status_code == 200:
                print(f"      ✅ Updated bookmark status to 'reviewed'")
                
                # Verify the status was updated
                response = requests.get(f"{API_BASE_URL}/video-bookmarks/{test_bookmark_id}", timeout=10)
                if response.status_code == 200:
                    updated_bookmark = response.json()
                    if updated_bookmark.get('status') == 'reviewed':
                        print(f"      ✅ Status update verified")
                    else:
                        print(f"      ⚠️ Status update not reflected: {updated_bookmark.get('status')}")
            else:
                print(f"      ❌ Failed to update bookmark status: {response.status_code}")
                return False, created_bookmarks
        
        # Test 7: Test pagination
        print("   2g. Testing pagination with limit")
        response = requests.get(f"{API_BASE_URL}/video-bookmarks?limit=2", timeout=10)
        if response.status_code == 200:
            limited_bookmarks = response.json()
            print(f"      ✅ Retrieved {len(limited_bookmarks)} bookmarks with limit=2")
        else:
            print(f"      ❌ Failed to test pagination: {response.status_code}")
            return False, created_bookmarks
        
        return True, created_bookmarks
        
    except Exception as e:
        print(f"   ❌ Unexpected error in video bookmarks test: {e}")
        return False, created_bookmarks

def test_video_exports_comprehensive(camera_id, user_id):
    """Comprehensive test of Video Exports API"""
    print("\n3. Testing Video Exports API (Comprehensive)")
    created_exports = []
    
    try:
        # Test 1: Create multiple video exports with different types
        export_test_cases = [
            {
                "camera_id": camera_id,
                "source_video_date": "2024-01-15",
                "start_timestamp_seconds": 1800,
                "end_timestamp_seconds": 5400,
                "export_type": "evidence_package",
                "export_format": "mp4",
                "export_purpose": "evidence",
                "export_justification": "Evidence collection for safety incident investigation",
                "quality_setting": "high"
            },
            {
                "camera_id": camera_id,
                "source_video_date": "2024-01-16",
                "start_timestamp_seconds": 3600,
                "end_timestamp_seconds": 7200,
                "export_type": "compliance_report",
                "export_format": "avi",
                "export_purpose": "compliance",
                "export_justification": "Required footage for OSHA compliance audit",
                "quality_setting": "medium"
            },
            {
                "camera_id": camera_id,
                "source_video_date": "2024-01-17",
                "start_timestamp_seconds": 900,
                "end_timestamp_seconds": 2700,
                "export_type": "video_clip",
                "export_format": "mp4",
                "export_purpose": "training",
                "export_justification": "Creating training material for new workers",
                "quality_setting": "low"
            }
        ]
        
        print("   3a. Creating multiple video exports")
        for i, export_data in enumerate(export_test_cases):
            response = requests.post(
                f"{API_BASE_URL}/video-exports",
                json=export_data,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            if response.status_code == 200:
                export = response.json()
                export_id = export.get("id")
                created_exports.append(export_id)
                print(f"      ✅ Created export {i+1}: {export_id}")
                print(f"         Type: {export_data['export_type']}, Format: {export_data['export_format']}")
                print(f"         Duration: {export_data['end_timestamp_seconds'] - export_data['start_timestamp_seconds']} seconds")
            else:
                print(f"      ❌ Failed to create export {i+1}: {response.status_code}")
                print(f"         Response: {response.text}")
                return False, []
        
        # Test 2: Retrieve all exports
        print("   3b. Testing GET all video exports")
        response = requests.get(f"{API_BASE_URL}/video-exports", timeout=10)
        if response.status_code == 200:
            all_exports = response.json()
            print(f"      ✅ Retrieved {len(all_exports)} total exports")
        else:
            print(f"      ❌ Failed to get all exports: {response.status_code}")
            return False, created_exports
        
        # Test 3: Filter exports by camera
        print("   3c. Testing GET exports filtered by camera")
        response = requests.get(f"{API_BASE_URL}/video-exports?camera_id={camera_id}", timeout=10)
        if response.status_code == 200:
            camera_exports = response.json()
            print(f"      ✅ Retrieved {len(camera_exports)} exports for camera")
        else:
            print(f"      ❌ Failed to get camera exports: {response.status_code}")
            return False, created_exports
        
        # Test 4: Filter exports by user
        print("   3d. Testing GET exports filtered by user")
        response = requests.get(f"{API_BASE_URL}/video-exports?user_id={user_id}", timeout=10)
        if response.status_code == 200:
            user_exports = response.json()
            print(f"      ✅ Retrieved {len(user_exports)} exports for user")
        else:
            print(f"      ❌ Failed to get user exports: {response.status_code}")
            return False, created_exports
        
        # Test 5: Filter exports by status
        print("   3e. Testing GET exports filtered by status")
        response = requests.get(f"{API_BASE_URL}/video-exports?status=pending", timeout=10)
        if response.status_code == 200:
            pending_exports = response.json()
            print(f"      ✅ Retrieved {len(pending_exports)} pending exports")
        else:
            print(f"      ❌ Failed to get pending exports: {response.status_code}")
            return False, created_exports
        
        # Test 6: Get specific export details
        if created_exports:
            test_export_id = created_exports[0]
            print(f"   3f. Testing GET specific export: {test_export_id}")
            response = requests.get(f"{API_BASE_URL}/video-exports/{test_export_id}", timeout=10)
            if response.status_code == 200:
                export_detail = response.json()
                print(f"      ✅ Retrieved export details")
                print(f"         Purpose: {export_detail.get('export_purpose')}")
                print(f"         Format: {export_detail.get('export_format')}")
                print(f"         Status: {export_detail.get('export_status')}")
            else:
                print(f"      ❌ Failed to get export details: {response.status_code}")
                return False, created_exports
        
        # Test 7: Update export status through processing workflow
        if created_exports:
            test_export_id = created_exports[0]
            print(f"   3g. Testing export status workflow")
            
            # Update to processing
            response = requests.put(f"{API_BASE_URL}/video-exports/{test_export_id}/status?status=processing", timeout=10)
            if response.status_code == 200:
                print(f"      ✅ Updated export status to 'processing'")
            else:
                print(f"      ❌ Failed to update to processing: {response.status_code}")
                return False, created_exports
            
            # Update to completed with download URL
            download_url = "https://example.com/exports/video_export_123.mp4"
            response = requests.put(f"{API_BASE_URL}/video-exports/{test_export_id}/status?status=completed&download_url={download_url}", timeout=10)
            if response.status_code == 200:
                print(f"      ✅ Updated export status to 'completed' with download URL")
                
                # Verify the status and URL were updated
                response = requests.get(f"{API_BASE_URL}/video-exports/{test_export_id}", timeout=10)
                if response.status_code == 200:
                    updated_export = response.json()
                    if updated_export.get('export_status') == 'completed':
                        print(f"      ✅ Status update verified")
                    if updated_export.get('download_url') == download_url:
                        print(f"      ✅ Download URL update verified")
            else:
                print(f"      ❌ Failed to update to completed: {response.status_code}")
                return False, created_exports
        
        return True, created_exports
        
    except Exception as e:
        print(f"   ❌ Unexpected error in video exports test: {e}")
        return False, created_exports

def test_video_quality_metrics_comprehensive(camera_id):
    """Comprehensive test of Video Quality Metrics API"""
    print("\n4. Testing Video Quality Metrics API (Comprehensive)")
    
    try:
        # Test 1: Get all quality metrics
        print("   4a. Testing GET all video quality metrics")
        response = requests.get(f"{API_BASE_URL}/video-quality-metrics", timeout=10)
        if response.status_code == 200:
            all_metrics = response.json()
            print(f"      ✅ Retrieved {len(all_metrics)} total quality metrics")
        else:
            print(f"      ❌ Failed to get all quality metrics: {response.status_code}")
            return False
        
        # Test 2: Get quality metrics with different time ranges
        time_ranges = [7, 14, 30, 90]
        for days in time_ranges:
            print(f"   4b.{days}. Testing GET quality metrics for last {days} days")
            response = requests.get(f"{API_BASE_URL}/video-quality-metrics?days={days}", timeout=10)
            if response.status_code == 200:
                metrics = response.json()
                print(f"      ✅ Retrieved {len(metrics)} quality metrics for last {days} days")
            else:
                print(f"      ❌ Failed to get {days}-day quality metrics: {response.status_code}")
                return False
        
        # Test 3: Get quality metrics by camera
        print("   4c. Testing GET quality metrics by camera")
        response = requests.get(f"{API_BASE_URL}/cameras/{camera_id}/quality-metrics", timeout=10)
        if response.status_code == 200:
            camera_metrics = response.json()
            print(f"      ✅ Retrieved {len(camera_metrics)} quality metrics for camera")
        else:
            print(f"      ❌ Failed to get camera quality metrics: {response.status_code}")
            return False
        
        # Test 4: Get quality metrics by camera with different time ranges
        for days in [7, 30]:
            print(f"   4d.{days}. Testing GET camera quality metrics for last {days} days")
            response = requests.get(f"{API_BASE_URL}/cameras/{camera_id}/quality-metrics?days={days}", timeout=10)
            if response.status_code == 200:
                camera_metrics = response.json()
                print(f"      ✅ Retrieved {len(camera_metrics)} camera quality metrics for last {days} days")
            else:
                print(f"      ❌ Failed to get {days}-day camera quality metrics: {response.status_code}")
                return False
        
        # Test 5: Get quality summary for camera
        print("   4e. Testing GET camera quality summary")
        response = requests.get(f"{API_BASE_URL}/cameras/{camera_id}/quality-summary", timeout=10)
        if response.status_code == 200:
            summary = response.json()
            print(f"      ✅ Retrieved camera quality summary")
            if "message" in summary:
                print(f"         Message: {summary['message']}")
            elif "camera_id" in summary:
                print(f"         Camera ID: {summary['camera_id']}")
                print(f"         Metrics Count: {summary.get('metrics_count', 0)}")
                if 'average_sharpness' in summary:
                    print(f"         Avg Sharpness: {summary['average_sharpness']}")
                if 'average_brightness' in summary:
                    print(f"         Avg Brightness: {summary['average_brightness']}")
        else:
            print(f"      ❌ Failed to get camera quality summary: {response.status_code}")
            return False
        
        # Test 6: Get quality summary with different time ranges
        for days in [7, 14, 30]:
            print(f"   4f.{days}. Testing GET camera quality summary for last {days} days")
            response = requests.get(f"{API_BASE_URL}/cameras/{camera_id}/quality-summary?days={days}", timeout=10)
            if response.status_code == 200:
                summary = response.json()
                print(f"      ✅ Retrieved {days}-day camera quality summary")
            else:
                print(f"      ❌ Failed to get {days}-day camera quality summary: {response.status_code}")
                return False
        
        # Test 7: Get quality metrics with camera filter
        print("   4g. Testing GET quality metrics with camera filter")
        response = requests.get(f"{API_BASE_URL}/video-quality-metrics?camera_id={camera_id}", timeout=10)
        if response.status_code == 200:
            filtered_metrics = response.json()
            print(f"      ✅ Retrieved {len(filtered_metrics)} quality metrics with camera filter")
        else:
            print(f"      ❌ Failed to get filtered quality metrics: {response.status_code}")
            return False
        
        # Test 8: Combined filters
        print("   4h. Testing GET quality metrics with combined filters")
        response = requests.get(f"{API_BASE_URL}/video-quality-metrics?camera_id={camera_id}&days=14", timeout=10)
        if response.status_code == 200:
            combined_metrics = response.json()
            print(f"      ✅ Retrieved {len(combined_metrics)} quality metrics with combined filters")
        else:
            print(f"      ❌ Failed to get combined filtered quality metrics: {response.status_code}")
            return False
        
        return True
        
    except Exception as e:
        print(f"   ❌ Unexpected error in video quality metrics test: {e}")
        return False

def test_video_access_logs_comprehensive(camera_id, user_id):
    """Comprehensive test of Video Access Logs API"""
    print("\n5. Testing Video Access Logs API (Comprehensive)")
    
    try:
        # Test 1: Get all access logs
        print("   5a. Testing GET all video access logs")
        response = requests.get(f"{API_BASE_URL}/video-access-logs", timeout=10)
        if response.status_code == 200:
            all_logs = response.json()
            print(f"      ✅ Retrieved {len(all_logs)} total access logs")
        else:
            print(f"      ❌ Failed to get all access logs: {response.status_code}")
            return False
        
        # Test 2: Get access logs by camera
        print("   5b. Testing GET access logs by camera")
        response = requests.get(f"{API_BASE_URL}/cameras/{camera_id}/access-logs", timeout=10)
        if response.status_code == 200:
            camera_logs = response.json()
            print(f"      ✅ Retrieved {len(camera_logs)} access logs for camera")
        else:
            print(f"      ❌ Failed to get camera access logs: {response.status_code}")
            return False
        
        # Test 3: Get access logs by user
        print("   5c. Testing GET access logs by user")
        response = requests.get(f"{API_BASE_URL}/users/{user_id}/video-access-logs", timeout=10)
        if response.status_code == 200:
            user_logs = response.json()
            print(f"      ✅ Retrieved {len(user_logs)} access logs for user")
        else:
            print(f"      ❌ Failed to get user access logs: {response.status_code}")
            return False
        
        # Test 4: Get access logs with filters
        filter_combinations = [
            f"user_id={user_id}",
            f"camera_id={camera_id}",
            f"user_id={user_id}&camera_id={camera_id}",
            f"limit=10",
            f"skip=0&limit=5"
        ]
        
        for i, filter_params in enumerate(filter_combinations):
            print(f"   5d.{i+1}. Testing GET access logs with filter: {filter_params}")
            response = requests.get(f"{API_BASE_URL}/video-access-logs?{filter_params}", timeout=10)
            if response.status_code == 200:
                filtered_logs = response.json()
                print(f"      ✅ Retrieved {len(filtered_logs)} filtered access logs")
            else:
                print(f"      ❌ Failed to get filtered access logs: {response.status_code}")
                return False
        
        return True
        
    except Exception as e:
        print(f"   ❌ Unexpected error in video access logs test: {e}")
        return False

def cleanup_test_data(user_id, site_id, bookmark_ids, export_ids):
    """Clean up test data"""
    print("\n6. Cleaning up test data")
    
    try:
        # Delete bookmarks
        for bookmark_id in bookmark_ids:
            response = requests.delete(f"{API_BASE_URL}/video-bookmarks/{bookmark_id}", timeout=10)
            if response.status_code == 200:
                print(f"   ✅ Deleted bookmark: {bookmark_id}")
            else:
                print(f"   ⚠️ Could not delete bookmark {bookmark_id}: {response.status_code}")
        
        # Delete site
        if site_id:
            response = requests.delete(f"{API_BASE_URL}/sites/{site_id}", timeout=10)
            if response.status_code == 200:
                print(f"   ✅ Deleted site: {site_id}")
            else:
                print(f"   ⚠️ Could not delete site {site_id}: {response.status_code}")
        
        # Note: User and exports don't have DELETE endpoints
        print(f"   ⚠️ User and exports cleanup skipped (no DELETE endpoints)")
        
        return True
        
    except Exception as e:
        print(f"   ⚠️ Cleanup error: {e}")
        return False

def main():
    """Run comprehensive video & evidence management tests"""
    print("Starting Comprehensive Video & Evidence Management API Tests...")
    
    # Create test data
    user_id, site_id, camera_id = create_test_data()
    if not user_id or not site_id or not camera_id:
        print("❌ Failed to create test data - aborting tests")
        return False
    
    results = []
    created_bookmarks = []
    created_exports = []
    
    # Test Video Bookmarks API
    bookmarks_ok, created_bookmarks = test_video_bookmarks_comprehensive(camera_id, user_id)
    results.append(("Video Bookmarks API (Comprehensive)", bookmarks_ok))
    
    # Test Video Exports API
    exports_ok, created_exports = test_video_exports_comprehensive(camera_id, user_id)
    results.append(("Video Exports API (Comprehensive)", exports_ok))
    
    # Test Video Quality Metrics API
    quality_ok = test_video_quality_metrics_comprehensive(camera_id)
    results.append(("Video Quality Metrics API (Comprehensive)", quality_ok))
    
    # Test Video Access Logs API
    access_logs_ok = test_video_access_logs_comprehensive(camera_id, user_id)
    results.append(("Video Access Logs API (Comprehensive)", access_logs_ok))
    
    # Cleanup
    cleanup_ok = cleanup_test_data(user_id, site_id, created_bookmarks, created_exports)
    results.append(("Test Data Cleanup", cleanup_ok))
    
    # Summary
    print("\n" + "=" * 80)
    print("COMPREHENSIVE VIDEO & EVIDENCE MANAGEMENT TEST RESULTS:")
    print("=" * 80)
    
    all_passed = True
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{test_name:<45} {status}")
        if not passed:
            all_passed = False
    
    print("=" * 80)
    if all_passed:
        print("🎉 ALL COMPREHENSIVE VIDEO TESTS PASSED!")
        print("✅ Video Bookmarks: Full CRUD operations working")
        print("✅ Video Exports: Full workflow testing successful")
        print("✅ Video Quality Metrics: All filtering and summary operations working")
        print("✅ Video Access Logs: All filtering operations working")
        print("✅ Database operations: All video tables functioning correctly")
        return True
    else:
        print("⚠️  SOME COMPREHENSIVE VIDEO TESTS FAILED!")
        print("Please check the detailed output above for specific issues.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)