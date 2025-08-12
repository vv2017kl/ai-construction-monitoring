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

export const mockCameras = {
  'dubai-001': [
    {
      id: 'cam-dubai-001-001',
      name: 'Main Entrance Security',
      site_id: 'dubai-001',
      coordinates: [55.2745, 25.1973, 15], // [longitude, latitude, height in meters]
      status: 'critical',
      type: 'entrance',
      zoneminder_monitor_id: 'zm-001',
      alerts: {
        active: 2,
        last_alert: '2025-01-20T14:30:00Z',
        alert_type: 'PPE Violation'
      },
      technical_status: 'online',
      field_of_view: 90,
      camera_direction: 45 // degrees from north
    },
    {
      id: 'cam-dubai-001-002',
      name: 'Crane Operation Zone A',
      site_id: 'dubai-001',
      coordinates: [55.2743, 25.1971, 25],
      status: 'normal',
      type: 'equipment',
      zoneminder_monitor_id: 'zm-002',
      alerts: {
        active: 0,
        last_alert: '2025-01-20T09:15:00Z',
        alert_type: null
      },
      technical_status: 'online',
      field_of_view: 60,
      camera_direction: 180
    },
    {
      id: 'cam-dubai-001-003',
      name: 'Floor 25 Construction Overview',
      site_id: 'dubai-001',
      coordinates: [55.2744, 25.1970, 75],
      status: 'warning',
      type: 'overview',
      zoneminder_monitor_id: 'zm-003',
      alerts: {
        active: 1,
        last_alert: '2025-01-20T13:45:00Z',
        alert_type: 'Unauthorized Access'
      },
      technical_status: 'online',
      field_of_view: 120,
      camera_direction: 270
    },
    {
      id: 'cam-dubai-001-004',
      name: 'Material Storage Area',
      site_id: 'dubai-001',
      coordinates: [55.2746, 25.1974, 10],
      status: 'normal',
      type: 'storage',
      zoneminder_monitor_id: 'zm-004',
      alerts: {
        active: 0,
        last_alert: '2025-01-20T08:30:00Z',
        alert_type: null
      },
      technical_status: 'online',
      field_of_view: 75,
      camera_direction: 90
    }
  ],
  'dubai-002': [
    {
      id: 'cam-dubai-002-001',
      name: 'Marina Entrance Gate',
      site_id: 'dubai-002',
      coordinates: [55.1385, 25.0778, 12],
      status: 'normal',
      type: 'entrance',
      zoneminder_monitor_id: 'zm-005',
      alerts: {
        active: 0,
        last_alert: '2025-01-20T11:20:00Z',
        alert_type: null
      },
      technical_status: 'online',
      field_of_view: 80,
      camera_direction: 0
    },
    {
      id: 'cam-dubai-002-002',
      name: 'Residential Block A',
      site_id: 'dubai-002',
      coordinates: [55.1383, 25.0776, 20],
      status: 'warning',
      type: 'construction',
      zoneminder_monitor_id: 'zm-006',
      alerts: {
        active: 1,
        last_alert: '2025-01-20T15:10:00Z',
        alert_type: 'Equipment Safety'
      },
      technical_status: 'online',
      field_of_view: 100,
      camera_direction: 135
    },
    {
      id: 'cam-dubai-002-003',
      name: 'Swimming Pool Construction',
      site_id: 'dubai-002',
      coordinates: [55.1386, 25.0775, 8],
      status: 'normal',
      type: 'amenity',
      zoneminder_monitor_id: 'zm-007',
      alerts: {
        active: 0,
        last_alert: '2025-01-20T07:45:00Z',
        alert_type: null
      },
      technical_status: 'online',
      field_of_view: 90,
      camera_direction: 225
    }
  ],
  'dubai-003': [
    {
      id: 'cam-dubai-003-001',
      name: 'Villa Plot 1 Overview',
      site_id: 'dubai-003',
      coordinates: [55.1168, 25.1125, 15],
      status: 'normal',
      type: 'overview',
      zoneminder_monitor_id: 'zm-008',
      alerts: {
        active: 0,
        last_alert: '2025-01-20T12:30:00Z',
        alert_type: null
      },
      technical_status: 'online',
      field_of_view: 110,
      camera_direction: 45
    },
    {
      id: 'cam-dubai-003-002',
      name: 'Beach Access Road',
      site_id: 'dubai-003',
      coordinates: [55.1166, 25.1123, 8],
      status: 'maintenance',
      type: 'access',
      zoneminder_monitor_id: 'zm-009',
      alerts: {
        active: 1,
        last_alert: '2025-01-20T10:15:00Z',
        alert_type: 'Camera Maintenance Required'
      },
      technical_status: 'offline',
      field_of_view: 85,
      camera_direction: 180
    },
    {
      id: 'cam-dubai-003-003',
      name: 'Villa Plot 2 Construction',
      site_id: 'dubai-003',
      coordinates: [55.1169, 25.1122, 12],
      status: 'normal',
      type: 'construction',
      zoneminder_monitor_id: 'zm-010',
      alerts: {
        active: 0,
        last_alert: '2025-01-20T14:00:00Z',
        alert_type: null
      },
      technical_status: 'online',
      field_of_view: 95,
      camera_direction: 315
    },
    {
      id: 'cam-dubai-003-004',
      name: 'Landscaping Area',
      site_id: 'dubai-003',
      coordinates: [55.1170, 25.1126, 6],
      status: 'warning',
      type: 'landscaping',
      zoneminder_monitor_id: 'zm-011',
      alerts: {
        active: 1,
        last_alert: '2025-01-20T16:20:00Z',
        alert_type: 'Personnel Safety'
      },
      technical_status: 'online',
      field_of_view: 70,
      camera_direction: 270
    }
  ],
  'dubai-004': [
    {
      id: 'cam-dubai-004-001',
      name: 'DIFC Main Entrance',
      site_id: 'dubai-004',
      coordinates: [55.2090, 25.2136, 10],
      status: 'normal',
      type: 'entrance',
      zoneminder_monitor_id: 'zm-012',
      alerts: {
        active: 0,
        last_alert: '2025-01-20T09:30:00Z',
        alert_type: null
      },
      technical_status: 'online',
      field_of_view: 85,
      camera_direction: 90
    },
    {
      id: 'cam-dubai-004-002',
      name: 'Foundation Work Area',
      site_id: 'dubai-004',
      coordinates: [55.2088, 25.2134, 5],
      status: 'normal',
      type: 'foundation',
      zoneminder_monitor_id: 'zm-013',
      alerts: {
        active: 0,
        last_alert: '2025-01-20T11:45:00Z',
        alert_type: null
      },
      technical_status: 'online',
      field_of_view: 100,
      camera_direction: 180
    },
    {
      id: 'cam-dubai-004-003',
      name: 'Site Office Complex',
      site_id: 'dubai-004',
      coordinates: [55.2091, 25.2133, 8],
      status: 'normal',
      type: 'office',
      zoneminder_monitor_id: 'zm-014',
      alerts: {
        active: 0,
        last_alert: '2025-01-20T13:15:00Z',
        alert_type: null
      },
      technical_status: 'online',
      field_of_view: 75,
      camera_direction: 0
    }
  ],
  'mumbai-001': [
    {
      id: 'cam-mumbai-001-001',
      name: 'BKC Tower Main Gate',
      site_id: 'mumbai-001',
      coordinates: [72.8698, 19.0626, 12],
      status: 'critical',
      type: 'entrance',
      zoneminder_monitor_id: 'zm-015',
      alerts: {
        active: 3,
        last_alert: '2025-01-20T15:30:00Z',
        alert_type: 'Multiple PPE Violations'
      },
      technical_status: 'online',
      field_of_view: 90,
      camera_direction: 45
    },
    {
      id: 'cam-mumbai-001-002',
      name: 'High-rise Construction Floor 15',
      site_id: 'mumbai-001',
      coordinates: [72.8696, 19.0624, 45],
      status: 'warning',
      type: 'construction',
      zoneminder_monitor_id: 'zm-016',
      alerts: {
        active: 2,
        last_alert: '2025-01-20T14:15:00Z',
        alert_type: 'Height Safety'
      },
      technical_status: 'online',
      field_of_view: 120,
      camera_direction: 180
    },
    {
      id: 'cam-mumbai-001-003',
      name: 'Crane Operations Central',
      site_id: 'mumbai-001',
      coordinates: [72.8695, 19.0623, 30],
      status: 'normal',
      type: 'equipment',
      zoneminder_monitor_id: 'zm-017',
      alerts: {
        active: 0,
        last_alert: '2025-01-20T10:20:00Z',
        alert_type: null
      },
      technical_status: 'online',
      field_of_view: 150,
      camera_direction: 270
    },
    {
      id: 'cam-mumbai-001-004',
      name: 'Material Delivery Dock',
      site_id: 'mumbai-001',
      coordinates: [72.8699, 19.0627, 8],
      status: 'normal',
      type: 'logistics',
      zoneminder_monitor_id: 'zm-018',
      alerts: {
        active: 0,
        last_alert: '2025-01-20T08:45:00Z',
        alert_type: null
      },
      technical_status: 'online',
      field_of_view: 80,
      camera_direction: 90
    }
  ],
  'bangalore-001': [
    {
      id: 'cam-bangalore-001-001',
      name: 'Electronic City Main Access',
      site_id: 'bangalore-001',
      coordinates: [77.6649, 12.8457, 10],
      status: 'normal',
      type: 'entrance',
      zoneminder_monitor_id: 'zm-019',
      alerts: {
        active: 0,
        last_alert: '2025-01-20T12:00:00Z',
        alert_type: null
      },
      technical_status: 'online',
      field_of_view: 85,
      camera_direction: 0
    },
    {
      id: 'cam-bangalore-001-002',
      name: 'IT Block A Construction',
      site_id: 'bangalore-001',
      coordinates: [77.6647, 12.8455, 20],
      status: 'warning',
      type: 'construction',
      zoneminder_monitor_id: 'zm-020',
      alerts: {
        active: 1,
        last_alert: '2025-01-20T13:30:00Z',
        alert_type: 'Equipment Safety Check'
      },
      technical_status: 'online',
      field_of_view: 95,
      camera_direction: 135
    },
    {
      id: 'cam-bangalore-001-003',
      name: 'Parking Structure Build',
      site_id: 'bangalore-001',
      coordinates: [77.6650, 12.8458, 15],
      status: 'normal',
      type: 'infrastructure',
      zoneminder_monitor_id: 'zm-021',
      alerts: {
        active: 0,
        last_alert: '2025-01-20T09:45:00Z',
        alert_type: null
      },
      technical_status: 'online',
      field_of_view: 100,
      camera_direction: 225
    }
  ],
  'delhi-001': [
    {
      id: 'cam-delhi-001-001',
      name: 'Cyber Hub Extension Gate',
      site_id: 'delhi-001',
      coordinates: [77.0689, 28.4596, 12],
      status: 'warning',
      type: 'entrance',
      zoneminder_monitor_id: 'zm-022',
      alerts: {
        active: 1,
        last_alert: '2025-01-20T14:45:00Z',
        alert_type: 'Unauthorized Vehicle'
      },
      technical_status: 'online',
      field_of_view: 90,
      camera_direction: 90
    },
    {
      id: 'cam-delhi-001-002',
      name: 'Office Tower Foundation',
      site_id: 'delhi-001',
      coordinates: [77.0687, 28.4594, 8],
      status: 'critical',
      type: 'foundation',
      zoneminder_monitor_id: 'zm-023',
      alerts: {
        active: 2,
        last_alert: '2025-01-20T15:15:00Z',
        alert_type: 'Structural Safety'
      },
      technical_status: 'online',
      field_of_view: 110,
      camera_direction: 180
    },
    {
      id: 'cam-delhi-001-003',
      name: 'Equipment Storage Yard',
      site_id: 'delhi-001',
      coordinates: [77.0685, 28.4593, 5],
      status: 'normal',
      type: 'storage',
      zoneminder_monitor_id: 'zm-024',
      alerts: {
        active: 0,
        last_alert: '2025-01-20T11:30:00Z',
        alert_type: null
      },
      technical_status: 'online',
      field_of_view: 75,
      camera_direction: 270
    },
    {
      id: 'cam-delhi-001-004',
      name: 'Server Room Construction',
      site_id: 'delhi-001',
      coordinates: [77.0691, 28.4597, 18],
      status: 'maintenance',
      type: 'technical',
      zoneminder_monitor_id: 'zm-025',
      alerts: {
        active: 1,
        last_alert: '2025-01-20T10:00:00Z',
        alert_type: 'Camera Maintenance'
      },
      technical_status: 'offline',
      field_of_view: 60,
      camera_direction: 45
    }
  ],
  'pune-001': [
    {
      id: 'cam-pune-001-001',
      name: 'Hinjewadi Phase 4 Main Gate',
      site_id: 'pune-001',
      coordinates: [73.7275, 18.5913, 8],
      status: 'normal',
      type: 'entrance',
      zoneminder_monitor_id: 'zm-026',
      alerts: {
        active: 0,
        last_alert: '2025-01-20T09:15:00Z',
        alert_type: null
      },
      technical_status: 'online',
      field_of_view: 80,
      camera_direction: 0
    },
    {
      id: 'cam-pune-001-002',
      name: 'Tech Park Building A',
      site_id: 'pune-001',
      coordinates: [73.7273, 18.5911, 15],
      status: 'normal',
      type: 'construction',
      zoneminder_monitor_id: 'zm-027',
      alerts: {
        active: 0,
        last_alert: '2025-01-20T12:20:00Z',
        alert_type: null
      },
      technical_status: 'online',
      field_of_view: 100,
      camera_direction: 180
    },
    {
      id: 'cam-pune-001-003',
      name: 'Landscaping and Utilities',
      site_id: 'pune-001',
      coordinates: [73.7276, 18.5914, 6],
      status: 'normal',
      type: 'infrastructure',
      zoneminder_monitor_id: 'zm-028',
      alerts: {
        active: 0,
        last_alert: '2025-01-20T08:30:00Z',
        alert_type: null
      },
      technical_status: 'online',
      field_of_view: 90,
      camera_direction: 270
    }
  ]
};

// Alert details for cameras
export const mockCameraAlerts = [
  {
    id: 'alert-001',
    camera_id: 'cam-dubai-001-001',
    site_id: 'dubai-001',
    type: 'PPE Violation',
    severity: 'critical',
    title: 'Hard Hat Not Worn',
    description: 'Worker detected without hard hat in restricted area',
    timestamp: '2025-01-20T14:30:00Z',
    status: 'active',
    evidence_url: '/api/alerts/alert-001/evidence.jpg'
  },
  {
    id: 'alert-002',
    camera_id: 'cam-dubai-001-001',
    site_id: 'dubai-001',
    type: 'PPE Violation',
    severity: 'high',
    title: 'Safety Vest Missing',
    description: 'Personnel without high-visibility safety vest',
    timestamp: '2025-01-20T13:45:00Z',
    status: 'active',
    evidence_url: '/api/alerts/alert-002/evidence.jpg'
  },
  {
    id: 'alert-003',
    camera_id: 'cam-mumbai-001-001',
    site_id: 'mumbai-001',
    type: 'PPE Violation',
    severity: 'critical',
    title: 'Multiple Safety Violations',
    description: 'Multiple workers without proper PPE equipment',
    timestamp: '2025-01-20T15:30:00Z',
    status: 'active',
    evidence_url: '/api/alerts/alert-003/evidence.jpg'
  }
];

// Pin styling configuration
export const sitePinColors = {
  critical: '#FF0000',    // Red
  high: '#FF8C00',        // Orange
  medium: '#FFD700',      // Gold
  low: '#32CD32',         // Green
  normal: '#32CD32',      // Green
  offline: '#808080'      // Gray
};

export const cameraPinColors = {
  critical: '#FF0000',    // Red - Safety violations
  warning: '#FFA500',     // Orange - PPE issues
  maintenance: '#FFFF00', // Yellow - Maintenance required
  normal: '#00FF00',      // Green - Operating normally  
  offline: '#808080'      // Gray - Camera offline
};

// Regional groupings for map navigation
export const regions = {
  'Middle East': {
    center: [55.2744, 25.1972],
    zoom: 8,
    sites: ['dubai-001', 'dubai-002', 'dubai-003', 'dubai-004']
  },
  'South Asia': {
    center: [75.7873, 22.9734], // Central India
    zoom: 5,
    sites: ['mumbai-001', 'bangalore-001', 'delhi-001', 'pune-001']
  }
};

// Default map settings
export const mapDefaults = {
  globalCenter: [65.0000, 20.0000], // Between Dubai and India
  globalZoom: 4,
  siteZoom: 16,
  cameraZoom: 18
};