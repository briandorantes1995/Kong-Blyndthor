#!/bin/sh
set -e

# Solo generar configuración si no existe o si se solicita explícitamente
if [ ! -f "/etc/kong/kong.yaml" ] || [ "${FORCE_REGENERATE_CONFIG:-}" = "true" ]; then
    echo "🔧 Generando configuración de Kong..."
    
    # Configurar ulimit para mejor rendimiento (si no está configurado en docker-compose)
    if [ "$(ulimit -n)" -lt 4096 ]; then
        ulimit -n 4096 2>/dev/null || echo "⚠️  No se pudo configurar ulimit (requiere privilegios)"
    fi
    
    # Asegurar que /etc/kong existe y tiene permisos correctos
    mkdir -p /etc/kong
    chown kong:kong /etc/kong
    
    # Generar kong.yaml
    cd /kong-config
    python3 generate-kong-config.py
    
    # Verificar que se generó correctamente
    if [ ! -f "kong.yaml" ]; then
        echo "❌ Error: kong.yaml no se generó"
        exit 1
    fi
    
    if [ -d "kong.yaml" ]; then
        echo "❌ Error: kong.yaml es un directorio"
        exit 1
    fi
    
    # Eliminar cualquier directorio o archivo existente en /etc/kong/kong.yaml
    rm -rf /etc/kong/kong.yaml
    
    # Copiar a la ubicación esperada por Kong
    cp kong.yaml /etc/kong/kong.yaml
    
    # Asegurar permisos correctos
    chown kong:kong /etc/kong/kong.yaml
    chmod 644 /etc/kong/kong.yaml
    
    # Verificar que el archivo se copió correctamente
    if [ ! -f "/etc/kong/kong.yaml" ]; then
        echo "❌ Error: No se pudo copiar kong.yaml a /etc/kong/"
        exit 1
    fi
    
    if [ -d "/etc/kong/kong.yaml" ]; then
        echo "❌ Error: /etc/kong/kong.yaml es un directorio"
        exit 1
    fi
    
    echo "✅ Configuración generada y copiada a /etc/kong/kong.yaml"
    echo "📄 Tamaño del archivo: $(wc -l < /etc/kong/kong.yaml) líneas"
else
    echo "ℹ️  Configuración ya existe, omitiendo generación"
fi

# Validar configuración antes de iniciar
echo "🔍 Validando configuración de Kong..."
if command -v gosu >/dev/null 2>&1; then
    VALIDATE_CMD="gosu kong kong config parse /etc/kong/kong.yaml"
elif command -v su-exec >/dev/null 2>&1; then
    VALIDATE_CMD="su-exec kong kong config parse /etc/kong/kong.yaml"
else
    VALIDATE_CMD="su -s /bin/sh kong -c 'kong config parse /etc/kong/kong.yaml'"
fi

if ! $VALIDATE_CMD > /dev/null 2>&1; then
    echo "❌ Error: La configuración de Kong es inválida"
    echo "Ejecutando validación con salida detallada:"
    $VALIDATE_CMD || true
    exit 1
fi
echo "✅ Configuración válida"

# Limpiar sockets colgantes antes de iniciar (evita warnings)
rm -f /usr/local/kong/*.sock 2>/dev/null || true

# Cambiar al usuario kong para ejecutar Kong
# Kong start inicia en modo daemon, necesitamos mantener el contenedor vivo
echo "🚀 Iniciando Kong..."
if command -v gosu >/dev/null 2>&1; then
    if ! gosu kong "$@"; then
        echo "❌ Error al iniciar Kong"
        exit 1
    fi
elif command -v su-exec >/dev/null 2>&1; then
    if ! su-exec kong "$@"; then
        echo "❌ Error al iniciar Kong"
        exit 1
    fi
else
    # Fallback: usar su
    if ! su -s /bin/sh kong -c "$*"; then
        echo "❌ Error al iniciar Kong"
        exit 1
    fi
fi

# Esperar un momento para que Kong inicie completamente
echo "⏳ Esperando que Kong inicie..."
sleep 3

# Verificar que Kong realmente está corriendo
MAX_RETRIES=6
RETRY_COUNT=0
KONG_RUNNING=false

while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
    if pgrep -f "nginx.*master" > /dev/null 2>&1; then
        KONG_RUNNING=true
        break
    fi
    RETRY_COUNT=$((RETRY_COUNT + 1))
    echo "⏳ Esperando proceso de Kong... ($RETRY_COUNT/$MAX_RETRIES)"
    sleep 2
done

if [ "$KONG_RUNNING" = false ]; then
    echo "❌ Error: Kong no pudo iniciar correctamente"
    echo "Revisando logs de error..."
    if [ -f /usr/local/kong/logs/error.log ]; then
        tail -50 /usr/local/kong/logs/error.log || true
    fi
    exit 1
fi

echo "✅ Kong iniciado correctamente, monitoreando proceso..."

# Mantener el contenedor vivo monitoreando el proceso de Kong
while true; do
    if ! pgrep -f "nginx.*master" > /dev/null 2>&1; then
        echo "⚠️  Proceso de Kong no encontrado, saliendo..."
        exit 1
    fi
    sleep 10
done

