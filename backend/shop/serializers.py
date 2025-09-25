from rest_framework import serializers
from .models import (
    Category, Product, ProductTag, Order, OrderItem,
    ProductImage, ProductSize, ProductColor, ProductVariant, PromoCode,
    ProductReview, ReviewHelpfulVote, ReviewImage
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
        return f"${obj.final_price:.2f}"


class ProductSerializer(serializers.ModelSerializer):
    category_label = serializers.CharField(source='category.label', read_only=True)
    price_display = serializers.CharField(read_only=True)
    is_in_stock = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = [
            'id', 'title', 'slug', 'price', 'price_display', 'description', 
            'category', 'category_label', 'stock_quantity', 
            'is_active', 'is_featured', 'is_in_stock', 'created_at'
        ]
    
    def get_is_in_stock(self, obj):
        """Check if product is in stock (considering both main stock and variants)"""
        # Use the model's property which now considers variants
        return obj.is_in_stock
    
    def to_representation(self, instance):
        """Add computed fields safely"""
        data = super().to_representation(instance)
        
        # Add is_featured field from the model
        try:
            data['is_featured'] = getattr(instance, 'is_featured', False)
        except AttributeError:
            data['is_featured'] = False
        
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
    is_in_stock = serializers.SerializerMethodField()
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
    
    def get_is_in_stock(self, obj):
        """Check if product is in stock (considering both main stock and variants)"""
        # Use the model's property which now considers variants
        return obj.is_in_stock
    
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
    
    def validate_items(self, items_data):
        """Validate stock availability for all items"""
        stock_errors = []
        
        for item_data in items_data:
            try:
                product = Product.objects.get(id=item_data['product_id'])
                requested_quantity = item_data.get('quantity', 1)
                variant_id = item_data.get('variant_id')
                
                # Check if product is active
                if not product.is_active:
                    stock_errors.append(f"{product.title} is no longer available")
                    continue
                
                # Check variant stock if variant is specified
                if variant_id:
                    try:
                        variant = ProductVariant.objects.get(id=variant_id, product=product)
                        if not variant.is_available:
                            stock_errors.append(f"{product.title} (selected variant) is not available")
                        elif variant.stock_quantity < requested_quantity:
                            stock_errors.append(
                                f"{product.title} (selected variant): Only {variant.stock_quantity} in stock, "
                                f"but {requested_quantity} requested"
                            )
                    except ProductVariant.DoesNotExist:
                        stock_errors.append(f"{product.title}: Selected variant not found")
                else:
                    # Check main product stock
                    if not product.is_in_stock:
                        stock_errors.append(f"{product.title} is out of stock")
                    elif product.stock_quantity < requested_quantity:
                        stock_errors.append(
                            f"{product.title}: Only {product.stock_quantity} in stock, "
                            f"but {requested_quantity} requested"
                        )
                        
            except Product.DoesNotExist:
                stock_errors.append(f"Product with ID {item_data.get('product_id')} not found")
        
        if stock_errors:
            raise serializers.ValidationError({
                'stock_errors': stock_errors,
                'message': 'Some items are out of stock or unavailable'
            })
        
        return items_data
    
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        
        for item_data in items_data:
            product = Product.objects.get(id=item_data['product_id'])
            
            # Get variant if specified
            product_variant = None
            variant_id = item_data.get('variant_id')
            if variant_id:
                try:
                    product_variant = ProductVariant.objects.get(id=variant_id, product=product)
                except ProductVariant.DoesNotExist:
                    pass
            
            OrderItem.objects.create(
                order=order,
                product=product,
                product_variant=product_variant,
                selected_size=item_data.get('selected_size', ''),
                selected_color=item_data.get('selected_color', ''),
                quantity=item_data['quantity'],
                unit_price=item_data['unit_price']
            )
            
            # Reduce stock after successful order creation
            requested_quantity = item_data['quantity']
            if product_variant:
                # Reduce variant stock
                product_variant.stock_quantity = max(0, product_variant.stock_quantity - requested_quantity)
                product_variant.save()
            else:
                # Reduce main product stock
                product.stock_quantity = max(0, product.stock_quantity - requested_quantity)
                product.save()
        
        return order


class PromoCodeSerializer(serializers.ModelSerializer):
    discount_display = serializers.CharField(source='get_discount_display', read_only=True)
    is_valid_now = serializers.SerializerMethodField()
    
    class Meta:
        model = PromoCode
        fields = [
            'code', 'description', 'discount_type', 'discount_value',
            'discount_display', 'minimum_order_amount', 'maximum_discount_amount',
            'is_active', 'valid_from', 'valid_until', 'is_valid_now'
        ]
    
    def get_is_valid_now(self, obj):
        """Check if promo code is currently valid"""
        is_valid, message = obj.is_valid()
        return is_valid


class ValidatePromoCodeSerializer(serializers.Serializer):
    """Serializer for validating promo codes"""
    code = serializers.CharField(max_length=50)
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2)
    
    def validate_code(self, value):
        """Validate that the promo code exists"""
        try:
            promo_code = PromoCode.objects.get(code=value.upper())
            return promo_code
        except PromoCode.DoesNotExist:
            raise serializers.ValidationError("Invalid promo code")
    
    def validate(self, data):
        """Validate the promo code against the subtotal"""
        promo_code = data['code']  # This is now a PromoCode object from validate_code
        subtotal = data['subtotal']
        
        # Check if promo code is valid
        is_valid, message = promo_code.is_valid()
        if not is_valid:
            raise serializers.ValidationError({"code": message})
        
        # Calculate discount
        discount_amount, discount_message = promo_code.calculate_discount(subtotal)
        
        if discount_amount == 0 and "required" in discount_message:
            raise serializers.ValidationError({"subtotal": discount_message})
        
        # Add calculated values to validated data
        data['promo_code'] = promo_code
        data['discount_amount'] = discount_amount
        data['discount_message'] = discount_message
        data['free_shipping'] = promo_code.discount_type == 'free_shipping'
        
        return data


class ReviewImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    
    class Meta:
        model = ReviewImage
        fields = ['image', 'alt_text']
    
    def get_image(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None


class ProductReviewSerializer(serializers.ModelSerializer):
    images = ReviewImageSerializer(many=True, read_only=True)
    rating_stars = serializers.CharField(read_only=True)
    
    class Meta:
        model = ProductReview
        fields = [
            'id', 'user_name', 'user_email', 'rating', 'rating_stars', 'title', 'comment',
            'created_at', 'verified_purchase', 'helpful_count', 'not_helpful_count',
            'images', 'size_purchased', 'color_purchased'
        ]
        read_only_fields = ['id', 'created_at', 'verified_purchase', 'helpful_count', 'not_helpful_count', 'rating_stars']
    
    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5")
        return value
    
    def validate_user_name(self, value):
        if len(value.strip()) < 2:
            raise serializers.ValidationError("Name must be at least 2 characters long")
        return value.strip()
    
    def validate_title(self, value):
        if len(value.strip()) < 5:
            raise serializers.ValidationError("Title must be at least 5 characters long")
        return value.strip()
    
    def validate_comment(self, value):
        if len(value.strip()) < 10:
            raise serializers.ValidationError("Comment must be at least 10 characters long")
        return value.strip()


class CreateReviewSerializer(serializers.ModelSerializer):
    """Serializer for creating new reviews"""
    
    class Meta:
        model = ProductReview
        fields = [
            'user_name', 'user_email', 'rating', 'title', 'comment',
            'size_purchased', 'color_purchased'
        ]
    
    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5")
        return value
    
    def validate_user_name(self, value):
        if len(value.strip()) < 2:
            raise serializers.ValidationError("Name must be at least 2 characters long")
        return value.strip()
    
    def validate_title(self, value):
        if len(value.strip()) < 5:
            raise serializers.ValidationError("Title must be at least 5 characters long")
        return value.strip()
    
    def validate_comment(self, value):
        if len(value.strip()) < 10:
            raise serializers.ValidationError("Comment must be at least 10 characters long")
        return value.strip()
    
    def create(self, validated_data):
        # Get product from context
        product = self.context['product']
        
        # Check for duplicate reviews (same email and name for same product)
        if validated_data.get('user_email'):
            existing_review = ProductReview.objects.filter(
                product=product,
                user_email=validated_data['user_email'],
                user_name=validated_data['user_name']
            ).first()
            
            if existing_review:
                raise serializers.ValidationError("You have already reviewed this product.")
        
        # Create the review
        review = ProductReview.objects.create(
            product=product,
            **validated_data
        )
        
        return review


class ReviewStatsSerializer(serializers.Serializer):
    """Serializer for review statistics"""
    average_rating = serializers.FloatField()
    total_reviews = serializers.IntegerField()
    rating_distribution = serializers.DictField()


class ReviewHelpfulVoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewHelpfulVote
        fields = ['helpful']