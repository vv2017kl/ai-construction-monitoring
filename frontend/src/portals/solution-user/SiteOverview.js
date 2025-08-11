import React, { useState, useRef, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  MapPin, Camera, Shield, AlertTriangle, Users, Car, 
  Layers, ZoomIn, ZoomOut, RotateCcw, Settings, Eye,
  Navigation, Clock, Thermometer, Wind, Sun, Activity,
  Square, Circle, Pen, Save, X, Plus, Edit3, Trash2,
  Play, Maximize2, Download, Share2
} from 'lucide-react';
import { useTheme } from '../../context/ThemeContext';
import MainLayout from '../../components/shared/Layout/MainLayout';
import { mockCameras, mockSites, mockUser, mockZones, mockDetections } from '../../data/mockData';

const SiteOverview = () => {
  const navigate = useNavigate();
  const { theme } = useTheme();
  const mapRef = useRef(null);
  
  // State management
  const [mapView, setMapView] = useState('satellite'); // 'satellite', 'blueprint', 'hybrid'
  const [showLayers, setShowLayers] = useState({
    cameras: true,
    zones: true,
    personnel: true,
    equipment: false,
    alerts: true
  });
  const [selectedCamera, setSelectedCamera] = useState(null);
  const [selectedZone, setSelectedZone] = useState(null);
  const [selectedItems, setSelectedItems] = useState(new Set());
  const [isDrawingMode, setIsDrawingMode] = useState(false);
  const [drawingTool, setDrawingTool] = useState('rectangle'); // 'rectangle', 'circle', 'polygon'
  const [zoomLevel, setZoomLevel] = useState(100);
  const [mapCenter, setMapCenter] = useState({ x: 50, y: 50 });
  const [showBulkActions, setShowBulkActions] = useState(false);
  const [showZoneModal, setShowZoneModal] = useState(false);
  const [editingZone, setEditingZone] = useState(null);
  const [showAnalytics, setShowAnalytics] = useState(false);
  const [zones, setZones] = useState(mockZones);
  const [newZone, setNewZone] = useState({
    name: '',
    type: 'work_area',
    safetyLevel: 'medium',
    maxOccupancy: 10,
    requiresPPE: true,
    coordinates: []
  });

  // Drawing state
  const [isDrawing, setIsDrawing] = useState(false);
  const [drawingPath, setDrawingPath] = useState([]);
  const [tempShapes, setTempShapes] = useState([]);
  const [drawingStartPoint, setDrawingStartPoint] = useState(null);

  const currentSite = mockSites.find(s => s.name === mockUser.currentSite) || mockSites[0];

  // Simulate live personnel positions
  const [personnelPositions, setPersonnelPositions] = useState([
    { id: 1, x: 25, y: 30, name: 'Worker A', status: 'working', ppe: 95 },
    { id: 2, x: 45, y: 60, name: 'Worker B', status: 'moving', ppe: 100 },
    { id: 3, x: 70, y: 40, name: 'Supervisor', status: 'inspecting', ppe: 100 },
    { id: 4, x: 35, y: 75, name: 'Worker C', status: 'break', ppe: 85 }
  ]);

  // Equipment positions
  const [equipmentPositions] = useState([
    { id: 1, x: 80, y: 20, type: 'excavator', status: 'active', name: 'EX-001' },
    { id: 2, x: 15, y: 85, type: 'crane', status: 'idle', name: 'CR-002' },
    { id: 3, x: 60, y: 25, type: 'truck', status: 'loading', name: 'TR-003' }
  ]);

  // Camera feed preview modal
  const [previewCamera, setPreviewCamera] = useState(null);

  // Zone Management Functions
  const handleCreateZone = () => {
    if (!newZone.name || newZone.coordinates.length === 0) return;
    
    const zone = {
      id: `zone-${Date.now()}`,
      ...newZone,
      status: 'active',
      currentOccupancy: 0
    };
    
    setZones(prev => [...prev, zone]);
    setNewZone({
      name: '',
      type: 'work_area',
      safetyLevel: 'medium',
      maxOccupancy: 10,
      requiresPPE: true,
      coordinates: []
    });
    setShowZoneModal(false);
    setIsDrawingMode(false);
  };

  const handleEditZone = (zone) => {
    setEditingZone({ ...zone });
    setShowZoneModal(true);
  };

  const handleUpdateZone = () => {
    if (!editingZone) return;
    
    setZones(prev => prev.map(zone => 
      zone.id === editingZone.id ? editingZone : zone
    ));
    setEditingZone(null);
    setShowZoneModal(false);
  };

  const handleDeleteZone = (zoneId) => {
    setZones(prev => prev.filter(zone => zone.id !== zoneId));
    if (selectedZone === zoneId) {
      setSelectedZone(null);
    }
  };

  // Multi-selection functions
  const handleSelectItem = (id, type) => {
    const itemKey = `${type}-${id}`;
    const newSelected = new Set(selectedItems);
    
    if (newSelected.has(itemKey)) {
      newSelected.delete(itemKey);
    } else {
      newSelected.add(itemKey);
    }
    
    setSelectedItems(newSelected);
    setShowBulkActions(newSelected.size > 0);
  };

  const handleSelectAll = (type) => {
    const items = type === 'cameras' ? mockCameras : zones;
    const allSelected = items.every(item => selectedItems.has(`${type}-${item.id}`));
    
    const newSelected = new Set(selectedItems);
    
    if (allSelected) {
      // Deselect all of this type
      items.forEach(item => newSelected.delete(`${type}-${item.id}`));
    } else {
      // Select all of this type
      items.forEach(item => newSelected.add(`${type}-${item.id}`));
    }
    
    setSelectedItems(newSelected);
    setShowBulkActions(newSelected.size > 0);
  };

  // Export functionality
  const handleExportSiteData = () => {
    const siteData = {
      site: currentSite,
      cameras: mockCameras,
      zones: zones,
      personnel: personnelPositions,
      equipment: equipmentPositions,
      exportDate: new Date().toISOString()
    };

    const dataStr = JSON.stringify(siteData, null, 2);
    const dataUri = 'data:application/json;charset=utf-8,'+ encodeURIComponent(dataStr);
    
    const exportFileDefaultName = `site_overview_${currentSite.code}_${new Date().toISOString().split('T')[0]}.json`;
    
    const linkElement = document.createElement('a');
    linkElement.setAttribute('href', dataUri);
    linkElement.setAttribute('download', exportFileDefaultName);
    linkElement.click();
  };

  // Drawing functions
  const getMapCoordinates = (e) => {
    const rect = e.currentTarget.getBoundingClientRect();
    const x = ((e.clientX - rect.left) / rect.width) * 100;
    const y = ((e.clientY - rect.top) / rect.height) * 100;
    return { x: Math.max(0, Math.min(100, x)), y: Math.max(0, Math.min(100, y)) };
  };

  const handleMapMouseDown = (e) => {
    if (!isDrawingMode) return;
    
    const point = getMapCoordinates(e);
    setDrawingStartPoint(point);
    
    if (drawingTool === 'polygon') {
      setDrawingPath(prev => [...prev, point]);
    } else {
      setIsDrawing(true);
    }
  };

  const handleMapMouseMove = (e) => {
    if (!isDrawingMode || (!isDrawing && drawingTool !== 'polygon')) return;
    
    const currentPoint = getMapCoordinates(e);
    
    if (drawingTool === 'rectangle' && drawingStartPoint) {
      const shape = {
        type: 'rectangle',
        coordinates: [
          { x: Math.min(drawingStartPoint.x, currentPoint.x), y: Math.min(drawingStartPoint.y, currentPoint.y) },
          { x: Math.max(drawingStartPoint.x, currentPoint.x), y: Math.min(drawingStartPoint.y, currentPoint.y) },
          { x: Math.max(drawingStartPoint.x, currentPoint.x), y: Math.max(drawingStartPoint.y, currentPoint.y) },
          { x: Math.min(drawingStartPoint.x, currentPoint.x), y: Math.max(drawingStartPoint.y, currentPoint.y) }
        ]
      };
      setTempShapes([shape]);
    } else if (drawingTool === 'circle' && drawingStartPoint) {
      const centerX = drawingStartPoint.x;
      const centerY = drawingStartPoint.y;
      const radius = Math.sqrt(Math.pow(currentPoint.x - centerX, 2) + Math.pow(currentPoint.y - centerY, 2));
      
      // Create circle as polygon with 16 points
      const points = [];
      for (let i = 0; i < 16; i++) {
        const angle = (i / 16) * 2 * Math.PI;
        points.push({
          x: centerX + radius * Math.cos(angle),
          y: centerY + radius * Math.sin(angle)
        });
      }
      
      const shape = {
        type: 'circle',
        coordinates: points
      };
      setTempShapes([shape]);
    }
  };

  const handleMapMouseUp = (e) => {
    if (!isDrawingMode) return;
    
    if (drawingTool === 'rectangle' || drawingTool === 'circle') {
      if (tempShapes.length > 0) {
        const coordinates = tempShapes[0].coordinates;
        setNewZone(prev => ({ ...prev, coordinates }));
        setTempShapes([]);
        setShowZoneModal(true);
        setIsDrawing(false);
        setDrawingStartPoint(null);
      }
    }
  };

  const handleMapDoubleClick = (e) => {
    if (!isDrawingMode || drawingTool !== 'polygon') return;
    
    if (drawingPath.length >= 3) {
      setNewZone(prev => ({ ...prev, coordinates: drawingPath }));
      setDrawingPath([]);
      setShowZoneModal(true);
    }
  };

  const finishDrawing = () => {
    if (drawingTool === 'polygon' && drawingPath.length >= 3) {
      setNewZone(prev => ({ ...prev, coordinates: drawingPath }));
      setDrawingPath([]);
      setShowZoneModal(true);
    }
    setIsDrawingMode(false);
    setIsDrawing(false);
    setTempShapes([]);
    setDrawingStartPoint(null);
  };

  const cancelDrawing = () => {
    setDrawingPath([]);
    setTempShapes([]);
    setIsDrawing(false);
    setDrawingStartPoint(null);
    setIsDrawingMode(false);
  };

  // Real-time updates simulation
  useEffect(() => {
    const interval = setInterval(() => {
      // Simulate personnel movement
      setPersonnelPositions(prev => prev.map(person => ({
        ...person,
        x: Math.max(5, Math.min(95, person.x + (Math.random() - 0.5) * 5)),
        y: Math.max(5, Math.min(95, person.y + (Math.random() - 0.5) * 5))
      })));
    }, 10000); // Update every 10 seconds

    return () => clearInterval(interval);
  }, []);

  const CameraIcon = ({ camera, onClick }) => {
    const isOnline = camera.status === 'online';
    const hasAlerts = camera.alerts > 0;
    const isSelected = selectedItems.has(`cameras-${camera.id}`);
    
    return (
      <div
        className={`absolute cursor-pointer transform -translate-x-1/2 -translate-y-1/2 transition-all hover:scale-110 ${
          selectedCamera === camera.id || isSelected ? 'z-20' : 'z-10'
        }`}
        style={{ 
          left: `${camera.coordinates.x}%`, 
          top: `${camera.coordinates.y}%` 
        }}
      >
        {/* Selection checkbox */}
        <div className="absolute -top-2 -left-2 z-30">
          <input
            type="checkbox"
            checked={isSelected}
            onChange={(e) => {
              e.stopPropagation();
              handleSelectItem(camera.id, 'cameras');
            }}
            className="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
          />
        </div>

        <div
          onClick={() => onClick(camera)}
          className={`relative p-2 rounded-full shadow-lg ${
            isOnline ? 'bg-green-500' : 'bg-red-500'
          } ${selectedCamera === camera.id ? 'ring-4 ring-blue-500' : ''} ${
            isSelected ? 'ring-2 ring-green-500' : ''
          }`}
        >
          <Camera className="w-4 h-4 text-white" />
          
          {/* Alert indicator */}
          {hasAlerts && (
            <div className="absolute -top-1 -right-1 w-3 h-3 bg-red-600 rounded-full flex items-center justify-center">
              <span className="text-xs text-white font-bold">{camera.alerts}</span>
            </div>
          )}
          
          {/* Field of view indicator */}
          <div className={`absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 opacity-30 ${
            selectedCamera === camera.id ? 'block' : 'hidden'
          }`}>
            <div 
              className="border-2 border-blue-500"
              style={{
                width: '100px',
                height: '60px',
                clipPath: 'polygon(0 0, 100% 0, 80% 100%, 20% 100%)'
              }}
            />
          </div>
        </div>

        
        {/* Camera label */}
        <div className="absolute top-full left-1/2 transform -translate-x-1/2 mt-1">
          <div className="bg-black/70 text-white px-2 py-1 rounded text-xs whitespace-nowrap">
            {camera.name}
          </div>
        </div>
      </div>
    );
  };

  const ZoneOverlay = ({ zone, onClick }) => {
    const zoneColors = {
      safety: 'border-yellow-500 bg-yellow-500/20',
      restricted: 'border-red-500 bg-red-500/20',
      work_area: 'border-blue-500 bg-blue-500/20',
      equipment: 'border-orange-500 bg-orange-500/20',
      hazardous: 'border-red-700 bg-red-700/30'
    };

    const coords = zone.coordinates;
    const minX = Math.min(...coords.map(c => c.x));
    const maxX = Math.max(...coords.map(c => c.x));
    const minY = Math.min(...coords.map(c => c.y));
    const maxY = Math.max(...coords.map(c => c.y));
    const isSelected = selectedItems.has(`zones-${zone.id}`);

    return (
      <div
        className={`absolute border-2 cursor-pointer transition-all hover:bg-opacity-40 ${
          zoneColors[zone.type] || 'border-gray-500 bg-gray-500/20'
        } ${selectedZone === zone.id ? 'ring-2 ring-blue-600' : ''} ${
          isSelected ? 'ring-2 ring-green-600' : ''
        }`}
        style={{
          left: `${minX}%`,
          top: `${minY}%`,
          width: `${maxX - minX}%`,
          height: `${maxY - minY}%`
        }}
      >
        {/* Selection checkbox */}
        <div className="absolute top-1 left-1 z-30">
          <input
            type="checkbox"
            checked={isSelected}
            onChange={(e) => {
              e.stopPropagation();
              handleSelectItem(zone.id, 'zones');
            }}
            className="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
          />
        </div>

        <div onClick={() => onClick(zone)} className="w-full h-full">
          {/* Zone label */}
          <div className="absolute top-2 left-2">
            <div className="bg-black/70 text-white px-2 py-1 rounded text-xs">
              {zone.name}
            </div>
          </div>
          
          {/* Zone status */}
          <div className="absolute top-2 right-2">
            <div className={`w-3 h-3 rounded-full ${
              zone.status === 'active' ? 'bg-green-500' : 
              zone.status === 'restricted' ? 'bg-red-500' : 'bg-gray-500'
            }`}></div>
          </div>

          {/* Occupancy indicator */}
          <div className="absolute bottom-2 left-2">
            <div className="bg-black/70 text-white px-2 py-1 rounded text-xs">
              {zone.currentOccupancy}/{zone.maxOccupancy}
            </div>
          </div>
        </div>

      </div>
    );
  };

  const PersonnelMarker = ({ person }) => (
    <div
      className="absolute cursor-pointer transform -translate-x-1/2 -translate-y-1/2 z-10"
      style={{ left: `${person.x}%`, top: `${person.y}%` }}
    >
      <div className={`relative p-1 rounded-full shadow-lg ${
        person.ppe >= 95 ? 'bg-green-500' : 
        person.ppe >= 85 ? 'bg-yellow-500' : 'bg-red-500'
      }`}>
        <Users className="w-3 h-3 text-white" />
      </div>
      <div className="absolute top-full left-1/2 transform -translate-x-1/2 mt-1">
        <div className="bg-black/70 text-white px-1 py-0.5 rounded text-xs whitespace-nowrap">
          {person.name} ({person.ppe}%)
        </div>
      </div>
    </div>
  );

  const EquipmentMarker = ({ equipment }) => (
    <div
      className="absolute cursor-pointer transform -translate-x-1/2 -translate-y-1/2 z-10"
      style={{ left: `${equipment.x}%`, top: `${equipment.y}%` }}
    >
      <div className={`relative p-2 rounded-full shadow-lg ${
        equipment.status === 'active' ? 'bg-orange-500' : 
        equipment.status === 'loading' ? 'bg-blue-500' : 'bg-gray-500'
      }`}>
        <Car className="w-4 h-4 text-white" />
      </div>
      <div className="absolute top-full left-1/2 transform -translate-x-1/2 mt-1">
        <div className="bg-black/70 text-white px-2 py-1 rounded text-xs whitespace-nowrap">
          {equipment.name} - {equipment.status}
        </div>
      </div>
    </div>
  );

  const CameraPreviewModal = () => {
    if (!previewCamera) return null;

    return (
      <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
        <div className="bg-white rounded-lg max-w-2xl w-full max-h-[80vh] overflow-hidden">
          <div className="p-4 border-b border-gray-200 flex items-center justify-between">
            <div>
              <h3 className="font-semibold text-gray-900">{previewCamera.name}</h3>
              <p className="text-sm text-gray-600">{previewCamera.location}</p>
            </div>
            <button
              onClick={() => setPreviewCamera(null)}
              className="p-2 hover:bg-gray-100 rounded-lg"
            >
              <X className="w-5 h-5" />
            </button>
          </div>
          
          <div className="p-4">
            <div className="bg-gray-900 rounded-lg aspect-video flex items-center justify-center relative">
              {/* Simulated camera feed */}
              <div className="absolute inset-0 bg-gradient-to-br from-blue-200 via-gray-300 to-amber-100 opacity-80 rounded-lg"></div>
              <div className="absolute top-4 left-4 bg-red-600 text-white px-2 py-1 rounded text-sm">
                🔴 LIVE
              </div>
              <Camera className="w-16 h-16 text-white/50 z-10" />
              
              {/* Quick actions */}
              <div className="absolute bottom-4 right-4 flex space-x-2">
                <button
                  onClick={() => navigate('/live-view')}
                  className="bg-blue-600 text-white p-2 rounded hover:bg-blue-700"
                >
                  <Maximize2 className="w-4 h-4" />
                </button>
                <button className="bg-green-600 text-white p-2 rounded hover:bg-green-700">
                  <Play className="w-4 h-4" />
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  };

  return (
    <MainLayout portal="solution-user">
      <div className="h-full flex flex-col">
        {/* Header */}
        <div className="bg-white border-b border-gray-200 px-6 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-xl font-bold text-gray-900">Site Overview</h1>
              <div className="flex items-center space-x-2 text-sm text-gray-600">
                <MapPin className="w-3 h-3" />
                <span>{currentSite.name}</span>
                <span>•</span>
                <span>{mockCameras.length} cameras</span>
                <span>•</span>
                <span>{mockZones.length} zones</span>
                <span>•</span>
                <span>{personnelPositions.length} personnel</span>
              </div>
            </div>

            {/* Map Controls */}
            <div className="flex items-center space-x-4">
              {/* Selection Controls */}
              <div className="flex items-center space-x-2">
                <button
                  onClick={() => handleSelectAll('cameras')}
                  className="flex items-center space-x-1 px-3 py-1 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors text-sm"
                >
                  <Camera className="w-3 h-3" />
                  <span>Select Cameras</span>
                </button>
                <button
                  onClick={() => handleSelectAll('zones')}
                  className="flex items-center space-x-1 px-3 py-1 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors text-sm"
                >
                  <Square className="w-3 h-3" />
                  <span>Select Zones</span>
                </button>
              </div>

              {/* Zone Management */}
              <button
                onClick={() => setShowZoneModal(true)}
                className="flex items-center space-x-2 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
              >
                <Plus className="w-4 h-4" />
                <span>Create Zone</span>
              </button>

              {/* View Toggle */}
              <div className="flex items-center space-x-2 bg-gray-100 rounded-lg p-1">
                {[
                  { id: 'satellite', label: 'Satellite' },
                  { id: 'blueprint', label: 'Blueprint' },
                  { id: 'hybrid', label: 'Hybrid' }
                ].map((view) => (
                  <button
                    key={view.id}
                    onClick={() => setMapView(view.id)}
                    className={`px-3 py-1 text-sm rounded transition-colors ${
                      mapView === view.id 
                        ? 'bg-white shadow-sm text-blue-600' 
                        : 'hover:bg-gray-200'
                    }`}
                  >
                    {view.label}
                  </button>
                ))}
              </div>

              {/* Zoom Controls */}
              <div className="flex items-center space-x-2">
                <button
                  onClick={() => setZoomLevel(Math.max(50, zoomLevel - 25))}
                  className="p-2 bg-gray-100 hover:bg-gray-200 rounded-lg"
                >
                  <ZoomOut className="w-4 h-4" />
                </button>
                <span className="text-sm font-medium w-12 text-center">{zoomLevel}%</span>
                <button
                  onClick={() => setZoomLevel(Math.min(200, zoomLevel + 25))}
                  className="p-2 bg-gray-100 hover:bg-gray-200 rounded-lg"
                >
                  <ZoomIn className="w-4 h-4" />
                </button>
              </div>

              {/* Drawing Tools */}
              <div className="flex items-center space-x-2">
                <button
                  onClick={() => {
                    setIsDrawingMode(!isDrawingMode);
                    if (!isDrawingMode) {
                      setDrawingTool('rectangle');
                    }
                  }}
                  className={`flex items-center space-x-1 px-3 py-2 rounded-lg transition-colors ${
                    isDrawingMode 
                      ? 'bg-blue-600 text-white' 
                      : 'bg-gray-100 hover:bg-gray-200 text-gray-700'
                  }`}
                >
                  <Pen className="w-4 h-4" />
                  <span>Draw</span>
                </button>

                {isDrawingMode && (
                  <div className="flex items-center space-x-1 bg-gray-100 rounded-lg p-1">
                    <button
                      onClick={() => setDrawingTool('rectangle')}
                      className={`p-1 rounded transition-colors ${
                        drawingTool === 'rectangle' 
                          ? 'bg-white shadow-sm text-blue-600' 
                          : 'hover:bg-gray-200'
                      }`}
                      title="Rectangle"
                    >
                      <Square className="w-3 h-3" />
                    </button>
                    <button
                      onClick={() => setDrawingTool('circle')}
                      className={`p-1 rounded transition-colors ${
                        drawingTool === 'circle' 
                          ? 'bg-white shadow-sm text-blue-600' 
                          : 'hover:bg-gray-200'
                      }`}
                      title="Circle"
                    >
                      <Circle className="w-3 h-3" />
                    </button>
                    <button
                      onClick={() => setDrawingTool('polygon')}
                      className={`p-1 rounded transition-colors ${
                        drawingTool === 'polygon' 
                          ? 'bg-white shadow-sm text-blue-600' 
                          : 'hover:bg-gray-200'
                      }`}
                      title="Polygon"
                    >
                      <Pen className="w-3 h-3" />
                    </button>
                  </div>
                )}
              </div>

              {/* Quick Actions */}
              <button
                onClick={() => navigate('/path-admin')}
                className="flex items-center space-x-2 px-4 py-2 text-white rounded-lg hover:opacity-90"
                style={{ backgroundColor: theme.primary[500] }}
              >
                <Navigation className="w-4 h-4" />
                <span>Path Admin</span>
              </button>
            </div>
          </div>
        </div>

        {/* Bulk Actions Bar */}
        {showBulkActions && (
          <div className="px-6 py-3 bg-blue-50 border-b border-blue-200">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-4">
                <span className="text-sm font-medium text-blue-900">
                  {selectedItems.size} item{selectedItems.size !== 1 ? 's' : ''} selected
                </span>
                <button
                  onClick={() => {
                    setSelectedItems(new Set());
                    setShowBulkActions(false);
                  }}
                  className="text-sm text-blue-600 hover:text-blue-800 transition-colors"
                >
                  Clear selection
                </button>
              </div>
              
              <div className="flex items-center space-x-2">
                <button className="flex items-center space-x-1 px-3 py-1 bg-green-100 text-green-700 rounded-md hover:bg-green-200 transition-colors text-sm">
                  <Eye className="w-3 h-3" />
                  <span>Monitor</span>
                </button>
                <button className="flex items-center space-x-1 px-3 py-1 bg-yellow-100 text-yellow-700 rounded-md hover:bg-yellow-200 transition-colors text-sm">
                  <Settings className="w-3 h-3" />
                  <span>Configure</span>
                </button>
                <button
                  onClick={handleExportSiteData}
                  className="flex items-center space-x-1 px-3 py-1 bg-blue-100 text-blue-700 rounded-md hover:bg-blue-200 transition-colors text-sm"
                >
                  <Download className="w-3 h-3" />
                  <span>Export</span>
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Main Content */}
        <div className="flex-1 flex overflow-hidden">
          {/* Map Area */}
          <div className="flex-1 relative bg-gray-100">
            <div 
              ref={mapRef}
              className="absolute inset-0 overflow-hidden"
              style={{ transform: `scale(${zoomLevel / 100})`, transformOrigin: 'center center' }}
            >
              {/* Base Map Layer */}
              <div className="w-full h-full relative">
                {mapView === 'satellite' && (
                  <div className="absolute inset-0 bg-gradient-to-br from-green-200 via-brown-200 to-gray-300">
                    {/* Simulated satellite imagery */}
                    <div className="absolute inset-0 opacity-60">
                      <div className="w-full h-full bg-gradient-to-b from-sky-200 to-amber-100"></div>
                      <div className="absolute bottom-0 left-0 right-0 h-1/2 bg-gradient-to-t from-amber-400 to-transparent opacity-50"></div>
                    </div>
                  </div>
                )}
                
                {mapView === 'blueprint' && (
                  <div className="absolute inset-0 bg-blue-50">
                    {/* Simulated blueprint lines */}
                    <svg className="w-full h-full">
                      <defs>
                        <pattern id="grid" width="50" height="50" patternUnits="userSpaceOnUse">
                          <path d="M 50 0 L 0 0 0 50" fill="none" stroke="#3b82f6" strokeWidth="0.5" opacity="0.3"/>
                        </pattern>
                      </defs>
                      <rect width="100%" height="100%" fill="url(#grid)" />
                    </svg>
                  </div>
                )}
                
                {mapView === 'hybrid' && (
                  <div className="absolute inset-0">
                    <div className="w-full h-full bg-gradient-to-b from-sky-200 to-amber-100 opacity-70"></div>
                    <svg className="absolute inset-0 w-full h-full">
                      <defs>
                        <pattern id="hybridgrid" width="50" height="50" patternUnits="userSpaceOnUse">
                          <path d="M 50 0 L 0 0 0 50" fill="none" stroke="#3b82f6" strokeWidth="0.5" opacity="0.2"/>
                        </pattern>
                      </defs>
                      <rect width="100%" height="100%" fill="url(#hybridgrid)" />
                    </svg>
                  </div>
                )}

                {/* Site Zones */}
                {showLayers.zones && zones.map((zone) => (
                  <ZoneOverlay
                    key={zone.id}
                    zone={zone}
                    onClick={(zone) => setSelectedZone(zone.id)}
                  />
                ))}

                {/* Camera Positions */}
                {showLayers.cameras && mockCameras.map((camera) => (
                  <CameraIcon
                    key={camera.id}
                    camera={camera}
                    onClick={(camera) => {
                      setSelectedCamera(camera.id);
                      setPreviewCamera(camera);
                    }}
                  />
                ))}

                {/* Personnel Positions */}
                {showLayers.personnel && personnelPositions.map((person) => (
                  <PersonnelMarker key={person.id} person={person} />
                ))}

                {/* Equipment Positions */}
                {showLayers.equipment && equipmentPositions.map((equipment) => (
                  <EquipmentMarker key={equipment.id} equipment={equipment} />
                ))}
              </div>
            </div>

            {/* Map Legend */}
            <div className="absolute bottom-6 left-6 bg-white rounded-lg p-4 shadow-lg border max-w-xs">
              <h4 className="font-semibold text-gray-900 mb-3">Legend</h4>
              <div className="grid grid-cols-2 gap-2 text-xs">
                <div className="flex items-center space-x-2">
                  <div className="w-3 h-3 bg-green-500 rounded-full"></div>
                  <span>Online Camera</span>
                </div>
                <div className="flex items-center space-x-2">
                  <div className="w-3 h-3 bg-red-500 rounded-full"></div>
                  <span>Offline Camera</span>
                </div>
                <div className="flex items-center space-x-2">
                  <div className="w-3 h-3 bg-yellow-500/50 border border-yellow-500"></div>
                  <span>Safety Zone</span>
                </div>
                <div className="flex items-center space-x-2">
                  <div className="w-3 h-3 bg-red-500/50 border border-red-500"></div>
                  <span>Restricted</span>
                </div>
                <div className="flex items-center space-x-2">
                  <div className="w-3 h-3 bg-green-500 rounded-full"></div>
                  <span>Safe Personnel</span>
                </div>
                <div className="flex items-center space-x-2">
                  <div className="w-3 h-3 bg-orange-500 rounded-full"></div>
                  <span>Active Equipment</span>
                </div>
              </div>
            </div>
          </div>

          {/* Right Panel */}
          <div className="w-80 bg-gray-50 border-l border-gray-200 p-6 space-y-6 overflow-y-auto">
            {/* Layer Controls */}
            <div className="bg-white rounded-lg p-4 border border-gray-200">
              <div className="flex items-center space-x-2 mb-4">
                <Layers className="w-5 h-5 text-gray-600" />
                <h3 className="font-semibold text-gray-900">Map Layers</h3>
              </div>
              
              <div className="space-y-3">
                {Object.entries(showLayers).map(([layer, visible]) => (
                  <label key={layer} className="flex items-center space-x-3 cursor-pointer">
                    <input
                      type="checkbox"
                      checked={visible}
                      onChange={(e) => setShowLayers(prev => ({ ...prev, [layer]: e.target.checked }))}
                      className="rounded border-gray-300"
                      style={{ accentColor: theme.primary[500] }}
                    />
                    <span className="text-sm capitalize text-gray-700">
                      {layer.replace('_', ' ')}
                    </span>
                    <span className="text-xs text-gray-500 ml-auto">
                      {layer === 'cameras' ? mockCameras.length :
                       layer === 'zones' ? zones.length :
                       layer === 'personnel' ? personnelPositions.length :
                       layer === 'equipment' ? equipmentPositions.length :
                       layer === 'alerts' ? mockCameras.reduce((acc, c) => acc + c.alerts, 0) : 0}
                    </span>
                  </label>
                ))}
              </div>
            </div>

            {/* Selected Item Details */}
            {selectedCamera && (
              <div className="bg-white rounded-lg p-4 border border-gray-200">
                <h3 className="font-semibold text-gray-900 mb-3">Camera Details</h3>
                {(() => {
                  const camera = mockCameras.find(c => c.id === selectedCamera);
                  return camera ? (
                    <div className="space-y-3">
                      <div className="flex items-center justify-between">
                        <span className="text-sm text-gray-600">Name</span>
                        <span className="text-sm font-medium">{camera.name}</span>
                      </div>
                      <div className="flex items-center justify-between">
                        <span className="text-sm text-gray-600">Status</span>
                        <span className={`text-sm font-medium ${
                          camera.status === 'online' ? 'text-green-600' : 'text-red-600'
                        }`}>
                          {camera.status}
                        </span>
                      </div>
                      <div className="flex items-center justify-between">
                        <span className="text-sm text-gray-600">Type</span>
                        <span className="text-sm font-medium capitalize">{camera.type}</span>
                      </div>
                      <div className="flex items-center justify-between">
                        <span className="text-sm text-gray-600">Resolution</span>
                        <span className="text-sm font-medium">{camera.resolution}</span>
                      </div>
                      {camera.alerts > 0 && (
                        <div className="flex items-center justify-between">
                          <span className="text-sm text-gray-600">Active Alerts</span>
                          <span className="text-sm font-medium text-red-600">{camera.alerts}</span>
                        </div>
                      )}
                      
                      <div className="pt-3 border-t space-y-2">
                        <button
                          onClick={() => navigate('/live-view')}
                          className="w-full flex items-center justify-center space-x-2 p-2 bg-blue-50 text-blue-700 rounded-lg hover:bg-blue-100"
                        >
                          <Eye className="w-4 h-4" />
                          <span>View Live Feed</span>
                        </button>
                        {camera.alerts > 0 && (
                          <button
                            onClick={() => navigate('/alert-center')}
                            className="w-full flex items-center justify-center space-x-2 p-2 bg-red-50 text-red-700 rounded-lg hover:bg-red-100"
                          >
                            <AlertTriangle className="w-4 h-4" />
                            <span>View Alerts</span>
                          </button>
                        )}
                      </div>
                    </div>
                  ) : null;
                })()}
              </div>
            )}

            {selectedZone && (
              <div className="bg-white rounded-lg p-4 border border-gray-200">
                <h3 className="font-semibold text-gray-900 mb-3">Zone Details</h3>
                {(() => {
                  const zone = zones.find(z => z.id === selectedZone);
                  return zone ? (
                    <div className="space-y-3">
                      <div className="flex items-center justify-between">
                        <span className="text-sm text-gray-600">Name</span>
                        <span className="text-sm font-medium">{zone.name}</span>
                      </div>
                      <div className="flex items-center justify-between">
                        <span className="text-sm text-gray-600">Type</span>
                        <span className="text-sm font-medium capitalize">{zone.type.replace('_', ' ')}</span>
                      </div>
                      <div className="flex items-center justify-between">
                        <span className="text-sm text-gray-600">Safety Level</span>
                        <span className={`text-sm font-medium ${
                          zone.safetyLevel === 'critical' ? 'text-red-600' :
                          zone.safetyLevel === 'high' ? 'text-orange-600' :
                          zone.safetyLevel === 'medium' ? 'text-yellow-600' : 'text-green-600'
                        }`}>
                          {zone.safetyLevel}
                        </span>
                      </div>
                      <div className="flex items-center justify-between">
                        <span className="text-sm text-gray-600">Occupancy</span>
                        <span className="text-sm font-medium">
                          {zone.currentOccupancy}/{zone.maxOccupancy}
                        </span>
                      </div>
                      <div className="flex items-center justify-between">
                        <span className="text-sm text-gray-600">PPE Required</span>
                        <span className={`text-sm font-medium ${zone.requiresPPE ? 'text-red-600' : 'text-green-600'}`}>
                          {zone.requiresPPE ? 'Yes' : 'No'}
                        </span>
                      </div>
                      
                      <div className="pt-3 border-t space-y-2">
                        <button
                          onClick={() => handleEditZone(zone)}
                          className="w-full flex items-center justify-center space-x-2 p-2 bg-blue-50 text-blue-700 rounded-lg hover:bg-blue-100"
                        >
                          <Edit3 className="w-4 h-4" />
                          <span>Edit Zone</span>
                        </button>
                        <button
                          onClick={() => handleDeleteZone(zone.id)}
                          className="w-full flex items-center justify-center space-x-2 p-2 bg-red-50 text-red-700 rounded-lg hover:bg-red-100"
                        >
                          <Trash2 className="w-4 h-4" />
                          <span>Delete Zone</span>
                        </button>
                      </div>
                    </div>
                  ) : null;
                })()}
              </div>
            )}

            {/* Quick Actions */}
            <div className="bg-white rounded-lg p-4 border border-gray-200">
              <h3 className="font-semibold text-gray-900 mb-3">Quick Actions</h3>
              <div className="space-y-2">
                <button
                  onClick={() => navigate('/live-view')}
                  className="w-full flex items-center space-x-3 p-3 text-left bg-blue-50 hover:bg-blue-100 rounded-lg transition-colors"
                >
                  <Eye className="w-5 h-5 text-blue-600" />
                  <div>
                    <div className="font-medium text-blue-900">Live Monitoring</div>
                    <div className="text-xs text-blue-600">View all camera feeds</div>
                  </div>
                </button>
                
                <button
                  onClick={() => navigate('/live-street-view')}
                  className="w-full flex items-center space-x-3 p-3 text-left bg-green-50 hover:bg-green-100 rounded-lg transition-colors"
                >
                  <Navigation className="w-5 h-5 text-green-600" />
                  <div>
                    <div className="font-medium text-green-900">Street View</div>
                    <div className="text-xs text-green-600">GPS navigation</div>
                  </div>
                </button>

                <button
                  onClick={() => navigate('/path-admin')}
                  className="w-full flex items-center space-x-3 p-3 text-left bg-purple-50 hover:bg-purple-100 rounded-lg transition-colors"
                >
                  <Settings className="w-5 h-5 text-purple-600" />
                  <div>
                    <div className="font-medium text-purple-900">Path Admin</div>
                    <div className="text-xs text-purple-600">Create routes A→B→C→D</div>
                  </div>
                </button>
              </div>
            </div>

            {/* Weather & Conditions */}
            <div className="bg-white rounded-lg p-4 border border-gray-200">
              <h3 className="font-semibold text-gray-900 mb-3">Site Conditions</h3>
              <div className="grid grid-cols-2 gap-3">
                <div className="text-center p-3 bg-orange-50 rounded-lg">
                  <Thermometer className="w-6 h-6 mx-auto mb-1 text-orange-600" />
                  <div className="text-lg font-bold text-orange-600">{currentSite.weather.temp}°F</div>
                  <div className="text-xs text-gray-600">Temperature</div>
                </div>
                <div className="text-center p-3 bg-blue-50 rounded-lg">
                  <Wind className="w-6 h-6 mx-auto mb-1 text-blue-600" />
                  <div className="text-lg font-bold text-blue-600">{currentSite.weather.wind}</div>
                  <div className="text-xs text-gray-600">Wind Speed</div>
                </div>
              </div>
              <div className="mt-3 p-3 bg-gray-50 rounded-lg text-center">
                <div className="text-sm font-medium text-gray-900">{currentSite.weather.condition}</div>
                <div className="text-xs text-gray-600">Optimal for construction</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Camera Preview Modal */}
      <CameraPreviewModal />

      {/* Zone Management Modal */}
      {showZoneModal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-lg max-w-md w-full p-6">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-gray-900">
                {editingZone ? 'Edit Zone' : 'Create New Zone'}
              </h3>
              <button
                onClick={() => {
                  setShowZoneModal(false);
                  setEditingZone(null);
                }}
                className="p-2 hover:bg-gray-100 rounded-lg"
              >
                <X className="w-5 h-5" />
              </button>
            </div>
            
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Zone Name</label>
                <input
                  type="text"
                  value={editingZone ? editingZone.name : newZone.name}
                  onChange={(e) => editingZone 
                    ? setEditingZone(prev => ({ ...prev, name: e.target.value }))
                    : setNewZone(prev => ({ ...prev, name: e.target.value }))
                  }
                  className="w-full px-3 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:border-transparent"
                  placeholder="Enter zone name"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Zone Type</label>
                <select
                  value={editingZone ? editingZone.type : newZone.type}
                  onChange={(e) => editingZone 
                    ? setEditingZone(prev => ({ ...prev, type: e.target.value }))
                    : setNewZone(prev => ({ ...prev, type: e.target.value }))
                  }
                  className="w-full px-3 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:border-transparent"
                >
                  <option value="work_area">Work Area</option>
                  <option value="safety">Safety Zone</option>
                  <option value="restricted">Restricted Area</option>
                  <option value="equipment">Equipment Zone</option>
                  <option value="hazardous">Hazardous Area</option>
                </select>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Safety Level</label>
                <select
                  value={editingZone ? editingZone.safetyLevel : newZone.safetyLevel}
                  onChange={(e) => editingZone 
                    ? setEditingZone(prev => ({ ...prev, safetyLevel: e.target.value }))
                    : setNewZone(prev => ({ ...prev, safetyLevel: e.target.value }))
                  }
                  className="w-full px-3 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:border-transparent"
                >
                  <option value="low">Low</option>
                  <option value="medium">Medium</option>
                  <option value="high">High</option>
                  <option value="critical">Critical</option>
                </select>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Maximum Occupancy</label>
                <input
                  type="number"
                  min="1"
                  max="100"
                  value={editingZone ? editingZone.maxOccupancy : newZone.maxOccupancy}
                  onChange={(e) => editingZone 
                    ? setEditingZone(prev => ({ ...prev, maxOccupancy: parseInt(e.target.value) }))
                    : setNewZone(prev => ({ ...prev, maxOccupancy: parseInt(e.target.value) }))
                  }
                  className="w-full px-3 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:border-transparent"
                />
              </div>
              
              <div className="flex items-center">
                <input
                  type="checkbox"
                  id="requiresPPE"
                  checked={editingZone ? editingZone.requiresPPE : newZone.requiresPPE}
                  onChange={(e) => editingZone 
                    ? setEditingZone(prev => ({ ...prev, requiresPPE: e.target.checked }))
                    : setNewZone(prev => ({ ...prev, requiresPPE: e.target.checked }))
                  }
                  className="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
                />
                <label htmlFor="requiresPPE" className="ml-2 text-sm text-gray-700">
                  Requires PPE
                </label>
              </div>
              
              {!editingZone && (
                <div className="p-3 bg-blue-50 rounded-lg">
                  <p className="text-sm text-blue-700">
                    After creating the zone, use the drawing tools to define its boundaries on the map.
                  </p>
                </div>
              )}
            </div>
            
            <div className="flex justify-end space-x-3 mt-6">
              <button
                onClick={() => {
                  setShowZoneModal(false);
                  setEditingZone(null);
                }}
                className="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors"
              >
                Cancel
              </button>
              <button
                onClick={editingZone ? handleUpdateZone : handleCreateZone}
                disabled={editingZone ? !editingZone.name : !newZone.name}
                className="flex items-center space-x-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <Save className="w-4 h-4" />
                <span>{editingZone ? 'Update Zone' : 'Create Zone'}</span>
              </button>
            </div>
          </div>
        </div>
      )}
    </MainLayout>
  );
};

export default SiteOverview;