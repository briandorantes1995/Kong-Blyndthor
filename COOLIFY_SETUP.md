# 🚀 Configuración de Coolify para KONG-Blyndthor

Esta guía te ayudará a configurar el despliegue automático con Coolify para que cada push genere y despliegue automáticamente la configuración de Kong.

## 📋 Prerrequisitos

1. **Coolify instalado** en tu servidor
2. **Repositorio Git** (GitHub, GitLab, Bitbucket, o Gitea)
3. **Variables de entorno** configuradas en Coolify

## 🔧 Paso 1: Configurar la Aplicación en Coolify

### 1.1 Crear Nueva Aplicación

1. Accede a tu panel de Coolify
2. Crea una nueva aplicación
3. Selecciona **"Docker Compose"** como tipo de aplicación
4. Conecta tu repositorio Git

### 1.2 Configuración del Repositorio

- **Tipo**: Docker Compose
- **Rama**: `main` o `master` (según tu repositorio)
- **Docker Compose File**: `docker-compose.yaml`
- **Puerto**: `8000` (puerto de Kong)

## 🔐 Paso 2: Configurar Variables de Entorno

En la sección de **Environment Variables** de Coolify, agrega:

```
INTERNAL_SECRET=tu-secreto-interno-aqui
JWT_SECRET=tu-secreto-jwt-aqui
```

⚠️ **Importante**: Usa los secretos que ya tienes configurados. No uses valores de ejemplo.

## 🛠️ Paso 3: Configurar Build Script

Coolify ejecutará automáticamente el script `.coolify/build.sh` antes del despliegue.

Este script:
- ✅ Instala dependencias Python
- ✅ Valida la configuración
- ✅ Genera `kong.yaml` automáticamente

### Verificar que el script sea ejecutable

Si necesitas hacer el script ejecutable manualmente:

```bash
chmod +x .coolify/build.sh
chmod +x .coolify/pre-deploy.sh
```

## 🔄 Paso 4: Habilitar Auto-Deploy

1. En la configuración de tu aplicación en Coolify
2. Ve a la sección **"CI/CD"** o **"Advanced"**
3. Activa **"Auto Deploy"**
4. Selecciona la rama que quieres monitorear (generalmente `main` o `master`)

## 🔗 Paso 5: Configurar Webhook (GitHub/GitLab)

### Para GitHub:

1. Ve a tu repositorio en GitHub
2. Settings → Webhooks → Add webhook
3. **Payload URL**: URL del webhook que te proporciona Coolify
4. **Content type**: `application/json`
5. **Secret**: El secreto configurado en Coolify
6. **Events**: Selecciona "Just the push event"
7. Guarda el webhook

### Para GitLab:

1. Ve a tu proyecto en GitLab
2. Settings → Webhooks
3. Agrega la URL del webhook de Coolify
4. Selecciona "Push events"
5. Guarda el webhook

## 📝 Paso 6: Estructura de Archivos

Asegúrate de que tu repositorio tenga esta estructura:

```
KONG-Blyndthor/
├── .coolify/
│   ├── build.sh          # Script de build (genera kong.yaml)
│   └── pre-deploy.sh     # Script pre-deploy
├── consumers/
│   └── app.yaml
├── services/
│   ├── api.yaml
│   ├── api-public.yaml
│   ├── auth.yaml
│   ├── sse.yaml
│   └── ws.yaml
├── plugins.yml/
│   ├── cors.yaml
│   ├── internal-header.yaml
│   ├── jwt.yaml
│   └── rate-limit.yaml
├── docker-compose.yaml
├── generate-kong-config.py
├── requirements.txt
└── README.md
```

## ✅ Paso 7: Verificar el Despliegue

1. Haz un push a tu repositorio
2. Coolify detectará el cambio automáticamente
3. Ejecutará el script de build
4. Generará `kong.yaml`
5. Desplegará los servicios

### Ver logs en Coolify

Puedes ver los logs del build y despliegue en el panel de Coolify:
- **Build Logs**: Muestra la ejecución de `build.sh`
- **Deployment Logs**: Muestra el despliegue de Docker Compose

## 🔍 Troubleshooting

### Error: "kong.yaml not found"

**Solución**: Verifica que el script `build.sh` se ejecute correctamente. Revisa los logs de build en Coolify.

### Error: "Python not found"

**Solución**: Asegúrate de que Python 3 esté disponible en el contenedor de build. Puedes agregar al `build.sh`:

```bash
python3 --version || python --version
```

### Error: "Module yaml not found"

**Solución**: El script `build.sh` ya instala las dependencias de `requirements.txt`. Verifica que el archivo existe.

### Variables de entorno no se aplican

**Solución**: 
1. Verifica que las variables estén configuradas en Coolify
2. Reinicia el servicio después de agregar variables
3. Verifica que los nombres coincidan exactamente (case-sensitive)

## 🎯 Flujo de Trabajo

1. **Desarrollas localmente** y modificas archivos en `services/`, `consumers/`, o `plugins.yml/`
2. **Haces commit y push** a tu repositorio
3. **Coolify detecta el cambio** automáticamente
4. **Ejecuta build.sh** que genera `kong.yaml`
5. **Despliega** con Docker Compose
6. **Kong se reinicia** con la nueva configuración

## 📚 Recursos Adicionales

- [Documentación de Coolify](https://coolify.io/docs)
- [Coolify Docker Compose](https://coolify.io/docs/applications/docker-compose)
- [Coolify CI/CD](https://coolify.io/docs/applications/ci-cd/introduction)

## 💡 Tips

- **Siempre valida localmente** antes de hacer push
- **Usa ramas** para probar cambios antes de mergear a main
- **Revisa los logs** en Coolify si algo falla
- **Mantén los secretos seguros** usando variables de entorno en Coolify

