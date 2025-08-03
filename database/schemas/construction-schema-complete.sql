-- ================================================================
-- COMPLETE CONSTRUCTION MANAGEMENT SYSTEM SCHEMA  
-- Construction Site AI Monitoring System - Construction Database
-- Version: 1.0
-- Tables: 23 (COMPLETE)
-- ================================================================

USE construction_management;

-- ================================================================
-- TABLE 1: COMPANIES
-- ================================================================
CREATE TABLE companies (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    name VARCHAR(200) NOT NULL,
    legal_name VARCHAR(250),
    registration_number VARCHAR(100),
    tax_id VARCHAR(50),
    
    -- Contact information
    headquarters_address TEXT,
    phone VARCHAR(20),
    email VARCHAR(100),
    website VARCHAR(255),
    
    -- Business information
    industry VARCHAR(100) DEFAULT 'Construction',
    company_size ENUM('small', 'medium', 'large', 'enterprise') DEFAULT 'medium',
    annual_revenue_range VARCHAR(50),
    
    -- Subscription and licensing
    license_type ENUM('trial', 'basic', 'professional', 'enterprise') DEFAULT 'trial',
    license_expiry DATE,
    max_sites INT DEFAULT 5,
    max_users INT DEFAULT 50,
    max_cameras INT DEFAULT 100,
    
    -- Configuration
    timezone VARCHAR(50) DEFAULT 'UTC',
    date_format VARCHAR(20) DEFAULT 'YYYY-MM-DD',
    currency VARCHAR(3) DEFAULT 'USD',
    
    -- Status
    status ENUM('active', 'suspended', 'cancelled') DEFAULT 'active',
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    UNIQUE KEY uk_company_registration (registration_number),
    INDEX idx_company_status (status),
    INDEX idx_company_license (license_type, license_expiry)
) ENGINE=InnoDB COMMENT='Top-level company entities';

-- ================================================================
-- TABLE 2: GROUPS
-- ================================================================
CREATE TABLE groups (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    company_id CHAR(36) NOT NULL,
    name VARCHAR(150) NOT NULL,
    description TEXT,
    
    -- Hierarchy
    parent_group_id CHAR(36) NULL COMMENT 'For nested group structures',
    group_level INT DEFAULT 1 COMMENT 'Hierarchy level',
    
    -- Geographic coverage
    region VARCHAR(100),
    country VARCHAR(100),
    state_province VARCHAR(100),
    coverage_area JSON COMMENT 'Geographic boundaries',
    
    -- Management
    group_manager_user_id CHAR(36),
    budget_allocation DECIMAL(15,2),
    
    -- Contact information
    office_address TEXT,
    phone VARCHAR(20),
    email VARCHAR(100),
    
    -- Status
    status ENUM('active', 'inactive') DEFAULT 'active',
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (company_id) REFERENCES companies(id) ON DELETE CASCADE,
    FOREIGN KEY (parent_group_id) REFERENCES groups(id) ON DELETE SET NULL,
    INDEX idx_group_company (company_id),
    INDEX idx_group_parent (parent_group_id),
    INDEX idx_group_manager (group_manager_user_id),
    INDEX idx_group_status (status)
) ENGINE=InnoDB COMMENT='Regional or divisional groupings within companies';

-- ================================================================
-- TABLE 3: SITES
-- ================================================================
CREATE TABLE sites (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    company_id CHAR(36) NOT NULL,
    group_id CHAR(36) NOT NULL,
    
    -- Basic information
    site_code VARCHAR(50) NOT NULL COMMENT 'Human-readable site identifier',
    name VARCHAR(200) NOT NULL,
    description TEXT,
    
    -- Project information
    project_type ENUM('residential', 'commercial', 'industrial', 'infrastructure', 'renovation') NOT NULL,
    project_phase ENUM('planning', 'preparation', 'construction', 'finishing', 'completed', 'maintenance') DEFAULT 'planning',
    
    -- Location
    address TEXT NOT NULL,
    city VARCHAR(100) NOT NULL,
    state_province VARCHAR(100),
    country VARCHAR(100) NOT NULL,
    postal_code VARCHAR(20),
    
    -- Geographic coordinates
    latitude DECIMAL(10, 7),
    longitude DECIMAL(10, 7),
    elevation_meters DECIMAL(8, 2),
    
    -- Site boundaries (for map display)
    boundary_coordinates JSON COMMENT 'Polygon coordinates defining site boundaries',
    site_area_sqm DECIMAL(12, 2),
    
    -- Timeline
    planned_start_date DATE,
    planned_end_date DATE,
    actual_start_date DATE,
    actual_end_date DATE,
    
    -- Management  
    site_manager_user_id CHAR(36),
    site_coordinator_user_id CHAR(36),
    contractor_company VARCHAR(200),
    
    -- Safety and compliance
    safety_requirements JSON COMMENT 'Site-specific safety requirements',
    compliance_standards JSON COMMENT 'OSHA, local regulations, etc.',
    hazard_classifications JSON COMMENT 'Known hazards at the site',
    
    -- Budget and resources
    project_budget DECIMAL(15,2),
    allocated_budget DECIMAL(15,2),
    
    -- Contact and access
    site_phone VARCHAR(20),
    site_email VARCHAR(100),
    access_instructions TEXT,
    emergency_contact JSON,
    
    -- Configuration
    timezone VARCHAR(50) DEFAULT 'UTC',
    working_hours JSON COMMENT 'Standard working hours for the site',
    
    -- Status
    status ENUM('planning', 'active', 'suspended', 'completed', 'archived') DEFAULT 'planning',
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (company_id) REFERENCES companies(id) ON DELETE CASCADE,
    FOREIGN KEY (group_id) REFERENCES groups(id) ON DELETE CASCADE,
    UNIQUE KEY uk_site_code (company_id, site_code),
    INDEX idx_site_company (company_id),
    INDEX idx_site_group (group_id),
    INDEX idx_site_status (status),
    INDEX idx_site_project_type (project_type),
    INDEX idx_site_location (city, state_province, country),
    INDEX idx_site_coordinates (latitude, longitude),
    INDEX idx_site_manager (site_manager_user_id),
    INDEX idx_site_timeline (planned_start_date, planned_end_date)
) ENGINE=InnoDB COMMENT='Individual construction sites';