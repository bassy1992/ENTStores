"""
Django management command to test order status change emails.
"""

from django.core.management.base import BaseCommand
from shop.models import Order
from shop.email_service import send_shipping_confirmation_email, send_status_update_email


class Command(BaseCommand):
    help = 'Test order status change emails'

    def add_arguments(self, parser):
        parser.add_argument(
            '--order-id',
            type=str,
            help='Order ID to test with'
        )
        parser.add_argument(
            '--email',
            type=str,
            help='Email address to send test to (overrides order email)'
        )
        parser.add_argument(
            '--type',
            type=str,
            choices=['shipping', 'status'],
            default='shipping',
            help='Type of email to test'
        )

    def handle(self, *args, **options):
        order_id = options.get('order_id')
        test_email = options.get('email')
        email_type = options['type']

        # Get an order to test with
        if order_id:
            try:
                order = Order.objects.get(id=order_id)
            except Order.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'Order {order_id} not found')
                )
                return
        else:
            # Get the first order
            order = Order.objects.first()
            if not order:
                self.stdout.write(
                    self.style.ERROR('No orders found in database')
                )
                return

        self.stdout.write(f"Testing {email_type} email for order {order.id}")

        # Override email if provided
        if test_email:
            original_email = order.customer_email
            order.customer_email = test_email
            self.stdout.write(f"Using test email: {test_email}")

        # Get order items
        order_items = []
        for item in order.items.all():
            order_items.append({
                'name': item.product.title,
                'quantity': item.quantity,
                'price': f"${item.unit_price / 100:.2f}",
                'total': f"${item.total_price / 100:.2f}"
            })

        try:
            if email_type == 'shipping':
                success = send_shipping_confirmation_email(
                    order,
                    tracking_number=f"TRK{order.id}",
                    tracking_url=f"https://track.example.com/{order.id}",
                    carrier="Standard Shipping"
                )
            else:
                success = send_status_update_email(
                    order,
                    'Shipped',
                    update_message='Your order has been shipped and is on its way!',
                    tracking_number=f"TRK{order.id}"
                )

            if success:
                self.stdout.write(
                    self.style.SUCCESS(f'✅ {email_type.title()} email sent successfully!')
                )
            else:
                self.stdout.write(
                    self.style.ERROR(f'❌ Failed to send {email_type} email')
                )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Error sending email: {str(e)}')
            )

        # Restore original email if we changed it
        if test_email:
            order.customer_email = original_email