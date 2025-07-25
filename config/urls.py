# ✅ NOVA VERSÃO CORRIGIDA
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.http import HttpResponse
from django.conf.urls.static import static
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

# API v1 URLs
api_v1_patterns = [
    # JWT Authentication (padrão DRF)
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    # Apps
    path('', include('apps.api.urls')),
    path('cadastro/', include('apps.cadastro.urls')),
    
    # Custom Authentication
    path('auth/', include('authentication.urls')),
]

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # Home
    path('', lambda request: HttpResponse("Bem-vindo à API do Cadastro Unificado!"), name='home'),
    
    # API v1
    path('api/v1/', include(api_v1_patterns)),
    
    # API Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
