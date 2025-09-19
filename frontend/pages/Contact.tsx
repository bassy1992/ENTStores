import Layout from '../components/layout/Layout';
import PageTransition from '../components/ui/PageTransition';
import { motion } from 'framer-motion';

export default function Contact() {
  return (
    <Layout>
      <PageTransition>
        <motion.section 
          className="container mx-auto px-4 py-10 grid gap-12 md:grid-cols-2"
          initial={{ opacity: 0, y: 15 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3 }}
        >
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.3, delay: 0.1 }}
          >
            <h1 className="text-3xl font-bold">Contact us</h1>
            <p className="mt-2 text-muted-foreground">We're here to help with orders, returns, sizing, and product questions.</p>
            <div className="mt-8 space-y-6">
              <motion.div
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.2, delay: 0.2 }}
              >
                <h2 className="font-semibold">FAQs</h2>
                <ul className="mt-3 space-y-2 text-sm text-muted-foreground">
                  <li>• Shipping times: 3–5 business days in the US.</li>
                  <li>• Returns: 30‑day hassle-free returns on unworn items.</li>
                  <li>• Exchanges: Start an exchange from your order email.</li>
                </ul>
              </motion.div>
              <motion.div 
                id="help"
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.2, delay: 0.25 }}
              >
                <h2 className="font-semibold">Returns & warranty</h2>
                <p className="mt-2 text-sm text-muted-foreground">Contact us within 30 days for returns. All products include a 1‑year limited warranty against defects.</p>
              </motion.div>
            </div>
          </motion.div>
          
          <motion.form 
            className="grid gap-4"
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.3, delay: 0.15 }}
          >
            <motion.div 
              className="grid gap-2"
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.2, delay: 0.2 }}
            >
              <label>Name</label>
              <input className="rounded-md border px-3 py-2 transition-all duration-150 focus:ring-2 focus:ring-blue-500 focus:border-transparent" />
            </motion.div>
            
            <motion.div 
              className="grid gap-2"
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.2, delay: 0.25 }}
            >
              <label>Email</label>
              <input className="rounded-md border px-3 py-2 transition-all duration-150 focus:ring-2 focus:ring-blue-500 focus:border-transparent" type="email" />
            </motion.div>
            
            <motion.div 
              className="grid gap-2"
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.2, delay: 0.3 }}
            >
              <label>Message</label>
              <textarea className="rounded-md border px-3 py-2 min-h-[120px] transition-all duration-150 focus:ring-2 focus:ring-blue-500 focus:border-transparent"></textarea>
            </motion.div>
            
            <motion.button 
              className="rounded-md bg-[hsl(var(--brand-blue))] text-white px-6 py-3 font-medium hover:scale-105 transition-transform duration-150"
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.2, delay: 0.35 }}
            >
              Send message
            </motion.button>
          </motion.form>
        </motion.section>
      </PageTransition>
    </Layout>
  );
}
