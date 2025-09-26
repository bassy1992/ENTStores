from django.contrib import admin
from django.utils.html import format_html
from django import forms
from .models import (
    Category, Product, ProductTag, ProductTagAssignment, Order, OrderItem,
    ProductImage, ProductSize, ProductColor, ProductVariant, PromoCode,
    ProductReview, ReviewHelpfulVote, ReviewImage
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['label', 'key', 'featured', 'product_count', 'created_at']
    list_filter = ['featured', 'created_at']
    search_fields = ['label', 'key', 'description']
    readonly_fields = ['product_count', 'created_at', 'updated_at']
    
    fieldsets = (
        (None, {
            'fields': ('key', 'label', 'description')
        }),
        ('Display', {
            'fields': ('image', 'featured')
        }),
        ('Statistics', {
            'fields': ('product_count',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('products')


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ensure category field shows proper choices
        if 'category' in self.fields:
            self.fields['category'].queryset = Category.objects.all()
            self.fields['category'].empty_label = "Select a category"


class ProductTagAssignmentInline(admin.TabularInline):
    model = ProductTagAssignment
    extra = 1
    autocomplete_fields = ['tag']


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3  # Show 3 empty forms for adding images
    fields = ['image', 'alt_text', 'is_primary', 'order']
    readonly_fields = ['created_at']
    verbose_name = "Product Image"
    verbose_name_plural = "Product Images"


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 2  # Show 2 empty forms for adding variants
    fields = ['size', 'color', 'stock_quantity', 'price_adjustment', 'is_available']
    verbose_name = "Product Variant"
    verbose_name_plural = "Product Variants (Size & Color Combinations)"
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "size":
            kwargs["queryset"] = ProductSize.objects.all().order_by('order', 'name')
        if db_field.name == "color":
            kwargs["queryset"] = ProductColor.objects.all().order_by('order', 'name')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductForm
    list_display = ['title', 'category', 'price_display', 'shipping_cost_display', 'stock_quantity', 'is_active', 'is_featured', 'created_at']
    list_filter = ['category', 'is_active', 'is_featured', 'created_at', 'tag_assignments__tag']
    search_fields = ['title', 'id', 'description']
    readonly_fields = ['created_at', 'updated_at']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ProductTagAssignmentInline, ProductImageInline, ProductVariantInline]
    
    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)
        }

    
    fieldsets = (
        (None, {
            'fields': ('id', 'title', 'slug', 'description')
        }),
        ('Pricing & Category', {
            'fields': ('price', 'shipping_cost', 'category')
        }),
        ('Main Image', {
            'fields': ('image',),
            'description': 'Upload a main product image. You can add more images in the "Product Images" section below.'
        }),
        ('Inventory & Settings', {
            'fields': ('stock_quantity', 'is_active', 'is_featured')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def price_display(self, obj):
        return obj.price_display
    price_display.short_description = 'Price'
    
    def shipping_cost_display(self, obj):
        return f"${obj.shipping_cost:.2f}"
    shipping_cost_display.short_description = 'Shipping'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('category')
    
    actions = ['create_basic_variants']
    
    def create_basic_variants(self, request, queryset):
        """Create basic variants (all size/color combinations) for selected products."""
        from django.contrib import messages
        
        created_count = 0
        for product in queryset:
            sizes = ProductSize.objects.all()[:4]  # First 4 sizes (S, M, L, XL)
            colors = ProductColor.objects.all()[:3]  # First 3 colors
            
            for size in sizes:
                for color in colors:
                    variant, created = ProductVariant.objects.get_or_create(
                        product=product,
                        size=size,
                        color=color,
                        defaults={
                            'stock_quantity': 10,
                            'price_adjustment': 0,
                            'is_available': True
                        }
                    )
                    if created:
                        created_count += 1
        
        messages.success(request, f'Created {created_count} new product variants.')
    create_basic_variants.short_description = "Create basic size/color variants for selected products"
    
    def save_model(self, request, obj, form, change):
        # Ensure the product is saved first before any inlines
        if not change:  # New product
            # Generate a unique ID if not provided
            if not obj.id:
                import uuid
                obj.id = f"prod-{uuid.uuid4().hex[:8]}"
        super().save_model(request, obj, form, change)


@admin.register(ProductTag)
class ProductTagAdmin(admin.ModelAdmin):
    list_display = ['display_name', 'name', 'color_preview', 'product_count', 'created_at']
    search_fields = ['name', 'display_name']
    readonly_fields = ['created_at']
    
    def color_preview(self, obj):
        return format_html(
            '<span style="background-color: {}; padding: 2px 8px; border-radius: 3px; color: white;">{}</span>',
            obj.color,
            obj.color
        )
    color_preview.short_description = 'Color'
    
    def product_count(self, obj):
        return obj.product_assignments.count()
    product_count.short_description = 'Products'


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['total_price', 'variant_display']
    fields = ['product', 'selected_size', 'selected_color', 'quantity', 'unit_price', 'total_price', 'variant_display']
    
    def variant_display(self, obj):
        """Display variant information in a readable format"""
        try:
            parts = []
            if hasattr(obj, 'selected_size') and obj.selected_size:
                parts.append(f"Size: {obj.selected_size}")
            if hasattr(obj, 'selected_color') and obj.selected_color:
                parts.append(f"Color: {obj.selected_color}")
            return ', '.join(parts) if parts else 'No variant selected'
        except Exception as e:
            return f'Error loading variant: {str(e)}'
    variant_display.short_description = 'Variant Info'
    
    def get_queryset(self, request):
        try:
            # Try the full queryset with relations
            queryset = super().get_queryset(request).select_related('product')
            
            # Test if product_variant field exists
            if hasattr(OrderItem._meta.get_field('product_variant'), 'related_model'):
                queryset = queryset.select_related('product_variant')
            
            return queryset
        except Exception as e:
            # Log the error for debugging
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"OrderItem inline queryset error: {e}")
            
            # Fallback to basic queryset
            return super().get_queryset(request)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer_name', 'customer_email', 'status_display', 'total_display', 'shipping_info', 'created_at']
    list_filter = ['status', 'payment_method', 'created_at', 'shipping_country']
    search_fields = ['id', 'customer_email', 'customer_name', 'payment_reference', 'shipping_address']
    readonly_fields = ['created_at', 'updated_at', 'tracking_number_display']
    inlines = [OrderItemInline]
    actions = ['mark_as_shipped', 'send_shipping_confirmation']
    
    fieldsets = (
        ('Order Information', {
            'fields': ('id', 'status'),
            'description': 'Changing the status will automatically send email notifications to the customer.'
        }),
        ('Customer Details', {
            'fields': ('customer_name', 'customer_email')
        }),
        ('Shipping Information', {
            'fields': ('shipping_address', 'shipping_city', 'shipping_country', 'shipping_postal_code', 'tracking_number', 'tracking_number_display'),
            'description': 'Complete shipping address and tracking information. You can manually set a tracking number or let the system generate one when status changes to shipped.'
        }),
        ('Payment & Totals', {
            'fields': ('subtotal', 'shipping_cost', 'tax_amount', 'total', 'payment_method', 'payment_reference')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def status_display(self, obj):
        colors = {
            'pending': '#fbbf24',      # yellow
            'processing': '#3b82f6',   # blue
            'shipped': '#10b981',      # green
            'delivered': '#059669',    # dark green
            'cancelled': '#ef4444',    # red
        }
        color = colors.get(obj.status, '#6b7280')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 2px 8px; border-radius: 12px; font-size: 11px; font-weight: bold;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_display.short_description = 'Status'
    
    def shipping_info(self, obj):
        """Display shipping information summary."""
        if obj.status == 'shipped':
            return format_html(
                '<span style="color: #10b981;">📦 Shipped</span><br>'
                '<small>{}, {}</small>',
                obj.shipping_city,
                obj.shipping_country
            )
        elif obj.status == 'delivered':
            return format_html(
                '<span style="color: #059669;">✅ Delivered</span><br>'
                '<small>{}, {}</small>',
                obj.shipping_city,
                obj.shipping_country
            )
        else:
            return format_html(
                '<span style="color: #6b7280;">📍 {}, {}</span>',
                obj.shipping_city,
                obj.shipping_country
            )
    shipping_info.short_description = 'Shipping'
    
    def tracking_number_display(self, obj):
        """Display tracking number if order is shipped."""
        if obj.status in ['shipped', 'delivered']:
            from django.utils import timezone
            tracking_number = f"ENT{obj.id}{obj.updated_at.strftime('%Y%m%d') if obj.updated_at else timezone.now().strftime('%Y%m%d')}"
            return format_html(
                '<code style="background: #f3f4f6; padding: 2px 4px; border-radius: 3px;">{}</code>',
                tracking_number
            )
        return "Not shipped yet"
    tracking_number_display.short_description = 'Tracking Number'
    
    def mark_as_shipped(self, request, queryset):
        """Mark selected orders as shipped."""
        updated = 0
        for order in queryset:
            if order.status != 'shipped':
                order.status = 'shipped'
                order.save()
                updated += 1
        
        self.message_user(
            request,
            f"{updated} order(s) marked as shipped. Shipping confirmation emails sent to customers."
        )
    mark_as_shipped.short_description = "Mark selected orders as shipped"
    
    def send_shipping_confirmation(self, request, queryset):
        """Send shipping confirmation emails for selected orders."""
        from .email_service import send_shipping_confirmation_email
        from django.utils import timezone
        
        sent = 0
        for order in queryset:
            if order.status in ['shipped', 'delivered']:
                tracking_number = f"ENT{order.id}{order.updated_at.strftime('%Y%m%d') if order.updated_at else timezone.now().strftime('%Y%m%d')}"
                success = send_shipping_confirmation_email(
                    order=order,
                    tracking_number=tracking_number,
                    carrier="Standard Shipping",
                    estimated_days=3
                )
                if success:
                    sent += 1
        
        self.message_user(
            request,
            f"Shipping confirmation emails sent for {sent} order(s)."
        )
    send_shipping_confirmation.short_description = "Send shipping confirmation emails"
    
    def save_model(self, request, obj, form, change):
        if change and 'status' in form.changed_data:
            # Status was changed, the signal will handle email sending
            super().save_model(request, obj, form, change)
            if obj.status == 'shipped':
                from django.utils import timezone
                tracking_number = f"ENT{obj.id}{timezone.now().strftime('%Y%m%d')}"
                self.message_user(
                    request, 
                    format_html(
                        'Order {} status updated to {}. Shipping confirmation email sent to customer with tracking number: <code>{}</code>',
                        obj.id,
                        obj.get_status_display(),
                        tracking_number
                    )
                )
            else:
                self.message_user(request, f"Order {obj.id} status updated to {obj.get_status_display()}. Email notification sent to customer.")
        else:
            super().save_model(request, obj, form, change)
    
    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('items__product')


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'variant_info_display', 'quantity', 'unit_price', 'total_display']
    list_filter = ['created_at', 'selected_size', 'selected_color']
    search_fields = ['order__id', 'product__title', 'selected_size', 'selected_color']
    readonly_fields = ['total_price', 'created_at']
    fields = ['order', 'product', 'product_variant', 'selected_size', 'selected_color', 'quantity', 'unit_price', 'total_price', 'created_at']
    
    def variant_info_display(self, obj):
        """Display variant information in list view"""
        try:
            parts = []
            if hasattr(obj, 'selected_size') and obj.selected_size:
                parts.append(f"Size: {obj.selected_size}")
            if hasattr(obj, 'selected_color') and obj.selected_color:
                parts.append(f"Color: {obj.selected_color}")
            return ', '.join(parts) if parts else '-'
        except Exception as e:
            return f'Error: {str(e)}'
    variant_info_display.short_description = 'Variant'
    
    def get_queryset(self, request):
        try:
            # Try the full queryset with all relations
            queryset = super().get_queryset(request).select_related('order', 'product')
            
            # Test if product_variant field exists by trying to access it
            if hasattr(OrderItem._meta.get_field('product_variant'), 'related_model'):
                queryset = queryset.select_related('product_variant')
            
            return queryset
        except Exception as e:
            # Log the error for debugging
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"OrderItem admin queryset error: {e}")
            
            # Fallback to basic queryset
            return super().get_queryset(request)


# Custom admin site configuration
admin.site.site_header = "ENNC Shop Administration"
admin.site.site_title = "ENNC Shop Admin"
admin.site.index_title = "Welcome to ENNC Shop Administration"

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['product', 'alt_text', 'is_primary', 'order', 'created_at']
    list_filter = ['is_primary', 'created_at']
    search_fields = ['product__title', 'alt_text']
    list_editable = ['is_primary', 'order']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('product')


@admin.register(ProductSize)
class ProductSizeAdmin(admin.ModelAdmin):
    list_display = ['display_name', 'name', 'order', 'products_count']
    list_editable = ['order']
    ordering = ['order', 'name']
    search_fields = ['name', 'display_name']
    
    def products_count(self, obj):
        return obj.productvariant_set.values('product').distinct().count()
    products_count.short_description = 'Products Using This Size'


@admin.register(ProductColor)
class ProductColorAdmin(admin.ModelAdmin):
    list_display = ['name', 'hex_code', 'color_preview', 'order', 'products_count']
    list_editable = ['order', 'hex_code']
    ordering = ['order', 'name']
    search_fields = ['name', 'hex_code']
    
    def color_preview(self, obj):
        return format_html(
            '<div style="width: 30px; height: 20px; background-color: {}; border: 1px solid #ccc; border-radius: 3px; display: inline-block; margin-right: 5px;"></div>{}',
            obj.hex_code,
            obj.name
        )
    color_preview.short_description = 'Preview'
    
    def products_count(self, obj):
        return obj.productvariant_set.values('product').distinct().count()
    products_count.short_description = 'Products Using This Color'


@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ['product', 'size', 'color', 'stock_quantity', 'price_adjustment', 'final_price_display', 'is_available']
    list_filter = ['size', 'color', 'is_available']
    search_fields = ['product__title']
    list_editable = ['stock_quantity', 'price_adjustment', 'is_available']
    
    def final_price_display(self, obj):
        return f"${obj.final_price:.2f}"
    final_price_display.short_description = 'Final Price'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('product', 'size', 'color')


@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ['code', 'description', 'discount_type', 'discount_value', 'is_active', 'usage_count', 'valid_from', 'valid_until']
    list_filter = ['discount_type', 'is_active', 'valid_from', 'valid_until']
    search_fields = ['code', 'description']
    readonly_fields = ['usage_count', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('code', 'description', 'is_active')
        }),
        ('Discount Settings', {
            'fields': ('discount_type', 'discount_value', 'minimum_order_amount', 'maximum_discount_amount')
        }),
        ('Usage Limits', {
            'fields': ('usage_limit', 'usage_count')
        }),
        ('Validity Period', {
            'fields': ('valid_from', 'valid_until')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        readonly_fields = list(self.readonly_fields)
        if obj and obj.usage_count > 0:
            # Don't allow changing critical fields if code has been used
            readonly_fields.extend(['code', 'discount_type', 'discount_value'])
        return readonly_fields


class ReviewImageInline(admin.TabularInline):
    model = ReviewImage
    extra = 1
    fields = ['image', 'alt_text', 'order']
    readonly_fields = ['created_at']


@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ['user_name', 'product', 'rating', 'rating_stars', 'title', 'is_approved', 'verified_purchase', 'helpful_count', 'created_at']
    list_filter = ['rating', 'is_approved', 'verified_purchase', 'created_at']
    search_fields = ['user_name', 'user_email', 'title', 'comment', 'product__title']
    readonly_fields = ['created_at', 'updated_at', 'helpful_count', 'not_helpful_count', 'rating_stars']
    list_editable = ['is_approved']
    ordering = ['-created_at']
    inlines = [ReviewImageInline]
    
    fieldsets = (
        ('Review Information', {
            'fields': ('product', 'rating', 'rating_stars', 'title', 'comment')
        }),
        ('User Information', {
            'fields': ('user_name', 'user_email')
        }),
        ('Purchase Details', {
            'fields': ('verified_purchase', 'order', 'size_purchased', 'color_purchased')
        }),
        ('Moderation', {
            'fields': ('is_approved', 'is_featured')
        }),
        ('Statistics', {
            'fields': ('helpful_count', 'not_helpful_count', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('product', 'order')
    
    actions = ['approve_reviews', 'disapprove_reviews', 'feature_reviews']
    
    def approve_reviews(self, request, queryset):
        updated = queryset.update(is_approved=True)
        self.message_user(request, f'{updated} review(s) approved.')
    approve_reviews.short_description = "Approve selected reviews"
    
    def disapprove_reviews(self, request, queryset):
        updated = queryset.update(is_approved=False)
        self.message_user(request, f'{updated} review(s) disapproved.')
    disapprove_reviews.short_description = "Disapprove selected reviews"
    
    def feature_reviews(self, request, queryset):
        updated = queryset.update(is_featured=True)
        self.message_user(request, f'{updated} review(s) featured.')
    feature_reviews.short_description = "Feature selected reviews"


@admin.register(ReviewHelpfulVote)
class ReviewHelpfulVoteAdmin(admin.ModelAdmin):
    list_display = ['review', 'user_ip', 'helpful', 'created_at']
    list_filter = ['helpful', 'created_at']
    readonly_fields = ['created_at']
    search_fields = ['review__user_name', 'review__product__title', 'user_ip']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('review', 'review__product')


@admin.register(ReviewImage)
class ReviewImageAdmin(admin.ModelAdmin):
    list_display = ['review', 'alt_text', 'order', 'created_at']
    list_filter = ['created_at']
    search_fields = ['review__user_name', 'review__product__title', 'alt_text']
    readonly_fields = ['created_at']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('review', 'review__product')