import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  Navigation, Calendar, Clock, Camera, MapPin, Play, Pause,
  SkipBack, SkipForward, RotateCcw, RotateCw, ZoomIn, ZoomOut,
  Maximize2, Download, Share2, Settings, Layers, Route,
  ChevronLeft, ChevronRight, ChevronUp, ChevronDown,
  Compass, Target, Grid3X3, Crosshair, Map, Eye, EyeOff,
  FastForward, Rewind, Square, Volume2, VolumeX, Home,
  ArrowLeft, ArrowRight, ArrowUp, ArrowDown, Move, Locate
} from 'lucide-react';
import { useTheme } from '../../context/ThemeContext';
import MainLayout from '../../components/shared/Layout/MainLayout';
import { mockSites, mockUser, mockCameras } from '../../data/mockData';

const HistoricalStreetView = () => {
  const navigate = useNavigate();
  const { theme } = useTheme();
  
  // State management
  const [selectedDate, setSelectedDate] = useState(new Date(Date.now() - 24 * 60 * 60 * 1000)); // Yesterday
  const [selectedTime, setSelectedTime] = useState('14:30');
  const [currentLocation, setCurrentLocation] = useState({
    x: 45, // Percentage from left
    y: 55, // Percentage from top
    heading: 90, // Degrees (0=North, 90=East, 180=South, 270=West)
    zoom: 1
  });
  const [viewMode, setViewMode] = useState('street'); // 'street', 'map', 'hybrid'
  const [isPlaying, setIsPlaying] = useState(false);
  const [playbackSpeed, setPlaybackSpeed] = useState(1);
  const [showOverlay, setShowOverlay] = useState(true);
  const [overlayType, setOverlayType] = useState('navigation'); // 'navigation', 'annotations', 'measurements'
  const [pathHistory, setPathHistory] = useState([]);
  const [bookmarks, setBookmarks] = useState([]);
  const [fieldOfView, setFieldOfView] = useState(90); // Degrees

  const currentSite = mockSites.find(s => s.name === mockUser.currentSite) || mockSites[0];

  // Mock historical locations/waypoints
  const historicalWaypoints = [
    {
      id: 'wp1',
      name: 'Main Entrance',
      x: 15,
      y: 30,
      timestamp: '2025-01-09T09:00:00Z',
      description: 'Site main entrance and security checkpoint',
      available: true
    },
    {
      id: 'wp2', 
      name: 'Zone A - Foundation',
      x: 45,
      y: 55,
      timestamp: '2025-01-09T10:30:00Z',
      description: 'Foundation work area with concrete pouring',
      available: true
    },
    {
      id: 'wp3',
      name: 'Equipment Yard',
      x: 70,
      y: 35,
      timestamp: '2025-01-09T12:15:00Z',
      description: 'Heavy equipment storage and maintenance area',
      available: true
    },
    {
      id: 'wp4',
      name: 'Zone B - Steel Frame',
      x: 60,
      y: 70,
      timestamp: '2025-01-09T14:00:00Z',
      description: 'Steel framework construction area',
      available: true
    },
    {
      id: 'wp5',
      name: 'Office Trailers',
      x: 25,
      y: 15,
      timestamp: '2025-01-09T16:30:00Z',
      description: 'Site office and meeting facilities',
      available: false
    }
  ];

  // Mock path recordings
  const pathRecordings = [
    {
      id: 'path1',
      name: 'Morning Safety Inspection',
      date: '2025-01-09',
      startTime: '08:00',
      duration: '45 minutes',
      waypoints: 8,
      distance: '2.3 km',
      inspector: 'Sarah Chen'
    },
    {
      id: 'path2',
      name: 'Construction Progress Review',
      date: '2025-01-09',
      startTime: '14:30',
      duration: '32 minutes',
      waypoints: 12,
      distance: '1.8 km',
      inspector: 'John Mitchell'
    },
    {
      id: 'path3',
      name: 'Equipment Audit Walk',
      date: '2025-01-09',
      startTime: '16:00',
      duration: '28 minutes',
      waypoints: 6,
      distance: '1.2 km',
      inspector: 'Mike Rodriguez'
    }
  ];

  const moveLocation = (direction, amount = 5) => {
    setCurrentLocation(prev => {
      let newX = prev.x;
      let newY = prev.y;
      
      switch (direction) {
        case 'up':
          newY = Math.max(5, prev.y - amount);
          break;
        case 'down':
          newY = Math.min(95, prev.y + amount);
          break;
        case 'left':
          newX = Math.max(5, prev.x - amount);
          break;
        case 'right':
          newX = Math.min(95, prev.x + amount);
          break;
      }
      
      return { ...prev, x: newX, y: newY };
    });
  };

  const rotateView = (direction, amount = 15) => {
    setCurrentLocation(prev => ({
      ...prev,
      heading: (prev.heading + (direction === 'left' ? -amount : amount) + 360) % 360
    }));
  };

  const zoomView = (direction, amount = 0.2) => {
    setCurrentLocation(prev => ({
      ...prev,
      zoom: Math.max(0.5, Math.min(3, prev.zoom + (direction === 'in' ? amount : -amount)))
    }));
  };

  const goToWaypoint = (waypoint) => {
    if (!waypoint.available) return;
    
    setCurrentLocation(prev => ({
      ...prev,
      x: waypoint.x,
      y: waypoint.y
    }));
    
    // Add to path history
    setPathHistory(prev => [...prev, waypoint]);
  };

  const formatHeading = (degrees) => {
    const directions = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'];
    const index = Math.round(degrees / 45) % 8;
    return `${directions[index]} (${degrees}°)`;
  };

  const formatDate = (date) => {
    return new Date(date).toLocaleDateString('en-US', {
      weekday: 'long',
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  };

  const StreetViewDisplay = () => (
    <div className="relative bg-gradient-to-b from-blue-200 to-green-200 rounded-lg overflow-hidden" style={{ height: '500px' }}>
      {/* Mock Street View Background */}
      <div className="absolute inset-0 bg-gradient-to-br from-blue-100 via-green-50 to-yellow-50">
        {/* Mock construction site elements */}
        <div className="absolute inset-0 opacity-60">
          {/* Sky gradient */}
          <div className="h-1/2 bg-gradient-to-b from-blue-300 to-blue-100"></div>
          {/* Ground */}
          <div className="h-1/2 bg-gradient-to-t from-yellow-200 to-green-100"></div>
        </div>
        
        {/* Mock construction elements based on location */}
        <div className="absolute inset-0 flex items-center justify-center">
          <div className="text-center text-gray-700">
            <div className="mb-4">
              <div className="w-32 h-20 mx-auto bg-gray-400 rounded mb-2 opacity-80"></div>
              <div className="w-20 h-16 mx-auto bg-yellow-500 rounded opacity-70"></div>
            </div>
            <h3 className="text-lg font-bold mb-2">Historical Street View</h3>
            <div className="space-y-1 text-sm">
              <p>{historicalWaypoints.find(wp => Math.abs(wp.x - currentLocation.x) < 10 && Math.abs(wp.y - currentLocation.y) < 10)?.name || 'Construction Site'}</p>
              <p>{formatDate(selectedDate)} at {selectedTime}</p>
              <div className="flex items-center justify-center space-x-4 text-xs mt-3">
                <span>Heading: {formatHeading(currentLocation.heading)}</span>
                <span>Zoom: {currentLocation.zoom.toFixed(1)}x</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Navigation Overlay */}
      {showOverlay && overlayType === 'navigation' && (
        <div className="absolute inset-0 pointer-events-none">
          {/* Compass */}
          <div className="absolute top-4 right-4 w-16 h-16 bg-black/50 rounded-full flex items-center justify-center">
            <div 
              className="w-6 h-6 text-white transform transition-transform"
              style={{ transform: `rotate(${currentLocation.heading}deg)` }}
            >
              <ChevronUp className="w-6 h-6" />
            </div>
          </div>
          
          {/* Field of view indicator */}
          <div className="absolute bottom-4 left-1/2 transform -translate-x-1/2">
            <div className="bg-black/50 text-white px-3 py-1 rounded-lg text-sm">
              FOV: {fieldOfView}°
            </div>
          </div>
        </div>
      )}

      {/* Street View Controls */}
      <div className="absolute bottom-4 right-4 flex flex-col space-y-2">
        <button
          onClick={() => zoomView('in')}
          className="p-2 bg-white/90 hover:bg-white rounded-lg shadow-sm transition-colors"
        >
          <ZoomIn className="w-4 h-4" />
        </button>
        <button
          onClick={() => zoomView('out')}
          className="p-2 bg-white/90 hover:bg-white rounded-lg shadow-sm transition-colors"
        >
          <ZoomOut className="w-4 h-4" />
        </button>
        <button className="p-2 bg-white/90 hover:bg-white rounded-lg shadow-sm transition-colors">
          <Maximize2 className="w-4 h-4" />
        </button>
      </div>

      {/* Movement Controls */}
      <div className="absolute left-4 bottom-4">
        <div className="grid grid-cols-3 gap-1">
          <div></div>
          <button
            onClick={() => moveLocation('up')}
            className="p-2 bg-white/90 hover:bg-white rounded-lg shadow-sm transition-colors"
          >
            <ArrowUp className="w-4 h-4" />
          </button>
          <div></div>
          <button
            onClick={() => moveLocation('left')}
            className="p-2 bg-white/90 hover:bg-white rounded-lg shadow-sm transition-colors"
          >
            <ArrowLeft className="w-4 h-4" />
          </button>
          <button className="p-2 bg-white/90 hover:bg-white rounded-lg shadow-sm transition-colors">
            <Crosshair className="w-4 h-4" />
          </button>
          <button
            onClick={() => moveLocation('right')}
            className="p-2 bg-white/90 hover:bg-white rounded-lg shadow-sm transition-colors"
          >
            <ArrowRight className="w-4 h-4" />
          </button>
          <div></div>
          <button
            onClick={() => moveLocation('down')}
            className="p-2 bg-white/90 hover:bg-white rounded-lg shadow-sm transition-colors"
          >
            <ArrowDown className="w-4 h-4" />
          </button>
          <div></div>
        </div>
      </div>

      {/* Rotation Controls */}
      <div className="absolute top-4 left-4 flex space-x-1">
        <button
          onClick={() => rotateView('left')}
          className="p-2 bg-white/90 hover:bg-white rounded-lg shadow-sm transition-colors"
        >
          <RotateCcw className="w-4 h-4" />
        </button>
        <button
          onClick={() => rotateView('right')}
          className="p-2 bg-white/90 hover:bg-white rounded-lg shadow-sm transition-colors"
        >
          <RotateCw className="w-4 h-4" />
        </button>
      </div>
    </div>
  );

  const MapOverview = () => (
    <div className="relative bg-gray-200 rounded-lg overflow-hidden" style={{ height: '300px' }}>
      {/* Mock Map Background */}
      <div className="absolute inset-0 bg-gradient-to-br from-green-100 to-blue-100">
        <div className="absolute inset-0 opacity-20">
          <div className="grid grid-cols-8 grid-rows-6 h-full">
            {Array.from({ length: 48 }).map((_, i) => (
              <div key={i} className="border border-gray-300"></div>
            ))}
          </div>
        </div>
      </div>

      {/* Waypoints */}
      {historicalWaypoints.map((waypoint, index) => (
        <div
          key={waypoint.id}
          className={`absolute w-4 h-4 rounded-full cursor-pointer transform -translate-x-1/2 -translate-y-1/2 ${
            waypoint.available ? 'bg-blue-600 hover:bg-blue-700' : 'bg-gray-400'
          } ${Math.abs(waypoint.x - currentLocation.x) < 5 && Math.abs(waypoint.y - currentLocation.y) < 5 ? 'ring-2 ring-white' : ''}`}
          style={{
            left: `${waypoint.x}%`,
            top: `${waypoint.y}%`
          }}
          onClick={() => goToWaypoint(waypoint)}
          title={`${waypoint.name} - ${waypoint.available ? 'Available' : 'No recording'}`}
        >
          <div className="w-full h-full rounded-full flex items-center justify-center text-white text-xs font-bold">
            {index + 1}
          </div>
        </div>
      ))}

      {/* Current Location */}
      <div
        className="absolute w-6 h-6 transform -translate-x-1/2 -translate-y-1/2"
        style={{
          left: `${currentLocation.x}%`,
          top: `${currentLocation.y}%`
        }}
      >
        <div className="w-6 h-6 bg-red-600 rounded-full animate-pulse relative">
          <div className="absolute inset-0 bg-red-600 rounded-full animate-ping"></div>
          {/* Direction indicator */}
          <div 
            className="absolute -top-2 left-1/2 w-0 h-0 border-l-2 border-r-2 border-b-4 border-l-transparent border-r-transparent border-b-red-600 transform -translate-x-1/2 transition-transform"
            style={{ transform: `translateX(-50%) rotate(${currentLocation.heading}deg)` }}
          ></div>
        </div>
      </div>

      {/* Map Controls */}
      <div className="absolute top-4 right-4 flex flex-col space-y-2">
        <button className="p-2 bg-white rounded-lg shadow-sm hover:shadow-md transition-shadow">
          <Target className="w-4 h-4" />
        </button>
        <button className="p-2 bg-white rounded-lg shadow-sm hover:shadow-md transition-shadow">
          <Layers className="w-4 h-4" />
        </button>
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
              <h1 className="text-xl font-bold text-gray-900">Historical Street View</h1>
              <div className="flex items-center space-x-2 text-sm text-gray-600">
                <Calendar className="w-3 h-3" />
                <span>{formatDate(selectedDate)}</span>
                <span>•</span>
                <Clock className="w-3 h-3" />
                <span>{selectedTime}</span>
                <span>•</span>
                <Locate className="w-3 h-3" />
                <span>Recording Available</span>
              </div>
            </div>

            <div className="flex items-center space-x-4">
              {/* View Mode Selector */}
              <div className="flex items-center space-x-2 bg-gray-100 rounded-lg p-1">
                {[
                  { key: 'street', label: 'Street View', icon: Navigation },
                  { key: 'map', label: 'Map View', icon: Map },
                  { key: 'hybrid', label: 'Hybrid', icon: Layers }
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
                <span>Export Path</span>
              </button>
            </div>
          </div>
        </div>

        {/* Time Controls */}
        <div className="bg-white border-b border-gray-200 px-6 py-4">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Date</label>
              <input
                type="date"
                value={selectedDate.toISOString().split('T')[0]}
                onChange={(e) => setSelectedDate(new Date(e.target.value))}
                className="w-full px-3 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:border-transparent"
                style={{ '--tw-ring-color': theme.primary[500] + '40' }}
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Time</label>
              <input
                type="time"
                value={selectedTime}
                onChange={(e) => setSelectedTime(e.target.value)}
                className="w-full px-3 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:border-transparent"
                style={{ '--tw-ring-color': theme.primary[500] + '40' }}
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Overlay</label>
              <select
                value={overlayType}
                onChange={(e) => setOverlayType(e.target.value)}
                className="w-full px-3 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:border-transparent"
              >
                <option value="navigation">Navigation</option>
                <option value="annotations">Annotations</option>
                <option value="measurements">Measurements</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Field of View</label>
              <input
                type="range"
                min="60"
                max="120"
                value={fieldOfView}
                onChange={(e) => setFieldOfView(Number(e.target.value))}
                className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
              />
              <div className="text-xs text-gray-500 mt-1">{fieldOfView}°</div>
            </div>
          </div>
        </div>

        {/* Main Content */}
        <div className="flex-1 overflow-auto">
          <div className="grid grid-cols-1 xl:grid-cols-4 gap-6 p-6">
            {/* Street View Area */}
            <div className="xl:col-span-3 space-y-6">
              <StreetViewDisplay />

              {/* Map Overview */}
              <div className="bg-white rounded-lg p-6 shadow-sm border border-gray-100">
                <div className="flex items-center justify-between mb-4">
                  <h2 className="font-semibold text-gray-900">Site Overview</h2>
                  <div className="flex items-center space-x-2">
                    <button
                      onClick={() => setShowOverlay(!showOverlay)}
                      className="p-2 hover:bg-gray-100 rounded-lg"
                    >
                      {showOverlay ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                    </button>
                  </div>
                </div>
                <MapOverview />
              </div>

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
                      Path Recording: Construction Progress Review
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
                        <option value={0.5}>0.5x</option>
                        <option value={1}>1x</option>
                        <option value={2}>2x</option>
                        <option value={4}>4x</option>
                      </select>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* Control Panel */}
            <div className="space-y-6">
              {/* Waypoints */}
              <div className="bg-white rounded-lg p-6 shadow-sm border border-gray-100">
                <h3 className="font-semibold text-gray-900 mb-4">Historical Waypoints</h3>
                <div className="space-y-3">
                  {historicalWaypoints.map((waypoint, index) => (
                    <div
                      key={waypoint.id}
                      onClick={() => goToWaypoint(waypoint)}
                      className={`p-3 rounded-lg border cursor-pointer transition-colors ${
                        waypoint.available 
                          ? 'border-gray-200 hover:border-blue-300 hover:bg-blue-50' 
                          : 'border-gray-100 bg-gray-50 cursor-not-allowed opacity-60'
                      }`}
                    >
                      <div className="flex items-center justify-between">
                        <div className="flex items-center space-x-3">
                          <div className={`w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold ${
                            waypoint.available ? 'bg-blue-600 text-white' : 'bg-gray-400 text-white'
                          }`}>
                            {index + 1}
                          </div>
                          <div>
                            <p className="font-medium text-gray-900">{waypoint.name}</p>
                            <p className="text-xs text-gray-600">{waypoint.description}</p>
                          </div>
                        </div>
                        {waypoint.available ? (
                          <Camera className="w-4 h-4 text-green-600" />
                        ) : (
                          <div className="w-4 h-4 rounded bg-gray-300"></div>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Path Recordings */}
              <div className="bg-white rounded-lg p-6 shadow-sm border border-gray-100">
                <h3 className="font-semibold text-gray-900 mb-4">Recorded Paths</h3>
                <div className="space-y-3">
                  {pathRecordings.map((path) => (
                    <div key={path.id} className="p-3 border border-gray-200 rounded-lg hover:bg-gray-50 cursor-pointer transition-colors">
                      <div className="flex items-start justify-between">
                        <div>
                          <h4 className="font-medium text-gray-900">{path.name}</h4>
                          <div className="text-xs text-gray-600 mt-1 space-y-1">
                            <p>Inspector: {path.inspector}</p>
                            <p>Duration: {path.duration}</p>
                            <p>{path.waypoints} waypoints • {path.distance}</p>
                          </div>
                        </div>
                        <div className="flex items-center space-x-2">
                          <Play className="w-4 h-4 text-blue-600" />
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Current Position Info */}
              <div className="bg-white rounded-lg p-6 shadow-sm border border-gray-100">
                <h3 className="font-semibold text-gray-900 mb-4">Current Position</h3>
                <div className="space-y-3">
                  <div className="flex justify-between">
                    <span className="text-gray-600">Location:</span>
                    <span className="font-medium">Zone A - Foundation</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Heading:</span>
                    <span className="font-medium">{formatHeading(currentLocation.heading)}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Zoom:</span>
                    <span className="font-medium">{currentLocation.zoom.toFixed(1)}x</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Field of View:</span>
                    <span className="font-medium">{fieldOfView}°</span>
                  </div>
                </div>
              </div>

              {/* Quick Actions */}
              <div className="bg-white rounded-lg p-6 shadow-sm border border-gray-100">
                <h3 className="font-semibold text-gray-900 mb-4">Quick Actions</h3>
                <div className="space-y-3">
                  <button
                    onClick={() => navigate('/street-comparison')}
                    className="w-full flex items-center space-x-3 p-3 text-left bg-blue-50 hover:bg-blue-100 rounded-lg transition-colors"
                  >
                    <Grid3X3 className="w-5 h-5 text-blue-600" />
                    <div>
                      <div className="font-medium text-blue-900">Compare Views</div>
                      <div className="text-xs text-blue-600">Side-by-side comparison</div>
                    </div>
                  </button>
                  
                  <button
                    onClick={() => navigate('/field-assessment')}
                    className="w-full flex items-center space-x-3 p-3 text-left bg-green-50 hover:bg-green-100 rounded-lg transition-colors"
                  >
                    <Route className="w-5 h-5 text-green-600" />
                    <div>
                      <div className="font-medium text-green-900">Field Assessment</div>
                      <div className="text-xs text-green-600">Live mobile view</div>
                    </div>
                  </button>
                  
                  <button className="w-full flex items-center space-x-3 p-3 text-left bg-purple-50 hover:bg-purple-100 rounded-lg transition-colors">
                    <Share2 className="w-5 h-5 text-purple-600" />
                    <div>
                      <div className="font-medium text-purple-900">Share View</div>
                      <div className="text-xs text-purple-600">Export current position</div>
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

export default HistoricalStreetView;