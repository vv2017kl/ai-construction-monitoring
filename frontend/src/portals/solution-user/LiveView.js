import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  Grid3X3, Grid2X2, Square, Maximize2, Camera, 
  Play, Pause, Volume2, VolumeX, RotateCcw, ZoomIn, ZoomOut,
  AlertTriangle, CheckCircle, Settings, Download, Fullscreen,
  Users, HardHat, Car, Wrench, Eye, MapPin, Clock, 
  ArrowUp, ArrowDown, ArrowLeft, ArrowRight, RotateCw
} from 'lucide-react';
import { useTheme } from '../../context/ThemeContext';
import MainLayout from '../../components/shared/Layout/MainLayout';
import { mockCameras, mockDetections, mockSites, mockUser, mockAlerts } from '../../data/mockData';

const LiveView = () => {
  const navigate = useNavigate();
  const { theme } = useTheme();
  const [gridLayout, setGridLayout] = useState('2x2'); // '1x1', '2x2', '3x3', '4x4'
  const [selectedCamera, setSelectedCamera] = useState(mockCameras[0].id);
  const [fullscreenCamera, setFullscreenCamera] = useState(null);
  const [showAIOverlay, setShowAIOverlay] = useState(true);
  const [audioEnabled, setAudioEnabled] = useState(false);
  const [ptzActive, setPtzActive] = useState(null);
  
  // New state for enhanced functionality
  const [showCameraSettings, setShowCameraSettings] = useState(false);
  const [selectedCameraForSettings, setSelectedCameraForSettings] = useState(null);
  const [recordingCameras, setRecordingCameras] = useState(new Set());
  const [showDetectionDetail, setShowDetectionDetail] = useState(false);
  const [selectedDetection, setSelectedDetection] = useState(null);
  const [cameraPTZSettings, setCameraPTZSettings] = useState({});

  const currentSite = mockSites.find(s => s.name === mockUser.currentSite) || mockSites[0];

  // Simulate live detections updates
  const [liveDetections, setLiveDetections] = useState(mockDetections);
  useEffect(() => {
    const interval = setInterval(() => {
      setLiveDetections(prev => prev.map(detection => ({
        ...detection,
        personCount: Math.max(0, detection.personCount + Math.floor(Math.random() * 3 - 1)),
        ppeCompliance: Math.max(70, Math.min(100, detection.ppeCompliance + Math.floor(Math.random() * 10 - 5))),
        timestamp: new Date().toISOString()
      })));
    }, 3000);
    return () => clearInterval(interval);
  }, []);

  // PTZ Control Functions
  const handlePTZControl = (cameraId, direction) => {
    setPtzActive(cameraId);
    console.log(`PTZ Control: Camera ${cameraId} moving ${direction}`);
    setTimeout(() => setPtzActive(null), 1000);
  };

  const handleZoom = (cameraId, zoomIn) => {
    console.log(`Zoom: Camera ${cameraId} ${zoomIn ? 'zoom in' : 'zoom out'}`);
  };

  // Recording Functions
  const toggleRecording = (cameraId) => {
    setRecordingCameras(prev => {
      const newSet = new Set(prev);
      if (newSet.has(cameraId)) {
        newSet.delete(cameraId);
        console.log(`Recording stopped for camera ${cameraId}`);
      } else {
        newSet.add(cameraId);
        console.log(`Recording started for camera ${cameraId}`);
      }
      return newSet;
    });
  };

  // Camera Settings Functions
  const openCameraSettings = (camera) => {
    setSelectedCameraForSettings(camera);
    setShowCameraSettings(true);
  };

  // Detection Detail Functions
  const showDetectionDetails = (detection) => {
    setSelectedDetection(detection);
    setShowDetectionDetail(true);
  };

  const gridLayouts = {
    '1x1': { cols: 1, rows: 1 },
    '2x2': { cols: 2, rows: 2 },
    '3x3': { cols: 3, rows: 3 },
    '4x4': { cols: 4, rows: 4 }
  };

  const getCamerasForGrid = () => {
    const layout = gridLayouts[gridLayout];
    const totalSlots = layout.cols * layout.rows;
    return mockCameras.slice(0, Math.min(totalSlots, mockCameras.length));
  };

  const CameraFeed = ({ camera, isSelected, onClick, detection }) => {
    const isOnline = camera.status === 'online';
    
    return (
      <div 
        className={`relative bg-gray-900 rounded-lg overflow-hidden cursor-pointer border-2 transition-all duration-200 ${
          isSelected ? `border-blue-500` : 'border-gray-600 hover:border-gray-400'
        }`}
        onClick={onClick}
        style={{ aspectRatio: '16/9' }}
      >
        {/* Video Stream Placeholder */}
        <div className="absolute inset-0 bg-gradient-to-br from-gray-800 to-gray-900 flex items-center justify-center">
          {isOnline ? (
            <div className="relative w-full h-full bg-gray-700 flex items-center justify-center">
              {/* Simulated construction site scene */}
              <div className="absolute inset-0 bg-gradient-to-b from-blue-200 via-gray-300 to-amber-100 opacity-80"></div>
              <div className="absolute bottom-0 left-0 right-0 h-1/3 bg-gradient-to-t from-amber-600 to-amber-400 opacity-60"></div>
              
              {/* AI Detection Overlays */}
              {showAIOverlay && detection && (
                <>
                  {/* Person Detection Boxes */}
                  {Array.from({ length: detection.personCount }, (_, i) => (
                    <div
                      key={`person-${i}`}
                      className="absolute border-2 border-green-400 bg-green-400/20"
                      style={{
                        left: `${20 + i * 25}%`,
                        top: `${40 + (i % 2) * 15}%`,
                        width: '60px',
                        height: '80px'
                      }}
                    >
                      <div className="absolute -top-6 left-0 bg-green-400 text-black text-xs px-1 rounded">
                        Person {detection.confidence}
                      </div>
                    </div>
                  ))}
                  
                  {/* Equipment Detection Boxes */}
                  {detection.equipmentCount > 0 && (
                    <div
                      className="absolute border-2 border-orange-400 bg-orange-400/20"
                      style={{
                        right: '15%',
                        bottom: '25%',
                        width: '120px',
                        height: '60px'
                      }}
                    >
                      <div className="absolute -top-6 left-0 bg-orange-400 text-black text-xs px-1 rounded">
                        Equipment {detection.confidence}
                      </div>
                    </div>
                  )}
                </>
              )}
              
              {/* Camera Info Overlay */}
              <div className="absolute top-2 left-2 bg-black/60 text-white text-xs px-2 py-1 rounded">
                🔴 LIVE
              </div>
            </div>
          ) : (
            <div className="text-center text-gray-400">
              <Camera className="w-12 h-12 mx-auto mb-2 opacity-50" />
              <p className="text-sm">Camera Offline</p>
            </div>
          )}
        </div>

        {/* Camera Info Footer */}
        <div className="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/80 to-transparent p-3">
          <div className="flex items-center justify-between text-white text-sm">
            <div>
              <div className="font-semibold">{camera.name}</div>
              <div className="text-xs text-gray-300">{camera.location}</div>
            </div>
            <div className="flex items-center space-x-2">
              {camera.alerts > 0 && (
                <span className="bg-red-500 text-white text-xs px-2 py-0.5 rounded-full">
                  {camera.alerts}
                </span>
              )}
              <div className={`w-2 h-2 rounded-full ${isOnline ? 'bg-green-400' : 'bg-red-400'}`}></div>
            </div>
          </div>
        </div>

        {/* Fullscreen Button */}
        <button
          onClick={(e) => {
            e.stopPropagation();
            setFullscreenCamera(camera.id);
          }}
          className="absolute top-2 right-2 bg-black/60 hover:bg-black/80 text-white p-1 rounded transition-colors"
        >
          <Maximize2 className="w-4 h-4" />
        </button>
      </div>
    );
  };

  const PTZControls = ({ camera }) => {
    if (camera?.type !== 'ptz') return null;

    return (
      <div className="bg-white rounded-lg p-4 border border-gray-200">
        <h3 className="font-semibold text-gray-900 mb-3">PTZ Controls - {camera.name}</h3>
        <div className="grid grid-cols-3 gap-2">
          {/* PTZ Direction Controls */}
          <div></div>
          <button className="p-3 bg-gray-100 hover:bg-gray-200 rounded-lg transition-colors">
            <ArrowUp className="w-4 h-4 mx-auto" />
          </button>
          <div></div>
          
          <button className="p-3 bg-gray-100 hover:bg-gray-200 rounded-lg transition-colors">
            <ArrowLeft className="w-4 h-4 mx-auto" />
          </button>
          <button className="p-3 bg-gray-100 hover:bg-gray-200 rounded-lg transition-colors">
            <RotateCcw className="w-4 h-4 mx-auto" />
          </button>
          <button className="p-3 bg-gray-100 hover:bg-gray-200 rounded-lg transition-colors">
            <ArrowRight className="w-4 h-4 mx-auto" />
          </button>
          
          <div></div>
          <button className="p-3 bg-gray-100 hover:bg-gray-200 rounded-lg transition-colors">
            <ArrowDown className="w-4 h-4 mx-auto" />
          </button>
          <div></div>
        </div>

        {/* Zoom Controls */}
        <div className="mt-4 flex space-x-2">
          <button className="flex-1 flex items-center justify-center space-x-2 p-2 bg-gray-100 hover:bg-gray-200 rounded-lg transition-colors">
            <ZoomOut className="w-4 h-4" />
            <span className="text-sm">Zoom Out</span>
          </button>
          <button className="flex-1 flex items-center justify-center space-x-2 p-2 bg-gray-100 hover:bg-gray-200 rounded-lg transition-colors">
            <ZoomIn className="w-4 h-4" />
            <span className="text-sm">Zoom In</span>
          </button>
        </div>
      </div>
    );
  };

  const DetectionPanel = () => {
    const activeDetection = liveDetections.find(d => d.camera === selectedCamera);
    
    return (
      <div className="bg-white rounded-lg p-4 border border-gray-200">
        <h3 className="font-semibold text-gray-900 mb-4">Live Detection Analysis</h3>
        
        {activeDetection ? (
          <div className="space-y-4">
            {/* Detection Stats */}
            <div className="grid grid-cols-2 gap-4">
              <div className="text-center p-3 bg-blue-50 rounded-lg">
                <Users className="w-6 h-6 mx-auto mb-1 text-blue-600" />
                <div className="text-2xl font-bold text-blue-600">{activeDetection.personCount}</div>
                <div className="text-xs text-gray-600">Personnel</div>
              </div>
              
              <div className="text-center p-3 bg-green-50 rounded-lg">
                <HardHat className="w-6 h-6 mx-auto mb-1 text-green-600" />
                <div className="text-2xl font-bold text-green-600">{activeDetection.ppeCompliance}%</div>
                <div className="text-xs text-gray-600">PPE Compliance</div>
              </div>
              
              <div className="text-center p-3 bg-purple-50 rounded-lg">
                <Car className="w-6 h-6 mx-auto mb-1 text-purple-600" />
                <div className="text-2xl font-bold text-purple-600">{activeDetection.vehicleCount}</div>
                <div className="text-xs text-gray-600">Vehicles</div>
              </div>
              
              <div className="text-center p-3 bg-orange-50 rounded-lg">
                <Wrench className="w-6 h-6 mx-auto mb-1 text-orange-600" />
                <div className="text-2xl font-bold text-orange-600">{activeDetection.equipmentCount}</div>
                <div className="text-xs text-gray-600">Equipment</div>
              </div>
            </div>

            {/* Confidence Score */}
            <div className="p-3 bg-gray-50 rounded-lg">
              <div className="flex items-center justify-between mb-2">
                <span className="text-sm font-medium text-gray-700">AI Confidence</span>
                <span className="text-sm font-bold text-gray-900">
                  {Math.round(activeDetection.confidence * 100)}%
                </span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div 
                  className="h-2 rounded-full transition-all duration-300"
                  style={{ 
                    width: `${activeDetection.confidence * 100}%`,
                    backgroundColor: activeDetection.confidence > 0.8 ? theme.success[500] : 
                                   activeDetection.confidence > 0.6 ? theme.warning[500] : theme.danger[500]
                  }}
                ></div>
              </div>
            </div>

            {/* Safety Status */}
            <div className={`p-3 rounded-lg ${
              activeDetection.safetyViolations === 0 ? 'bg-green-50 border border-green-200' : 'bg-red-50 border border-red-200'
            }`}>
              <div className="flex items-center space-x-2">
                {activeDetection.safetyViolations === 0 ? (
                  <CheckCircle className="w-5 h-5 text-green-600" />
                ) : (
                  <AlertTriangle className="w-5 h-5 text-red-600" />
                )}
                <span className={`font-medium ${
                  activeDetection.safetyViolations === 0 ? 'text-green-800' : 'text-red-800'
                }`}>
                  {activeDetection.safetyViolations === 0 ? 'No Safety Violations' : `${activeDetection.safetyViolations} Safety Violations`}
                </span>
              </div>
            </div>
          </div>
        ) : (
          <div className="text-center text-gray-500 py-8">
            <Eye className="w-12 h-12 mx-auto mb-2 opacity-50" />
            <p>Select a camera to view detection data</p>
          </div>
        )}
      </div>
    );
  };

  const selectedCameraObj = mockCameras.find(c => c.id === selectedCamera);

  return (
    <MainLayout portal="solution-user">
      <div className="h-full flex flex-col">
        {/* Header Controls */}
        <div className="bg-white border-b border-gray-200 px-6 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-xl font-bold text-gray-900">Live Camera Monitoring</h1>
              <div className="flex items-center space-x-2 text-sm text-gray-600">
                <div className="flex items-center space-x-1">
                  <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                  <span>Live</span>
                </div>
                <span>•</span>
                <MapPin className="w-3 h-3" />
                <span>{currentSite.name}</span>
                <span>•</span>
                <span>{getCamerasForGrid().length} cameras active</span>
              </div>
            </div>

            {/* View Controls */}
            <div className="flex items-center space-x-4">
              {/* Grid Layout Selector */}
              <div className="flex items-center space-x-2 bg-gray-100 rounded-lg p-1">
                {Object.keys(gridLayouts).map((layout) => (
                  <button
                    key={layout}
                    onClick={() => setGridLayout(layout)}
                    className={`p-2 rounded-md transition-colors ${
                      gridLayout === layout 
                        ? 'bg-white shadow-sm' + ` text-[${theme.primary[500]}]`
                        : 'hover:bg-gray-200'
                    }`}
                    title={`${layout} Grid`}
                  >
                    {layout === '1x1' && <Square className="w-4 h-4" />}
                    {layout === '2x2' && <Grid2X2 className="w-4 h-4" />}
                    {layout === '3x3' && <Grid3X3 className="w-4 h-4" />}
                    {layout === '4x4' && <Grid3X3 className="w-4 h-4" />}
                  </button>
                ))}
              </div>

              {/* AI Overlay Toggle */}
              <label className="flex items-center space-x-2 cursor-pointer">
                <input
                  type="checkbox"
                  checked={showAIOverlay}
                  onChange={(e) => setShowAIOverlay(e.target.checked)}
                  className="rounded border-gray-300"
                  style={{ accentColor: theme.primary[500] }}
                />
                <span className="text-sm font-medium text-gray-700">AI Overlay</span>
              </label>

              {/* Audio Toggle */}
              <button
                onClick={() => setAudioEnabled(!audioEnabled)}
                className={`p-2 rounded-lg transition-colors ${
                  audioEnabled ? 'bg-blue-100 text-blue-600' : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                }`}
              >
                {audioEnabled ? <Volume2 className="w-4 h-4" /> : <VolumeX className="w-4 h-4" />}
              </button>

              {/* Quick Actions */}
              <button
                onClick={() => navigate('/alert-center')}
                className="flex items-center space-x-2 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
              >
                <AlertTriangle className="w-4 h-4" />
                <span>Alert Center</span>
                {mockAlerts.filter(a => a.status === 'open').length > 0 && (
                  <span className="bg-red-800 text-white text-xs px-2 py-0.5 rounded-full">
                    {mockAlerts.filter(a => a.status === 'open').length}
                  </span>
                )}
              </button>
            </div>
          </div>
        </div>

        {/* Main Content Area */}
        <div className="flex-1 flex overflow-hidden">
          {/* Camera Grid */}
          <div className="flex-1 p-6">
            <div 
              className={`grid gap-4 h-full`}
              style={{ 
                gridTemplateColumns: `repeat(${gridLayouts[gridLayout].cols}, 1fr)`,
                gridTemplateRows: `repeat(${gridLayouts[gridLayout].rows}, 1fr)`
              }}
            >
              {getCamerasForGrid().map((camera) => {
                const detection = liveDetections.find(d => d.camera === camera.id);
                return (
                  <CameraFeed
                    key={camera.id}
                    camera={camera}
                    detection={detection}
                    isSelected={selectedCamera === camera.id}
                    onClick={() => setSelectedCamera(camera.id)}
                  />
                );
              })}
            </div>
          </div>

          {/* Right Panel */}
          <div className="w-80 bg-gray-50 border-l border-gray-200 p-6 space-y-6 overflow-y-auto">
            {/* Detection Panel */}
            <DetectionPanel />
            
            {/* PTZ Controls */}
            <PTZControls camera={selectedCameraObj} />
            
            {/* Quick Actions */}
            <div className="bg-white rounded-lg p-4 border border-gray-200">
              <h3 className="font-semibold text-gray-900 mb-3">Quick Actions</h3>
              <div className="space-y-2">
                <button
                  onClick={() => navigate('/live-street-view')}
                  className="w-full flex items-center space-x-3 p-3 text-left bg-blue-50 hover:bg-blue-100 rounded-lg transition-colors"
                >
                  <Eye className="w-5 h-5 text-blue-600" />
                  <div>
                    <div className="font-medium text-blue-900">Start Street View</div>
                    <div className="text-xs text-blue-600">GPS-guided inspection</div>
                  </div>
                </button>
                
                <button
                  className="w-full flex items-center space-x-3 p-3 text-left bg-gray-50 hover:bg-gray-100 rounded-lg transition-colors"
                >
                  <Download className="w-5 h-5 text-gray-600" />
                  <div>
                    <div className="font-medium text-gray-900">Export Evidence</div>
                    <div className="text-xs text-gray-600">Save current views</div>
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

export default LiveView;