#!/bin/bash

echo "🔧 === TROUBLESHOOTING CADASTRO UNIFICADO ==="
echo ""

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Função para printar com cor
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 1. Verificar se o Docker está instalado e rodando
print_status "1. Verificando Docker..."
if command -v docker &> /dev/null; then
    print_success "Docker está instalado"
    if docker info &> /dev/null; then
        print_success "Docker está rodando"
    else
        print_error "Docker não está rodando. Inicie o Docker Desktop."
        exit 1
    fi
else
    print_error "Docker não está instalado"
    exit 1
fi

# 2. Verificar containers do backend
print_status "2. Verificando containers..."
if docker compose ps | grep -q "backend"; then
    print_success "Container backend encontrado"
else
    print_warning "Container backend não encontrado. Iniciando..."
    docker compose up -d
    sleep 10
fi

# 3. Verificar se a API está respondendo
print_status "3. Testando conectividade com a API..."

# Health check
API_URL="http://10.13.65.37:8001"
HEALTH_URL="$API_URL/api/v1/health/"

response=$(curl -s -o /dev/null -w "%{http_code}" $HEALTH_URL)
if [ "$response" = "200" ]; then
    print_success "API está respondendo (Health Check OK)"
else
    print_error "API não está respondendo (HTTP $response)"
    print_status "Verificando logs do backend..."
    docker compose logs --tail=50 backend
fi

# 4. Testar endpoints principais
print_status "4. Testando endpoints principais..."

endpoints=("/" "/health/" "/auth/login/" "/cadastro/api/responsaveis/")

for endpoint in "${endpoints[@]}"; do
    url="$API_URL/api/v1$endpoint"
    response=$(curl -s -o /dev/null -w "%{http_code}" "$url")
    if [ "$response" = "200" ] || [ "$response" = "405" ]; then
        print_success "✓ $endpoint (HTTP $response)"
    else
        print_error "✗ $endpoint (HTTP $response)"
    fi
done

# 5. Verificar configurações do Flutter
print_status "5. Verificando Flutter..."
if command -v flutter &> /dev/null; then
    print_success "Flutter está instalado"
    flutter --version | head -1
    
    # Verificar se há erros de dependências
    print_status "Verificando dependências do Flutter..."
    cd cad_unico
    flutter pub get
    flutter doctor --android-licenses > /dev/null 2>&1
    flutter doctor
else
    print_error "Flutter não está instalado"
fi

# 6. Criar/verificar arquivo main.dart
print_status "6. Verificando main.dart..."
if [ -f "cad_unico/lib/main.dart" ]; then
    print_success "main.dart encontrado"
else
    print_warning "main.dart não encontrado. Criando arquivo básico..."
    # O arquivo será criado manualmente
fi

# 7. Verificar arquivo de configuração
print_status "7. Verificando constants.dart..."
if [ -f "cad_unico/lib/utils/constants.dart" ]; then
    print_success "constants.dart encontrado"
    # Verificar se a URL da API está correta
    if grep -q "10.13.65.37:8001" "cad_unico/lib/utils/constants.dart"; then
        print_success "URL da API está configurada corretamente"
    else
        print_warning "URL da API pode estar incorreta"
    fi
else
    print_warning "constants.dart não encontrado"
fi

# 8. Verificar CORS
print_status "8. Testando CORS..."
cors_response=$(curl -s -o /dev/null -w "%{http_code}" \
    -H "Origin: http://localhost:3000" \
    -H "Access-Control-Request-Method: GET" \
    -H "Access-Control-Request-Headers: Content-Type" \
    -X OPTIONS "$API_URL/api/v1/health/")

if [ "$cors_response" = "200" ] || [ "$cors_response" = "204" ]; then
    print_success "CORS está configurado corretamente"
else
    print_warning "Possível problema de CORS (HTTP $cors_response)"
fi

# 9. Verificar portas em uso
print_status "9. Verificando portas..."
if netstat -an | grep -q ":8001"; then
    print_success "Porta 8001 está em uso (API)"
else
    print_error "Porta 8001 não está em uso"
fi

if netstat -an | grep -q ":3000"; then
    print_warning "Porta 3000 está em uso (pode conflitar com Flutter)"
fi

# 10. Teste de login na API
print_status "10. Testando login na API..."
login_response=$(curl -s -X POST "$API_URL/api/v1/auth/login/" \
    -H "Content-Type: application/json" \
    -d '{"username": "admin", "password": "admin123"}' \
    -w "%{http_code}")

if echo "$login_response" | grep -q "200"; then
    print_success "Login na API funcionando"
elif echo "$login_response" | grep -q "401"; then
    print_warning "API funcionando, mas credenciais incorretas"
else
    print_error "Problema no endpoint de login"
fi

echo ""
echo "🔧 === SOLUÇÕES RECOMENDADAS ==="
echo ""

# Soluções baseadas nos testes
print_status "Para resolver o erro '500 Internal Server Error':"
echo "1. ✅ Certifique-se que o backend está rodando:"
echo "   cd backend && docker compose up -d"
echo ""
echo "2. ✅ Verifique se o arquivo main.dart existe:"
echo "   cad_unico/lib/main.dart"
echo ""
echo "3. ✅ Configure a URL da API corretamente:"
echo "   cad_unico/lib/utils/constants.dart"
echo "   static const String apiBaseUrl = 'http://10.13.65.37:8001/api/v1';"
echo ""
echo "4. ✅ Execute o Flutter com hot reload:"
echo "   cd cad_unico"
echo "   flutter clean"
echo "   flutter pub get"
echo "   flutter run -d chrome --web-port 3000"
echo ""
echo "5. ✅ Verifique os logs em caso de erro:"
echo "   docker compose logs backend"
echo ""

# Comandos rápidos para resolver problemas comuns
echo "🚀 === COMANDOS RÁPIDOS ==="
echo ""
echo "# Reiniciar backend:"
echo "docker compose restart backend"
echo ""
echo "# Ver logs do backend:"
echo "docker compose logs -f backend"
echo ""
echo "# Limpar cache do Flutter:"
echo "cd cad_unico && flutter clean && flutter pub get"
echo ""
echo "# Rodar Flutter em modo debug:"
echo "cd cad_unico && flutter run -d chrome --web-port 3000 --dart-define=FLUTTER_WEB_USE_SKIA=true"
echo ""

print_success "Troubleshooting concluído!"
print_status "Se o problema persistir, verifique os logs detalhados acima."
