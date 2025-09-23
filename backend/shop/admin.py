from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Category, Product, ProductTag, ProductTagAssignment, Order, OrderItem,
    ProductImage, ProductSize, ProductColor, ProductVariant
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


class ProductTagAssignmentInline(admin.TabularInline):
    model = ProductTagAssignment
    extra = 1
    autocomplete_fields = ['tag']


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ['image', 'alt_text', 'is_primary', 'order']
    readonly_fields = ['created_at']


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1
    fields = ['size', 'color', 'stock_quantity', 'price_adjustment', 'is_available']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'price_display', 'stock_quantity', 'is_active', 'created_at']
    list_filter = ['category', 'is_active', 'created_at', 'tag_assignments__tag']
    search_fields = ['title', 'id', 'description']
    readonly_fields = ['created_at', 'updated_at']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ProductTagAssignmentInline, ProductImageInline, ProductVariantInline]
    
    fieldsets = (
        (None, {
            'fields': ('id', 'title', 'slug', 'description')
        }),
        ('Pricing & Category', {
            'fields': ('price', 'category')
        }),
        ('Media', {
            'fields': ('image',)
        }),
        ('Inventory', {
            'fields': ('stock_quantity', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def price_display(self, obj):
        return obj.price_display
    price_display.short_description = 'Price'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('category')


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
    readonly_fields = ['total_price']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('product')


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
    list_display = ['order', 'product', 'quantity', 'unit_price', 'total_display']
    list_filter = ['created_at']
    search_fields = ['order__id', 'product__title']
    readonly_fields = ['total_price', 'created_at']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('order', 'product')


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
    list_display = ['display_name', 'name', 'order']
    list_editable = ['order']
    ordering = ['order', 'name']


@admin.register(ProductColor)
class ProductColorAdmin(admin.ModelAdmin):
    list_display = ['name', 'hex_code', 'color_preview', 'order']
    list_editable = ['order']
    ordering = ['order', 'name']
    
    def color_preview(self, obj):
        return format_html(
            '<div style="width: 20px; height: 20px; background-color: {}; border: 1px solid #ccc; border-radius: 3px; display: inline-block;"></div>',
            obj.hex_code
        )
    color_preview.short_description = 'Preview'


@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ['product', 'size', 'color', 'stock_quantity', 'price_adjustment', 'final_price_display', 'is_available']
    list_filter = ['size', 'color', 'is_available']
    search_fields = ['product__title']
    list_editable = ['stock_quantity', 'price_adjustment', 'is_available']
    
    def final_price_display(self, obj):
        return f"${obj.final_price / 100:.2f}"
    final_price_display.short_description = 'Final Price'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('product', 'size', 'color')