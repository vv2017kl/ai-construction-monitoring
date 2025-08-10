import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  Shield, Lock, Unlock, Key, Users, Eye, Edit3, Trash2,
  Plus, Search, Filter, Crown, AlertTriangle, CheckCircle,
  Settings, User, UserCheck, UserX, MoreVertical, Clock,
  Globe, Building2, Camera, FileText, BarChart3, Wrench,
  Activity, RefreshCw, Download, Upload, Grid, List,
  TrendingUp, Database, Server, Wifi, Monitor, Zap
} from 'lucide-react';
import { useTheme } from '../../context/ThemeContext';
import MainLayout from '../../components/shared/Layout/MainLayout';
import { mockPersonnel, mockDepartments, mockSites } from '../../data/mockData';

const AccessControl = () => {
  const navigate = useNavigate();
  const { theme } = useTheme();
  
  // State management
  const [activeTab, setActiveTab] = useState('roles'); // 'roles', 'permissions', 'users', 'policies'
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedRole, setSelectedRole] = useState(null);
  const [showCreateRoleModal, setShowCreateRoleModal] = useState(false);
  const [showPermissionMatrix, setShowPermissionMatrix] = useState(false);
  const [viewMode, setViewMode] = useState('grid');

  // Mock roles data
  const systemRoles = [
    {
      id: 'role_001',
      name: 'System Administrator',
      description: 'Full system access with all administrative privileges',
      level: 'system',
      userCount: 2,
      color: '#8B5CF6',
      createdAt: new Date('2024-01-10'),
      lastModified: new Date('2024-12-15'),
      permissions: [
        'user_management', 'system_config', 'security_settings', 'audit_access',
        'database_admin', 'backup_restore', 'integration_settings', 'ai_model_management'
      ],
      inherits: [],
      sites: ['All Sites'],
      isDefault: true,
      riskLevel: 'critical'
    },
    {
      id: 'role_002',
      name: 'Site Administrator',
      description: 'Administrative access for specific construction sites',
      level: 'site',
      userCount: 4,
      color: '#3B82F6',
      createdAt: new Date('2024-01-15'),
      lastModified: new Date('2024-12-10'),
      permissions: [
        'site_management', 'user_oversight', 'personnel_management', 'equipment_access',
        'reports_access', 'alert_center', 'camera_control', 'zone_configuration'
      ],
      inherits: ['Site Manager'],
      sites: ['Assigned Sites Only'],
      isDefault: true,
      riskLevel: 'high'
    },
    {
      id: 'role_003',
      name: 'Site Manager',
      description: 'Operational management for construction site activities',
      level: 'management',
      userCount: 6,
      color: '#10B981',
      createdAt: new Date('2024-01-20'),
      lastModified: new Date('2024-11-28'),
      permissions: [
        'site_access', 'personnel_management', 'report_generation', 'alert_management',
        'equipment_oversight', 'safety_compliance', 'progress_tracking'
      ],
      inherits: ['Site Supervisor'],
      sites: ['Assigned Sites Only'],
      isDefault: true,
      riskLevel: 'medium'
    },
    {
      id: 'role_004',
      name: 'Site Supervisor',
      description: 'On-site supervision and coordination of daily operations',
      level: 'operations',
      userCount: 8,
      color: '#F59E0B',
      createdAt: new Date('2024-02-01'),
      lastModified: new Date('2024-12-01'),
      permissions: [
        'site_access', 'personnel_coordination', 'basic_reports', 'safety_alerts',
        'equipment_logs', 'zone_access', 'time_tracking'
      ],
      inherits: ['Site Worker'],
      sites: ['Assigned Sites Only'],
      isDefault: true,
      riskLevel: 'medium'
    },
    {
      id: 'role_005',
      name: 'Safety Inspector',
      description: 'Safety compliance monitoring and incident management',
      level: 'specialized',
      userCount: 5,
      color: '#EF4444',
      createdAt: new Date('2024-02-10'),
      lastModified: new Date('2024-11-20'),
      permissions: [
        'safety_management', 'alert_center', 'compliance_access', 'incident_reports',
        'audit_trail', 'training_management', 'regulatory_reports', 'site_access'
      ],
      inherits: ['Site Worker'],
      sites: ['Multi-Site Access'],
      isDefault: true,
      riskLevel: 'medium'
    },
    {
      id: 'role_006',
      name: 'Equipment Operator',
      description: 'Heavy machinery and equipment operation privileges',
      level: 'operations',
      userCount: 12,
      color: '#6B7280',
      createdAt: new Date('2024-02-15'),
      lastModified: new Date('2024-10-15'),
      permissions: [
        'equipment_access', 'machinery_logs', 'maintenance_alerts', 'site_access',
        'basic_reports', 'safety_compliance'
      ],
      inherits: ['Site Worker'],
      sites: ['Assigned Sites Only'],
      isDefault: true,
      riskLevel: 'low'
    },
    {
      id: 'role_007',
      name: 'Site Worker',
      description: 'Basic site access for construction workers',
      level: 'worker',
      userCount: 28,
      color: '#84CC16',
      createdAt: new Date('2024-03-01'),
      lastModified: new Date('2024-09-10'),
      permissions: [
        'site_access', 'basic_alerts', 'time_tracking', 'safety_compliance'
      ],
      inherits: [],
      sites: ['Assigned Sites Only'],
      isDefault: true,
      riskLevel: 'low'
    },
    {
      id: 'role_008',
      name: 'Quality Control',
      description: 'Quality assurance and testing oversight',
      level: 'specialized',
      userCount: 4,
      color: '#8B5CF6',
      createdAt: new Date('2024-03-10'),
      lastModified: new Date('2024-11-05'),
      permissions: [
        'quality_management', 'testing_access', 'compliance_verification', 
        'documentation_access', 'progress_reports', 'site_access'
      ],
      inherits: ['Site Worker'],
      sites: ['Assigned Sites Only'],
      isDefault: true,
      riskLevel: 'medium'
    }
  ];

  // Mock permissions data
  const systemPermissions = [
    { id: 'user_management', name: 'User Management', category: 'Administration', description: 'Create, edit, delete user accounts', riskLevel: 'high' },
    { id: 'system_config', name: 'System Configuration', category: 'Administration', description: 'Modify system settings and parameters', riskLevel: 'critical' },
    { id: 'security_settings', name: 'Security Settings', category: 'Security', description: 'Configure security policies and access controls', riskLevel: 'critical' },
    { id: 'audit_access', name: 'Audit Access', category: 'Security', description: 'View audit logs and system activities', riskLevel: 'medium' },
    { id: 'database_admin', name: 'Database Administration', category: 'System', description: 'Database management and maintenance', riskLevel: 'critical' },
    { id: 'site_management', name: 'Site Management', category: 'Operations', description: 'Manage site configurations and settings', riskLevel: 'high' },
    { id: 'personnel_management', name: 'Personnel Management', category: 'HR', description: 'Manage personnel assignments and schedules', riskLevel: 'medium' },
    { id: 'equipment_access', name: 'Equipment Access', category: 'Equipment', description: 'Access and control site equipment', riskLevel: 'medium' },
    { id: 'camera_control', name: 'Camera Control', category: 'Surveillance', description: 'Control PTZ cameras and recordings', riskLevel: 'medium' },
    { id: 'alert_center', name: 'Alert Center', category: 'Monitoring', description: 'Manage alerts and notifications', riskLevel: 'low' },
    { id: 'reports_access', name: 'Reports Access', category: 'Analytics', description: 'Generate and view reports', riskLevel: 'low' },
    { id: 'ai_model_management', name: 'AI Model Management', category: 'AI', description: 'Manage AI models and configurations', riskLevel: 'high' },
    { id: 'safety_management', name: 'Safety Management', category: 'Safety', description: 'Safety oversight and compliance', riskLevel: 'medium' },
    { id: 'quality_management', name: 'Quality Management', category: 'Quality', description: 'Quality control and assurance', riskLevel: 'medium' },
    { id: 'site_access', name: 'Site Access', category: 'Basic', description: 'Basic site entry and navigation', riskLevel: 'low' }
  ];

  const [roles, setRoles] = useState(systemRoles);
  const [permissions, setPermissions] = useState(systemPermissions);

  // Filter roles
  const filteredRoles = roles.filter(role => 
    role.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    role.description.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const getRiskLevelColor = (level) => {
    switch (level) {
      case 'critical': return { bg: 'bg-red-100', text: 'text-red-800', border: 'border-red-200' };
      case 'high': return { bg: 'bg-orange-100', text: 'text-orange-800', border: 'border-orange-200' };
      case 'medium': return { bg: 'bg-yellow-100', text: 'text-yellow-800', border: 'border-yellow-200' };
      case 'low': return { bg: 'bg-green-100', text: 'text-green-800', border: 'border-green-200' };
      default: return { bg: 'bg-gray-100', text: 'text-gray-800', border: 'border-gray-200' };
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

  const RoleCard = ({ role }) => {
    const riskConfig = getRiskLevelColor(role.riskLevel);
    
    return (
      <div className="bg-white rounded-lg border border-gray-200 p-6 hover:shadow-md transition-all duration-200">
        {/* Header */}
        <div className="flex items-start justify-between mb-4">
          <div className="flex items-start space-x-3">
            <div 
              className="w-10 h-10 rounded-lg flex items-center justify-center"
              style={{ backgroundColor: role.color + '20' }}
            >
              <Shield className="w-5 h-5" style={{ color: role.color }} />
            </div>
            <div>
              <h3 className="font-semibold text-gray-900 mb-1">{role.name}</h3>
              <p className="text-sm text-gray-600 mb-2 line-clamp-2">{role.description}</p>
              <div className="flex items-center space-x-2">
                <span className={`px-2 py-1 text-xs font-semibold rounded-md border ${riskConfig.bg} ${riskConfig.text} ${riskConfig.border}`}>
                  {role.riskLevel.toUpperCase()} RISK
                </span>
                {role.isDefault && (
                  <span className="px-2 py-1 text-xs font-semibold rounded-md border border-blue-200 bg-blue-100 text-blue-800">
                    DEFAULT
                  </span>
                )}
              </div>
            </div>
          </div>
          
          <button className="p-1 text-gray-400 hover:text-gray-600">
            <MoreVertical className="w-4 h-4" />
          </button>
        </div>

        {/* Metrics */}
        <div className="grid grid-cols-2 gap-4 mb-4">
          <div className="text-center">
            <div className="text-2xl font-bold text-blue-600">{role.userCount}</div>
            <div className="text-xs text-gray-600">Users Assigned</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-green-600">{role.permissions.length}</div>
            <div className="text-xs text-gray-600">Permissions</div>
          </div>
        </div>

        {/* Details */}
        <div className="space-y-2 mb-4">
          <div className="flex justify-between items-center text-sm">
            <span className="text-gray-600">Level:</span>
            <span className="font-medium capitalize">{role.level}</span>
          </div>
          <div className="flex justify-between items-center text-sm">
            <span className="text-gray-600">Site Access:</span>
            <span className="font-medium text-xs">{role.sites[0]}</span>
          </div>
          {role.inherits.length > 0 && (
            <div className="flex justify-between items-center text-sm">
              <span className="text-gray-600">Inherits:</span>
              <span className="font-medium text-xs">{role.inherits[0]}</span>
            </div>
          )}
        </div>

        {/* Actions */}
        <div className="flex items-center justify-between pt-4 border-t border-gray-100">
          <div className="text-xs text-gray-500">
            Modified {new Date(role.lastModified).toLocaleDateString()}
          </div>
          <div className="flex space-x-2">
            <button
              onClick={() => {
                setSelectedRole(role);
                setShowPermissionMatrix(true);
              }}
              className="p-1 hover:bg-gray-100 rounded"
              title="View Permissions"
            >
              <Key className="w-4 h-4 text-green-600" />
            </button>
            <button
              onClick={() => navigate(`/admin/users?role=${role.name}`)}
              className="p-1 hover:bg-gray-100 rounded"
              title="View Users"
            >
              <Users className="w-4 h-4 text-blue-600" />
            </button>
            <button
              className="p-1 hover:bg-gray-100 rounded"
              title="Edit Role"
            >
              <Edit3 className="w-4 h-4 text-gray-600" />
            </button>
          </div>
        </div>
      </div>
    );
  };

  const PermissionMatrix = () => {
    if (!showPermissionMatrix || !selectedRole) return null;

    const categories = [...new Set(permissions.map(p => p.category))];
    
    return (
      <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
        <div className="bg-white rounded-lg max-w-4xl w-full max-h-[90vh] overflow-hidden">
          <div className="p-6 border-b border-gray-200">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-xl font-bold text-gray-900">Permission Matrix</h2>
                <p className="text-sm text-gray-600">Role: {selectedRole.name}</p>
              </div>
              <button 
                onClick={() => setShowPermissionMatrix(false)}
                className="p-2 hover:bg-gray-100 rounded-lg"
              >
                <X className="w-5 h-5" />
              </button>
            </div>
          </div>
          
          <div className="p-6 overflow-y-auto max-h-[70vh]">
            {categories.map(category => (
              <div key={category} className="mb-6">
                <h3 className="font-semibold text-gray-900 mb-3 flex items-center">
                  <Shield className="w-4 h-4 mr-2 text-blue-600" />
                  {category}
                </h3>
                <div className="space-y-2">
                  {permissions.filter(p => p.category === category).map(permission => {
                    const hasPermission = selectedRole.permissions.includes(permission.id);
                    const riskConfig = getRiskLevelColor(permission.riskLevel);
                    
                    return (
                      <div key={permission.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                        <div className="flex items-center space-x-3">
                          <div className={`p-1 rounded ${hasPermission ? 'bg-green-100' : 'bg-gray-200'}`}>
                            {hasPermission ? (
                              <CheckCircle className="w-4 h-4 text-green-600" />
                            ) : (
                              <X className="w-4 h-4 text-gray-400" />
                            )}
                          </div>
                          <div>
                            <div className="font-medium text-gray-900">{permission.name}</div>
                            <div className="text-sm text-gray-600">{permission.description}</div>
                          </div>
                        </div>
                        <span className={`px-2 py-1 text-xs font-semibold rounded border ${riskConfig.bg} ${riskConfig.text} ${riskConfig.border}`}>
                          {permission.riskLevel.toUpperCase()}
                        </span>
                      </div>
                    );
                  })}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  };

  const CreateRoleModal = () => {
    if (!showCreateRoleModal) return null;

    return (
      <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
        <div className="bg-white rounded-lg max-w-2xl w-full max-h-[90vh] overflow-hidden">
          <div className="p-6 border-b border-gray-200">
            <h2 className="text-xl font-bold text-gray-900">Create New Role</h2>
          </div>
          
          <div className="p-6 overflow-y-auto">
            <div className="space-y-6">
              <div className="grid grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Role Name</label>
                  <input
                    type="text"
                    className="w-full px-3 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="Enter role name"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Risk Level</label>
                  <select className="w-full px-3 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
                    <option value="low">Low Risk</option>
                    <option value="medium">Medium Risk</option>
                    <option value="high">High Risk</option>
                    <option value="critical">Critical Risk</option>
                  </select>
                </div>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Description</label>
                <textarea
                  rows={3}
                  className="w-full px-3 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="Enter role description and responsibilities"
                />
              </div>

              <div className="grid grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Inherits From</label>
                  <select className="w-full px-3 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
                    <option value="">Select base role (optional)...</option>
                    {roles.map(role => (
                      <option key={role.id} value={role.id}>{role.name}</option>
                    ))}
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Site Access</label>
                  <select className="w-full px-3 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
                    <option value="assigned">Assigned Sites Only</option>
                    <option value="all">All Sites</option>
                    <option value="multi">Multi-Site Access</option>
                  </select>
                </div>
              </div>
            </div>
          </div>
          
          <div className="p-6 border-t border-gray-200 flex justify-end space-x-3">
            <button
              onClick={() => setShowCreateRoleModal(false)}
              className="px-4 py-2 text-gray-700 hover:bg-gray-100 rounded-lg transition-colors"
            >
              Cancel
            </button>
            <button className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
              Create Role
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
              <h1 className="text-xl font-bold text-gray-900">Access Control</h1>
              <div className="flex items-center space-x-2 text-sm text-gray-600">
                <Shield className="w-3 h-3" />
                <span>{roles.length} roles</span>
                <span>•</span>
                <span>{permissions.length} permissions</span>
                <span>•</span>
                <span>{roles.reduce((sum, role) => sum + role.userCount, 0)} users managed</span>
              </div>
            </div>

            <div className="flex items-center space-x-4">
              <button className="flex items-center space-x-2 px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors">
                <Download className="w-4 h-4" />
                <span>Export</span>
              </button>

              <button
                onClick={() => setShowCreateRoleModal(true)}
                className="flex items-center space-x-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
              >
                <Plus className="w-4 h-4" />
                <span>Add Role</span>
              </button>
            </div>
          </div>
        </div>

        {/* Tabs */}
        <div className="bg-white border-b border-gray-200 px-6">
          <nav className="flex space-x-8">
            {[
              { id: 'roles', name: 'Roles', icon: Crown },
              { id: 'permissions', name: 'Permissions', icon: Key },
              { id: 'users', name: 'User Assignments', icon: Users },
              { id: 'policies', name: 'Security Policies', icon: Shield }
            ].map((tab) => {
              const Icon = tab.icon;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`flex items-center space-x-2 py-4 border-b-2 font-medium text-sm ${
                    activeTab === tab.id
                      ? 'border-blue-500 text-blue-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700'
                  }`}
                >
                  <Icon className="w-4 h-4" />
                  <span>{tab.name}</span>
                </button>
              );
            })}
          </nav>
        </div>

        {/* Statistics */}
        <div className="px-6 py-4 bg-gray-50 border-b border-gray-200">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <StatCard
              title="Total Roles"
              value={roles.length}
              icon={Crown}
              color={theme.primary[500]}
            />
            <StatCard
              title="Active Users"
              value={roles.reduce((sum, role) => sum + role.userCount, 0)}
              subtitle="With assigned roles"
              icon={Users}
              color={theme.success[500]}
            />
            <StatCard
              title="Critical Roles"
              value={roles.filter(role => role.riskLevel === 'critical').length}
              subtitle="High-risk access"
              icon={AlertTriangle}
              color={theme.danger[500]}
            />
            <StatCard
              title="System Permissions"
              value={permissions.length}
              subtitle="Available permissions"
              icon={Key}
              color={theme.warning[500]}
            />
          </div>
        </div>

        {/* Search and Filters */}
        <div className="px-6 py-4 bg-white border-b border-gray-200">
          <div className="flex items-center space-x-4">
            <div className="flex-1">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
                <input
                  type="text"
                  placeholder="Search roles and permissions..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>
            </div>

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
          </div>
        </div>

        {/* Main Content */}
        <div className="flex-1 overflow-auto">
          {activeTab === 'roles' && (
            <div className="p-6">
              <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
                {filteredRoles.map((role) => (
                  <RoleCard key={role.id} role={role} />
                ))}
              </div>
            </div>
          )}

          {activeTab === 'permissions' && (
            <div className="p-6">
              <div className="bg-white rounded-lg border border-gray-200">
                <div className="p-6 border-b border-gray-200">
                  <h3 className="text-lg font-semibold text-gray-900">System Permissions</h3>
                  <p className="text-sm text-gray-600">Manage individual permissions and access rights</p>
                </div>
                <div className="p-6">
                  {[...new Set(permissions.map(p => p.category))].map(category => (
                    <div key={category} className="mb-6">
                      <h4 className="font-semibold text-gray-900 mb-3 flex items-center">
                        <Key className="w-4 h-4 mr-2 text-blue-600" />
                        {category} Permissions
                      </h4>
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        {permissions.filter(p => p.category === category).map(permission => {
                          const riskConfig = getRiskLevelColor(permission.riskLevel);
                          return (
                            <div key={permission.id} className="p-4 bg-gray-50 rounded-lg border border-gray-200">
                              <div className="flex items-start justify-between">
                                <div>
                                  <h5 className="font-medium text-gray-900">{permission.name}</h5>
                                  <p className="text-sm text-gray-600 mt-1">{permission.description}</p>
                                </div>
                                <span className={`px-2 py-1 text-xs font-semibold rounded ${riskConfig.bg} ${riskConfig.text}`}>
                                  {permission.riskLevel.toUpperCase()}
                                </span>
                              </div>
                            </div>
                          );
                        })}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}

          {activeTab === 'users' && (
            <div className="p-6">
              <div className="bg-white rounded-lg border border-gray-200">
                <div className="p-6 border-b border-gray-200">
                  <h3 className="text-lg font-semibold text-gray-900">User Role Assignments</h3>
                  <p className="text-sm text-gray-600">View and manage role assignments for all users</p>
                </div>
                <div className="p-6">
                  <p className="text-center text-gray-500 py-12">
                    User assignment interface - Integration with User Directory
                  </p>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'policies' && (
            <div className="p-6">
              <div className="bg-white rounded-lg border border-gray-200">
                <div className="p-6 border-b border-gray-200">
                  <h3 className="text-lg font-semibold text-gray-900">Security Policies</h3>
                  <p className="text-sm text-gray-600">Configure system-wide security policies and access controls</p>
                </div>
                <div className="p-6">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div className="p-4 bg-blue-50 rounded-lg border border-blue-200">
                      <h4 className="font-semibold text-blue-900 mb-2">Password Policy</h4>
                      <p className="text-sm text-blue-700">Minimum 8 characters, special characters required</p>
                    </div>
                    <div className="p-4 bg-green-50 rounded-lg border border-green-200">
                      <h4 className="font-semibold text-green-900 mb-2">Session Timeout</h4>
                      <p className="text-sm text-green-700">Automatic logout after 60 minutes of inactivity</p>
                    </div>
                    <div className="p-4 bg-yellow-50 rounded-lg border border-yellow-200">
                      <h4 className="font-semibold text-yellow-900 mb-2">Two-Factor Authentication</h4>
                      <p className="text-sm text-yellow-700">Required for administrative roles</p>
                    </div>
                    <div className="p-4 bg-red-50 rounded-lg border border-red-200">
                      <h4 className="font-semibold text-red-900 mb-2">Failed Login Attempts</h4>
                      <p className="text-sm text-red-700">Account locked after 5 failed attempts</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Modals */}
      <CreateRoleModal />
      <PermissionMatrix />
    </MainLayout>
  );
};

export default AccessControl;