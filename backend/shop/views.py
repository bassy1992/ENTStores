from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Q
from .models import Category, Product, ProductTag, Order
from .serializers import (
    CategorySerializer, ProductSerializer, ProductTagSerializer,
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
            queryset = Product.objects.filter(is_active=True).select_related('category').prefetch_related(
                'tag_assignments__tag',
                'images',
                'variants__size',
                'variants__color'
            )
            
            # Filter by category
            category = self.request.query_params.get('category')
            if category:
                queryset = queryset.filter(category__key=category)
            
            # Filter by tags
            tags = self.request.query_params.get('tags')
            if tags:
                tag_list = tags.split(',')
                queryset = queryset.filter(tag_assignments__tag__name__in=tag_list).distinct()
            
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
        # Handle missing is_featured field gracefully
        try:
            # Check if is_featured field exists by trying to use it
            return Product.objects.filter(
                is_active=True,
                is_featured=True
            ).select_related('category')
        except Exception as e:
            # Fallback to tag-based if is_featured field doesn't exist
            print(f"Using tag-based featured products fallback: {e}")
            return Product.objects.filter(
                is_active=True,
                tag_assignments__tag__name='featured'
            ).select_related('category').distinct()


class ProductDetailView(generics.RetrieveAPIView):
    """Get product details by slug"""
    queryset = Product.objects.filter(is_active=True).select_related('category')
    serializer_class = ProductSerializer
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
    try:
        featured_products = Product.objects.filter(
            is_active=True,
            is_featured=True
        ).count()
    except Exception as e:
        # Fallback if is_featured field doesn't exist
        print(f"Using tag-based featured count fallback: {e}")
        featured_products = Product.objects.filter(
            is_active=True,
            tag_assignments__tag__name='featured'
        ).distinct().count()
    
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
        products = Product.objects.filter(is_active=True).select_related('category')[:10]
        
        simple_data = []
        for product in products:
            simple_data.append({
                'id': product.id,
                'title': product.title,
                'price': product.price,
                'price_display': f"${product.price / 100:.2f}",
                'category': product.category.key if product.category else None,
                'category_label': product.category.label if product.category else None,
                'is_active': product.is_active,
                'stock_quantity': product.stock_quantity,
            })
        
        return Response({
            'results': simple_data,
            'count': len(simple_data),
            'message': 'Simple products data'
        })
        
    except Exception as e:
        return Response({
            'error': str(e),
            'message': 'Simple products failed'
        }, status=500)