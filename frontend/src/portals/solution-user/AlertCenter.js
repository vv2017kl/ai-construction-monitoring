import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { 
  AlertTriangle, Shield, Users, Clock, MapPin, Camera, 
  Filter, Search, Download, RefreshCw, CheckCircle, X,
  Eye, Play, ExternalLink, MessageSquare, User, Bell,
  Calendar, TrendingUp, BarChart3, Settings, ChevronDown,
  Zap, AlertCircle, Info, CheckCircle2, XCircle, Plus,
  Trash2, UserPlus, Send, FileText, Archive, MoreHorizontal
} from 'lucide-react';
import { useTheme } from '../../context/ThemeContext';
import MainLayout from '../../components/shared/Layout/MainLayout';
import { mockAlerts, mockSites, mockUser, mockCameras } from '../../data/mockData';

const AlertCenter = () => {
  const navigate = useNavigate();
  const { alertId } = useParams();
  const { theme } = useTheme();
  
  // State management
  const [alerts, setAlerts] = useState(mockAlerts);
  const [selectedAlert, setSelectedAlert] = useState(null);
  const [filterStatus, setFilterStatus] = useState('all');
  const [filterPriority, setFilterPriority] = useState('all');
  const [filterType, setFilterType] = useState('all');
  const [sortBy, setSortBy] = useState('timestamp');
  const [searchTerm, setSearchTerm] = useState('');
  const [viewMode, setViewMode] = useState('list'); // 'list', 'cards', 'timeline'
  const [showFilters, setShowFilters] = useState(false);
  const [selectedAlerts, setSelectedAlerts] = useState(new Set());
  const [showBulkActions, setShowBulkActions] = useState(false);
  const [showAssignModal, setShowAssignModal] = useState(false);
  const [showEvidenceModal, setShowEvidenceModal] = useState(false);
  const [currentEvidence, setCurrentEvidence] = useState(null);
  const [showCommentModal, setShowCommentModal] = useState(false);
  const [alertComments, setAlertComments] = useState({});
  const [newComment, setNewComment] = useState('');

  const currentSite = mockSites.find(s => s.name === mockUser.currentSite) || mockSites[0];

  // Initialize selected alert from URL parameter
  useEffect(() => {
    if (alertId) {
      const alert = alerts.find(a => a.id === alertId);
      setSelectedAlert(alert);
    }
  }, [alertId, alerts]);

  // Filter and sort alerts
  const filteredAlerts = alerts
    .filter(alert => {
      const statusMatch = filterStatus === 'all' || alert.status === filterStatus;
      const priorityMatch = filterPriority === 'all' || alert.priority === filterPriority;
      const typeMatch = filterType === 'all' || alert.type === filterType;
      const searchMatch = searchTerm === '' || 
        alert.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
        alert.message.toLowerCase().includes(searchTerm.toLowerCase()) ||
        alert.location.toLowerCase().includes(searchTerm.toLowerCase());
      
      return statusMatch && priorityMatch && typeMatch && searchMatch;
    })
    .sort((a, b) => {
      switch (sortBy) {
        case 'priority':
          const priorityOrder = { critical: 4, high: 3, medium: 2, low: 1 };
          return priorityOrder[b.priority] - priorityOrder[a.priority];
        case 'status':
          return a.status.localeCompare(b.status);
        case 'location':
          return a.location.localeCompare(b.location);
        default: // timestamp
          return new Date(b.timestamp) - new Date(a.timestamp);
      }
    });

  const alertStats = {
    total: alerts.length,
    critical: alerts.filter(a => a.priority === 'critical').length,
    open: alerts.filter(a => a.status === 'open').length,
    investigating: alerts.filter(a => a.status === 'investigating').length,
    resolved: alerts.filter(a => a.status === 'resolved').length,
    avgResponseTime: Math.round(alerts.filter(a => a.responseTime).reduce((acc, a) => acc + a.responseTime, 0) / alerts.filter(a => a.responseTime).length)
  };

  // Alert actions
  const handleUpdateStatus = (alertId, newStatus) => {
    setAlerts(prev => prev.map(alert => 
      alert.id === alertId 
        ? { ...alert, status: newStatus, responseTime: newStatus !== 'open' ? (alert.responseTime || Math.floor(Math.random() * 30) + 5) : null }
        : alert
    ));
    
    if (selectedAlert?.id === alertId) {
      setSelectedAlert(prev => ({ ...prev, status: newStatus }));
    }
  };

  const handleAssignAlert = (alertId, assignee) => {
    setAlerts(prev => prev.map(alert => 
      alert.id === alertId ? { ...alert, assignedTo: assignee } : alert
    ));
  };

  // Bulk operations
  const handleSelectAlert = (alertId) => {
    const newSelected = new Set(selectedAlerts);
    if (newSelected.has(alertId)) {
      newSelected.delete(alertId);
    } else {
      newSelected.add(alertId);
    }
    setSelectedAlerts(newSelected);
    setShowBulkActions(newSelected.size > 0);
  };

  const handleSelectAll = () => {
    if (selectedAlerts.size === filteredAlerts.length) {
      setSelectedAlerts(new Set());
      setShowBulkActions(false);
    } else {
      setSelectedAlerts(new Set(filteredAlerts.map(alert => alert.id)));
      setShowBulkActions(true);
    }
  };

  const handleBulkStatusUpdate = (newStatus) => {
    setAlerts(prev => prev.map(alert => 
      selectedAlerts.has(alert.id) 
        ? { ...alert, status: newStatus, responseTime: newStatus !== 'open' ? (alert.responseTime || Math.floor(Math.random() * 30) + 5) : null }
        : alert
    ));
    setSelectedAlerts(new Set());
    setShowBulkActions(false);
  };

  const handleBulkAssign = (assignee) => {
    setAlerts(prev => prev.map(alert => 
      selectedAlerts.has(alert.id) ? { ...alert, assignedTo: assignee } : alert
    ));
    setSelectedAlerts(new Set());
    setShowBulkActions(false);
    setShowAssignModal(false);
  };

  // Comments functionality
  const handleAddComment = (alertId) => {
    if (newComment.trim()) {
      const comment = {
        id: Date.now(),
        text: newComment,
        author: mockUser.displayName,
        timestamp: new Date().toISOString(),
        avatar: mockUser.avatar
      };
      
      setAlertComments(prev => ({
        ...prev,
        [alertId]: [...(prev[alertId] || []), comment]
      }));
      
      setNewComment('');
      if (alertId === selectedAlert?.id) {
        setShowCommentModal(false);
      }
    }
  };

  // Evidence viewer
  const handleViewEvidence = (evidence) => {
    setCurrentEvidence(evidence);
    setShowEvidenceModal(true);
  };

  // Export functionality
  const handleExportAlerts = () => {
    const exportData = filteredAlerts.map(alert => ({
      ID: alert.id,
      Type: alert.type,
      Priority: alert.priority,
      Title: alert.title,
      Message: alert.message,
      Location: alert.location,
      Camera: alert.camera,
      Status: alert.status,
      AssignedTo: alert.assignedTo,
      Timestamp: alert.timestamp,
      ResponseTime: alert.responseTime
    }));

    const dataStr = JSON.stringify(exportData, null, 2);
    const dataUri = 'data:application/json;charset=utf-8,'+ encodeURIComponent(dataStr);
    
    const exportFileDefaultName = `alerts_export_${new Date().toISOString().split('T')[0]}.json`;
    
    const linkElement = document.createElement('a');
    linkElement.setAttribute('href', dataUri);
    linkElement.setAttribute('download', exportFileDefaultName);
    linkElement.click();
  };

  // Simulate real-time updates
  useEffect(() => {
    const interval = setInterval(() => {
      // Simulate new alert occasionally
      if (Math.random() < 0.1) { // 10% chance every 10 seconds
        const newAlert = {
          id: `alert-${Date.now()}`,
          type: ['safety_violation', 'equipment_violation', 'access_violation'][Math.floor(Math.random() * 3)],
          priority: ['critical', 'high', 'medium', 'low'][Math.floor(Math.random() * 4)],
          title: `New Alert - ${new Date().toLocaleTimeString()}`,
          message: 'Automatically generated alert for demonstration',
          location: ['Zone A', 'Zone B', 'Zone C'][Math.floor(Math.random() * 3)],
          camera: 'Camera ' + Math.floor(Math.random() * 10 + 1),
          timestamp: new Date().toISOString(),
          status: 'open',
          assignedTo: 'Unassigned',
          evidence: [],
          responseTime: null
        };
        
        setAlerts(prev => [newAlert, ...prev]);
      }
    }, 10000); // Check every 10 seconds

    return () => clearInterval(interval);
  }, []);

  const getPriorityColor = (priority) => {
    switch (priority) {
      case 'critical': return { bg: 'bg-red-100', text: 'text-red-800', border: 'border-red-200', icon: 'text-red-600' };
      case 'high': return { bg: 'bg-orange-100', text: 'text-orange-800', border: 'border-orange-200', icon: 'text-orange-600' };
      case 'medium': return { bg: 'bg-yellow-100', text: 'text-yellow-800', border: 'border-yellow-200', icon: 'text-yellow-600' };
      case 'low': return { bg: 'bg-blue-100', text: 'text-blue-800', border: 'border-blue-200', icon: 'text-blue-600' };
      default: return { bg: 'bg-gray-100', text: 'text-gray-800', border: 'border-gray-200', icon: 'text-gray-600' };
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'open': return { bg: 'bg-red-100', text: 'text-red-800', icon: AlertCircle };
      case 'investigating': return { bg: 'bg-yellow-100', text: 'text-yellow-800', icon: Info };
      case 'resolved': return { bg: 'bg-green-100', text: 'text-green-800', icon: CheckCircle2 };
      case 'acknowledged': return { bg: 'bg-blue-100', text: 'text-blue-800', icon: Eye };
      default: return { bg: 'bg-gray-100', text: 'text-gray-800', icon: AlertCircle };
    }
  };

  const getPriorityIcon = (priority) => {
    switch (priority) {
      case 'critical': return XCircle;
      case 'high': return AlertTriangle;
      case 'medium': return AlertCircle;
      case 'low': return CheckCircle;
      default: return Info;
    }
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

  const AlertCard = ({ alert, onClick, isSelected = false }) => {
    const priorityColors = getPriorityColor(alert.priority);
    const statusColors = getStatusColor(alert.status);
    const PriorityIcon = getPriorityIcon(alert.priority);
    const StatusIcon = statusColors.icon;
    const isCardSelected = selectedAlerts.has(alert.id);
    
    return (
      <div 
        className={`p-4 rounded-lg border cursor-pointer hover:shadow-md transition-all duration-200 ${
          isSelected ? 'ring-2 ring-blue-500 border-blue-200 bg-blue-50' : 
          isCardSelected ? 'ring-2 ring-green-500 border-green-200 bg-green-50' :
          'border-gray-200 bg-white hover:border-gray-300'
        }`}
      >
        <div className="flex items-start justify-between">
          <div className="flex items-start space-x-3 flex-1">
            <div className="flex items-center space-x-2">
              <input
                type="checkbox"
                checked={isCardSelected}
                onChange={(e) => {
                  e.stopPropagation();
                  handleSelectAlert(alert.id);
                }}
                className="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
              />
              <div className={`p-2 rounded-lg ${priorityColors.bg}`}>
                <PriorityIcon className={`w-5 h-5 ${priorityColors.icon}`} />
              </div>
            </div>
            
            <div className="flex-1 min-w-0" onClick={() => onClick(alert)}>
              <div className="flex items-center justify-between mb-2">
                <h3 className="text-sm font-semibold text-gray-900 truncate">{alert.title}</h3>
                <span className={`px-2 py-1 text-xs font-semibold rounded-full ${statusColors.bg} ${statusColors.text}`}>
                  {alert.status.toUpperCase()}
                </span>
              </div>
              
              <p className="text-sm text-gray-600 mb-3">{alert.message}</p>
              
              <div className="flex flex-wrap items-center gap-4 text-xs text-gray-500">
                <div className="flex items-center space-x-1">
                  <MapPin className="w-3 h-3" />
                  <span>{alert.location}</span>
                </div>
                <div className="flex items-center space-x-1">
                  <Camera className="w-3 h-3" />
                  <span>{alert.camera}</span>
                </div>
                <div className="flex items-center space-x-1">
                  <Clock className="w-3 h-3" />
                  <span>{new Date(alert.timestamp).toLocaleString()}</span>
                </div>
                <div className="flex items-center space-x-1">
                  <User className="w-3 h-3" />
                  <span>{alert.assignedTo}</span>
                </div>
                {alert.responseTime && (
                  <div className="flex items-center space-x-1">
                    <Zap className="w-3 h-3" />
                    <span>{alert.responseTime}min response</span>
                  </div>
                )}
              </div>
            </div>
          </div>
          
          <div className="flex items-center space-x-2 ml-4">
            <span className={`px-2 py-1 text-xs font-semibold rounded-full ${priorityColors.bg} ${priorityColors.text}`}>
              {alert.priority.toUpperCase()}
            </span>
            {alert.evidence.length > 0 && (
              <div className="flex items-center space-x-1 text-blue-600">
                <Eye className="w-3 h-3" />
                <span className="text-xs">{alert.evidence.length}</span>
              </div>
            )}
          </div>
        </div>
      </div>
    );
  };

  const AlertDetailModal = () => {
    if (!selectedAlert) return null;

    const priorityColors = getPriorityColor(selectedAlert.priority);
    const statusColors = getStatusColor(selectedAlert.status);
    const PriorityIcon = getPriorityIcon(selectedAlert.priority);

    return (
      <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
        <div className="bg-white rounded-lg max-w-4xl w-full max-h-[90vh] overflow-hidden">
          {/* Header */}
          <div className="p-6 border-b border-gray-200">
            <div className="flex items-start justify-between">
              <div className="flex items-start space-x-4">
                <div className={`p-3 rounded-lg ${priorityColors.bg}`}>
                  <PriorityIcon className={`w-6 h-6 ${priorityColors.icon}`} />
                </div>
                <div>
                  <h2 className="text-xl font-bold text-gray-900">{selectedAlert.title}</h2>
                  <p className="text-gray-600 mt-1">{selectedAlert.message}</p>
                  <div className="flex items-center space-x-4 mt-3 text-sm text-gray-500">
                    <span className={`px-2 py-1 rounded-full ${priorityColors.bg} ${priorityColors.text} font-semibold`}>
                      {selectedAlert.priority.toUpperCase()}
                    </span>
                    <span className={`px-2 py-1 rounded-full ${statusColors.bg} ${statusColors.text} font-semibold`}>
                      {selectedAlert.status.toUpperCase()}
                    </span>
                  </div>
                </div>
              </div>
              <button
                onClick={() => setSelectedAlert(null)}
                className="p-2 hover:bg-gray-100 rounded-lg"
              >
                <X className="w-5 h-5" />
              </button>
            </div>
          </div>

          {/* Content */}
          <div className="p-6 overflow-y-auto max-h-[70vh]">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* Alert Details */}
              <div className="space-y-6">
                <div>
                  <h3 className="font-semibold text-gray-900 mb-4">Alert Information</h3>
                  <div className="space-y-3">
                    <div className="flex justify-between">
                      <span className="text-gray-600">Alert ID:</span>
                      <span className="font-medium">{selectedAlert.id}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Type:</span>
                      <span className="font-medium capitalize">{selectedAlert.type.replace('_', ' ')}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Location:</span>
                      <span className="font-medium">{selectedAlert.location}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Camera:</span>
                      <span className="font-medium">{selectedAlert.camera}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Detected:</span>
                      <span className="font-medium">{new Date(selectedAlert.timestamp).toLocaleString()}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Assigned To:</span>
                      <span className="font-medium">{selectedAlert.assignedTo}</span>
                    </div>
                    {selectedAlert.responseTime && (
                      <div className="flex justify-between">
                        <span className="text-gray-600">Response Time:</span>
                        <span className="font-medium">{selectedAlert.responseTime} minutes</span>
                      </div>
                    )}
                  </div>
                </div>

                {/* Actions */}
                <div>
                  <h3 className="font-semibold text-gray-900 mb-4">Quick Actions</h3>
                  <div className="grid grid-cols-2 gap-3">
                    <button
                      onClick={() => handleUpdateStatus(selectedAlert.id, 'investigating')}
                      className="flex items-center justify-center space-x-2 p-3 bg-yellow-50 text-yellow-700 rounded-lg hover:bg-yellow-100 transition-colors"
                    >
                      <Info className="w-4 h-4" />
                      <span>Investigate</span>
                    </button>
                    <button
                      onClick={() => handleUpdateStatus(selectedAlert.id, 'resolved')}
                      className="flex items-center justify-center space-x-2 p-3 bg-green-50 text-green-700 rounded-lg hover:bg-green-100 transition-colors"
                    >
                      <CheckCircle2 className="w-4 h-4" />
                      <span>Resolve</span>
                    </button>
                    <button
                      onClick={() => navigate('/live-view')}
                      className="flex items-center justify-center space-x-2 p-3 bg-blue-50 text-blue-700 rounded-lg hover:bg-blue-100 transition-colors"
                    >
                      <Camera className="w-4 h-4" />
                      <span>View Camera</span>
                    </button>
                    <button className="flex items-center justify-center space-x-2 p-3 bg-gray-50 text-gray-700 rounded-lg hover:bg-gray-100 transition-colors">
                      <Download className="w-4 h-4" />
                      <span>Export</span>
                    </button>
                  </div>
                </div>
              </div>

              {/* Evidence & Timeline */}
              <div className="space-y-6">
                {selectedAlert.evidence.length > 0 && (
                  <div>
                    <h3 className="font-semibold text-gray-900 mb-4">Evidence</h3>
                    <div className="grid grid-cols-1 gap-3">
                      {selectedAlert.evidence.map((item, index) => (
                        <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                          <div className="flex items-center space-x-3">
                            {item.includes('.jpg') || item.includes('.png') ? (
                              <Eye className="w-4 h-4 text-blue-600" />
                            ) : (
                              <Play className="w-4 h-4 text-green-600" />
                            )}
                            <span className="text-sm text-gray-900">
                              {item.includes('.jpg') || item.includes('.png') ? 'Screenshot' : 'Video Recording'}
                            </span>
                          </div>
                          <button className="text-blue-600 hover:text-blue-800 text-sm">
                            <ExternalLink className="w-4 h-4" />
                          </button>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Response Timeline */}
                <div>
                  <h3 className="font-semibold text-gray-900 mb-4">Response Timeline</h3>
                  <div className="space-y-3">
                    <div className="flex items-start space-x-3">
                      <div className="w-2 h-2 bg-red-500 rounded-full mt-2"></div>
                      <div>
                        <p className="text-sm font-medium">Alert Triggered</p>
                        <p className="text-xs text-gray-500">{new Date(selectedAlert.timestamp).toLocaleString()}</p>
                      </div>
                    </div>
                    {selectedAlert.status !== 'open' && (
                      <div className="flex items-start space-x-3">
                        <div className="w-2 h-2 bg-yellow-500 rounded-full mt-2"></div>
                        <div>
                          <p className="text-sm font-medium">Response Started</p>
                          <p className="text-xs text-gray-500">Assigned to {selectedAlert.assignedTo}</p>
                        </div>
                      </div>
                    )}
                    {selectedAlert.status === 'resolved' && (
                      <div className="flex items-start space-x-3">
                        <div className="w-2 h-2 bg-green-500 rounded-full mt-2"></div>
                        <div>
                          <p className="text-sm font-medium">Alert Resolved</p>
                          <p className="text-xs text-gray-500">Total response time: {selectedAlert.responseTime} minutes</p>
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            </div>
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
              <h1 className="text-xl font-bold text-gray-900">Alert Center</h1>
              <div className="flex items-center space-x-2 text-sm text-gray-600">
                <MapPin className="w-3 h-3" />
                <span>{currentSite.name}</span>
                <span>•</span>
                <span>{filteredAlerts.length} of {alerts.length} alerts</span>
                <span>•</span>
                <span className="flex items-center space-x-1">
                  <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                  <span>Real-time</span>
                </span>
              </div>
            </div>

            <div className="flex items-center space-x-4">
              <button
                onClick={() => setShowFilters(!showFilters)}
                className="flex items-center space-x-2 px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors"
              >
                <Filter className="w-4 h-4" />
                <span>Filters</span>
              </button>
              <button className="flex items-center space-x-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
                <RefreshCw className="w-4 h-4" />
                <span>Refresh</span>
              </button>
            </div>
          </div>
        </div>

        {/* Alert Statistics */}
        <div className="px-6 py-4 bg-gray-50 border-b border-gray-200">
          <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
            <StatCard
              title="Total Alerts"
              value={alertStats.total}
              icon={Bell}
              color={theme.primary[500]}
              onClick={() => setFilterStatus('all')}
            />
            <StatCard
              title="Critical"
              value={alertStats.critical}
              subtitle="Requires immediate action"
              icon={XCircle}
              color={theme.danger[500]}
              onClick={() => setFilterPriority('critical')}
            />
            <StatCard
              title="Open"
              value={alertStats.open}
              icon={AlertCircle}
              color="#ef4444"
              onClick={() => setFilterStatus('open')}
            />
            <StatCard
              title="In Progress"
              value={alertStats.investigating}
              icon={Info}
              color="#f59e0b"
              onClick={() => setFilterStatus('investigating')}
            />
            <StatCard
              title="Avg Response"
              value={`${alertStats.avgResponseTime}min`}
              icon={Zap}
              color={theme.success[500]}
            />
          </div>
        </div>

        {/* Filters Panel */}
        {showFilters && (
          <div className="px-6 py-4 bg-white border-b border-gray-200">
            <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Search</label>
                <div className="relative">
                  <Search className="w-4 h-4 absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
                  <input
                    type="text"
                    placeholder="Search alerts..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    className="w-full pl-10 pr-4 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:border-transparent"
                    style={{ '--tw-ring-color': theme.primary[500] + '40' }}
                  />
                </div>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Status</label>
                <select
                  value={filterStatus}
                  onChange={(e) => setFilterStatus(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:border-transparent"
                >
                  <option value="all">All Status</option>
                  <option value="open">Open</option>
                  <option value="investigating">Investigating</option>
                  <option value="resolved">Resolved</option>
                  <option value="acknowledged">Acknowledged</option>
                </select>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Priority</label>
                <select
                  value={filterPriority}
                  onChange={(e) => setFilterPriority(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:border-transparent"
                >
                  <option value="all">All Priorities</option>
                  <option value="critical">Critical</option>
                  <option value="high">High</option>
                  <option value="medium">Medium</option>
                  <option value="low">Low</option>
                </select>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Type</label>
                <select
                  value={filterType}
                  onChange={(e) => setFilterType(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:border-transparent"
                >
                  <option value="all">All Types</option>
                  <option value="safety_violation">Safety Violation</option>
                  <option value="equipment_violation">Equipment Violation</option>
                  <option value="access_violation">Access Violation</option>
                  <option value="system_alert">System Alert</option>
                </select>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Sort By</label>
                <select
                  value={sortBy}
                  onChange={(e) => setSortBy(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:border-transparent"
                >
                  <option value="timestamp">Latest First</option>
                  <option value="priority">Priority</option>
                  <option value="status">Status</option>
                  <option value="location">Location</option>
                </select>
              </div>
            </div>
          </div>
        )}

        {/* Alert List */}
        <div className="flex-1 flex overflow-hidden">
          <div className="flex-1 p-6 overflow-y-auto">
            {filteredAlerts.length === 0 ? (
              <div className="text-center py-12">
                <Shield className="w-16 h-16 mx-auto text-gray-400 mb-4" />
                <h3 className="text-lg font-medium text-gray-900 mb-2">No Alerts Found</h3>
                <p className="text-gray-600">
                  {searchTerm || filterStatus !== 'all' || filterPriority !== 'all' || filterType !== 'all'
                    ? 'No alerts match your current filters'
                    : 'All clear! No active alerts at this time'}
                </p>
              </div>
            ) : (
              <div className="space-y-4">
                {filteredAlerts.map((alert) => (
                  <AlertCard
                    key={alert.id}
                    alert={alert}
                    onClick={setSelectedAlert}
                    isSelected={selectedAlert?.id === alert.id}
                  />
                ))}
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Alert Detail Modal */}
      <AlertDetailModal />
    </MainLayout>
  );
};

export default AlertCenter;