#!/bin/bash
# Script para iniciar el proyecto con Docker

set -e

echo "🚀 Iniciando Sales Datamart API con Docker..."

# Verificar que existe la carpeta datamart
if [ ! -d "datamart" ]; then
    echo "Error: La carpeta 'datamart' no existe"
    echo "Crea la carpeta y coloca los archivos .parquet"
    exit 1
fi

# Verificar que hay archivos .parquet
if [ -z "$(ls -A datamart/*.parquet 2>/dev/null)" ]; then
    echo "Advertencia: No se encontraron archivos .parquet en 'datamart/'"
    read -p "¿Continuar de todos modos? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Verificar que existe .env
if [ ! -f ".env" ]; then
    echo "No existe archivo .env, creando desde .env.example..."
    cp .env.example .env
    echo "Archivo .env creado. Por favor, ajusta los valores necesarios."
    echo "Presiona Enter para continuar..."
    read
fi


docker-compose build

docker-compose up -d