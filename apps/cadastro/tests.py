#!/usr/bin/env python3
"""
Script para testar todas as URLs da API corrigidas
"""
import requests
import json

BASE_URL = "http://10.13.65.37:8001/api/v1"

def test_health():
    """Testa o endpoint de health check"""
    print("🔍 Testando health check...")
    try:
        response = requests.get(f"{BASE_URL}/health/")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        print()
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def test_api_info():
    """Testa o endpoint de informações da API"""
    print("🔍 Testando informações da API...")
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        print()
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def test_jwt_login():
    """Testa o login JWT padrão"""
    print("🔍 Testando login JWT padrão...")
    data = {
        "username": "admin",
        "password": "admin123"
    }
    try:
        response = requests.post(f"{BASE_URL}/auth/login/", json=data)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            tokens = response.json()
            print(f"Response: {json.dumps(tokens, indent=2)}")
            return tokens.get('access')
        else:
            print(f"Erro: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Erro: {e}")
        return None
    finally:
        print()

def test_custom_login():
    """Testa o login customizado"""
    print("🔍 Testando login customizado...")
    data = {
        "username": "admin", 
        "password": "admin123"
    }
    try:
        response = requests.post(f"{BASE_URL}/auth/login/", json=data)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Response: {json.dumps(result, indent=2)}")
            return result.get('token')
        else:
            print(f"Erro: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Erro: {e}")
        return None
    finally:
        print()

def test_register():
    """Testa o registro de usuário"""
    print("🔍 Testando registro de usuário...")
    data = {
        "username": "testuser_" + str(hash("test") % 10000),
        "email": "test@example.com",
        "password": "testpass123",
        "password_confirm": "testpass123",
        "first_name": "Test",
        "last_name": "User"
    }
    try:
        response = requests.post(f"{BASE_URL}/auth/register/", json=data)
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        print()
        return response.status_code == 201
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def test_protected_endpoint(token, endpoint, description):
    """Testa endpoints protegidos"""
    print(f"🔍 Testando {description}...")
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.get(f"{BASE_URL}/{endpoint}", headers=headers)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, dict) and 'results' in data:
                print(f"Total de registros: {data.get('count', 'N/A')}")
                print(f"Resultados na página: {len(data['results'])}")
            else:
                print(f"Response: {json.dumps(data, indent=2)}")
        else:
            print(f"Erro: {response.text}")
        print()
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def test_responsavel_endpoints(token):
    """Testa endpoints específicos de responsáveis"""
    print("🔍 Testando endpoints específicos de responsáveis...")
    
    # Buscar por CPF inexistente
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.get(f"{BASE_URL}/cadastro/responsaveis/buscar_por_cpf/?cpf=99999999999", headers=headers)
        print(f"Busca por CPF inexistente - Status: {response.status_code}")
        
        # Testar ações customizadas se houver dados
        response = requests.get(f"{BASE_URL}/cadastro/responsaveis/", headers=headers)
        if response.status_code == 200:
            data = response.json()
            if data.get('results'):
                # Pegar o primeiro CPF para testar
                primeiro_cpf = data['results'][0].get('cpf')
                if primeiro_cpf:
                    print(f"Testando com CPF: {primeiro_cpf}")
                    
                    # Testar com_membros
                    response = requests.get(f"{BASE_URL}/cadastro/responsaveis/{primeiro_cpf}/com_membros/", headers=headers)
                    print(f"Com membros - Status: {response.status_code}")
                    
                    # Testar com_demandas
                    response = requests.get(f"{BASE_URL}/cadastro/responsaveis/{primeiro_cpf}/com_demandas/", headers=headers)
                    print(f"Com demandas - Status: {response.status_code}")
        print()
    except Exception as e:
        print(f"❌ Erro: {e}")

def main():
    """Executa todos os testes"""
    print("=== Testando API Cadastro Unificado - URLs Corrigidas ===\n")
    
    resultados = {}
    
    # Testes públicos
    resultados['health'] = test_health()
    resultados['api_info'] = test_api_info()
    resultados['register'] = test_register()
    
    # Teste de autenticação
    token = test_jwt_login()
    if not token:
        token = test_custom_login()
    
    if token:
        print(f"✅ Token obtido: {token[:50]}...")
        print()
        
        # Testes de endpoints protegidos
        endpoints = [
            ("auth/profile/", "perfil do usuário"),
            ("cadastro/responsaveis/", "lista de responsáveis"),
            ("cadastro/membros/", "lista de membros"),
            ("cadastro/alojamentos/", "lista de alojamentos"),
            ("cadastro/ceps-atingidos/", "CEPs atingidos"),
            ("cadastro/demandas-saude/", "demandas de saúde"),
            ("cadastro/demandas-educacao/", "demandas de educação"),
            ("cadastro/demandas-habitacao/", "demandas de habitação"),
            ("cadastro/demandas-ambiente/", "demandas de ambiente"),
            ("cadastro/demandas-internas/", "demandas internas"),
            ("cadastro/desaparecidos/", "desaparecidos"),
        ]
        
        for endpoint, desc in endpoints:
            resultados[endpoint] = test_protected_endpoint(token, endpoint, desc)
        
        # Testes específicos
        test_responsavel_endpoints(token)
        
        # Testa grupos prioritários
        resultados['grupos_prioritarios'] = test_protected_endpoint(
            token, 
            "cadastro/demandas-saude/grupos_prioritarios/", 
            "grupos prioritários de saúde"
        )
        
        # Testa desaparecidos recentes
        resultados['desaparecidos_recentes'] = test_protected_endpoint(
            token,
            "cadastro/desaparecidos/recentes/",
            "desaparecidos recentes"
        )
    else:
        print("❌ Não foi possível obter token de autenticação")
    
    # Sumário dos resultados
    print("=" * 50)
    print("📊 RESUMO DOS TESTES")
    print("=" * 50)
    
    sucesso = 0
    total = 0
    
    for teste, resultado in resultados.items():
        total += 1
        if resultado:
            sucesso += 1
            print(f"✅ {teste}")
        else:
            print(f"❌ {teste}")
    
    print(f"\n🎯 Sucessos: {sucesso}/{total} ({(sucesso/total)*100:.1f}%)")
    
    if sucesso == total:
        print("🎉 Todos os testes passaram! URLs estão consistentes.")
    else:
        print("⚠️  Alguns testes falharam. Verifique as URLs e configurações.")

if __name__ == "__main__":
    main()
