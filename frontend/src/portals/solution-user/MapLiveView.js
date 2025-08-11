import React, { useState, useEffect, useContext } from 'react';
import { useParams, useNavigate, useSearchParams } from 'react-router-dom';
import MainLayout from '../../components/Layout/MainLayout';
import { useTheme } from '../../context/ThemeContext';
import { mockCameras, mockSites } from '../../data/cesiumMockData';
import { 
  ArrowLeft, MapPin, Camera, AlertTriangle, Maximize, 
  Minimize, Volume2, VolumeX, RotateCcw, Settings,
  Home, Navigation, Fullscreen, ExitFullscreen
} from 'lucide-react';

const MapLiveView = () => {
  const { cameraId } = useParams();
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const { theme } = useTheme();
  
  // Get parameters from URL
  const mapContext = searchParams.get('mapContext') === 'true';
  const sidebarCollapsed = searchParams.get('sidebar') === 'collapsed';
  
  // Component state
  const [isFullscreen, setIsFullscreen] = useState(false);
  const [isMuted, setIsMuted] = useState(false);
  const [showControls, setShowControls] = useState(true);
  const [streamQuality, setStreamQuality] = useState('high');
  
  // Find camera and site data
  const findCameraAndSite = () => {
    for (const [siteId, cameras] of Object.entries(mockCameras)) {
      const camera = cameras.find(c => c.id === cameraId);
      if (camera) {
        const site = mockSites.find(s => s.id === siteId);
        return { camera, site };
      }
    }
    return { camera: null, site: null };
  };

  const { camera, site } = findCameraAndSite();

  // Handle back navigation
  const handleBackToMap = () => {
    if (mapContext) {
      navigate('/cesium-dashboard');
    } else {
      navigate('/live-view');
    }
  };

  // Toggle fullscreen
  const toggleFullscreen = () => {
    setIsFullscreen(!isFullscreen);
  };

  // Auto-hide controls
  useEffect(() => {
    if (!showControls) return;
    
    const timer = setTimeout(() => {
      setShowControls(false);
    }, 3000);
    
    return () => clearTimeout(timer);
  }, [showControls]);

  // Show controls on mouse move
  const handleMouseMove = () => {
    setShowControls(true);
  };

  if (!camera || !site) {
    return (
      <MainLayout showSidebar={!sidebarCollapsed}>
        <div className="flex items-center justify-center h-full">
          <div className="text-center">
            <Camera className="w-16 h-16 text-gray-400 mx-auto mb-4" />
            <h2 className="text-xl font-semibold text-gray-900 mb-2">Camera Not Found</h2>
            <p className="text-gray-600 mb-4">The requested camera could not be found.</p>
            <button
              onClick={handleBackToMap}
              className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
            >
              {mapContext ? 'Back to Map' : 'Back to Live View'}
            </button>
          </div>
        </div>
      </MainLayout>
    );
  }

  return (
    <MainLayout 
      showSidebar={!sidebarCollapsed && !isFullscreen}
      className={isFullscreen ? 'fixed inset-0 z-50 bg-black' : ''}
    >
      <div 
        className={`relative ${isFullscreen ? 'h-screen w-screen' : 'h-full w-full'} bg-black`}
        onMouseMove={handleMouseMove}
      >
        {/* Header Controls */}
        <div className={`absolute top-0 left-0 right-0 z-30 transition-opacity duration-300 ${
          showControls || !isFullscreen ? 'opacity-100' : 'opacity-0'
        }`}>
          <div className="bg-gradient-to-b from-black/70 to-transparent p-4">
            <div className="flex items-center justify-between text-white">
              {/* Left: Back and Camera Info */}
              <div className="flex items-center space-x-4">
                <button
                  onClick={handleBackToMap}
                  className="flex items-center space-x-2 px-3 py-2 bg-black/50 hover:bg-black/70 rounded-lg transition-all"
                >
                  <ArrowLeft className="w-4 h-4" />
                  <span>{mapContext ? 'Back to Map' : 'Back to Live View'}</span>
                </button>
                
                <div className="flex items-center space-x-3">
                  <div className="w-3 h-3 bg-red-500 rounded-full animate-pulse"></div>
                  <div>
                    <h1 className="text-lg font-semibold">{camera.name}</h1>
                    <p className="text-sm text-gray-300">{site.name} • {site.city}, {site.country}</p>
                  </div>
                </div>
              </div>

              {/* Right: Controls */}
              <div className="flex items-center space-x-2">
                <button
                  onClick={() => navigate('/dashboard')}
                  className="p-2 bg-black/50 hover:bg-black/70 rounded-lg transition-all"
                  title="Dashboard"
                >
                  <Home className="w-5 h-5" />
                </button>
                
                <button
                  onClick={toggleFullscreen}
                  className="p-2 bg-black/50 hover:bg-black/70 rounded-lg transition-all"
                  title={isFullscreen ? 'Exit Fullscreen' : 'Fullscreen'}
                >
                  {isFullscreen ? <ExitFullscreen className="w-5 h-5" /> : <Fullscreen className="w-5 h-5" />}
                </button>
              </div>
            </div>
          </div>
        </div>

        {/* Main Video Container */}
        <div className="h-full w-full flex items-center justify-center">
          {/* Mock Video Feed */}
          <div className="relative w-full h-full bg-gray-900 flex items-center justify-center">
            {/* Simulated video feed placeholder */}
            <div className="text-center text-white">
              <Camera className="w-24 h-24 mx-auto mb-4 text-gray-400" />
              <h3 className="text-xl font-semibold mb-2">Live Stream: {camera.name}</h3>
              <p className="text-gray-400 mb-4">Camera ID: {camera.zoneminder_monitor_id}</p>
              <div className="bg-green-600 text-white px-3 py-1 rounded-full text-sm inline-block">
                🔴 LIVE • {streamQuality.toUpperCase()}
              </div>
            </div>

            {/* Camera Status Overlay */}
            <div className="absolute top-4 right-4">
              <div className={`px-3 py-1 rounded-full text-xs font-medium ${
                camera.status === 'critical' ? 'bg-red-500 text-white' :
                camera.status === 'warning' ? 'bg-orange-500 text-white' :
                camera.status === 'normal' ? 'bg-green-500 text-white' :
                'bg-gray-500 text-white'
              }`}>
                {camera.status.toUpperCase()}
              </div>
            </div>

            {/* Active Alerts Indicator */}
            {camera.alerts?.active > 0 && (
              <div className="absolute top-4 left-4">
                <div className="bg-red-500 text-white px-3 py-2 rounded-lg flex items-center space-x-2">
                  <AlertTriangle className="w-4 h-4" />
                  <span className="text-sm font-medium">
                    {camera.alerts.active} Active Alert{camera.alerts.active > 1 ? 's' : ''}
                  </span>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Bottom Controls */}
        <div className={`absolute bottom-0 left-0 right-0 z-30 transition-opacity duration-300 ${
          showControls || !isFullscreen ? 'opacity-100' : 'opacity-0'
        }`}>
          <div className="bg-gradient-to-t from-black/70 to-transparent p-4">
            <div className="flex items-center justify-center space-x-4">
              {/* Stream Quality */}
              <select
                value={streamQuality}
                onChange={(e) => setStreamQuality(e.target.value)}
                className="bg-black/50 text-white border border-gray-600 rounded px-3 py-1 text-sm"
              >
                <option value="high">High Quality</option>
                <option value="medium">Medium Quality</option>
                <option value="low">Low Quality</option>
              </select>

              {/* Audio Toggle */}
              <button
                onClick={() => setIsMuted(!isMuted)}
                className={`p-2 rounded-lg transition-all ${
                  isMuted ? 'bg-red-500/20 text-red-400' : 'bg-black/50 text-white hover:bg-black/70'
                }`}
                title={isMuted ? 'Unmute' : 'Mute'}
              >
                {isMuted ? <VolumeX className="w-5 h-5" /> : <Volume2 className="w-5 h-5" />}
              </button>

              {/* Refresh Stream */}
              <button
                className="p-2 bg-black/50 hover:bg-black/70 text-white rounded-lg transition-all"
                title="Refresh Stream"
              >
                <RotateCcw className="w-5 h-5" />
              </button>

              {/* Camera Settings */}
              <button
                className="p-2 bg-black/50 hover:bg-black/70 text-white rounded-lg transition-all"
                title="Camera Settings"
              >
                <Settings className="w-5 h-5" />
              </button>

              {/* View on Map */}
              {mapContext && (
                <button
                  onClick={() => navigate(`/cesium-dashboard?camera=${cameraId}`)}
                  className="flex items-center space-x-2 px-3 py-2 bg-blue-600/80 hover:bg-blue-600 text-white rounded-lg transition-all"
                >
                  <MapPin className="w-4 h-4" />
                  <span>View on Map</span>
                </button>
              )}
            </div>
          </div>
        </div>

        {/* Camera Information Panel */}
        {!isFullscreen && (
          <div className="absolute top-20 right-4 w-80 bg-white rounded-lg shadow-xl border border-gray-200 z-20">
            <div className="p-4">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Camera Details</h3>
              
              <div className="space-y-3 text-sm">
                <div className="flex justify-between">
                  <span className="text-gray-600">Type:</span>
                  <span className="font-medium capitalize">{camera.type}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Status:</span>
                  <span className={`font-medium ${
                    camera.status === 'critical' ? 'text-red-600' :
                    camera.status === 'warning' ? 'text-orange-600' :
                    camera.status === 'normal' ? 'text-green-600' :
                    'text-gray-600'
                  }`}>
                    {camera.status.charAt(0).toUpperCase() + camera.status.slice(1)}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Field of View:</span>
                  <span className="font-medium">{camera.field_of_view}°</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Technical Status:</span>
                  <span className={`font-medium ${
                    camera.technical_status === 'online' ? 'text-green-600' : 'text-red-600'
                  }`}>
                    {camera.technical_status.charAt(0).toUpperCase() + camera.technical_status.slice(1)}
                  </span>
                </div>
              </div>

              {camera.alerts?.active > 0 && (
                <div className="mt-4 p-3 bg-red-50 border border-red-200 rounded-lg">
                  <div className="flex items-center space-x-2 mb-2">
                    <AlertTriangle className="w-4 h-4 text-red-600" />
                    <span className="text-sm font-medium text-red-800">Active Alerts</span>
                  </div>
                  <p className="text-sm text-red-700">{camera.alerts.alert_type}</p>
                  <p className="text-xs text-red-600 mt-1">
                    Last: {new Date(camera.alerts.last_alert).toLocaleString()}
                  </p>
                </div>
              )}

              <div className="mt-4 pt-4 border-t border-gray-200">
                <button
                  onClick={() => navigate(`/alert-center?camera=${cameraId}`)}
                  className="w-full bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors text-sm font-medium"
                >
                  View Alert History
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Loading Indicator */}
        <div className="absolute inset-0 flex items-center justify-center bg-black/50 opacity-0 pointer-events-none transition-opacity duration-300">
          <div className="bg-white rounded-lg p-4 flex items-center space-x-3">
            <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-600"></div>
            <span className="text-gray-700">Loading stream...</span>
          </div>
        </div>
      </div>
    </MainLayout>
  );
};

export default MapLiveView;