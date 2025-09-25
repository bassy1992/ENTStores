from django.db import models
from django.utils.text import slugify
from django.core.validators import MinValueValidator
from decimal import Decimal
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils import timezone


class Category(models.Model):
    """Category model for organizing products"""
    
    CATEGORY_CHOICES = [
        ('t-shirts', 'T-Shirts'),
        ('polos', 'Polos'),
        ('hoodies', 'Hoodies / Crewnecks'),
        ('sweatshirts', 'Sweatshirts'),
        ('tracksuits', 'Tracksuits'),
        ('jackets', 'Jackets'),
        ('shorts', 'Shorts'),
        ('headwear', 'Headwear'),
        ('accessories', 'Accessories'),
    ]
    
    key = models.CharField(
        max_length=50, 
        choices=CATEGORY_CHOICES, 
        unique=True,
        help_text="Unique identifier for the category"
    )
    label = models.CharField(
        max_length=100,
        help_text="Display name for the category"
    )
    description = models.TextField(
        help_text="Description of the category"
    )
    image = models.ImageField(
        upload_to='categories/',
        blank=True,
        null=True,
        help_text="Category image file"
    )
    featured = models.BooleanField(
        default=False,
        help_text="Whether this category is featured on the homepage"
    )
    product_count = models.PositiveIntegerField(
        default=0,
        help_text="Number of products in this category (auto-calculated)"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['label']
    
    def __str__(self):
        return self.label
    
    def update_product_count(self):
        """Update the product count for this category"""
        self.product_count = self.products.count()
        self.save(update_fields=['product_count'])


class Product(models.Model):
    """Product model for shop items"""
    
    id = models.CharField(
        max_length=100, 
        primary_key=True,
        help_text="Unique product identifier"
    )
    title = models.CharField(
        max_length=200,
        help_text="Product title"
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        help_text="URL-friendly version of the title"
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        help_text="Price in dollars (e.g., 25.00 = $25.00)"
    )
    description = models.TextField(
        help_text="Product description"
    )
    image = models.ImageField(
        upload_to='products/',
        blank=True,
        null=True,
        help_text="Product image file"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products',
        to_field='key',
        help_text="Product category"
    )
    
    # Stock and availability
    stock_quantity = models.PositiveIntegerField(
        default=0,
        help_text="Available stock quantity"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Whether the product is active and available for purchase"
    )
    is_featured = models.BooleanField(
        default=False,
        help_text="Whether the product should be featured on the home page"
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
        
        # Update category product count
        if hasattr(self, 'category') and self.category:
            self.category.update_product_count()
    
    def delete(self, *args, **kwargs):
        category = self.category
        super().delete(*args, **kwargs)
        if category:
            category.update_product_count()
    
    @property
    def price_display(self):
        """Return formatted price as currency"""
        return f"${self.price:.2f}"
    
    @property
    def is_in_stock(self):
        """Check if product is in stock (considering both main stock and variants)"""
        # First check main product stock
        if self.stock_quantity > 0:
            return True
        
        # If main stock is 0, check if any variants are in stock
        try:
            # Check if any variants have stock
            return self.variants.filter(
                stock_quantity__gt=0,
                is_available=True
            ).exists()
        except Exception:
            # If variants table doesn't exist or there's an error, fall back to main stock
            return self.stock_quantity > 0


class ProductTag(models.Model):
    """Tags for products (featured, new, bestseller, etc.)"""
    
    name = models.CharField(
        max_length=50,
        unique=True,
        help_text="Tag name (e.g., 'featured', 'new', 'bestseller')"
    )
    display_name = models.CharField(
        max_length=100,
        help_text="Display name for the tag"
    )
    color = models.CharField(
        max_length=7,
        default='#3B82F6',
        help_text="Hex color code for the tag"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.display_name


class ProductTagAssignment(models.Model):
    """Many-to-many relationship between products and tags"""
    
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='tag_assignments'
    )
    tag = models.ForeignKey(
        ProductTag,
        on_delete=models.CASCADE,
        related_name='product_assignments'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['product', 'tag']
        ordering = ['tag__name']
    
    def __str__(self):
        return f"{self.product.title} - {self.tag.display_name}"


# Note: Removed dynamic property addition to avoid production issues
# Tags are now accessed via tag_assignments relationship in serializers


class Order(models.Model):
    """Order model for tracking purchases"""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    
    id = models.CharField(
        max_length=20,
        primary_key=True,
        help_text="Order ID (e.g., 'ORD123456')"
    )
    customer_email = models.EmailField(
        help_text="Customer email address"
    )
    customer_name = models.CharField(
        max_length=200,
        help_text="Customer full name"
    )
    
    # Shipping information
    shipping_address = models.TextField(
        help_text="Full shipping address"
    )
    shipping_city = models.CharField(max_length=100)
    shipping_country = models.CharField(max_length=100)
    shipping_postal_code = models.CharField(max_length=20, blank=True)
    
    # Order details
    subtotal = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Subtotal in dollars"
    )
    shipping_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        help_text="Shipping cost in dollars"
    )
    tax_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        help_text="Tax amount in dollars"
    )
    total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Total amount in dollars"
    )
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    
    # Shipping tracking
    tracking_number = models.CharField(
        max_length=100,
        blank=True,
        help_text="Shipping tracking number"
    )
    
    # Payment information
    payment_method = models.CharField(
        max_length=50,
        help_text="Payment method used (stripe, momo, etc.)"
    )
    payment_reference = models.CharField(
        max_length=200,
        blank=True,
        help_text="Payment gateway reference"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Order {self.id} - {self.customer_email}"
    
    @property
    def total_display(self):
        """Return formatted total as currency"""
        return f"${self.total:.2f}"


class OrderItem(models.Model):
    """Individual items within an order"""
    
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )
    # Variant information
    product_variant = models.ForeignKey(
        'ProductVariant',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Selected product variant (size/color combination)"
    )
    selected_size = models.CharField(
        max_length=50,
        blank=True,
        help_text="Selected size name (stored as text for historical record)"
    )
    selected_color = models.CharField(
        max_length=50,
        blank=True,
        help_text="Selected color name (stored as text for historical record)"
    )
    quantity = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )
    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Price per unit in dollars at time of purchase"
    )
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Total price for this line item in dollars"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['id']
    
    def __str__(self):
        variant_info = ""
        if self.selected_size or self.selected_color:
            parts = []
            if self.selected_size:
                parts.append(f"Size: {self.selected_size}")
            if self.selected_color:
                parts.append(f"Color: {self.selected_color}")
            variant_info = f" ({', '.join(parts)})"
        return f"{self.quantity}x {self.product.title}{variant_info}"
    
    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.unit_price
        super().save(*args, **kwargs)
    
    @property
    def total_display(self):
        """Return formatted total as currency"""
        return f"${self.total_price:.2f}"


# Signal handlers for email notifications
@receiver(post_save, sender=Order)
def order_status_changed(sender, instance, created, **kwargs):
    """Send email notifications when order status changes or new order is created"""
    try:
        if created:
            # New order created - send admin notification
            try:
                from .email_service import send_admin_notification_email
                
                # Get order items for the notification
                order_items = []
                for item in instance.items.all():
                    order_items.append({
                        'name': item.product.title,
                        'sku': getattr(item.product, 'sku', 'N/A'),
                        'quantity': item.quantity,
                        'price': f"${item.unit_price:.2f}",
                        'total': f"${item.total_price:.2f}"
                    })
                
                success = send_admin_notification_email(instance, order_items)
                print(f"Admin notification email sent for new order {instance.id}: {success}")
                
            except Exception as e:
                print(f"Failed to send admin notification for new order {instance.id}: {e}")
        
        elif not created and instance.pk:  # Only for existing orders (not new ones)
            try:
                # Get the previous state from the database
                if hasattr(instance, '_old_status'):
                    old_status = instance._old_status
                    
                    if old_status != instance.status:
                        # Status has changed, send appropriate email
                        from .email_service import send_shipping_confirmation_email, send_status_update_email
                        
                        if instance.status == 'shipped':
                            # Use existing tracking number or generate one
                            tracking_number = instance.tracking_number
                            if not tracking_number:
                                tracking_number = f"ENT{instance.id}{timezone.now().strftime('%Y%m%d')}"
                                # Save the generated tracking number
                                instance.tracking_number = tracking_number
                                instance.save(update_fields=['tracking_number'])
                            
                            # Send shipping confirmation with enhanced details
                            success = send_shipping_confirmation_email(
                                instance,
                                tracking_number=tracking_number,
                                carrier="Standard Shipping",
                                estimated_days=3,
                                delivery_instructions="Package will be left at your door if no one is available to receive it. Please ensure someone is available during delivery hours (9 AM - 6 PM)."
                            )
                            print(f"Shipping confirmation email sent for order {instance.id} with tracking {tracking_number}: {success}")
                        
                        elif instance.status in ['processing', 'delivered', 'cancelled']:
                            # Send status update
                            status_messages = {
                                'processing': 'Your order is now being processed and will ship soon.',
                                'delivered': 'Your order has been delivered! Thank you for your purchase.',
                                'cancelled': 'Your order has been cancelled. If you have questions, please contact support.'
                            }
                            
                            success = send_status_update_email(
                                instance,
                                instance.status.title(),
                                update_message=status_messages.get(instance.status, ''),
                                tracking_number=f"TRK{instance.id}" if instance.status == 'delivered' else None
                            )
                            print(f"Status update email sent for order {instance.id} - Status: {instance.status}: {success}")
                            
            except Exception as e:
                print(f"Failed to send status change email for order {instance.id}: {e}")
    except Exception as e:
        # Catch any other errors to prevent admin page crashes
        print(f"Error in order signal handler for order {instance.id}: {e}")
        pass  # Don't let email errors break the admin interface


# Store old status before saving
@receiver(pre_save, sender=Order)
def store_old_status(sender, instance, **kwargs):
    """Store the old status before saving"""
    if instance.pk:
        try:
            old_order = Order.objects.get(pk=instance.pk)
            instance._old_status = old_order.status
        except Order.DoesNotExist:
            instance._old_status = None


class ProductImage(models.Model):
    """Multiple images for a product"""
    
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images',
        help_text="Product this image belongs to"
    )
    image = models.ImageField(
        upload_to='products/',
        help_text="Product image file"
    )
    alt_text = models.CharField(
        max_length=200,
        blank=True,
        help_text="Alternative text for the image"
    )
    is_primary = models.BooleanField(
        default=False,
        help_text="Whether this is the primary product image"
    )
    order = models.PositiveIntegerField(
        default=0,
        help_text="Display order of the image"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', 'created_at']
        
    def __str__(self):
        return f"{self.product.title} - Image {self.order}"


class ProductSize(models.Model):
    """Available sizes for products"""
    
    name = models.CharField(
        max_length=10,
        unique=True,
        help_text="Size name (e.g., S, M, L, XL)"
    )
    display_name = models.CharField(
        max_length=50,
        help_text="Display name for the size"
    )
    order = models.PositiveIntegerField(
        default=0,
        help_text="Display order"
    )
    
    class Meta:
        ordering = ['order', 'name']
        
    def __str__(self):
        return self.display_name


class ProductColor(models.Model):
    """Available colors for products"""
    
    name = models.CharField(
        max_length=50,
        unique=True,
        help_text="Color name (e.g., Red, Blue, Black)"
    )
    hex_code = models.CharField(
        max_length=7,
        help_text="Hex color code (e.g., #FF0000)"
    )
    order = models.PositiveIntegerField(
        default=0,
        help_text="Display order"
    )
    
    class Meta:
        ordering = ['order', 'name']
        
    def __str__(self):
        return self.name


class ProductVariant(models.Model):
    """Product variants with specific size and color combinations"""
    
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='variants',
        help_text="Product this variant belongs to"
    )
    size = models.ForeignKey(
        ProductSize,
        on_delete=models.CASCADE,
        help_text="Size of this variant"
    )
    color = models.ForeignKey(
        ProductColor,
        on_delete=models.CASCADE,
        help_text="Color of this variant"
    )
    stock_quantity = models.PositiveIntegerField(
        default=0,
        help_text="Stock quantity for this specific variant"
    )
    price_adjustment = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        help_text="Price adjustment in dollars (can be negative)"
    )
    is_available = models.BooleanField(
        default=True,
        help_text="Whether this variant is available"
    )
    
    class Meta:
        unique_together = ['product', 'size', 'color']
        
    def __str__(self):
        return f"{self.product.title} - {self.size.name} - {self.color.name}"
    
    @property
    def final_price(self):
        """Calculate final price including adjustment"""
        return self.product.price + self.price_adjustment
    
    @property
    def is_in_stock(self):
        """Check if this variant is in stock"""
        return self.stock_quantity > 0 and self.is_available