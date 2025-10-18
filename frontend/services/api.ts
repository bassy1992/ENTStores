import { CategoryModel, Category } from '../data/products';

// API configuration
// Use explicit VITE_SHOP_API_BASE_URL when provided. During local development
// use relative URLs to leverage Vite proxy. In production use the full URL.
const _env = (import.meta as any).env;
const API_BASE_URL = _env.VITE_SHOP_API_BASE_URL || (_env.DEV ? '/api/shop' : 'https://entstores-production.up.railway.app/api/shop');

// Helper function to process image URLs for development and production
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
  
  // In production, if we get a relative URL, convert to full production URL
  if (!_env.DEV && imageUrl.startsWith('/media/')) {
    return `https://entstores-production.up.railway.app${imageUrl}`;
  }
  
  // If it's already a full URL, return as is
  if (imageUrl.startsWith('http://') || imageUrl.startsWith('https://')) {
    return imageUrl;
  }
  
  // Fallback: assume it's a relative path and prepend production URL
  if (!_env.DEV) {
    return `https://entstores-production.up.railway.app/media/${imageUrl}`;
  }
  
  return imageUrl;
}

// Types for API responses
export interface ApiProductImage {
  id: number;
  image: string;
  alt_text: string;
  is_primary: boolean;
  order: number;
}

export interface ApiProductSize {
  id: number;
  name: string;
  display_name: string;
  order: number;
}

export interface ApiProductColor {
  id: number;
  name: string;
  hex_code: string;
  order: number;
}

export interface ApiProductVariant {
  id: number;
  size: ApiProductSize;
  color: ApiProductColor;
  stock_quantity: number;
  price_adjustment: number;
  final_price: number;
  final_price_display: string;
  is_available: boolean;
  is_in_stock: boolean;
}

export interface ApiProduct {
  id: string;
  title: string;
  slug: string;
  price: number;
  price_display: string;
  shipping_cost: number;
  description: string;
  image: string;
  images: ApiProductImage[];
  category: string;
  category_label: string;
  stock_quantity: number;
  is_active: boolean;
  is_in_stock: boolean;
  tags: string[];
  variants: ApiProductVariant[];
  available_sizes: ApiProductSize[];
  available_colors: ApiProductColor[];
  created_at: string;
  average_rating?: number;
  total_reviews?: number;
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

    // Add cache busting timestamp
    searchParams.append('_t', Date.now().toString());
    
    const response = await fetch(`${API_BASE_URL}/products/?${searchParams}`, {
      headers: {
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache'
      }
    });
    if (!response.ok) {
      throw new Error(`Failed to fetch products: ${response.statusText}`);
    }
    const data = await response.json();
    
    // Process image URLs for development
    if (data.results) {
      data.results = data.results.map((product: ApiProduct) => ({
        ...product,
        image: processImageUrl(product.image),
        images: product.images?.map(img => ({
          ...img,
          image: processImageUrl(img.image)
        })) || []
      }));
    }
    
    return data;
  },

  async getFeaturedProducts(): Promise<ApiResponse<ApiProduct>> {
    // Add cache busting timestamp
    const timestamp = Date.now();
    const response = await fetch(`${API_BASE_URL}/products/featured/?_t=${timestamp}`, {
      headers: {
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache'
      }
    });
    if (!response.ok) {
      throw new Error(`Failed to fetch featured products: ${response.statusText}`);
    }
    const data = await response.json();
    
    // Process image URLs for development
    if (data.results) {
      data.results = data.results.map((product: ApiProduct) => ({
        ...product,
        image: processImageUrl(product.image),
        images: product.images?.map(img => ({
          ...img,
          image: processImageUrl(img.image)
        })) || []
      }));
    }
    
    return data;
  },

  async getProduct(slug: string): Promise<ApiProduct> {
    // Add cache busting timestamp
    const timestamp = Date.now();
    const response = await fetch(`${API_BASE_URL}/products/${slug}/?_t=${timestamp}`, {
      headers: {
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache'
      }
    });
    if (!response.ok) {
      throw new Error(`Failed to fetch product: ${response.statusText}`);
    }
    const product = await response.json();
    
    // Process image URLs for development
    return {
      ...product,
      image: processImageUrl(product.image),
      images: product.images?.map(img => ({
        ...img,
        image: processImageUrl(img.image)
      })) || []
    };
  },

  async searchProducts(query: string): Promise<SearchResponse> {
    // Add cache busting timestamp
    const timestamp = Date.now();
    const response = await fetch(`${API_BASE_URL}/search/?q=${encodeURIComponent(query)}&_t=${timestamp}`, {
      headers: {
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache'
      }
    });
    if (!response.ok) {
      throw new Error(`Failed to search products: ${response.statusText}`);
    }
    const data = await response.json();
    
    // Process image URLs for development
    if (data.results) {
      data.results = data.results.map((product: ApiProduct) => ({
        ...product,
        image: processImageUrl(product.image),
        images: product.images?.map(img => ({
          ...img,
          image: processImageUrl(img.image)
        })) || []
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
  },

  // Stock validation
  async validateStock(items: Array<{
    product_id: string;
    quantity: number;
    variant_id?: number;
  }>): Promise<{
    valid: boolean;
    errors: Array<{
      product_id: string;
      product_title?: string;
      variant_id?: number;
      error: string;
      available_quantity?: number;
    }>;
    warnings: Array<{
      product_id: string;
      product_title?: string;
      variant_id?: number;
      warning: string;
    }>;
    message: string;
  }> {
    const response = await fetch(`${API_BASE_URL}/validate-stock/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ items }),
    });
    
    if (!response.ok) {
      throw new Error(`Failed to validate stock: ${response.statusText}`);
    }
    
    return response.json();
  },

  // Promo code validation
  async validatePromoCode(code: string, subtotal: number): Promise<{
    valid: boolean;
    code?: string;
    description?: string;
    discount_type?: string;
    discount_amount?: number;
    discount_display?: string;
    free_shipping?: boolean;
    message?: string;
    errors?: any;
    error?: string;
  }> {
    const response = await fetch(`${API_BASE_URL}/validate-promo-code/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ 
        code: code.trim().toUpperCase(), 
        subtotal: subtotal / 100 // Convert cents to dollars
      }),
    });
    
    if (!response.ok) {
      const errorData = await response.json();
      return {
        valid: false,
        error: errorData.error || 'Failed to validate promo code',
        errors: errorData.errors
      };
    }
    
    return response.json();
  },

  // Get available promo codes (for promotional display)
  async getPromoCodes(): Promise<Array<{
    code: string;
    description: string;
    discount_display: string;
    minimum_order_amount: number;
  }>> {
    const response = await fetch(`${API_BASE_URL}/promo-codes/`);
    if (!response.ok) {
      throw new Error(`Failed to fetch promo codes: ${response.statusText}`);
    }
    const data = await response.json();
    return data.results || data;
  },

  // Reviews
  async getProductReviews(productId: string, params?: {
    page?: number;
    sort?: 'newest' | 'oldest' | 'highest' | 'lowest' | 'helpful';
    rating?: number;
  }): Promise<{
    reviews: Array<{
      id: string;
      user_name: string;
      user_email?: string;
      rating: number;
      title: string;
      comment: string;
      created_at: string;
      verified_purchase: boolean;
      helpful_count: number;
      not_helpful_count: number;
      user_found_helpful?: boolean | null;
      images?: string[];
      size_purchased?: string;
      color_purchased?: string;
    }>;
    stats: {
      average_rating: number;
      total_reviews: number;
      rating_distribution: {
        5: number;
        4: number;
        3: number;
        2: number;
        1: number;
      };
    };
    pagination: {
      page: number;
      total_pages: number;
      has_next: boolean;
      has_previous: boolean;
    };
  }> {
    const searchParams = new URLSearchParams();
    
    if (params?.page) searchParams.append('page', params.page.toString());
    if (params?.sort) searchParams.append('sort', params.sort);
    if (params?.rating) searchParams.append('rating', params.rating.toString());

    const response = await fetch(`${API_BASE_URL}/products/${productId}/reviews/?${searchParams}`);
    if (!response.ok) {
      throw new Error(`Failed to fetch reviews: ${response.statusText}`);
    }
    return response.json();
  },

  async submitReview(productId: string, review: {
    rating: number;
    title: string;
    comment: string;
    user_name: string;
    user_email?: string;
    size_purchased?: string;
    color_purchased?: string;
  }): Promise<{
    success: boolean;
    message: string;
    review_id?: string;
    errors?: any;
  }> {
    const response = await fetch(`${API_BASE_URL}/products/${productId}/reviews/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(review),
    });
    
    const data = await response.json();
    
    if (!response.ok) {
      return {
        success: false,
        message: data.message || 'Failed to submit review',
        errors: data.errors
      };
    }
    
    return {
      success: true,
      message: data.message || 'Review submitted successfully',
      review_id: data.review_id
    };
  },

  async voteOnReview(reviewId: string, helpful: boolean): Promise<{
    success: boolean;
    helpful_count: number;
    not_helpful_count: number;
  }> {
    const response = await fetch(`${API_BASE_URL}/reviews/${reviewId}/vote/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ helpful }),
    });
    
    if (!response.ok) {
      throw new Error(`Failed to vote on review: ${response.statusText}`);
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
    shipping_cost: apiProduct.shipping_cost,
    description: apiProduct.description,
    image: apiProduct.image,
    images: apiProduct.images || [],
    category: apiProduct.category,
    tags: apiProduct.tags,
    stock_quantity: apiProduct.stock_quantity,
    is_in_stock: apiProduct.is_in_stock,
    variants: apiProduct.variants || [],
    available_sizes: apiProduct.available_sizes || [],
    available_colors: apiProduct.available_colors || [],
    average_rating: (apiProduct as any).average_rating || 0,
    total_reviews: (apiProduct as any).total_reviews || 0,
  };
}

// Helper function to convert API category to frontend category format
export function convertApiCategory(apiCategory: ApiCategory): CategoryModel {
  return {
    key: apiCategory.key as Category,
    label: apiCategory.label,
    description: apiCategory.description,
    image: apiCategory.image,
    featured: apiCategory.featured,
    productCount: apiCategory.product_count,
  };
}