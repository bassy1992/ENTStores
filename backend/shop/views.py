from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
from .models import Category, Product, ProductTag, Order, ProductVariant, PromoCode
from .serializers import (
    CategorySerializer, ProductSerializer, ProductFullSerializer, ProductTagSerializer,
    OrderSerializer, CreateOrderSerializer, PromoCodeSerializer, ValidatePromoCodeSerializer
)
import logging

logger = logging.getLogger(__name__)


class CategoryListView(generics.ListAPIView):
    """List all categories"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class FeaturedCategoriesView(generics.ListAPIView):
    """List featured categories only"""
    queryset = Category.objects.filter(featured=True)
    serializer_class = CategorySerializer


class ProductListView(generics.ListAPIView):
    """List all products with optional filtering"""
    serializer_class = ProductSerializer
    
    def get_queryset(self):
        try:
            # Start with basic queryset - no prefetch_related for now
            queryset = Product.objects.filter(is_active=True).select_related('category')
            
            # Filter by category
            category = self.request.query_params.get('category')
            if category:
                queryset = queryset.filter(category__key=category)
            
            # Search functionality
            search = self.request.query_params.get('search')
            if search:
                queryset = queryset.filter(
                    Q(title__icontains=search) | 
                    Q(description__icontains=search)
                )
            
            # Filter by stock availability
            in_stock = self.request.query_params.get('in_stock')
            if in_stock and in_stock.lower() == 'true':
                queryset = queryset.filter(stock_quantity__gt=0)
            
            return queryset
        except Exception as e:
            # Return empty queryset if there's an error
            return Product.objects.none()


class FeaturedProductsView(generics.ListAPIView):
    """List featured products"""
    serializer_class = ProductSerializer
    
    def get_queryset(self):
        # Use the is_featured field
        return Product.objects.filter(
            is_active=True,
            is_featured=True
        ).select_related('category')


class ProductDetailView(generics.RetrieveAPIView):
    """Get product details by slug"""
    queryset = Product.objects.filter(is_active=True).select_related('category')
    serializer_class = ProductFullSerializer
    lookup_field = 'slug'


class ProductTagListView(generics.ListAPIView):
    """List all product tags"""
    queryset = ProductTag.objects.all()
    serializer_class = ProductTagSerializer


class OrderCreateView(generics.CreateAPIView):
    """Create a new order"""
    queryset = Order.objects.all()
    serializer_class = CreateOrderSerializer


class OrderDetailView(generics.RetrieveAPIView):
    """Get order details"""
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    lookup_field = 'id'


class ValidateStockView(APIView):
    """Validate stock availability for cart items"""
    
    def post(self, request):
        try:
            items = request.data.get('items', [])
            if not items:
                return Response({'error': 'No items provided'}, status=status.HTTP_400_BAD_REQUEST)
            
            stock_errors = []
            stock_warnings = []
            
            for item in items:
                try:
                    product = Product.objects.get(id=item['product_id'])
                    requested_quantity = item.get('quantity', 1)
                    variant_id = item.get('variant_id')
                    
                    # Check if product is active
                    if not product.is_active:
                        stock_errors.append({
                            'product_id': product.id,
                            'product_title': product.title,
                            'error': 'Product is no longer available'
                        })
                        continue
                    
                    # Check variant stock if variant is specified
                    if variant_id:
                        try:
                            variant = ProductVariant.objects.get(id=variant_id, product=product)
                            if not variant.is_available:
                                stock_errors.append({
                                    'product_id': product.id,
                                    'product_title': product.title,
                                    'variant_id': variant_id,
                                    'error': 'Selected variant is not available'
                                })
                            elif variant.stock_quantity == 0:
                                stock_errors.append({
                                    'product_id': product.id,
                                    'product_title': product.title,
                                    'variant_id': variant_id,
                                    'error': 'Selected variant is out of stock'
                                })
                            elif variant.stock_quantity < requested_quantity:
                                stock_errors.append({
                                    'product_id': product.id,
                                    'product_title': product.title,
                                    'variant_id': variant_id,
                                    'error': f'Only {variant.stock_quantity} in stock, but {requested_quantity} requested',
                                    'available_quantity': variant.stock_quantity
                                })
                            elif variant.stock_quantity <= 5:  # Low stock warning
                                stock_warnings.append({
                                    'product_id': product.id,
                                    'product_title': product.title,
                                    'variant_id': variant_id,
                                    'warning': f'Low stock: only {variant.stock_quantity} remaining'
                                })
                        except ProductVariant.DoesNotExist:
                            stock_errors.append({
                                'product_id': product.id,
                                'product_title': product.title,
                                'variant_id': variant_id,
                                'error': 'Selected variant not found'
                            })
                    else:
                        # Check main product stock
                        if not product.is_in_stock:
                            stock_errors.append({
                                'product_id': product.id,
                                'product_title': product.title,
                                'error': 'Product is out of stock'
                            })
                        elif product.stock_quantity < requested_quantity:
                            stock_errors.append({
                                'product_id': product.id,
                                'product_title': product.title,
                                'error': f'Only {product.stock_quantity} in stock, but {requested_quantity} requested',
                                'available_quantity': product.stock_quantity
                            })
                        elif product.stock_quantity <= 5:  # Low stock warning
                            stock_warnings.append({
                                'product_id': product.id,
                                'product_title': product.title,
                                'warning': f'Low stock: only {product.stock_quantity} remaining'
                            })
                            
                except Product.DoesNotExist:
                    stock_errors.append({
                        'product_id': item.get('product_id'),
                        'error': 'Product not found'
                    })
            
            return Response({
                'valid': len(stock_errors) == 0,
                'errors': stock_errors,
                'warnings': stock_warnings,
                'message': 'Stock validation completed'
            })
            
        except Exception as e:
            logger.error(f"Stock validation error: {e}")
            return Response({'error': 'Failed to validate stock'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ValidatePromoCodeView(APIView):
    """Validate a promo code and calculate discount"""
    
    def post(self, request):
        try:
            serializer = ValidatePromoCodeSerializer(data=request.data)
            if serializer.is_valid():
                validated_data = serializer.validated_data
                promo_code = validated_data['promo_code']
                
                return Response({
                    'valid': True,
                    'code': promo_code.code,
                    'description': promo_code.description,
                    'discount_type': promo_code.discount_type,
                    'discount_amount': validated_data['discount_amount'],
                    'discount_display': promo_code.get_discount_display(),
                    'free_shipping': validated_data['free_shipping'],
                    'message': validated_data['discount_message']
                })
            else:
                return Response({
                    'valid': False,
                    'errors': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
                
        except Exception as e:
            logger.error(f"Promo code validation error: {e}")
            return Response({
                'valid': False,
                'error': 'Failed to validate promo code'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PromoCodeListView(generics.ListAPIView):
    """List active promo codes (for admin or promotional purposes)"""
    serializer_class = PromoCodeSerializer
    
    def get_queryset(self):
        # Only return active promo codes that are currently valid
        from django.utils import timezone
        now = timezone.now()
        return PromoCode.objects.filter(
            is_active=True,
            valid_from__lte=now,
            valid_until__gte=now
        )


@api_view(['GET'])
def shop_stats(request):
    """Get shop statistics"""
    total_products = Product.objects.filter(is_active=True).count()
    total_categories = Category.objects.count()
    
    # Use the is_featured field
    featured_products = Product.objects.filter(
        is_active=True,
        is_featured=True
    ).count()
    
    return Response({
        'total_products': total_products,
        'total_categories': total_categories,
        'featured_products': featured_products,
        'categories': CategorySerializer(Category.objects.all(), many=True).data
    })


@api_view(['GET'])
def product_search(request):
    """Search products"""
    query = request.GET.get('q', '')
    if not query:
        return Response({'results': [], 'count': 0})
    
    products = Product.objects.filter(
        Q(title__icontains=query) | Q(description__icontains=query),
        is_active=True
    ).select_related('category')
    
    serializer = ProductSerializer(products, many=True)
    return Response({
        'results': serializer.data,
        'count': products.count(),
        'query': query
    })


@api_view(['GET'])
def debug_products(request):
    """Debug products API issues"""
    try:
        # Test basic product count
        total_products = Product.objects.count()
        active_products = Product.objects.filter(is_active=True).count()
        
        # Test if we can get a single product without serialization
        first_product = Product.objects.first()
        basic_product_data = None
        
        if first_product:
            basic_product_data = {
                'id': first_product.id,
                'title': first_product.title,
                'price': first_product.price,
                'category_key': first_product.category.key if first_product.category else None,
                'is_active': first_product.is_active,
            }
            
            # Test serialization step by step
            try:
                # Test minimal serialization
                serializer = ProductSerializer(first_product, context={'request': request})
                product_data = serializer.data
            except Exception as e:
                product_data = {'serialization_error': str(e)}
        
        # Test category relationships
        categories_count = Category.objects.count()
        
        return Response({
            'total_products': total_products,
            'active_products': active_products,
            'categories_count': categories_count,
            'basic_product_data': basic_product_data,
            'serialized_product': product_data if 'product_data' in locals() else None,
            'message': 'Products debug info'
        })
        
    except Exception as e:
        return Response({
            'error': str(e),
            'message': 'Debug products failed'
        }, status=500)


@api_view(['GET'])
def simple_products(request):
    """Simple products endpoint without complex serialization"""
    try:
        # Get category filter if provided
        category = request.GET.get('category')
        
        # Build queryset
        queryset = Product.objects.filter(is_active=True).select_related('category')
        
        if category:
            queryset = queryset.filter(category__key=category)
        
        products = queryset[:50]  # Limit to 50 products
        
        simple_data = []
        for product in products:
            # Build image URL
            image_url = "https://via.placeholder.com/400x400/e5e7eb/6b7280?text=No+Image"
            if product.image:
                try:
                    image_url = request.build_absolute_uri(product.image.url)
                except:
                    pass
            
            simple_data.append({
                'id': product.id,
                'title': product.title,
                'slug': product.slug,
                'price': product.price,
                'price_display': f"${product.price:.2f}",
                'description': product.description,
                'image': image_url,
                'category': product.category.key if product.category else None,
                'category_label': product.category.label if product.category else None,
                'stock_quantity': product.stock_quantity,
                'is_active': product.is_active,
                'is_in_stock': product.is_in_stock,
                'is_featured': getattr(product, 'is_featured', False),
                'tags': [],  # Default for now
                'created_at': product.created_at.isoformat() if product.created_at else None,
            })
        
        return Response({
            'results': simple_data,
            'count': len(simple_data),
            'message': 'Simple products data with full fields'
        })
        
    except Exception as e:
        return Response({
            'error': str(e),
            'message': 'Simple products failed'
        }, status=500)