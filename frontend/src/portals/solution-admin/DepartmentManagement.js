import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  Building2, Users, UserPlus, Search, Plus, Edit3, Trash2, Eye,
  MoreVertical, Crown, MapPin, Calendar, TrendingUp, TrendingDown,
  Award, Target, Clock, Activity, AlertCircle, CheckCircle,
  BarChart3, PieChart, Filter, Download, Upload, RefreshCw,
  Settings, User, Mail, Phone, Grid, List, ArrowUp, ArrowDown
} from 'lucide-react';
import { useTheme } from '../../context/ThemeContext';
import MainLayout from '../../components/shared/Layout/MainLayout';
import { mockPersonnel, mockDepartments, mockSites } from '../../data/mockData';

const DepartmentManagement = () => {
  const navigate = useNavigate();
  const { theme } = useTheme();
  
  // State management
  const [searchTerm, setSearchTerm] = useState('');
  const [sortBy, setSortBy] = useState('name');
  const [sortOrder, setSortOrder] = useState('asc');
  const [viewMode, setViewMode] = useState('grid'); // 'grid' or 'list'
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [showEditModal, setShowEditModal] = useState(false);
  const [selectedDepartment, setSelectedDepartment] = useState(null);
  const [filterSite, setFilterSite] = useState('all');

  // Extended mock department data
  const extendedDepartments = [
    {
      id: 'dept001',
      name: 'Construction',
      description: 'Core construction and building operations',
      personnel: 28,
      manager: 'John Mitchell',
      managerId: 'p001',
      managerEmail: 'j.mitchell@constructionai.com',
      establishedDate: new Date('2024-01-15'),
      budget: 850000,
      status: 'active',
      sites: ['Downtown Construction Site', 'Riverside Apartments'],
      avgSafetyScore: 92,
      productivity: 89,
      completedProjects: 12,
      activeProjects: 4,
      equipmentCount: 15,
      lastActivity: new Date(Date.now() - 2 * 60 * 60 * 1000),
      kpis: {
        efficiency: 87,
        qualityScore: 94,
        budgetUtilization: 78,
        timelineAdherence: 92
      },
      roles: ['Site Supervisor', 'Construction Worker', 'Heavy Equipment Operator', 'Concrete Specialist'],
      monthlyGrowth: 8.5
    },
    {
      id: 'dept002',
      name: 'Safety',
      description: 'Workplace safety, compliance, and risk management',
      personnel: 8,
      manager: 'Sarah Chen',
      managerId: 'p002',
      managerEmail: 's.chen@constructionai.com',
      establishedDate: new Date('2024-01-20'),
      budget: 320000,
      status: 'active',
      sites: ['All Sites'],
      avgSafetyScore: 98,
      productivity: 95,
      completedProjects: 35,
      activeProjects: 8,
      equipmentCount: 12,
      lastActivity: new Date(Date.now() - 1 * 60 * 60 * 1000),
      kpis: {
        efficiency: 96,
        qualityScore: 99,
        budgetUtilization: 85,
        timelineAdherence: 97
      },
      roles: ['Safety Inspector', 'Compliance Officer', 'Training Coordinator', 'Risk Analyst'],
      monthlyGrowth: 12.3
    },
    {
      id: 'dept003',
      name: 'Equipment',
      description: 'Heavy machinery operations and maintenance',
      personnel: 15,
      manager: 'Mike Rodriguez',
      managerId: 'p003',
      managerEmail: 'm.rodriguez@constructionai.com',
      establishedDate: new Date('2024-02-01'),
      budget: 620000,
      status: 'active',
      sites: ['Downtown Construction Site', 'Industrial Complex Alpha'],
      avgSafetyScore: 85,
      productivity: 91,
      completedProjects: 18,
      activeProjects: 6,
      equipmentCount: 45,
      lastActivity: new Date(Date.now() - 3 * 60 * 60 * 1000),
      kpis: {
        efficiency: 89,
        qualityScore: 88,
        budgetUtilization: 92,
        timelineAdherence: 87
      },
      roles: ['Equipment Operator', 'Maintenance Technician', 'Logistics Coordinator'],
      monthlyGrowth: 5.7
    },
    {
      id: 'dept004',
      name: 'Quality Assurance',
      description: 'Quality control, testing, and compliance verification',
      personnel: 6,
      manager: 'Emma Thompson',
      managerId: 'p004',
      managerEmail: 'e.thompson@constructionai.com',
      establishedDate: new Date('2024-02-15'),
      budget: 280000,
      status: 'active',
      sites: ['Residential Tower Phase 2', 'Riverside Apartments'],
      avgSafetyScore: 96,
      productivity: 88,
      completedProjects: 22,
      activeProjects: 5,
      equipmentCount: 8,
      lastActivity: new Date(Date.now() - 5 * 60 * 60 * 1000),
      kpis: {
        efficiency: 91,
        qualityScore: 97,
        budgetUtilization: 76,
        timelineAdherence: 93
      },
      roles: ['Quality Inspector', 'Test Technician', 'Documentation Specialist'],
      monthlyGrowth: 3.2
    },
    {
      id: 'dept005',
      name: 'IT & Technology',
      description: 'System administration, AI management, and technical support',
      personnel: 5,
      manager: 'Lisa Wang',
      managerId: 'admin001',
      managerEmail: 'l.wang@constructionai.com',
      establishedDate: new Date('2024-03-01'),
      budget: 450000,
      status: 'active',
      sites: ['All Sites'],
      avgSafetyScore: null,
      productivity: 93,
      completedProjects: 8,
      activeProjects: 12,
      equipmentCount: 35,
      lastActivity: new Date(Date.now() - 30 * 60 * 1000),
      kpis: {
        efficiency: 95,
        qualityScore: 92,
        budgetUtilization: 88,
        timelineAdherence: 89
      },
      roles: ['System Administrator', 'AI Specialist', 'Network Engineer', 'Support Technician'],
      monthlyGrowth: 15.8
    },
    {
      id: 'dept006',
      name: 'Administration',
      description: 'HR, finance, procurement, and general administration',
      personnel: 4,
      manager: 'Robert Chen',
      managerId: 'admin002',
      managerEmail: 'r.chen@constructionai.com',
      establishedDate: new Date('2024-01-10'),
      budget: 380000,
      status: 'active',
      sites: ['Main Office'],
      avgSafetyScore: null,
      productivity: 86,
      completedProjects: 15,
      activeProjects: 3,
      equipmentCount: 2,
      lastActivity: new Date(Date.now() - 1 * 24 * 60 * 60 * 1000),
      kpis: {
        efficiency: 84,
        qualityScore: 91,
        budgetUtilization: 94,
        timelineAdherence: 88
      },
      roles: ['HR Specialist', 'Finance Analyst', 'Procurement Manager', 'Office Coordinator'],
      monthlyGrowth: -2.1
    }
  ];

  const [departments, setDepartments] = useState(extendedDepartments);

  // Filter and sort departments
  const filteredDepartments = departments
    .filter(dept => {
      const matchesSearch = dept.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                           dept.description.toLowerCase().includes(searchTerm.toLowerCase()) ||
                           dept.manager.toLowerCase().includes(searchTerm.toLowerCase());
      const matchesSite = filterSite === 'all' || dept.sites.some(site => site.includes(filterSite)) || 
                         (filterSite === 'All Sites' && dept.sites.includes('All Sites'));
      
      return matchesSearch && matchesSite;
    })
    .sort((a, b) => {
      let aVal = a[sortBy];
      let bVal = b[sortBy];
      
      if (sortBy === 'lastActivity') {
        aVal = new Date(aVal);
        bVal = new Date(bVal);
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
      case 'restructuring': return { bg: 'bg-yellow-100', text: 'text-yellow-800', dot: 'bg-yellow-500' };
      case 'inactive': return { bg: 'bg-red-100', text: 'text-red-800', dot: 'bg-red-500' };
      default: return { bg: 'bg-gray-100', text: 'text-gray-800', dot: 'bg-gray-500' };
    }
  };

  const getPerformanceColor = (score) => {
    if (score >= 90) return 'text-green-600';
    if (score >= 80) return 'text-yellow-600';
    if (score >= 70) return 'text-orange-600';
    return 'text-red-600';
  };

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0
    }).format(amount);
  };

  const formatRelativeTime = (timestamp) => {
    const now = new Date();
    const diff = now - new Date(timestamp);
    const hours = Math.floor(diff / (1000 * 60 * 60));
    const days = Math.floor(hours / 24);

    if (days > 0) return `${days}d ago`;
    if (hours > 0) return `${hours}h ago`;
    return 'Just now';
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

  const DepartmentCard = ({ department }) => {
    const statusConfig = getStatusColor(department.status);
    
    return (
      <div className="bg-white rounded-lg border border-gray-200 p-6 hover:shadow-md transition-all duration-200">
        {/* Header */}
        <div className="flex items-start justify-between mb-4">
          <div>
            <div className="flex items-center space-x-2 mb-2">
              <Building2 className="w-5 h-5 text-gray-600" />
              <h3 className="font-semibold text-gray-900">{department.name}</h3>
              <span className={`px-2 py-1 text-xs font-semibold rounded-full ${statusConfig.bg} ${statusConfig.text}`}>
                {department.status.toUpperCase()}
              </span>
            </div>
            <p className="text-sm text-gray-600 mb-2">{department.description}</p>
            <div className="flex items-center space-x-2 text-sm text-gray-500">
              <Crown className="w-3 h-3" />
              <span>{department.manager}</span>
            </div>
          </div>
          
          <button className="p-1 text-gray-400 hover:text-gray-600">
            <MoreVertical className="w-4 h-4" />
          </button>
        </div>

        {/* Metrics */}
        <div className="grid grid-cols-2 gap-4 mb-4">
          <div className="text-center">
            <div className="text-2xl font-bold text-blue-600">{department.personnel}</div>
            <div className="text-xs text-gray-600">Personnel</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-green-600">{department.activeProjects}</div>
            <div className="text-xs text-gray-600">Active Projects</div>
          </div>
        </div>

        {/* KPIs */}
        <div className="space-y-2 mb-4">
          <div className="flex justify-between items-center">
            <span className="text-sm text-gray-600">Efficiency:</span>
            <span className={`font-bold ${getPerformanceColor(department.kpis.efficiency)}`}>
              {department.kpis.efficiency}%
            </span>
          </div>
          <div className="flex justify-between items-center">
            <span className="text-sm text-gray-600">Quality Score:</span>
            <span className={`font-bold ${getPerformanceColor(department.kpis.qualityScore)}`}>
              {department.kpis.qualityScore}%
            </span>
          </div>
          {department.avgSafetyScore && (
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-600">Safety Score:</span>
              <span className={`font-bold ${getPerformanceColor(department.avgSafetyScore)}`}>
                {department.avgSafetyScore}%
              </span>
            </div>
          )}
        </div>

        {/* Budget & Growth */}
        <div className="flex items-center justify-between pt-4 border-t border-gray-100">
          <div className="text-sm">
            <span className="text-gray-500">Budget: </span>
            <span className="font-medium">{formatCurrency(department.budget)}</span>
          </div>
          <div className={`flex items-center text-sm ${department.monthlyGrowth >= 0 ? 'text-green-600' : 'text-red-600'}`}>
            {department.monthlyGrowth >= 0 ? <ArrowUp className="w-3 h-3 mr-1" /> : <ArrowDown className="w-3 h-3 mr-1" />}
            <span>{Math.abs(department.monthlyGrowth).toFixed(1)}%</span>
          </div>
        </div>

        {/* Actions */}
        <div className="flex items-center justify-between pt-4 border-t border-gray-100 mt-4">
          <div className="text-xs text-gray-500">
            Updated {formatRelativeTime(department.lastActivity)}
          </div>
          <div className="flex space-x-2">
            <button
              onClick={() => navigate(`/admin/departments/${department.id}`)}
              className="p-1 hover:bg-gray-100 rounded"
              title="View Details"
            >
              <Eye className="w-4 h-4 text-blue-600" />
            </button>
            <button
              onClick={() => {
                setSelectedDepartment(department);
                setShowEditModal(true);
              }}
              className="p-1 hover:bg-gray-100 rounded"
              title="Edit Department"
            >
              <Edit3 className="w-4 h-4 text-gray-600" />
            </button>
            <button
              onClick={() => navigate(`/admin/users?department=${department.name}`)}
              className="p-1 hover:bg-gray-100 rounded"
              title="View Personnel"
            >
              <Users className="w-4 h-4 text-green-600" />
            </button>
          </div>
        </div>
      </div>
    );
  };

  const CreateDepartmentModal = () => {
    if (!showCreateModal) return null;

    return (
      <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
        <div className="bg-white rounded-lg max-w-2xl w-full max-h-[90vh] overflow-hidden">
          <div className="p-6 border-b border-gray-200">
            <h2 className="text-xl font-bold text-gray-900">Create New Department</h2>
          </div>
          
          <div className="p-6 overflow-y-auto">
            <div className="space-y-6">
              <div className="grid grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Department Name</label>
                  <input
                    type="text"
                    className="w-full px-3 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="Enter department name"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Department Manager</label>
                  <select className="w-full px-3 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
                    <option value="">Select manager...</option>
                    {mockPersonnel.map(person => (
                      <option key={person.id} value={person.id}>{person.name}</option>
                    ))}
                  </select>
                </div>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Description</label>
                <textarea
                  rows={3}
                  className="w-full px-3 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="Enter department description and responsibilities"
                />
              </div>

              <div className="grid grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Annual Budget</label>
                  <input
                    type="number"
                    className="w-full px-3 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="0"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Site Assignment</label>
                  <select className="w-full px-3 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
                    <option value="">Select primary site...</option>
                    {mockSites.map(site => (
                      <option key={site.id} value={site.name}>{site.name}</option>
                    ))}
                    <option value="All Sites">All Sites</option>
                  </select>
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
              Create Department
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
              <h1 className="text-xl font-bold text-gray-900">Department Management</h1>
              <div className="flex items-center space-x-2 text-sm text-gray-600">
                <Building2 className="w-3 h-3" />
                <span>{filteredDepartments.length} departments</span>
                <span>•</span>
                <span>{departments.reduce((sum, dept) => sum + dept.personnel, 0)} total personnel</span>
                <span>•</span>
                <span>{formatCurrency(departments.reduce((sum, dept) => sum + dept.budget, 0))} total budget</span>
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
                  <Grid className="w-4 h-4" />
                </button>
                <button
                  onClick={() => setViewMode('list')}
                  className={`px-3 py-1 text-sm rounded transition-colors ${
                    viewMode === 'list' 
                      ? 'bg-white shadow-sm text-blue-600' 
                      : 'hover:bg-gray-200'
                  }`}
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
                <span>Add Department</span>
              </button>
            </div>
          </div>
        </div>

        {/* Statistics */}
        <div className="px-6 py-4 bg-gray-50 border-b border-gray-200">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <StatCard
              title="Total Departments"
              value={departments.length}
              icon={Building2}
              color={theme.primary[500]}
            />
            <StatCard
              title="Total Personnel"
              value={departments.reduce((sum, dept) => sum + dept.personnel, 0)}
              subtitle="Across all departments"
              icon={Users}
              color={theme.success[500]}
            />
            <StatCard
              title="Active Projects"
              value={departments.reduce((sum, dept) => sum + dept.activeProjects, 0)}
              subtitle="In progress"
              icon={Target}
              color={theme.warning[500]}
            />
            <StatCard
              title="Avg Efficiency"
              value={`${Math.round(departments.reduce((sum, dept) => sum + dept.kpis.efficiency, 0) / departments.length)}%`}
              subtitle="Organization-wide"
              icon={TrendingUp}
              color={theme.secondary[500]}
              trend={{ positive: true, value: '+3.2% this month' }}
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
                  placeholder="Search departments, managers..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>
            </div>

            {/* Site Filter */}
            <select
              value={filterSite}
              onChange={(e) => setFilterSite(e.target.value)}
              className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="all">All Sites</option>
              {mockSites.map(site => (
                <option key={site.id} value={site.name}>{site.name}</option>
              ))}
              <option value="All Sites">Multi-Site Departments</option>
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
              <option value="personnel-desc">Most Personnel</option>
              <option value="budget-desc">Highest Budget</option>
              <option value="lastActivity-desc">Recently Updated</option>
            </select>
          </div>
        </div>

        {/* Department List */}
        <div className="flex-1 overflow-auto">
          {viewMode === 'grid' ? (
            <div className="p-6">
              <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
                {filteredDepartments.map((department) => (
                  <DepartmentCard key={department.id} department={department} />
                ))}
              </div>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-gray-50 border-b border-gray-200">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Department</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Manager</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Personnel</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Projects</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Efficiency</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Budget</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {filteredDepartments.map((department) => {
                    const statusConfig = getStatusColor(department.status);
                    
                    return (
                      <tr key={department.id} className="hover:bg-gray-50 border-b border-gray-100">
                        <td className="px-6 py-4">
                          <div className="flex items-center space-x-3">
                            <Building2 className="w-5 h-5 text-gray-400" />
                            <div>
                              <div className="font-medium text-gray-900">{department.name}</div>
                              <div className="text-sm text-gray-500 truncate max-w-xs">{department.description}</div>
                            </div>
                          </div>
                        </td>
                        <td className="px-6 py-4">
                          <div className="text-sm text-gray-900">{department.manager}</div>
                          <div className="text-sm text-gray-500">{department.managerEmail}</div>
                        </td>
                        <td className="px-6 py-4 text-sm text-gray-900">{department.personnel}</td>
                        <td className="px-6 py-4">
                          <div className="text-sm text-gray-900">{department.activeProjects} active</div>
                          <div className="text-sm text-gray-500">{department.completedProjects} completed</div>
                        </td>
                        <td className="px-6 py-4">
                          <span className={`font-medium ${getPerformanceColor(department.kpis.efficiency)}`}>
                            {department.kpis.efficiency}%
                          </span>
                        </td>
                        <td className="px-6 py-4 text-sm text-gray-900">{formatCurrency(department.budget)}</td>
                        <td className="px-6 py-4">
                          <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-semibold ${statusConfig.bg} ${statusConfig.text}`}>
                            <span className={`w-1.5 h-1.5 rounded-full mr-2 ${statusConfig.dot}`}></span>
                            {department.status}
                          </span>
                        </td>
                        <td className="px-6 py-4">
                          <div className="flex items-center space-x-2">
                            <button
                              onClick={() => navigate(`/admin/departments/${department.id}`)}
                              className="p-1 text-blue-600 hover:bg-blue-50 rounded transition-colors"
                              title="View Details"
                            >
                              <Eye className="w-4 h-4" />
                            </button>
                            <button
                              onClick={() => {
                                setSelectedDepartment(department);
                                setShowEditModal(true);
                              }}
                              className="p-1 text-gray-600 hover:bg-gray-50 rounded transition-colors"
                              title="Edit Department"
                            >
                              <Edit3 className="w-4 h-4" />
                            </button>
                            <button
                              onClick={() => navigate(`/admin/users?department=${department.name}`)}
                              className="p-1 text-green-600 hover:bg-green-50 rounded transition-colors"
                              title="View Personnel"
                            >
                              <Users className="w-4 h-4" />
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

          {filteredDepartments.length === 0 && (
            <div className="text-center py-12">
              <Building2 className="w-12 h-12 text-gray-400 mx-auto mb-4" />
              <h3 className="text-lg font-medium text-gray-900 mb-2">No departments found</h3>
              <p className="text-gray-600">Try adjusting your search or filter criteria.</p>
            </div>
          )}
        </div>
      </div>

      {/* Create Department Modal */}
      <CreateDepartmentModal />
    </MainLayout>
  );
};

export default DepartmentManagement;