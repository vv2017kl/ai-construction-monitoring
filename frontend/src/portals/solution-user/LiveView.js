import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  Grid3X3, Grid2X2, Square, Maximize2, Camera, 
  Play, Pause, Volume2, VolumeX, RotateCcw, ZoomIn, ZoomOut,
  AlertTriangle, CheckCircle, Settings, Download, Fullscreen,
  Users, HardHat, Car, Wrench, Eye, MapPin, Clock, 
  ArrowUp, ArrowDown, ArrowLeft, ArrowRight, RotateCw, Loader,
  Wifi, WifiOff, Record, Square as StopIcon
} from 'lucide-react';
import { useTheme } from '../../context/ThemeContext';
import MainLayout from '../../components/shared/Layout/MainLayout';
import { zoneminderAPI } from '../../services';
import { useZoneminderCameras, useRecentEvents, useRealTimeData } from '../../hooks/useAPI';
import { formatters } from '../../utils/formatters';
import { ZONEMINDER_CONSTANTS } from '../../utils/constants';

const LiveView = () => {
  const navigate = useNavigate();
  const { theme } = useTheme();
  
  // Layout and UI state
  const [gridLayout, setGridLayout] = useState('2x2'); // '1x1', '2x2', '3x3', '4x4'
  const [selectedCamera, setSelectedCamera] = useState(null);
  const [fullscreenCamera, setFullscreenCamera] = useState(null);
  const [showAIOverlay, setShowAIOverlay] = useState(true);
  const [audioEnabled, setAudioEnabled] = useState(false);
  const [ptzActive, setPtzActive] = useState(null);
  
  // Enhanced functionality state
  const [showCameraSettings, setShowCameraSettings] = useState(false);
  const [selectedCameraForSettings, setSelectedCameraForSettings] = useState(null);
  const [recordingCameras, setRecordingCameras] = useState(new Set());
  const [showDetectionDetail, setShowDetectionDetail] = useState(false);
  const [selectedDetection, setSelectedDetection] = useState(null);
  const [cameraPTZSettings, setCameraPTZSettings] = useState({});
  const [streamQuality, setStreamQuality] = useState('high');
  const [cameraStreams, setCameraStreams] = useState({});
  const [cameraSnapshots, setCameraSnapshots] = useState({});

  // API hooks for real-time data
  const { data: cameras, loading: camerasLoading } = useZoneminderCameras();
  const { data: recentEvents } = useRealTimeData(
    () => zoneminderAPI.events.getRecent(1), // Last hour of events
    10000 // Update every 10 seconds
  );

  // Get camera list and set default selected camera
  const cameraList = cameras?.cameras || [];
  
  useEffect(() => {
    if (cameraList.length > 0 && !selectedCamera) {
      setSelectedCamera(cameraList[0].camera_id);
    }
  }, [cameraList, selectedCamera]);

  // Load stream information for cameras
  useEffect(() => {
    const loadCameraStreams = async () => {
      const streams = {};
      const snapshots = {};
      
      for (const camera of cameraList) {
        try {
          // Get stream info
          const streamInfo = await zoneminderAPI.streams.getStreamInfo(camera.camera_id, streamQuality);
          streams[camera.camera_id] = streamInfo;
          
          // Get snapshot
          const snapshotInfo = await zoneminderAPI.streams.getSnapshot(camera.camera_id);
          snapshots[camera.camera_id] = snapshotInfo;
        } catch (error) {
          console.error(`Error loading stream for camera ${camera.camera_id}:`, error);
        }
      }
      
      setCameraStreams(streams);
      setCameraSnapshots(snapshots);
    };

    if (cameraList.length > 0) {
      loadCameraStreams();
    }
  }, [cameraList, streamQuality]);

  // Get recent detections for AI overlay
  const liveDetections = recentEvents?.events?.filter(event => 
    cameraList.some(cam => cam.camera_id === event.camera_id)
  ) || [];

  // PTZ Control Functions
  const handlePTZControl = async (cameraId, direction) => {
    setPtzActive(cameraId);
    
    try {
      // Find camera to check if PTZ capable
      const camera = cameraList.find(cam => cam.camera_id === cameraId);
      if (!camera?.ptz_capable) {
        console.warn(`Camera ${cameraId} is not PTZ capable`);
        return;
      }
      
      // Simulate PTZ control API call (implement when real ZoneMinder PTZ is available)
      console.log(`PTZ Control: Camera ${cameraId}, Direction: ${direction}`);
      
      setCameraPTZSettings(prev => ({
        ...prev,
        [cameraId]: {
          ...prev[cameraId],
          lastCommand: direction,
          timestamp: new Date().toISOString()
        }
      }));
      
      // Visual feedback
      setTimeout(() => setPtzActive(null), 500);
      
    } catch (error) {
      console.error('PTZ control error:', error);
      setPtzActive(null);
    }
  };

  const handleZoom = async (cameraId, zoomIn) => {
    try {
      const camera = cameraList.find(cam => cam.camera_id === cameraId);
      if (!camera?.ptz_capable) {
        console.warn(`Camera ${cameraId} does not support zoom`);
        return;
      }
      
      console.log(`Zoom ${zoomIn ? 'In' : 'Out'}: Camera ${cameraId}`);
      
      // Update PTZ settings for zoom
      setCameraPTZSettings(prev => ({
        ...prev,
        [cameraId]: {
          ...prev[cameraId],
          zoom: zoomIn ? 'in' : 'out',
          lastCommand: `zoom_${zoomIn ? 'in' : 'out'}`,
          timestamp: new Date().toISOString()
        }
      }));
      
    } catch (error) {
      console.error('Zoom control error:', error);
    }
  };

  // Recording Functions
  const toggleRecording = async (cameraId) => {
    try {
      const isCurrentlyRecording = recordingCameras.has(cameraId);
      
      if (isCurrentlyRecording) {
        // Stop recording
        await zoneminderAPI.streams.stopRecording(cameraId, 'current_session');
        setRecordingCameras(prev => {
          const newSet = new Set(prev);
          newSet.delete(cameraId);
          return newSet;
        });
        console.log(`Recording stopped for camera ${cameraId}`);
      } else {
        // Start recording
        await zoneminderAPI.streams.startRecording(cameraId, 3600); // 1 hour duration
        setRecordingCameras(prev => {
          const newSet = new Set(prev);
          newSet.add(cameraId);
          return newSet;
        });
        console.log(`Recording started for camera ${cameraId}`);
      }
    } catch (error) {
      console.error('Recording toggle error:', error);
      // Revert recording state on error
      setRecordingCameras(prev => {
        const newSet = new Set(prev);
        if (newSet.has(cameraId)) {
          newSet.delete(cameraId);
        }
        return newSet;
      });
    }
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
    return cameraList.slice(0, Math.min(totalSlots, cameraList.length));
  };

  const CameraFeed = ({ camera, isSelected, onClick, detection }) => {
    const isOnline = camera.status === 'online';
    const cameraStream = cameraStreams[camera.camera_id];
    const cameraSnapshot = cameraSnapshots[camera.camera_id];
    
    return (
      <div 
        className={`relative bg-gray-900 rounded-lg overflow-hidden cursor-pointer border-2 transition-all duration-200 ${
          isSelected ? `border-blue-500` : 'border-gray-600 hover:border-gray-400'
        }`}
        onClick={onClick}
        style={{ aspectRatio: '16/9' }}
      >
        {/* Video Stream */}
        <div className="absolute inset-0 bg-gradient-to-br from-gray-800 to-gray-900 flex items-center justify-center">
          {isOnline ? (
            <div className="relative w-full h-full bg-gray-700 flex items-center justify-center">
              {/* Real camera stream or snapshot */}
              {cameraSnapshot ? (
                <img 
                  src={cameraSnapshot.snapshot_url} 
                  alt={`Camera ${camera.camera_id}`}
                  className="w-full h-full object-cover"
                  onError={(e) => {
                    // Fallback to construction site visualization if image fails
                    e.target.style.display = 'none';
                  }}
                />
              ) : null}
              
              {/* Fallback construction site visualization */}
              {(!cameraSnapshot || !cameraSnapshot.snapshot_url) && (
                <>
                  <div className="absolute inset-0 bg-gradient-to-b from-blue-200 via-gray-300 to-amber-100 opacity-80"></div>
                  <div className="absolute bottom-0 left-0 right-0 h-1/3 bg-gradient-to-t from-amber-600 to-amber-400 opacity-60"></div>
                </>
              )}
              
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
          <button 
            onClick={() => handlePTZControl(camera.id, 'up')}
            className={`p-3 bg-gray-100 hover:bg-gray-200 rounded-lg transition-colors ${
              ptzActive === camera.id ? 'bg-blue-200' : ''
            }`}
          >
            <ArrowUp className="w-4 h-4 mx-auto" />
          </button>
          <div></div>
          
          <button 
            onClick={() => handlePTZControl(camera.id, 'left')}
            className={`p-3 bg-gray-100 hover:bg-gray-200 rounded-lg transition-colors ${
              ptzActive === camera.id ? 'bg-blue-200' : ''
            }`}
          >
            <ArrowLeft className="w-4 h-4 mx-auto" />
          </button>
          <button 
            onClick={() => handlePTZControl(camera.id, 'home')}
            className="p-3 bg-gray-100 hover:bg-gray-200 rounded-lg transition-colors"
          >
            <RotateCcw className="w-4 h-4 mx-auto" />
          </button>
          <button 
            onClick={() => handlePTZControl(camera.id, 'right')}
            className={`p-3 bg-gray-100 hover:bg-gray-200 rounded-lg transition-colors ${
              ptzActive === camera.id ? 'bg-blue-200' : ''
            }`}
          >
            <ArrowRight className="w-4 h-4 mx-auto" />
          </button>
          
          <div></div>
          <button 
            onClick={() => handlePTZControl(camera.id, 'down')}
            className={`p-3 bg-gray-100 hover:bg-gray-200 rounded-lg transition-colors ${
              ptzActive === camera.id ? 'bg-blue-200' : ''
            }`}
          >
            <ArrowDown className="w-4 h-4 mx-auto" />
          </button>
          <div></div>
        </div>

        {/* Zoom Controls */}
        <div className="flex justify-center space-x-2 mt-4">
          <button 
            onClick={() => handleZoom(camera.id, false)}
            className="flex items-center space-x-1 px-3 py-2 bg-gray-100 hover:bg-gray-200 rounded-lg transition-colors"
          >
            <ZoomOut className="w-4 h-4" />
            <span className="text-sm">Zoom Out</span>
          </button>
          <button 
            onClick={() => handleZoom(camera.id, true)}
            className="flex items-center space-x-1 px-3 py-2 bg-gray-100 hover:bg-gray-200 rounded-lg transition-colors"
          >
            <ZoomIn className="w-4 h-4" />
            <span className="text-sm">Zoom In</span>
          </button>
        </div>
        
        {/* Recording Controls */}
        <div className="mt-4 pt-4 border-t border-gray-200">
          <h4 className="text-sm font-medium text-gray-700 mb-2">Recording</h4>
          <div className="flex space-x-2">
            <button 
              onClick={() => toggleRecording(camera.id)}
              className={`flex items-center space-x-1 px-3 py-2 rounded-lg transition-colors ${
                recordingCameras.has(camera.id)
                  ? 'bg-red-100 text-red-700 hover:bg-red-200'
                  : 'bg-green-100 text-green-700 hover:bg-green-200'
              }`}
            >
              {recordingCameras.has(camera.id) ? (
                <>
                  <Pause className="w-4 h-4" />
                  <span className="text-sm">Stop Recording</span>
                </>
              ) : (
                <>
                  <Play className="w-4 h-4" />
                  <span className="text-sm">Start Recording</span>
                </>
              )}
            </button>
            <button 
              onClick={() => openCameraSettings(camera)}
              className="flex items-center space-x-1 px-3 py-2 bg-gray-100 hover:bg-gray-200 rounded-lg transition-colors"
            >
              <Settings className="w-4 h-4" />
              <span className="text-sm">Settings</span>
            </button>
          </div>
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
                  onClick={() => navigate('/alert-center')}
                  className="w-full flex items-center space-x-3 p-3 text-left bg-red-50 hover:bg-red-100 rounded-lg transition-colors"
                >
                  <AlertTriangle className="w-5 h-5 text-red-600" />
                  <div>
                    <div className="font-medium text-red-900">Alert Center</div>
                    <div className="text-xs text-red-600">{mockAlerts.length} active alerts</div>
                  </div>
                </button>
                
                <button
                  className="w-full flex items-center space-x-3 p-3 text-left bg-gray-50 hover:bg-gray-100 rounded-lg transition-colors"
                  onClick={() => console.log('Export evidence for all cameras')}
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

      {/* Fullscreen Camera Modal */}
      {fullscreenCamera && (
        <div className="fixed inset-0 bg-black z-50 flex items-center justify-center">
          <div className="relative w-full h-full">
            {/* Fullscreen Camera View */}
            <div className="absolute inset-0">
              {(() => {
                const camera = mockCameras.find(c => c.id === fullscreenCamera);
                const detection = liveDetections.find(d => d.camera === camera?.name);
                return (
                  <div className="relative w-full h-full bg-gray-900">
                    {/* Video Stream */}
                    <div className="absolute inset-0 bg-gradient-to-br from-gray-800 to-gray-900 flex items-center justify-center">
                      <div className="relative w-full h-full bg-gray-700">
                        {/* Simulated construction site scene */}
                        <div className="absolute inset-0 bg-gradient-to-b from-blue-200 via-gray-300 to-amber-100 opacity-80"></div>
                        <div className="absolute bottom-0 left-0 right-0 h-1/3 bg-gradient-to-t from-amber-600 to-amber-400 opacity-60"></div>
                        
                        {/* AI Detection Overlays */}
                        {showAIOverlay && detection && (
                          <>
                            {Array.from({ length: detection.personCount }, (_, i) => (
                              <div
                                key={`person-${i}`}
                                className="absolute border-2 border-green-400 bg-green-400/20 cursor-pointer"
                                style={{
                                  left: `${20 + i * 25}%`,
                                  top: `${40 + (i % 2) * 15}%`,
                                  width: '120px',
                                  height: '160px'
                                }}
                                onClick={() => showDetectionDetails(detection)}
                              >
                                <div className="absolute -top-8 left-0 bg-green-400 text-black text-sm px-2 py-1 rounded">
                                  Person {detection.confidence}%
                                </div>
                              </div>
                            ))}
                          </>
                        )}
                      </div>
                    </div>
                    
                    {/* Fullscreen Controls */}
                    <div className="absolute top-4 left-4 right-4 flex items-center justify-between">
                      <div className="bg-black/60 text-white px-4 py-2 rounded-lg">
                        <h3 className="font-semibold">{camera?.name}</h3>
                        <div className="text-sm opacity-80">{camera?.location}</div>
                      </div>
                      <div className="flex items-center space-x-2">
                        <button
                          onClick={() => setShowAIOverlay(!showAIOverlay)}
                          className={`px-3 py-2 rounded-lg text-sm font-medium ${
                            showAIOverlay ? 'bg-green-600 text-white' : 'bg-white/20 text-white'
                          }`}
                        >
                          AI Detection {showAIOverlay ? 'ON' : 'OFF'}
                        </button>
                        <button
                          onClick={() => toggleRecording(fullscreenCamera)}
                          className={`px-3 py-2 rounded-lg text-sm font-medium ${
                            recordingCameras.has(fullscreenCamera) ? 'bg-red-600 text-white' : 'bg-white/20 text-white'
                          }`}
                        >
                          {recordingCameras.has(fullscreenCamera) ? 'Recording...' : 'Record'}
                        </button>
                        <button
                          onClick={() => setFullscreenCamera(null)}
                          className="bg-white/20 hover:bg-white/30 text-white p-2 rounded-lg transition-colors"
                        >
                          <Maximize2 className="w-5 h-5" />
                        </button>
                      </div>
                    </div>
                    
                    {/* Bottom Controls for PTZ */}
                    {camera?.type === 'ptz' && (
                      <div className="absolute bottom-4 left-1/2 transform -translate-x-1/2">
                        <div className="bg-black/60 p-4 rounded-lg">
                          <div className="grid grid-cols-3 gap-2">
                            <div></div>
                            <button 
                              onClick={() => handlePTZControl(camera.id, 'up')}
                              className="p-2 bg-white/20 hover:bg-white/30 text-white rounded transition-colors"
                            >
                              <ArrowUp className="w-4 h-4" />
                            </button>
                            <div></div>
                            <button 
                              onClick={() => handlePTZControl(camera.id, 'left')}
                              className="p-2 bg-white/20 hover:bg-white/30 text-white rounded transition-colors"
                            >
                              <ArrowLeft className="w-4 h-4" />
                            </button>
                            <button 
                              onClick={() => handlePTZControl(camera.id, 'home')}
                              className="p-2 bg-white/20 hover:bg-white/30 text-white rounded transition-colors"
                            >
                              <RotateCcw className="w-4 h-4" />
                            </button>
                            <button 
                              onClick={() => handlePTZControl(camera.id, 'right')}
                              className="p-2 bg-white/20 hover:bg-white/30 text-white rounded transition-colors"
                            >
                              <ArrowRight className="w-4 h-4" />
                            </button>
                            <div></div>
                            <button 
                              onClick={() => handlePTZControl(camera.id, 'down')}
                              className="p-2 bg-white/20 hover:bg-white/30 text-white rounded transition-colors"
                            >
                              <ArrowDown className="w-4 h-4" />
                            </button>
                          </div>
                          <div className="flex justify-center space-x-2 mt-3">
                            <button 
                              onClick={() => handleZoom(camera.id, false)}
                              className="px-3 py-1 bg-white/20 hover:bg-white/30 text-white rounded transition-colors text-sm"
                            >
                              <ZoomOut className="w-4 h-4 inline mr-1" />
                              Zoom Out
                            </button>
                            <button 
                              onClick={() => handleZoom(camera.id, true)}
                              className="px-3 py-1 bg-white/20 hover:bg-white/30 text-white rounded transition-colors text-sm"
                            >
                              <ZoomIn className="w-4 h-4 inline mr-1" />
                              Zoom In
                            </button>
                          </div>
                        </div>
                      </div>
                    )}
                  </div>
                );
              })()}
            </div>
          </div>
        </div>
      )}

      {/* Camera Settings Modal */}
      {showCameraSettings && selectedCameraForSettings && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-lg max-w-2xl w-full max-h-[90vh] overflow-hidden">
            <div className="p-6 border-b border-gray-200 flex items-center justify-between">
              <div>
                <h2 className="text-xl font-bold text-gray-900">Camera Settings</h2>
                <p className="text-sm text-gray-600">{selectedCameraForSettings.name}</p>
              </div>
              <button 
                onClick={() => setShowCameraSettings(false)}
                className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
              >
                <Maximize2 className="w-5 h-5 transform rotate-45" />
              </button>
            </div>
            
            <div className="p-6 overflow-y-auto max-h-[60vh]">
              <div className="space-y-6">
                {/* Basic Settings */}
                <div>
                  <h3 className="font-semibold text-gray-900 mb-4">Basic Settings</h3>
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">Resolution</label>
                      <select className="w-full px-3 py-2 border border-gray-200 rounded-lg">
                        <option>1920x1080 (Full HD)</option>
                        <option>1280x720 (HD)</option>
                        <option>4096x2160 (4K)</option>
                      </select>
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">Frame Rate</label>
                      <select className="w-full px-3 py-2 border border-gray-200 rounded-lg">
                        <option>30 FPS</option>
                        <option>24 FPS</option>
                        <option>60 FPS</option>
                      </select>
                    </div>
                  </div>
                </div>

                {/* AI Detection Settings */}
                <div>
                  <h3 className="font-semibold text-gray-900 mb-4">AI Detection</h3>
                  <div className="space-y-4">
                    <label className="flex items-center justify-between">
                      <span className="text-sm font-medium text-gray-700">Person Detection</span>
                      <input type="checkbox" defaultChecked className="rounded border-gray-300" />
                    </label>
                    <label className="flex items-center justify-between">
                      <span className="text-sm font-medium text-gray-700">PPE Compliance</span>
                      <input type="checkbox" defaultChecked className="rounded border-gray-300" />
                    </label>
                    <label className="flex items-center justify-between">
                      <span className="text-sm font-medium text-gray-700">Equipment Detection</span>
                      <input type="checkbox" defaultChecked className="rounded border-gray-300" />
                    </label>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">Confidence Threshold</label>
                      <input 
                        type="range" 
                        min="0" 
                        max="100" 
                        defaultValue="85" 
                        className="w-full"
                      />
                      <div className="flex justify-between text-xs text-gray-500 mt-1">
                        <span>0%</span>
                        <span>85%</span>
                        <span>100%</span>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Recording Settings */}
                <div>
                  <h3 className="font-semibold text-gray-900 mb-4">Recording</h3>
                  <div className="space-y-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">Recording Quality</label>
                      <select className="w-full px-3 py-2 border border-gray-200 rounded-lg">
                        <option>High Quality</option>
                        <option>Medium Quality</option>
                        <option>Low Quality</option>
                      </select>
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">Storage Duration (days)</label>
                      <input 
                        type="number" 
                        defaultValue="30" 
                        className="w-full px-3 py-2 border border-gray-200 rounded-lg"
                      />
                    </div>
                  </div>
                </div>
              </div>
            </div>
            
            <div className="p-6 border-t border-gray-200 flex justify-end space-x-3">
              <button 
                onClick={() => setShowCameraSettings(false)}
                className="px-4 py-2 text-gray-700 hover:bg-gray-100 rounded-lg transition-colors"
              >
                Cancel
              </button>
              <button className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
                Save Settings
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Detection Detail Modal */}
      {showDetectionDetail && selectedDetection && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-lg max-w-xl w-full">
            <div className="p-6 border-b border-gray-200 flex items-center justify-between">
              <div>
                <h2 className="text-xl font-bold text-gray-900">Detection Details</h2>
                <p className="text-sm text-gray-600">{selectedDetection.camera}</p>
              </div>
              <button 
                onClick={() => setShowDetectionDetail(false)}
                className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
              >
                <Maximize2 className="w-5 h-5 transform rotate-45" />
              </button>
            </div>
            
            <div className="p-6">
              <div className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <span className="text-sm font-medium text-gray-700">Personnel Count:</span>
                    <span className="ml-2 font-bold text-green-600">{selectedDetection.personCount}</span>
                  </div>
                  <div>
                    <span className="text-sm font-medium text-gray-700">Confidence:</span>
                    <span className="ml-2 font-bold text-blue-600">{selectedDetection.confidence}%</span>
                  </div>
                  <div>
                    <span className="text-sm font-medium text-gray-700">PPE Compliance:</span>
                    <span className={`ml-2 font-bold ${selectedDetection.ppeCompliance >= 90 ? 'text-green-600' : 'text-orange-600'}`}>
                      {selectedDetection.ppeCompliance}%
                    </span>
                  </div>
                  <div>
                    <span className="text-sm font-medium text-gray-700">Zone:</span>
                    <span className="ml-2 font-medium text-gray-900">{selectedDetection.zone}</span>
                  </div>
                </div>
                
                <div>
                  <span className="text-sm font-medium text-gray-700">Detection Time:</span>
                  <span className="ml-2 text-gray-900">{new Date(selectedDetection.timestamp).toLocaleString()}</span>
                </div>
                
                {selectedDetection.ppeCompliance < 90 && (
                  <div className="p-3 bg-orange-50 border border-orange-200 rounded-lg">
                    <div className="flex items-center space-x-2">
                      <AlertTriangle className="w-4 h-4 text-orange-600" />
                      <span className="text-sm font-medium text-orange-800">PPE Compliance Warning</span>
                    </div>
                    <p className="text-sm text-orange-700 mt-1">
                      Some personnel may not be wearing proper safety equipment.
                    </p>
                  </div>
                )}
              </div>
            </div>
            
            <div className="p-6 border-t border-gray-200 flex justify-end space-x-3">
              <button 
                onClick={() => navigate('/alert-center')}
                className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
              >
                Create Alert
              </button>
              <button 
                onClick={() => setShowDetectionDetail(false)}
                className="px-4 py-2 text-gray-700 hover:bg-gray-100 rounded-lg transition-colors"
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

export default LiveView;