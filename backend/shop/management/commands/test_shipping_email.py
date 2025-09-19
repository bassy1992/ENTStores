"""
Management command to test shipping confirmation emails.
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from shop.models import Order, OrderItem, Product, Category
from shop.email_service import send_shipping_confirmation_email
import random


class Command(BaseCommand):
    help = 'Test shipping confirmation email functionality'

    def add_arguments(self, parser):
        parser.add_argument(
            '--order-id',
            type=str,
            help='Specific order ID to test with (optional)',
        )
        parser.add_argument(
            '--create-test-order',
            action='store_true',
            help='Create a test order for testing',
        )
        parser.add_argument(
            '--tracking-number',
            type=str,
            default=None,
            help='Custom tracking number to use',
        )
        parser.add_argument(
            '--carrier',
            type=str,
            default='Standard Shipping',
            help='Shipping carrier name',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Testing shipping confirmation email...'))

        # Get or create test order
        if options['create_test_order']:
            order = self.create_test_order()
            self.stdout.write(f'Created test order: {order.id}')
        elif options['order_id']:
            try:
                order = Order.objects.get(id=options['order_id'])
                self.stdout.write(f'Using existing order: {order.id}')
            except Order.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'Order {options["order_id"]} not found')
                )
                return
        else:
            # Use the most recent order
            order = Order.objects.first()
            if not order:
                self.stdout.write(
                    self.style.ERROR('No orders found. Use --create-test-order to create one.')
                )
                return
            self.stdout.write(f'Using most recent order: {order.id}')

        # Generate tracking number
        tracking_number = options['tracking_number'] or f"ENT{order.id}{timezone.now().strftime('%Y%m%d')}"
        carrier = options['carrier']

        # Send shipping confirmation email
        try:
            success = send_shipping_confirmation_email(
                order=order,
                tracking_number=tracking_number,
                carrier=carrier,
                estimated_days=3,
                delivery_instructions="Package will be left at your door if no one is available to receive it. Please ensure someone is available during delivery hours (9 AM - 6 PM)."
            )

            if success:
                self.stdout.write(
                    self.style.SUCCESS(
                        f'✅ Shipping confirmation email sent successfully!\n'
                        f'   Order: {order.id}\n'
                        f'   Customer: {order.customer_name} ({order.customer_email})\n'
                        f'   Tracking: {tracking_number}\n'
                        f'   Carrier: {carrier}'
                    )
                )
            else:
                self.stdout.write(
                    self.style.ERROR('❌ Failed to send shipping confirmation email')
                )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Error sending email: {str(e)}')
            )

    def create_test_order(self):
        """Create a test order for testing purposes."""
        # Ensure we have a test category and product
        category, _ = Category.objects.get_or_create(
            key='t-shirts',
            defaults={
                'label': 'T-Shirts',
                'description': 'Comfortable cotton t-shirts',
                'image': 'https://example.com/tshirt.jpg',
                'featured': True
            }
        )

        product, _ = Product.objects.get_or_create(
            id='test-tshirt-001',
            defaults={
                'title': 'Test T-Shirt',
                'price': 2500,  # $25.00
                'description': 'A comfortable test t-shirt',
                'image': 'https://example.com/test-tshirt.jpg',
                'category': category,
                'stock_quantity': 100,
                'is_active': True
            }
        )

        # Create test order
        order_id = f"ORD{random.randint(100000, 999999)}"
        order = Order.objects.create(
            id=order_id,
            customer_email='test@example.com',
            customer_name='Test Customer',
            shipping_address='123 Test Street',
            shipping_city='Test City',
            shipping_country='United States',
            shipping_postal_code='12345',
            subtotal=2500,
            shipping_cost=500,
            tax_amount=200,
            total=3200,
            status='processing',
            payment_method='test'
        )

        # Create order item
        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=1,
            unit_price=2500,
            total_price=2500
        )

        return order