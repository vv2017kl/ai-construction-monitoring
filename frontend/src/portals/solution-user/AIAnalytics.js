import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  BarChart3, TrendingUp, TrendingDown, Users, HardHat, 
  Car, Wrench, Shield, AlertTriangle, CheckCircle, 
  Calendar, Clock, Camera, Eye, Download, RefreshCw,
  Filter, Settings, Zap, Activity, Target, Cpu, 
  PieChart, LineChart, BarChart, MapPin, Layers, X,
  Play, Pause, Search, ArrowUpDown, FileText, FileSpreadsheet,
  Compare, Maximize2, Minimize2, RotateCcw, ChevronDown
} from 'lucide-react';
import { useTheme } from '../../context/ThemeContext';
import MainLayout from '../../components/shared/Layout/MainLayout';
import { mockAnalytics, mockSites, mockUser, mockDetections, mockCameras } from '../../data/mockData';

const AIAnalytics = () => {
  const navigate = useNavigate();
  const { theme } = useTheme();
  
  // State management
  const [timeRange, setTimeRange] = useState('24h'); // '1h', '24h', '7d', '30d'
  const [selectedMetric, setSelectedMetric] = useState('safety');
  const [showAdvancedFilters, setShowAdvancedFilters] = useState(false);
  const [chartType, setChartType] = useState('bar'); // 'bar', 'line', 'pie'
  const [selectedCamera, setSelectedCamera] = useState('all');
  const [selectedChartData, setSelectedChartData] = useState(null);
  const [showExportModal, setShowExportModal] = useState(false);
  const [exportFormat, setExportFormat] = useState('csv');
  const [realTimeEnabled, setRealTimeEnabled] = useState(true);
  const [comparisonMode, setComparisonMode] = useState(false);
  const [comparisonPeriod, setComparisonPeriod] = useState('prev_week');
  const [selectedDataPoints, setSelectedDataPoints] = useState(new Set());
  const [searchTerm, setSearchTerm] = useState('');
  const [sortBy, setSortBy] = useState('detections');
  const [sortOrder, setSortOrder] = useState('desc');
  
  const currentSite = mockSites.find(s => s.name === mockUser.currentSite) || mockSites[0];

  // Simulated analytics data based on time range
  const getAnalyticsData = () => {
    const baseData = mockAnalytics;
    const multiplier = timeRange === '1h' ? 0.1 : timeRange === '24h' ? 1 : timeRange === '7d' ? 7 : 30;
    
    return {
      aiPerformance: {
        ...baseData.aiPerformance,
        detectionsToday: Math.round(baseData.aiPerformance.detectionsToday * multiplier),
        processingTime: baseData.aiPerformance.processingTime + (multiplier * 2)
      },
      safetyMetrics: {
        ...baseData.safetyMetrics,
        incidentCount: Math.round(baseData.safetyMetrics.incidentCount * (multiplier / 7)),
        nearMissCount: Math.round(baseData.safetyMetrics.nearMissCount * (multiplier / 7))
      }
    };
  };

  const analytics = getAnalyticsData();

  // Enhanced Interactive Functions
  const handleChartDataClick = (dataPoint, chartName) => {
    setSelectedChartData({ ...dataPoint, chart: chartName });
  };

  const handleExportData = () => {
    const exportData = {
      metrics: analytics,
      chartData: chartData,
      cameras: chartData.cameraPerformance,
      timeRange: timeRange,
      exportDate: new Date().toISOString()
    };

    let dataStr, fileName, mimeType;
    
    if (exportFormat === 'csv') {
      // Convert to CSV format
      const csvRows = [];
      csvRows.push(['Metric', 'Value', 'Time Range']);
      csvRows.push(['AI Confidence', `${Math.round(analytics.aiPerformance.averageConfidence * 100)}%`, timeRange]);
      csvRows.push(['PPE Compliance', `${analytics.safetyMetrics.ppeComplianceRate}%`, timeRange]);
      csvRows.push(['Processing Speed', `${analytics.aiPerformance.processingTime}ms`, timeRange]);
      csvRows.push(['Safety Score', `${analytics.safetyMetrics.safetyScore}/10`, timeRange]);
      
      dataStr = csvRows.map(row => row.join(',')).join('\n');
      fileName = `ai_analytics_${timeRange}_${new Date().toISOString().split('T')[0]}.csv`;
      mimeType = 'text/csv';
    } else {
      dataStr = JSON.stringify(exportData, null, 2);
      fileName = `ai_analytics_${timeRange}_${new Date().toISOString().split('T')[0]}.json`;
      mimeType = 'application/json';
    }

    const dataUri = `data:${mimeType};charset=utf-8,${encodeURIComponent(dataStr)}`;
    const linkElement = document.createElement('a');
    linkElement.setAttribute('href', dataUri);
    linkElement.setAttribute('download', fileName);
    linkElement.click();
    
    setShowExportModal(false);
  };

  const handleTableSort = (column) => {
    if (sortBy === column) {
      setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc');
    } else {
      setSortBy(column);
      setSortOrder('desc');
    }
  };

  const filteredCameraData = chartData.cameraPerformance.filter(camera =>
    camera.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    camera.location.toLowerCase().includes(searchTerm.toLowerCase())
  ).sort((a, b) => {
    const aValue = a[sortBy];
    const bValue = b[sortBy];
    const multiplier = sortOrder === 'asc' ? 1 : -1;
    return (aValue < bValue ? -1 : aValue > bValue ? 1 : 0) * multiplier;
  });

  // Real-time updates simulation
  useEffect(() => {
    if (!realTimeEnabled) return;
    
    const interval = setInterval(() => {
      // Simulate real-time metric updates
      const randomChange = () => Math.floor(Math.random() * 3) - 1; // -1, 0, or 1
      
      // This would typically trigger a re-fetch of analytics data
      console.log('Real-time update:', new Date().toLocaleTimeString());
    }, 30000); // Update every 30 seconds

    return () => clearInterval(interval);
  }, [realTimeEnabled]);

  // Mock chart data
  const chartData = {
    hourlyDetections: [
      { time: '00:00', personnel: 12, violations: 1 },
      { time: '02:00', personnel: 8, violations: 0 },
      { time: '04:00', personnel: 15, violations: 2 },
      { time: '06:00', personnel: 28, violations: 1 },
      { time: '08:00', personnel: 45, violations: 3 },
      { time: '10:00', personnel: 42, violations: 2 },
      { time: '12:00', personnel: 38, violations: 1 },
      { time: '14:00', personnel: 41, violations: 4 },
      { time: '16:00', personnel: 35, violations: 2 },
      { time: '18:00', personnel: 22, violations: 1 },
      { time: '20:00', personnel: 15, violations: 0 },
      { time: '22:00', personnel: 8, violations: 0 }
    ],
    ppeCompliance: [
      { category: 'Hard Hats', compliance: 94, violations: 6 },
      { category: 'Safety Vests', compliance: 89, violations: 11 },
      { category: 'Steel Boots', compliance: 92, violations: 8 },
      { category: 'Safety Glasses', compliance: 86, violations: 14 },
      { category: 'Gloves', compliance: 78, violations: 22 }
    ],
    cameraPerformance: mockCameras.map(camera => ({
      ...camera,
      detections: Math.floor(Math.random() * 50) + 10,
      uptime: Math.floor(Math.random() * 10) + 90,
      accuracy: Math.floor(Math.random() * 15) + 85
    }))
  };

  const MetricCard = ({ title, value, change, icon: Icon, color, subtitle, onClick }) => (
    <div 
      className="bg-white rounded-xl p-6 shadow-sm border border-gray-100 hover:shadow-md transition-all duration-200 cursor-pointer"
      onClick={onClick}
    >
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-sm font-medium text-gray-600">{title}</h3>
          <p className="text-2xl font-bold text-gray-900 mt-2">{value}</p>
          {change && (
            <div className={`flex items-center mt-2 text-sm ${
              change.direction === 'up' ? 'text-green-600' : change.direction === 'down' ? 'text-red-600' : 'text-gray-600'
            }`}>
              {change.direction === 'up' && <TrendingUp className="w-4 h-4 mr-1" />}
              {change.direction === 'down' && <TrendingDown className="w-4 h-4 mr-1" />}
              <span>{change.value}</span>
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

  const ChartContainer = ({ title, children, actions }) => (
    <div className="bg-white rounded-xl shadow-sm border border-gray-100">
      <div className="p-6 border-b border-gray-100">
        <div className="flex items-center justify-between">
          <h2 className="text-lg font-semibold text-gray-900">{title}</h2>
          {actions && <div className="flex items-center space-x-2">{actions}</div>}
        </div>
      </div>
      <div className="p-6">{children}</div>
    </div>
  );

  const SimpleBarChart = ({ data, xKey, yKey, color }) => (
    <div className="space-y-3">
      {data.slice(0, 6).map((item, index) => (
        <div key={index} className="flex items-center space-x-3">
          <div className="w-16 text-sm text-gray-600">{item[xKey]}</div>
          <div className="flex-1">
            <div className="flex items-center justify-between mb-1">
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div 
                  className="h-2 rounded-full transition-all duration-500"
                  style={{ 
                    width: `${Math.min(100, (item[yKey] / Math.max(...data.map(d => d[yKey]))) * 100)}%`,
                    backgroundColor: color 
                  }}
                ></div>
              </div>
            </div>
          </div>
          <div className="w-12 text-sm font-medium text-gray-900">{item[yKey]}</div>
        </div>
      ))}
    </div>
  );

  const PPEComplianceChart = () => (
    <div className="space-y-4">
      {chartData.ppeCompliance.map((item, index) => (
        <div key={index} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
          <div className="flex items-center space-x-3">
            <HardHat className="w-5 h-5 text-gray-600" />
            <div>
              <p className="font-medium text-gray-900">{item.category}</p>
              <p className="text-sm text-gray-600">{item.violations} violations today</p>
            </div>
          </div>
          <div className="flex items-center space-x-3">
            <div className="w-24 bg-gray-200 rounded-full h-2">
              <div 
                className="h-2 rounded-full"
                style={{ 
                  width: `${item.compliance}%`,
                  backgroundColor: item.compliance >= 90 ? theme.success[500] : 
                                 item.compliance >= 80 ? theme.warning[500] : theme.danger[500]
                }}
              ></div>
            </div>
            <span className="text-lg font-bold text-gray-900">{item.compliance}%</span>
          </div>
        </div>
      ))}
    </div>
  );

  const CameraPerformanceTable = () => (
    <div className="overflow-x-auto">
      <table className="w-full">
        <thead>
          <tr className="border-b border-gray-200">
            <th className="text-left py-3 px-4 font-semibold text-gray-900">Camera</th>
            <th className="text-left py-3 px-4 font-semibold text-gray-900">Detections</th>
            <th className="text-left py-3 px-4 font-semibold text-gray-900">Accuracy</th>
            <th className="text-left py-3 px-4 font-semibold text-gray-900">Uptime</th>
            <th className="text-left py-3 px-4 font-semibold text-gray-900">Status</th>
          </tr>
        </thead>
        <tbody>
          {chartData.cameraPerformance.map((camera, index) => (
            <tr key={camera.id} className="border-b border-gray-100 hover:bg-gray-50">
              <td className="py-3 px-4">
                <div>
                  <p className="font-medium text-gray-900">{camera.name}</p>
                  <p className="text-sm text-gray-600">{camera.location}</p>
                </div>
              </td>
              <td className="py-3 px-4">
                <span className="text-lg font-bold text-gray-900">{camera.detections}</span>
                <span className="text-sm text-gray-500 ml-1">today</span>
              </td>
              <td className="py-3 px-4">
                <span className={`font-medium ${
                  camera.accuracy >= 90 ? 'text-green-600' : 
                  camera.accuracy >= 80 ? 'text-yellow-600' : 'text-red-600'
                }`}>
                  {camera.accuracy}%
                </span>
              </td>
              <td className="py-3 px-4">
                <span className={`font-medium ${
                  camera.uptime >= 95 ? 'text-green-600' : 
                  camera.uptime >= 90 ? 'text-yellow-600' : 'text-red-600'
                }`}>
                  {camera.uptime}%
                </span>
              </td>
              <td className="py-3 px-4">
                <span className={`px-2 py-1 text-xs font-semibold rounded-full ${
                  camera.status === 'online' ? 'bg-green-100 text-green-600' : 'bg-red-100 text-red-600'
                }`}>
                  {camera.status.toUpperCase()}
                </span>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );

  return (
    <MainLayout portal="solution-user">
      <div className="h-full flex flex-col">
        {/* Header */}
        <div className="bg-white border-b border-gray-200 px-6 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-xl font-bold text-gray-900">AI Analytics & Insights</h1>
              <div className="flex items-center space-x-2 text-sm text-gray-600">
                <MapPin className="w-3 h-3" />
                <span>{currentSite.name}</span>
                <span>•</span>
                <span>{analytics.aiPerformance.detectionsToday} detections today</span>
                <span>•</span>
                <span className="flex items-center space-x-1">
                  <Cpu className="w-3 h-3" />
                  <span>Model v{Math.floor(Math.random() * 3) + 8}.{Math.floor(Math.random() * 9) + 1}</span>
                </span>
              </div>
            </div>

            <div className="flex items-center space-x-4">
              {/* Time Range Selector */}
              <div className="flex items-center space-x-2 bg-gray-100 rounded-lg p-1">
                {['1h', '24h', '7d', '30d'].map((range) => (
                  <button
                    key={range}
                    onClick={() => setTimeRange(range)}
                    className={`px-3 py-1 text-sm rounded transition-colors ${
                      timeRange === range 
                        ? 'bg-white shadow-sm text-blue-600' 
                        : 'hover:bg-gray-200'
                    }`}
                  >
                    {range}
                  </button>
                ))}
              </div>

              <button className="flex items-center space-x-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
                <RefreshCw className="w-4 h-4" />
                <span>Refresh</span>
              </button>
            </div>
          </div>
        </div>

        {/* Main Content */}
        <div className="flex-1 overflow-auto p-6 space-y-6">
          {/* Key Metrics */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <MetricCard
              title="AI Confidence"
              value={`${Math.round(analytics.aiPerformance.averageConfidence * 100)}%`}
              change={{ direction: 'up', value: '+2.1%' }}
              icon={Target}
              color={theme.success[500]}
              subtitle="Average detection accuracy"
            />
            <MetricCard
              title="PPE Compliance"
              value={`${analytics.safetyMetrics.ppeComplianceRate}%`}
              change={{ direction: analytics.safetyMetrics.trendDirection === 'up' ? 'up' : 'down', value: analytics.safetyMetrics.lastWeekComparison }}
              icon={Shield}
              color={analytics.safetyMetrics.ppeComplianceRate >= 90 ? theme.success[500] : theme.warning[500]}
              subtitle="Site-wide compliance rate"
            />
            <MetricCard
              title="Processing Speed"
              value={`${analytics.aiPerformance.processingTime}ms`}
              change={{ direction: 'down', value: '-12ms' }}
              icon={Zap}
              color={theme.primary[500]}
              subtitle="Average per detection"
            />
            <MetricCard
              title="Safety Score"
              value={`${analytics.safetyMetrics.safetyScore}/10`}
              change={{ direction: 'up', value: '+0.3' }}
              icon={CheckCircle}
              color={theme.success[500]}
              subtitle="Overall site safety rating"
            />
          </div>

          {/* Charts Grid */}
          <div className="grid grid-cols-1 xl:grid-cols-2 gap-6">
            {/* Personnel Detection Trends */}
            <ChartContainer 
              title="Personnel Detection Trends"
              actions={[
                <button key="export" className="text-gray-600 hover:text-gray-800">
                  <Download className="w-4 h-4" />
                </button>
              ]}
            >
              <div className="mb-4">
                <p className="text-sm text-gray-600">Hourly personnel count and safety violations</p>
              </div>
              <SimpleBarChart 
                data={chartData.hourlyDetections} 
                xKey="time" 
                yKey="personnel" 
                color={theme.primary[500]} 
              />
            </ChartContainer>

            {/* PPE Compliance Breakdown */}
            <ChartContainer title="PPE Compliance Breakdown">
              <div className="mb-4">
                <p className="text-sm text-gray-600">Compliance rates by equipment type</p>
              </div>
              <PPEComplianceChart />
            </ChartContainer>
          </div>

          {/* AI Performance Metrics */}
          <div className="grid grid-cols-1 xl:grid-cols-3 gap-6">
            {/* Model Performance */}
            <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Model Performance</h3>
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <span className="text-gray-600">Detection Accuracy</span>
                  <span className="font-bold text-green-600">{Math.round(analytics.aiPerformance.modelAccuracy * 100)}%</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-gray-600">False Positive Rate</span>
                  <span className="font-bold text-yellow-600">{(analytics.aiPerformance.falsePositiveRate * 100).toFixed(1)}%</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-gray-600">Detections Today</span>
                  <span className="font-bold text-blue-600">{analytics.aiPerformance.detectionsToday}</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-gray-600">Last Model Update</span>
                  <span className="font-bold text-gray-900">
                    {new Date(analytics.aiPerformance.lastModelUpdate).toLocaleDateString()}
                  </span>
                </div>
              </div>
            </div>

            {/* Real-time Alerts */}
            <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Safety Incidents</h3>
              <div className="space-y-4">
                <div className="text-center p-4 bg-red-50 rounded-lg">
                  <AlertTriangle className="w-8 h-8 mx-auto mb-2 text-red-600" />
                  <div className="text-2xl font-bold text-red-600">{analytics.safetyMetrics.incidentCount}</div>
                  <div className="text-sm text-gray-600">Incidents This Period</div>
                </div>
                <div className="text-center p-4 bg-yellow-50 rounded-lg">
                  <Eye className="w-8 h-8 mx-auto mb-2 text-yellow-600" />
                  <div className="text-2xl font-bold text-yellow-600">{analytics.safetyMetrics.nearMissCount}</div>
                  <div className="text-sm text-gray-600">Near Misses</div>
                </div>
              </div>
            </div>

            {/* Quick Actions */}
            <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Quick Actions</h3>
              <div className="space-y-3">
                <button
                  onClick={() => navigate('/live-view')}
                  className="w-full flex items-center space-x-3 p-3 text-left bg-blue-50 hover:bg-blue-100 rounded-lg transition-colors"
                >
                  <Camera className="w-5 h-5 text-blue-600" />
                  <div>
                    <div className="font-medium text-blue-900">Live Monitoring</div>
                    <div className="text-xs text-blue-600">View real-time detections</div>
                  </div>
                </button>
                
                <button
                  onClick={() => navigate('/alert-center')}
                  className="w-full flex items-center space-x-3 p-3 text-left bg-red-50 hover:bg-red-100 rounded-lg transition-colors"
                >
                  <AlertTriangle className="w-5 h-5 text-red-600" />
                  <div>
                    <div className="font-medium text-red-900">Alert Center</div>
                    <div className="text-xs text-red-600">Manage safety alerts</div>
                  </div>
                </button>
                
                <button className="w-full flex items-center space-x-3 p-3 text-left bg-green-50 hover:bg-green-100 rounded-lg transition-colors">
                  <Download className="w-5 h-5 text-green-600" />
                  <div>
                    <div className="font-medium text-green-900">Export Report</div>
                    <div className="text-xs text-green-600">Generate analytics report</div>
                  </div>
                </button>
              </div>
            </div>
          </div>

          {/* Camera Performance Table */}
          <ChartContainer title="Camera Performance Analytics">
            <div className="mb-4">
              <p className="text-sm text-gray-600">Individual camera performance metrics and detection statistics</p>
            </div>
            <CameraPerformanceTable />
          </ChartContainer>
        </div>
      </div>
    </MainLayout>
  );
};

export default AIAnalytics;