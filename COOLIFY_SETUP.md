# 🚀 Configuración de Coolify

Guía rápida para configurar el despliegue automático con Coolify.

## 📋 Pasos Rápidos

1. **Crear aplicación** en Coolify (tipo: Docker Compose)
2. **Conectar repositorio** Git
3. **Configurar variables de entorno**:
   - `INTERNAL_SECRET`
   - `JWT_SECRET`
4. **Activar Auto-Deploy**
5. **Configurar webhook** (opcional)

## 🔄 Flujo Automático

Cada push a tu repositorio:
1. Coolify detecta el cambio
2. Ejecuta `.coolify/build.sh` (genera `kong.yaml`)
3. Despliega con Docker Compose
4. Kong se reinicia con la nueva configuración

## 🔍 Troubleshooting

- **Error de build**: Revisa los Build Logs en Coolify
- **Variables no aplican**: Verifica nombres exactos (case-sensitive)
- **Python no encontrado**: El build.sh instala dependencias automáticamente

## 📚 Recursos

- [Documentación de Coolify](https://coolify.io/docs)
- [Coolify Docker Compose](https://coolify.io/docs/applications/docker-compose)

