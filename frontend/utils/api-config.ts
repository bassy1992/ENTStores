// API configuration utility
// Centralized API configuration for consistent usage across components

const _env = (import.meta as any).env;

// API Base URL configuration
export const API_BASE_URL = _env.VITE_SHOP_API_BASE_URL || 
  (_env.DEV ? '/api/shop' : 'https://entstores-production.up.railway.app/api/shop');

// Environment detection
export const isDevelopment = _env.DEV;
export const isProduction = !_env.DEV;

// API endpoints
export const API_ENDPOINTS = {
  // Products
  products: `${API_BASE_URL}/products`,
  productDetail: (slug: string) => `${API_BASE_URL}/products/${slug}`,
  
  // Reviews
  productReviews: (productId: string) => `${API_BASE_URL}/products/${productId}/reviews`,
  reviewVote: (reviewId: string) => `${API_BASE_URL}/reviews/${reviewId}/vote`,
  
  // Other endpoints
  categories: `${API_BASE_URL}/categories`,
  promoCodes: `${API_BASE_URL}/promo-codes`,
  validatePromoCode: `${API_BASE_URL}/validate-promo-code`,
};

// Debug logging for API configuration
export const logApiConfig = () => {
  console.log('🔧 API Configuration:');
  console.log('   Environment:', isDevelopment ? 'Development' : 'Production');
  console.log('   API Base URL:', API_BASE_URL);
  console.log('   VITE_SHOP_API_BASE_URL:', _env.VITE_SHOP_API_BASE_URL);
};

// Helper function to make API requests with proper error handling
export const apiRequest = async (url: string, options: RequestInit = {}) => {
  try {
    console.log(`🌐 API Request: ${options.method || 'GET'} ${url}`);
    
    const response = await fetch(url, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
    });

    console.log(`📡 API Response: ${response.status} ${response.statusText}`);

    if (!response.ok) {
      const errorText = await response.text();
      console.error(`❌ API Error: ${response.status} - ${errorText}`);
      throw new Error(`API Error: ${response.status} - ${errorText}`);
    }

    const data = await response.json();
    console.log('✅ API Success:', data);
    return data;

  } catch (error) {
    console.error('❌ Network Error:', error);
    throw error;
  }
};