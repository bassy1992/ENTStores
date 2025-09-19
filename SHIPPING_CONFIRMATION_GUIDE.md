# 📦 Shipping Confirmation System Guide

This guide covers the enhanced shipping confirmation system implemented for the ENTstore e-commerce platform.

## 🎯 Overview

The shipping confirmation system provides:
- **Automated email notifications** when orders are shipped
- **Professional HTML email templates** with tracking information
- **Admin interface enhancements** for shipping management
- **API endpoints** for integration with shipping providers
- **Customer tracking pages** for order status checking
- **Webhook support** for automatic status updates

## 📧 Email Features

### Enhanced Shipping Confirmation Email
- **Professional design** matching brand colors and style
- **Tracking number display** with carrier information
- **Delivery tips** and instructions for customers
- **Order items summary** showing what was shipped
- **Shipping address confirmation**
- **Responsive design** for mobile devices
- **Fallback logo handling** if images fail to load

### Automatic Email Triggers
- **Status change detection**: Emails sent automatically when order status changes
- **Shipping confirmation**: Sent when status changes to "shipped"
- **Status updates**: Sent for processing, delivered, and cancelled statuses
- **Tracking number generation**: Automatic tracking number creation

## 🔧 Admin Interface Enhancements

### Order Management
- **Enhanced order list** with shipping information display
- **Bulk actions** for marking orders as shipped
- **Manual shipping confirmation** email sending
- **Tracking number display** for shipped orders
- **Status color coding** for quick visual identification

### Admin Actions
```python
# Available admin actions:
- Mark selected orders as shipped
- Send shipping confirmation emails
- View tracking numbers
- Enhanced order details display
```

## 🌐 API Endpoints

### Shipping Webhook
```http
POST /shop/shipping/api/webhook/
Content-Type: application/json

{
    "order_id": "ORD123456",
    "status": "shipped",
    "tracking_number": "1Z999AA1234567890",
    "tracking_url": "https://www.ups.com/track?tracknum=1Z999AA1234567890",
    "carrier": "UPS",
    "estimated_delivery": "2024-01-15"
}
```

### Update Shipping Status
```http
POST /shop/shipping/api/update/
Content-Type: application/json

{
    "order_id": "ORD123456",
    "status": "shipped",
    "tracking_number": "TRK123456789",
    "carrier": "FedEx"
}
```

### Get Shipping Status
```http
GET /shop/shipping/api/status/ORD123456/
```

Response:
```json
{
    "order_id": "ORD123456",
    "status": "shipped",
    "status_display": "Shipped",
    "tracking_number": "ENTORD12345620241201",
    "customer_email": "customer@example.com",
    "customer_name": "John Doe",
    "shipping_address": {
        "address": "123 Main St",
        "city": "New York",
        "country": "United States",
        "postal_code": "10001"
    },
    "created_at": "2024-01-01T10:00:00Z",
    "updated_at": "2024-01-02T14:30:00Z"
}
```

## 📱 Customer Tracking Page

### Features
- **Visual status timeline** showing order progress
- **Tracking number display** with copy functionality
- **Order details** including items and shipping address
- **Responsive design** for mobile and desktop
- **Professional styling** matching the email templates

### URL Pattern
```
/shop/shipping/track/<order_id>/
```

Example: `/shop/shipping/track/ORD123456/`

## 🧪 Testing

### Management Command
```bash
# Test shipping confirmation emails
python manage.py test_shipping_email

# Create test order and send email
python manage.py test_shipping_email --create-test-order

# Test specific order
python manage.py test_shipping_email --order-id ORD123456

# Custom tracking number and carrier
python manage.py test_shipping_email --tracking-number TRK123 --carrier "UPS Ground"
```

### Test Script
```bash
# Run comprehensive test suite
python test_shipping_system.py
```

## 🔧 Configuration

### Email Settings
Ensure your Django settings include:
```python
# Email configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'your-smtp-server.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@domain.com'
EMAIL_HOST_PASSWORD = 'your-password'
DEFAULT_FROM_EMAIL = 'ENTstore <noreply@entstore.com>'
ADMIN_EMAIL = 'admin@entstore.com'
```

### Store Information
Update the email service with your store details:
```python
# In shop/email_service.py
context = {
    'store_name': 'Your Store Name',
    'store_url': 'https://yourstore.com',
    'store_logo_url': 'https://yourstore.com/logo.png',
    'support_email': 'support@yourstore.com',
    'support_phone': '1-800-YOUR-STORE',
}
```

## 📋 File Structure

```
backend/shop/
├── templates/emails/
│   ├── shipping_confirmation.html     # Enhanced shipping email template
│   ├── order_confirmation.html        # Order confirmation template
│   └── admin_new_order.html          # Admin notification template
├── templates/shipping/
│   └── tracking.html                  # Customer tracking page
├── management/commands/
│   └── test_shipping_email.py         # Test command for shipping emails
├── email_service.py                   # Enhanced email service
├── shipping_views.py                  # Shipping API endpoints
├── shipping_urls.py                   # Shipping URL configuration
├── models.py                          # Enhanced with email signals
└── admin.py                           # Enhanced admin interface
```

## 🚀 Usage Examples

### Programmatic Usage
```python
from shop.email_service import send_shipping_confirmation_email
from shop.models import Order

# Get order
order = Order.objects.get(id='ORD123456')

# Send shipping confirmation
success = send_shipping_confirmation_email(
    order=order,
    tracking_number='TRK123456789',
    carrier='UPS Ground',
    estimated_days=3,
    delivery_instructions='Package will be left at door if no one available.'
)
```

### Admin Interface
1. Go to Django Admin → Orders
2. Select orders to ship
3. Choose "Mark selected orders as shipped" action
4. Emails are sent automatically

### API Integration
```python
import requests

# Update order status via API
response = requests.post('http://yoursite.com/shop/shipping/api/update/', json={
    'order_id': 'ORD123456',
    'status': 'shipped',
    'tracking_number': 'TRK123456789',
    'carrier': 'UPS'
})
```

## 🎨 Customization

### Email Template Customization
1. Edit `backend/shop/templates/emails/shipping_confirmation.html`
2. Update colors, fonts, and layout as needed
3. Add your logo URL and brand information
4. Test with the management command

### Tracking Number Format
Customize tracking number generation in `models.py`:
```python
# Current format: ENT{order_id}{date}
tracking_number = f"ENT{instance.id}{timezone.now().strftime('%Y%m%d')}"

# Custom format example:
tracking_number = f"STORE{instance.id}{random.randint(1000, 9999)}"
```

### Carrier Integration
Add carrier-specific tracking URLs in `email_service.py`:
```python
carrier_urls = {
    'ups': f'https://www.ups.com/track?tracknum={tracking_number}',
    'fedex': f'https://www.fedex.com/fedextrack/?tracknumbers={tracking_number}',
    'usps': f'https://tools.usps.com/go/TrackConfirmAction?qtc_tLabels1={tracking_number}',
    'dhl': f'https://www.dhl.com/en/express/tracking.html?AWB={tracking_number}',
    'your_carrier': f'https://track.yourcarrier.com/{tracking_number}',
}
```

## 🔍 Troubleshooting

### Common Issues

1. **Emails not sending**
   - Check email configuration in settings
   - Verify SMTP credentials
   - Run `python manage.py test_shipping_email` to test

2. **Templates not loading**
   - Ensure templates are in correct directory
   - Check Django template settings
   - Verify file permissions

3. **Tracking numbers not generating**
   - Check order status change signals
   - Verify timezone settings
   - Test with management command

4. **API endpoints not working**
   - Check URL configuration
   - Verify CSRF settings for API endpoints
   - Test with curl or Postman

### Debug Mode
Enable debug logging in settings:
```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'shop.email_service': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}
```

## 📈 Future Enhancements

### Planned Features
- **SMS notifications** for shipping updates
- **Push notifications** for mobile apps
- **Advanced tracking** with delivery photos
- **Delivery scheduling** integration
- **Return shipping** management
- **Multi-package** shipment support

### Integration Opportunities
- **Shipping provider APIs** (UPS, FedEx, USPS)
- **Inventory management** systems
- **Customer service** platforms
- **Analytics and reporting** tools

## 📞 Support

For questions or issues with the shipping confirmation system:
1. Check this documentation
2. Run the test script: `python test_shipping_system.py`
3. Use the management command: `python manage.py test_shipping_email`
4. Check Django logs for error messages
5. Contact the development team

---

**Last Updated**: December 2024  
**Version**: 1.0  
**Compatibility**: Django 4.x+, Python 3.8+