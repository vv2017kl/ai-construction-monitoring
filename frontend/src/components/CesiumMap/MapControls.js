import React, { useState } from 'react';
import { ChevronDown, MapPin, Camera, Globe, Building, Home, Navigation, Layers } from 'lucide-react';

const MapControls = ({
  sites = [],
  selectedSite = null,
  selectedRegion = null,
  viewMode = 'global',
  onSiteSelect,
  onRegionSelect,
  onViewModeChange,
  onZoomToGlobal,
  onToggleLayers,
  userRole = {},
  className = ''
}) => {
  const [siteDropdownOpen, setSiteDropdownOpen] = useState(false);
  const [layersOpen, setLayersOpen] = useState(false);

  // Import regions data
  const { regions } = require('../../data/cesiumMockData');

  // Filter sites based on user role
  const accessibleSites = sites.filter(site => {
    // Basic access control - in real app this would be more sophisticated
    if (userRole.level >= 4) return userRole.accessible_sites?.includes(site.id);
    return true; // For now, show all sites
  });

  // Group sites by region for dropdown
  const sitesByRegion = accessibleSites.reduce((acc, site) => {
    const region = site.region === 'MIDDLE_EAST' ? 'Middle East' : 'South Asia';
    if (!acc[region]) acc[region] = [];
    acc[region].push(site);
    return acc;
  }, {});

  const getViewModeIcon = () => {
    switch (viewMode) {
      case 'global': return <Globe className="w-4 h-4" />;
      case 'regional': return <MapPin className="w-4 h-4" />;
      case 'site': return <Building className="w-4 h-4" />;
      default: return <Globe className="w-4 h-4" />;
    }
  };

  const getViewModeText = () => {
    switch (viewMode) {
      case 'global': return 'Global View';
      case 'regional': return 'Regional View';
      case 'site': return `Site View${selectedSite ? ` - ${selectedSite.name}` : ''}`;
      default: return 'Global View';
    }
  };

  const getSiteStatusIcon = (site) => {
    const { critical, high, medium, low } = site.alerts || {};
    if (critical > 0) return <span className="text-red-600">🔴</span>;
    if (high > 0) return <span className="text-orange-600">🟠</span>;
    if (medium > 0) return <span className="text-amber-600">🟡</span>;
    if (low > 0) return <span className="text-green-600">🟢</span>;
    return <span className="text-gray-500">⚫</span>;
  };

  const handleSiteSelect = (site) => {
    onSiteSelect(site);
    setSiteDropdownOpen(false);
  };

  return (
    <div className={`fixed top-4 left-4 z-10 ${className}`}>
      <div className="bg-white rounded-lg shadow-lg border border-gray-200 p-2">
        {/* Site Selector Dropdown */}
        <div className="relative mb-2">
          <button
            onClick={() => setSiteDropdownOpen(!siteDropdownOpen)}
            className="w-64 max-w-[calc(100vw-6rem)] flex items-center justify-between px-3 py-2 bg-gray-50 border border-gray-300 rounded-md hover:bg-gray-100 transition-colors"
          >
            <div className="flex items-center space-x-2">
              <Building className="w-4 h-4 text-gray-600" />
              <span className="text-sm font-medium text-gray-700">
                {selectedSite ? selectedSite.name : 'Select Site'}
              </span>
            </div>
            <ChevronDown 
              className={`w-4 h-4 text-gray-500 transition-transform ${
                siteDropdownOpen ? 'rotate-180' : ''
              }`}
            />
          </button>

          {siteDropdownOpen && (
            <div className="absolute top-full left-0 mt-1 w-full bg-white border border-gray-200 rounded-md shadow-lg max-h-96 overflow-y-auto z-20">
              <div className="p-2">
                <button
                  onClick={() => {
                    onZoomToGlobal();
                    setSiteDropdownOpen(false);
                  }}
                  className="w-full flex items-center space-x-2 px-3 py-2 text-left hover:bg-blue-50 rounded-md transition-colors"
                >
                  <Globe className="w-4 h-4 text-blue-600" />
                  <span className="text-sm text-blue-600 font-medium">View All Sites</span>
                </button>
              </div>

              <div className="border-t border-gray-100">
                {Object.entries(sitesByRegion).map(([region, regionSites]) => (
                  <div key={region} className="p-1">
                    <div className="px-3 py-1 text-xs font-semibold text-gray-500 uppercase tracking-wide bg-gray-50">
                      {region}
                    </div>
                    {regionSites.map(site => (
                      <button
                        key={site.id}
                        onClick={() => handleSiteSelect(site)}
                        className={`w-full flex items-center justify-between px-3 py-2 text-left hover:bg-gray-50 transition-colors ${
                          selectedSite?.id === site.id ? 'bg-blue-50 border-l-2 border-blue-500' : ''
                        }`}
                      >
                        <div className="flex items-center space-x-2">
                          {getSiteStatusIcon(site)}
                          <div>
                            <div className="text-sm font-medium text-gray-900">{site.name}</div>
                            <div className="text-xs text-gray-500">{site.code} • {site.project_type}</div>
                          </div>
                        </div>
                        <div className="text-right">
                          <div className="text-xs text-gray-500">{site.site_stats?.active_cameras || 0} cameras</div>
                          <div className="text-xs text-red-500">
                            {(site.alert_summary?.critical || 0) + (site.alert_summary?.high || 0)} alerts
                          </div>
                        </div>
                      </button>
                    ))}
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* View Mode Controls */}
        <div className="flex items-center space-x-1 mb-2">
          <button
            onClick={() => onViewModeChange('global')}
            className={`flex items-center space-x-1 px-2 py-1 rounded text-xs transition-colors ${
              viewMode === 'global' 
                ? 'bg-blue-100 text-blue-700' 
                : 'text-gray-600 hover:bg-gray-100'
            }`}
          >
            <Globe className="w-3 h-3" />
            <span>Global</span>
          </button>
          <button
            onClick={() => onViewModeChange('regional')}
            className={`flex items-center space-x-1 px-2 py-1 rounded text-xs transition-colors ${
              viewMode === 'regional' 
                ? 'bg-blue-100 text-blue-700' 
                : 'text-gray-600 hover:bg-gray-100'
            }`}
            disabled={!selectedSite}
          >
            <MapPin className="w-3 h-3" />
            <span>Regional</span>
          </button>
          <button
            onClick={() => onViewModeChange('site')}
            className={`flex items-center space-x-1 px-2 py-1 rounded text-xs transition-colors ${
              viewMode === 'site' 
                ? 'bg-blue-100 text-blue-700' 
                : 'text-gray-600 hover:bg-gray-100'
            }`}
            disabled={!selectedSite}
          >
            <Building className="w-3 h-3" />
            <span>Site</span>
          </button>
        </div>

        {/* Current View Status */}
        <div className="flex items-center justify-between px-2 py-1 bg-gray-50 rounded text-xs">
          <div className="flex items-center space-x-1">
            {getViewModeIcon()}
            <span className="text-gray-700">{getViewModeText()}</span>
          </div>
          {selectedSite && (
            <div className="flex items-center space-x-1">
              <Camera className="w-3 h-3 text-gray-500" />
              <span className="text-gray-500">
                {selectedSite.site_stats?.active_cameras || 0} cameras
              </span>
            </div>
          )}
        </div>

        {/* Layer Controls */}
        <div className="relative mt-2">
          <button
            onClick={() => setLayersOpen(!layersOpen)}
            className="flex items-center space-x-1 px-2 py-1 text-xs text-gray-600 hover:bg-gray-100 rounded transition-colors"
          >
            <Layers className="w-3 h-3" />
            <span>Layers</span>
            <ChevronDown 
              className={`w-3 h-3 transition-transform ${
                layersOpen ? 'rotate-180' : ''
              }`}
            />
          </button>

          {layersOpen && (
            <div className="absolute top-full left-0 mt-1 bg-white border border-gray-200 rounded-md shadow-lg p-2 min-w-48 z-20">
              <label className="flex items-center space-x-2 text-xs py-1">
                <input type="checkbox" className="form-checkbox h-3 w-3 text-blue-600" defaultChecked />
                <span>Site Boundaries</span>
              </label>
              <label className="flex items-center space-x-2 text-xs py-1">
                <input type="checkbox" className="form-checkbox h-3 w-3 text-blue-600" defaultChecked />
                <span>Camera Labels</span>
              </label>
              <label className="flex items-center space-x-2 text-xs py-1">
                <input type="checkbox" className="form-checkbox h-3 w-3 text-blue-600" defaultChecked />
                <span>Alert Indicators</span>
              </label>
              <label className="flex items-center space-x-2 text-xs py-1">
                <input type="checkbox" className="form-checkbox h-3 w-3 text-blue-600" />
                <span>Terrain</span>
              </label>
            </div>
          )}
        </div>

        {/* Legend */}
        {viewMode !== 'global' && (
          <div className="mt-2 pt-2 border-t border-gray-200">
            <div className="text-xs font-medium text-gray-600 mb-1">Legend</div>
            <div className="space-y-1">
              {viewMode === 'site' ? (
                // Camera legend
                <>
                  <div className="flex items-center space-x-2 text-xs">
                    <span className="text-green-500">🟢</span>
                    <span className="text-gray-600">Normal</span>
                  </div>
                  <div className="flex items-center space-x-2 text-xs">
                    <span className="text-orange-500">🟠</span>
                    <span className="text-gray-600">Warning</span>
                  </div>
                  <div className="flex items-center space-x-2 text-xs">
                    <span className="text-red-500">🔴</span>
                    <span className="text-gray-600">Critical</span>
                  </div>
                  <div className="flex items-center space-x-2 text-xs">
                    <span className="text-gray-500">⚫</span>
                    <span className="text-gray-600">Offline</span>
                  </div>
                </>
              ) : (
                // Site legend
                <>
                  <div className="flex items-center space-x-2 text-xs">
                    <span className="text-green-500">🟢</span>
                    <span className="text-gray-600">No alerts</span>
                  </div>
                  <div className="flex items-center space-x-2 text-xs">
                    <span className="text-orange-500">🟠</span>
                    <span className="text-gray-600">High alerts</span>
                  </div>
                  <div className="flex items-center space-x-2 text-xs">
                    <span className="text-red-500">🔴</span>
                    <span className="text-gray-600">Critical alerts</span>
                  </div>
                </>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default MapControls;