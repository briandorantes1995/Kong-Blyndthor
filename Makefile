.PHONY: help generate validate start stop restart logs clean

help: ## Muestra esta ayuda
	@echo "Comandos disponibles:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

generate: ## Genera kong.yaml desde archivos de configuración
	@echo "Generando configuración de Kong..."
	python generate-kong-config.py


start: generate ## Inicia Kong Gateway
	@echo "Iniciando Kong Gateway..."
	docker-compose up -d
	@echo "Kong Gateway iniciado. Espera unos segundos para que esté listo..."
	@sleep 5
	@docker-compose ps

stop: ## Detiene Kong Gateway
	@echo "Deteniendo Kong Gateway..."
	docker-compose down

restart: stop start ## Reinicia Kong Gateway

logs: ## Muestra logs de Kong Gateway
	docker-compose logs -f kong

clean: ## Limpia archivos generados y contenedores
	@echo "Limpiando..."
	docker-compose down -v
	rm -f kong.yaml
	@echo "Limpieza completada"

setup: ## Configura el entorno por primera vez
	@echo "Instalando dependencias Python..."
	pip install -r requirements.txt
	@echo "Generando configuración inicial..."
	python generate-kong-config.py
	@echo "⚠️  IMPORTANTE: Configura las variables de entorno INTERNAL_SECRET y JWT_SECRET"

check: generate ## Regenera configuración

