# KONG-Blyndthor

Configuración declarativa de Kong Gateway en modo DB-less para gestión de APIs.

## 📋 Descripción

Este proyecto contiene una configuración modular de Kong Gateway que permite gestionar múltiples servicios, consumidores y plugins de forma organizada y mantenible.

## 🏗️ Estructura del Proyecto

```
KONG-Blyndthor/
├── consumers/          # Configuración de consumidores (usuarios/apps)
│   └── app.yaml
├── services/           # Definición de servicios backend
│   ├── api.yaml
│   ├── api-public.yaml
│   ├── auth.yaml
│   ├── sse.yaml
│   └── ws.yaml
├── plugins.yml/        # Plugins de Kong
│   ├── cors.yaml
│   ├── internal-header.yaml
│   ├── jwt.yaml
│   └── rate-limit.yaml
├── docker-compose.yaml # Orquestación de servicios
├── generate-kong-config.py  # Script para generar kong.yaml
└── kong.yaml          # Configuración generada (no editar manualmente)
```

## 🚀 Inicio Rápido

### Prerrequisitos

- Docker y Docker Compose
- Python 3.6+ (para el script de generación)

### Instalación

1. **Clonar el repositorio**
   ```bash
   git clone <tu-repositorio>
   cd KONG-Blyndthor
   ```

2. **Configurar variables de entorno**
   ```bash
   cp .env.example .env
   # Editar .env con tus secretos
   ```

3. **Generar configuración de Kong**
   ```bash
   python generate-kong-config.py
   ```

4. **Iniciar Kong Gateway**
   ```bash
   docker-compose up -d
   ```

5. **Verificar que Kong está funcionando**
   ```bash
   curl http://localhost:8000
   ```

## 📝 Servicios Configurados

- **api-main** (`/api`) - API principal protegida con JWT
- **api-public** (`/api/public`) - API pública sin autenticación
- **auth** (`/auth`) - Servicio de autenticación
- **sse** (`/sse`) - Server-Sent Events
- **ws** (`/ws`) - WebSocket

## 🔌 Plugins Configurados

### JWT
- Verificación de tokens JWT en servicios protegidos
- Validación de expiración (`exp` claim)
- Key claim: `iss`

### CORS
- Orígenes permitidos: `https://tuweb.com`
- Métodos: GET, POST, PUT, DELETE
- Headers: Authorization, Content-Type
- Credenciales habilitadas

### Rate Limiting
- Límite: 200 solicitudes por minuto
- Política: local (en memoria)

### Internal Header
- Agrega header `X-Internal-Auth` con secreto interno
- Para autenticación entre servicios

## 👤 Consumidores

- **app** (`main-app`) - Aplicación principal con JWT configurado

## 🔧 Desarrollo

### Regenerar configuración

Después de modificar cualquier archivo de configuración:

```bash
python generate-kong-config.py
docker-compose restart kong
```

### Ver logs de Kong

```bash
docker-compose logs -f kong
```

## 🔒 Seguridad

- ⚠️ **NUNCA** commitees el archivo `.env` al repositorio
- Usa secretos fuertes y únicos para `INTERNAL_SECRET` y `JWT_SECRET`
- Revisa regularmente los permisos de los archivos de configuración
- Considera usar un gestor de secretos en producción

## 📚 Recursos

- [Documentación de Kong Gateway](https://docs.konghq.com/)
- [Kong Declarative Configuration](https://docs.konghq.com/gateway/latest/production/deployment-topologies/db-less-and-declarative-config/)
- [Kong Docker](https://hub.docker.com/_/kong)

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo LICENSE para más detalles.

## ⚠️ Notas

- El archivo `kong.yaml` es generado automáticamente, no lo edites manualmente
- Asegúrate de regenerar la configuración después de cualquier cambio
- En producción, considera usar Kong con base de datos para mejor rendimiento

## 🚀 Despliegue con Coolify

Este proyecto está configurado para desplegarse automáticamente con **Coolify**.

### Configuración Automática

Cada vez que hagas push a tu repositorio:
1. ✅ Coolify detecta los cambios
2. ✅ Ejecuta el script de build (`.coolify/build.sh`)
3. ✅ Genera automáticamente `kong.yaml`
4. ✅ Valida la configuración
5. ✅ Despliega con Docker Compose

### Pasos para Configurar

Ver la guía completa en **[COOLIFY_SETUP.md](COOLIFY_SETUP.md)**

**Resumen rápido:**
1. Crea una aplicación Docker Compose en Coolify
2. Conecta tu repositorio Git
3. Configura las variables de entorno (`INTERNAL_SECRET`, `JWT_SECRET`)
4. Activa Auto-Deploy
5. Configura el webhook en tu repositorio

¡Listo! Cada push generará y desplegará automáticamente. 🎉

