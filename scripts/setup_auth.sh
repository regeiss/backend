#!/bin/bash
# quick_fix_authentication.sh

echo "🚨 Corrigindo erro: ModuleNotFoundError: No module named 'authentication.urls'"
echo ""

# Parar containers
echo "⏹️ Parando containers..."
docker compose down

# Verificar e criar estrutura necessária
echo "📁 Verificando estrutura de diretórios..."
mkdir -p backend/authentication

# Criar __init__.py
echo "🐍 Criando __init__.py..."
cat > backend/authentication/__init__.py << 'EOF'
# Arquivo para tornar o diretório um módulo Python válido
EOF

# Criar apps.py
echo "📱 Criando apps.py..."
cat > backend/authentication/apps.py << 'EOF'
from django.apps import AppConfig

class AuthenticationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'authentication'
EOF

# Criar urls.py corrigido
echo "🔗 Criando urls.py..."
cat > backend/authentication/urls.py << 'EOF'
from django.urls import path
from . import views

app_name = 'authentication'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('user/', views.user_profile_view, name='user_profile'),
    path('logout/', views.logout_view, name='logout'),
    path('change-password/', views.change_password_view, name='change_password'),
]
EOF

# Verificar se views.py existe
if [ ! -f "backend/authentication/views.py" ]; then
    echo "📝 Criando views.py básico..."
    cat > backend/authentication/views.py << 'EOF'
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response({
            'success': False,
            'message': 'Username e password são obrigatórios'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    user = authenticate(username=username, password=password)
    
    if user and user.is_active:
        refresh = RefreshToken.for_user(user)
        return Response({
            'success': True,
            'token': str(refresh.access_token),
            'refresh': str(refresh),
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
            }
        })
    else:
        return Response({
            'success': False,
            'message': 'Credenciais inválidas'
        }, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile_view(request):
    user = request.user
    return Response({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
    })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    return Response({
        'success': True,
        'message': 'Logout realizado com sucesso'
    })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password_view(request):
    user = request.user
    current_password = request.data.get('current_password')
    new_password = request.data.get('new_password')
    
    if not user.check_password(current_password):
        return Response({
            'success': False,
            'message': 'Senha atual incorreta'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    user.set_password(new_password)
    user.save()
    
    return Response({
        'success': True,
        'message': 'Senha alterada com sucesso'
    })
EOF
fi

# Corrigir urls.py principal
echo "🔧 Corrigindo config/urls.py..."
cat > backend/config/urls.py << 'EOF'
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

# API URLs v1
api_v1_patterns = [
    # JWT Authentication
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    # Custom authentication endpoints
    path('auth/', include('authentication.urls')),
    
    # Apps
    path('', include('apps.api.urls')),
    path('cadastro/', include('apps.cadastro.urls')),
]

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # Root
    path('', lambda request: HttpResponse("Bem-vindo à API do Cadastro Unificado!"), name='home'),
    
    # API v1
    path('api/v1/', include(api_v1_patterns)),
    
    # Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
EOF

# Verificar estrutura criada
echo "📋 Estrutura criada:"
find backend/authentication -type f -name "*.py" | head -10

# Verificar sintaxe
echo "🔍 Verificando sintaxe..."
python3 -m py_compile backend/authentication/*.py
python3 -m py_compile backend/config/urls.py

# Subir containers
echo "🚀 Iniciando containers..."
docker compose up -d

# Aguardar containers subirem
echo "⏱️ Aguardando containers..."
sleep 10

# Verificar se o erro foi corrigido
echo "✅ Verificando se o erro foi corrigido..."
if docker-compose logs backend 2>&1 | grep -q "ModuleNotFoundError.*authentication"; then
    echo "❌ Erro ainda presente nos logs"
    echo "📋 Logs atuais:"
    docker-compose logs backend --tail=20
else
    echo "✅ Erro corrigido! Container iniciou sem erros."
fi

# Testar endpoint
echo "🧪 Testando endpoint..."
sleep 5
response=$(curl -s -o /dev/null -w "%{http_code}" http://10.13.65.37:8001/api/v1/health/)
if [ "$response" = "200" ]; then
    echo "✅ API respondendo corretamente!"
else
    echo "⚠️ API retornou código: $response"
fi

echo ""
echo "🎉 Correção concluída!"
echo ""
echo "📚 URLs disponíveis:"
echo "   - Health check: http://10.13.65.37:8001/api/v1/health/"
echo "   - API docs: http://10.13.65.37:8001/api/docs/"
echo "   - Login: http://10.13.65.37:8001/api/v1/auth/login/"
echo ""
echo "🔍 Para verificar logs: docker-compose logs backend"
