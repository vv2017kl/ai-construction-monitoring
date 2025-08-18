/**
 * Application Constants
 * ====================
 * 
 * Centralized constants for the application
 */

// ZoneMinder Constants
export const ZONEMINDER_CONSTANTS = {
  STREAM_QUALITIES: {
    LOW: 'low',
    MEDIUM: 'medium', 
    HIGH: 'high',
    ULTRA: 'ultra'
  },
  
  DETECTION_TYPES: {
    PPE_VIOLATION: 'ppe_violation',
    RESTRICTED_ACCESS: 'restricted_access',
    EQUIPMENT_OPERATION: 'equipment_operation',
    PERSONNEL_COUNT: 'personnel_count',
    SAFETY_HAZARD: 'safety_hazard',
    PROGRESS_MILESTONE: 'progress_milestone',
    WEATHER_ALERT: 'weather_alert'
  },

  ZONE_TYPES: {
    SAFETY: 'safety',
    PROGRESS: 'progress',
    EQUIPMENT: 'equipment',
    RESTRICTED: 'restricted'
  },

  SEVERITY_LEVELS: {
    LOW: 'low',
    MEDIUM: 'medium',
    HIGH: 'high',
    CRITICAL: 'critical'
  },

  CAMERA_STATUSES: {
    ONLINE: 'online',
    OFFLINE: 'offline',
    ERROR: 'error',
    MAINTENANCE: 'maintenance'
  },

  CAMERA_TYPES: {
    FIXED_SECURITY: 'fixed_security',
    PTZ_MONITORING: 'ptz_monitoring',
    MOBILE_INSPECTION: 'mobile_inspection',
    DRONE_AERIAL: 'drone_aerial',
    TIMELAPSE: 'timelapse'
  }
};

// Construction Industry Constants
export const CONSTRUCTION_CONSTANTS = {
  PROJECT_TYPES: {
    HIGH_RISE_BUILDING: 'high_rise_building',
    RESIDENTIAL_COMPLEX: 'residential_complex',
    COMMERCIAL_MALL: 'commercial_mall',
    INFRASTRUCTURE_HIGHWAY: 'infrastructure_highway',
    INDUSTRIAL_FACILITY: 'industrial_facility',
    RENOVATION_PROJECT: 'renovation_project'
  },

  HAZARD_LEVELS: {
    LOW: 'low',
    MEDIUM: 'medium',
    HIGH: 'high',
    CRITICAL: 'critical'
  },

  SECURITY_LEVELS: {
    STANDARD: 'standard',
    HIGH: 'high',
    MAXIMUM: 'maximum'
  },

  PROJECT_PHASES: [
    'Site Preparation',
    'Foundation',
    'Structure',
    'Building Envelope',
    'MEP Systems',
    'Interior Fit-out',
    'Final Inspections'
  ],

  EQUIPMENT_TYPES: [
    'Tower Crane',
    'Mobile Crane', 
    'Excavator',
    'Bulldozer',
    'Concrete Mixer',
    'Dump Truck',
    'Loader',
    'Forklift',
    'Generator',
    'Concrete Pump'
  ]
};

// UI Constants
export const UI_CONSTANTS = {
  THEME_COLORS: {
    PRIMARY: '#2563eb',
    SECONDARY: '#64748b',
    SUCCESS: '#16a34a',
    WARNING: '#d97706',
    ERROR: '#dc2626',
    INFO: '#0ea5e9'
  },

  REFRESH_INTERVALS: {
    DASHBOARD: 30000,      // 30 seconds
    LIVE_VIEW: 5000,       // 5 seconds
    ALERTS: 10000,         // 10 seconds
    ANALYTICS: 60000,      // 1 minute
    EVENTS: 15000,         // 15 seconds
    CAMERAS: 20000         // 20 seconds
  },

  PAGINATION_SIZES: [10, 25, 50, 100],

  DATE_FORMATS: {
    DISPLAY: 'MMM dd, yyyy HH:mm',
    API: 'yyyy-MM-dd\'T\'HH:mm:ss.SSSxxxxx',
    SHORT: 'MMM dd',
    TIME_ONLY: 'HH:mm:ss'
  }
};

// API Constants
export const API_CONSTANTS = {
  TIMEOUT: 30000,
  RETRY_ATTEMPTS: 3,
  RETRY_DELAY: 1000,
  
  STATUS_CODES: {
    SUCCESS: 200,
    CREATED: 201,
    BAD_REQUEST: 400,
    UNAUTHORIZED: 401,
    FORBIDDEN: 403,
    NOT_FOUND: 404,
    INTERNAL_ERROR: 500,
    SERVICE_UNAVAILABLE: 503
  }
};

// Local Storage Keys
export const STORAGE_KEYS = {
  AUTH_TOKEN: 'auth_token',
  USER_PREFERENCES: 'user_preferences',
  THEME: 'theme',
  DASHBOARD_LAYOUT: 'dashboard_layout',
  CAMERA_SETTINGS: 'camera_settings',
  RECENT_SITES: 'recent_sites'
};

// Routes
export const ROUTES = {
  HOME: '/',
  LOGIN: '/login',
  
  // Solution User Portal
  DASHBOARD: '/dashboard',
  LIVE_VIEW: '/live-view',
  LIVE_STREET_VIEW: '/live-street-view',
  VIDEO_REVIEW: '/video-review',
  SITE_OVERVIEW: '/site-overview',
  ALERT_CENTER: '/alert-center',
  AI_ANALYTICS: '/ai-analytics',
  TIME_LAPSE: '/time-lapse',
  PERSONNEL: '/personnel',
  REPORTS: '/reports',
  FIELD_ASSESSMENT: '/field-assessment',
  PROFILE: '/profile',
  SETTINGS: '/settings',
  HELP: '/help',
  
  // Solution Admin Portal
  ADMIN_DASHBOARD: '/admin/dashboard',
  ADMIN_USERS: '/admin/users',
  ADMIN_DEPARTMENTS: '/admin/departments',
  ADMIN_ACCESS_CONTROL: '/admin/access-control',
  ADMIN_SITE_CONFIG: '/admin/site-config',
  ADMIN_EQUIPMENT: '/admin/equipment',
  ADMIN_AI_MODELS: '/admin/ai-models',
  ADMIN_MONITORING: '/admin/monitoring',
  ADMIN_INTEGRATIONS: '/admin/integrations'
};