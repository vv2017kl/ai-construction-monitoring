/**
 * Authentication Context
 * ======================
 * 
 * Provides authentication state and functions throughout the application
 */

import React, { createContext, useContext, useState, useEffect } from 'react';
import { backendAPI } from '../services';

const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  // Initialize authentication state
  useEffect(() => {
    const initAuth = async () => {
      try {
        const token = localStorage.getItem('auth_token');
        if (token) {
          // For now, set a mock user - replace with real API call when backend auth is ready
          setUser({
            id: 'user_001',
            firstName: 'Site',
            lastName: 'Manager',
            email: 'manager@construction.com',
            role: 'site_manager',
            permissions: ['dashboard', 'live_view', 'alerts', 'analytics', 'personnel']
          });
          setIsAuthenticated(true);
        }
      } catch (error) {
        console.error('Auth initialization error:', error);
        localStorage.removeItem('auth_token');
      } finally {
        setLoading(false);
      }
    };

    initAuth();
  }, []);

  const login = async (email, password) => {
    try {
      setLoading(true);
      
      // Mock login for now - replace with real API call
      if (email && password) {
        const mockUser = {
          id: 'user_001',
          firstName: 'Site',
          lastName: 'Manager',
          email: email,
          role: 'site_manager',
          permissions: ['dashboard', 'live_view', 'alerts', 'analytics', 'personnel']
        };
        
        const mockToken = 'mock_jwt_token_' + Date.now();
        
        localStorage.setItem('auth_token', mockToken);
        setUser(mockUser);
        setIsAuthenticated(true);
        
        return { success: true, user: mockUser };
      } else {
        throw new Error('Invalid credentials');
      }
    } catch (error) {
      console.error('Login error:', error);
      return { success: false, error: error.message };
    } finally {
      setLoading(false);
    }
  };

  const logout = async () => {
    try {
      localStorage.removeItem('auth_token');
      setUser(null);
      setIsAuthenticated(false);
    } catch (error) {
      console.error('Logout error:', error);
    }
  };

  const updateProfile = async (profileData) => {
    try {
      // Mock profile update - replace with real API call
      const updatedUser = { ...user, ...profileData };
      setUser(updatedUser);
      return { success: true, user: updatedUser };
    } catch (error) {
      console.error('Profile update error:', error);
      return { success: false, error: error.message };
    }
  };

  const hasPermission = (permission) => {
    return user?.permissions?.includes(permission) || false;
  };

  const value = {
    user,
    loading,
    isAuthenticated,
    login,
    logout,
    updateProfile,
    hasPermission
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

export default AuthContext;