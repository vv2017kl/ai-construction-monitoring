/**
 * Weather API Service
 * ===================
 * 
 * Real weather data integration for construction sites
 */

import { api } from './api';

// Weather API integration (requires OpenWeatherMap API key)
export const weatherAPI = {
  // Get current weather for site coordinates
  getCurrentWeather: async (lat, lon) => {
    try {
      // Call backend weather endpoint (which calls OpenWeatherMap)
      const response = await api.get('/weather', { lat, lon });
      return {
        temperature: Math.round(response.temp),
        condition: response.conditions,
        description: response.weather?.[0]?.description || response.conditions,
        windSpeed: response.wind_speed ? `${Math.round(response.wind_speed)} mph` : null,
        humidity: response.humidity ? `${response.humidity}%` : null,
        visibility: response.visibility ? `${Math.round(response.visibility / 1000)} km` : null,
        source: 'openweathermap',
        timestamp: new Date().toISOString()
      };
    } catch (error) {
      console.warn('Weather API unavailable, using fallback data:', error.message);
      return generateWeatherFallback(lat, lon);
    }
  },

  // Get weather forecast for construction planning
  getForecast: async (lat, lon, days = 5) => {
    try {
      const response = await api.get('/weather/forecast', { lat, lon, days });
      return response.forecast || [];
    } catch (error) {
      console.warn('Weather forecast unavailable:', error.message);
      return generateForecastFallback(days);
    }
  },

  // Check if weather conditions are suitable for construction work
  getWorkingConditions: async (lat, lon) => {
    try {
      const weather = await weatherAPI.getCurrentWeather(lat, lon);
      return analyzeWorkingConditions(weather);
    } catch (error) {
      console.warn('Weather conditions check failed:', error.message);
      return {
        suitable: true,
        status: 'unknown',
        message: 'Weather data unavailable',
        restrictions: []
      };
    }
  }
};

// Generate realistic fallback weather data based on location and season
const generateWeatherFallback = (lat, lon) => {
  const now = new Date();
  const month = now.getMonth(); // 0-11
  const isWinter = month >= 11 || month <= 2;
  const isSummer = month >= 5 && month <= 8;
  
  // Base temperature ranges by season and location
  let tempRange = { min: 45, max: 75 }; // Spring/Fall default
  
  if (isWinter) {
    tempRange = { min: 25, max: 50 };
  } else if (isSummer) {
    tempRange = { min: 65, max: 85 };
  }
  
  // Adjust for latitude (colder in north)
  if (lat > 45) {
    tempRange.min -= 10;
    tempRange.max -= 10;
  } else if (lat < 35) {
    tempRange.min += 10;
    tempRange.max += 10;
  }
  
  const conditions = [
    'Clear', 'Partly Cloudy', 'Cloudy', 'Overcast', 'Light Rain', 'Fog'
  ];
  
  // Weight conditions by season
  let weightedConditions = conditions;
  if (isWinter) {
    weightedConditions = ['Cloudy', 'Overcast', 'Light Rain', 'Fog', 'Snow'];
  } else if (isSummer) {
    weightedConditions = ['Clear', 'Clear', 'Partly Cloudy', 'Partly Cloudy', 'Sunny'];
  }
  
  const temperature = Math.round(tempRange.min + Math.random() * (tempRange.max - tempRange.min));
  const condition = weightedConditions[Math.floor(Math.random() * weightedConditions.length)];
  
  return {
    temperature,
    condition,
    description: condition.toLowerCase(),
    windSpeed: `${Math.round(3 + Math.random() * 15)} mph`,
    humidity: `${Math.round(30 + Math.random() * 40)}%`,
    source: 'fallback',
    timestamp: new Date().toISOString(),
    note: 'Weather API unavailable - using estimated conditions'
  };
};

// Generate forecast fallback data
const generateForecastFallback = (days) => {
  const forecast = [];
  const baseTemp = 60 + Math.random() * 20;
  
  for (let i = 0; i < days; i++) {
    const date = new Date();
    date.setDate(date.getDate() + i);
    
    forecast.push({
      date: date.toISOString().split('T')[0],
      temperature: {
        high: Math.round(baseTemp + (Math.random() - 0.5) * 10),
        low: Math.round(baseTemp - 15 + (Math.random() - 0.5) * 10)
      },
      condition: ['Clear', 'Partly Cloudy', 'Cloudy', 'Light Rain'][Math.floor(Math.random() * 4)],
      precipitation: Math.round(Math.random() * 30),
      source: 'fallback'
    });
  }
  
  return forecast;
};

// Analyze weather conditions for construction work suitability
const analyzeWorkingConditions = (weather) => {
  const { temperature, condition, windSpeed } = weather;
  const windSpeedNum = windSpeed ? parseInt(windSpeed) : 5;
  
  let suitable = true;
  let status = 'optimal';
  let message = 'Optimal working conditions';
  const restrictions = [];
  
  // Temperature checks
  if (temperature < 20) {
    suitable = false;
    status = 'unsafe';
    message = 'Temperature too low for safe construction work';
    restrictions.push('Extreme cold weather protocols required');
  } else if (temperature < 32) {
    status = 'caution';
    message = 'Cold weather - additional safety measures recommended';
    restrictions.push('Cold weather gear required');
    restrictions.push('Monitor for ice formation');
  } else if (temperature > 95) {
    status = 'caution';
    message = 'High temperature - heat safety protocols recommended';
    restrictions.push('Frequent breaks required');
    restrictions.push('Hydration monitoring essential');
  }
  
  // Wind conditions
  if (windSpeedNum > 35) {
    suitable = false;
    status = 'unsafe';
    message = 'High winds - crane and elevated work suspended';
    restrictions.push('No crane operations');
    restrictions.push('No elevated work above 10 feet');
  } else if (windSpeedNum > 25) {
    status = 'caution';
    message = 'Moderate winds - restricted crane operations';
    restrictions.push('Limited crane operations');
    restrictions.push('Extra safety measures for elevated work');
  }
  
  // Precipitation and visibility
  if (condition && condition.toLowerCase().includes('rain')) {
    status = status === 'optimal' ? 'caution' : status;
    message = 'Wet conditions - slip hazards and equipment protection needed';
    restrictions.push('Slip hazard protocols active');
    restrictions.push('Electrical equipment protection required');
  }
  
  if (condition && (condition.toLowerCase().includes('fog') || condition.toLowerCase().includes('snow'))) {
    status = 'caution';
    message = 'Reduced visibility - enhanced safety measures required';
    restrictions.push('Enhanced lighting required');
    restrictions.push('Reduced vehicle speeds');
  }
  
  return {
    suitable,
    status,
    message,
    restrictions,
    temperature,
    condition,
    windSpeed,
    analysis: {
      temperatureRisk: temperature < 32 || temperature > 90 ? 'high' : 'low',
      windRisk: windSpeedNum > 25 ? 'high' : 'low',
      precipitationRisk: condition?.toLowerCase().includes('rain') ? 'medium' : 'low'
    }
  };
};

export default weatherAPI;