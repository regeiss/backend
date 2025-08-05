# Local Development Environment

This document explains how to set up and use the local development environment for the Cadastro Unificado API.

## 🚀 Quick Start

### Prerequisites

- Docker Desktop installed and running
- Git (to clone the repository)

### 1. Start the Local Environment

**Windows (PowerShell):**

```powershell
.\scripts\local-dev.ps1 start
```

**Linux/Mac:**

```bash
./scripts/local-dev.sh start
```

### 2. Test the Environment

**Windows (PowerShell):**

```powershell
.\scripts\local-dev.ps1 test
```

**Linux/Mac:**

```bash
./scripts/local-dev.sh test
```

## 📊 Services

Once started, the following services will be available:

| Service         | URL                   | Description                 |
| --------------- | --------------------- | --------------------------- |
| **Backend API** | http://localhost:8001 | Direct access to Django API |
| **Nginx Proxy** | http://localhost:8081 | Production-like proxy setup |
| **Redis**       | localhost:6379        | Cache and session storage   |

## 🔍 Health Checks

Test the health of each service:

- **Nginx Health**: http://localhost:8081/nginx-health
- **Backend Health**: http://localhost:8001/api/v1/health/
- **Proxy Health**: http://localhost:8081/api/v1/health/

## 🛠️ Available Commands

### Windows (PowerShell)

```powershell
.\scripts\local-dev.ps1 start    # Start environment
.\scripts\local-dev.ps1 stop     # Stop environment
.\scripts\local-dev.ps1 restart  # Restart environment
.\scripts\local-dev.ps1 logs     # View logs
.\scripts\local-dev.ps1 test     # Run health checks
.\scripts\local-dev.ps1 build    # Build containers
.\scripts\local-dev.ps1 clean    # Clean up everything
```

### Linux/Mac

```bash
./scripts/local-dev.sh start    # Start environment
./scripts/local-dev.sh stop     # Stop environment
./scripts/local-dev.sh restart  # Restart environment
./scripts/local-dev.sh logs     # View logs
./scripts/local-dev.sh test     # Run health checks
./scripts/local-dev.sh build    # Build containers
./scripts/local-dev.sh clean    # Clean up everything
```

## 🔧 Configuration

### Environment Variables

The local environment uses these default settings:

- `DEBUG=1` - Django debug mode enabled
- `SECURE_SSL_REDIRECT=False` - No HTTPS redirect
- `USE_TLS=False` - No TLS/SSL
- `CORS_ALLOWED_ORIGINS=http://localhost:8081,http://localhost:8001`

### Database

The local environment expects a PostgreSQL database at:

```
postgresql://postgres:postgres@host.docker.internal:5432/dev_cadastro_unificado
```

**Note**: You need to have PostgreSQL running locally or update the `DATABASE_URL` in `docker-compose.local.yml`.

## 🐛 Troubleshooting

### Common Issues

1. **Port Already in Use**

   ```bash
   # Check what's using the port
   netstat -ano | findstr :8001
   netstat -ano | findstr :8081
   ```

2. **Database Connection Failed**

   - Ensure PostgreSQL is running
   - Check the `DATABASE_URL` in `docker-compose.local.yml`
   - Verify database exists: `dev_cadastro_unificado`

3. **Container Won't Start**

   ```bash
   # Check logs
   .\scripts\local-dev.ps1 logs

   # Rebuild containers
   .\scripts\local-dev.ps1 build
   ```

4. **Health Checks Fail**
   - Wait a few seconds for services to start
   - Check if all containers are running: `docker ps`
   - Verify nginx configuration: `docker exec cadastro_nginx_local nginx -t`

### Manual Commands

If the scripts don't work, you can run commands manually:

```bash
# Start environment
docker compose -f docker-compose.local.yml up -d

# Check status
docker compose -f docker-compose.local.yml ps

# View logs
docker compose -f docker-compose.local.yml logs -f

# Stop environment
docker compose -f docker-compose.local.yml down
```

## 🔄 Differences from Production

The local environment differs from production in these ways:

- **No SSL/TLS**: HTTP only for easier development
- **Debug Mode**: Django debug enabled
- **Direct Port Access**: Backend exposed on port 8001
- **Simplified Nginx**: No SSL configuration
- **Local Database**: Uses `host.docker.internal` for database

## 📝 Development Workflow

1. **Start the environment**: `.\scripts\local-dev.ps1 start`
2. **Make code changes**: Edit files in your IDE
3. **Test changes**: `.\scripts\local-dev.ps1 test`
4. **View logs**: `.\scripts\local-dev.ps1 logs`
5. **Restart if needed**: `.\scripts\local-dev.ps1 restart`
6. **Stop when done**: `.\scripts\local-dev.ps1 stop`

## 🧹 Cleanup

To completely clean up the local environment:

```bash
.\scripts\local-dev.ps1 clean
```

This will:

- Stop all containers
- Remove all volumes
- Clean up Docker system
- Free up disk space
