# 💳 Payment Integration Setup - Stripe & MTN MoMo

Complete payment integration for the ENNC Shop checkout page with Stripe and MTN MoMo support.

## 🚀 **What's Implemented:**

### **Backend (Django)**
- ✅ Stripe Checkout Session creation
- ✅ MTN MoMo payment initiation (demo/sandbox)
- ✅ Payment status checking
- ✅ Order creation after successful payment
- ✅ Webhook handling for Stripe
- ✅ Test endpoints for development

### **Frontend (React)**
- ✅ Updated checkout page with proper API endpoints
- ✅ Payment service for API calls
- ✅ Form validation and error handling
- ✅ Real-time MoMo status checking
- ✅ Smooth payment flow with loading states

## 🔧 **Setup Instructions:**

### **1. Install Backend Dependencies**
```bash
cd backend
pip install stripe requests
```

### **2. Configure Stripe (Required for Production)**
Update `backend/myproject/settings.py`:
```python
# Get these from your Stripe Dashboard
STRIPE_PUBLISHABLE_KEY = 'pk_test_...'  # Your publishable key
STRIPE_SECRET_KEY = 'sk_test_...'       # Your secret key
STRIPE_WEBHOOK_SECRET = 'whsec_...'     # Your webhook secret
```

### **3. Configure MTN MoMo (Optional - Demo Mode Works)**
```python
# MTN MoMo Settings (for production)
MOMO_SUBSCRIPTION_KEY = 'your_momo_subscription_key'
MOMO_API_USER = 'your_momo_api_user'
MOMO_API_KEY = 'your_momo_api_key'
```

### **4. Restart Django Server**
```bash
cd backend
python manage.py runserver 8000
```

## 🧪 **Testing the Integration:**

### **1. Test Payment APIs**
Open `frontend/test-payments.html` in your browser to test:
- ✅ Configuration status
- ✅ Stripe checkout session creation
- ✅ MoMo payment initiation
- ✅ Order creation

### **2. Test Checkout Flow**
1. Add items to cart: http://localhost:8080/shop
2. Go to checkout: http://localhost:8080/checkout
3. Fill in customer details
4. Select payment method (Stripe or MoMo)
5. Complete payment

### **3. MoMo Test Numbers (Demo Mode)**
- `+233XXXXXXX1111` - Will succeed after 5 seconds
- `+233XXXXXXX2222` - Will fail after 3 seconds  
- `+233XXXXXXX0000` - Will stay pending

## 📡 **API Endpoints:**

### **Payment Endpoints:**
- `POST /api/payments/stripe/create-checkout-session/` - Create Stripe session
- `POST /api/payments/momo/initiate/` - Initiate MoMo payment
- `GET /api/payments/momo/status/{reference}/` - Check MoMo status
- `POST /api/payments/create-order/` - Create order after payment
- `GET /api/payments/test/` - Test configuration

### **Legacy Endpoints (for frontend compatibility):**
- `POST /api/stripe/create-checkout-session/`
- `POST /api/momo/initiate/`
- `GET /api/momo/status/{reference}/`

## 💳 **Stripe Integration:**

### **How it Works:**
1. User selects Stripe payment
2. Frontend calls `/api/payments/stripe/create-checkout-session/`
3. Backend creates Stripe session and returns checkout URL
4. User is redirected to Stripe's secure checkout page
5. After payment, user returns to success/cancel URL
6. Webhook handles payment confirmation (optional)

### **Test Cards (Stripe Test Mode):**
- `4242 4242 4242 4242` - Visa (success)
- `4000 0000 0000 0002` - Card declined
- `4000 0000 0000 9995` - Insufficient funds

## 📱 **MTN MoMo Integration:**

### **How it Works:**
1. User enters phone number and selects MoMo
2. Frontend calls `/api/payments/momo/initiate/`
3. Backend initiates payment (demo mode simulates API)
4. Frontend polls `/api/payments/momo/status/{reference}/` every 2 seconds
5. When status becomes 'success', order is completed

### **Demo Mode:**
- No actual MoMo API calls (for development)
- Simulates different scenarios based on phone number
- Real implementation would call MTN MoMo APIs

## 🔒 **Security Features:**

- ✅ CORS configured for frontend domain
- ✅ Input validation and sanitization
- ✅ Error handling and logging
- ✅ Secure payment processing (Stripe handles card data)
- ✅ Phone number formatting and validation
- ✅ Transaction reference generation

## 📦 **Order Management:**

After successful payment:
1. Order is created in database with unique ID
2. Order items are linked to products
3. Customer details are stored
4. Payment reference is saved
5. Order status is set to 'processing'

## 🚨 **Important Notes:**

### **For Production:**
1. **Replace test Stripe keys** with live keys
2. **Implement real MTN MoMo API** calls
3. **Set up Stripe webhooks** for payment confirmation
4. **Use secure HTTPS** for all payment endpoints
5. **Implement proper error logging** and monitoring
6. **Add rate limiting** to prevent abuse

### **Current Status:**
- ✅ **Stripe**: Ready for production (just add real keys)
- ✅ **MoMo**: Demo mode (needs real API integration)
- ✅ **Orders**: Fully functional
- ✅ **Frontend**: Complete payment flow

## 🎯 **User Experience:**

### **Stripe Flow:**
1. Select "Credit/Debit Card"
2. Click "Pay with Card"
3. Redirected to Stripe checkout
4. Complete payment securely
5. Return to order confirmation

### **MoMo Flow:**
1. Select "MTN Mobile Money"
2. Enter phone number
3. Click "Pay with MoMo"
4. See real-time status updates
5. Payment completes automatically

The checkout page now supports both payment methods with a smooth, professional user experience! 🎉

## 🔗 **Quick Links:**
- **Checkout Page**: http://localhost:8080/checkout
- **Payment Test**: `frontend/test-payments.html`
- **Django Admin**: http://localhost:8000/admin/
- **API Test**: http://localhost:8000/api/payments/test/