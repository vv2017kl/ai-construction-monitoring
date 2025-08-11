// Cesium Map Mock Data
// Construction Site Management - Geospatial Data

export const mockSites = [
  // Dubai Sites
  {
    id: 'dubai-001',
    name: 'Downtown Dubai Tower',
    code: 'DXB-DT-001',
    coordinates: [55.2744, 25.1972, 0], // Near Burj Khalifa [longitude, latitude, height]
    project_type: 'commercial',
    project_phase: 'construction',
    status: 'active',
    country: 'UAE',
    city: 'Dubai',
    region: 'Middle East',
    company_id: '11111111-1111-1111-1111-111111111111',
    group_id: '33333333-3333-3333-3333-333333333333',
    alert_summary: {
      critical: 2,
      high: 5,
      medium: 12,
      low: 8
    },
    site_stats: {
      total_cameras: 4,
      active_cameras: 4,
      offline_cameras: 0,
      personnel_count: 45,
      equipment_count: 8
    },
    boundary_coordinates: [
      [55.2740, 25.1975],
      [55.2748, 25.1975],
      [55.2748, 25.1969],
      [55.2740, 25.1969],
      [55.2740, 25.1975]
    ]
  },
  {
    id: 'dubai-002',
    name: 'Dubai Marina Residential Complex',
    code: 'DXB-MR-002',
    coordinates: [55.1384, 25.0777, 0], // Dubai Marina
    project_type: 'residential',
    project_phase: 'construction',
    status: 'active',
    country: 'UAE',
    city: 'Dubai',
    region: 'Middle East',
    company_id: '11111111-1111-1111-1111-111111111111',
    group_id: '33333333-3333-3333-3333-333333333333',
    alert_summary: {
      critical: 0,
      high: 3,
      medium: 8,
      low: 15
    },
    site_stats: {
      total_cameras: 3,
      active_cameras: 3,
      offline_cameras: 0,
      personnel_count: 32,
      equipment_count: 5
    },
    boundary_coordinates: [
      [55.1380, 25.0780],
      [55.1388, 25.0780],
      [55.1388, 25.0774],
      [55.1380, 25.0774],
      [55.1380, 25.0780]
    ]
  },
  {
    id: 'dubai-003',
    name: 'Palm Jumeirah Villa Project',
    code: 'DXB-PJ-003',
    coordinates: [55.1167, 25.1124, 0], // Palm Jumeirah
    project_type: 'residential',
    project_phase: 'finishing',
    status: 'active',
    country: 'UAE',
    city: 'Dubai',
    region: 'Middle East',
    company_id: '11111111-1111-1111-1111-111111111111',
    group_id: '33333333-3333-3333-3333-333333333333',
    alert_summary: {
      critical: 1,
      high: 2,
      medium: 6,
      low: 4
    },
    site_stats: {
      total_cameras: 4,
      active_cameras: 3,
      offline_cameras: 1,
      personnel_count: 28,
      equipment_count: 4
    },
    boundary_coordinates: [
      [55.1163, 25.1127],
      [55.1171, 25.1127],
      [55.1171, 25.1121],
      [55.1163, 25.1121],
      [55.1163, 25.1127]
    ]
  },
  {
    id: 'dubai-004',
    name: 'DIFC Office Complex',
    code: 'DXB-OF-004',
    coordinates: [55.2089, 25.2135, 0], // Dubai International Financial Centre
    project_type: 'commercial',
    project_phase: 'preparation',
    status: 'active',
    country: 'UAE',
    city: 'Dubai',
    region: 'Middle East',
    company_id: '11111111-1111-1111-1111-111111111111',
    group_id: '33333333-3333-3333-3333-333333333333',
    alert_summary: {
      critical: 0,
      high: 1,
      medium: 4,
      low: 2
    },
    site_stats: {
      total_cameras: 3,
      active_cameras: 3,
      offline_cameras: 0,
      personnel_count: 15,
      equipment_count: 3
    },
    boundary_coordinates: [
      [55.2085, 25.2138],
      [55.2093, 25.2138],
      [55.2093, 25.2132],
      [55.2085, 25.2132],
      [55.2085, 25.2138]
    ]
  },

  // India Sites
  {
    id: 'mumbai-001',
    name: 'Bandra-Kurla Complex Office Tower',
    code: 'MUM-BK-001',
    coordinates: [72.8697, 19.0625, 0], // BKC Mumbai
    project_type: 'commercial',
    project_phase: 'construction',
    status: 'active',
    country: 'India',
    city: 'Mumbai',
    region: 'South Asia',
    company_id: '11111111-1111-1111-1111-111111111111',
    group_id: '44444444-4444-4444-4444-444444444444',
    alert_summary: {
      critical: 3,
      high: 7,
      medium: 15,
      low: 12
    },
    site_stats: {
      total_cameras: 4,
      active_cameras: 4,
      offline_cameras: 0,
      personnel_count: 65,
      equipment_count: 12
    },
    boundary_coordinates: [
      [72.8693, 19.0628],
      [72.8701, 19.0628],
      [72.8701, 19.0622],
      [72.8693, 19.0622],
      [72.8693, 19.0628]
    ]
  },
  {
    id: 'bangalore-001',
    name: 'Electronic City IT Campus',
    code: 'BLR-EC-001',
    coordinates: [77.6648, 12.8456, 0], // Electronic City Bangalore
    project_type: 'commercial',
    project_phase: 'construction',
    status: 'active',
    country: 'India',
    city: 'Bangalore',
    region: 'South Asia',
    company_id: '11111111-1111-1111-1111-111111111111',
    group_id: '44444444-4444-4444-4444-444444444444',
    alert_summary: {
      critical: 1,
      high: 4,
      medium: 9,
      low: 18
    },
    site_stats: {
      total_cameras: 3,
      active_cameras: 3,
      offline_cameras: 0,
      personnel_count: 42,
      equipment_count: 7
    },
    boundary_coordinates: [
      [77.6644, 12.8459],
      [77.6652, 12.8459],
      [77.6652, 12.8453],
      [77.6644, 12.8453],
      [77.6644, 12.8459]
    ]
  },
  {
    id: 'delhi-001',
    name: 'Gurgaon Cyber Hub Extension',
    code: 'DEL-GH-001',
    coordinates: [77.0688, 28.4595, 0], // Gurgaon
    project_type: 'commercial',
    project_phase: 'construction',
    status: 'active',
    country: 'India',
    city: 'Gurgaon',
    region: 'South Asia',
    company_id: '11111111-1111-1111-1111-111111111111',
    group_id: '44444444-4444-4444-4444-444444444444',
    alert_summary: {
      critical: 2,
      high: 6,
      medium: 11,
      low: 9
    },
    site_stats: {
      total_cameras: 4,
      active_cameras: 3,
      offline_cameras: 1,
      personnel_count: 38,
      equipment_count: 9
    },
    boundary_coordinates: [
      [77.0684, 28.4598],
      [77.0692, 28.4598],
      [77.0692, 28.4592],
      [77.0684, 28.4592],
      [77.0684, 28.4598]
    ]
  },
  {
    id: 'pune-001',
    name: 'Hinjewadi Tech Park Phase 4',
    code: 'PUN-HP-001',
    coordinates: [73.7274, 18.5912, 0], // Hinjewadi Pune
    project_type: 'commercial',
    project_phase: 'preparation',
    status: 'active',
    country: 'India',
    city: 'Pune',
    region: 'South Asia',
    company_id: '11111111-1111-1111-1111-111111111111',
    group_id: '44444444-4444-4444-4444-444444444444',
    alert_summary: {
      critical: 0,
      high: 2,
      medium: 7,
      low: 11
    },
    site_stats: {
      total_cameras: 3,
      active_cameras: 3,
      offline_cameras: 0,
      personnel_count: 25,
      equipment_count: 4
    },
    boundary_coordinates: [
      [73.7270, 18.5915],
      [73.7278, 18.5915],
      [73.7278, 18.5909],
      [73.7270, 18.5909],
      [73.7270, 18.5915]
    ]
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