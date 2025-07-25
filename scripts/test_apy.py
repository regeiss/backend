#!/usr/bin/env python3
"""
Script para testar a API
"""
import requests
import json

BASE_URL = "http://10.13.65.37:8001/api/v1"

def test_health():
    """Testa o endpoint de health check"""
    print("🔍 Testando health check...")
    response = requests.get(f"{BASE_URL}/health/")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

def test_api_info():
    """Testa o endpoint de informações da API"""
    print("🔍 Testando informações da API...")
    response = requests.get(f"{BASE_URL}/")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

def test_register():
    """Testa o registro de usuário"""
    print("🔍 Testando registro de usuário...")
    data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpass123",
        "password_confirm": "testpass123",
        "first_name": "Test",
        "last_name": "User"
    }
    response = requests.post(f"{BASE_URL}/auth/register/", json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

def test_login():
    """Testa o login"""
    print("🔍 Testando login...")
    data = {
        "username": "testuser",
        "password": "testpass123"
    }
    response = requests.post(f"{BASE_URL}/auth/login/", json=data)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        tokens = response.json()
        print(f"Response: {json.dumps(tokens, indent=2)}")
        return tokens['access']
    else:
        print(f"Erro: {response.text}")
        return None

def test_profile(token):
    """Testa o endpoint de perfil"""
    print("🔍 Testando perfil do usuário...")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/auth/profile/", headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

def test_pessoas_list(token=None):
    """Testa a listagem de pessoas"""
    print("🔍 Testando listagem de pessoas...")
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    response = requests.get(f"{BASE_URL}/cadastro/pessoas/", headers=headers)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    else:
        print(f"Erro: {response.text}")
    print()

if __name__ == "__main__":
    print("=== Testando API Cadastro Unificado ===\n")
    
    # Testes públicos
    test_health()
    test_api_info()
    
    # Testes de autenticação
    test_register()
    token = test_login()
    
    if token:
        test_profile(token)
        test_pessoas_list(token)
    
    print("=== Testes concluídos ===")
