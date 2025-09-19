"""
Django management command to test email functionality.
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from shop.email_service import EmailService
from shop.models import Order
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Test email functionality'

    def add_arguments(self, parser):
        parser.add_argument(
            '--type',
            type=str,
            choices=['test', 'confirmation', 'admin', 'shipping', 'status'],
            default='test',
            help='Type of email to test'
        )
        parser.add_argument(
            '--order-id',
            type=int,
            help='Order ID to use for testing (creates mock order if not provided)'
        )
        parser.add_argument(
            '--email',
            type=str,
            help='Email address to send test emails to'
        )

    def handle(self, *args, **options):
        email_type = options['type']
        order_id = options.get('order_id')
        test_email = options.get('email')

        self.stdout.write(f"Testing {email_type} email...")

        if email_type == 'test':
            success = EmailService.test_email_configuration()
            if success:
                self.stdout.write(
                    self.style.SUCCESS('✅ Test email sent successfully!')
                )
            else:
                self.stdout.write(
                    self.style.ERROR('❌ Failed to send test email. Check your email configuration.')
                )
            return

        # Create or get order for testing
        if order_id:
            try:
                order = Order.objects.get(id=order_id)
                self.stdout.write(f"Using existing order #{order.id}")
            except Order.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'❌ Order #{order_id} not found')
                )
                return
        else:
            # Create a mock order object for testing
            order = self.create_mock_order(test_email)
            self.stdout.write(f"Created mock order for testing")

        # Test specific email type
        success = False
        
        if email_type == 'confirmation':
            mock_items = self.create_mock_order_items()
            success = EmailService.send_order_confirmation(order, mock_items)
            
        elif email_type == 'admin':
            mock_items = self.create_mock_order_items()
            success = EmailService.send_admin_notification(order, mock_items)
            
        elif email_type == 'shipping':
            success = EmailService.send_shipping_confirmation(
                order,
                tracking_number='1Z999AA1234567890',
                tracking_url='https://www.ups.com/track?tracknum=1Z999AA1234567890',
                carrier='UPS'
            )
            
        elif email_type == 'status':
            success = EmailService.send_status_update(
                order,
                new_status='Processing',
                update_message='Your order is being prepared for shipment.',
                tracking_number='1Z999AA1234567890',
                tracking_url='https://www.ups.com/track?tracknum=1Z999AA1234567890'
            )

        if success:
            self.stdout.write(
                self.style.SUCCESS(f'✅ {email_type.title()} email sent successfully!')
            )
        else:
            self.stdout.write(
                self.style.ERROR(f'❌ Failed to send {email_type} email. Check logs for details.')
            )

    def create_mock_order(self, email=None):
        """Create a mock order object for testing."""
        class MockOrder:
            def __init__(self):
                self.id = 'TEST-12345'
                self.customer_name = 'John Doe'
                self.customer_email = email or 'test@example.com'
                self.customer_phone = '+1234567890'
                self.total_amount = 149.99
                self.status = 'confirmed'
                self.created_at = timezone.now()
                self.payment_method = 'Credit Card'

        return MockOrder()

    def create_mock_order_items(self):
        """Create mock order items for testing."""
        return [
            {
                'name': 'Premium T-Shirt',
                'sku': 'TSH-001',
                'quantity': 2,
                'price': '$29.99',
                'total': '$59.98'
            },
            {
                'name': 'Denim Jeans',
                'sku': 'JNS-002',
                'quantity': 1,
                'price': '$89.99',
                'total': '$89.99'
            }
        ]