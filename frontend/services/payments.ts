// Payment service for Stripe and MTN MoMo integration

// Prefer VITE_API_BASE_URL when provided. In development, default to local backend.
const _env = (import.meta as any).env;
const API_BASE_URL = _env.VITE_API_BASE_URL || (_env.DEV ? 'http://localhost:8000/api/payments' : 'https://entstores.onrender.com/api/payments');

// Stripe configuration
export const STRIPE_PUBLISHABLE_KEY = 'pk_test_51S8JhCPc249cE7TRlO5jHggCQiBAt31e1rKCioN5KlmCkh03q5pBpWZIKjyFS6hj8rZQ1DlMeQU6DHqoXUubcl4Y00wRmW9uId';

export interface PaymentItem {
  title: string;
  amount: number;
  quantity: number;
  image: string;
  product_id?: string;
}

export interface StripeCheckoutRequest {
  items: PaymentItem[];
  success_url: string;
  cancel_url: string;
}

export interface StripeCheckoutResponse {
  url: string;
  session_id: string;
}

export interface MoMoPaymentRequest {
  phone: string;
  amount: number;
  currency: string;
}

export interface MoMoPaymentResponse {
  reference: string;
  status: string;
  message: string;
}

export interface MoMoStatusResponse {
  reference: string;
  status: 'pending' | 'success' | 'failed';
  phone: string;
  amount: number;
  currency: string;
}

export interface OrderRequest {
  customer_email: string;
  customer_name: string;
  shipping_address: string;
  shipping_city: string;
  shipping_country: string;
  shipping_postal_code: string;
  subtotal: number;
  shipping_cost: number;
  tax_amount: number;
  total: number;
  payment_method: string;
  payment_reference: string;
  items: Array<{
    product_id: string;
    quantity: number;
    unit_price: number;
  }>;
}

export interface OrderResponse {
  order_id: string;
  status: string;
  message: string;
}

export const paymentService = {
  // Stripe payments
  async createStripeCheckoutSession(request: StripeCheckoutRequest): Promise<StripeCheckoutResponse> {
    const response = await fetch(`${API_BASE_URL}/stripe/create-checkout-session/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error || 'Failed to create Stripe checkout session');
    }

    return response.json();
  },

  // MTN MoMo payments
  async initiateMoMoPayment(request: MoMoPaymentRequest): Promise<MoMoPaymentResponse> {
    const response = await fetch(`${API_BASE_URL}/momo/initiate/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error || 'Failed to initiate MoMo payment');
    }

    return response.json();
  },

  async checkMoMoStatus(reference: string): Promise<MoMoStatusResponse> {
    const response = await fetch(`${API_BASE_URL}/momo/status/${reference}/`);

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error || 'Failed to check MoMo payment status');
    }

    return response.json();
  },

  // Order creation
  async createOrder(request: OrderRequest): Promise<OrderResponse> {
    const response = await fetch(`${API_BASE_URL}/create-order/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error || 'Failed to create order');
    }

    return response.json();
  },

  // Test endpoint
  async testPayments(): Promise<any> {
    const response = await fetch(`${API_BASE_URL}/test/`);
    return response.json();
  },
};

// Utility functions
export const formatPhoneNumber = (phone: string): string => {
  // Clean phone number
  let cleaned = phone.replace(/\D/g, '');
  
  // Add Ghana country code if not present
  if (!cleaned.startsWith('233')) {
    if (cleaned.startsWith('0')) {
      cleaned = '233' + cleaned.substring(1);
    } else {
      cleaned = '233' + cleaned;
    }
  }
  
  return '+' + cleaned;
};

export const validatePaymentForm = (form: any, paymentMethod: string): string[] => {
  const errors: string[] = [];
  
  if (!form.email) errors.push('Email is required');
  if (!form.name) errors.push('Name is required');
  if (!form.address) errors.push('Address is required');
  if (!form.city) errors.push('City is required');
  if (!form.country) errors.push('Country is required');
  
  if (!paymentMethod) {
    errors.push('Please select a payment method');
  }
  
  return errors;
};