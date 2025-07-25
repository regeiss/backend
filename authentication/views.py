from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

# ✅ Imports do DRF Spectacular
from drf_spectacular.utils import extend_schema, OpenApiResponse
from drf_spectacular.types import OpenApiTypes

# ✅ Imports dos serializers
from .serializers import (
    LoginSerializer, LoginResponseSerializer, UserProfileSerializer,
    LogoutSerializer, LogoutResponseSerializer, ChangePasswordSerializer,
    ChangePasswordResponseSerializer, ErrorResponseSerializer
)


@extend_schema(
    summary="Login de usuário",
    description="Autentica um usuário e retorna tokens JWT para acesso à API",
    request=LoginSerializer,
    responses={
        200: OpenApiResponse(
            response=LoginResponseSerializer,
            description="Login realizado com sucesso"
        ),
        400: OpenApiResponse(
            response=ErrorResponseSerializer,
            description="Dados inválidos"
        ),
        401: OpenApiResponse(
            response=ErrorResponseSerializer,
            description="Credenciais inválidas ou conta desativada"
        ),
    },
    tags=['Autenticação']
)
@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """
    Endpoint de login customizado que retorna tokens JWT
    
    Recebe username e password, valida as credenciais e retorna:
    - Token de acesso (access)
    - Token de refresh
    - Dados do usuário
    """
    serializer = LoginSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response({
            'success': False,
            'message': 'Dados inválidos',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    user = serializer.validated_data['user']
    
    # Gerar tokens JWT
    refresh = RefreshToken.for_user(user)
    
    return Response({
        'success': True,
        'token': str(refresh.access_token),
        'refresh': str(refresh),
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'is_staff': user.is_staff,
            'is_active': user.is_active,
            'date_joined': user.date_joined.isoformat(),
        }
    })


@extend_schema(
    summary="Perfil do usuário",
    description="Retorna informações do usuário autenticado",
    responses={
        200: OpenApiResponse(
            response=UserProfileSerializer,
            description="Dados do usuário"
        ),
        401: OpenApiResponse(
            response=ErrorResponseSerializer,
            description="Token inválido ou expirado"
        ),
    },
    tags=['Autenticação']
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile_view(request):
    """
    Retorna informações do usuário autenticado
    
    Requer token JWT válido no header Authorization
    """
    serializer = UserProfileSerializer(request.user)
    return Response(serializer.data)


@extend_schema(
    summary="Logout de usuário",
    description="Invalida o token de refresh do usuário (logout)",
    request=LogoutSerializer,
    responses={
        200: OpenApiResponse(
            response=LogoutResponseSerializer,
            description="Logout realizado com sucesso"
        ),
        400: OpenApiResponse(
            response=ErrorResponseSerializer,
            description="Erro ao processar logout"
        ),
        401: OpenApiResponse(
            response=ErrorResponseSerializer,
            description="Token inválido"
        ),
    },
    tags=['Autenticação']
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """
    Endpoint de logout que invalida o token de refresh
    
    Opcionalmente recebe o refresh token para invalidar.
    Se não fornecido, apenas confirma o logout.
    """
    try:
        refresh_token = request.data.get('refresh')
        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
            except Exception:
                pass  # Token já pode estar inválido
        
        return Response({
            'success': True,
            'message': 'Logout realizado com sucesso'
        })
    except Exception as e:
        return Response({
            'success': False,
            'message': 'Erro ao fazer logout'
        }, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    summary="Alterar senha",
    description="Permite ao usuário alterar sua senha atual",
    request=ChangePasswordSerializer,
    responses={
        200: OpenApiResponse(
            response=ChangePasswordResponseSerializer,
            description="Senha alterada com sucesso"
        ),
        400: OpenApiResponse(
            response=ErrorResponseSerializer,
            description="Senha atual incorreta ou nova senha inválida"
        ),
        401: OpenApiResponse(
            response=ErrorResponseSerializer,
            description="Token inválido"
        ),
    },
    tags=['Autenticação']
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password_view(request):
    """
    Permite alterar a senha do usuário autenticado
    
    Requer a senha atual para confirmação e uma nova senha válida.
    """
    serializer = ChangePasswordSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response({
            'success': False,
            'message': 'Dados inválidos',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    user = request.user
    current_password = serializer.validated_data['current_password']
    new_password = serializer.validated_data['new_password']
    
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
