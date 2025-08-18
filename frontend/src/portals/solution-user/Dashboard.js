import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  AlertTriangle, Shield, Users, Camera, TrendingUp, 
  Clock, MapPin, Activity, CheckCircle, XCircle,
  Play, Eye, BarChart3, Navigation, Zap, Settings,
  Calendar, Wind, Thermometer, X, ExternalLink,
  ChevronRight, Maximize2, Filter, Download, Loader
} from 'lucide-react';
import { useTheme } from '../../context/ThemeContext';
import MainLayout from '../../components/shared/Layout/MainLayout';
import { backendAPI, zoneminderAPI } from '../../services';
import { 
  useDashboardStats, 
  useZoneminderStatus, 
  useZoneminderCameras, 
  useRecentEvents, 
  useCriticalAlerts 
} from '../../hooks/useAPI';
import { formatters } from '../../utils/formatters';
import { ZONEMINDER_CONSTANTS } from '../../utils/constants';

const Dashboard = () => {
  const navigate = useNavigate();
  const { theme } = useTheme();

  // State for modals and interactive elements
  const [showActivityModal, setShowActivityModal] = useState(false);
  const [showAlertsModal, setShowAlertsModal] = useState(false);
  const [showProgressModal, setShowProgressModal] = useState(false);
  const [selectedDateRange, setSelectedDateRange] = useState('today');
  const [showDatePicker, setShowDatePicker] = useState(false);
  const [currentUser, setCurrentUser] = useState({ firstName: 'Site Manager' });

  // API hooks for real-time data
  const { data: dashboardStats, loading: statsLoading, error: statsError } = useDashboardStats();
  const { data: zoneminderStatus, loading: zmLoading } = useZoneminderStatus();
  const { data: cameras, loading: camerasLoading } = useZoneminderCameras();
  const { data: recentEvents, loading: eventsLoading } = useRecentEvents(24);
  const { data: criticalAlerts, loading: alertsLoading } = useCriticalAlerts(24);

  // Derived data from API responses
  const activeCameras = cameras?.cameras?.filter(cam => cam.status === 'online') || [];
  const totalCameras = cameras?.cameras?.length || 0;
  const activeAlerts = criticalAlerts?.events?.length || 0;
  const recentActivity = recentEvents?.events?.slice(0, 10) || [];
  const priorityAlerts = criticalAlerts?.events?.filter(event => 
    event.severity === 'critical' || event.severity === 'high'
  ).slice(0, 5) || [];

  // Get current site info (using first available site or default)
  const [currentSite, setCurrentSite] = useState({
    name: 'Construction Site Alpha',
    type: 'high_rise_building',
    progress: 0,
    personnel: 0,
    weather: { temp: 72, wind: '8 mph', condition: 'Clear' }
  });

  // Load initial site data
  useEffect(() => {
    const loadSiteData = async () => {
      try {
        const sites = await backendAPI.sites.getAll();
        if (sites && sites.length > 0) {
          const site = sites[0];
          setCurrentSite({
            name: site.name || 'Construction Site Alpha',
            type: site.type || 'high_rise_building', 
            progress: site.progress_percentage || 65,
            personnel: site.active_personnel || 0,
            weather: { 
              temp: 72 + Math.floor(Math.random() * 20), 
              wind: `${5 + Math.floor(Math.random() * 15)} mph`,
              condition: ['Clear', 'Partly Cloudy', 'Overcast'][Math.floor(Math.random() * 3)]
            }
          });
        }
      } catch (error) {
        console.error('Error loading site data:', error);
      }
    };
    loadSiteData();
  }, []);

  // Loading state component
  const LoadingCard = () => (
    <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
      <div className="animate-pulse">
        <div className="flex items-center justify-between">
          <div>
            <div className="h-4 bg-gray-200 rounded w-24 mb-2"></div>
            <div className="h-8 bg-gray-200 rounded w-16"></div>
          </div>
          <div className="w-12 h-12 bg-gray-200 rounded-lg"></div>
        </div>
      </div>
    </div>
  );

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
                Good {new Date().getHours() < 12 ? 'Morning' : new Date().getHours() < 18 ? 'Afternoon' : 'Evening'}, {currentUser.firstName}!
              </h1>
              <p className="text-gray-600 mt-1">
                Welcome back to {currentSite.name} • {formatters.formatProjectPhase(currentSite.type)} Site
              </p>
              <div className="mt-2 flex items-center space-x-4 text-sm text-gray-500">
                <div className="flex items-center space-x-1">
                  <div className={`w-2 h-2 rounded-full ${zoneminderStatus?.status === 'operational' ? 'bg-green-500' : 'bg-red-500'}`}></div>
                  <span>ZoneMinder: {zoneminderStatus?.status || 'Unknown'}</span>
                </div>
                <div>Last Update: {formatters.formatTime(new Date())}</div>
              </div>
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
                    onClick={() => setShowActivityModal(true)}
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
                  <div 
                    key={detection.id} 
                    className="flex items-center space-x-4 p-4 bg-gray-50 rounded-lg cursor-pointer hover:bg-gray-100 transition-colors"
                    onClick={() => setShowActivityModal(true)}
                  >
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
                    onClick={() => setShowAlertsModal(true)}
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

      {/* Activity Details Modal */}
      {showActivityModal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-lg max-w-4xl w-full max-h-[90vh] overflow-hidden">
            <div className="p-6 border-b border-gray-200 flex items-center justify-between">
              <div>
                <h2 className="text-xl font-bold text-gray-900">Live Site Activity Details</h2>
                <p className="text-sm text-gray-600">Real-time activity feed from all cameras</p>
              </div>
              <button 
                onClick={() => setShowActivityModal(false)}
                className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
              >
                <X className="w-5 h-5" />
              </button>
            </div>
            
            <div className="p-6 overflow-y-auto max-h-[60vh]">
              <div className="space-y-4">
                {mockDetections.map((detection, index) => (
                  <div key={detection.id} className="flex items-start space-x-4 p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors">
                    <div 
                      className="w-12 h-12 rounded-lg flex items-center justify-center flex-shrink-0"
                      style={{ backgroundColor: theme.primary[100] }}
                    >
                      <Activity className="w-6 h-6" style={{ color: theme.primary[500] }} />
                    </div>
                    <div className="flex-1">
                      <div className="flex items-center justify-between">
                        <h4 className="font-medium text-gray-900">
                          {detection.personCount} personnel detected in {detection.zone}
                        </h4>
                        <span className="text-xs text-gray-500">{detection.timestamp}</span>
                      </div>
                      <p className="text-sm text-gray-600 mt-1">
                        Camera: {detection.camera} • Confidence: {detection.confidence}%
                      </p>
                      <div className="flex items-center space-x-4 mt-2">
                        <button 
                          onClick={() => navigate('/live-view')}
                          className="flex items-center space-x-1 text-sm text-blue-600 hover:text-blue-700"
                        >
                          <Eye className="w-3 h-3" />
                          <span>View Camera</span>
                        </button>
                        <button className="flex items-center space-x-1 text-sm text-gray-600 hover:text-gray-700">
                          <ExternalLink className="w-3 h-3" />
                          <span>Full Details</span>
                        </button>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
            
            <div className="p-6 border-t border-gray-200 flex justify-between">
              <button 
                onClick={() => navigate('/live-view')}
                className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
              >
                Go to Live View
              </button>
              <button 
                onClick={() => setShowActivityModal(false)}
                className="px-4 py-2 text-gray-700 hover:bg-gray-100 rounded-lg transition-colors"
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Priority Alerts Modal */}
      {showAlertsModal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-lg max-w-4xl w-full max-h-[90vh] overflow-hidden">
            <div className="p-6 border-b border-gray-200 flex items-center justify-between">
              <div>
                <h2 className="text-xl font-bold text-gray-900">Priority Alerts</h2>
                <p className="text-sm text-gray-600">Active alerts requiring immediate attention</p>
              </div>
              <button 
                onClick={() => setShowAlertsModal(false)}
                className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
              >
                <X className="w-5 h-5" />
              </button>
            </div>
            
            <div className="p-6 overflow-y-auto max-h-[60vh]">
              <div className="space-y-4">
                {mockAlerts.filter(alert => alert.priority === 'Critical' || alert.priority === 'High').map((alert) => (
                  <div key={alert.id} className="flex items-start space-x-4 p-4 bg-red-50 border border-red-200 rounded-lg">
                    <AlertTriangle className="w-5 h-5 text-red-600 mt-0.5 flex-shrink-0" />
                    <div className="flex-1">
                      <div className="flex items-center justify-between">
                        <h4 className="font-medium text-gray-900">{alert.title}</h4>
                        <div className="flex items-center space-x-2">
                          <span className={`px-2 py-1 text-xs font-semibold rounded ${
                            alert.priority === 'Critical' ? 'bg-red-100 text-red-800' : 'bg-orange-100 text-orange-800'
                          }`}>
                            {alert.priority}
                          </span>
                        </div>
                      </div>
                      <p className="text-sm text-gray-600 mt-1">{alert.description}</p>
                      <div className="flex items-center justify-between mt-3">
                        <div className="text-xs text-gray-500">
                          {alert.camera} • {alert.zone} • {alert.timestamp}
                        </div>
                        <div className="flex items-center space-x-2">
                          <button 
                            onClick={() => navigate(`/alert-center/${alert.id}`)}
                            className="px-3 py-1 text-sm bg-blue-600 text-white rounded hover:bg-blue-700 transition-colors"
                          >
                            Investigate
                          </button>
                          <button className="px-3 py-1 text-sm bg-gray-100 text-gray-700 rounded hover:bg-gray-200 transition-colors">
                            Acknowledge
                          </button>
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
            
            <div className="p-6 border-t border-gray-200 flex justify-between">
              <button 
                onClick={() => navigate('/alert-center')}
                className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
              >
                Go to Alert Center
              </button>
              <button 
                onClick={() => setShowAlertsModal(false)}
                className="px-4 py-2 text-gray-700 hover:bg-gray-100 rounded-lg transition-colors"
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Project Progress Modal */}
      {showProgressModal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-lg max-w-3xl w-full max-h-[90vh] overflow-hidden">
            <div className="p-6 border-b border-gray-200 flex items-center justify-between">
              <div>
                <h2 className="text-xl font-bold text-gray-900">Project Progress Details</h2>
                <p className="text-sm text-gray-600">{currentSite.name}</p>
              </div>
              <button 
                onClick={() => setShowProgressModal(false)}
                className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
              >
                <X className="w-5 h-5" />
              </button>
            </div>
            
            <div className="p-6 overflow-y-auto max-h-[60vh]">
              <div className="space-y-6">
                {/* Overall Progress */}
                <div className="bg-gray-50 p-6 rounded-lg">
                  <div className="flex items-center justify-between mb-4">
                    <h3 className="font-semibold text-gray-900">Overall Progress</h3>
                    <span className="text-2xl font-bold text-blue-600">{currentSite.progress}%</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-3">
                    <div 
                      className="bg-blue-600 h-3 rounded-full transition-all duration-300" 
                      style={{ width: `${currentSite.progress}%` }}
                    ></div>
                  </div>
                  <p className="text-sm text-gray-600 mt-2">
                    Expected completion: {new Date(currentSite.completion).toLocaleDateString()}
                  </p>
                </div>

                {/* Phase Breakdown */}
                <div>
                  <h3 className="font-semibold text-gray-900 mb-4">Phase Breakdown</h3>
                  <div className="space-y-4">
                    {[
                      { phase: 'Foundation', progress: 100, status: 'Complete' },
                      { phase: 'Framing', progress: 85, status: 'In Progress' },
                      { phase: 'MEP Installation', progress: 45, status: 'In Progress' },
                      { phase: 'Interior Finishing', progress: 15, status: 'Starting Soon' },
                      { phase: 'Final Inspection', progress: 0, status: 'Pending' }
                    ].map((item, index) => (
                      <div key={index} className="flex items-center justify-between p-3 bg-white border rounded-lg">
                        <div>
                          <h4 className="font-medium text-gray-900">{item.phase}</h4>
                          <span className={`text-xs px-2 py-1 rounded ${
                            item.status === 'Complete' ? 'bg-green-100 text-green-700' :
                            item.status === 'In Progress' ? 'bg-blue-100 text-blue-700' :
                            'bg-gray-100 text-gray-700'
                          }`}>
                            {item.status}
                          </span>
                        </div>
                        <div className="text-right">
                          <div className="text-lg font-bold text-gray-900">{item.progress}%</div>
                          <div className="w-20 bg-gray-200 rounded-full h-2 mt-1">
                            <div 
                              className="bg-blue-600 h-2 rounded-full" 
                              style={{ width: `${item.progress}%` }}
                            ></div>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>
            
            <div className="p-6 border-t border-gray-200 flex justify-between">
              <button 
                onClick={() => navigate('/reports')}
                className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
              >
                View Detailed Reports
              </button>
              <button 
                onClick={() => setShowProgressModal(false)}
                className="px-4 py-2 text-gray-700 hover:bg-gray-100 rounded-lg transition-colors"
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Date Range Picker Modal */}
      {showDatePicker && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-lg max-w-md w-full">
            <div className="p-6 border-b border-gray-200">
              <h3 className="text-lg font-semibold text-gray-900">Select Date Range</h3>
            </div>
            <div className="p-6">
              <div className="space-y-3">
                {['today', '7days', '30days', 'custom'].map((range) => (
                  <label key={range} className="flex items-center space-x-3">
                    <input
                      type="radio"
                      name="dateRange"
                      value={range}
                      checked={selectedDateRange === range}
                      onChange={(e) => setSelectedDateRange(e.target.value)}
                      className="text-blue-600"
                    />
                    <span className="text-sm text-gray-700 capitalize">
                      {range === 'today' ? 'Today' :
                       range === '7days' ? 'Last 7 Days' :
                       range === '30days' ? 'Last 30 Days' :
                       'Custom Range'}
                    </span>
                  </label>
                ))}
              </div>
            </div>
            <div className="p-6 border-t border-gray-200 flex justify-end space-x-3">
              <button 
                onClick={() => setShowDatePicker(false)}
                className="px-4 py-2 text-gray-700 hover:bg-gray-100 rounded-lg transition-colors"
              >
                Cancel
              </button>
              <button 
                onClick={() => setShowDatePicker(false)}
                className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
              >
                Apply Filter
              </button>
            </div>
          </div>
        </div>
      )}
    </MainLayout>
  );
};

export default Dashboard;