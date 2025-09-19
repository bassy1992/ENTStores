from django.urls import path
from . import payment_views

urlpatterns = [
    # Stripe endpoints
    path('stripe/create-checkout-session/', payment_views.create_stripe_checkout_session, name='stripe-checkout'),
    path('stripe/verify-session/<str:session_id>/', payment_views.verify_stripe_session, name='stripe-verify-session'),
    path('stripe/webhook/', payment_views.stripe_webhook, name='stripe-webhook'),
    
    # MTN MoMo endpoints
    path('momo/initiate/', payment_views.initiate_momo_payment, name='momo-initiate'),
    path('momo/status/<str:reference>/', payment_views.check_momo_status, name='momo-status'),
    
    # Order creation
    path('create-order/', payment_views.create_order, name='create-order'),
    
    # Test endpoint
    path('test/', payment_views.test_payments, name='test-payments'),
    
    # Exchange rate endpoint
    path('exchange-rate/', payment_views.get_exchange_rate, name='exchange-rate'),
    
    # Legacy endpoints (for frontend compatibility)
    path('create-checkout-session/', payment_views.create_stripe_checkout_session, name='legacy-stripe-checkout'),
    path('initiate/', payment_views.initiate_momo_payment, name='legacy-momo-initiate'),
    path('status/<str:reference>/', payment_views.check_momo_status, name='legacy-momo-status'),
]