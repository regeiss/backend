# Makefile para facilitar comandos do projeto

.PHONY: help build up down logs shell migrate makemigrations createsuperuser test inspectdb

help: ## Mostra esta ajuda
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

build: ## Constrói as imagens Docker
	docker compose build

up: ## Inicia os containers
	docker compose up -d

down: ## Para os containers
	docker compose down

logs: ## Mostra os logs
	docker compose logs -f

rebuild: ## Faz o rebuild sem cache do conatainer
	docker compose down --rmi local --volumes --remove-orphans
	docker compose build --no-cache 
	docker compose up -d

shell: ## Abre o shell do Django
	docker compose exec backend python manage.py shell

bash: ## Abre o bash do container backend
	docker compose exec backend bash

migrate: ## Executa as migrations
	docker compose exec backend python manage.py migrate

makemigrations: ## Cria novas migrations
	docker compose exec backend python manage.py makemigrations

createsuperuser: ## Cria um superusuário
	docker compose exec backend python manage.py createsuperuser

test: ## Executa os testes
	docker compose exec backend python manage.py test

inspectdb: ## Gera models das tabelas existentes
	docker compose exec backend python manage.py inspectdb > backend/apps/cadastro/models_generated.py
	@echo "Models gerados em backend/apps/cadastro/models_generated.py"

collectstatic: ## Coleta arquivos estáticos
	docker compose exec backend python manage.py collectstatic --noinput

restart: ## Reinicia os containers
	docker compose restart

ps: ## Lista os containers
	docker compose ps

clean: ## Remove containers, volumes e imagens
	docker compose down -v --rmi local
