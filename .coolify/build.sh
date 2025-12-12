#!/bin/bash
# Script de build para Coolify
# Este script se ejecuta automáticamente antes del despliegue

set -e

echo "🚀 Iniciando build para Kong Gateway..."

# Instalar dependencias Python si es necesario
if [ -f "requirements.txt" ]; then
    echo "📦 Instalando dependencias Python..."
    pip install -q -r requirements.txt || python3 -m pip install -q -r requirements.txt
fi

# Asegurar que kong.yaml no sea un directorio (limpiar si existe como directorio)
if [ -d "kong.yaml" ]; then
    echo "⚠️  Eliminando directorio kong.yaml existente..."
    rm -rf kong.yaml
fi

# Generar configuración de Kong
echo "🔧 Generando configuración de Kong..."
python generate-kong-config.py || python3 generate-kong-config.py

# Verificar que kong.yaml se generó correctamente como archivo
if [ ! -f "kong.yaml" ]; then
    echo "❌ Error: kong.yaml no se generó"
    exit 1
fi

if [ -d "kong.yaml" ]; then
    echo "❌ Error: kong.yaml es un directorio, debería ser un archivo"
    exit 1
fi

# Verificar que el archivo no esté vacío
if [ ! -s "kong.yaml" ]; then
    echo "❌ Error: kong.yaml está vacío"
    exit 1
fi

echo "✅ Build completado exitosamente"
echo "📄 Configuración generada: kong.yaml ($(wc -l < kong.yaml) líneas)"

