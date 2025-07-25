#!/bin/bash

echo "=== Setup do Projeto Cadastro Unificado API ==="

# Verificar se o arquivo .env existe
if [ ! -f .env ]; then
    echo "Criando arquivo .env a partir do .env.example..."
    cp .env.example .env
    echo "⚠️  Por favor, edite o arquivo .env com suas configurações antes de continuar!"
    echo "Pressione ENTER depois de configurar o .env..."
    read
fi

# Construir as imagens
echo "Construindo imagens Docker..."
docker-compose build

# Subir os containers
echo "Iniciando containers..."
docker-compose up -d

# Aguardar o banco estar pronto
echo "Aguardando banco de dados..."
sleep 10

# Executar migrations
echo "Executando migrations..."
docker-compose exec backend python manage.py migrate

# Gerar models das tabelas existentes
echo "Gerando models das tabelas existentes..."
docker-compose exec backend python manage.py inspectdb > backend/apps/cadastro/models_generated.py

echo "✅ Models gerados em backend/apps/cadastro/models_generated.py"
echo "⚠️  IMPORTANTE: Revise o arquivo gerado e copie os models relevantes para backend/apps/cadastro/models.py"

# Coletar static files
echo "Coletando arquivos estáticos..."
docker-compose exec backend python manage.py collectstatic --noinput

# Criar superusuário
echo "Deseja criar um superusuário? (s/n)"
read -r resposta
if [[ "$resposta" == "s" || "$resposta" == "S" ]]; then
    docker-compose exec backend python manage.py createsuperuser
fi

echo ""
echo "=== Setup Concluído! ==="
echo ""
echo "📝 Próximos passos:"
echo "1. Revise os models gerados em backend/apps/cadastro/models_generated.py"
echo "2. Copie os models relevantes para backend/apps/cadastro/models.py"
echo "3. Ajuste os serializers e views conforme necessário"
echo ""
echo "🚀 A API está rodando em:"
echo "   - API: http://10.13.65.37:8001"
echo "   - Nginx: http://10.13.65.37:8081"
echo "   - Documentação: http://10.13.65.37:8001/api/docs/"
echo ""
echo "📚 Comandos úteis:"
echo "   - make logs      # Ver logs"
echo "   - make shell     # Shell Django"
echo "   - make test      # Executar testes"
echo "   - make down      # Parar containers"
