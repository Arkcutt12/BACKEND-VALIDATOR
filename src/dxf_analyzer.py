"""
DXF Analyzer - Sistema de análisis y detección de errores para archivos DXF
Orientado a corte láser con detección de errores críticos, advertencias y problemas de exportación.
"""

import ezdxf
import os
import math
from typing import List, Dict, Any, Tuple, Optional
from dataclasses import dataclass, asdict
from collections import defaultdict, Counter
import hashlib
import json
from datetime import datetime
import numpy as np
from math import sqrt, isclose

@dataclass
class ErrorReport:
    """Estructura para reportar un error específico"""
    error_id: int
    error_type: str  # 'CRITICAL', 'WARNING', 'EXPORT_ERROR'
    title: str
    description: str
    cause: str
    suggestion: str
    affected_entities: List[str]
    severity_score: int  # 1-10 (10 más crítico)

@dataclass
class AnalysisResult:
    """Resultado completo del análisis"""
    file_name: str
    analysis_date: str
    total_entities: int
    health_percentage: float
    critical_errors: List[ErrorReport]
    warnings: List[ErrorReport]
    export_errors: List[ErrorReport]
    summary: Dict[str, Any]
    recommendations: List[str]

class DXFAnalyzer:
    """Analizador principal de archivos DXF para corte láser"""
    
    # Capas válidas para corte láser
    VALID_LAYERS = {'CUT', 'ENGRAVE', 'MARK', 'ETCH', 'SCORE', 'REFERENCE'}
    
    # Configuración de análisis
    MIN_SIZE_MM = 5.0
    MAX_SIZE_MM = 3000.0
    MIN_TEXT_HEIGHT_MM = 2.0
    MAX_FILE_SIZE_MB = 50.0
    
    def __init__(self, min_distance_mm: float = 1.0):
        self.min_distance_mm = min_distance_mm
        self.errors = []
        self.warnings = []
        self.export_errors = []
        self.doc = None
        self.total_entities = 0
        
    def analyze_dxf_file(self, file_path: str) -> AnalysisResult:
        """
        Análisis completo de un archivo DXF
        
        Args:
            file_path: Ruta al archivo DXF
            
        Returns:
            AnalysisResult: Resultado completo del análisis
        """
        try:
            # Resetear estado
            self._reset_analysis()
            
            # Cargar archivo DXF
            self.doc = ezdxf.readfile(file_path)
            
            # Contar entidades totales
            self.total_entities = self._count_total_entities()
            
            # Ejecutar todas las validaciones
            self._validate_file_structure()
            self._validate_critical_errors()
            self._validate_warnings()
            self._validate_export_errors()
            self._check_vector_distances()
            self._check_layer_usage()
            self._validate_entities()
            self._check_dimensions()
            
            # Calcular porcentaje de salud
            health_percentage = self._calculate_health_percentage()
            
            # Generar recomendaciones
            recommendations = self._generate_recommendations()
            
            # Crear resultado
            result = AnalysisResult(
                file_name=os.path.basename(file_path),
                analysis_date=datetime.now().isoformat(),
                total_entities=self.total_entities,
                health_percentage=health_percentage,
                critical_errors=self.errors,
                warnings=self.warnings,
                export_errors=self.export_errors,
                summary=self._generate_summary(),
                recommendations=recommendations
            )
            
            return result
            
        except Exception as e:
            # Error al cargar el archivo
            error = ErrorReport(
                error_id=0,
                error_type="CRITICAL",
                title="Error al cargar archivo",
                description=f"No se pudo cargar el archivo DXF: {str(e)}",
                cause="Archivo corrupto, versión no compatible o formato incorrecto",
                suggestion="Verificar que el archivo sea un DXF válido y no esté corrupto",
                affected_entities=["FILE"],
                severity_score=10
            )
            
            return AnalysisResult(
                file_name=os.path.basename(file_path),
                analysis_date=datetime.now().isoformat(),
                total_entities=0,
                health_percentage=0.0,
                critical_errors=[error],
                warnings=[],
                export_errors=[],
                summary={"status": "ERROR", "message": str(e)},
                recommendations=["Verificar integridad del archivo DXF"]
            )
    
    def _reset_analysis(self):
        """Resetea el estado del análisis"""
        self.errors = []
        self.warnings = []
        self.export_errors = []
        self.doc = None
        self.total_entities = 0
    
    def _count_total_entities(self) -> int:
        """Cuenta todas las entidades en el archivo"""
        count = 0
        for layout in self.doc.layouts:
            count += len(list(layout))
        return count
    
    def _validate_file_structure(self):
        """Validaciones básicas de estructura del archivo"""
        # Verificar versión DXF
        if hasattr(self.doc, 'dxfversion'):
            version = self.doc.dxfversion
            if version > 'AC1027':  # Posterior a 2013
                self.export_errors.append(ErrorReport(
                    error_id=20,
                    error_type="EXPORT_ERROR",
                    title="Versión de DXF no compatible",
                    description=f"Archivo creado con versión {version} (posterior a 2013)",
                    cause="Versión muy nueva del formato DXF",
                    suggestion="Exportar como DXF R2010 o R2013 para mejor compatibilidad",
                    affected_entities=["FILE"],
                    severity_score=6
                ))
    
    def _validate_critical_errors(self):
        """Validar errores críticos que bloquean el proceso"""
        
        # Recorrer todos los layouts
        for layout in self.doc.layouts:
            for entity in layout:
                entity_handle = entity.dxf.handle
                
                # Error 1: Vectores abiertos
                if entity.dxftype() in ['LWPOLYLINE', 'POLYLINE']:
                    if not entity.is_closed:
                        layer = entity.dxf.layer
                        if layer.upper() in ['CUT', 'ENGRAVE']:
                            self.errors.append(ErrorReport(
                                error_id=1,
                                error_type="CRITICAL",
                                title="Vectores abiertos",
                                description=f"Polilínea abierta en capa de corte '{layer}'",
                                cause="Mal uso de 'Join'/'Cerrar ruta' en el software de diseño",
                                suggestion="Cerrar todas las polilíneas en capas de corte",
                                affected_entities=[entity_handle],
                                severity_score=10
                            ))
                
                # Error 2: Vectores sin capa asignada
                if not hasattr(entity.dxf, 'layer') or entity.dxf.layer == '0':
                    self.errors.append(ErrorReport(
                        error_id=2,
                        error_type="CRITICAL",
                        title="Vectores sin capa asignada",
                        description="Elemento sin asignación clara de capa",
                        cause="Olvido al diseñar o elementos en capa por defecto",
                        suggestion="Asignar todos los elementos a capas específicas (CUT, ENGRAVE, etc.)",
                        affected_entities=[entity_handle],
                        severity_score=9
                    ))
                
                # Error 3: Texto editable
                if entity.dxftype() in ['TEXT', 'MTEXT']:
                    self.errors.append(ErrorReport(
                        error_id=3,
                        error_type="CRITICAL",
                        title="Texto editable",
                        description="Texto encontrado sin convertir a curvas",
                        cause="No se han convertido las fuentes a contornos vectoriales",
                        suggestion="Convertir todos los textos a curvas/contornos antes de exportar",
                        affected_entities=[entity_handle],
                        severity_score=8
                    ))
                
                # Error 4: Capas incorrectas
                if hasattr(entity.dxf, 'layer'):
                    layer = entity.dxf.layer.upper()
                    if layer not in self.VALID_LAYERS and layer != '0':
                        self.errors.append(ErrorReport(
                            error_id=4,
                            error_type="CRITICAL",
                            title="Capas incorrectas",
                            description=f"Capa '{entity.dxf.layer}' no reconocida",
                            cause="Uso de nombres de capas personalizados",
                            suggestion="Usar nombres estándar: CUT, ENGRAVE, MARK, ETCH, SCORE",
                            affected_entities=[entity_handle],
                            severity_score=7
                        ))
                
                # Error 5: Objetos fuera de área
                bounds = self._get_entity_bounds(entity)
                if bounds:
                    x_min, y_min, x_max, y_max = bounds
                    if abs(x_min) > 2000 or abs(y_min) > 2000 or abs(x_max) > 2000 or abs(y_max) > 2000:
                        self.errors.append(ErrorReport(
                            error_id=5,
                            error_type="CRITICAL",
                            title="Objetos fuera de área",
                            description="Geometría alejada del origen o fuera del área de trabajo",
                            cause="Pegado de objetos externos o errores de escala",
                            suggestion="Mover todos los objetos cerca del origen (0,0)",
                            affected_entities=[entity_handle],
                            severity_score=8
                        ))
                
                # Error 9: Vectores con grosor de línea
                if hasattr(entity.dxf, 'lineweight') and entity.dxf.lineweight > 0:
                    self.errors.append(ErrorReport(
                        error_id=9,
                        error_type="CRITICAL",
                        title="Vectores con grosor de línea",
                        description="Línea con grosor definido encontrada",
                        cause="Exportación incorrecta con grosor de línea",
                        suggestion="Exportar con grosor de línea 0 o 'ByLayer'",
                        affected_entities=[entity_handle],
                        severity_score=6
                    ))
                
                # Error 23: Z-coordinates no planas
                if hasattr(entity.dxf, 'start') and hasattr(entity.dxf.start, 'z'):
                    if abs(entity.dxf.start.z) > 0.001:
                        self.export_errors.append(ErrorReport(
                            error_id=23,
                            error_type="EXPORT_ERROR",
                            title="Z-coordinates no planas",
                            description="Entidad con coordenadas Z diferentes de 0",
                            cause="Diseño en 3D o exportación incorrecta",
                            suggestion="Aplanar todas las entidades al plano Z=0",
                            affected_entities=[entity_handle],
                            severity_score=5
                        ))
        
        # Error 7: Duplicación de vectores
        self._check_duplicate_vectors()
        
        # Error 6: Objetos en capas invisibles
        self._check_invisible_layers()
    
    def _validate_warnings(self):
        """Validar advertencias que no bloquean pero deben revisarse"""
        
        for layout in self.doc.layouts:
            for entity in layout:
                entity_handle = entity.dxf.handle
                
                # Advertencia 11: Escala demasiado pequeña o grande
                bounds = self._get_entity_bounds(entity)
                if bounds:
                    x_min, y_min, x_max, y_max = bounds
                    width = x_max - x_min
                    height = y_max - y_min
                    
                    if width < self.MIN_SIZE_MM or height < self.MIN_SIZE_MM:
                        self.warnings.append(ErrorReport(
                            error_id=11,
                            error_type="WARNING",
                            title="Escala demasiado pequeña",
                            description=f"Elemento muy pequeño ({width:.2f}x{height:.2f}mm)",
                            cause="Escala incorrecta o elementos demasiado pequeños",
                            suggestion=f"Verificar que elementos tengan al menos {self.MIN_SIZE_MM}mm",
                            affected_entities=[entity_handle],
                            severity_score=4
                        ))
                    
                    if width > self.MAX_SIZE_MM or height > self.MAX_SIZE_MM:
                        self.warnings.append(ErrorReport(
                            error_id=11,
                            error_type="WARNING",
                            title="Escala demasiado grande",
                            description=f"Elemento muy grande ({width:.2f}x{height:.2f}mm)",
                            cause="Escala incorrecta o unidades mal configuradas",
                            suggestion=f"Verificar que elementos no excedan {self.MAX_SIZE_MM}mm",
                            affected_entities=[entity_handle],
                            severity_score=5
                        ))
        
        # Advertencia 15: Vectores en capas de referencia
        self._check_reference_layers()
        
        # Advertencia 18: Polilíneas con puntos redundantes
        self._check_excessive_points()
    
    def _validate_export_errors(self):
        """Validar errores de exportación"""
        
        # Error 24: Archivo demasiado pesado
        try:
            file_size_mb = os.path.getsize(self.doc.filename) / (1024 * 1024)
            if file_size_mb > self.MAX_FILE_SIZE_MB:
                self.export_errors.append(ErrorReport(
                    error_id=24,
                    error_type="EXPORT_ERROR",
                    title="Archivo demasiado pesado",
                    description=f"Archivo de {file_size_mb:.2f}MB es muy grande",
                    cause="Demasiados nodos por mala vectorización",
                    suggestion="Simplificar curvas y reducir nodos innecesarios",
                    affected_entities=["FILE"],
                    severity_score=6
                ))
        except:
            pass
    
    def _get_entity_bounds(self, entity) -> Optional[Tuple[float, float, float, float]]:
        """Obtiene los límites de una entidad"""
        try:
            if hasattr(entity, 'bounding_box') and entity.bounding_box:
                bbox = entity.bounding_box
                return (bbox[0].x, bbox[0].y, bbox[1].x, bbox[1].y)
            elif hasattr(entity.dxf, 'start') and hasattr(entity.dxf, 'end'):
                return (
                    min(entity.dxf.start.x, entity.dxf.end.x),
                    min(entity.dxf.start.y, entity.dxf.end.y),
                    max(entity.dxf.start.x, entity.dxf.end.x),
                    max(entity.dxf.start.y, entity.dxf.end.y)
                )
        except:
            pass
        return None
    
    def _check_duplicate_vectors(self):
        """Detecta vectores duplicados"""
        entity_hashes = defaultdict(list)
        
        for layout in self.doc.layouts:
            for entity in layout:
                entity_hash = self._get_entity_hash(entity)
                if entity_hash:
                    entity_hashes[entity_hash].append(entity.dxf.handle)
        
        for hash_value, handles in entity_hashes.items():
            if len(handles) > 1:
                self.errors.append(ErrorReport(
                    error_id=7,
                    error_type="CRITICAL",
                    title="Duplicación de vectores",
                    description=f"Se encontraron {len(handles)} vectores idénticos superpuestos",
                    cause="Copiado sin borrar el original",
                    suggestion="Eliminar vectores duplicados",
                    affected_entities=handles,
                    severity_score=7
                ))
    
    def _get_entity_hash(self, entity) -> Optional[str]:
        """Genera un hash único para una entidad"""
        try:
            # Crear representación de la entidad
            repr_data = {
                'type': entity.dxftype(),
                'layer': entity.dxf.layer if hasattr(entity.dxf, 'layer') else None
            }
            
            # Agregar coordenadas específicas según el tipo
            if hasattr(entity.dxf, 'start') and hasattr(entity.dxf, 'end'):
                repr_data['start'] = (round(entity.dxf.start.x, 3), round(entity.dxf.start.y, 3))
                repr_data['end'] = (round(entity.dxf.end.x, 3), round(entity.dxf.end.y, 3))
            
            return hashlib.md5(str(repr_data).encode()).hexdigest()
        except:
            return None
    
    def _check_invisible_layers(self):
        """Verifica capas invisibles o bloqueadas"""
        for layer_name, layer in self.doc.layers.items():
            if layer.is_off or layer.is_frozen:
                # Contar entidades en esta capa
                entity_count = 0
                for layout in self.doc.layouts:
                    for entity in layout:
                        if hasattr(entity.dxf, 'layer') and entity.dxf.layer == layer_name:
                            entity_count += 1
                
                if entity_count > 0:
                    self.errors.append(ErrorReport(
                        error_id=6,
                        error_type="CRITICAL",
                        title="Objetos en capas invisibles",
                        description=f"Capa '{layer_name}' está oculta/bloqueada con {entity_count} objetos",
                        cause="Capa oculta accidentalmente",
                        suggestion="Activar visibilidad de todas las capas necesarias",
                        affected_entities=[layer_name],
                        severity_score=8
                    ))
    
    def _check_reference_layers(self):
        """Verifica capas de referencia que deberían eliminarse"""
        reference_layers = ['LAYER 0', 'SKETCH', 'REFERENCE', 'GUIDE', 'DEFPOINTS']
        
        for layout in self.doc.layouts:
            for entity in layout:
                if hasattr(entity.dxf, 'layer'):
                    layer_name = entity.dxf.layer.upper()
                    if any(ref in layer_name for ref in reference_layers):
                        self.warnings.append(ErrorReport(
                            error_id=15,
                            error_type="WARNING",
                            title="Vectores en capas de referencia",
                            description=f"Elemento en capa de referencia '{entity.dxf.layer}'",
                            cause="Elementos en capas que no deberían exportarse",
                            suggestion="Eliminar elementos de capas de referencia antes de exportar",
                            affected_entities=[entity.dxf.handle],
                            severity_score=3
                        ))
    
    def _check_excessive_points(self):
        """Verifica polilíneas con demasiados puntos"""
        for layout in self.doc.layouts:
            for entity in layout:
                if entity.dxftype() in ['LWPOLYLINE', 'POLYLINE']:
                    if hasattr(entity, 'vertices'):
                        vertex_count = len(list(entity.vertices))
                        if vertex_count > 100:  # Umbral arbitrario
                            self.warnings.append(ErrorReport(
                                error_id=18,
                                error_type="WARNING",
                                title="Polilíneas con puntos redundantes",
                                description=f"Polilínea con {vertex_count} puntos",
                                cause="Muchas subdivisiones generan ruido en el láser",
                                suggestion="Simplificar curva para reducir puntos",
                                affected_entities=[entity.dxf.handle],
                                severity_score=4
                            ))
    
    def _calculate_health_percentage(self) -> float:
        """Calcula el porcentaje de salud del archivo"""
        if self.total_entities == 0:
            return 0.0
        
        # Pesos por tipo de error
        critical_weight = 10
        warning_weight = 3
        export_weight = 5
        
        # Calcular puntos de error
        critical_points = sum(error.severity_score * critical_weight for error in self.errors)
        warning_points = sum(warning.severity_score * warning_weight for warning in self.warnings)
        export_points = sum(error.severity_score * export_weight for error in self.export_errors)
        
        total_error_points = critical_points + warning_points + export_points
        
        # Calcular porcentaje (máximo teórico de errores)
        max_possible_errors = self.total_entities * 100  # Valor base
        
        if max_possible_errors == 0:
            return 100.0
        
        health_percentage = max(0, 100 - (total_error_points / max_possible_errors * 100))
        return round(health_percentage, 2)
    
    def _generate_summary(self) -> Dict[str, Any]:
        """Genera resumen del análisis"""
        return {
            "total_entities": self.total_entities,
            "critical_errors_count": len(self.errors),
            "warnings_count": len(self.warnings),
            "export_errors_count": len(self.export_errors),
            "layers_found": list(self.doc.layers.keys()) if self.doc else [],
            "dxf_version": self.doc.dxfversion if self.doc and hasattr(self.doc, 'dxfversion') else "Unknown",
            "status": "READY" if len(self.errors) == 0 else "NEEDS_REVIEW" if len(self.errors) < 5 else "CRITICAL"
        }
    
    def _generate_recommendations(self) -> List[str]:
        """Genera recomendaciones basadas en los errores encontrados"""
        recommendations = []
        
        if self.errors:
            recommendations.append("🔴 Corrija todos los errores críticos antes de proceder al corte")
        
        if any(error.error_id == 1 for error in self.errors):
            recommendations.append("✅ Cerrar todas las polilíneas en capas de corte")
        
        if any(error.error_id == 3 for error in self.errors):
            recommendations.append("📝 Convertir todos los textos a curvas/contornos")
        
        if any(error.error_id == 4 for error in self.errors):
            recommendations.append("🏷️ Usar nombres de capas estándar: CUT, ENGRAVE, MARK")
        
        if any(error.error_id == 7 for error in self.errors):
            recommendations.append("🔄 Eliminar vectores duplicados")
        
        if self.warnings:
            recommendations.append("⚠️ Revisar las advertencias para optimizar el proceso")
        
        if not self.errors and not self.warnings:
            recommendations.append("✅ Archivo listo para corte láser")
        
        return recommendations

    def _check_vector_distances(self):
        """Verifica las distancias mínimas entre vectores."""
        msp = self.doc.modelspace()
        entities = list(msp)
        
        for i, entity1 in enumerate(entities):
            if not self._is_vector_entity(entity1):
                continue
                
            points1 = self._get_entity_points(entity1)
            
            for entity2 in entities[i+1:]:
                if not self._is_vector_entity(entity2):
                    continue
                    
                points2 = self._get_entity_points(entity2)
                
                # Verificar distancia entre todos los puntos
                for p1 in points1:
                    for p2 in points2:
                        distance = self._calculate_distance(p1, p2)
                        if 0 < distance < self.min_distance_mm:
                            self.errors.append(ErrorReport(
                                error_id=25,
                                error_type="CRITICAL",
                                title="Vectores demasiado cercanos",
                                description=f"Vectores demasiado cercanos ({distance:.2f}mm). La distancia mínima debe ser {self.min_distance_mm}mm.",
                                cause="Distancias entre vectores muy pequeñas",
                                suggestion="Aumentar la distancia entre vectores",
                                affected_entities=[entity1.handle, entity2.handle],
                                severity_score=10
                            ))

    def _is_vector_entity(self, entity) -> bool:
        """Determina si una entidad es un vector."""
        return entity.dxftype() in ['LINE', 'LWPOLYLINE', 'POLYLINE', 'ARC', 'CIRCLE']

    def _get_entity_points(self, entity) -> List[Tuple[float, float, float]]:
        """Obtiene los puntos de una entidad."""
        points = []
        
        if entity.dxftype() == 'LINE':
            points = [entity.dxf.start, entity.dxf.end]
        elif entity.dxftype() in ['LWPOLYLINE', 'POLYLINE']:
            points = [vertex.dxf.location for vertex in entity.vertices]
        elif entity.dxftype() == 'ARC':
            # Convertir arco a puntos
            center = entity.dxf.center
            radius = entity.dxf.radius
            start_angle = entity.dxf.start_angle
            end_angle = entity.dxf.end_angle
            
            # Crear puntos cada 5 grados
            angles = np.linspace(start_angle, end_angle, 72)
            for angle in angles:
                x = center[0] + radius * np.cos(np.radians(angle))
                y = center[1] + radius * np.sin(np.radians(angle))
                points.append((x, y, center[2]))
        elif entity.dxftype() == 'CIRCLE':
            # Convertir círculo a puntos
            center = entity.dxf.center
            radius = entity.dxf.radius
            
            # Crear puntos cada 5 grados
            angles = np.linspace(0, 360, 72)
            for angle in angles:
                x = center[0] + radius * np.cos(np.radians(angle))
                y = center[1] + radius * np.sin(np.radians(angle))
                points.append((x, y, center[2]))
                
        return points

    def _calculate_distance(self, p1: Tuple[float, float, float], p2: Tuple[float, float, float]) -> float:
        """Calcula la distancia entre dos puntos."""
        return sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2 + (p2[2] - p1[2])**2)

    def _check_layer_usage(self):
        """Verifica el uso correcto de capas."""
        msp = self.doc.modelspace()
        used_layers = set()
        
        for entity in msp:
            used_layers.add(entity.dxf.layer)
            
        if not used_layers:
            self.errors.append(ErrorReport(
                error_id=26,
                error_type="CRITICAL",
                title="No se encontraron capas en uso en el archivo",
                description="No se encontraron capas en uso en el archivo",
                cause="No se encontraron capas en uso en el archivo",
                suggestion="Asignar todas las entidades a capas válidas",
                affected_entities=list(used_layers),
                severity_score=10
            ))

    def _validate_entities(self):
        """Valida las entidades del documento."""
        msp = self.doc.modelspace()
        
        for entity in msp:
            # Verificar entidades sin capa
            if not hasattr(entity, 'dxf') or not hasattr(entity.dxf, 'layer'):
                self.errors.append(ErrorReport(
                    error_id=27,
                    error_type="CRITICAL",
                    title="Entidad sin capa asignada",
                    description=f"Entidad sin capa asignada: {entity}",
                    cause="Entidad sin capa asignada",
                    suggestion="Asignar todas las entidades a capas válidas",
                    affected_entities=[entity.dxf.handle],
                    severity_score=10
                ))
            
            # Verificar entidades muy pequeñas
            if self._is_vector_entity(entity):
                size = self._calculate_entity_size(entity)
                if size < 1.0:  # 1mm mínimo
                    self.warnings.append(ErrorReport(
                        error_id=28,
                        error_type="WARNING",
                        title="Entidad muy pequeña",
                        description=f"Entidad muy pequeña ({size:.2f}mm): {entity}",
                        cause="Entidad muy pequeña",
                        suggestion="Verificar tamaño de la entidad",
                        affected_entities=[entity.dxf.handle],
                        severity_score=5
                    ))

    def _calculate_entity_size(self, entity) -> float:
        """Calcula el tamaño de una entidad."""
        if entity.dxftype() == 'LINE':
            return self._calculate_distance(entity.dxf.start, entity.dxf.end)
        elif entity.dxftype() in ['LWPOLYLINE', 'POLYLINE']:
            points = [vertex.dxf.location for vertex in entity.vertices]
            if len(points) < 2:
                return 0
            return sum(self._calculate_distance(points[i], points[i+1]) 
                      for i in range(len(points)-1))
        elif entity.dxftype() == 'ARC':
            return 2 * np.pi * entity.dxf.radius * (entity.dxf.end_angle - entity.dxf.start_angle) / 360
        elif entity.dxftype() == 'CIRCLE':
            return 2 * np.pi * entity.dxf.radius
        return 0

    def _check_dimensions(self):
        """Verifica las dimensiones del documento."""
        msp = self.doc.modelspace()
        min_x = min_y = float('inf')
        max_x = max_y = float('-inf')
        
        for entity in msp:
            if self._is_vector_entity(entity):
                points = self._get_entity_points(entity)
                for point in points:
                    min_x = min(min_x, point[0])
                    min_y = min(min_y, point[1])
                    max_x = max(max_x, point[0])
                    max_y = max(max_y, point[1])
        
        if min_x != float('inf'):
            width = max_x - min_x
            height = max_y - min_y
            
            if width > 3000 or height > 3000:  # 3 metros máximo
                self.warnings.append(ErrorReport(
                    error_id=29,
                    error_type="WARNING",
                    title="Dimensiones muy grandes",
                    description=f"Dimensiones muy grandes: {width:.0f}mm x {height:.0f}mm",
                    cause="Dimensiones muy grandes",
                    suggestion="Verificar tamaño del archivo",
                    affected_entities=["FILE"],
                    severity_score=5
                ))
            
            if width < 5 or height < 5:  # 5mm mínimo
                self.warnings.append(ErrorReport(
                    error_id=30,
                    error_type="WARNING",
                    title="Dimensiones muy pequeñas",
                    description=f"Dimensiones muy pequeñas: {width:.0f}mm x {height:.0f}mm",
                    cause="Dimensiones muy pequeñas",
                    suggestion="Verificar tamaño del archivo",
                    affected_entities=["FILE"],
                    severity_score=5
                ))

# Funciones auxiliares para la API
def analyze_dxf_file(file_path: str) -> Dict[str, Any]:
    """
    Función principal para analizar un archivo DXF
    
    Args:
        file_path: Ruta al archivo DXF
        
    Returns:
        Dict con el resultado del análisis
    """
    analyzer = DXFAnalyzer()
    result = analyzer.analyze_dxf_file(file_path)
    return asdict(result)

def get_analysis_summary(analysis_result: Dict[str, Any]) -> str:
    """
    Genera un resumen textual del análisis
    
    Args:
        analysis_result: Resultado del análisis
        
    Returns:
        Resumen en texto plano
    """
    summary = f"""
📄 ANÁLISIS DE ARCHIVO DXF: {analysis_result['file_name']}
📊 SALUD DEL ARCHIVO: {analysis_result['health_percentage']}%
📈 ENTIDADES TOTALES: {analysis_result['total_entities']}

🔴 ERRORES CRÍTICOS: {len(analysis_result['critical_errors'])}
⚠️ ADVERTENCIAS: {len(analysis_result['warnings'])}
📤 ERRORES DE EXPORTACIÓN: {len(analysis_result['export_errors'])}

📋 RECOMENDACIONES:
""" + "\n".join(f"• {rec}" for rec in analysis_result['recommendations'])
    
    return summary

if __name__ == "__main__":
    # Ejemplo de uso
    print("🔧 DXF Analyzer - Sistema de análisis de archivos DXF para corte láser")
    print("📄 Listo para analizar archivos DXF y detectar errores críticos") 