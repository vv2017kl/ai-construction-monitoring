import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  User, Camera, Save, Edit3, Mail, Phone, MapPin, Calendar,
  Shield, Key, Bell, Eye, EyeOff, Upload, Download, Trash2,
  CheckCircle, AlertCircle, Clock, Activity, Award, Settings,
  Lock, Unlock, Smartphone, Globe, Languages, Palette
} from 'lucide-react';
import { useTheme } from '../../context/ThemeContext';
import { useAuth } from '../../context/AuthContext';
import MainLayout from '../../components/shared/Layout/MainLayout';

const MyProfile = () => {
  const navigate = useNavigate();
  const { theme } = useTheme();
  const { user, updateUser } = useAuth();
  
  // Role-based feature access
  const isAdmin = user?.role === 'admin' || user?.role === 'system_administrator';
  const isManager = user?.role === 'site_manager' || user?.role === 'site_supervisor';
  const isWorker = user?.role === 'site_worker' || user?.role === 'equipment_operator';
  
  const [activeTab, setActiveTab] = useState('profile');
  const [loading, setLoading] = useState(false);
  const [saved, setSaved] = useState(false);
  const [profileData, setProfileData] = useState({
    // Basic Information
    firstName: user?.first_name || '',
    lastName: user?.last_name || '',
    email: user?.email || '',
    phone: user?.phone || '',
    avatar: user?.avatar || null,
    
    // Personal Details
    dateOfBirth: user?.date_of_birth || '',
    address: user?.address || '',
    city: user?.city || '',
    state: user?.state || '',
    zipCode: user?.zip_code || '',
    emergencyContact: user?.emergency_contact || '',
    emergencyPhone: user?.emergency_phone || '',
    
    // Professional Information
    employeeId: user?.employee_id || '',
    department: user?.department || '',
    position: user?.position || '',
    startDate: user?.start_date || '',
    supervisor: user?.supervisor || '',
    
    // Skills and Certifications (Manager/Admin)
    skills: user?.skills || [],
    certifications: user?.certifications || [],
    languages: user?.languages || ['English'],
    
    // System Preferences
    timezone: user?.timezone || 'America/New_York',
    language: user?.language || 'en',
    theme: user?.theme_preference || 'light',
    notifications: {
      email: true,
      sms: false,
      push: true,
      safety: true,
      equipment: isManager || isAdmin,
      system: isAdmin
    }
  });

  const [securityData, setSecurityData] = useState({
    currentPassword: '',
    newPassword: '',
    confirmPassword: '',
    twoFactorEnabled: user?.two_factor_enabled || false,
    sessionTimeout: user?.session_timeout || 480, // 8 hours
    loginAlerts: user?.login_alerts || true
  });

  const [sessions, setSessions] = useState([
    {
      id: 1,
      device: 'Chrome on Windows',
      location: 'New York, NY',
      lastActive: '2 minutes ago',
      current: true
    },
    {
      id: 2,
      device: 'Mobile App on iPhone',
      location: 'New York, NY', 
      lastActive: '1 hour ago',
      current: false
    }
  ]);

  // Role-based tabs
  const getTabs = () => {
    const baseTabs = [
      { id: 'profile', label: 'Profile', icon: User },
      { id: 'security', label: 'Security', icon: Shield },
      { id: 'preferences', label: 'Preferences', icon: Settings }
    ];
    
    if (isManager || isAdmin) {
      baseTabs.splice(2, 0, { id: 'professional', label: 'Professional', icon: Award });
    }
    
    if (!isWorker) {
      baseTabs.push({ id: 'activity', label: 'Activity', icon: Activity });
    }
    
    return baseTabs;
  };

  const handleProfileUpdate = (field, value) => {
    setProfileData(prev => ({
      ...prev,
      [field]: value
    }));
    setSaved(false);
  };

  const handleNestedUpdate = (parent, field, value) => {
    setProfileData(prev => ({
      ...prev,
      [parent]: {
        ...prev[parent],
        [field]: value
      }
    }));
    setSaved(false);
  };

  const handleSecurityUpdate = (field, value) => {
    setSecurityData(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const saveProfile = async () => {
    setLoading(true);
    try {
      // API call to save profile
      await new Promise(resolve => setTimeout(resolve, 1000)); // Mock API call
      setSaved(true);
      setTimeout(() => setSaved(false), 3000);
    } catch (error) {
      console.error('Failed to save profile:', error);
    } finally {
      setLoading(false);
    }
  };

  const changePassword = async () => {
    if (securityData.newPassword !== securityData.confirmPassword) {
      alert('Passwords do not match');
      return;
    }
    
    setLoading(true);
    try {
      // API call to change password
      await new Promise(resolve => setTimeout(resolve, 1000));
      setSecurityData(prev => ({
        ...prev,
        currentPassword: '',
        newPassword: '',
        confirmPassword: ''
      }));
      alert('Password updated successfully');
    } catch (error) {
      console.error('Failed to change password:', error);
    } finally {
      setLoading(false);
    }
  };

  const terminateSession = (sessionId) => {
    setSessions(prev => prev.filter(session => session.id !== sessionId));
  };

  const handleAvatarUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        handleProfileUpdate('avatar', e.target.result);
      };
      reader.readAsDataURL(file);
    }
  };

  const ProfileTab = () => (
    <div className="space-y-6">
      {/* Avatar Section */}
      <div className="flex items-center space-x-6">
        <div className="relative">
          <div className="w-24 h-24 rounded-full bg-gray-200 flex items-center justify-center overflow-hidden">
            {profileData.avatar ? (
              <img src={profileData.avatar} alt="Profile" className="w-full h-full object-cover" />
            ) : (
              <User className="w-12 h-12 text-gray-400" />
            )}
          </div>
          <label className="absolute bottom-0 right-0 bg-blue-600 text-white p-2 rounded-full cursor-pointer hover:bg-blue-700 transition-colors">
            <Camera className="w-4 h-4" />
            <input type="file" accept="image/*" onChange={handleAvatarUpload} className="hidden" />
          </label>
        </div>
        <div>
          <h3 className="text-lg font-medium">Profile Picture</h3>
          <p className="text-sm text-gray-600">Upload a clear photo of yourself</p>
          <div className="flex space-x-2 mt-2">
            <label className="text-sm text-blue-600 cursor-pointer hover:text-blue-800">
              Upload new photo
              <input type="file" accept="image/*" onChange={handleAvatarUpload} className="hidden" />
            </label>
            {profileData.avatar && (
              <button 
                onClick={() => handleProfileUpdate('avatar', null)}
                className="text-sm text-red-600 hover:text-red-800"
              >
                Remove
              </button>
            )}
          </div>
        </div>
      </div>

      {/* Basic Information */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium mb-1">First Name</label>
          <input
            type="text"
            value={profileData.firstName}
            onChange={(e) => handleProfileUpdate('firstName', e.target.value)}
            className={`w-full p-2 border rounded-md ${
              theme === 'dark' ? 'bg-gray-700 border-gray-600 text-white' : 'bg-white border-gray-300'
            }`}
          />
        </div>
        <div>
          <label className="block text-sm font-medium mb-1">Last Name</label>
          <input
            type="text"
            value={profileData.lastName}
            onChange={(e) => handleProfileUpdate('lastName', e.target.value)}
            className={`w-full p-2 border rounded-md ${
              theme === 'dark' ? 'bg-gray-700 border-gray-600 text-white' : 'bg-white border-gray-300'
            }`}
          />
        </div>
        <div>
          <label className="block text-sm font-medium mb-1">Email</label>
          <input
            type="email"
            value={profileData.email}
            onChange={(e) => handleProfileUpdate('email', e.target.value)}
            className={`w-full p-2 border rounded-md ${
              theme === 'dark' ? 'bg-gray-700 border-gray-600 text-white' : 'bg-white border-gray-300'
            }`}
          />
        </div>
        <div>
          <label className="block text-sm font-medium mb-1">Phone Number</label>
          <input
            type="tel"
            value={profileData.phone}
            onChange={(e) => handleProfileUpdate('phone', e.target.value)}
            className={`w-full p-2 border rounded-md ${
              theme === 'dark' ? 'bg-gray-700 border-gray-600 text-white' : 'bg-white border-gray-300'
            }`}
          />
        </div>
      </div>

      {/* Address Information */}
      <div className="space-y-4">
        <h4 className="font-medium">Address</h4>
        <div>
          <label className="block text-sm font-medium mb-1">Street Address</label>
          <input
            type="text"
            value={profileData.address}
            onChange={(e) => handleProfileUpdate('address', e.target.value)}
            className={`w-full p-2 border rounded-md ${
              theme === 'dark' ? 'bg-gray-700 border-gray-600 text-white' : 'bg-white border-gray-300'
            }`}
          />
        </div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label className="block text-sm font-medium mb-1">City</label>
            <input
              type="text"
              value={profileData.city}
              onChange={(e) => handleProfileUpdate('city', e.target.value)}
              className={`w-full p-2 border rounded-md ${
                theme === 'dark' ? 'bg-gray-700 border-gray-600 text-white' : 'bg-white border-gray-300'
              }`}
            />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">State</label>
            <input
              type="text"
              value={profileData.state}
              onChange={(e) => handleProfileUpdate('state', e.target.value)}
              className={`w-full p-2 border rounded-md ${
                theme === 'dark' ? 'bg-gray-700 border-gray-600 text-white' : 'bg-white border-gray-300'
              }`}
            />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Zip Code</label>
            <input
              type="text"
              value={profileData.zipCode}
              onChange={(e) => handleProfileUpdate('zipCode', e.target.value)}
              className={`w-full p-2 border rounded-md ${
                theme === 'dark' ? 'bg-gray-700 border-gray-600 text-white' : 'bg-white border-gray-300'
              }`}
            />
          </div>
        </div>
      </div>

      {/* Emergency Contact */}
      <div className="space-y-4">
        <h4 className="font-medium">Emergency Contact</h4>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium mb-1">Contact Name</label>
            <input
              type="text"
              value={profileData.emergencyContact}
              onChange={(e) => handleProfileUpdate('emergencyContact', e.target.value)}
              className={`w-full p-2 border rounded-md ${
                theme === 'dark' ? 'bg-gray-700 border-gray-600 text-white' : 'bg-white border-gray-300'
              }`}
            />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Contact Phone</label>
            <input
              type="tel"
              value={profileData.emergencyPhone}
              onChange={(e) => handleProfileUpdate('emergencyPhone', e.target.value)}
              className={`w-full p-2 border rounded-md ${
                theme === 'dark' ? 'bg-gray-700 border-gray-600 text-white' : 'bg-white border-gray-300'
              }`}
            />
          </div>
        </div>
      </div>
    </div>
  );

  const ProfessionalTab = () => (
    <div className="space-y-6">
      {/* Professional Information */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium mb-1">Employee ID</label>
          <input
            type="text"
            value={profileData.employeeId}
            disabled
            className={`w-full p-2 border rounded-md bg-gray-100 ${
              theme === 'dark' ? 'bg-gray-800 border-gray-600 text-gray-400' : 'bg-gray-100 border-gray-300 text-gray-600'
            }`}
          />
        </div>
        <div>
          <label className="block text-sm font-medium mb-1">Department</label>
          <input
            type="text"
            value={profileData.department}
            onChange={(e) => handleProfileUpdate('department', e.target.value)}
            className={`w-full p-2 border rounded-md ${
              theme === 'dark' ? 'bg-gray-700 border-gray-600 text-white' : 'bg-white border-gray-300'
            }`}
          />
        </div>
        <div>
          <label className="block text-sm font-medium mb-1">Position</label>
          <input
            type="text"
            value={profileData.position}
            onChange={(e) => handleProfileUpdate('position', e.target.value)}
            className={`w-full p-2 border rounded-md ${
              theme === 'dark' ? 'bg-gray-700 border-gray-600 text-white' : 'bg-white border-gray-300'
            }`}
          />
        </div>
        <div>
          <label className="block text-sm font-medium mb-1">Start Date</label>
          <input
            type="date"
            value={profileData.startDate}
            onChange={(e) => handleProfileUpdate('startDate', e.target.value)}
            className={`w-full p-2 border rounded-md ${
              theme === 'dark' ? 'bg-gray-700 border-gray-600 text-white' : 'bg-white border-gray-300'
            }`}
          />
        </div>
      </div>

      {/* Skills & Certifications */}
      <div className="space-y-4">
        <h4 className="font-medium">Skills & Certifications</h4>
        <div>
          <label className="block text-sm font-medium mb-1">Skills</label>
          <textarea
            value={profileData.skills.join(', ')}
            onChange={(e) => handleProfileUpdate('skills', e.target.value.split(', '))}
            placeholder="Construction Safety, Equipment Operation, Quality Control..."
            className={`w-full p-2 border rounded-md ${
              theme === 'dark' ? 'bg-gray-700 border-gray-600 text-white' : 'bg-white border-gray-300'
            }`}
            rows={3}
          />
        </div>
        <div>
          <label className="block text-sm font-medium mb-1">Certifications</label>
          <textarea
            value={profileData.certifications.join(', ')}
            onChange={(e) => handleProfileUpdate('certifications', e.target.value.split(', '))}
            placeholder="OSHA 30-Hour, First Aid/CPR, Forklift Certification..."
            className={`w-full p-2 border rounded-md ${
              theme === 'dark' ? 'bg-gray-700 border-gray-600 text-white' : 'bg-white border-gray-300'
            }`}
            rows={3}
          />
        </div>
      </div>
    </div>
  );

  const SecurityTab = () => (
    <div className="space-y-6">
      {/* Password Change */}
      <div className="space-y-4">
        <h4 className="font-medium">Change Password</h4>
        <div>
          <label className="block text-sm font-medium mb-1">Current Password</label>
          <input
            type="password"
            value={securityData.currentPassword}
            onChange={(e) => handleSecurityUpdate('currentPassword', e.target.value)}
            className={`w-full p-2 border rounded-md ${
              theme === 'dark' ? 'bg-gray-700 border-gray-600 text-white' : 'bg-white border-gray-300'
            }`}
          />
        </div>
        <div>
          <label className="block text-sm font-medium mb-1">New Password</label>
          <input
            type="password"
            value={securityData.newPassword}
            onChange={(e) => handleSecurityUpdate('newPassword', e.target.value)}
            className={`w-full p-2 border rounded-md ${
              theme === 'dark' ? 'bg-gray-700 border-gray-600 text-white' : 'bg-white border-gray-300'
            }`}
          />
        </div>
        <div>
          <label className="block text-sm font-medium mb-1">Confirm New Password</label>
          <input
            type="password"
            value={securityData.confirmPassword}
            onChange={(e) => handleSecurityUpdate('confirmPassword', e.target.value)}
            className={`w-full p-2 border rounded-md ${
              theme === 'dark' ? 'bg-gray-700 border-gray-600 text-white' : 'bg-white border-gray-300'
            }`}
          />
        </div>
        <button
          onClick={changePassword}
          className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
        >
          Update Password
        </button>
      </div>

      {/* Two-Factor Authentication */}
      <div className="border-t pt-6">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h4 className="font-medium">Two-Factor Authentication</h4>
            <p className="text-sm text-gray-600">Add an extra layer of security to your account</p>
          </div>
          <label className="relative inline-flex items-center cursor-pointer">
            <input
              type="checkbox"
              checked={securityData.twoFactorEnabled}
              onChange={(e) => handleSecurityUpdate('twoFactorEnabled', e.target.checked)}
              className="sr-only peer"
            />
            <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 dark:peer-focus:ring-blue-800 rounded-full peer dark:bg-gray-700 peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all dark:border-gray-600 peer-checked:bg-blue-600"></div>
          </label>
        </div>
      </div>

      {/* Active Sessions */}
      <div className="border-t pt-6">
        <h4 className="font-medium mb-4">Active Sessions</h4>
        <div className="space-y-3">
          {sessions.map(session => (
            <div key={session.id} className={`flex items-center justify-between p-3 border rounded-lg ${
              theme === 'dark' ? 'border-gray-600' : 'border-gray-200'
            }`}>
              <div className="flex items-center space-x-3">
                <div className={`w-2 h-2 rounded-full ${session.current ? 'bg-green-500' : 'bg-gray-400'}`}></div>
                <div>
                  <p className="font-medium">{session.device}</p>
                  <p className="text-sm text-gray-600">{session.location} • {session.lastActive}</p>
                </div>
              </div>
              {!session.current && (
                <button
                  onClick={() => terminateSession(session.id)}
                  className="text-red-600 hover:text-red-800 text-sm"
                >
                  Terminate
                </button>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  );

  const PreferencesTab = () => (
    <div className="space-y-6">
      {/* System Preferences */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium mb-1">Timezone</label>
          <select 
            value={profileData.timezone}
            onChange={(e) => handleProfileUpdate('timezone', e.target.value)}
            className={`w-full p-2 border rounded-md ${
              theme === 'dark' ? 'bg-gray-700 border-gray-600 text-white' : 'bg-white border-gray-300'
            }`}
          >
            <option value="America/New_York">Eastern Time</option>
            <option value="America/Chicago">Central Time</option>
            <option value="America/Denver">Mountain Time</option>
            <option value="America/Los_Angeles">Pacific Time</option>
          </select>
        </div>
        
        <div>
          <label className="block text-sm font-medium mb-1">Language</label>
          <select 
            value={profileData.language}
            onChange={(e) => handleProfileUpdate('language', e.target.value)}
            className={`w-full p-2 border rounded-md ${
              theme === 'dark' ? 'bg-gray-700 border-gray-600 text-white' : 'bg-white border-gray-300'
            }`}
          >
            <option value="en">English</option>
            <option value="es">Spanish</option>
            <option value="fr">French</option>
          </select>
        </div>
      </div>

      {/* Notification Preferences */}
      <div className="space-y-4">
        <h4 className="font-medium">Notification Preferences</h4>
        <div className="space-y-3">
          <div className="flex items-center justify-between">
            <div>
              <p className="font-medium">Email Notifications</p>
              <p className="text-sm text-gray-600">Receive updates via email</p>
            </div>
            <label className="relative inline-flex items-center cursor-pointer">
              <input
                type="checkbox"
                checked={profileData.notifications.email}
                onChange={(e) => handleNestedUpdate('notifications', 'email', e.target.checked)}
                className="sr-only peer"
              />
              <div className="w-11 h-6 bg-gray-200 rounded-full peer peer-checked:after:translate-x-full after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
            </label>
          </div>
          
          <div className="flex items-center justify-between">
            <div>
              <p className="font-medium">Safety Alerts</p>
              <p className="text-sm text-gray-600">Critical safety notifications</p>
            </div>
            <label className="relative inline-flex items-center cursor-pointer">
              <input
                type="checkbox"
                checked={profileData.notifications.safety}
                onChange={(e) => handleNestedUpdate('notifications', 'safety', e.target.checked)}
                className="sr-only peer"
              />
              <div className="w-11 h-6 bg-gray-200 rounded-full peer peer-checked:after:translate-x-full after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
            </label>
          </div>

          {(isManager || isAdmin) && (
            <div className="flex items-center justify-between">
              <div>
                <p className="font-medium">Equipment Alerts</p>
                <p className="text-sm text-gray-600">Equipment maintenance notifications</p>
              </div>
              <label className="relative inline-flex items-center cursor-pointer">
                <input
                  type="checkbox"
                  checked={profileData.notifications.equipment}
                  onChange={(e) => handleNestedUpdate('notifications', 'equipment', e.target.checked)}
                  className="sr-only peer"
                />
                <div className="w-11 h-6 bg-gray-200 rounded-full peer peer-checked:after:translate-x-full after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
              </label>
            </div>
          )}
        </div>
      </div>
    </div>
  );

  const ActivityTab = () => (
    <div className="space-y-6">
      <h4 className="font-medium">Recent Activity</h4>
      <div className="space-y-3">
        {[
          { action: 'Logged into system', time: '2 hours ago', icon: Lock },
          { action: 'Viewed live camera feed - Zone A', time: '3 hours ago', icon: Camera },
          { action: 'Updated profile information', time: '1 day ago', icon: Edit3 },
          { action: 'Completed safety training', time: '3 days ago', icon: CheckCircle }
        ].map((activity, index) => {
          const Icon = activity.icon;
          return (
            <div key={index} className={`flex items-center space-x-3 p-3 border rounded-lg ${
              theme === 'dark' ? 'border-gray-600' : 'border-gray-200'
            }`}>
              <Icon className="w-5 h-5 text-gray-400" />
              <div className="flex-1">
                <p className="font-medium">{activity.action}</p>
                <p className="text-sm text-gray-600">{activity.time}</p>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );

  return (
    <MainLayout>
      <div className="p-6">
        {/* Header */}
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center space-x-3">
            <User className="w-8 h-8 text-blue-600" />
            <div>
              <h1 className="text-2xl font-bold">My Profile</h1>
              <p className="text-gray-600">Manage your personal information and preferences</p>
            </div>
          </div>
          
          <button
            onClick={saveProfile}
            disabled={loading}
            className={`flex items-center space-x-2 px-4 py-2 rounded-lg transition-colors ${
              saved
                ? 'bg-green-600 text-white'
                : 'bg-blue-600 hover:bg-blue-700 text-white'
            } disabled:opacity-50`}
          >
            <Save className="w-4 h-4" />
            <span>{loading ? 'Saving...' : saved ? 'Saved!' : 'Save Changes'}</span>
          </button>
        </div>

        {/* Role-based complexity indicator */}
        {isWorker && (
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6">
            <div className="flex items-center space-x-2">
              <User className="w-5 h-5 text-blue-600" />
              <span className="text-sm text-blue-800">
                Simplified profile view - showing essential information for {user?.role?.replace('_', ' ')}
              </span>
            </div>
          </div>
        )}

        <div className="max-w-6xl mx-auto">
          {/* Tab Navigation */}
          <div className="border-b border-gray-200 dark:border-gray-700 mb-6">
            <nav className="flex space-x-8">
              {getTabs().map(tab => {
                const Icon = tab.icon;
                return (
                  <button
                    key={tab.id}
                    onClick={() => setActiveTab(tab.id)}
                    className={`flex items-center space-x-2 py-2 px-1 border-b-2 font-medium text-sm transition-colors ${
                      activeTab === tab.id
                        ? 'border-blue-500 text-blue-600'
                        : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                    }`}
                  >
                    <Icon className="w-4 h-4" />
                    <span>{tab.label}</span>
                  </button>
                );
              })}
            </nav>
          </div>

          {/* Tab Content */}
          <div className="bg-white dark:bg-gray-800 rounded-lg border p-6">
            {activeTab === 'profile' && <ProfileTab />}
            {activeTab === 'professional' && <ProfessionalTab />}
            {activeTab === 'security' && <SecurityTab />}
            {activeTab === 'preferences' && <PreferencesTab />}
            {activeTab === 'activity' && <ActivityTab />}
          </div>
        </div>
      </div>
    </MainLayout>
  );
};

export default MyProfile;