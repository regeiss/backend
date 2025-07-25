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
