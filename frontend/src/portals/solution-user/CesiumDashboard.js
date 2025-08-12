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
  const [isFullscreen, setIsFullscreen] = useState(false);
  const [showSidebar, setShowSidebar] = useState(true);

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



  const breadcrumbItems = getBreadcrumb();

  return (
    // Pure immersive mode without MainLayout
    <div className="fixed inset-0 z-50 bg-black h-screen w-screen">
      {/* Top Navigation Controls */}
      <div className="absolute top-4 right-4 z-30 flex items-center space-x-2">
        <button
          onClick={() => navigate('/dashboard')}
          className="flex items-center space-x-2 px-3 py-2 bg-black bg-opacity-50 hover:bg-opacity-70 text-white rounded-md transition-all"
        >
          <Home className="w-4 h-4" />
          <span>Dashboard</span>
        </button>
      </div>

      {/* Main Map Container */}
      <div className="h-full">
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
      </div>
    </div>
  );
};

export default CesiumDashboard;