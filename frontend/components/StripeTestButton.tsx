import React, { useState } from 'react';
import { Button } from './ui/button';
import { CreditCard, Loader2 } from 'lucide-react';
import { paymentService } from '../services/payments';

interface StripeTestButtonProps {
  amount?: number;
  productName?: string;
}

export const StripeTestButton: React.FC<StripeTestButtonProps> = ({ 
  amount = 25, // $25.00 in dollars
  productName = 'Test Product'
}) => {
  const [loading, setLoading] = useState(false);

  const handleStripePayment = async () => {
    setLoading(true);
    
    try {
      const response = await paymentService.createStripeCheckoutSession({
        items: [
          {
            title: productName,
            amount: amount,
            quantity: 1,
            image: 'https://via.placeholder.com/150'
          }
        ],
        success_url: `${window.location.origin}/order-confirmation?success=true`,
        cancel_url: window.location.href
      });

      // Redirect to Stripe Checkout
      window.location.href = response.url;
    } catch (error) {
      console.error('Stripe payment error:', error);
      alert('Failed to create checkout session. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Button
      onClick={handleStripePayment}
      disabled={loading}
      className="bg-blue-600 hover:bg-blue-700 text-white"
    >
      {loading ? (
        <>
          <Loader2 className="w-4 h-4 mr-2 animate-spin" />
          Creating checkout...
        </>
      ) : (
        <>
          <CreditCard className="w-4 h-4 mr-2" />
          Pay ${(amount / 100).toFixed(2)} with Stripe
        </>
      )}
    </Button>
  );
};

export default StripeTestButton;