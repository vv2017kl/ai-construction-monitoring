# 👥 **Screen Analysis #19: User Directory**

## **📋 Basic Information**
- **Screen Name**: User Directory
- **Route**: `/admin/users`
- **Component**: `UserDirectory.js`
- **Portal**: Solution Admin
- **Analysis Date**: 2025-01-12
- **Priority**: TIER 5 (Specialized Priority) - Admin Portal Functions

## **🎯 Functional Requirements**

### **Core Functionality**
1. **User Management System**
   - Create, edit, delete, and manage user accounts
   - Role-based access control and permissions management
   - Multi-site user assignment and access control
   - User status management (active, suspended, inactive)

2. **User Directory Interface**
   - Comprehensive user listing with search and filtering
   - Table and card view modes for different use cases
   - Advanced filtering by role, site, status, and department
   - Real-time online status tracking

3. **User Profile Management**
   - Personal information management
   - Contact details and location tracking
   - Safety scores and assessment history
   - Login activity and usage analytics

4. **Administrative Controls**
   - Bulk user operations and management
   - User import/export functionality
   - Permission assignment and role management
   - Activity monitoring and audit trails

5. **Security & Access Management**
   - Multi-level authentication and authorization
   - Site-specific access permissions
   - Department-based role assignments
   - Session management and security monitoring

### **User Management Categories**
1. **Field Personnel**
   - Field workers, equipment operators
   - Site supervisors and team leads
   - Safety inspectors and compliance officers
   - Quality control and assessment specialists

2. **Administrative Users**
   - Project managers and executives
   - System administrators and IT staff
   - HR and compliance personnel
   - External contractors and consultants

3. **Multi-Site Managers**
   - Cross-site access permissions
   - Elevated reporting capabilities
   - System-wide oversight functions
   - Executive dashboard access

## **🗄️ Database Schema Requirements**

### **New Tables**

#### **user_management_profiles**
```sql
id: UUID (Primary Key)
user_id: UUID (Foreign Key → users.id)

-- Extended profile information
employee_number: VARCHAR(50) UNIQUE
badge_number: VARCHAR(50) UNIQUE
social_security_number: VARCHAR(20) -- Encrypted
date_of_birth: DATE
gender: ENUM('male', 'female', 'other', 'prefer_not_to_say')
nationality: VARCHAR(100)

-- Address and contact
home_address: TEXT
home_city: VARCHAR(100)
home_state: VARCHAR(100)
home_zip_code: VARCHAR(20)
home_country: VARCHAR(100)
emergency_contact_name: VARCHAR(255)
emergency_contact_phone: VARCHAR(20)
emergency_contact_relationship: VARCHAR(100)

-- Professional details
position_title: VARCHAR(255)
position_level: ENUM('entry', 'junior', mid', 'senior', 'lead', 'supervisor', 'manager', 'director', 'executive')
pay_grade: VARCHAR(50)
reports_to_user_id: UUID -- Reference to supervisor
direct_reports_count: INTEGER DEFAULT 0

-- Employment information
employment_type: ENUM('full_time', 'part_time', 'contract', 'temporary', 'consultant', 'intern')
employment_status: ENUM('active', 'on_leave', 'terminated', 'retired', 'suspended')
start_date: DATE NOT NULL
end_date: DATE
probation_end_date: DATE
performance_review_due: DATE

-- Skills and qualifications
skills: JSON -- Array of skills
qualifications: JSON -- Professional qualifications
languages: JSON -- Languages spoken
special_certifications: JSON -- Special certifications beyond basic

-- Preferences and settings
notification_preferences: JSON -- Communication preferences
ui_theme: VARCHAR(50) DEFAULT 'default'
timezone: VARCHAR(100)
language_preference: VARCHAR(10) DEFAULT 'en'

-- Privacy and compliance
privacy_settings: JSON -- Privacy preferences
gdpr_consent: BOOLEAN DEFAULT FALSE
marketing_consent: BOOLEAN DEFAULT FALSE
data_retention_consent: BOOLEAN DEFAULT TRUE

created_at: TIMESTAMP DEFAULT CURRENT_TIMESTAMP
updated_at: TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
```

#### **user_role_assignments**
```sql
id: UUID (Primary Key)
user_id: UUID (Foreign Key → users.id)
role_type: ENUM('system_role', 'site_role', 'department_role', 'project_role', 'temporary_role')
role_name: VARCHAR(255) NOT NULL
role_description: TEXT

-- Assignment scope
site_id: UUID -- Site-specific role assignment
department_id: UUID -- Department-specific role assignment
project_id: UUID -- Project-specific role assignment

-- Permission details
permissions: JSON -- Detailed permissions array
access_level: ENUM('read', 'write', 'admin', 'super_admin') DEFAULT 'read'
resource_restrictions: JSON -- Restricted resources
time_restrictions: JSON -- Time-based access restrictions

-- Assignment metadata
assigned_by: UUID (Foreign Key → users.id)
assigned_at: TIMESTAMP DEFAULT CURRENT_TIMESTAMP
effective_from: DATE NOT NULL
effective_until: DATE
is_primary_role: BOOLEAN DEFAULT FALSE

-- Approval workflow
requires_approval: BOOLEAN DEFAULT FALSE
approved_by: UUID -- Reference to approving manager
approved_at: TIMESTAMP
approval_notes: TEXT

-- Status and monitoring
assignment_status: ENUM('pending', 'active', 'suspended', 'expired', 'revoked') DEFAULT 'pending'
last_used: TIMESTAMP
usage_count: INTEGER DEFAULT 0

-- Audit trail
revoked_by: UUID -- Who revoked the assignment
revoked_at: TIMESTAMP
revocation_reason: TEXT

created_at: TIMESTAMP DEFAULT CURRENT_TIMESTAMP
updated_at: TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
```

#### **user_session_management**
```sql
id: UUID (Primary Key)
user_id: UUID (Foreign Key → users.id)
session_id: VARCHAR(255) UNIQUE NOT NULL
session_token: VARCHAR(512) UNIQUE NOT NULL

-- Session details
login_timestamp: TIMESTAMP DEFAULT CURRENT_TIMESTAMP
logout_timestamp: TIMESTAMP
last_activity: TIMESTAMP DEFAULT CURRENT_TIMESTAMP
session_duration_seconds: INTEGER
is_active: BOOLEAN DEFAULT TRUE

-- Client information
ip_address: INET NOT NULL
user_agent: TEXT
browser_info: JSON -- Browser details
device_info: JSON -- Device information
operating_system: VARCHAR(100)

-- Location and access
login_location: POINT -- GPS coordinates if available
access_method: ENUM('web', 'mobile_app', 'api', 'sso', 'ldap') DEFAULT 'web'
authentication_method: ENUM('password', 'sso', 'mfa', 'biometric', 'certificate') DEFAULT 'password'

-- Security context
mfa_verified: BOOLEAN DEFAULT FALSE
risk_score: DECIMAL(3,1) -- 0-10 security risk assessment
suspicious_activity: BOOLEAN DEFAULT FALSE
concurrent_sessions: INTEGER DEFAULT 1

-- Session management
force_logout: BOOLEAN DEFAULT FALSE
session_timeout_minutes: INTEGER DEFAULT 480 -- 8 hours default
remember_me: BOOLEAN DEFAULT FALSE
auto_logout_at: TIMESTAMP

-- Activity tracking
page_views: INTEGER DEFAULT 0
api_calls: INTEGER DEFAULT 0
downloads: INTEGER DEFAULT 0
uploads: INTEGER DEFAULT 0

-- Compliance and audit
compliance_acknowledgment: BOOLEAN DEFAULT FALSE
terms_accepted_version: VARCHAR(20)
privacy_policy_accepted: BOOLEAN DEFAULT FALSE

created_at: TIMESTAMP DEFAULT CURRENT_TIMESTAMP
updated_at: TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
```

#### **user_activity_tracking**
```sql
id: UUID (Primary Key)
user_id: UUID (Foreign Key → users.id)
session_id: UUID (Foreign Key → user_session_management.id)

-- Activity details
activity_type: ENUM('login', 'logout', 'page_view', 'api_call', 'data_access', 'configuration_change', 'user_management', 'report_generation', 'alert_action') NOT NULL
activity_description: TEXT NOT NULL
activity_category: VARCHAR(100) -- High-level category

-- Context information
resource_type: VARCHAR(100) -- Type of resource accessed
resource_id: UUID -- Specific resource accessed
resource_name: VARCHAR(255) -- Human-readable resource name
site_id: UUID -- Site context

-- Request details
request_method: VARCHAR(10) -- GET, POST, PUT, DELETE
request_url: TEXT
request_payload: JSON -- Request data (sensitive data excluded)
response_status: INTEGER -- HTTP status code
response_time_ms: INTEGER

-- Geolocation and timing
activity_timestamp: TIMESTAMP DEFAULT CURRENT_TIMESTAMP
location_coordinates: POINT
location_accuracy: DECIMAL(8,2) -- GPS accuracy in meters
timezone_offset: INTEGER -- Minutes from UTC

-- Security and compliance
security_level: ENUM('public', 'internal', 'confidential', 'restricted') DEFAULT 'internal'
data_classification: VARCHAR(100) -- Data sensitivity classification
requires_audit: BOOLEAN DEFAULT TRUE
compliance_tags: JSON -- Compliance framework tags

-- Performance metrics
processing_time_ms: INTEGER
database_queries: INTEGER DEFAULT 0
cache_hits: INTEGER DEFAULT 0
errors_count: INTEGER DEFAULT 0

-- User behavior analysis
is_automated: BOOLEAN DEFAULT FALSE -- Automated vs manual activity
pattern_anomaly: BOOLEAN DEFAULT FALSE -- Unusual pattern detected
risk_indicator: DECIMAL(3,1) -- Risk score for this activity

created_at: TIMESTAMP DEFAULT CURRENT_TIMESTAMP
```

#### **user_permissions_matrix**
```sql
id: UUID (Primary Key)
user_id: UUID (Foreign Key → users.id)
permission_category: VARCHAR(100) NOT NULL -- Category of permission
permission_name: VARCHAR(255) NOT NULL -- Specific permission name

-- Permission scope
scope_type: ENUM('global', 'site', 'department', 'project', 'resource') NOT NULL
scope_id: UUID -- ID of the scope (site_id, department_id, etc.)
scope_name: VARCHAR(255) -- Human-readable scope name

-- Access details
access_level: ENUM('none', 'read', 'write', 'admin', 'owner') NOT NULL
can_delegate: BOOLEAN DEFAULT FALSE -- Can grant this permission to others
can_revoke: BOOLEAN DEFAULT FALSE -- Can revoke this permission from others

-- Conditions and restrictions
conditions: JSON -- Conditional access rules
time_restrictions: JSON -- Time-based limitations
location_restrictions: JSON -- Geographic limitations
device_restrictions: JSON -- Device/platform restrictions

-- Grant information
granted_by: UUID (Foreign Key → users.id)
granted_at: TIMESTAMP DEFAULT CURRENT_TIMESTAMP
granted_reason: TEXT
approval_required: BOOLEAN DEFAULT FALSE
approved_by: UUID -- Reference to approving authority

-- Status and lifecycle
status: ENUM('pending', 'active', 'suspended', 'expired', 'revoked') DEFAULT 'pending'
effective_from: TIMESTAMP DEFAULT CURRENT_TIMESTAMP
effective_until: TIMESTAMP
auto_renewal: BOOLEAN DEFAULT FALSE
renewal_period_days: INTEGER

-- Usage tracking
first_used: TIMESTAMP
last_used: TIMESTAMP
usage_count: INTEGER DEFAULT 0
abuse_reports: INTEGER DEFAULT 0

-- Audit and compliance
audit_required: BOOLEAN DEFAULT TRUE
compliance_notes: TEXT
last_reviewed: DATE
next_review_due: DATE
reviewer_user_id: UUID

created_at: TIMESTAMP DEFAULT CURRENT_TIMESTAMP
updated_at: TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
```

### **Enhanced Existing Tables**

#### **users** (Additional Admin Fields)
```sql
-- Enhanced authentication
password_last_changed: TIMESTAMP
password_expiry_date: TIMESTAMP
failed_login_count: INTEGER DEFAULT 0
account_locked_until: TIMESTAMP
mfa_enabled: BOOLEAN DEFAULT FALSE
mfa_secret: VARCHAR(255) -- Encrypted MFA secret

-- Profile enhancements
middle_name: VARCHAR(100)
preferred_name: VARCHAR(100)
pronouns: VARCHAR(50)
profile_picture_url: VARCHAR(500)
bio: TEXT

-- Administrative metadata
created_by: UUID -- Who created this user account
last_modified_by: UUID -- Who last modified the account
account_type: ENUM('regular', 'admin', 'service', 'guest') DEFAULT 'regular'
source_system: VARCHAR(100) -- Where the account originated
external_id: VARCHAR(255) -- ID in external system

-- Compliance and legal
gdpr_consent_date: TIMESTAMP
terms_accepted_date: TIMESTAMP
privacy_policy_accepted_date: TIMESTAMP
background_check_completed: BOOLEAN DEFAULT FALSE
background_check_date: DATE
```

## **📹 ZoneMinder Integration Requirements**

### **User Access Control**
1. **Camera Access Management**
   - User-specific camera permissions
   - Site-based access restrictions
   - Time-based viewing limitations
   - Recording access controls

2. **Activity Monitoring**
   - User video access logging
   - Viewing session tracking
   - Download/export permissions
   - Evidence handling compliance

3. **Administrative Controls**
   - Bulk camera permission management
   - User access analytics
   - Security monitoring
   - Audit trail maintenance

### **ZoneMinder API Endpoints**
```
GET /api/zm/users/{user_id}/camera-permissions - User camera access
POST /api/zm/users/{user_id}/grant-access - Grant camera access
DELETE /api/zm/users/{user_id}/revoke-access - Revoke camera access
GET /api/zm/admin/user-activity-logs - User video access logs
```

## **🤖 AI Integration Requirements (Roboflow)**

### **User Behavior Analytics**
1. **Access Pattern Analysis**
   - Unusual login pattern detection
   - Anomalous activity identification
   - Security risk assessment
   - Behavioral profiling

2. **Permission Optimization**
   - Optimal permission set recommendations
   - Role mining and optimization
   - Access pattern analysis
   - Compliance gap identification

3. **Administrative Intelligence**
   - User productivity analytics
   - Performance correlation analysis
   - Training needs identification
   - Resource utilization optimization

### **AI Model Configuration**
```yaml
user_analytics:
  behavior_analysis:
    type: "anomaly_detection"
    input: ["login_patterns", "activity_logs", "access_patterns"]
    confidence_threshold: 0.80
    
  permission_optimization:
    type: "recommendation_engine"
    input: ["user_roles", "access_patterns", "resource_usage"]
    confidence_threshold: 0.85
    
  security_risk:
    type: "risk_assessment"
    input: ["user_activity", "security_events", "compliance_data"]
    confidence_threshold: 0.75
```

## **🔗 Backend API Requirements**

### **User Management**
```
# User CRUD Operations
GET /api/admin/users - List all users with filtering and pagination
POST /api/admin/users - Create new user account
GET /api/admin/users/{id} - Get user details and profile
PUT /api/admin/users/{id} - Update user information
DELETE /api/admin/users/{id} - Deactivate user account
POST /api/admin/users/{id}/activate - Reactivate user account

# User Status Management
PUT /api/admin/users/{id}/status - Update user status
POST /api/admin/users/{id}/suspend - Suspend user account
POST /api/admin/users/{id}/unsuspend - Unsuspend user account
POST /api/admin/users/{id}/reset-password - Reset user password

# Bulk Operations
POST /api/admin/users/bulk-create - Bulk user creation
PUT /api/admin/users/bulk-update - Bulk user updates
POST /api/admin/users/bulk-status-change - Bulk status changes
DELETE /api/admin/users/bulk-deactivate - Bulk deactivation
```

### **Role & Permission Management**
```
# Role Management
GET /api/admin/roles - List available roles
POST /api/admin/users/{id}/roles - Assign role to user
DELETE /api/admin/users/{id}/roles/{role_id} - Remove role from user
GET /api/admin/users/{id}/permissions - Get user permissions
POST /api/admin/users/{id}/permissions - Grant specific permissions
DELETE /api/admin/users/{id}/permissions/{permission_id} - Revoke permission

# Permission Analytics
GET /api/admin/permissions/matrix - Permission matrix overview
GET /api/admin/permissions/conflicts - Identify permission conflicts
GET /api/admin/permissions/optimization - Permission optimization suggestions
```

### **Session & Activity Management**
```
# Session Management
GET /api/admin/users/{id}/sessions - List active user sessions
DELETE /api/admin/users/{id}/sessions/{session_id} - Terminate session
POST /api/admin/users/{id}/force-logout - Force logout all sessions
GET /api/admin/sessions/overview - System-wide session overview

# Activity Tracking
GET /api/admin/users/{id}/activity - User activity history
GET /api/admin/activity/summary - System activity summary
GET /api/admin/activity/suspicious - Suspicious activity alerts
POST /api/admin/activity/analyze - Analyze activity patterns
```

### **Import & Export**
```
POST /api/admin/users/import - Import users from CSV/Excel
GET /api/admin/users/export - Export user directory
POST /api/admin/users/sync-ldap - Sync with LDAP/AD
GET /api/admin/users/compliance-report - Generate compliance report
```

## **🎨 UI/UX Requirements**

### **User Management Interface**
1. **Directory Views**
   - Table view with sortable columns
   - Card view for visual overview
   - Advanced filtering capabilities
   - Real-time search functionality

2. **User Profile Management**
   - Comprehensive profile editing
   - Permission visualization
   - Activity timeline display
   - Security status indicators

3. **Bulk Operations**
   - Multi-select functionality
   - Bulk action confirmations
   - Progress indicators
   - Error handling and reporting

4. **Administrative Controls**
   - Role assignment interface
   - Permission matrix display
   - Security monitoring dashboard
   - Audit trail visualization

### **Responsive Design**
- Mobile-friendly user management
- Touch-optimized interactions
- Responsive table layouts
- Mobile-specific bulk operations

## **⚡ Performance Considerations**

### **Large User Base Handling**
1. **Pagination & Search**
   - Efficient pagination strategies
   - Server-side search implementation
   - Indexed database queries
   - Caching for frequent searches

2. **Permission Calculations**
   - Cached permission matrices
   - Efficient role resolution
   - Background permission sync
   - Optimized access control checks

### **Real-time Features**
- WebSocket connections for online status
- Live activity feed updates
- Real-time security alerts
- Session status monitoring

## **🔒 Security & Access Control**

### **Administrative Security**
1. **Multi-Level Authentication**
   - MFA requirement for admin functions
   - Session timeout management
   - IP-based access restrictions
   - Audit trail maintenance

2. **Data Protection**
   - Encrypted sensitive information
   - GDPR compliance features
   - Data retention policies
   - Secure password handling

### **Privacy & Compliance**
- User consent management
- Data export capabilities
- Right to deletion support
- Compliance reporting tools

## **🧪 Testing Requirements**

### **Functional Testing**
1. **User Management Operations**
   - User creation and editing
   - Role assignment functionality
   - Permission management
   - Status change workflows

2. **Security Testing**
   - Authentication mechanisms
   - Authorization controls
   - Session management
   - Data protection measures

### **Performance Testing**
- Large user dataset handling
- Concurrent admin operations
- Search and filter performance
- Bulk operation efficiency

## **📊 Success Metrics**

### **Administrative Efficiency**
- User onboarding time reduction
- Permission management accuracy
- Security incident response time
- Compliance audit success rate

### **System Performance**
- User directory load times
- Search operation response times
- Permission resolution speed
- Session management efficiency

---

## **🎉 Summary**

The **User Directory** screen provides comprehensive user management capabilities for administrators, enabling them to:

- **Manage user accounts** with full CRUD operations, status management, and profile administration
- **Control access permissions** through role-based assignments, permission matrices, and security management
- **Monitor user activity** with session tracking, behavior analysis, and security monitoring
- **Ensure compliance** through audit trails, data protection, and regulatory reporting

**Key Features**: Advanced filtering and search, role-based access control, real-time activity monitoring, bulk operations, security management, and comprehensive audit trails.

**Database Impact**: **5 new tables** added to support user management profiles, role assignments, session management, activity tracking, and permission matrices.

**Integration Requirements**: ZoneMinder integration for camera access control and Roboflow AI integration for user behavior analytics and security monitoring.

This analysis provides the complete foundation for implementing a robust user directory system with comprehensive administrative capabilities and enterprise-grade security features.