import React from 'react';
import { X, AlertTriangle, Shield, Eye, MapPin, Calendar, Users, Camera } from 'lucide-react';

const AlertSummaryPanel = ({ 
  site = null, 
  cameras = [], 
  visible = false, 
  onClose, 
  onViewSite, 
  onViewCamera,
  className = ''
}) => {
  if (!visible || !site) return null;

  const { alert_summary, site_stats } = site;
  const totalAlerts = (alert_summary?.critical || 0) + (alert_summary?.high || 0) + (alert_summary?.medium || 0) + (alert_summary?.low || 0);

  // Get cameras with active alerts
  const camerasWithAlerts = cameras.filter(camera => camera.alerts?.active > 0);

  const getAlertPriorityColor = (priority) => {
    switch (priority) {
      case 'critical': return 'text-red-600 bg-red-50';
      case 'high': return 'text-orange-600 bg-orange-50';
      case 'medium': return 'text-yellow-600 bg-yellow-50';
      case 'low': return 'text-blue-600 bg-blue-50';
      default: return 'text-gray-600 bg-gray-50';
    }
  };

  const getCameraStatusColor = (status) => {
    switch (status) {
      case 'critical': return 'text-red-500';
      case 'warning': return 'text-orange-500';
      case 'maintenance': return 'text-yellow-500';
      case 'normal': return 'text-green-500';
      default: return 'text-gray-500';
    }
  };

  const formatTimestamp = (timestamp) => {
    return new Date(timestamp).toLocaleString('en-US', {
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  return (
    <div className={`absolute top-4 right-4 w-96 bg-white rounded-lg shadow-xl border border-gray-200 z-20 ${className}`}>
      {/* Header */}
      <div className="flex items-center justify-between p-4 border-b border-gray-200">
        <div>
          <h3 className="text-lg font-semibold text-gray-900">{site.name}</h3>
          <p className="text-sm text-gray-500">{site.code} • {site.city}, {site.country}</p>
        </div>
        <button
          onClick={onClose}
          className="p-1 hover:bg-gray-100 rounded-md transition-colors"
        >
          <X className="w-5 h-5 text-gray-500" />
        </button>
      </div>

      {/* Site Status Overview */}
      <div className="p-4 border-b border-gray-200">
        <div className="grid grid-cols-2 gap-4">
          <div className="text-center">
            <div className="text-2xl font-bold text-gray-900">{totalAlerts}</div>
            <div className="text-sm text-gray-500">Total Alerts</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-gray-900">{site_stats?.active_cameras || 0}</div>
            <div className="text-sm text-gray-500">Active Cameras</div>
          </div>
        </div>
      </div>

      {/* Alert Summary */}
      <div className="p-4 border-b border-gray-200">
        <h4 className="flex items-center text-sm font-medium text-gray-900 mb-3">
          <AlertTriangle className="w-4 h-4 mr-2" />
          Alert Summary
        </h4>
        <div className="space-y-2">
          {[
            { level: 'critical', count: alert_summary?.critical || 0, label: 'Critical', icon: '🔴' },
            { level: 'high', count: alert_summary?.high || 0, label: 'High', icon: '🟠' },
            { level: 'medium', count: alert_summary?.medium || 0, label: 'Medium', icon: '🟡' },
            { level: 'low', count: alert_summary?.low || 0, label: 'Low', icon: '🔵' }
          ].map(({ level, count, label, icon }) => (
            <div key={level} className={`flex items-center justify-between px-3 py-2 rounded-md ${getAlertPriorityColor(level)}`}>
              <div className="flex items-center space-x-2">
                <span>{icon}</span>
                <span className="text-sm font-medium">{label}</span>
              </div>
              <span className="text-sm font-bold">{count}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Site Statistics */}
      <div className="p-4 border-b border-gray-200">
        <h4 className="flex items-center text-sm font-medium text-gray-900 mb-3">
          <Shield className="w-4 h-4 mr-2" />
          Site Statistics
        </h4>
        <div className="grid grid-cols-2 gap-4 text-sm">
          <div className="flex items-center space-x-2">
            <Users className="w-4 h-4 text-gray-500" />
            <span className="text-gray-600">Personnel:</span>
            <span className="font-medium">{site_stats?.personnel_count || 0}</span>
          </div>
          <div className="flex items-center space-x-2">
            <Camera className="w-4 h-4 text-gray-500" />
            <span className="text-gray-600">Cameras:</span>
            <span className="font-medium">{site_stats?.active_cameras || 0}/{site_stats?.total_cameras || 0}</span>
          </div>
          <div className="flex items-center space-x-2">
            <MapPin className="w-4 h-4 text-gray-500" />
            <span className="text-gray-600">Project:</span>
            <span className="font-medium capitalize">{site.project_type}</span>
          </div>
          <div className="flex items-center space-x-2">
            <Calendar className="w-4 h-4 text-gray-500" />
            <span className="text-gray-600">Phase:</span>
            <span className="font-medium capitalize">{site.project_phase}</span>
          </div>
        </div>
      </div>

      {/* Cameras with Alerts */}
      {camerasWithAlerts.length > 0 && (
        <div className="p-4 border-b border-gray-200">
          <h4 className="flex items-center text-sm font-medium text-gray-900 mb-3">
            <Camera className="w-4 h-4 mr-2" />
            Cameras with Active Alerts
          </h4>
          <div className="space-y-2 max-h-40 overflow-y-auto">
            {camerasWithAlerts.map(camera => (
              <div key={camera.id} className="flex items-center justify-between p-2 bg-gray-50 rounded-md">
                <div className="flex items-center space-x-2">
                  <span className={`text-lg ${getCameraStatusColor(camera.status)}`}>●</span>
                  <div>
                    <div className="text-sm font-medium text-gray-900">{camera.name}</div>
                    <div className="text-xs text-gray-500">
                      {camera.alerts.alert_type} • {formatTimestamp(camera.alerts.last_alert)}
                    </div>
                  </div>
                </div>
                <div className="flex items-center space-x-2">
                  <span className="bg-red-100 text-red-800 text-xs px-2 py-1 rounded-full font-medium">
                    {camera.alerts.active}
                  </span>
                  <button
                    onClick={() => onViewCamera && onViewCamera(camera)}
                    className="p-1 hover:bg-gray-200 rounded transition-colors"
                    title="View Camera"
                  >
                    <Eye className="w-4 h-4 text-gray-600" />
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Action Buttons */}
      <div className="p-4">
        <div className="flex space-x-2">
          <button
            onClick={() => onViewSite && onViewSite(site)}
            className="flex-1 bg-blue-600 text-white px-3 py-2 rounded-md text-sm font-medium hover:bg-blue-700 transition-colors flex items-center justify-center space-x-2"
          >
            <MapPin className="w-4 h-4" />
            <span>View Site Details</span>
          </button>
          <button
            onClick={() => {
              // Navigate to site's dashboard or detailed view
              window.location.href = `/dashboard?site=${site.id}`;
            }}
            className="px-3 py-2 border border-gray-300 text-gray-700 rounded-md text-sm font-medium hover:bg-gray-50 transition-colors"
          >
            Dashboard
          </button>
        </div>

        {totalAlerts > 0 && (
          <button
            onClick={() => {
              // Navigate to alerts page for this site
              window.location.href = `/alerts?site=${site.id}`;
            }}
            className="w-full mt-2 bg-red-50 text-red-700 px-3 py-2 rounded-md text-sm font-medium hover:bg-red-100 transition-colors flex items-center justify-center space-x-2"
          >
            <AlertTriangle className="w-4 h-4" />
            <span>View All Alerts ({totalAlerts})</span>
          </button>
        )}
      </div>
    </div>
  );
};

export default AlertSummaryPanel;