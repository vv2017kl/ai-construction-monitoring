import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  Navigation, MapPin, Play, Pause, Volume2, VolumeX, 
  RotateCcw, ArrowUp, ArrowDown, ArrowLeft, ArrowRight,
  Clock, Users, Shield, AlertTriangle, Camera, Compass,
  Route, PhoneCall, StopCircle, Zap
} from 'lucide-react';
import { useTheme } from '../../context/ThemeContext';
import MainLayout from '../../components/shared/Layout/MainLayout';
import { mockRoutes, mockSites, mockUser, mockCameras } from '../../data/mockData';

const LiveStreetView = () => {
  const navigate = useNavigate();
  const { theme } = useTheme();
  const [selectedRoute, setSelectedRoute] = useState(mockRoutes[0].id);
  const [isNavigating, setIsNavigating] = useState(false);
  const [currentWaypoint, setCurrentWaypoint] = useState(0);
  const [audioGuidance, setAudioGuidance] = useState(true);
  const [currentCamera, setCurrentCamera] = useState(mockCameras[0].id);

  const currentSite = mockSites.find(s => s.name === mockUser.currentSite) || mockSites[0];
  const activeRoute = mockRoutes.find(r => r.id === selectedRoute);

  // Simulate GPS navigation progress
  useEffect(() => {
    if (!isNavigating) return;

    const interval = setInterval(() => {
      setCurrentWaypoint(prev => {
        const next = prev + 1;
        if (next >= activeRoute.waypoints.length) {
          setIsNavigating(false);
          return 0;
        }
        return next;
      });
    }, 5000); // Change waypoint every 5 seconds for demo

    return () => clearInterval(interval);
  }, [isNavigating, activeRoute?.waypoints.length]);

  const startNavigation = () => {
    setIsNavigating(true);
    setCurrentWaypoint(0);
  };

  const stopNavigation = () => {
    setIsNavigating(false);
    setCurrentWaypoint(0);
  };

  const emergencyStop = () => {
    setIsNavigating(false);
    alert('Emergency stop activated! Site manager has been notified.');
  };

  const RouteCard = ({ route, isSelected, onClick }) => (
    <div
      onClick={onClick}
      className={`p-4 rounded-lg border-2 cursor-pointer transition-all ${
        isSelected
          ? 'border-blue-500 bg-blue-50'
          : 'border-gray-200 hover:border-gray-300 bg-white'
      }`}
    >
      <div className="flex items-center justify-between mb-2">
        <h3 className="font-semibold text-gray-900">{route.name}</h3>
        <span className="text-xs text-gray-500">{route.code}</span>
      </div>
      <div className="text-sm text-gray-600 mb-3">{route.description || 'Route description'}</div>
      
      <div className="grid grid-cols-3 gap-2 text-xs">
        <div className="text-center p-2 bg-gray-50 rounded">
          <Clock className="w-3 h-3 mx-auto mb-1 text-gray-600" />
          <div className="font-medium">{route.estimatedDuration}min</div>
        </div>
        <div className="text-center p-2 bg-gray-50 rounded">
          <Route className="w-3 h-3 mx-auto mb-1 text-gray-600" />
          <div className="font-medium">{route.totalDistance}m</div>
        </div>
        <div className="text-center p-2 bg-green-50 rounded">
          <div className="font-medium text-green-600">{route.completionRate}%</div>
          <div className="text-gray-600">Success</div>
        </div>
      </div>
    </div>
  );

  const WaypointStatus = () => {
    if (!activeRoute || !isNavigating) return null;

    const waypoint = activeRoute.waypoints[currentWaypoint];
    const isLastWaypoint = currentWaypoint === activeRoute.waypoints.length - 1;

    return (
      <div className="bg-white rounded-lg p-6 shadow-sm border border-gray-200">
        <div className="flex items-center justify-between mb-4">
          <h3 className="font-semibold text-gray-900">Current Waypoint</h3>
          <span className="text-sm text-gray-500">
            {currentWaypoint + 1} of {activeRoute.waypoints.length}
          </span>
        </div>

        {waypoint && (
          <div className="space-y-4">
            <div className="p-4 bg-blue-50 rounded-lg">
              <div className="flex items-center space-x-2 mb-2">
                <MapPin className="w-5 h-5 text-blue-600" />
                <h4 className="font-medium text-blue-900">{waypoint.name}</h4>
              </div>
              <p className="text-sm text-blue-700">{waypoint.instructions}</p>
            </div>

            {/* GPS Simulation */}
            <div className="grid grid-cols-2 gap-4">
              <div className="text-center p-3 bg-gray-50 rounded-lg">
                <div className="text-xs text-gray-600 mb-1">Distance Remaining</div>
                <div className="font-bold text-gray-900">
                  {Math.max(0, (activeRoute.waypoints.length - currentWaypoint - 1) * 150)}m
                </div>
              </div>
              <div className="text-center p-3 bg-gray-50 rounded-lg">
                <div className="text-xs text-gray-600 mb-1">Estimated Time</div>
                <div className="font-bold text-gray-900">
                  {Math.max(1, (activeRoute.waypoints.length - currentWaypoint - 1) * 2)}min
                </div>
              </div>
            </div>

            {/* Next Instruction */}
            {!isLastWaypoint && (
              <div className="p-3 bg-green-50 border border-green-200 rounded-lg">
                <div className="flex items-center space-x-2">
                  <ArrowUp className="w-4 h-4 text-green-600" />
                  <span className="text-sm font-medium text-green-800">
                    Next: {activeRoute.waypoints[currentWaypoint + 1]?.name}
                  </span>
                </div>
              </div>
            )}

            {isLastWaypoint && (
              <div className="p-3 bg-yellow-50 border border-yellow-200 rounded-lg">
                <div className="flex items-center space-x-2">
                  <Shield className="w-4 h-4 text-yellow-600" />
                  <span className="text-sm font-medium text-yellow-800">
                    Final checkpoint reached! Route complete.
                  </span>
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    );
  };

  const CameraView = () => (
    <div className="bg-gray-900 rounded-lg aspect-video flex items-center justify-center relative overflow-hidden">
      {/* Simulated Street-Level Camera View */}
      <div className="absolute inset-0 bg-gradient-to-b from-sky-300 via-gray-200 to-yellow-200 opacity-70"></div>
      <div className="absolute bottom-0 left-0 right-0 h-1/2 bg-gradient-to-t from-gray-600 to-gray-400 opacity-50"></div>
      
      {/* Construction Site Elements */}
      <div className="absolute bottom-1/4 left-1/4 w-8 h-8 bg-orange-400 rounded opacity-80"></div>
      <div className="absolute bottom-1/3 right-1/3 w-6 h-6 bg-yellow-400 rounded opacity-80"></div>
      
      {/* Street View Overlay */}
      <div className="absolute top-4 left-4 bg-black/70 text-white text-sm px-3 py-1 rounded">
        📍 STREET VIEW
      </div>
      
      {/* Camera Info */}
      <div className="absolute bottom-4 left-4 bg-black/70 text-white text-xs px-2 py-1 rounded">
        Camera: {mockCameras.find(c => c.id === currentCamera)?.name || 'Mobile View'}
      </div>

      {/* Navigation Arrow Overlay */}
      {isNavigating && (
        <div className="absolute inset-0 flex items-center justify-center">
          <div className="bg-green-500/80 p-4 rounded-full">
            <ArrowUp className="w-8 h-8 text-white transform rotate-45" />
          </div>
        </div>
      )}
    </div>
  );

  return (
    <MainLayout portal="solution-user">
      <div className="h-full flex flex-col">
        {/* Header */}
        <div className="bg-white border-b border-gray-200 px-6 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-xl font-bold text-gray-900">Live Street View Navigation</h1>
              <div className="flex items-center space-x-2 text-sm text-gray-600">
                <MapPin className="w-3 h-3" />
                <span>{currentSite.name}</span>
                <span>•</span>
                <span>{isNavigating ? 'Navigating' : 'Ready'}</span>
                {audioGuidance && (
                  <>
                    <span>•</span>
                    <Volume2 className="w-3 h-3" />
                    <span>Audio On</span>
                  </>
                )}
              </div>
            </div>

            {/* Controls */}
            <div className="flex items-center space-x-3">
              <button
                onClick={() => setAudioGuidance(!audioGuidance)}
                className={`p-2 rounded-lg transition-colors ${
                  audioGuidance 
                    ? 'bg-blue-100 text-blue-600' 
                    : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                }`}
              >
                {audioGuidance ? <Volume2 className="w-4 h-4" /> : <VolumeX className="w-4 h-4" />}
              </button>

              {isNavigating ? (
                <button
                  onClick={stopNavigation}
                  className="flex items-center space-x-2 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
                >
                  <Pause className="w-4 h-4" />
                  <span>Stop Navigation</span>
                </button>
              ) : (
                <button
                  onClick={startNavigation}
                  className="flex items-center space-x-2 px-4 py-2 text-white rounded-lg hover:opacity-90 transition-colors"
                  style={{ backgroundColor: theme.primary[500] }}
                  disabled={!selectedRoute}
                >
                  <Play className="w-4 h-4" />
                  <span>Start Navigation</span>
                </button>
              )}

              <button
                onClick={emergencyStop}
                className="flex items-center space-x-2 px-4 py-2 bg-red-700 text-white rounded-lg hover:bg-red-800 transition-colors"
              >
                <StopCircle className="w-4 h-4" />
                <span>EMERGENCY</span>
              </button>
            </div>
          </div>
        </div>

        {/* Main Content */}
        <div className="flex-1 flex overflow-hidden">
          {/* Camera View - Main Area */}
          <div className="flex-1 p-6">
            <div className="h-full flex flex-col space-y-6">
              <CameraView />
              
              {/* Navigation Status */}
              {isNavigating && <WaypointStatus />}
              
              {/* Compass and Controls */}
              <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
                <div className="bg-white p-4 rounded-lg border border-gray-200 text-center">
                  <Compass className="w-8 h-8 mx-auto mb-2 text-blue-600" />
                  <div className="text-sm font-medium text-gray-900">Heading</div>
                  <div className="text-lg font-bold text-blue-600">NE</div>
                </div>
                
                <div className="bg-white p-4 rounded-lg border border-gray-200 text-center">
                  <Users className="w-8 h-8 mx-auto mb-2 text-green-600" />
                  <div className="text-sm font-medium text-gray-900">Personnel</div>
                  <div className="text-lg font-bold text-green-600">3</div>
                </div>
                
                <div className="bg-white p-4 rounded-lg border border-gray-200 text-center">
                  <Shield className="w-8 h-8 mx-auto mb-2 text-orange-600" />
                  <div className="text-sm font-medium text-gray-900">PPE Status</div>
                  <div className="text-lg font-bold text-orange-600">95%</div>
                </div>
                
                <div className="bg-white p-4 rounded-lg border border-gray-200 text-center">
                  <AlertTriangle className="w-8 h-8 mx-auto mb-2 text-red-600" />
                  <div className="text-sm font-medium text-gray-900">Alerts</div>
                  <div className="text-lg font-bold text-red-600">0</div>
                </div>
              </div>
            </div>
          </div>

          {/* Right Panel - Route Selection */}
          <div className="w-80 bg-gray-50 border-l border-gray-200 p-6 space-y-6 overflow-y-auto">
            <div className="bg-white rounded-lg p-4 border border-gray-200">
              <h3 className="font-semibold text-gray-900 mb-4">Available Routes</h3>
              <div className="space-y-3">
                {mockRoutes.map((route) => (
                  <RouteCard
                    key={route.id}
                    route={route}
                    isSelected={selectedRoute === route.id}
                    onClick={() => setSelectedRoute(route.id)}
                  />
                ))}
              </div>
            </div>

            {/* Quick Actions */}
            <div className="bg-white rounded-lg p-4 border border-gray-200">
              <h3 className="font-semibold text-gray-900 mb-3">Quick Actions</h3>
              <div className="space-y-2">
                <button
                  onClick={() => navigate('/live-view')}
                  className="w-full flex items-center space-x-3 p-3 text-left bg-blue-50 hover:bg-blue-100 rounded-lg transition-colors"
                >
                  <Camera className="w-5 h-5 text-blue-600" />
                  <div>
                    <div className="font-medium text-blue-900">Live Cameras</div>
                    <div className="text-xs text-blue-600">View all camera feeds</div>
                  </div>
                </button>
                
                <button
                  onClick={() => navigate('/alert-center')}
                  className="w-full flex items-center space-x-3 p-3 text-left bg-red-50 hover:bg-red-100 rounded-lg transition-colors"
                >
                  <AlertTriangle className="w-5 h-5 text-red-600" />
                  <div>
                    <div className="font-medium text-red-900">Alert Center</div>
                    <div className="text-xs text-red-600">Manage active alerts</div>
                  </div>
                </button>

                <button
                  className="w-full flex items-center space-x-3 p-3 text-left bg-green-50 hover:bg-green-100 rounded-lg transition-colors"
                  onClick={() => window.open('tel:+15551234567')}
                >
                  <PhoneCall className="w-5 h-5 text-green-600" />
                  <div>
                    <div className="font-medium text-green-900">Site Manager</div>
                    <div className="text-xs text-green-600">Call for assistance</div>
                  </div>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </MainLayout>
  );
};

export default LiveStreetView;