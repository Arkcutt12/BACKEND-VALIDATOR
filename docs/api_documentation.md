# 📚 Documentación de la API DXF Analyzer

## Endpoints

### GET /
Endpoint raíz que proporciona información básica sobre la API.

**Respuesta:**
```json
{
    "message": "DXF Analyzer API",
    "version": "1.0.0",
    "status": "online"
}
```

### GET /health
Verifica el estado de salud del sistema.

**Respuesta:**
```json
{
    "status": "healthy",
    "version": "1.0.0"
}
```

### POST /api/v1/analyze
Analiza un archivo DXF y retorna el resultado del análisis.

**Parámetros:**
- `file`: Archivo DXF a analizar (multipart/form-data)

**Respuesta:**
```json
{
    "file_name": "ejemplo.dxf",
    "analysis_date": "2024-01-01T12:00:00",
    "total_entities": 100,
    "health_percentage": 85.5,
    "critical_errors": [
        {
            "error_id": 1,
            "error_type": "CRITICAL",
            "title": "Vectores abiertos",
            "description": "Polilínea abierta en capa de corte 'CUT'",
            "cause": "Mal uso de 'Join'/'Cerrar ruta' en el software de diseño",
            "suggestion": "Cerrar todas las polilíneas en capas de corte",
            "affected_entities": ["1A2B3C"],
            "severity_score": 10
        }
    ],
    "warnings": [...],
    "export_errors": [...],
    "summary": {
        "total_entities": 100,
        "critical_errors_count": 1,
        "warnings_count": 2,
        "export_errors_count": 0,
        "layers_found": ["CUT", "ENGRAVE"],
        "dxf_version": "AC1027",
        "status": "NEEDS_REVIEW"
    },
    "recommendations": [
        "🔴 Corrija todos los errores críticos antes de proceder al corte",
        "✅ Cerrar todas las polilíneas en capas de corte"
    ]
}
```

### GET /api/v1/errors/catalog
Retorna el catálogo completo de errores detectables.

**Respuesta:**
```json
{
    "critical_errors": [
        {
            "id": 1,
            "title": "Vectores abiertos",
            "description": "Polilíneas sin cerrar en capas de corte"
        },
        ...
    ],
    "warnings": [
        {
            "id": 11,
            "title": "Escala incorrecta",
            "description": "Elementos <5mm o >3000mm"
        },
        ...
    ],
    "export_errors": [
        {
            "id": 20,
            "title": "Versión DXF",
            "description": "Formato muy nuevo o no compatible"
        },
        ...
    ]
}
```

## Códigos de Error

### Errores HTTP
- `400 Bad Request`: Archivo no válido o formato incorrecto
- `413 Payload Too Large`: Archivo demasiado grande
- `415 Unsupported Media Type`: Tipo de archivo no soportado
- `500 Internal Server Error`: Error interno del servidor

### Errores de Análisis
- `0`: Error al cargar archivo
- `1`: Vectores abiertos
- `2`: Vectores sin capa
- `3`: Texto editable
- `4`: Capas incorrectas
- `5`: Objetos fuera de área
- `6`: Capas invisibles
- `7`: Vectores duplicados
- `8`: Capas mezcladas
- `9`: Grosor de línea
- `10`: Unidades incorrectas

## Ejemplos de Uso

### cURL
```bash
# Analizar archivo
curl -X POST "http://localhost:8000/api/v1/analyze" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@mi_archivo.dxf"

# Obtener catálogo de errores
curl -X GET "http://localhost:8000/api/v1/errors/catalog" \
     -H "accept: application/json"
```

### Python
```python
import requests

# Analizar archivo
with open("mi_archivo.dxf", "rb") as f:
    response = requests.post(
        "http://localhost:8000/api/v1/analyze",
        files={"file": f}
    )
    result = response.json()

# Obtener catálogo de errores
response = requests.get("http://localhost:8000/api/v1/errors/catalog")
catalog = response.json()
```

### JavaScript
```javascript
// Analizar archivo
const formData = new FormData();
formData.append("file", fileInput.files[0]);

fetch("http://localhost:8000/api/v1/analyze", {
    method: "POST",
    body: formData
})
.then(response => response.json())
.then(result => console.log(result));

// Obtener catálogo de errores
fetch("http://localhost:8000/api/v1/errors/catalog")
.then(response => response.json())
.then(catalog => console.log(catalog));
```

## Límites y Restricciones

- Tamaño máximo de archivo: 50MB
- Formatos soportados: DXF
- Versiones DXF soportadas: R2010, R2013
- Límites de tamaño:
  - Mínimo: 5mm
  - Máximo: 3000mm
- Capas válidas: CUT, ENGRAVE, MARK, ETCH, SCORE, REFERENCE

## Mejores Prácticas

1. **Preparación de Archivos**
   - Exportar como DXF R2010 o R2013
   - Usar nombres de capas estándar
   - Convertir textos a curvas
   - Cerrar todas las polilíneas

2. **Manejo de Errores**
   - Revisar siempre los errores críticos primero
   - Considerar las advertencias para optimización
   - Seguir las recomendaciones proporcionadas

3. **Rendimiento**
   - Limitar el tamaño de los archivos
   - Simplificar geometrías complejas
   - Eliminar elementos innecesarios

## Soporte

Para reportar problemas o solicitar ayuda:
- Crear un issue en GitHub
- Contactar al equipo de soporte
- Consultar la documentación completa 