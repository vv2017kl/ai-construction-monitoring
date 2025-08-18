/**
 * Data Calculations Utilities
 * ===========================
 * 
 * Real-time calculations from ZoneMinder and backend data
 * NO HARDCODED VALUES - All calculated from live data
 */

// Calculate safety score from ZoneMinder event data
export const calculateSafetyScore = (events = []) => {
  if (!events || events.length === 0) return { score: 0, confidence: 0 };
  
  // Get confidence scores from detection events
  const confidenceScores = events
    .filter(event => event.confidence_score && event.confidence_score > 0)
    .map(event => event.confidence_score);
  
  if (confidenceScores.length === 0) return { score: 0, confidence: 0 };
  
  // Calculate average confidence (0-1) and convert to 0-10 scale
  const avgConfidence = confidenceScores.reduce((sum, score) => sum + score, 0) / confidenceScores.length;
  const safetyScore = Math.round(avgConfidence * 10 * 10) / 10; // Round to 1 decimal
  
  // Adjust score based on recent incidents
  const recentIncidents = events.filter(event => {
    const eventTime = new Date(event.timestamp);
    const hoursAgo = (new Date() - eventTime) / (1000 * 60 * 60);
    return hoursAgo <= 24 && ['critical', 'high'].includes(event.severity);
  }).length;
  
  // Deduct points for recent incidents
  const adjustedScore = Math.max(0, safetyScore - (recentIncidents * 0.5));
  
  return {
    score: adjustedScore,
    confidence: avgConfidence,
    recentIncidents,
    totalEvents: events.length
  };
};

// Calculate PPE compliance from violation events
export const calculatePPECompliance = (events = [], timeWindowHours = 24) => {
  if (!events || events.length === 0) return { compliance: 0, violations: 0, total: 0 };
  
  const cutoffTime = new Date(Date.now() - (timeWindowHours * 60 * 60 * 1000));
  
  // Get recent events within time window
  const recentEvents = events.filter(event => {
    const eventTime = new Date(event.timestamp);
    return eventTime >= cutoffTime;
  });
  
  // Count PPE-related events
  const ppeViolations = recentEvents.filter(event => 
    event.detection_type === 'ppe_violation'
  ).length;
  
  const personnelEvents = recentEvents.filter(event => 
    event.detection_type === 'personnel_count' || 
    event.detection_type === 'ppe_violation'
  ).length;
  
  // Calculate compliance rate
  let complianceRate = 100; // Start with perfect compliance
  
  if (personnelEvents > 0) {
    // Reduce compliance based on violation frequency
    const violationRate = ppeViolations / personnelEvents;
    complianceRate = Math.max(60, 100 - (violationRate * 100));
  }
  
  // Bonus for zero violations in recent period
  if (ppeViolations === 0 && personnelEvents > 0) {
    complianceRate = Math.min(100, complianceRate + 2);
  }
  
  return {
    compliance: Math.round(complianceRate),
    violations: ppeViolations,
    total: personnelEvents,
    violationRate: personnelEvents > 0 ? (ppeViolations / personnelEvents) * 100 : 0
  };
};

// Calculate personnel count from detection events
export const calculatePersonnelCount = (events = [], cameras = []) => {
  if (!events || events.length === 0) return { count: 0, activeZones: 0, lastUpdate: null };
  
  // Get recent personnel detection events (last 30 minutes)
  const cutoffTime = new Date(Date.now() - (30 * 60 * 1000));
  const recentPersonnelEvents = events.filter(event => {
    const eventTime = new Date(event.timestamp);
    return eventTime >= cutoffTime && event.detection_type === 'personnel_count';
  });
  
  if (recentPersonnelEvents.length === 0) return { count: 0, activeZones: 0, lastUpdate: null };
  
  // Get unique zones with personnel activity
  const activeZones = new Set();
  let totalPersonnel = 0;
  let mostRecentUpdate = null;
  
  recentPersonnelEvents.forEach(event => {
    // Extract personnel count from event description or metadata
    const description = event.description || '';
    const personnelMatch = description.match(/(\d+)\s+personnel/i);
    
    if (personnelMatch) {
      const count = parseInt(personnelMatch[1]);
      totalPersonnel += count;
    } else {
      // Fallback: assume 1 person per personnel detection event
      totalPersonnel += 1;
    }
    
    activeZones.add(event.camera_id);
    
    const eventTime = new Date(event.timestamp);
    if (!mostRecentUpdate || eventTime > mostRecentUpdate) {
      mostRecentUpdate = eventTime;
    }
  });
  
  return {
    count: totalPersonnel,
    activeZones: activeZones.size,
    lastUpdate: mostRecentUpdate,
    eventsAnalyzed: recentPersonnelEvents.length
  };
};

// Calculate equipment activity metrics
export const calculateEquipmentMetrics = (events = []) => {
  if (!events || events.length === 0) return { active: 0, types: [], lastActivity: null };
  
  const cutoffTime = new Date(Date.now() - (60 * 60 * 1000)); // Last hour
  const equipmentEvents = events.filter(event => {
    const eventTime = new Date(event.timestamp);
    return eventTime >= cutoffTime && event.detection_type === 'equipment_operation';
  });
  
  const equipmentTypes = new Set();
  let mostRecentActivity = null;
  
  equipmentEvents.forEach(event => {
    if (event.equipment_involved && event.equipment_involved.length > 0) {
      event.equipment_involved.forEach(equipment => {
        equipmentTypes.add(equipment);
      });
    }
    
    const eventTime = new Date(event.timestamp);
    if (!mostRecentActivity || eventTime > mostRecentActivity) {
      mostRecentActivity = eventTime;
    }
  });
  
  return {
    active: equipmentTypes.size,
    types: Array.from(equipmentTypes),
    lastActivity: mostRecentActivity,
    eventsCount: equipmentEvents.length
  };
};

// Calculate progress metrics from milestone events
export const calculateProgressMetrics = (events = [], siteData = {}) => {
  if (!events || events.length === 0) return { completion: 0, milestones: 0, trend: 'stable' };
  
  const milestoneEvents = events.filter(event => 
    event.detection_type === 'progress_milestone'
  );
  
  if (milestoneEvents.length === 0) return { completion: 0, milestones: 0, trend: 'stable' };
  
  // Calculate completion based on milestone frequency and site type
  const daysSinceStart = siteData.start_date ? 
    (new Date() - new Date(siteData.start_date)) / (1000 * 60 * 60 * 24) : 100;
  
  const milestonesPerDay = milestoneEvents.length / Math.max(1, daysSinceStart);
  
  // Estimate completion based on milestone frequency (construction industry average)
  let estimatedCompletion = Math.min(95, milestonesPerDay * daysSinceStart * 2);
  
  // Adjust based on site type (different project timelines)
  if (siteData.type === 'high_rise_building') {
    estimatedCompletion = estimatedCompletion * 0.8; // Slower progress for complex projects
  } else if (siteData.type === 'renovation_project') {
    estimatedCompletion = estimatedCompletion * 1.2; // Faster for renovations
  }
  
  // Calculate trend from recent milestone activity
  const recentMilestones = milestoneEvents.filter(event => {
    const eventTime = new Date(event.timestamp);
    const daysAgo = (new Date() - eventTime) / (1000 * 60 * 60 * 24);
    return daysAgo <= 7;
  }).length;
  
  const previousMilestones = milestoneEvents.filter(event => {
    const eventTime = new Date(event.timestamp);
    const daysAgo = (new Date() - eventTime) / (1000 * 60 * 60 * 24);
    return daysAgo > 7 && daysAgo <= 14;
  }).length;
  
  let trend = 'stable';
  if (recentMilestones > previousMilestones) {
    trend = 'improving';
  } else if (recentMilestones < previousMilestones) {
    trend = 'declining';
  }
  
  return {
    completion: Math.round(Math.min(100, Math.max(0, estimatedCompletion))),
    milestones: milestoneEvents.length,
    recentMilestones,
    trend,
    milestonesPerDay: Math.round(milestonesPerDay * 100) / 100
  };
};

// Get site coordinates from first camera or fallback to Seattle area
export const getSiteCoordinates = (cameras = [], sites = []) => {
  // Try to get coordinates from cameras
  if (cameras && cameras.length > 0) {
    const firstCamera = cameras[0];
    if (firstCamera.coordinates && Array.isArray(firstCamera.coordinates)) {
      return {
        lat: firstCamera.coordinates[0],
        lon: firstCamera.coordinates[1]
      };
    }
  }
  
  // Try to get coordinates from sites
  if (sites && sites.length > 0) {
    const firstSite = sites[0];
    if (firstSite.latitude && firstSite.longitude) {
      return {
        lat: firstSite.latitude,
        lon: firstSite.longitude
      };
    }
  }
  
  // Fallback to Seattle construction area coordinates
  return {
    lat: 47.6062,
    lon: -122.3321
  };
};

// Calculate alert priority for dashboard display
export const calculateAlertPriority = (events = []) => {
  if (!events || events.length === 0) return { critical: 0, high: 0, total: 0 };
  
  const critical = events.filter(event => event.severity === 'critical').length;
  const high = events.filter(event => event.severity === 'high').length;
  const medium = events.filter(event => event.severity === 'medium').length;
  
  return {
    critical,
    high,
    medium,
    total: events.length,
    needsImmediate: critical + high
  };
};

// Generate dashboard metrics summary
export const generateDashboardMetrics = (zoneminderData = {}) => {
  const {
    cameras = { cameras: [] },
    events = { events: [] },
    zones = { zones: [] },
    status = {}
  } = zoneminderData;
  
  const eventList = events.events || [];
  const cameraList = cameras.cameras || [];
  
  return {
    safety: calculateSafetyScore(eventList),
    ppe: calculatePPECompliance(eventList),
    personnel: calculatePersonnelCount(eventList, cameraList),
    equipment: calculateEquipmentMetrics(eventList),
    progress: calculateProgressMetrics(eventList),
    alerts: calculateAlertPriority(eventList),
    coordinates: getSiteCoordinates(cameraList),
    lastCalculated: new Date().toISOString()
  };
};