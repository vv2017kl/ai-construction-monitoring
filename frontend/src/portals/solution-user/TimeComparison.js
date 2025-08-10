import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  Play, Pause, RotateCcw, Download, Share2, Calendar, 
  Clock, Camera, Maximize2, SkipBack, SkipForward,
  Volume2, VolumeX, Settings, Layers, MapPin, 
  FastForward, Rewind, Square, Filter, Split,
  ChevronLeft, ChevronRight, ZoomIn, ZoomOut,
  Grid3X3, BarChart3, Eye, Fullscreen, Monitor,
  ArrowLeftRight, ArrowUpDown, RotateCw, Shuffle,
  Columns2, Rows2, AlignCenter, Move, RefreshCw
} from 'lucide-react';
import { useTheme } from '../../context/ThemeContext';
import MainLayout from '../../components/shared/Layout/MainLayout';
import { mockCameras, mockSites, mockUser, mockTimeLapseData } from '../../data/mockData';

const TimeComparison = () => {
  const navigate = useNavigate();
  const { theme } = useTheme();
  
  // State management
  const [selectedCameras, setSelectedCameras] = useState([mockCameras[0], mockCameras[1]]);
  const [comparisonMode, setComparisonMode] = useState('side-by-side'); // 'side-by-side', 'overlay', 'split-screen', 'difference'
  const [timeRanges, setTimeRanges] = useState([
    {
      id: 'period1',
      label: 'Period 1',
      start: new Date(Date.now() - 7 * 24 * 60 * 60 * 1000), // 7 days ago
      end: new Date(Date.now() - 6 * 24 * 60 * 60 * 1000),
      color: '#3b82f6'
    },
    {
      id: 'period2',
      label: 'Period 2', 
      start: new Date(Date.now() - 24 * 60 * 60 * 1000), // 1 day ago
      end: new Date(),
      color: '#ef4444'
    }
  ]);
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentTime, setCurrentTime] = useState(0);
  const [duration, setDuration] = useState(3600); // 1 hour
  const [playbackSpeed, setPlaybackSpeed] = useState(1);
  const [syncPlayback, setSyncPlayback] = useState(true);
  const [overlayOpacity, setOverlayOpacity] = useState(0.5);
  const [analysisMode, setAnalysisMode] = useState('visual'); // 'visual', 'motion', 'changes'
  const [showMetrics, setShowMetrics] = useState(true);

  const currentSite = mockSites.find(s => s.name === mockUser.currentSite) || mockSites[0];
  const playbackSpeeds = [0.25, 0.5, 1, 2, 4, 8];

  // Mock comparison metrics
  const comparisonMetrics = {
    motionDetected: {
      period1: 85,
      period2: 92,
      change: '+8.2%'
    },
    personnelCount: {
      period1: 12,
      period2: 18,
      change: '+50%'
    },
    equipmentActivity: {
      period1: 6,
      period2: 4,
      change: '-33%'
    },
    safetyEvents: {
      period1: 2,
      period2: 0,
      change: '-100%'
    },
    weatherConditions: {
      period1: 'Sunny',
      period2: 'Overcast',
      change: 'Different'
    }
  };

  // Mock detected changes
  const detectedChanges = [
    {
      id: 1,
      timestamp: 1200,
      type: 'personnel_increase',
      description: 'Personnel count increased from 12 to 18',
      confidence: 95,
      location: 'Zone A - Foundation'
    },
    {
      id: 2,
      timestamp: 1800,
      type: 'equipment_change',
      description: 'New excavator detected in Period 2',
      confidence: 87,
      location: 'Zone C - Excavation'
    },
    {
      id: 3,
      timestamp: 2400,
      type: 'construction_progress',
      description: 'Foundation work progress detected',
      confidence: 92,
      location: 'Zone B - Steel Frame'
    }
  ];

  const formatTime = (seconds) => {
    const hrs = Math.floor(seconds / 3600);
    const mins = Math.floor((seconds % 3600) / 60);
    const secs = Math.floor(seconds % 60);
    
    if (hrs > 0) {
      return `${hrs}:${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    }
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  const formatDate = (date) => {
    return new Date(date).toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const getChangeColor = (change) => {
    if (change.startsWith('+')) return 'text-green-600';
    if (change.startsWith('-')) return 'text-red-600';
    return 'text-gray-600';
  };

  const getChangeIcon = (change) => {
    if (change.startsWith('+')) return '↗';
    if (change.startsWith('-')) return '↘';
    return '→';
  };

  const VideoPlayer = ({ period, position }) => (
    <div className={`relative bg-black rounded-lg overflow-hidden ${position === 'left' ? '' : 'ml-2'}`}>
      {/* Video Mock Display */}
      <div className="aspect-video flex items-center justify-center">
        <div className="text-center text-white">
          <Camera className="w-12 h-12 mx-auto mb-3 opacity-50" />
          <h3 className="text-lg font-bold mb-2">{period.label} Comparison</h3>
          <div className="text-sm text-gray-300 space-y-1">
            <p>{selectedCameras[position === 'left' ? 0 : 1]?.name}</p>
            <p>{formatDate(period.start)} - {formatDate(period.end)}</p>
            <div className="mt-3">
              <div className={`w-3 h-3 mx-auto rounded-full`} style={{ backgroundColor: period.color }}></div>
            </div>
          </div>
        </div>
      </div>

      {/* Video Overlay Controls */}
      <div className="absolute top-4 right-4 flex space-x-2">
        <button className="p-2 bg-black/50 hover:bg-black/70 text-white rounded-lg transition-colors">
          <Fullscreen className="w-4 h-4" />
        </button>
        <button className="p-2 bg-black/50 hover:bg-black/70 text-white rounded-lg transition-colors">
          <Settings className="w-4 h-4" />
        </button>
      </div>

      {/* Period Indicator */}
      <div 
        className="absolute bottom-4 left-4 px-3 py-2 rounded-lg text-white text-sm font-medium"
        style={{ backgroundColor: period.color + 'CC' }}
      >
        {period.label}
      </div>

      {/* Playback Speed Indicator */}
      {playbackSpeed !== 1 && (
        <div className="absolute top-4 left-4 bg-black/70 text-white px-2 py-1 rounded text-sm">
          {playbackSpeed}x
        </div>
      )}
    </div>
  );

  const MetricsCard = ({ title, metric }) => (
    <div className="bg-white rounded-lg p-4 shadow-sm border border-gray-100">
      <h4 className="font-medium text-gray-900 mb-3">{title}</h4>
      <div className="space-y-2">
        <div className="flex justify-between items-center">
          <span className="text-sm text-gray-600">Period 1:</span>
          <span className="font-medium">{metric.period1}</span>
        </div>
        <div className="flex justify-between items-center">
          <span className="text-sm text-gray-600">Period 2:</span>
          <span className="font-medium">{metric.period2}</span>
        </div>
        <div className="flex justify-between items-center pt-2 border-t border-gray-100">
          <span className="text-sm font-medium text-gray-700">Change:</span>
          <span className={`font-bold ${getChangeColor(metric.change)}`}>
            {getChangeIcon(metric.change)} {metric.change}
          </span>
        </div>
      </div>
    </div>
  );

  const ChangeDetectionItem = ({ change }) => (
    <div className="flex items-start space-x-3 p-3 bg-white rounded-lg border border-gray-200 hover:shadow-sm transition-shadow">
      <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center flex-shrink-0">
        <span className="text-blue-600 text-xs font-bold">{change.confidence}%</span>
      </div>
      <div className="flex-1">
        <div className="flex items-center justify-between mb-1">
          <h4 className="font-medium text-gray-900 text-sm">{change.description}</h4>
          <span className="text-xs text-gray-500">{formatTime(change.timestamp)}</span>
        </div>
        <p className="text-xs text-gray-600">{change.location}</p>
        <span className="inline-block mt-2 px-2 py-1 bg-gray-100 text-gray-700 text-xs rounded capitalize">
          {change.type.replace('_', ' ')}
        </span>
      </div>
    </div>
  );

  const Timeline = () => (
    <div className="bg-gray-900 rounded-lg p-4">
      <div className="mb-4">
        <div className="text-xs text-gray-400 mb-2">Comparison Timeline</div>
        <div 
          className="relative h-12 bg-gray-800 rounded cursor-pointer"
          onClick={(e) => {
            const rect = e.currentTarget.getBoundingClientRect();
            const clickTime = ((e.clientX - rect.left) / rect.width) * duration;
            setCurrentTime(clickTime);
          }}
        >
          {/* Progress bar */}
          <div 
            className="absolute top-0 left-0 h-full bg-blue-600 rounded"
            style={{ width: `${(currentTime / duration) * 100}%` }}
          />
          
          {/* Change markers */}
          {detectedChanges.map((change, index) => (
            <div
              key={change.id}
              className="absolute top-0 w-1 h-full bg-yellow-400 cursor-pointer"
              style={{ left: `${(change.timestamp / duration) * 100}%` }}
              title={change.description}
            />
          ))}
          
          {/* Current time indicator */}
          <div 
            className="absolute top-0 w-0.5 h-full bg-white"
            style={{ left: `${(currentTime / duration) * 100}%` }}
          />
        </div>
        
        <div className="flex justify-between text-xs text-gray-400 mt-1">
          <span>0:00</span>
          <span>15:00</span>
          <span>30:00</span>
          <span>45:00</span>
          <span>1:00:00</span>
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
              <h1 className="text-xl font-bold text-gray-900">Time Comparison</h1>
              <div className="flex items-center space-x-2 text-sm text-gray-600">
                <Camera className="w-3 h-3" />
                <span>{selectedCameras.map(c => c.name).join(' vs ')}</span>
                <span>•</span>
                <Clock className="w-3 h-3" />
                <span>Comparing {timeRanges.length} time periods</span>
              </div>
            </div>

            <div className="flex items-center space-x-4">
              {/* Comparison Mode Selector */}
              <div className="flex items-center space-x-2 bg-gray-100 rounded-lg p-1">
                {[
                  { key: 'side-by-side', label: 'Side by Side', icon: Columns2 },
                  { key: 'overlay', label: 'Overlay', icon: Layers },
                  { key: 'split-screen', label: 'Split', icon: Split },
                  { key: 'difference', label: 'Difference', icon: BarChart3 }
                ].map(({ key, label, icon: Icon }) => (
                  <button
                    key={key}
                    onClick={() => setComparisonMode(key)}
                    className={`flex items-center space-x-1 px-3 py-1 text-sm rounded transition-colors ${
                      comparisonMode === key 
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
                <span>Export Analysis</span>
              </button>
            </div>
          </div>
        </div>

        {/* Configuration Panel */}
        <div className="bg-white border-b border-gray-200 px-6 py-4">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            {/* Time Period 1 */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Period 1 (Blue)</label>
              <div className="space-y-2">
                <input
                  type="date"
                  value={timeRanges[0].start.toISOString().split('T')[0]}
                  onChange={(e) => {
                    const newRanges = [...timeRanges];
                    newRanges[0].start = new Date(e.target.value);
                    setTimeRanges(newRanges);
                  }}
                  className="w-full px-3 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:border-transparent text-sm"
                />
                <input
                  type="date"
                  value={timeRanges[0].end.toISOString().split('T')[0]}
                  onChange={(e) => {
                    const newRanges = [...timeRanges];
                    newRanges[0].end = new Date(e.target.value);
                    setTimeRanges(newRanges);
                  }}
                  className="w-full px-3 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:border-transparent text-sm"
                />
              </div>
            </div>

            {/* Time Period 2 */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Period 2 (Red)</label>
              <div className="space-y-2">
                <input
                  type="date"
                  value={timeRanges[1].start.toISOString().split('T')[0]}
                  onChange={(e) => {
                    const newRanges = [...timeRanges];
                    newRanges[1].start = new Date(e.target.value);
                    setTimeRanges(newRanges);
                  }}
                  className="w-full px-3 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:border-transparent text-sm"
                />
                <input
                  type="date"
                  value={timeRanges[1].end.toISOString().split('T')[0]}
                  onChange={(e) => {
                    const newRanges = [...timeRanges];
                    newRanges[1].end = new Date(e.target.value);
                    setTimeRanges(newRanges);
                  }}
                  className="w-full px-3 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:border-transparent text-sm"
                />
              </div>
            </div>

            {/* Camera Selection */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Camera</label>
              <select
                value={selectedCameras[0]?.id || ''}
                onChange={(e) => {
                  const camera = mockCameras.find(c => c.id === e.target.value);
                  setSelectedCameras(prev => [camera, prev[1]]);
                }}
                className="w-full px-3 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:border-transparent text-sm"
              >
                {mockCameras.map(camera => (
                  <option key={camera.id} value={camera.id}>{camera.name}</option>
                ))}
              </select>
              {comparisonMode === 'side-by-side' && (
                <select
                  value={selectedCameras[1]?.id || ''}
                  onChange={(e) => {
                    const camera = mockCameras.find(c => c.id === e.target.value);
                    setSelectedCameras(prev => [prev[0], camera]);
                  }}
                  className="w-full px-3 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:border-transparent text-sm mt-2"
                >
                  {mockCameras.map(camera => (
                    <option key={camera.id} value={camera.id}>{camera.name}</option>
                  ))}
                </select>
              )}
            </div>

            {/* Analysis Options */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Analysis</label>
              <div className="space-y-2">
                <select
                  value={analysisMode}
                  onChange={(e) => setAnalysisMode(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:border-transparent text-sm"
                >
                  <option value="visual">Visual Comparison</option>
                  <option value="motion">Motion Detection</option>
                  <option value="changes">Change Detection</option>
                </select>
                <div className="flex items-center justify-between">
                  <label className="text-sm text-gray-700">Sync Playback</label>
                  <button
                    onClick={() => setSyncPlayback(!syncPlayback)}
                    className={`relative inline-flex h-5 w-9 items-center rounded-full transition-colors ${
                      syncPlayback ? 'bg-blue-600' : 'bg-gray-200'
                    }`}
                  >
                    <span className={`inline-block h-3 w-3 transform rounded-full bg-white transition-transform ${
                      syncPlayback ? 'translate-x-5' : 'translate-x-1'
                    }`} />
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Main Content */}
        <div className="flex-1 overflow-auto">
          <div className="grid grid-cols-1 xl:grid-cols-4 gap-6 p-6">
            {/* Video Comparison Area */}
            <div className="xl:col-span-3 space-y-6">
              {/* Video Players */}
              <div className="bg-white rounded-lg p-6 shadow-sm border border-gray-100">
                <div className="flex items-center justify-between mb-4">
                  <h2 className="font-semibold text-gray-900">Video Comparison</h2>
                  <div className="flex items-center space-x-2">
                    {comparisonMode === 'overlay' && (
                      <div className="flex items-center space-x-2">
                        <span className="text-sm text-gray-600">Opacity:</span>
                        <input
                          type="range"
                          min="0"
                          max="1"
                          step="0.1"
                          value={overlayOpacity}
                          onChange={(e) => setOverlayOpacity(Number(e.target.value))}
                          className="w-20"
                        />
                        <span className="text-sm text-gray-600">{Math.round(overlayOpacity * 100)}%</span>
                      </div>
                    )}
                    <button className="p-2 hover:bg-gray-100 rounded-lg">
                      <RefreshCw className="w-4 h-4" />
                    </button>
                  </div>
                </div>

                {comparisonMode === 'side-by-side' ? (
                  <div className="grid grid-cols-2 gap-4">
                    <VideoPlayer period={timeRanges[0]} position="left" />
                    <VideoPlayer period={timeRanges[1]} position="right" />
                  </div>
                ) : (
                  <div className="relative">
                    <VideoPlayer period={timeRanges[0]} position="left" />
                    {comparisonMode === 'overlay' && (
                      <div className="absolute inset-0" style={{ opacity: overlayOpacity }}>
                        <VideoPlayer period={timeRanges[1]} position="right" />
                      </div>
                    )}
                  </div>
                )}
              </div>

              {/* Timeline */}
              <Timeline />

              {/* Playback Controls */}
              <div className="bg-gray-900 text-white rounded-lg p-4">
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-4">
                    <button
                      onClick={() => setIsPlaying(!isPlaying)}
                      className="flex items-center justify-center w-12 h-12 bg-blue-600 hover:bg-blue-700 rounded-full transition-colors"
                    >
                      {isPlaying ? <Pause className="w-6 h-6" /> : <Play className="w-6 h-6 ml-0.5" />}
                    </button>
                    
                    <button className="p-2 hover:bg-gray-700 rounded-lg transition-colors">
                      <SkipBack className="w-5 h-5" />
                    </button>
                    
                    <button className="p-2 hover:bg-gray-700 rounded-lg transition-colors">
                      <SkipForward className="w-5 h-5" />
                    </button>

                    <div className="text-sm text-gray-300">
                      {formatTime(currentTime)} / {formatTime(duration)}
                    </div>
                  </div>

                  <div className="flex items-center space-x-4">
                    <div className="flex items-center space-x-2">
                      <span className="text-sm text-gray-400">Speed:</span>
                      <select
                        value={playbackSpeed}
                        onChange={(e) => setPlaybackSpeed(Number(e.target.value))}
                        className="bg-gray-800 border border-gray-600 rounded px-2 py-1 text-sm"
                      >
                        {playbackSpeeds.map(speed => (
                          <option key={speed} value={speed}>{speed}x</option>
                        ))}
                      </select>
                    </div>

                    <button className="p-2 hover:bg-gray-700 rounded-lg transition-colors">
                      <Volume2 className="w-5 h-5" />
                    </button>
                  </div>
                </div>
              </div>
            </div>

            {/* Analysis Panel */}
            <div className="space-y-6">
              {/* Comparison Metrics */}
              {showMetrics && (
                <div className="bg-white rounded-lg p-6 shadow-sm border border-gray-100">
                  <div className="flex items-center justify-between mb-4">
                    <h3 className="font-semibold text-gray-900">Comparison Metrics</h3>
                    <button
                      onClick={() => setShowMetrics(!showMetrics)}
                      className="text-gray-600 hover:text-gray-800"
                    >
                      <Eye className="w-4 h-4" />
                    </button>
                  </div>
                  <div className="space-y-4">
                    <MetricsCard title="Motion" metric={comparisonMetrics.motionDetected} />
                    <MetricsCard title="Personnel" metric={comparisonMetrics.personnelCount} />
                    <MetricsCard title="Equipment" metric={comparisonMetrics.equipmentActivity} />
                    <MetricsCard title="Safety Events" metric={comparisonMetrics.safetyEvents} />
                  </div>
                </div>
              )}

              {/* Detected Changes */}
              <div className="bg-white rounded-lg p-6 shadow-sm border border-gray-100">
                <h3 className="font-semibold text-gray-900 mb-4">Detected Changes</h3>
                <div className="space-y-3">
                  {detectedChanges.map((change) => (
                    <ChangeDetectionItem key={change.id} change={change} />
                  ))}
                </div>
              </div>

              {/* Quick Actions */}
              <div className="bg-white rounded-lg p-6 shadow-sm border border-gray-100">
                <h3 className="font-semibold text-gray-900 mb-4">Quick Actions</h3>
                <div className="space-y-3">
                  <button
                    onClick={() => navigate('/time-lapse')}
                    className="w-full flex items-center space-x-3 p-3 text-left bg-blue-50 hover:bg-blue-100 rounded-lg transition-colors"
                  >
                    <Clock className="w-5 h-5 text-blue-600" />
                    <div>
                      <div className="font-medium text-blue-900">Time Lapse View</div>
                      <div className="text-xs text-blue-600">View condensed timeline</div>
                    </div>
                  </button>
                  
                  <button
                    onClick={() => navigate('/reports')}
                    className="w-full flex items-center space-x-3 p-3 text-left bg-green-50 hover:bg-green-100 rounded-lg transition-colors"
                  >
                    <Download className="w-5 h-5 text-green-600" />
                    <div>
                      <div className="font-medium text-green-900">Generate Report</div>
                      <div className="text-xs text-green-600">Create comparison analysis</div>
                    </div>
                  </button>
                  
                  <button className="w-full flex items-center space-x-3 p-3 text-left bg-purple-50 hover:bg-purple-100 rounded-lg transition-colors">
                    <Share2 className="w-5 h-5 text-purple-600" />
                    <div>
                      <div className="font-medium text-purple-900">Share Analysis</div>
                      <div className="text-xs text-purple-600">Export or send findings</div>
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

export default TimeComparison;