import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  Users, UserPlus, Search, Filter, Download, RefreshCw,
  MoreVertical, Eye, Edit, Trash2, Shield, HardHat,
  Clock, MapPin, Phone, Mail, Calendar, CheckCircle,
  AlertTriangle, XCircle, User, Building2, Briefcase,
  Activity, TrendingUp, BarChart3, Camera, Bell, X,
  Plus, Save, Navigation, UserCheck, UserX, Send,
  Archive, FileText, Map, Zap, Target, Settings
} from 'lucide-react';
import { useTheme } from '../../context/ThemeContext';
import MainLayout from '../../components/shared/Layout/MainLayout';
import { mockPersonnel, mockSites, mockUser, mockDepartments } from '../../data/mockData';

const PersonnelManagement = () => {
  const navigate = useNavigate();
  const { theme } = useTheme();
  
  // State management
  const [personnel, setPersonnel] = useState(mockPersonnel || []);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterDepartment, setFilterDepartment] = useState('all');
  const [filterStatus, setFilterStatus] = useState('all');
  const [filterRole, setFilterRole] = useState('all');
  const [sortBy, setSortBy] = useState('name');
  const [sortOrder, setSortOrder] = useState('asc');
  const [selectedPersonnel, setSelectedPersonnel] = useState(new Set());
  const [showAddModal, setShowAddModal] = useState(false);
  const [showDetailModal, setShowDetailModal] = useState(false);
  const [selectedPerson, setSelectedPerson] = useState(null);
  const [viewMode, setViewMode] = useState('table'); // 'table', 'cards'
  const [showBulkActions, setShowBulkActions] = useState(false);
  const [showEditModal, setShowEditModal] = useState(false);
  const [showLocationModal, setShowLocationModal] = useState(false);
  const [showAssignModal, setShowAssignModal] = useState(false);
  const [editingPerson, setEditingPerson] = useState(null);
  const [newPersonForm, setNewPersonForm] = useState({
    name: '',
    role: '',
    department: '',
    email: '',
    phone: '',
    certifications: []
  });

  const currentSite = mockSites.find(s => s.name === mockUser.currentSite) || mockSites[0];

  // Generate mock personnel data if not available
  const generateMockPersonnel = () => {
    if (mockPersonnel && mockPersonnel.length > 0) return mockPersonnel;
    
    return [
      {
        id: 'p001',
        name: 'John Mitchell',
        role: 'Site Supervisor',
        department: 'Construction',
        email: 'j.mitchell@constructionai.com',
        phone: '+1 (555) 0123',
        status: 'active',
        currentLocation: 'Zone A - Foundation',
        lastSeen: new Date(Date.now() - 15 * 60 * 1000),
        certifications: ['OSHA 30', 'First Aid', 'Forklift'],
        safetyScore: 95,
        hoursWorked: 42,
        checkInTime: new Date().setHours(7, 30),
        ppeCompliance: 98,
        avatar: null
      },
      {
        id: 'p002',
        name: 'Sarah Chen',
        role: 'Safety Inspector',
        department: 'Safety',
        email: 's.chen@constructionai.com',
        phone: '+1 (555) 0124',
        status: 'active',
        currentLocation: 'Zone B - Steel Frame',
        lastSeen: new Date(Date.now() - 5 * 60 * 1000),
        certifications: ['OSHA 10', 'Safety Management'],
        safetyScore: 100,
        hoursWorked: 40,
        checkInTime: new Date().setHours(8, 0),
        ppeCompliance: 100,
        avatar: null
      },
      {
        id: 'p003',
        name: 'Mike Rodriguez',
        role: 'Equipment Operator',
        department: 'Equipment',
        email: 'm.rodriguez@constructionai.com',
        phone: '+1 (555) 0125',
        status: 'active',
        currentLocation: 'Zone C - Excavation',
        lastSeen: new Date(Date.now() - 30 * 60 * 1000),
        certifications: ['Heavy Equipment', 'CDL Class A'],
        safetyScore: 88,
        hoursWorked: 45,
        checkInTime: new Date().setHours(6, 45),
        ppeCompliance: 92,
        avatar: null
      },
      {
        id: 'p004',
        name: 'Emma Thompson',
        role: 'Quality Control',
        department: 'Quality Assurance',
        email: 'e.thompson@constructionai.com',
        phone: '+1 (555) 0126',
        status: 'break',
        currentLocation: 'Break Room',
        lastSeen: new Date(Date.now() - 10 * 60 * 1000),
        certifications: ['QA Certification', 'Material Testing'],
        safetyScore: 96,
        hoursWorked: 38,
        checkInTime: new Date().setHours(8, 15),
        ppeCompliance: 94,
        avatar: null
      },
      {
        id: 'p005',
        name: 'David Park',
        role: 'Electrician',
        department: 'Electrical',
        email: 'd.park@constructionai.com',
        phone: '+1 (555) 0127',
        status: 'off-site',
        currentLocation: 'Off-Site',
        lastSeen: new Date(Date.now() - 2 * 60 * 60 * 1000),
        certifications: ['Electrical License', 'Arc Flash Safety'],
        safetyScore: 91,
        hoursWorked: 35,
        checkInTime: null,
        ppeCompliance: 89,
        avatar: null
      }
    ];
  };

  const personnelData = generateMockPersonnel();

  // CRUD Operations
  const handleAddPersonnel = () => {
    if (!newPersonForm.name || !newPersonForm.role || !newPersonForm.department) return;
    
    const newPerson = {
      id: `p${Date.now()}`,
      ...newPersonForm,
      status: 'active',
      currentLocation: 'Main Office',
      lastSeen: new Date(),
      safetyScore: 100,
      hoursWorked: 0,
      checkInTime: null,
      ppeCompliance: 100,
      avatar: null,
      certifications: newPersonForm.certifications.filter(cert => cert.trim())
    };
    
    setPersonnel(prev => [...prev, newPerson]);
    setNewPersonForm({
      name: '',
      role: '',
      department: '',
      email: '',
      phone: '',
      certifications: []
    });
    setShowAddModal(false);
  };

  const handleEditPersonnel = () => {
    if (!editingPerson) return;
    
    setPersonnel(prev => prev.map(person => 
      person.id === editingPerson.id ? editingPerson : person
    ));
    setShowEditModal(false);
    setEditingPerson(null);
  };

  const handleDeletePersonnel = (personId) => {
    setPersonnel(prev => prev.filter(person => person.id !== personId));
    if (selectedPerson?.id === personId) {
      setShowDetailModal(false);
      setSelectedPerson(null);
    }
  };

  // Bulk Operations
  const handleSelectPersonnel = (personId) => {
    const newSelected = new Set(selectedPersonnel);
    if (newSelected.has(personId)) {
      newSelected.delete(personId);
    } else {
      newSelected.add(personId);
    }
    setSelectedPersonnel(newSelected);
    setShowBulkActions(newSelected.size > 0);
  };

  const handleSelectAll = () => {
    if (selectedPersonnel.size === filteredPersonnel.length) {
      setSelectedPersonnel(new Set());
      setShowBulkActions(false);
    } else {
      setSelectedPersonnel(new Set(filteredPersonnel.map(person => person.id)));
      setShowBulkActions(true);
    }
  };

  const handleBulkStatusUpdate = (newStatus) => {
    setPersonnel(prev => prev.map(person => 
      selectedPersonnel.has(person.id) 
        ? { ...person, status: newStatus, lastSeen: new Date() }
        : person
    ));
    setSelectedPersonnel(new Set());
    setShowBulkActions(false);
  };

  // Status and Location Updates
  const handleStatusUpdate = (personId, newStatus) => {
    setPersonnel(prev => prev.map(person => 
      person.id === personId 
        ? { ...person, status: newStatus, lastSeen: new Date() }
        : person
    ));
  };

  const handleLocationUpdate = (personId, newLocation) => {
    setPersonnel(prev => prev.map(person => 
      person.id === personId 
        ? { ...person, currentLocation: newLocation, lastSeen: new Date() }
        : person
    ));
  };

  // Export functionality
  const handleExportPersonnel = () => {
    const exportData = filteredPersonnel.map(person => ({
      ID: person.id,
      Name: person.name,
      Role: person.role,
      Department: person.department,
      Email: person.email,
      Phone: person.phone,
      Status: person.status,
      Location: person.currentLocation,
      SafetyScore: person.safetyScore,
      PPECompliance: person.ppeCompliance,
      HoursWorked: person.hoursWorked,
      LastSeen: person.lastSeen,
      Certifications: person.certifications.join('; ')
    }));

    const dataStr = JSON.stringify(exportData, null, 2);
    const dataUri = 'data:application/json;charset=utf-8,'+ encodeURIComponent(dataStr);
    
    const exportFileDefaultName = `personnel_export_${new Date().toISOString().split('T')[0]}.json`;
    
    const linkElement = document.createElement('a');
    linkElement.setAttribute('href', dataUri);
    linkElement.setAttribute('download', exportFileDefaultName);
    linkElement.click();
  };

  // Real-time updates simulation
  useEffect(() => {
    const interval = setInterval(() => {
      // Simulate location updates for active personnel
      setPersonnel(prev => prev.map(person => {
        if (person.status === 'active' && Math.random() < 0.3) {
          const locations = ['Zone A - Foundation', 'Zone B - Steel Frame', 'Zone C - Excavation', 'Safety Office', 'Equipment Storage'];
          const randomLocation = locations[Math.floor(Math.random() * locations.length)];
          return { ...person, currentLocation: randomLocation, lastSeen: new Date() };
        }
        return person;
      }));
    }, 15000); // Update every 15 seconds

    return () => clearInterval(interval);
  }, []);

  // Filter and sort personnel
  const filteredPersonnel = personnelData
    .filter(person => {
      const nameMatch = person.name.toLowerCase().includes(searchTerm.toLowerCase());
      const emailMatch = person.email.toLowerCase().includes(searchTerm.toLowerCase());
      const roleMatch = person.role.toLowerCase().includes(searchTerm.toLowerCase());
      const searchMatch = nameMatch || emailMatch || roleMatch;
      
      const departmentMatch = filterDepartment === 'all' || person.department === filterDepartment;
      const statusMatch = filterStatus === 'all' || person.status === filterStatus;
      const roleFilterMatch = filterRole === 'all' || person.role === filterRole;
      
      return searchMatch && departmentMatch && statusMatch && roleFilterMatch;
    })
    .sort((a, b) => {
      let aValue = a[sortBy];
      let bValue = b[sortBy];
      
      if (sortBy === 'lastSeen') {
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
      case 'active': return { bg: 'bg-green-100', text: 'text-green-800', dot: 'bg-green-500' };
      case 'break': return { bg: 'bg-yellow-100', text: 'text-yellow-800', dot: 'bg-yellow-500' };
      case 'off-site': return { bg: 'bg-gray-100', text: 'text-gray-800', dot: 'bg-gray-500' };
      case 'absent': return { bg: 'bg-red-100', text: 'text-red-800', dot: 'bg-red-500' };
      default: return { bg: 'bg-gray-100', text: 'text-gray-800', dot: 'bg-gray-500' };
    }
  };

  const getSafetyScoreColor = (score) => {
    if (score >= 95) return 'text-green-600';
    if (score >= 85) return 'text-yellow-600';
    return 'text-red-600';
  };

  const formatTime = (timestamp) => {
    if (!timestamp) return 'Not checked in';
    const date = new Date(timestamp);
    return date.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });
  };

  const formatLastSeen = (timestamp) => {
    const now = new Date();
    const lastSeen = new Date(timestamp);
    const diffMinutes = Math.floor((now - lastSeen) / (1000 * 60));
    
    if (diffMinutes < 1) return 'Just now';
    if (diffMinutes < 60) return `${diffMinutes}m ago`;
    
    const diffHours = Math.floor(diffMinutes / 60);
    if (diffHours < 24) return `${diffHours}h ago`;
    
    const diffDays = Math.floor(diffHours / 24);
    return `${diffDays}d ago`;
  };

  const StatCard = ({ title, value, subtitle, icon: Icon, color, trend }) => (
    <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-sm font-medium text-gray-600">{title}</h3>
          <p className="text-2xl font-bold text-gray-900 mt-2">{value}</p>
          {subtitle && <p className="text-xs text-gray-500 mt-1">{subtitle}</p>}
          {trend && (
            <div className={`flex items-center mt-2 text-sm ${trend.positive ? 'text-green-600' : 'text-red-600'}`}>
              <TrendingUp className="w-4 h-4 mr-1" />
              <span>{trend.value}</span>
            </div>
          )}
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

  const PersonnelDetailModal = () => {
    if (!showDetailModal || !selectedPerson) return null;

    return (
      <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
        <div className="bg-white rounded-lg max-w-2xl w-full max-h-[90vh] overflow-hidden">
          {/* Header */}
          <div className="p-6 border-b border-gray-200">
            <div className="flex items-start justify-between">
              <div className="flex items-start space-x-4">
                <div className="w-16 h-16 bg-gray-200 rounded-full flex items-center justify-center">
                  <User className="w-8 h-8 text-gray-600" />
                </div>
                <div>
                  <h2 className="text-xl font-bold text-gray-900">{selectedPerson.name}</h2>
                  <p className="text-gray-600">{selectedPerson.role}</p>
                  <div className="flex items-center space-x-2 mt-2">
                    <span className={`px-2 py-1 text-xs font-semibold rounded-full ${getStatusColor(selectedPerson.status).bg} ${getStatusColor(selectedPerson.status).text}`}>
                      {selectedPerson.status.toUpperCase()}
                    </span>
                    <span className="text-sm text-gray-500">
                      Last seen: {formatLastSeen(selectedPerson.lastSeen)}
                    </span>
                  </div>
                </div>
              </div>
              <button
                onClick={() => setShowDetailModal(false)}
                className="p-2 hover:bg-gray-100 rounded-lg"
              >
                <XCircle className="w-5 h-5" />
              </button>
            </div>
          </div>

          {/* Content */}
          <div className="p-6 overflow-y-auto max-h-[70vh]">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* Contact Information */}
              <div>
                <h3 className="font-semibold text-gray-900 mb-4">Contact Information</h3>
                <div className="space-y-3">
                  <div className="flex items-center space-x-3">
                    <Mail className="w-4 h-4 text-gray-400" />
                    <span className="text-gray-900">{selectedPerson.email}</span>
                  </div>
                  <div className="flex items-center space-x-3">
                    <Phone className="w-4 h-4 text-gray-400" />
                    <span className="text-gray-900">{selectedPerson.phone}</span>
                  </div>
                  <div className="flex items-center space-x-3">
                    <Building2 className="w-4 h-4 text-gray-400" />
                    <span className="text-gray-900">{selectedPerson.department}</span>
                  </div>
                  <div className="flex items-center space-x-3">
                    <MapPin className="w-4 h-4 text-gray-400" />
                    <span className="text-gray-900">{selectedPerson.currentLocation}</span>
                  </div>
                </div>
              </div>

              {/* Work Information */}
              <div>
                <h3 className="font-semibold text-gray-900 mb-4">Work Information</h3>
                <div className="space-y-3">
                  <div className="flex justify-between">
                    <span className="text-gray-600">Check-in Time:</span>
                    <span className="font-medium">{formatTime(selectedPerson.checkInTime)}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Hours Worked:</span>
                    <span className="font-medium">{selectedPerson.hoursWorked}h</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Safety Score:</span>
                    <span className={`font-medium ${getSafetyScoreColor(selectedPerson.safetyScore)}`}>
                      {selectedPerson.safetyScore}%
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">PPE Compliance:</span>
                    <span className={`font-medium ${getSafetyScoreColor(selectedPerson.ppeCompliance)}`}>
                      {selectedPerson.ppeCompliance}%
                    </span>
                  </div>
                </div>
              </div>
            </div>

            {/* Certifications */}
            <div className="mt-6">
              <h3 className="font-semibold text-gray-900 mb-4">Certifications</h3>
              <div className="flex flex-wrap gap-2">
                {selectedPerson.certifications.map((cert, index) => (
                  <span
                    key={index}
                    className="px-3 py-1 bg-blue-100 text-blue-800 text-sm rounded-full"
                  >
                    {cert}
                  </span>
                ))}
              </div>
            </div>

            {/* Quick Actions */}
            <div className="mt-6">
              <h3 className="font-semibold text-gray-900 mb-4">Quick Actions</h3>
              <div className="grid grid-cols-2 gap-3">
                <button className="flex items-center justify-center space-x-2 p-3 bg-blue-50 text-blue-700 rounded-lg hover:bg-blue-100 transition-colors">
                  <Camera className="w-4 h-4" />
                  <span>View Location</span>
                </button>
                <button className="flex items-center justify-center space-x-2 p-3 bg-green-50 text-green-700 rounded-lg hover:bg-green-100 transition-colors">
                  <Phone className="w-4 h-4" />
                  <span>Call</span>
                </button>
                <button className="flex items-center justify-center space-x-2 p-3 bg-yellow-50 text-yellow-700 rounded-lg hover:bg-yellow-100 transition-colors">
                  <Bell className="w-4 h-4" />
                  <span>Send Alert</span>
                </button>
                <button className="flex items-center justify-center space-x-2 p-3 bg-purple-50 text-purple-700 rounded-lg hover:bg-purple-100 transition-colors">
                  <BarChart3 className="w-4 h-4" />
                  <span>View Reports</span>
                </button>
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
              <h1 className="text-xl font-bold text-gray-900">Personnel Management</h1>
              <div className="flex items-center space-x-2 text-sm text-gray-600">
                <MapPin className="w-3 h-3" />
                <span>{currentSite.name}</span>
                <span>•</span>
                <span>{filteredPersonnel.length} personnel</span>
                <span>•</span>
                <span className="flex items-center space-x-1">
                  <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                  <span>Live tracking</span>
                </span>
              </div>
            </div>

            <div className="flex items-center space-x-4">
              {/* View Mode Toggle */}
              <div className="flex items-center space-x-2 bg-gray-100 rounded-lg p-1">
                <button
                  onClick={() => setViewMode('table')}
                  className={`px-3 py-1 text-sm rounded transition-colors ${
                    viewMode === 'table' 
                      ? 'bg-white shadow-sm text-blue-600' 
                      : 'hover:bg-gray-200'
                  }`}
                >
                  Table
                </button>
                <button
                  onClick={() => setViewMode('cards')}
                  className={`px-3 py-1 text-sm rounded transition-colors ${
                    viewMode === 'cards' 
                      ? 'bg-white shadow-sm text-blue-600' 
                      : 'hover:bg-gray-200'
                  }`}
                >
                  Cards
                </button>
              </div>

              <button
                onClick={() => setShowAddModal(true)}
                className="flex items-center space-x-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
              >
                <UserPlus className="w-4 h-4" />
                <span>Add Personnel</span>
              </button>
            </div>
          </div>
        </div>

        {/* Statistics */}
        <div className="px-6 py-4 bg-gray-50 border-b border-gray-200">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <StatCard
              title="Total Personnel"
              value={personnelData.length}
              icon={Users}
              color={theme.primary[500]}
            />
            <StatCard
              title="On Site"
              value={personnelData.filter(p => p.status === 'active').length}
              subtitle="Currently working"
              icon={CheckCircle}
              color={theme.success[500]}
            />
            <StatCard
              title="Average Safety Score"
              value={`${Math.round(personnelData.reduce((acc, p) => acc + p.safetyScore, 0) / personnelData.length)}%`}
              trend={{ positive: true, value: '+2.1%' }}
              icon={Shield}
              color={theme.warning[500]}
            />
            <StatCard
              title="PPE Compliance"
              value={`${Math.round(personnelData.reduce((acc, p) => acc + p.ppeCompliance, 0) / personnelData.length)}%`}
              trend={{ positive: false, value: '-0.5%' }}
              icon={HardHat}
              color={theme.danger[500]}
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
                placeholder="Search personnel..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-10 pr-4 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:border-transparent"
                style={{ '--tw-ring-color': theme.primary[500] + '40' }}
              />
            </div>

            {/* Department Filter */}
            <select
              value={filterDepartment}
              onChange={(e) => setFilterDepartment(e.target.value)}
              className="px-3 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:border-transparent"
            >
              <option value="all">All Departments</option>
              <option value="Construction">Construction</option>
              <option value="Safety">Safety</option>
              <option value="Equipment">Equipment</option>
              <option value="Quality Assurance">Quality Assurance</option>
              <option value="Electrical">Electrical</option>
            </select>

            {/* Status Filter */}
            <select
              value={filterStatus}
              onChange={(e) => setFilterStatus(e.target.value)}
              className="px-3 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:border-transparent"
            >
              <option value="all">All Status</option>
              <option value="active">Active</option>
              <option value="break">On Break</option>
              <option value="off-site">Off-Site</option>
              <option value="absent">Absent</option>
            </select>

            {/* Role Filter */}
            <select
              value={filterRole}
              onChange={(e) => setFilterRole(e.target.value)}
              className="px-3 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:border-transparent"
            >
              <option value="all">All Roles</option>
              <option value="Site Supervisor">Site Supervisor</option>
              <option value="Safety Inspector">Safety Inspector</option>
              <option value="Equipment Operator">Equipment Operator</option>
              <option value="Quality Control">Quality Control</option>
              <option value="Electrician">Electrician</option>
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
              <option value="name-asc">Name A-Z</option>
              <option value="name-desc">Name Z-A</option>
              <option value="lastSeen-desc">Recently Seen</option>
              <option value="safetyScore-desc">Safety Score High</option>
              <option value="hoursWorked-desc">Hours Worked</option>
            </select>
          </div>
        </div>

        {/* Personnel List */}
        <div className="flex-1 overflow-auto">
          {viewMode === 'table' ? (
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-gray-50 border-b border-gray-200">
                  <tr>
                    <th className="text-left py-3 px-6 font-semibold text-gray-900">Personnel</th>
                    <th className="text-left py-3 px-6 font-semibold text-gray-900">Role & Department</th>
                    <th className="text-left py-3 px-6 font-semibold text-gray-900">Status</th>
                    <th className="text-left py-3 px-6 font-semibold text-gray-900">Location</th>
                    <th className="text-left py-3 px-6 font-semibold text-gray-900">Safety Score</th>
                    <th className="text-left py-3 px-6 font-semibold text-gray-900">Hours</th>
                    <th className="text-left py-3 px-6 font-semibold text-gray-900">Last Seen</th>
                    <th className="text-left py-3 px-6 font-semibold text-gray-900">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {filteredPersonnel.map((person) => (
                    <tr key={person.id} className="border-b border-gray-100 hover:bg-gray-50">
                      <td className="py-4 px-6">
                        <div className="flex items-center space-x-3">
                          <div className="w-10 h-10 bg-gray-200 rounded-full flex items-center justify-center">
                            <User className="w-5 h-5 text-gray-600" />
                          </div>
                          <div>
                            <p className="font-medium text-gray-900">{person.name}</p>
                            <p className="text-sm text-gray-600">{person.email}</p>
                          </div>
                        </div>
                      </td>
                      <td className="py-4 px-6">
                        <div>
                          <p className="font-medium text-gray-900">{person.role}</p>
                          <p className="text-sm text-gray-600">{person.department}</p>
                        </div>
                      </td>
                      <td className="py-4 px-6">
                        <span className={`px-2 py-1 text-xs font-semibold rounded-full ${getStatusColor(person.status).bg} ${getStatusColor(person.status).text}`}>
                          {person.status.replace('-', ' ').toUpperCase()}
                        </span>
                      </td>
                      <td className="py-4 px-6">
                        <span className="text-gray-900">{person.currentLocation}</span>
                      </td>
                      <td className="py-4 px-6">
                        <span className={`font-medium ${getSafetyScoreColor(person.safetyScore)}`}>
                          {person.safetyScore}%
                        </span>
                      </td>
                      <td className="py-4 px-6">
                        <span className="text-gray-900">{person.hoursWorked}h</span>
                      </td>
                      <td className="py-4 px-6">
                        <span className="text-sm text-gray-600">{formatLastSeen(person.lastSeen)}</span>
                      </td>
                      <td className="py-4 px-6">
                        <div className="flex items-center space-x-2">
                          <button
                            onClick={() => {
                              setSelectedPerson(person);
                              setShowDetailModal(true);
                            }}
                            className="p-1 hover:bg-gray-200 rounded"
                            title="View Details"
                          >
                            <Eye className="w-4 h-4 text-gray-600" />
                          </button>
                          <button
                            className="p-1 hover:bg-gray-200 rounded"
                            title="More Actions"
                          >
                            <MoreVertical className="w-4 h-4 text-gray-600" />
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <div className="p-6 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
              {filteredPersonnel.map((person) => (
                <div
                  key={person.id}
                  className="bg-white rounded-lg border border-gray-200 p-4 hover:shadow-md transition-all duration-200 cursor-pointer"
                  onClick={() => {
                    setSelectedPerson(person);
                    setShowDetailModal(true);
                  }}
                >
                  <div className="flex items-center justify-between mb-3">
                    <div className="w-12 h-12 bg-gray-200 rounded-full flex items-center justify-center">
                      <User className="w-6 h-6 text-gray-600" />
                    </div>
                    <span className={`px-2 py-1 text-xs font-semibold rounded-full ${getStatusColor(person.status).bg} ${getStatusColor(person.status).text}`}>
                      {person.status.toUpperCase()}
                    </span>
                  </div>
                  
                  <h3 className="font-semibold text-gray-900 mb-1">{person.name}</h3>
                  <p className="text-sm text-gray-600 mb-3">{person.role}</p>
                  
                  <div className="space-y-2 text-xs text-gray-600">
                    <div className="flex items-center space-x-2">
                      <MapPin className="w-3 h-3" />
                      <span>{person.currentLocation}</span>
                    </div>
                    <div className="flex items-center space-x-2">
                      <Shield className="w-3 h-3" />
                      <span>Safety Score: </span>
                      <span className={getSafetyScoreColor(person.safetyScore)}>
                        {person.safetyScore}%
                      </span>
                    </div>
                    <div className="flex items-center space-x-2">
                      <Clock className="w-3 h-3" />
                      <span>Last seen: {formatLastSeen(person.lastSeen)}</span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Personnel Detail Modal */}
      <PersonnelDetailModal />
    </MainLayout>
  );
};

export default PersonnelManagement;