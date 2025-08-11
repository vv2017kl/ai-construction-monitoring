import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  Monitor, Activity, AlertTriangle, CheckCircle, XCircle,
  Cpu, HardDrive, Wifi, Database, Server, Zap, Globe,
  TrendingUp, TrendingDown, Clock, RefreshCw, Settings,
  BarChart3, Eye, Filter, Download, Calendar, Info,
  Battery, Signal, Thermometer, ArrowUp, ArrowDown,
  Users, Camera, Building2, Brain, Shield, Target
} from 'lucide-react';
import { useTheme } from '../../context/ThemeContext';
import MainLayout from '../../components/shared/Layout/MainLayout';
import { mockSites } from '../../data/mockData';

const SystemMonitoring = () => {
  const navigate = useNavigate();
  const { theme } = useTheme();
  
  // State management
  const [selectedTimeframe, setSelectedTimeframe] = useState('24h');
  const [selectedMetric, setSelectedMetric] = useState('overview');
  const [autoRefresh, setAutoRefresh] = useState(true);
  const [lastRefresh, setLastRefresh] = useState(new Date());

  // Mock system health data
  const systemHealth = {
    overall: 94,
    services: [
      { name: 'AI Detection Service', status: 'healthy', uptime: 99.8, response_time: 125, cpu: 67, memory: 78, errors: 0 },
      { name: 'Video Streaming', status: 'healthy', uptime: 99.9, response_time: 45, cpu: 34, memory: 45, errors: 2 },
      { name: 'Database Cluster', status: 'healthy', uptime: 100.0, response_time: 12, cpu: 23, memory: 62, errors: 0 },
      { name: 'API Gateway', status: 'healthy', uptime: 99.7, response_time: 89, cpu: 41, memory: 38, errors: 1 },
      { name: 'Notification Service', status: 'warning', uptime: 98.5, response_time: 234, cpu: 89, memory: 82, errors: 12 },
      { name: 'File Storage', status: 'healthy', uptime: 99.6, response_time: 156, cpu: 19, memory: 71, errors: 3 }
    ],
    infrastructure: [
      { name: 'Load Balancer', status: 'healthy', connections: 1247, throughput: '2.4 GB/s', cpu: 34, memory: 42 },
      { name: 'CDN Network', status: 'healthy', hit_ratio: 87.3, bandwidth: '15.2 GB/s', cpu: 12, memory: 28 },
      { name: 'Redis Cache', status: 'healthy', hit_ratio: 94.6, memory_usage: 68, operations: '45K/sec', cpu: 28 },
      { name: 'Message Queue', status: 'warning', queue_size: 892, processing_rate: '1.2K/sec', cpu: 78, memory: 84 }
    ]
  };

  // Site monitoring data
  const siteMetrics = [
    {
      site: 'Downtown Construction Site',
      status: 'healthy',
      cameras_online: 23,
      cameras_total: 24,
      ai_accuracy: 94.7,
      alerts_24h: 3,
      bandwidth_usage: 78,
      storage_usage: 67,
      last_incident: '2 days ago'
    },
    {
      site: 'Riverside Apartments',
      status: 'healthy', 
      cameras_online: 14,
      cameras_total: 15,
      ai_accuracy: 96.1,
      alerts_24h: 1,
      bandwidth_usage: 45,
      storage_usage: 52,
      last_incident: '5 days ago'
    },
    {
      site: 'Industrial Complex Alpha',
      status: 'warning',
      cameras_online: 6,
      cameras_total: 8,
      ai_accuracy: 89.3,
      alerts_24h: 8,
      bandwidth_usage: 92,
      storage_usage: 89,
      last_incident: '3 hours ago'
    },
    {
      site: 'Harbor Bridge Extension',
      status: 'healthy',
      cameras_online: 19,
      cameras_total: 20,
      ai_accuracy: 97.2,
      alerts_24h: 2,
      bandwidth_usage: 67,
      storage_usage: 71,
      last_incident: '1 day ago'
    }
  ];

  // Performance metrics over time (mock data)
  const performanceMetrics = {
    cpu: [45, 52, 48, 67, 58, 61, 55, 49, 63, 57, 52, 58],
    memory: [62, 65, 68, 71, 69, 74, 72, 68, 75, 73, 70, 72],
    network: [234, 456, 389, 512, 445, 523, 467, 398, 534, 478, 423, 456],
    storage: [78, 79, 80, 81, 82, 83, 84, 83, 85, 86, 87, 88]
  };

  // Alert data
  const recentAlerts = [
    { id: 1, level: 'critical', message: 'High memory usage detected on AI Detection Service', site: 'Industrial Complex Alpha', timestamp: '2 minutes ago', status: 'active' },
    { id: 2, level: 'warning', message: 'Camera offline at Zone C', site: 'Downtown Construction Site', timestamp: '15 minutes ago', status: 'investigating' },
    { id: 3, level: 'info', message: 'Scheduled maintenance completed successfully', site: 'All Sites', timestamp: '1 hour ago', status: 'resolved' },
    { id: 4, level: 'warning', message: 'Bandwidth usage approaching limit', site: 'Industrial Complex Alpha', timestamp: '2 hours ago', status: 'active' },
    { id: 5, level: 'critical', message: 'Database connection timeout detected', site: 'Riverside Apartments', timestamp: '3 hours ago', status: 'resolved' }
  ];

  const getStatusColor = (status) => {
    switch (status) {
      case 'healthy': return { bg: 'bg-green-100', text: 'text-green-800', dot: 'bg-green-500', icon: CheckCircle };
      case 'warning': return { bg: 'bg-yellow-100', text: 'text-yellow-800', dot: 'bg-yellow-500', icon: AlertTriangle };
      case 'critical': return { bg: 'bg-red-100', text: 'text-red-800', dot: 'bg-red-500', icon: XCircle };
      case 'offline': return { bg: 'bg-gray-100', text: 'text-gray-800', dot: 'bg-gray-500', icon: XCircle };
      default: return { bg: 'bg-gray-100', text: 'text-gray-800', dot: 'bg-gray-500', icon: Activity };
    }
  };

  const getAlertLevelColor = (level) => {
    switch (level) {
      case 'critical': return 'border-l-red-500 bg-red-50';
      case 'warning': return 'border-l-yellow-500 bg-yellow-50';
      case 'info': return 'border-l-blue-500 bg-blue-50';
      default: return 'border-l-gray-500 bg-gray-50';
    }
  };

  const getMetricColor = (value, type) => {
    if (type === 'uptime') {
      if (value >= 99) return 'text-green-600';
      if (value >= 95) return 'text-yellow-600';
      return 'text-red-600';
    }
    if (value >= 90) return 'text-red-600';
    if (value >= 70) return 'text-yellow-600';
    return 'text-green-600';
  };

  const StatCard = ({ title, value, subtitle, icon: Icon, color, trend, status }) => (
    <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-sm font-medium text-gray-600">{title}</h3>
          <p className="text-2xl font-bold text-gray-900 mt-2">{value}</p>
          {trend && (
            <div className={`flex items-center mt-2 text-sm ${trend.positive ? 'text-green-600' : 'text-red-600'}`}>
              {trend.positive ? <TrendingUp className="w-4 h-4 mr-1" /> : <TrendingDown className="w-4 h-4 mr-1" />}
              <span>{trend.value}</span>
            </div>
          )}
          {subtitle && <p className="text-xs text-gray-500 mt-1">{subtitle}</p>}
        </div>
        <div 
          className="p-3 rounded-lg"
          style={{ backgroundColor: color + '20' }}
        >
          <Icon className="w-6 h-6" style={{ color }} />
        </div>
      </div>
      {status && (
        <div className="mt-4 flex items-center space-x-2">
          <div className={`w-2 h-2 rounded-full ${getStatusColor(status).dot}`}></div>
          <span className="text-xs font-medium text-gray-600 capitalize">{status}</span>
        </div>
      )}
    </div>
  );

  const ServiceCard = ({ service }) => {
    const statusConfig = getStatusColor(service.status);
    const StatusIcon = statusConfig.icon;
    
    return (
      <div className="bg-white rounded-lg border border-gray-200 p-4">
        <div className="flex items-center justify-between mb-3">
          <div className="flex items-center space-x-2">
            <StatusIcon className="w-4 h-4" style={{ color: statusConfig.dot.replace('bg-', '').replace('500', '') === 'green' ? '#10B981' : statusConfig.dot.replace('bg-', '').replace('500', '') === 'yellow' ? '#F59E0B' : '#EF4444' }} />
            <h4 className="font-medium text-gray-900">{service.name}</h4>
          </div>
          <span className={`px-2 py-1 text-xs font-semibold rounded-full ${statusConfig.bg} ${statusConfig.text}`}>
            {service.status.toUpperCase()}
          </span>
        </div>
        
        <div className="grid grid-cols-2 gap-4 text-sm">
          <div>
            <span className="text-gray-600">Uptime:</span>
            <span className={`ml-2 font-medium ${getMetricColor(service.uptime, 'uptime')}`}>
              {service.uptime}%
            </span>
          </div>
          <div>
            <span className="text-gray-600">Response:</span>
            <span className="ml-2 font-medium text-blue-600">{service.response_time}ms</span>
          </div>
          <div>
            <span className="text-gray-600">CPU:</span>
            <span className={`ml-2 font-medium ${getMetricColor(service.cpu)}`}>{service.cpu}%</span>
          </div>
          <div>
            <span className="text-gray-600">Memory:</span>
            <span className={`ml-2 font-medium ${getMetricColor(service.memory)}`}>{service.memory}%</span>
          </div>
        </div>
        
        {service.errors > 0 && (
          <div className="mt-3 flex items-center space-x-2 text-red-600">
            <AlertTriangle className="w-3 h-3" />
            <span className="text-xs">{service.errors} errors in last 24h</span>
          </div>
        )}
      </div>
    );
  };

  const SiteCard = ({ site }) => {
    const statusConfig = getStatusColor(site.status);
    
    return (
      <div className="bg-white rounded-lg border border-gray-200 p-4">
        <div className="flex items-center justify-between mb-3">
          <div className="flex items-center space-x-2">
            <Building2 className="w-4 h-4 text-gray-600" />
            <h4 className="font-medium text-gray-900">{site.site}</h4>
          </div>
          <span className={`px-2 py-1 text-xs font-semibold rounded-full ${statusConfig.bg} ${statusConfig.text}`}>
            {site.status.toUpperCase()}
          </span>
        </div>
        
        <div className="space-y-2 text-sm">
          <div className="flex justify-between">
            <span className="text-gray-600">Cameras:</span>
            <span className="font-medium">{site.cameras_online}/{site.cameras_total} online</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-600">AI Accuracy:</span>
            <span className="font-medium text-green-600">{site.ai_accuracy}%</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-600">Alerts (24h):</span>
            <span className={`font-medium ${site.alerts_24h > 5 ? 'text-red-600' : site.alerts_24h > 2 ? 'text-yellow-600' : 'text-green-600'}`}>
              {site.alerts_24h}
            </span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-600">Bandwidth:</span>
            <span className={`font-medium ${getMetricColor(site.bandwidth_usage)}`}>{site.bandwidth_usage}%</span>
          </div>
        </div>
        
        <div className="mt-3 text-xs text-gray-500">
          Last incident: {site.last_incident}
        </div>
      </div>
    );
  };

  const AlertItem = ({ alert }) => (
    <div className={`border-l-4 p-4 mb-3 rounded-r-lg ${getAlertLevelColor(alert.level)}`}>
      <div className="flex items-start justify-between">
        <div>
          <div className="flex items-center space-x-2 mb-1">
            <span className={`px-2 py-1 text-xs font-semibold rounded ${
              alert.level === 'critical' ? 'bg-red-100 text-red-800' :
              alert.level === 'warning' ? 'bg-yellow-100 text-yellow-800' :
              'bg-blue-100 text-blue-800'
            }`}>
              {alert.level.toUpperCase()}
            </span>
            <span className="text-sm font-medium text-gray-900">{alert.site}</span>
          </div>
          <p className="text-sm text-gray-700 mb-2">{alert.message}</p>
          <p className="text-xs text-gray-500">{alert.timestamp}</p>
        </div>
        <span className={`px-2 py-1 text-xs rounded ${
          alert.status === 'active' ? 'bg-red-100 text-red-700' :
          alert.status === 'investigating' ? 'bg-yellow-100 text-yellow-700' :
          'bg-green-100 text-green-700'
        }`}>
          {alert.status}
        </span>
      </div>
    </div>
  );

  // Auto-refresh functionality
  useEffect(() => {
    if (autoRefresh) {
      const interval = setInterval(() => {
        setLastRefresh(new Date());
      }, 30000); // 30 seconds
      
      return () => clearInterval(interval);
    }
  }, [autoRefresh]);

  return (
    <MainLayout portal="solution-admin">
      <div className="h-full flex flex-col">
        {/* Header */}
        <div className="bg-white border-b border-gray-200 px-6 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-xl font-bold text-gray-900">System Monitoring</h1>
              <div className="flex items-center space-x-2 text-sm text-gray-600">
                <Activity className="w-3 h-3" />
                <span>{systemHealth.services.filter(s => s.status === 'healthy').length}/{systemHealth.services.length} services healthy</span>
                <span>•</span>
                <span>Overall health: {systemHealth.overall}%</span>
                <span>•</span>
                <span>Last updated: {lastRefresh.toLocaleTimeString()}</span>
              </div>
            </div>

            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-2">
                <label className="text-sm text-gray-600">Auto-refresh:</label>
                <label className="relative inline-flex items-center cursor-pointer">
                  <input
                    type="checkbox"
                    checked={autoRefresh}
                    onChange={(e) => setAutoRefresh(e.target.checked)}
                    className="sr-only peer"
                  />
                  <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
                </label>
              </div>

              <select
                value={selectedTimeframe}
                onChange={(e) => setSelectedTimeframe(e.target.value)}
                className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="1h">Last Hour</option>
                <option value="24h">Last 24 Hours</option>
                <option value="7d">Last 7 Days</option>
                <option value="30d">Last 30 Days</option>
              </select>

              <button
                onClick={() => setLastRefresh(new Date())}
                className="flex items-center space-x-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
              >
                <RefreshCw className="w-4 h-4" />
                <span>Refresh</span>
              </button>
            </div>
          </div>
        </div>

        {/* Overview Stats */}
        <div className="px-6 py-4 bg-gray-50 border-b border-gray-200">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <StatCard
              title="System Health"
              value={`${systemHealth.overall}%`}
              icon={Activity}
              color={theme.success[500]}
              status="healthy"
            />
            <StatCard
              title="Active Services"
              value={`${systemHealth.services.filter(s => s.status === 'healthy').length}/${systemHealth.services.length}`}
              subtitle="Services operational"
              icon={Server}
              color={theme.primary[500]}
            />
            <StatCard
              title="Critical Alerts"
              value={recentAlerts.filter(a => a.level === 'critical' && a.status === 'active').length}
              subtitle="Requiring attention"
              icon={AlertTriangle}
              color={theme.danger[500]}
            />
            <StatCard
              title="Sites Online"
              value={`${siteMetrics.filter(s => s.status === 'healthy').length}/${siteMetrics.length}`}
              subtitle="Construction sites"
              icon={Building2}
              color={theme.warning[500]}
            />
          </div>
        </div>

        {/* Main Content */}
        <div className="flex-1 overflow-auto">
          <div className="p-6">
            {/* Services Grid */}
            <div className="mb-8">
              <h2 className="text-lg font-semibold text-gray-900 mb-4">System Services</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {systemHealth.services.map((service, index) => (
                  <ServiceCard key={index} service={service} />
                ))}
              </div>
            </div>

            {/* Sites Grid */}
            <div className="mb-8">
              <h2 className="text-lg font-semibold text-gray-900 mb-4">Site Monitoring</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                {siteMetrics.map((site, index) => (
                  <SiteCard key={index} site={site} />
                ))}
              </div>
            </div>

            {/* Infrastructure Status */}
            <div className="mb-8">
              <h2 className="text-lg font-semibold text-gray-900 mb-4">Infrastructure Status</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                {systemHealth.infrastructure.map((infra, index) => {
                  const statusConfig = getStatusColor(infra.status);
                  return (
                    <div key={index} className="bg-white rounded-lg border border-gray-200 p-4">
                      <div className="flex items-center justify-between mb-3">
                        <h4 className="font-medium text-gray-900">{infra.name}</h4>
                        <span className={`px-2 py-1 text-xs font-semibold rounded-full ${statusConfig.bg} ${statusConfig.text}`}>
                          {infra.status.toUpperCase()}
                        </span>
                      </div>
                      <div className="space-y-2 text-sm">
                        {infra.connections && (
                          <div className="flex justify-between">
                            <span className="text-gray-600">Connections:</span>
                            <span className="font-medium">{infra.connections.toLocaleString()}</span>
                          </div>
                        )}
                        {infra.hit_ratio && (
                          <div className="flex justify-between">
                            <span className="text-gray-600">Hit Ratio:</span>
                            <span className="font-medium text-green-600">{infra.hit_ratio}%</span>
                          </div>
                        )}
                        <div className="flex justify-between">
                          <span className="text-gray-600">CPU:</span>
                          <span className={`font-medium ${getMetricColor(infra.cpu)}`}>{infra.cpu}%</span>
                        </div>
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>

            {/* Recent Alerts */}
            <div>
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-lg font-semibold text-gray-900">Recent Alerts</h2>
                <button className="text-blue-600 hover:text-blue-800 text-sm font-medium">
                  View All Alerts →
                </button>
              </div>
              <div className="bg-white rounded-lg border border-gray-200 p-4">
                {recentAlerts.map((alert) => (
                  <AlertItem key={alert.id} alert={alert} />
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </MainLayout>
  );
};

export default SystemMonitoring;