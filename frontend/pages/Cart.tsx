import Layout from '../components/layout/Layout';
import { useCart } from '../context/cart';
import { formatPrice, products } from '../data/products';
import { Link, useNavigate } from 'react-router-dom';
import { useState, useEffect } from 'react';
import PageTransition from '../components/ui/PageTransition';
import { motion } from 'framer-motion';
import { Trash2, Plus, Minus, ShoppingBag, ArrowLeft, Tag, Shield, Truck, CreditCard } from 'lucide-react';
import { apiService } from '../services/api';

export default function Cart() {
  const { state, setQty, remove, subtotal, clear, appliedPromoCode, setAppliedPromoCode } = useCart();
  const navigate = useNavigate();

  const [coupon, setCoupon] = useState('');
  const [couponError, setCouponError] = useState<string | null>(null);
  const [couponLoading, setCouponLoading] = useState(false);
  const [productDetails, setProductDetails] = useState<{[key: string]: any}>({});

  // Enhanced coupon logic with API validation
  const applyCoupon = async (code: string) => {
    if (!code.trim()) {
      setCouponError('Please enter a promo code');
      return;
    }

    setCouponLoading(true);
    setCouponError(null);

    try {
      const result = await apiService.validatePromoCode(code, subtotal);
      
      if (result.valid) {
        setAppliedPromoCode({
          code: result.code,
          description: result.description,
          discount_type: result.discount_type,
          discount_amount: Math.round((result.discount_amount || 0) * 100), // Convert to cents
          discount_display: result.discount_display,
          free_shipping: result.free_shipping,
          message: result.message
        });
        setCouponError(null);
        setCoupon(''); // Clear input after successful application
      } else {
        setAppliedPromoCode(null);
        if (result.errors) {
          // Handle validation errors from serializer
          const errorMessages = [];
          if (result.errors.code) {
            errorMessages.push(Array.isArray(result.errors.code) ? result.errors.code[0] : result.errors.code);
          }
          if (result.errors.subtotal) {
            errorMessages.push(Array.isArray(result.errors.subtotal) ? result.errors.subtotal[0] : result.errors.subtotal);
          }
          setCouponError(errorMessages.join('. ') || 'Invalid promo code');
        } else {
          setCouponError(result.error || 'Invalid promo code');
        }
      }
    } catch (error) {
      console.error('Promo code validation error:', error);
      setCouponError('Failed to validate promo code. Please try again.');
      setAppliedPromoCode(null);
    } finally {
      setCouponLoading(false);
    }
  };

  const removeCoupon = () => {
    setAppliedPromoCode(null);
    setCouponError(null);
    setCoupon('');
  };

  // Fetch product details for cart items
  useEffect(() => {
    const fetchProductDetails = async () => {
      console.log('Cart items:', state.items.map(item => ({ id: item.id, title: item.title })));
      console.log('Local products:', products.map(p => ({ id: p.id, slug: p.slug })));
      
      const details: {[key: string]: any} = {};
      
      for (const item of state.items) {
        // First try to find in local products array
        let product = products.find((x) => x.id === item.id);
        
        if (!product) {
          // If not found locally, try to fetch from API
          try {
            console.log('Product not found locally, fetching from API for ID:', item.id);
            const apiProducts = await apiService.getProducts();
            const apiProduct = apiProducts.results.find((x: any) => x.id === item.id);
            if (apiProduct) {
              product = {
                id: apiProduct.id,
                slug: apiProduct.slug,
                category: apiProduct.category,
                title: apiProduct.title
              };
              console.log('Found API product:', product);
            } else {
              console.log('Product not found in API either for ID:', item.id);
            }
          } catch (error) {
            console.error('Failed to fetch product details for', item.id, error);
          }
        } else {
          console.log('Found local product:', product);
        }
        
        if (product) {
          details[item.id] = product;
        }
      }
      
      setProductDetails(details);
    };

    if (state.items.length > 0) {
      fetchProductDetails();
    }
  }, [state.items]);



  const discount = appliedPromoCode ? appliedPromoCode.discount_amount : 0;
  const freeShippingFromPromo = appliedPromoCode?.free_shipping || false;
  const shipping = (subtotal >= 75 || freeShippingFromPromo) ? 0 : 9.99; // dollars
  const tax = Math.round((subtotal - discount) * 0.07); // simple 7% tax estimate
  const total = Math.max(0, subtotal - discount) + shipping + tax;

  return (
    <Layout>
      <PageTransition>
        <div className="min-h-screen bg-gray-50">
          {/* Header Section */}
          <div className="bg-white border-b">
            <div className="container mx-auto px-4 py-6">
              <motion.div 
                className="flex items-center justify-between"
                initial={{ opacity: 0, y: -10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.3 }}
              >
                <div className="flex items-center gap-4">
                  <Link 
                    to="/shop" 
                    className="flex items-center gap-2 text-gray-600 hover:text-gray-900 transition-colors"
                  >
                    <ArrowLeft className="w-5 h-5" />
                    <span className="hidden sm:inline">Continue Shopping</span>
                  </Link>
                  <div className="h-6 w-px bg-gray-300 hidden sm:block"></div>
                  <div className="flex items-center gap-2">
                    <ShoppingBag className="w-6 h-6 text-blue-600" />
                    <h1 className="text-2xl font-bold text-gray-900">Shopping Cart</h1>
                    <span className="bg-blue-100 text-blue-800 text-sm font-medium px-2.5 py-0.5 rounded-full">
                      {state.items.length} {state.items.length === 1 ? 'item' : 'items'}
                    </span>
                  </div>
                </div>
                {state.items.length > 0 && (
                  <button
                    onClick={() => clear()}
                    className="flex items-center gap-2 text-red-600 hover:text-red-700 transition-colors"
                  >
                    <Trash2 className="w-4 h-4" />
                    <span className="hidden sm:inline">Clear Cart</span>
                  </button>
                )}
              </motion.div>
            </div>
          </div>

          <div className="container mx-auto px-4 py-8">
            <div className="grid gap-8 lg:grid-cols-3">
              {/* Cart Items */}
              <main className="lg:col-span-2">
                <motion.div 
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ duration: 0.3, delay: 0.1 }}
                >
                  {state.items.length === 0 ? (
                    <motion.div 
                      className="bg-white rounded-2xl shadow-sm border p-12 text-center"
                      initial={{ opacity: 0, scale: 0.95 }}
                      animate={{ opacity: 1, scale: 1 }}
                      transition={{ duration: 0.25, delay: 0.1 }}
                    >
                      <div className="w-24 h-24 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-6">
                        <ShoppingBag className="w-12 h-12 text-gray-400" />
                      </div>
                      <h3 className="text-xl font-semibold text-gray-900 mb-2">Your cart is empty</h3>
                      <p className="text-gray-500 mb-8">Looks like you haven't added any items to your cart yet.</p>
                      <Link 
                        to="/shop" 
                        className="inline-flex items-center gap-2 bg-blue-600 text-white px-8 py-3 rounded-lg font-medium hover:bg-blue-700 transition-colors"
                      >
                        <ShoppingBag className="w-5 h-5" />
                        Start Shopping
                      </Link>
                    </motion.div>
                  ) : (
                    <div className="bg-white rounded-2xl shadow-sm border overflow-hidden">
                      <div className="p-6 border-b bg-gray-50">
                        <h2 className="text-lg font-semibold text-gray-900">Order Items</h2>
                      </div>
                      <div className="divide-y divide-gray-100">
                        {state.items.map((item, index) => {
                          // Get product details from our fetched data or fallback to local products
                          const p = productDetails[item.id] || products.find((x) => x.id === item.id);
                          
                          // If product not found, skip rendering the links but show the item
                          const productSlug = p?.slug || null;
                          
                          return (
                            <motion.div 
                              key={item.uniqueKey || item.id} 
                              className="p-6 hover:bg-gray-50 transition-colors"
                              initial={{ opacity: 0, y: 10 }}
                              animate={{ opacity: 1, y: 0 }}
                              transition={{ duration: 0.2, delay: 0.05 + index * 0.05 }}
                            >
                              <div className="flex gap-4">
                                {/* Product Image */}
                                <div className="flex-shrink-0">
                                  {productSlug ? (
                                    <Link to={`/product/${productSlug}`} className="block">
                                      <img 
                                        src={item.image} 
                                        alt={item.title} 
                                        className="w-20 h-20 rounded-lg object-cover border border-gray-200"
                                      />
                                    </Link>
                                  ) : (
                                    <img 
                                      src={item.image} 
                                      alt={item.title} 
                                      className="w-20 h-20 rounded-lg object-cover border border-gray-200"
                                    />
                                  )}
                                </div>

                                {/* Product Details */}
                                <div className="flex-1 min-w-0">
                                  <div className="flex justify-between items-start mb-2">
                                    <div className="flex-1">
                                      {productSlug ? (
                                        <Link 
                                          to={`/product/${productSlug}`} 
                                          className="text-lg font-medium text-gray-900 hover:text-blue-600 transition-colors line-clamp-1"
                                        >
                                          {item.title}
                                        </Link>
                                      ) : (
                                        <h3 className="text-lg font-medium text-gray-900 line-clamp-1">
                                          {item.title}
                                        </h3>
                                      )}
                                      <p className="text-sm text-gray-500 capitalize">{p?.category || 'Unknown'}</p>
                                    </div>
                                    <button
                                      onClick={() => remove(item.uniqueKey || item.id)}
                                      className="ml-4 p-2 text-gray-400 hover:text-red-500 transition-colors"
                                      aria-label={`Remove ${item.title} from cart`}
                                    >
                                      <Trash2 className="w-4 h-4" />
                                    </button>
                                  </div>

                                  {/* Variant Information */}
                                  {(item.selectedSize || item.selectedColor) && (
                                    <div className="flex flex-wrap gap-2 mb-3">
                                      {item.selectedSize && (
                                        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                                          Size: {item.selectedSize}
                                        </span>
                                      )}
                                      {item.selectedColor && (
                                        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                                          Color: {item.selectedColor}
                                        </span>
                                      )}
                                    </div>
                                  )}

                                  {/* Price and Quantity */}
                                  <div className="flex items-center justify-between">
                                    <div className="flex items-center gap-4">
                                      <div className="flex items-center border border-gray-300 rounded-lg">
                                        <button
                                          onClick={() => setQty(item.uniqueKey || item.id, Math.max(1, item.quantity - 1))}
                                          className="p-2 hover:bg-gray-100 transition-colors"
                                          aria-label={`Decrease quantity of ${item.title}`}
                                        >
                                          <Minus className="w-4 h-4" />
                                        </button>
                                        <input
                                          className="w-16 text-center text-sm py-2 border-0 focus:ring-0"
                                          value={item.quantity}
                                          onChange={(e) => {
                                            const v = Math.max(1, parseInt(e.target.value || '1'));
                                            setQty(item.uniqueKey || item.id, v);
                                          }}
                                          min="1"
                                        />
                                        <button
                                          onClick={() => setQty(item.uniqueKey || item.id, item.quantity + 1)}
                                          className="p-2 hover:bg-gray-100 transition-colors"
                                          aria-label={`Increase quantity of ${item.title}`}
                                        >
                                          <Plus className="w-4 h-4" />
                                        </button>
                                      </div>
                                      <div className="text-sm text-gray-500">
                                        {formatPrice(item.price)} each
                                      </div>
                                    </div>
                                    <div className="text-lg font-semibold text-gray-900">
                                      {formatPrice(item.price * item.quantity)}
                                    </div>
                                  </div>
                                </div>
                              </div>
                            </motion.div>
                          );
                        })}
                      </div>
                    </div>
                  )}
                </motion.div>
              </main>

              {/* Order Summary */}
              <aside className="lg:col-span-1">
                <motion.div 
                  className="lg:sticky lg:top-8 space-y-6"
                  initial={{ opacity: 0, x: 20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ duration: 0.3, delay: 0.15 }}
                >
                  {/* Order Summary Card */}
                  <div className="bg-white rounded-2xl shadow-sm border p-6">
                    <h2 className="text-lg font-semibold text-gray-900 mb-6">Order Summary</h2>

                    <div className="space-y-4">
                      <div className="flex justify-between text-gray-600">
                        <span>Subtotal ({state.items.length} items)</span>
                        <span className="font-medium">{formatPrice(subtotal)}</span>
                      </div>
                      
                      {discount > 0 && (
                        <div className="flex justify-between text-green-600">
                          <div className="flex items-center gap-1">
                            <span>Discount</span>
                            {appliedPromoCode && (
                              <span className="text-xs bg-green-100 text-green-800 px-2 py-0.5 rounded-full">
                                {appliedPromoCode.code}
                              </span>
                            )}
                          </div>
                          <span className="font-medium">-{formatPrice(discount)}</span>
                        </div>
                      )}
                      
                      <div className="flex justify-between text-gray-600">
                        <div className="flex items-center gap-1">
                          <Truck className="w-4 h-4" />
                          <span>Shipping</span>
                        </div>
                        <span className="font-medium">
                          {shipping === 0 ? (
                            <span className="text-green-600">
                              Free {freeShippingFromPromo && appliedPromoCode && (
                                <span className="text-xs bg-green-100 text-green-800 px-2 py-0.5 rounded-full ml-1">
                                  {appliedPromoCode.code}
                                </span>
                              )}
                            </span>
                          ) : (
                            formatPrice(shipping)
                          )}
                        </span>
                      </div>
                      
                      <div className="flex justify-between text-gray-600">
                        <span>Estimated tax</span>
                        <span className="font-medium">{formatPrice(tax)}</span>
                      </div>

                      <div className="border-t pt-4">
                        <div className="flex justify-between items-center">
                          <span className="text-lg font-semibold text-gray-900">Total</span>
                          <span className="text-2xl font-bold text-gray-900">{formatPrice(total)}</span>
                        </div>
                      </div>
                    </div>

                    <button
                      disabled={state.items.length === 0}
                      onClick={() => navigate('/checkout')}
                      className="mt-6 w-full flex items-center justify-center gap-2 bg-blue-600 text-white px-6 py-4 rounded-lg font-semibold hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                    >
                      <CreditCard className="w-5 h-5" />
                      Proceed to Checkout
                    </button>

                    {subtotal < 75 && (
                      <div className="mt-4 p-3 bg-blue-50 border border-blue-200 rounded-lg">
                        <p className="text-sm text-blue-800">
                          <Truck className="w-4 h-4 inline mr-1" />
                          Add {formatPrice(75 - subtotal)} more for free shipping!
                        </p>
                      </div>
                    )}
                  </div>

                  {/* Coupon Card - Only show if no promo code is applied */}
                  {!appliedPromoCode && (
                    <div className="bg-white rounded-2xl shadow-sm border p-6">
                      <div className="flex items-center gap-2 mb-4">
                        <Tag className="w-5 h-5 text-gray-600" />
                        <h3 className="font-semibold text-gray-900">Promo Code</h3>
                      </div>
                      
                      <div className="space-y-3">
                        <div className="flex gap-2">
                          <input
                            value={coupon}
                            onChange={(e) => setCoupon(e.target.value)}
                            onKeyPress={(e) => e.key === 'Enter' && applyCoupon(coupon)}
                            placeholder="Enter promo code"
                            className="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                            disabled={couponLoading}
                          />
                          <button
                            onClick={() => applyCoupon(coupon)}
                            disabled={couponLoading || !coupon.trim()}
                            className="px-4 py-2 bg-gray-900 text-white rounded-lg font-medium hover:bg-gray-800 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                          >
                            {couponLoading ? 'Checking...' : 'Apply'}
                          </button>
                        </div>
                        
                        {couponError && (
                          <div className="text-sm text-red-600 bg-red-50 border border-red-200 p-3 rounded-lg">
                            {couponError}
                          </div>
                        )}
                      </div>
                    </div>
                  )}

                  {/* Security Features */}
                  <div className="bg-white rounded-2xl shadow-sm border p-6">
                    <h3 className="font-semibold text-gray-900 mb-4">Why shop with us?</h3>
                    <div className="space-y-3">
                      <div className="flex items-center gap-3 text-sm text-gray-600">
                        <Shield className="w-4 h-4 text-green-500" />
                        <span>Secure checkout</span>
                      </div>
                      <div className="flex items-center gap-3 text-sm text-gray-600">
                        <Truck className="w-4 h-4 text-blue-500" />
                        <span>Free shipping over $75</span>
                      </div>
                      <div className="flex items-center gap-3 text-sm text-gray-600">
                        <CreditCard className="w-4 h-4 text-purple-500" />
                        <span>30-day returns</span>
                      </div>
                    </div>
                  </div>
                </motion.div>
              </aside>
            </div>
          </div>
        </div>
      </PageTransition>
    </Layout>
  );
}