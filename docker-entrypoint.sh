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

# Limpiar sockets colgantes antes de iniciar (evita warnings)
rm -f /usr/local/kong/*.sock 2>/dev/null || true

# Cambiar al usuario kong para ejecutar Kong
# Intentar diferentes métodos según lo disponible
if command -v gosu >/dev/null 2>&1; then
    exec gosu kong "$@"
elif command -v su-exec >/dev/null 2>&1; then
    exec su-exec kong "$@"
else
    # Fallback: usar su (menos seguro pero funciona)
    exec su -s /bin/sh kong -c "exec \"\$@\"" -- "$@"
fi

