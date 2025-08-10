import React, { useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { 
  Home, Video, History, Clock, MapPin, Navigation, 
  AlertTriangle, BarChart3, Settings, Phone, 
  Menu, X, Shield, Building2, Users, ChevronDown,
  ChevronRight, FileText
} from 'lucide-react';
import { useTheme } from '../../../context/ThemeContext';
import { mockUser, mockSites, mockNotifications } from '../../../data/mockData';

const Sidebar = ({ isCollapsed, onToggleCollapse, portal = 'solution-user' }) => {
  const location = useLocation();
  const navigate = useNavigate();
  const { theme } = useTheme();
  const [expandedSections, setExpandedSections] = useState(['live_operations', 'historical']);

  const toggleSection = (sectionId) => {
    setExpandedSections(prev => 
      prev.includes(sectionId) 
        ? prev.filter(id => id !== sectionId)
        : [...prev, sectionId]
    );
  };

  const menuSections = {
    'solution-user': [
      {
        id: 'dashboard',
        title: 'DASHBOARD',
        icon: Home,
        items: [
          { name: 'Dashboard Home', path: '/dashboard', icon: Home }
        ]
      },
      {
        id: 'live_operations',
        title: 'LIVE OPERATIONS',
        icon: Video,
        items: [
          { name: 'Live View', path: '/live-view', icon: Video, badge: 'LIVE' },
          { name: 'Live Street View', path: '/live-street-view', icon: Navigation, badge: 'GPS' }
        ]
      },
      {
        id: 'historical',
        title: 'HISTORICAL ANALYSIS',
        icon: History,
        items: [
          { name: 'Video Review', path: '/video-review', icon: History },
          { name: 'Time Lapse', path: '/time-lapse', icon: Clock },
          { name: 'Time Comparison', path: '/time-comparison', icon: Clock },
          { name: 'Historical Street View', path: '/historical-street', icon: Navigation },
          { name: 'Street View Comparison', path: '/street-comparison', icon: Navigation }
        ]
      },
      {
        id: 'site_management',
        title: 'SITE MANAGEMENT',
        icon: MapPin,
        items: [
          { name: 'Site Overview', path: '/site-overview', icon: MapPin },
          { name: 'Personnel Management', path: '/personnel', icon: Users },
          { name: 'Field Assessment', path: '/field-assessment', icon: Navigation }
        ]
      },
      {
        id: 'safety_alerts',
        title: 'SAFETY & ALERTS',
        icon: AlertTriangle,
        items: [
          { name: 'Alert Center', path: '/alert-center', icon: AlertTriangle, badge: mockNotifications.filter(n => !n.read).length },
          { name: 'AI Analytics', path: '/ai-analytics', icon: BarChart3 }
        ]
      },
      {
        id: 'reports_docs',
        title: 'REPORTS & DOCUMENTATION',
        icon: FileText,
        items: [
          { name: 'Reports Center', path: '/reports', icon: FileText }
        ]
      },
      {
        id: 'settings',
        title: 'SETTINGS',
        icon: Settings,
        items: [
          { name: 'Path Administration', path: '/path-admin', icon: MapPin },
          { name: 'My Profile', path: '/profile', icon: Users }
        ]
      }
    ],
    'solution-admin': [
      {
        id: 'dashboard',
        title: 'EXECUTIVE DASHBOARD',
        icon: Home,
        items: [
          { name: 'Admin Dashboard', path: '/admin/dashboard', icon: Home }
        ]
      },
      {
        id: 'organization',
        title: 'ORGANIZATION',
        icon: Building2,
        items: [
          { name: 'User Directory', path: '/admin/users', icon: Users },
          { name: 'Department Management', path: '/admin/departments', icon: Building2 },
          { name: 'Access Control', path: '/admin/access-control', icon: Shield }
        ]
      },
      {
        id: 'ai_management',
        title: 'AI MANAGEMENT',
        icon: BarChart3,
        items: [
          { name: 'AI Models', path: '/admin/ai-models', icon: BarChart3 },
          { name: 'Detection Rules', path: '/admin/detection-rules', icon: Settings }
        ]
      },
      {
        id: 'system_config',
        title: 'SYSTEM CONFIG',
        icon: Settings,
        items: [
          { name: 'Global Settings', path: '/admin/settings', icon: Settings },
          { name: 'Reporting & Analytics', path: '/admin/reports', icon: BarChart3 }
        ]
      }
    ]
  };

  const currentSections = menuSections[portal] || menuSections['solution-user'];

  const isActiveRoute = (path) => {
    return location.pathname === path;
  };

  return (
    <div className={`fixed left-0 top-0 h-full bg-white border-r border-gray-200 transition-all duration-300 z-30 flex flex-col ${
      isCollapsed ? 'w-16' : 'w-64'
    }`}>
      {/* Header */}
      <div className="flex items-center justify-between p-4 border-b border-gray-200">
        <div className={`flex items-center space-x-3 ${isCollapsed ? 'justify-center' : ''}`}>
          <Shield className="w-8 h-8" style={{ color: theme.primary[500] }} />
          {!isCollapsed && (
            <div>
              <h1 className="text-lg font-bold text-gray-900">ConstructionAI</h1>
              <p className="text-xs text-gray-500">{mockUser.company}</p>
            </div>
          )}
        </div>
        <button
          onClick={onToggleCollapse}
          className="p-1 hover:bg-gray-100 rounded-lg transition-colors"
        >
          {isCollapsed ? <Menu className="w-5 h-5" /> : <X className="w-5 h-5" />}
        </button>
      </div>

      {/* Site Selector */}
      {!isCollapsed && (
        <div className="p-4 border-b border-gray-100">
          <select 
            className="w-full text-sm px-3 py-2 border border-gray-200 rounded-lg focus:ring-1 focus:border-transparent"
            style={{ '--tw-ring-color': theme.primary[500] + '40' }}
            defaultValue={mockUser.currentSite}
          >
            {mockSites.map(site => (
              <option key={site.id} value={site.name}>{site.name}</option>
            ))}
          </select>
        </div>
      )}

      {/* Navigation Menu */}
      <div 
        className="flex-1 min-h-0 overflow-y-scroll sidebar-scroll"
        style={{
          scrollbarWidth: 'thin',
          scrollbarColor: '#d1d5db #f3f4f6'
        }}
      >
        <nav className="px-2 py-4 space-y-2">
          {currentSections.map((section) => (
            <div key={section.id}>
              {/* Section Header */}
              <div
                className={`flex items-center justify-between px-3 py-2 text-xs font-semibold text-gray-500 uppercase tracking-wide cursor-pointer hover:text-gray-700 ${
                  isCollapsed ? 'justify-center' : ''
                }`}
                onClick={() => !isCollapsed && toggleSection(section.id)}
              >
                {isCollapsed ? (
                  <section.icon className="w-5 h-5" />
                ) : (
                  <>
                    <span>{section.title}</span>
                    {section.items.length > 1 && (
                      expandedSections.includes(section.id) ? 
                        <ChevronDown className="w-4 h-4" /> : 
                        <ChevronRight className="w-4 h-4" />
                    )}
                  </>
                )}
              </div>

              {/* Section Items */}
              {(isCollapsed || expandedSections.includes(section.id)) && (
                <div className={isCollapsed ? 'space-y-1' : 'ml-2 space-y-1'}>
                  {section.items.map((item) => (
                    <button
                      key={item.path}
                      onClick={() => navigate(item.path)}
                      className={`w-full flex items-center space-x-3 px-3 py-2 text-sm rounded-lg transition-all duration-200 ${
                        isActiveRoute(item.path)
                          ? 'text-white shadow-md'
                          : 'text-gray-700 hover:bg-gray-100'
                      } ${isCollapsed ? 'justify-center' : ''}`}
                      style={{
                        backgroundColor: isActiveRoute(item.path) ? theme.primary[500] : 'transparent'
                      }}
                    >
                      <item.icon className="w-5 h-5 flex-shrink-0" />
                      {!isCollapsed && (
                        <>
                          <span className="flex-1 text-left">{item.name}</span>
                          {item.badge && (
                            <span 
                              className={`px-2 py-0.5 text-xs font-semibold rounded-full ${
                                typeof item.badge === 'number' 
                                  ? 'bg-red-100 text-red-600'
                                  : item.badge === 'LIVE'
                                  ? 'bg-green-100 text-green-600'
                                  : 'bg-blue-100 text-blue-600'
                              }`}
                            >
                              {item.badge}
                            </span>
                          )}
                        </>
                      )}
                    </button>
                  ))}
                </div>
              )}
            </div>
          ))}
        </nav>
      </div>

      {/* Emergency Footer */}
      <div className="border-t border-gray-200 p-4">
        <button 
          className="w-full flex items-center justify-center space-x-2 bg-red-600 text-white py-2 px-3 rounded-lg hover:bg-red-700 transition-colors"
          onClick={() => window.open('tel:+15551234567')}
        >
          <Phone className="w-4 h-4" />
          {!isCollapsed && <span className="text-sm font-medium">EMERGENCY</span>}
        </button>
        {!isCollapsed && (
          <p className="text-center text-xs text-gray-500 mt-2">(555) 123-4567</p>
        )}
      </div>
    </div>
  );
};

export default Sidebar;