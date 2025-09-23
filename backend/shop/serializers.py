from rest_framework import serializers
from .models import (
    Category, Product, ProductTag, Order, OrderItem,
    ProductImage, ProductSize, ProductColor, ProductVariant
)


class CategorySerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ['key', 'label', 'description', 'image', 'featured', 'product_count']
    
    def get_image(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None


class ProductTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductTag
        fields = ['name', 'display_name', 'color']


class ProductImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'alt_text', 'is_primary', 'order']
    
    def get_image(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None


class ProductSizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSize
        fields = ['id', 'name', 'display_name', 'order']


class ProductColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductColor
        fields = ['id', 'name', 'hex_code', 'order']


class ProductVariantSerializer(serializers.ModelSerializer):
    size = ProductSizeSerializer(read_only=True)
    color = ProductColorSerializer(read_only=True)
    final_price = serializers.IntegerField(read_only=True)
    final_price_display = serializers.SerializerMethodField()
    
    class Meta:
        model = ProductVariant
        fields = [
            'id', 'size', 'color', 'stock_quantity', 'price_adjustment', 
            'final_price', 'final_price_display', 'is_available', 'is_in_stock'
        ]
    
    def get_final_price_display(self, obj):
        return f"${obj.final_price / 100:.2f}"


class ProductSerializer(serializers.ModelSerializer):
    category_label = serializers.CharField(source='category.label', read_only=True)
    price_display = serializers.CharField(read_only=True)
    is_in_stock = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Product
        fields = [
            'id', 'title', 'slug', 'price', 'price_display', 'description', 
            'category', 'category_label', 'stock_quantity', 
            'is_active', 'is_in_stock', 'created_at'
        ]
    
    def to_representation(self, instance):
        """Add computed fields safely"""
        data = super().to_representation(instance)
        
        # Add is_featured field
        data['is_featured'] = False  # Default to False for now
        
        # Add tags field
        data['tags'] = []  # Default to empty list for now
        
        # Add image field
        try:
            if instance.image:
                request = self.context.get('request')
                if request:
                    data['image'] = request.build_absolute_uri(instance.image.url)
                else:
                    data['image'] = instance.image.url
            else:
                data['image'] = "https://via.placeholder.com/400x400/e5e7eb/6b7280?text=No+Image"
        except Exception:
            data['image'] = "https://via.placeholder.com/400x400/e5e7eb/6b7280?text=No+Image"
        
        return data


# Keep the full serializer as a backup for when all tables are properly set up
class ProductFullSerializer(serializers.ModelSerializer):
    category_label = serializers.CharField(source='category.label', read_only=True)
    tags = serializers.SerializerMethodField()
    price_display = serializers.CharField(read_only=True)
    is_in_stock = serializers.BooleanField(read_only=True)
    image = serializers.SerializerMethodField()
    images = ProductImageSerializer(many=True, read_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True)
    available_sizes = serializers.SerializerMethodField()
    available_colors = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = [
            'id', 'title', 'slug', 'price', 'price_display', 'description', 
            'image', 'images', 'category', 'category_label', 'stock_quantity', 
            'is_active', 'is_in_stock', 'tags', 'variants', 'available_sizes', 
            'available_colors', 'created_at'
        ]
        
    def to_representation(self, instance):
        """Handle missing fields gracefully"""
        data = super().to_representation(instance)
        
        # Use tag-based is_featured to avoid database field issues
        try:
            # Check if tag_assignments relationship exists and has the featured tag
            if hasattr(instance, 'tag_assignments'):
                has_featured_tag = instance.tag_assignments.filter(tag__name='featured').exists()
                data['is_featured'] = has_featured_tag
            else:
                data['is_featured'] = False
        except Exception as e:
            # If there's any error (missing tables, etc.), default to False
            data['is_featured'] = False
            
        return data
    
    def get_tags(self, obj):
        try:
            # Check if tag_assignments relationship exists
            if hasattr(obj, 'tag_assignments'):
                return [assignment.tag.name for assignment in obj.tag_assignments.all()]
            else:
                return []
        except Exception as e:
            # Fallback to empty list if there's an error (missing tables, etc.)
            return []
    
    def get_image(self, obj):
        try:
            # First try to get primary image from ProductImage (only if table exists)
            if hasattr(obj, 'images'):
                try:
                    primary_image = obj.images.filter(is_primary=True).first()
                    if primary_image and primary_image.image:
                        request = self.context.get('request')
                        if request:
                            return request.build_absolute_uri(primary_image.image.url)
                        return primary_image.image.url
                except Exception:
                    # ProductImage table might not exist, continue to fallback
                    pass
            
            # Fallback to the main image field
            if obj.image:
                request = self.context.get('request')
                if request:
                    return request.build_absolute_uri(obj.image.url)
                return obj.image.url
        except Exception as e:
            # If there's any error with images, return placeholder
            pass
        
        return "https://via.placeholder.com/400x400/e5e7eb/6b7280?text=No+Image"
    
    def get_available_sizes(self, obj):
        try:
            # Check if ProductSize and ProductVariant tables exist
            from django.db import connection
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1 FROM shop_productsize LIMIT 1")
            
            sizes = ProductSize.objects.filter(
                productvariant__product=obj,
                productvariant__is_available=True
            ).distinct()
            return ProductSizeSerializer(sizes, many=True).data
        except Exception as e:
            # Tables don't exist or other error
            return []
    
    def get_available_colors(self, obj):
        try:
            # Check if ProductColor and ProductVariant tables exist
            from django.db import connection
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1 FROM shop_productcolor LIMIT 1")
            
            colors = ProductColor.objects.filter(
                productvariant__product=obj,
                productvariant__is_available=True
            ).distinct()
            return ProductColorSerializer(colors, many=True).data
        except Exception as e:
            # Tables don't exist or other error
            return []


class OrderItemSerializer(serializers.ModelSerializer):
    product_title = serializers.CharField(source='product.title', read_only=True)
    product_image = serializers.SerializerMethodField()
    total_display = serializers.CharField(read_only=True)
    variant_info = serializers.SerializerMethodField()
    
    class Meta:
        model = OrderItem
        fields = [
            'product', 'product_title', 'product_image', 'quantity', 
            'unit_price', 'total_price', 'total_display', 'selected_size', 
            'selected_color', 'variant_info'
        ]
    
    def get_product_image(self, obj):
        if obj.product.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.product.image.url)
            return obj.product.image.url
        return None
    
    def get_variant_info(self, obj):
        """Get formatted variant information"""
        parts = []
        if obj.selected_size:
            parts.append(f"Size: {obj.selected_size}")
        if obj.selected_color:
            parts.append(f"Color: {obj.selected_color}")
        return ", ".join(parts) if parts else None


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    total_display = serializers.CharField(read_only=True)
    
    class Meta:
        model = Order
        fields = [
            'id', 'customer_email', 'customer_name', 'shipping_address',
            'shipping_city', 'shipping_country', 'shipping_postal_code',
            'subtotal', 'shipping_cost', 'tax_amount', 'total', 'total_display',
            'status', 'payment_method', 'payment_reference', 'items',
            'created_at', 'updated_at'
        ]


class CreateOrderSerializer(serializers.ModelSerializer):
    items = serializers.ListField(
        child=serializers.DictField(),
        write_only=True
    )
    
    class Meta:
        model = Order
        fields = [
            'id', 'customer_email', 'customer_name', 'shipping_address',
            'shipping_city', 'shipping_country', 'shipping_postal_code',
            'subtotal', 'shipping_cost', 'tax_amount', 'total',
            'payment_method', 'payment_reference', 'items'
        ]
    
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        
        for item_data in items_data:
            product = Product.objects.get(id=item_data['product_id'])
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=item_data['quantity'],
                unit_price=item_data['unit_price']
            )
        
        return order