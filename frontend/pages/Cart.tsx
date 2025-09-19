import Layout from '../components/layout/Layout';
import { useCart } from '../context/cart';
import { formatPrice, products } from '../data/products';
import { Link, useNavigate } from 'react-router-dom';
import { useState } from 'react';
import PageTransition from '../components/ui/PageTransition';
import { motion } from 'framer-motion';

export default function Cart() {
  const { state, setQty, remove, subtotal, clear } = useCart();
  const navigate = useNavigate();

  const [coupon, setCoupon] = useState('');
  const [appliedCoupon, setAppliedCoupon] = useState<string | null>(null);
  const [couponError, setCouponError] = useState<string | null>(null);

  // simple coupon logic: ENNC10 => 10% off
  const applyCoupon = (code: string) => {
    const c = code.trim().toUpperCase();
    if (c === 'ENNC10') {
      setAppliedCoupon(c);
      setCouponError(null);
      return;
    }
    setCouponError('Invalid code');
    setAppliedCoupon(null);
  };

  const discount = appliedCoupon === 'ENNC10' ? Math.round(subtotal * 0.1) : 0;
  const shipping = subtotal >= 7500 ? 0 : 999; // cents
  const tax = Math.round((subtotal - discount) * 0.07); // simple 7% tax estimate
  const total = Math.max(0, subtotal - discount) + shipping + tax;

  return (
    <Layout>
      <PageTransition>
        <motion.section 
          className="container mx-auto px-4 py-12"
          initial={{ opacity: 0, y: 15 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3 }}
        >
          <div className="grid gap-8 lg:grid-cols-12">
            <main className="lg:col-span-8">
              <motion.div 
                className="flex items-center justify-between mb-6"
                initial={{ opacity: 0, x: -10 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.2, delay: 0.05 }}
              >
                <h1 className="text-2xl font-bold">Your cart</h1>
                <div className="flex items-center gap-3">
                  <Link to="/shop" className="text-sm text-foreground/70 hover:text-foreground">Continue shopping</Link>
                  <button
                    onClick={() => clear()}
                    className="text-sm text-[hsl(var(--brand-red))] hover:underline"
                  >
                    Clear cart
                  </button>
                </div>
              </motion.div>

              {state.items.length === 0 ? (
                <motion.div 
                  className="rounded-xl border p-8 text-center bg-card"
                  initial={{ opacity: 0, scale: 0.95 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ duration: 0.25, delay: 0.1 }}
                >
                  <p className="text-muted-foreground">Your cart is empty.</p>
                  <Link to="/shop" className="mt-4 inline-block rounded-md bg-[hsl(var(--brand-blue))] text-white px-5 py-3 hover:scale-105 transition-transform duration-150">Shop products</Link>
                </motion.div>
              ) : (
                <div className="space-y-6">
                  {state.items.map((item, index) => {
                    const p = products.find((x) => x.id === item.id);
                    return (
                      <motion.div 
                        key={item.id} 
                        className="grid grid-cols-12 gap-4 items-center rounded-lg p-4 border bg-card"
                        initial={{ opacity: 0, y: 10 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.2, delay: 0.05 + index * 0.05 }}
                      >
                      <div className="col-span-3 sm:col-span-2">
                        <Link to={`/product/${p?.slug}`} className="block rounded-md overflow-hidden bg-muted">
                          <img src={item.image} alt={item.title} className="w-full h-24 object-cover" />
                        </Link>
                      </div>

                      <div className="col-span-9 sm:col-span-7">
                        <div className="flex items-start justify-between">
                          <div>
                            <Link to={`/product/${p?.slug}`} className="font-medium hover:underline">{item.title}</Link>
                            <div className="text-sm text-muted-foreground mt-1">{p?.category}</div>
                            <div className="text-sm text-muted-foreground mt-2">Unit: {formatPrice(item.price)}</div>
                          </div>
                          <div className="hidden sm:block font-medium">{formatPrice(item.price * item.quantity)}</div>
                        </div>

                        <div className="mt-4 flex items-center gap-3">
                          <div className="flex items-center border rounded-md overflow-hidden">
                            <button
                              onClick={() => setQty(item.id, Math.max(0, item.quantity - 1))}
                              className="px-3 py-1 text-sm"
                              aria-label={`Decrease quantity of ${item.title}`}
                            >
                              −
                            </button>
                            <input
                              className="w-14 text-center text-sm border-l border-r px-2 py-1"
                              value={item.quantity}
                              onChange={(e) => {
                                const v = Math.max(0, parseInt(e.target.value || '0'));
                                setQty(item.id, v);
                              }}
                            />
                            <button
                              onClick={() => setQty(item.id, item.quantity + 1)}
                              className="px-3 py-1 text-sm"
                              aria-label={`Increase quantity of ${item.title}`}
                            >
                              +
                            </button>
                          </div>

                          <button onClick={() => remove(item.id)} className="text-sm text-[hsl(var(--brand-red))] hover:underline">Remove</button>
                        </div>

                        {/* Mobile price row */}
                        <div className="mt-3 sm:hidden font-medium">{formatPrice(item.price * item.quantity)}</div>
                      </div>
                      </motion.div>
                    );
                  })}
                </div>
              )}
            </main>

            <aside className="lg:col-span-4">
              <motion.div 
                className="lg:sticky lg:top-24 rounded-xl border bg-card p-6"
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.3, delay: 0.15 }}
              >
              <h2 className="font-semibold text-lg">Order summary</h2>

              <div className="mt-4 space-y-3 text-sm">
                <div className="flex justify-between"><span>Subtotal</span><span>{formatPrice(subtotal)}</span></div>
                {discount > 0 && (
                  <div className="flex justify-between text-[hsl(var(--brand-red))]"><span>Discount</span><span>-{formatPrice(discount)}</span></div>
                )}
                <div className="flex justify-between"><span>Shipping</span><span>{shipping === 0 ? 'Free' : formatPrice(shipping)}</span></div>
                <div className="flex justify-between"><span>Estimated tax</span><span>{formatPrice(tax)}</span></div>

                <div className="pt-3 border-t flex items-center justify-between">
                  <div className="text-sm">Total</div>
                  <div className="text-xl font-semibold">{formatPrice(total)}</div>
                </div>
              </div>

              <button
                disabled={state.items.length === 0}
                onClick={() => navigate('/checkout')}
                className="mt-6 w-full rounded-md bg-[hsl(var(--brand-blue))] text-white px-5 py-3 font-medium disabled:opacity-50"
              >
                Checkout
              </button>

              <div className="mt-4">
                <label className="text-sm block mb-2">Have a coupon?</label>
                <div className="flex gap-2">
                  <input
                    value={coupon}
                    onChange={(e) => setCoupon(e.target.value)}
                    placeholder="Code"
                    className="w-full rounded-md border px-3 py-2"
                  />
                  <button
                    onClick={() => applyCoupon(coupon)}
                    className="rounded-md bg-foreground text-background px-4 py-2 font-medium"
                  >
                    Apply
                  </button>
                </div>
                {couponError && <div className="mt-2 text-sm text-[hsl(var(--brand-red))]">{couponError}</div>}
                {appliedCoupon && <div className="mt-2 text-sm text-[hsl(var(--brand-blue))]">Applied {appliedCoupon}</div>}
              </div>
              </motion.div>
            </aside>
          </div>
        </motion.section>
      </PageTransition>
    </Layout>
  );
}
