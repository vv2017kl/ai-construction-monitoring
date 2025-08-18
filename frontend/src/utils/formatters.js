/**
 * Data Formatters
 * ===============
 * 
 * Utility functions for formatting data display
 */

import { format, formatDistanceToNow, parseISO, isValid } from 'date-fns';

// Date/Time Formatters
export const formatters = {
  // Format date for display
  formatDate: (date, formatString = 'MMM dd, yyyy') => {
    if (!date) return 'N/A';
    
    try {
      const dateObj = typeof date === 'string' ? parseISO(date) : date;
      return isValid(dateObj) ? format(dateObj, formatString) : 'Invalid Date';
    } catch (error) {
      console.warn('Date formatting error:', error);
      return 'Invalid Date';
    }
  },

  // Format date and time for display
  formatDateTime: (date, formatString = 'MMM dd, yyyy HH:mm') => {
    return formatters.formatDate(date, formatString);
  },

  // Format time only
  formatTime: (date, formatString = 'HH:mm:ss') => {
    return formatters.formatDate(date, formatString);
  },

  // Format relative time (e.g., "2 hours ago")
  formatRelativeTime: (date) => {
    if (!date) return 'N/A';
    
    try {
      const dateObj = typeof date === 'string' ? parseISO(date) : date;
      return isValid(dateObj) ? formatDistanceToNow(dateObj, { addSuffix: true }) : 'Unknown';
    } catch (error) {
      console.warn('Relative time formatting error:', error);
      return 'Unknown';
    }
  },

  // Format duration in seconds to human readable
  formatDuration: (seconds) => {
    if (!seconds || seconds < 0) return '0s';
    
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = Math.floor(seconds % 60);
    
    if (hours > 0) {
      return `${hours}h ${minutes}m ${secs}s`;
    } else if (minutes > 0) {
      return `${minutes}m ${secs}s`;
    } else {
      return `${secs}s`;
    }
  },

  // Number Formatters
  formatNumber: (num, decimals = 0) => {
    if (num === null || num === undefined) return 'N/A';
    return Number(num).toLocaleString(undefined, { 
      minimumFractionDigits: decimals,
      maximumFractionDigits: decimals 
    });
  },

  // Format percentage
  formatPercentage: (value, decimals = 1) => {
    if (value === null || value === undefined) return 'N/A';
    return `${Number(value).toFixed(decimals)}%`;
  },

  // Format file size
  formatFileSize: (bytes) => {
    if (!bytes || bytes === 0) return '0 B';
    
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB', 'TB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    
    return `${parseFloat((bytes / Math.pow(k, i)).toFixed(1))} ${sizes[i]}`;
  },

  // Format currency
  formatCurrency: (amount, currency = 'USD') => {
    if (amount === null || amount === undefined) return 'N/A';
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: currency
    }).format(amount);
  },

  // String Formatters
  formatCameraType: (type) => {
    if (!type) return 'Unknown';
    return type.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
  },

  formatDetectionType: (type) => {
    if (!type) return 'Unknown';
    return type.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
  },

  formatSeverity: (severity) => {
    if (!severity) return 'Unknown';
    return severity.charAt(0).toUpperCase() + severity.slice(1);
  },

  formatStatus: (status) => {
    if (!status) return 'Unknown';
    return status.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
  },

  // Truncate text with ellipsis
  truncateText: (text, maxLength = 50) => {
    if (!text) return '';
    return text.length > maxLength ? `${text.substring(0, maxLength)}...` : text;
  },

  // Format coordinates
  formatCoordinates: (lat, lon, decimals = 6) => {
    if (!lat || !lon) return 'N/A';
    return `${Number(lat).toFixed(decimals)}, ${Number(lon).toFixed(decimals)}`;
  },

  // Construction-specific formatters
  formatProjectPhase: (phase) => {
    if (!phase) return 'Unknown';
    return phase.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
  },

  formatHazardLevel: (level) => {
    if (!level) return 'Unknown';
    const colors = {
      low: 'text-green-600',
      medium: 'text-yellow-600', 
      high: 'text-orange-600',
      critical: 'text-red-600'
    };
    return {
      text: level.toUpperCase(),
      className: colors[level?.toLowerCase()] || 'text-gray-600'
    };
  },

  formatComplianceScore: (score) => {
    if (score === null || score === undefined) return 'N/A';
    const numScore = Number(score);
    let color = 'text-gray-600';
    
    if (numScore >= 90) color = 'text-green-600';
    else if (numScore >= 75) color = 'text-yellow-600';
    else if (numScore >= 60) color = 'text-orange-600';
    else color = 'text-red-600';
    
    return {
      text: `${numScore.toFixed(1)}%`,
      className: color
    };
  },

  // Event priority formatting
  formatEventPriority: (severity, detectionType) => {
    const severityWeight = {
      critical: 4,
      high: 3,
      medium: 2,
      low: 1
    };
    
    const typeWeight = {
      safety_hazard: 4,
      ppe_violation: 3,
      restricted_access: 3,
      equipment_operation: 2,
      personnel_count: 1,
      progress_milestone: 1,
      weather_alert: 3
    };
    
    const totalWeight = (severityWeight[severity] || 1) + (typeWeight[detectionType] || 1);
    
    if (totalWeight >= 7) return { text: 'URGENT', className: 'text-red-600 font-bold' };
    if (totalWeight >= 5) return { text: 'HIGH', className: 'text-orange-600 font-semibold' };
    if (totalWeight >= 3) return { text: 'MEDIUM', className: 'text-yellow-600' };
    return { text: 'LOW', className: 'text-green-600' };
  }
};