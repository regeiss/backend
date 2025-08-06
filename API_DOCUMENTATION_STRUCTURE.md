# API Documentation - Cadastro Unificado System

**Version:** 1.0.0  
**Date:** January 2024  
**Author:** Sistema de Cadastro Unificado  
**Contact:** Technical Support Team

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [System Overview](#system-overview)
3. [Technical Architecture](#technical-architecture)
4. [API Authentication](#api-authentication)
5. [API Endpoints](#api-endpoints)
6. [Data Models](#data-models)
7. [Error Handling](#error-handling)
8. [Usage Examples](#usage-examples)
9. [Integration Guide](#integration-guide)
10. [Troubleshooting](#troubleshooting)
11. [Appendices](#appendices)

---

## 1. Executive Summary

### 1.1 Purpose

This document provides comprehensive documentation for the Cadastro Unificado API, a RESTful web service designed to manage unified registration data for family representatives, members, and various types of demands (health, education, housing, environment, and internal demands).

### 1.2 Key Features

- **JWT Authentication**: Secure token-based authentication system
- **CRUD Operations**: Complete Create, Read, Update, Delete functionality
- **Advanced Filtering**: Search and filter capabilities across all entities
- **Pagination**: Efficient data retrieval with pagination support
- **Comprehensive Documentation**: Swagger UI and ReDoc interfaces
- **HTTPS Security**: Encrypted communication with SSL/TLS

### 1.3 Target Audience

- **Developers**: Frontend and mobile application developers
- **System Administrators**: IT personnel managing the system
- **Business Analysts**: Users requiring API understanding for integration
- **Quality Assurance**: Testing teams validating API functionality

---

## 2. System Overview

### 2.1 System Purpose

The Cadastro Unificado system serves as a centralized platform for managing family registration data, including:

- Family representatives (Responsáveis)
- Family members (Membros)
- Health demands (Demandas de Saúde)
- Education demands (Demandas de Educação)
- Housing demands (Demandas de Habitação)
- Environment demands (Demandas de Ambiente)
- Internal demands (Demandas Internas)
- Missing persons (Desaparecidos)
- Shelters (Alojamentos)
- Affected ZIP codes (CEPs Atingidos)

### 2.2 System Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Client Apps   │    │   Nginx Proxy   │    │  Django API     │
│   (Flutter,     │◄──►│   (SSL/TLS,     │◄──►│  (REST API,     │
│   Web, etc.)    │    │   CORS, Auth)   │    │   JWT Auth)     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │   PostgreSQL    │
                       │   Database      │
                       └─────────────────┘
```

### 2.3 Technology Stack

- **Backend Framework**: Django 5.0.1 with Django REST Framework
- **Authentication**: JWT (JSON Web Tokens)
- **Database**: PostgreSQL
- **Web Server**: Nginx with SSL/TLS
- **Documentation**: drf-spectacular (Swagger/OpenAPI)
- **Containerization**: Docker with Docker Compose

---

## 3. Technical Architecture

### 3.1 Base URL

```
Production: https://10.13.65.37:8443
Development: https://localhost:8443
```

### 3.2 API Versioning

- **Current Version**: v1
- **URL Pattern**: `/api/v1/`
- **Version Strategy**: URL-based versioning

### 3.3 Security Features

- **HTTPS**: All communications encrypted with SSL/TLS
- **JWT Authentication**: Stateless token-based authentication
- **CORS Support**: Cross-origin resource sharing enabled
- **Rate Limiting**: API protection against abuse
- **Input Validation**: Comprehensive data validation
- **SQL Injection Protection**: Django ORM security

### 3.4 Response Formats

- **Primary Format**: JSON
- **Character Encoding**: UTF-8
- **Date Format**: ISO 8601 (UTC)
- **Pagination**: Page-based with configurable page size

---

## 4. API Authentication

### 4.1 Authentication Method

The API uses JWT (JSON Web Token) authentication for secure access control.

### 4.2 Authentication Flow

#### Step 1: Login

**Endpoint:** `POST /api/v1/auth/login/`

**Request:**

```json
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

#### Step 2: Using Access Token

Include the access token in the Authorization header:

```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

#### Step 3: Token Refresh

**Endpoint:** `POST /api/v1/auth/refresh/`

**Request:**

```json
{
  "refresh": "your_refresh_token"
}
```

#### Step 4: Token Verification

**Endpoint:** `POST /api/v1/auth/verify/`

**Request:**

```json
{
  "token": "your_access_token"
}
```

### 4.3 Token Lifecycle

- **Access Token Lifetime**: 1 hour
- **Refresh Token Lifetime**: 7 days
- **Token Rotation**: Enabled
- **Blacklist After Rotation**: Enabled

### 4.4 Security Headers

```
Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Referrer-Policy: strict-origin-when-cross-origin
```

---

## 5. API Endpoints

### 5.1 Health Check

#### GET /api/v1/health/

**Description:** System health check endpoint  
**Authentication:** Not required  
**Response:** System status information

### 5.2 Family Representatives (Responsáveis)

#### 5.2.1 List Representatives

**Endpoint:** `GET /api/v1/cadastro/responsaveis/`  
**Authentication:** Required  
**Description:** Retrieve paginated list of family representatives

**Query Parameters:**

- `search` (string): Search by CPF, name, or mother's name
- `status` (string): Filter by status (ativo, inativo, pendente)
- `bairro` (string): Filter by neighborhood
- `cep` (string): Filter by ZIP code
- `ordering` (string): Sort by field (- for descending)
- `page` (integer): Page number
- `page_size` (integer): Items per page (max 100)

**Example Request:**

```bash
curl -X GET "https://10.13.65.37:8443/api/v1/cadastro/responsaveis/?search=João&status=ativo&page=1" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -k
```

#### 5.2.2 Get Representative by ID

**Endpoint:** `GET /api/v1/cadastro/responsaveis/{id}/`  
**Authentication:** Required  
**Description:** Retrieve specific representative details

#### 5.2.3 Create Representative

**Endpoint:** `POST /api/v1/cadastro/responsaveis/`  
**Authentication:** Required  
**Description:** Create new family representative

**Request Body:**

```json
{
  "cpf": "12345678901",
  "nome": "João Silva",
  "nome_mae": "Maria Silva",
  "cep": "93000000",
  "bairro": "Centro",
  "status": "ativo"
}
```

#### 5.2.4 Update Representative

**Endpoint:** `PUT /api/v1/cadastro/responsaveis/{id}/`  
**Authentication:** Required  
**Description:** Update all fields of a representative

#### 5.2.5 Partial Update Representative

**Endpoint:** `PATCH /api/v1/cadastro/responsaveis/{id}/`  
**Authentication:** Required  
**Description:** Update specific fields of a representative

#### 5.2.6 Delete Representative

**Endpoint:** `DELETE /api/v1/cadastro/responsaveis/{id}/`  
**Authentication:** Required  
**Description:** Remove representative from system

#### 5.2.7 Get Representative with Members

**Endpoint:** `GET /api/v1/cadastro/responsaveis/{id}/com_membros/`  
**Authentication:** Required  
**Description:** Retrieve representative with complete family member list

#### 5.2.8 Get Representative with Demands

**Endpoint:** `GET /api/v1/cadastro/responsaveis/{id}/com_demandas/`  
**Authentication:** Required  
**Description:** Retrieve representative with all associated demands

#### 5.2.9 Search Representative by CPF

**Endpoint:** `GET /api/v1/cadastro/responsaveis/buscar_por_cpf/`  
**Authentication:** Required  
**Description:** Find representative by CPF number

**Query Parameters:**

- `cpf` (string, required): CPF number to search

### 5.3 Family Members (Membros)

#### 5.3.1 List Members

**Endpoint:** `GET /api/v1/cadastro/membros/`  
**Authentication:** Required  
**Description:** Retrieve paginated list of family members

**Query Parameters:**

- `search` (string): Search by CPF, name, or responsible's name
- `status` (string): Filter by status
- `cpf_responsavel` (string): Filter by responsible's CPF
- `ordering` (string): Sort by field
- `page` (integer): Page number
- `page_size` (integer): Items per page

#### 5.3.2 Get Member by ID

**Endpoint:** `GET /api/v1/cadastro/membros/{id}/`  
**Authentication:** Required  
**Description:** Retrieve specific member details

#### 5.3.3 Create Member

**Endpoint:** `POST /api/v1/cadastro/membros/`  
**Authentication:** Required  
**Description:** Create new family member

**Request Body:**

```json
{
  "cpf": "98765432100",
  "nome": "Ana Silva",
  "cpf_responsavel": "12345678901",
  "data_nascimento": "2010-05-15",
  "genero": "F",
  "status": "ativo"
}
```

#### 5.3.4 Get Members by Responsible

**Endpoint:** `GET /api/v1/cadastro/membros/por_responsavel/`  
**Authentication:** Required  
**Description:** Retrieve all members of a specific responsible

**Query Parameters:**

- `cpf_responsavel` (string, required): CPF of the responsible

### 5.4 Health Demands (Demandas de Saúde)

#### 5.4.1 List Health Demands

**Endpoint:** `GET /api/v1/cadastro/demandas-saude/`  
**Authentication:** Required  
**Description:** Retrieve paginated list of health demands

**Query Parameters:**

- `search` (string): Search by CPF or health CID
- `genero` (string): Filter by gender
- `gest_puer_nutriz` (boolean): Filter by pregnancy/nursing status
- `mob_reduzida` (boolean): Filter by reduced mobility

#### 5.4.2 Create Health Demand

**Endpoint:** `POST /api/v1/cadastro/demandas-saude/`  
**Authentication:** Required  
**Description:** Create new health demand

**Request Body:**

```json
{
  "cpf": "12345678901",
  "saude_cid": "F41.1",
  "genero": "M",
  "gest_puer_nutriz": false,
  "mob_reduzida": false,
  "descricao": "Consulta médica"
}
```

#### 5.4.3 Get Priority Groups

**Endpoint:** `GET /api/v1/cadastro/demandas-saude/grupos_prioritarios/`  
**Authentication:** Required  
**Description:** Retrieve priority groups for health demands

### 5.5 Education Demands (Demandas de Educação)

#### 5.5.1 List Education Demands

**Endpoint:** `GET /api/v1/cadastro/demandas-educacao/`  
**Authentication:** Required  
**Description:** Retrieve paginated list of education demands

**Query Parameters:**

- `search` (string): Search by CPF, name, or responsible's CPF
- `genero` (string): Filter by gender
- `turno` (string): Filter by shift
- `alojamento` (string): Filter by shelter
- `unidade_ensino` (string): Filter by school unit

#### 5.5.2 Create Education Demand

**Endpoint:** `POST /api/v1/cadastro/demandas-educacao/`  
**Authentication:** Required  
**Description:** Create new education demand

**Request Body:**

```json
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

### 5.6 Housing Demands (Demandas de Habitação)

#### 5.6.1 List Housing Demands

**Endpoint:** `GET /api/v1/cadastro/demandas-habitacao/`  
**Authentication:** Required  
**Description:** Retrieve paginated list of housing demands

**Query Parameters:**

- `search` (string): Search by CPF
- `material` (string): Filter by construction material
- `relacao_imovel` (string): Filter by property relationship
- `uso_imovel` (string): Filter by property use
- `area_verde` (boolean): Filter by green area
- `ocupacao` (string): Filter by occupation

#### 5.6.2 Create Housing Demand

**Endpoint:** `POST /api/v1/cadastro/demandas-habitacao/`  
**Authentication:** Required  
**Description:** Create new housing demand

**Request Body:**

```json
{
  "cpf": "12345678901",
  "material": "alvenaria",
  "relacao_imovel": "proprietario",
  "uso_imovel": "residencial",
  "area_verde": true,
  "ocupacao": "propria"
}
```

### 5.7 Environment Demands (Demandas de Ambiente)

#### 5.7.1 List Environment Demands

**Endpoint:** `GET /api/v1/cadastro/demandas-ambiente/`  
**Authentication:** Required  
**Description:** Retrieve paginated list of environment demands

**Query Parameters:**

- `search` (string): Search by CPF or responsible's name
- `especie` (string): Filter by species
- `vacinado` (boolean): Filter by vaccination status
- `castrado` (boolean): Filter by neutering status
- `porte` (string): Filter by size

#### 5.7.2 Create Environment Demand

**Endpoint:** `POST /api/v1/cadastro/demandas-ambiente/`  
**Authentication:** Required  
**Description:** Create new environment demand

**Request Body:**

```json
{
  "cpf": "12345678901",
  "especie": "canino",
  "vacinado": true,
  "castrado": false,
  "porte": "medio",
  "descricao": "Cão para adoção"
}
```

### 5.8 Internal Demands (Demandas Internas)

#### 5.8.1 List Internal Demands

**Endpoint:** `GET /api/v1/cadastro/demandas-internas/`  
**Authentication:** Required  
**Description:** Retrieve paginated list of internal demands

**Query Parameters:**

- `search` (string): Search by CPF or demand description
- `status` (string): Filter by status
- `ordering` (string): Sort by date

#### 5.8.2 Create Internal Demand

**Endpoint:** `POST /api/v1/cadastro/demandas-internas/`  
**Authentication:** Required  
**Description:** Create new internal demand

**Request Body:**

```json
{
  "cpf": "12345678901",
  "demanda": "Documentação",
  "status": "pendente",
  "data": "2024-01-15",
  "observacoes": "Precisa de RG"
}
```

#### 5.8.3 Get by Status

**Endpoint:** `GET /api/v1/cadastro/demandas-internas/por_status/`  
**Authentication:** Required  
**Description:** Retrieve internal demands by status

**Query Parameters:**

- `status` (string, required): Status to filter by

### 5.9 Shelters (Alojamentos)

#### 5.9.1 List Shelters

**Endpoint:** `GET /api/v1/cadastro/alojamentos/`  
**Authentication:** Required  
**Description:** Retrieve paginated list of shelters

**Query Parameters:**

- `search` (string): Search by name
- `nome` (string): Filter by name

### 5.10 Affected ZIP Codes (CEPs Atingidos)

#### 5.10.1 List Affected ZIP Codes

**Endpoint:** `GET /api/v1/cadastro/ceps-atingidos/`  
**Authentication:** Required  
**Description:** Retrieve paginated list of affected ZIP codes

**Query Parameters:**

- `search` (string): Search by CEP, street, city, or neighborhood
- `uf` (string): Filter by state
- `municipio` (string): Filter by city

### 5.11 Missing Persons (Desaparecidos)

#### 5.11.1 List Missing Persons

**Endpoint:** `GET /api/v1/cadastro/desaparecidos/`  
**Authentication:** Required  
**Description:** Retrieve paginated list of missing persons

**Query Parameters:**

- `search` (string): Search by missing person's name, CPF, or contact phone
- `vinculo` (string): Filter by relationship
- `ordering` (string): Sort by disappearance date

#### 5.11.2 Create Missing Person Record

**Endpoint:** `POST /api/v1/cadastro/desaparecidos/`  
**Authentication:** Required  
**Description:** Create new missing person record

**Request Body:**

```json
{
  "nome_desaparecido": "Maria Silva",
  "cpf": "12345678901",
  "tel_contato": "51999999999",
  "vinculo": "filho",
  "data_desaparecimento": "2024-01-15",
  "descricao": "Vestia calça jeans e camiseta branca"
}
```

#### 5.11.3 Get Recent Missing Persons

**Endpoint:** `GET /api/v1/cadastro/desaparecidos/recentes/`  
**Authentication:** Required  
**Description:** Retrieve recent missing persons records

---

## 6. Data Models

### 6.1 Family Representative (Responsável)

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

### 6.2 Family Member (Membro)

```json
{
  "id": 1,
  "cpf": "98765432100",
  "nome": "Ana Silva",
  "cpf_responsavel": "12345678901",
  "data_nascimento": "2010-05-15",
  "genero": "F",
  "status": "ativo",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### 6.3 Health Demand (Demanda de Saúde)

```json
{
  "id": 1,
  "cpf": "12345678901",
  "saude_cid": "F41.1",
  "genero": "M",
  "gest_puer_nutriz": false,
  "mob_reduzida": false,
  "cuida_outrem": false,
  "pcd_ou_mental": false,
  "descricao": "Consulta médica",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### 6.4 Education Demand (Demanda de Educação)

```json
{
  "id": 1,
  "cpf": "12345678901",
  "nome": "João Silva",
  "cpf_responsavel": "12345678901",
  "genero": "M",
  "turno": "manha",
  "alojamento": "Centro",
  "unidade_ensino": "Escola Municipal",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### 6.5 Housing Demand (Demanda de Habitação)

```json
{
  "id": 1,
  "cpf": "12345678901",
  "material": "alvenaria",
  "relacao_imovel": "proprietario",
  "uso_imovel": "residencial",
  "area_verde": true,
  "ocupacao": "propria",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### 6.6 Environment Demand (Demanda de Ambiente)

```json
{
  "id": 1,
  "cpf": "12345678901",
  "especie": "canino",
  "vacinado": true,
  "castrado": false,
  "porte": "medio",
  "descricao": "Cão para adoção",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### 6.7 Internal Demand (Demanda Interna)

```json
{
  "id": 1,
  "cpf": "12345678901",
  "demanda": "Documentação",
  "status": "pendente",
  "data": "2024-01-15",
  "observacoes": "Precisa de RG",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### 6.8 Missing Person (Desaparecido)

```json
{
  "id": 1,
  "nome_desaparecido": "Maria Silva",
  "cpf": "12345678901",
  "tel_contato": "51999999999",
  "vinculo": "filho",
  "data_desaparecimento": "2024-01-15",
  "descricao": "Vestia calça jeans e camiseta branca",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

---

## 7. Error Handling

### 7.1 HTTP Status Codes

#### 2xx Success

- **200 OK**: Request successful
- **201 Created**: Resource created successfully
- **204 No Content**: Request successful, no content to return

#### 4xx Client Errors

- **400 Bad Request**: Invalid request syntax or parameters
- **401 Unauthorized**: Authentication required or failed
- **403 Forbidden**: Access denied
- **404 Not Found**: Resource not found
- **405 Method Not Allowed**: HTTP method not supported
- **422 Unprocessable Entity**: Validation errors

#### 5xx Server Errors

- **500 Internal Server Error**: Server error
- **502 Bad Gateway**: Gateway error
- **503 Service Unavailable**: Service temporarily unavailable

### 7.2 Error Response Format

```json
{
  "detail": "Error message description",
  "code": "ERROR_CODE",
  "field_errors": {
    "field_name": ["Error description"]
  }
}
```

### 7.3 Common Error Scenarios

#### Authentication Errors

```json
{
  "detail": "Authentication credentials were not provided."
}
```

#### Validation Errors

```json
{
  "cpf": ["This field is required."],
  "nome": ["This field may not be blank."]
}
```

#### Not Found Errors

```json
{
  "detail": "Responsável não encontrado"
}
```

---

## 8. Usage Examples

### 8.1 Complete Authentication Flow

#### Step 1: Login

```bash
curl -X POST https://10.13.65.37:8443/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "your_password"
  }' \
  -k
```

#### Step 2: Store Token

```bash
# Store the access token
TOKEN="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
```

#### Step 3: Use Token

```bash
curl -X GET https://10.13.65.37:8443/api/v1/cadastro/responsaveis/ \
  -H "Authorization: Bearer $TOKEN" \
  -k
```

### 8.2 CRUD Operations Example

#### Create Representative

```bash
curl -X POST https://10.13.65.37:8443/api/v1/cadastro/responsaveis/ \
  -H "Authorization: Bearer $TOKEN" \
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

#### Read Representative

```bash
curl -X GET https://10.13.65.37:8443/api/v1/cadastro/responsaveis/1/ \
  -H "Authorization: Bearer $TOKEN" \
  -k
```

#### Update Representative

```bash
curl -X PUT https://10.13.65.37:8443/api/v1/cadastro/responsaveis/1/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "cpf": "12345678901",
    "nome": "João Silva Updated",
    "nome_mae": "Maria Silva",
    "cep": "93000000",
    "bairro": "Centro",
    "status": "ativo"
  }' \
  -k
```

#### Delete Representative

```bash
curl -X DELETE https://10.13.65.37:8443/api/v1/cadastro/responsaveis/1/ \
  -H "Authorization: Bearer $TOKEN" \
  -k
```

### 8.3 Search and Filter Examples

#### Search by Name

```bash
curl -X GET "https://10.13.65.37:8443/api/v1/cadastro/responsaveis/?search=João" \
  -H "Authorization: Bearer $TOKEN" \
  -k
```

#### Filter by Status

```bash
curl -X GET "https://10.13.65.37:8443/api/v1/cadastro/responsaveis/?status=ativo" \
  -H "Authorization: Bearer $TOKEN" \
  -k
```

#### Complex Search

```bash
curl -X GET "https://10.13.65.37:8443/api/v1/cadastro/responsaveis/?search=Silva&status=ativo&ordering=-timestamp&page=1&page_size=10" \
  -H "Authorization: Bearer $TOKEN" \
  -k
```

### 8.4 JavaScript/Node.js Examples

#### Authentication

```javascript
const axios = require("axios");

// Login
const loginResponse = await axios.post(
  "https://10.13.65.37:8443/api/v1/auth/login/",
  {
    username: "admin",
    password: "your_password",
  },
  {
    httpsAgent: new https.Agent({ rejectUnauthorized: false }),
  }
);

const token = loginResponse.data.access;

// Use token
const config = {
  headers: { Authorization: `Bearer ${token}` },
  httpsAgent: new https.Agent({ rejectUnauthorized: false }),
};

const responsaveis = await axios.get(
  "https://10.13.65.37:8443/api/v1/cadastro/responsaveis/",
  config
);
```

### 8.5 Python Examples

#### Authentication

```python
import requests
import urllib3

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Login
login_data = {
    'username': 'admin',
    'password': 'your_password'
}

response = requests.post(
    'https://10.13.65.37:8443/api/v1/auth/login/',
    json=login_data,
    verify=False
)

token = response.json()['access']

# Use token
headers = {'Authorization': f'Bearer {token}'}

responsaveis = requests.get(
    'https://10.13.65.37:8443/api/v1/cadastro/responsaveis/',
    headers=headers,
    verify=False
)
```

---

## 9. Integration Guide

### 9.1 Prerequisites

- **HTTPS Support**: Client must support HTTPS connections
- **JSON Handling**: Client must handle JSON request/response format
- **JWT Library**: Client should have JWT token handling capability
- **SSL Certificate**: Handle self-signed certificates in development

### 9.2 Integration Steps

#### Step 1: Environment Setup

1. Configure HTTPS client settings
2. Set up JWT token management
3. Configure error handling
4. Set up logging for debugging

#### Step 2: Authentication Implementation

1. Implement login endpoint call
2. Store and manage access tokens
3. Implement token refresh logic
4. Handle authentication errors

#### Step 3: API Integration

1. Implement CRUD operations
2. Add search and filter functionality
3. Implement pagination handling
4. Add error handling and retry logic

#### Step 4: Testing

1. Test authentication flow
2. Test all CRUD operations
3. Test search and filter functionality
4. Test error scenarios
5. Performance testing

### 9.3 Best Practices

#### Security

- Always use HTTPS in production
- Store tokens securely
- Implement token refresh before expiration
- Validate all input data
- Handle sensitive data appropriately

#### Performance

- Implement caching where appropriate
- Use pagination for large datasets
- Minimize API calls
- Handle timeouts gracefully

#### Error Handling

- Implement comprehensive error handling
- Log errors for debugging
- Provide user-friendly error messages
- Implement retry logic for transient failures

#### Monitoring

- Monitor API response times
- Track error rates
- Monitor token usage
- Set up alerts for critical failures

---

## 10. Troubleshooting

### 10.1 Common Issues

#### SSL Certificate Issues

**Problem:** SSL certificate verification fails
**Solution:** Use `-k` flag with curl or configure SSL settings

```bash
curl -k https://10.13.65.37:8443/api/v1/health/
```

#### Authentication Errors

**Problem:** 401 Unauthorized errors
**Solution:** Check token validity and refresh if needed

```bash
# Verify token
curl -X POST https://10.13.65.37:8443/api/v1/auth/verify/ \
  -H "Content-Type: application/json" \
  -d '{"token": "YOUR_TOKEN"}' \
  -k
```

#### Connection Timeout

**Problem:** Connection times out
**Solution:** Check network connectivity and firewall settings

```bash
# Test connectivity
ping 10.13.65.37
telnet 10.13.65.37 8443
```

#### Rate Limiting

**Problem:** 429 Too Many Requests
**Solution:** Implement rate limiting and retry logic

### 10.2 Debugging Tools

#### Health Check

```bash
curl -k https://10.13.65.37:8443/api/v1/health/
```

#### Schema Validation

```bash
curl -k https://10.13.65.37:8443/api/schema/ | jq .
```

#### Logs

```bash
# Check container logs
docker compose logs backend
docker compose logs nginx
```

### 10.3 Performance Optimization

#### Pagination

- Use appropriate page sizes
- Implement infinite scrolling
- Cache frequently accessed data

#### Caching

- Cache authentication tokens
- Cache frequently accessed data
- Implement client-side caching

#### Connection Pooling

- Reuse HTTP connections
- Implement connection pooling
- Use keep-alive connections

---

## 11. Appendices

### 11.1 API Documentation URLs

- **Swagger UI**: https://10.13.65.37:8443/api/docs/
- **ReDoc**: https://10.13.65.37:8443/api/redoc/
- **OpenAPI Schema**: https://10.13.65.37:8443/api/schema/

### 11.2 Status Codes Reference

| Code | Description           | Usage                      |
| ---- | --------------------- | -------------------------- |
| 200  | OK                    | Successful GET, PUT, PATCH |
| 201  | Created               | Successful POST            |
| 204  | No Content            | Successful DELETE          |
| 400  | Bad Request           | Invalid input              |
| 401  | Unauthorized          | Authentication required    |
| 403  | Forbidden             | Access denied              |
| 404  | Not Found             | Resource not found         |
| 405  | Method Not Allowed    | HTTP method not supported  |
| 422  | Unprocessable Entity  | Validation errors          |
| 429  | Too Many Requests     | Rate limit exceeded        |
| 500  | Internal Server Error | Server error               |

### 11.3 Field Validation Rules

#### CPF (Brazilian ID)

- **Format**: 11 digits, numeric only
- **Validation**: Must be valid CPF format
- **Example**: "12345678901"

#### CEP (ZIP Code)

- **Format**: 8 digits, numeric only
- **Example**: "93000000"

#### Date Fields

- **Format**: ISO 8601 (YYYY-MM-DD)
- **Example**: "2024-01-15"

#### Status Fields

- **Values**: "ativo", "inativo", "pendente"
- **Default**: "ativo"

### 11.4 Environment Variables

```bash
# Database
DATABASE_URL=postgresql://user:password@host:port/database

# Security
SECRET_KEY=your_secret_key
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,10.13.65.37

# SSL
SECURE_SSL_REDIRECT=True
SECURE_PROXY_SSL_HEADER=True

# CORS
CORS_ALLOW_ALL_ORIGINS=True
CORS_ALLOW_CREDENTIALS=True
```

### 11.5 Docker Commands

```bash
# Start services
docker compose up -d

# Stop services
docker compose down

# View logs
docker compose logs -f

# Restart services
docker compose restart

# Rebuild and start
docker compose up -d --build
```

### 11.6 Contact Information

- **Technical Support**: support@example.com
- **Documentation**: docs@example.com
- **Emergency**: emergency@example.com

---

## Document Information

**Document Version:** 1.0.0  
**Last Updated:** January 2024  
**Next Review:** March 2024  
**Author:** Technical Documentation Team  
**Approved By:** System Administrator

**Change History:**

- v1.0.0 (January 2024): Initial documentation release

---

_This document is maintained by the Technical Documentation Team. For questions or suggestions, please contact the documentation team._
