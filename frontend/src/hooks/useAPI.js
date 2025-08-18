/**
 * API Hooks
 * =========
 * 
 * Custom React hooks for API interactions with loading states and error handling
 */

import { useState, useEffect, useCallback } from 'react';
import { backendAPI, zoneminderAPI } from '../services';

// Generic API hook with loading and error states
export function useAPI(apiCall, dependencies = []) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchData = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const result = await apiCall();
      setData(result);
    } catch (err) {
      setError(err.message || 'An error occurred');
      console.error('API Error:', err);
    } finally {
      setLoading(false);
    }
  }, dependencies);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  return { data, loading, error, refetch: fetchData };
}

// Hook for ZoneMinder system status
export function useZoneminderStatus() {
  return useAPI(() => zoneminderAPI.system.getStatus());
}

// Hook for ZoneMinder cameras
export function useZoneminderCameras(siteId = null) {
  return useAPI(() => {
    const params = siteId ? { site_id: siteId } : {};
    return zoneminderAPI.cameras.getAll(params);
  }, [siteId]);
}

// Hook for ZoneMinder events with filtering
export function useZoneminderEvents(filters = {}) {
  return useAPI(() => zoneminderAPI.events.getAll(filters), [JSON.stringify(filters)]);
}

// Hook for ZoneMinder zones
export function useZoneminderZones(cameraId = null) {
  return useAPI(() => {
    const params = cameraId ? { camera_id: cameraId } : {};
    return zoneminderAPI.zones.getAll(params);
  }, [cameraId]);
}

// Hook for backend sites
export function useSites() {
  return useAPI(() => backendAPI.sites.getAll());
}

// Hook for backend users
export function useUsers() {
  return useAPI(() => backendAPI.users.getAll());
}

// Hook for dashboard stats
export function useDashboardStats() {
  return useAPI(() => backendAPI.core.getDashboardStats());
}

// Hook for AI detections
export function useAIDetections(params = {}) {
  return useAPI(() => backendAPI.aiDetection.getDetections(params), [JSON.stringify(params)]);
}

// Hook for analytics data
export function useAnalytics(type = 'kpi', params = {}) {
  return useAPI(() => {
    switch (type) {
      case 'kpi':
        return backendAPI.analytics.getKPIDashboard(params);
      case 'performance':
        return backendAPI.analytics.getPerformanceMetrics(params);
      case 'trends':
        return backendAPI.analytics.getTrendAnalysis(params);
      default:
        return backendAPI.analytics.getKPIDashboard(params);
    }
  }, [type, JSON.stringify(params)]);
}

// Hook for real-time data with polling
export function useRealTimeData(apiCall, interval = 30000, dependencies = []) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchData = useCallback(async () => {
    try {
      setError(null);
      const result = await apiCall();
      setData(result);
      setLoading(false);
    } catch (err) {
      setError(err.message || 'An error occurred');
      console.error('Real-time Data Error:', err);
    }
  }, dependencies);

  useEffect(() => {
    fetchData();
    const intervalId = setInterval(fetchData, interval);
    return () => clearInterval(intervalId);
  }, [fetchData, interval]);

  return { data, loading, error, refetch: fetchData };
}

// Hook for live camera data
export function useLiveCameraData(siteId = null, interval = 15000) {
  return useRealTimeData(
    () => zoneminderAPI.utils.getLiveCameras(siteId),
    interval,
    [siteId]
  );
}

// Hook for recent events
export function useRecentEvents(hours = 24, interval = 10000) {
  return useRealTimeData(
    () => zoneminderAPI.events.getRecent(hours),
    interval,
    [hours]
  );
}

// Hook for critical alerts
export function useCriticalAlerts(hours = 24, interval = 5000) {
  return useRealTimeData(
    () => zoneminderAPI.utils.getCriticalEvents(hours),
    interval,
    [hours]
  );
}