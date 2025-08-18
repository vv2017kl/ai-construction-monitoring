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
import weatherAPI from '../../services/weatherAPI';
import { 
  useDashboardStats, 
  useZoneminderStatus, 
  useZoneminderCameras, 
  useRecentEvents, 
  useCriticalAlerts 
} from '../../hooks/useAPI';
import { formatters } from '../../utils/formatters';
import { ZONEMINDER_CONSTANTS } from '../../utils/constants';
import { generateDashboardMetrics } from '../../utils/dataCalculations';

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

  // State for calculated metrics and weather
  const [calculatedMetrics, setCalculatedMetrics] = useState(null);
  const [weatherData, setWeatherData] = useState(null);
  const [currentSite, setCurrentSite] = useState({
    name: 'Loading...',
    type: 'construction_site',
    progress: 0,
    personnel: 0
  });

  // Calculate real-time metrics from ZoneMinder data
  useEffect(() => {
    if (cameras && recentEvents && criticalAlerts) {
      const metrics = generateDashboardMetrics({
        cameras,
        events: recentEvents,
        zones: {},
        status: zoneminderStatus
      });
      setCalculatedMetrics(metrics);
      
      // Load weather data for site coordinates
      if (metrics.coordinates && !weatherData) {
        loadWeatherData(metrics.coordinates.lat, metrics.coordinates.lon);
      }
    }
  }, [cameras, recentEvents, criticalAlerts, zoneminderStatus]);

  // Load site data from backend
  useEffect(() => {
    const loadSiteData = async () => {
      try {
        const sites = await backendAPI.sites.getAll();
        if (sites && sites.length > 0) {
          const site = sites[0];
          setCurrentSite({
            name: site.name || site.site_name || 'Construction Site Alpha',
            type: site.type || site.project_type || 'high_rise_building',
            progress: calculatedMetrics?.progress?.completion || 0,
            personnel: calculatedMetrics?.personnel?.count || 0,
            location: site.location || 'Seattle, WA',
            contractor: site.contractor || 'Construction Management LLC'
          });
        }
      } catch (error) {
        console.error('Error loading site data:', error);
        // Keep default values if API fails
      }
    };
    loadSiteData();
  }, [calculatedMetrics]);

  // Load real weather data
  const loadWeatherData = async (lat, lon) => {
    try {
      const weather = await weatherAPI.getCurrentWeather(lat, lon);
      const conditions = await weatherAPI.getWorkingConditions(lat, lon);
      
      setWeatherData({
        ...weather,
        workingConditions: conditions,
        displayTemp: `${weather.temperature}°F`,
        displayWind: weather.windSpeed || 'Light winds',
        displayCondition: weather.condition || 'Clear'
      });
    } catch (error) {
      console.error('Error loading weather data:', error);
    }
  };

  // Derived data from API responses and calculations
  const activeCameras = cameras?.cameras?.filter(cam => cam.status === 'online') || [];
  const totalCameras = cameras?.cameras?.length || 0;
  const activeAlerts = criticalAlerts?.events?.length || 0;
  const recentActivity = recentEvents?.events?.slice(0, 10) || [];
  const priorityAlerts = criticalAlerts?.events?.filter(event => 
    event.severity === 'critical' || event.severity === 'high'
  ).slice(0, 5) || [];

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
          {statsLoading || camerasLoading || alertsLoading ? (
            // Loading state
            Array(4).fill(0).map((_, i) => <LoadingCard key={i} />)
          ) : (
            <>
              <StatCard
                title="Active Personnel"
                value={calculatedMetrics?.personnel?.count || 0}
                subtitle={calculatedMetrics?.personnel?.activeZones ? 
                  `Active in ${calculatedMetrics.personnel.activeZones} zones` : 
                  'No recent activity detected'
                }
                icon={Users}
                color={theme.success[500]}
                onClick={() => navigate('/personnel')}
                badge={{ type: 'live', text: 'LIVE' }}
              />
              <StatCard
                title="Camera Status"
                value={`${activeCameras.length}/${totalCameras}`}
                subtitle={`${totalCameras - activeCameras.length} offline/maintenance`}
                icon={Camera}
                color={theme.primary[500]}
                onClick={() => navigate('/live-view')}
              />
              <StatCard
                title="Active Alerts"
                value={activeAlerts}
                subtitle={activeAlerts > 0 ? `${priorityAlerts.length} critical/high` : 'All clear'}
                icon={AlertTriangle}
                color={activeAlerts > 0 ? theme.danger[500] : theme.success[500]}
                onClick={() => navigate('/alert-center')}
                badge={activeAlerts > 0 ? { type: 'alert', text: 'ACTION NEEDED' } : null}
              />
              <StatCard
                title="Safety Score"
                value={calculatedMetrics?.safety ? `${calculatedMetrics.safety.score}/10` : '0/10'}
                subtitle={calculatedMetrics?.ppe ? 
                  `${calculatedMetrics.ppe.compliance}% PPE compliance` : 
                  'Calculating compliance...'
                }
                icon={Shield}
                color={theme.primary[500]}
                onClick={() => navigate('/ai-analytics')}
              />
            </>
          )}
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
              {eventsLoading ? (
                <div className="space-y-4">
                  {Array(5).fill(0).map((_, i) => (
                    <div key={i} className="animate-pulse flex items-center space-x-4 p-4 bg-gray-50 rounded-lg">
                      <div className="w-12 h-12 bg-gray-200 rounded-lg"></div>
                      <div className="flex-1">
                        <div className="h-4 bg-gray-200 rounded w-3/4 mb-2"></div>
                        <div className="h-3 bg-gray-200 rounded w-1/2"></div>
                      </div>
                    </div>
                  ))}
                </div>
              ) : recentActivity.length > 0 ? (
                <div className="space-y-4">
                  {recentActivity.map((event, index) => (
                    <div 
                      key={event.event_id || index} 
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
                            {formatters.formatDetectionType(event.detection_type)}
                          </h4>
                          <span className={`px-2 py-0.5 text-xs font-semibold rounded-full ${
                            event.confidence_score >= 0.9 ? 'bg-green-100 text-green-600' :
                            event.confidence_score >= 0.75 ? 'bg-yellow-100 text-yellow-600' :
                            'bg-red-100 text-red-600'
                          }`}>
                            {Math.round(event.confidence_score * 100)}% confidence
                          </span>
                        </div>
                        <div className="text-sm text-gray-600 mt-1">
                          Camera: {event.camera_id} • Location: {event.location}
                        </div>
                      </div>
                      <div className="text-sm text-gray-500">
                        {formatters.formatRelativeTime(event.timestamp)}
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="text-center py-8 text-gray-500">
                  <Activity className="w-12 h-12 mx-auto mb-4 opacity-50" />
                  <p>No recent activity detected</p>
                </div>
              )}
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
                    View All ({priorityAlerts.length})
                  </button>
                </div>
              </div>
              <div className="p-6 space-y-4">
                {alertsLoading ? (
                  Array(3).fill(0).map((_, i) => (
                    <div key={i} className="animate-pulse p-4 bg-gray-50 rounded-lg">
                      <div className="flex items-start space-x-3">
                        <div className="w-5 h-5 bg-gray-200 rounded"></div>
                        <div className="flex-1">
                          <div className="h-4 bg-gray-200 rounded w-3/4 mb-2"></div>
                          <div className="h-3 bg-gray-200 rounded w-1/2"></div>
                        </div>
                      </div>
                    </div>
                  ))
                ) : priorityAlerts.length > 0 ? (
                  priorityAlerts.slice(0, 3).map((event) => (
                    <AlertCard 
                      key={event.event_id} 
                      alert={{
                        id: event.event_id,
                        priority: event.severity,
                        title: formatters.formatDetectionType(event.detection_type),
                        message: event.description,
                        location: event.location,
                        timestamp: event.timestamp,
                        status: event.acknowledged ? 'acknowledged' : 'open'
                      }} 
                    />
                  ))
                ) : (
                  <div className="text-center py-4 text-gray-500">
                    <CheckCircle className="w-8 h-8 mx-auto mb-2 text-green-500" />
                    <p>No priority alerts</p>
                  </div>
                )}
              </div>
            </div>

            {/* Weather & Site Conditions */}
            <div className="bg-white rounded-xl shadow-sm border border-gray-100">
              <div className="p-6 border-b border-gray-100">
                <h2 className="text-lg font-semibold text-gray-900">Site Conditions</h2>
              </div>
              <div className="p-6">
                {weatherData ? (
                  <>
                    <div className="grid grid-cols-2 gap-4">
                      <div className="text-center">
                        <div className="flex items-center justify-center mb-2">
                          <Thermometer className="w-8 h-8 text-orange-500" />
                        </div>
                        <div className="text-2xl font-bold text-gray-900">{weatherData.displayTemp}</div>
                        <div className="text-sm text-gray-500">Temperature</div>
                      </div>
                      <div className="text-center">
                        <div className="flex items-center justify-center mb-2">
                          <Wind className="w-8 h-8 text-blue-500" />
                        </div>
                        <div className="text-2xl font-bold text-gray-900">{weatherData.displayWind}</div>
                        <div className="text-sm text-gray-500">Wind Speed</div>
                      </div>
                    </div>
                    <div className={`mt-4 p-3 rounded-lg text-center ${
                      weatherData.workingConditions?.status === 'optimal' ? 'bg-green-50' :
                      weatherData.workingConditions?.status === 'caution' ? 'bg-yellow-50' :
                      'bg-red-50'
                    }`}>
                      <div className="text-sm font-medium text-gray-900">{weatherData.displayCondition}</div>
                      <div className={`text-xs mt-1 ${
                        weatherData.workingConditions?.status === 'optimal' ? 'text-green-600' :
                        weatherData.workingConditions?.status === 'caution' ? 'text-yellow-600' :
                        'text-red-600'
                      }`}>
                        {weatherData.workingConditions?.message || 'Working conditions assessment'}
                      </div>
                    </div>
                  </>
                ) : (
                  <>
                    <div className="grid grid-cols-2 gap-4">
                      <div className="text-center">
                        <div className="flex items-center justify-center mb-2">
                          <Thermometer className="w-8 h-8 text-gray-300" />
                        </div>
                        <div className="animate-pulse bg-gray-200 h-8 w-16 mx-auto rounded"></div>
                        <div className="text-sm text-gray-500">Temperature</div>
                      </div>
                      <div className="text-center">
                        <div className="flex items-center justify-center mb-2">
                          <Wind className="w-8 h-8 text-gray-300" />
                        </div>
                        <div className="animate-pulse bg-gray-200 h-8 w-16 mx-auto rounded"></div>
                        <div className="text-sm text-gray-500">Wind Speed</div>
                      </div>
                    </div>
                    <div className="mt-4 p-3 bg-gray-50 rounded-lg text-center">
                      <div className="animate-pulse bg-gray-200 h-4 w-32 mx-auto rounded"></div>
                      <div className="text-xs text-gray-600 mt-1">Loading weather conditions...</div>
                    </div>
                  </>
                )}
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
                {recentActivity.map((event, index) => (
                  <div key={event.event_id || index} className="flex items-start space-x-4 p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors">
                    <div 
                      className="w-12 h-12 rounded-lg flex items-center justify-center flex-shrink-0"
                      style={{ backgroundColor: theme.primary[100] }}
                    >
                      <Activity className="w-6 h-6" style={{ color: theme.primary[500] }} />
                    </div>
                    <div className="flex-1">
                      <div className="flex items-center justify-between">
                        <h4 className="font-medium text-gray-900">
                          {formatters.formatDetectionType(event.detection_type)}
                        </h4>
                        <span className="text-xs text-gray-500">{formatters.formatRelativeTime(event.timestamp)}</span>
                      </div>
                      <p className="text-sm text-gray-600 mt-1">
                        Camera: {event.camera_id} • Location: {event.location} • Confidence: {Math.round(event.confidence_score * 100)}%
                      </p>
                      <div className="flex items-center space-x-4 mt-2">
                        <button 
                          onClick={() => navigate('/live-view')}
                          className="flex items-center space-x-1 text-sm text-blue-600 hover:text-blue-700"
                        >
                          <Eye className="w-3 h-3" />
                          <span>View Camera</span>
                        </button>
                        <button 
                          onClick={() => navigate(`/alert-center/${event.event_id}`)}
                          className="flex items-center space-x-1 text-sm text-gray-600 hover:text-gray-700"
                        >
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
                {priorityAlerts.map((event) => (
                  <div key={event.event_id} className="flex items-start space-x-4 p-4 bg-red-50 border border-red-200 rounded-lg">
                    <AlertTriangle className="w-5 h-5 text-red-600 mt-0.5 flex-shrink-0" />
                    <div className="flex-1">
                      <div className="flex items-center justify-between">
                        <h4 className="font-medium text-gray-900">{formatters.formatDetectionType(event.detection_type)}</h4>
                        <div className="flex items-center space-x-2">
                          <span className={`px-2 py-1 text-xs font-semibold rounded ${
                            event.severity === 'critical' ? 'bg-red-100 text-red-800' : 'bg-orange-100 text-orange-800'
                          }`}>
                            {formatters.formatSeverity(event.severity)}
                          </span>
                        </div>
                      </div>
                      <p className="text-sm text-gray-600 mt-1">{event.description}</p>
                      <div className="flex items-center justify-between mt-3">
                        <div className="text-xs text-gray-500">
                          {event.camera_id} • {event.location} • {formatters.formatDateTime(event.timestamp)}
                        </div>
                        <div className="flex items-center space-x-2">
                          <button 
                            onClick={() => navigate(`/alert-center/${event.event_id}`)}
                            className="px-3 py-1 text-sm bg-blue-600 text-white rounded hover:bg-blue-700 transition-colors"
                          >
                            Investigate
                          </button>
                          <button 
                            onClick={() => zoneminderAPI.events.acknowledge(event.event_id, 'current_user')}
                            className="px-3 py-1 text-sm bg-gray-100 text-gray-700 rounded hover:bg-gray-200 transition-colors"
                          >
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