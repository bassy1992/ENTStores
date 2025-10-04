# Country-Based Checkout Flow Implementation

## Overview

This implementation provides different checkout experiences based on the customer's shipping country:

- **Payment Required Countries**: USA, Ghana, UK, and European Union countries
- **Free Checkout Countries**: All other countries worldwide

## How It Works

### Payment Required Countries
Countries: `US`, `GH`, `GB`, and all EU countries (`DE`, `FR`, `IT`, `ES`, etc.)

**Flow:**
1. Customer selects shipping country
2. Payment methods are shown (Stripe for cards, MoMo for Ghana)
3. Customer completes payment
4. Order is created with "processing" status
5. Confirmation email sent

### Free Checkout Countries
Countries: All others (Nigeria, Brazil, Kenya, Japan, etc.)

**Flow:**
1. Customer selects shipping country
2. No payment methods shown
3. Green "Confirm Order - No Payment Required" button displayed
4. Order is created immediately with "confirmed" status
5. Payment method set to "free_checkout"
6. Confirmation email sent with special messaging

## Backend Implementation

### New Endpoint
- `POST /api/payments/create-free-order/` - Creates orders without payment for eligible countries

### Modified Endpoint
- `POST /api/payments/create-order/` - Enhanced to handle country-based logic

### Key Features
- Country validation
- Automatic payment method assignment
- Stock validation for all orders
- Email notifications for both flows
- Order status differentiation

## Frontend Implementation

### New Utilities
- `frontend/utils/countryPaymentRules.ts` - Country classification logic
- Functions: `requiresPayment()`, `getCheckoutFlow()`, `getCheckoutMessage()`

### Modified Components
- `frontend/pages/Checkout.tsx` - Dynamic UI based on country
- Different payment method displays
- Country-specific messaging
- Conditional button text and behavior

### User Experience
- **Payment Countries**: Traditional checkout with payment selection
- **Free Countries**: Simplified confirmation flow with clear messaging
- Automatic country detection and flow switching
- Clear explanations of what happens next

## Configuration

### Payment Required Countries List
Located in both:
- Backend: `backend/shop/payment_views.py` (line ~350)
- Frontend: `frontend/utils/countryPaymentRules.ts`

To modify which countries require payment, update the `PAYMENT_REQUIRED_COUNTRIES` array in both files.

### Current Payment Required Countries
- **US** - United States
- **GH** - Ghana  
- **GB** - United Kingdom
- **EU Countries**: DE, FR, IT, ES, NL, BE, CH, AT, SE, NO, DK, FI, IE, PT, GR, PL, CZ, HU, SK, SI, HR, RO, BG, EE, LV, LT, LU, MT, CY

## Testing

Use the provided test script:
```bash
python test_country_checkout_flow.py
```

This tests:
- Payment required countries (USA, Ghana)
- Free checkout countries (Nigeria, Brazil)
- Invalid scenarios (trying free checkout for payment countries)

## API Response Examples

### Payment Required Country Response
```json
{
  "order_id": "ORD12345678",
  "status": "created",
  "message": "Order created successfully",
  "email_sent": true,
  "requires_payment": true,
  "payment_method": "stripe",
  "order_status": "processing"
}
```

### Free Checkout Country Response
```json
{
  "order_id": "ORD87654321",
  "status": "confirmed",
  "message": "Order confirmed successfully - No payment required",
  "email_sent": true,
  "payment_method": "free_checkout",
  "shipping_country": "NG"
}
```

## Email Notifications

Both flows send confirmation emails, but with different messaging:
- **Payment countries**: Standard order confirmation
- **Free countries**: Special messaging explaining the process and next steps

## Security Considerations

- Country validation on both frontend and backend
- Payment method validation for payment-required countries
- Stock validation for all orders regardless of payment flow
- Proper order status management

## Future Enhancements

1. **Admin Dashboard**: View and manage free checkout orders
2. **Payment Collection**: Tools for collecting payment from free checkout orders
3. **Country Rules Management**: Admin interface to modify country rules
4. **Analytics**: Track conversion rates by country and checkout type
5. **Fraud Prevention**: Additional validation for high-risk countries