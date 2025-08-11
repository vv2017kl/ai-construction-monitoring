import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  Play, Pause, RotateCcw, Download, Share2, Calendar, 
  Clock, Camera, Maximize2, SkipBack, SkipForward,
  Volume2, VolumeX, Settings, Layers, MapPin, 
  FastForward, Rewind, Square, Filter, 
  ChevronLeft, ChevronRight, ZoomIn, ZoomOut,
  Grid3X3, BarChart3, Eye, Fullscreen, Monitor
} from 'lucide-react';
import { useTheme } from '../../context/ThemeContext';
import MainLayout from '../../components/shared/Layout/MainLayout';
import { mockCameras, mockSites, mockUser, mockTimeLapseData } from '../../data/mockData';

const TimeLapse = () => {
  const navigate = useNavigate();
  const { theme } = useTheme();
  const videoRef = useRef(null);
  
  // State management
  const [selectedCamera, setSelectedCamera] = useState(mockCameras[0]);
  const [selectedDateRange, setSelectedDateRange] = useState({
    start: new Date(Date.now() - 7 * 24 * 60 * 60 * 1000), // 7 days ago
    end: new Date()
  });
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentTime, setCurrentTime] = useState(0);
  const [duration, setDuration] = useState(3600); // 1 hour in seconds
  const [playbackSpeed, setPlaybackSpeed] = useState(1);
  const [isMuted, setIsMuted] = useState(false);
  const [isFullscreen, setIsFullscreen] = useState(false);
  const [showControls, setShowControls] = useState(true);
  const [selectedView, setSelectedView] = useState('single'); // 'single', 'grid', 'comparison'
  const [compressionLevel, setCompressionLevel] = useState('medium'); // 'low', 'medium', 'high'
  const [showAnnotations, setShowAnnotations] = useState(true);
  const [timelineHover, setTimelineHover] = useState(null);
  
  // Enhanced interactive features
  const [bookmarks, setBookmarks] = useState([]);
  const [showExportModal, setShowExportModal] = useState(false);
  const [exportSettings, setExportSettings] = useState({
    format: 'mp4',
    quality: 'high',
    startTime: 0,
    endTime: 3600,
    includeAnnotations: true,
    fps: 30
  });
  const [isLooping, setIsLooping] = useState(false);
  const [comparisonCamera, setComparisonCamera] = useState(null);
  const [showBookmarkModal, setShowBookmarkModal] = useState(false);
  const [newBookmark, setNewBookmark] = useState({ time: 0, name: '', description: '' });
  const [selectedCameras, setSelectedCameras] = useState(new Set([mockCameras[0].id]));
  const [isGenerating, setIsGenerating] = useState(false);
  const [showShareModal, setShowShareModal] = useState(false);
  const [playbackHistory, setPlaybackHistory] = useState([]);
  const [autoRewind, setAutoRewind] = useState(false);

  const currentSite = mockSites.find(s => s.name === mockUser.currentSite) || mockSites[0];
  const availableCameras = mockCameras.filter(camera => camera.location.includes(currentSite.name));

  // Format time display
  const formatTime = (seconds) => {
    const hrs = Math.floor(seconds / 3600);
    const mins = Math.floor((seconds % 3600) / 60);
    const secs = Math.floor(seconds % 60);
    
    if (hrs > 0) {
      return `${hrs}:${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    }
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  // Mock time-lapse data for the timeline
  const timelineData = {
    events: [
      { time: 300, type: 'personnel', count: 5, description: 'Workers arrived' },
      { time: 900, type: 'equipment', count: 2, description: 'Excavator on site' },
      { time: 1800, type: 'safety', count: 1, description: 'Safety violation detected' },
      { time: 2700, type: 'progress', count: 1, description: 'Foundation work completed' },
      { time: 3300, type: 'personnel', count: 8, description: 'Peak activity period' }
    ],
    activities: [
      { start: 0, end: 1200, type: 'preparation', intensity: 0.3 },
      { start: 1200, end: 2400, type: 'construction', intensity: 0.8 },
      { start: 2400, end: 3200, type: 'inspection', intensity: 0.4 },
      { start: 3200, end: 3600, type: 'cleanup', intensity: 0.2 }
    ]
  };

  const playbackSpeeds = [0.25, 0.5, 1, 2, 4, 8, 16];

  const handlePlayPause = () => {
    setIsPlaying(!isPlaying);
  };

  const handleSeek = (newTime) => {
    setCurrentTime(newTime);
  };

  const handleSpeedChange = (speed) => {
    setPlaybackSpeed(speed);
  };

  // Enhanced interactive functions
  const handleAddBookmark = () => {
    const bookmark = {
      id: Date.now(),
      time: currentTime,
      name: newBookmark.name || `Bookmark ${bookmarks.length + 1}`,
      description: newBookmark.description,
      camera: selectedCamera.id,
      timestamp: new Date().toISOString()
    };
    
    setBookmarks(prev => [...prev, bookmark].sort((a, b) => a.time - b.time));
    setNewBookmark({ time: 0, name: '', description: '' });
    setShowBookmarkModal(false);
  };

  const handleDeleteBookmark = (bookmarkId) => {
    setBookmarks(prev => prev.filter(b => b.id !== bookmarkId));
  };

  const handleJumpToBookmark = (time) => {
    setCurrentTime(time);
    setPlaybackHistory(prev => [...prev, { time, action: 'bookmark_jump', timestamp: new Date() }]);
  };

  const handleFrameStep = (direction) => {
    const frameTime = 1 / 30; // 30 FPS
    const newTime = direction > 0 
      ? Math.min(duration, currentTime + frameTime)
      : Math.max(0, currentTime - frameTime);
    setCurrentTime(newTime);
  };

  const handleExportClip = () => {
    setIsGenerating(true);
    
    // Simulate export process
    setTimeout(() => {
      const filename = `timelapse_${selectedCamera.name}_${new Date().toISOString().split('T')[0]}.${exportSettings.format}`;
      
      // Create mock download
      const element = document.createElement('a');
      element.setAttribute('href', `data:text/plain;charset=utf-8,Mock time-lapse export: ${filename}`);
      element.setAttribute('download', filename);
      element.style.display = 'none';
      document.body.appendChild(element);
      element.click();
      document.body.removeChild(element);
      
      setIsGenerating(false);
      setShowExportModal(false);
    }, 3000);
  };

  const handleCameraSelection = (cameraId, isSelected) => {
    const newSelected = new Set(selectedCameras);
    if (isSelected) {
      newSelected.add(cameraId);
    } else {
      newSelected.delete(cameraId);
    }
    setSelectedCameras(newSelected);
  };

  const handleGenerateShareLink = () => {
    const shareData = {
      camera: selectedCamera.id,
      startTime: currentTime,
      dateRange: selectedDateRange,
      bookmarks: bookmarks,
      settings: { playbackSpeed, compressionLevel, showAnnotations }
    };
    
    const shareUrl = `${window.location.origin}/time-lapse/share/${btoa(JSON.stringify(shareData))}`;
    navigator.clipboard.writeText(shareUrl);
    
    return shareUrl;
  };

  // Auto-play functionality
  useEffect(() => {
    let interval;
    
    if (isPlaying) {
      interval = setInterval(() => {
        setCurrentTime(prev => {
          const newTime = prev + playbackSpeed;
          
          if (newTime >= duration) {
            if (isLooping) {
              return 0;
            } else if (autoRewind) {
              setIsPlaying(false);
              return 0;
            } else {
              setIsPlaying(false);
              return duration;
            }
          }
          
          return newTime;
        });
      }, 1000);
    }
    
    return () => clearInterval(interval);
  }, [isPlaying, playbackSpeed, duration, isLooping, autoRewind]);

  const getActivityColor = (type) => {
    switch (type) {
      case 'preparation': return theme.warning[400];
      case 'construction': return theme.primary[500];
      case 'inspection': return theme.success[400];
      case 'cleanup': return theme.secondary[400];
      default: return theme.gray[400];
    }
  };

  const getEventColor = (type) => {
    switch (type) {
      case 'personnel': return theme.primary[500];
      case 'equipment': return theme.warning[500];
      case 'safety': return theme.danger[500];
      case 'progress': return theme.success[500];
      default: return theme.gray[500];
    }
  };

  // Timeline component
  const Timeline = () => (
    <div className="relative bg-gray-900 rounded-lg p-4">
      {/* Activity Track */}
      <div className="mb-4">
        <div className="text-xs text-gray-400 mb-2">Activity Intensity</div>
        <div className="relative h-8 bg-gray-800 rounded">
          {timelineData.activities.map((activity, index) => (
            <div
              key={index}
              className="absolute top-0 h-full rounded opacity-70"
              style={{
                left: `${(activity.start / duration) * 100}%`,
                width: `${((activity.end - activity.start) / duration) * 100}%`,
                backgroundColor: getActivityColor(activity.type),
                height: `${activity.intensity * 100}%`,
                top: `${(1 - activity.intensity) * 100}%`
              }}
              title={`${activity.type}: ${Math.round(activity.intensity * 100)}% intensity`}
            />
          ))}
        </div>
      </div>

      {/* Main Timeline */}
      <div className="relative">
        <div className="text-xs text-gray-400 mb-2">Timeline Progress</div>
        <div 
          className="relative h-12 bg-gray-800 rounded cursor-pointer"
          onMouseMove={(e) => {
            const rect = e.currentTarget.getBoundingClientRect();
            const hoverTime = ((e.clientX - rect.left) / rect.width) * duration;
            setTimelineHover(hoverTime);
          }}
          onMouseLeave={() => setTimelineHover(null)}
          onClick={(e) => {
            const rect = e.currentTarget.getBoundingClientRect();
            const clickTime = ((e.clientX - rect.left) / rect.width) * duration;
            handleSeek(clickTime);
          }}
        >
          {/* Progress bar */}
          <div 
            className="absolute top-0 left-0 h-full bg-blue-600 rounded"
            style={{ width: `${(currentTime / duration) * 100}%` }}
          />
          
          {/* Events */}
          {timelineData.events.map((event, index) => (
            <div
              key={index}
              className="absolute top-0 w-1 h-full cursor-pointer group"
              style={{ 
                left: `${(event.time / duration) * 100}%`,
                backgroundColor: getEventColor(event.type)
              }}
            >
              <div className="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 opacity-0 group-hover:opacity-100 transition-opacity bg-gray-900 text-white text-xs p-2 rounded whitespace-nowrap z-10">
                {event.description}
                <div className="text-gray-400">{formatTime(event.time)}</div>
              </div>
            </div>
          ))}
          
          {/* Current time indicator */}
          <div 
            className="absolute top-0 w-0.5 h-full bg-white"
            style={{ left: `${(currentTime / duration) * 100}%` }}
          />
          
          {/* Hover indicator */}
          {timelineHover !== null && (
            <div 
              className="absolute top-0 w-0.5 h-full bg-yellow-400 opacity-50"
              style={{ left: `${(timelineHover / duration) * 100}%` }}
            />
          )}
        </div>
        
        {/* Time markers */}
        <div className="flex justify-between text-xs text-gray-400 mt-1">
          <span>0:00</span>
          <span>15:00</span>
          <span>30:00</span>
          <span>45:00</span>
          <span>1:00:00</span>
        </div>
      </div>
      
      {/* Event Legend */}
      <div className="flex flex-wrap gap-4 mt-4 text-xs">
        <div className="flex items-center space-x-1">
          <div className="w-2 h-2 rounded" style={{ backgroundColor: getEventColor('personnel') }}></div>
          <span className="text-gray-400">Personnel</span>
        </div>
        <div className="flex items-center space-x-1">
          <div className="w-2 h-2 rounded" style={{ backgroundColor: getEventColor('equipment') }}></div>
          <span className="text-gray-400">Equipment</span>
        </div>
        <div className="flex items-center space-x-1">
          <div className="w-2 h-2 rounded" style={{ backgroundColor: getEventColor('safety') }}></div>
          <span className="text-gray-400">Safety Events</span>
        </div>
        <div className="flex items-center space-x-1">
          <div className="w-2 h-2 rounded" style={{ backgroundColor: getEventColor('progress') }}></div>
          <span className="text-gray-400">Progress Milestones</span>
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
              <h1 className="text-xl font-bold text-gray-900">Time Lapse View</h1>
              <div className="flex items-center space-x-2 text-sm text-gray-600">
                <Camera className="w-3 h-3" />
                <span>{selectedCamera.name}</span>
                <span>•</span>
                <MapPin className="w-3 h-3" />
                <span>{selectedCamera.location}</span>
                <span>•</span>
                <Clock className="w-3 h-3" />
                <span>{selectedDateRange.start.toLocaleDateString()} - {selectedDateRange.end.toLocaleDateString()}</span>
              </div>
            </div>

            <div className="flex items-center space-x-4">
              {/* View Mode Selector */}
              <div className="flex items-center space-x-2 bg-gray-100 rounded-lg p-1">
                {[
                  { key: 'single', label: 'Single', icon: Monitor },
                  { key: 'grid', label: 'Grid', icon: Grid3X3 },
                  { key: 'comparison', label: 'Compare', icon: BarChart3 }
                ].map(({ key, label, icon: Icon }) => (
                  <button
                    key={key}
                    onClick={() => setSelectedView(key)}
                    className={`flex items-center space-x-1 px-3 py-1 text-sm rounded transition-colors ${
                      selectedView === key 
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
                <span>Export</span>
              </button>
            </div>
          </div>
        </div>

        {/* Main Content Area */}
        <div className="flex-1 flex overflow-hidden">
          {/* Left Sidebar - Camera Selection & Settings */}
          <div className="w-80 bg-white border-r border-gray-200 flex flex-col">
            {/* Camera Selection */}
            <div className="p-4 border-b border-gray-200">
              <h3 className="font-semibold text-gray-900 mb-3">Camera Selection</h3>
              <div className="space-y-2 max-h-40 overflow-y-auto">
                {availableCameras.map((camera) => (
                  <div
                    key={camera.id}
                    onClick={() => setSelectedCamera(camera)}
                    className={`p-3 rounded-lg cursor-pointer transition-colors ${
                      selectedCamera.id === camera.id 
                        ? 'bg-blue-50 border-blue-200 border' 
                        : 'hover:bg-gray-50 border border-transparent'
                    }`}
                  >
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="font-medium text-gray-900">{camera.name}</p>
                        <p className="text-sm text-gray-600">{camera.location}</p>
                      </div>
                      <div className={`w-2 h-2 rounded-full ${
                        camera.status === 'online' ? 'bg-green-500' : 'bg-red-500'
                      }`} />
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Date Range Selection */}
            <div className="p-4 border-b border-gray-200">
              <h3 className="font-semibold text-gray-900 mb-3">Date Range</h3>
              <div className="space-y-3">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Start Date</label>
                  <input
                    type="date"
                    value={selectedDateRange.start.toISOString().split('T')[0]}
                    onChange={(e) => setSelectedDateRange(prev => ({
                      ...prev,
                      start: new Date(e.target.value)
                    }))}
                    className="w-full px-3 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:border-transparent"
                    style={{ '--tw-ring-color': theme.primary[500] + '40' }}
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">End Date</label>
                  <input
                    type="date"
                    value={selectedDateRange.end.toISOString().split('T')[0]}
                    onChange={(e) => setSelectedDateRange(prev => ({
                      ...prev,
                      end: new Date(e.target.value)
                    }))}
                    className="w-full px-3 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:border-transparent"
                    style={{ '--tw-ring-color': theme.primary[500] + '40' }}
                  />
                </div>
              </div>
            </div>

            {/* Compression & Quality Settings */}
            <div className="p-4 border-b border-gray-200">
              <h3 className="font-semibold text-gray-900 mb-3">Quality Settings</h3>
              <div className="space-y-3">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Compression Level</label>
                  <select
                    value={compressionLevel}
                    onChange={(e) => setCompressionLevel(e.target.value)}
                    className="w-full px-3 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:border-transparent"
                  >
                    <option value="low">Low (High Quality)</option>
                    <option value="medium">Medium (Balanced)</option>
                    <option value="high">High (Fast Loading)</option>
                  </select>
                </div>
                
                <div className="flex items-center justify-between">
                  <label className="text-sm font-medium text-gray-700">Show Annotations</label>
                  <button
                    onClick={() => setShowAnnotations(!showAnnotations)}
                    className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                      showAnnotations ? 'bg-blue-600' : 'bg-gray-200'
                    }`}
                  >
                    <span
                      className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                        showAnnotations ? 'translate-x-6' : 'translate-x-1'
                      }`}
                    />
                  </button>
                </div>
              </div>
            </div>

            {/* Quick Stats */}
            <div className="p-4 flex-1">
              <h3 className="font-semibold text-gray-900 mb-3">Session Statistics</h3>
              <div className="space-y-3">
                <div className="flex justify-between">
                  <span className="text-gray-600">Duration:</span>
                  <span className="font-medium">{formatTime(duration)}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Events:</span>
                  <span className="font-medium">{timelineData.events.length}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Compression:</span>
                  <span className="font-medium">{compressionLevel}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">File Size:</span>
                  <span className="font-medium">
                    {compressionLevel === 'low' ? '2.1 GB' : 
                     compressionLevel === 'medium' ? '834 MB' : '312 MB'}
                  </span>
                </div>
              </div>
            </div>
          </div>

          {/* Main Video Area */}
          <div className="flex-1 flex flex-col">
            {/* Video Player */}
            <div className="flex-1 relative bg-black">
              {/* Video Mock Display */}
              <div className="absolute inset-0 flex items-center justify-center">
                <div className="text-center text-white">
                  <Camera className="w-16 h-16 mx-auto mb-4 opacity-50" />
                  <h3 className="text-xl font-bold mb-2">Time Lapse Preview</h3>
                  <p className="text-gray-300">
                    {selectedCamera.name} • {selectedDateRange.start.toLocaleDateString()} - {selectedDateRange.end.toLocaleDateString()}
                  </p>
                  <div className="mt-4 text-sm text-gray-400">
                    Click play to start time-lapse playback at {playbackSpeed}x speed
                  </div>
                </div>
              </div>

              {/* Overlay Controls */}
              {showControls && (
                <div className="absolute top-4 right-4 flex space-x-2">
                  <button 
                    onClick={() => setIsFullscreen(!isFullscreen)}
                    className="p-2 bg-black/50 hover:bg-black/70 text-white rounded-lg transition-colors"
                  >
                    <Fullscreen className="w-5 h-5" />
                  </button>
                  <button className="p-2 bg-black/50 hover:bg-black/70 text-white rounded-lg transition-colors">
                    <Share2 className="w-5 h-5" />
                  </button>
                </div>
              )}

              {/* Speed Indicator */}
              {playbackSpeed !== 1 && (
                <div className="absolute top-4 left-4 bg-black/70 text-white px-3 py-1 rounded-lg text-sm">
                  {playbackSpeed}x Speed
                </div>
              )}
            </div>

            {/* Video Controls */}
            <div className="bg-gray-900 text-white p-4">
              <div className="mb-4">
                <Timeline />
              </div>

              {/* Playback Controls */}
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-4">
                  <button
                    onClick={handlePlayPause}
                    className="flex items-center justify-center w-12 h-12 bg-blue-600 hover:bg-blue-700 rounded-full transition-colors"
                  >
                    {isPlaying ? <Pause className="w-6 h-6" /> : <Play className="w-6 h-6 ml-0.5" />}
                  </button>
                  
                  <button
                    onClick={() => handleSeek(Math.max(0, currentTime - 60))}
                    className="p-2 hover:bg-gray-700 rounded-lg transition-colors"
                  >
                    <SkipBack className="w-5 h-5" />
                  </button>
                  
                  <button
                    onClick={() => handleSeek(Math.min(duration, currentTime + 60))}
                    className="p-2 hover:bg-gray-700 rounded-lg transition-colors"
                  >
                    <SkipForward className="w-5 h-5" />
                  </button>

                  <div className="text-sm text-gray-300">
                    {formatTime(currentTime)} / {formatTime(duration)}
                  </div>
                </div>

                <div className="flex items-center space-x-4">
                  {/* Speed Control */}
                  <div className="flex items-center space-x-2">
                    <span className="text-sm text-gray-400">Speed:</span>
                    <select
                      value={playbackSpeed}
                      onChange={(e) => handleSpeedChange(Number(e.target.value))}
                      className="bg-gray-800 border border-gray-600 rounded px-2 py-1 text-sm"
                    >
                      {playbackSpeeds.map(speed => (
                        <option key={speed} value={speed}>{speed}x</option>
                      ))}
                    </select>
                  </div>

                  {/* Volume Control */}
                  <button
                    onClick={() => setIsMuted(!isMuted)}
                    className="p-2 hover:bg-gray-700 rounded-lg transition-colors"
                  >
                    {isMuted ? <VolumeX className="w-5 h-5" /> : <Volume2 className="w-5 h-5" />}
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

export default TimeLapse;