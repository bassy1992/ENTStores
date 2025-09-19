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
from django.urls import path, include
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from shop import payment_views

def health_check(request):
    return JsonResponse({"status": "ok", "message": "ENTstore API is running", "cors_enabled": True, "timestamp": "2025-09-18-23:35"})

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
        "message": "Media configuration debug"
    })

urlpatterns = [
    # API endpoints
    path('api/health/', health_check, name='health-check'),
    path('api/csrf-test/', csrf_test, name='csrf-test'),
    path('api/cors-test/', cors_test, name='cors-test'),
    path('api/debug-media/', debug_media, name='debug-media'),
    path('admin/', admin.site.urls),
    path('api/shop/', include('shop.urls')),
    path('api/payments/', include('shop.payment_urls')),
    
    # Legacy endpoints for frontend compatibility (without namespace)
    path('api/stripe/create-checkout-session/', payment_views.create_stripe_checkout_session, name='legacy-stripe'),
    path('api/momo/initiate/', payment_views.initiate_momo_payment, name='legacy-momo-initiate'),
    path('api/momo/status/<str:reference>/', payment_views.check_momo_status, name='legacy-momo-status'),
]

# Serve media files during development and production
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # Serve frontend assets (but not catch-all root path that conflicts with admin)
    urlpatterns += static('/assets/', document_root=os.path.join(settings.BASE_DIR.parent, 'frontend', 'dist', 'spa', 'assets'))
    # Remove the catch-all static serving that conflicts with admin
    # urlpatterns += static('/', document_root=os.path.join(settings.BASE_DIR.parent, 'frontend', 'public'))
else:
    # For production, serve media files through Django (Railway doesn't have a separate media server)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static('/assets/', document_root=os.path.join(settings.BASE_DIR.parent, 'frontend', 'dist', 'spa', 'assets'))

# Serve React app for all other routes (must be last)
# Note: This catch-all pattern is commented out to avoid conflicts with admin
# urlpatterns += [
#     path('', TemplateView.as_view(template_name='index.html'), name='frontend'),
# ]


