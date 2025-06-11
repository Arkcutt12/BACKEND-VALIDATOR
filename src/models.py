"""
Modelos Pydantic para la API
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime

class ErrorReport(BaseModel):
    """Modelo para reportar un error específico"""
    error_id: int = Field(..., description="ID único del error")
    error_type: str = Field(..., description="Tipo de error: CRITICAL, WARNING, EXPORT_ERROR")
    title: str = Field(..., description="Título del error")
    description: str = Field(..., description="Descripción detallada del error")
    cause: str = Field(..., description="Causa probable del error")
    suggestion: str = Field(..., description="Sugerencia para corregir el error")
    affected_entities: List[str] = Field(..., description="Lista de entidades afectadas")
    severity_score: int = Field(..., ge=1, le=10, description="Puntuación de severidad (1-10)")

class AnalysisResult(BaseModel):
    """Modelo para el resultado completo del análisis"""
    file_name: str = Field(..., description="Nombre del archivo analizado")
    analysis_date: str = Field(..., description="Fecha y hora del análisis")
    total_entities: int = Field(..., description="Número total de entidades en el archivo")
    health_percentage: float = Field(..., ge=0, le=100, description="Porcentaje de salud del archivo")
    critical_errors: List[ErrorReport] = Field(default_factory=list, description="Lista de errores críticos")
    warnings: List[ErrorReport] = Field(default_factory=list, description="Lista de advertencias")
    export_errors: List[ErrorReport] = Field(default_factory=list, description="Lista de errores de exportación")
    summary: Dict[str, Any] = Field(..., description="Resumen del análisis")
    recommendations: List[str] = Field(..., description="Lista de recomendaciones")

class ErrorCatalog(BaseModel):
    """Modelo para el catálogo de errores"""
    critical_errors: List[Dict[str, Any]] = Field(..., description="Lista de errores críticos")
    warnings: List[Dict[str, Any]] = Field(..., description="Lista de advertencias")
    export_errors: List[Dict[str, Any]] = Field(..., description="Lista de errores de exportación")

class HealthCheck(BaseModel):
    """Modelo para la verificación de salud del sistema"""
    status: str = Field(..., description="Estado del sistema")
    version: str = Field(..., description="Versión actual del sistema")
    timestamp: datetime = Field(default_factory=datetime.now, description="Fecha y hora de la verificación")

class APIResponse(BaseModel):
    """Modelo base para respuestas de la API"""
    success: bool = Field(..., description="Indica si la operación fue exitosa")
    message: str = Field(..., description="Mensaje descriptivo")
    data: Optional[Dict[str, Any]] = Field(None, description="Datos de la respuesta") 