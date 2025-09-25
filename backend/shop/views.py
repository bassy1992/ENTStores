from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Q
from .models import Category, Product, ProductTag, Order
from .serializers import (
    CategorySerializer, ProductSerializer, ProductFullSerializer, ProductTagSerializer,
    OrderSerializer, CreateOrderSerializer
)


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
                'is_in_stock': product.stock_quantity > 0,
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