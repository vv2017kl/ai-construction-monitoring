import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  Navigation, Calendar, Clock, Camera, MapPin, Play, Pause,
  SkipBack, SkipForward, RotateCcw, RotateCw, ZoomIn, ZoomOut,
  Maximize2, Download, Share2, Settings, Layers, Route,
  ChevronLeft, ChevronRight, Split, Columns2, Grid3X3,
  Compass, Target, Crosshair, Map, Eye, EyeOff, Shuffle,
  ArrowLeftRight, ArrowUpDown, Move, Locate, RefreshCw,
  BarChart3, TrendingUp, AlertTriangle, CheckCircle, Info
} from 'lucide-react';
import { useTheme } from '../../context/ThemeContext';
import MainLayout from '../../components/shared/Layout/MainLayout';
import { mockSites, mockUser, mockCameras } from '../../data/mockData';

const StreetViewComparison = () => {
  const navigate = useNavigate();
  const { theme } = useTheme();
  
  // State management
  const [comparisonSessions] = useState([
    {
      id: 'session1',
      label: 'Before (Week 1)',
      date: new Date(Date.now() - 14 * 24 * 60 * 60 * 1000), // 2 weeks ago
      time: '14:00',
      color: '#3b82f6',
      location: { x: 45, y: 55, heading: 90 }
    },
    {
      id: 'session2',
      label: 'After (Current)',
      date: new Date(Date.now() - 24 * 60 * 60 * 1000), // Yesterday
      time: '14:00',
      color: '#ef4444',
      location: { x: 45, y: 55, heading: 90 }
    }
  ]);
  
  const [viewMode, setViewMode] = useState('side-by-side'); // 'side-by-side', 'split-screen', 'overlay', 'difference'
  const [syncNavigation, setSyncNavigation] = useState(true);
  const [selectedLocation, setSelectedLocation] = useState('zone-a');
  const [overlayOpacity, setOverlayOpacity] = useState(0.5);
  const [showAnalysis, setShowAnalysis] = useState(true);
  const [analysisType, setAnalysisType] = useState('changes'); // 'changes', 'progress', 'safety'
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentTime, setCurrentTime] = useState(0);
  const [zoomLevel, setZoomLevel] = useState(1);

  const currentSite = mockSites.find(s => s.name === mockUser.currentSite) || mockSites[0];

  // Mock comparison locations
  const comparisonLocations = [
    {
      id: 'zone-a',
      name: 'Zone A - Foundation',
      description: 'Main foundation work area',
      coordinates: { x: 45, y: 55 },
      hasChanges: true,
      changeCount: 8
    },
    {
      id: 'zone-b',
      name: 'Zone B - Steel Frame',
      description: 'Steel framework construction',
      coordinates: { x: 60, y: 70 },
      hasChanges: true,
      changeCount: 12
    },
    {
      id: 'entrance',
      name: 'Main Entrance',
      description: 'Site entrance and security',
      coordinates: { x: 15, y: 30 },
      hasChanges: false,
      changeCount: 2
    },
    {
      id: 'equipment',
      name: 'Equipment Yard',
      description: 'Heavy equipment storage',
      coordinates: { x: 70, y: 35 },
      hasChanges: true,
      changeCount: 15
    }
  ];

  // Mock detected changes
  const detectedChanges = [
    {
      id: 1,
      type: 'construction_progress',
      severity: 'high',
      description: 'Foundation concrete pouring completed',
      location: 'Zone A - Foundation',
      confidence: 95,
      impact: 'Significant construction progress visible'
    },
    {
      id: 2,
      type: 'equipment_addition',
      severity: 'medium',
      description: 'New crane installed',
      location: 'Zone B - Steel Frame',
      confidence: 87,
      impact: 'Major equipment change affects site layout'
    },
    {
      id: 3,
      type: 'safety_improvement',
      severity: 'low',
      description: 'Additional safety barriers installed',
      location: 'Main Entrance',
      confidence: 92,
      impact: 'Enhanced safety measures implemented'
    },
    {
      id: 4,
      type: 'personnel_increase',
      severity: 'medium',
      description: 'Workforce increased by 40%',
      location: 'Multiple zones',
      confidence: 89,
      impact: 'Higher activity levels observed'
    }
  ];

  // Mock analysis metrics
  const analysisMetrics = {
    overallProgress: 78,
    constructionGrowth: '+34%',
    equipmentChanges: 6,
    safetyImprovements: 4,
    personnelVariation: '+40%',
    timespan: '14 days'
  };

  const getCurrentLocationData = () => {
    return comparisonLocations.find(loc => loc.id === selectedLocation);
  };

  const getChangeIcon = (type) => {
    switch (type) {
      case 'construction_progress': return TrendingUp;
      case 'equipment_addition': return Settings;
      case 'safety_improvement': return CheckCircle;
      case 'personnel_increase': return Navigation;
      default: return Info;
    }
  };

  const getChangeColor = (type) => {
    switch (type) {
      case 'construction_progress': return 'text-green-600';
      case 'equipment_addition': return 'text-blue-600';
      case 'safety_improvement': return 'text-purple-600';
      case 'personnel_increase': return 'text-orange-600';
      default: return 'text-gray-600';
    }
  };

  const getSeverityColor = (severity) => {
    switch (severity) {
      case 'high': return 'bg-red-100 text-red-800';
      case 'medium': return 'bg-yellow-100 text-yellow-800';
      case 'low': return 'bg-green-100 text-green-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const StreetViewPanel = ({ session, position }) => (
    <div className={`relative bg-black rounded-lg overflow-hidden ${position === 'right' ? 'ml-2' : ''}`}>
      {/* Mock Street View Display */}
      <div className="aspect-video flex items-center justify-center">
        <div className="text-center text-white">
          <Camera className="w-12 h-12 mx-auto mb-3 opacity-50" />
          <h3 className="text-lg font-bold mb-2">{session.label}</h3>
          <div className="text-sm text-gray-300 space-y-1">
            <p>{getCurrentLocationData()?.name}</p>
            <p>{session.date.toLocaleDateString()} at {session.time}</p>
            <div className="mt-3">
              <div 
                className="w-4 h-4 mx-auto rounded"
                style={{ backgroundColor: session.color }}
              ></div>
            </div>
          </div>
        </div>
      </div>

      {/* Progress indicator for construction progress */}
      {session.id === 'session2' && (
        <div className="absolute top-4 left-4 bg-green-600/80 text-white px-3 py-1 rounded-lg text-sm">
          Progress: +34%
        </div>
      )}

      {/* Change indicators */}
      {getCurrentLocationData()?.hasChanges && (
        <div className="absolute bottom-4 left-4 bg-blue-600/80 text-white px-3 py-1 rounded-lg text-sm flex items-center space-x-1">
          <AlertTriangle className="w-3 h-3" />
          <span>{getCurrentLocationData()?.changeCount} changes</span>
        </div>
      )}

      {/* View Controls */}
      <div className="absolute top-4 right-4 flex space-x-2">
        <button className="p-2 bg-black/50 hover:bg-black/70 text-white rounded-lg transition-colors">
          <ZoomIn className="w-4 h-4" />
        </button>
        <button className="p-2 bg-black/50 hover:bg-black/70 text-white rounded-lg transition-colors">
          <RotateCw className="w-4 h-4" />
        </button>
        <button className="p-2 bg-black/50 hover:bg-black/70 text-white rounded-lg transition-colors">
          <Maximize2 className="w-4 h-4" />
        </button>
      </div>

      {/* Session Color Indicator */}
      <div 
        className="absolute bottom-4 right-4 w-6 h-6 rounded-full border-2 border-white"
        style={{ backgroundColor: session.color }}
      ></div>
    </div>
  );

  const ChangeAnalysisItem = ({ change }) => {
    const Icon = getChangeIcon(change.type);
    
    return (
      <div className="p-4 bg-white rounded-lg border border-gray-200 hover:shadow-sm transition-shadow">
        <div className="flex items-start space-x-3">
          <div className={`p-2 rounded-full ${change.severity === 'high' ? 'bg-red-100' : change.severity === 'medium' ? 'bg-yellow-100' : 'bg-green-100'}`}>
            <Icon className={`w-5 h-5 ${getChangeColor(change.type)}`} />
          </div>
          
          <div className="flex-1">
            <div className="flex items-center justify-between mb-2">
              <h4 className="font-medium text-gray-900">{change.description}</h4>
              <span className={`px-2 py-1 text-xs font-semibold rounded-full ${getSeverityColor(change.severity)}`}>
                {change.severity.toUpperCase()}
              </span>
            </div>
            
            <p className="text-sm text-gray-600 mb-2">{change.impact}</p>
            
            <div className="flex items-center justify-between text-xs text-gray-500">
              <span>{change.location}</span>
              <div className="flex items-center space-x-2">
                <span>Confidence: {change.confidence}%</span>
                <div className="w-16 bg-gray-200 rounded-full h-2">
                  <div 
                    className="bg-blue-600 h-2 rounded-full"
                    style={{ width: `${change.confidence}%` }}
                  ></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  };

  const AnalysisMetrics = () => (
    <div className="grid grid-cols-2 gap-4">
      <div className="bg-white p-4 rounded-lg border border-gray-200">
        <div className="text-center">
          <div className="text-2xl font-bold text-green-600">{analysisMetrics.overallProgress}%</div>
          <div className="text-sm text-gray-600">Overall Progress</div>
        </div>
      </div>
      
      <div className="bg-white p-4 rounded-lg border border-gray-200">
        <div className="text-center">
          <div className="text-2xl font-bold text-blue-600">{analysisMetrics.constructionGrowth}</div>
          <div className="text-sm text-gray-600">Construction Growth</div>
        </div>
      </div>
      
      <div className="bg-white p-4 rounded-lg border border-gray-200">
        <div className="text-center">
          <div className="text-2xl font-bold text-purple-600">{analysisMetrics.equipmentChanges}</div>
          <div className="text-sm text-gray-600">Equipment Changes</div>
        </div>
      </div>
      
      <div className="bg-white p-4 rounded-lg border border-gray-200">
        <div className="text-center">
          <div className="text-2xl font-bold text-orange-600">{analysisMetrics.personnelVariation}</div>
          <div className="text-sm text-gray-600">Personnel Change</div>
        </div>
      </div>
    </div>
  );

  return (
    <MainLayout portal="solution-user">
      <div className="h-full flex flex-col bg-gray-100">
        {/* Header */}
        <div className="bg-white border-b border-gray-200 px-6 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-xl font-bold text-gray-900">Street View Comparison</h1>
              <div className="flex items-center space-x-2 text-sm text-gray-600">
                <Calendar className="w-3 h-3" />
                <span>Comparing {analysisMetrics.timespan} of progress</span>
                <span>•</span>
                <Locate className="w-3 h-3" />
                <span>{getCurrentLocationData()?.name}</span>
                <span>•</span>
                <BarChart3 className="w-3 h-3" />
                <span>{detectedChanges.length} changes detected</span>
              </div>
            </div>

            <div className="flex items-center space-x-4">
              {/* View Mode Selector */}
              <div className="flex items-center space-x-2 bg-gray-100 rounded-lg p-1">
                {[
                  { key: 'side-by-side', label: 'Side by Side', icon: Columns2 },
                  { key: 'split-screen', label: 'Split', icon: Split },
                  { key: 'overlay', label: 'Overlay', icon: Layers },
                  { key: 'difference', label: 'Difference', icon: BarChart3 }
                ].map(({ key, label, icon: Icon }) => (
                  <button
                    key={key}
                    onClick={() => setViewMode(key)}
                    className={`flex items-center space-x-1 px-3 py-1 text-sm rounded transition-colors ${
                      viewMode === key 
                        ? 'bg-white shadow-sm text-blue-600' 
                        : 'hover:bg-gray-200'
                    }`}
                  >
                    <Icon className="w-4 h-4" />
                    <span>{label}</span>
                  </button>
                ))}
              </div>

              <button className="flex items-center space-x-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
                <Download className="w-4 h-4" />
                <span>Export Comparison</span>
              </button>
            </div>
          </div>
        </div>

        {/* Configuration Panel */}
        <div className="bg-white border-b border-gray-200 px-6 py-4">
          <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
            {/* Location Selector */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Location</label>
              <select
                value={selectedLocation}
                onChange={(e) => setSelectedLocation(e.target.value)}
                className="w-full px-3 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:border-transparent text-sm"
              >
                {comparisonLocations.map(location => (
                  <option key={location.id} value={location.id}>
                    {location.name} {location.hasChanges && `(${location.changeCount} changes)`}
                  </option>
                ))}
              </select>
            </div>

            {/* Analysis Type */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Analysis</label>
              <select
                value={analysisType}
                onChange={(e) => setAnalysisType(e.target.value)}
                className="w-full px-3 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:border-transparent text-sm"
              >
                <option value="changes">Change Detection</option>
                <option value="progress">Progress Analysis</option>
                <option value="safety">Safety Comparison</option>
              </select>
            </div>

            {/* Sync Navigation Toggle */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Navigation</label>
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-600">Sync Views</span>
                <button
                  onClick={() => setSyncNavigation(!syncNavigation)}
                  className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                    syncNavigation ? 'bg-blue-600' : 'bg-gray-200'
                  }`}
                >
                  <span className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                    syncNavigation ? 'translate-x-6' : 'translate-x-1'
                  }`} />
                </button>
              </div>
            </div>

            {/* Overlay Opacity (if overlay mode) */}
            {viewMode === 'overlay' && (
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Opacity</label>
                <input
                  type="range"
                  min="0"
                  max="1"
                  step="0.1"
                  value={overlayOpacity}
                  onChange={(e) => setOverlayOpacity(Number(e.target.value))}
                  className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
                />
                <div className="text-xs text-gray-500 mt-1">{Math.round(overlayOpacity * 100)}%</div>
              </div>
            )}

            {/* Show Analysis Toggle */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Display</label>
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-600">Show Analysis</span>
                <button
                  onClick={() => setShowAnalysis(!showAnalysis)}
                  className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                    showAnalysis ? 'bg-blue-600' : 'bg-gray-200'
                  }`}
                >
                  <span className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                    showAnalysis ? 'translate-x-6' : 'translate-x-1'
                  }`} />
                </button>
              </div>
            </div>
          </div>
        </div>

        {/* Main Content */}
        <div className="flex-1 overflow-auto">
          <div className="grid grid-cols-1 xl:grid-cols-4 gap-6 p-6">
            {/* Street View Comparison Area */}
            <div className="xl:col-span-3 space-y-6">
              {/* Street View Panels */}
              <div className="bg-white rounded-lg p-6 shadow-sm border border-gray-100">
                <div className="flex items-center justify-between mb-4">
                  <h2 className="font-semibold text-gray-900">Street View Comparison</h2>
                  <div className="flex items-center space-x-2">
                    <div className="text-sm text-gray-600">
                      Timespan: {analysisMetrics.timespan}
                    </div>
                    <button className="p-2 hover:bg-gray-100 rounded-lg">
                      <RefreshCw className="w-4 h-4" />
                    </button>
                  </div>
                </div>

                {viewMode === 'side-by-side' ? (
                  <div className="grid grid-cols-2 gap-4">
                    <StreetViewPanel session={comparisonSessions[0]} position="left" />
                    <StreetViewPanel session={comparisonSessions[1]} position="right" />
                  </div>
                ) : viewMode === 'overlay' ? (
                  <div className="relative">
                    <StreetViewPanel session={comparisonSessions[0]} position="left" />
                    <div className="absolute inset-0" style={{ opacity: overlayOpacity }}>
                      <StreetViewPanel session={comparisonSessions[1]} position="right" />
                    </div>
                  </div>
                ) : (
                  <div className="relative">
                    <StreetViewPanel session={comparisonSessions[0]} position="left" />
                    <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent">
                      <div className="w-1 h-full bg-white/80 mx-auto"></div>
                    </div>
                  </div>
                )}
              </div>

              {/* Comparison Timeline */}
              <div className="bg-white rounded-lg p-6 shadow-sm border border-gray-100">
                <h3 className="font-semibold text-gray-900 mb-4">Comparison Timeline</h3>
                <div className="relative">
                  <div className="flex justify-between items-center mb-4">
                    <div className="flex items-center space-x-2">
                      <div className="w-4 h-4 rounded" style={{ backgroundColor: comparisonSessions[0].color }}></div>
                      <span className="text-sm text-gray-600">{comparisonSessions[0].label}</span>
                    </div>
                    <div className="flex items-center space-x-2">
                      <div className="w-4 h-4 rounded" style={{ backgroundColor: comparisonSessions[1].color }}></div>
                      <span className="text-sm text-gray-600">{comparisonSessions[1].label}</span>
                    </div>
                  </div>
                  
                  <div className="h-2 bg-gray-200 rounded-full relative">
                    <div className="absolute left-0 top-0 h-2 w-1/3 rounded-l-full" style={{ backgroundColor: comparisonSessions[0].color }}></div>
                    <div className="absolute right-0 top-0 h-2 w-1/3 rounded-r-full" style={{ backgroundColor: comparisonSessions[1].color }}></div>
                  </div>
                  
                  <div className="flex justify-between text-xs text-gray-500 mt-2">
                    <span>{comparisonSessions[0].date.toLocaleDateString()}</span>
                    <span>{analysisMetrics.timespan} difference</span>
                    <span>{comparisonSessions[1].date.toLocaleDateString()}</span>
                  </div>
                </div>
              </div>

              {/* Analysis Metrics */}
              {showAnalysis && (
                <div className="bg-white rounded-lg p-6 shadow-sm border border-gray-100">
                  <h3 className="font-semibold text-gray-900 mb-4">Analysis Overview</h3>
                  <AnalysisMetrics />
                </div>
              )}
            </div>

            {/* Analysis Panel */}
            <div className="space-y-6">
              {/* Location Summary */}
              <div className="bg-white rounded-lg p-6 shadow-sm border border-gray-100">
                <h3 className="font-semibold text-gray-900 mb-4">Current Location</h3>
                <div className="space-y-3">
                  <div>
                    <p className="font-medium text-gray-900">{getCurrentLocationData()?.name}</p>
                    <p className="text-sm text-gray-600">{getCurrentLocationData()?.description}</p>
                  </div>
                  
                  <div className="flex items-center justify-between py-2 border-t border-gray-100">
                    <span className="text-sm text-gray-600">Changes Detected:</span>
                    <div className="flex items-center space-x-2">
                      {getCurrentLocationData()?.hasChanges ? (
                        <>
                          <span className="font-bold text-orange-600">{getCurrentLocationData()?.changeCount}</span>
                          <div className="w-2 h-2 bg-orange-500 rounded-full animate-pulse"></div>
                        </>
                      ) : (
                        <span className="text-green-600 text-sm">No major changes</span>
                      )}
                    </div>
                  </div>
                </div>
              </div>

              {/* Detected Changes */}
              <div className="bg-white rounded-lg p-6 shadow-sm border border-gray-100">
                <h3 className="font-semibold text-gray-900 mb-4">Detected Changes</h3>
                <div className="space-y-4">
                  {detectedChanges.map((change) => (
                    <ChangeAnalysisItem key={change.id} change={change} />
                  ))}
                </div>
              </div>

              {/* Quick Actions */}
              <div className="bg-white rounded-lg p-6 shadow-sm border border-gray-100">
                <h3 className="font-semibold text-gray-900 mb-4">Quick Actions</h3>
                <div className="space-y-3">
                  <button
                    onClick={() => navigate('/historical-street')}
                    className="w-full flex items-center space-x-3 p-3 text-left bg-blue-50 hover:bg-blue-100 rounded-lg transition-colors"
                  >
                    <Navigation className="w-5 h-5 text-blue-600" />
                    <div>
                      <div className="font-medium text-blue-900">Historical View</div>
                      <div className="text-xs text-blue-600">Navigate through timeline</div>
                    </div>
                  </button>
                  
                  <button
                    onClick={() => navigate('/time-comparison')}
                    className="w-full flex items-center space-x-3 p-3 text-left bg-green-50 hover:bg-green-100 rounded-lg transition-colors"
                  >
                    <Clock className="w-5 h-5 text-green-600" />
                    <div>
                      <div className="font-medium text-green-900">Time Comparison</div>
                      <div className="text-xs text-green-600">Compare video timelines</div>
                    </div>
                  </button>
                  
                  <button
                    onClick={() => navigate('/reports')}
                    className="w-full flex items-center space-x-3 p-3 text-left bg-purple-50 hover:bg-purple-100 rounded-lg transition-colors"
                  >
                    <Download className="w-5 h-5 text-purple-600" />
                    <div>
                      <div className="font-medium text-purple-900">Generate Report</div>
                      <div className="text-xs text-purple-600">Create comparison analysis</div>
                    </div>
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </MainLayout>
  );
};

export default StreetViewComparison;