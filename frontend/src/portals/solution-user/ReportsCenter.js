import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  FileText, Download, Calendar, Filter, Search, Share2,
  BarChart3, TrendingUp, Clock, MapPin, Users, Shield,
  AlertTriangle, CheckCircle, Eye, Edit, Trash2, Plus,
  Layout, PieChart, LineChart, Activity, Building2,
  Camera, HardHat, Wrench, Zap, RefreshCw, Settings
} from 'lucide-react';
import { useTheme } from '../../context/ThemeContext';
import MainLayout from '../../components/shared/Layout/MainLayout';
import { mockReports, mockSites, mockUser } from '../../data/mockData';

const ReportsCenter = () => {
  const navigate = useNavigate();
  const { theme } = useTheme();
  
  // State management
  const [reports, setReports] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterType, setFilterType] = useState('all');
  const [filterStatus, setFilterStatus] = useState('all');
  const [filterDateRange, setFilterDateRange] = useState('all');
  const [sortBy, setSortBy] = useState('createdAt');
  const [sortOrder, setSortOrder] = useState('desc');
  const [selectedReports, setSelectedReports] = useState([]);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [viewMode, setViewMode] = useState('grid'); // 'grid', 'list'

  const currentSite = mockSites.find(s => s.name === mockUser.currentSite) || mockSites[0];

  // Generate mock reports data
  const generateMockReports = () => [
    {
      id: 'r001',
      title: 'Daily Safety Report',
      type: 'safety',
      description: 'Comprehensive daily safety metrics and incident reports',
      status: 'completed',
      createdAt: new Date(Date.now() - 2 * 60 * 60 * 1000),
      updatedAt: new Date(Date.now() - 1 * 60 * 60 * 1000),
      author: 'Sarah Chen',
      fileSize: '2.1 MB',
      format: 'PDF',
      pages: 12,
      downloads: 45,
      schedule: 'daily',
      tags: ['safety', 'compliance', 'incidents'],
      preview: true
    },
    {
      id: 'r002',
      title: 'Weekly Personnel Analytics',
      type: 'personnel',
      description: 'Personnel productivity, attendance, and performance metrics',
      status: 'completed',
      createdAt: new Date(Date.now() - 24 * 60 * 60 * 1000),
      updatedAt: new Date(Date.now() - 22 * 60 * 60 * 1000),
      author: 'John Mitchell',
      fileSize: '5.7 MB',
      format: 'XLSX',
      pages: null,
      downloads: 23,
      schedule: 'weekly',
      tags: ['personnel', 'productivity', 'attendance'],
      preview: false
    },
    {
      id: 'r003',
      title: 'AI Detection Summary',
      type: 'ai_analytics',
      description: 'AI detection accuracy, false positives, and model performance',
      status: 'processing',
      createdAt: new Date(Date.now() - 30 * 60 * 1000),
      updatedAt: new Date(Date.now() - 15 * 60 * 1000),
      author: 'System Generated',
      fileSize: null,
      format: 'PDF',
      pages: null,
      downloads: 0,
      schedule: 'real-time',
      tags: ['ai', 'detection', 'performance'],
      preview: false
    },
    {
      id: 'r004',
      title: 'Equipment Utilization Report',
      type: 'equipment',
      description: 'Equipment usage, maintenance schedules, and efficiency metrics',
      status: 'completed',
      createdAt: new Date(Date.now() - 7 * 24 * 60 * 60 * 1000),
      updatedAt: new Date(Date.now() - 7 * 24 * 60 * 60 * 1000),
      author: 'Mike Rodriguez',
      fileSize: '3.2 MB',
      format: 'PDF',
      pages: 18,
      downloads: 67,
      schedule: 'weekly',
      tags: ['equipment', 'utilization', 'maintenance'],
      preview: true
    },
    {
      id: 'r005',
      title: 'Construction Progress Report',
      type: 'progress',
      description: 'Project milestones, completion rates, and timeline analysis',
      status: 'completed',
      createdAt: new Date(Date.now() - 3 * 24 * 60 * 60 * 1000),
      updatedAt: new Date(Date.now() - 3 * 24 * 60 * 60 * 1000),
      author: 'Emma Thompson',
      fileSize: '8.4 MB',
      format: 'PDF',
      pages: 25,
      downloads: 112,
      schedule: 'weekly',
      tags: ['progress', 'milestones', 'timeline'],
      preview: true
    },
    {
      id: 'r006',
      title: 'Compliance Audit Report',
      type: 'compliance',
      description: 'Regulatory compliance status and audit findings',
      status: 'draft',
      createdAt: new Date(Date.now() - 4 * 60 * 60 * 1000),
      updatedAt: new Date(Date.now() - 1 * 60 * 60 * 1000),
      author: 'Sarah Chen',
      fileSize: null,
      format: 'PDF',
      pages: null,
      downloads: 0,
      schedule: 'monthly',
      tags: ['compliance', 'audit', 'regulatory'],
      preview: false
    }
  ];

  useEffect(() => {
    setReports(generateMockReports());
  }, []);

  // Filter and sort reports
  const filteredReports = reports
    .filter(report => {
      const searchMatch = report.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         report.description.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         report.author.toLowerCase().includes(searchTerm.toLowerCase());
      
      const typeMatch = filterType === 'all' || report.type === filterType;
      const statusMatch = filterStatus === 'all' || report.status === filterStatus;
      
      let dateMatch = true;
      if (filterDateRange !== 'all') {
        const now = new Date();
        const reportDate = new Date(report.createdAt);
        const daysDiff = Math.floor((now - reportDate) / (1000 * 60 * 60 * 24));
        
        switch (filterDateRange) {
          case 'today': dateMatch = daysDiff === 0; break;
          case 'week': dateMatch = daysDiff <= 7; break;
          case 'month': dateMatch = daysDiff <= 30; break;
          default: dateMatch = true;
        }
      }
      
      return searchMatch && typeMatch && statusMatch && dateMatch;
    })
    .sort((a, b) => {
      let aValue = a[sortBy];
      let bValue = b[sortBy];
      
      if (sortBy === 'createdAt' || sortBy === 'updatedAt') {
        aValue = new Date(aValue);
        bValue = new Date(bValue);
      }
      
      if (typeof aValue === 'string') {
        aValue = aValue.toLowerCase();
        bValue = bValue.toLowerCase();
      }
      
      const comparison = aValue < bValue ? -1 : aValue > bValue ? 1 : 0;
      return sortOrder === 'asc' ? comparison : -comparison;
    });

  const getStatusColor = (status) => {
    switch (status) {
      case 'completed': return { bg: 'bg-green-100', text: 'text-green-800', icon: CheckCircle };
      case 'processing': return { bg: 'bg-yellow-100', text: 'text-yellow-800', icon: Clock };
      case 'draft': return { bg: 'bg-gray-100', text: 'text-gray-800', icon: Edit };
      case 'error': return { bg: 'bg-red-100', text: 'text-red-800', icon: AlertTriangle };
      default: return { bg: 'bg-gray-100', text: 'text-gray-800', icon: FileText };
    }
  };

  const getTypeIcon = (type) => {
    switch (type) {
      case 'safety': return Shield;
      case 'personnel': return Users;
      case 'ai_analytics': return Activity;
      case 'equipment': return Wrench;
      case 'progress': return TrendingUp;
      case 'compliance': return CheckCircle;
      default: return FileText;
    }
  };

  const getTypeColor = (type) => {
    switch (type) {
      case 'safety': return theme.danger[500];
      case 'personnel': return theme.primary[500];
      case 'ai_analytics': return theme.success[500];
      case 'equipment': return theme.warning[500];
      case 'progress': return theme.primary[600]; // Using primary variant instead of non-existent info
      case 'compliance': return theme.secondary[500];
      default: return theme.secondary[600]; // Using secondary instead of non-existent gray
    }
  };

  const formatFileSize = (bytes) => {
    if (!bytes || bytes === 0) return 'N/A';
    const sizes = ['B', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(1024));
    return Math.round(bytes / Math.pow(1024, i) * 100) / 100 + ' ' + sizes[i];
  };

  const formatDate = (date) => {
    return new Date(date).toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const StatCard = ({ title, value, subtitle, icon: Icon, color, onClick }) => (
    <div 
      className="bg-white rounded-xl p-6 shadow-sm border border-gray-100 hover:shadow-md transition-all duration-200 cursor-pointer"
      onClick={onClick}
    >
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

  const ReportCard = ({ report }) => {
    const statusConfig = getStatusColor(report.status);
    const TypeIcon = getTypeIcon(report.type);
    const StatusIcon = statusConfig.icon;
    
    return (
      <div className="bg-white rounded-lg border border-gray-200 p-6 hover:shadow-md transition-all duration-200">
        <div className="flex items-start justify-between mb-4">
          <div className="flex items-center space-x-3">
            <div 
              className="p-2 rounded-lg"
              style={{ backgroundColor: getTypeColor(report.type) + '20' }}
            >
              <TypeIcon className="w-5 h-5" style={{ color: getTypeColor(report.type) }} />
            </div>
            <div>
              <h3 className="font-semibold text-gray-900">{report.title}</h3>
              <p className="text-sm text-gray-600 capitalize">{report.type.replace('_', ' ')}</p>
            </div>
          </div>
          <span className={`px-2 py-1 text-xs font-semibold rounded-full ${statusConfig.bg} ${statusConfig.text}`}>
            {report.status.toUpperCase()}
          </span>
        </div>

        <p className="text-sm text-gray-600 mb-4 line-clamp-2">{report.description}</p>

        <div className="flex items-center justify-between text-xs text-gray-500 mb-4">
          <div className="flex items-center space-x-4">
            <span>By {report.author}</span>
            <span>{formatDate(report.createdAt)}</span>
          </div>
          {report.fileSize && (
            <span className="font-medium">{report.fileSize}</span>
          )}
        </div>

        <div className="flex flex-wrap gap-1 mb-4">
          {report.tags.map((tag, index) => (
            <span key={index} className="px-2 py-1 bg-gray-100 text-gray-600 text-xs rounded">
              {tag}
            </span>
          ))}
        </div>

        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2 text-xs text-gray-500">
            {report.downloads > 0 && (
              <span className="flex items-center space-x-1">
                <Download className="w-3 h-3" />
                <span>{report.downloads}</span>
              </span>
            )}
            {report.pages && (
              <span>{report.pages} pages</span>
            )}
            <span className="uppercase font-medium">{report.format}</span>
          </div>
          
          <div className="flex items-center space-x-2">
            {report.preview && (
              <button className="p-1 hover:bg-gray-100 rounded text-gray-600">
                <Eye className="w-4 h-4" />
              </button>
            )}
            <button className="p-1 hover:bg-gray-100 rounded text-gray-600">
              <Share2 className="w-4 h-4" />
            </button>
            <button className="p-1 hover:bg-gray-100 rounded text-blue-600">
              <Download className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>
    );
  };

  const CreateReportModal = () => {
    if (!showCreateModal) return null;

    return (
      <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
        <div className="bg-white rounded-lg max-w-2xl w-full max-h-[90vh] overflow-hidden">
          <div className="p-6 border-b border-gray-200">
            <h2 className="text-xl font-bold text-gray-900">Create New Report</h2>
          </div>
          
          <div className="p-6 overflow-y-auto">
            <div className="grid grid-cols-2 gap-6">
              <div
                className="p-6 border-2 border-dashed border-gray-300 rounded-lg hover:border-blue-400 cursor-pointer transition-colors"
                onClick={() => {
                  setShowCreateModal(false);
                  // Navigate to report builder
                }}
              >
                <div className="text-center">
                  <BarChart3 className="w-12 h-12 mx-auto mb-4 text-gray-400" />
                  <h3 className="font-semibold text-gray-900 mb-2">Custom Report</h3>
                  <p className="text-sm text-gray-600">Build a custom report with your selected metrics and data</p>
                </div>
              </div>
              
              <div
                className="p-6 border-2 border-dashed border-gray-300 rounded-lg hover:border-blue-400 cursor-pointer transition-colors"
                onClick={() => {
                  setShowCreateModal(false);
                  // Show template selector
                }}
              >
                <div className="text-center">
                  <Layout className="w-12 h-12 mx-auto mb-4 text-gray-400" />
                  <h3 className="font-semibold text-gray-900 mb-2">From Template</h3>
                  <p className="text-sm text-gray-600">Choose from pre-built report templates</p>
                </div>
              </div>
            </div>
            
            <div className="mt-6">
              <h3 className="font-semibold text-gray-900 mb-4">Quick Reports</h3>
              <div className="grid grid-cols-1 gap-3">
                {[
                  { name: 'Daily Safety Summary', type: 'safety', icon: Shield },
                  { name: 'Personnel Attendance', type: 'personnel', icon: Users },
                  { name: 'Equipment Status', type: 'equipment', icon: Wrench },
                  { name: 'AI Performance Metrics', type: 'ai_analytics', icon: Activity }
                ].map((quickReport, index) => (
                  <button
                    key={index}
                    className="flex items-center space-x-3 p-3 text-left hover:bg-gray-50 rounded-lg transition-colors"
                    onClick={() => {
                      setShowCreateModal(false);
                      // Generate quick report
                    }}
                  >
                    <quickReport.icon className="w-5 h-5 text-gray-600" />
                    <div>
                      <p className="font-medium text-gray-900">{quickReport.name}</p>
                      <p className="text-sm text-gray-600">Generate instantly</p>
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
              <h1 className="text-xl font-bold text-gray-900">Reports Center</h1>
              <div className="flex items-center space-x-2 text-sm text-gray-600">
                <MapPin className="w-3 h-3" />
                <span>{currentSite.name}</span>
                <span>•</span>
                <span>{filteredReports.length} reports</span>
                <span>•</span>
                <span>Last generated: {formatDate(new Date())}</span>
              </div>
            </div>

            <div className="flex items-center space-x-4">
              {/* View Mode Toggle */}
              <div className="flex items-center space-x-2 bg-gray-100 rounded-lg p-1">
                <button
                  onClick={() => setViewMode('grid')}
                  className={`px-3 py-1 text-sm rounded transition-colors ${
                    viewMode === 'grid' 
                      ? 'bg-white shadow-sm text-blue-600' 
                      : 'hover:bg-gray-200'
                  }`}
                >
                  Grid
                </button>
                <button
                  onClick={() => setViewMode('list')}
                  className={`px-3 py-1 text-sm rounded transition-colors ${
                    viewMode === 'list' 
                      ? 'bg-white shadow-sm text-blue-600' 
                      : 'hover:bg-gray-200'
                  }`}
                >
                  List
                </button>
              </div>

              <button
                onClick={() => setShowCreateModal(true)}
                className="flex items-center space-x-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
              >
                <Plus className="w-4 h-4" />
                <span>Create Report</span>
              </button>
            </div>
          </div>
        </div>

        {/* Statistics */}
        <div className="px-6 py-4 bg-gray-50 border-b border-gray-200">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <StatCard
              title="Total Reports"
              value={reports.length}
              icon={FileText}
              color={theme.primary[500]}
            />
            <StatCard
              title="Completed"
              value={reports.filter(r => r.status === 'completed').length}
              subtitle="Ready for download"
              icon={CheckCircle}
              color={theme.success[500]}
            />
            <StatCard
              title="Processing"
              value={reports.filter(r => r.status === 'processing').length}
              subtitle="Being generated"
              icon={Clock}
              color={theme.warning[500]}
            />
            <StatCard
              title="Total Downloads"
              value={reports.reduce((acc, r) => acc + r.downloads, 0)}
              subtitle="All time"
              icon={Download}
              color={theme.info[500]}
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
                placeholder="Search reports..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-10 pr-4 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:border-transparent"
                style={{ '--tw-ring-color': theme.primary[500] + '40' }}
              />
            </div>

            {/* Type Filter */}
            <select
              value={filterType}
              onChange={(e) => setFilterType(e.target.value)}
              className="px-3 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:border-transparent"
            >
              <option value="all">All Types</option>
              <option value="safety">Safety</option>
              <option value="personnel">Personnel</option>
              <option value="ai_analytics">AI Analytics</option>
              <option value="equipment">Equipment</option>
              <option value="progress">Progress</option>
              <option value="compliance">Compliance</option>
            </select>

            {/* Status Filter */}
            <select
              value={filterStatus}
              onChange={(e) => setFilterStatus(e.target.value)}
              className="px-3 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:border-transparent"
            >
              <option value="all">All Status</option>
              <option value="completed">Completed</option>
              <option value="processing">Processing</option>
              <option value="draft">Draft</option>
              <option value="error">Error</option>
            </select>

            {/* Date Range */}
            <select
              value={filterDateRange}
              onChange={(e) => setFilterDateRange(e.target.value)}
              className="px-3 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:border-transparent"
            >
              <option value="all">All Time</option>
              <option value="today">Today</option>
              <option value="week">This Week</option>
              <option value="month">This Month</option>
            </select>

            {/* Sort */}
            <select
              value={`${sortBy}-${sortOrder}`}
              onChange={(e) => {
                const [field, order] = e.target.value.split('-');
                setSortBy(field);
                setSortOrder(order);
              }}
              className="px-3 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:border-transparent"
            >
              <option value="createdAt-desc">Newest First</option>
              <option value="createdAt-asc">Oldest First</option>
              <option value="title-asc">Title A-Z</option>
              <option value="downloads-desc">Most Downloaded</option>
              <option value="fileSize-desc">Largest First</option>
            </select>
          </div>
        </div>

        {/* Reports List/Grid */}
        <div className="flex-1 overflow-auto p-6">
          {filteredReports.length === 0 ? (
            <div className="text-center py-12">
              <FileText className="w-16 h-16 mx-auto text-gray-400 mb-4" />
              <h3 className="text-lg font-medium text-gray-900 mb-2">No Reports Found</h3>
              <p className="text-gray-600 mb-6">
                {searchTerm || filterType !== 'all' || filterStatus !== 'all' || filterDateRange !== 'all'
                  ? 'No reports match your current filters'
                  : 'Get started by creating your first report'}
              </p>
              <button
                onClick={() => setShowCreateModal(true)}
                className="inline-flex items-center space-x-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
              >
                <Plus className="w-4 h-4" />
                <span>Create Report</span>
              </button>
            </div>
          ) : (
            <div className={viewMode === 'grid' 
              ? "grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6" 
              : "space-y-4"
            }>
              {filteredReports.map((report) => (
                <ReportCard key={report.id} report={report} />
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Create Report Modal */}
      <CreateReportModal />
    </MainLayout>
  );
};

export default ReportsCenter;