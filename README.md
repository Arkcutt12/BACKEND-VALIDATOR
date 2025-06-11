# 🎯 DXF Analyzer API

API para análisis y detección de errores en archivos DXF para corte láser. Esta API proporciona endpoints para validar y analizar archivos DXF, detectando problemas comunes que podrían afectar el proceso de corte láser.

## 🌟 Características

- Análisis de archivos DXF para corte láser
- Detección de errores críticos y advertencias
- Validación de capas y elementos
- Recomendaciones de optimización
- API RESTful con documentación OpenAPI
- Soporte para archivos DXF de diferentes versiones

## 🚀 Endpoints Principales

### Análisis de Archivos
```http
POST /api/v1/analyze
Content-Type: multipart/form-data

file: [archivo DXF]
```

### Catálogo de Errores
```http
GET /api/v1/errors/catalog
```

### Estado del Sistema
```http
GET /health
```

## 📋 Requisitos

- Python 3.9+
- pip
- virtualenv (recomendado)

## 🛠️ Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/Arkcutt12/BACKEND-VALIDATOR.git
cd BACKEND-VALIDATOR
```

2. Crear y activar entorno virtual:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python -m venv venv
source venv/bin/activate
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Configurar variables de entorno:
```bash
cp .env.example .env
# Editar .env con tus configuraciones
```

## 🏃‍♂️ Ejecución

### Desarrollo Local
```bash
python run.py
```

### Producción
```bash
gunicorn src.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## 🔧 Configuración

### Variables de Entorno
```env
DEBUG=false
LOG_LEVEL=INFO
API_VERSION=v1
MAX_FILE_SIZE_MB=50.0
UPLOAD_FOLDER=./uploads
MIN_SIZE_MM=5.0
MAX_SIZE_MM=3000.0
MIN_TEXT_HEIGHT_MM=2.0
MAX_POLYLINE_POINTS=100
```

## 📦 Estructura del Proyecto

```
BACKEND-VALIDATOR/
├── src/
│   ├── __init__.py
│   ├── main.py           # Punto de entrada de la API
│   ├── config.py         # Configuración
│   ├── models.py         # Modelos de datos
│   └── dxf_analyzer.py   # Lógica de análisis DXF
├── tests/
│   ├── __init__.py
│   └── test_analyzer.py  # Tests unitarios
├── docs/
│   ├── api_documentation.md
│   ├── error_catalog.md
│   └── deployment.md
├── scripts/
│   ├── batch_analyze.py
│   └── setup_dev.py
├── requirements.txt
└── README.md
```

## 🧪 Testing

```bash
# Ejecutar tests
pytest

# Ejecutar tests con cobertura
pytest --cov=src tests/
```

## 📚 Documentación

- [Documentación de la API](docs/api_documentation.md)
- [Catálogo de Errores](docs/error_catalog.md)
- [Guía de Despliegue](docs/deployment.md)

## 🔍 Ejemplos de Uso

### Python
```python
import requests

url = "https://tu-api.com/api/v1/analyze"
files = {"file": open("archivo.dxf", "rb")}

response = requests.post(url, files=files)
print(response.json())
```

### JavaScript
```javascript
const formData = new FormData();
formData.append('file', fileInput.files[0]);

fetch('https://tu-api.com/api/v1/analyze', {
  method: 'POST',
  body: formData
})
.then(response => response.json())
.then(data => console.log(data));
```

### cURL
```bash
curl -X POST \
  -F "file=@archivo.dxf" \
  https://tu-api.com/api/v1/analyze
```

## 📊 Respuestas de la API

### Análisis Exitoso
```json
{
  "status": "success",
  "data": {
    "critical_errors": [],
    "warnings": [],
    "recommendations": []
  }
}
```

### Error en el Análisis
```json
{
  "status": "error",
  "error": {
    "code": "INVALID_FILE",
    "message": "El archivo no es un DXF válido"
  }
}
```

## 🔒 Límites y Restricciones

- Tamaño máximo de archivo: 50MB
- Formatos soportados: DXF
- Versiones DXF soportadas: 2000, 2004, 2007, 2010, 2013, 2018
- Tiempo máximo de análisis: 30 segundos

## 🤝 Contribución

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 📞 Soporte

- Email: soporte@tu-dominio.com
- Discord: [Servidor de Soporte](https://discord.gg/tu-servidor)
- GitHub: [Issues](https://github.com/Arkcutt12/BACKEND-VALIDATOR/issues)

## 🙏 Agradecimientos

- [ezdxf](https://github.com/mozman/ezdxf) - Biblioteca para manejo de archivos DXF
- [FastAPI](https://fastapi.tiangolo.com/) - Framework web moderno
- [Render](https://render.com) - Plataforma de despliegue 