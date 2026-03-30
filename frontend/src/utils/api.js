/**
 * API Utility Functions
 * Handles API calls and URL configuration
 */

// Get API base URL - in production, this will be set via environment variable
const getAPIBaseUrl = () => {
  // Check for environment variable (set during build)
  if (typeof import.meta !== 'undefined' && import.meta.env.VITE_API_URL) {
    return import.meta.env.VITE_API_URL
  }
  
  // Development: use relative path (proxied by Vite)
  if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
    return '/api'
  }
  
  // Production: default to same domain as frontend
  return `${window.location.protocol}//${window.location.host}/api`
}

const API_BASE_URL = getAPIBaseUrl()

export const apiCall = async (endpoint, options = {}) => {
  const url = `${API_BASE_URL}${endpoint}`
  
  try {
    const response = await fetch(url, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
    })
    
    if (!response.ok) {
      throw new Error(`API Error: ${response.status} ${response.statusText}`)
    }
    
    return await response.json()
  } catch (error) {
    console.error(`API call failed for ${endpoint}:`, error)
    throw error
  }
}

export default {
  baseUrl: API_BASE_URL,
  apiCall,
}
