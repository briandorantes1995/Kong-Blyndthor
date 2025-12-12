#!/usr/bin/env python3
"""
Script para generar secretos seguros para Kong Gateway.
Genera INTERNAL_SECRET y JWT_SECRET usando secrets de Python.
"""

import secrets
import sys

def generate_secret(length=32):
    """Genera un secreto seguro usando secrets.token_urlsafe."""
    return secrets.token_urlsafe(length)

def main():
    print("🔐 Generando secretos seguros para Kong Gateway...\n")
    
    # Leer JWT_SECRET existente si existe
    jwt_secret = None
    try:
        with open(".env", "r") as f:
            for line in f:
                if line.startswith("JWT_SECRET="):
                    jwt_secret = line.strip().split("=", 1)[1]
                    break
    except FileNotFoundError:
        pass
    
    internal_secret = generate_secret(32)
    
    print("✅ Secreto generado:")
    print("=" * 60)
    print(f"INTERNAL_SECRET={internal_secret}")
    if jwt_secret:
        print(f"JWT_SECRET={jwt_secret} (mantenido)")
    else:
        jwt_secret = generate_secret(32)
        print(f"JWT_SECRET={jwt_secret}")
    print("=" * 60)
    
    print("\n💡 Copia el INTERNAL_SECRET a tu archivo .env")
    print("   O ejecuta: python generate-secrets.py --save")
    
    # Si se pasa --save, guardar directamente
    if "--save" in sys.argv or "-s" in sys.argv:
        try:
            # Leer .env existente o crear nuevo
            env_content = ""
            jwt_found = False
            internal_found = False
            
            try:
                with open(".env", "r") as f:
                    for line in f:
                        if line.startswith("JWT_SECRET="):
                            env_content += line
                            jwt_found = True
                        elif line.startswith("INTERNAL_SECRET="):
                            env_content += f"INTERNAL_SECRET={internal_secret}\n"
                            internal_found = True
                        else:
                            env_content += line
            except FileNotFoundError:
                pass
            
            # Agregar los que faltan
            if not internal_found:
                env_content += f"INTERNAL_SECRET={internal_secret}\n"
            if not jwt_found and jwt_secret:
                env_content += f"JWT_SECRET={jwt_secret}\n"
            
            with open(".env", "w") as f:
                f.write(env_content)
            print("\n✅ INTERNAL_SECRET guardado en .env (JWT_SECRET preservado)")
        except Exception as e:
            print(f"\n❌ Error al guardar: {e}")
            sys.exit(1)

if __name__ == "__main__":
    main()

