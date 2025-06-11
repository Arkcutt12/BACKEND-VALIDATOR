"""
Script para análisis por lotes de archivos DXF
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any

# Agregar el directorio raíz al path
sys.path.append(str(Path(__file__).parent.parent))

from src.dxf_analyzer import analyze_dxf_file, get_analysis_summary

def analyze_directory(directory: str, output_file: str = None) -> List[Dict[str, Any]]:
    """
    Analiza todos los archivos DXF en un directorio
    
    Args:
        directory: Ruta al directorio con archivos DXF
        output_file: Ruta opcional para guardar resultados en JSON
        
    Returns:
        Lista de resultados del análisis
    """
    results = []
    dxf_files = list(Path(directory).glob("**/*.dxf"))
    
    print(f"🔍 Encontrados {len(dxf_files)} archivos DXF")
    
    for dxf_file in dxf_files:
        try:
            print(f"\n📄 Analizando: {dxf_file.name}")
            result = analyze_dxf_file(str(dxf_file))
            results.append(result)
            
            # Mostrar resumen
            print(get_analysis_summary(result))
            
        except Exception as e:
            print(f"❌ Error al analizar {dxf_file.name}: {str(e)}")
    
    # Guardar resultados si se especificó archivo de salida
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"\n💾 Resultados guardados en: {output_file}")
    
    return results

def main():
    """Función principal"""
    if len(sys.argv) < 2:
        print("Uso: python batch_analyze.py <directorio> [archivo_salida.json]")
        sys.exit(1)
    
    directory = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    if not os.path.isdir(directory):
        print(f"❌ El directorio {directory} no existe")
        sys.exit(1)
    
    print(f"🚀 Iniciando análisis por lotes en: {directory}")
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    results = analyze_directory(directory, output_file)
    
    # Resumen final
    total_files = len(results)
    files_with_errors = sum(1 for r in results if r["critical_errors"])
    files_with_warnings = sum(1 for r in results if r["warnings"])
    
    print("\n📊 Resumen Final:")
    print(f"📁 Total archivos analizados: {total_files}")
    print(f"❌ Archivos con errores críticos: {files_with_errors}")
    print(f"⚠️ Archivos con advertencias: {files_with_warnings}")
    print(f"✅ Archivos sin problemas: {total_files - files_with_errors}")

if __name__ == "__main__":
    main() 