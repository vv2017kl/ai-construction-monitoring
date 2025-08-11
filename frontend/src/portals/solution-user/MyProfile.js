import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  User, Mail, Phone, MapPin, Building2, Calendar, 
  Shield, Settings, Bell, Eye, EyeOff, Edit, Save,
  Camera, Upload, Download, Trash2, Key, Lock,
  CheckCircle, AlertTriangle, Clock, Activity,
  Smartphone, Monitor, Palette, Globe, Moon, Sun
} from 'lucide-react';
import { useTheme } from '../../context/ThemeContext';
import MainLayout from '../../components/shared/Layout/MainLayout';
import { mockUser, mockSites, mockPersonnel } from '../../data/mockData';

const MyProfile = () => {
  const navigate = useNavigate();
  const { theme } = useTheme();
  
  // State management
  const [activeTab, setActiveTab] = useState('profile'); // 'profile', 'security', 'preferences', 'activity'
  const [isEditing, setIsEditing] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  
  // Enhanced interactive features
  const [showProfilePictureModal, setShowProfilePictureModal] = useState(false);
  const [showExportModal, setShowExportModal] = useState(false);
  const [showDeleteAccountModal, setShowDeleteAccountModal] = useState(false);
  const [showChangePasswordModal, setShowChangePasswordModal] = useState(false);
  const [passwordData, setPasswordData] = useState({
    current: '',
    new: '',
    confirm: ''
  });
  const [activityFilter, setActivityFilter] = useState('all');
  const [activitySearch, setActivitySearch] = useState('');
  const [profileCompletion, setProfileCompletion] = useState(85);
  const [isSaving, setIsSaving] = useState(false);
  const [lastSaved, setLastSaved] = useState(new Date());
  const [exportFormat, setExportFormat] = useState('json');
  const [formData, setFormData] = useState({
    firstName: mockUser.firstName,
    lastName: mockUser.lastName,
    email: mockUser.email,
    phone: mockUser.phone || '+1 (555) 0100',
    department: mockUser.department,
    role: mockUser.role,
    location: mockUser.location || 'New York, NY',
    bio: 'Experienced construction management professional with focus on safety and efficiency.',
    emergencyContact: 'Jane Smith - +1 (555) 0101'
  });
  const [preferences, setPreferences] = useState({
    theme: 'light',
    language: 'en',
    timezone: 'America/New_York',
    emailNotifications: true,
    pushNotifications: true,
    smsNotifications: false,
    weeklyReports: true,
    safetyAlerts: true,
    autoSave: true,
    defaultDashboard: 'standard', // 'standard' or 'cesium'
    mapViewLevel: 'global', // 'global', 'regional', 'site'
    autoZoomToAlerts: true,
    showCameraLabels: true
  });

  const currentSite = mockSites.find(s => s.name === mockUser.currentSite) || mockSites[0];

  // Mock activity data
  const recentActivity = [
    {
      id: 1,
      type: 'login',
      description: 'Logged in from mobile device',
      timestamp: new Date(Date.now() - 15 * 60 * 1000),
      location: 'Construction Site A',
      device: 'Mobile'
    },
    {
      id: 2,
      type: 'assessment',
      description: 'Completed field assessment for Zone A',
      timestamp: new Date(Date.now() - 2 * 60 * 60 * 1000),
      location: 'Zone A - Foundation',
      device: 'Tablet'
    },
    {
      id: 3,
      type: 'report',
      description: 'Generated safety compliance report',
      timestamp: new Date(Date.now() - 4 * 60 * 60 * 1000),
      location: 'Office',
      device: 'Desktop'
    },
    {
      id: 4,
      type: 'alert',
      description: 'Acknowledged safety alert',
      timestamp: new Date(Date.now() - 6 * 60 * 60 * 1000),
      location: 'Zone B - Steel Frame',
      device: 'Mobile'
    }
  ];

  const handleInputChange = (field, value) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const handlePreferenceChange = (field, value) => {
    setPreferences(prev => ({ ...prev, [field]: value }));
  };

  const handleSave = () => {
    setIsSaving(true);
    
    // Simulate save process
    setTimeout(() => {
      setIsEditing(false);
      setIsSaving(false);
      setLastSaved(new Date());
      
      // Calculate profile completion
      const fields = [formData.firstName, formData.lastName, formData.email, formData.phone, formData.bio, formData.emergencyContact];
      const completedFields = fields.filter(field => field && field.trim()).length;
      setProfileCompletion(Math.round((completedFields / fields.length) * 100));
    }, 1500);
  };

  // Enhanced functions
  const handleProfilePictureUpload = (file) => {
    // Simulate file upload
    console.log('Uploading profile picture:', file.name);
    setShowProfilePictureModal(false);
  };

  const handlePasswordChange = () => {
    if (passwordData.new !== passwordData.confirm) {
      alert('Passwords do not match');
      return;
    }
    
    // Simulate password change
    setShowChangePasswordModal(false);
    setPasswordData({ current: '', new: '', confirm: '' });
  };

  const handleExportData = () => {
    const exportData = {
      profile: formData,
      preferences: preferences,
      activity: recentActivity,
      exportDate: new Date().toISOString()
    };

    let dataStr, fileName, mimeType;
    
    if (exportFormat === 'json') {
      dataStr = JSON.stringify(exportData, null, 2);
      fileName = `profile_data_${new Date().toISOString().split('T')[0]}.json`;
      mimeType = 'application/json';
    } else {
      // CSV format
      const csvRows = [];
      csvRows.push(['Field', 'Value']);
      Object.entries(formData).forEach(([key, value]) => {
        csvRows.push([key, value]);
      });
      
      dataStr = csvRows.map(row => row.join(',')).join('\n');
      fileName = `profile_data_${new Date().toISOString().split('T')[0]}.csv`;
      mimeType = 'text/csv';
    }

    const dataUri = `data:${mimeType};charset=utf-8,${encodeURIComponent(dataStr)}`;
    const linkElement = document.createElement('a');
    linkElement.setAttribute('href', dataUri);
    linkElement.setAttribute('download', fileName);
    linkElement.click();
    
    setShowExportModal(false);
  };

  const handleRevokeSession = (sessionId) => {
    // Simulate session revocation
    console.log('Revoking session:', sessionId);
  };

  const getPasswordStrength = (password) => {
    if (!password) return { strength: 0, label: 'None', color: 'gray' };
    
    let score = 0;
    if (password.length >= 8) score++;
    if (/[A-Z]/.test(password)) score++;
    if (/[0-9]/.test(password)) score++;
    if (/[^A-Za-z0-9]/.test(password)) score++;
    
    const strengthMap = {
      0: { strength: 0, label: 'Very Weak', color: 'red' },
      1: { strength: 25, label: 'Weak', color: 'red' },
      2: { strength: 50, label: 'Fair', color: 'yellow' },
      3: { strength: 75, label: 'Good', color: 'blue' },
      4: { strength: 100, label: 'Strong', color: 'green' }
    };
    
    return strengthMap[score];
  };

  const filteredActivity = recentActivity.filter(activity => {
    const matchesSearch = activity.description.toLowerCase().includes(activitySearch.toLowerCase()) ||
                         activity.location.toLowerCase().includes(activitySearch.toLowerCase());
    const matchesFilter = activityFilter === 'all' || activity.type === activityFilter;
    return matchesSearch && matchesFilter;
  });

  const getActivityIcon = (type) => {
    switch (type) {
      case 'login': return User;
      case 'assessment': return CheckCircle;
      case 'report': return Activity;
      case 'alert': return AlertTriangle;
      default: return Activity;
    }
  };

  const getActivityColor = (type) => {
    switch (type) {
      case 'login': return 'text-blue-600';
      case 'assessment': return 'text-green-600';
      case 'report': return 'text-purple-600';
      case 'alert': return 'text-red-600';
      default: return 'text-gray-600';
    }
  };

  const formatRelativeTime = (timestamp) => {
    const now = new Date();
    const diff = now - new Date(timestamp);
    const minutes = Math.floor(diff / (1000 * 60));
    const hours = Math.floor(minutes / 60);
    const days = Math.floor(hours / 24);

    if (minutes < 60) return `${minutes}m ago`;
    if (hours < 24) return `${hours}h ago`;
    return `${days}d ago`;
  };

  const TabButton = ({ id, label, icon: Icon }) => (
    <button
      onClick={() => setActiveTab(id)}
      className={`flex items-center space-x-2 px-4 py-2 rounded-lg transition-colors ${
        activeTab === id
          ? 'bg-blue-100 text-blue-700 border border-blue-200'
          : 'text-gray-600 hover:bg-gray-100'
      }`}
    >
      <Icon className="w-4 h-4" />
      <span>{label}</span>
    </button>
  );

  const ProfileTab = () => (
    <div className="space-y-8">
      {/* Profile Completion */}
      <div className="bg-gradient-to-r from-blue-50 to-purple-50 rounded-lg p-6 border border-blue-200">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h3 className="text-lg font-semibold text-gray-900">Profile Completion</h3>
            <p className="text-sm text-gray-600">Complete your profile to unlock all features</p>
          </div>
          <div className="text-right">
            <div className="text-2xl font-bold text-blue-600">{profileCompletion}%</div>
            <div className="text-sm text-gray-500">Complete</div>
          </div>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-2">
          <div 
            className="bg-blue-600 h-2 rounded-full transition-all duration-500"
            style={{ width: `${profileCompletion}%` }}
          ></div>
        </div>
      </div>

      {/* Profile Header */}
      <div className="bg-white rounded-lg p-6 shadow-sm border border-gray-100">
        <div className="flex items-start space-x-6">
          <div className="relative">
            <div 
              className="w-24 h-24 rounded-full flex items-center justify-center text-white text-2xl font-bold"
              style={{ backgroundColor: theme.primary[500] }}
            >
              {formData.firstName[0]}{formData.lastName[0]}
            </div>
            <button 
              onClick={() => setShowProfilePictureModal(true)}
              className="absolute bottom-0 right-0 p-2 bg-blue-600 text-white rounded-full hover:bg-blue-700 transition-colors"
            >
              <Camera className="w-4 h-4" />
            </button>
          </div>
          
          <div className="flex-1">
            <div className="flex items-center justify-between mb-4">
              <div>
                <h2 className="text-2xl font-bold text-gray-900">
                  {formData.firstName} {formData.lastName}
                </h2>
                <p className="text-gray-600">{formData.role} • {formData.department}</p>
              </div>
              <div className="flex items-center space-x-3">
                {isEditing && (
                  <div className="text-sm text-gray-500">
                    Last saved: {lastSaved.toLocaleTimeString()}
                  </div>
                )}
                <button
                  onClick={isEditing ? handleSave : () => setIsEditing(true)}
                  disabled={isSaving}
                  className="flex items-center space-x-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50"
                >
                  {isSaving ? (
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                  ) : isEditing ? (
                    <Save className="w-4 h-4" />
                  ) : (
                    <Edit className="w-4 h-4" />
                  )}
                  <span>
                    {isSaving ? 'Saving...' : isEditing ? 'Save Changes' : 'Edit Profile'}
                  </span>
                </button>
              </div>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
              <div className="flex items-center space-x-2">
                <Mail className="w-4 h-4 text-gray-400" />
                <span>{formData.email}</span>
              </div>
              <div className="flex items-center space-x-2">
                <Phone className="w-4 h-4 text-gray-400" />
                <span>{formData.phone}</span>
              </div>
              <div className="flex items-center space-x-2">
                <MapPin className="w-4 h-4 text-gray-400" />
                <span>{formData.location}</span>
              </div>
              <div className="flex items-center space-x-2">
                <Building2 className="w-4 h-4 text-gray-400" />
                <span>{currentSite.name}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Personal Information */}
      <div className="bg-white rounded-lg p-6 shadow-sm border border-gray-100">
        <h3 className="text-lg font-semibold text-gray-900 mb-6">Personal Information</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">First Name</label>
            <input
              type="text"
              value={formData.firstName}
              onChange={(e) => handleInputChange('firstName', e.target.value)}
              disabled={!isEditing}
              className="w-full px-3 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:border-transparent disabled:bg-gray-50 disabled:text-gray-500"
              style={{ '--tw-ring-color': theme.primary[500] + '40' }}
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Last Name</label>
            <input
              type="text"
              value={formData.lastName}
              onChange={(e) => handleInputChange('lastName', e.target.value)}
              disabled={!isEditing}
              className="w-full px-3 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:border-transparent disabled:bg-gray-50 disabled:text-gray-500"
              style={{ '--tw-ring-color': theme.primary[500] + '40' }}
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Email</label>
            <input
              type="email"
              value={formData.email}
              onChange={(e) => handleInputChange('email', e.target.value)}
              disabled={!isEditing}
              className="w-full px-3 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:border-transparent disabled:bg-gray-50 disabled:text-gray-500"
              style={{ '--tw-ring-color': theme.primary[500] + '40' }}
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Phone</label>
            <input
              type="tel"
              value={formData.phone}
              onChange={(e) => handleInputChange('phone', e.target.value)}
              disabled={!isEditing}
              className="w-full px-3 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:border-transparent disabled:bg-gray-50 disabled:text-gray-500"
              style={{ '--tw-ring-color': theme.primary[500] + '40' }}
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Department</label>
            <input
              type="text"
              value={formData.department}
              disabled={true}
              className="w-full px-3 py-2 border border-gray-200 rounded-lg disabled:bg-gray-50 disabled:text-gray-500"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Role</label>
            <input
              type="text"
              value={formData.role}
              disabled={true}
              className="w-full px-3 py-2 border border-gray-200 rounded-lg disabled:bg-gray-50 disabled:text-gray-500"
            />
          </div>
          <div className="md:col-span-2">
            <label className="block text-sm font-medium text-gray-700 mb-2">Emergency Contact</label>
            <input
              type="text"
              value={formData.emergencyContact}
              onChange={(e) => handleInputChange('emergencyContact', e.target.value)}
              disabled={!isEditing}
              className="w-full px-3 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:border-transparent disabled:bg-gray-50 disabled:text-gray-500"
              style={{ '--tw-ring-color': theme.primary[500] + '40' }}
            />
          </div>
          <div className="md:col-span-2">
            <label className="block text-sm font-medium text-gray-700 mb-2">Bio</label>
            <textarea
              rows={3}
              value={formData.bio}
              onChange={(e) => handleInputChange('bio', e.target.value)}
              disabled={!isEditing}
              className="w-full px-3 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:border-transparent disabled:bg-gray-50 disabled:text-gray-500"
              style={{ '--tw-ring-color': theme.primary[500] + '40' }}
            />
          </div>
        </div>
      </div>
    </div>
  );

  const SecurityTab = () => (
    <div className="space-y-6">
      {/* Password Section */}
      <div className="bg-white rounded-lg p-6 shadow-sm border border-gray-100">
        <h3 className="text-lg font-semibold text-gray-900 mb-6">Password & Security</h3>
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Current Password</label>
            <div className="relative">
              <input
                type={showPassword ? 'text' : 'password'}
                placeholder="Enter current password"
                className="w-full px-3 py-2 pr-10 border border-gray-200 rounded-lg focus:ring-2 focus:border-transparent"
                style={{ '--tw-ring-color': theme.primary[500] + '40' }}
              />
              <button
                onClick={() => setShowPassword(!showPassword)}
                className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600"
              >
                {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
              </button>
            </div>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">New Password</label>
            <input
              type="password"
              placeholder="Enter new password"
              className="w-full px-3 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:border-transparent"
              style={{ '--tw-ring-color': theme.primary[500] + '40' }}
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Confirm New Password</label>
            <input
              type="password"
              placeholder="Confirm new password"
              className="w-full px-3 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:border-transparent"
              style={{ '--tw-ring-color': theme.primary[500] + '40' }}
            />
          </div>
          <button 
            onClick={() => setShowChangePasswordModal(true)}
            className="flex items-center space-x-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            <Key className="w-4 h-4" />
            <span>Change Password</span>
          </button>
        </div>
      </div>

      {/* Two-Factor Authentication */}
      <div className="bg-white rounded-lg p-6 shadow-sm border border-gray-100">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Two-Factor Authentication</h3>
        <div className="flex items-center justify-between p-4 bg-green-50 border border-green-200 rounded-lg">
          <div className="flex items-center space-x-3">
            <Shield className="w-5 h-5 text-green-600" />
            <div>
              <p className="font-medium text-green-900">2FA Enabled</p>
              <p className="text-sm text-green-700">Your account is protected with two-factor authentication</p>
            </div>
          </div>
          <button className="px-4 py-2 bg-white border border-green-300 text-green-700 rounded-lg hover:bg-green-50 transition-colors">
            Manage
          </button>
        </div>
      </div>

      {/* Active Sessions */}
      <div className="bg-white rounded-lg p-6 shadow-sm border border-gray-100">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Active Sessions</h3>
        <div className="space-y-4">
          <div className="flex items-center justify-between p-4 border border-gray-200 rounded-lg">
            <div className="flex items-center space-x-3">
              <Monitor className="w-5 h-5 text-gray-600" />
              <div>
                <p className="font-medium">Desktop - Chrome</p>
                <p className="text-sm text-gray-600">New York, NY • Current session</p>
              </div>
            </div>
            <span className="px-2 py-1 bg-green-100 text-green-800 text-sm rounded-full">Active</span>
          </div>
          <div className="flex items-center justify-between p-4 border border-gray-200 rounded-lg">
            <div className="flex items-center space-x-3">
              <Smartphone className="w-5 h-5 text-gray-600" />
              <div>
                <p className="font-medium">Mobile - Safari</p>
                <p className="text-sm text-gray-600">Construction Site A • 2 hours ago</p>
              </div>
            </div>
            <button className="text-red-600 hover:text-red-800 text-sm">Revoke</button>
          </div>
        </div>
      </div>
    </div>
  );

  const PreferencesTab = () => (
    <div className="space-y-6">
      {/* General Preferences */}
      <div className="bg-white rounded-lg p-6 shadow-sm border border-gray-100">
        <h3 className="text-lg font-semibold text-gray-900 mb-6">General Preferences</h3>
        <div className="space-y-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <Palette className="w-5 h-5 text-gray-600" />
              <div>
                <p className="font-medium">Theme</p>
                <p className="text-sm text-gray-600">Choose your preferred theme</p>
              </div>
            </div>
            <select
              value={preferences.theme}
              onChange={(e) => handlePreferenceChange('theme', e.target.value)}
              className="px-3 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:border-transparent"
            >
              <option value="light">Light</option>
              <option value="dark">Dark</option>
              <option value="auto">Auto</option>
            </select>
          </div>

          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <Globe className="w-5 h-5 text-gray-600" />
              <div>
                <p className="font-medium">Language</p>
                <p className="text-sm text-gray-600">Select your preferred language</p>
              </div>
            </div>
            <select
              value={preferences.language}
              onChange={(e) => handlePreferenceChange('language', e.target.value)}
              className="px-3 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:border-transparent"
            >
              <option value="en">English</option>
              <option value="es">Spanish</option>
              <option value="fr">French</option>
            </select>
          </div>

          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <Clock className="w-5 h-5 text-gray-600" />
              <div>
                <p className="font-medium">Timezone</p>
                <p className="text-sm text-gray-600">Your local timezone</p>
              </div>
            </div>
            <select
              value={preferences.timezone}
              onChange={(e) => handlePreferenceChange('timezone', e.target.value)}
              className="px-3 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:border-transparent"
            >
              <option value="America/New_York">Eastern Time</option>
              <option value="America/Chicago">Central Time</option>
              <option value="America/Denver">Mountain Time</option>
              <option value="America/Los_Angeles">Pacific Time</option>
            </select>
          </div>
        </div>
      </div>

      {/* Dashboard Preferences */}
      <div className="bg-white rounded-lg p-6 shadow-sm border border-gray-100">
        <h3 className="text-lg font-semibold text-gray-900 mb-6 flex items-center">
          <Monitor className="w-5 h-5 mr-2" />
          Dashboard Preferences
        </h3>
        <div className="space-y-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <Home className="w-5 h-5 text-gray-600" />
              <div>
                <p className="font-medium">Default Dashboard</p>
                <p className="text-sm text-gray-600">Choose your preferred dashboard view on login</p>
              </div>
            </div>
            <select
              value={preferences.defaultDashboard}
              onChange={(e) => handlePreferenceChange('defaultDashboard', e.target.value)}
              className="px-3 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:border-transparent"
            >
              <option value="standard">Standard Dashboard</option>
              <option value="cesium">Cesium Map Dashboard</option>
            </select>
          </div>

          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <Globe className="w-5 h-5 text-gray-600" />
              <div>
                <p className="font-medium">Map View Level</p>
                <p className="text-sm text-gray-600">Default zoom level for map dashboard</p>
              </div>
            </div>
            <select
              value={preferences.mapViewLevel}
              onChange={(e) => handlePreferenceChange('mapViewLevel', e.target.value)}
              className="px-3 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:border-transparent"
              disabled={preferences.defaultDashboard !== 'cesium'}
            >
              <option value="global">Global View</option>
              <option value="regional">Regional View</option>
              <option value="site">Site View</option>
            </select>
          </div>

          <div className="flex items-center justify-between">
            <div>
              <p className="font-medium">Auto-zoom to Alerts</p>
              <p className="text-sm text-gray-600">Automatically zoom to locations with active alerts</p>
            </div>
            <button
              onClick={() => handlePreferenceChange('autoZoomToAlerts', !preferences.autoZoomToAlerts)}
              className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                preferences.autoZoomToAlerts ? 'bg-blue-600' : 'bg-gray-200'
              }`}
              disabled={preferences.defaultDashboard !== 'cesium'}
            >
              <span
                className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                  preferences.autoZoomToAlerts ? 'translate-x-6' : 'translate-x-1'
                }`}
              />
            </button>
          </div>

          <div className="flex items-center justify-between">
            <div>
              <p className="font-medium">Show Camera Labels</p>
              <p className="text-sm text-gray-600">Display camera names on the map</p>
            </div>
            <button
              onClick={() => handlePreferenceChange('showCameraLabels', !preferences.showCameraLabels)}
              className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                preferences.showCameraLabels ? 'bg-blue-600' : 'bg-gray-200'
              }`}
              disabled={preferences.defaultDashboard !== 'cesium'}
            >
              <span
                className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                  preferences.showCameraLabels ? 'translate-x-6' : 'translate-x-1'
                }`}
              />
            </button>
          </div>

          {preferences.defaultDashboard === 'cesium' && (
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
              <div className="flex items-start space-x-3">
                <Globe className="w-5 h-5 text-blue-600 mt-0.5" />
                <div>
                  <h4 className="text-sm font-medium text-blue-900">Cesium Map Dashboard</h4>
                  <p className="text-sm text-blue-700 mt-1">
                    Experience a powerful 3D geospatial view of your construction sites with interactive cameras, 
                    real-time alerts, and drill-down capabilities from global to site-specific views.
                  </p>
                  <button
                    onClick={() => navigate('/cesium-dashboard')}
                    className="mt-2 text-sm text-blue-600 hover:text-blue-800 font-medium"
                  >
                    Preview Cesium Dashboard →
                  </button>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Notification Preferences */}
      <div className="bg-white rounded-lg p-6 shadow-sm border border-gray-100">
        <h3 className="text-lg font-semibold text-gray-900 mb-6">Notifications</h3>
        <div className="space-y-6">
          {[
            { key: 'emailNotifications', label: 'Email Notifications', description: 'Receive notifications via email' },
            { key: 'pushNotifications', label: 'Push Notifications', description: 'Receive push notifications on your devices' },
            { key: 'smsNotifications', label: 'SMS Notifications', description: 'Receive text message notifications' },
            { key: 'weeklyReports', label: 'Weekly Reports', description: 'Receive weekly summary reports' },
            { key: 'safetyAlerts', label: 'Safety Alerts', description: 'Immediate notifications for safety issues' },
            { key: 'autoSave', label: 'Auto Save', description: 'Automatically save your work' }
          ].map((pref) => (
            <div key={pref.key} className="flex items-center justify-between">
              <div>
                <p className="font-medium">{pref.label}</p>
                <p className="text-sm text-gray-600">{pref.description}</p>
              </div>
              <button
                onClick={() => handlePreferenceChange(pref.key, !preferences[pref.key])}
                className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                  preferences[pref.key] ? 'bg-blue-600' : 'bg-gray-200'
                }`}
              >
                <span
                  className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                    preferences[pref.key] ? 'translate-x-6' : 'translate-x-1'
                  }`}
                />
              </button>
            </div>
          ))}
        </div>
      </div>
    </div>
  );

  const ActivityTab = () => (
    <div className="space-y-6">
      <div className="bg-white rounded-lg p-6 shadow-sm border border-gray-100">
        <h3 className="text-lg font-semibold text-gray-900 mb-6">Recent Activity</h3>
        <div className="space-y-4">
          {recentActivity.map((activity) => {
            const Icon = getActivityIcon(activity.type);
            return (
              <div key={activity.id} className="flex items-start space-x-4 p-4 hover:bg-gray-50 rounded-lg transition-colors">
                <div className={`p-2 rounded-full bg-gray-100 ${getActivityColor(activity.type)}`}>
                  <Icon className="w-4 h-4" />
                </div>
                <div className="flex-1">
                  <p className="font-medium text-gray-900">{activity.description}</p>
                  <div className="flex items-center space-x-4 text-sm text-gray-600 mt-1">
                    <span>{formatRelativeTime(activity.timestamp)}</span>
                    <span>•</span>
                    <span>{activity.location}</span>
                    <span>•</span>
                    <span>{activity.device}</span>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
        <div className="mt-6 text-center">
          <button className="text-blue-600 hover:text-blue-800 text-sm font-medium">
            View All Activity
          </button>
        </div>
      </div>
    </div>
  );

  const renderActiveTab = () => {
    switch (activeTab) {
      case 'security': return <SecurityTab />;
      case 'preferences': return <PreferencesTab />;
      case 'activity': return <ActivityTab />;
      default: return <ProfileTab />;
    }
  };

  return (
    <MainLayout portal="solution-user">
      <div className="h-full flex flex-col">
        {/* Header */}
        <div className="bg-white border-b border-gray-200 px-6 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-xl font-bold text-gray-900">My Profile</h1>
              <div className="flex items-center space-x-2 text-sm text-gray-600">
                <User className="w-3 h-3" />
                <span>Account Management</span>
                <span>•</span>
                <span>Last updated: {new Date().toLocaleDateString()}</span>
              </div>
            </div>

            <div className="flex items-center space-x-4">
              <button className="flex items-center space-x-2 px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors">
                <Download className="w-4 h-4" />
                <span>Export Data</span>
              </button>
            </div>
          </div>
        </div>

        {/* Tab Navigation */}
        <div className="bg-gray-50 border-b border-gray-200 px-6 py-4">
          <div className="flex space-x-2">
            <TabButton id="profile" label="Profile" icon={User} />
            <TabButton id="security" label="Security" icon={Lock} />
            <TabButton id="preferences" label="Preferences" icon={Settings} />
            <TabButton id="activity" label="Activity" icon={Activity} />
          </div>
        </div>

        {/* Tab Content */}
        <div className="flex-1 overflow-auto">
          <div className="p-6">
            {renderActiveTab()}
          </div>
        </div>
      </div>
    </MainLayout>
  );
};

export default MyProfile;