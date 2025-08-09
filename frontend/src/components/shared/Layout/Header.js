import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  Bell, Search, Settings, LogOut, User, Shield, 
  ChevronDown, Menu, Sun, Cloud, Wind, Thermometer,
  Clock, MapPin
} from 'lucide-react';
import { useTheme } from '../../../context/ThemeContext';
import { mockUser, mockSites, mockNotifications } from '../../../data/mockData';

const Header = ({ onToggleSidebar, portal = 'solution-user' }) => {
  const navigate = useNavigate();
  const { theme, themes, changeTheme, themeDisplayNames } = useTheme();
  const [showNotifications, setShowNotifications] = useState(false);
  const [showProfile, setShowProfile] = useState(false);
  const [showThemeSelector, setShowThemeSelector] = useState(false);

  const currentSite = mockSites.find(s => s.name === mockUser.currentSite) || mockSites[0];
  const unreadCount = mockNotifications.filter(n => !n.read).length;

  const handleLogout = () => {
    navigate('/login');
  };

  const getPortalTitle = (portal) => {
    switch(portal) {
      case 'solution-admin': return 'Admin Portal';
      case 'vms-user': return 'VMS Operations';
      case 'vms-admin': return 'VMS Admin';
      default: return 'Construction Portal';
    }
  };

  const WeatherWidget = () => (
    <div className="hidden md:flex items-center space-x-4 px-4 py-2 bg-gray-50 rounded-lg">
      <div className="flex items-center space-x-2">
        {currentSite.weather.condition === 'Clear' ? (
          <Sun className="w-4 h-4 text-yellow-500" />
        ) : currentSite.weather.condition === 'Partly Cloudy' ? (
          <Cloud className="w-4 h-4 text-gray-500" />
        ) : (
          <Cloud className="w-4 h-4 text-gray-600" />
        )}
        <span className="text-sm font-medium">{currentSite.weather.temp}°F</span>
      </div>
      <div className="flex items-center space-x-1 text-xs text-gray-600">
        <Wind className="w-3 h-3" />
        <span>{currentSite.weather.wind}</span>
      </div>
      <div className="text-xs text-gray-500">{currentSite.weather.condition}</div>
    </div>
  );

  return (
    <header className="bg-white border-b border-gray-200 px-6 py-4 flex items-center justify-between relative z-20">
      {/* Left Section */}
      <div className="flex items-center space-x-4">
        <button
          onClick={onToggleSidebar}
          className="lg:hidden p-2 hover:bg-gray-100 rounded-lg transition-colors"
        >
          <Menu className="w-5 h-5" />
        </button>
        
        <div className="flex items-center space-x-3">
          <div>
            <h1 className="text-xl font-bold text-gray-900">{getPortalTitle(portal)}</h1>
            <div className="flex items-center space-x-2 text-sm text-gray-600">
              <MapPin className="w-3 h-3" />
              <span>{currentSite.name}</span>
              <span className="text-gray-400">•</span>
              <Clock className="w-3 h-3" />
              <span>{new Date().toLocaleTimeString()}</span>
            </div>
          </div>
        </div>
      </div>

      {/* Center Section - Weather & Status */}
      <div className="hidden lg:flex items-center space-x-6">
        <WeatherWidget />
        
        {/* Site Status */}
        <div className="flex items-center space-x-4">
          <div className="text-center">
            <div className="text-lg font-bold text-gray-900">{currentSite.personnel}</div>
            <div className="text-xs text-gray-500">Personnel</div>
          </div>
          <div className="text-center">
            <div className="text-lg font-bold text-gray-900">{currentSite.cameras}</div>
            <div className="text-xs text-gray-500">Cameras</div>
          </div>
          <div className="text-center">
            <div className={`text-lg font-bold ${currentSite.activeAlerts > 0 ? 'text-red-600' : 'text-green-600'}`}>
              {currentSite.activeAlerts}
            </div>
            <div className="text-xs text-gray-500">Alerts</div>
          </div>
        </div>
      </div>

      {/* Right Section */}
      <div className="flex items-center space-x-4">
        {/* Global Search */}
        <div className="hidden md:flex items-center relative">
          <Search className="w-4 h-4 absolute left-3 text-gray-400" />
          <input
            type="text"
            placeholder="Search cameras, alerts..."
            className="pl-10 pr-4 py-2 w-64 text-sm border border-gray-200 rounded-lg focus:ring-1 focus:border-transparent"
            style={{ '--tw-ring-color': theme.primary[500] + '40' }}
          />
        </div>

        {/* Notifications */}
        <div className="relative">
          <button
            onClick={() => setShowNotifications(!showNotifications)}
            className="relative p-2 hover:bg-gray-100 rounded-lg transition-colors"
          >
            <Bell className="w-5 h-5" />
            {unreadCount > 0 && (
              <span className="absolute -top-1 -right-1 bg-red-500 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center">
                {unreadCount}
              </span>
            )}
          </button>

          {showNotifications && (
            <div className="absolute right-0 mt-2 w-80 bg-white rounded-lg shadow-lg border border-gray-200 py-2 z-50">
              <div className="px-4 py-2 border-b border-gray-100">
                <h3 className="font-semibold text-gray-900">Notifications</h3>
              </div>
              <div className="max-h-64 overflow-y-auto">
                {mockNotifications.map((notification) => (
                  <div
                    key={notification.id}
                    className={`px-4 py-3 hover:bg-gray-50 cursor-pointer ${
                      !notification.read ? 'bg-blue-50' : ''
                    }`}
                    onClick={() => {
                      navigate(notification.actionUrl);
                      setShowNotifications(false);
                    }}
                  >
                    <div className="flex items-start space-x-3">
                      <div className={`w-2 h-2 rounded-full mt-2 ${
                        notification.priority === 'high' ? 'bg-red-500' :
                        notification.priority === 'medium' ? 'bg-yellow-500' : 'bg-blue-500'
                      }`}></div>
                      <div className="flex-1">
                        <p className="text-sm font-medium text-gray-900">{notification.title}</p>
                        <p className="text-xs text-gray-600 mt-1">{notification.message}</p>
                        <p className="text-xs text-gray-400 mt-1">
                          {new Date(notification.timestamp).toLocaleTimeString()}
                        </p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Profile Menu */}
        <div className="relative">
          <button
            onClick={() => setShowProfile(!showProfile)}
            className="flex items-center space-x-2 p-2 hover:bg-gray-100 rounded-lg transition-colors"
          >
            <div 
              className="w-8 h-8 rounded-full flex items-center justify-center text-white text-sm font-semibold"
              style={{ backgroundColor: theme.primary[500] }}
            >
              {mockUser.firstName[0]}{mockUser.lastName[0]}
            </div>
            <div className="hidden md:block text-left">
              <p className="text-sm font-medium text-gray-900">{mockUser.displayName}</p>
              <p className="text-xs text-gray-500">{mockUser.role}</p>
            </div>
            <ChevronDown className="w-4 h-4" />
          </button>

          {showProfile && (
            <div className="absolute right-0 mt-2 w-64 bg-white rounded-lg shadow-lg border border-gray-200 py-2 z-50">
              <div className="px-4 py-3 border-b border-gray-100">
                <p className="font-medium text-gray-900">{mockUser.displayName}</p>
                <p className="text-sm text-gray-500">{mockUser.email}</p>
                <p className="text-xs text-gray-400">{mockUser.role} • {mockUser.company}</p>
              </div>
              
              <div className="py-2">
                <button
                  onClick={() => {
                    navigate('/profile');
                    setShowProfile(false);
                  }}
                  className="w-full px-4 py-2 text-left flex items-center space-x-3 hover:bg-gray-50"
                >
                  <User className="w-4 h-4" />
                  <span className="text-sm">My Profile</span>
                </button>
                
                <button
                  onClick={() => {
                    navigate('/settings');
                    setShowProfile(false);
                  }}
                  className="w-full px-4 py-2 text-left flex items-center space-x-3 hover:bg-gray-50"
                >
                  <Settings className="w-4 h-4" />
                  <span className="text-sm">Settings</span>
                </button>

                {/* Theme Selector */}
                <div className="relative">
                  <button
                    onClick={() => setShowThemeSelector(!showThemeSelector)}
                    className="w-full px-4 py-2 text-left flex items-center space-x-3 hover:bg-gray-50"
                  >
                    <div 
                      className="w-4 h-4 rounded-full border-2 border-gray-300"
                      style={{ backgroundColor: theme.primary[500] }}
                    ></div>
                    <span className="text-sm">Theme: {themeDisplayNames[theme.currentTheme] || 'Microsoft Blue'}</span>
                    <ChevronDown className="w-3 h-3 ml-auto" />
                  </button>

                  {showThemeSelector && (
                    <div className="absolute left-0 top-full w-full bg-white rounded-lg shadow-lg border border-gray-200 py-1 z-50">
                      {themes.map((themeName) => (
                        <button
                          key={themeName}
                          onClick={() => {
                            changeTheme(themeName);
                            setShowThemeSelector(false);
                          }}
                          className="w-full px-4 py-2 text-left flex items-center space-x-3 hover:bg-gray-50"
                        >
                          <div 
                            className="w-3 h-3 rounded-full border border-gray-300"
                            style={{ backgroundColor: Object.values(themes)[themes.indexOf(themeName)]?.primary?.[500] || '#0078d4' }}
                          ></div>
                          <span className="text-sm">{themeDisplayNames[themeName]}</span>
                        </button>
                      ))}
                    </div>
                  )}
                </div>
              </div>

              <div className="border-t border-gray-100 pt-2">
                <button
                  onClick={handleLogout}
                  className="w-full px-4 py-2 text-left flex items-center space-x-3 hover:bg-gray-50 text-red-600"
                >
                  <LogOut className="w-4 h-4" />
                  <span className="text-sm">Sign Out</span>
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </header>
  );
};

export default Header;