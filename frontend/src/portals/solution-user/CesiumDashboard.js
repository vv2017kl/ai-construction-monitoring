import React, { useState, useEffect, useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import MainLayout from '../../components/Layout/MainLayout';
import CesiumContainer from '../../components/CesiumMap/CesiumContainer';
import MapControls from '../../components/CesiumMap/MapControls';
import AlertSummaryPanel from '../../components/CesiumMap/AlertSummaryPanel';
import { useTheme } from '../../context/ThemeContext';
import { mockSites, mockCameras, regions } from '../../data/cesiumMockData';
import { ArrowLeft, Home, Navigation2, Maximize } from 'lucide-react';

const CesiumDashboard = () => {
  const navigate = useNavigate();
  const { theme } = useTheme();
  
  // Map state
  const [viewMode, setViewMode] = useState('global'); // 'global', 'regional', 'site'
  const [selectedSite, setSelectedSite] = useState(null);
  const [selectedCamera, setSelectedCamera] = useState(null);
  const [selectedRegion, setSelectedRegion] = useState(null);
  const [showAlertPanel, setShowAlertPanel] = useState(false);
  
  // UI state - Default to fullscreen with collapsed sidebar
  const [isFullscreen, setIsFullscreen] = useState(true);
  const [showSidebar, setShowSidebar] = useState(false);

  // User context (mock - in real app this would come from auth context)
  const [userRole] = useState({
    level: 4, // Site Manager
    company_id: '11111111-1111-1111-1111-111111111111',
    accessible_sites: ['dubai-001', 'dubai-002', 'mumbai-001'], // Mock accessible sites
    accessible_groups: ['33333333-3333-3333-3333-333333333333']
  });

  // Filter sites and cameras based on user permissions
  const accessibleSites = mockSites.filter(site => {
    if (userRole.level === 1) return true; // SysAdmin
    if (userRole.level === 2) return site.company_id === userRole.company_id;
    if (userRole.level === 3) return userRole.accessible_groups.includes(site.group_id);
    if (userRole.level >= 4) return userRole.accessible_sites.includes(site.id);
    return false;
  });

  const getCurrentCameras = () => {
    if (!selectedSite) return [];
    return mockCameras[selectedSite.id] || [];
  };

  // Navigation breadcrumb
  const getBreadcrumb = () => {
    const items = [
      { label: 'Construction Management', action: () => navigate('/dashboard') },
      { label: 'Cesium Map', action: () => setViewMode('global') }
    ];

    if (selectedRegion) {
      items.push({ label: selectedRegion, action: () => setViewMode('regional') });
    }
    
    if (selectedSite) {
      items.push({ label: selectedSite.name, action: () => setViewMode('site') });
    }

    if (selectedCamera) {
      items.push({ label: selectedCamera.name, active: true });
    }

    return items;
  };

  // Event handlers
  const handleSiteClick = (site) => {
    setSelectedSite(site);
    setSelectedCamera(null);
    setViewMode('site');
    setShowAlertPanel(true);
  };

  const handleCameraClick = (camera) => {
    setSelectedCamera(camera);
    // Navigate to live view with collapsed sidebar
    navigate(`/live-view/${camera.id}?mapContext=true&sidebar=collapsed`);
  };

  const handleSiteSelect = (site) => {
    setSelectedSite(site);
    setSelectedCamera(null);
    setViewMode(site ? 'site' : 'global');
    setShowAlertPanel(!!site);
  };

  const handleViewModeChange = (mode) => {
    setViewMode(mode);
    if (mode === 'global') {
      setSelectedSite(null);
      setSelectedCamera(null);
      setShowAlertPanel(false);
    }
  };

  const handleZoomToGlobal = () => {
    setViewMode('global');
    setSelectedSite(null);
    setSelectedCamera(null);
    setSelectedRegion(null);
    setShowAlertPanel(false);
  };

  const toggleFullscreen = () => {
    setIsFullscreen(!isFullscreen);
    setShowSidebar(isFullscreen); // Show sidebar when exiting fullscreen, hide when entering
  };

  // Keyboard shortcuts
  useEffect(() => {
    const handleKeyPress = (event) => {
      if (event.key === 'Escape') {
        if (isFullscreen && (selectedCamera || selectedSite)) {
          // If in fullscreen with selection, clear selection first
          if (selectedCamera) {
            setSelectedCamera(null);
          } else if (selectedSite) {
            setSelectedSite(null);
            setViewMode('global');
            setShowAlertPanel(false);
          }
        } else if (isFullscreen) {
          // If just in fullscreen with no selection, exit fullscreen
          setIsFullscreen(false);
          setShowSidebar(true);
        }
      } else if (event.key === 'F11') {
        event.preventDefault();
        toggleFullscreen();
      }
    };

    window.addEventListener('keydown', handleKeyPress);
    return () => window.removeEventListener('keydown', handleKeyPress);
  }, [isFullscreen, selectedCamera, selectedSite]);

  const breadcrumbItems = getBreadcrumb();

  return (
    <MainLayout 
      showSidebar={showSidebar}
      className={isFullscreen ? 'fixed inset-0 z-50 bg-black' : ''}
    >
      <div className={`relative ${isFullscreen ? 'h-screen w-screen' : 'h-full w-full'}`}>
        {/* Header Bar - Show only when sidebar is visible */}
        {showSidebar && (
          <div className="absolute top-0 left-0 right-0 z-30 bg-white border-b border-gray-200 px-6 py-3">
            <div className="flex items-center justify-between">
              {/* Breadcrumb Navigation */}
              <nav className="flex items-center space-x-2 text-sm">
                {breadcrumbItems.map((item, index) => (
                  <React.Fragment key={index}>
                    {index > 0 && <span className="text-gray-400">/</span>}
                    {item.active ? (
                      <span className="text-gray-900 font-medium">{item.label}</span>
                    ) : (
                      <button
                        onClick={item.action}
                        className="text-blue-600 hover:text-blue-800 transition-colors"
                      >
                        {item.label}
                      </button>
                    )}
                  </React.Fragment>
                ))}
              </nav>

              {/* Action Buttons */}
              <div className="flex items-center space-x-2">
                <button
                  onClick={() => navigate('/dashboard')}
                  className="flex items-center space-x-2 px-3 py-1.5 text-sm bg-gray-100 hover:bg-gray-200 rounded-md transition-colors"
                >
                  <Home className="w-4 h-4" />
                  <span>Dashboard</span>
                </button>
                <button
                  onClick={toggleFullscreen}
                  className="flex items-center space-x-2 px-3 py-1.5 text-sm bg-blue-100 hover:bg-blue-200 text-blue-700 rounded-md transition-colors"
                >
                  <Maximize className="w-4 h-4" />
                  <span>Exit Immersive</span>
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Fullscreen Controls - Show when sidebar is hidden */}
        {!showSidebar && (
          <div className="absolute top-4 right-4 z-30 flex items-center space-x-2">
            <button
              onClick={() => navigate('/dashboard')}
              className="flex items-center space-x-2 px-3 py-2 bg-black bg-opacity-50 hover:bg-opacity-70 text-white rounded-md transition-all"
            >
              <Home className="w-4 h-4" />
              <span>Dashboard</span>
            </button>
            <button
              onClick={toggleFullscreen}
              className="flex items-center space-x-2 px-3 py-2 bg-black bg-opacity-50 hover:bg-opacity-70 text-white rounded-md transition-all"
            >
              <ArrowLeft className="w-4 h-4" />
              <span>Show Sidebar</span>
            </button>
          </div>
        )}

        {/* Main Map Container */}
        <div className={`${showSidebar ? 'h-full pt-16' : 'h-full'}`}>
          <CesiumContainer
            sites={accessibleSites}
            cameras={getCurrentCameras()}
            selectedSite={selectedSite}
            selectedCamera={selectedCamera}
            viewMode={viewMode}
            onSiteClick={handleSiteClick}
            onCameraClick={handleCameraClick}
            className="h-full w-full"
          />

          {/* Map Controls */}
          <MapControls
            sites={accessibleSites}
            selectedSite={selectedSite}
            selectedRegion={selectedRegion}
            viewMode={viewMode}
            onSiteSelect={handleSiteSelect}
            onRegionSelect={setSelectedRegion}
            onViewModeChange={handleViewModeChange}
            onZoomToGlobal={handleZoomToGlobal}
            userRole={userRole}
          />

          {/* Alert Summary Panel */}
          <AlertSummaryPanel
            site={selectedSite}
            cameras={getCurrentCameras()}
            visible={showAlertPanel}
            onClose={() => setShowAlertPanel(false)}
            onViewSite={(site) => {
              navigate(`/site-overview/${site.id}`);
            }}
            onViewCamera={handleCameraClick}
          />

          {/* Status Bar - Show when sidebar is visible */}
          {showSidebar && (
            <div className="absolute bottom-4 left-1/2 transform -translate-x-1/2 z-20">
              <div className="bg-black bg-opacity-70 text-white px-4 py-2 rounded-full text-sm">
                <div className="flex items-center space-x-4">
                  <span className="flex items-center space-x-1">
                    <Navigation2 className="w-4 h-4" />
                    <span>
                      {viewMode === 'global' && 'Global View'}
                      {viewMode === 'regional' && `Regional: ${selectedRegion || 'All Regions'}`}
                      {viewMode === 'site' && `Site: ${selectedSite?.name || 'None Selected'}`}
                    </span>
                  </span>
                  <span>•</span>
                  <span>{accessibleSites.length} accessible sites</span>
                  {selectedSite && (
                    <>
                      <span>•</span>
                      <span>{getCurrentCameras().length} cameras</span>
                    </>
                  )}
                </div>
              </div>
            </div>
          )}

          {/* Help Text */}
          {viewMode === 'global' && !selectedSite && (
            <div className="absolute bottom-20 left-1/2 transform -translate-x-1/2 z-20">
              <div className="bg-blue-50 border border-blue-200 text-blue-800 px-4 py-2 rounded-lg text-sm text-center max-w-md">
                <p className="font-medium">🗺️ Welcome to Cesium Site Manager</p>
                <p className="mt-1">Click on site pins to drill down, or use the site selector to navigate directly.</p>
              </div>
            </div>
          )}
        </div>
      </div>
    </MainLayout>
  );
};

export default CesiumDashboard;