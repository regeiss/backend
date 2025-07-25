#!/bin/bash

echo "=== DIAGNÓSTICO COMPLETO - LOGIN API ==="
echo

# Função para testar endpoint
test_endpoint() {
    local url=$1
    local description=$2
    echo "🔍 Testando: $description"
    echo "URL: $url"
    
    response=$(curl -s -w "HTTP_CODE:%{http_code}" "$url")
    http_code=$(echo "$response" | grep -o "HTTP_CODE:[0-9]*" | cut -d: -f2)
    body=$(echo "$response" | sed 's/HTTP_CODE:[0-9]*$//')
    
    if [ "$http_code" -eq 200 ]; then
        echo "✅ Status: $http_code"
    else
        echo "❌ Status: $http_code"
    fi
    echo "Response: $body"
    echo
}

# 1. Verificar containers
echo "🐳 VERIFICANDO CONTAINERS"
echo "=" * 50
docker compose ps

echo
echo "📡 VERIFICANDO ENDPOINTS BÁSICOS"
echo "=" * 50
test_endpoint "http://10.13.65.37:8001/" "Root da API"
test_endpoint "http://10.13.65.37:8001/api/v1/" "API v1 Info"
test_endpoint "http://10.13.65.37:8001/api/v1/health/" "Health Check"

# 2. Diagnóstico detalhado dos usuários
echo "👥 DIAGNÓSTICO DETALHADO DOS USUÁRIOS"
echo "=" * 50

docker compose exec backend python manage.py shell -c "
import os
import django
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.conf import settings
import traceback

print('🔧 CONFIGURAÇÕES DO SISTEMA:')
print(f'DEBUG: {settings.DEBUG}')
print(f'SECRET_KEY configurada: {bool(settings.SECRET_KEY)}')
print(f'DATABASE: {settings.DATABASES[\"default\"][\"ENGINE\"]}')
print()

print('👥 ANÁLISE DETALHADA DOS USUÁRIOS:')
print('-' * 60)

usernames_to_check = ['robertogeiss', 'admin']

for username in usernames_to_check:
    print(f'🔍 VERIFICANDO: {username}')
    print('-' * 30)
    
    try:
        # Verificar se usuário existe
        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            print(f'✅ Usuário encontrado!')
            print(f'   ID: {user.id}')
            print(f'   Username: {user.username}')
            print(f'   Email: {user.email}')
            print(f'   is_active: {user.is_active}')
            print(f'   is_staff: {user.is_staff}')
            print(f'   is_superuser: {user.is_superuser}')
            print(f'   last_login: {user.last_login}')
            print(f'   date_joined: {user.date_joined}')
            print(f'   password (hash): {user.password[:20]}...')
            
            # Testar check_password diretamente
            passwords_to_test = []
            if username == 'robertogeiss':
                passwords_to_test = ['testeSenha', '(*erdeeth0*)']
            elif username == 'admin':
                passwords_to_test = ['admin123']
                
            for pwd in passwords_to_test:
                check_result = user.check_password(pwd)
                print(f'   check_password(\"{pwd}\"): {check_result}')
            
            # Testar authenticate
            for pwd in passwords_to_test:
                auth_user = authenticate(username=username, password=pwd)
                if auth_user:
                    print(f'   authenticate(\"{username}\", \"{pwd}\"): ✅ Sucesso')
                else:
                    print(f'   authenticate(\"{username}\", \"{pwd}\"): ❌ Falhou')
            
        else:
            print(f'❌ Usuário {username} NÃO encontrado!')
            
    except Exception as e:
        print(f'❌ Erro ao verificar {username}: {e}')
        traceback.print_exc()
    
    print()

print('🔧 CRIANDO/RECRIANDO USUÁRIOS COM SENHAS SIMPLES:')
print('-' * 60)

# Recriar usuários com senhas mais simples para teste
test_users = [
    {'username': 'roberto', 'password': 'teste123', 'email': 'roberto@test.com'},
    {'username': 'admin', 'password': 'admin123', 'email': 'admin@test.com'},
]

for user_data in test_users:
    username = user_data['username']
    password = user_data['password']
    email = user_data['email']
    
    try:
        # Deletar se existir
        if User.objects.filter(username=username).exists():
            User.objects.get(username=username).delete()
            print(f'🗑️ Usuário {username} deletado')
        
        # Criar novo
        user = User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )
        print(f'✅ Usuário {username} criado!')
        
        # Verificar imediatamente
        check_result = user.check_password(password)
        print(f'   check_password: {check_result}')
        
        auth_user = authenticate(username=username, password=password)
        if auth_user:
            print(f'   authenticate: ✅ Sucesso')
        else:
            print(f'   authenticate: ❌ Falhou')
            
    except Exception as e:
        print(f'❌ Erro ao criar {username}: {e}')

print()
print('📋 USUÁRIOS FINAIS NO BANCO:')
print('-' * 30)
for user in User.objects.all():
    status = '✅' if user.is_active else '❌'
    admin = '👑' if user.is_superuser else '👤'
    print(f'{admin} {user.username:15} | {user.email:25} | {status}')
"

# 3. Testar endpoints de login
echo "🔐 TESTANDO ENDPOINTS DE LOGIN"
echo "=" * 50

# Testar com usuários simples
test_login() {
    local username=$1
    local password=$2
    local endpoint=$3
    local description=$4
    
    echo "🔍 Testando: $description"
    echo "Username: $username | Password: $password"
    echo "Endpoint: $endpoint"
    
    response=$(curl -s -w "HTTP_CODE:%{http_code}" -X POST "$endpoint" \
        -H "Content-Type: application/json" \
        -d "{\"username\": \"$username\", \"password\": \"$password\"}")
    
    http_code=$(echo "$response" | grep -o "HTTP_CODE:[0-9]*" | cut -d: -f2)
    body=$(echo "$response" | sed 's/HTTP_CODE:[0-9]*$//')
    
    if [ "$http_code" -eq 200 ]; then
        echo "✅ Status: $http_code"
        if echo "$body" | grep -q '"success": true'; then
            echo "✅ Login: Sucesso"
        else
            echo "❌ Login: Falhou"
        fi
    else
        echo "❌ Status: $http_code"
    fi
    
    echo "Response: $body"
    echo
}

# Testar ambos os endpoints
test_login "roberto" "teste123" "http://10.13.65.37:8001/api/v1/auth/login/" "Login Customizado"
test_login "admin" "admin123" "http://10.13.65.37:8001/api/v1/auth/login/" "Login Customizado"

test_login "roberto" "teste123" "http://10.13.65.37:8001/api/v1/auth/token/" "JWT Padrão"
test_login "admin" "admin123" "http://10.13.65.37:8001/api/v1/auth/token/" "JWT Padrão"

# 4. Verificar logs
echo "📋 LOGS RECENTES DO BACKEND"
echo "=" * 50
docker compose logs --tail=20 backend

echo
echo "=== DIAGNÓSTICO CONCLUÍDO ==="
echo
echo "📋 CREDENCIAIS PARA TESTE:"
echo "   • roberto : teste123"
echo "   • admin   : admin123"
echo
echo "🔗 ENDPOINTS PARA TESTE:"
echo "   • Login Customizado: http://10.13.65.37:8001/api/v1/auth/login/"
echo "   • JWT Padrão:        http://10.13.65.37:8001/api/v1/auth/token/"
