# 🚀 Guía de Despliegue DXF Analyzer

## Requisitos del Sistema

### Hardware Mínimo
- CPU: 2 cores
- RAM: 4GB
- Disco: 10GB

### Software
- Python 3.8+
- pip
- virtualenv (recomendado)
- Git

## Instalación

### 1. Clonar Repositorio
```bash
git clone https://github.com/tu-usuario/dxf-analyzer-backend.git
cd dxf-analyzer-backend
```

### 2. Configurar Entorno Virtual
```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno
# En Windows:
venv\Scripts\activate
# En Linux/Mac:
source venv/bin/activate
```

### 3. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar Variables de Entorno
```bash
# Copiar archivo de ejemplo
cp .env.example .env

# Editar variables según necesidad
nano .env
```

## Configuración

### Variables de Entorno
```env
# Configuración general
DEBUG=false
LOG_LEVEL=INFO
API_VERSION=v1

# Límites de archivos
MAX_FILE_SIZE_MB=50.0
UPLOAD_FOLDER=./uploads

# Configuración del analizador
MIN_SIZE_MM=5.0
MAX_SIZE_MM=3000.0
MIN_TEXT_HEIGHT_MM=2.0
MAX_POLYLINE_POINTS=100

# Configuración de la API
API_TITLE=DXF Analyzer API
API_DESCRIPTION=API para análisis y detección de errores en archivos DXF para corte láser
API_VERSION=1.0.0

# CORS
CORS_ORIGINS=["https://tu-dominio.com"]
```

## Despliegue

### Desarrollo Local
```bash
# Iniciar servidor de desarrollo
python run.py
```

### Producción con Gunicorn
```bash
# Instalar Gunicorn
pip install gunicorn

# Iniciar servidor
gunicorn src.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

### Docker
```bash
# Construir imagen
docker build -t dxf-analyzer .

# Ejecutar contenedor
docker run -d -p 8000:8000 --name dxf-analyzer dxf-analyzer
```

### Docker Compose
```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./uploads:/app/uploads
    environment:
      - DEBUG=false
      - LOG_LEVEL=INFO
    restart: unless-stopped
```

## Monitoreo

### Logs
```bash
# Ver logs
tail -f logs/app.log

# Rotación de logs
logrotate -f /etc/logrotate.d/dxf-analyzer
```

### Métricas
- Tiempo de análisis por archivo
- Tipos de errores más frecuentes
- Tamaño promedio de archivos
- Tasa de éxito del análisis

## Seguridad

### Configuración de CORS
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://tu-dominio.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Límites de Archivos
```python
# Configurar límites
MAX_FILE_SIZE_MB = 50.0
ALLOWED_EXTENSIONS = {"dxf"}
```

### Autenticación (Opcional)
```python
# Agregar autenticación básica
from fastapi.security import HTTPBasic, HTTPBasicCredentials

security = HTTPBasic()

@app.post("/api/v1/analyze")
async def analyze_file(
    file: UploadFile = File(...),
    credentials: HTTPBasicCredentials = Depends(security)
):
    # Verificar credenciales
    if not verify_credentials(credentials):
        raise HTTPException(
            status_code=401,
            detail="Credenciales inválidas"
        )
```

## Mantenimiento

### Actualización
```bash
# Actualizar código
git pull origin main

# Actualizar dependencias
pip install -r requirements.txt

# Reiniciar servicio
systemctl restart dxf-analyzer
```

### Backup
```bash
# Backup de archivos
tar -czf backup-$(date +%Y%m%d).tar.gz uploads/

# Backup de configuración
cp .env backup-env-$(date +%Y%m%d)
```

### Limpieza
```bash
# Limpiar archivos temporales
find uploads/ -type f -mtime +7 -delete

# Limpiar logs antiguos
find logs/ -type f -mtime +30 -delete
```

## Solución de Problemas

### Logs de Error
```bash
# Ver errores
grep ERROR logs/app.log

# Ver advertencias
grep WARNING logs/app.log
```

### Diagnóstico
```bash
# Verificar estado del servicio
systemctl status dxf-analyzer

# Verificar puertos
netstat -tulpn | grep 8000

# Verificar espacio en disco
df -h
```

### Recuperación
```bash
# Reiniciar servicio
systemctl restart dxf-analyzer

# Limpiar archivos temporales
rm -rf uploads/*

# Verificar permisos
chown -R www-data:www-data .
```

## Escalabilidad

### Balanceo de Carga
```nginx
# Configuración Nginx
upstream dxf_analyzer {
    server 127.0.0.1:8000;
    server 127.0.0.1:8001;
    server 127.0.0.1:8002;
}

server {
    listen 80;
    server_name api.tu-dominio.com;

    location / {
        proxy_pass http://dxf_analyzer;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Caché
```python
# Configurar caché
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

@app.on_event("startup")
async def startup():
    redis = aioredis.from_url("redis://localhost")
    FastAPICache.init(RedisBackend(redis), prefix="dxf-analyzer")
```

## Monitoreo en Producción

### Prometheus
```yaml
# Configuración de métricas
metrics:
  - name: analysis_duration_seconds
    type: histogram
    help: "Duración del análisis en segundos"
  - name: file_size_bytes
    type: gauge
    help: "Tamaño de archivos analizados"
```

### Grafana
```json
{
  "dashboard": {
    "title": "DXF Analyzer Metrics",
    "panels": [
      {
        "title": "Análisis por Hora",
        "type": "graph",
        "datasource": "Prometheus"
      }
    ]
  }
}
```

## Soporte

### Contacto
- Email: soporte@tu-dominio.com
- Discord: [Servidor de Soporte](https://discord.gg/tu-servidor)
- GitHub: [Issues](https://github.com/tu-usuario/dxf-analyzer-backend/issues)

### Documentación
- [API Documentation](docs/api_documentation.md)
- [Error Catalog](docs/error_catalog.md)
- [Deployment Guide](docs/deployment.md) 