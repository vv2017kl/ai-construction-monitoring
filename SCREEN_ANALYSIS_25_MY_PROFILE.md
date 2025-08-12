# 👤 **Screen Analysis #25: My Profile**

## **📋 Basic Information**
- **Screen Name**: My Profile
- **Route**: `/my-profile`
- **Component**: `MyProfile.js` (needs full implementation)
- **Portal**: Solution User
- **Analysis Date**: 2025-01-12
- **Priority**: TIER 6 (Final User Experience) - User Interface Completion

## **🎯 Functional Requirements**

### **Core Functionality**
1. **User Profile Management**
   - Personal information editing and updates
   - Professional details and contact information
   - Avatar/profile picture management
   - Preference settings and customization

2. **Security Settings**
   - Password change and management
   - Two-factor authentication setup
   - Session management and device tracking
   - Security audit log viewing

3. **Notification Preferences**
   - Email notification settings
   - SMS alert preferences
   - In-app notification configuration
   - Alert priority and frequency settings

4. **Dashboard Customization**
   - Dashboard layout preferences
   - Widget selection and arrangement
   - Theme and appearance settings
   - Default view configurations

## **🗄️ Database Schema Requirements**

### **New Tables**

#### **user_profile_settings**
```sql
id: UUID (Primary Key)
user_id: UUID (Foreign Key → users.id) UNIQUE
profile_picture_url: VARCHAR(500)
bio: TEXT
preferences: JSON -- User preferences
notification_settings: JSON -- Notification preferences
dashboard_config: JSON -- Dashboard customization
theme_settings: JSON -- Theme and appearance
privacy_settings: JSON -- Privacy configuration

created_at: TIMESTAMP DEFAULT CURRENT_TIMESTAMP
updated_at: TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
```

### **Enhanced Existing Tables**

#### **users** (Additional Profile Fields)
```sql
-- Profile enhancements
middle_name: VARCHAR(100)
preferred_name: VARCHAR(100)
pronouns: VARCHAR(50)
bio: TEXT
profile_completed: BOOLEAN DEFAULT FALSE
last_profile_update: TIMESTAMP
```

## **🔗 Backend API Requirements**

### **Profile Management**
```
# Profile Operations
GET /api/users/profile - Get current user profile
PUT /api/users/profile - Update profile information
POST /api/users/profile/avatar - Upload profile picture
DELETE /api/users/profile/avatar - Remove profile picture

# Security Settings
PUT /api/users/security/password - Change password
POST /api/users/security/mfa/enable - Enable 2FA
POST /api/users/security/mfa/disable - Disable 2FA
GET /api/users/security/sessions - Get active sessions
DELETE /api/users/security/sessions/{id} - Terminate session

# Preferences
PUT /api/users/preferences/notifications - Update notification preferences
PUT /api/users/preferences/dashboard - Update dashboard settings
PUT /api/users/preferences/theme - Update theme settings
```

## **🎉 Summary**

The **My Profile** screen provides comprehensive user profile management, enabling users to manage personal information, security settings, notification preferences, and dashboard customization.

**Key Features**: Profile editing, security management, notification preferences, dashboard customization.

**Database Impact**: **1 new table** added for user profile settings.