from rest_framework import serializers
from .models import Category, Product, ProductTag, Order, OrderItem


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


class ProductSerializer(serializers.ModelSerializer):
    category_label = serializers.CharField(source='category.label', read_only=True)
    tags = serializers.SerializerMethodField()
    price_display = serializers.CharField(read_only=True)
    is_in_stock = serializers.BooleanField(read_only=True)
    image = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = [
            'id', 'title', 'slug', 'price', 'price_display', 'description', 
            'image', 'category', 'category_label', 'stock_quantity', 
            'is_active', 'is_in_stock', 'tags', 'created_at'
        ]
    
    def get_tags(self, obj):
        return [tag.name for tag in obj.tags]
    
    def get_image(self, obj):
        if obj.image:
            try:
                request = self.context.get('request')
                if request:
                    return request.build_absolute_uri(obj.image.url)
                return obj.image.url
            except:
                # If image file doesn't exist, return placeholder
                return "https://via.placeholder.com/400x400/e5e7eb/6b7280?text=No+Image"
        return "https://via.placeholder.com/400x400/e5e7eb/6b7280?text=No+Image"


class OrderItemSerializer(serializers.ModelSerializer):
    product_title = serializers.CharField(source='product.title', read_only=True)
    product_image = serializers.SerializerMethodField()
    total_display = serializers.CharField(read_only=True)
    
    class Meta:
        model = OrderItem
        fields = [
            'product', 'product_title', 'product_image', 'quantity', 
            'unit_price', 'total_price', 'total_display'
        ]
    
    def get_product_image(self, obj):
        if obj.product.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.product.image.url)
            return obj.product.image.url
        return None


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