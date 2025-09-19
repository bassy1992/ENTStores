"""
URL configuration for shipping-related views.
"""

from django.urls import path
from . import shipping_views

app_name = 'shipping'

urlpatterns = [
    # API endpoints
    path('api/webhook/', shipping_views.ShippingWebhookView.as_view(), name='webhook'),
    path('api/update/', shipping_views.update_shipping_status, name='update_status'),
    path('api/status/<str:order_id>/', shipping_views.get_shipping_status, name='get_status'),
    
    # Customer tracking page
    path('track/<str:order_id>/', shipping_views.shipping_tracking_page, name='track_order'),
]