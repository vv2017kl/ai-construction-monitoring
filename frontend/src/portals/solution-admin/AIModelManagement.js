import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  Brain, Cpu, Database, Zap, Activity, Settings, Eye,
  Plus, Search, Filter, Edit3, Trash2, MoreVertical,
  Download, Upload, RefreshCw, Grid, List, Play, Pause,
  CheckCircle, XCircle, AlertTriangle, Clock, Calendar,
  TrendingUp, TrendingDown, BarChart3, Target, Award,
  Monitor, Globe, Users, Building2, Camera, Shield,
  ArrowUp, ArrowDown, RotateCcw, Info, AlertCircle
} from 'lucide-react';
import { useTheme } from '../../context/ThemeContext';
import MainLayout from '../../components/shared/Layout/MainLayout';
import { mockSites } from '../../data/mockData';

const AIModelManagement = () => {
  const navigate = useNavigate();
  const { theme } = useTheme();
  
  // State management
  const [searchTerm, setSearchTerm] = useState('');
  const [filterStatus, setFilterStatus] = useState('all');
  const [filterType, setFilterType] = useState('all');
  const [sortBy, setSortBy] = useState('name');
  const [sortOrder, setSortOrder] = useState('asc');
  const [viewMode, setViewMode] = useState('grid');
  const [selectedModel, setSelectedModel] = useState(null);
  const [showDeployModal, setShowDeployModal] = useState(false);
  const [showMetricsModal, setShowMetricsModal] = useState(false);

  // Mock AI models data
  const aiModels = [
    {
      id: 'model_001',
      name: 'PPE Detection v8.2',
      type: 'object_detection',
      category: 'Safety Compliance',
      version: '8.2.1',
      status: 'deployed',
      accuracy: 94.7,
      latency: 125, // ms
      confidence_threshold: 0.85,
      framework: 'YOLOv8',
      deployment_sites: ['site-001', 'site-002'],
      total_detections: 847293,
      false_positives: 2.3,
      false_negatives: 1.8,
      last_training: new Date('2024-11-15'),
      deployment_date: new Date('2024-12-01'),
      model_size: '64.2 MB',
      gpu_utilization: 78,
      cpu_utilization: 34,
      memory_usage: '2.1 GB',
      classes: ['hard_hat', 'safety_vest', 'safety_boots', 'gloves', 'mask'],
      training_images: 125000,
      validation_accuracy: 96.1,
      precision: 93.4,
      recall: 95.8,
      f1_score: 94.6,
      inference_time: 0.125,
      batch_size: 16,
      input_resolution: '640x640'
    },
    {
      id: 'model_002',
      name: 'Equipment Tracking v5.1',
      type: 'object_tracking',
      category: 'Equipment Management',
      version: '5.1.3',
      status: 'deployed',
      accuracy: 91.2,
      latency: 89,
      confidence_threshold: 0.80,
      framework: 'DeepSORT',
      deployment_sites: ['site-001', 'site-003'],
      total_detections: 456781,
      false_positives: 3.7,
      false_negatives: 4.1,
      last_training: new Date('2024-10-20'),
      deployment_date: new Date('2024-11-10'),
      model_size: '89.4 MB',
      gpu_utilization: 82,
      cpu_utilization: 41,
      memory_usage: '3.4 GB',
      classes: ['excavator', 'crane', 'bulldozer', 'truck', 'mixer'],
      training_images: 95000,
      validation_accuracy: 92.8,
      precision: 89.7,
      recall: 92.4,
      f1_score: 91.0,
      inference_time: 0.089,
      batch_size: 8,
      input_resolution: '1024x1024'
    },
    {
      id: 'model_003',
      name: 'Person Detection v7.4',
      type: 'person_detection',
      category: 'Personnel Tracking',
      version: '7.4.2',
      status: 'training',
      accuracy: 97.1,
      latency: 45,
      confidence_threshold: 0.90,
      framework: 'YOLOv9',
      deployment_sites: [],
      total_detections: 0,
      false_positives: 1.2,
      false_negatives: 1.7,
      last_training: new Date('2024-12-08'),
      deployment_date: null,
      model_size: '45.7 MB',
      gpu_utilization: 0,
      cpu_utilization: 0,
      memory_usage: '0 GB',
      classes: ['person', 'worker', 'supervisor', 'visitor'],
      training_images: 200000,
      validation_accuracy: 98.3,
      precision: 96.8,
      recall: 97.4,
      f1_score: 97.1,
      inference_time: 0.045,
      batch_size: 32,
      input_resolution: '416x416'
    },
    {
      id: 'model_004',
      name: 'Safety Violation v3.8',
      type: 'behavior_analysis',
      category: 'Safety Compliance',
      version: '3.8.0',
      status: 'deployed',
      accuracy: 88.4,
      latency: 203,
      confidence_threshold: 0.75,
      framework: 'Custom CNN',
      deployment_sites: ['site-002', 'site-004'],
      total_detections: 234567,
      false_positives: 6.8,
      false_negatives: 4.8,
      last_training: new Date('2024-09-30'),
      deployment_date: new Date('2024-10-15'),
      model_size: '156.3 MB',
      gpu_utilization: 91,
      cpu_utilization: 52,
      memory_usage: '4.8 GB',
      classes: ['unsafe_behavior', 'restricted_area', 'improper_equipment_use'],
      training_images: 85000,
      validation_accuracy: 90.1,
      precision: 86.2,
      recall: 90.7,
      f1_score: 88.4,
      inference_time: 0.203,
      batch_size: 4,
      input_resolution: '1280x720'
    },
    {
      id: 'model_005',
      name: 'Quality Inspection v2.1',
      type: 'defect_detection',
      category: 'Quality Control',
      version: '2.1.5',
      status: 'inactive',
      accuracy: 85.7,
      latency: 340,
      confidence_threshold: 0.70,
      framework: 'ResNet-50',
      deployment_sites: [],
      total_detections: 12450,
      false_positives: 9.2,
      false_negatives: 5.1,
      last_training: new Date('2024-08-15'),
      deployment_date: new Date('2024-09-01'),
      model_size: '234.1 MB',
      gpu_utilization: 0,
      cpu_utilization: 0,
      memory_usage: '0 GB',
      classes: ['crack', 'surface_defect', 'alignment_issue', 'material_defect'],
      training_images: 45000,
      validation_accuracy: 87.3,
      precision: 83.9,
      recall: 87.8,
      f1_score: 85.8,
      inference_time: 0.340,
      batch_size: 2,
      input_resolution: '1920x1080'
    }
  ];

  const [models, setModels] = useState(aiModels);

  // Filter and sort models
  const filteredModels = models
    .filter(model => {
      const matchesSearch = model.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                           model.category.toLowerCase().includes(searchTerm.toLowerCase()) ||
                           model.framework.toLowerCase().includes(searchTerm.toLowerCase());
      const matchesStatus = filterStatus === 'all' || model.status === filterStatus;
      const matchesType = filterType === 'all' || model.type === filterType;
      
      return matchesSearch && matchesStatus && matchesType;
    })
    .sort((a, b) => {
      let aVal = a[sortBy];
      let bVal = b[sortBy];
      
      if (sortBy === 'last_training' || sortBy === 'deployment_date') {
        aVal = aVal ? new Date(aVal) : new Date(0);
        bVal = bVal ? new Date(bVal) : new Date(0);
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
      case 'deployed': return { bg: 'bg-green-100', text: 'text-green-800', dot: 'bg-green-500', icon: CheckCircle };
      case 'training': return { bg: 'bg-blue-100', text: 'text-blue-800', dot: 'bg-blue-500', icon: Activity };
      case 'testing': return { bg: 'bg-yellow-100', text: 'text-yellow-800', dot: 'bg-yellow-500', icon: Clock };
      case 'inactive': return { bg: 'bg-gray-100', text: 'text-gray-800', dot: 'bg-gray-500', icon: XCircle };
      case 'error': return { bg: 'bg-red-100', text: 'text-red-800', dot: 'bg-red-500', icon: AlertTriangle };
      default: return { bg: 'bg-gray-100', text: 'text-gray-800', dot: 'bg-gray-500', icon: Activity };
    }
  };

  const getFrameworkColor = (framework) => {
    switch (framework.toLowerCase()) {
      case 'yolov8':
      case 'yolov9': return 'bg-blue-100 text-blue-800 border-blue-200';
      case 'deepsort': return 'bg-purple-100 text-purple-800 border-purple-200';
      case 'resnet-50': return 'bg-orange-100 text-orange-800 border-orange-200';
      case 'custom cnn': return 'bg-green-100 text-green-800 border-green-200';
      default: return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  const getAccuracyColor = (accuracy) => {
    if (accuracy >= 95) return 'text-green-600';
    if (accuracy >= 90) return 'text-blue-600';
    if (accuracy >= 85) return 'text-yellow-600';
    return 'text-red-600';
  };

  const formatBytes = (bytes) => {
    const sizes = ['B', 'KB', 'MB', 'GB'];
    if (bytes === 0) return '0 B';
    const i = Math.floor(Math.log(bytes) / Math.log(1024));
    return `${(bytes / Math.pow(1024, i)).toFixed(1)} ${sizes[i]}`;
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

  const ModelCard = ({ model }) => {
    const statusConfig = getStatusColor(model.status);
    const StatusIcon = statusConfig.icon;
    
    return (
      <div className="bg-white rounded-lg border border-gray-200 p-6 hover:shadow-md transition-all duration-200">
        {/* Header */}
        <div className="flex items-start justify-between mb-4">
          <div>
            <div className="flex items-center space-x-2 mb-2">
              <Brain className="w-5 h-5" style={{ color: theme.primary[500] }} />
              <h3 className="font-semibold text-gray-900">{model.name}</h3>
            </div>
            <p className="text-sm text-gray-600 mb-2">{model.category}</p>
            <div className="flex items-center space-x-2">
              <span className={`px-2 py-1 text-xs font-medium rounded border ${getFrameworkColor(model.framework)}`}>
                {model.framework}
              </span>
              <span className="text-xs text-gray-500">v{model.version}</span>
            </div>
          </div>
          
          <div className="flex items-center space-x-2">
            <span className={`px-2 py-1 text-xs font-semibold rounded-full ${statusConfig.bg} ${statusConfig.text}`}>
              {model.status.toUpperCase()}
            </span>
            <button className="p-1 text-gray-400 hover:text-gray-600">
              <MoreVertical className="w-4 h-4" />
            </button>
          </div>
        </div>

        {/* Performance Metrics */}
        <div className="grid grid-cols-2 gap-4 mb-4">
          <div className="text-center">
            <div className={`text-lg font-bold ${getAccuracyColor(model.accuracy)}`}>
              {model.accuracy}%
            </div>
            <div className="text-xs text-gray-600">Accuracy</div>
          </div>
          <div className="text-center">
            <div className="text-lg font-bold text-blue-600">{model.latency}ms</div>
            <div className="text-xs text-gray-600">Latency</div>
          </div>
        </div>

        {/* Details */}
        <div className="space-y-2 mb-4">
          <div className="flex justify-between items-center">
            <span className="text-sm text-gray-600">Sites Deployed:</span>
            <span className="text-sm font-medium">{model.deployment_sites.length}</span>
          </div>
          <div className="flex justify-between items-center">
            <span className="text-sm text-gray-600">Model Size:</span>
            <span className="text-sm font-medium">{model.model_size}</span>
          </div>
          <div className="flex justify-between items-center">
            <span className="text-sm text-gray-600">Detections:</span>
            <span className="text-sm font-medium">{model.total_detections.toLocaleString()}</span>
          </div>
          {model.status === 'deployed' && (
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-600">GPU Usage:</span>
              <span className="text-sm font-medium text-orange-600">{model.gpu_utilization}%</span>
            </div>
          )}
        </div>

        {/* Actions */}
        <div className="flex items-center justify-between pt-4 border-t border-gray-100">
          <div className="text-xs text-gray-500">
            {model.deployment_date ? `Deployed ${model.deployment_date.toLocaleDateString()}` : 'Not deployed'}
          </div>
          
          <div className="flex space-x-2">
            <button
              onClick={() => {
                setSelectedModel(model);
                setShowMetricsModal(true);
              }}
              className="p-1 hover:bg-gray-100 rounded"
              title="View Metrics"
            >
              <BarChart3 className="w-4 h-4 text-blue-600" />
            </button>
            <button
              onClick={() => {
                setSelectedModel(model);
                setShowDeployModal(true);
              }}
              className="p-1 hover:bg-gray-100 rounded"
              title="Deploy/Manage"
            >
              <Zap className="w-4 h-4 text-green-600" />
            </button>
            <button
              className="p-1 hover:bg-gray-100 rounded"
              title="Edit Model"
            >
              <Edit3 className="w-4 h-4 text-gray-600" />
            </button>
          </div>
        </div>
      </div>
    );
  };

  const DeploymentModal = () => {
    if (!showDeployModal || !selectedModel) return null;

    return (
      <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
        <div className="bg-white rounded-lg max-w-2xl w-full max-h-[90vh] overflow-hidden">
          <div className="p-6 border-b border-gray-200">
            <h2 className="text-xl font-bold text-gray-900">Deploy AI Model</h2>
            <p className="text-sm text-gray-600">{selectedModel.name}</p>
          </div>
          
          <div className="p-6 overflow-y-auto">
            <div className="space-y-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Target Sites</label>
                <div className="space-y-2 max-h-32 overflow-y-auto border border-gray-200 rounded-lg p-3">
                  {mockSites.map(site => (
                    <label key={site.id} className="flex items-center space-x-2">
                      <input 
                        type="checkbox" 
                        defaultChecked={selectedModel.deployment_sites.includes(site.id)}
                        className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                      />
                      <span className="text-sm">{site.name}</span>
                    </label>
                  ))}
                </div>
              </div>

              <div className="grid grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Confidence Threshold</label>
                  <input
                    type="number"
                    step="0.01"
                    min="0"
                    max="1"
                    defaultValue={selectedModel.confidence_threshold}
                    className="w-full px-3 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Batch Size</label>
                  <input
                    type="number"
                    defaultValue={selectedModel.batch_size}
                    className="w-full px-3 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>
              </div>

              <div>
                <h3 className="font-medium text-gray-900 mb-2">Model Performance</h3>
                <div className="grid grid-cols-2 gap-4 text-sm">
                  <div className="bg-gray-50 p-3 rounded-lg">
                    <div className="text-gray-600">Accuracy</div>
                    <div className="font-bold text-green-600">{selectedModel.accuracy}%</div>
                  </div>
                  <div className="bg-gray-50 p-3 rounded-lg">
                    <div className="text-gray-600">Inference Time</div>
                    <div className="font-bold text-blue-600">{selectedModel.inference_time}s</div>
                  </div>
                  <div className="bg-gray-50 p-3 rounded-lg">
                    <div className="text-gray-600">Precision</div>
                    <div className="font-bold text-purple-600">{selectedModel.precision}%</div>
                  </div>
                  <div className="bg-gray-50 p-3 rounded-lg">
                    <div className="text-gray-600">Recall</div>
                    <div className="font-bold text-orange-600">{selectedModel.recall}%</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <div className="p-6 border-t border-gray-200 flex justify-end space-x-3">
            <button
              onClick={() => setShowDeployModal(false)}
              className="px-4 py-2 text-gray-700 hover:bg-gray-100 rounded-lg transition-colors"
            >
              Cancel
            </button>
            <button className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
              Deploy Model
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
              <h1 className="text-xl font-bold text-gray-900">AI Model Management</h1>
              <div className="flex items-center space-x-2 text-sm text-gray-600">
                <Brain className="w-3 h-3" />
                <span>{filteredModels.length} models</span>
                <span>•</span>
                <span>{models.filter(m => m.status === 'deployed').length} deployed</span>
                <span>•</span>
                <span>{models.reduce((sum, m) => sum + m.total_detections, 0).toLocaleString()} total detections</span>
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

              <button className="flex items-center space-x-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
                <Plus className="w-4 h-4" />
                <span>Upload Model</span>
              </button>
            </div>
          </div>
        </div>

        {/* Statistics */}
        <div className="px-6 py-4 bg-gray-50 border-b border-gray-200">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <StatCard
              title="Total Models"
              value={models.length}
              icon={Brain}
              color={theme.primary[500]}
            />
            <StatCard
              title="Deployed Models"
              value={models.filter(m => m.status === 'deployed').length}
              subtitle="Currently active"
              icon={CheckCircle}
              color={theme.success[500]}
            />
            <StatCard
              title="Avg Accuracy"
              value={`${Math.round(models.reduce((sum, m) => sum + m.accuracy, 0) / models.length)}%`}
              subtitle="Across all models"
              icon={Target}
              color={theme.warning[500]}
              trend={{ positive: true, value: '+2.1% this month' }}
            />
            <StatCard
              title="Total Detections"
              value={`${(models.reduce((sum, m) => sum + m.total_detections, 0) / 1000000).toFixed(1)}M`}
              subtitle="Lifetime detections"
              icon={Activity}
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
                  placeholder="Search models, categories, frameworks..."
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
              <option value="deployed">Deployed</option>
              <option value="training">Training</option>
              <option value="testing">Testing</option>
              <option value="inactive">Inactive</option>
              <option value="error">Error</option>
            </select>

            {/* Type Filter */}
            <select
              value={filterType}
              onChange={(e) => setFilterType(e.target.value)}
              className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="all">All Types</option>
              <option value="object_detection">Object Detection</option>
              <option value="object_tracking">Object Tracking</option>
              <option value="person_detection">Person Detection</option>
              <option value="behavior_analysis">Behavior Analysis</option>
              <option value="defect_detection">Defect Detection</option>
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
              <option value="accuracy-desc">Highest Accuracy</option>
              <option value="latency-asc">Lowest Latency</option>
              <option value="deployment_date-desc">Recently Deployed</option>
              <option value="total_detections-desc">Most Detections</option>
            </select>
          </div>
        </div>

        {/* Models List */}
        <div className="flex-1 overflow-auto">
          <div className="p-6">
            <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
              {filteredModels.map((model) => (
                <ModelCard key={model.id} model={model} />
              ))}
            </div>
          </div>

          {filteredModels.length === 0 && (
            <div className="text-center py-12">
              <Brain className="w-12 h-12 text-gray-400 mx-auto mb-4" />
              <h3 className="text-lg font-medium text-gray-900 mb-2">No AI models found</h3>
              <p className="text-gray-600">Try adjusting your search or filter criteria.</p>
            </div>
          )}
        </div>
      </div>

      {/* Deployment Modal */}
      <DeploymentModal />
    </MainLayout>
  );
};

export default AIModelManagement;