"""
API principal para el DXF Analyzer
"""

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
import tempfile
from typing import Dict, Any

from .dxf_analyzer import analyze_dxf_file, get_analysis_summary

app = FastAPI(
    title="DXF Analyzer API",
    description="API para análisis y detección de errores en archivos DXF para corte láser",
    version="1.0.0"
)

# Configuración CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar los orígenes permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Endpoint raíz"""
    return {
        "message": "DXF Analyzer API",
        "version": "1.0.0",
        "status": "online"
    }

@app.get("/health")
async def health_check():
    """Endpoint de verificación de salud"""
    return {
        "status": "healthy",
        "version": "1.0.0"
    }

@app.post("/api/v1/analyze")
async def analyze_file(file: UploadFile = File(...)) -> Dict[str, Any]:
    """
    Analiza un archivo DXF y retorna el resultado del análisis
    
    Args:
        file: Archivo DXF a analizar
        
    Returns:
        Dict con el resultado del análisis
    """
    if not file.filename.lower().endswith('.dxf'):
        raise HTTPException(
            status_code=400,
            detail="Solo se aceptan archivos DXF"
        )
    
    try:
        # Crear archivo temporal
        with tempfile.NamedTemporaryFile(delete=False, suffix='.dxf') as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file.flush()
            
            # Analizar archivo
            result = analyze_dxf_file(temp_file.name)
            
            # Limpiar archivo temporal
            os.unlink(temp_file.name)
            
            return result
            
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al analizar el archivo: {str(e)}"
        )

@app.get("/api/v1/errors/catalog")
async def get_error_catalog():
    """Retorna el catálogo completo de errores detectables"""
    return {
        "critical_errors": [
            {
                "id": 1,
                "title": "Vectores abiertos",
                "description": "Polilíneas sin cerrar en capas de corte"
            },
            {
                "id": 2,
                "title": "Vectores sin capa",
                "description": "Elementos sin asignación clara (CUT, ENGRAVE, etc.)"
            },
            {
                "id": 3,
                "title": "Texto editable",
                "description": "Letras como fuente, no como contornos"
            },
            {
                "id": 4,
                "title": "Capas incorrectas",
                "description": "Nombres de capas no reconocidas"
            },
            {
                "id": 5,
                "title": "Objetos fuera de área",
                "description": "Geometrías alejadas del 0,0"
            }
        ],
        "warnings": [
            {
                "id": 11,
                "title": "Escala incorrecta",
                "description": "Elementos <5mm o >3000mm"
            },
            {
                "id": 15,
                "title": "Capas de referencia",
                "description": "Elementos en capas guía"
            },
            {
                "id": 18,
                "title": "Puntos redundantes",
                "description": "Polilíneas con muchos nodos"
            }
        ],
        "export_errors": [
            {
                "id": 20,
                "title": "Versión DXF",
                "description": "Formato muy nuevo o no compatible"
            },
            {
                "id": 23,
                "title": "Z-coordinates",
                "description": "Entidades con valores Z ≠ 0"
            },
            {
                "id": 24,
                "title": "Archivo pesado",
                "description": "Demasiados nodos innecesarios"
            }
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 