import React, { createContext, useContext, useState, useEffect } from 'react';
import { themes, defaultTheme } from '../theme/colors';

const ThemeContext = createContext();

export const useTheme = () => {
  const context = useContext(ThemeContext);
  if (!context) {
    throw new Error('useTheme must be used within a ThemeProvider');
  }
  return context;
};

export const ThemeProvider = ({ children }) => {
  const [currentTheme, setCurrentTheme] = useState(() => {
    // Get theme from localStorage or use default
    const savedTheme = localStorage.getItem('construction-app-theme');
    return savedTheme || defaultTheme;
  });

  const theme = themes[currentTheme];

  const changeTheme = (themeName) => {
    setCurrentTheme(themeName);
    localStorage.setItem('construction-app-theme', themeName);
  };

  // Apply CSS custom properties to document root
  useEffect(() => {
    const root = document.documentElement;
    
    // Apply primary colors
    root.style.setProperty('--color-primary-50', theme.primary[50]);
    root.style.setProperty('--color-primary-100', theme.primary[100]);
    root.style.setProperty('--color-primary-500', theme.primary[500]);
    root.style.setProperty('--color-primary-600', theme.primary[600]);
    root.style.setProperty('--color-primary-700', theme.primary[700]);
    root.style.setProperty('--color-primary-800', theme.primary[800]);
    root.style.setProperty('--color-primary-900', theme.primary[900]);

    // Apply secondary colors
    root.style.setProperty('--color-secondary-50', theme.secondary[50]);
    root.style.setProperty('--color-secondary-100', theme.secondary[100]);
    root.style.setProperty('--color-secondary-500', theme.secondary[500]);
    root.style.setProperty('--color-secondary-600', theme.secondary[600]);
    root.style.setProperty('--color-secondary-700', theme.secondary[700]);
    root.style.setProperty('--color-secondary-800', theme.secondary[800]);
    root.style.setProperty('--color-secondary-900', theme.secondary[900]);

    // Apply semantic colors
    root.style.setProperty('--color-success-50', theme.success[50]);
    root.style.setProperty('--color-success-500', theme.success[500]);
    root.style.setProperty('--color-success-600', theme.success[600]);

    root.style.setProperty('--color-warning-50', theme.warning[50]);
    root.style.setProperty('--color-warning-500', theme.warning[500]);
    root.style.setProperty('--color-warning-600', theme.warning[600]);

    root.style.setProperty('--color-danger-50', theme.danger[50]);
    root.style.setProperty('--color-danger-500', theme.danger[500]);
    root.style.setProperty('--color-danger-600', theme.danger[600]);

    // Apply background colors
    root.style.setProperty('--color-bg-primary', theme.background.primary);
    root.style.setProperty('--color-bg-secondary', theme.background.secondary);
    root.style.setProperty('--color-bg-tertiary', theme.background.tertiary);

  }, [theme]);

  const value = {
    currentTheme,
    theme,
    themes: Object.keys(themes),
    changeTheme,
    themeDisplayNames: Object.entries(themes).reduce((acc, [key, value]) => {
      acc[key] = value.name;
      return acc;
    }, {})
  };

  return (
    <ThemeContext.Provider value={value}>
      {children}
    </ThemeContext.Provider>
  );
};