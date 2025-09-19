import Layout from '../components/layout/Layout';
import ProductGrid from '../components/shop/ProductGrid';
import { products } from '../data/products';
import { useLocation } from 'react-router-dom';
import PageTransition from '../components/ui/PageTransition';
import { motion } from 'framer-motion';

export default function Search() {
  const { search } = useLocation();
  const params = new URLSearchParams(search);
  const q = (params.get('q') || '').toLowerCase();
  const results = products.filter(
    (p) => p.title.toLowerCase().includes(q) || p.description.toLowerCase().includes(q),
  );

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
            Results for "{q}" — {results.length} found
          </motion.p>
          
          <motion.div 
            className="mt-6"
            initial={{ opacity: 0, y: 15 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.25, delay: 0.15 }}
          >
            <ProductGrid products={results} />
          </motion.div>
        </motion.section>
      </PageTransition>
    </Layout>
  );
}