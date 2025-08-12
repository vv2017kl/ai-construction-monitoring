import React, { useRef, useEffect, useState } from 'react';
import { 
  Viewer, 
  Cartesian3, 
  Math as CesiumMath, 
  VerticalOrigin, 
  HeightReference,
  LabelStyle,
  Cartesian2,
  Color,
  Ion
} from 'cesium';
import 'cesium/Build/Cesium/Widgets/widgets.css';
import './cesium-overrides.css';

// Set Cesium Ion access token
const CESIUM_ACCESS_TOKEN = process.env.REACT_APP_CESIUM_ACCESS_TOKEN;
if (CESIUM_ACCESS_TOKEN) {
  Ion.defaultAccessToken = CESIUM_ACCESS_TOKEN;
}

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
      try {
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
      } catch (error) {
        console.error('Failed to initialize Cesium viewer:', error);
      }
    }

    return () => {
      if (viewerRef.current) {
        try {
          viewerRef.current.destroy();
        } catch (error) {
          console.error('Error destroying Cesium viewer:', error);
        }
        viewerRef.current = null;
        setViewer(null);
      }
    };
  }, []);

  // Site pin color determination
  const getSitePinColor = (site) => {
    const { critical, high, medium, low } = site.alerts || {};
    if (critical > 0) return '#DC2626'; // Red - Critical
    if (high > 0) return '#EA580C';     // Orange - High
    if (medium > 0) return '#D97706';   // Amber - Medium
    if (low > 0) return '#65A30D';      // Green - Low
    return '#6B7280';                   // Gray - No alerts
  };

  // Camera pin color determination  
  const getCameraPinColor = (camera) => {
    // Color based on camera alerts and status
    if (camera.alerts && camera.alerts.includes('critical')) return '#DC2626'; // Red
    if (camera.alerts && camera.alerts.includes('high')) return '#EA580C';     // Orange
    if (camera.status === 'maintenance') return '#D97706';                     // Amber
    if (camera.status === 'active') return '#65A30D';                          // Green
    return '#6B7280';                                                           // Gray - offline/unknown
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
          image: createFactoryIcon(pinColor),
          scale: 0.8,
          verticalOrigin: VerticalOrigin.BOTTOM,
          heightReference: HeightReference.CLAMP_TO_GROUND,
          disableDepthTestDistance: Number.POSITIVE_INFINITY
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
          image: createCameraIcon(pinColor, camera.type),
          scale: 0.8,
          verticalOrigin: VerticalOrigin.BOTTOM,
          heightReference: HeightReference.CLAMP_TO_GROUND,
          disableDepthTestDistance: Number.POSITIVE_INFINITY
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
    if (!viewer || !viewer.cesiumWidget || !viewer.cesiumWidget.cesiumContainer) return;

    const clickHandler = (event) => {
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
    };

    viewer.cesiumWidget.cesiumContainer.addEventListener('click', clickHandler);

    return () => {
      if (viewer && viewer.cesiumWidget && viewer.cesiumWidget.cesiumContainer) {
        viewer.cesiumWidget.cesiumContainer.removeEventListener('click', clickHandler);
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

  // Helper functions for creating factory icons
  const createFactoryIcon = (color) => {
    const canvas = document.createElement('canvas');
    canvas.width = 48;
    canvas.height = 48;
    const ctx = canvas.getContext('2d');
    
    // Clear canvas
    ctx.clearRect(0, 0, 48, 48);
    
    // Factory building base
    ctx.fillStyle = color;
    ctx.fillRect(6, 25, 36, 18);
    
    // Factory chimney 1
    ctx.fillRect(12, 15, 6, 28);
    
    // Factory chimney 2
    ctx.fillRect(30, 10, 6, 33);
    
    // Factory roof
    ctx.fillStyle = '#4A5568';
    ctx.fillRect(6, 22, 36, 6);
    
    // Factory windows
    ctx.fillStyle = '#E2E8F0';
    ctx.fillRect(10, 30, 4, 4);
    ctx.fillRect(18, 30, 4, 4);
    ctx.fillRect(26, 30, 4, 4);
    ctx.fillRect(34, 30, 4, 4);
    
    // Smoke from chimneys
    ctx.fillStyle = '#A0AEC0';
    ctx.beginPath();
    ctx.arc(15, 12, 2, 0, 2 * Math.PI);
    ctx.fill();
    ctx.beginPath();
    ctx.arc(33, 7, 2, 0, 2 * Math.PI);
    ctx.fill();
    
    // White border for visibility
    ctx.strokeStyle = '#FFFFFF';
    ctx.lineWidth = 2;
    ctx.strokeRect(6, 25, 36, 18);
    ctx.strokeRect(12, 15, 6, 28);
    ctx.strokeRect(30, 10, 6, 33);
    
    return canvas.toDataURL();
  };

  const createCameraIcon = (color, cameraType) => {
    const canvas = document.createElement('canvas');
    canvas.width = 24;
    canvas.height = 24;
    const ctx = canvas.getContext('2d');
    
    // Clear canvas
    ctx.clearRect(0, 0, 24, 24);
    
    // Camera base circle
    ctx.fillStyle = color;
    ctx.beginPath();
    ctx.arc(12, 12, 10, 0, 2 * Math.PI);
    ctx.fill();
    
    // Camera lens (larger for fisheye type)
    const lensSize = cameraType === 'fisheye' ? 6 : 4;
    ctx.fillStyle = '#1A202C';
    ctx.beginPath();
    ctx.arc(12, 12, lensSize, 0, 2 * Math.PI);
    ctx.fill();
    
    // Camera lens reflection
    ctx.fillStyle = '#4A5568';
    ctx.beginPath();
    ctx.arc(12, 12, lensSize - 1, 0, 2 * Math.PI);
    ctx.fill();
    
    // Lens highlight
    ctx.fillStyle = '#E2E8F0';
    ctx.beginPath();
    ctx.arc(10, 10, 1, 0, 2 * Math.PI);
    ctx.fill();
    
    // Camera mounting bracket (if PTZ)
    if (cameraType === 'ptz') {
      ctx.fillStyle = '#4A5568';
      ctx.fillRect(11, 20, 2, 3);
    }
    
    // White border for visibility
    ctx.strokeStyle = '#FFFFFF';
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.arc(12, 12, 10, 0, 2 * Math.PI);
    ctx.stroke();
    
    return canvas.toDataURL();
  };

  const createAlertIcon = (alertType, count) => {
    const canvas = document.createElement('canvas');
    canvas.width = 20;
    canvas.height = 20;
    const ctx = canvas.getContext('2d');
    
    // Alert colors based on type
    const colors = {
      critical: '#DC2626',
      high: '#EA580C', 
      medium: '#D97706',
      low: '#65A30D',
      info: '#2563EB'
    };
    
    // Alert circle
    ctx.fillStyle = colors[alertType] || '#6B7280';
    ctx.beginPath();
    ctx.arc(10, 10, 8, 0, 2 * Math.PI);
    ctx.fill();
    
    // Alert count text
    ctx.fillStyle = '#FFFFFF';
    ctx.font = 'bold 10px Arial';
    ctx.textAlign = 'center';
    ctx.fillText(count.toString(), 10, 14);
    
    // White border
    ctx.strokeStyle = '#FFFFFF';
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.arc(10, 10, 8, 0, 2 * Math.PI);
    ctx.stroke();
    
    return canvas.toDataURL();
  };

  const createSiteDescription = (site) => {
    return `
      <div style="font-family: Arial, sans-serif; max-width: 350px; background: white; padding: 15px; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.15);">
        <h3 style="margin: 0 0 12px 0; color: #1a202c; font-size: 18px; font-weight: bold;">${site.name}</h3>
        <div style="margin-bottom: 12px;">
          <p style="margin: 0 0 6px 0; font-size: 14px;"><strong>Code:</strong> ${site.code}</p>
          <p style="margin: 0 0 6px 0; font-size: 14px;"><strong>Type:</strong> ${site.projectType}</p>
          <p style="margin: 0 0 6px 0; font-size: 14px;"><strong>Stage:</strong> ${site.constructionStage}</p>
          <p style="margin: 0 0 6px 0; font-size: 14px;"><strong>Location:</strong> ${site.city}, ${site.country}</p>
          <p style="margin: 0 0 6px 0; font-size: 14px;"><strong>Manager:</strong> ${site.projectManager}</p>
          <p style="margin: 0 0 6px 0; font-size: 14px;"><strong>Progress:</strong> ${site.completionPercent}%</p>
        </div>
        
        <div style="margin-bottom: 12px; padding: 10px; background: #f8fafc; border-radius: 6px;">
          <h4 style="margin: 0 0 8px 0; color: #374151; font-size: 14px;">Site Status</h4>
          <p style="margin: 0 0 4px 0; font-size: 13px;">👷 Workers: ${site.activeWorkers}</p>
          <p style="margin: 0 0 4px 0; font-size: 13px;">📹 Cameras: ${site.totalCameras}</p>
          <p style="margin: 0 0 4px 0; font-size: 13px;">🛡️ Safety Score: ${site.safetyScore}%</p>
        </div>
        
        <div style="padding: 10px; background: #fef2f2; border-radius: 6px; border-left: 4px solid #dc2626;">
          <h4 style="margin: 0 0 8px 0; color: #dc2626; font-size: 14px;">Active Alerts</h4>
          <div style="display: flex; gap: 12px; font-size: 12px;">
            ${site.alerts.critical > 0 ? `<span style="color: #dc2626;">🔴 ${site.alerts.critical} Critical</span>` : ''}
            ${site.alerts.high > 0 ? `<span style="color: #ea580c;">🟠 ${site.alerts.high} High</span>` : ''}
            ${site.alerts.medium > 0 ? `<span style="color: #d97706;">🟡 ${site.alerts.medium} Medium</span>` : ''}
            ${site.alerts.low > 0 ? `<span style="color: #65a30d;">🟢 ${site.alerts.low} Low</span>` : ''}
            ${site.alerts.info > 0 ? `<span style="color: #2563eb;">ℹ️ ${site.alerts.info} Info</span>` : ''}
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