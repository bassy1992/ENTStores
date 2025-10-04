import Layout from '../components/layout/Layout';
import { useCart } from '../context/cart';
import { formatPrice } from '../data/products';
import { useNavigate } from 'react-router-dom';
import { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { Label } from '../components/ui/label';
import { RadioGroup, RadioGroupItem } from '../components/ui/radio-group';
import { Separator } from '../components/ui/separator';
import { Badge } from '../components/ui/badge';
import { CreditCard, Smartphone, Shield, Clock, CheckCircle, AlertCircle, Globe, MapPin, Tag } from 'lucide-react';
import PageTransition from '../components/ui/PageTransition';
import { motion } from 'framer-motion';
import { API_ENDPOINTS, API_BASE_URL } from '../config/api';
import { countries, getShippingCost, getShippingZone } from '../data/countries';
import { requiresPayment, getCheckoutFlow, getCheckoutMessage } from '../utils/countryPaymentRules';

// Fetch exchange rate when component mounts
const fetchExchangeRate = async () => {
  try {
    const response = await fetch(API_ENDPOINTS.EXCHANGE_RATE);
    if (response.ok) {
      const data = await response.json();
      return data;
    }
  } catch (error) {
    console.error('Failed to fetch exchange rate:', error);
  }
  return null;
};

export default function Checkout() {
  const { state, subtotal, shipping, clear, saveCheckoutData, appliedPromoCode } = useCart();
  const navigate = useNavigate();

  const [form, setForm] = useState({
    email: '',
    name: '',
    address: '',
    addressLine2: '',
    city: '',
    state: '',
    country: 'GH', // Default to Ghana
    postal: '',
    phone: '',
  });

  const [paymentMethod, setPaymentMethod] = useState<'stripe' | 'momo' | null>(null);
  const [momoPhone, setMomoPhone] = useState('');
  const [processing, setProcessing] = useState(false);
  const [momoRef, setMomoRef] = useState<string | null>(null);
  const [momoStatus, setMomoStatus] = useState<string | null>(null);
  const [exchangeRate, setExchangeRate] = useState<any>(null);
  const [momoConversion, setMomoConversion] = useState<any>(null);

  // Check if current country requires payment
  const countryRequiresPayment = requiresPayment(form.country);
  const checkoutFlow = getCheckoutFlow(form.country);
  const checkoutMessage = getCheckoutMessage(form.country);

  // Show payment options only for countries that require payment
  const available = { 
    stripe: countryRequiresPayment, 
    momo: countryRequiresPayment && form.country === 'GH' // MoMo only for Ghana
  };

  // Calculate totals with product-based shipping
  const selectedCountry = countries.find(c => c.code === form.country);
  const shippingZone = getShippingZone(form.country);
  const discount = appliedPromoCode ? appliedPromoCode.discount_amount : 0;
  const freeShippingFromPromo = appliedPromoCode?.free_shipping || false;
  
  // Use product-based shipping from cart, but apply free shipping if applicable
  const finalShipping = freeShippingFromPromo ? 0 : shipping;
  const tax = Math.round((subtotal - discount) * 0.05); // 5% tax on discounted amount
  const total = Math.max(0, subtotal - discount) + finalShipping + tax;

  // Fetch exchange rate on component mount
  useEffect(() => {
    fetchExchangeRate().then(rate => {
      if (rate) {
        setExchangeRate(rate);
      }
    });
  }, []);

  async function handlePay(e?: React.FormEvent) {
    if (e) e.preventDefault();

    // Validate required fields
    if (!form.email || !form.name || !form.address || !form.city || !form.country) {
      alert('Please fill in all required fields (Email, Name, Address, City, and Country)');
      return;
    }

    // Validate payment method selection for countries that require payment
    if (countryRequiresPayment && !paymentMethod) {
      alert('Please select a payment method (Credit Card or MTN MoMo)');
      return;
    }

    // Handle free checkout for countries that don't require payment
    if (!countryRequiresPayment) {
      try {
        setProcessing(true);
        
        const orderData = {
          customer_email: form.email,
          customer_name: form.name,
          shipping_address: `${form.address}${form.addressLine2 ? ', ' + form.addressLine2 : ''}`,
          shipping_city: form.city,
          shipping_country: form.country,
          shipping_postal_code: form.postal,
          subtotal: subtotal,
          shipping_cost: finalShipping,
          tax_amount: tax,
          total: total,
          items: state.items.map(item => ({
            product_id: item.id,
            quantity: item.quantity,
            unit_price: item.price,
            selected_size: item.selectedSize || '',
            selected_color: item.selectedColor || '',
            variant_id: item.variantId || null
          }))
        };

        const response = await fetch(API_ENDPOINTS.CREATE_FREE_ORDER, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(orderData),
        });

        const result = await response.json();

        if (response.ok) {
          // Clear cart and navigate to confirmation
          const orderSummary = {
            id: result.order_id,
            total: total,
            items: state.items.map(item => ({
              id: item.id,
              title: item.title,
              price: item.price,
              quantity: item.quantity,
              image: item.image,
              selectedSize: item.selectedSize,
              selectedColor: item.selectedColor,
              variantId: item.variantId
            })),
            paymentMethod: 'free_checkout',
            shippingCountry: form.country
          };
          
          clear();
          navigate('/order-confirmation', { state: orderSummary });
        } else {
          console.error('Free order creation failed:', result);
          alert(result.message || 'Failed to create order. Please try again.');
        }
      } catch (error) {
        console.error('Free checkout error:', error);
        alert('Failed to process order. Please try again.');
      } finally {
        setProcessing(false);
      }
      return;
    }

    if (paymentMethod === 'stripe') {
      try {
        setProcessing(true);
        const items = state.items.map((i) => ({ 
          title: i.title, 
          amount: i.price, 
          quantity: i.quantity, 
          image: i.image,
          shipping_cost: i.shipping_cost || 9.99 // Include shipping cost per item
        }));
        
        // Add shipping and tax as separate line items if they exist
        const checkoutItems = [...items];
        if (finalShipping > 0) {
          checkoutItems.push({
            title: 'Shipping',
            amount: finalShipping,
            quantity: 1,
            image: '',
            shipping_cost: 0
          });
        }
        if (tax > 0) {
          checkoutItems.push({
            title: 'Tax (5%)',
            amount: tax,
            quantity: 1,
            image: '',
            shipping_cost: 0
          });
        }
        
        const resp = await fetch(API_ENDPOINTS.STRIPE_CHECKOUT, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ 
            items: checkoutItems, 
            success_url: `${location.origin}/stripe-success`, 
            cancel_url: `${location.origin}/cart`,
            shipping_cost: finalShipping,
            tax_amount: tax
          }),
        });
        const data = await resp.json();
        if (data.url) {
          // Save checkout data before redirect
          saveCheckoutData({
            form,
            items: state.items,
            subtotal,
            shipping: finalShipping,
            tax,
            total,
            timestamp: Date.now()
          });
          
          // redirect to Stripe Checkout
          window.location.href = data.url;
        } else {
          console.error('Stripe create session failed', data);
          alert('Failed to create Stripe checkout session');
        }
      } catch (err) {
        console.error(err);
        alert('Payment error');
      } finally {
        setProcessing(false);
      }
    } else {
      // MTN MoMo flow (demo)
      if (!momoPhone) return alert('Enter mobile number for MoMo');
      try {
        setProcessing(true);
        const resp = await fetch(API_ENDPOINTS.MOMO_INITIATE, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ phone: momoPhone, amount: total, currency: 'USD' }),
        });
        const data = await resp.json();
        if (data.reference) {
          setMomoRef(data.reference);
          setMomoStatus(data.status || 'pending');
          setMomoConversion(data.currency_conversion);
          
          // poll status every 2s
          const interval = setInterval(async () => {
            const s = await (await fetch(`${API_BASE_URL}/api/payments/momo/status/${data.reference}/`)).json();
            setMomoStatus(s.status);
            if (s.status === 'success') {
              clearInterval(interval);
              // complete order
              const orderId = Math.random().toString(36).slice(2, 10).toUpperCase();
              const summary = { 
                id: orderId, 
                total, 
                items: state.items.map(item => ({
                  id: item.id,
                  title: item.title,
                  price: item.price,
                  quantity: item.quantity,
                  image: item.image,
                  selectedSize: item.selectedSize,
                  selectedColor: item.selectedColor,
                  variantId: item.variantId
                }))
              };
              clear();
              navigate('/order-confirmation', { state: summary });
            }
            if (s.status === 'failed') {
              clearInterval(interval);
              alert('Payment failed');
            }
          }, 2000);
        } else {
          alert('Failed to initiate MoMo payment.');
        }
      } catch (err) {
        console.error(err);
        alert('MoMo error');
      } finally {
        setProcessing(false);
      }
    }
  }

  return (
    <Layout>
      <PageTransition>
        <motion.div 
          className="container mx-auto px-4 py-8"
          initial={{ opacity: 0, y: 15 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3 }}
        >
          <div className="max-w-6xl mx-auto">
            <motion.div 
              className="mb-8"
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.25, delay: 0.05 }}
            >
              <h1 className="text-3xl font-bold text-gray-900">Secure Checkout</h1>
              <p className="text-gray-600 mt-2">Complete your order with confidence</p>
            </motion.div>

            <div className="grid gap-8 lg:grid-cols-3">
              {/* Main Checkout Form */}
              <div className="lg:col-span-2 space-y-6">
                {/* Contact Information */}
                <motion.div
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ duration: 0.3, delay: 0.1 }}
                >
                  <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center">
                      <span className="text-blue-600 font-semibold text-sm">1</span>
                    </div>
                    Contact Information
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div>
                    <Label htmlFor="email">Email Address</Label>
                    <Input
                      id="email"
                      type="email"
                      value={form.email}
                      onChange={(e) => setForm({ ...form, email: e.target.value })}
                      placeholder="your@email.com"
                      required
                    />
                  </div>
                  </CardContent>
                </Card>
              </motion.div>

              {/* Shipping Information */}
              <motion.div
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.3, delay: 0.15 }}
              >
                <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center">
                      <span className="text-blue-600 font-semibold text-sm">2</span>
                    </div>
                    Shipping Information
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  {/* Full Name and Phone */}
                  <div className="grid gap-4 md:grid-cols-2">
                    <div>
                      <Label htmlFor="name">Full Name *</Label>
                      <Input
                        id="name"
                        value={form.name}
                        onChange={(e) => setForm({ ...form, name: e.target.value })}
                        placeholder="John Doe"
                        required
                      />
                    </div>
                    <div>
                      <Label htmlFor="phone">Phone Number</Label>
                      <Input
                        id="phone"
                        type="tel"
                        value={form.phone}
                        onChange={(e) => setForm({ ...form, phone: e.target.value })}
                        placeholder="+233 XX XXX XXXX"
                      />
                      <p className="text-xs text-gray-500 mt-1">For delivery coordination</p>
                    </div>
                  </div>

                  {/* Country Selection */}
                  <div>
                    <Label htmlFor="country" className="flex items-center gap-2">
                      <Globe className="w-4 h-4" />
                      Country / Region *
                    </Label>
                    <select
                      id="country"
                      value={form.country}
                      onChange={(e) => setForm({ ...form, country: e.target.value })}
                      className="w-full rounded-md border border-gray-300 px-3 py-2 bg-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      required
                    >
                      {countries.map((country) => (
                        <option key={country.code} value={country.code}>
                          {country.flag} {country.name}
                        </option>
                      ))}
                    </select>
                    {selectedCountry && (
                      <div className="mt-2 p-2 bg-blue-50 rounded-md">
                        <p className="text-sm text-blue-800">
                          <MapPin className="w-4 h-4 inline mr-1" />
                          Shipping to: <strong>{selectedCountry.name}</strong> ({shippingZone.name})
                        </p>
                        <p className="text-xs text-blue-600 mt-1">
                          Free shipping on orders over ${shippingZone.freeShippingThreshold.toFixed(0)}
                        </p>
                      </div>
                    )}
                  </div>

                  {/* Address Line 1 */}
                  <div>
                    <Label htmlFor="address">Street Address *</Label>
                    <Input
                      id="address"
                      value={form.address}
                      onChange={(e) => setForm({ ...form, address: e.target.value })}
                      placeholder="123 Main Street, Apartment, Suite, etc."
                      required
                    />
                  </div>

                  {/* Address Line 2 */}
                  <div>
                    <Label htmlFor="addressLine2">Address Line 2 (Optional)</Label>
                    <Input
                      id="addressLine2"
                      value={form.addressLine2}
                      onChange={(e) => setForm({ ...form, addressLine2: e.target.value })}
                      placeholder="Apartment, suite, unit, building, floor, etc."
                    />
                  </div>

                  {/* City, State, Postal Code */}
                  <div className="grid gap-4 md:grid-cols-3">
                    <div>
                      <Label htmlFor="city">City *</Label>
                      <Input
                        id="city"
                        value={form.city}
                        onChange={(e) => setForm({ ...form, city: e.target.value })}
                        placeholder="Accra"
                        required
                      />
                    </div>
                    <div>
                      <Label htmlFor="state">State / Province</Label>
                      <Input
                        id="state"
                        value={form.state}
                        onChange={(e) => setForm({ ...form, state: e.target.value })}
                        placeholder="Greater Accra"
                      />
                    </div>
                    <div>
                      <Label htmlFor="postal">Postal / ZIP Code</Label>
                      <Input
                        id="postal"
                        value={form.postal}
                        onChange={(e) => setForm({ ...form, postal: e.target.value })}
                        placeholder="GA-123-4567"
                      />
                    </div>
                  </div>

                  {/* International Shipping Notice */}
                  {form.country !== 'GH' && (
                    <div className="p-4 bg-amber-50 border border-amber-200 rounded-lg">
                      <div className="flex items-start gap-2">
                        <AlertCircle className="w-5 h-5 text-amber-600 mt-0.5" />
                        <div>
                          <h4 className="font-medium text-amber-800">International Shipping</h4>
                          <p className="text-sm text-amber-700 mt-1">
                            • Delivery time: 7-21 business days depending on location
                          </p>
                          <p className="text-sm text-amber-700">
                            • Additional customs fees may apply at destination
                          </p>
                          <p className="text-sm text-amber-700">
                            • We'll provide tracking information once shipped
                          </p>
                        </div>
                      </div>
                    </div>
                  )}
                  </CardContent>
                </Card>
              </motion.div>

              {/* Payment Method */}
              <motion.div
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.3, delay: 0.2 }}
              >
                <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center">
                      <span className="text-blue-600 font-semibold text-sm">3</span>
                    </div>
                    {countryRequiresPayment ? 'Choose Payment Method' : 'Order Confirmation'}
                  </CardTitle>
                  <p className="text-sm text-gray-600 mt-2">
                    {countryRequiresPayment 
                      ? 'Select how you\'d like to pay for your order. Both options are secure and reliable.'
                      : checkoutMessage
                    }
                  </p>
                </CardHeader>
                <CardContent>
                  {!countryRequiresPayment ? (
                    // Free checkout message for countries that don't require payment
                    <div className="space-y-4">
                      <div className="p-6 bg-green-50 border border-green-200 rounded-lg">
                        <div className="flex items-center gap-3 text-green-800 mb-3">
                          <CheckCircle className="w-6 h-6" />
                          <span className="font-bold text-lg">No Payment Required!</span>
                        </div>
                        <p className="text-green-700 mb-4">
                          Great news! Orders to <strong>{selectedCountry?.name}</strong> don't require upfront payment. 
                          Your order will be confirmed immediately and we'll contact you for payment arrangements.
                        </p>
                        <div className="bg-white p-4 rounded-md border border-green-200">
                          <h4 className="font-medium text-green-800 mb-2">What happens next:</h4>
                          <ul className="text-sm text-green-700 space-y-1">
                            <li>• Your order will be confirmed immediately</li>
                            <li>• We'll send you an order confirmation email</li>
                            <li>• Our team will contact you within 24 hours</li>
                            <li>• Payment arrangements will be made before shipping</li>
                          </ul>
                        </div>
                      </div>
                    </div>
                  ) : (
                    // Payment method selection for countries that require payment
                    <div className="space-y-4">
                      {!paymentMethod && (
                        <div className="p-4 bg-blue-50 border border-blue-200 rounded-lg">
                          <div className="flex items-center gap-2 text-blue-800">
                            <AlertCircle className="w-5 h-5" />
                            <span className="font-medium">Choose your preferred payment method</span>
                          </div>
                          <p className="text-sm text-blue-700 mt-1">Select either card payment or mobile money to continue</p>
                        </div>
                      )}

                      <div className="grid gap-4">
                        {/* Stripe Payment Option - only show if available */}
                        {available.stripe && (
                          <div
                            className={`p-5 border-2 rounded-xl cursor-pointer transition-all duration-200 ${paymentMethod === 'stripe'
                                ? 'border-blue-500 bg-blue-50 ring-2 ring-blue-200 shadow-md'
                                : 'border-gray-200 hover:border-blue-300 hover:bg-blue-25 hover:shadow-sm'
                              }`}
                            onClick={() => setPaymentMethod('stripe')}
                          >
                        <div className="flex items-center justify-between">
                          <div className="flex items-center gap-4">
                            <div className={`w-14 h-14 rounded-xl flex items-center justify-center ${paymentMethod === 'stripe' ? 'bg-blue-100' : 'bg-gray-100'
                              }`}>
                              <CreditCard className={`w-7 h-7 ${paymentMethod === 'stripe' ? 'text-blue-600' : 'text-gray-600'
                                }`} />
                            </div>
                            <div>
                              <div className="font-bold text-lg text-gray-900">Credit/Debit Card</div>
                              <div className="text-sm text-gray-600">Visa, Mastercard, American Express</div>
                              <div className="text-xs text-gray-500 mt-1 flex items-center gap-1">
                                <Shield className="w-3 h-3" />
                                Instant & secure payment processing
                              </div>
                            </div>
                          </div>
                          <div className="flex items-center gap-3">
                            <Badge variant="secondary" className="bg-green-100 text-green-700 border-green-200">
                              <Shield className="w-3 h-3 mr-1" />
                              SSL Secure
                            </Badge>
                            <div className={`w-6 h-6 rounded-full border-2 flex items-center justify-center ${paymentMethod === 'stripe'
                                ? 'border-blue-500 bg-blue-500'
                                : 'border-gray-300'
                              }`}>
                              {paymentMethod === 'stripe' && (
                                <CheckCircle className="w-4 h-4 text-white" />
                              )}
                            </div>
                            </div>
                          </div>
                        </div>
                        )}

                        {/* MTN MoMo Payment Option - only show if available */}
                        {available.momo && (
                          <div
                            className={`p-5 border-2 rounded-xl cursor-pointer transition-all duration-200 ${paymentMethod === 'momo'
                                ? 'border-yellow-500 bg-yellow-50 ring-2 ring-yellow-200 shadow-md'
                                : 'border-gray-200 hover:border-yellow-300 hover:bg-yellow-25 hover:shadow-sm'
                              }`}
                            onClick={() => setPaymentMethod('momo')}
                          >
                        <div className="flex items-center justify-between">
                          <div className="flex items-center gap-4">
                            <div className={`w-14 h-14 rounded-xl flex items-center justify-center ${paymentMethod === 'momo' ? 'bg-yellow-100' : 'bg-gray-100'
                              }`}>
                              <Smartphone className={`w-7 h-7 ${paymentMethod === 'momo' ? 'text-yellow-600' : 'text-gray-600'
                                }`} />
                            </div>
                            <div>
                              <div className="font-bold text-lg text-gray-900">MTN Mobile Money</div>
                              <div className="text-sm text-gray-600">Pay directly from your MTN MoMo wallet</div>
                              <div className="text-xs text-gray-500 mt-1 flex items-center gap-1">
                                <Smartphone className="w-3 h-3" />
                                No card required • Most popular in Ghana
                              </div>
                            </div>
                          </div>
                          <div className="flex items-center gap-3">
                            <Badge variant="secondary" className="bg-yellow-100 text-yellow-700 border-yellow-200">
                              🇬🇭 Ghana Favorite
                            </Badge>
                            <div className={`w-6 h-6 rounded-full border-2 flex items-center justify-center ${paymentMethod === 'momo'
                                ? 'border-yellow-500 bg-yellow-500'
                                : 'border-gray-300'
                              }`}>
                              {paymentMethod === 'momo' && (
                                <CheckCircle className="w-4 h-4 text-white" />
                              )}
                            </div>
                            </div>
                          </div>
                        </div>
                        )}
                      </div>

                      {/* Payment Method Benefits */}
                      {paymentMethod && (
                        <div className="mt-4 p-4 rounded-lg bg-gray-50 border">
                          <div className="text-sm font-medium text-gray-900 mb-2">
                            {paymentMethod === 'stripe' ? '💳 Card Payment Benefits:' : '📱 MoMo Payment Benefits:'}
                          </div>
                          <ul className="text-xs text-gray-600 space-y-1">
                            {paymentMethod === 'stripe' ? (
                              <>
                                <li>• Instant payment confirmation</li>
                                <li>• International cards accepted</li>
                                <li>• Bank-level security encryption</li>
                                <li>• Automatic receipt via email</li>
                              </>
                            ) : (
                              <>
                                <li>• No need for bank cards</li>
                                <li>• Pay directly from your phone</li>
                                <li>• Familiar MTN MoMo interface</li>
                                <li>• Supports all MTN Ghana numbers</li>
                              </>
                            )}
                          </ul>
                        </div>
                      )}
                    </div>
                  )}

                  {/* MTN MoMo Phone Input - only show for payment required countries */}
                  {countryRequiresPayment && paymentMethod === 'momo' && (
                    <div className="mt-6 space-y-4">
                      <div className="p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
                        <Label htmlFor="momoPhone" className="text-sm font-medium text-gray-700">
                          MTN Mobile Money Number
                        </Label>
                        <Input
                          id="momoPhone"
                          type="tel"
                          value={momoPhone}
                          onChange={(e) => setMomoPhone(e.target.value)}
                          placeholder="+233 XX XXX XXXX"
                          className="mt-2"
                        />
                        <p className="text-xs text-gray-600 mt-2">
                          Enter your registered MTN MoMo number. You'll receive a prompt to authorize the payment.
                        </p>
                      </div>
                      
                      {/* Currency Conversion Display */}
                      {countryRequiresPayment && exchangeRate && (
                        <div className="p-4 bg-green-50 border border-green-200 rounded-lg">
                          <div className="flex items-center gap-2 mb-2">
                            <div className="w-5 h-5 bg-green-100 rounded-full flex items-center justify-center">
                              <span className="text-green-600 text-xs">₵</span>
                            </div>
                            <span className="font-medium text-green-800">Payment in Ghanaian Cedis</span>
                          </div>
                          <div className="space-y-1 text-sm">
                            <div className="flex justify-between">
                              <span className="text-gray-600">Order Total (USD):</span>
                              <span className="font-medium">${(total / 100).toFixed(2)}</span>
                            </div>
                            <div className="flex justify-between">
                              <span className="text-gray-600">You'll be charged (GHS):</span>
                              <span className="font-bold text-green-700">
                                GH₵ {((total / 100) * exchangeRate.rate).toFixed(2)}
                              </span>
                            </div>
                            <div className="text-xs text-gray-500 mt-2 pt-2 border-t border-green-200">
                              Exchange Rate: {exchangeRate.display}
                              {exchangeRate.is_cached && ' (cached)'}
                              {exchangeRate.is_fallback && ' (estimated)'}
                            </div>
                          </div>
                        </div>
                      )}
                    </div>
                  )}

                  {/* MoMo Status Display */}
                  {countryRequiresPayment && momoRef && (
                    <div className="mt-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
                      <div className="flex items-center gap-2 mb-2">
                        <CheckCircle className="w-5 h-5 text-blue-600" />
                        <span className="font-medium text-blue-900">Payment Initiated</span>
                      </div>
                      <div className="space-y-1 text-sm">
                        <div>Reference: <span className="font-mono font-medium">{momoRef}</span></div>
                        <div>Status: <Badge variant={momoStatus === 'success' ? 'default' : 'secondary'}>{momoStatus}</Badge></div>
                        {momoConversion && (
                          <div className="mt-2 p-2 bg-white rounded border">
                            <div className="text-xs text-gray-600">Payment Amount:</div>
                            <div className="font-medium text-green-700">{momoConversion.charged_amount}</div>
                            <div className="text-xs text-gray-500">{momoConversion.rate_note}</div>
                          </div>
                        )}
                      </div>
                      {momoStatus === 'pending' && (
                        <p className="text-xs text-blue-600 mt-2">
                          Please check your phone for the MoMo authorization prompt.
                        </p>
                      )}
                    </div>
                  )}

                  {/* Payment/Confirmation Button */}
                  <div className="mt-6 space-y-3">
                    {countryRequiresPayment && !paymentMethod && (
                      <div className="text-center text-sm text-gray-500 bg-gray-50 p-3 rounded-lg">
                        👆 Choose your preferred payment method above to continue
                      </div>
                    )}

                    <Button
                      onClick={handlePay}
                      disabled={processing || (countryRequiresPayment && !paymentMethod) || !form.email || !form.address}
                      className={`w-full h-12 text-lg font-medium transition-all duration-200 ${
                        !countryRequiresPayment
                          ? 'bg-green-600 hover:bg-green-700'
                          : !paymentMethod
                            ? 'bg-gray-300 hover:bg-gray-300 cursor-not-allowed'
                            : paymentMethod === 'stripe'
                              ? 'bg-blue-600 hover:bg-blue-700'
                              : 'bg-yellow-600 hover:bg-yellow-700'
                        }`}
                      size="lg"
                    >
                      {processing ? (
                        <div className="flex items-center gap-2">
                          <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                          {countryRequiresPayment ? 'Processing Payment...' : 'Confirming Order...'}
                        </div>
                      ) : !countryRequiresPayment ? (
                        <div className="flex items-center gap-2">
                          <CheckCircle className="w-4 h-4" />
                          Confirm Order - No Payment Required
                        </div>
                      ) : !paymentMethod ? (
                        <div className="flex items-center gap-2">
                          <AlertCircle className="w-4 h-4" />
                          Select Payment Method First
                        </div>
                      ) : paymentMethod === 'stripe' ? (
                        <div className="flex items-center gap-2">
                          <CreditCard className="w-4 h-4" />
                          Pay {formatPrice(total)} with Card
                        </div>
                      ) : (
                        <div className="flex items-center gap-2">
                          <Smartphone className="w-4 h-4" />
                          Pay {formatPrice(total)} with MoMo
                        </div>
                      )}
                    </Button>

                    {/* Payment method specific info */}
                    {!countryRequiresPayment ? (
                      <div className="text-xs text-center text-green-600 bg-green-50 p-2 rounded">
                        🎉 Your order will be confirmed immediately without payment
                      </div>
                    ) : paymentMethod === 'stripe' ? (
                      <div className="text-xs text-center text-gray-500">
                        You'll be redirected to Stripe's secure payment page
                      </div>
                    ) : paymentMethod === 'momo' ? (
                      <div className="text-xs text-center text-gray-500">
                        You'll receive a prompt on your MTN phone to authorize payment
                      </div>
                    ) : null}
                  </div>
                  </CardContent>
                </Card>
              </motion.div>
            </div>

            {/* Order Summary Sidebar */}
            <div className="lg:col-span-1">
              <motion.div
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.3, delay: 0.25 }}
              >
                <Card className="sticky top-4">
                <CardHeader>
                  <CardTitle>Order Summary</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  {/* Cart Items */}
                  <div className="space-y-3">
                    {state.items.map((item) => (
                      <div key={item.id} className="flex items-center gap-3">
                        <div className="w-12 h-12 bg-gray-100 rounded-lg flex items-center justify-center">
                          <img
                            src={item.image}
                            alt={item.title}
                            className="w-10 h-10 object-cover rounded"
                          />
                        </div>
                        <div className="flex-1 min-w-0">
                          <div className="text-sm font-medium truncate">{item.title}</div>
                          <div className="text-xs text-gray-500">Qty: {item.quantity}</div>
                        </div>
                        <div className="text-sm font-medium">
                          {formatPrice(item.price * item.quantity)}
                        </div>
                      </div>
                    ))}
                  </div>

                  <Separator />

                  {/* Price Breakdown */}
                  <div className="space-y-2 text-sm">
                    <div className="flex justify-between">
                      <span>Subtotal</span>
                      <span>{formatPrice(subtotal)}</span>
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
                    
                    <div className="flex justify-between">
                      <span className="flex items-center gap-1">
                        Shipping
                        {selectedCountry && selectedCountry.code !== 'GH' && (
                          <span className="text-xs text-gray-500">({shippingZone.name})</span>
                        )}
                      </span>
                      <span>
                        {finalShipping === 0 ? (
                          <span className="text-green-600">
                            Free {freeShippingFromPromo && appliedPromoCode && (
                              <span className="text-xs bg-green-100 text-green-800 px-2 py-0.5 rounded-full ml-1">
                                {appliedPromoCode.code}
                              </span>
                            )}
                          </span>
                        ) : (
                          formatPrice(finalShipping)
                        )}
                      </span>
                    </div>
                    
                    {finalShipping === 0 && freeShippingFromPromo ? (
                      <div className="text-xs text-green-600">
                        🎉 Free shipping applied with promo code
                      </div>
                    ) : finalShipping === 0 ? (
                      <div className="text-xs text-green-600">
                        🎉 Free shipping included
                      </div>
                    ) : (
                      <div className="text-xs text-gray-500">
                        Shipping calculated per product
                      </div>
                    )}
                    
                    <div className="flex justify-between">
                      <span>Tax (5%)</span>
                      <span>{formatPrice(tax)}</span>
                    </div>
                    
                    {selectedCountry && selectedCountry.code !== 'GH' && (
                      <div className="text-xs text-amber-600 bg-amber-50 p-2 rounded">
                        ⚠️ Additional customs fees may apply at destination
                      </div>
                    )}
                  </div>

                  <Separator />

                  <div className="flex justify-between text-lg font-semibold">
                    <span>Total</span>
                    <span>{formatPrice(total)}</span>
                  </div>
                  
                  {selectedCountry && (
                    <div className="text-xs text-center text-gray-500">
                      Shipping to {selectedCountry.flag} {selectedCountry.name}
                    </div>
                  )}

                  {/* Promo Code Section */}
                  {!appliedPromoCode && (
                    <div className="border-t pt-4">
                      <div className="text-sm font-medium text-gray-900 mb-2 flex items-center gap-2">
                        <Tag className="w-4 h-4" />
                        Have a promo code?
                      </div>
                      <div className="text-xs text-gray-500 mb-3">
                        Go back to your cart to apply promo codes and see updated pricing.
                      </div>
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => navigate('/cart')}
                        className="w-full text-xs"
                      >
                        Apply Promo Code in Cart
                      </Button>
                    </div>
                  )}

                  {/* Security Badge */}
                  <div className="flex items-center gap-2 text-xs text-gray-500 bg-gray-50 p-3 rounded-lg">
                    <Shield className="w-4 h-4" />
                    <span>Your payment information is secure and encrypted</span>
                  </div>
                  </CardContent>
                </Card>
              </motion.div>
            </div>
          </div>
        </div>
      </motion.div>
      </PageTransition>
    </Layout>
  );
}
