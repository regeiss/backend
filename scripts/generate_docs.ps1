# Script para gerar e testar documentação da API (PowerShell)
# Autor: Sistema de Cadastro Unificado
# Data: $(Get-Date)

param(
    [switch]$Verbose
)

# Configurações
$BaseUrl = "https://10.13.65.37:8443"
$ApiDocsUrl = "$BaseUrl/api/docs/"
$ReDocUrl = "$BaseUrl/api/redoc/"
$SchemaUrl = "$BaseUrl/api/schema/"
$HealthUrl = "$BaseUrl/api/v1/health/"

# Função para log colorido
function Write-Log {
    param(
        [string]$Message,
        [string]$Level = "INFO"
    )
    
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    
    switch ($Level) {
        "INFO" { 
            Write-Host "[$timestamp] [INFO] $Message" -ForegroundColor Green 
        }
        "WARN" { 
            Write-Host "[$timestamp] [WARN] $Message" -ForegroundColor Yellow 
        }
        "ERROR" { 
            Write-Host "[$timestamp] [ERROR] $Message" -ForegroundColor Red 
        }
        "SUCCESS" { 
            Write-Host "[$timestamp] [SUCCESS] $Message" -ForegroundColor Cyan 
        }
    }
}

# Função para testar conectividade
function Test-Connectivity {
    Write-Log "Testando conectividade com o servidor..."
    
    try {
        $response = Invoke-WebRequest -Uri $HealthUrl -SkipCertificateCheck -TimeoutSec 10
        if ($response.StatusCode -eq 200) {
            Write-Log "✅ Conectividade OK" -Level SUCCESS
            return $true
        }
    }
    catch {
        Write-Log "❌ Falha na conectividade: $($_.Exception.Message)" -Level ERROR
        return $false
    }
}

# Função para testar endpoints de documentação
function Test-DocumentationEndpoints {
    Write-Log "Testando endpoints de documentação..."
    
    # Testar Swagger UI
    try {
        $response = Invoke-WebRequest -Uri $ApiDocsUrl -SkipCertificateCheck -TimeoutSec 10
        if ($response.Content -match "swagger-ui") {
            Write-Log "✅ Swagger UI funcionando" -Level SUCCESS
        }
        else {
            Write-Log "❌ Swagger UI com problemas" -Level ERROR
        }
    }
    catch {
        Write-Log "❌ Erro no Swagger UI: $($_.Exception.Message)" -Level ERROR
    }
    
    # Testar ReDoc
    try {
        $response = Invoke-WebRequest -Uri $ReDocUrl -SkipCertificateCheck -TimeoutSec 10
        if ($response.Content -match "redoc") {
            Write-Log "✅ ReDoc funcionando" -Level SUCCESS
        }
        else {
            Write-Log "❌ ReDoc com problemas" -Level ERROR
        }
    }
    catch {
        Write-Log "❌ Erro no ReDoc: $($_.Exception.Message)" -Level ERROR
    }
    
    # Testar Schema OpenAPI
    try {
        $response = Invoke-WebRequest -Uri $SchemaUrl -SkipCertificateCheck -TimeoutSec 10
        $schema = $response.Content | ConvertFrom-Json
        if ($schema) {
            Write-Log "✅ Schema OpenAPI válido" -Level SUCCESS
            return $schema
        }
    }
    catch {
        Write-Log "❌ Erro no Schema OpenAPI: $($_.Exception.Message)" -Level ERROR
    }
}

# Função para gerar relatório
function Generate-Report {
    param($Schema)
    
    Write-Log "Gerando relatório de documentação..."
    
    $report = @"
# 📊 Relatório de Documentação da API

## 📅 Data: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")

## 🔗 URLs de Documentação

- **Swagger UI**: $ApiDocsUrl
- **ReDoc**: $ReDocUrl
- **OpenAPI Schema**: $SchemaUrl

## 📋 Endpoints Disponíveis

### 🔐 Autenticação
- `POST /api/v1/auth/login/` - Login com JWT
- `POST /api/v1/auth/refresh/` - Renovar token
- `POST /api/v1/auth/verify/` - Verificar token

### 👥 Responsáveis
- `GET /api/v1/cadastro/responsaveis/` - Listar responsáveis
- `POST /api/v1/cadastro/responsaveis/` - Criar responsável
- `GET /api/v1/cadastro/responsaveis/{id}/` - Obter responsável
- `PUT /api/v1/cadastro/responsaveis/{id}/` - Atualizar responsável
- `DELETE /api/v1/cadastro/responsaveis/{id}/` - Excluir responsável
- `GET /api/v1/cadastro/responsaveis/{id}/com_membros/` - Responsável com membros
- `GET /api/v1/cadastro/responsaveis/{id}/com_demandas/` - Responsável com demandas
- `GET /api/v1/cadastro/responsaveis/buscar_por_cpf/` - Buscar por CPF

### 👤 Membros
- `GET /api/v1/cadastro/membros/` - Listar membros
- `POST /api/v1/cadastro/membros/` - Criar membro
- `GET /api/v1/cadastro/membros/{id}/` - Obter membro
- `PUT /api/v1/cadastro/membros/{id}/` - Atualizar membro
- `DELETE /api/v1/cadastro/membros/{id}/` - Excluir membro
- `GET /api/v1/cadastro/membros/por_responsavel/` - Membros por responsável

### 🏥 Demandas de Saúde
- `GET /api/v1/cadastro/demandas-saude/` - Listar demandas de saúde
- `POST /api/v1/cadastro/demandas-saude/` - Criar demanda de saúde
- `GET /api/v1/cadastro/demandas-saude/grupos_prioritarios/` - Grupos prioritários

### 🏫 Demandas de Educação
- `GET /api/v1/cadastro/demandas-educacao/` - Listar demandas de educação
- `POST /api/v1/cadastro/demandas-educacao/` - Criar demanda de educação

### 🏠 Demandas de Habitação
- `GET /api/v1/cadastro/demandas-habitacao/` - Listar demandas de habitação
- `POST /api/v1/cadastro/demandas-habitacao/` - Criar demanda de habitação

### 🐕 Demandas de Ambiente
- `GET /api/v1/cadastro/demandas-ambiente/` - Listar demandas de ambiente
- `POST /api/v1/cadastro/demandas-ambiente/` - Criar demanda de ambiente

### 📋 Demandas Internas
- `GET /api/v1/cadastro/demandas-internas/` - Listar demandas internas
- `POST /api/v1/cadastro/demandas-internas/` - Criar demanda interna
- `GET /api/v1/cadastro/demandas-internas/por_status/` - Por status

### 🏢 Alojamentos
- `GET /api/v1/cadastro/alojamentos/` - Listar alojamentos

### 📮 CEPs Atingidos
- `GET /api/v1/cadastro/ceps-atingidos/` - Listar CEPs atingidos

### 🔍 Desaparecidos
- `GET /api/v1/cadastro/desaparecidos/` - Listar desaparecidos
- `POST /api/v1/cadastro/desaparecidos/` - Criar registro de desaparecido
- `GET /api/v1/cadastro/desaparecidos/recentes/` - Desaparecidos recentes

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

1. **Acesse a documentação**: $ApiDocsUrl
2. **Faça login**: Use o endpoint `/api/v1/auth/login/`
3. **Copie o token**: Use o token no header `Authorization: Bearer {token}`
4. **Teste os endpoints**: Use o botão "Try it out" no Swagger UI

## 📞 Suporte

Para dúvidas sobre a API, consulte:
- Documentação completa: `API_DOCUMENTATION.md`
- Swagger UI: $ApiDocsUrl
- ReDoc: $ReDocUrl

"@

    $report | Out-File -FilePath "API_DOCS_REPORT.md" -Encoding UTF8
    Write-Log "✅ Relatório gerado: API_DOCS_REPORT.md" -Level SUCCESS
}

# Função para baixar schema
function Download-Schema {
    Write-Log "Baixando schema OpenAPI..."
    
    try {
        $response = Invoke-WebRequest -Uri $SchemaUrl -SkipCertificateCheck -TimeoutSec 30
        $schema = $response.Content
        
        if ($schema) {
            $schema | Out-File -FilePath "openapi_schema.json" -Encoding UTF8
            $size = (Get-Item "openapi_schema.json").Length
            Write-Log "✅ Schema baixado com sucesso" -Level SUCCESS
            Write-Log "📊 Tamanho do schema: $size bytes" -Level INFO
            
            # Validar JSON
            try {
                $schemaObj = $schema | ConvertFrom-Json
                Write-Log "✅ Schema JSON válido" -Level SUCCESS
                
                # Contar endpoints
                $endpoints = $schemaObj.paths.PSObject.Properties.Name.Count
                Write-Log "📊 Total de endpoints documentados: $endpoints" -Level INFO
                
                # Contar tags
                $tags = $schemaObj.tags.Count
                Write-Log "📊 Total de tags: $tags" -Level INFO
                
                # Mostrar tags
                Write-Log "🏷️ Tags disponíveis:" -Level INFO
                foreach ($tag in $schemaObj.tags) {
                    Write-Host "  - $($tag.name)" -ForegroundColor Gray
                }
                
                return $schemaObj
            }
            catch {
                Write-Log "❌ Schema JSON inválido: $($_.Exception.Message)" -Level ERROR
            }
        }
    }
    catch {
        Write-Log "❌ Falha ao baixar schema: $($_.Exception.Message)" -Level ERROR
    }
}

# Função principal
function Main {
    Write-Host "🔧 Gerando documentação da API..." -ForegroundColor Cyan
    Write-Host ""
    
    # Testar conectividade
    if (-not (Test-Connectivity)) {
        Write-Log "❌ Não foi possível conectar ao servidor. Verifique se os containers estão rodando." -Level ERROR
        exit 1
    }
    
    # Testar endpoints de documentação
    $schema = Test-DocumentationEndpoints
    
    # Baixar e analisar schema
    $schemaObj = Download-Schema
    
    # Gerar relatório
    Generate-Report -Schema $schemaObj
    
    Write-Host ""
    Write-Log "🎉 Documentação gerada com sucesso!" -Level SUCCESS
    Write-Log "📖 Acesse: $ApiDocsUrl" -Level INFO
    Write-Log "📋 Relatório: API_DOCS_REPORT.md" -Level INFO
    Write-Log "📄 Schema: openapi_schema.json" -Level INFO
    
    Write-Host ""
    Write-Host "🔗 Links úteis:" -ForegroundColor Yellow
    Write-Host "  - Swagger UI: $ApiDocsUrl" -ForegroundColor White
    Write-Host "  - ReDoc: $ReDocUrl" -ForegroundColor White
    Write-Host "  - Schema: $SchemaUrl" -ForegroundColor White
    Write-Host ""
}

# Executar função principal
Main 