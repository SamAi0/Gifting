"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
import os

def home(request):
    return JsonResponse({
        "status": "online",
        "message": "Gifting API is running 🚀",
        "endpoints": [
            "/api/products/",
            "/api/orders/",
            "/admin/"
        ]
    })

from django.views.generic.base import RedirectView

urlpatterns = [
    path('', home, name='home'),
    path('favicon.ico', RedirectView.as_view(url='/static/favicon.ico')),
    path('admin/', admin.site.urls),
    # Consolidated API URLs
    path('api/', include([
        path('', include('api.urls')),
        path('', include('products.urls')),
        path('auth/', include('authentication.urls')),
        path('orders/', include('orders.urls')),
    ])),
]

from django.views.static import serve
from django.urls import re_path

def cors_static(prefix, document_root, **kwargs):
    """
    A wrapper around django.views.static.serve that adds CORS headers.
    """
    return [
        re_path(r'^%s(?P<path>.*)$' % prefix.lstrip('/'), cors_serve, {'document_root': document_root, **kwargs})
    ]

def cors_serve(request, path, document_root=None, show_indexes=False):
    response = serve(request, path, document_root, show_indexes)
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "GET, OPTIONS"
    response["Access-Control-Allow-Headers"] = "Origin, Content-Type, Accept, Authorization"
    return response

# Serve media and static files with CORS headers
# We use /cors-static/ and /cors-media/ to avoid conflicts with default Django handlers
# which often bypass middleware and don't add CORS headers in development.
urlpatterns += [
    path('cors-static/<path:path>', cors_serve, {'document_root': os.path.join(settings.BASE_DIR, 'static')}),
    path('cors-media/<path:path>', cors_serve, {'document_root': settings.MEDIA_ROOT}),
]

if settings.DEBUG:
    # Also add standard paths for convenience
    urlpatterns += static(settings.STATIC_URL, document_root=os.path.join(settings.BASE_DIR, 'static'))
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns += cors_static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += cors_static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
