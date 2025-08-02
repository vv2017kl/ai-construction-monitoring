-- ================================================================
-- SAMPLE DATA FOR TESTING
-- Construction Site AI Monitoring System
-- Version: 1.0
-- ================================================================

USE construction_management;

-- ================================================================
-- SAMPLE COMPANIES
-- ================================================================
INSERT INTO companies (id, name, legal_name, registration_number, status, license_type, max_sites, max_users, max_cameras) VALUES
('11111111-1111-1111-1111-111111111111', 'Acme Construction', 'Acme Construction LLC', 'LLC-2024-001', 'active', 'professional', 20, 100, 500),
('22222222-2222-2222-2222-222222222222', 'BuildCorp Industries', 'BuildCorp Industries Inc.', 'INC-2024-002', 'active', 'enterprise', 50, 500, 2000);

-- ================================================================
-- SAMPLE GROUPS
-- ================================================================
INSERT INTO groups (id, company_id, name, description, region, country, status) VALUES
('33333333-3333-3333-3333-333333333333', '11111111-1111-1111-1111-111111111111', 'Northeast Division', 'Construction projects in northeastern US', 'Northeast', 'USA', 'active'),
('44444444-4444-4444-4444-444444444444', '11111111-1111-1111-1111-111111111111', 'Southeast Division', 'Construction projects in southeastern US', 'Southeast', 'USA', 'active');

-- ================================================================
-- SAMPLE SITES
-- ================================================================
INSERT INTO sites (id, company_id, group_id, site_code, name, project_type, project_phase, address, city, state_province, country, latitude, longitude, status) VALUES
('55555555-5555-5555-5555-555555555555', '11111111-1111-1111-1111-111111111111', '33333333-3333-3333-3333-333333333333', 'NYC-001', 'Manhattan Office Tower', 'commercial', 'construction', '123 Main St', 'New York', 'NY', 'USA', 40.7128, -74.0060, 'active'),
('66666666-6666-6666-6666-666666666666', '11111111-1111-1111-1111-111111111111', '44444444-4444-4444-4444-444444444444', 'MIA-001', 'Miami Residential Complex', 'residential', 'preparation', '456 Ocean Dr', 'Miami', 'FL', 'USA', 25.7617, -80.1918, 'active');

-- ================================================================
-- SAMPLE ROLES
-- ================================================================
INSERT INTO roles (id, company_id, name, display_name, hierarchy_level, permissions, can_acknowledge_alerts, can_manage_sites, can_manage_cameras) VALUES
('77777777-7777-7777-7777-777777777777', '11111111-1111-1111-1111-111111111111', 'sysadmin', 'System Administrator', '1', '{"all": true}', TRUE, TRUE, TRUE),
('88888888-8888-8888-8888-888888888888', '11111111-1111-1111-1111-111111111111', 'company_exec', 'Company Executive', '2', '{"company": ["read", "write"], "reports": ["all"]}', TRUE, TRUE, FALSE),
('99999999-9999-9999-9999-999999999999', '11111111-1111-1111-1111-111111111111', 'group_site_manager', 'Group Site Manager', '3', '{"groups": ["read", "write"], "sites": ["read", "write"]}', TRUE, TRUE, FALSE),
('aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa', '11111111-1111-1111-1111-111111111111', 'site_manager', 'Site Manager', '4', '{"sites": ["read", "write"], "alerts": ["read", "acknowledge"]}', TRUE, FALSE, FALSE),
('bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb', '11111111-1111-1111-1111-111111111111', 'site_coordinator', 'Site Coordinator', '5', '{"sites": ["read"], "alerts": ["read"]}', FALSE, FALSE, FALSE);

-- ================================================================
-- SAMPLE USERS
-- ================================================================
INSERT INTO users (id, company_id, username, email, first_name, last_name, password_hash, status, default_site_id) VALUES
('cccccccc-cccc-cccc-cccc-cccccccccccc', '11111111-1111-1111-1111-111111111111', 'admin', 'admin@acme.com', 'System', 'Administrator', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewqWTUZEDu5N6ey2', 'active', '55555555-5555-5555-5555-555555555555'),
('dddddddd-dddd-dddd-dddd-dddddddddddd', '11111111-1111-1111-1111-111111111111', 'john.manager', 'john@acme.com', 'John', 'Manager', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewqWTUZEDu5N6ey2', 'active', '55555555-5555-5555-5555-555555555555'),
('eeeeeeee-eeee-eeee-eeee-eeeeeeeeeeee', '11111111-1111-1111-1111-111111111111', 'mary.coord', 'mary@acme.com', 'Mary', 'Coordinator', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewqWTUZEDu5N6ey2', 'active', '66666666-6666-6666-6666-666666666666');

-- ================================================================
-- SAMPLE USER ROLES
-- ================================================================
INSERT INTO user_roles (id, user_id, role_id, is_active) VALUES
('ffffffff-ffff-ffff-ffff-ffffffffffff', 'cccccccc-cccc-cccc-cccc-cccccccccccc', '77777777-7777-7777-7777-777777777777', TRUE),
('10101010-1010-1010-1010-101010101010', 'dddddddd-dddd-dddd-dddd-dddddddddddd', 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa', TRUE),
('11111111-2222-3333-4444-555555555555', 'eeeeeeee-eeee-eeee-eeee-eeeeeeeeeeee', 'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb', TRUE);

-- ================================================================
-- SAMPLE SITE COORDINATES
-- ================================================================
INSERT INTO site_coordinates (id, site_id, latitude, longitude, coordinate_system, address_verified) VALUES
('12121212-1212-1212-1212-121212121212', '55555555-5555-5555-5555-555555555555', 40.7128, -74.0060, 'WGS84', TRUE),
('13131313-1313-1313-1313-131313131313', '66666666-6666-6666-6666-666666666666', 25.7617, -80.1918, 'WGS84', TRUE);

-- ================================================================
-- SAMPLE AI MODELS
-- ================================================================
INSERT INTO ai_models (id, name, display_name, model_type, framework, version, supported_classes, input_resolution, status) VALUES
('14141414-1414-1414-1414-141414141414', 'yolov8_construction_safety', 'YOLOv8 Construction Safety Model', 'object_detection', 'YOLOv8', '1.0', '["person", "hard_hat", "no_hard_hat", "safety_vest", "no_safety_vest", "excavator", "crane"]', '{"width": 640, "height": 640}', 'active');

-- Switch to VMS database for camera data
USE construction_vms;

-- ================================================================
-- SAMPLE CAMERA MANUFACTURERS
-- ================================================================
INSERT INTO camera_manufacturers (id, name, display_name, status) VALUES
('15151515-1515-1515-1515-151515151515', 'hikvision', 'Hikvision Digital Technology Co.', 'active'),
('16161616-1616-1616-1616-161616161616', 'dahua', 'Dahua Technology Co.', 'active'),
('17171717-1717-1717-1717-171717171717', 'axis', 'Axis Communications AB', 'active');

-- ================================================================
-- SAMPLE CAMERA MODELS
-- ================================================================
INSERT INTO camera_models (id, manufacturer_id, model_number, model_name, category, max_resolution, night_vision) VALUES
('18181818-1818-1818-1818-181818181818', '15151515-1515-1515-1515-151515151515', 'DS-2CD2143G0-I', 'Hikvision 4MP IR Dome', 'dome', '4MP', TRUE),
('19191919-1919-1919-1919-191919191919', '16161616-1616-1616-1616-161616161616', 'IPC-HDW4433C-A', 'Dahua 4MP Eyeball', 'dome', '4MP', TRUE),
('20202020-2020-2020-2020-202020202020', '17171717-1717-1717-1717-171717171717', 'M3007-PV', 'Axis M3007-PV Network Camera', 'fisheye', '5MP', FALSE);

-- ================================================================
-- SAMPLE CAMERAS
-- ================================================================
INSERT INTO cameras (id, camera_identifier, name, manufacturer_id, model_id, ip_address, primary_stream_url, location_description, status) VALUES
('21212121-2121-2121-2121-212121212121', 'NYC-001-CAM-01', 'Main Entrance Camera', '15151515-1515-1515-1515-151515151515', '18181818-1818-1818-1818-181818181818', '192.168.1.101', 'rtsp://192.168.1.101:554/stream1', 'Main entrance to construction site', 'active'),
('22222222-2323-2323-2323-232323232323', 'NYC-001-CAM-02', 'Crane Operation Area', '16161616-1616-1616-1616-161616161616', '19191919-1919-1919-1919-191919191919', '192.168.1.102', 'rtsp://192.168.1.102:554/stream1', 'Crane operation zone monitoring', 'active'),
('23232323-2424-2424-2424-242424242424', 'MIA-001-CAM-01', 'Site Overview Camera', '17171717-1717-1717-1717-171717171717', '20202020-2020-2020-2020-202020202020', '192.168.2.101', 'rtsp://192.168.2.101:554/stream1', '360-degree site overview', 'active');

-- Display success message
SELECT 'Sample data inserted successfully!' as Status;
SELECT 'Companies: 2, Sites: 2, Users: 3, Cameras: 3' as Summary;