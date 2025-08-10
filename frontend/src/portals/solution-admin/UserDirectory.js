import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  Users, UserPlus, Search, Filter, Download, Upload,
  Edit, Trash2, Eye, MoreVertical, Shield, Clock,
  Mail, Phone, MapPin, Building2, User, CheckCircle,
  XCircle, AlertTriangle, Settings, Key, Lock,
  Calendar, Activity, TrendingUp, BarChart3, Globe
} from 'lucide-react';
import { useTheme } from '../../context/ThemeContext';
import MainLayout from '../../components/shared/Layout/MainLayout';
import { mockSites, mockUser, mockPersonnel, mockDepartments } from '../../data/mockData';

const UserDirectory = () => {
  const navigate = useNavigate();
  const { theme } = useTheme();
  
  // State management
  const [users, setUsers] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterRole, setFilterRole] = useState('all');
  const [filterSite, setFilterSite] = useState('all');
  const [filterStatus, setFilterStatus] = useState('all');
  const [filterDepartment, setFilterDepartment] = useState('all');
  const [sortBy, setSortBy] = useState('lastActive');
  const [sortOrder, setSortOrder] = useState('desc');
  const [selectedUsers, setSelectedUsers] = useState([]);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [showEditModal, setShowEditModal] = useState(false);
  const [selectedUser, setSelectedUser] = useState(null);
  const [viewMode, setViewMode] = useState('table'); // 'table', 'cards'

  // Generate comprehensive mock user data
  const generateMockUsers = () => [
    {
      id: 'u001',
      firstName: 'John',
      lastName: 'Mitchell',
      email: 'john.mitchell@constructionai.com',
      phone: '+1 (555) 0123',
      role: 'Site Supervisor',
      department: 'Construction',
      site: 'Downtown Construction Site',
      status: 'active',
      lastActive: new Date(Date.now() - 15 * 60 * 1000),
      createdAt: new Date(Date.now() - 180 * 24 * 60 * 60 * 1000),
      loginCount: 247,
      permissions: ['site_access', 'personnel_management', 'report_generation'],
      avatar: null,
      isOnline: true,
      lastLocation: 'Zone A - Foundation',
      safetyScore: 95,
      completedAssessments: 43
    },
    {
      id: 'u002',
      firstName: 'Sarah',
      lastName: 'Chen',
      email: 'sarah.chen@constructionai.com',
      phone: '+1 (555) 0124',
      role: 'Safety Inspector',
      department: 'Safety',
      site: 'Harbor Bridge Project',
      status: 'active',
      lastActive: new Date(Date.now() - 5 * 60 * 1000),
      createdAt: new Date(Date.now() - 120 * 24 * 60 * 60 * 1000),
      loginCount: 189,
      permissions: ['site_access', 'safety_management', 'alert_center'],
      avatar: null,
      isOnline: true,
      lastLocation: 'Zone B - Steel Frame',
      safetyScore: 100,
      completedAssessments: 67
    },
    {
      id: 'u003',
      firstName: 'Mike',
      lastName: 'Rodriguez',
      email: 'mike.rodriguez@constructionai.com',
      phone: '+1 (555) 0125',
      role: 'Equipment Operator',
      department: 'Equipment',
      site: 'Industrial Complex Alpha',
      status: 'active',
      lastActive: new Date(Date.now() - 30 * 60 * 1000),
      createdAt: new Date(Date.now() - 90 * 24 * 60 * 60 * 1000),
      loginCount: 134,
      permissions: ['site_access', 'equipment_management'],
      avatar: null,
      isOnline: false,
      lastLocation: 'Equipment Yard',
      safetyScore: 88,
      completedAssessments: 29
    },
    {
      id: 'u004',
      firstName: 'Emma',
      lastName: 'Thompson',
      email: 'emma.thompson@constructionai.com',
      phone: '+1 (555) 0126',
      role: 'Quality Control',
      department: 'Quality Assurance',
      site: 'Residential Tower Phase 2',
      status: 'active',
      lastActive: new Date(Date.now() - 2 * 60 * 60 * 1000),
      createdAt: new Date(Date.now() - 200 * 24 * 60 * 60 * 1000),
      loginCount: 298,
      permissions: ['site_access', 'quality_management', 'report_generation'],
      avatar: null,
      isOnline: false,
      lastLocation: 'Zone C - Quality Lab',
      safetyScore: 96,
      completedAssessments: 58
    },
    {
      id: 'u005',
      firstName: 'David',
      lastName: 'Park',
      email: 'david.park@constructionai.com',
      phone: '+1 (555) 0127',
      role: 'Project Manager',
      department: 'Management',
      site: 'Multiple Sites',
      status: 'active',
      lastActive: new Date(Date.now() - 45 * 60 * 1000),
      createdAt: new Date(Date.now() - 300 * 24 * 60 * 60 * 1000),
      loginCount: 456,
      permissions: ['multi_site_access', 'user_management', 'analytics', 'report_generation'],
      avatar: null,
      isOnline: true,
      lastLocation: 'Remote Office',
      safetyScore: 92,
      completedAssessments: 12
    },
    {
      id: 'u006',
      firstName: 'Lisa',
      lastName: 'Wang',
      email: 'lisa.wang@constructionai.com',
      phone: '+1 (555) 0128',
      role: 'System Administrator',
      department: 'IT',
      site: 'All Sites',
      status: 'active',
      lastActive: new Date(Date.now() - 10 * 60 * 1000),
      createdAt: new Date(Date.now() - 400 * 24 * 60 * 60 * 1000),
      loginCount: 789,
      permissions: ['admin_access', 'user_management', 'system_config', 'all_sites'],
      avatar: null,
      isOnline: true,
      lastLocation: 'Data Center',
      safetyScore: null,
      completedAssessments: 0
    },
    {
      id: 'u007',
      firstName: 'Robert',
      lastName: 'Johnson',
      email: 'robert.johnson@constructionai.com',
      phone: '+1 (555) 0129',
      role: 'Field Worker',
      department: 'Construction',
      site: 'Downtown Construction Site',
      status: 'suspended',
      lastActive: new Date(Date.now() - 7 * 24 * 60 * 60 * 1000),
      createdAt: new Date(Date.now() - 60 * 24 * 60 * 60 * 1000),
      loginCount: 67,
      permissions: ['site_access'],
      avatar: null,
      isOnline: false,
      lastLocation: 'Zone D - Inactive',
      safetyScore: 74,
      completedAssessments: 8
    },
    {
      id: 'u008',
      firstName: 'Maria',
      lastName: 'Garcia',
      email: 'maria.garcia@constructionai.com',
      phone: '+1 (555) 0130',
      role: 'Compliance Officer',
      department: 'Compliance',
      site: 'All Sites',
      status: 'active',
      lastActive: new Date(Date.now() - 1 * 60 * 60 * 1000),
      createdAt: new Date(Date.now() - 250 * 24 * 60 * 60 * 1000),
      loginCount: 223,
      permissions: ['compliance_access', 'audit_trail', 'regulatory_reports'],
      avatar: null,
      isOnline: false,
      lastLocation: 'Compliance Office',
      safetyScore: 98,
      completedAssessments: 34
    }
  ];

  useEffect(() => {
    setUsers(generateMockUsers());
  }, []);

  // Filter and sort users
  const filteredUsers = users
    .filter(user => {
      const searchMatch = user.firstName.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         user.lastName.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         user.email.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         user.role.toLowerCase().includes(searchTerm.toLowerCase());
      
      const roleMatch = filterRole === 'all' || user.role === filterRole;
      const siteMatch = filterSite === 'all' || user.site === filterSite;
      const statusMatch = filterStatus === 'all' || user.status === filterStatus;
      const departmentMatch = filterDepartment === 'all' || user.department === filterDepartment;
      
      return searchMatch && roleMatch && siteMatch && statusMatch && departmentMatch;
    })
    .sort((a, b) => {
      let aValue = a[sortBy];
      let bValue = b[sortBy];
      
      if (sortBy === 'lastActive') {
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

  const getStatusConfig = (status) => {
    switch (status) {
      case 'active': return { bg: 'bg-green-100', text: 'text-green-800', icon: CheckCircle };
      case 'suspended': return { bg: 'bg-red-100', text: 'text-red-800', icon: XCircle };
      case 'inactive': return { bg: 'bg-gray-100', text: 'text-gray-800', icon: AlertTriangle };
      default: return { bg: 'bg-gray-100', text: 'text-gray-800', icon: User };
    }
  };

  const formatLastActive = (timestamp) => {
    const now = new Date();
    const lastActive = new Date(timestamp);
    const diffMinutes = Math.floor((now - lastActive) / (1000 * 60));
    const diffHours = Math.floor(diffMinutes / 60);
    const diffDays = Math.floor(diffHours / 24);

    if (diffMinutes < 60) return `${diffMinutes}m ago`;
    if (diffHours < 24) return `${diffHours}h ago`;
    return `${diffDays}d ago`;
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

  const UserCard = ({ user }) => {
    const statusConfig = getStatusConfig(user.status);
    const StatusIcon = statusConfig.icon;
    
    return (
      <div className="bg-white rounded-lg border border-gray-200 p-6 hover:shadow-md transition-all duration-200">
        <div className="flex items-start justify-between mb-4">
          <div className="flex items-start space-x-3">
            <div 
              className="w-12 h-12 rounded-full flex items-center justify-center text-white font-bold"
              style={{ backgroundColor: theme.primary[500] }}
            >
              {user.firstName[0]}{user.lastName[0]}
            </div>
            
            <div>
              <h3 className="font-semibold text-gray-900">{user.firstName} {user.lastName}</h3>
              <p className="text-sm text-gray-600">{user.role}</p>
              <p className="text-xs text-gray-500">{user.department}</p>
            </div>
          </div>
          
          <div className="flex items-center space-x-2">
            {user.isOnline && (
              <div className="w-3 h-3 bg-green-500 rounded-full animate-pulse"></div>
            )}
            <span className={`px-2 py-1 text-xs font-semibold rounded-full ${statusConfig.bg} ${statusConfig.text}`}>
              {user.status.toUpperCase()}
            </span>
          </div>
        </div>

        <div className="space-y-2 mb-4">
          <div className="flex items-center space-x-2 text-sm text-gray-600">
            <Mail className="w-3 h-3" />
            <span>{user.email}</span>
          </div>
          <div className="flex items-center space-x-2 text-sm text-gray-600">
            <MapPin className="w-3 h-3" />
            <span>{user.site}</span>
          </div>
          <div className="flex items-center space-x-2 text-sm text-gray-600">
            <Clock className="w-3 h-3" />
            <span>Active {formatLastActive(user.lastActive)}</span>
          </div>
        </div>

        <div className="flex items-center justify-between pt-4 border-t border-gray-100">
          <div className="flex items-center space-x-4 text-xs text-gray-500">
            <span>{user.loginCount} logins</span>
            {user.safetyScore && (
              <span>Safety: {user.safetyScore}%</span>
            )}
          </div>
          
          <div className="flex space-x-2">
            <button
              onClick={() => {
                setSelectedUser(user);
                setShowEditModal(true);
              }}
              className="p-1 hover:bg-gray-100 rounded"
              title="Edit User"
            >
              <Edit className="w-4 h-4 text-gray-600" />
            </button>
            <button className="p-1 hover:bg-gray-100 rounded" title="View Details">
              <Eye className="w-4 h-4 text-blue-600" />
            </button>
            <button className="p-1 hover:bg-gray-100 rounded" title="More Actions">
              <MoreVertical className="w-4 h-4 text-gray-600" />
            </button>
          </div>
        </div>
      </div>
    );
  };

  const CreateUserModal = () => {
    if (!showCreateModal) return null;

    return (
      <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
        <div className="bg-white rounded-lg max-w-2xl w-full max-h-[90vh] overflow-hidden">
          <div className="p-6 border-b border-gray-200">
            <h2 className="text-xl font-bold text-gray-900">Create New User</h2>
          </div>
          
          <div className="p-6 overflow-y-auto">
            <div className="grid grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">First Name</label>
                <input
                  type="text"
                  className="w-full px-3 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:border-transparent"
                  placeholder="Enter first name"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Last Name</label>
                <input
                  type="text"
                  className="w-full px-3 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:border-transparent"
                  placeholder="Enter last name"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Email</label>
                <input
                  type="email"
                  className="w-full px-3 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:border-transparent"
                  placeholder="Enter email address"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Phone</label>
                <input
                  type="tel"
                  className="w-full px-3 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:border-transparent"
                  placeholder="Enter phone number"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Role</label>
                <select className="w-full px-3 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:border-transparent">
                  <option value="">Select role...</option>
                  <option value="Field Worker">Field Worker</option>
                  <option value="Site Supervisor">Site Supervisor</option>
                  <option value="Safety Inspector">Safety Inspector</option>
                  <option value="Equipment Operator">Equipment Operator</option>
                  <option value="Quality Control">Quality Control</option>
                  <option value="Project Manager">Project Manager</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Department</label>
                <select className="w-full px-3 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:border-transparent">
                  <option value="">Select department...</option>
                  <option value="Construction">Construction</option>
                  <option value="Safety">Safety</option>
                  <option value="Equipment">Equipment</option>
                  <option value="Quality Assurance">Quality Assurance</option>
                  <option value="Management">Management</option>
                </select>
              </div>
              <div className="col-span-2">
                <label className="block text-sm font-medium text-gray-700 mb-2">Site Assignment</label>
                <select className="w-full px-3 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:border-transparent">
                  <option value="">Select site...</option>
                  {mockSites.map(site => (
                    <option key={site.id} value={site.name}>{site.name}</option>
                  ))}
                </select>
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
              Create User
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
              <h1 className="text-xl font-bold text-gray-900">User Directory</h1>
              <div className="flex items-center space-x-2 text-sm text-gray-600">
                <Globe className="w-3 h-3" />
                <span>All Sites</span>
                <span>•</span>
                <span>{filteredUsers.length} users</span>
                <span>•</span>
                <span>{filteredUsers.filter(u => u.isOnline).length} online now</span>
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

              <button className="flex items-center space-x-2 px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors">
                <Download className="w-4 h-4" />
                <span>Export</span>
              </button>

              <button
                onClick={() => setShowCreateModal(true)}
                className="flex items-center space-x-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
              >
                <UserPlus className="w-4 h-4" />
                <span>Add User</span>
              </button>
            </div>
          </div>
        </div>

        {/* Statistics */}
        <div className="px-6 py-4 bg-gray-50 border-b border-gray-200">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <StatCard
              title="Total Users"
              value={users.length}
              icon={Users}
              color={theme.primary[500]}
            />
            <StatCard
              title="Online Users"
              value={users.filter(u => u.isOnline).length}
              subtitle="Currently active"
              icon={Activity}
              color={theme.success[500]}
            />
            <StatCard
              title="Active Users"
              value={users.filter(u => u.status === 'active').length}
              subtitle="Not suspended"
              icon={CheckCircle}
              color={theme.warning[500]}
            />
            <StatCard
              title="New This Month"
              value={users.filter(u => new Date(u.createdAt) > new Date(Date.now() - 30 * 24 * 60 * 60 * 1000)).length}
              subtitle="Recent additions"
              icon={TrendingUp}
              color={theme.secondary[500]}
            />
          </div>
        </div>

        {/* Filters */}
        <div className="px-6 py-4 bg-white border-b border-gray-200">
          <div className="grid grid-cols-1 md:grid-cols-6 gap-4">
            {/* Search */}
            <div className="relative">
              <Search className="w-4 h-4 absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
              <input
                type="text"
                placeholder="Search users..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-10 pr-4 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:border-transparent"
                style={{ '--tw-ring-color': theme.primary[500] + '40' }}
              />
            </div>

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
              <option value="Project Manager">Project Manager</option>
              <option value="System Administrator">System Administrator</option>
            </select>

            {/* Site Filter */}
            <select
              value={filterSite}
              onChange={(e) => setFilterSite(e.target.value)}
              className="px-3 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:border-transparent"
            >
              <option value="all">All Sites</option>
              {mockSites.map(site => (
                <option key={site.id} value={site.name}>{site.name}</option>
              ))}
              <option value="Multiple Sites">Multiple Sites</option>
              <option value="All Sites">All Sites</option>
            </select>

            {/* Status Filter */}
            <select
              value={filterStatus}
              onChange={(e) => setFilterStatus(e.target.value)}
              className="px-3 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:border-transparent"
            >
              <option value="all">All Status</option>
              <option value="active">Active</option>
              <option value="suspended">Suspended</option>
              <option value="inactive">Inactive</option>
            </select>

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
              <option value="Management">Management</option>
              <option value="IT">IT</option>
              <option value="Compliance">Compliance</option>
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
              <option value="lastActive-desc">Recently Active</option>
              <option value="firstName-asc">Name A-Z</option>
              <option value="firstName-desc">Name Z-A</option>
              <option value="createdAt-desc">Newest First</option>
              <option value="loginCount-desc">Most Active</option>
            </select>
          </div>
        </div>

        {/* User List */}
        <div className="flex-1 overflow-auto">
          {viewMode === 'cards' ? (
            <div className="p-6 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {filteredUsers.map((user) => (
                <UserCard key={user.id} user={user} />
              ))}
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-gray-50 border-b border-gray-200">
                  <tr>
                    <th className="text-left py-3 px-6 font-semibold text-gray-900">User</th>
                    <th className="text-left py-3 px-6 font-semibold text-gray-900">Role & Department</th>
                    <th className="text-left py-3 px-6 font-semibold text-gray-900">Site</th>
                    <th className="text-left py-3 px-6 font-semibold text-gray-900">Status</th>
                    <th className="text-left py-3 px-6 font-semibold text-gray-900">Last Active</th>
                    <th className="text-left py-3 px-6 font-semibold text-gray-900">Login Count</th>
                    <th className="text-left py-3 px-6 font-semibold text-gray-900">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {filteredUsers.map((user) => {
                    const statusConfig = getStatusConfig(user.status);
                    const StatusIcon = statusConfig.icon;
                    
                    return (
                      <tr key={user.id} className="border-b border-gray-100 hover:bg-gray-50">
                        <td className="py-4 px-6">
                          <div className="flex items-center space-x-3">
                            <div 
                              className="w-10 h-10 rounded-full flex items-center justify-center text-white font-bold text-sm"
                              style={{ backgroundColor: theme.primary[500] }}
                            >
                              {user.firstName[0]}{user.lastName[0]}
                            </div>
                            <div>
                              <div className="flex items-center space-x-2">
                                <p className="font-medium text-gray-900">{user.firstName} {user.lastName}</p>
                                {user.isOnline && (
                                  <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                                )}
                              </div>
                              <p className="text-sm text-gray-600">{user.email}</p>
                            </div>
                          </div>
                        </td>
                        <td className="py-4 px-6">
                          <div>
                            <p className="font-medium text-gray-900">{user.role}</p>
                            <p className="text-sm text-gray-600">{user.department}</p>
                          </div>
                        </td>
                        <td className="py-4 px-6">
                          <span className="text-gray-900">{user.site}</span>
                        </td>
                        <td className="py-4 px-6">
                          <div className="flex items-center space-x-2">
                            <StatusIcon className={`w-4 h-4 ${statusConfig.text}`} />
                            <span className={`px-2 py-1 text-xs font-semibold rounded-full ${statusConfig.bg} ${statusConfig.text}`}>
                              {user.status.toUpperCase()}
                            </span>
                          </div>
                        </td>
                        <td className="py-4 px-6">
                          <span className="text-sm text-gray-600">{formatLastActive(user.lastActive)}</span>
                        </td>
                        <td className="py-4 px-6">
                          <span className="font-medium text-gray-900">{user.loginCount}</span>
                        </td>
                        <td className="py-4 px-6">
                          <div className="flex items-center space-x-2">
                            <button
                              onClick={() => {
                                setSelectedUser(user);
                                setShowEditModal(true);
                              }}
                              className="p-1 hover:bg-gray-200 rounded"
                              title="Edit User"
                            >
                              <Edit className="w-4 h-4 text-gray-600" />
                            </button>
                            <button className="p-1 hover:bg-gray-200 rounded" title="View Details">
                              <Eye className="w-4 h-4 text-blue-600" />
                            </button>
                            <button className="p-1 hover:bg-gray-200 rounded" title="More Actions">
                              <MoreVertical className="w-4 h-4 text-gray-600" />
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
        </div>
      </div>

      {/* Create User Modal */}
      <CreateUserModal />
    </MainLayout>
  );
};

export default UserDirectory;