# 📚 API Documentation - Cadastro Unificado

## 🌐 Base URL

```
https://10.13.65.37:8443
```

## 📖 Documentation Endpoints

- **Swagger UI**: `https://10.13.65.37:8443/api/docs/`
- **ReDoc**: `https://10.13.65.37:8443/api/redoc/`
- **OpenAPI Schema**: `https://10.13.65.37:8443/api/schema/`

---

## 🔐 Authentication

### JWT Token Authentication

This API uses JWT (JSON Web Token) for authentication.

#### 1. Login

```http
POST /api/v1/auth/login/
Content-Type: application/json

{
    "username": "your_username",
    "password": "your_password"
}
```

**Response:**

```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

#### 2. Using the Token

Include the token in the Authorization header:

```http
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

#### 3. Refresh Token

```http
POST /api/v1/auth/refresh/
Content-Type: application/json

{
    "refresh": "your_refresh_token"
}
```

#### 4. Verify Token

```http
POST /api/v1/auth/verify/
Content-Type: application/json

{
    "token": "your_access_token"
}
```

---

## 📋 API Endpoints

### 🔍 Health Check

```http
GET /api/v1/health/
```

### 👥 Responsáveis (Family Representatives)

#### List Responsáveis

```http
GET /api/v1/cadastro/responsaveis/
Authorization: Bearer {token}
```

**Query Parameters:**

- `search`: Search by CPF, name, or mother's name
- `status`: Filter by status
- `bairro`: Filter by neighborhood
- `cep`: Filter by ZIP code
- `ordering`: Sort by field (e.g., `-timestamp`, `nome`)

#### Get Responsável by ID

```http
GET /api/v1/cadastro/responsaveis/{id}/
Authorization: Bearer {token}
```

#### Get Responsável with Members

```http
GET /api/v1/cadastro/responsaveis/{id}/com_membros/
Authorization: Bearer {token}
```

#### Get Responsável with Demands

```http
GET /api/v1/cadastro/responsaveis/{id}/com_demandas/
Authorization: Bearer {token}
```

#### Search Responsável by CPF

```http
GET /api/v1/cadastro/responsaveis/buscar_por_cpf/?cpf=12345678901
Authorization: Bearer {token}
```

#### Create Responsável

```http
POST /api/v1/cadastro/responsaveis/
Authorization: Bearer {token}
Content-Type: application/json

{
    "cpf": "12345678901",
    "nome": "João Silva",
    "nome_mae": "Maria Silva",
    "cep": "93000000",
    "bairro": "Centro",
    "status": "ativo"
}
```

#### Update Responsável

```http
PUT /api/v1/cadastro/responsaveis/{id}/
Authorization: Bearer {token}
Content-Type: application/json

{
    "cpf": "12345678901",
    "nome": "João Silva Updated",
    "nome_mae": "Maria Silva",
    "cep": "93000000",
    "bairro": "Centro",
    "status": "ativo"
}
```

#### Delete Responsável

```http
DELETE /api/v1/cadastro/responsaveis/{id}/
Authorization: Bearer {token}
```

### 👤 Membros (Family Members)

#### List Membros

```http
GET /api/v1/cadastro/membros/
Authorization: Bearer {token}
```

**Query Parameters:**

- `search`: Search by CPF, name, or responsible's name
- `status`: Filter by status
- `cpf_responsavel`: Filter by responsible's CPF
- `ordering`: Sort by field

#### Get Membro by ID

```http
GET /api/v1/cadastro/membros/{id}/
Authorization: Bearer {token}
```

#### Get Membros by Responsável

```http
GET /api/v1/cadastro/membros/por_responsavel/?cpf_responsavel=12345678901
Authorization: Bearer {token}
```

#### Create Membro

```http
POST /api/v1/cadastro/membros/
Authorization: Bearer {token}
Content-Type: application/json

{
    "cpf": "98765432100",
    "nome": "Ana Silva",
    "cpf_responsavel": "12345678901",
    "data_nascimento": "2010-05-15",
    "genero": "F",
    "status": "ativo"
}
```

### 🏥 Demandas de Saúde (Health Demands)

#### List Health Demands

```http
GET /api/v1/cadastro/demandas-saude/
Authorization: Bearer {token}
```

**Query Parameters:**

- `search`: Search by CPF or health CID
- `genero`: Filter by gender
- `gest_puer_nutriz`: Filter by pregnancy/nursing status
- `mob_reduzida`: Filter by reduced mobility

#### Get Priority Groups

```http
GET /api/v1/cadastro/demandas-saude/grupos_prioritarios/
Authorization: Bearer {token}
```

#### Create Health Demand

```http
POST /api/v1/cadastro/demandas-saude/
Authorization: Bearer {token}
Content-Type: application/json

{
    "cpf": "12345678901",
    "saude_cid": "F41.1",
    "genero": "M",
    "gest_puer_nutriz": false,
    "mob_reduzida": false,
    "descricao": "Consulta médica"
}
```

### 🏫 Demandas de Educação (Education Demands)

#### List Education Demands

```http
GET /api/v1/cadastro/demandas-educacao/
Authorization: Bearer {token}
```

**Query Parameters:**

- `search`: Search by CPF, name, or responsible's CPF
- `genero`: Filter by gender
- `turno`: Filter by shift
- `alojamento`: Filter by shelter
- `unidade_ensino`: Filter by school unit

#### Create Education Demand

```http
POST /api/v1/cadastro/demandas-educacao/
Authorization: Bearer {token}
Content-Type: application/json

{
    "cpf": "12345678901",
    "nome": "João Silva",
    "cpf_responsavel": "12345678901",
    "genero": "M",
    "turno": "manha",
    "alojamento": "Centro",
    "unidade_ensino": "Escola Municipal"
}
```

### 🏠 Demandas de Habitação (Housing Demands)

#### List Housing Demands

```http
GET /api/v1/cadastro/demandas-habitacao/
Authorization: Bearer {token}
```

**Query Parameters:**

- `search`: Search by CPF
- `material`: Filter by construction material
- `relacao_imovel`: Filter by property relationship
- `uso_imovel`: Filter by property use
- `area_verde`: Filter by green area
- `ocupacao`: Filter by occupation

#### Create Housing Demand

```http
POST /api/v1/cadastro/demandas-habitacao/
Authorization: Bearer {token}
Content-Type: application/json

{
    "cpf": "12345678901",
    "material": "alvenaria",
    "relacao_imovel": "proprietario",
    "uso_imovel": "residencial",
    "area_verde": true,
    "ocupacao": "propria"
}
```

### 🐕 Demandas de Ambiente (Environment Demands)

#### List Environment Demands

```http
GET /api/v1/cadastro/demandas-ambiente/
Authorization: Bearer {token}
```

**Query Parameters:**

- `search`: Search by CPF or responsible's name
- `especie`: Filter by species
- `vacinado`: Filter by vaccination status
- `castrado`: Filter by neutering status
- `porte`: Filter by size

#### Create Environment Demand

```http
POST /api/v1/cadastro/demandas-ambiente/
Authorization: Bearer {token}
Content-Type: application/json

{
    "cpf": "12345678901",
    "especie": "canino",
    "vacinado": true,
    "castrado": false,
    "porte": "medio",
    "descricao": "Cão para adoção"
}
```

### 📋 Demandas Internas (Internal Demands)

#### List Internal Demands

```http
GET /api/v1/cadastro/demandas-internas/
Authorization: Bearer {token}
```

**Query Parameters:**

- `search`: Search by CPF or demand description
- `status`: Filter by status
- `ordering`: Sort by date

#### Get by Status

```http
GET /api/v1/cadastro/demandas-internas/por_status/?status=pendente
Authorization: Bearer {token}
```

#### Create Internal Demand

```http
POST /api/v1/cadastro/demandas-internas/
Authorization: Bearer {token}
Content-Type: application/json

{
    "cpf": "12345678901",
    "demanda": "Documentação",
    "status": "pendente",
    "data": "2024-01-15",
    "observacoes": "Precisa de RG"
}
```

### 🏢 Alojamentos (Shelters)

#### List Shelters

```http
GET /api/v1/cadastro/alojamentos/
Authorization: Bearer {token}
```

**Query Parameters:**

- `search`: Search by name
- `nome`: Filter by name

### 📮 CEPs Atingidos (Affected ZIP Codes)

#### List Affected ZIP Codes

```http
GET /api/v1/cadastro/ceps-atingidos/
Authorization: Bearer {token}
```

**Query Parameters:**

- `search`: Search by CEP, street, city, or neighborhood
- `uf`: Filter by state
- `municipio`: Filter by city

### 🔍 Desaparecidos (Missing Persons)

#### List Missing Persons

```http
GET /api/v1/cadastro/desaparecidos/
Authorization: Bearer {token}
```

**Query Parameters:**

- `search`: Search by missing person's name, CPF, or contact phone
- `vinculo`: Filter by relationship
- `ordering`: Sort by disappearance date

#### Get Recent Missing Persons

```http
GET /api/v1/cadastro/desaparecidos/recentes/
Authorization: Bearer {token}
```

#### Create Missing Person Record

```http
POST /api/v1/cadastro/desaparecidos/
Authorization: Bearer {token}
Content-Type: application/json

{
    "nome_desaparecido": "Maria Silva",
    "cpf": "12345678901",
    "tel_contato": "51999999999",
    "vinculo": "filho",
    "data_desaparecimento": "2024-01-15",
    "descricao": "Vestia calça jeans e camiseta branca"
}
```

---

## 📊 Response Formats

### Success Response

```json
{
  "id": 1,
  "cpf": "12345678901",
  "nome": "João Silva",
  "nome_mae": "Maria Silva",
  "cep": "93000000",
  "bairro": "Centro",
  "status": "ativo",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### Error Response

```json
{
  "detail": "Authentication credentials were not provided."
}
```

### Pagination Response

```json
{
  "count": 100,
  "next": "https://10.13.65.37:8443/api/v1/cadastro/responsaveis/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "cpf": "12345678901",
      "nome": "João Silva"
      // ... other fields
    }
  ]
}
```

---

## 🔧 Query Parameters

### Common Parameters

- `page`: Page number for pagination
- `page_size`: Number of items per page (max 100)
- `search`: Search across multiple fields
- `ordering`: Sort by field (prefix with `-` for descending)

### Filtering

- Use `?field=value` for exact matches
- Use `?field__contains=value` for partial matches
- Use `?field__in=value1,value2` for multiple values

### Examples

```http
# Search responsáveis by name containing "João"
GET /api/v1/cadastro/responsaveis/?search=João

# Filter by status and order by timestamp
GET /api/v1/cadastro/responsaveis/?status=ativo&ordering=-timestamp

# Get page 2 with 10 items per page
GET /api/v1/cadastro/responsaveis/?page=2&page_size=10
```

---

## 🚀 Quick Start Examples

### 1. Get Access Token

```bash
curl -X POST https://10.13.65.37:8443/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "your_username", "password": "your_password"}' \
  -k
```

### 2. List Responsáveis

```bash
curl -X GET https://10.13.65.37:8443/api/v1/cadastro/responsaveis/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -k
```

### 3. Search by CPF

```bash
curl -X GET "https://10.13.65.37:8443/api/v1/cadastro/responsaveis/buscar_por_cpf/?cpf=12345678901" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -k
```

### 4. Create New Responsável

```bash
curl -X POST https://10.13.65.37:8443/api/v1/cadastro/responsaveis/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "cpf": "12345678901",
    "nome": "João Silva",
    "nome_mae": "Maria Silva",
    "cep": "93000000",
    "bairro": "Centro",
    "status": "ativo"
  }' \
  -k
```

---

## 📝 Notes

- All endpoints require authentication except `/api/v1/health/`
- Use `-k` flag with curl to ignore SSL certificate verification
- The API uses pagination with 20 items per page by default
- All timestamps are in ISO 8601 format (UTC)
- CPF fields should be numeric only (no dots or dashes)
- Status fields typically accept: `ativo`, `inativo`, `pendente`

---

## 🔗 Related Links

- [Swagger UI Documentation](https://10.13.65.37:8443/api/docs/)
- [ReDoc Documentation](https://10.13.65.37:8443/api/redoc/)
- [OpenAPI Schema](https://10.13.65.37:8443/api/schema/)
