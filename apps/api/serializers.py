"""
Serializers gerais da API
"""
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):
    """Serializer para User"""
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'date_joined')
        read_only_fields = ('id', 'date_joined')


class RegisterSerializer(serializers.ModelSerializer):
    """Serializer para registro de usuários"""
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password_confirm', 'first_name', 'last_name')
        
    def validate_email(self, value):
        """Valida se o email já existe"""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Este email já está cadastrado.")
        return value
    
    def validate(self, attrs):
        """Valida se as senhas correspondem"""
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password": "As senhas não correspondem."})
        return attrs
    
    def create(self, validated_data):
        """Cria o usuário"""
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    """Serializer para login"""
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        
        if username and password:
            user = authenticate(username=username, password=password)
            
            if not user:
                raise serializers.ValidationError('Credenciais inválidas.')
            
            if not user.is_active:
                raise serializers.ValidationError('Usuário desativado.')
            
            attrs['user'] = user
            return attrs
        else:
            raise serializers.ValidationError('Username e password são obrigatórios.')

# Serializers para as views da API
class HealthCheckSerializer(serializers.Serializer):
    """Serializer para resposta do health check"""
    status = serializers.CharField(read_only=True)
    message = serializers.CharField(read_only=True)
    version = serializers.CharField(read_only=True)


class EndpointInfoSerializer(serializers.Serializer):
    """Serializer para informações de endpoints"""
    login = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)
    verify = serializers.CharField(read_only=True)
    register = serializers.CharField(read_only=True)


class CadastroEndpointsSerializer(serializers.Serializer):
    """Serializer para endpoints de cadastro"""
    pessoas = serializers.CharField(read_only=True)
    enderecos = serializers.CharField(read_only=True)


class DocsEndpointsSerializer(serializers.Serializer):
    """Serializer para endpoints de documentação"""
    swagger = serializers.CharField(read_only=True)
    redoc = serializers.CharField(read_only=True)
    schema = serializers.CharField(read_only=True)


class AllEndpointsSerializer(serializers.Serializer):
    """Serializer para todos os endpoints"""
    auth = EndpointInfoSerializer(read_only=True)
    cadastro = CadastroEndpointsSerializer(read_only=True)
    docs = DocsEndpointsSerializer(read_only=True)


class ApiInfoSerializer(serializers.Serializer):
    """Serializer para informações da API"""
    name = serializers.CharField(read_only=True)
    version = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)
    endpoints = AllEndpointsSerializer(read_only=True)
    base_url = serializers.CharField(read_only=True)
