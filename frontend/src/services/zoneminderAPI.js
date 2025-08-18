/**
 * ZoneMinder API Service
 * ======================
 * 
 * Service layer for ZoneMinder integration APIs
 */

import { api } from './api';

export const zoneminderAPI = {
  // System Status and Health
  system: {
    getStatus: () => api.get('/zoneminder/status'),
    getHealth: () => api.get('/zoneminder/status'),
  },

  // Camera Management
  cameras: {
    getAll: (params = {}) => api.get('/zoneminder/cameras', params),
    getById: (cameraId) => api.get(`/zoneminder/cameras/${cameraId}`),
    create: (cameraData) => api.post('/zoneminder/cameras', cameraData),
    update: (cameraId, cameraData) => api.put(`/zoneminder/cameras/${cameraId}`, cameraData),
    delete: (cameraId) => api.delete(`/zoneminder/cameras/${cameraId}`),
    
    // Camera-specific operations
    getStatistics: (cameraId, startDate, endDate) => 
      api.get(`/zoneminder/cameras/${cameraId}/statistics`, { 
        start_date: startDate, 
        end_date: endDate 
      }),
  },

  // Stream Management
  streams: {
    getStreamInfo: (cameraId, quality = 'high') => 
      api.get(`/zoneminder/cameras/${cameraId}/stream`, { quality }),
    getSnapshot: (cameraId) => 
      api.get(`/zoneminder/cameras/${cameraId}/snapshot`),
    startRecording: (cameraId, duration) => 
      api.post(`/zoneminder/cameras/${cameraId}/recording/start`, { duration }),
    stopRecording: (cameraId, recordingId) => 
      api.post(`/zoneminder/cameras/${cameraId}/recording/stop`, { recordingId }),
  },

  // Detection Events
  events: {
    getAll: (params = {}) => api.get('/zoneminder/events', params),
    getById: (eventId) => api.get(`/zoneminder/events/${eventId}`),
    acknowledge: (eventId, userId) => 
      api.post(`/zoneminder/events/${eventId}/acknowledge`, { user_id: userId }),
    resolve: (eventId, userId, notes) => 
      api.post(`/zoneminder/events/${eventId}/resolve`, { 
        user_id: userId, 
        resolution_notes: notes 
      }),
    
    // Event filtering helpers
    getByCamera: (cameraId, params = {}) => 
      api.get('/zoneminder/events', { ...params, camera_id: cameraId }),
    getByType: (detectionType, params = {}) => 
      api.get('/zoneminder/events', { ...params, detection_type: detectionType }),
    getBySeverity: (severity, params = {}) => 
      api.get('/zoneminder/events', { ...params, severity }),
    getRecent: (hours = 24, params = {}) => {
      const endDate = new Date();
      const startDate = new Date(endDate.getTime() - (hours * 60 * 60 * 1000));
      return api.get('/zoneminder/events', { 
        ...params, 
        start_date: startDate.toISOString(),
        end_date: endDate.toISOString()
      });
    },
  },

  // Monitoring Zones
  zones: {
    getAll: (params = {}) => api.get('/zoneminder/zones', params),
    getById: (zoneId) => api.get(`/zoneminder/zones/${zoneId}`),
    create: (zoneData) => api.post('/zoneminder/zones', zoneData),
    update: (zoneId, zoneData) => api.put(`/zoneminder/zones/${zoneId}`, zoneData),
    delete: (zoneId) => api.delete(`/zoneminder/zones/${zoneId}`),
    
    // Zone filtering helpers
    getByCamera: (cameraId, params = {}) => 
      api.get('/zoneminder/zones', { ...params, camera_id: cameraId }),
    getByType: (zoneType, params = {}) => 
      api.get('/zoneminder/zones', { ...params, zone_type: zoneType }),
  },

  // Analytics and Insights
  analytics: {
    getSiteAnalytics: (siteId, startDate, endDate) => 
      api.get(`/zoneminder/sites/${siteId}/analytics`, { 
        start_date: startDate, 
        end_date: endDate 
      }),
    getCameraAnalytics: (cameraId, startDate, endDate) => 
      api.get(`/zoneminder/cameras/${cameraId}/statistics`, { 
        start_date: startDate, 
        end_date: endDate 
      }),
  },

  // Mock Data (Development Only)
  mock: {
    getStatistics: () => api.get('/zoneminder/mock/statistics'),
    getConfig: () => api.get('/zoneminder/mock/config'),
  },

  // Utility functions for common operations
  utils: {
    // Get live cameras with recent activity
    getLiveCameras: async (siteId = null) => {
      const params = siteId ? { site_id: siteId } : {};
      const cameras = await api.get('/zoneminder/cameras', params);
      return cameras.cameras?.filter(camera => camera.status === 'online') || [];
    },

    // Get recent critical events
    getCriticalEvents: async (hours = 24) => {
      const endDate = new Date();
      const startDate = new Date(endDate.getTime() - (hours * 60 * 60 * 1000));
      return api.get('/zoneminder/events', { 
        severity: 'critical',
        start_date: startDate.toISOString(),
        end_date: endDate.toISOString(),
        limit: 50
      });
    },

    // Get unacknowledged events
    getUnacknowledgedEvents: async (params = {}) => {
      const events = await api.get('/zoneminder/events', { ...params, limit: 100 });
      return events.events?.filter(event => !event.acknowledged) || [];
    },

    // Get construction safety events
    getSafetyEvents: async (params = {}) => {
      return api.get('/zoneminder/events', { 
        ...params, 
        detection_type: 'ppe_violation,safety_hazard',
        limit: 50
      });
    },

    // Get equipment operation events
    getEquipmentEvents: async (params = {}) => {
      return api.get('/zoneminder/events', { 
        ...params, 
        detection_type: 'equipment_operation',
        limit: 50
      });
    },

    // Get progress milestone events
    getProgressEvents: async (params = {}) => {
      return api.get('/zoneminder/events', { 
        ...params, 
        detection_type: 'progress_milestone',
        limit: 50
      });
    },

    // Stream quality options
    getStreamQualities: () => ['low', 'medium', 'high', 'ultra'],
    
    // Detection type options
    getDetectionTypes: () => [
      'ppe_violation',
      'restricted_access', 
      'equipment_operation',
      'personnel_count',
      'safety_hazard',
      'progress_milestone',
      'weather_alert'
    ],

    // Zone type options
    getZoneTypes: () => ['safety', 'progress', 'equipment', 'restricted'],

    // Severity levels
    getSeverityLevels: () => ['low', 'medium', 'high', 'critical'],
  },
};