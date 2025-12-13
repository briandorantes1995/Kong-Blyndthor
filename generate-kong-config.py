#!/usr/bin/env python3
"""
Script para generar kong.yaml desde archivos de configuración fragmentados.
Combina servicios, consumidores y plugins en un único archivo declarativo.
"""

import os
import yaml
import sys
import re
from pathlib import Path

def load_env_file(env_file_path):
    """Carga variables de un archivo .env si existe."""
    env_vars = {}
    if env_file_path.exists():
        try:
            with open(env_file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        # Eliminar comillas si existen
                        value = value.strip('"').strip("'")
                        env_vars[key.strip()] = value
        except Exception as e:
            print(f"⚠️  Advertencia: No se pudo leer {env_file_path}: {e}")
    return env_vars

def expand_env_vars(obj, env_vars=None):
    """Expande variables de entorno en el formato ${VAR_NAME} de forma recursiva."""
    if isinstance(obj, dict):
        return {key: expand_env_vars(value, env_vars) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [expand_env_vars(item, env_vars) for item in obj]
    elif isinstance(obj, str):
        # Buscar patrones ${VAR_NAME} y reemplazarlos
        pattern = r'\$\{([^}]+)\}'
        def replace_var(match):
            var_name = match.group(1)
            # Primero buscar en variables de entorno del sistema
            value = os.getenv(var_name)
            # Si no existe y tenemos env_vars, buscar ahí
            if value is None and env_vars:
                value = env_vars.get(var_name)
            if value is None:
                print(f"⚠️  Advertencia: Variable de entorno {var_name} no está definida")
                return match.group(0)  # Mantener el original si no existe
            return value
        return re.sub(pattern, replace_var, obj)
    else:
        return obj

def load_yaml_file(file_path):
    """Carga un archivo YAML y retorna su contenido."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f) or {}
    except FileNotFoundError:
        print(f"⚠️  Advertencia: Archivo no encontrado: {file_path}")
        return {}
    except yaml.YAMLError as e:
        print(f"❌ Error al parsear YAML en {file_path}: {e}")
        sys.exit(1)

def merge_dicts(base, new):
    """Fusiona dos diccionarios, combinando listas cuando es necesario."""
    if not isinstance(base, dict) or not isinstance(new, dict):
        return new
    
    result = base.copy()
    for key, value in new.items():
        if key in result and isinstance(result[key], list) and isinstance(value, list):
            result[key].extend(value)
        elif key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = merge_dicts(result[key], value)
        else:
            result[key] = value
    return result

def generate_kong_config():
    """Genera el archivo kong.yaml combinando todos los archivos de configuración."""
    base_dir = Path(__file__).parent
    output_file = base_dir / "kong.yaml"
    
    # Cargar variables de entorno desde .env si existe
    env_file = base_dir / ".env"
    env_vars = load_env_file(env_file)
    
    # Estructura base del archivo Kong
    kong_config = {
        "_format_version": "3.0",
        "services": [],
        "consumers": [],
        "plugins": []
    }
    
    # Cargar servicios
    services_dir = base_dir / "services"
    if services_dir.exists():
        for service_file in sorted(services_dir.glob("*.yaml")):
            print(f"📄 Procesando servicio: {service_file.name}")
            service_data = load_yaml_file(service_file)
            if "services" in service_data:
                kong_config["services"].extend(service_data["services"])
    
    # Cargar consumidores
    consumers_dir = base_dir / "consumers"
    if consumers_dir.exists():
        for consumer_file in sorted(consumers_dir.glob("*.yaml")):
            print(f"👤 Procesando consumidor: {consumer_file.name}")
            consumer_data = load_yaml_file(consumer_file)
            if "consumers" in consumer_data:
                kong_config["consumers"].extend(consumer_data["consumers"])
    
    # Cargar plugins
    plugins_dir = base_dir / "plugins.yml"
    if plugins_dir.exists():
        for plugin_file in sorted(plugins_dir.glob("*.yaml")):
            print(f"🔌 Procesando plugin: {plugin_file.name}")
            plugin_data = load_yaml_file(plugin_file)
            if "plugins" in plugin_data:
                kong_config["plugins"].extend(plugin_data["plugins"])
    
    # Validaciones básicas
    if not kong_config["services"]:
        print("⚠️  Advertencia: No se encontraron servicios")
    
    if not kong_config["consumers"]:
        print("⚠️  Advertencia: No se encontraron consumidores")
    
    # Expandir variables de entorno en la configuración
    print("🔧 Expandiendo variables de entorno...")
    kong_config = expand_env_vars(kong_config, env_vars)
    
    # Verificar que las variables críticas fueron expandidas
    def check_critical_vars(obj, path=""):
        """Verifica que no queden variables sin expandir críticas."""
        if isinstance(obj, dict):
            for key, value in obj.items():
                check_critical_vars(value, f"{path}.{key}" if path else key)
        elif isinstance(obj, list):
            for idx, item in enumerate(obj):
                check_critical_vars(item, f"{path}[{idx}]" if path else f"[{idx}]")
        elif isinstance(obj, str) and "${" in obj:
            # Solo advertir, no fallar (puede haber variables opcionales)
            if "JWT_SECRET" in obj or "INTERNAL_SECRET" in obj:
                print(f"⚠️  ADVERTENCIA: Variable crítica sin expandir en {path}: {obj}")
    
    check_critical_vars(kong_config)
    
    # Escribir el archivo de salida
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            yaml.dump(kong_config, f, default_flow_style=False, 
                     sort_keys=False, allow_unicode=True, indent=2)
        print(f"✅ Configuración generada exitosamente: {output_file}")
        print(f"   - Servicios: {len(kong_config['services'])}")
        print(f"   - Consumidores: {len(kong_config['consumers'])}")
        print(f"   - Plugins: {len(kong_config['plugins'])}")
        return True
    except Exception as e:
        print(f"❌ Error al escribir {output_file}: {e}")
        sys.exit(1)

if __name__ == "__main__":
    print("🚀 Generando configuración de Kong Gateway...\n")
    generate_kong_config()

