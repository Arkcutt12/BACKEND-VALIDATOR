"""
Configuración del sistema DXF Analyzer
"""

import os
from typing import Set
from pydantic import BaseSettings

class Settings(BaseSettings):
    """Configuración principal del sistema"""
    
    # Configuración general
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"
    API_VERSION: str = "v1"
    
    # Límites de archivos
    MAX_FILE_SIZE_MB: float = 50.0
    ALLOWED_EXTENSIONS: Set[str] = {"dxf"}
    UPLOAD_FOLDER: str = "./uploads"
    
    # Configuración del analizador
    MIN_SIZE_MM: float = 5.0
    MAX_SIZE_MM: float = 3000.0
    MIN_TEXT_HEIGHT_MM: float = 2.0
    MAX_POLYLINE_POINTS: int = 100
    
    # Capas válidas
    VALID_LAYERS: Set[str] = {
        "CUT",
        "ENGRAVE",
        "MARK",
        "ETCH",
        "SCORE",
        "REFERENCE"
    }
    
    # Configuración de la API
    API_TITLE: str = "DXF Analyzer API"
    API_DESCRIPTION: str = "API para análisis y detección de errores en archivos DXF para corte láser"
    API_VERSION: str = "1.0.0"
    
    # CORS
    CORS_ORIGINS: Set[str] = {"*"}
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Instancia global de configuración
settings = Settings()

# Asegurar que existe el directorio de uploads
os.makedirs(settings.UPLOAD_FOLDER, exist_ok=True) 