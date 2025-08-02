# **Construction Site AI Monitoring System - DDL Design Document**

**Version:** 1.0  
**Date:** January 2025  
**Database:** MySQL 8.0+  
**Total Tables:** 35 (12 VMS + 23 Construction Management)

## **📋 Quick Reference**

### **Database Architecture:**
- **VMS Database:** `construction_vms` (12 tables)
- **Construction Database:** `construction_management` (23 tables)
- **Communication:** REST APIs + Message Queue
- **Cross-DB References:** Application-level integrity

### **VMS/NVR System Tables (12)**
```
cameras, camera_manufacturers, camera_models, camera_configurations,
camera_api_endpoints, video_storage, video_encoders, recording_policies,
performance_metrics, system_configurations, audit_logs, api_access_logs
```

### **Construction Management System Tables (23)**
```
companies, groups, sites, users, roles, user_roles, user_sessions,
site_coordinates, site_zones, site_maps, ai_models, detection_results,
safety_violations, personnel_tracking, equipment_detections, confidence_metrics,
alert_rules, alerts, alert_escalations, notifications, assessment_routes,
mobile_recordings, field_reports, route_waypoints, security_patrol_routes,
patrol_camera_sequences, patrol_schedules, zone_actions, zone_external_data_sources,
zone_action_logs, compliance_reports, analytics_dashboards, external_systems,
api_webhooks, data_retention_policies
```

## **🚀 Quick Setup**

1. **Create Databases:**
   ```bash
   mysql -u root -p < database/setup/01_create_databases.sql
   ```

2. **Setup VMS Schema:**
   ```bash
   mysql -u root -p construction_vms < database/schemas/vms-schema.sql
   ```

3. **Setup Construction Schema:**
   ```bash
   mysql -u root -p construction_management < database/schemas/construction-schema.sql
   ```

4. **Create Indexes:**
   ```bash
   mysql -u root -p < database/setup/03_create_indexes.sql
   ```

5. **Load Sample Data:**
   ```bash
   mysql -u root -p < database/sample-data/sample-data.sql
   ```

## **📊 Key Design Decisions**

### **Separation Strategy:**
- **VMS System:** Handles pure video management (can be swapped with external VMS)
- **Construction System:** Business logic independent of video source
- **Integration:** REST APIs + WebSocket streams + Message Queue

### **Performance Optimizations:**
- **Partitioning:** Time-based partitioning for large tables (detection_results, alerts, logs)
- **Indexing:** Optimized for time-series queries and user access patterns
- **JSON Fields:** Flexible schema for varying configurations
- **Cross-DB:** Application-level foreign key integrity

### **Scalability Features:**
- **Modular Design:** Each system can scale independently
- **Pluggable Storage:** S3, disk mounts, NFS support
- **Multi-tenant:** Company-based data isolation
- **Archive Support:** Automated data lifecycle management

## **🔗 Critical Relationships**

### **User Hierarchy:**
```
Companies → Groups → Sites → Users → Roles
SYSADMIN → COMPANY EXEC → Group Site Manager → Site Manager → Site Coordinator
```

### **Detection Flow:**
```
VMS Cameras → Detection Results → Safety Violations → Alerts → Escalations → Notifications
```

### **Zone System:**
```
Sites → Site Zones → Zone Actions + External Data Sources → Action Logs
```

### **Field Assessment:**
```
Sites → Assessment Routes → Mobile Recordings → Field Reports
```

## **⚠️ Important Notes**

1. **Cross-Database References:** Camera IDs from VMS are referenced in Construction system but NOT as foreign keys
2. **JSON Schema Validation:** Implement application-level validation for JSON fields
3. **Partitioning Management:** Set up automated partition management for time-series tables
4. **Security:** All sensitive data should be encrypted at application level
5. **Performance:** Monitor and optimize indexes based on actual query patterns

## **📈 Monitoring & Maintenance**

### **Key Metrics to Monitor:**
- Table sizes and growth rates
- Query performance on time-series tables
- Partition utilization
- Cross-database query performance
- JSON field query efficiency

### **Maintenance Tasks:**
- Daily: Archive old detection results
- Weekly: Optimize tables and rebuild indexes
- Monthly: Review partition strategy and performance
- Quarterly: Update retention policies and cleanup archived data

---

For complete table definitions, see individual schema files in `/database/schemas/`