import Layout from '../components/layout/Layout';
import { useLocation, Link } from 'react-router-dom';
import { formatPrice } from '../data/products';
import PageTransition from '../components/ui/PageTransition';
import { motion } from 'framer-motion';
import { 
  CheckCircle, 
  Package, 
  Truck, 
  Mail, 
  Calendar, 
  CreditCard, 
  Download,
  ArrowRight,
  Shield,
  Clock,
  MapPin
} from 'lucide-react';
import { useState, useEffect } from 'react';

type Summary = {
  id: string;
  total: number;
  items: { 
    id: string; 
    title: string; 
    price: number; 
    quantity: number; 
    image: string;
    selectedSize?: string;
    selectedColor?: string;
    variantId?: number;
  }[];
};

export default function OrderConfirmation() {
  const { state } = useLocation();
  const s = (state || {}) as Summary;
  const [currentDate] = useState(new Date());
  const [estimatedDelivery] = useState(() => {
    const delivery = new Date();
    delivery.setDate(delivery.getDate() + 5); // 5 business days
    return delivery;
  });

  // Generate a more realistic order number if none provided
  const orderNumber = s.id || `ENNC${Date.now().toString().slice(-6)}`;

  return (
    <Layout>
      <PageTransition>
        <div className="min-h-screen bg-gradient-to-br from-gray-50 to-white">
          {/* Success Header */}
          <div className="bg-white border-b">
            <div className="container mx-auto px-4 py-8">
              <motion.div 
                className="max-w-4xl mx-auto text-center"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5 }}
              >
                <motion.div 
                  className="inline-flex items-center justify-center w-20 h-20 bg-green-100 rounded-full mb-6"
                  initial={{ scale: 0 }}
                  animate={{ scale: 1 }}
                  transition={{ duration: 0.6, delay: 0.2, type: "spring", stiffness: 200 }}
                >
                  <CheckCircle className="w-10 h-10 text-green-600" />
                </motion.div>
                
                <motion.h1 
                  className="text-4xl font-bold text-gray-900 mb-4"
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.4, delay: 0.3 }}
                >
                  Order Confirmed!
                </motion.h1>
                
                <motion.p 
                  className="text-xl text-gray-600 mb-2"
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.4, delay: 0.4 }}
                >
                  Thank you for your purchase from ENNC
                </motion.p>
                
                <motion.p 
                  className="text-gray-500"
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.4, delay: 0.5 }}
                >
                  Order #{orderNumber} • Placed on {currentDate.toLocaleDateString('en-US', { 
                    weekday: 'long', 
                    year: 'numeric', 
                    month: 'long', 
                    day: 'numeric' 
                  })}
                </motion.p>
              </motion.div>
            </div>
          </div>

          <div className="container mx-auto px-4 py-12">
            <div className="max-w-6xl mx-auto grid gap-8 lg:grid-cols-3">
              
              {/* Main Content */}
              <div className="lg:col-span-2 space-y-8">
                
                {/* Order Status Timeline */}
                <motion.div 
                  className="bg-white rounded-2xl shadow-sm border p-8"
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.5, delay: 0.6 }}
                >
                  <h2 className="text-2xl font-semibold text-gray-900 mb-6">Order Status</h2>
                  
                  <div className="space-y-6">
                    {/* Order Confirmed */}
                    <div className="flex items-center gap-4">
                      <div className="flex-shrink-0 w-10 h-10 bg-green-100 rounded-full flex items-center justify-center">
                        <CheckCircle className="w-5 h-5 text-green-600" />
                      </div>
                      <div className="flex-1">
                        <h3 className="font-medium text-gray-900">Order Confirmed</h3>
                        <p className="text-sm text-gray-500">Your order has been received and is being processed</p>
                        <p className="text-xs text-green-600 font-medium">Completed • {currentDate.toLocaleTimeString()}</p>
                      </div>
                    </div>
                    
                    {/* Processing */}
                    <div className="flex items-center gap-4">
                      <div className="flex-shrink-0 w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center">
                        <Package className="w-5 h-5 text-blue-600" />
                      </div>
                      <div className="flex-1">
                        <h3 className="font-medium text-gray-900">Processing</h3>
                        <p className="text-sm text-gray-500">We're preparing your items for shipment</p>
                        <p className="text-xs text-blue-600 font-medium">In Progress • Est. 1-2 business days</p>
                      </div>
                    </div>
                    
                    {/* Shipped */}
                    <div className="flex items-center gap-4">
                      <div className="flex-shrink-0 w-10 h-10 bg-gray-100 rounded-full flex items-center justify-center">
                        <Truck className="w-5 h-5 text-gray-400" />
                      </div>
                      <div className="flex-1">
                        <h3 className="font-medium text-gray-500">Shipped</h3>
                        <p className="text-sm text-gray-400">Your order will be shipped soon</p>
                        <p className="text-xs text-gray-400">Pending</p>
                      </div>
                    </div>
                    
                    {/* Delivered */}
                    <div className="flex items-center gap-4">
                      <div className="flex-shrink-0 w-10 h-10 bg-gray-100 rounded-full flex items-center justify-center">
                        <MapPin className="w-5 h-5 text-gray-400" />
                      </div>
                      <div className="flex-1">
                        <h3 className="font-medium text-gray-500">Delivered</h3>
                        <p className="text-sm text-gray-400">Estimated delivery date</p>
                        <p className="text-xs text-gray-400">
                          Est. {estimatedDelivery.toLocaleDateString('en-US', { 
                            weekday: 'long', 
                            month: 'long', 
                            day: 'numeric' 
                          })}
                        </p>
                      </div>
                    </div>
                  </div>
                </motion.div>

                {/* Order Items */}
                <motion.div 
                  className="bg-white rounded-2xl shadow-sm border p-8"
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.5, delay: 0.7 }}
                >
                  <h2 className="text-2xl font-semibold text-gray-900 mb-6">Order Items</h2>
                  
                  <div className="space-y-4">
                    {s.items?.map((item, index) => (
                      <motion.div 
                        key={item.id}
                        className="flex items-center gap-4 p-4 border border-gray-100 rounded-xl hover:bg-gray-50 transition-colors"
                        initial={{ opacity: 0, x: -20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ duration: 0.3, delay: 0.8 + index * 0.1 }}
                      >
                        <div className="w-20 h-20 bg-gray-100 rounded-lg overflow-hidden flex-shrink-0">
                          <img 
                            src={item.image} 
                            alt={item.title} 
                            className="w-full h-full object-cover"
                            onError={(e) => {
                              // Fallback to placeholder if image fails to load
                              const target = e.target as HTMLImageElement;
                              target.style.display = 'none';
                              const parent = target.parentElement;
                              if (parent) {
                                parent.innerHTML = `
                                  <div class="w-full h-full flex items-center justify-center">
                                    <svg class="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"></path>
                                    </svg>
                                  </div>
                                `;
                              }
                            }}
                          />
                        </div>
                        <div className="flex-1 min-w-0">
                          <h3 className="font-medium text-gray-900 mb-1 line-clamp-2">{item.title}</h3>
                          
                          {/* Variant Information */}
                          {(item.selectedSize || item.selectedColor) && (
                            <div className="flex flex-wrap gap-2 mb-2">
                              {item.selectedSize && (
                                <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                                  Size: {item.selectedSize}
                                </span>
                              )}
                              {item.selectedColor && (
                                <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800">
                                  Color: {item.selectedColor}
                                </span>
                              )}
                            </div>
                          )}
                          
                          <div className="flex items-center gap-4 text-sm text-gray-500">
                            <span>Qty: {item.quantity}</span>
                            <span>•</span>
                            <span>{formatPrice(item.price)} each</span>
                          </div>
                        </div>
                        <div className="text-right flex-shrink-0">
                          <p className="font-semibold text-lg text-gray-900">{formatPrice(item.price * item.quantity)}</p>
                          {item.quantity > 1 && (
                            <p className="text-sm text-gray-500">{item.quantity} × {formatPrice(item.price)}</p>
                          )}
                        </div>
                      </motion.div>
                    ))}
                  </div>
                </motion.div>

                {/* What's Next */}
                <motion.div 
                  className="bg-blue-50 rounded-2xl border border-blue-200 p-8"
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.5, delay: 0.8 }}
                >
                  <h2 className="text-2xl font-semibold text-gray-900 mb-6">What happens next?</h2>
                  
                  <div className="grid gap-6 md:grid-cols-2">
                    <div className="flex items-start gap-3">
                      <div className="flex-shrink-0 w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center">
                        <Mail className="w-4 h-4 text-blue-600" />
                      </div>
                      <div>
                        <h3 className="font-medium text-gray-900 mb-1">Email Confirmation</h3>
                        <p className="text-sm text-gray-600">You'll receive an email confirmation with your order details and tracking information.</p>
                      </div>
                    </div>
                    
                    <div className="flex items-start gap-3">
                      <div className="flex-shrink-0 w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center">
                        <Package className="w-4 h-4 text-blue-600" />
                      </div>
                      <div>
                        <h3 className="font-medium text-gray-900 mb-1">Order Processing</h3>
                        <p className="text-sm text-gray-600">We'll prepare your items with care and quality check each product.</p>
                      </div>
                    </div>
                    
                    <div className="flex items-start gap-3">
                      <div className="flex-shrink-0 w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center">
                        <Truck className="w-4 h-4 text-blue-600" />
                      </div>
                      <div>
                        <h3 className="font-medium text-gray-900 mb-1">Shipping Updates</h3>
                        <p className="text-sm text-gray-600">Track your package with real-time updates sent to your email.</p>
                      </div>
                    </div>
                    
                    <div className="flex items-start gap-3">
                      <div className="flex-shrink-0 w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center">
                        <Clock className="w-4 h-4 text-blue-600" />
                      </div>
                      <div>
                        <h3 className="font-medium text-gray-900 mb-1">Delivery</h3>
                        <p className="text-sm text-gray-600">Your order will arrive within 3-5 business days.</p>
                      </div>
                    </div>
                  </div>
                </motion.div>
              </div>

              {/* Sidebar */}
              <div className="space-y-6">
                
                {/* Order Summary */}
                <motion.div 
                  className="bg-white rounded-2xl shadow-sm border p-6"
                  initial={{ opacity: 0, x: 20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ duration: 0.5, delay: 0.9 }}
                >
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">Order Summary</h3>
                  
                  <div className="space-y-3 text-sm">
                    <div className="flex justify-between">
                      <span className="text-gray-600">Subtotal</span>
                      <span className="font-medium">{formatPrice(s.total || 0)}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Shipping</span>
                      <span className="font-medium text-green-600">Free</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Tax</span>
                      <span className="font-medium">Included</span>
                    </div>
                    <div className="border-t pt-3">
                      <div className="flex justify-between items-center">
                        <span className="text-lg font-semibold text-gray-900">Total</span>
                        <span className="text-2xl font-bold text-gray-900">{formatPrice(s.total || 0)}</span>
                      </div>
                    </div>
                  </div>
                </motion.div>

                {/* Quick Actions */}
                <motion.div 
                  className="bg-white rounded-2xl shadow-sm border p-6"
                  initial={{ opacity: 0, x: 20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ duration: 0.5, delay: 1.0 }}
                >
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">Quick Actions</h3>
                  
                  <div className="space-y-3">
                    <button className="w-full flex items-center justify-between p-3 text-left border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors">
                      <div className="flex items-center gap-3">
                        <Download className="w-4 h-4 text-gray-600" />
                        <span className="text-sm font-medium">Download Receipt</span>
                      </div>
                      <ArrowRight className="w-4 h-4 text-gray-400" />
                    </button>
                    
                    <Link 
                      to="/contact" 
                      className="w-full flex items-center justify-between p-3 text-left border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors"
                    >
                      <div className="flex items-center gap-3">
                        <Mail className="w-4 h-4 text-gray-600" />
                        <span className="text-sm font-medium">Contact Support</span>
                      </div>
                      <ArrowRight className="w-4 h-4 text-gray-400" />
                    </Link>
                    
                    <Link 
                      to="/shop" 
                      className="w-full flex items-center justify-between p-3 text-left border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors"
                    >
                      <div className="flex items-center gap-3">
                        <Package className="w-4 h-4 text-gray-600" />
                        <span className="text-sm font-medium">Continue Shopping</span>
                      </div>
                      <ArrowRight className="w-4 h-4 text-gray-400" />
                    </Link>
                  </div>
                </motion.div>

                {/* Security & Trust */}
                <motion.div 
                  className="bg-gray-50 rounded-2xl border p-6"
                  initial={{ opacity: 0, x: 20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ duration: 0.5, delay: 1.1 }}
                >
                  <div className="flex items-center gap-2 mb-4">
                    <Shield className="w-5 h-5 text-green-600" />
                    <h3 className="font-semibold text-gray-900">Secure & Protected</h3>
                  </div>
                  
                  <div className="space-y-3 text-sm text-gray-600">
                    <div className="flex items-center gap-2">
                      <CreditCard className="w-4 h-4" />
                      <span>SSL encrypted payment</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <Shield className="w-4 h-4" />
                      <span>30-day return policy</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <Truck className="w-4 h-4" />
                      <span>Free shipping & returns</span>
                    </div>
                  </div>
                </motion.div>
              </div>
            </div>
          </div>
        </div>
      </PageTransition>
    </Layout>
  );
}
