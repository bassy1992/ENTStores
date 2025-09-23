from django.urls import path, include
from . import views

app_name = 'shop'

urlpatterns = [
    # Categories
    path('categories/', views.CategoryListView.as_view(), name='category-list'),
    path('categories/featured/', views.FeaturedCategoriesView.as_view(), name='featured-categories'),
    
    # Products
    path('products/', views.ProductListView.as_view(), name='product-list'),
    path('products/featured/', views.FeaturedProductsView.as_view(), name='featured-products'),
    path('products/<slug:slug>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('products/search/', views.product_search, name='product-search'),
    
    # Tags
    path('tags/', views.ProductTagListView.as_view(), name='tag-list'),
    
    # Orders
    path('orders/', views.OrderCreateView.as_view(), name='order-create'),
    path('orders/<str:id>/', views.OrderDetailView.as_view(), name='order-detail'),
    
    # Shipping
    path('shipping/', include('shop.shipping_urls')),
    
    # Stats
    path('stats/', views.shop_stats, name='shop-stats'),
    path('search/', views.product_search, name='search'),
    
    # Debug
    path('debug-products/', views.debug_products, name='debug-products'),
]