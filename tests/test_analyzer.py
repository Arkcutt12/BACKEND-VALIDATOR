"""
Tests para el analizador DXF
"""

import pytest
import os
from src.dxf_analyzer import DXFAnalyzer, analyze_dxf_file

def test_analyzer_initialization():
    """Test de inicialización del analizador"""
    analyzer = DXFAnalyzer()
    assert analyzer.errors == []
    assert analyzer.warnings == []
    assert analyzer.export_errors == []
    assert analyzer.doc is None
    assert analyzer.total_entities == 0

def test_valid_layers():
    """Test de capas válidas"""
    analyzer = DXFAnalyzer()
    valid_layers = {'CUT', 'ENGRAVE', 'MARK', 'ETCH', 'SCORE', 'REFERENCE'}
    assert analyzer.VALID_LAYERS == valid_layers

def test_configuration_limits():
    """Test de límites de configuración"""
    analyzer = DXFAnalyzer()
    assert analyzer.MIN_SIZE_MM == 5.0
    assert analyzer.MAX_SIZE_MM == 3000.0
    assert analyzer.MIN_TEXT_HEIGHT_MM == 2.0
    assert analyzer.MAX_FILE_SIZE_MB == 50.0

@pytest.mark.skipif(not os.path.exists("tests/fixtures/valid_file.dxf"),
                   reason="Archivo de prueba no encontrado")
def test_analyze_valid_file():
    """Test de análisis de archivo válido"""
    result = analyze_dxf_file("tests/fixtures/valid_file.dxf")
    assert result["health_percentage"] > 0
    assert len(result["critical_errors"]) == 0
    assert "file_name" in result
    assert "analysis_date" in result
    assert "total_entities" in result

@pytest.mark.skipif(not os.path.exists("tests/fixtures/error_file.dxf"),
                   reason="Archivo de prueba no encontrado")
def test_analyze_error_file():
    """Test de análisis de archivo con errores"""
    result = analyze_dxf_file("tests/fixtures/error_file.dxf")
    assert result["health_percentage"] < 100
    assert len(result["critical_errors"]) > 0
    assert len(result["recommendations"]) > 0

def test_invalid_file():
    """Test de manejo de archivo inválido"""
    with pytest.raises(Exception):
        analyze_dxf_file("tests/fixtures/nonexistent.dxf") 