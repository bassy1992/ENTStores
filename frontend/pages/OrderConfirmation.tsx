import Layout from '../components/layout/Layout';
import { useLocation, Link } from 'react-router-dom';
import { formatPrice } from '../data/products';
import PageTransition from '../components/ui/PageTransition';
import { motion } from 'framer-motion';

type Summary = {
  id: string;
  total: number;
  items: { id: string; title: string; price: number; quantity: number }[];
};

export default function OrderConfirmation() {
  const { state } = useLocation();
  const s = (state || {}) as Summary;

  return (
    <Layout>
      <PageTransition>
        <motion.section 
          className="container mx-auto px-4 py-16 max-w-2xl text-center"
          initial={{ opacity: 0, y: 15 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3 }}
        >
          <motion.div 
            className="mx-auto h-16 w-16 rounded-full bg-[hsl(var(--brand-blue))] text-white grid place-items-center text-3xl"
            initial={{ opacity: 0, scale: 0 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.4, delay: 0.1, type: "spring", stiffness: 300 }}
          >
            ✓
          </motion.div>
          
          <motion.h1 
            className="mt-6 text-3xl font-bold"
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.25, delay: 0.2 }}
          >
            Thank you for your purchase!
          </motion.h1>
          
          <motion.p 
            className="mt-2 text-muted-foreground"
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.25, delay: 0.25 }}
          >
            Your order {s.id ? `#${s.id}` : ''} has been received.
          </motion.p>
          
          <motion.div 
            className="mt-8 rounded-xl border p-6 text-left"
            initial={{ opacity: 0, y: 15 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3, delay: 0.3 }}
          >
            <h2 className="font-semibold">Order summary</h2>
            <ul className="mt-4 space-y-2 text-sm">
              {s.items?.map((i, index) => (
                <motion.li 
                  key={i.id} 
                  className="flex justify-between"
                  initial={{ opacity: 0, x: -10 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ duration: 0.2, delay: 0.35 + index * 0.05 }}
                >
                  <span>
                    {i.title} × {i.quantity}
                  </span>
                  <span>{formatPrice(i.price * i.quantity)}</span>
                </motion.li>
              ))}
            </ul>
            <motion.div 
              className="flex justify-between font-semibold text-lg pt-4 border-t mt-4"
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.25, delay: 0.45 }}
            >
              <span>Total</span>
              <span>{formatPrice(s.total || 0)}</span>
            </motion.div>
          </motion.div>
          
          <motion.div 
            className="mt-8 flex justify-center gap-3"
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.25, delay: 0.5 }}
          >
            <Link to="/shop" className="rounded-md border px-5 py-3 hover:bg-gray-50 transition-colors duration-150">Continue shopping</Link>
            <Link to="/contact" className="rounded-md bg-foreground text-background px-5 py-3 hover:scale-105 transition-transform duration-150">Get support</Link>
          </motion.div>
        </motion.section>
      </PageTransition>
    </Layout>
  );
}
