# Cesium-Based Geospatial Site Management Implementation Plan

## **Feature Overview**
Create a Cesium-powered interactive map interface for construction site management with:
- Global site overview with alert summaries
- Site-specific drill down with camera positioning
- Live camera integration with map context
- Role-based access control
- User preference for default dashboard type

---

## **1. Component Architecture**

### **New Components to Create:**
```
frontend/src/components/
├── CesiumMap/
│   ├── CesiumContainer.js          # Main Cesium viewer container
│   ├── SitePin.js                  # Site marker with alert summary
│   ├── CameraPin.js                # Camera marker with status
│   ├── MapControls.js              # Zoom, layers, site selector
│   ├── AlertSummaryPanel.js        # Floating panel with alert details
│   └── MapNavigation.js            # Breadcrumb navigation
└── shared/
    └── MapLiveView.js              # Live view with map return option
```

### **New Pages:**
```
frontend/src/portals/solution-user/
├── CesiumDashboard.js              # Main map dashboard
└── MapLiveView.js                  # Live view with map context
```

---

## **2. Sample Data Structure**

### **Dubai Sites (4 sites)**
```javascript
const dubaiSites = [
  {
    id: 'dubai-001',
    name: 'Downtown Dubai Tower',
    coordinates: [55.2744, 25.1972], // Near Burj Khalifa
    project_type: 'commercial',
    alert_summary: { critical: 2, high: 5, medium: 12 }
  },
  {
    id: 'dubai-002', 
    name: 'Dubai Marina Residential Complex',
    coordinates: [55.1384, 25.0777], // Dubai Marina
    project_type: 'residential',
    alert_summary: { critical: 0, high: 3, medium: 8 }
  },
  {
    id: 'dubai-003',
    name: 'Palm Jumeirah Villa Project',
    coordinates: [55.1167, 25.1124], // Palm Jumeirah
    project_type: 'residential', 
    alert_summary: { critical: 1, high: 2, medium: 6 }
  },
  {
    id: 'dubai-004',
    name: 'DIFC Office Complex',
    coordinates: [55.2089, 25.2135], // Dubai International Financial Centre
    project_type: 'commercial',
    alert_summary: { critical: 0, high: 1, medium: 4 }
  }
];
```

### **India Sites (4 sites)**
```javascript
const indiaSites = [
  {
    id: 'mumbai-001',
    name: 'Bandra-Kurla Complex Office Tower',
    coordinates: [72.8697, 19.0625], // BKC Mumbai
    project_type: 'commercial',
    alert_summary: { critical: 3, high: 7, medium: 15 }
  },
  {
    id: 'bangalore-001',
    name: 'Electronic City IT Campus',
    coordinates: [77.6648, 12.8456], // Electronic City Bangalore
    project_type: 'commercial',
    alert_summary: { critical: 1, high: 4, medium: 9 }
  },
  {
    id: 'delhi-001',
    name: 'Gurgaon Cyber Hub Extension',
    coordinates: [77.0688, 28.4595], // Gurgaon
    project_type: 'commercial',
    alert_summary: { critical: 2, high: 6, medium: 11 }
  },
  {
    id: 'pune-001',
    name: 'Hinjewadi Tech Park Phase 4',
    coordinates: [73.7274, 18.5912], // Hinjewadi Pune
    project_type: 'commercial',
    alert_summary: { critical: 0, high: 2, medium: 7 }
  }
];
```

### **Camera Positions Per Site (3-4 cameras each)**
```javascript
const siteCamera = {
  'dubai-001': [
    { id: 'cam-001', name: 'Main Entrance', position: [55.2745, 25.1973], status: 'critical', type: 'entrance' },
    { id: 'cam-002', name: 'Crane Zone A', position: [55.2743, 25.1971], status: 'normal', type: 'equipment' },
    { id: 'cam-003', name: 'Floor 25 Overview', position: [55.2744, 25.1970], status: 'warning', type: 'overview' },
    { id: 'cam-004', name: 'Material Storage', position: [55.2746, 25.1974], status: 'normal', type: 'storage' }
  ]
  // ... similar for all sites
};
```

---

## **3. Pin Color Coding System**

### **Site Pins:**
```javascript
const sitePinColors = {
  critical: '#FF0000',    // Red - Critical alerts present
  high: '#FF8C00',        // Orange - High priority alerts
  medium: '#FFD700',      // Gold - Medium alerts only
  normal: '#32CD32',      // Green - No significant alerts
  offline: '#808080'      // Gray - Site offline/inactive
};
```

### **Camera Pins:**
```javascript
const cameraPinColors = {
  critical: '#FF0000',    // Red - Safety violations detected
  warning: '#FFA500',     // Orange - PPE compliance issues
  maintenance: '#FFFF00', // Yellow - Maintenance required
  normal: '#00FF00',      // Green - Operating normally
  offline: '#808080'      // Gray - Camera offline
};
```

---

## **4. User Profile Enhancement**

### **Add Dashboard Preference Setting:**
```javascript
// In MyProfile.js - add new preference tab
const dashboardPreferences = {
  defaultDashboard: 'standard', // 'standard' | 'cesium'
  mapViewLevel: 'global',       // 'global' | 'regional' | 'site'
  autoZoomToAlerts: true,
  showCameraLabels: true,
  alertNotifications: true
};
```

### **Database Schema Addition:**
```sql
-- Add to users table or create user_preferences table
ALTER TABLE users ADD COLUMN ui_preferences JSON COMMENT 'Dashboard and UI preferences';

-- Sample structure:
{
  "defaultDashboard": "cesium",
  "mapSettings": {
    "autoZoomToAlerts": true,
    "showCameraLabels": true,
    "defaultZoomLevel": 15
  }
}
```

---

## **5. Navigation Flow**

### **Navigation Hierarchy:**
```
1. Global View (Earth)
   ├── Show all sites user has access to
   ├── Color-coded by alert severity
   └── Site selector dropdown

2. Regional View (Country/City)
   ├── Zoom to selected region
   ├── Show sites in that area
   └── Summary statistics panel

3. Site View (Individual Site)
   ├── Show site boundary
   ├── Camera pin positions
   ├── Site-specific alerts
   └── Camera status indicators

4. Camera View (Live Feed)
   ├── Live video stream
   ├── Camera controls
   ├── Alert history for camera
   └── "Back to Map" button
```

### **Breadcrumb Navigation:**
```javascript
// Example breadcrumb state
const breadcrumbs = [
  { label: 'Global', level: 'global', action: () => showGlobalView() },
  { label: 'Dubai', level: 'regional', action: () => showRegional('dubai') },
  { label: 'Downtown Tower', level: 'site', action: () => showSite('dubai-001') },
  { label: 'Camera 1', level: 'camera', active: true }
];
```

---

## **6. Component Implementation Details**

### **CesiumContainer.js Structure:**
```javascript
import { Viewer, Entity, BillboardGraphics } from 'cesium';

const CesiumContainer = ({ sites, cameras, selectedSite, onSiteSelect, onCameraSelect }) => {
  // Cesium viewer initialization
  // Site pin rendering
  // Camera pin rendering
  // Click event handling
  // Zoom and camera controls
};
```

### **Site Pin Component:**
```javascript
const SitePin = ({ site, onClick }) => {
  const pinColor = determinePinColor(site.alert_summary);
  const pinIcon = determinePinIcon(site.project_type);
  
  return (
    <Entity
      position={Cartesian3.fromDegrees(...site.coordinates)}
      billboard={{
        image: createPinImage(pinColor, pinIcon),
        scale: 1.0,
        verticalOrigin: VerticalOrigin.BOTTOM
      }}
      onClick={() => onClick(site)}
    />
  );
};
```

### **Alert Summary Panel:**
```javascript
const AlertSummaryPanel = ({ site, visible }) => {
  if (!visible) return null;
  
  return (
    <div className="absolute top-4 right-4 bg-white p-4 rounded-lg shadow-lg">
      <h3>{site.name}</h3>
      <div className="alert-summary">
        <span className="critical">🔴 {site.alert_summary.critical} Critical</span>
        <span className="high">🟠 {site.alert_summary.high} High</span>
        <span className="medium">🟡 {site.alert_summary.medium} Medium</span>
      </div>
      <button onClick={() => drillDownToSite(site)}>
        View Site Details
      </button>
    </div>
  );
};
```

---

## **7. Integration Points**

### **Role-Based Site Filtering:**
```javascript
const getAccessibleSites = (userRole, userSiteAccess) => {
  return allSites.filter(site => {
    switch(userRole.level) {
      case 1: return true; // SysAdmin sees all
      case 2: return site.company_id === user.company_id; // Company exec
      case 3: return userSiteAccess.groups.includes(site.group_id); // Group manager
      case 4: 
      case 5: return userSiteAccess.sites.includes(site.id); // Site manager/coordinator
    }
  });
};
```

### **ZoneMinder Integration:**
```javascript
const getCameraStreamUrl = async (cameraId) => {
  const camera = await getCameraDetails(cameraId);
  return await zmClient.get_live_stream_url(camera.zoneminder_monitor_id);
};
```

### **Alert Data Integration:**
```javascript
const getSiteAlertSummary = async (siteId) => {
  const alerts = await api.get(`/api/sites/${siteId}/alerts/summary`);
  return {
    critical: alerts.filter(a => a.priority === 'critical').length,
    high: alerts.filter(a => a.priority === 'high').length,
    medium: alerts.filter(a => a.priority === 'medium').length
  };
};
```

---

## **8. Technical Requirements**

### **Dependencies to Add:**
```json
{
  "cesium": "^1.111.0",
  "resium": "^1.17.0"
}
```

### **Environment Variables:**
```env
# Add to frontend/.env
REACT_APP_CESIUM_ACCESS_TOKEN=your_cesium_ion_access_token
REACT_APP_DEFAULT_MAP_CENTER=[55.2744, 25.1972]
REACT_APP_DEFAULT_ZOOM_LEVEL=10
```

### **Route Addition:**
```javascript
// In App.js
import CesiumDashboard from './portals/solution-user/CesiumDashboard';
import MapLiveView from './portals/solution-user/MapLiveView';

// Add routes
<Route path="/cesium-dashboard" element={<CesiumDashboard />} />
<Route path="/map-live-view/:cameraId" element={<MapLiveView />} />
```

---

## **9. Implementation Phases**

### **Phase 1: Core Map Infrastructure**
- Install Cesium and dependencies
- Create basic CesiumContainer component
- Implement global site view with pins
- Add site selector dropdown

### **Phase 2: Site Drill-Down**
- Implement site-level camera positioning
- Add camera pin components with status colors
- Create alert summary panels
- Implement zoom and navigation controls

### **Phase 3: Live View Integration**
- Create MapLiveView component
- Integrate with existing LiveView functionality
- Add "Back to Map" navigation
- Implement collapsed sidebar mode

### **Phase 4: User Preferences**
- Add dashboard preference to MyProfile
- Implement login redirect logic
- Add map-specific user settings
- Create preference persistence

### **Phase 5: Polish & Optimization**
- Add realistic sample data
- Implement role-based filtering
- Performance optimization
- Mobile responsiveness

---

**Ready to begin implementation! This will create a powerful geospatial interface that transforms how site managers interact with their construction sites.**