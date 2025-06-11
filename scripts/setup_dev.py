"""
Script de configuración para el entorno de desarrollo
"""

import os
import sys
import shutil
from pathlib import Path

def setup_development_environment():
    """Configura el entorno de desarrollo"""
    
    # Obtener el directorio raíz del proyecto
    root_dir = Path(__file__).parent.parent
    
    # Crear directorios necesarios
    directories = [
        "uploads",
        "tests/fixtures",
        "logs"
    ]
    
    for directory in directories:
        dir_path = root_dir / directory
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"✅ Directorio creado: {directory}")
    
    # Crear archivo .env si no existe
    env_file = root_dir / ".env"
    if not env_file.exists():
        env_example = root_dir / ".env.example"
        if env_example.exists():
            shutil.copy(env_example, env_file)
            print("✅ Archivo .env creado desde .env.example")
        else:
            print("⚠️ No se encontró .env.example")
    
    # Crear archivos de prueba básicos
    fixtures_dir = root_dir / "tests/fixtures"
    
    # Crear archivo DXF de prueba válido
    valid_dxf = fixtures_dir / "valid_file.dxf"
    if not valid_dxf.exists():
        with open(valid_dxf, "w") as f:
            f.write("0\nSECTION\n2\nHEADER\n0\nENDSEC\n0\nEOF")
        print("✅ Archivo de prueba válido creado")
    
    # Crear archivo DXF de prueba con errores
    error_dxf = fixtures_dir / "error_file.dxf"
    if not error_dxf.exists():
        with open(error_dxf, "w") as f:
            f.write("0\nSECTION\n2\nHEADER\n0\nENDSEC\n0\nEOF")
        print("✅ Archivo de prueba con errores creado")
    
    print("\n🎉 Configuración completada!")
    print("\nPróximos pasos:")
    print("1. Instalar dependencias: pip install -r requirements.txt")
    print("2. Activar entorno virtual (si lo usas)")
    print("3. Ejecutar tests: pytest")
    print("4. Iniciar servidor: python run.py")

if __name__ == "__main__":
    setup_development_environment() 