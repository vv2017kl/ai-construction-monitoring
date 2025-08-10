import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  Route, MapPin, Plus, Edit, Trash2, Search, Filter,
  Download, Upload, Settings, Eye, Play, Pause,
  Calendar, Clock, Users, Camera, Navigation,
  Target, Compass, Grid3X3, Layers, Map, Save,
  RefreshCw, Share2, Copy, ExternalLink, AlertTriangle,
  CheckCircle, XCircle, Info, TrendingUp, Activity,
  Zap, Shield, Building2, User, Phone, Mail
} from 'lucide-react';
import { useTheme } from '../../context/ThemeContext';
import MainLayout from '../../components/shared/Layout/MainLayout';
import { mockSites, mockUser, mockPersonnel, mockCameras } from '../../data/mockData';

const PathAdministration = () => {
  const navigate = useNavigate();
  const { theme } = useTheme();
  
  // State management
  const [paths, setPaths] = useState([]);
  const [selectedPath, setSelectedPath] = useState(null);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [showEditModal, setShowEditModal] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterStatus, setFilterStatus] = useState('all');
  const [filterType, setFilterType] = useState('all');
  const [sortBy, setSortBy] = useState('lastModified');
  const [viewMode, setViewMode] = useState('list'); // 'list', 'grid', 'map'

  const currentSite = mockSites.find(s => s.name === mockUser.currentSite) || mockSites[0];

  // Generate mock path data
  const generateMockPaths = () => [
    {
      id: 'path-001',
      name: 'Daily Safety Inspection Route',
      description: 'Comprehensive daily safety inspection covering all construction zones',
      type: 'inspection',
      status: 'active',
      priority: 'high',
      createdBy: 'Sarah Chen',
      assignedTo: 'Safety Team',
      estimatedDuration: '45 minutes',
      distance: '2.3 km',
      waypoints: 12,
      lastModified: new Date(Date.now() - 2 * 60 * 60 * 1000),
      lastUsed: new Date(Date.now() - 4 * 60 * 60 * 1000),
      usageCount: 47,
      completionRate: 98,
      averageTime: 42,
      zones: ['Zone A', 'Zone B', 'Zone C', 'Equipment Yard'],
      coordinates: [
        { x: 15, y: 30, name: 'Main Entrance', type: 'checkpoint' },
        { x: 45, y: 55, name: 'Zone A - Foundation', type: 'inspection' },
        { x: 60, y: 70, name: 'Zone B - Steel Frame', type: 'inspection' },
        { x: 70, y: 35, name: 'Equipment Yard', type: 'checkpoint' }
      ]
    },
    {
      id: 'path-002',
      name: 'Equipment Maintenance Rounds',
      description: 'Weekly equipment inspection and maintenance verification route',
      type: 'maintenance',
      status: 'active',
      priority: 'medium',
      createdBy: 'Mike Rodriguez',
      assignedTo: 'Maintenance Team',
      estimatedDuration: '30 minutes',
      distance: '1.8 km',
      waypoints: 8,
      lastModified: new Date(Date.now() - 1 * 24 * 60 * 60 * 1000),
      lastUsed: new Date(Date.now() - 6 * 60 * 60 * 1000),
      usageCount: 23,
      completionRate: 91,
      averageTime: 28,
      zones: ['Equipment Yard', 'Zone C', 'Storage Area'],
      coordinates: [
        { x: 70, y: 35, name: 'Equipment Yard', type: 'maintenance' },
        { x: 55, y: 80, name: 'Zone C - Excavation', type: 'inspection' },
        { x: 25, y: 85, name: 'Storage Area', type: 'checkpoint' }
      ]
    },
    {
      id: 'path-003',
      name: 'Emergency Evacuation Route A',
      description: 'Primary emergency evacuation route from main construction areas',
      type: 'emergency',
      status: 'active',
      priority: 'critical',
      createdBy: 'John Mitchell',
      assignedTo: 'All Personnel',
      estimatedDuration: '8 minutes',
      distance: '0.9 km',
      waypoints: 5,
      lastModified: new Date(Date.now() - 7 * 24 * 60 * 60 * 1000),
      lastUsed: new Date(Date.now() - 30 * 24 * 60 * 60 * 1000),
      usageCount: 3,
      completionRate: 100,
      averageTime: 7,
      zones: ['Zone A', 'Zone B', 'Main Exit'],
      coordinates: [
        { x: 45, y: 55, name: 'Zone A - Foundation', type: 'evacuation' },
        { x: 30, y: 40, name: 'Assembly Point 1', type: 'assembly' },
        { x: 15, y: 30, name: 'Main Exit', type: 'exit' }
      ]
    },
    {
      id: 'path-004',
      name: 'Quality Control Assessment',
      description: 'Quality control inspection route for construction standards verification',
      type: 'quality',
      status: 'draft',
      priority: 'medium',
      createdBy: 'Emma Thompson',
      assignedTo: 'QC Team',
      estimatedDuration: '60 minutes',
      distance: '2.1 km',
      waypoints: 15,
      lastModified: new Date(Date.now() - 30 * 60 * 1000),
      lastUsed: null,
      usageCount: 0,
      completionRate: 0,
      averageTime: 0,
      zones: ['Zone A', 'Zone B', 'Zone C', 'Zone D'],
      coordinates: [
        { x: 45, y: 55, name: 'Zone A - Foundation', type: 'quality' },
        { x: 60, y: 70, name: 'Zone B - Steel Frame', type: 'quality' },
        { x: 55, y: 80, name: 'Zone C - Excavation', type: 'quality' }
      ]
    },
    {
      id: 'path-005',
      name: 'Visitor Tour Route',
      description: 'Guided tour route for clients and stakeholders visiting the construction site',
      type: 'tour',
      status: 'inactive',
      priority: 'low',
      createdBy: 'John Mitchell',
      assignedTo: 'Site Manager',
      estimatedDuration: '25 minutes',
      distance: '1.5 km',
      waypoints: 6,
      lastModified: new Date(Date.now() - 14 * 24 * 60 * 60 * 1000),
      lastUsed: new Date(Date.now() - 21 * 24 * 60 * 60 * 1000),
      usageCount: 12,
      completionRate: 100,
      averageTime: 23,
      zones: ['Main Entrance', 'Zone A', 'Office Area'],
      coordinates: [
        { x: 15, y: 30, name: 'Main Entrance', type: 'start' },
        { x: 45, y: 55, name: 'Zone A - Foundation', type: 'viewpoint' },
        { x: 25, y: 15, name: 'Office Area', type: 'end' }
      ]
    }
  ];

  useEffect(() => {
    setPaths(generateMockPaths());
  }, []);

  // Filter and sort paths
  const filteredPaths = paths
    .filter(path => {
      const searchMatch = path.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         path.description.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         path.createdBy.toLowerCase().includes(searchTerm.toLowerCase());
      
      const statusMatch = filterStatus === 'all' || path.status === filterStatus;
      const typeMatch = filterType === 'all' || path.type === filterType;
      
      return searchMatch && statusMatch && typeMatch;
    })
    .sort((a, b) => {
      switch (sortBy) {
        case 'name':
          return a.name.localeCompare(b.name);
        case 'usage':
          return b.usageCount - a.usageCount;
        case 'priority':
          const priorityOrder = { critical: 3, high: 2, medium: 1, low: 0 };
          return priorityOrder[b.priority] - priorityOrder[a.priority];
        default: // lastModified
          return new Date(b.lastModified) - new Date(a.lastModified);
      }
    });

  const getStatusColor = (status) => {
    switch (status) {
      case 'active': return { bg: 'bg-green-100', text: 'text-green-800', dot: 'bg-green-500' };
      case 'inactive': return { bg: 'bg-gray-100', text: 'text-gray-800', dot: 'bg-gray-500' };
      case 'draft': return { bg: 'bg-yellow-100', text: 'text-yellow-800', dot: 'bg-yellow-500' };
      case 'archived': return { bg: 'bg-red-100', text: 'text-red-800', dot: 'bg-red-500' };
      default: return { bg: 'bg-gray-100', text: 'text-gray-800', dot: 'bg-gray-500' };
    }
  };

  const getPriorityColor = (priority) => {
    switch (priority) {
      case 'critical': return { bg: 'bg-red-100', text: 'text-red-800' };
      case 'high': return { bg: 'bg-orange-100', text: 'text-orange-800' };
      case 'medium': return { bg: 'bg-blue-100', text: 'text-blue-800' };
      case 'low': return { bg: 'bg-gray-100', text: 'text-gray-800' };
      default: return { bg: 'bg-gray-100', text: 'text-gray-800' };
    }
  };

  const getTypeIcon = (type) => {
    switch (type) {
      case 'inspection': return Shield;
      case 'maintenance': return Settings;
      case 'emergency': return AlertTriangle;
      case 'quality': return CheckCircle;
      case 'tour': return Users;
      default: return Route;
    }
  };

  const formatRelativeTime = (timestamp) => {
    if (!timestamp) return 'Never';
    
    const now = new Date();
    const diff = now - new Date(timestamp);
    const minutes = Math.floor(diff / (1000 * 60));
    const hours = Math.floor(minutes / 60);
    const days = Math.floor(hours / 24);

    if (minutes < 60) return `${minutes}m ago`;
    if (hours < 24) return `${hours}h ago`;
    return `${days}d ago`;
  };

  const PathCard = ({ path }) => {
    const statusConfig = getStatusColor(path.status);
    const priorityConfig = getPriorityColor(path.priority);
    const TypeIcon = getTypeIcon(path.type);
    
    return (
      <div className="bg-white rounded-lg border border-gray-200 p-6 hover:shadow-md transition-all duration-200">
        <div className="flex items-start justify-between mb-4">
          <div className="flex items-start space-x-3">
            <div className="p-2 bg-blue-100 rounded-lg">
              <TypeIcon className="w-5 h-5 text-blue-600" />
            </div>
            <div>
              <h3 className="font-semibold text-gray-900">{path.name}</h3>
              <p className="text-sm text-gray-600 mt-1">{path.description}</p>
            </div>
          </div>
          
          <div className="flex flex-col items-end space-y-2">
            <span className={`px-2 py-1 text-xs font-semibold rounded-full ${statusConfig.bg} ${statusConfig.text}`}>
              {path.status.toUpperCase()}
            </span>
            <span className={`px-2 py-1 text-xs font-semibold rounded-full ${priorityConfig.bg} ${priorityConfig.text}`}>
              {path.priority.toUpperCase()}
            </span>
          </div>
        </div>

        <div className="grid grid-cols-2 gap-4 mb-4">
          <div>
            <div className="flex items-center space-x-2 text-sm text-gray-600">
              <Clock className="w-3 h-3" />
              <span>{path.estimatedDuration}</span>
            </div>
            <div className="flex items-center space-x-2 text-sm text-gray-600">
              <Navigation className="w-3 h-3" />
              <span>{path.distance}</span>
            </div>
          </div>
          <div>
            <div className="flex items-center space-x-2 text-sm text-gray-600">
              <Target className="w-3 h-3" />
              <span>{path.waypoints} waypoints</span>
            </div>
            <div className="flex items-center space-x-2 text-sm text-gray-600">
              <Activity className="w-3 h-3" />
              <span>{path.usageCount} uses</span>
            </div>
          </div>
        </div>

        <div className="flex items-center justify-between text-xs text-gray-500 mb-4">
          <div>
            <span>Created by {path.createdBy}</span>
            <span className="mx-2">•</span>
            <span>Modified {formatRelativeTime(path.lastModified)}</span>
          </div>
          {path.completionRate > 0 && (
            <div className="flex items-center space-x-1">
              <span>Success:</span>
              <span className="font-medium text-green-600">{path.completionRate}%</span>
            </div>
          )}
        </div>

        <div className="flex flex-wrap gap-2 mb-4">
          {path.zones.slice(0, 3).map((zone, index) => (
            <span key={index} className="px-2 py-1 bg-gray-100 text-gray-700 text-xs rounded">
              {zone}
            </span>
          ))}
          {path.zones.length > 3 && (
            <span className="px-2 py-1 bg-gray-100 text-gray-700 text-xs rounded">
              +{path.zones.length - 3} more
            </span>
          )}
        </div>

        <div className="flex items-center justify-between pt-4 border-t border-gray-100">
          <div className="flex items-center space-x-2">
            <User className="w-3 h-3 text-gray-400" />
            <span className="text-sm text-gray-600">{path.assignedTo}</span>
          </div>
          
          <div className="flex space-x-2">
            <button
              onClick={() => {
                setSelectedPath(path);
                setShowEditModal(true);
              }}
              className="p-1 hover:bg-gray-100 rounded"
              title="Edit Path"
            >
              <Edit className="w-4 h-4 text-gray-600" />
            </button>
            <button
              onClick={() => navigate('/field-assessment')}
              className="p-1 hover:bg-gray-100 rounded"
              title="Test Path"
            >
              <Play className="w-4 h-4 text-green-600" />
            </button>
            <button className="p-1 hover:bg-gray-100 rounded" title="Share Path">
              <Share2 className="w-4 h-4 text-blue-600" />
            </button>
          </div>
        </div>
      </div>
    );
  };

  const StatCard = ({ title, value, subtitle, icon: Icon, color }) => (
    <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-sm font-medium text-gray-600">{title}</h3>
          <p className="text-2xl font-bold text-gray-900 mt-2">{value}</p>
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

  const CreatePathModal = () => {
    if (!showCreateModal) return null;

    return (
      <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
        <div className="bg-white rounded-lg max-w-2xl w-full max-h-[90vh] overflow-hidden">
          <div className="p-6 border-b border-gray-200">
            <h2 className="text-xl font-bold text-gray-900">Create New Path</h2>
          </div>
          
          <div className="p-6 overflow-y-auto">
            <div className="grid grid-cols-2 gap-6">
              <div
                className="p-6 border-2 border-dashed border-gray-300 rounded-lg hover:border-blue-400 cursor-pointer transition-colors"
                onClick={() => {
                  setShowCreateModal(false);
                  navigate('/field-assessment');
                }}
              >
                <div className="text-center">
                  <Route className="w-12 h-12 mx-auto mb-4 text-gray-400" />
                  <h3 className="font-semibold text-gray-900 mb-2">Draw New Path</h3>
                  <p className="text-sm text-gray-600">Use field assessment to draw a new path on-site</p>
                </div>
              </div>
              
              <div
                className="p-6 border-2 border-dashed border-gray-300 rounded-lg hover:border-blue-400 cursor-pointer transition-colors"
                onClick={() => {
                  setShowCreateModal(false);
                }}
              >
                <div className="text-center">
                  <Upload className="w-12 h-12 mx-auto mb-4 text-gray-400" />
                  <h3 className="font-semibold text-gray-900 mb-2">Import Path</h3>
                  <p className="text-sm text-gray-600">Import path from GPS data or existing file</p>
                </div>
              </div>
            </div>
            
            <div className="mt-6">
              <h3 className="font-semibold text-gray-900 mb-4">Quick Templates</h3>
              <div className="space-y-3">
                {[
                  { name: 'Safety Inspection Route', type: 'inspection', icon: Shield, zones: 4 },
                  { name: 'Equipment Maintenance Path', type: 'maintenance', icon: Settings, zones: 3 },
                  { name: 'Emergency Evacuation Route', type: 'emergency', icon: AlertTriangle, zones: 2 },
                  { name: 'Quality Control Assessment', type: 'quality', icon: CheckCircle, zones: 5 }
                ].map((template, index) => (
                  <button
                    key={index}
                    className="w-full flex items-center space-x-3 p-3 text-left hover:bg-gray-50 rounded-lg transition-colors"
                    onClick={() => {
                      setShowCreateModal(false);
                    }}
                  >
                    <template.icon className="w-5 h-5 text-gray-600" />
                    <div>
                      <p className="font-medium text-gray-900">{template.name}</p>
                      <p className="text-sm text-gray-600">{template.zones} zones • {template.type} path</p>
                    </div>
                  </button>
                ))}
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
          </div>
        </div>
      </div>
    );
  };

  return (
    <MainLayout portal="solution-user">
      <div className="h-full flex flex-col">
        {/* Header */}
        <div className="bg-white border-b border-gray-200 px-6 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-xl font-bold text-gray-900">Path Administration</h1>
              <div className="flex items-center space-x-2 text-sm text-gray-600">
                <MapPin className="w-3 h-3" />
                <span>{currentSite.name}</span>
                <span>•</span>
                <span>{filteredPaths.length} paths configured</span>
                <span>•</span>
                <span>{filteredPaths.filter(p => p.status === 'active').length} active</span>
              </div>
            </div>

            <div className="flex items-center space-x-4">
              {/* View Mode Toggle */}
              <div className="flex items-center space-x-2 bg-gray-100 rounded-lg p-1">
                {[
                  { key: 'list', label: 'List', icon: Grid3X3 },
                  { key: 'grid', label: 'Grid', icon: Layers },
                  { key: 'map', label: 'Map', icon: Map }
                ].map(({ key, label, icon: Icon }) => (
                  <button
                    key={key}
                    onClick={() => setViewMode(key)}
                    className={`flex items-center space-x-1 px-3 py-1 text-sm rounded transition-colors ${
                      viewMode === key 
                        ? 'bg-white shadow-sm text-blue-600' 
                        : 'hover:bg-gray-200'
                    }`}
                  >
                    <Icon className="w-4 h-4" />
                    <span>{label}</span>
                  </button>
                ))}
              </div>

              <button
                onClick={() => setShowCreateModal(true)}
                className="flex items-center space-x-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
              >
                <Plus className="w-4 h-4" />
                <span>Create Path</span>
              </button>
            </div>
          </div>
        </div>

        {/* Statistics */}
        <div className="px-6 py-4 bg-gray-50 border-b border-gray-200">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <StatCard
              title="Total Paths"
              value={paths.length}
              icon={Route}
              color={theme.primary[500]}
            />
            <StatCard
              title="Active Paths"
              value={paths.filter(p => p.status === 'active').length}
              subtitle="Currently in use"
              icon={CheckCircle}
              color={theme.success[500]}
            />
            <StatCard
              title="Total Usage"
              value={paths.reduce((acc, p) => acc + p.usageCount, 0)}
              subtitle="All time completions"
              icon={TrendingUp}
              color={theme.warning[500]}
            />
            <StatCard
              title="Avg Success Rate"
              value={`${Math.round(paths.reduce((acc, p) => acc + p.completionRate, 0) / paths.length)}%`}
              subtitle="Path completion rate"
              icon={Zap}
              color={theme.secondary[500]}
            />
          </div>
        </div>

        {/* Filters */}
        <div className="px-6 py-4 bg-white border-b border-gray-200">
          <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
            {/* Search */}
            <div className="relative">
              <Search className="w-4 h-4 absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
              <input
                type="text"
                placeholder="Search paths..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-10 pr-4 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:border-transparent"
                style={{ '--tw-ring-color': theme.primary[500] + '40' }}
              />
            </div>

            {/* Status Filter */}
            <select
              value={filterStatus}
              onChange={(e) => setFilterStatus(e.target.value)}
              className="px-3 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:border-transparent"
            >
              <option value="all">All Status</option>
              <option value="active">Active</option>
              <option value="inactive">Inactive</option>
              <option value="draft">Draft</option>
              <option value="archived">Archived</option>
            </select>

            {/* Type Filter */}
            <select
              value={filterType}
              onChange={(e) => setFilterType(e.target.value)}
              className="px-3 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:border-transparent"
            >
              <option value="all">All Types</option>
              <option value="inspection">Inspection</option>
              <option value="maintenance">Maintenance</option>
              <option value="emergency">Emergency</option>
              <option value="quality">Quality Control</option>
              <option value="tour">Tour</option>
            </select>

            {/* Sort */}
            <select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value)}
              className="px-3 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:border-transparent"
            >
              <option value="lastModified">Recently Modified</option>
              <option value="name">Name A-Z</option>
              <option value="usage">Most Used</option>
              <option value="priority">Priority</option>
            </select>

            {/* Bulk Actions */}
            <div className="flex space-x-2">
              <button className="flex items-center space-x-1 px-3 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors">
                <Download className="w-4 h-4" />
                <span>Export</span>
              </button>
              <button className="p-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors">
                <RefreshCw className="w-4 h-4" />
              </button>
            </div>
          </div>
        </div>

        {/* Path List/Grid */}
        <div className="flex-1 overflow-auto">
          {filteredPaths.length === 0 ? (
            <div className="text-center py-12">
              <Route className="w-16 h-16 mx-auto text-gray-400 mb-4" />
              <h3 className="text-lg font-medium text-gray-900 mb-2">No Paths Found</h3>
              <p className="text-gray-600 mb-6">
                {searchTerm || filterStatus !== 'all' || filterType !== 'all'
                  ? 'No paths match your current filters'
                  : 'Get started by creating your first inspection path'}
              </p>
              <button
                onClick={() => setShowCreateModal(true)}
                className="inline-flex items-center space-x-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
              >
                <Plus className="w-4 h-4" />
                <span>Create Path</span>
              </button>
            </div>
          ) : (
            <div className="p-6">
              {viewMode === 'grid' ? (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {filteredPaths.map((path) => (
                    <PathCard key={path.id} path={path} />
                  ))}
                </div>
              ) : viewMode === 'map' ? (
                <div className="bg-white rounded-lg border border-gray-200 p-6">
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">Site Map View</h3>
                  <div className="relative bg-gradient-to-br from-green-100 to-blue-100 rounded-lg h-96 flex items-center justify-center">
                    <div className="text-center text-gray-600">
                      <Map className="w-12 h-12 mx-auto mb-4 opacity-50" />
                      <p>Interactive site map with path visualization</p>
                      <p className="text-sm mt-2">Showing {filteredPaths.length} configured paths</p>
                    </div>
                  </div>
                </div>
              ) : (
                <div className="space-y-4">
                  {filteredPaths.map((path) => (
                    <PathCard key={path.id} path={path} />
                  ))}
                </div>
              )}
            </div>
          )}
        </div>
      </div>

      {/* Create Path Modal */}
      <CreatePathModal />
    </MainLayout>
  );
};

export default PathAdministration;