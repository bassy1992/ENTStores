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
        queryset = Product.objects.filter(is_active=True).select_related('category')
        
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


class FeaturedProductsView(generics.ListAPIView):
    """List featured products"""
    serializer_class = ProductSerializer
    
    def get_queryset(self):
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
    featured_products = Product.objects.filter(
        is_active=True,
        tag_assignments__tag__name='featured'
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