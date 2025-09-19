import { useEffect, useState } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import Layout from '../components/layout/Layout';
import { Loader2, CheckCircle, AlertCircle } from 'lucide-react';
import { useCart } from '../context/cart';
import { formatPrice } from '../data/products';
import { API_ENDPOINTS, API_BASE_URL } from '../config/api';

export default function StripeSuccess() {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const { state: cartState, clear, getCheckoutData, clearCheckoutData } = useCart();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [processed, setProcessed] = useState(false);

  useEffect(() => {
    const sessionId = searchParams.get('session_id');
    
    if (!sessionId) {
      setError('No session ID found');
      setLoading(false);
      return;
    }

    // Prevent duplicate processing
    if (processed) {
      return;
    }

    // Verify the payment and create order
    const processOrder = async () => {
      setProcessed(true);
      try {
        // 1. Verify the Stripe session on backend
        const verifyResponse = await fetch(`${API_BASE_URL}/api/payments/stripe/verify-session/${sessionId}/`);
        const verifyData = await verifyResponse.json();

        if (!verifyResponse.ok || !verifyData.success) {
          console.error('Payment verification failed:', verifyData);
          throw new Error(`Payment verification failed: ${verifyData.error || verifyData.message || 'Unknown error'}`);
        }

        // 2. Get saved checkout data or use current cart
        const checkoutData = getCheckoutData();
        const items = checkoutData?.items || cartState.items;
        const total = checkoutData?.total || cartState.items.reduce((sum, item) => sum + (item.price * item.quantity), 0);
        
        const orderSummary = {
          id: `ORD${Date.now().toString().slice(-8)}`,
          total: total,
          items: items.map((item: any) => ({
            id: item.id,
            title: item.title,
            price: item.price,
            quantity: item.quantity
          })),
          payment_method: 'stripe',
          payment_reference: sessionId,
          customer_email: verifyData.customer_email,
          customer_name: verifyData.customer_name,
          form: checkoutData?.form
        };

        // 3. Create order in backend with proper shipping address
        try {
          const form = checkoutData?.form || {};
          const subtotal = checkoutData?.subtotal || total;
          const shipping = checkoutData?.shipping || 0;
          const tax = checkoutData?.tax || 0;
          
          console.log('Creating order with data:', {
            customer_email: verifyData.customer_email || form.email,
            customer_name: verifyData.customer_name || form.name,
            items: items.map((item: any) => ({
              product_id: item.id,
              quantity: item.quantity,
              unit_price: item.price
            }))
          });
          
          const orderResponse = await fetch(API_ENDPOINTS.CREATE_ORDER, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              customer_email: verifyData.customer_email || form.email || 'customer@example.com',
              customer_name: verifyData.customer_name || form.name || 'Customer',
              shipping_address: form.address || 'Address not provided',
              shipping_city: form.city || 'City not provided',
              shipping_country: form.country || 'Country not provided',
              shipping_postal_code: form.postal || '',
              subtotal: subtotal,
              shipping_cost: shipping,
              tax_amount: tax,
              total: total,
              payment_method: 'stripe',
              payment_reference: sessionId,
              items: items.map((item: any) => ({
                product_id: item.id,
                quantity: item.quantity,
                unit_price: item.price
              }))
            })
          });
          
          const orderResult = await orderResponse.json();
          console.log('Order creation result:', orderResult);
          
          if (!orderResponse.ok) {
            throw new Error(`Order creation failed: ${orderResult.error || 'Unknown error'}`);
          }
          
          console.log('✅ Order created successfully:', orderResult.order_id);
          
        } catch (orderError) {
          console.error('Failed to create order in backend:', orderError);
          // Continue anyway - we have the payment confirmation
        }

        // 4. Clear the cart and checkout data
        clear();
        clearCheckoutData();

        // 5. Navigate to order confirmation with order data
        navigate('/order-confirmation', { 
          state: orderSummary,
          replace: true 
        });

      } catch (err) {
        console.error('Error processing order:', err);
        setError('Failed to process your order. Please contact support.');
        setLoading(false);
        setProcessed(false); // Reset on error so user can retry
      }
    };

    processOrder();
  }, [searchParams, navigate, cartState, clear, processed]);

  if (loading) {
    return (
      <Layout>
        <div className="container mx-auto px-4 py-16 max-w-2xl text-center">
          <div className="flex flex-col items-center gap-4">
            <Loader2 className="w-12 h-12 animate-spin text-blue-600" />
            <h1 className="text-2xl font-bold">Processing Your Order</h1>
            <p className="text-gray-600">
              Please wait while we confirm your payment and prepare your order...
            </p>
          </div>
        </div>
      </Layout>
    );
  }

  if (error) {
    return (
      <Layout>
        <div className="container mx-auto px-4 py-16 max-w-2xl text-center">
          <div className="flex flex-col items-center gap-4">
            <AlertCircle className="w-12 h-12 text-red-600" />
            <h1 className="text-2xl font-bold text-red-600">Order Processing Error</h1>
            <p className="text-gray-600">{error}</p>
            <div className="flex gap-4 mt-6">
              <button
                onClick={() => navigate('/cart')}
                className="px-6 py-2 bg-gray-200 text-gray-800 rounded-md hover:bg-gray-300"
              >
                Return to Cart
              </button>
              <button
                onClick={() => navigate('/contact')}
                className="px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
              >
                Contact Support
              </button>
            </div>
          </div>
        </div>
      </Layout>
    );
  }

  return null;
}