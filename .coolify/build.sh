#!/bin/bash
# Script de build para Coolify
# Este script se ejecuta automáticamente antes del despliegue

set -e

echo "🚀 Iniciando build para Kong Gateway..."

# Instalar dependencias Python si es necesario
if [ -f "requirements.txt" ]; then
    echo "📦 Instalando dependencias Python..."
    pip install -q -r requirements.txt
fi

# Generar configuración de Kong
echo "🔧 Generando configuración de Kong..."
python generate-kong-config.py

# Verificar que kong.yaml se generó correctamente
if [ ! -f "kong.yaml" ]; then
    echo "❌ Error: kong.yaml no se generó"
    exit 1
fi

echo "✅ Build completado exitosamente"
echo "📄 Configuración generada: kong.yaml"

