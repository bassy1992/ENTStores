import Layout from '../components/layout/Layout';
import ProductGrid from '../components/shop/ProductGrid';
import CategoryPills from '../components/shop/CategoryPills';
import CategoryGrid, { CategoryGridCompact } from '../components/shop/CategoryGrid';
import CategoryStats from '../components/shop/CategoryStats';
import { Link } from 'react-router-dom';
import TypographicHero from '../components/ui/TypographicHero';
import PageTransition from '../components/ui/PageTransition';
import { motion } from 'framer-motion';
import { useState, useEffect } from 'react';
import { apiService, convertApiProduct } from '../services/api';

export default function Home() {
  const [featured, setFeatured] = useState<any[]>([]);
  const [loadingFeatured, setLoadingFeatured] = useState(true);

  useEffect(() => {
    const fetchFeaturedProducts = async () => {
      try {
        const response = await apiService.getFeaturedProducts();
        const convertedProducts = response.results.map(convertApiProduct).slice(0, 4);
        setFeatured(convertedProducts);
      } catch (err) {
        console.error('Failed to fetch featured products:', err);
        setFeatured([]);
      } finally {
        setLoadingFeatured(false);
      }
    };

    fetchFeaturedProducts();
  }, []);

  const sliderImages = [
    'https://tailsandtrailsmedia.sfo3.cdn.digitaloceanspaces.com/ENNC/IMG_1173.jpg',
    'https://cdn.builder.io/api/v1/image/assets%2F261a98e6df434ad1ad15c1896e5c6aa3%2F7e980c238ab54fb5893ffdd1999f2c37?format=webp&width=1200',
    'https://cdn.builder.io/api/v1/image/assets%2F261a98e6df434ad1ad15c1896e5c6aa3%2Fa03929e1731e4efcadc34cef66af98ba?format=webp&width=1200',
  ];

  return (
    <Layout>
      <PageTransition>
        <motion.section
          initial={{ opacity: 0, scale: 0.98 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.3, ease: "easeOut" }}
        >
          <TypographicHero images={sliderImages} />
        </motion.section>

        <motion.section 
          id="categories" 
          className="container mx-auto px-4 py-12"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3, delay: 0.1 }}
        >
          <div className="flex items-center justify-between mb-8">
            <div>
              <h2 className="text-3xl font-bold text-gray-900">Shop by Category</h2>
              <p className="text-gray-600 mt-2">Discover our complete range of premium apparel and accessories</p>
            </div>
            <Link 
              to="/categories" 
              className="hidden sm:flex items-center gap-2 text-sm text-blue-600 hover:text-blue-700 font-medium"
            >
              View all categories
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
              </svg>
            </Link>
          </div>
          
          {/* Featured Categories Grid */}
          <CategoryGrid showFeaturedOnly={true} />
          
          {/* Mobile View All Link */}
          <div className="mt-8 text-center sm:hidden">
            <Link 
              to="/categories" 
              className="inline-flex items-center gap-2 text-sm text-blue-600 hover:text-blue-700 font-medium"
            >
              View all categories
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
              </svg>
            </Link>
          </div>
        </motion.section>

        <motion.section 
          className="container mx-auto px-4 py-12"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3, delay: 0.15 }}
        >
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-semibold">Featured Products</h2>
            <Link to="/shop" className="text-sm text-foreground/70 hover:text-foreground">Browse shop</Link>
          </div>
          {loadingFeatured ? (
            <div className="grid gap-6 grid-cols-2 sm:grid-cols-3 lg:grid-cols-4">
              {[...Array(4)].map((_, i) => (
                <div key={i} className="animate-pulse">
                  <div className="bg-gray-200 aspect-square rounded-lg mb-3"></div>
                  <div className="bg-gray-200 h-4 rounded mb-2"></div>
                  <div className="bg-gray-200 h-4 rounded w-2/3"></div>
                </div>
              ))}
            </div>
          ) : (
            <ProductGrid products={featured} />
          )}
        </motion.section>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3, delay: 0.2 }}
        >
          <CategoryStats />
        </motion.div>

        <motion.section 
          className="container mx-auto px-4 py-16"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3, delay: 0.25 }}
        >
          <div className="rounded-2xl bg-gradient-to-r from-[hsl(var(--brand-red))] to-[hsl(var(--brand-blue))] p-10 text-white grid gap-6 md:grid-cols-2 items-center">
            <div>
              <h3 className="text-2xl font-bold">Free shipping over $75</h3>
              <p className="mt-2 opacity-90">Fast dispatch and easy 30‑day returns on all orders. Shop with confidence.</p>
            </div>
            <div className="flex gap-3 md:justify-end">
              <Link to="/contact" className="rounded-md bg-white/15 hover:bg-white/25 px-5 py-3 font-medium">Contact support</Link>
              <Link to="/shop" className="rounded-md bg-white text-black px-5 py-3 font-medium">Start shopping</Link>
            </div>
          </div>
        </motion.section>
      </PageTransition>
    </Layout>
  );
}
