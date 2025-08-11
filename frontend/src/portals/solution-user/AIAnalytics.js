import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  BarChart3, TrendingUp, TrendingDown, Users, HardHat, 
  Car, Wrench, Shield, AlertTriangle, CheckCircle, 
  Calendar, Clock, Camera, Eye, Download, RefreshCw,
  Filter, Settings, Zap, Activity, Target, Cpu, 
  PieChart, LineChart, BarChart, MapPin, Layers, X,
  Play, Pause, Search, ArrowUpDown, FileText, FileSpreadsheet,
  GitCompare, Maximize2, Minimize2, RotateCcw, ChevronDown
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
    cameraPerformance: [
      { id: 'cam001', name: 'Camera 01', location: 'Main Entrance', detections: 156, accuracy: 94, uptime: 99.2, status: 'online' },
      { id: 'cam002', name: 'Camera 02', location: 'Construction Zone A', detections: 203, accuracy: 91, uptime: 98.7, status: 'online' },
      { id: 'cam003', name: 'Camera 03', location: 'Equipment Storage', detections: 89, accuracy: 96, uptime: 99.8, status: 'online' },
      { id: 'cam004', name: 'Camera 04', location: 'Safety Office', detections: 45, accuracy: 98, uptime: 97.3, status: 'online' },
      { id: 'cam005', name: 'Camera 05', location: 'Loading Dock', detections: 178, accuracy: 88, uptime: 95.1, status: 'maintenance' },
      { id: 'cam006', name: 'Camera 06', location: 'Break Area', detections: 67, accuracy: 93, uptime: 99.5, status: 'online' }
    ],
    ppeCompliance: [
      { category: 'Hard Hat', violations: 12, compliance: 94 },
      { category: 'Safety Vest', violations: 8, compliance: 96 },
      { category: 'Safety Boots', violations: 5, compliance: 98 },
      { category: 'Gloves', violations: 15, compliance: 92 },
      { category: 'Eye Protection', violations: 3, compliance: 99 }
    ]
  };

  // Filtered and sorted camera data (calculated after chartData is available)
  const filteredCameraData = chartData.cameraPerformance.filter(camera => {
    const matchesSearch = camera.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         camera.location.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesCamera = selectedCamera === 'all' || camera.id === selectedCamera;
    return matchesSearch && matchesCamera;
  }).sort((a, b) => {
    const aValue = a[sortBy];
    const bValue = b[sortBy];
    const multiplier = sortOrder === 'asc' ? 1 : -1;
    return (aValue < bValue ? -1 : aValue > bValue ? 1 : 0) * multiplier;
  });

  const MetricCard = ({ title, value, change, icon: Icon, color, subtitle, onClick, isSelected = false, showTrend = false }) => (
    <div 
      className={`bg-white rounded-xl p-6 shadow-sm border transition-all duration-200 cursor-pointer ${
        isSelected ? 'border-blue-500 ring-2 ring-blue-500/20' : 'border-gray-100 hover:shadow-md'
      }`}
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
    <div className="space-y-4">
      {/* Table Controls */}
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
            <input
              type="text"
              placeholder="Search cameras..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="pl-10 pr-4 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:border-transparent"
              style={{ '--tw-ring-color': theme.primary[500] + '40' }}
            />
          </div>
          <select
            value={selectedCamera}
            onChange={(e) => setSelectedCamera(e.target.value)}
            className="px-3 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:border-transparent"
          >
            <option value="all">All Cameras</option>
            {chartData.cameraPerformance.map(camera => (
              <option key={camera.id} value={camera.id}>{camera.name}</option>
            ))}
          </select>
        </div>
        <div className="text-sm text-gray-600">
          Showing {filteredCameraData.length} of {chartData.cameraPerformance.length} cameras
        </div>
      </div>

      {/* Enhanced Table */}
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead className="bg-gray-50 border-b">
            <tr>
              <th 
                className="text-left py-3 px-4 font-semibold text-gray-900 cursor-pointer hover:bg-gray-100"
                onClick={() => handleTableSort('name')}
              >
                <div className="flex items-center space-x-1">
                  <span>Camera</span>
                  <ArrowUpDown className="w-3 h-3" />
                </div>
              </th>
              <th 
                className="text-left py-3 px-4 font-semibold text-gray-900 cursor-pointer hover:bg-gray-100"
                onClick={() => handleTableSort('location')}
              >
                <div className="flex items-center space-x-1">
                  <span>Location</span>
                  <ArrowUpDown className="w-3 h-3" />
                </div>
              </th>
              <th 
                className="text-left py-3 px-4 font-semibold text-gray-900 cursor-pointer hover:bg-gray-100"
                onClick={() => handleTableSort('detections')}
              >
                <div className="flex items-center space-x-1">
                  <span>Detections</span>
                  <ArrowUpDown className="w-3 h-3" />
                </div>
              </th>
              <th 
                className="text-left py-3 px-4 font-semibold text-gray-900 cursor-pointer hover:bg-gray-100"
                onClick={() => handleTableSort('accuracy')}
              >
                <div className="flex items-center space-x-1">
                  <span>Accuracy</span>
                  <ArrowUpDown className="w-3 h-3" />
                </div>
              </th>
              <th 
                className="text-left py-3 px-4 font-semibold text-gray-900 cursor-pointer hover:bg-gray-100"
                onClick={() => handleTableSort('uptime')}
              >
                <div className="flex items-center space-x-1">
                  <span>Uptime</span>
                  <ArrowUpDown className="w-3 h-3" />
                </div>
              </th>
              <th className="text-left py-3 px-4 font-semibold text-gray-900">Status</th>
              <th className="text-left py-3 px-4 font-semibold text-gray-900">Actions</th>
            </tr>
          </thead>
          <tbody>
            {filteredCameraData.map((camera, index) => (
              <tr key={camera.id} className="border-b border-gray-100 hover:bg-gray-50">
                <td className="py-3 px-4">
                  <div className="flex items-center space-x-3">
                    <div className="w-2 h-2 rounded-full bg-green-500"></div>
                    <div>
                      <p className="font-medium text-gray-900">{camera.name}</p>
                      <p className="text-xs text-gray-500">ID: {camera.id}</p>
                    </div>
                  </div>
                </td>
                <td className="py-3 px-4">
                  <div className="flex items-center space-x-2">
                    <MapPin className="w-4 h-4 text-gray-400" />
                    <span className="text-gray-900">{camera.location}</span>
                  </div>
                </td>
                <td className="py-3 px-4">
                  <div>
                    <span className="text-lg font-bold text-gray-900">{camera.detections}</span>
                    <span className="text-sm text-gray-500 ml-1">today</span>
                  </div>
                </td>
                <td className="py-3 px-4">
                  <div className="flex items-center space-x-2">
                    <div className="w-12 bg-gray-200 rounded-full h-1.5">
                      <div 
                        className="h-1.5 rounded-full"
                        style={{ 
                          width: `${camera.accuracy}%`,
                          backgroundColor: camera.accuracy >= 90 ? theme.success[500] : 
                                         camera.accuracy >= 80 ? theme.warning[500] : theme.danger[500]
                        }}
                      ></div>
                    </div>
                    <span className={`font-medium text-sm ${
                      camera.accuracy >= 90 ? 'text-green-600' : 
                      camera.accuracy >= 80 ? 'text-yellow-600' : 'text-red-600'
                    }`}>
                      {camera.accuracy}%
                    </span>
                  </div>
                </td>
                <td className="py-3 px-4">
                  <div className="flex items-center space-x-2">
                    <div className="w-12 bg-gray-200 rounded-full h-1.5">
                      <div 
                        className="h-1.5 rounded-full"
                        style={{ 
                          width: `${camera.uptime}%`,
                          backgroundColor: camera.uptime >= 95 ? theme.success[500] : 
                                         camera.uptime >= 90 ? theme.warning[500] : theme.danger[500]
                        }}
                      ></div>
                    </div>
                    <span className={`font-medium text-sm ${
                      camera.uptime >= 95 ? 'text-green-600' : 
                      camera.uptime >= 90 ? 'text-yellow-600' : 'text-red-600'
                    }`}>
                      {camera.uptime}%
                    </span>
                  </div>
                </td>
                <td className="py-3 px-4">
                  <div className="flex items-center space-x-2">
                    <div className={`w-2 h-2 rounded-full ${
                      camera.status === 'online' ? 'bg-green-500' : 'bg-red-500'
                    }`}></div>
                    <span className={`text-sm font-medium ${
                      camera.status === 'online' ? 'text-green-600' : 'text-red-600'
                    }`}>
                      {camera.status.charAt(0).toUpperCase() + camera.status.slice(1)}
                    </span>
                  </div>
                </td>
                <td className="py-3 px-4">
                  <div className="flex items-center space-x-2">
                    <button
                      onClick={() => navigate(`/camera/${camera.id}`)}
                      className="p-1 text-gray-400 hover:text-blue-600 transition-colors"
                      title="View Camera"
                    >
                      <Eye className="w-4 h-4" />
                    </button>
                    <button
                      className="p-1 text-gray-400 hover:text-gray-600 transition-colors"
                      title="Camera Settings"
                    >
                      <Settings className="w-4 h-4" />
                    </button>
                    <button
                      className="p-1 text-gray-400 hover:text-red-600 transition-colors"
                      title="Download Footage"
                    >
                      <Download className="w-4 h-4" />
                    </button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
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
              {/* Chart Type Selector */}
              <div className="flex items-center space-x-2 bg-gray-100 rounded-lg p-1">
                <button
                  onClick={() => setChartType('bar')}
                  className={`p-2 rounded transition-colors ${
                    chartType === 'bar' ? 'bg-white shadow-sm text-blue-600' : 'hover:bg-gray-200'
                  }`}
                  title="Bar Chart"
                >
                  <BarChart className="w-3 h-3" />
                </button>
                <button
                  onClick={() => setChartType('line')}
                  className={`p-2 rounded transition-colors ${
                    chartType === 'line' ? 'bg-white shadow-sm text-blue-600' : 'hover:bg-gray-200'
                  }`}
                  title="Line Chart"
                >
                  <LineChart className="w-3 h-3" />
                </button>
                <button
                  onClick={() => setChartType('pie')}
                  className={`p-2 rounded transition-colors ${
                    chartType === 'pie' ? 'bg-white shadow-sm text-blue-600' : 'hover:bg-gray-200'
                  }`}
                  title="Pie Chart"
                >
                  <PieChart className="w-3 h-3" />
                </button>
              </div>

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

              {/* Comparison Mode Toggle */}
              <button
                onClick={() => setComparisonMode(!comparisonMode)}
                className={`flex items-center space-x-2 px-3 py-2 rounded-lg transition-colors ${
                  comparisonMode ? 'bg-purple-100 text-purple-700' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                <GitCompare className="w-4 h-4" />
                <span>Compare</span>
              </button>

              {/* Real-time Toggle */}
              <button
                onClick={() => setRealTimeEnabled(!realTimeEnabled)}
                className={`flex items-center space-x-2 px-3 py-2 rounded-lg transition-colors ${
                  realTimeEnabled ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                {realTimeEnabled ? <Play className="w-4 h-4" /> : <Pause className="w-4 h-4" />}
                <span>Live</span>
              </button>

              {/* Export Button */}
              <button
                onClick={() => setShowExportModal(true)}
                className="flex items-center space-x-2 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
              >
                <Download className="w-4 h-4" />
                <span>Export</span>
              </button>

              <button 
                onClick={() => window.location.reload()}
                className="flex items-center space-x-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
              >
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

      {/* Export Modal */}
      {showExportModal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-lg max-w-md w-full p-6">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-gray-900">Export Analytics Data</h3>
              <button
                onClick={() => setShowExportModal(false)}
                className="p-2 hover:bg-gray-100 rounded-lg"
              >
                <X className="w-5 h-5" />
              </button>
            </div>
            
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Export Format</label>
                <div className="space-y-2">
                  <label className="flex items-center space-x-3">
                    <input
                      type="radio"
                      name="exportFormat"
                      value="csv"
                      checked={exportFormat === 'csv'}
                      onChange={(e) => setExportFormat(e.target.value)}
                      className="w-4 h-4 text-blue-600 border-gray-300"
                    />
                    <div className="flex items-center space-x-2">
                      <FileSpreadsheet className="w-4 h-4 text-green-600" />
                      <span>CSV (Excel compatible)</span>
                    </div>
                  </label>
                  <label className="flex items-center space-x-3">
                    <input
                      type="radio"
                      name="exportFormat"
                      value="json"
                      checked={exportFormat === 'json'}
                      onChange={(e) => setExportFormat(e.target.value)}
                      className="w-4 h-4 text-blue-600 border-gray-300"
                    />
                    <div className="flex items-center space-x-2">
                      <FileText className="w-4 h-4 text-blue-600" />
                      <span>JSON (Raw data)</span>
                    </div>
                  </label>
                </div>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Time Range</label>
                <div className="p-3 bg-gray-50 rounded-lg">
                  <span className="text-sm text-gray-900">Current: {timeRange}</span>
                </div>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Data Preview</label>
                <div className="p-3 bg-gray-50 rounded-lg max-h-32 overflow-y-auto">
                  <div className="text-xs text-gray-600">
                    • AI Performance Metrics<br/>
                    • Safety Compliance Data<br/>
                    • Camera Performance Statistics<br/>
                    • Chart Data Points<br/>
                    • Time Series Information
                  </div>
                </div>
              </div>
            </div>
            
            <div className="flex justify-end space-x-3 mt-6">
              <button
                onClick={() => setShowExportModal(false)}
                className="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors"
              >
                Cancel
              </button>
              <button
                onClick={handleExportData}
                className="flex items-center space-x-2 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
              >
                <Download className="w-4 h-4" />
                <span>Export Data</span>
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Chart Data Detail Modal */}
      {selectedChartData && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-lg max-w-lg w-full p-6">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-gray-900">Data Point Details</h3>
              <button
                onClick={() => setSelectedChartData(null)}
                className="p-2 hover:bg-gray-100 rounded-lg"
              >
                <X className="w-5 h-5" />
              </button>
            </div>
            
            <div className="space-y-4">
              <div className="flex items-center space-x-3 p-3 bg-blue-50 rounded-lg">
                <BarChart3 className="w-5 h-5 text-blue-600" />
                <div>
                  <p className="font-medium text-blue-900">Chart: {selectedChartData.chart}</p>
                  <p className="text-sm text-blue-600">Interactive data exploration</p>
                </div>
              </div>
              
              <div className="grid grid-cols-2 gap-4">
                {Object.entries(selectedChartData).filter(([key]) => key !== 'chart').map(([key, value]) => (
                  <div key={key} className="p-3 bg-gray-50 rounded-lg">
                    <p className="text-sm text-gray-600 capitalize">{key.replace(/([A-Z])/g, ' $1')}</p>
                    <p className="text-lg font-semibold text-gray-900">{value}</p>
                  </div>
                ))}
              </div>
              
              <div className="flex items-center space-x-2 p-3 bg-yellow-50 rounded-lg">
                <Target className="w-4 h-4 text-yellow-600" />
                <span className="text-sm text-yellow-700">
                  Click on chart elements to explore detailed analytics
                </span>
              </div>
            </div>
            
            <div className="flex justify-end space-x-3 mt-6">
              <button
                onClick={() => navigate('/live-view')}
                className="flex items-center space-x-2 px-4 py-2 bg-blue-100 text-blue-700 rounded-lg hover:bg-blue-200 transition-colors"
              >
                <Eye className="w-4 h-4" />
                <span>View Live</span>
              </button>
              <button
                onClick={() => setSelectedChartData(null)}
                className="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors"
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}
    </MainLayout>
  );
};

export default AIAnalytics;