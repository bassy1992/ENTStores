import { useState } from 'react';
import { useCart } from '../../context/cart';
import { apiService } from '../../services/api';
import { Tag, X } from 'lucide-react';

interface PromoCodeInputProps {
  className?: string;
  showTitle?: boolean;
}

export default function PromoCodeInput({ className = '', showTitle = true }: PromoCodeInputProps) {
  const { subtotal, appliedPromoCode, setAppliedPromoCode } = useCart();
  const [coupon, setCoupon] = useState('');
  const [couponError, setCouponError] = useState<string | null>(null);
  const [couponLoading, setCouponLoading] = useState(false);

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

  if (appliedPromoCode) {
    return (
      <div className={`bg-green-50 border border-green-200 rounded-lg p-4 ${className}`}>
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Tag className="w-4 h-4 text-green-600" />
            <div>
              <div className="font-medium text-green-800">
                Promo code applied: {appliedPromoCode.code}
              </div>
              {appliedPromoCode.description && (
                <div className="text-sm text-green-600">
                  {appliedPromoCode.description}
                </div>
              )}
            </div>
          </div>
          <button
            onClick={removeCoupon}
            className="text-green-600 hover:text-green-800 transition-colors"
            aria-label="Remove promo code"
          >
            <X className="w-4 h-4" />
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className={`bg-white rounded-lg border p-4 ${className}`}>
      {showTitle && (
        <div className="flex items-center gap-2 mb-3">
          <Tag className="w-4 h-4 text-gray-600" />
          <h3 className="font-medium text-gray-900">Promo Code</h3>
        </div>
      )}
      
      <div className="space-y-3">
        <div className="flex gap-2">
          <input
            value={coupon}
            onChange={(e) => setCoupon(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && applyCoupon(coupon)}
            placeholder="Enter promo code"
            className="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-sm"
            disabled={couponLoading}
          />
          <button
            onClick={() => applyCoupon(coupon)}
            disabled={couponLoading || !coupon.trim()}
            className="px-4 py-2 bg-gray-900 text-white rounded-lg font-medium hover:bg-gray-800 disabled:opacity-50 disabled:cursor-not-allowed transition-colors text-sm"
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
  );
}