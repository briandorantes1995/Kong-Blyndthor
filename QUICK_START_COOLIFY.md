# ⚡ Inicio Rápido con Coolify

## 🎯 Pasos Rápidos para Configurar Auto-Deploy

### 1️⃣ Crear Aplicación en Coolify

1. Abre tu panel de Coolify
2. **Nueva Aplicación** → **Docker Compose**
3. Conecta tu repositorio Git (GitHub/GitLab/Bitbucket)
4. Configura:
   - **Tipo**: Docker Compose
   - **Docker Compose File**: `docker-compose.yaml`
   - **Puerto**: `8000`

### 2️⃣ Variables de Entorno

En **Environment Variables** de Coolify, agrega:

```
INTERNAL_SECRET=tu-secreto-interno-real
JWT_SECRET=tu-secreto-jwt-real
```

### 3️⃣ Activar Auto-Deploy

1. Ve a **CI/CD** o **Advanced** en tu aplicación
2. Activa **"Auto Deploy"**
3. Selecciona la rama (ej: `main`)

### 4️⃣ Configurar Webhook (Opcional pero Recomendado)

**GitHub:**
- Settings → Webhooks → Add webhook
- URL: La que te da Coolify
- Event: `push`
- Guardar

**GitLab:**
- Settings → Webhooks
- URL: La que te da Coolify
- Trigger: `Push events`
- Guardar

## ✅ ¡Listo!

Ahora cada vez que hagas:

```bash
git add .
git commit -m "Actualizar configuración"
git push
```

Coolify automáticamente:
1. 🔍 Detecta el cambio
2. 🔧 Ejecuta `.coolify/build.sh` (genera `kong.yaml`)
3. ✅ Valida la configuración
4. 🚀 Despliega con Docker Compose
5. 🔄 Reinicia Kong con la nueva configuración

## 📋 Checklist

- [ ] Aplicación creada en Coolify
- [ ] Repositorio conectado
- [ ] Variables de entorno configuradas
- [ ] Auto-Deploy activado
- [ ] Webhook configurado (opcional)
- [ ] Hacer push de prueba

## 🐛 Si algo falla

1. Revisa los **Build Logs** en Coolify
2. Verifica que las variables de entorno estén correctas
3. Asegúrate de que Python 3 esté disponible en el build
4. Revisa que `requirements.txt` exista

## 📚 Más Detalles

Ver **[COOLIFY_SETUP.md](COOLIFY_SETUP.md)** para la guía completa.

