# 🚀 Setup Completo - Cadastro Unificado (10.13.65.37)

## 📋 Configuração para Desenvolvedor Senior Django + Flutter

### 🎯 Objetivo
Configurar ambiente completo com:
- **Backend**: Django + PostgreSQL + Redis + Nginx (Linux)
- **Frontend**: Flutter (Windows PowerShell)
- **TLS**: Certificados próprios (não auto-assinados)
- **IP**: 10.13.65.37 (configurado no `server_name` do Nginx)

---

## 🔧 1. Configuração do Backend (Linux)

### 1.1. Configuração do Nginx para 10.13.65.37

O arquivo `nginx.conf` está configurado especificamente para o IP **10.13.65.37**:

```nginx
# Servidor HTTPS principal
server {
    listen 443 ssl http2;
    server_name 10.13.65.37;  # 👈 Configuração específica para seu IP
    
    ssl_certificate /etc/nginx/ssl/server.crt;
    ssl_certificate_key /etc/nginx/ssl/server.key;
    
    # ... resto da configuração
}

# Redirecionamento HTTP -> HTTPS
server {
    listen 80;
    server_name 10.13.65.37;  # 👈 Mesmo IP aqui
    return 301 https://$server_name$request_uri;
}
```

### 1.2. Executar Setup Backend

```bash
# Dar permissão de execução
chmod +x setup-backend.sh

# Executar setup completo
./setup-backend.sh
```

**O script irá:**
- ✅ Verificar Docker e Docker Compose
- 🔐 Gerar certificados SSL próprios para 10.13.65.37
- 🏗️ Fazer build das imagens Docker
- 🚀 Iniciar containers (backend, redis, nginx)
- 🔄 Executar migrations Django
- 📦 Coletar arquivos estáticos
- 🌐 Testar conectividade
- 👤 Criar superusuário (opcional)

### 1.3. URLs do Backend Disponíveis

| Serviço | HTTP | HTTPS |
|---------|------|-------|
| **API Django** | http://10.13.65.37:8001/api/v1/ | https://10.13.65.37:8443/api/v1/ |
| **Documentação** | http://10.13.65.37:8001/api/docs/ | https://10.13.65.37:8443/api/docs/ |
| **Admin Django** | http://10.13.65.37:8001/admin/ | https://10.13.65.37:8443/admin/ |
| **Nginx** | http://10.13.65.37:8081/ | https://10.13.65.37:8443/ |

---

## 🔧 2. Configuração do Frontend (Windows PowerShell)

### 2.1. Executar Setup Frontend

```powershell
# Executar setup completo
.\setup-frontend.ps1

# Executar com build para web
.\setup-frontend.ps1 -Build -Device web

# Executar e rodar no Chrome
.\setup-frontend.ps1 -Run -Device chrome

# Limpeza completa
.\setup-frontend.ps1 -Clean
```

**O script irá:**
- ✅ Verificar instalação do Flutter
- 📝 Criar arquivo `.env` com configurações para 10.13.65.37
- 📦 Instalar dependências (`flutter pub get`)
- 🔄 Gerar código (build_runner)
- 🌐 Testar conectividade com backend
- 🔍 Executar análise de código
- 🚀 Executar app (se `-Run` especificado)

### 2.2. Configuração Automática do .env

O script cria automaticamente:

```env
# API Configuration
API_BASE_URL=https://10.13.65.37:8443/api/v1
API_BASE_URL_DEV=http://10.13.65.37:8081/api/v1
API_TIMEOUT=30000

# Environment
ENVIRONMENT=development
DEBUG_MODE=true

# Security
ENABLE_SSL_PINNING=false
TRUST_SELF_SIGNED_CERTS=true
```

---

## 🔐 3. Certificados TLS Próprios

### 3.1. Geração Automática

Os certificados são gerados automaticamente pelo script backend:

```bash
# Geração manual se necessário
openssl genpkey -algorithm RSA -out nginx/ssl/server.key -pkcs8
openssl req -new -x509 -key nginx/ssl/server.key -out nginx/ssl/server.crt \
    -days 365 -subj "/C=BR/ST=RS/L=NovoHamburgo/O=Development/CN=10.13.65.37" \
    -addext "subjectAltName=IP:10.13.65.37,DNS:localhost"
```

### 3.2. Localização dos Certificados

```
nginx/
└── ssl/
    ├── server.key     # Chave privada
    ├── server.crt     # Certificado público
    └── openssl.conf   # Configuração OpenSSL
```

---

## 🐳 4. Docker Compose

### 4.1. Comandos Úteis

```bash
# Iniciar todos os serviços
docker compose up -d

# Ver logs em tempo real
docker compose logs -f backend
docker compose logs -f nginx

# Parar todos os serviços
docker compose down

# Rebuild completo
docker compose down && docker compose build --no-cache && docker compose up -d

# Shell no container backend
docker compose exec backend bash

# Executar comando Django
docker compose exec backend python manage.py migrate
```

### 4.2. Estrutura dos Containers

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   nginx:alpine  │    │   python:3.11   │    │  redis:7-alpine │
│   (Proxy/TLS)   │◄───┤   (Django API)  │◄───┤     (Cache)     │
│   Port: 8081    │    │   Port: 8001    │    │   Port: 6379    │
│   Port: 8443    │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

---

## 🛠️ 5. Troubleshooting

### 5.1. Problemas Comuns

#### ❌ "server_name não funciona"
```bash
# Verificar se o IP está correto no nginx.conf
grep -n "server_name" nginx/nginx.conf

# Reiniciar nginx
docker compose restart nginx
```

#### ❌ "Certificado SSL inválido"
```bash
# Verificar certificado
openssl x509 -in nginx/ssl/server.crt -noout -subject -dates -ext subjectAltName

# Regenerar se necessário
rm nginx/ssl/server.*
./setup-backend.sh
```

#### ❌ "CORS errors no Flutter"
```bash
# Verificar configurações CORS no Django
docker compose exec backend python manage.py shell
>>> from django.conf import settings
>>> print(settings.CORS_ALLOWED_ORIGINS)
```

#### ❌ "Backend não acessível"
```bash
# Verificar containers
docker compose ps

# Verificar logs
docker compose logs backend --tail=50

# Testar conectividade
curl -I http://10.13.65.37:8081/nginx-health
curl -I -k https://10.13.65.37:8443/nginx-health
```

### 5.2. Comandos de Diagnóstico

```bash
# Verificar portas em uso
sudo netstat -tulpn | grep -E ':(8001|8081|8443)'

# Verificar containers
docker compose ps
docker stats

# Verificar certificados
openssl s_client -connect 10.13.65.37:8443 -servername 10.13.65.37

# Testar DNS/conectividade
ping 10.13.65.37
telnet 10.13.65.37 8081
```

---

## 📚 6. Comandos de Desenvolvimento

### 6.1. Backend (Django)

```bash
# Migrations
docker compose exec backend python manage.py makemigrations
docker compose exec backend python manage.py migrate

# Shell Django
docker compose exec backend python manage.py shell

# Testes
docker compose exec backend python manage.py test

# Criar app
docker compose exec backend python manage.py startapp nova_app
```

### 6.2. Frontend (Flutter)

```powershell
# Hot reload (durante desenvolvimento)
flutter run -d chrome --dart-define-from-file=.env

# Build para produção
flutter build web --release

# Testes
flutter test

# Análise de código
flutter analyze
```

---

## 🎯 7. Configurações Específicas para 10.13.65.37

### 7.1. Django Settings

```python
# Hosts permitidos
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '10.13.65.37']

# CORS Origins
CORS_ALLOWED_ORIGINS = [
    'https://10.13.65.37:3000',
    'https://10.13.65.37',
    'http://10.13.65.37:8001',
    'http://10.13.65.37:8081'
]

# CSRF Trusted Origins (apenas para produção)
CSRF_TRUSTED_ORIGINS = [
    'https://10.13.65.37',
    'https://10.13.65.37:8443'
]
```

### 7.2. Flutter Configuration

```dart
// lib/core/config/api_config.dart
class ApiConfig {
  static const String baseUrl = String.fromEnvironment(
    'API_BASE_URL',
    defaultValue: 'https://10.13.65.37:8443/api/v1',
  );
  
  static const String baseUrlDev = String.fromEnvironment(
    'API_BASE_URL_DEV', 
    defaultValue: 'http://10.13.65.37:8081/api/v1',
  );
}
```

---

## ✅ 8. Checklist Final

### Backend
- [ ] Docker Compose instalado (v2 preferível)
- [ ] Certificados SSL gerados
- [ ] Containers rodando (backend, redis, nginx)
- [ ] Migrations executadas
- [ ] API respondendo em 10.13.65.37:8001 e 10.13.65.37:8081
- [ ] HTTPS funcionando em 10.13.65.37:8443

### Frontend
- [ ] Flutter SDK instalado (3.16+)
- [ ] Dependências instaladas (`flutter pub get`)
- [ ] Arquivo `.env` configurado
- [ ] Build runner executado
- [ ] App conectando com backend via HTTPS
- [ ] CORS configurado corretamente

### Testes
- [ ] `curl http://10.13.65.37:8081/nginx-health` → 200 OK
- [ ] `curl -k https://10.13.65.37:8443/nginx-health` → 200 OK
- [ ] Flutter app fazendo requisições com sucesso
- [ ] Admin Django acessível
- [ ] Documentação API acessível

---

## 🎉 Setup Concluído!

Após seguir este guia, você terá:
- ✅ Backend Django rodando com TLS em **10.13.65.37**
- ✅ Nginx configurado como proxy reverso com `server_name 10.13.65.37`
- ✅ Certificados próprios (não auto-assinados) funcionando
- ✅ Flutter conectando via HTTPS
- ✅ Scripts automatizados para desenvolvimento

**URLs principais:**
- 🌐 **API**: https://10.13.65.37:8443/api/v1/
- 📖 **Docs**: https://10.13.65.37:8443/api/docs/
- ⚙️ **Admin**: https://10.13.65.37:8443/admin/