// Cesium Map Mock Data
// Construction Sites with Realistic Data and Hierarchical Navigation

// Alert Types and Colors
export const alertTypes = {
  CRITICAL: { color: '#DC2626', name: 'Critical', priority: 1 },
  HIGH: { color: '#EA580C', name: 'High', priority: 2 },
  MEDIUM: { color: '#D97706', name: 'Medium', priority: 3 },
  LOW: { color: '#65A30D', name: 'Low', priority: 4 },
  INFO: { color: '#2563EB', name: 'Info', priority: 5 }
};

// Regional Data
export const regions = {
  MIDDLE_EAST: {
    id: 'middle_east',
    name: 'Middle East',
    center: [55.2708, 25.2048], // Dubai coordinates
    zoom: 7,
    sites: ['site_1', 'site_2', 'site_3', 'site_4']
  },
  SOUTH_ASIA: {
    id: 'south_asia', 
    name: 'South Asia',
    center: [72.8777, 19.0760], // Mumbai coordinates
    zoom: 7,
    sites: ['site_5', 'site_6', 'site_7', 'site_8']
  }
};

// Construction Sites with Real Coordinates and Data
export const constructionSites = [
  // Middle East Region - Dubai Projects
  {
    id: 'site_1',
    name: 'Downtown Dubai Tower Complex',
    code: 'DD-TC-2024',
    region: 'MIDDLE_EAST',
    coordinates: [55.2744, 25.1972], // Downtown Dubai
    city: 'Dubai',
    country: 'UAE',
    projectType: 'High-Rise Mixed Use',
    constructionStage: 'Foundation & Structure',
    alerts: {
      critical: 2,
      high: 5,
      medium: 8,
      low: 12,
      info: 3
    },
    totalCameras: 8,
    activeWorkers: 145,
    safetyScore: 72,
    projectManager: 'Ahmed Hassan',
    completionPercent: 35
  },
  {
    id: 'site_2',
    name: 'Dubai Marina Residential Tower',
    code: 'DM-RT-2024',
    region: 'MIDDLE_EAST',
    coordinates: [55.1416, 25.0823], // Dubai Marina
    city: 'Dubai',
    country: 'UAE',
    projectType: 'Residential Tower',
    constructionStage: 'Exterior Finishing',
    alerts: {
      critical: 0,
      high: 2,
      medium: 4,
      low: 8,
      info: 6
    },
    totalCameras: 6,
    activeWorkers: 89,
    safetyScore: 91,
    projectManager: 'Sarah Al-Mansouri',
    completionPercent: 78
  },
  {
    id: 'site_3',
    name: 'Business Bay Commercial Complex',
    code: 'BB-CC-2024',
    region: 'MIDDLE_EAST',
    coordinates: [55.2634, 25.1848], // Business Bay
    city: 'Dubai',
    country: 'UAE',
    projectType: 'Commercial Complex',
    constructionStage: 'Interior Fit-out',
    alerts: {
      critical: 1,
      high: 3,
      medium: 6,
      low: 15,
      info: 4
    },
    totalCameras: 10,
    activeWorkers: 203,
    safetyScore: 85,
    projectManager: 'Mohammad Rahman',
    completionPercent: 62
  },
  {
    id: 'site_4',
    name: 'Dubai Silicon Oasis Data Center',
    code: 'DSO-DC-2024',
    region: 'MIDDLE_EAST',
    coordinates: [55.3781, 25.1207], // Dubai Silicon Oasis
    city: 'Dubai',
    country: 'UAE',
    projectType: 'Data Center',
    constructionStage: 'MEP Installation',
    alerts: {
      critical: 0,
      high: 1,
      medium: 2,
      low: 5,
      info: 8
    },
    totalCameras: 12,
    activeWorkers: 67,
    safetyScore: 96,
    projectManager: 'James Wilson',
    completionPercent: 89
  },
  
  // South Asia Region - Mumbai Projects
  {
    id: 'site_5',
    name: 'Bandra-Kurla Complex Office Tower',
    code: 'BKC-OT-2024',
    region: 'SOUTH_ASIA',
    coordinates: [72.8697, 19.0606], // BKC Mumbai
    city: 'Mumbai',
    country: 'India',
    projectType: 'Office Tower',
    constructionStage: 'Structure Completion',
    alerts: {
      critical: 3,
      high: 7,
      medium: 11,
      low: 18,
      info: 5
    },
    totalCameras: 9,
    activeWorkers: 178,
    safetyScore: 68,
    projectManager: 'Rajesh Sharma',
    completionPercent: 43
  },
  {
    id: 'site_6',
    name: 'Powai Tech Park Expansion',
    code: 'PTP-EX-2024',
    region: 'SOUTH_ASIA',
    coordinates: [72.9081, 19.1136], // Powai
    city: 'Mumbai',
    country: 'India',
    projectType: 'Tech Campus',
    constructionStage: 'Foundation',
    alerts: {
      critical: 1,
      high: 4,
      medium: 9,
      low: 14,
      info: 7
    },
    totalCameras: 7,
    activeWorkers: 156,
    safetyScore: 79,
    projectManager: 'Priya Patel',
    completionPercent: 25
  },
  {
    id: 'site_7',
    name: 'Andheri Metro Station Hub',
    code: 'AMS-HUB-2024',
    region: 'SOUTH_ASIA',
    coordinates: [72.8467, 19.1197], // Andheri
    city: 'Mumbai',
    country: 'India',
    projectType: 'Transport Infrastructure',
    constructionStage: 'Excavation & Foundation',
    alerts: {
      critical: 0,
      high: 2,
      medium: 5,
      low: 11,
      info: 9
    },
    totalCameras: 11,
    activeWorkers: 234,
    safetyScore: 87,
    projectManager: 'Vikram Singh',
    completionPercent: 31
  },
  {
    id: 'site_8',
    name: 'Navi Mumbai Smart City Phase 2',
    code: 'NMSC-P2-2024',
    region: 'SOUTH_ASIA',
    coordinates: [73.0297, 19.0330], // Navi Mumbai
    city: 'Navi Mumbai',
    country: 'India',
    projectType: 'Smart City Development',
    constructionStage: 'Infrastructure Development',
    alerts: {
      critical: 0,
      high: 1,
      medium: 3,
      low: 7,
      info: 12
    },
    totalCameras: 15,
    activeWorkers: 312,
    safetyScore: 93,
    projectManager: 'Ananya Desai',
    completionPercent: 56
  }
];

// Camera Data with IP Camera Types and Positions
export const constructionCameras = [
  // Downtown Dubai Tower Complex Cameras
  { id: 'cam_1_1', siteId: 'site_1', name: 'Tower Crane Cam 1', type: 'fisheye', coordinates: [55.2745, 25.1973], angle: 0, status: 'active', alerts: ['critical', 'high'] },
  { id: 'cam_1_2', siteId: 'site_1', name: 'Foundation Monitoring', type: 'ptz', coordinates: [55.2743, 25.1971], angle: 45, status: 'active', alerts: ['medium'] },
  { id: 'cam_1_3', siteId: 'site_1', name: 'Main Entrance Security', type: 'fixed', coordinates: [55.2742, 25.1970], angle: 180, status: 'active', alerts: [] },
  { id: 'cam_1_4', siteId: 'site_1', name: 'Material Storage Area', type: 'fisheye', coordinates: [55.2746, 25.1974], angle: 270, status: 'active', alerts: ['low'] },
  { id: 'cam_1_5', siteId: 'site_1', name: 'Worker Safety Zone', type: 'ptz', coordinates: [55.2744, 25.1972], angle: 90, status: 'maintenance', alerts: ['critical'] },
  { id: 'cam_1_6', siteId: 'site_1', name: 'Perimeter North', type: 'fixed', coordinates: [55.2745, 25.1975], angle: 0, status: 'active', alerts: [] },
  { id: 'cam_1_7', siteId: 'site_1', name: 'Concrete Pour Area', type: 'fisheye', coordinates: [55.2743, 25.1969], angle: 135, status: 'active', alerts: ['high', 'medium'] },
  { id: 'cam_1_8', siteId: 'site_1', name: 'Tower Crane Cam 2', type: 'ptz', coordinates: [55.2747, 25.1973], angle: 315, status: 'active', alerts: ['info'] },

  // Dubai Marina Residential Tower Cameras
  { id: 'cam_2_1', siteId: 'site_2', name: 'Facade Installation Cam', type: 'fisheye', coordinates: [55.1417, 25.0824], angle: 0, status: 'active', alerts: [] },
  { id: 'cam_2_2', siteId: 'site_2', name: 'Elevator Shaft Monitor', type: 'fixed', coordinates: [55.1415, 25.0822], angle: 90, status: 'active', alerts: ['low'] },
  { id: 'cam_2_3', siteId: 'site_2', name: 'Balcony Work Area', type: 'ptz', coordinates: [55.1418, 25.0825], angle: 180, status: 'active', alerts: ['medium'] },
  { id: 'cam_2_4', siteId: 'site_2', name: 'Marina View Security', type: 'fisheye', coordinates: [55.1414, 25.0821], angle: 270, status: 'active', alerts: [] },
  { id: 'cam_2_5', siteId: 'site_2', name: 'Rooftop Equipment', type: 'fixed', coordinates: [55.1419, 25.0826], angle: 45, status: 'active', alerts: ['info'] },
  { id: 'cam_2_6', siteId: 'site_2', name: 'Parking Garage', type: 'ptz', coordinates: [55.1413, 25.0820], angle: 225, status: 'active', alerts: ['high'] },

  // Business Bay Commercial Complex Cameras  
  { id: 'cam_3_1', siteId: 'site_3', name: 'Lobby Construction Cam', type: 'fisheye', coordinates: [55.2635, 25.1849], angle: 0, status: 'active', alerts: ['medium'] },
  { id: 'cam_3_2', siteId: 'site_3', name: 'Office Floor Progress', type: 'ptz', coordinates: [55.2633, 25.1847], angle: 90, status: 'active', alerts: [] },
  { id: 'cam_3_3', siteId: 'site_3', name: 'Bay View Exterior', type: 'fixed', coordinates: [55.2636, 25.1850], angle: 180, status: 'active', alerts: ['low'] },
  { id: 'cam_3_4', siteId: 'site_3', name: 'HVAC Installation', type: 'fisheye', coordinates: [55.2632, 25.1846], angle: 270, status: 'active', alerts: ['critical'] },
  { id: 'cam_3_5', siteId: 'site_3', name: 'Electrical Room', type: 'fixed', coordinates: [55.2637, 25.1851], angle: 45, status: 'active', alerts: [] },
  { id: 'cam_3_6', siteId: 'site_3', name: 'Fire Safety Systems', type: 'ptz', coordinates: [55.2634, 25.1848], angle: 135, status: 'maintenance', alerts: ['high'] },
  { id: 'cam_3_7', siteId: 'site_3', name: 'Retail Space Fit-out', type: 'fisheye', coordinates: [55.2635, 25.1847], angle: 225, status: 'active', alerts: ['medium'] },
  { id: 'cam_3_8', siteId: 'site_3', name: 'Loading Dock', type: 'fixed', coordinates: [55.2631, 25.1845], angle: 315, status: 'active', alerts: ['info'] },
  { id: 'cam_3_9', siteId: 'site_3', name: 'Perimeter Security', type: 'ptz', coordinates: [55.2638, 25.1852], angle: 0, status: 'active', alerts: [] },
  { id: 'cam_3_10', siteId: 'site_3', name: 'Conference Room Build', type: 'fisheye', coordinates: [55.2633, 25.1849], angle: 90, status: 'active', alerts: ['low'] },

  // Dubai Silicon Oasis Data Center Cameras
  { id: 'cam_4_1', siteId: 'site_4', name: 'Server Room Construction', type: 'fisheye', coordinates: [55.3782, 25.1208], angle: 0, status: 'active', alerts: [] },
  { id: 'cam_4_2', siteId: 'site_4', name: 'Cooling System Install', type: 'ptz', coordinates: [55.3780, 25.1206], angle: 90, status: 'active', alerts: ['info'] },
  { id: 'cam_4_3', siteId: 'site_4', name: 'Power Infrastructure', type: 'fixed', coordinates: [55.3783, 25.1209], angle: 180, status: 'active', alerts: [] },
  { id: 'cam_4_4', siteId: 'site_4', name: 'Security Perimeter', type: 'fisheye', coordinates: [55.3779, 25.1205], angle: 270, status: 'active', alerts: ['low'] },
  { id: 'cam_4_5', siteId: 'site_4', name: 'Cable Management', type: 'ptz', coordinates: [55.3784, 25.1210], angle: 45, status: 'active', alerts: [] },
  { id: 'cam_4_6', siteId: 'site_4', name: 'Generator Room', type: 'fixed', coordinates: [55.3778, 25.1204], angle: 225, status: 'active', alerts: [] },
  { id: 'cam_4_7', siteId: 'site_4', name: 'Clean Room Setup', type: 'fisheye', coordinates: [55.3785, 25.1211], angle: 135, status: 'active', alerts: [] },
  { id: 'cam_4_8', siteId: 'site_4', name: 'Fire Suppression', type: 'ptz', coordinates: [55.3777, 25.1203], angle: 315, status: 'active', alerts: [] },
  { id: 'cam_4_9', siteId: 'site_4', name: 'Network Operations', type: 'fixed', coordinates: [55.3786, 25.1212], angle: 0, status: 'active', alerts: [] },
  { id: 'cam_4_10', siteId: 'site_4', name: 'Loading Bay Monitor', type: 'fisheye', coordinates: [55.3776, 25.1202], angle: 90, status: 'active', alerts: [] },
  { id: 'cam_4_11', siteId: 'site_4', name: 'Exterior North Wall', type: 'ptz', coordinates: [55.3787, 25.1213], angle: 180, status: 'active', alerts: [] },
  { id: 'cam_4_12', siteId: 'site_4', name: 'Emergency Exit Monitor', type: 'fixed', coordinates: [55.3775, 25.1201], angle: 270, status: 'active', alerts: [] },

  // Bandra-Kurla Complex Office Tower Cameras
  { id: 'cam_5_1', siteId: 'site_5', name: 'Main Structure Progress', type: 'fisheye', coordinates: [72.8698, 19.0607], angle: 0, status: 'active', alerts: ['critical', 'high'] },
  { id: 'cam_5_2', siteId: 'site_5', name: 'Foundation Monitoring', type: 'ptz', coordinates: [72.8696, 19.0605], angle: 90, status: 'active', alerts: ['medium'] },
  { id: 'cam_5_3', siteId: 'site_5', name: 'BKC Road Entrance', type: 'fixed', coordinates: [72.8699, 19.0608], angle: 180, status: 'active', alerts: [] },
  { id: 'cam_5_4', siteId: 'site_5', name: 'Worker Assembly Area', type: 'fisheye', coordinates: [72.8695, 19.0604], angle: 270, status: 'active', alerts: ['high'] },
  { id: 'cam_5_5', siteId: 'site_5', name: 'Material Hoist Operations', type: 'ptz', coordinates: [72.8700, 19.0609], angle: 45, status: 'maintenance', alerts: ['critical'] },
  { id: 'cam_5_6', siteId: 'site_5', name: 'Concrete Batching Plant', type: 'fixed', coordinates: [72.8694, 19.0603], angle: 225, status: 'active', alerts: ['low'] },
  { id: 'cam_5_7', siteId: 'site_5', name: 'Tower Crane Operations', type: 'fisheye', coordinates: [72.8701, 19.0610], angle: 135, status: 'active', alerts: ['medium'] },
  { id: 'cam_5_8', siteId: 'site_5', name: 'Safety Compliance Zone', type: 'ptz', coordinates: [72.8693, 19.0602], angle: 315, status: 'active', alerts: ['high'] },
  { id: 'cam_5_9', siteId: 'site_5', name: 'Quality Control Point', type: 'fixed', coordinates: [72.8702, 19.0611], angle: 0, status: 'active', alerts: ['info'] },

  // Powai Tech Park Expansion Cameras
  { id: 'cam_6_1', siteId: 'site_6', name: 'Excavation Progress', type: 'fisheye', coordinates: [72.9082, 19.1137], angle: 0, status: 'active', alerts: ['medium'] },
  { id: 'cam_6_2', siteId: 'site_6', name: 'Soil Testing Area', type: 'ptz', coordinates: [72.9080, 19.1135], angle: 90, status: 'active', alerts: [] },
  { id: 'cam_6_3', siteId: 'site_6', name: 'Equipment Storage', type: 'fixed', coordinates: [72.9083, 19.1138], angle: 180, status: 'active', alerts: ['low'] },
  { id: 'cam_6_4', siteId: 'site_6', name: 'Powai Lake View', type: 'fisheye', coordinates: [72.9079, 19.1134], angle: 270, status: 'active', alerts: [] },
  { id: 'cam_6_5', siteId: 'site_6', name: 'Tech Campus Entrance', type: 'ptz', coordinates: [72.9084, 19.1139], angle: 45, status: 'active', alerts: ['critical'] },
  { id: 'cam_6_6', siteId: 'site_6', name: 'Utility Installation', type: 'fixed', coordinates: [72.9078, 19.1133], angle: 225, status: 'active', alerts: ['high'] },
  { id: 'cam_6_7', siteId: 'site_6', name: 'Environmental Monitor', type: 'fisheye', coordinates: [72.9085, 19.1140], angle: 135, status: 'active', alerts: ['info'] },

  // Andheri Metro Station Hub Cameras  
  { id: 'cam_7_1', siteId: 'site_7', name: 'Underground Excavation', type: 'fisheye', coordinates: [72.8468, 19.1198], angle: 0, status: 'active', alerts: [] },
  { id: 'cam_7_2', siteId: 'site_7', name: 'Station Platform Area', type: 'ptz', coordinates: [72.8466, 19.1196], angle: 90, status: 'active', alerts: ['medium'] },
  { id: 'cam_7_3', siteId: 'site_7', name: 'Main Road Interface', type: 'fixed', coordinates: [72.8469, 19.1199], angle: 180, status: 'active', alerts: [] },
  { id: 'cam_7_4', siteId: 'site_7', name: 'Metro Line Connection', type: 'fisheye', coordinates: [72.8465, 19.1195], angle: 270, status: 'active', alerts: ['low'] },
  { id: 'cam_7_5', siteId: 'site_7', name: 'Tunnel Boring Progress', type: 'ptz', coordinates: [72.8470, 19.1200], angle: 45, status: 'active', alerts: [] },
  { id: 'cam_7_6', siteId: 'site_7', name: 'Ventilation Shaft', type: 'fixed', coordinates: [72.8464, 19.1194], angle: 225, status: 'active', alerts: ['high'] },
  { id: 'cam_7_7', siteId: 'site_7', name: 'Emergency Access', type: 'fisheye', coordinates: [72.8471, 19.1201], angle: 135, status: 'active', alerts: [] },
  { id: 'cam_7_8', siteId: 'site_7', name: 'Power Substation', type: 'ptz', coordinates: [72.8463, 19.1193], angle: 315, status: 'active', alerts: ['info'] },
  { id: 'cam_7_9', siteId: 'site_7', name: 'Ticketing Area Build', type: 'fixed', coordinates: [72.8472, 19.1202], angle: 0, status: 'active', alerts: ['medium'] },
  { id: 'cam_7_10', siteId: 'site_7', name: 'Concourse Construction', type: 'fisheye', coordinates: [72.8462, 19.1192], angle: 90, status: 'active', alerts: [] },
  { id: 'cam_7_11', siteId: 'site_7', name: 'Escalator Installation', type: 'ptz', coordinates: [72.8473, 19.1203], angle: 180, status: 'active', alerts: ['low'] },

  // Navi Mumbai Smart City Phase 2 Cameras
  { id: 'cam_8_1', siteId: 'site_8', name: 'Smart Infrastructure Hub', type: 'fisheye', coordinates: [73.0298, 19.0331], angle: 0, status: 'active', alerts: [] },
  { id: 'cam_8_2', siteId: 'site_8', name: 'IoT Sensor Network', type: 'ptz', coordinates: [73.0296, 19.0329], angle: 90, status: 'active', alerts: ['info'] },
  { id: 'cam_8_3', siteId: 'site_8', name: 'Digital Signage Install', type: 'fixed', coordinates: [73.0299, 19.0332], angle: 180, status: 'active', alerts: [] },
  { id: 'cam_8_4', siteId: 'site_8', name: 'Fiber Optic Deployment', type: 'fisheye', coordinates: [73.0295, 19.0328], angle: 270, status: 'active', alerts: ['low'] },
  { id: 'cam_8_5', siteId: 'site_8', name: 'Traffic Management', type: 'ptz', coordinates: [73.0300, 19.0333], angle: 45, status: 'active', alerts: [] },
  { id: 'cam_8_6', siteId: 'site_8', name: 'Green Building Systems', type: 'fixed', coordinates: [73.0294, 19.0327], angle: 225, status: 'active', alerts: [] },
  { id: 'cam_8_7', siteId: 'site_8', name: 'Water Management', type: 'fisheye', coordinates: [73.0301, 19.0334], angle: 135, status: 'active', alerts: [] },
  { id: 'cam_8_8', siteId: 'site_8', name: 'Solar Panel Array', type: 'ptz', coordinates: [73.0293, 19.0326], angle: 315, status: 'active', alerts: [] },
  { id: 'cam_8_9', siteId: 'site_8', name: 'Waste Processing Unit', type: 'fixed', coordinates: [73.0302, 19.0335], angle: 0, status: 'active', alerts: [] },
  { id: 'cam_8_10', siteId: 'site_8', name: 'Community Center Build', type: 'fisheye', coordinates: [73.0292, 19.0325], angle: 90, status: 'active', alerts: [] },
  { id: 'cam_8_11', siteId: 'site_8', name: 'Smart Parking System', type: 'ptz', coordinates: [73.0303, 19.0336], angle: 180, status: 'active', alerts: [] },
  { id: 'cam_8_12', siteId: 'site_8', name: 'Emergency Response', type: 'fixed', coordinates: [73.0291, 19.0324], angle: 270, status: 'active', alerts: [] },
  { id: 'cam_8_13', siteId: 'site_8', name: 'Public Wi-Fi Network', type: 'fisheye', coordinates: [73.0304, 19.0337], angle: 45, status: 'active', alerts: [] },
  { id: 'cam_8_14', siteId: 'site_8', name: 'Environmental Sensors', type: 'ptz', coordinates: [73.0290, 19.0323], angle: 225, status: 'active', alerts: [] },
  { id: 'cam_8_15', siteId: 'site_8', name: 'Central Control Room', type: 'fixed', coordinates: [73.0298, 19.0330], angle: 135, status: 'active', alerts: [] }
];

// Layer Configuration for Cesium Map
export const mapLayers = {
  SATELLITE: {
    id: 'satellite',
    name: 'Satellite Imagery',
    type: 'imagery',
    enabled: true,
    opacity: 1.0
  },
  TERRAIN: {
    id: 'terrain',
    name: '3D Terrain',
    type: 'terrain',
    enabled: true,
    opacity: 1.0
  },
  SITES: {
    id: 'sites',
    name: 'Construction Sites',
    type: 'vector',
    enabled: true,
    opacity: 1.0
  },
  CAMERAS: {
    id: 'cameras',
    name: 'Security Cameras',
    type: 'vector',
    enabled: true,
    opacity: 0.8
  },
  ALERTS: {
    id: 'alerts',
    name: 'Alert Indicators',
    type: 'vector',
    enabled: true,
    opacity: 0.9
  },
  REGIONS: {
    id: 'regions',
    name: 'Regional Boundaries',
    type: 'vector',
    enabled: false,
    opacity: 0.5
  },
  LABELS: {
    id: 'labels',
    name: 'Site Labels',
    type: 'vector',
    enabled: true,
    opacity: 1.0
  }
};

// Default view settings
export const defaultMapSettings = {
  globalCenter: [65.0000, 20.0000], // Between Middle East and South Asia
  globalZoom: 4,
  regionalZoom: 7,
  siteZoom: 16,
  cameraZoom: 18
};