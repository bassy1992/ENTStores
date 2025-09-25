import Layout from '../components/layout/Layout';
import ProductGrid from '../components/shop/ProductGrid';
import CategoryPills from '../components/shop/CategoryPills';
import { useLocation } from 'react-router-dom';
import PageTransition from '../components/ui/PageTransition';
import { motion } from 'framer-motion';
import { useState, useEffect } from 'react';
import { apiService, convertApiProduct } from '../services/api';
import { useNavigate } from 'react-router-dom';

export default function Shop() {
  const { search } = useLocation();
  const params = new URLSearchParams(search);
  const category = params.get('c') || params.get('category');
  const searchQuery = params.get('search') || params.get('q');

  const [products, setProducts] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [localSearch, setLocalSearch] = useState(searchQuery || '');
  const navigate = useNavigate();

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        setLoading(true);
        setError(null);

        let response;
        
        if (searchQuery) {
          // If there's a search query, use search API
          response = await apiService.searchProducts(searchQuery);
        } else {
          // Otherwise, get products with optional category filter
          response = await apiService.getProducts({
            category: category || undefined,
          });
        }

        const convertedProducts = response.results.map(convertApiProduct);
        setProducts(convertedProducts);
      } catch (err) {
        console.error('Failed to fetch products:', err);
        setError('Failed to load products. Please try again.');
      } finally {
        setLoading(false);
      }
    };

    fetchProducts();
  }, [category, searchQuery]);

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    const query = localSearch.trim();
    if (query) {
      navigate(`/shop?search=${encodeURIComponent(query)}`);
    } else {
      navigate('/shop');
    }
  };

  return (
    <Layout>
      <PageTransition>
        <div className="container mx-auto px-4 py-8">
          <motion.div
            className="flex items-center justify-between mb-8"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4 }}
          >
            <h1 className="text-3xl font-bold text-gray-900">
              {searchQuery ? `Search Results` : 'Shop'}
            </h1>
            <div className="text-gray-600">
              {!loading && (
                <span>{products.length} products</span>
              )}
            </div>
          </motion.div>

          {/* Search Bar */}
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3, delay: 0.1 }}
            className="mb-6"
          >
            <form onSubmit={handleSearch} className="max-w-md">
              <div className="relative">
                <svg className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
                <input
                  type="text"
                  value={localSearch}
                  onChange={(e) => setLocalSearch(e.target.value)}
                  placeholder="Search products..."
                  className="w-full pl-10 pr-4 py-2.5 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
                {localSearch && (
                  <button
                    type="button"
                    onClick={() => {
                      setLocalSearch('');
                      navigate('/shop');
                    }}
                    className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600"
                  >
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                    </svg>
                  </button>
                )}
              </div>
            </form>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3, delay: 0.15 }}
            className="mb-8"
          >
            <CategoryPills />
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4, delay: 0.2 }}
          >
            {loading ? (
              <div className="flex justify-center items-center py-16">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-gray-900"></div>
                <span className="ml-3 text-gray-600">Loading products...</span>
              </div>
            ) : error ? (
              <div className="text-center py-16">
                <p className="text-red-600 mb-4">{error}</p>
                <button
                  onClick={() => window.location.reload()}
                  className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                >
                  Try Again
                </button>
              </div>
            ) : products.length === 0 ? (
              <div className="text-center py-16">
                <p className="text-gray-600 mb-4">
                  {searchQuery 
                    ? `No products found for "${searchQuery}"${category ? ` in "${category}" category` : ''}`
                    : `No products found${category ? ` in "${category}" category` : ''}`
                  }
                </p>
                <a href="/shop" className="text-blue-600 hover:underline">
                  {searchQuery || category ? 'View all products' : 'Refresh page'}
                </a>
              </div>
            ) : (
              <ProductGrid products={products} />
            )}
          </motion.div>
        </div>
      </PageTransition>
    </Layout>
  );
}