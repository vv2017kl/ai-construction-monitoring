import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  Wrench, Settings, Activity, AlertTriangle, CheckCircle, 
  XCircle, Clock, Calendar, Plus, Search, Filter, Edit3,
  Trash2, Eye, MoreVertical, Download, Upload, RefreshCw,
  Grid, List, TrendingUp, TrendingDown, MapPin, User,
  Battery, Wifi, Signal, Zap, Construction, 
  Truck, HardDrive, Monitor, Globe, Target,
  Award, BarChart3, Users, Building2, Crown
} from 'lucide-react';
import { useTheme } from '../../context/ThemeContext';
import MainLayout from '../../components/shared/Layout/MainLayout';
import { mockSites, mockPersonnel } from '../../data/mockData';

const EquipmentManagement = () => {
  const navigate = useNavigate();
  const { theme } = useTheme();
  
  // State management
  const [searchTerm, setSearchTerm] = useState('');
  const [filterStatus, setFilterStatus] = useState('all');
  const [filterType, setFilterType] = useState('all');
  const [filterSite, setFilterSite] = useState('all');
  const [sortBy, setSortBy] = useState('name');
  const [sortOrder, setSortOrder] = useState('asc');
  const [viewMode, setViewMode] = useState('grid');
  const [selectedEquipment, setSelectedEquipment] = useState(null);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [showMaintenanceModal, setShowMaintenanceModal] = useState(false);

  // Mock equipment data
  const mockEquipment = [
    {
      id: 'eq-001',
      name: 'Tower Crane TC-1',
      type: 'crane',
      category: 'Heavy Machinery',
      model: 'Liebherr 280 EC-H',
      serialNumber: 'LH-280-2024-001',
      status: 'operational',
      site: 'Downtown Construction Site',
      siteId: 'site-001',
      operator: 'Mike Rodriguez',
      operatorId: 'p003',
      location: 'Zone A - Central',
      batteryLevel: 85,
      signalStrength: 92,
      lastMaintenance: new Date('2024-11-15'),
      nextMaintenance: new Date('2025-01-15'),
      hoursUsed: 1247,
      maxHours: 8000,
      purchaseDate: new Date('2024-01-20'),
      warrantyExpiry: new Date('2026-01-20'),
      maintenanceCost: 15600,
      utilizationRate: 78,
      efficiency: 94,
      alerts: 0,
      specifications: {
        capacity: '8 tons',
        reach: '60 meters',
        height: '150 meters',
        power: '400V 3-phase'
      }
    },
    {
      id: 'eq-002',
      name: 'Excavator EX-450',
      type: 'excavator',
      category: 'Heavy Machinery',
      model: 'Caterpillar 345 GC',
      serialNumber: 'CAT-345-2024-002',
      status: 'maintenance',
      site: 'Industrial Complex Alpha',
      siteId: 'site-003',
      operator: 'David Park',
      operatorId: 'p005',
      location: 'Equipment Bay',
      batteryLevel: 45,
      signalStrength: 88,
      lastMaintenance: new Date('2024-12-01'),
      nextMaintenance: new Date('2024-12-15'),
      hoursUsed: 2890,
      maxHours: 10000,
      purchaseDate: new Date('2023-08-10'),
      warrantyExpiry: new Date('2025-08-10'),
      maintenanceCost: 22400,
      utilizationRate: 85,
      efficiency: 89,
      alerts: 2,
      specifications: {
        capacity: '45 tons',
        bucketCapacity: '2.2 m³',
        engine: '345 HP',
        fuel: 'Diesel'
      }
    },
    {
      id: 'eq-003',
      name: 'Concrete Mixer CM-12',
      type: 'mixer',
      category: 'Concrete Equipment',
      model: 'Volvo FM 460 8x4',
      serialNumber: 'VO-FM460-2024-003',
      status: 'operational',
      site: 'Riverside Apartments',
      siteId: 'site-002',
      operator: 'Emma Thompson',
      operatorId: 'p004',
      location: 'Loading Zone B',
      batteryLevel: 92,
      signalStrength: 95,
      lastMaintenance: new Date('2024-10-20'),
      nextMaintenance: new Date('2025-01-20'),
      hoursUsed: 856,
      maxHours: 12000,
      purchaseDate: new Date('2024-03-15'),
      warrantyExpiry: new Date('2027-03-15'),
      maintenanceCost: 8900,
      utilizationRate: 72,
      efficiency: 96,
      alerts: 0,
      specifications: {
        capacity: '12 m³',
        drumSpeed: '0-14 rpm',
        discharge: 'Hydraulic',
        chassis: '8x4 configuration'
      }
    },
    {
      id: 'eq-004',
      name: 'Bulldozer BD-750',
      type: 'bulldozer',
      category: 'Earthmoving',
      model: 'Komatsu D65PX-18',
      serialNumber: 'KM-D65-2024-004',
      status: 'offline',
      site: 'Downtown Construction Site',
      siteId: 'site-001',
      operator: null,
      operatorId: null,
      location: 'Storage Yard',
      batteryLevel: 12,
      signalStrength: 15,
      lastMaintenance: new Date('2024-09-10'),
      nextMaintenance: new Date('2024-12-10'),
      hoursUsed: 3456,
      maxHours: 15000,
      purchaseDate: new Date('2023-05-20'),
      warrantyExpiry: new Date('2025-05-20'),
      maintenanceCost: 31200,
      utilizationRate: 45,
      efficiency: 67,
      alerts: 4,
      specifications: {
        capacity: '750 HP',
        bladeWidth: '4.2 meters',
        weight: '20.5 tons',
        engine: 'Komatsu SAA6D125E'
      }
    },
    {
      id: 'eq-005',
      name: 'Generator GEN-500',
      type: 'generator',
      category: 'Power Equipment',
      model: 'Caterpillar C18 ACERT',
      serialNumber: 'CAT-C18-2024-005',
      status: 'operational',
      site: 'Harbor Bridge Extension',
      siteId: 'site-004',
      operator: 'John Mitchell',
      operatorId: 'p001',
      location: 'Power Station',
      batteryLevel: null, // Generator doesn't have battery
      signalStrength: 89,
      lastMaintenance: new Date('2024-11-30'),
      nextMaintenance: new Date('2025-02-28'),
      hoursUsed: 1890,
      maxHours: 20000,
      purchaseDate: new Date('2024-02-10'),
      warrantyExpiry: new Date('2029-02-10'),
      maintenanceCost: 12800,
      utilizationRate: 92,
      efficiency: 98,
      alerts: 0,
      specifications: {
        output: '500 kVA',
        voltage: '480V',
        frequency: '60 Hz',
        fuel: 'Diesel'
      }
    },
    {
      id: 'eq-006',
      name: 'Safety Monitor SM-01',
      type: 'monitor',
      category: 'Safety Equipment',
      model: 'ConstructionAI SafeWatch Pro',
      serialNumber: 'CAI-SW-2024-006',
      status: 'operational',
      site: 'Riverside Apartments',
      siteId: 'site-002',
      operator: 'Sarah Chen',
      operatorId: 'p002',
      location: 'Zone C - Safety Station',
      batteryLevel: 78,
      signalStrength: 98,
      lastMaintenance: new Date('2024-12-05'),
      nextMaintenance: new Date('2025-03-05'),
      hoursUsed: 4320, // Always on
      maxHours: 50000,
      purchaseDate: new Date('2024-04-01'),
      warrantyExpiry: new Date('2026-04-01'),
      maintenanceCost: 3200,
      utilizationRate: 99,
      efficiency: 99,
      alerts: 0,
      specifications: {
        cameras: '4K Resolution',
        aiProcessing: 'Edge Computing',
        storage: '2TB SSD',
        connectivity: '5G/WiFi'
      }
    }
  ];

  const [equipment, setEquipment] = useState(mockEquipment);

  // Filter and sort equipment
  const filteredEquipment = equipment
    .filter(item => {
      const matchesSearch = item.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                           item.model.toLowerCase().includes(searchTerm.toLowerCase()) ||
                           item.serialNumber.toLowerCase().includes(searchTerm.toLowerCase());
      const matchesStatus = filterStatus === 'all' || item.status === filterStatus;
      const matchesType = filterType === 'all' || item.type === filterType;
      const matchesSite = filterSite === 'all' || item.siteId === filterSite;
      
      return matchesSearch && matchesStatus && matchesType && matchesSite;
    })
    .sort((a, b) => {
      let aVal = a[sortBy];
      let bVal = b[sortBy];
      
      if (sortBy === 'lastMaintenance' || sortBy === 'nextMaintenance') {
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
      case 'operational': return { bg: 'bg-green-100', text: 'text-green-800', dot: 'bg-green-500', icon: CheckCircle };
      case 'maintenance': return { bg: 'bg-yellow-100', text: 'text-yellow-800', dot: 'bg-yellow-500', icon: Wrench };
      case 'offline': return { bg: 'bg-red-100', text: 'text-red-800', dot: 'bg-red-500', icon: XCircle };
      case 'idle': return { bg: 'bg-gray-100', text: 'text-gray-800', dot: 'bg-gray-500', icon: Clock };
      default: return { bg: 'bg-gray-100', text: 'text-gray-800', dot: 'bg-gray-500', icon: Activity };
    }
  };

  const getEquipmentIcon = (type) => {
    switch (type) {
      case 'crane': return Construction;
      case 'excavator': return Construction;
      case 'mixer': return Truck;
      case 'bulldozer': return Construction;
      case 'generator': return Zap;
      case 'monitor': return Monitor;
      default: return Wrench;
    }
  };

  const getUtilizationColor = (rate) => {
    if (rate >= 90) return 'text-green-600';
    if (rate >= 70) return 'text-yellow-600';
    if (rate >= 50) return 'text-orange-600';
    return 'text-red-600';
  };

  const getBatteryColor = (level) => {
    if (level === null) return 'text-gray-400';
    if (level >= 70) return 'text-green-600';
    if (level >= 30) return 'text-yellow-600';
    return 'text-red-600';
  };

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0
    }).format(amount);
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

  const EquipmentCard = ({ item }) => {
    const statusConfig = getStatusColor(item.status);
    const EquipmentIcon = getEquipmentIcon(item.type);
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
              <EquipmentIcon className="w-5 h-5" style={{ color: theme.primary[500] }} />
            </div>
            <div>
              <h3 className="font-semibold text-gray-900 mb-1">{item.name}</h3>
              <p className="text-sm text-gray-600 mb-1">{item.model}</p>
              <p className="text-xs text-gray-500">{item.category}</p>
            </div>
          </div>
          
          <div className="flex items-center space-x-2">
            <span className={`px-2 py-1 text-xs font-semibold rounded-full ${statusConfig.bg} ${statusConfig.text}`}>
              {item.status.toUpperCase()}
            </span>
            <button className="p-1 text-gray-400 hover:text-gray-600">
              <MoreVertical className="w-4 h-4" />
            </button>
          </div>
        </div>

        {/* Metrics */}
        <div className="grid grid-cols-2 gap-4 mb-4">
          <div className="text-center">
            <div className={`text-lg font-bold ${getUtilizationColor(item.utilizationRate)}`}>
              {item.utilizationRate}%
            </div>
            <div className="text-xs text-gray-600">Utilization</div>
          </div>
          <div className="text-center">
            <div className="text-lg font-bold text-green-600">{item.efficiency}%</div>
            <div className="text-xs text-gray-600">Efficiency</div>
          </div>
        </div>

        {/* Status Indicators */}
        <div className="space-y-2 mb-4">
          <div className="flex justify-between items-center">
            <span className="text-sm text-gray-600">Location:</span>
            <span className="text-sm font-medium">{item.location}</span>
          </div>
          <div className="flex justify-between items-center">
            <span className="text-sm text-gray-600">Site:</span>
            <span className="text-sm font-medium">{item.site}</span>
          </div>
          {item.batteryLevel !== null && (
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-600">Battery:</span>
              <div className="flex items-center space-x-2">
                <Battery className={`w-3 h-3 ${getBatteryColor(item.batteryLevel)}`} />
                <span className={`text-sm font-medium ${getBatteryColor(item.batteryLevel)}`}>
                  {item.batteryLevel}%
                </span>
              </div>
            </div>
          )}
          <div className="flex justify-between items-center">
            <span className="text-sm text-gray-600">Signal:</span>
            <div className="flex items-center space-x-2">
              <Signal className="w-3 h-3 text-blue-600" />
              <span className="text-sm font-medium text-blue-600">{item.signalStrength}%</span>
            </div>
          </div>
        </div>

        {/* Usage Progress */}
        <div className="mb-4">
          <div className="flex justify-between items-center mb-2">
            <span className="text-sm text-gray-600">Usage:</span>
            <span className="text-sm font-medium">{item.hoursUsed.toLocaleString()} / {item.maxHours.toLocaleString()}h</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div 
              className="bg-blue-600 h-2 rounded-full" 
              style={{ width: `${(item.hoursUsed / item.maxHours) * 100}%` }}
            ></div>
          </div>
        </div>

        {/* Alerts & Operator */}
        <div className="flex items-center justify-between pt-4 border-t border-gray-100">
          <div className="flex items-center space-x-4 text-sm">
            {item.alerts > 0 ? (
              <div className="flex items-center space-x-1 text-red-600">
                <AlertTriangle className="w-3 h-3" />
                <span>{item.alerts} alerts</span>
              </div>
            ) : (
              <div className="flex items-center space-x-1 text-green-600">
                <CheckCircle className="w-3 h-3" />
                <span>No issues</span>
              </div>
            )}
            {item.operator && (
              <div className="flex items-center space-x-1 text-gray-600">
                <User className="w-3 h-3" />
                <span className="text-xs">{item.operator}</span>
              </div>
            )}
          </div>
          
          <div className="flex space-x-2">
            <button
              onClick={() => navigate(`/admin/equipment/${item.id}`)}
              className="p-1 hover:bg-gray-100 rounded"
              title="View Details"
            >
              <Eye className="w-4 h-4 text-blue-600" />
            </button>
            <button
              onClick={() => {
                setSelectedEquipment(item);
                setShowMaintenanceModal(true);
              }}
              className="p-1 hover:bg-gray-100 rounded"
              title="Schedule Maintenance"
            >
              <Wrench className="w-4 h-4 text-orange-600" />
            </button>
            <button
              className="p-1 hover:bg-gray-100 rounded"
              title="Edit Equipment"
            >
              <Edit3 className="w-4 h-4 text-gray-600" />
            </button>
          </div>
        </div>
      </div>
    );
  };

  const CreateEquipmentModal = () => {
    if (!showCreateModal) return null;

    return (
      <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
        <div className="bg-white rounded-lg max-w-3xl w-full max-h-[90vh] overflow-hidden">
          <div className="p-6 border-b border-gray-200">
            <h2 className="text-xl font-bold text-gray-900">Add New Equipment</h2>
          </div>
          
          <div className="p-6 overflow-y-auto max-h-[70vh]">
            <div className="space-y-6">
              <div className="grid grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Equipment Name</label>
                  <input
                    type="text"
                    className="w-full px-3 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="Enter equipment name"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Equipment Type</label>
                  <select className="w-full px-3 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
                    <option value="">Select type...</option>
                    <option value="crane">Crane</option>
                    <option value="excavator">Excavator</option>
                    <option value="mixer">Concrete Mixer</option>
                    <option value="bulldozer">Bulldozer</option>
                    <option value="generator">Generator</option>
                    <option value="monitor">Safety Monitor</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Model</label>
                  <input
                    type="text"
                    className="w-full px-3 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="Equipment model"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Serial Number</label>
                  <input
                    type="text"
                    className="w-full px-3 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="Serial number"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Assigned Site</label>
                  <select className="w-full px-3 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
                    <option value="">Select site...</option>
                    {mockSites.map(site => (
                      <option key={site.id} value={site.id}>{site.name}</option>
                    ))}
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Operator</label>
                  <select className="w-full px-3 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
                    <option value="">Select operator...</option>
                    {mockPersonnel.map(person => (
                      <option key={person.id} value={person.id}>{person.name}</option>
                    ))}
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
              Add Equipment
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
              <h1 className="text-xl font-bold text-gray-900">Equipment Management</h1>
              <div className="flex items-center space-x-2 text-sm text-gray-600">
                <Wrench className="w-3 h-3" />
                <span>{filteredEquipment.length} equipment</span>
                <span>•</span>
                <span>{equipment.filter(e => e.status === 'operational').length} operational</span>
                <span>•</span>
                <span>{equipment.reduce((sum, e) => sum + e.maintenanceCost, 0).toLocaleString()} total maintenance cost</span>
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
                <span>Add Equipment</span>
              </button>
            </div>
          </div>
        </div>

        {/* Statistics */}
        <div className="px-6 py-4 bg-gray-50 border-b border-gray-200">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <StatCard
              title="Total Equipment"
              value={equipment.length}
              icon={Wrench}
              color={theme.primary[500]}
            />
            <StatCard
              title="Operational"
              value={equipment.filter(e => e.status === 'operational').length}
              subtitle="Currently active"
              icon={CheckCircle}
              color={theme.success[500]}
            />
            <StatCard
              title="In Maintenance"
              value={equipment.filter(e => e.status === 'maintenance').length}
              subtitle="Scheduled/ongoing"
              icon={Settings}
              color={theme.warning[500]}
            />
            <StatCard
              title="Avg Utilization"
              value={`${Math.round(equipment.reduce((sum, e) => sum + e.utilizationRate, 0) / equipment.length)}%`}
              subtitle="Fleet-wide efficiency"
              icon={BarChart3}
              color={theme.secondary[500]}
              trend={{ positive: true, value: '+4.2% this month' }}
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
                  placeholder="Search equipment, models, serial numbers..."
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
              <option value="operational">Operational</option>
              <option value="maintenance">Maintenance</option>
              <option value="offline">Offline</option>
              <option value="idle">Idle</option>
            </select>

            {/* Type Filter */}
            <select
              value={filterType}
              onChange={(e) => setFilterType(e.target.value)}
              className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="all">All Types</option>
              <option value="crane">Cranes</option>
              <option value="excavator">Excavators</option>
              <option value="mixer">Concrete Mixers</option>
              <option value="bulldozer">Bulldozers</option>
              <option value="generator">Generators</option>
              <option value="monitor">Safety Monitors</option>
            </select>

            {/* Site Filter */}
            <select
              value={filterSite}
              onChange={(e) => setFilterSite(e.target.value)}
              className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="all">All Sites</option>
              {mockSites.map(site => (
                <option key={site.id} value={site.id}>{site.name}</option>
              ))}
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
              <option value="utilizationRate-desc">Highest Utilization</option>
              <option value="efficiency-desc">Most Efficient</option>
              <option value="nextMaintenance-asc">Maintenance Due</option>
            </select>
          </div>
        </div>

        {/* Equipment List */}
        <div className="flex-1 overflow-auto">
          {viewMode === 'grid' ? (
            <div className="p-6">
              <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
                {filteredEquipment.map((item) => (
                  <EquipmentCard key={item.id} item={item} />
                ))}
              </div>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-gray-50 border-b border-gray-200">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Equipment</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Site</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Operator</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Utilization</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Next Maintenance</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {filteredEquipment.map((item) => {
                    const statusConfig = getStatusColor(item.status);
                    const EquipmentIcon = getEquipmentIcon(item.type);
                    
                    return (
                      <tr key={item.id} className="hover:bg-gray-50">
                        <td className="px-6 py-4">
                          <div className="flex items-center space-x-3">
                            <EquipmentIcon className="w-5 h-5 text-gray-400" />
                            <div>
                              <div className="font-medium text-gray-900">{item.name}</div>
                              <div className="text-sm text-gray-500">{item.model}</div>
                            </div>
                          </div>
                        </td>
                        <td className="px-6 py-4 text-sm text-gray-900">{item.site}</td>
                        <td className="px-6 py-4 text-sm text-gray-900">{item.operator || 'Unassigned'}</td>
                        <td className="px-6 py-4">
                          <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-semibold ${statusConfig.bg} ${statusConfig.text}`}>
                            <span className={`w-1.5 h-1.5 rounded-full mr-2 ${statusConfig.dot}`}></span>
                            {item.status}
                          </span>
                        </td>
                        <td className="px-6 py-4">
                          <span className={`font-medium ${getUtilizationColor(item.utilizationRate)}`}>
                            {item.utilizationRate}%
                          </span>
                        </td>
                        <td className="px-6 py-4 text-sm text-gray-900">
                          {new Date(item.nextMaintenance).toLocaleDateString()}
                        </td>
                        <td className="px-6 py-4">
                          <div className="flex items-center space-x-2">
                            <button
                              className="p-1 text-blue-600 hover:bg-blue-50 rounded transition-colors"
                              title="View Details"
                            >
                              <Eye className="w-4 h-4" />
                            </button>
                            <button
                              className="p-1 text-orange-600 hover:bg-orange-50 rounded transition-colors"
                              title="Schedule Maintenance"
                            >
                              <Wrench className="w-4 h-4" />
                            </button>
                            <button
                              className="p-1 text-gray-600 hover:bg-gray-50 rounded transition-colors"
                              title="Edit Equipment"
                            >
                              <Edit3 className="w-4 h-4" />
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

          {filteredEquipment.length === 0 && (
            <div className="text-center py-12">
              <Wrench className="w-12 h-12 text-gray-400 mx-auto mb-4" />
              <h3 className="text-lg font-medium text-gray-900 mb-2">No equipment found</h3>
              <p className="text-gray-600">Try adjusting your search or filter criteria.</p>
            </div>
          )}
        </div>
      </div>

      {/* Create Equipment Modal */}
      <CreateEquipmentModal />
    </MainLayout>
  );
};

export default EquipmentManagement;