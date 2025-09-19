# Email System Guide

This guide explains how to set up and use the email system in your ENTstore application.

## Features

The email system includes:

- **Order Confirmation Emails** - Sent to customers when orders are placed
- **Admin Notifications** - Sent to store admins when new orders are received
- **Shipping Confirmations** - Sent when orders are shipped with tracking info
- **Status Updates** - Sent when order status changes
- **Professional HTML Templates** - Responsive, branded email templates
- **Secure Configuration** - All credentials stored in environment variables

## Setup Instructions

### 1. Environment Variables

Copy `.env.example` to `.env` and fill in your actual values:

```bash
cp .env.example .env
```

Update the following variables in your `.env` file:

```env
# Email Configuration (Brevo SMTP)
EMAIL_HOST_USER=your_brevo_smtp_user
EMAIL_HOST_PASSWORD=your_brevo_smtp_password

# Stripe Payment Settings (if using Stripe)
STRIPE_PUBLISHABLE_KEY=pk_test_your_publishable_key_here
STRIPE_SECRET_KEY=sk_test_your_secret_key_here
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret_here
```

### 2. Install Dependencies

Make sure you have python-dotenv installed:

```bash
pip install python-dotenv
```

### 3. Test Email Configuration

Test your email setup:

```bash
python manage.py test_email --type=test
```

Test specific email types:

```bash
# Test order confirmation email
python manage.py test_email --type=confirmation --email=your-email@example.com

# Test admin notification
python manage.py test_email --type=admin

# Test shipping confirmation
python manage.py test_email --type=shipping --email=your-email@example.com

# Test status update
python manage.py test_email --type=status --email=your-email@example.com
```

## Usage

### In Your Views/Models

```python
from shop.email_service import (
    send_order_confirmation_email,
    send_admin_notification_email,
    send_shipping_confirmation_email,
    send_status_update_email
)

# When an order is created
def create_order(request):
    # ... create order logic ...
    
    # Send confirmation to customer
    send_order_confirmation_email(order, order_items)
    
    # Send notification to admin
    send_admin_notification_email(order, order_items)

# When order status changes
def update_order_status(order, new_status):
    order.status = new_status
    order.save()
    
    # Send status update to customer
    send_status_update_email(
        order, 
        new_status, 
        update_message="Your order status has been updated."
    )

# When order ships
def ship_order(order, tracking_number):
    send_shipping_confirmation_email(
        order,
        tracking_number=tracking_number,
        tracking_url=f"https://ups.com/track?tracknum={tracking_number}",
        carrier="UPS"
    )
```

### Email Templates

The system includes these HTML email templates:

- `emails/order_confirmation.html` - Customer order confirmation
- `emails/admin_new_order.html` - Admin new order notification
- `emails/shipping_confirmation.html` - Shipping confirmation with tracking
- `emails/order_status_update.html` - Order status updates

### Customization

#### Update Store Information

Edit `backend/shop/email_service.py` and update the `get_email_context` method:

```python
context = {
    'store_name': 'Your Store Name',
    'store_url': 'https://yourstore.com',
    'store_logo_url': 'https://yourstore.com/logo.png',
    'support_email': 'support@yourstore.com',
    # ...
}
```

#### Customize Email Templates

The email templates are located in `backend/shop/templates/emails/`. You can:

- Modify the HTML structure
- Update colors and styling
- Add your branding
- Change the layout

#### Add New Email Types

1. Create a new HTML template in `backend/shop/templates/emails/`
2. Add a new method to the `EmailService` class
3. Create a convenience function for easy importing

## Email Configuration Details

### Brevo SMTP Settings

The system is configured to use Brevo (formerly Sendinblue) SMTP:

- **Host**: smtp-relay.brevo.com
- **Port**: 587
- **TLS**: Enabled
- **Authentication**: Required

### Email Addresses

Configure these in `settings.py`:

- `DEFAULT_FROM_EMAIL` - The "from" address for customer emails
- `ADMIN_EMAIL` - Where admin notifications are sent
- `SERVER_EMAIL` - Used for server error emails

## Security Features

- All API keys and passwords are stored in environment variables
- The `.env` file is gitignored to prevent accidental commits
- Email templates are safe from XSS attacks using Django's template system

## Troubleshooting

### Common Issues

1. **Emails not sending**
   - Check your `.env` file has correct credentials
   - Verify Brevo account is active and verified
   - Check Django logs for error messages

2. **Templates not loading**
   - Ensure templates are in `backend/shop/templates/emails/`
   - Check that `shop` app is in `INSTALLED_APPS`

3. **Environment variables not loading**
   - Verify `python-dotenv` is installed
   - Check `.env` file is in the project root
   - Ensure `load_dotenv()` is called in settings.py

### Debug Mode

Enable debug logging in `settings.py`:

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

## Production Considerations

1. **Use a dedicated email service** - Brevo, SendGrid, or AWS SES
2. **Set up proper DNS records** - SPF, DKIM, DMARC
3. **Monitor email delivery** - Track bounces and complaints
4. **Use environment-specific settings** - Different configs for dev/staging/prod
5. **Implement email queues** - For high-volume applications, use Celery

## Support

If you need help with the email system:

1. Check the Django logs for error messages
2. Test with the management command: `python manage.py test_email`
3. Verify your Brevo account settings
4. Check that all environment variables are set correctly