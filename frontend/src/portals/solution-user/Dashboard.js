import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  AlertTriangle, Shield, Users, Camera, TrendingUp, 
  Clock, MapPin, Activity, CheckCircle, XCircle,
  Play, Eye, BarChart3, Navigation, Zap, Settings,
  Calendar, Wind, Thermometer, X, ExternalLink,
  ChevronRight, Maximize2, Filter, Download
} from 'lucide-react';
import { useTheme } from '../../context/ThemeContext';
import MainLayout from '../../components/shared/Layout/MainLayout';
import { mockSites, mockAlerts, mockAnalytics, mockDetections, mockUser } from '../../data/mockData';

const Dashboard = () => {
  const navigate = useNavigate();
  const { theme } = useTheme();
  const currentSite = mockSites.find(s => s.name === mockUser.currentSite) || mockSites[0];

  const StatCard = ({ title, value, subtitle, icon: Icon, color, onClick, badge }) => (
    <div 
      className="bg-white rounded-xl p-6 shadow-sm border border-gray-100 hover:shadow-md transition-all duration-200 cursor-pointer transform hover:scale-[1.02]"
      onClick={onClick}
    >
      <div className="flex items-center justify-between">
        <div>
          <div className="flex items-center space-x-2">
            <h3 className="text-sm font-medium text-gray-600">{title}</h3>
            {badge && (
              <span className={`px-2 py-0.5 text-xs font-semibold rounded-full ${
                badge.type === 'live' ? 'bg-green-100 text-green-600' :
                badge.type === 'alert' ? 'bg-red-100 text-red-600' :
                'bg-blue-100 text-blue-600'
              }`}>
                {badge.text}
              </span>
            )}
          </div>
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

  const AlertCard = ({ alert }) => {
    const priorityColors = {
      critical: 'border-red-200 bg-red-50',
      high: 'border-orange-200 bg-orange-50',
      medium: 'border-yellow-200 bg-yellow-50',
      low: 'border-blue-200 bg-blue-50'
    };

    const priorityIcons = {
      critical: XCircle,
      high: AlertTriangle,
      medium: AlertTriangle,
      low: CheckCircle
    };

    const IconComponent = priorityIcons[alert.priority];

    return (
      <div 
        className={`p-4 rounded-lg border-l-4 ${priorityColors[alert.priority]} cursor-pointer hover:shadow-sm transition-shadow`}
        onClick={() => navigate(`/alert-center/${alert.id}`)}
      >
        <div className="flex items-start space-x-3">
          <IconComponent className={`w-5 h-5 mt-0.5 ${
            alert.priority === 'critical' ? 'text-red-600' :
            alert.priority === 'high' ? 'text-orange-600' :
            alert.priority === 'medium' ? 'text-yellow-600' : 'text-blue-600'
          }`} />
          <div className="flex-1 min-w-0">
            <h4 className="text-sm font-semibold text-gray-900 truncate">{alert.title}</h4>
            <p className="text-sm text-gray-600 mt-1">{alert.message}</p>
            <div className="flex items-center justify-between mt-2">
              <div className="flex items-center space-x-2 text-xs text-gray-500">
                <MapPin className="w-3 h-3" />
                <span>{alert.location}</span>
                <Clock className="w-3 h-3 ml-2" />
                <span>{new Date(alert.timestamp).toLocaleTimeString()}</span>
              </div>
              <span className={`px-2 py-1 text-xs font-medium rounded-full ${
                alert.status === 'open' ? 'bg-red-100 text-red-600' :
                alert.status === 'investigating' ? 'bg-yellow-100 text-yellow-600' :
                'bg-green-100 text-green-600'
              }`}>
                {alert.status.toUpperCase()}
              </span>
            </div>
          </div>
        </div>
      </div>
    );
  };

  const QuickActionButton = ({ icon: Icon, title, subtitle, onClick, color, disabled = false }) => (
    <button
      onClick={onClick}
      disabled={disabled}
      className={`p-4 bg-white rounded-xl border border-gray-200 hover:border-gray-300 transition-all duration-200 text-left group ${
        disabled ? 'opacity-50 cursor-not-allowed' : 'hover:shadow-md transform hover:scale-[1.02]'
      }`}
    >
      <div className="flex items-center space-x-4">
        <div 
          className="p-3 rounded-lg group-hover:scale-110 transition-transform"
          style={{ backgroundColor: color + '20' }}
        >
          <Icon className="w-5 h-5" style={{ color }} />
        </div>
        <div>
          <h3 className="font-semibold text-gray-900">{title}</h3>
          <p className="text-sm text-gray-600">{subtitle}</p>
        </div>
      </div>
    </button>
  );

  return (
    <MainLayout portal="solution-user">
      <div className="p-6 space-y-6">
        {/* Welcome Header */}
        <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
          <div className="flex flex-col md:flex-row md:items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">
                Good {new Date().getHours() < 12 ? 'Morning' : new Date().getHours() < 18 ? 'Afternoon' : 'Evening'}, {mockUser.firstName}!
              </h1>
              <p className="text-gray-600 mt-1">
                Welcome back to {currentSite.name} • {currentSite.type.charAt(0).toUpperCase() + currentSite.type.slice(1)} Site
              </p>
            </div>
            <div className="mt-4 md:mt-0 flex items-center space-x-4">
              <div className="text-right">
                <div className="text-sm text-gray-500">Project Progress</div>
                <div className="text-xl font-bold" style={{ color: theme.primary[500] }}>
                  {currentSite.progress}%
                </div>
              </div>
              <div className="w-16 h-16 relative">
                <svg className="w-16 h-16 transform -rotate-90" viewBox="0 0 36 36">
                  <path
                    d="m18,2.0845 a 15.9155,15.9155 0 0,1 0,31.831 a 15.9155,15.9155 0 0,1 0,-31.831"
                    fill="none"
                    stroke="#e5e7eb"
                    strokeWidth="2"
                  />
                  <path
                    d="m18,2.0845 a 15.9155,15.9155 0 0,1 0,31.831 a 15.9155,15.9155 0 0,1 0,-31.831"
                    fill="none"
                    stroke={theme.primary[500]}
                    strokeWidth="2"
                    strokeDasharray={`${currentSite.progress}, 100`}
                  />
                </svg>
              </div>
            </div>
          </div>
        </div>

        {/* Key Metrics Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <StatCard
            title="Active Personnel"
            value={currentSite.personnel}
            subtitle={`${mockAnalytics.operationalMetrics.lastWeekComparison} from last week`}
            icon={Users}
            color={theme.success[500]}
            onClick={() => navigate('/personnel-tracking')}
            badge={{ type: 'live', text: 'LIVE' }}
          />
          <StatCard
            title="Camera Status"
            value={`${currentSite.cameras - 1}/${currentSite.cameras}`}
            subtitle="1 camera in maintenance"
            icon={Camera}
            color={theme.primary[500]}
            onClick={() => navigate('/live-view')}
          />
          <StatCard
            title="Active Alerts"
            value={currentSite.activeAlerts}
            subtitle={currentSite.activeAlerts > 0 ? `${mockAlerts.filter(a => a.priority === 'critical').length} critical` : 'All clear'}
            icon={AlertTriangle}
            color={currentSite.activeAlerts > 0 ? theme.danger[500] : theme.success[500]}
            onClick={() => navigate('/alert-center')}
            badge={currentSite.activeAlerts > 0 ? { type: 'alert', text: 'ACTION NEEDED' } : null}
          />
          <StatCard
            title="Safety Score"
            value={`${mockAnalytics.safetyMetrics.safetyScore}/10`}
            subtitle={`${mockAnalytics.safetyMetrics.ppeComplianceRate}% PPE compliance`}
            icon={Shield}
            color={theme.primary[500]}
            onClick={() => navigate('/ai-analytics')}
          />
        </div>

        {/* Main Content Grid */}
        <div className="grid grid-cols-1 xl:grid-cols-3 gap-6">
          {/* Live Activity Feed */}
          <div className="xl:col-span-2 bg-white rounded-xl shadow-sm border border-gray-100">
            <div className="p-6 border-b border-gray-100">
              <div className="flex items-center justify-between">
                <h2 className="text-lg font-semibold text-gray-900">Live Site Activity</h2>
                <div className="flex items-center space-x-2">
                  <div className="flex items-center space-x-1">
                    <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                    <span className="text-sm text-gray-500">Live</span>
                  </div>
                  <button 
                    onClick={() => navigate('/live-view')}
                    className="text-sm font-medium hover:underline"
                    style={{ color: theme.primary[500] }}
                  >
                    View All
                  </button>
                </div>
              </div>
            </div>
            
            <div className="p-6">
              <div className="space-y-4">
                {mockDetections.map((detection, index) => (
                  <div key={detection.id} className="flex items-center space-x-4 p-4 bg-gray-50 rounded-lg">
                    <div 
                      className="w-12 h-12 rounded-lg flex items-center justify-center"
                      style={{ backgroundColor: theme.primary[100] }}
                    >
                      <Activity className="w-6 h-6" style={{ color: theme.primary[500] }} />
                    </div>
                    <div className="flex-1">
                      <div className="flex items-center space-x-2">
                        <h4 className="font-medium text-gray-900">
                          {detection.personCount} personnel detected
                        </h4>
                        <span className={`px-2 py-0.5 text-xs font-semibold rounded-full ${
                          detection.ppeCompliance >= 90 ? 'bg-green-100 text-green-600' :
                          detection.ppeCompliance >= 75 ? 'bg-yellow-100 text-yellow-600' :
                          'bg-red-100 text-red-600'
                        }`}>
                          {detection.ppeCompliance}% PPE
                        </span>
                      </div>
                      <div className="text-sm text-gray-600 mt-1">
                        Camera: {mockSites[0].cameras > index ? `Camera ${index + 1}` : 'Main Entrance'} • 
                        Confidence: {Math.round(detection.confidence * 100)}%
                      </div>
                    </div>
                    <div className="text-sm text-gray-500">
                      {new Date(detection.timestamp).toLocaleTimeString()}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Priority Alerts & Quick Actions */}
          <div className="space-y-6">
            {/* Priority Alerts */}
            <div className="bg-white rounded-xl shadow-sm border border-gray-100">
              <div className="p-6 border-b border-gray-100">
                <div className="flex items-center justify-between">
                  <h2 className="text-lg font-semibold text-gray-900">Priority Alerts</h2>
                  <button 
                    onClick={() => navigate('/alert-center')}
                    className="text-sm font-medium hover:underline"
                    style={{ color: theme.primary[500] }}
                  >
                    View All ({mockAlerts.length})
                  </button>
                </div>
              </div>
              <div className="p-6 space-y-4">
                {mockAlerts.slice(0, 3).map((alert) => (
                  <AlertCard key={alert.id} alert={alert} />
                ))}
              </div>
            </div>

            {/* Weather & Site Conditions */}
            <div className="bg-white rounded-xl shadow-sm border border-gray-100">
              <div className="p-6 border-b border-gray-100">
                <h2 className="text-lg font-semibold text-gray-900">Site Conditions</h2>
              </div>
              <div className="p-6">
                <div className="grid grid-cols-2 gap-4">
                  <div className="text-center">
                    <div className="flex items-center justify-center mb-2">
                      <Thermometer className="w-8 h-8 text-orange-500" />
                    </div>
                    <div className="text-2xl font-bold text-gray-900">{currentSite.weather.temp}°F</div>
                    <div className="text-sm text-gray-500">Temperature</div>
                  </div>
                  <div className="text-center">
                    <div className="flex items-center justify-center mb-2">
                      <Wind className="w-8 h-8 text-blue-500" />
                    </div>
                    <div className="text-2xl font-bold text-gray-900">{currentSite.weather.wind}</div>
                    <div className="text-sm text-gray-500">Wind Speed</div>
                  </div>
                </div>
                <div className="mt-4 p-3 bg-blue-50 rounded-lg text-center">
                  <div className="text-sm font-medium text-gray-900">{currentSite.weather.condition}</div>
                  <div className="text-xs text-gray-600 mt-1">Optimal working conditions</div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-100">
          <div className="p-6 border-b border-gray-100">
            <h2 className="text-lg font-semibold text-gray-900">Quick Actions</h2>
          </div>
          <div className="p-6">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
              <QuickActionButton
                icon={Eye}
                title="Live Monitoring"
                subtitle="View all camera feeds"
                onClick={() => navigate('/live-view')}
                color={theme.primary[500]}
              />
              <QuickActionButton
                icon={Navigation}
                title="Street View Tour"
                subtitle="Start GPS-guided inspection"
                onClick={() => navigate('/live-street-view')}
                color={theme.success[500]}
              />
              <QuickActionButton
                icon={BarChart3}
                title="Generate Report"
                subtitle="Create safety analysis"
                onClick={() => navigate('/ai-analytics')}
                color={theme.warning[500]}
              />
              <QuickActionButton
                icon={Settings}
                title="Field Assessment"
                subtitle="Mobile inspection tool"
                onClick={() => navigate('/field-assessment')}
                color={theme.secondary[600]}
              />
            </div>
          </div>
        </div>
      </div>
    </MainLayout>
  );
};

export default Dashboard;