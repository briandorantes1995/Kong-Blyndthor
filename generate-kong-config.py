#!/usr/bin/env python3
"""
Script para generar kong.yaml desde archivos de configuración fragmentados.
Combina servicios, consumidores y plugins en un único archivo declarativo.
"""

import os
import yaml
import sys
from pathlib import Path

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

