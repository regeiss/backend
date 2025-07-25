# backend/apps/api/views.py
"""
Views gerais da API
"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework import generics
from drf_spectacular.utils import extend_schema
from .serializers import (
    UserSerializer, RegisterSerializer, HealthCheckSerializer, 
    ApiInfoSerializer
)


@extend_schema(
    summary="Health check da API",
    description="Endpoint para verificar se a API está funcionando",
    responses={200: HealthCheckSerializer}
)
@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """Endpoint para verificar se a API está funcionando"""
    return Response({
        'status': 'ok',
        'message': 'API Cadastro Unificado está funcionando',
        'version': '1.0.0'
    })


@extend_schema(
    summary="Informações da API",
    description="Retorna informações sobre a API e endpoints disponíveis",
    responses={200: ApiInfoSerializer}
)
@api_view(['GET'])
@permission_classes([AllowAny])
def api_info(request):
    """Retorna informações sobre a API"""
    return Response({
        'name': 'Cadastro Unificado API',
        'version': '1.0.0',
        'description': 'API para integração com banco de dados de cadastro unificado',
        'endpoints': {
            'auth': {
                'login': '/api/v1/auth/login/',
                'refresh': '/api/v1/auth/refresh/',
                'verify': '/api/v1/auth/verify/',
                'register': '/api/v1/auth/register/',
            },
            'cadastro': {
                'pessoas': '/api/v1/cadastro/pessoas/',
                'enderecos': '/api/v1/cadastro/enderecos/',
            },
            'docs': {
                'swagger': '/api/docs/',
                'redoc': '/api/redoc/',
                'schema': '/api/schema/',
            }
        },
        'base_url': 'http://10.13.65.37:8001'
    })


@extend_schema(
    summary="Registro de usuário",
    description="Endpoint para registro de novos usuários",
    request=RegisterSerializer,
    responses={201: UserSerializer}
)
class RegisterView(generics.CreateAPIView):
    """
    Endpoint para registro de novos usuários
    """
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


@extend_schema(
    summary="Perfil do usuário",
    description="Endpoint para visualizar e atualizar perfil do usuário",
    responses={200: UserSerializer}
)
class ProfileView(generics.RetrieveUpdateAPIView):
    """
    Endpoint para visualizar e atualizar perfil do usuário
    """
    serializer_class = UserSerializer
    
    def get_object(self):
        return self.request.user
