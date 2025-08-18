import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  BarChart3, TrendingUp, TrendingDown, Users, Building2, 
  Server, Shield, AlertTriangle, CheckCircle, Clock,
  Activity, Zap, Database, Globe, Settings, Eye,
  RefreshCw, Download, Filter, Calendar, MapPin,
  User, Camera, Bell, Wifi, HardDrive, Cpu, Monitor, Loader
} from 'lucide-react';
import { useTheme } from '../../context/ThemeContext';
import MainLayout from '../../components/shared/Layout/MainLayout';
import { backendAPI, zoneminderAPI } from '../../services';
import { useRealTimeData, useAPI } from '../../hooks/useAPI';
import { formatters } from '../../utils/formatters';
import { generateDashboardMetrics } from '../../utils/dataCalculations';

const AdminDashboard = () => {
  const navigate = useNavigate();
  const { theme } = useTheme();
  
  // State management
  const [selectedTimeRange, setSelectedTimeRange] = useState('24h'); // '1h', '24h', '7d', '30d'
  const [refreshInterval, setRefreshInterval] = useState(30); // seconds
  const [lastRefresh, setLastRefresh] = useState(new Date());

  // Mock admin-level data
  const systemMetrics = {
    totalUsers: 247,
    activeSites: 12,
    totalCameras: 184,
    systemUptime: 99.7,
    dataProcessed: '847 GB',
    apiCalls: '2.4M',
    activeAlerts: 7,
    resolvedToday: 23
  };

  const sitePerformance = [
    {
      id: 'site-001',
      name: 'Downtown Construction Site',
      status: 'operational',
      personnel: 34,
      cameras: 16,
      alerts: 2,
      uptime: 99.9,
      lastUpdate: new Date(Date.now() - 15 * 60 * 1000),
      aiAccuracy: 94.5,
      safetyScore: 89
    },
    {
      id: 'site-002',
      name: 'Harbor Bridge Project',
      status: 'operational',
      personnel: 28,
      cameras: 12,
      alerts: 1,
      uptime: 98.7,
      lastUpdate: new Date(Date.now() - 8 * 60 * 1000),
      aiAccuracy: 91.2,
      safetyScore: 96
    },
    {
      id: 'site-003',
      name: 'Industrial Complex Alpha',
      status: 'maintenance',
      personnel: 42,
      cameras: 24,
      alerts: 4,
      uptime: 95.2,
      lastUpdate: new Date(Date.now() - 45 * 60 * 1000),
      aiAccuracy: 87.8,
      safetyScore: 82
    },
    {
      id: 'site-004',
      name: 'Residential Tower Phase 2',
      status: 'operational',
      personnel: 22,
      cameras: 8,
      alerts: 0,
      uptime: 100.0,
      lastUpdate: new Date(Date.now() - 5 * 60 * 1000),
      aiAccuracy: 96.1,
      safetyScore: 94
    }
  ];

  const systemHealth = {
    cpu: 78,
    memory: 65,
    disk: 42,
    network: 89,
    database: 91,
    aiModels: 96
  };

  const recentActivity = [
    {
      id: 1,
      type: 'user_login',
      description: 'Sarah Chen logged into Harbor Bridge Project',
      timestamp: new Date(Date.now() - 5 * 60 * 1000),
      severity: 'info',
      site: 'Harbor Bridge Project'
    },
    {
      id: 2,
      type: 'alert_resolved',
      description: 'Safety violation alert resolved at Downtown Site',
      timestamp: new Date(Date.now() - 12 * 60 * 1000),
      severity: 'success',
      site: 'Downtown Construction Site'
    },
    {
      id: 3,
      type: 'system_update',
      description: 'AI model v8.2 deployed to Industrial Complex Alpha',
      timestamp: new Date(Date.now() - 18 * 60 * 1000),
      severity: 'info',
      site: 'Industrial Complex Alpha'
    },
    {
      id: 4,
      type: 'maintenance',
      description: 'Scheduled maintenance started on cameras 15-24',
      timestamp: new Date(Date.now() - 25 * 60 * 1000),
      severity: 'warning',
      site: 'Industrial Complex Alpha'
    },
    {
      id: 5,
      type: 'alert_triggered',
      description: 'Equipment violation detected - requires attention',
      timestamp: new Date(Date.now() - 35 * 60 * 1000),
      severity: 'error',
      site: 'Downtown Construction Site'
    }
  ];

  const formatRelativeTime = (timestamp) => {
    const now = new Date();
    const diff = now - new Date(timestamp);
    const minutes = Math.floor(diff / (1000 * 60));
    const hours = Math.floor(minutes / 60);

    if (minutes < 60) return `${minutes}m ago`;
    return `${hours}h ago`;
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'operational': return { bg: 'bg-green-100', text: 'text-green-800', dot: 'bg-green-500' };
      case 'maintenance': return { bg: 'bg-yellow-100', text: 'text-yellow-800', dot: 'bg-yellow-500' };
      case 'offline': return { bg: 'bg-red-100', text: 'text-red-800', dot: 'bg-red-500' };
      default: return { bg: 'bg-gray-100', text: 'text-gray-800', dot: 'bg-gray-500' };
    }
  };

  const getSeverityColor = (severity) => {
    switch (severity) {
      case 'success': return 'text-green-600';
      case 'warning': return 'text-yellow-600';
      case 'error': return 'text-red-600';
      default: return 'text-blue-600';
    }
  };

  const getSeverityIcon = (severity) => {
    switch (severity) {
      case 'success': return CheckCircle;
      case 'warning': return AlertTriangle;
      case 'error': return AlertTriangle;
      default: return Activity;
    }
  };

  const getHealthColor = (percentage) => {
    if (percentage >= 90) return 'text-green-600';
    if (percentage >= 70) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getHealthBarColor = (percentage) => {
    if (percentage >= 90) return theme.success[500];
    if (percentage >= 70) return theme.warning[500];
    return theme.danger[500];
  };

  const MetricCard = ({ title, value, subtitle, icon: Icon, color, trend, onClick }) => (
    <div 
      className="bg-white rounded-xl p-6 shadow-sm border border-gray-100 hover:shadow-md transition-all duration-200 cursor-pointer"
      onClick={onClick}
    >
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-sm font-medium text-gray-600">{title}</h3>
          <p className="text-3xl font-bold text-gray-900 mt-2">{value}</p>
          {trend && (
            <div className={`flex items-center mt-2 text-sm ${trend.positive ? 'text-green-600' : 'text-red-600'}`}>
              {trend.positive ? <TrendingUp className="w-4 h-4 mr-1" /> : <TrendingDown className="w-4 h-4 mr-1" />}
              <span>{trend.value}</span>
            </div>
          )}
          {subtitle && <p className="text-xs text-gray-500 mt-1">{subtitle}</p>}
        </div>
        <div 
          className="p-4 rounded-lg"
          style={{ backgroundColor: color + '20' }}
        >
          <Icon className="w-8 h-8" style={{ color }} />
        </div>
      </div>
    </div>
  );

  const SiteCard = ({ site }) => {
    const statusConfig = getStatusColor(site.status);
    
    return (
      <div 
        className="bg-white rounded-lg border border-gray-200 p-6 hover:shadow-md transition-all duration-200 cursor-pointer"
        onClick={() => navigate(`/admin/site-config?site=${site.id}`)}
      >
        <div className="flex items-center justify-between mb-4">
          <div>
            <h3 className="font-semibold text-gray-900">{site.name}</h3>
            <p className="text-sm text-gray-600">Last update: {formatRelativeTime(site.lastUpdate)}</p>
          </div>
          <span className={`px-3 py-1 text-xs font-semibold rounded-full ${statusConfig.bg} ${statusConfig.text}`}>
            {site.status.toUpperCase()}
          </span>
        </div>

        <div className="grid grid-cols-2 gap-4 mb-4">
          <div className="text-center">
            <div className="text-2xl font-bold text-blue-600">{site.personnel}</div>
            <div className="text-xs text-gray-600">Personnel</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-purple-600">{site.cameras}</div>
            <div className="text-xs text-gray-600">Cameras</div>
          </div>
        </div>

        <div className="space-y-2">
          <div className="flex justify-between items-center">
            <span className="text-sm text-gray-600">Uptime:</span>
            <span className={`font-bold ${getHealthColor(site.uptime)}`}>{site.uptime}%</span>
          </div>
          <div className="flex justify-between items-center">
            <span className="text-sm text-gray-600">AI Accuracy:</span>
            <span className={`font-bold ${getHealthColor(site.aiAccuracy)}`}>{site.aiAccuracy}%</span>
          </div>
          <div className="flex justify-between items-center">
            <span className="text-sm text-gray-600">Safety Score:</span>
            <span className={`font-bold ${getHealthColor(site.safetyScore)}`}>{site.safetyScore}/100</span>
          </div>
          {site.alerts > 0 && (
            <div className="flex justify-between items-center pt-2 border-t border-gray-100">
              <span className="text-sm text-red-600">Active Alerts:</span>
              <span className="font-bold text-red-600">{site.alerts}</span>
            </div>
          )}
        </div>
      </div>
    );
  };

  const ActivityItem = ({ activity }) => {
    const Icon = getSeverityIcon(activity.severity);
    
    return (
      <div className="flex items-start space-x-3 p-3 hover:bg-gray-50 rounded-lg transition-colors">
        <div className={`p-2 rounded-full bg-gray-100`}>
          <Icon className={`w-4 h-4 ${getSeverityColor(activity.severity)}`} />
        </div>
        <div className="flex-1 min-w-0">
          <p className="text-sm font-medium text-gray-900">{activity.description}</p>
          <div className="flex items-center space-x-2 text-xs text-gray-500 mt-1">
            <span>{formatRelativeTime(activity.timestamp)}</span>
            <span>•</span>
            <span>{activity.site}</span>
          </div>
        </div>
      </div>
    );
  };

  const HealthMetric = ({ title, value, icon: Icon }) => (
    <div className="flex items-center justify-between p-4 bg-white rounded-lg border border-gray-200">
      <div className="flex items-center space-x-3">
        <Icon className="w-5 h-5 text-gray-600" />
        <span className="font-medium text-gray-900">{title}</span>
      </div>
      <div className="flex items-center space-x-3">
        <div className="w-24 bg-gray-200 rounded-full h-2">
          <div 
            className="h-2 rounded-full transition-all duration-500"
            style={{ 
              width: `${value}%`,
              backgroundColor: getHealthBarColor(value)
            }}
          ></div>
        </div>
        <span className={`font-bold text-lg ${getHealthColor(value)}`}>{value}%</span>
      </div>
    </div>
  );

  return (
    <MainLayout portal="solution-admin">
      <div className="h-full flex flex-col">
        {/* Header */}
        <div className="bg-white border-b border-gray-200 px-6 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-xl font-bold text-gray-900">Admin Dashboard</h1>
              <div className="flex items-center space-x-2 text-sm text-gray-600">
                <Globe className="w-3 h-3" />
                <span>{systemMetrics.activeSites} active sites</span>
                <span>•</span>
                <span>{systemMetrics.totalUsers} users</span>
                <span>•</span>
                <Clock className="w-3 h-3" />
                <span>Last updated: {lastRefresh.toLocaleTimeString()}</span>
              </div>
            </div>

            <div className="flex items-center space-x-4">
              {/* Time Range Selector */}
              <div className="flex items-center space-x-2 bg-gray-100 rounded-lg p-1">
                {['1h', '24h', '7d', '30d'].map((range) => (
                  <button
                    key={range}
                    onClick={() => setSelectedTimeRange(range)}
                    className={`px-3 py-1 text-sm rounded transition-colors ${
                      selectedTimeRange === range 
                        ? 'bg-white shadow-sm text-blue-600' 
                        : 'hover:bg-gray-200'
                    }`}
                  >
                    {range}
                  </button>
                ))}
              </div>

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

        {/* Main Content */}
        <div className="flex-1 overflow-auto p-6 space-y-6">
          {/* Key Metrics */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <MetricCard
              title="Total Users"
              value={systemMetrics.totalUsers.toLocaleString()}
              subtitle="Across all sites"
              icon={Users}
              color={theme.primary[500]}
              trend={{ positive: true, value: '+12 this week' }}
              onClick={() => navigate('/admin/users')}
            />
            <MetricCard
              title="Active Sites"
              value={systemMetrics.activeSites}
              subtitle={`${systemMetrics.totalCameras} cameras total`}
              icon={Building2}
              color={theme.success[500]}
              trend={{ positive: true, value: '+2 this month' }}
              onClick={() => navigate('/admin/sites')}
            />
            <MetricCard
              title="System Uptime"
              value={`${systemMetrics.systemUptime}%`}
              subtitle="Last 30 days"
              icon={Server}
              color={theme.warning[500]}
              onClick={() => navigate('/admin/monitoring')}
            />
            <MetricCard
              title="Active Alerts"
              value={systemMetrics.activeAlerts}
              subtitle={`${systemMetrics.resolvedToday} resolved today`}
              icon={AlertTriangle}
              color={theme.danger[500]}
              onClick={() => navigate('/admin/alerts')}
            />
          </div>

          {/* Site Performance Overview */}
          <div className="grid grid-cols-1 xl:grid-cols-3 gap-6">
            <div className="xl:col-span-2">
              <div className="bg-white rounded-lg shadow-sm border border-gray-100">
                <div className="p-6 border-b border-gray-100">
                  <div className="flex items-center justify-between">
                    <h2 className="text-lg font-semibold text-gray-900">Site Performance</h2>
                    <button 
                      onClick={() => navigate('/admin/sites')}
                      className="text-blue-600 hover:text-blue-800 text-sm font-medium"
                    >
                      View All Sites
                    </button>
                  </div>
                </div>
                <div className="p-6">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    {sitePerformance.map((site) => (
                      <SiteCard key={site.id} site={site} />
                    ))}
                  </div>
                </div>
              </div>
            </div>

            {/* System Health & Recent Activity */}
            <div className="space-y-6">
              {/* System Health */}
              <div className="bg-white rounded-lg shadow-sm border border-gray-100">
                <div className="p-6 border-b border-gray-100">
                  <h3 className="text-lg font-semibold text-gray-900">System Health</h3>
                </div>
                <div className="p-6 space-y-4">
                  <HealthMetric title="CPU Usage" value={systemHealth.cpu} icon={Cpu} />
                  <HealthMetric title="Memory" value={systemHealth.memory} icon={Monitor} />
                  <HealthMetric title="Disk Space" value={systemHealth.disk} icon={HardDrive} />
                  <HealthMetric title="Network" value={systemHealth.network} icon={Wifi} />
                  <HealthMetric title="Database" value={systemHealth.database} icon={Database} />
                  <HealthMetric title="AI Models" value={systemHealth.aiModels} icon={Zap} />
                </div>
              </div>

              {/* Recent Activity */}
              <div className="bg-white rounded-lg shadow-sm border border-gray-100">
                <div className="p-6 border-b border-gray-100">
                  <h3 className="text-lg font-semibold text-gray-900">Recent Activity</h3>
                </div>
                <div className="p-6">
                  <div className="space-y-1">
                    {recentActivity.map((activity) => (
                      <ActivityItem key={activity.id} activity={activity} />
                    ))}
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Quick Actions */}
          <div className="bg-white rounded-lg shadow-sm border border-gray-100">
            <div className="p-6 border-b border-gray-100">
              <h3 className="text-lg font-semibold text-gray-900">Quick Actions</h3>
            </div>
            <div className="p-6">
              <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                <button
                  onClick={() => navigate('/admin/users')}
                  className="flex items-center space-x-3 p-4 bg-blue-50 hover:bg-blue-100 rounded-lg transition-colors"
                >
                  <User className="w-6 h-6 text-blue-600" />
                  <div className="text-left">
                    <div className="font-medium text-blue-900">Manage Users</div>
                    <div className="text-sm text-blue-600">Add, edit, or remove user accounts</div>
                  </div>
                </button>
                
                <button
                  onClick={() => navigate('/admin/site-config')}
                  className="flex items-center space-x-3 p-4 bg-green-50 hover:bg-green-100 rounded-lg transition-colors"
                >
                  <Settings className="w-6 h-6 text-green-600" />
                  <div className="text-left">
                    <div className="font-medium text-green-900">Site Configuration</div>
                    <div className="text-sm text-green-600">Configure site settings and zones</div>
                  </div>
                </button>
                
                <button
                  onClick={() => navigate('/admin/monitoring')}
                  className="flex items-center space-x-3 p-4 bg-purple-50 hover:bg-purple-100 rounded-lg transition-colors"
                >
                  <Activity className="w-6 h-6 text-purple-600" />
                  <div className="text-left">
                    <div className="font-medium text-purple-900">System Monitoring</div>
                    <div className="text-sm text-purple-600">Monitor system performance</div>
                  </div>
                </button>
                
                <button
                  onClick={() => navigate('/admin/analytics')}
                  className="flex items-center space-x-3 p-4 bg-orange-50 hover:bg-orange-100 rounded-lg transition-colors"
                >
                  <BarChart3 className="w-6 h-6 text-orange-600" />
                  <div className="text-left">
                    <div className="font-medium text-orange-900">Executive Analytics</div>
                    <div className="text-sm text-orange-600">View business intelligence</div>
                  </div>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </MainLayout>
  );
};

export default AdminDashboard;