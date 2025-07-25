from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class LoginSerializer(serializers.Serializer):
    """Serializer para login customizado"""
    username = serializers.CharField(max_length=150, help_text="Nome de usuário")
    password = serializers.CharField(
        write_only=True, 
        style={'input_type': 'password'},
        help_text="Senha do usuário"
    )
    
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


class LoginResponseSerializer(serializers.Serializer):
    """Serializer para resposta do login"""
    success = serializers.BooleanField(help_text="Se o login foi bem-sucedido")
    token = serializers.CharField(help_text="Token JWT de acesso")
    refresh = serializers.CharField(help_text="Token de refresh")
    user = serializers.DictField(help_text="Dados do usuário logado")
    
    class Meta:
        examples = {
            'application/json': {
                'success': True,
                'token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...',
                'refresh': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...',
                'user': {
                    'id': 1,
                    'username': 'admin',
                    'email': 'admin@example.com',
                    'first_name': 'Admin',
                    'last_name': 'User',
                    'is_staff': True,
                    'is_active': True,
                    'date_joined': '2024-01-01T00:00:00Z'
                }
            }
        }


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer para perfil do usuário"""
    date_joined = serializers.DateTimeField(read_only=True, help_text="Data de criação da conta")
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'is_staff', 'is_active', 'date_joined'
        ]
        read_only_fields = ['id', 'username', 'is_staff', 'is_active', 'date_joined']


class LogoutSerializer(serializers.Serializer):
    """Serializer para logout"""
    refresh = serializers.CharField(
        required=False,
        help_text="Token de refresh para invalidar (opcional)"
    )


class LogoutResponseSerializer(serializers.Serializer):
    """Serializer para resposta do logout"""
    success = serializers.BooleanField(help_text="Se o logout foi bem-sucedido")
    message = serializers.CharField(help_text="Mensagem de confirmação")


class ChangePasswordSerializer(serializers.Serializer):
    """Serializer para alteração de senha"""
    current_password = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'},
        help_text="Senha atual do usuário"
    )
    new_password = serializers.CharField(
        write_only=True,
        min_length=8,
        style={'input_type': 'password'},
        help_text="Nova senha (mínimo 8 caracteres)"
    )
    
    def validate_new_password(self, value):
        """Validação básica da nova senha"""
        if len(value) < 8:
            raise serializers.ValidationError("A nova senha deve ter pelo menos 8 caracteres.")
        return value


class ChangePasswordResponseSerializer(serializers.Serializer):
    """Serializer para resposta da alteração de senha"""
    success = serializers.BooleanField(help_text="Se a alteração foi bem-sucedida")
    message = serializers.CharField(help_text="Mensagem de confirmação")


class ErrorResponseSerializer(serializers.Serializer):
    """Serializer para respostas de erro"""
    success = serializers.BooleanField(default=False, help_text="Sempre False para erros")
    message = serializers.CharField(help_text="Mensagem de erro")
    
    class Meta:
        examples = {
            'application/json': {
                'success': False,
                'message': 'Credenciais inválidas'
            }
        }
