// API configuration
// Use explicit VITE_SHOP_API_BASE_URL when provided. During local development
// use relative URLs to leverage Vite proxy. In production use the full URL.
const _env = (import.meta as any).env;
const API_BASE_URL = _env.VITE_SHOP_API_BASE_URL || (_env.DEV ? '/api/shop' : 'https://enontino-production.up.railway.app/api/shop');

// Helper function to process image URLs for development
function processImageUrl(imageUrl: string): string {
  if (!imageUrl) return '';
  
  // In development, if we get a full URL from the backend, convert to relative URL for proxy
  if (_env.DEV && imageUrl.startsWith('http://localhost:8000/media/')) {
    return imageUrl.replace('http://localhost:8000', '');
  }
  
  // In development, if we get a relative URL, keep it as is for proxy
  if (_env.DEV && imageUrl.startsWith('/media/')) {
    return imageUrl;
  }
  
  return imageUrl;
}

// Types for API responses
export interface ApiProduct {
  id: string;
  title: string;
  slug: string;
  price: number;
  price_display: string;
  description: string;
  image: string;
  category: string;
  category_label: string;
  stock_quantity: number;
  is_active: boolean;
  is_in_stock: boolean;
  tags: string[];
  created_at: string;
}

export interface ApiCategory {
  key: string;
  label: string;
  description: string;
  image: string;
  featured: boolean;
  product_count: number;
}

export interface ApiResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

export interface SearchResponse {
  results: ApiProduct[];
  count: number;
  query: string;
}

// API service functions
export const apiService = {
  // Products
  async getProducts(params?: {
    category?: string;
    tags?: string;
    search?: string;
    in_stock?: boolean;
    page?: number;
  }): Promise<ApiResponse<ApiProduct>> {
    const searchParams = new URLSearchParams();
    
    if (params?.category) searchParams.append('category', params.category);
    if (params?.tags) searchParams.append('tags', params.tags);
    if (params?.search) searchParams.append('search', params.search);
    if (params?.in_stock) searchParams.append('in_stock', 'true');
    if (params?.page) searchParams.append('page', params.page.toString());

    const response = await fetch(`${API_BASE_URL}/products/?${searchParams}`);
    if (!response.ok) {
      throw new Error(`Failed to fetch products: ${response.statusText}`);
    }
    const data = await response.json();
    
    // Process image URLs for development
    if (data.results) {
      data.results = data.results.map((product: ApiProduct) => ({
        ...product,
        image: processImageUrl(product.image)
      }));
    }
    
    return data;
  },

  async getFeaturedProducts(): Promise<ApiResponse<ApiProduct>> {
    const response = await fetch(`${API_BASE_URL}/products/featured/`);
    if (!response.ok) {
      throw new Error(`Failed to fetch featured products: ${response.statusText}`);
    }
    const data = await response.json();
    
    // Process image URLs for development
    if (data.results) {
      data.results = data.results.map((product: ApiProduct) => ({
        ...product,
        image: processImageUrl(product.image)
      }));
    }
    
    return data;
  },

  async getProduct(slug: string): Promise<ApiProduct> {
    const response = await fetch(`${API_BASE_URL}/products/${slug}/`);
    if (!response.ok) {
      throw new Error(`Failed to fetch product: ${response.statusText}`);
    }
    const product = await response.json();
    
    // Process image URL for development
    return {
      ...product,
      image: processImageUrl(product.image)
    };
  },

  async searchProducts(query: string): Promise<SearchResponse> {
    const response = await fetch(`${API_BASE_URL}/search/?q=${encodeURIComponent(query)}`);
    if (!response.ok) {
      throw new Error(`Failed to search products: ${response.statusText}`);
    }
    const data = await response.json();
    
    // Process image URLs for development
    if (data.results) {
      data.results = data.results.map((product: ApiProduct) => ({
        ...product,
        image: processImageUrl(product.image)
      }));
    }
    
    return data;
  },

  // Categories
  async getCategories(): Promise<ApiCategory[]> {
    const response = await fetch(`${API_BASE_URL}/categories/`);
    if (!response.ok) {
      throw new Error(`Failed to fetch categories: ${response.statusText}`);
    }
    const data = await response.json();
    
    let categories: ApiCategory[] = [];
    
    // Handle paginated response
    if (data.results && Array.isArray(data.results)) {
      categories = data.results;
    }
    // Handle direct array response (fallback)
    else if (Array.isArray(data)) {
      categories = data;
    }
    else {
      throw new Error('Invalid response format from categories API');
    }
    
    // Process image URLs for development
    return categories.map(category => ({
      ...category,
      image: processImageUrl(category.image)
    }));
  },

  async getFeaturedCategories(): Promise<ApiCategory[]> {
    const response = await fetch(`${API_BASE_URL}/categories/featured/`);
    if (!response.ok) {
      throw new Error(`Failed to fetch featured categories: ${response.statusText}`);
    }
    const data = await response.json();
    
    let categories: ApiCategory[] = [];
    
    // Handle paginated response
    if (data.results && Array.isArray(data.results)) {
      categories = data.results;
    }
    // Handle direct array response (fallback)
    else if (Array.isArray(data)) {
      categories = data;
    }
    else {
      throw new Error('Invalid response format from featured categories API');
    }
    
    // Process image URLs for development
    return categories.map(category => ({
      ...category,
      image: processImageUrl(category.image)
    }));
  },

  // Shop stats
  async getShopStats(): Promise<{
    total_products: number;
    total_categories: number;
    featured_products: number;
    categories: ApiCategory[];
  }> {
    const response = await fetch(`${API_BASE_URL}/stats/`);
    if (!response.ok) {
      throw new Error(`Failed to fetch shop stats: ${response.statusText}`);
    }
    return response.json();
  }
};

// Helper function to convert API product to frontend product format
export function convertApiProduct(apiProduct: ApiProduct): any {
  return {
    id: apiProduct.id,
    title: apiProduct.title,
    slug: apiProduct.slug,
    price: apiProduct.price,
    description: apiProduct.description,
    image: apiProduct.image,
    category: apiProduct.category,
    tags: apiProduct.tags,
  };
}

// Helper function to convert API category to frontend category format
export function convertApiCategory(apiCategory: ApiCategory): any {
  return {
    key: apiCategory.key,
    label: apiCategory.label,
  };
}