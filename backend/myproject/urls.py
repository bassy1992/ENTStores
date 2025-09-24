"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import os
from django.contrib import admin
from django.urls import path, include, re_path
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.views.static import serve
from shop import payment_views

def health_check(request):
    return JsonResponse({"status": "ok", "message": "ENTstore API is running", "cors_enabled": True, "timestamp": "2025-09-19-23:30"})

def root_view(request):
    """Root endpoint showing available API endpoints"""
    return JsonResponse({
        "message": "ENTstore API is running successfully on Render!",
        "status": "ok",
        "available_endpoints": {
            "health": "/api/health/",
            "admin": "/admin/",
            "shop_api": "/api/shop/",
            "payments": "/api/payments/",
            "cors_test": "/api/cors-test/",
            "csrf_test": "/api/csrf-test/",
            "debug_media": "/api/debug-media/",
            "debug_static": "/api/debug-static/",
            "debug_env": "/api/debug-env/",
            "test_email": "/api/test-email/"
        },
        "deployment": "render",
        "timestamp": "2025-09-19"
    })

@csrf_exempt
@require_http_methods(["GET", "POST"])
def csrf_test(request):
    return JsonResponse({
        "method": request.method,
        "csrf_cookie": request.META.get('CSRF_COOKIE'),
        "has_csrf_token": 'csrfmiddlewaretoken' in request.POST,
        "message": "CSRF test endpoint"
    })

def cors_test(request):
    """Test endpoint to check CORS configuration"""
    from django.conf import settings
    return JsonResponse({
        "cors_allow_all_origins": getattr(settings, 'CORS_ALLOW_ALL_ORIGINS', False),
        "cors_allowed_origins": getattr(settings, 'CORS_ALLOWED_ORIGINS', []),
        "corsheaders_installed": 'corsheaders' in settings.INSTALLED_APPS,
        "cors_middleware_installed": 'corsheaders.middleware.CorsMiddleware' in settings.MIDDLEWARE,
        "origin": request.META.get('HTTP_ORIGIN', 'No origin header'),
        "message": "CORS configuration test"
    })

def debug_media(request):
    """Debug endpoint to check media configuration"""
    from django.conf import settings
    import os
    
    media_files = []
    if os.path.exists(settings.MEDIA_ROOT):
        for root, dirs, files in os.walk(settings.MEDIA_ROOT):
            for file in files:
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, settings.MEDIA_ROOT)
                media_files.append({
                    'file': rel_path,
                    'exists': os.path.exists(full_path),
                    'size': os.path.getsize(full_path) if os.path.exists(full_path) else 0
                })
    
    return JsonResponse({
        "debug": settings.DEBUG,
        "media_root": settings.MEDIA_ROOT,
        "media_url": settings.MEDIA_URL,
        "media_root_exists": os.path.exists(settings.MEDIA_ROOT),
        "media_files": media_files,
        "media_files_count": len(media_files),
        "alternative_paths": {
            "persistent_disk": os.path.exists('/opt/render/project/data/media'),
            "backend_media": os.path.exists('/opt/render/project/src/backend/media'),
        },
        "message": "Media configuration debug"
    })

def debug_static(request):
    """Debug endpoint to check static files configuration"""
    from django.conf import settings
    import os
    
    static_files = []
    if os.path.exists(settings.STATIC_ROOT):
        for root, dirs, files in os.walk(settings.STATIC_ROOT):
            for file in files[:10]:  # Limit to first 10 files
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, settings.STATIC_ROOT)
                static_files.append({
                    'file': rel_path,
                    'exists': os.path.exists(full_path),
                    'size': os.path.getsize(full_path) if os.path.exists(full_path) else 0
                })
    
    return JsonResponse({
        "debug": settings.DEBUG,
        "static_root": settings.STATIC_ROOT,
        "static_url": settings.STATIC_URL,
        "static_root_exists": os.path.exists(settings.STATIC_ROOT),
        "staticfiles_dirs": getattr(settings, 'STATICFILES_DIRS', []),
        "staticfiles_storage": getattr(settings, 'STATICFILES_STORAGE', 'Not set'),
        "whitenoise_middleware": 'whitenoise.middleware.WhiteNoiseMiddleware' in settings.MIDDLEWARE,
        "static_files_sample": static_files,
        "admin_static_exists": os.path.exists(os.path.join(settings.STATIC_ROOT, 'admin')) if os.path.exists(settings.STATIC_ROOT) else False,
        "message": "Static files configuration debug"
    })

def debug_env(request):
    """Debug endpoint to check environment variables"""
    import os
    from django.conf import settings
    
    return JsonResponse({
        "environment_variables": {
            "DATABASE_URL": os.environ.get('DATABASE_URL', 'Not set')[:50] + "..." if os.environ.get('DATABASE_URL') else 'Not set',
            "USE_SQLITE": os.environ.get('USE_SQLITE', 'Not set'),
            "DEBUG": os.environ.get('DEBUG', 'Not set'),
            "DJANGO_SECRET_KEY": "Set" if os.environ.get('DJANGO_SECRET_KEY') else 'Not set',
            "EMAIL_HOST_USER": os.environ.get('EMAIL_HOST_USER', 'Not set'),
            "EMAIL_HOST_PASSWORD": "Set" if os.environ.get('EMAIL_HOST_PASSWORD') else 'Not set',
        },
        "django_settings": {
            "DEBUG": settings.DEBUG,
            "DATABASE_ENGINE": settings.DATABASES['default']['ENGINE'],
            "DATABASE_NAME": settings.DATABASES['default']['NAME'],
            "EMAIL_BACKEND": settings.EMAIL_BACKEND,
            "EMAIL_HOST": settings.EMAIL_HOST,
            "EMAIL_PORT": settings.EMAIL_PORT,
            "EMAIL_USE_TLS": settings.EMAIL_USE_TLS,
            "DEFAULT_FROM_EMAIL": settings.DEFAULT_FROM_EMAIL,
        },
        "message": "Environment variables debug"
    })

def test_email(request):
    """Test email functionality"""
    from shop.email_service import EmailService
    from django.utils import timezone
    
    # Create a mock order for testing
    class MockOrder:
        def __init__(self):
            self.id = 'TEST-EMAIL-' + str(int(timezone.now().timestamp()))
            self.customer_name = 'Test Customer'
            self.customer_email = 'Enontinoclothing@gmail.com'
            self.total = 2500  # $25.00 in cents
            self.status = 'confirmed'
            self.created_at = timezone.now()
    
    mock_order = MockOrder()
    mock_items = [
        {
            'name': 'Test Product',
            'quantity': 1,
            'price': '$25.00',
            'total': '$25.00'
        }
    ]
    
    try:
        # Test basic email configuration
        basic_test = EmailService.test_email_configuration()
        
        # Test order confirmation email
        confirmation_test = EmailService.send_order_confirmation(mock_order, mock_items)
        
        # Test admin notification
        admin_test = EmailService.send_admin_notification(mock_order, mock_items)
        
        return JsonResponse({
            "email_tests": {
                "basic_configuration": basic_test,
                "order_confirmation": confirmation_test,
                "admin_notification": admin_test,
            },
            "test_order_id": mock_order.id,
            "test_email": mock_order.customer_email,
            "message": "Email tests completed"
        })
        
    except Exception as e:
        return JsonResponse({
            "error": str(e),
            "message": "Email test failed"
        }, status=500)

urlpatterns = [
    # Root endpoint
    path('', root_view, name='root'),
    # API endpoints
    path('api/health/', health_check, name='health-check'),
    path('api/csrf-test/', csrf_test, name='csrf-test'),
    path('api/cors-test/', cors_test, name='cors-test'),
    path('api/debug-media/', debug_media, name='debug-media'),
    path('api/debug-static/', debug_static, name='debug-static'),
    path('api/debug-env/', debug_env, name='debug-env'),
    path('api/test-email/', test_email, name='test-email'),
    path('admin/', admin.site.urls),
    path('api/shop/', include('shop.urls')),
    path('api/payments/', include('shop.payment_urls')),
    
    # Legacy endpoints for frontend compatibility (without namespace)
    path('api/stripe/create-checkout-session/', payment_views.create_stripe_checkout_session, name='legacy-stripe'),
    path('api/momo/initiate/', payment_views.initiate_momo_payment, name='legacy-momo-initiate'),
    path('api/momo/status/<str:reference>/', payment_views.check_momo_status, name='legacy-momo-status'),
]

# Serve media files in all environments (required for Render Web Services)
if settings.DEBUG:
    # Development: serve media files
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    # Production: serve media files manually since DEBUG=False
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    ]

# Serve frontend assets
if settings.DEBUG:
    # Serve frontend assets (but not catch-all root path that conflicts with admin)
    urlpatterns += static('/assets/', document_root=os.path.join(settings.BASE_DIR.parent, 'frontend', 'dist', 'spa', 'assets'))
    # Remove the catch-all static serving that conflicts with admin
    # urlpatterns += static('/', document_root=os.path.join(settings.BASE_DIR.parent, 'frontend', 'public'))
else:
    # For production, serve frontend assets
    urlpatterns += static('/assets/', document_root=os.path.join(settings.BASE_DIR.parent, 'frontend', 'dist', 'spa', 'assets'))

# Serve React app for all other routes (must be last)
# Note: This catch-all pattern is commented out to avoid conflicts with admin
# urlpatterns += [
#     path('', TemplateView.as_view(template_name='index.html'), name='frontend'),
# ]


