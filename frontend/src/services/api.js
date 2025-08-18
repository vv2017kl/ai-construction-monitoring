/**
 * Core API Service Layer
 * =====================
 * 
 * Centralized API service for all backend interactions
 */

import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API_BASE = `${BACKEND_URL}/api`;

// Create axios instance with common configuration
const apiClient = axios.create({
  baseURL: API_BASE,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for authentication and logging
apiClient.interceptors.request.use(
  (config) => {
    // Add auth token if available
    const token = localStorage.getItem('auth_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    
    // Log API calls in development
    if (process.env.NODE_ENV === 'development') {
      console.log(`🔄 API Request: ${config.method?.toUpperCase()} ${config.url}`);
    }
    
    return config;
  },
  (error) => {
    console.error('❌ API Request Error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => {
    // Log successful responses in development
    if (process.env.NODE_ENV === 'development') {
      console.log(`✅ API Response: ${response.config.method?.toUpperCase()} ${response.config.url}`, response.status);
    }
    return response;
  },
  (error) => {
    console.error('❌ API Response Error:', error.response?.status, error.response?.data || error.message);
    
    // Handle common error scenarios
    if (error.response?.status === 401) {
      // Unauthorized - redirect to login
      localStorage.removeItem('auth_token');
      window.location.href = '/login';
    }
    
    return Promise.reject(error);
  }
);

// Generic API methods
export const api = {
  // GET request
  get: async (endpoint, params = {}) => {
    const response = await apiClient.get(endpoint, { params });
    return response.data;
  },

  // POST request
  post: async (endpoint, data = {}) => {
    const response = await apiClient.post(endpoint, data);
    return response.data;
  },

  // PUT request
  put: async (endpoint, data = {}) => {
    const response = await apiClient.put(endpoint, data);
    return response.data;
  },

  // DELETE request
  delete: async (endpoint) => {
    const response = await apiClient.delete(endpoint);
    return response.data;
  },

  // PATCH request
  patch: async (endpoint, data = {}) => {
    const response = await apiClient.patch(endpoint, data);
    return response.data;
  }
};

// Health check utility
export const checkAPIHealth = async () => {
  try {
    const response = await api.get('/health');
    return { status: 'healthy', data: response };
  } catch (error) {
    return { status: 'unhealthy', error: error.message };
  }
};

export default api;