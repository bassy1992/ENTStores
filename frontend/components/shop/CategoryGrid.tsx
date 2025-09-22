import { Link } from 'react-router-dom';
import { CategoryModel } from '../../data/products';
import { ArrowRight, Package } from 'lucide-react';
import { useState, useEffect } from 'react';
import { apiService, convertApiCategory } from '../../services/api';

interface CategoryGridProps {
  showFeaturedOnly?: boolean;
  limit?: number;
}

export default function CategoryGrid({ showFeaturedOnly = false, limit }: CategoryGridProps) {
  const [categories, setCategories] = useState<CategoryModel[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchCategories = async () => {
      try {
        setLoading(true);
        let apiCategories;
        
        if (showFeaturedOnly) {
          apiCategories = await apiService.getFeaturedCategories();
        } else {
          apiCategories = await apiService.getCategories();
        }
        
        let convertedCategories = apiCategories.map(convertApiCategory);
        
        if (limit) {
          convertedCategories = convertedCategories.slice(0, limit);
        }
        
        setCategories(convertedCategories);
        setError(null);
      } catch (err) {
        console.error('Failed to fetch categories:', err);
        setError('Failed to load categories');
        setCategories([]);
      } finally {
        setLoading(false);
      }
    };

    fetchCategories();
  }, [showFeaturedOnly, limit]);

  if (loading) {
    return (
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
        {[...Array(showFeaturedOnly ? 4 : 8)].map((_, i) => (
          <div key={i} className="animate-pulse">
            <div className="aspect-[4/3] bg-gray-200 rounded-2xl mb-4"></div>
            <div className="p-5">
              <div className="bg-gray-200 h-6 rounded mb-2"></div>
              <div className="bg-gray-200 h-4 rounded mb-2"></div>
              <div className="bg-gray-200 h-4 rounded w-2/3"></div>
            </div>
          </div>
        ))}
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center py-8">
        <p className="text-gray-500">{error}</p>
        <button 
          onClick={() => window.location.reload()} 
          className="mt-2 text-blue-600 hover:text-blue-700"
        >
          Try again
        </button>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
      {categories.map((category) => (
        <CategoryCard key={category.key} category={category} />
      ))}
    </div>
  );
}

function CategoryCard({ category }: { category: CategoryModel }) {
  return (
    <Link 
      to={`/shop?c=${encodeURIComponent(category.key)}`}
      className="group relative overflow-hidden rounded-2xl bg-white border border-gray-200 hover:border-gray-300 transition-all duration-300 hover:shadow-lg"
    >
      {/* Image Container */}
      <div className="aspect-[4/3] overflow-hidden bg-gray-100">
        <img 
          src={category.image} 
          alt={category.label}
          className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
        />
        
        {/* Overlay */}
        <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-black/20 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
        
        {/* Featured Badge */}
        {category.featured && (
          <div className="absolute top-3 left-3">
            <span className="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800 border border-blue-200">
              ⭐ Featured
            </span>
          </div>
        )}
        
        {/* Product Count */}
        <div className="absolute top-3 right-3">
          <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-xs font-medium bg-white/90 text-gray-700 backdrop-blur-sm">
            <Package className="w-3 h-3" />
            {category.productCount}
          </span>
        </div>
      </div>

      {/* Content */}
      <div className="p-5">
        <div className="flex items-center justify-between mb-2">
          <h3 className="text-lg font-semibold text-gray-900 group-hover:text-blue-600 transition-colors">
            {category.label}
          </h3>
          <ArrowRight className="w-4 h-4 text-gray-400 group-hover:text-blue-600 group-hover:translate-x-1 transition-all duration-200" />
        </div>
        
        <p className="text-sm text-gray-600 leading-relaxed">
          {category.description}
        </p>
        
        {/* Shop Now Button */}
        <div className="mt-4 pt-3 border-t border-gray-100">
          <span className="text-sm font-medium text-blue-600 group-hover:text-blue-700">
            Shop {category.label} →
          </span>
        </div>
      </div>
    </Link>
  );
}

// Alternative compact version for smaller spaces
export function CategoryGridCompact({ limit = 6 }: { limit?: number }) {
  const [categories, setCategories] = useState<CategoryModel[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchCategories = async () => {
      try {
        setLoading(true);
        const apiCategories = await apiService.getCategories();
        const convertedCategories = apiCategories.map(convertApiCategory).slice(0, limit);
        setCategories(convertedCategories);
      } catch (err) {
        console.error('Failed to fetch categories:', err);
        setCategories([]);
      } finally {
        setLoading(false);
      }
    };

    fetchCategories();
  }, [limit]);

  if (loading) {
    return (
      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-4">
        {[...Array(limit)].map((_, i) => (
          <div key={i} className="animate-pulse flex flex-col items-center p-4">
            <div className="w-16 h-16 bg-gray-200 rounded-full mb-3"></div>
            <div className="bg-gray-200 h-4 rounded w-16 mb-1"></div>
            <div className="bg-gray-200 h-3 rounded w-12"></div>
          </div>
        ))}
      </div>
    );
  }

  return (
    <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-4">
      {categories.map((category) => (
        <Link
          key={category.key}
          to={`/shop?c=${encodeURIComponent(category.key)}`}
          className="group flex flex-col items-center p-4 rounded-xl border border-gray-200 hover:border-blue-300 hover:bg-blue-50/50 transition-all duration-200"
        >
          <div className="w-16 h-16 rounded-full overflow-hidden mb-3 ring-2 ring-gray-100 group-hover:ring-blue-200 transition-all">
            <img 
              src={category.image} 
              alt={category.label}
              className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-300"
            />
          </div>
          <span className="text-sm font-medium text-center text-gray-700 group-hover:text-blue-600 transition-colors">
            {category.label}
          </span>
          <span className="text-xs text-gray-500 mt-1">
            {category.productCount} items
          </span>
        </Link>
      ))}
    </div>
  );
}