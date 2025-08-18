import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  Settings as SettingsIcon, User, Bell, Shield, Palette, Globe, Clock, 
  Save, RefreshCw, Download, Upload, ChevronRight, ChevronDown,
  Moon, Sun, Monitor, Volume2, VolumeX, Eye, EyeOff, Key,
  MapPin, Calendar, Languages, Smartphone, Mail, MessageSquare
} from 'lucide-react';
import { useTheme } from '../../context/ThemeContext';
import { useAuth } from '../../context/AuthContext';
import MainLayout from '../../components/shared/Layout/MainLayout';

const Settings = () => {
  const navigate = useNavigate();
  const { theme } = useTheme();
  const { user } = useAuth();
  
  // Role-based complexity management
  const isAdmin = user?.role === 'admin' || user?.role === 'system_administrator';
  const isManager = user?.role === 'site_manager' || user?.role === 'site_supervisor';
  const isWorker = user?.role === 'site_worker' || user?.role === 'equipment_operator';
  
  // Progressive disclosure state
  const [expandedSections, setExpandedSections] = useState({
    general: true,
    notifications: false,
    appearance: false,
    privacy: false,
    advanced: false
  });
  
  const [showAdvanced, setShowAdvanced] = useState(!isWorker);
  
  // Settings state
  const [settings, setSettings] = useState({
    // General settings
    language: 'en',
    timezone: 'America/New_York',
    dateFormat: 'MM/DD/YYYY',
    timeFormat: '12h',
    measurementUnit: 'imperial',
    
    // Appearance settings
    theme: 'light',
    fontSize: 'medium',
    colorScheme: 'blue',
    compactMode: false,
    
    // Notification settings
    emailNotifications: true,
    smsNotifications: false,
    pushNotifications: true,
    soundEnabled: true,
    quietHoursEnabled: false,
    quietHoursStart: '22:00',
    quietHoursEnd: '07:00',
    
    // Alert preferences (role-based)
    criticalAlerts: true,
    safetyAlerts: true,
    equipmentAlerts: isManager || isAdmin,
    systemAlerts: isAdmin,
    
    // Privacy settings
    dataSharing: true,
    analyticsEnabled: true,
    locationTracking: false,
    
    // Advanced settings (admin only)
    debugMode: false,
    betaFeatures: false,
    apiAccess: false
  });
  
  const [loading, setLoading] = useState(false);
  const [saved, setSaved] = useState(false);

  // Role-based setting categories
  const getVisibleSettings = () => {
    const base = ['general', 'appearance', 'notifications'];
    
    if (isManager || isAdmin) {
      base.push('privacy');
    }
    
    if (isAdmin) {
      base.push('advanced');
    }
    
    return base;
  };

  const toggleSection = (section) => {
    setExpandedSections(prev => ({
      ...prev,
      [section]: !prev[section]
    }));
  };

  const handleSettingChange = (category, setting, value) => {
    setSettings(prev => ({
      ...prev,
      [setting]: value
    }));
    setSaved(false);
  };

  const saveSettings = async () => {
    setLoading(true);
    try {
      // API call to save settings
      await new Promise(resolve => setTimeout(resolve, 1000)); // Mock API call
      setSaved(true);
      setTimeout(() => setSaved(false), 3000);
    } catch (error) {
      console.error('Failed to save settings:', error);
    } finally {
      setLoading(false);
    }
  };

  const resetSettings = () => {
    if (window.confirm('Reset all settings to default values?')) {
      setSettings({
        ...settings,
        language: 'en',
        timezone: 'America/New_York',
        theme: 'light',
        fontSize: 'medium'
      });
    }
  };

  const exportSettings = () => {
    const dataStr = JSON.stringify(settings, null, 2);
    const dataUri = 'data:application/json;charset=utf-8,'+ encodeURIComponent(dataStr);
    
    const exportFileDefaultName = 'construction-ai-settings.json';
    
    const linkElement = document.createElement('a');
    linkElement.setAttribute('href', dataUri);
    linkElement.setAttribute('download', exportFileDefaultName);
    linkElement.click();
  };

  // Role-based UI components
  const SettingSection = ({ id, title, icon: Icon, children, adminOnly = false, managerOnly = false }) => {
    if (adminOnly && !isAdmin) return null;
    if (managerOnly && !isManager && !isAdmin) return null;
    
    const isExpanded = expandedSections[id];
    
    return (
      <div className={`border rounded-lg ${theme === 'dark' ? 'border-gray-600' : 'border-gray-200'} mb-4`}>
        <div 
          className={`p-4 cursor-pointer flex items-center justify-between ${
            theme === 'dark' ? 'hover:bg-gray-700' : 'hover:bg-gray-50'
          }`}
          onClick={() => toggleSection(id)}
        >
          <div className="flex items-center space-x-3">
            <Icon className="w-5 h-5 text-blue-600" />
            <h3 className="text-lg font-medium">{title}</h3>
          </div>
          {isExpanded ? <ChevronDown className="w-5 h-5" /> : <ChevronRight className="w-5 h-5" />}
        </div>
        
        {isExpanded && (
          <div className={`border-t p-4 space-y-4 ${theme === 'dark' ? 'border-gray-600' : 'border-gray-200'}`}>
            {children}
          </div>
        )}
      </div>
    );
  };

  const ToggleSwitch = ({ label, description, checked, onChange, disabled = false }) => (
    <div className="flex items-center justify-between py-2">
      <div className="flex-1">
        <label className="text-sm font-medium">{label}</label>
        {description && <p className="text-xs text-gray-500 mt-1">{description}</p>}
      </div>
      <label className="relative inline-flex items-center cursor-pointer">
        <input
          type="checkbox"
          checked={checked}
          onChange={(e) => onChange(e.target.checked)}
          disabled={disabled}
          className="sr-only peer"
        />
        <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 dark:peer-focus:ring-blue-800 rounded-full peer dark:bg-gray-700 peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all dark:border-gray-600 peer-checked:bg-blue-600"></div>
      </label>
    </div>
  );

  const SelectInput = ({ label, value, options, onChange }) => (
    <div className="space-y-1">
      <label className="text-sm font-medium">{label}</label>
      <select 
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className={`w-full p-2 border rounded-md ${
          theme === 'dark' 
            ? 'bg-gray-700 border-gray-600 text-white' 
            : 'bg-white border-gray-300'
        }`}
      >
        {options.map(option => (
          <option key={option.value} value={option.value}>
            {option.label}
          </option>
        ))}
      </select>
    </div>
  );

  return (
    <MainLayout>
      <div className="p-6">
        {/* Header */}
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center space-x-3">
            <SettingsIcon className="w-8 h-8 text-blue-600" />
            <div>
              <h1 className="text-2xl font-bold">Settings</h1>
              <p className="text-gray-600">Customize your experience</p>
            </div>
          </div>
          
          <div className="flex items-center space-x-2">
            {!isWorker && (
              <>
                <button
                  onClick={exportSettings}
                  className="flex items-center space-x-1 px-3 py-2 text-gray-600 hover:text-gray-800 transition-colors"
                >
                  <Download className="w-4 h-4" />
                  <span className="text-sm">Export</span>
                </button>
                <button
                  onClick={resetSettings}
                  className="flex items-center space-x-1 px-3 py-2 text-gray-600 hover:text-gray-800 transition-colors"
                >
                  <RefreshCw className="w-4 h-4" />
                  <span className="text-sm">Reset</span>
                </button>
              </>
            )}
            <button
              onClick={saveSettings}
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
        </div>

        {/* Role-based complexity indicator */}
        {isWorker && (
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6">
            <div className="flex items-center space-x-2">
              <User className="w-5 h-5 text-blue-600" />
              <span className="text-sm text-blue-800">
                Simplified view for {user?.role?.replace('_', ' ')} - showing essential settings only
              </span>
            </div>
          </div>
        )}

        <div className="max-w-4xl mx-auto">
          {/* General Settings */}
          <SettingSection id="general" title="General" icon={Globe}>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <SelectInput
                label="Language"
                value={settings.language}
                onChange={(value) => handleSettingChange('general', 'language', value)}
                options={[
                  { value: 'en', label: 'English' },
                  { value: 'es', label: 'Spanish' },
                  { value: 'fr', label: 'French' }
                ]}
              />
              
              <SelectInput
                label="Timezone"
                value={settings.timezone}
                onChange={(value) => handleSettingChange('general', 'timezone', value)}
                options={[
                  { value: 'America/New_York', label: 'Eastern Time' },
                  { value: 'America/Chicago', label: 'Central Time' },
                  { value: 'America/Denver', label: 'Mountain Time' },
                  { value: 'America/Los_Angeles', label: 'Pacific Time' }
                ]}
              />
              
              <SelectInput
                label="Date Format"
                value={settings.dateFormat}
                onChange={(value) => handleSettingChange('general', 'dateFormat', value)}
                options={[
                  { value: 'MM/DD/YYYY', label: 'MM/DD/YYYY' },
                  { value: 'DD/MM/YYYY', label: 'DD/MM/YYYY' },
                  { value: 'YYYY-MM-DD', label: 'YYYY-MM-DD' }
                ]}
              />
              
              <SelectInput
                label="Time Format"
                value={settings.timeFormat}
                onChange={(value) => handleSettingChange('general', 'timeFormat', value)}
                options={[
                  { value: '12h', label: '12 Hour' },
                  { value: '24h', label: '24 Hour' }
                ]}
              />
            </div>
          </SettingSection>

          {/* Appearance Settings */}
          <SettingSection id="appearance" title="Appearance" icon={Palette}>
            <div className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <SelectInput
                  label="Theme"
                  value={settings.theme}
                  onChange={(value) => handleSettingChange('appearance', 'theme', value)}
                  options={[
                    { value: 'light', label: 'Light' },
                    { value: 'dark', label: 'Dark' },
                    { value: 'auto', label: 'Auto (System)' }
                  ]}
                />
                
                <SelectInput
                  label="Font Size"
                  value={settings.fontSize}
                  onChange={(value) => handleSettingChange('appearance', 'fontSize', value)}
                  options={[
                    { value: 'small', label: 'Small' },
                    { value: 'medium', label: 'Medium' },
                    { value: 'large', label: 'Large' }
                  ]}
                />
              </div>
              
              <ToggleSwitch
                label="Compact Mode"
                description="Reduce spacing and show more information on screen"
                checked={settings.compactMode}
                onChange={(value) => handleSettingChange('appearance', 'compactMode', value)}
              />
            </div>
          </SettingSection>

          {/* Notifications Settings */}
          <SettingSection id="notifications" title="Notifications" icon={Bell}>
            <div className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <h4 className="font-medium mb-3">Delivery Methods</h4>
                  <div className="space-y-2">
                    <ToggleSwitch
                      label="Email Notifications"
                      checked={settings.emailNotifications}
                      onChange={(value) => handleSettingChange('notifications', 'emailNotifications', value)}
                    />
                    <ToggleSwitch
                      label="Push Notifications"
                      checked={settings.pushNotifications}
                      onChange={(value) => handleSettingChange('notifications', 'pushNotifications', value)}
                    />
                    {(isManager || isAdmin) && (
                      <ToggleSwitch
                        label="SMS Notifications"
                        checked={settings.smsNotifications}
                        onChange={(value) => handleSettingChange('notifications', 'smsNotifications', value)}
                      />
                    )}
                  </div>
                </div>
                
                <div>
                  <h4 className="font-medium mb-3">Alert Types</h4>
                  <div className="space-y-2">
                    <ToggleSwitch
                      label="Critical Safety Alerts"
                      description="Emergency situations and safety violations"
                      checked={settings.criticalAlerts}
                      onChange={(value) => handleSettingChange('notifications', 'criticalAlerts', value)}
                    />
                    <ToggleSwitch
                      label="General Safety Alerts"
                      description="PPE reminders and safety guidelines"
                      checked={settings.safetyAlerts}
                      onChange={(value) => handleSettingChange('notifications', 'safetyAlerts', value)}
                    />
                    {(isManager || isAdmin) && (
                      <ToggleSwitch
                        label="Equipment Alerts"
                        description="Equipment maintenance and issues"
                        checked={settings.equipmentAlerts}
                        onChange={(value) => handleSettingChange('notifications', 'equipmentAlerts', value)}
                      />
                    )}
                    {isAdmin && (
                      <ToggleSwitch
                        label="System Alerts"
                        description="Technical issues and system status"
                        checked={settings.systemAlerts}
                        onChange={(value) => handleSettingChange('notifications', 'systemAlerts', value)}
                      />
                    )}
                  </div>
                </div>
              </div>
              
              <div className="border-t pt-4">
                <ToggleSwitch
                  label="Quiet Hours"
                  description="Reduce notifications during specified hours"
                  checked={settings.quietHoursEnabled}
                  onChange={(value) => handleSettingChange('notifications', 'quietHoursEnabled', value)}
                />
                
                {settings.quietHoursEnabled && (
                  <div className="mt-3 grid grid-cols-2 gap-4">
                    <div>
                      <label className="text-sm font-medium">Start Time</label>
                      <input
                        type="time"
                        value={settings.quietHoursStart}
                        onChange={(e) => handleSettingChange('notifications', 'quietHoursStart', e.target.value)}
                        className={`w-full p-2 border rounded-md mt-1 ${
                          theme === 'dark' 
                            ? 'bg-gray-700 border-gray-600 text-white' 
                            : 'bg-white border-gray-300'
                        }`}
                      />
                    </div>
                    <div>
                      <label className="text-sm font-medium">End Time</label>
                      <input
                        type="time"
                        value={settings.quietHoursEnd}
                        onChange={(e) => handleSettingChange('notifications', 'quietHoursEnd', e.target.value)}
                        className={`w-full p-2 border rounded-md mt-1 ${
                          theme === 'dark' 
                            ? 'bg-gray-700 border-gray-600 text-white' 
                            : 'bg-white border-gray-300'
                        }`}
                      />
                    </div>
                  </div>
                )}
              </div>
            </div>
          </SettingSection>

          {/* Privacy Settings - Manager/Admin only */}
          <SettingSection id="privacy" title="Privacy & Data" icon={Shield} managerOnly>
            <div className="space-y-4">
              <ToggleSwitch
                label="Data Sharing"
                description="Share anonymous usage data to help improve the platform"
                checked={settings.dataSharing}
                onChange={(value) => handleSettingChange('privacy', 'dataSharing', value)}
              />
              
              <ToggleSwitch
                label="Analytics"
                description="Enable analytics to track feature usage and performance"
                checked={settings.analyticsEnabled}
                onChange={(value) => handleSettingChange('privacy', 'analyticsEnabled', value)}
              />
              
              {(isManager || isAdmin) && (
                <ToggleSwitch
                  label="Location Tracking"
                  description="Allow location tracking for site-based features"
                  checked={settings.locationTracking}
                  onChange={(value) => handleSettingChange('privacy', 'locationTracking', value)}
                />
              )}
            </div>
          </SettingSection>

          {/* Advanced Settings - Admin only */}
          <SettingSection id="advanced" title="Advanced" icon={SettingsIcon} adminOnly>
            <div className="space-y-4">
              <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
                <div className="flex items-center space-x-2">
                  <Shield className="w-5 h-5 text-yellow-600" />
                  <span className="text-sm text-yellow-800">
                    These settings are for advanced users only. Changes may affect system stability.
                  </span>
                </div>
              </div>
              
              <ToggleSwitch
                label="Debug Mode"
                description="Enable detailed logging and debug information"
                checked={settings.debugMode}
                onChange={(value) => handleSettingChange('advanced', 'debugMode', value)}
              />
              
              <ToggleSwitch
                label="Beta Features"
                description="Access experimental features before general release"
                checked={settings.betaFeatures}
                onChange={(value) => handleSettingChange('advanced', 'betaFeatures', value)}
              />
              
              <ToggleSwitch
                label="API Access"
                description="Enable API access for third-party integrations"
                checked={settings.apiAccess}
                onChange={(value) => handleSettingChange('advanced', 'apiAccess', value)}
              />
            </div>
          </SettingSection>
        </div>
      </div>
    </MainLayout>
  );
};

export default Settings;