/**
 * API Utility Functions
 * Handles API calls and URL configuration
 */

let API_BASE_URL = null;

// Load API base URL from config file
const getAPIBaseUrl = async () => {
  if (API_BASE_URL) {
    return API_BASE_URL;
  }

  try {
    // Try to load from config file (production)
    const response = await fetch('/config.json');
    if (response.ok) {
      const config = await response.json();
      API_BASE_URL = config.API_URL;
      console.log('Loaded API URL from config.json:', API_BASE_URL);
      return API_BASE_URL;
    }
  } catch (error) {
    console.warn('Could not load config.json:', error);
  }

  // Fallback: check environment variable (development)
  if (typeof import.meta !== 'undefined' && import.meta.env.VITE_API_URL) {
    API_BASE_URL = import.meta.env.VITE_API_URL;
    console.log('Using VITE_API_URL:', API_BASE_URL);
    return API_BASE_URL;
  }

  // Development: use relative path (proxied by Vite)
  if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
    API_BASE_URL = '/api';
    console.log('Using localhost relative path:', API_BASE_URL);
    return API_BASE_URL;
  }

  // Production fallback: assume API is on same domain/port
  API_BASE_URL = `${window.location.protocol}//${window.location.host}/api`;
  console.log('Using same-domain fallback:', API_BASE_URL);
  return API_BASE_URL;
};

export const apiCall = async (endpoint, options = {}) => {
  const baseUrl = await getAPIBaseUrl();
  const url = `${baseUrl}${endpoint}`;
  
  try {
    const response = await fetch(url, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
    });
    
    if (!response.ok) {
      throw new Error(`API Error: ${response.status} ${response.statusText}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error(`API call failed for ${endpoint}:`, error);
    throw error;
  }
};

export default {
  apiCall,
}
