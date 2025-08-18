/**
 * Services Export Index
 * ====================
 * 
 * Central export point for all API services
 */

export { api, checkAPIHealth } from './api';
export { backendAPI } from './backendAPI';
export { zoneminderAPI } from './zoneminderAPI';

// Re-export commonly used utilities
export const apiServices = {
  core: () => import('./api'),
  backend: () => import('./backendAPI'), 
  zoneminder: () => import('./zoneminderAPI'),
};