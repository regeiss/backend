#!/bin/bash

# Script para gerar e testar documentação da API
# Autor: Sistema de Cadastro Unificado
# Data: $(date)

set -e

echo "🔧 Gerando documentação da API..."

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Função para log colorido
log() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Verificar se o container está rodando
log "Verificando status dos containers..."
if ! docker compose ps | grep -q "Up"; then
    error "Containers não estão rodando. Iniciando..."
    docker compose up -d
    sleep 10
fi

# Aguardar o backend estar pronto
log "Aguardando backend estar pronto..."
for i in {1..30}; do
    if curl -s -k https://10.13.65.37:8443/api/v1/health/ > /dev/null 2>&1; then
        log "Backend está pronto!"
        break
    fi
    if [ $i -eq 30 ]; then
        error "Timeout: Backend não respondeu em 30 segundos"
        exit 1
    fi
    echo -n "."
    sleep 2
done

# Testar endpoints de documentação
log "Testando endpoints de documentação..."

# Testar schema OpenAPI
log "Testando schema OpenAPI..."
if curl -s -k https://10.13.65.37:8443/api/schema/ | jq . > /dev/null 2>&1; then
    log "✅ Schema OpenAPI está funcionando"
else
    error "❌ Erro no schema OpenAPI"
fi

# Testar Swagger UI
log "Testando Swagger UI..."
if curl -s -k https://10.13.65.37:8443/api/docs/ | grep -q "swagger-ui" > /dev/null 2>&1; then
    log "✅ Swagger UI está funcionando"
else
    error "❌ Erro no Swagger UI"
fi

# Testar ReDoc
log "Testando ReDoc..."
if curl -s -k https://10.13.65.37:8443/api/redoc/ | grep -q "redoc" > /dev/null 2>&1; then
    log "✅ ReDoc está funcionando"
else
    error "❌ Erro no ReDoc"
fi

# Gerar relatório de documentação
log "Gerando relatório de documentação..."

cat > API_DOCS_REPORT.md << EOF
# 📊 Relatório de Documentação da API

## 📅 Data: $(date)

## 🔗 URLs de Documentação

- **Swagger UI**: https://10.13.65.37:8443/api/docs/
- **ReDoc**: https://10.13.65.37:8443/api/redoc/
- **OpenAPI Schema**: https://10.13.65.37:8443/api/schema/

## 📋 Endpoints Disponíveis

### 🔐 Autenticação
- \`POST /api/v1/auth/login/\` - Login com JWT
- \`POST /api/v1/auth/refresh/\` - Renovar token
- \`POST /api/v1/auth/verify/\` - Verificar token

### 👥 Responsáveis
- \`GET /api/v1/cadastro/responsaveis/\` - Listar responsáveis
- \`POST /api/v1/cadastro/responsaveis/\` - Criar responsável
- \`GET /api/v1/cadastro/responsaveis/{id}/\` - Obter responsável
- \`PUT /api/v1/cadastro/responsaveis/{id}/\` - Atualizar responsável
- \`DELETE /api/v1/cadastro/responsaveis/{id}/\` - Excluir responsável
- \`GET /api/v1/cadastro/responsaveis/{id}/com_membros/\` - Responsável com membros
- \`GET /api/v1/cadastro/responsaveis/{id}/com_demandas/\` - Responsável com demandas
- \`GET /api/v1/cadastro/responsaveis/buscar_por_cpf/\` - Buscar por CPF

### 👤 Membros
- \`GET /api/v1/cadastro/membros/\` - Listar membros
- \`POST /api/v1/cadastro/membros/\` - Criar membro
- \`GET /api/v1/cadastro/membros/{id}/\` - Obter membro
- \`PUT /api/v1/cadastro/membros/{id}/\` - Atualizar membro
- \`DELETE /api/v1/cadastro/membros/{id}/\` - Excluir membro
- \`GET /api/v1/cadastro/membros/por_responsavel/\` - Membros por responsável

### 🏥 Demandas de Saúde
- \`GET /api/v1/cadastro/demandas-saude/\` - Listar demandas de saúde
- \`POST /api/v1/cadastro/demandas-saude/\` - Criar demanda de saúde
- \`GET /api/v1/cadastro/demandas-saude/grupos_prioritarios/\` - Grupos prioritários

### 🏫 Demandas de Educação
- \`GET /api/v1/cadastro/demandas-educacao/\` - Listar demandas de educação
- \`POST /api/v1/cadastro/demandas-educacao/\` - Criar demanda de educação

### 🏠 Demandas de Habitação
- \`GET /api/v1/cadastro/demandas-habitacao/\` - Listar demandas de habitação
- \`POST /api/v1/cadastro/demandas-habitacao/\` - Criar demanda de habitação

### 🐕 Demandas de Ambiente
- \`GET /api/v1/cadastro/demandas-ambiente/\` - Listar demandas de ambiente
- \`POST /api/v1/cadastro/demandas-ambiente/\` - Criar demanda de ambiente

### 📋 Demandas Internas
- \`GET /api/v1/cadastro/demandas-internas/\` - Listar demandas internas
- \`POST /api/v1/cadastro/demandas-internas/\` - Criar demanda interna
- \`GET /api/v1/cadastro/demandas-internas/por_status/\` - Por status

### 🏢 Alojamentos
- \`GET /api/v1/cadastro/alojamentos/\` - Listar alojamentos

### 📮 CEPs Atingidos
- \`GET /api/v1/cadastro/ceps-atingidos/\` - Listar CEPs atingidos

### 🔍 Desaparecidos
- \`GET /api/v1/cadastro/desaparecidos/\` - Listar desaparecidos
- \`POST /api/v1/cadastro/desaparecidos/\` - Criar registro de desaparecido
- \`GET /api/v1/cadastro/desaparecidos/recentes/\` - Desaparecidos recentes

## 🔧 Funcionalidades

### ✅ Implementado
- [x] Documentação Swagger UI
- [x] Documentação ReDoc
- [x] Schema OpenAPI
- [x] Autenticação JWT
- [x] Filtros e busca
- [x] Paginação
- [x] Ordenação
- [x] Exemplos de uso
- [x] Tags organizadas
- [x] Descrições detalhadas

### 📝 Melhorias Sugeridas
- [ ] Adicionar mais exemplos de resposta
- [ ] Documentar códigos de erro
- [ ] Adicionar testes automatizados
- [ ] Implementar rate limiting
- [ ] Adicionar validação de entrada

## 🚀 Como Usar

1. **Acesse a documentação**: https://10.13.65.37:8443/api/docs/
2. **Faça login**: Use o endpoint \`/api/v1/auth/login/\`
3. **Copie o token**: Use o token no header \`Authorization: Bearer {token}\`
4. **Teste os endpoints**: Use o botão "Try it out" no Swagger UI

## 📞 Suporte

Para dúvidas sobre a API, consulte:
- Documentação completa: \`API_DOCUMENTATION.md\`
- Swagger UI: https://10.13.65.37:8443/api/docs/
- ReDoc: https://10.13.65.37:8443/api/redoc/

EOF

log "✅ Relatório gerado: API_DOCS_REPORT.md"

# Testar alguns endpoints específicos
log "Testando endpoints específicos..."

# Testar health check
if curl -s -k https://10.13.65.37:8443/api/v1/health/ | grep -q "healthy" > /dev/null 2>&1; then
    log "✅ Health check funcionando"
else
    error "❌ Health check falhou"
fi

# Testar schema com curl
log "Baixando schema OpenAPI..."
curl -s -k https://10.13.65.37:8443/api/schema/ > openapi_schema.json

if [ -s openapi_schema.json ]; then
    log "✅ Schema baixado com sucesso"
    log "📊 Tamanho do schema: $(wc -c < openapi_schema.json) bytes"
else
    error "❌ Falha ao baixar schema"
fi

# Verificar se o schema é válido JSON
if jq . openapi_schema.json > /dev/null 2>&1; then
    log "✅ Schema JSON válido"
else
    error "❌ Schema JSON inválido"
fi

# Contar endpoints no schema
ENDPOINTS=$(jq '.paths | keys | length' openapi_schema.json)
log "📊 Total de endpoints documentados: $ENDPOINTS"

# Contar tags
TAGS=$(jq '.tags | length' openapi_schema.json)
log "📊 Total de tags: $TAGS"

# Mostrar tags disponíveis
log "🏷️ Tags disponíveis:"
jq -r '.tags[].name' openapi_schema.json | while read tag; do
    echo "  - $tag"
done

log "🎉 Documentação gerada com sucesso!"
log "📖 Acesse: https://10.13.65.37:8443/api/docs/"
log "📋 Relatório: API_DOCS_REPORT.md"
log "📄 Schema: openapi_schema.json"

echo ""
echo "🔗 Links úteis:"
echo "  - Swagger UI: https://10.13.65.37:8443/api/docs/"
echo "  - ReDoc: https://10.13.65.37:8443/api/redoc/"
echo "  - Schema: https://10.13.65.37:8443/api/schema/"
echo "" 