import Layout from '../components/layout/Layout';
import ProductGrid from '../components/shop/ProductGrid';
import { useLocation } from 'react-router-dom';
import PageTransition from '../components/ui/PageTransition';
import { motion } from 'framer-motion';
import { useState, useEffect } from 'react';
import { apiService, convertApiProduct } from '../services/api';

export default function Search() {
  const { search } = useLocation();
  const params = new URLSearchParams(search);
  const q = params.get('q') || '';
  
  const [results, setResults] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const performSearch = async () => {
      if (!q.trim()) {
        setResults([]);
        setLoading(false);
        return;
      }

      try {
        setLoading(true);
        setError(null);

        const response = await apiService.searchProducts(q);
        const convertedProducts = response.results.map(convertApiProduct);
        setResults(convertedProducts);
      } catch (err) {
        console.error('Search failed:', err);
        setError('Search failed. Please try again.');
        setResults([]);
      } finally {
        setLoading(false);
      }
    };

    performSearch();
  }, [q]);

  return (
    <Layout>
      <PageTransition>
        <motion.section 
          className="container mx-auto px-4 py-10"
          initial={{ opacity: 0, y: 15 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3 }}
        >
          <motion.h1 
            className="text-2xl font-bold"
            initial={{ opacity: 0, x: -10 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.2, delay: 0.05 }}
          >
            Search
          </motion.h1>
          
          <motion.p 
            className="mt-1 text-sm text-muted-foreground"
            initial={{ opacity: 0, x: -10 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.2, delay: 0.1 }}
          >
            {q ? `Results for "${q}"` : 'Enter a search term'} 
            {!loading && q && ` — ${results.length} found`}
          </motion.p>
          
          <motion.div 
            className="mt-6"
            initial={{ opacity: 0, y: 15 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.25, delay: 0.15 }}
          >
            {loading ? (
              <div className="flex justify-center items-center py-16">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-gray-900"></div>
                <span className="ml-3 text-gray-600">Searching...</span>
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
            ) : !q.trim() ? (
              <div className="text-center py-16">
                <p className="text-gray-600">Enter a search term to find products</p>
              </div>
            ) : results.length === 0 ? (
              <div className="text-center py-16">
                <p className="text-gray-600 mb-4">No products found for "{q}"</p>
                <p className="text-sm text-gray-500">Try different keywords or browse our categories</p>
              </div>
            ) : (
              <ProductGrid products={results} />
            )}
          </motion.div>
        </motion.section>
      </PageTransition>
    </Layout>
  );
}