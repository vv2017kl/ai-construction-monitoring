import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  Settings, Link, Globe, Database, Key, Shield, 
  Plus, Search, Filter, Edit3, Trash2, Eye, MoreVertical,
  CheckCircle, XCircle, AlertTriangle, Clock, RefreshCw,
  Download, Upload, Grid, List, TrendingUp, Activity,
  Mail, MessageSquare, Bell, Smartphone, Cloud, Server,
  Zap, Camera, Monitor, Brain, Target, Award, Info
} from 'lucide-react';
import { useTheme } from '../../context/ThemeContext';
import MainLayout from '../../components/shared/Layout/MainLayout';

const IntegrationSettings = () => {
  const navigate = useNavigate();
  const { theme } = useTheme();
  
  // State management
  const [searchTerm, setSearchTerm] = useState('');
  const [filterCategory, setFilterCategory] = useState('all');
  const [filterStatus, setFilterStatus] = useState('all');
  const [viewMode, setViewMode] = useState('grid');
  const [selectedIntegration, setSelectedIntegration] = useState(null);
  const [showConfigModal, setShowConfigModal] = useState(false);

  // Mock integrations data
  const integrations = [
    {
      id: 'smtp_01',
      name: 'SMTP Email Service',
      category: 'Communication',
      type: 'email',
      status: 'active',
      description: 'Email notifications and alerts via SMTP server',
      provider: 'Internal SMTP',
      last_sync: new Date('2024-12-10T14:30:00'),
      health: 98,
      monthly_usage: 12456,
      monthly_limit: 50000,
      config: {
        host: 'smtp.constructionai.com',
        port: 587,
        security: 'TLS',
        auth_required: true
      },
      endpoints: 2,
      error_rate: 0.2,
      avg_response_time: 1.2
    },
    {
      id: 'webhook_01',
      name: 'Webhook Notifications',
      category: 'Communication',
      type: 'webhook',
      status: 'active',
      description: 'Real-time webhook notifications for external systems',
      provider: 'Multiple Endpoints',
      last_sync: new Date('2024-12-10T15:45:00'),
      health: 95,
      monthly_usage: 8923,
      monthly_limit: 100000,
      config: {
        endpoints: 4,
        retry_attempts: 3,
        timeout: 30
      },
      endpoints: 4,
      error_rate: 1.8,
      avg_response_time: 0.45
    },
    {
      id: 'sms_01',
      name: 'SMS Alerts',
      category: 'Communication',
      type: 'sms',
      status: 'inactive',
      description: 'SMS notifications for critical alerts',
      provider: 'Twilio',
      last_sync: new Date('2024-12-05T09:15:00'),
      health: 0,
      monthly_usage: 0,
      monthly_limit: 5000,
      config: {
        account_sid: 'AC***************',
        auth_token: '***************',
        from_number: '+1234567890'
      },
      endpoints: 1,
      error_rate: 0,
      avg_response_time: 0
    },
    {
      id: 'aws_s3_01',
      name: 'AWS S3 Storage',
      category: 'Storage',
      type: 'cloud_storage',
      status: 'active',
      description: 'Cloud storage for video recordings and files',
      provider: 'Amazon Web Services',
      last_sync: new Date('2024-12-10T16:20:00'),
      health: 99,
      monthly_usage: 2.4, // TB
      monthly_limit: 10, // TB
      config: {
        bucket_name: 'construction-ai-media',
        region: 'us-east-1',
        encryption: 'AES-256'
      },
      endpoints: 1,
      error_rate: 0.1,
      avg_response_time: 0.8
    },
    {
      id: 'slack_01',
      name: 'Slack Integration',
      category: 'Communication',
      type: 'chat',
      status: 'warning',
      description: 'Team notifications and alerts via Slack channels',
      provider: 'Slack Technologies',
      last_sync: new Date('2024-12-10T13:10:00'),
      health: 87,
      monthly_usage: 3421,
      monthly_limit: 10000,
      config: {
        workspace: 'construction-ai',
        channels: ['#alerts', '#safety', '#general'],
        bot_token: 'xoxb-***************'
      },
      endpoints: 3,
      error_rate: 4.2,
      avg_response_time: 2.1
    },
    {
      id: 'api_gateway_01',
      name: 'External API Gateway',
      category: 'API',
      type: 'api_gateway',
      status: 'active',
      description: 'Gateway for external API integrations and third-party services',
      provider: 'Internal Gateway',
      last_sync: new Date('2024-12-10T16:45:00'),
      health: 96,
      monthly_usage: 156780,
      monthly_limit: 1000000,
      config: {
        rate_limit: '1000/hour',
        auth_methods: ['API Key', 'OAuth 2.0'],
        endpoints: 12
      },
      endpoints: 12,
      error_rate: 2.1,
      avg_response_time: 0.35
    },
    {
      id: 'weather_api_01',
      name: 'Weather API',
      category: 'External Data',
      type: 'weather',
      status: 'active',
      description: 'Weather data integration for site conditions',
      provider: 'OpenWeatherMap',
      last_sync: new Date('2024-12-10T16:50:00'),
      health: 99,
      monthly_usage: 4567,
      monthly_limit: 60000,
      config: {
        api_key: '***************',
        update_frequency: '15 minutes',
        locations: 4
      },
      endpoints: 1,
      error_rate: 0.05,
      avg_response_time: 0.6
    },
    {
      id: 'database_sync_01',
      name: 'Database Synchronization',
      category: 'Data',
      type: 'database',
      status: 'active',
      description: 'Real-time data synchronization with external databases',
      provider: 'Multiple Sources',
      last_sync: new Date('2024-12-10T16:55:00'),
      health: 94,
      monthly_usage: 892340,
      monthly_limit: 5000000,
      config: {
        sources: 3,
        sync_frequency: '5 minutes',
        conflict_resolution: 'last_write_wins'
      },
      endpoints: 3,
      error_rate: 1.2,
      avg_response_time: 0.2
    }
  ];

  const [integrationsData, setIntegrationsData] = useState(integrations);

  // Filter integrations
  const filteredIntegrations = integrationsData
    .filter(integration => {
      const matchesSearch = integration.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                           integration.description.toLowerCase().includes(searchTerm.toLowerCase()) ||
                           integration.provider.toLowerCase().includes(searchTerm.toLowerCase());
      const matchesCategory = filterCategory === 'all' || integration.category === filterCategory;
      const matchesStatus = filterStatus === 'all' || integration.status === filterStatus;
      
      return matchesSearch && matchesCategory && matchesStatus;
    });

  const getStatusColor = (status) => {
    switch (status) {
      case 'active': return { bg: 'bg-green-100', text: 'text-green-800', dot: 'bg-green-500', icon: CheckCircle };
      case 'warning': return { bg: 'bg-yellow-100', text: 'text-yellow-800', dot: 'bg-yellow-500', icon: AlertTriangle };
      case 'inactive': return { bg: 'bg-gray-100', text: 'text-gray-800', dot: 'bg-gray-500', icon: XCircle };
      case 'error': return { bg: 'bg-red-100', text: 'text-red-800', dot: 'bg-red-500', icon: XCircle };
      default: return { bg: 'bg-gray-100', text: 'text-gray-800', dot: 'bg-gray-500', icon: Activity };
    }
  };

  const getTypeIcon = (type) => {
    switch (type) {
      case 'email': return Mail;
      case 'sms': return Smartphone;
      case 'webhook': return Link;
      case 'chat': return MessageSquare;
      case 'cloud_storage': return Cloud;
      case 'api_gateway': return Globe;
      case 'weather': return Cloud;
      case 'database': return Database;
      default: return Settings;
    }
  };

  const getHealthColor = (health) => {
    if (health >= 95) return 'text-green-600';
    if (health >= 85) return 'text-yellow-600';
    if (health >= 70) return 'text-orange-600';
    return 'text-red-600';
  };

  const formatUsage = (usage, limit, type) => {
    if (type === 'cloud_storage') {
      return `${usage}TB / ${limit}TB`;
    }
    return `${usage.toLocaleString()} / ${limit.toLocaleString()}`;
  };

  const StatCard = ({ title, value, subtitle, icon: Icon, color, trend }) => (
    <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-sm font-medium text-gray-600">{title}</h3>
          <p className="text-2xl font-bold text-gray-900 mt-2">{value}</p>
          {trend && (
            <div className={`flex items-center mt-2 text-sm ${trend.positive ? 'text-green-600' : 'text-red-600'}`}>
              {trend.positive ? <TrendingUp className="w-4 h-4 mr-1" /> : <TrendingUp className="w-4 h-4 mr-1 transform rotate-180" />}
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
    </div>
  );

  const IntegrationCard = ({ integration }) => {
    const statusConfig = getStatusColor(integration.status);
    const TypeIcon = getTypeIcon(integration.type);
    const StatusIcon = statusConfig.icon;
    
    return (
      <div className="bg-white rounded-lg border border-gray-200 p-6 hover:shadow-md transition-all duration-200">
        {/* Header */}
        <div className="flex items-start justify-between mb-4">
          <div className="flex items-start space-x-3">
            <div 
              className="w-10 h-10 rounded-lg flex items-center justify-center"
              style={{ backgroundColor: theme.primary[500] + '20' }}
            >
              <TypeIcon className="w-5 h-5" style={{ color: theme.primary[500] }} />
            </div>
            <div>
              <h3 className="font-semibold text-gray-900 mb-1">{integration.name}</h3>
              <p className="text-sm text-gray-600 mb-2">{integration.description}</p>
              <p className="text-xs text-gray-500">{integration.provider}</p>
            </div>
          </div>
          
          <div className="flex items-center space-x-2">
            <span className={`px-2 py-1 text-xs font-semibold rounded-full ${statusConfig.bg} ${statusConfig.text}`}>
              {integration.status.toUpperCase()}
            </span>
            <button className="p-1 text-gray-400 hover:text-gray-600">
              <MoreVertical className="w-4 h-4" />
            </button>
          </div>
        </div>

        {/* Metrics */}
        <div className="grid grid-cols-2 gap-4 mb-4">
          <div className="text-center">
            <div className={`text-lg font-bold ${getHealthColor(integration.health)}`}>
              {integration.health}%
            </div>
            <div className="text-xs text-gray-600">Health</div>
          </div>
          <div className="text-center">
            <div className="text-lg font-bold text-blue-600">{integration.endpoints}</div>
            <div className="text-xs text-gray-600">Endpoints</div>
          </div>
        </div>

        {/* Usage */}
        <div className="space-y-2 mb-4">
          <div className="flex justify-between items-center">
            <span className="text-sm text-gray-600">Monthly Usage:</span>
            <span className="text-sm font-medium">
              {formatUsage(integration.monthly_usage, integration.monthly_limit, integration.type)}
            </span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div 
              className={`h-2 rounded-full ${
                (integration.monthly_usage / integration.monthly_limit) * 100 > 80 ? 'bg-red-500' :
                (integration.monthly_usage / integration.monthly_limit) * 100 > 60 ? 'bg-yellow-500' : 'bg-blue-500'
              }`}
              style={{ width: `${Math.min((integration.monthly_usage / integration.monthly_limit) * 100, 100)}%` }}
            ></div>
          </div>
        </div>

        {/* Performance */}
        <div className="space-y-2 mb-4">
          <div className="flex justify-between items-center">
            <span className="text-sm text-gray-600">Error Rate:</span>
            <span className={`text-sm font-medium ${integration.error_rate > 5 ? 'text-red-600' : integration.error_rate > 2 ? 'text-yellow-600' : 'text-green-600'}`}>
              {integration.error_rate}%
            </span>
          </div>
          <div className="flex justify-between items-center">
            <span className="text-sm text-gray-600">Response Time:</span>
            <span className="text-sm font-medium text-blue-600">{integration.avg_response_time}s</span>
          </div>
        </div>

        {/* Actions */}
        <div className="flex items-center justify-between pt-4 border-t border-gray-100">
          <div className="text-xs text-gray-500">
            Last sync: {integration.last_sync.toLocaleString()}
          </div>
          
          <div className="flex space-x-2">
            <button
              onClick={() => navigate(`/admin/integrations/${integration.id}/logs`)}
              className="p-1 hover:bg-gray-100 rounded"
              title="View Logs"
            >
              <Eye className="w-4 h-4 text-blue-600" />
            </button>
            <button
              onClick={() => {
                setSelectedIntegration(integration);
                setShowConfigModal(true);
              }}
              className="p-1 hover:bg-gray-100 rounded"
              title="Configure"
            >
              <Settings className="w-4 h-4 text-green-600" />
            </button>
            <button
              className="p-1 hover:bg-gray-100 rounded"
              title="Test Connection"
            >
              <Zap className="w-4 h-4 text-purple-600" />
            </button>
          </div>
        </div>
      </div>
    );
  };

  const ConfigModal = () => {
    if (!showConfigModal || !selectedIntegration) return null;

    return (
      <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
        <div className="bg-white rounded-lg max-w-2xl w-full max-h-[90vh] overflow-hidden">
          <div className="p-6 border-b border-gray-200">
            <h2 className="text-xl font-bold text-gray-900">Configure Integration</h2>
            <p className="text-sm text-gray-600">{selectedIntegration.name}</p>
          </div>
          
          <div className="p-6 overflow-y-auto max-h-[60vh]">
            <div className="space-y-6">
              <div>
                <h3 className="font-medium text-gray-900 mb-4">Connection Status</h3>
                <div className="grid grid-cols-2 gap-4">
                  <div className="bg-gray-50 p-4 rounded-lg">
                    <div className="text-sm text-gray-600">Health Score</div>
                    <div className={`text-xl font-bold ${getHealthColor(selectedIntegration.health)}`}>
                      {selectedIntegration.health}%
                    </div>
                  </div>
                  <div className="bg-gray-50 p-4 rounded-lg">
                    <div className="text-sm text-gray-600">Last Sync</div>
                    <div className="text-sm font-medium text-gray-900">
                      {selectedIntegration.last_sync.toLocaleString()}
                    </div>
                  </div>
                </div>
              </div>

              <div>
                <h3 className="font-medium text-gray-900 mb-4">Configuration Settings</h3>
                <div className="space-y-4">
                  {Object.entries(selectedIntegration.config).map(([key, value]) => (
                    <div key={key}>
                      <label className="block text-sm font-medium text-gray-700 mb-2 capitalize">
                        {key.replace(/_/g, ' ')}
                      </label>
                      <input
                        type={key.includes('token') || key.includes('key') || key.includes('password') ? 'password' : 'text'}
                        defaultValue={typeof value === 'object' ? JSON.stringify(value) : value}
                        className="w-full px-3 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      />
                    </div>
                  ))}
                </div>
              </div>

              <div>
                <h3 className="font-medium text-gray-900 mb-4">Usage & Limits</h3>
                <div className="bg-gray-50 p-4 rounded-lg">
                  <div className="mb-2">
                    <div className="flex justify-between items-center mb-1">
                      <span className="text-sm text-gray-600">Monthly Usage</span>
                      <span className="text-sm font-medium">
                        {formatUsage(selectedIntegration.monthly_usage, selectedIntegration.monthly_limit, selectedIntegration.type)}
                      </span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div 
                        className={`h-2 rounded-full ${
                          (selectedIntegration.monthly_usage / selectedIntegration.monthly_limit) * 100 > 80 ? 'bg-red-500' :
                          (selectedIntegration.monthly_usage / selectedIntegration.monthly_limit) * 100 > 60 ? 'bg-yellow-500' : 'bg-blue-500'
                        }`}
                        style={{ width: `${Math.min((selectedIntegration.monthly_usage / selectedIntegration.monthly_limit) * 100, 100)}%` }}
                      ></div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <div className="p-6 border-t border-gray-200 flex justify-between">
            <button
              className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
            >
              Test Connection
            </button>
            <div className="flex space-x-3">
              <button
                onClick={() => setShowConfigModal(false)}
                className="px-4 py-2 text-gray-700 hover:bg-gray-100 rounded-lg transition-colors"
              >
                Cancel
              </button>
              <button className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
                Save Changes
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  };

  return (
    <MainLayout portal="solution-admin">
      <div className="h-full flex flex-col">
        {/* Header */}
        <div className="bg-white border-b border-gray-200 px-6 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-xl font-bold text-gray-900">Integration Settings</h1>
              <div className="flex items-center space-x-2 text-sm text-gray-600">
                <Link className="w-3 h-3" />
                <span>{filteredIntegrations.length} integrations</span>
                <span>•</span>
                <span>{integrationsData.filter(i => i.status === 'active').length} active</span>
                <span>•</span>
                <span>{Math.round(integrationsData.reduce((sum, i) => sum + i.health, 0) / integrationsData.length)}% avg health</span>
              </div>
            </div>

            <div className="flex items-center space-x-4">
              {/* View Mode Toggle */}
              <div className="flex items-center space-x-2 bg-gray-100 rounded-lg p-1">
                <button
                  onClick={() => setViewMode('grid')}
                  className={`p-2 rounded transition-colors ${viewMode === 'grid' ? 'bg-white shadow-sm text-blue-600' : 'hover:bg-gray-200'}`}
                >
                  <Grid className="w-4 h-4" />
                </button>
                <button
                  onClick={() => setViewMode('list')}
                  className={`p-2 rounded transition-colors ${viewMode === 'list' ? 'bg-white shadow-sm text-blue-600' : 'hover:bg-gray-200'}`}
                >
                  <List className="w-4 h-4" />
                </button>
              </div>

              <button className="flex items-center space-x-2 px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors">
                <RefreshCw className="w-4 h-4" />
                <span>Sync All</span>
              </button>

              <button className="flex items-center space-x-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
                <Plus className="w-4 h-4" />
                <span>Add Integration</span>
              </button>
            </div>
          </div>
        </div>

        {/* Statistics */}
        <div className="px-6 py-4 bg-gray-50 border-b border-gray-200">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <StatCard
              title="Total Integrations"
              value={integrationsData.length}
              icon={Link}
              color={theme.primary[500]}
            />
            <StatCard
              title="Active Integrations"
              value={integrationsData.filter(i => i.status === 'active').length}
              subtitle="Currently operational"
              icon={CheckCircle}
              color={theme.success[500]}
            />
            <StatCard
              title="Avg Health Score"
              value={`${Math.round(integrationsData.reduce((sum, i) => sum + i.health, 0) / integrationsData.length)}%`}
              subtitle="System-wide health"
              icon={Activity}
              color={theme.warning[500]}
              trend={{ positive: true, value: '+3.2% this month' }}
            />
            <StatCard
              title="API Calls Today"
              value="156.7K"
              subtitle="Across all integrations"
              icon={Globe}
              color={theme.secondary[500]}
            />
          </div>
        </div>

        {/* Filters */}
        <div className="px-6 py-4 bg-white border-b border-gray-200">
          <div className="flex flex-wrap items-center gap-4">
            {/* Search */}
            <div className="flex-1 min-w-64">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
                <input
                  type="text"
                  placeholder="Search integrations, providers..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>
            </div>

            {/* Category Filter */}
            <select
              value={filterCategory}
              onChange={(e) => setFilterCategory(e.target.value)}
              className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="all">All Categories</option>
              <option value="Communication">Communication</option>
              <option value="Storage">Storage</option>
              <option value="API">API</option>
              <option value="External Data">External Data</option>
              <option value="Data">Data</option>
            </select>

            {/* Status Filter */}
            <select
              value={filterStatus}
              onChange={(e) => setFilterStatus(e.target.value)}
              className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="all">All Status</option>
              <option value="active">Active</option>
              <option value="warning">Warning</option>
              <option value="inactive">Inactive</option>
              <option value="error">Error</option>
            </select>
          </div>
        </div>

        {/* Integrations List */}
        <div className="flex-1 overflow-auto">
          <div className="p-6">
            <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
              {filteredIntegrations.map((integration) => (
                <IntegrationCard key={integration.id} integration={integration} />
              ))}
            </div>
          </div>

          {filteredIntegrations.length === 0 && (
            <div className="text-center py-12">
              <Link className="w-12 h-12 text-gray-400 mx-auto mb-4" />
              <h3 className="text-lg font-medium text-gray-900 mb-2">No integrations found</h3>
              <p className="text-gray-600">Try adjusting your search or filter criteria.</p>
            </div>
          )}
        </div>
      </div>

      {/* Configuration Modal */}
      <ConfigModal />
    </MainLayout>
  );
};

export default IntegrationSettings;