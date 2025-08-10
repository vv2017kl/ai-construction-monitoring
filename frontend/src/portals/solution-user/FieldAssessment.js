import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  MapPin, Navigation, Camera, Mic, FileText, CheckSquare,
  AlertTriangle, Clock, Users, Smartphone, Tablet, Monitor,
  Locate, Compass, Route, Map, Layers, Target, Upload,
  Download, Save, Share2, RefreshCw, Settings, Eye,
  Play, Pause, Square, ZoomIn, ZoomOut, RotateCw,
  Battery, Wifi, Signal, Volume2, VolumeX, Bell
} from 'lucide-react';
import { useTheme } from '../../context/ThemeContext';
import MainLayout from '../../components/shared/Layout/MainLayout';
import { mockSites, mockUser, mockPersonnel, mockCameras } from '../../data/mockData';

const FieldAssessment = () => {
  const navigate = useNavigate();
  const { theme } = useTheme();
  
  // State management
  const [deviceMode, setDeviceMode] = useState('tablet'); // 'tablet', 'mobile', 'desktop'
  const [isRecording, setIsRecording] = useState(false);
  const [currentLocation, setCurrentLocation] = useState(null);
  const [selectedZone, setSelectedZone] = useState(null);
  const [assessmentMode, setAssessmentMode] = useState('inspection'); // 'inspection', 'survey', 'documentation'
  const [activeTools, setActiveTools] = useState({
    gps: true,
    camera: false,
    voice: false,
    measurement: false
  });
  const [pathData, setPathData] = useState([]);
  const [currentAssessment, setCurrentAssessment] = useState(null);

  const currentSite = mockSites.find(s => s.name === mockUser.currentSite) || mockSites[0];

  // Mock GPS coordinates for demonstration
  const mockGPSLocation = {
    latitude: 40.7128,
    longitude: -74.0060,
    accuracy: 3.2,
    heading: 180,
    speed: 0
  };

  // Mock assessment data
  const mockAssessments = [
    {
      id: 'fa001',
      title: 'Foundation Inspection - Zone A',
      type: 'inspection',
      status: 'in_progress',
      progress: 65,
      startTime: new Date(Date.now() - 45 * 60 * 1000),
      inspector: mockUser.displayName,
      checkpoints: 8,
      completedCheckpoints: 5,
      issues: 2,
      photos: 12
    },
    {
      id: 'fa002', 
      title: 'Safety Compliance Survey',
      type: 'survey',
      status: 'completed',
      progress: 100,
      startTime: new Date(Date.now() - 2 * 60 * 60 * 1000),
      endTime: new Date(Date.now() - 30 * 60 * 1000),
      inspector: 'Sarah Chen',
      checkpoints: 15,
      completedCheckpoints: 15,
      issues: 0,
      photos: 8
    }
  ];

  // Mock zones for field assessment
  const mockZones = [
    { id: 'zone-a', name: 'Zone A - Foundation', color: '#3b82f6', coordinates: [40.7128, -74.0060] },
    { id: 'zone-b', name: 'Zone B - Steel Frame', color: '#ef4444', coordinates: [40.7130, -74.0058] },
    { id: 'zone-c', name: 'Zone C - Excavation', color: '#f59e0b', coordinates: [40.7125, -74.0062] },
    { id: 'zone-d', name: 'Zone D - Utilities', color: '#10b981', coordinates: [40.7132, -74.0055] }
  ];

  const formatTime = (date) => {
    return new Date(date).toLocaleTimeString('en-US', { 
      hour: '2-digit', 
      minute: '2-digit' 
    });
  };

  const formatDuration = (start, end = new Date()) => {
    const duration = Math.floor((end - new Date(start)) / (1000 * 60));
    const hours = Math.floor(duration / 60);
    const minutes = duration % 60;
    
    if (hours > 0) {
      return `${hours}h ${minutes}m`;
    }
    return `${minutes}m`;
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'in_progress': return { bg: 'bg-blue-100', text: 'text-blue-800', dot: 'bg-blue-500' };
      case 'completed': return { bg: 'bg-green-100', text: 'text-green-800', dot: 'bg-green-500' };
      case 'pending': return { bg: 'bg-yellow-100', text: 'text-yellow-800', dot: 'bg-yellow-500' };
      case 'on_hold': return { bg: 'bg-gray-100', text: 'text-gray-800', dot: 'bg-gray-500' };
      default: return { bg: 'bg-gray-100', text: 'text-gray-800', dot: 'bg-gray-500' };
    }
  };

  const DeviceStatusBar = () => (
    <div className="bg-gray-900 text-white px-4 py-2 flex items-center justify-between text-sm">
      <div className="flex items-center space-x-4">
        <div className="flex items-center space-x-1">
          <Signal className="w-4 h-4" />
          <span>4G</span>
        </div>
        <div className="flex items-center space-x-1">
          <Wifi className="w-4 h-4" />
          <span>Connected</span>
        </div>
        <div className="flex items-center space-x-1">
          <GPS className="w-4 h-4 text-green-400" />
          <span>{mockGPSLocation.accuracy}m</span>
        </div>
      </div>
      
      <div className="flex items-center space-x-4">
        <span>{new Date().toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' })}</span>
        <div className="flex items-center space-x-1">
          <Battery className="w-4 h-4 text-green-400" />
          <span>87%</span>
        </div>
      </div>
    </div>
  );

  const MapInterface = () => (
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

      {/* Zone Markers */}
      {mockZones.map((zone, index) => (
        <div
          key={zone.id}
          className={`absolute w-6 h-6 rounded-full cursor-pointer transform -translate-x-1/2 -translate-y-1/2 ${
            selectedZone === zone.id ? 'ring-4 ring-white shadow-lg' : ''
          }`}
          style={{
            backgroundColor: zone.color,
            left: `${25 + (index * 15)}%`,
            top: `${30 + (index * 10)}%`
          }}
          onClick={() => setSelectedZone(zone.id)}
          title={zone.name}
        >
          <div className="w-full h-full rounded-full flex items-center justify-center text-white text-xs font-bold">
            {index + 1}
          </div>
        </div>
      ))}

      {/* Current Location Indicator */}
      <div
        className="absolute w-4 h-4 bg-blue-600 rounded-full animate-pulse transform -translate-x-1/2 -translate-y-1/2 ring-4 ring-blue-200"
        style={{ left: '45%', top: '55%' }}
        title="Current Location"
      >
        <div className="absolute inset-0 bg-blue-600 rounded-full animate-ping"></div>
      </div>

      {/* Path Trail */}
      <svg className="absolute inset-0 w-full h-full pointer-events-none">
        <path
          d="M 25% 30% Q 35% 45% 45% 55% T 65% 50%"
          stroke="#3b82f6"
          strokeWidth="3"
          strokeDasharray="5,5"
          fill="none"
          className="animate-pulse"
        />
      </svg>

      {/* Map Controls */}
      <div className="absolute top-4 right-4 flex flex-col space-y-2">
        <button className="p-2 bg-white rounded-lg shadow-sm hover:shadow-md transition-shadow">
          <ZoomIn className="w-4 h-4" />
        </button>
        <button className="p-2 bg-white rounded-lg shadow-sm hover:shadow-md transition-shadow">
          <ZoomOut className="w-4 h-4" />
        </button>
        <button className="p-2 bg-white rounded-lg shadow-sm hover:shadow-md transition-shadow">
          <Compass className="w-4 h-4" />
        </button>
        <button className="p-2 bg-white rounded-lg shadow-sm hover:shadow-md transition-shadow">
          <Layers className="w-4 h-4" />
        </button>
      </div>

      {/* GPS Coordinates */}
      <div className="absolute bottom-4 left-4 bg-black/70 text-white px-3 py-1 rounded-lg text-xs">
        {mockGPSLocation.latitude.toFixed(6)}, {mockGPSLocation.longitude.toFixed(6)}
      </div>
    </div>
  );

  const AssessmentCard = ({ assessment }) => {
    const statusConfig = getStatusColor(assessment.status);
    
    return (
      <div className="bg-white rounded-lg border border-gray-200 p-4 hover:shadow-md transition-shadow">
        <div className="flex items-start justify-between mb-3">
          <div>
            <h3 className="font-semibold text-gray-900">{assessment.title}</h3>
            <p className="text-sm text-gray-600 capitalize">{assessment.type}</p>
          </div>
          <span className={`px-2 py-1 text-xs font-semibold rounded-full ${statusConfig.bg} ${statusConfig.text}`}>
            {assessment.status.replace('_', ' ').toUpperCase()}
          </span>
        </div>

        <div className="mb-4">
          <div className="flex justify-between text-sm text-gray-600 mb-1">
            <span>Progress</span>
            <span>{assessment.progress}%</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div 
              className="bg-blue-600 h-2 rounded-full transition-all duration-300"
              style={{ width: `${assessment.progress}%` }}
            ></div>
          </div>
        </div>

        <div className="grid grid-cols-2 gap-4 text-sm">
          <div>
            <span className="text-gray-600">Checkpoints:</span>
            <span className="ml-2 font-medium">{assessment.completedCheckpoints}/{assessment.checkpoints}</span>
          </div>
          <div>
            <span className="text-gray-600">Issues:</span>
            <span className={`ml-2 font-medium ${assessment.issues > 0 ? 'text-red-600' : 'text-green-600'}`}>
              {assessment.issues}
            </span>
          </div>
          <div>
            <span className="text-gray-600">Duration:</span>
            <span className="ml-2 font-medium">{formatDuration(assessment.startTime, assessment.endTime)}</span>
          </div>
          <div>
            <span className="text-gray-600">Photos:</span>
            <span className="ml-2 font-medium">{assessment.photos}</span>
          </div>
        </div>

        <div className="flex items-center justify-between mt-4 pt-4 border-t border-gray-100">
          <span className="text-xs text-gray-500">
            Started: {formatTime(assessment.startTime)}
          </span>
          <div className="flex space-x-2">
            <button className="p-1 hover:bg-gray-100 rounded">
              <Eye className="w-4 h-4 text-gray-600" />
            </button>
            <button className="p-1 hover:bg-gray-100 rounded">
              <Share2 className="w-4 h-4 text-gray-600" />
            </button>
            <button className="p-1 hover:bg-gray-100 rounded">
              <Download className="w-4 h-4 text-gray-600" />
            </button>
          </div>
        </div>
      </div>
    );
  };

  const QuickActionButton = ({ icon: Icon, label, active, onClick, color = theme.primary[500] }) => (
    <button
      onClick={onClick}
      className={`flex flex-col items-center p-4 rounded-lg border-2 transition-all duration-200 ${
        active 
          ? 'border-blue-500 bg-blue-50 text-blue-700' 
          : 'border-gray-200 hover:border-gray-300 bg-white text-gray-700'
      }`}
    >
      <Icon className="w-6 h-6 mb-2" style={{ color: active ? color : undefined }} />
      <span className="text-sm font-medium">{label}</span>
    </button>
  );

  return (
    <MainLayout portal="solution-user">
      <div className="h-full flex flex-col bg-gray-50">
        {/* Device Status Bar */}
        <DeviceStatusBar />
        
        {/* Main Header */}
        <div className="bg-white border-b border-gray-200 px-6 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-xl font-bold text-gray-900">Field Assessment</h1>
              <div className="flex items-center space-x-2 text-sm text-gray-600">
                <MapPin className="w-3 h-3" />
                <span>{currentSite.name}</span>
                <span>•</span>
                <GPS className="w-3 h-3 text-green-500" />
                <span>GPS Active</span>
                <span>•</span>
                <Clock className="w-3 h-3" />
                <span>{new Date().toLocaleTimeString()}</span>
              </div>
            </div>

            <div className="flex items-center space-x-4">
              {/* Device Mode Selector */}
              <div className="flex items-center space-x-2 bg-gray-100 rounded-lg p-1">
                {[
                  { key: 'tablet', label: 'Tablet', icon: Tablet },
                  { key: 'mobile', label: 'Mobile', icon: Smartphone },
                  { key: 'desktop', label: 'Desktop', icon: Monitor }
                ].map(({ key, label, icon: Icon }) => (
                  <button
                    key={key}
                    onClick={() => setDeviceMode(key)}
                    className={`flex items-center space-x-1 px-3 py-1 text-sm rounded transition-colors ${
                      deviceMode === key 
                        ? 'bg-white shadow-sm text-blue-600' 
                        : 'hover:bg-gray-200'
                    }`}
                  >
                    <Icon className="w-4 h-4" />
                    <span>{label}</span>
                  </button>
                ))}
              </div>

              <button
                onClick={() => setIsRecording(!isRecording)}
                className={`flex items-center space-x-2 px-4 py-2 rounded-lg transition-colors ${
                  isRecording 
                    ? 'bg-red-600 text-white hover:bg-red-700' 
                    : 'bg-blue-600 text-white hover:bg-blue-700'
                }`}
              >
                {isRecording ? <Square className="w-4 h-4" /> : <Play className="w-4 h-4" />}
                <span>{isRecording ? 'Stop Assessment' : 'Start Assessment'}</span>
              </button>
            </div>
          </div>
        </div>

        {/* Main Content */}
        <div className="flex-1 overflow-auto">
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 p-6">
            {/* Left Column - Map & Navigation */}
            <div className="lg:col-span-2 space-y-6">
              {/* Interactive Map */}
              <div className="bg-white rounded-lg p-6 shadow-sm border border-gray-100">
                <div className="flex items-center justify-between mb-4">
                  <h2 className="font-semibold text-gray-900">Site Map & Navigation</h2>
                  <div className="flex items-center space-x-2">
                    <button className="p-2 hover:bg-gray-100 rounded-lg">
                      <Route className="w-4 h-4" />
                    </button>
                    <button className="p-2 hover:bg-gray-100 rounded-lg">
                      <Target className="w-4 h-4" />
                    </button>
                    <button className="p-2 hover:bg-gray-100 rounded-lg">
                      <RefreshCw className="w-4 h-4" />
                    </button>
                  </div>
                </div>
                <MapInterface />
              </div>

              {/* Zone Information */}
              {selectedZone && (
                <div className="bg-white rounded-lg p-6 shadow-sm border border-gray-100">
                  <h3 className="font-semibold text-gray-900 mb-4">Zone Information</h3>
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <p className="text-sm text-gray-600">Zone Name:</p>
                      <p className="font-medium">{mockZones.find(z => z.id === selectedZone)?.name}</p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-600">Status:</p>
                      <span className="px-2 py-1 bg-green-100 text-green-800 text-sm rounded-full">Active</span>
                    </div>
                    <div>
                      <p className="text-sm text-gray-600">Personnel:</p>
                      <p className="font-medium">3 workers</p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-600">Last Inspection:</p>
                      <p className="font-medium">2 hours ago</p>
                    </div>
                  </div>
                </div>
              )}

              {/* Quick Actions */}
              <div className="bg-white rounded-lg p-6 shadow-sm border border-gray-100">
                <h3 className="font-semibold text-gray-900 mb-4">Quick Actions</h3>
                <div className="grid grid-cols-4 gap-4">
                  <QuickActionButton
                    icon={Camera}
                    label="Photo"
                    active={activeTools.camera}
                    onClick={() => setActiveTools(prev => ({ ...prev, camera: !prev.camera }))}
                  />
                  <QuickActionButton
                    icon={Mic}
                    label="Voice Note"
                    active={activeTools.voice}
                    onClick={() => setActiveTools(prev => ({ ...prev, voice: !prev.voice }))}
                  />
                  <QuickActionButton
                    icon={FileText}
                    label="Report"
                    active={false}
                    onClick={() => navigate('/reports')}
                  />
                  <QuickActionButton
                    icon={AlertTriangle}
                    label="Issue"
                    active={false}
                    onClick={() => navigate('/alert-center')}
                    color={theme.danger[500]}
                  />
                </div>
              </div>
            </div>

            {/* Right Column - Assessment Details */}
            <div className="space-y-6">
              {/* Current Location */}
              <div className="bg-white rounded-lg p-6 shadow-sm border border-gray-100">
                <h3 className="font-semibold text-gray-900 mb-4">Current Location</h3>
                <div className="space-y-3">
                  <div className="flex items-center space-x-2">
                    <GPS className="w-4 h-4 text-green-500" />
                    <span className="text-sm">GPS Coordinates</span>
                  </div>
                  <p className="text-xs font-mono bg-gray-100 p-2 rounded">
                    {mockGPSLocation.latitude.toFixed(6)}, {mockGPSLocation.longitude.toFixed(6)}
                  </p>
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-600">Accuracy:</span>
                    <span className="font-medium text-green-600">{mockGPSLocation.accuracy}m</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-600">Heading:</span>
                    <span className="font-medium">{mockGPSLocation.heading}°</span>
                  </div>
                </div>
              </div>

              {/* Active Assessments */}
              <div className="bg-white rounded-lg p-6 shadow-sm border border-gray-100">
                <div className="flex items-center justify-between mb-4">
                  <h3 className="font-semibold text-gray-900">Active Assessments</h3>
                  <button className="text-blue-600 hover:text-blue-800 text-sm font-medium">
                    View All
                  </button>
                </div>
                <div className="space-y-4">
                  {mockAssessments.slice(0, 2).map((assessment) => (
                    <AssessmentCard key={assessment.id} assessment={assessment} />
                  ))}
                </div>
              </div>

              {/* Tools Status */}
              <div className="bg-white rounded-lg p-6 shadow-sm border border-gray-100">
                <h3 className="font-semibold text-gray-900 mb-4">Tool Status</h3>
                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-2">
                      <GPS className="w-4 h-4 text-green-500" />
                      <span className="text-sm">GPS</span>
                    </div>
                    <span className="text-xs bg-green-100 text-green-800 px-2 py-1 rounded-full">Active</span>
                  </div>
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-2">
                      <Camera className={`w-4 h-4 ${activeTools.camera ? 'text-blue-500' : 'text-gray-400'}`} />
                      <span className="text-sm">Camera</span>
                    </div>
                    <span className={`text-xs px-2 py-1 rounded-full ${
                      activeTools.camera 
                        ? 'bg-blue-100 text-blue-800' 
                        : 'bg-gray-100 text-gray-600'
                    }`}>
                      {activeTools.camera ? 'Ready' : 'Standby'}
                    </span>
                  </div>
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-2">
                      <Mic className={`w-4 h-4 ${activeTools.voice ? 'text-red-500' : 'text-gray-400'}`} />
                      <span className="text-sm">Voice Recording</span>
                    </div>
                    <span className={`text-xs px-2 py-1 rounded-full ${
                      activeTools.voice 
                        ? 'bg-red-100 text-red-800' 
                        : 'bg-gray-100 text-gray-600'
                    }`}>
                      {activeTools.voice ? 'Recording' : 'Off'}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </MainLayout>
  );
};

export default FieldAssessment;