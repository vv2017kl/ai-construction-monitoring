import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  MapPin, Building2, Settings, Camera, Users, Activity,
  Plus, Search, Filter, Edit3, Trash2, Eye, MoreVertical,
  CheckCircle, XCircle, AlertTriangle, Clock, Calendar,
  Zap, Shield, Wifi, Database, Monitor, HardDrive,
  TrendingUp, TrendingDown, Download, Upload, RefreshCw,
  Grid, List, Map, Navigation, Target, Layers, Globe,
  Construction, Wrench, BarChart3, Award, Crown, Key
} from 'lucide-react';
import { useTheme } from '../../context/ThemeContext';
import MainLayout from '../../components/shared/Layout/MainLayout';
import { mockSites, mockPersonnel, mockCameras, mockZones } from '../../data/mockData';

const SiteConfiguration = () => {
  const navigate = useNavigate();
  const { theme } = useTheme();
  
  // State management
  const [searchTerm, setSearchTerm] = useState('');
  const [filterStatus, setFilterStatus] = useState('all');
  const [filterType, setFilterType] = useState('all');
  const [sortBy, setSortBy] = useState('name');
  const [sortOrder, setSortOrder] = useState('asc');
  const [viewMode, setViewMode] = useState('grid');
  const [selectedSite, setSelectedSite] = useState(null);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [showEditModal, setShowEditModal] = useState(false);
  const [showZoneModal, setShowZoneModal] = useState(false);
  const [activeTab, setActiveTab] = useState('overview'); // 'overview', 'zones', 'cameras', 'personnel'

  // Extended mock site data for admin configuration
  const extendedSites = [
    {
      ...mockSites[0],
      configuration: {
        timezone: 'America/New_York',
        workingHours: { start: '06:00', end: '18:00' },
        maxOccupancy: 150,
        safetyLevel: 'standard',
        aiDetection: true,
        recordingRetention: 30, // days
        alertNotifications: true,
        emergencyContacts: [
          { name: 'Site Safety Officer', phone: '+1-555-0199' },
          { name: 'Project Manager', phone: '+1-555-0167' }
        ]
      },
      infrastructure: {
        networkStatus: 'excellent',
        powerStatus: 'stable',
        internetSpeed: '1000 Mbps',
        backupPower: true,
        weatherStation: true,
        accessControl: 'biometric'
      },
      zones: 4,
      activeAlerts: 3,
      systemHealth: 95,
      lastMaintenance: new Date('2024-12-01'),
      nextMaintenance: new Date('2025-01-15'),
      complianceScore: 92,
      securityLevel: 'high'
    },
    {
      ...mockSites[1],
      configuration: {
        timezone: 'America/New_York',
        workingHours: { start: '07:00', end: '17:00' },
        maxOccupancy: 80,
        safetyLevel: 'high',
        aiDetection: true,
        recordingRetention: 45,
        alertNotifications: true,
        emergencyContacts: [
          { name: 'Safety Coordinator', phone: '+1-555-0188' }
        ]
      },
      infrastructure: {
        networkStatus: 'good',
        powerStatus: 'stable',
        internetSpeed: '500 Mbps',
        backupPower: true,
        weatherStation: false,
        accessControl: 'keycard'
      },
      zones: 3,
      activeAlerts: 1,
      systemHealth: 88,
      lastMaintenance: new Date('2024-11-20'),
      nextMaintenance: new Date('2025-01-10'),
      complianceScore: 96,
      securityLevel: 'medium'
    },
    {
      ...mockSites[2],
      configuration: {
        timezone: 'America/New_York',
        workingHours: { start: '06:30', end: '16:30' },
        maxOccupancy: 200,
        safetyLevel: 'critical',
        aiDetection: false,
        recordingRetention: 60,
        alertNotifications: true,
        emergencyContacts: [
          { name: 'Industrial Safety Manager', phone: '+1-555-0177' },
          { name: 'Emergency Response', phone: '+1-555-0911' }
        ]
      },
      infrastructure: {
        networkStatus: 'fair',
        powerStatus: 'backup_active',
        internetSpeed: '250 Mbps',
        backupPower: true,
        weatherStation: true,
        accessControl: 'manual'
      },
      zones: 6,
      activeAlerts: 0,
      systemHealth: 72,
      lastMaintenance: new Date('2024-10-15'),
      nextMaintenance: new Date('2025-01-20'),
      complianceScore: 78,
      securityLevel: 'critical'
    },
    // Additional sites for demo
    {
      id: 'site-004',
      name: 'Harbor Bridge Extension',
      code: 'HBE-004',
      address: '800 Harbor Drive, Marina District, NY 10004',
      status: 'active',
      type: 'infrastructure',
      phase: 'foundation',
      progress: 35,
      cameras: 20,
      personnel: 65,
      weather: { temp: 68, condition: 'Overcast', wind: '10 mph' },
      lastActivity: '30 minutes ago',
      coordinates: { lat: 40.7505, lng: -73.9934 },
      manager: 'Jennifer Walsh',
      budget: 24500000,
      completion: '2025-09-30',
      configuration: {
        timezone: 'America/New_York',
        workingHours: { start: '05:30', end: '19:30' },
        maxOccupancy: 120,
        safetyLevel: 'critical',
        aiDetection: true,
        recordingRetention: 90,
        alertNotifications: true,
        emergencyContacts: [
          { name: 'Marine Safety Officer', phone: '+1-555-0145' }
        ]
      },
      infrastructure: {
        networkStatus: 'excellent',
        powerStatus: 'stable',
        internetSpeed: '1500 Mbps',
        backupPower: true,
        weatherStation: true,
        accessControl: 'biometric'
      },
      zones: 8,
      activeAlerts: 2,
      systemHealth: 98,
      lastMaintenance: new Date('2024-12-05'),
      nextMaintenance: new Date('2025-01-25'),
      complianceScore: 99,
      securityLevel: 'high'
    }
  ];

  const [sites, setSites] = useState(extendedSites);

  // Filter and sort sites
  const filteredSites = sites
    .filter(site => {
      const matchesSearch = site.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                           site.address.toLowerCase().includes(searchTerm.toLowerCase()) ||
                           site.manager.toLowerCase().includes(searchTerm.toLowerCase());
      const matchesStatus = filterStatus === 'all' || site.status === filterStatus;
      const matchesType = filterType === 'all' || site.type === filterType;
      
      return matchesSearch && matchesStatus && matchesType;
    })
    .sort((a, b) => {
      let aVal = a[sortBy];
      let bVal = b[sortBy];
      
      if (sortBy === 'lastActivity') {
        // Convert relative time to comparable format
        aVal = new Date(); 
        bVal = new Date();
      }
      
      if (typeof aVal === 'string') {
        aVal = aVal.toLowerCase();
        bVal = bVal.toLowerCase();
      }
      
      const comparison = aVal < bVal ? -1 : aVal > bVal ? 1 : 0;
      return sortOrder === 'asc' ? comparison : -comparison;
    });

  const getStatusColor = (status) => {
    switch (status) {
      case 'active': return { bg: 'bg-green-100', text: 'text-green-800', dot: 'bg-green-500' };
      case 'maintenance': return { bg: 'bg-yellow-100', text: 'text-yellow-800', dot: 'bg-yellow-500' };
      case 'planning': return { bg: 'bg-blue-100', text: 'text-blue-800', dot: 'bg-blue-500' };
      case 'inactive': return { bg: 'bg-gray-100', text: 'text-gray-800', dot: 'bg-gray-500' };
      default: return { bg: 'bg-gray-100', text: 'text-gray-800', dot: 'bg-gray-500' };
    }
  };

  const getHealthColor = (health) => {
    if (health >= 90) return 'text-green-600';
    if (health >= 80) return 'text-yellow-600';
    if (health >= 70) return 'text-orange-600';
    return 'text-red-600';
  };

  const getInfrastructureStatus = (status) => {
    switch (status) {
      case 'excellent': return { color: 'text-green-600', bg: 'bg-green-100' };
      case 'good': return { color: 'text-blue-600', bg: 'bg-blue-100' };
      case 'fair': return { color: 'text-yellow-600', bg: 'bg-yellow-100' };
      case 'poor': return { color: 'text-red-600', bg: 'bg-red-100' };
      default: return { color: 'text-gray-600', bg: 'bg-gray-100' };
    }
  };

  const StatCard = ({ title, value, subtitle, icon: Icon, color, trend }) => (
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
    </div>
  );

  const SiteCard = ({ site }) => {
    const statusConfig = getStatusColor(site.status);
    const networkConfig = getInfrastructureStatus(site.infrastructure.networkStatus);
    
    return (
      <div className="bg-white rounded-lg border border-gray-200 p-6 hover:shadow-md transition-all duration-200">
        {/* Header */}
        <div className="flex items-start justify-between mb-4">
          <div>
            <div className="flex items-center space-x-2 mb-2">
              <Building2 className="w-5 h-5 text-gray-600" />
              <h3 className="font-semibold text-gray-900">{site.name}</h3>
              <span className={`px-2 py-1 text-xs font-semibold rounded-full ${statusConfig.bg} ${statusConfig.text}`}>
                {site.status.toUpperCase()}
              </span>
            </div>
            <p className="text-sm text-gray-600 mb-2">{site.address}</p>
            <div className="flex items-center space-x-2 text-sm text-gray-500">
              <Crown className="w-3 h-3" />
              <span>{site.manager}</span>
            </div>
          </div>
          
          <button className="p-1 text-gray-400 hover:text-gray-600">
            <MoreVertical className="w-4 h-4" />
          </button>
        </div>

        {/* Progress & Metrics */}
        <div className="grid grid-cols-3 gap-4 mb-4">
          <div className="text-center">
            <div className="text-lg font-bold text-blue-600">{site.progress}%</div>
            <div className="text-xs text-gray-600">Progress</div>
          </div>
          <div className="text-center">
            <div className="text-lg font-bold text-green-600">{site.cameras}</div>
            <div className="text-xs text-gray-600">Cameras</div>
          </div>
          <div className="text-center">
            <div className="text-lg font-bold text-purple-600">{site.zones}</div>
            <div className="text-xs text-gray-600">Zones</div>
          </div>
        </div>

        {/* Infrastructure Status */}
        <div className="space-y-2 mb-4">
          <div className="flex justify-between items-center">
            <span className="text-sm text-gray-600">Network:</span>
            <span className={`px-2 py-1 text-xs font-medium rounded ${networkConfig.bg} ${networkConfig.color}`}>
              {site.infrastructure.networkStatus.toUpperCase()}
            </span>
          </div>
          <div className="flex justify-between items-center">
            <span className="text-sm text-gray-600">System Health:</span>
            <span className={`font-bold ${getHealthColor(site.systemHealth)}`}>
              {site.systemHealth}%
            </span>
          </div>
          <div className="flex justify-between items-center">
            <span className="text-sm text-gray-600">Compliance:</span>
            <span className={`font-bold ${getHealthColor(site.complianceScore)}`}>
              {site.complianceScore}%
            </span>
          </div>
        </div>

        {/* Alerts & Personnel */}
        <div className="flex items-center justify-between pt-4 border-t border-gray-100">
          <div className="flex items-center space-x-4 text-sm">
            <div className="flex items-center space-x-1">
              <Users className="w-3 h-3 text-gray-500" />
              <span>{site.personnel}</span>
            </div>
            {site.activeAlerts > 0 && (
              <div className="flex items-center space-x-1 text-red-600">
                <AlertTriangle className="w-3 h-3" />
                <span>{site.activeAlerts} alerts</span>
              </div>
            )}
          </div>
          
          <div className="flex space-x-2">
            <button
              onClick={() => {
                setSelectedSite(site);
                setActiveTab('overview');
                navigate(`/admin/site-config/${site.id}`);
              }}
              className="p-1 hover:bg-gray-100 rounded"
              title="Configure Site"
            >
              <Settings className="w-4 h-4 text-blue-600" />
            </button>
            <button
              onClick={() => navigate(`/admin/site-config/${site.id}/zones`)}
              className="p-1 hover:bg-gray-100 rounded"
              title="Manage Zones"
            >
              <Map className="w-4 h-4 text-green-600" />
            </button>
            <button
              onClick={() => navigate(`/admin/site-config/${site.id}/cameras`)}
              className="p-1 hover:bg-gray-100 rounded"
              title="Camera Setup"
            >
              <Camera className="w-4 h-4 text-purple-600" />
            </button>
          </div>
        </div>
      </div>
    );
  };

  const CreateSiteModal = () => {
    if (!showCreateModal) return null;

    return (
      <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
        <div className="bg-white rounded-lg max-w-3xl w-full max-h-[90vh] overflow-hidden">
          <div className="p-6 border-b border-gray-200">
            <h2 className="text-xl font-bold text-gray-900">Add New Construction Site</h2>
          </div>
          
          <div className="p-6 overflow-y-auto max-h-[70vh]">
            <div className="space-y-6">
              {/* Basic Information */}
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Basic Information</h3>
                <div className="grid grid-cols-2 gap-6">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Site Name</label>
                    <input
                      type="text"
                      className="w-full px-3 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      placeholder="Enter site name"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Site Code</label>
                    <input
                      type="text"
                      className="w-full px-3 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      placeholder="e.g. DTP-001"
                    />
                  </div>
                  <div className="col-span-2">
                    <label className="block text-sm font-medium text-gray-700 mb-2">Address</label>
                    <input
                      type="text"
                      className="w-full px-3 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      placeholder="Enter complete address"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Site Type</label>
                    <select className="w-full px-3 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
                      <option value="commercial">Commercial</option>
                      <option value="residential">Residential</option>
                      <option value="industrial">Industrial</option>
                      <option value="infrastructure">Infrastructure</option>
                    </select>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Project Manager</label>
                    <select className="w-full px-3 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
                      <option value="">Select manager...</option>
                      {mockPersonnel.map(person => (
                        <option key={person.id} value={person.id}>{person.name}</option>
                      ))}
                    </select>
                  </div>
                </div>
              </div>

              {/* Configuration */}
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Site Configuration</h3>
                <div className="grid grid-cols-2 gap-6">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Timezone</label>
                    <select className="w-full px-3 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
                      <option value="America/New_York">Eastern Time (EST/EDT)</option>
                      <option value="America/Chicago">Central Time (CST/CDT)</option>
                      <option value="America/Denver">Mountain Time (MST/MDT)</option>
                      <option value="America/Los_Angeles">Pacific Time (PST/PDT)</option>
                    </select>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Max Occupancy</label>
                    <input
                      type="number"
                      className="w-full px-3 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      placeholder="150"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Working Hours Start</label>
                    <input
                      type="time"
                      className="w-full px-3 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      defaultValue="06:00"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Working Hours End</label>
                    <input
                      type="time"
                      className="w-full px-3 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      defaultValue="18:00"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Safety Level</label>
                    <select className="w-full px-3 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
                      <option value="standard">Standard</option>
                      <option value="high">High</option>
                      <option value="critical">Critical</option>
                    </select>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Recording Retention (days)</label>
                    <input
                      type="number"
                      className="w-full px-3 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      placeholder="30"
                    />
                  </div>
                </div>
              </div>

              {/* Features */}
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Features & Settings</h3>
                <div className="space-y-4">
                  <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                    <div>
                      <h4 className="font-medium text-gray-900">AI Detection</h4>
                      <p className="text-sm text-gray-600">Enable AI-powered safety and security detection</p>
                    </div>
                    <label className="relative inline-flex items-center cursor-pointer">
                      <input type="checkbox" className="sr-only peer" defaultChecked />
                      <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
                    </label>
                  </div>
                  
                  <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                    <div>
                      <h4 className="font-medium text-gray-900">Alert Notifications</h4>
                      <p className="text-sm text-gray-600">Send real-time alerts via email and SMS</p>
                    </div>
                    <label className="relative inline-flex items-center cursor-pointer">
                      <input type="checkbox" className="sr-only peer" defaultChecked />
                      <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
                    </label>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <div className="p-6 border-t border-gray-200 flex justify-end space-x-3">
            <button
              onClick={() => setShowCreateModal(false)}
              className="px-4 py-2 text-gray-700 hover:bg-gray-100 rounded-lg transition-colors"
            >
              Cancel
            </button>
            <button className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
              Create Site
            </button>
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
              <h1 className="text-xl font-bold text-gray-900">Site Configuration</h1>
              <div className="flex items-center space-x-2 text-sm text-gray-600">
                <Globe className="w-3 h-3" />
                <span>{filteredSites.length} sites</span>
                <span>•</span>
                <span>{sites.reduce((sum, site) => sum + site.personnel, 0)} total personnel</span>
                <span>•</span>
                <span>{sites.reduce((sum, site) => sum + site.cameras, 0)} cameras deployed</span>
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
                <Download className="w-4 h-4" />
                <span>Export</span>
              </button>

              <button
                onClick={() => setShowCreateModal(true)}
                className="flex items-center space-x-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
              >
                <Plus className="w-4 h-4" />
                <span>Add Site</span>
              </button>
            </div>
          </div>
        </div>

        {/* Statistics */}
        <div className="px-6 py-4 bg-gray-50 border-b border-gray-200">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <StatCard
              title="Total Sites"
              value={sites.length}
              icon={Building2}
              color={theme.primary[500]}
            />
            <StatCard
              title="Active Sites"
              value={sites.filter(site => site.status === 'active').length}
              subtitle="Currently operational"
              icon={CheckCircle}
              color={theme.success[500]}
            />
            <StatCard
              title="Critical Alerts"
              value={sites.reduce((sum, site) => sum + site.activeAlerts, 0)}
              subtitle="Requiring attention"
              icon={AlertTriangle}
              color={theme.danger[500]}
            />
            <StatCard
              title="Avg System Health"
              value={`${Math.round(sites.reduce((sum, site) => sum + site.systemHealth, 0) / sites.length)}%`}
              subtitle="Across all sites"
              icon={Monitor}
              color={theme.warning[500]}
              trend={{ positive: true, value: '+2.3% this month' }}
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
                  placeholder="Search sites, addresses, managers..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>
            </div>

            {/* Status Filter */}
            <select
              value={filterStatus}
              onChange={(e) => setFilterStatus(e.target.value)}
              className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="all">All Status</option>
              <option value="active">Active</option>
              <option value="maintenance">Maintenance</option>
              <option value="planning">Planning</option>
              <option value="inactive">Inactive</option>
            </select>

            {/* Type Filter */}
            <select
              value={filterType}
              onChange={(e) => setFilterType(e.target.value)}
              className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="all">All Types</option>
              <option value="commercial">Commercial</option>
              <option value="residential">Residential</option>
              <option value="industrial">Industrial</option>
              <option value="infrastructure">Infrastructure</option>
            </select>

            {/* Sort */}
            <select
              value={`${sortBy}-${sortOrder}`}
              onChange={(e) => {
                const [field, order] = e.target.value.split('-');
                setSortBy(field);
                setSortOrder(order);
              }}
              className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="name-asc">Name A-Z</option>
              <option value="name-desc">Name Z-A</option>
              <option value="progress-desc">Highest Progress</option>
              <option value="systemHealth-desc">Best Health</option>
              <option value="personnel-desc">Most Personnel</option>
            </select>
          </div>
        </div>

        {/* Site List */}
        <div className="flex-1 overflow-auto">
          {viewMode === 'grid' ? (
            <div className="p-6">
              <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
                {filteredSites.map((site) => (
                  <SiteCard key={site.id} site={site} />
                ))}
              </div>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-gray-50 border-b border-gray-200">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Site</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Manager</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Progress</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Health</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Personnel</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Cameras</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {filteredSites.map((site) => {
                    const statusConfig = getStatusColor(site.status);
                    
                    return (
                      <tr key={site.id} className="hover:bg-gray-50">
                        <td className="px-6 py-4">
                          <div className="flex items-center space-x-3">
                            <Building2 className="w-5 h-5 text-gray-400" />
                            <div>
                              <div className="font-medium text-gray-900">{site.name}</div>
                              <div className="text-sm text-gray-500">{site.code}</div>
                            </div>
                          </div>
                        </td>
                        <td className="px-6 py-4 text-sm text-gray-900">{site.manager}</td>
                        <td className="px-6 py-4">
                          <div className="flex items-center">
                            <span className="text-sm font-medium text-gray-900 mr-2">{site.progress}%</span>
                            <div className="w-16 bg-gray-200 rounded-full h-2">
                              <div 
                                className="bg-blue-600 h-2 rounded-full" 
                                style={{ width: `${site.progress}%` }}
                              ></div>
                            </div>
                          </div>
                        </td>
                        <td className="px-6 py-4">
                          <span className={`font-medium ${getHealthColor(site.systemHealth)}`}>
                            {site.systemHealth}%
                          </span>
                        </td>
                        <td className="px-6 py-4 text-sm text-gray-900">{site.personnel}</td>
                        <td className="px-6 py-4 text-sm text-gray-900">{site.cameras}</td>
                        <td className="px-6 py-4">
                          <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-semibold ${statusConfig.bg} ${statusConfig.text}`}>
                            <span className={`w-1.5 h-1.5 rounded-full mr-2 ${statusConfig.dot}`}></span>
                            {site.status}
                          </span>
                        </td>
                        <td className="px-6 py-4">
                          <div className="flex items-center space-x-2">
                            <button
                              className="p-1 text-blue-600 hover:bg-blue-50 rounded transition-colors"
                              title="Configure Site"
                            >
                              <Settings className="w-4 h-4" />
                            </button>
                            <button
                              className="p-1 text-green-600 hover:bg-green-50 rounded transition-colors"
                              title="Manage Zones"
                            >
                              <Map className="w-4 h-4" />
                            </button>
                            <button
                              className="p-1 text-purple-600 hover:bg-purple-50 rounded transition-colors"
                              title="Camera Setup"
                            >
                              <Camera className="w-4 h-4" />
                            </button>
                          </div>
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          )}

          {filteredSites.length === 0 && (
            <div className="text-center py-12">
              <Building2 className="w-12 h-12 text-gray-400 mx-auto mb-4" />
              <h3 className="text-lg font-medium text-gray-900 mb-2">No sites found</h3>
              <p className="text-gray-600">Try adjusting your search or filter criteria.</p>
            </div>
          )}
        </div>
      </div>

      {/* Create Site Modal */}
      <CreateSiteModal />
    </MainLayout>
  );
};

export default SiteConfiguration;