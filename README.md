# Cadastro Unificado API

API Django para integração com banco de dados Oracle existente.

## Instalação

1. Clone o repositório
2. Configure as variáveis de ambiente no arquivo `.env`
3. Execute: `docker-compose up -d`
4. Acesse a documentação da API em: `http://localhost:8001/api/docs/`

## Comandos úteis

```bash
# Gerar models das tabelas existentes
docker-compose exec backend python manage.py inspectdb > apps/cadastro/models_generated.py

# Aplicar migrations
docker-compose exec backend python manage.py migrate

# Criar superusuário
docker-compose exec backend python manage.py createsuperuser
```
