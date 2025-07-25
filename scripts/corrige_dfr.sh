#!/bin/bash

echo "=== Corrigindo Problema do DRF Spectacular ==="

# Parar containers
echo "Parando containers..."
docker compose down

# Remover containers e imagens para rebuild completo
echo "Removendo containers e imagens..."
docker compose down --rmi local --volumes --remove-orphans

# Limpar cache do pip no container
echo "Limpando cache..."
docker system prune -f

# Reconstruir as imagens com as versões corrigidas
echo "Reconstruindo imagens com requirements.txt atualizado..."
docker compose build --no-cache

# Subir os containers
echo "Iniciando containers..."
docker compose up -d

# Aguardar o banco estar pronto
echo "Aguardando banco de dados..."
sleep 15

# Verificar se o backend está funcionando
echo "Verificando status do backend..."
docker-compose exec backend python -c "
import django
django.setup()
print('Django configurado com sucesso!')

# Verificar se DRF Spectacular está funcionando
try:
    from drf_spectacular.openapi import AutoSchema
    print('DRF Spectacular importado com sucesso!')
except Exception as e:
    print(f'Erro no DRF Spectacular: {e}')

# Verificar se as apps estão carregadas
from django.apps import apps
print('Apps carregadas:', [app.name for app in apps.get_app_configs()])
"

# Executar migrations
echo "Executando migrations..."
docker compose exec backend python manage.py migrate --run-syncdb

# Coletar static files
echo "Coletando arquivos estáticos..."
docker compose exec backend python manage.py collectstatic --noinput

# Testar a documentação da API
echo "Testando documentação da API..."
sleep 5

# Verificar se os endpoints estão funcionando
echo "Verificando endpoints..."
curl -s http://localhost:8001/api/v1/ || echo "Erro ao acessar API"
curl -s http://localhost:8001/api/schema/ || echo "Erro ao acessar schema"

echo ""
echo "=== Correção Concluída! ==="
echo ""
echo "🚀 Teste os seguintes endpoints:"
echo "   - API: http://localhost:8001/api/v1/"
echo "   - Health: http://localhost:8001/api/v1/health/"
echo "   - Docs: http://localhost:8001/api/docs/"
echo "   - Schema: http://localhost:8001/api/schema/"
echo ""
echo "📝 Se ainda houver problemas:"
echo "   1. Verifique os logs: make logs"
echo "   2. Entre no container: make bash"
echo "   3. Teste manualmente: python manage.py spectacular --validate"
