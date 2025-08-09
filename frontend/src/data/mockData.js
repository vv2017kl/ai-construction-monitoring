// Brilliant looking fake data for wireframes

export const mockUser = {
  id: 'user-001',
  username: 'james.wilson',
  email: 'j.wilson@skylineconstruction.com',
  firstName: 'James',
  lastName: 'Wilson',
  displayName: 'James Wilson',
  role: 'Site Manager',
  avatar: '/api/placeholder/32/32',
  company: 'Skyline Construction Group',
  currentSite: 'Downtown Plaza Project',
  phone: '+1 (555) 123-4567',
  lastLogin: '2025-01-09T08:30:00Z',
  permissions: ['view_all_cameras', 'manage_alerts', 'create_reports']
};

export const mockSites = [
  {
    id: 'site-001',
    name: 'Downtown Plaza Project',
    code: 'DTP-001',
    address: '123 Main Street, Downtown, NY 10001',
    status: 'active',
    type: 'commercial',
    phase: 'construction',
    progress: 67,
    cameras: 24,
    activeAlerts: 3,
    personnel: 45,
    weather: { temp: 72, condition: 'Partly Cloudy', wind: '8 mph' },
    lastActivity: '2 minutes ago',
    coordinates: { lat: 40.7589, lng: -73.9851 },
    manager: 'James Wilson',
    budget: 12500000,
    completion: '2025-08-15'
  },
  {
    id: 'site-002', 
    name: 'Riverside Apartments',
    code: 'RVA-002',
    address: '456 River Road, Riverside, NY 10002',
    status: 'active',
    type: 'residential',
    phase: 'finishing',
    progress: 85,
    cameras: 16,
    activeAlerts: 1,
    personnel: 28,
    weather: { temp: 74, condition: 'Clear', wind: '5 mph' },
    lastActivity: '5 minutes ago',
    coordinates: { lat: 40.7614, lng: -73.9776 },
    manager: 'Sarah Chen',
    budget: 8750000,
    completion: '2025-05-30'
  },
  {
    id: 'site-003',
    name: 'Industrial Complex East',
    code: 'ICE-003', 
    address: '789 Industrial Blvd, East Side, NY 10003',
    status: 'planning',
    type: 'industrial',
    phase: 'preparation',
    progress: 12,
    cameras: 8,
    activeAlerts: 0,
    personnel: 12,
    weather: { temp: 69, condition: 'Overcast', wind: '12 mph' },
    lastActivity: '1 hour ago',
    coordinates: { lat: 40.7505, lng: -73.9934 },
    manager: 'Mike Rodriguez',
    budget: 18900000,
    completion: '2025-12-20'
  }
];

export const mockCameras = [
  {
    id: 'cam-001',
    name: 'Main Entrance Gate',
    location: 'Gate A - North Entrance',
    status: 'online',
    type: 'fixed',
    resolution: '4K',
    lastSeen: '2025-01-09T10:45:00Z',
    recording: true,
    alerts: 0,
    coordinates: { x: 120, y: 80 },
    streamUrl: '/api/camera/stream/001'
  },
  {
    id: 'cam-002',
    name: 'Tower Crane View',
    location: 'Tower Crane #1',
    status: 'online',
    type: 'ptz',
    resolution: '1080p',
    lastSeen: '2025-01-09T10:44:30Z',
    recording: true,
    alerts: 2,
    coordinates: { x: 250, y: 150 },
    streamUrl: '/api/camera/stream/002'
  },
  {
    id: 'cam-003',
    name: 'Loading Zone Alpha',
    location: 'Material Loading - Zone A',
    status: 'online',
    type: 'dome',
    resolution: '4K',
    lastSeen: '2025-01-09T10:45:00Z',
    recording: true,
    alerts: 1,
    coordinates: { x: 180, y: 200 },
    streamUrl: '/api/camera/stream/003'
  },
  {
    id: 'cam-004',
    name: 'Safety Office View',
    location: 'Safety Office - Building B',
    status: 'maintenance',
    type: 'fixed',
    resolution: '1080p',
    lastSeen: '2025-01-09T09:15:00Z',
    recording: false,
    alerts: 0,
    coordinates: { x: 320, y: 120 },
    streamUrl: null
  }
];

export const mockAlerts = [
  {
    id: 'alert-001',
    type: 'safety_violation',
    priority: 'critical',
    title: 'PPE Violation - Missing Hard Hat',
    message: 'Worker detected without required safety helmet in Zone A',
    location: 'Zone A - Loading Area',
    camera: 'Loading Zone Alpha',
    timestamp: '2025-01-09T10:42:15Z',
    status: 'open',
    assignedTo: 'James Wilson',
    evidence: ['/api/evidence/alert-001-image1.jpg'],
    responseTime: null,
    zone: 'zone-001'
  },
  {
    id: 'alert-002', 
    type: 'equipment_violation',
    priority: 'high',
    title: 'Unauthorized Equipment Movement',
    message: 'Excavator moved outside designated work area',
    location: 'Zone C - Excavation',
    camera: 'Tower Crane View',
    timestamp: '2025-01-09T10:38:45Z',
    status: 'investigating',
    assignedTo: 'Mike Rodriguez',
    evidence: ['/api/evidence/alert-002-image1.jpg', '/api/evidence/alert-002-video1.mp4'],
    responseTime: 8,
    zone: 'zone-003'
  },
  {
    id: 'alert-003',
    type: 'access_violation', 
    priority: 'medium',
    title: 'Unauthorized Area Access',
    message: 'Personnel detected in restricted area during off-hours',
    location: 'Restricted Zone - Electrical',
    camera: 'Main Entrance Gate',
    timestamp: '2025-01-09T10:15:30Z',
    status: 'resolved',
    assignedTo: 'Sarah Chen',
    evidence: ['/api/evidence/alert-003-image1.jpg'],
    responseTime: 25,
    zone: 'zone-004'
  },
  {
    id: 'alert-004',
    type: 'system_alert',
    priority: 'low',
    title: 'Camera Maintenance Required',
    message: 'Camera lens cleaning required due to dust accumulation',
    location: 'Safety Office - Building B',
    camera: 'Safety Office View',
    timestamp: '2025-01-09T09:45:00Z',
    status: 'acknowledged',
    assignedTo: 'IT Support',
    evidence: [],
    responseTime: 15,
    zone: null
  }
];

export const mockDetections = [
  {
    id: 'detection-001',
    timestamp: '2025-01-09T10:45:00Z',
    camera: 'cam-001',
    personCount: 3,
    vehicleCount: 1,
    equipmentCount: 0,
    ppeCompliance: 85,
    safetyViolations: 0,
    confidence: 0.92
  },
  {
    id: 'detection-002',
    timestamp: '2025-01-09T10:44:30Z', 
    camera: 'cam-002',
    personCount: 8,
    vehicleCount: 0,
    equipmentCount: 2,
    ppeCompliance: 75,
    safetyViolations: 1,
    confidence: 0.88
  },
  {
    id: 'detection-003',
    timestamp: '2025-01-09T10:44:00Z',
    camera: 'cam-003', 
    personCount: 5,
    vehicleCount: 2,
    equipmentCount: 1,
    ppeCompliance: 100,
    safetyViolations: 0,
    confidence: 0.95
  }
];

export const mockZones = [
  {
    id: 'zone-001',
    name: 'Loading Area Zone A',
    type: 'work_area',
    safetyLevel: 'medium',
    maxOccupancy: 10,
    currentOccupancy: 3,
    requiresPPE: true,
    requiredPPE: ['hard_hat', 'safety_vest', 'steel_boots'],
    status: 'active',
    coordinates: [
      { x: 150, y: 180 },
      { x: 200, y: 180 },
      { x: 200, y: 220 },
      { x: 150, y: 220 }
    ]
  },
  {
    id: 'zone-002',
    name: 'Crane Operation Zone',
    type: 'equipment',
    safetyLevel: 'high', 
    maxOccupancy: 5,
    currentOccupancy: 2,
    requiresPPE: true,
    requiredPPE: ['hard_hat', 'safety_vest', 'steel_boots', 'safety_harness'],
    status: 'active',
    coordinates: [
      { x: 230, y: 130 },
      { x: 280, y: 130 },
      { x: 280, y: 180 },
      { x: 230, y: 180 }
    ]
  },
  {
    id: 'zone-003',
    name: 'Excavation Area',
    type: 'hazardous',
    safetyLevel: 'critical',
    maxOccupancy: 3,
    currentOccupancy: 1,
    requiresPPE: true,
    requiredPPE: ['hard_hat', 'safety_vest', 'steel_boots', 'safety_harness', 'high_vis'],
    status: 'active',
    coordinates: [
      { x: 100, y: 250 },
      { x: 180, y: 250 },
      { x: 180, y: 300 },
      { x: 100, y: 300 }
    ]
  },
  {
    id: 'zone-004',
    name: 'Electrical Restricted',
    type: 'restricted',
    safetyLevel: 'critical',
    maxOccupancy: 2,
    currentOccupancy: 0,
    requiresPPE: true,
    requiredPPE: ['hard_hat', 'safety_vest', 'steel_boots', 'electrical_gloves'],
    status: 'restricted',
    coordinates: [
      { x: 300, y: 100 },
      { x: 350, y: 100 },
      { x: 350, y: 140 },
      { x: 300, y: 140 }
    ]
  }
];

export const mockRoutes = [
  {
    id: 'route-001',
    name: 'Morning Safety Inspection',
    code: 'MSI-001',
    type: 'inspection',
    estimatedDuration: 45,
    totalDistance: 850,
    status: 'active',
    waypoints: [
      { id: 'wp-001', name: 'Main Gate', lat: 40.7589, lng: -73.9851, order: 1, instructions: 'Check entry log and visitor badges' },
      { id: 'wp-002', name: 'Equipment Storage', lat: 40.7592, lng: -73.9848, order: 2, instructions: 'Verify equipment security and inventory' },
      { id: 'wp-003', name: 'Active Work Zone', lat: 40.7595, lng: -73.9845, order: 3, instructions: 'Inspect PPE compliance and safety protocols' },
      { id: 'wp-004', name: 'Safety Office', lat: 40.7598, lng: -73.9842, order: 4, instructions: 'Review overnight incident reports' }
    ],
    safetyRequirements: ['hard_hat', 'safety_vest', 'steel_boots'],
    authorizedRoles: ['site_manager', 'safety_officer'],
    completionRate: 95,
    averageTime: 42,
    lastCompleted: '2025-01-09T07:30:00Z'
  },
  {
    id: 'route-002',
    name: 'Perimeter Security Check',
    code: 'PSC-002', 
    type: 'patrol',
    estimatedDuration: 30,
    totalDistance: 1200,
    status: 'active',
    waypoints: [
      { id: 'wp-005', name: 'North Fence Line', lat: 40.7601, lng: -73.9855, order: 1, instructions: 'Check fence integrity and lighting' },
      { id: 'wp-006', name: 'East Gate', lat: 40.7598, lng: -73.9840, order: 2, instructions: 'Verify gate lock and access log' },
      { id: 'wp-007', name: 'South Storage Area', lat: 40.7585, lng: -73.9845, order: 3, instructions: 'Check material security and lighting' },
      { id: 'wp-008', name: 'West Emergency Exit', lat: 40.7588, lng: -73.9860, order: 4, instructions: 'Test emergency systems and clear pathways' }
    ],
    safetyRequirements: ['hard_hat', 'safety_vest', 'flashlight'],
    authorizedRoles: ['security_guard', 'site_coordinator'],
    completionRate: 88,
    averageTime: 35,
    lastCompleted: '2025-01-08T22:15:00Z'
  }
];

export const mockAnalytics = {
  safetyMetrics: {
    ppeComplianceRate: 89,
    incidentCount: 3,
    nearMissCount: 7,
    safetyScore: 8.7,
    trendDirection: 'up',
    lastWeekComparison: '+5%'
  },
  operationalMetrics: {
    personnelCount: 45,
    equipmentUtilization: 78,
    weatherImpactScore: 2,
    productivityIndex: 94,
    trendDirection: 'stable',
    lastWeekComparison: '+2%'
  },
  aiPerformance: {
    averageConfidence: 0.91,
    detectionsToday: 1247,
    falsePositiveRate: 0.05,
    modelAccuracy: 0.94,
    processingTime: 125,
    lastModelUpdate: '2025-01-05T14:00:00Z'
  }
};

export const mockNotifications = [
  {
    id: 'notif-001',
    type: 'alert',
    priority: 'high',
    title: 'New Safety Violation',
    message: 'PPE violation detected in Zone A',
    timestamp: '2025-01-09T10:42:15Z',
    read: false,
    actionUrl: '/alerts/alert-001'
  },
  {
    id: 'notif-002', 
    type: 'system',
    priority: 'medium',
    title: 'Camera Offline',
    message: 'Safety Office camera requires maintenance',
    timestamp: '2025-01-09T09:45:00Z',
    read: false,
    actionUrl: '/cameras/cam-004'
  },
  {
    id: 'notif-003',
    type: 'reminder',
    priority: 'low',
    title: 'Daily Report Due',
    message: 'Morning safety inspection report pending',
    timestamp: '2025-01-09T08:00:00Z',
    read: true,
    actionUrl: '/reports/daily'
  }
];