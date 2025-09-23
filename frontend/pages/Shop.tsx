import Layout from '../components/layout/Layout';
import ProductGrid from '../components/shop/ProductGrid';
import CategoryPills from '../components/shop/CategoryPills';
import { useLocation } from 'react-router-dom';
import PageTransition from '../components/ui/PageTransition';
import { motion } from 'framer-motion';
import { useState, useEffect } from 'react';
import { apiService, convertApiProduct } from '../services/api';

export default function Shop() {
  const { search } = useLocation();
  const params = new URLSearchParams(search);
  const category = params.get('c') || params.get('category');

  const [products, setProducts] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        setLoading(true);
        setError(null);

        const response = await apiService.getProducts({
          category: category || undefined,
        });

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
  }, [category]);

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
            <h1 className="text-3xl font-bold text-gray-900">Shop</h1>
            <div className="text-gray-600">
              {!loading && (
                <span>{products.length} products</span>
              )}
            </div>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3, delay: 0.1 }}
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
                  No products found{category ? ` in "${category}" category` : ''}.
                </p>
                <a href="/shop" className="text-blue-600 hover:underline">
                  View all products
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