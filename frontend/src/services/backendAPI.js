/**
 * Backend API Service
 * ===================
 * 
 * Service layer for core backend database APIs
 */

import { api } from './api';

export const backendAPI = {
  // Core APIs
  core: {
    getHealth: () => api.get('/'),
    getStatus: () => api.get('/status'),
    getDashboardStats: () => api.get('/dashboard/stats'),
  },

  // Sites Management
  sites: {
    getAll: (params = {}) => api.get('/sites', params),
    getById: (siteId) => api.get(`/sites/${siteId}`),
    create: (siteData) => api.post('/sites', siteData),
    update: (siteId, siteData) => api.put(`/sites/${siteId}`, siteData),
    delete: (siteId) => api.delete(`/sites/${siteId}`),
    getZones: (siteId) => api.get(`/sites/${siteId}/zones`),
    getCameras: (siteId) => api.get(`/sites/${siteId}/cameras`),
    getAlerts: (siteId) => api.get(`/sites/${siteId}/alerts`),
    getPersonnel: (siteId) => api.get(`/sites/${siteId}/personnel`),
  },

  // Users Management
  users: {
    getAll: (params = {}) => api.get('/users', params),
    getById: (userId) => api.get(`/users/${userId}`),
    create: (userData) => api.post('/users', userData),
    update: (userId, userData) => api.put(`/users/${userId}`, userData),
    delete: (userId) => api.delete(`/users/${userId}`),
  },

  // Cameras Management
  cameras: {
    getAll: (params = {}) => api.get('/cameras', params),
    getById: (cameraId) => api.get(`/cameras/${cameraId}`),
    create: (cameraData) => api.post('/cameras', cameraData),
    update: (cameraId, cameraData) => api.put(`/cameras/${cameraId}`, cameraData),
    delete: (cameraId) => api.delete(`/cameras/${cameraId}`),
  },

  // Alerts Management
  alerts: {
    getAll: (params = {}) => api.get('/alerts', params),
    getById: (alertId) => api.get(`/alerts/${alertId}`),
    create: (alertData) => api.post('/alerts', alertData),
    update: (alertId, alertData) => api.put(`/alerts/${alertId}`, alertData),
    delete: (alertId) => api.delete(`/alerts/${alertId}`),
    acknowledge: (alertId, userId) => api.post(`/alerts/${alertId}/acknowledge`, { user_id: userId }),
    resolve: (alertId, resolution) => api.post(`/alerts/${alertId}/resolve`, resolution),
  },

  // AI Detection APIs
  aiDetection: {
    getDetections: (params = {}) => api.get('/ai-detections', params),
    getById: (detectionId) => api.get(`/ai-detections/${detectionId}`),
    getAnalytics: (params = {}) => api.get('/ai-detections/analytics', params),
    getCameraPerformance: (params = {}) => api.get('/ai-detections/camera-performance', params),
  },

  // Analytics APIs
  analytics: {
    getCertifications: (params = {}) => api.get('/analytics/certifications', params),
    getPerformanceMetrics: (params = {}) => api.get('/analytics/performance-metrics', params),
    getTrendAnalysis: (params = {}) => api.get('/analytics/trend-analysis', params),
    getReportTemplates: (params = {}) => api.get('/analytics/report-templates', params),
    getDashboardWidgets: (params = {}) => api.get('/analytics/dashboard-widgets', params),
    getKPIDashboard: (params = {}) => api.get('/analytics/kpi-dashboard', params),
    getComplianceSummary: (params = {}) => api.get('/analytics/compliance-summary', params),
  },

  // Field Operations APIs
  fieldOperations: {
    getInspectionPaths: (params = {}) => api.get('/field-operations/inspection-paths', params),
    getPathWaypoints: (params = {}) => api.get('/field-operations/path-waypoints', params),
    getPathExecutions: (params = {}) => api.get('/field-operations/path-executions', params),
    getPathTemplates: (params = {}) => api.get('/field-operations/path-templates', params),
    getAnalytics: (params = {}) => api.get('/field-operations/analytics', params),
  },

  // Navigation APIs
  navigation: {
    getRoutes: (params = {}) => api.get('/navigation/routes', params),
    getWaypoints: (params = {}) => api.get('/navigation/waypoints', params),
    getSessions: (params = {}) => api.get('/navigation/sessions', params),
    getStreetViewCameras: (params = {}) => api.get('/navigation/street-view-cameras', params),
    getRouteAnalytics: (params = {}) => api.get('/navigation/route-analytics', params),
    getSessionAnalytics: (params = {}) => api.get('/navigation/session-analytics', params),
  },

  // Admin APIs
  admin: {
    getDashboardMetrics: (params = {}) => api.get('/admin/dashboard-metrics', params),
    getCurrentMetrics: (params = {}) => api.get('/admin/current-metrics', params),
    getSitePerformance: (params = {}) => api.get('/admin/site-performance', params),
    getSystemHealth: (params = {}) => api.get('/admin/system-health', params),
    getActivityLogs: (params = {}) => api.get('/admin/activity-logs', params),
    getSystemOverview: (params = {}) => api.get('/admin/system-overview', params),
  },

  // User Management APIs
  userManagement: {
    getProfiles: (params = {}) => api.get('/user-management/profiles', params),
    getRoleAssignments: (params = {}) => api.get('/user-management/role-assignments', params),
    getSessionManagement: (params = {}) => api.get('/user-management/session-management', params),
    getActivityTracking: (params = {}) => api.get('/user-management/activity-tracking', params),
    getPermissionsMatrix: (params = {}) => api.get('/user-management/permissions-matrix', params),
  },

  // Access Control APIs
  accessControl: {
    getRoles: (params = {}) => api.get('/access-control/roles', params),
    getPermissions: (params = {}) => api.get('/access-control/permissions', params),
    getRolePermissions: (params = {}) => api.get('/access-control/role-permissions', params),
    getSecurityPolicies: (params = {}) => api.get('/access-control/security-policies', params),
    getAuditLogs: (params = {}) => api.get('/access-control/audit-logs', params),
  },

  // AI Models APIs
  aiModels: {
    getModels: (params = {}) => api.get('/ai-models/models', params),
    getDeployments: (params = {}) => api.get('/ai-models/deployments', params),
    getPerformanceMetrics: (params = {}) => api.get('/ai-models/performance-metrics', params),
    getTrainingJobs: (params = {}) => api.get('/ai-models/training-jobs', params),
    getEvaluationResults: (params = {}) => api.get('/ai-models/evaluation-results', params),
  },

  // System Monitoring APIs
  systemMonitoring: {
    getSystemMetrics: (params = {}) => api.get('/system-monitoring/system-metrics', params),
    getPerformanceLogs: (params = {}) => api.get('/system-monitoring/performance-logs', params),
    getResourceUsage: (params = {}) => api.get('/system-monitoring/resource-usage', params),
    getAlertConfigurations: (params = {}) => api.get('/system-monitoring/alert-configurations', params),
    getHealthChecks: (params = {}) => api.get('/system-monitoring/health-checks', params),
  },
};