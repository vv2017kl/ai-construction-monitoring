import React, { useRef, useEffect, useState } from 'react';
import { 
  Viewer, 
  createWorldTerrainAsync, 
  Cartesian3, 
  Math as CesiumMath, 
  VerticalOrigin, 
  HeightReference,
  LabelStyle,
  Cartesian2,
  Color
} from 'cesium';
import 'cesium/Build/Cesium/Widgets/widgets.css';
import './cesium-overrides.css';

const CesiumContainer = ({
  sites = [],
  cameras = [],
  selectedSite = null,
  selectedCamera = null,
  viewMode = 'global', // 'global', 'regional', 'site'
  onSiteClick,
  onCameraClick,
  className = ''
}) => {
  const viewerRef = useRef(null);
  const cesiumContainerRef = useRef(null);
  const [viewer, setViewer] = useState(null);
  const sitePinsRef = useRef([]);
  const cameraPinsRef = useRef([]);

  // Initialize Cesium viewer
  useEffect(() => {
    if (cesiumContainerRef.current && !viewer) {
      const cesiumViewer = new Viewer(cesiumContainerRef.current, {
        baseLayerPicker: false,
        geocoder: false,
        homeButton: false,
        sceneModePicker: false,
        navigationHelpButton: false,
        animation: false,
        timeline: false,
        fullscreenButton: false,
        vrButton: false
      });

      // Load terrain asynchronously (optional)
      createWorldTerrainAsync({
        requestVertexNormals: true,
        requestWaterMask: true,
      }).then(terrain => {
        cesiumViewer.terrainProvider = terrain;
      }).catch(error => {
        console.warn('Failed to load terrain:', error);
        // Continue without terrain
      });

      // Set initial camera position (global view)
      cesiumViewer.camera.setView({
        destination: Cartesian3.fromDegrees(65.0000, 20.0000, 5000000), // Between Dubai and India
        orientation: {
          heading: 0.0,
          pitch: -CesiumMath.PI_OVER_TWO,
          roll: 0.0
        }
      });

      setViewer(cesiumViewer);
      viewerRef.current = cesiumViewer;
    }

    return () => {
      if (viewerRef.current) {
        viewerRef.current.destroy();
        viewerRef.current = null;
        setViewer(null);
      }
    };
  }, []);

  // Site pin color determination
  const getSitePinColor = (site) => {
    const { critical, high, medium } = site.alert_summary || {};
    if (critical > 0) return '#FF0000'; // Red
    if (high > 0) return '#FF8C00';     // Orange
    if (medium > 0) return '#FFD700';   // Gold
    return '#32CD32';                   // Green
  };

  // Camera pin color determination
  const getCameraPinColor = (camera) => {
    switch (camera.status) {
      case 'critical': return '#FF0000';    // Red
      case 'warning': return '#FFA500';     // Orange
      case 'maintenance': return '#FFFF00'; // Yellow
      case 'normal': return '#00FF00';      // Green
      default: return '#808080';            // Gray
    }
  };

  // Create site pins
  useEffect(() => {
    if (!viewer || !sites.length) return;

    // Clear existing site pins
    sitePinsRef.current.forEach(entity => {
      viewer.entities.remove(entity);
    });
    sitePinsRef.current = [];

    // Add site pins
    sites.forEach(site => {
      const [longitude, latitude, height = 0] = site.coordinates;
      const pinColor = getSitePinColor(site);
      
      const siteEntity = viewer.entities.add({
        id: `site-${site.id}`,
        position: Cartesian3.fromDegrees(longitude, latitude, height + 100),
        billboard: {
          image: createSitePinImage(pinColor, site.project_type),
          scale: 0.8,
          verticalOrigin: VerticalOrigin.BOTTOM,
          heightReference: HeightReference.CLAMP_TO_GROUND
        },
        label: {
          text: site.name,
          font: '12pt sans-serif',
          fillColor: Color.WHITE,
          outlineColor: Color.BLACK,
          outlineWidth: 2,
          style: LabelStyle.FILL_AND_OUTLINE,
          pixelOffset: new Cartesian2(0, -50),
          show: viewMode === 'global' || viewMode === 'regional'
        },
        description: createSiteDescription(site),
        properties: {
          type: 'site',
          siteData: site
        }
      });

      sitePinsRef.current.push(siteEntity);
    });
  }, [viewer, sites, viewMode]);

  // Create camera pins
  useEffect(() => {
    if (!viewer || !cameras.length || viewMode !== 'site') return;

    // Clear existing camera pins
    cameraPinsRef.current.forEach(entity => {
      viewer.entities.remove(entity);
    });
    cameraPinsRef.current = [];

    // Add camera pins
    cameras.forEach(camera => {
      const [longitude, latitude, height = 0] = camera.coordinates;
      const pinColor = getCameraPinColor(camera);
      
      const cameraEntity = viewer.entities.add({
        id: `camera-${camera.id}`,
        position: Cartesian3.fromDegrees(longitude, latitude, height),
        billboard: {
          image: createCameraPinImage(pinColor, camera.type),
          scale: 0.6,
          verticalOrigin: VerticalOrigin.BOTTOM,
          heightReference: HeightReference.CLAMP_TO_GROUND
        },
        label: {
          text: camera.name,
          font: '10pt sans-serif',
          fillColor: Color.WHITE,
          outlineColor: Color.BLACK,
          outlineWidth: 1,
          style: LabelStyle.FILL_AND_OUTLINE,
          pixelOffset: new Cartesian2(0, -30),
          show: true
        },
        description: createCameraDescription(camera),
        properties: {
          type: 'camera',
          cameraData: camera
        }
      });

      cameraPinsRef.current.push(cameraEntity);
    });
  }, [viewer, cameras, viewMode]);

  // Handle click events
  useEffect(() => {
    if (!viewer) return;

    const handler = viewer.cesiumWidget.cesiumContainer.addEventListener('click', (event) => {
      const picked = viewer.scene.pick(viewer.camera.getPickRay(event));
      
      if (picked && picked.id) {
        const entity = picked.id;
        const properties = entity.properties;
        
        if (properties && properties.type) {
          if (properties.type._value === 'site' && onSiteClick) {
            onSiteClick(properties.siteData._value);
          } else if (properties.type._value === 'camera' && onCameraClick) {
            onCameraClick(properties.cameraData._value);
          }
        }
      }
    });

    return () => {
      if (handler) {
        viewer.cesiumWidget.cesiumContainer.removeEventListener('click', handler);
      }
    };
  }, [viewer, onSiteClick, onCameraClick]);

  // Camera movement based on view mode
  useEffect(() => {
    if (!viewer) return;

    switch (viewMode) {
      case 'global':
        viewer.camera.setView({
          destination: Cartesian3.fromDegrees(65.0000, 20.0000, 5000000),
          orientation: {
            heading: 0.0,
            pitch: -CesiumMath.PI_OVER_TWO,
            roll: 0.0
          }
        });
        break;
      
      case 'regional':
        if (selectedSite) {
          const [longitude, latitude] = selectedSite.coordinates;
          viewer.camera.setView({
            destination: Cartesian3.fromDegrees(longitude, latitude, 50000),
            orientation: {
              heading: 0.0,
              pitch: -CesiumMath.PI_OVER_FOUR,
              roll: 0.0
            }
          });
        }
        break;
      
      case 'site':
        if (selectedSite) {
          const [longitude, latitude] = selectedSite.coordinates;
          viewer.camera.setView({
            destination: Cartesian3.fromDegrees(longitude, latitude, 1000),
            orientation: {
              heading: 0.0,
              pitch: -CesiumMath.PI_OVER_FOUR,
              roll: 0.0
            }
          });
        }
        break;
    }
  }, [viewer, viewMode, selectedSite]);

  // Helper functions
  const createSitePinImage = (color, projectType) => {
    const canvas = document.createElement('canvas');
    canvas.width = 48;
    canvas.height = 64;
    const ctx = canvas.getContext('2d');
    
    // Draw pin shape
    ctx.fillStyle = color;
    ctx.beginPath();
    ctx.arc(24, 20, 18, 0, 2 * Math.PI);
    ctx.fill();
    
    // Draw pin point
    ctx.beginPath();
    ctx.moveTo(24, 38);
    ctx.lineTo(12, 52);
    ctx.lineTo(36, 52);
    ctx.closePath();
    ctx.fill();
    
    // Add project type icon
    ctx.fillStyle = '#FFFFFF';
    ctx.font = 'bold 16px Arial';
    ctx.textAlign = 'center';
    ctx.fillText(getProjectTypeIcon(projectType), 24, 26);
    
    return canvas.toDataURL();
  };

  const createCameraPinImage = (color, cameraType) => {
    const canvas = document.createElement('canvas');
    canvas.width = 32;
    canvas.height = 32;
    const ctx = canvas.getContext('2d');
    
    // Draw camera circle
    ctx.fillStyle = color;
    ctx.beginPath();
    ctx.arc(16, 16, 14, 0, 2 * Math.PI);
    ctx.fill();
    
    // Draw camera icon
    ctx.fillStyle = '#FFFFFF';
    ctx.font = 'bold 12px Arial';
    ctx.textAlign = 'center';
    ctx.fillText('📹', 16, 20);
    
    return canvas.toDataURL();
  };

  const getProjectTypeIcon = (projectType) => {
    switch (projectType) {
      case 'commercial': return '🏢';
      case 'residential': return '🏠';
      case 'industrial': return '🏭';
      case 'infrastructure': return '🌉';
      default: return '🏗️';
    }
  };

  const createSiteDescription = (site) => {
    const { alert_summary, site_stats } = site;
    return `
      <div style="font-family: Arial, sans-serif; max-width: 300px;">
        <h3 style="margin: 0 0 10px 0; color: #2c3e50;">${site.name}</h3>
        <p style="margin: 0 0 5px 0;"><strong>Code:</strong> ${site.code}</p>
        <p style="margin: 0 0 5px 0;"><strong>Type:</strong> ${site.project_type}</p>
        <p style="margin: 0 0 5px 0;"><strong>Phase:</strong> ${site.project_phase}</p>
        <p style="margin: 0 0 10px 0;"><strong>Location:</strong> ${site.city}, ${site.country}</p>
        
        <div style="background: #f8f9fa; padding: 8px; border-radius: 4px; margin: 10px 0;">
          <h4 style="margin: 0 0 5px 0; color: #e74c3c;">🚨 Active Alerts</h4>
          <div style="display: flex; gap: 10px; font-size: 12px;">
            <span style="color: #e74c3c;">Critical: ${alert_summary.critical}</span>
            <span style="color: #f39c12;">High: ${alert_summary.high}</span>
            <span style="color: #f1c40f;">Medium: ${alert_summary.medium}</span>
          </div>
        </div>
        
        <div style="background: #e8f5e8; padding: 8px; border-radius: 4px;">
          <h4 style="margin: 0 0 5px 0; color: #27ae60;">📊 Site Stats</h4>
          <div style="font-size: 12px;">
            <p style="margin: 2px 0;">📹 Cameras: ${site_stats.active_cameras}/${site_stats.total_cameras}</p>
            <p style="margin: 2px 0;">👷 Personnel: ${site_stats.personnel_count}</p>
            <p style="margin: 2px 0;">🏗️ Equipment: ${site_stats.equipment_count}</p>
          </div>
        </div>
      </div>
    `;
  };

  const createCameraDescription = (camera) => {
    return `
      <div style="font-family: Arial, sans-serif; max-width: 250px;">
        <h3 style="margin: 0 0 10px 0; color: #2c3e50;">${camera.name}</h3>
        <p style="margin: 0 0 5px 0;"><strong>Type:</strong> ${camera.type}</p>
        <p style="margin: 0 0 5px 0;"><strong>Status:</strong> 
          <span style="color: ${getCameraPinColor(camera)};">⬤</span> ${camera.status}
        </p>
        <p style="margin: 0 0 5px 0;"><strong>Technical:</strong> ${camera.technical_status}</p>
        
        ${camera.alerts.active > 0 ? `
          <div style="background: #fff3cd; padding: 6px; border-radius: 4px; margin: 8px 0;">
            <h4 style="margin: 0 0 3px 0; color: #856404;">⚠️ Active Alerts: ${camera.alerts.active}</h4>
            <p style="margin: 0; font-size: 11px;">Last: ${camera.alerts.alert_type}</p>
          </div>
        ` : `
          <div style="background: #d4edda; padding: 6px; border-radius: 4px; margin: 8px 0;">
            <p style="margin: 0; color: #155724; font-size: 11px;">✅ No active alerts</p>
          </div>
        `}
        
        <div style="margin-top: 10px;">
          <button onclick="viewLiveStream('${camera.id}')" 
                  style="background: #007bff; color: white; border: none; padding: 6px 12px; border-radius: 4px; cursor: pointer;">
            📹 View Live Stream
          </button>
        </div>
      </div>
    `;
  };

  // Expose viewLiveStream function globally for button clicks
  useEffect(() => {
    window.viewLiveStream = (cameraId) => {
      const camera = cameras.find(c => c.id === cameraId);
      if (camera && onCameraClick) {
        onCameraClick(camera);
      }
    };
    
    return () => {
      delete window.viewLiveStream;
    };
  }, [cameras, onCameraClick]);

  return (
    <div 
      ref={cesiumContainerRef} 
      className={`cesium-container ${className}`}
      style={{ 
        width: '100%', 
        height: '100%', 
        display: 'block',
        position: 'relative'
      }}
    />
  );
};

export default CesiumContainer;