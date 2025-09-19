"""
Email service for handling all email communications in the shop.
"""

from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)


class EmailService:
    """Service class for handling email operations."""
    
    @staticmethod
    def get_email_context(order=None, **kwargs):
        """Get common context variables for email templates."""
        context = {
            'store_name': 'ENTstore',
            'store_url': 'https://entstore.com',  # Update with your actual domain
            'store_logo_url': 'https://entstore.com/static/images/logo.png',  # Update with your logo URL
            'support_email': settings.ADMIN_EMAIL,
            'current_year': timezone.now().year,
        }
        
        if order:
            # Handle both total_amount (mock orders) and total (real orders)
            total = getattr(order, 'total_amount', None) or getattr(order, 'total', 0)
            if hasattr(order, 'total') and order.total:
                total = order.total / 100  # Convert from cents to dollars
            
            context.update({
                'order_id': order.id,
                'customer_name': order.customer_name,
                'customer_email': order.customer_email,
                'order_total': f"${total:.2f}",
                'order_date': order.created_at,
                'order_status': order.status,
            })
        
        # Add any additional context
        context.update(kwargs)
        return context
    
    @staticmethod
    def send_order_confirmation(order, order_items=None):
        """Send order confirmation email to customer."""
        try:
            context = EmailService.get_email_context(
                order=order,
                order_items=order_items,
                estimated_delivery="3-5 business days"
            )
            
            # Render email templates
            html_content = render_to_string('emails/order_confirmation.html', context)
            
            # Create email
            email = EmailMultiAlternatives(
                subject=f'Order Confirmation - {order.id}',
                body=f'Thank you for your order #{order.id}. Your order has been confirmed and is being processed.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[order.customer_email],
            )
            email.attach_alternative(html_content, "text/html")
            
            # Send email
            email.send()
            logger.info(f"Order confirmation email sent for order {order.id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send order confirmation email for order {order.id}: {str(e)}")
            return False
    
    @staticmethod
    def send_admin_notification(order, order_items=None):
        """Send new order notification to admin."""
        try:
            # Determine if this is a high-value order
            total = getattr(order, 'total_amount', None) or (getattr(order, 'total', 0) / 100)
            is_high_value = total > 500  # Adjust threshold as needed
            
            context = EmailService.get_email_context(
                order=order,
                order_items=order_items,
                is_high_value=is_high_value,
                items_count=len(order_items) if order_items else 0,
                admin_url='https://entstore.com/admin/',  # Update with your admin URL
                payment_method=getattr(order, 'payment_method', 'Not specified')
            )
            
            # Render email template
            html_content = render_to_string('emails/admin_new_order.html', context)
            
            # Create email
            email = EmailMultiAlternatives(
                subject=f'🛒 New Order #{order.id} - ${total:.2f}',
                body=f'A new order #{order.id} has been placed by {order.customer_name} for ${total:.2f}.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[settings.ADMIN_EMAIL],
            )
            email.attach_alternative(html_content, "text/html")
            
            # Send email
            email.send()
            logger.info(f"Admin notification email sent for order {order.id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send admin notification email for order {order.id}: {str(e)}")
            return False
    
    @staticmethod
    def send_shipping_confirmation(order, tracking_number=None, tracking_url=None, carrier=None, estimated_days=3, delivery_instructions=None):
        """Send shipping confirmation email to customer."""
        try:
            # Generate tracking URL if not provided but tracking number exists
            if tracking_number and not tracking_url:
                tracking_url = EmailService._generate_tracking_url(tracking_number, carrier)
            
            # Get order items for the email
            order_items = []
            if hasattr(order, 'items'):
                for item in order.items.all():
                    order_items.append({
                        'name': item.product.title,
                        'quantity': item.quantity,
                        'price': f"${item.unit_price / 100:.2f}",
                        'total': f"${item.total_price / 100:.2f}"
                    })
            
            # Prepare shipping address
            shipping_address = None
            if hasattr(order, 'shipping_address') and order.shipping_address:
                shipping_address = {
                    'name': order.customer_name,
                    'address_line_1': order.shipping_address,
                    'city': order.shipping_city,
                    'country': order.shipping_country,
                    'postal_code': order.shipping_postal_code,
                }
            
            context = EmailService.get_email_context(
                order=order,
                tracking_number=tracking_number,
                tracking_url=tracking_url,
                shipping_carrier=carrier or "Standard Shipping",
                shipped_date=timezone.now(),
                estimated_delivery_date=timezone.now() + timezone.timedelta(days=estimated_days),
                delivery_instructions=delivery_instructions or "Package will be left at your door if no one is available to receive it.",
                order_items=order_items,
                shipping_address=shipping_address,
                support_phone="1-800-ENTSTORE"  # Add support phone
            )
            
            # Render email template
            html_content = render_to_string('emails/shipping_confirmation.html', context)
            
            # Create email
            email = EmailMultiAlternatives(
                subject=f'📦 Your Order #{order.id} Has Shipped!',
                body=f'Great news! Your order #{order.id} has been shipped and is on its way to you. {f"Track it here: {tracking_url}" if tracking_url else ""}',
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[order.customer_email],
            )
            email.attach_alternative(html_content, "text/html")
            
            # Send email
            email.send()
            logger.info(f"Shipping confirmation email sent for order {order.id} with tracking: {tracking_number}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send shipping confirmation email for order {order.id}: {str(e)}")
            return False
    
    @staticmethod
    def _generate_tracking_url(tracking_number, carrier=None):
        """Generate tracking URL based on carrier."""
        carrier_urls = {
            'ups': f'https://www.ups.com/track?tracknum={tracking_number}',
            'fedex': f'https://www.fedex.com/fedextrack/?tracknumbers={tracking_number}',
            'usps': f'https://tools.usps.com/go/TrackConfirmAction?qtc_tLabels1={tracking_number}',
            'dhl': f'https://www.dhl.com/en/express/tracking.html?AWB={tracking_number}',
        }
        
        if carrier and carrier.lower() in carrier_urls:
            return carrier_urls[carrier.lower()]
        
        # Default to a generic tracking page or return None
        return f'https://track.example.com/{tracking_number}'
    
    @staticmethod
    def send_status_update(order, new_status, update_message=None, tracking_number=None, tracking_url=None):
        """Send order status update email to customer."""
        try:
            # Define next steps based on status
            next_steps_map = {
                'confirmed': 'We are preparing your order for processing.',
                'processing': 'Your order is being prepared and will ship soon.',
                'shipped': 'Your order is on its way! You should receive it within 3-5 business days.',
                'delivered': 'Thank you for your purchase! We hope you love your items.',
                'cancelled': 'Your order has been cancelled. If you have any questions, please contact support.'
            }
            
            context = EmailService.get_email_context(
                order=order,
                new_status=new_status,
                update_date=timezone.now(),
                update_message=update_message,
                tracking_number=tracking_number,
                tracking_url=tracking_url,
                next_steps=next_steps_map.get(new_status.lower(), '')
            )
            
            # Render email template
            html_content = render_to_string('emails/order_status_update.html', context)
            
            # Create email
            email = EmailMultiAlternatives(
                subject=f'Order Update - #{order.id} Status: {new_status}',
                body=f'Your order #{order.id} status has been updated to: {new_status}',
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[order.customer_email],
            )
            email.attach_alternative(html_content, "text/html")
            
            # Send email
            email.send()
            logger.info(f"Status update email sent for order {order.id} - Status: {new_status}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send status update email for order {order.id}: {str(e)}")
            return False
    
    @staticmethod
    def test_email_configuration():
        """Test email configuration by sending a test email."""
        try:
            send_mail(
                subject='ENTstore Email Configuration Test',
                message='This is a test email to verify email configuration is working correctly.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.ADMIN_EMAIL],
                fail_silently=False,
            )
            logger.info("Test email sent successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to send test email: {str(e)}")
            return False


# Convenience functions for easy importing
def send_order_confirmation_email(order, order_items=None):
    """Convenience function to send order confirmation email."""
    return EmailService.send_order_confirmation(order, order_items)


def send_admin_notification_email(order, order_items=None):
    """Convenience function to send admin notification email."""
    return EmailService.send_admin_notification(order, order_items)


def send_shipping_confirmation_email(order, tracking_number=None, tracking_url=None, carrier=None, estimated_days=3, delivery_instructions=None):
    """Convenience function to send shipping confirmation email."""
    return EmailService.send_shipping_confirmation(order, tracking_number, tracking_url, carrier, estimated_days, delivery_instructions)


def send_status_update_email(order, new_status, update_message=None, tracking_number=None, tracking_url=None):
    """Convenience function to send status update email."""
    return EmailService.send_status_update(order, new_status, update_message, tracking_number, tracking_url)


def test_email_setup():
    """Convenience function to test email configuration."""
    return EmailService.test_email_configuration()