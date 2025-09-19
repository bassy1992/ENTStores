// API Configuration
const _env = (import.meta as any).env;
const isDevelopment = _env.DEV;

export const API_BASE_URL = isDevelopment
  ? 'http://localhost:8000'
  : _env.VITE_API_URL || 'https://enontino-production.up.railway.app';

export const API_ENDPOINTS = {
  // Payment endpoints
  EXCHANGE_RATE: `${API_BASE_URL}/api/payments/exchange-rate/`,
  STRIPE_CHECKOUT: `${API_BASE_URL}/api/payments/stripe/create-checkout-session/`,
  STRIPE_VERIFY: `${API_BASE_URL}/api/payments/stripe/verify-session/`,
  MOMO_INITIATE: `${API_BASE_URL}/api/payments/momo/initiate/`,
  MOMO_STATUS: `${API_BASE_URL}/api/payments/momo/status/`,
  CREATE_ORDER: `${API_BASE_URL}/api/payments/create-order/`,
  
  // Add other endpoints as needed
  PRODUCTS: `${API_BASE_URL}/api/products/`,
  CATEGORIES: `${API_BASE_URL}/api/categories/`,
} as const;

// Helper function to build API URLs
export const buildApiUrl = (endpoint: string) => `${API_BASE_URL}${endpoint}`;

// Helper function for API calls with error handling
export const apiCall = async (url: string, options?: RequestInit) => {
  try {
    const response = await fetch(url, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options?.headers,
      },
    });
    
    if (!response.ok) {
      throw new Error(`API call failed: ${response.status} ${response.statusText}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error('API call error:', error);
    throw error;
  }
};