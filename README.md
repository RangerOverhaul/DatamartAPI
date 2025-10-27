# DatamartAPI
API developed in Python using Parquet files as data resources for review, FastApi Framework, unit testing, and CI/CD integration.

# 🚀 Sales Datamart API

API RESTful para consulta y análisis de datos de ventas, desarrollada con FastAPI y diseñada para procesar grandes volúmenes de datos desde archivos Parquet.

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/Tests-Passing-success.svg)](tests/)
[![Coverage](https://img.shields.io/badge/Coverage-95%25-brightgreen.svg)](htmlcov/)

---

## 📋 Tabla de Contenidos

- [Descripción](#-descripción)
- [Características](#-características)
- [Tecnologías](#-tecnologías)
- [Arquitectura](#-arquitectura)
- [Requisitos Previos](#-requisitos-previos)
- [Instalación](#-instalación)
  - [Instalación Local](#instalación-local)
  - [Instalación con Docker](#instalación-con-docker)
- [Configuración](#-configuración)
- [Uso](#-uso)
- [Endpoints Disponibles](#-endpoints-disponibles)
- [Testing](#-testing)
- [Docker](#-docker)
- [CI/CD](#-cicd)
- [Deployment](#-deployment)
- [Autor](#-autor)

---

## 📖 Descripción

**Sales Datamart API** es un microservicio diseñado para proporcionar acceso eficiente y seguro a datos analíticos de ventas almacenados en formato Parquet. La API permite realizar consultas complejas, agregaciones y análisis de datos de ventas por diferentes dimensiones (empleados, productos, tiendas).

### Casos de Uso

- 📊 **Análisis de Desempeño**: Evaluar ventas por empleado, producto o tienda
- 📈 **Reportes Ejecutivos**: Generar métricas de totales y promedios
- 🔍 **Análisis Temporal**: Consultar ventas en periodos específicos
- 📉 **Identificación de Tendencias**: Detectar patrones de venta
- 🏆 **KPIs**: Calcular indicadores clave de rendimiento

---

## ✨ Características

### Funcionalidades Principales

- ✅ **Consultas por Periodo**
  - Ventas por empleado en rango de fechas
  - Ventas por producto en rango de fechas
  - Ventas por tienda en rango de fechas

- ✅ **Agregaciones y Estadísticas**
  - Total y promedio de ventas por empleado
  - Total y promedio de ventas por producto
  - Total y promedio de ventas por tienda

### Características Técnicas

- 🚀 **Alto Rendimiento**: Procesamiento eficiente de grandes volúmenes de datos
- 📊 **Datos en Parquet**: Lectura optimizada de archivos columnares
- 🔐 **Seguridad**: Autenticación JWT (preparado para implementación)
- ✅ **Validación**: Validación automática de parámetros con Pydantic
- 📝 **Documentación**: Swagger UI y ReDoc integrados
- 🐳 **Dockerizado**: Fácil despliegue con Docker y Docker Compose
- 🧪 **Testing**: Cobertura >95% con tests unitarios
- 🔄 **CI/CD**: Pipeline automatizado con GitHub Actions
- 📈 **Logging**: Sistema robusto de logs para debugging
- 🏥 **Health Checks**: Endpoints de monitoreo

---

## 🛠 Tecnologías

### Backend

- **[FastAPI](https://fastapi.tiangolo.com/)** 0.104+ - Framework web moderno y rápido
- **[Python](https://www.python.org/)** 3.11+ - Lenguaje de programación
- **[Pydantic](https://docs.pydantic.dev/)** 2.5+ - Validación de datos
- **[Pandas](https://pandas.pydata.org/)** 2.1+ - Procesamiento de datos
- **[PyArrow](https://arrow.apache.org/docs/python/)** 14.0+ - Lectura de archivos Parquet
- **[Uvicorn](https://www.uvicorn.org/)** - Servidor ASGI

### Testing

- **[Pytest](https://docs.pytest.org/)** 7.4+ - Framework de testing
- **[Pytest-cov](https://pytest-cov.readthedocs.io/)** - Cobertura de código
- **[Pytest-asyncio](https://pytest-asyncio.readthedocs.io/)** - Tests asíncronos
- **[Pytest-mock](https://pytest-mock.readthedocs.io/)** - Mocking

### DevOps

- **[Docker](https://www.docker.com/)** - Containerización
- **[Docker Compose](https://docs.docker.com/compose/)** - Orquestación de contenedores
- **[GitHub Actions](https://github.com/features/actions)** - CI/CD

### Code Quality

- **[Black](https://black.readthedocs.io/)** - Formateo de código
- **[Flake8](https://flake8.pycqa.org/)** - Linting
- **[isort](https://pycqa.github.io/isort/)** - Ordenamiento de imports
- **[Bandit](https://bandit.readthedocs.io/)** - Análisis de seguridad

---

## 🏗 Arquitectura

### Arquitectura de Alto Nivel
```
┌─────────────────┐
│   Cliente/UI    │
└────────┬────────┘
         │ HTTP/REST
         ▼
┌─────────────────────────────────────┐
│         FastAPI Application         │
│  ┌─────────────────────────────┐   │
│  │      API Routes Layer       │   │
│  └──────────┬──────────────────┘   │
│             │                       │
│  ┌──────────▼──────────────────┐   │
│  │   Business Logic Layer      │   │
│  │  (DatamartService)          │   │
│  └──────────┬──────────────────┘   │
│             │                       │
│  ┌──────────▼──────────────────┐   │
│  │    Data Access Layer        │   │
│  │    (Pandas + PyArrow)       │   │
│  └──────────┬──────────────────┘   │
└─────────────┼───────────────────────┘
              │
              ▼
      ┌───────────────┐
      │  Parquet Files│
      │   (Datamart)  │
      └───────────────┘
```

### Estructura de Capas

1. **API Layer** (`app/api/routes/`)
   - Manejo de requests/responses
   - Validación de parámetros
   - Documentación de endpoints

2. **Business Logic Layer** (`app/services/`)
   - Lógica de negocio
   - Cálculos y agregaciones
   - Transformación de datos

3. **Data Access Layer** (`app/services/datamart.py`)
   - Lectura de archivos Parquet
   - Filtrado y consultas
   - Optimización de queries

4. **Models Layer** (`app/models/`)
   - Modelos Pydantic
   - Validación de datos
   - Serialización

---

## 📋 Requisitos Previos

### Opción 1: Instalación Local

- Python 3.11 o superior
- pip (gestor de paquetes de Python)
- Archivos .parquet del datamart

### Opción 2: Instalación con Docker

- Docker 20.10 o superior
- Docker Compose 2.0 o superior
- Archivos .parquet del datamart

---

## 🚀 Instalación

### Instalación Local

#### 1. Clonar el repositorio
```bash
git clone https://github.com/tu-usuario/sales-datamart-api.git
cd sales-datamart-api
```

#### 2. Crear entorno virtual
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

#### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

#### 4. Configurar variables de entorno
```bash
# Copiar archivo de ejemplo
cp .env.example .env

# Editar .env con tus valores
# En Windows: notepad .env
# En Linux/Mac: nano .env
```

#### 5. Preparar el datamart
```bash
# Crear carpeta para archivos parquet
mkdir datamart

# Copiar tus archivos .parquet a la carpeta datamart/
# Los archivos deben tener la estructura esperada
```

#### 6. Iniciar la aplicación
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### 7. Verificar instalación
```bash
# Abrir navegador en:
# http://localhost:8000/docs
# O verificar con curl:
curl http://localhost:8000/health
```

---

### Instalación con Docker

#### 1. Clonar el repositorio
```bash
git clone https://github.com/tu-usuario/sales-datamart-api.git
cd sales-datamart-api
```

#### 2. Preparar el datamart
```bash
# Crear carpeta y copiar archivos .parquet
mkdir datamart
# Copiar tus archivos .parquet a datamart/
```

#### 3. Configurar variables de entorno
```bash
cp .env.example .env
# Editar .env si es necesario
```

#### 4. Iniciar con Docker Compose
```bash
# Usando script (recomendado)
chmod +x scripts/*.sh
./scripts/start.sh

# O manualmente
docker-compose up -d
```

#### 5. Verificar instalación
```bash
# Ver logs
docker-compose logs -f api

# Verificar health
curl http://localhost:8000/health

# Abrir documentación
# http://localhost:8000/docs
```

---

## ⚙ Configuración

### Variables de Entorno

El archivo `.env` debe contener las siguientes variables:
```bash
# Ruta al directorio con archivos .parquet
# Local: ./datamart
# Docker: /datamart (no cambiar)
DATAMART_PATH=./datamart

# Modo debug (True/False)
DEBUG=False

# Nivel de logging (DEBUG, INFO, WARNING, ERROR)
LOG_LEVEL=INFO

# Seguridad JWT (para implementación futura)
SECRET_KEY=tu-secret-key-super-segura-cambiar
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS (orígenes permitidos, separados por coma)
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000
```

### Generar SECRET_KEY segura
```bash
# Linux/Mac
openssl rand -hex 32

# Python
python -c "import secrets; print(secrets.token_hex(32))"
```

---

## 📚 Uso

### Acceder a la Documentación

Una vez iniciada la aplicación, puedes acceder a:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/api/v1/openapi.json

### Ejemplo de Uso con cURL

#### 1. Health Check
```bash
curl http://localhost:8000/health
```

**Respuesta:**
```json
{
  "status": "healthy",
  "service": "Sales Datamart API",
  "version": "1.0.0",
  "datamart_loaded": true,
  "records_count": 323326
}
```

#### 2. Consultar ventas por empleado
```bash
curl "http://localhost:8000/api/v1/sales/by-employee?key_employee=1%7C343&date_start=2023-11-01&date_end=2023-11-30"
```

**Respuesta:**
```json
{
  "success": true,
  "key_employee": "1|343",
  "date_start": "2023-11-01",
  "date_end": "2023-11-30",
  "total_amount": -24873.95,
  "total_quantity": -4,
  "records_count": 1,
  "sales": [
    {
      "date": "2023-11-02",
      "amount": -24873.95,
      "quantity": -4,
      "ticket_id": "N01-00000385",
      "product": "1|44733",
      "store": "1|023"
    }
  ]
}
```

### Ejemplo de Uso con Python
```python
import requests

# Base URL
BASE_URL = "http://localhost:8000"

# 1. Health check
health = requests.get(f"{BASE_URL}/health")
print(health.json())

# 2. Consultar ventas por empleado
response = requests.get(
    f"{BASE_URL}/api/v1/sales/by-employee",
    params={
        "key_employee": "1|343",
        "date_start": "2023-11-01",
        "date_end": "2023-11-30"
    }
)
data = response.json()
print(f"Total ventas: ${data['total_amount']:,.2f}")
print(f"Registros: {data['records_count']}")

# 3. Resumen de todos los empleados
summary = requests.get(f"{BASE_URL}/api/v1/sales/employee-summary")
print(summary.json())
```

### Ejemplo de Uso con JavaScript/Fetch
```javascript
// Base URL
const BASE_URL = 'http://localhost:8000';

// Consultar ventas por producto
async function getSalesByProduct() {
  const response = await fetch(
    `${BASE_URL}/api/v1/sales/by-product?` +
    `key_product=1|44733&` +
    `date_start=2023-11-01&` +
    `date_end=2023-11-30`
  );
  
  const data = await response.json();
  console.log('Total ventas:', data.total_amount);
  console.log('Cantidad:', data.total_quantity);
}

getSalesByProduct();
```

---

## 🔌 Endpoints Disponibles

### 🏥 Health & Status

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/` | Información básica del API |
| GET | `/health` | Estado del servicio y datamart |

### 📅 Consultas por Periodo

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/v1/sales/by-employee` | Ventas por empleado en periodo |
| GET | `/api/v1/sales/by-product` | Ventas por producto en periodo |
| GET | `/api/v1/sales/by-store` | Ventas por tienda en periodo |

**Parámetros comunes:**
- `key_employee/key_product/key_store`: ID de la entidad (formato: "1|343")
- `date_start`: Fecha inicio (formato: YYYY-MM-DD)
- `date_end`: Fecha fin (formato: YYYY-MM-DD)

### 📊 Agregaciones y Resúmenes

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/v1/sales/employee-summary` | Total y promedio por empleado |
| GET | `/api/v1/sales/product-summary` | Total y promedio por producto |
| GET | `/api/v1/sales/store-summary` | Total y promedio por tienda |

**Parámetros opcionales:**
- `key_employee/key_product/key_store`: ID de la entidad (opcional)
  - Si se proporciona: resumen de esa entidad específica
  - Si NO se proporciona: resumen de todas las entidades

### 📖 Documentación

| Endpoint | Descripción |
|----------|-------------|
| `/docs` | Documentación Swagger UI (interactiva) |
| `/redoc` | Documentación ReDoc (alternativa) |
| `/api/v1/openapi.json` | Esquema OpenAPI en JSON |

---

## 🧪 Testing

### Ejecutar Tests Localmente
```bash
# Todos los tests
pytest

# Solo unit tests
pytest tests/unit/ -v

# Con cobertura
pytest tests/unit/ --cov=app --cov-report=html --cov-report=term-missing

# Tests específicos
pytest tests/unit/test_datamart_service.py -v

# Tests con marca específica
pytest -m unit -v

# Ver reporte de cobertura HTML
# Abrir: htmlcov/index.html
```

### Ejecutar Tests en Docker
```bash
# Usando script
./scripts/test.sh

# Manualmente
docker-compose run --rm api pytest tests/unit/ -v --cov=app
```

### Estructura de Tests
```
tests/
├── conftest.py              # Fixtures compartidas
├── unit/                    # Tests unitarios (95% cobertura)
│   ├── test_config.py
│   ├── test_datamart_service.py
│   ├── test_datamart_service_product.py
│   ├── test_datamart_service_summary.py
│   ├── test_datamart_service_product_summary.py
│   ├── test_datamart_service_store_summary.py
│   ├── test_sales_endpoint.py
│   ├── test_sales_endpoint_product.py
│   ├── test_sales_endpoint_summary.py
│   ├── test_sales_endpoint_product_summary.py
│   └── test_sales_endpoint_store_summary.py
└── fixtures/
    └── sample_datamart.parquet
```

### Métricas de Cobertura

- **Cobertura Total**: >95%
- **Cobertura por Módulo**:
  - `app/config.py`: 92%
  - `app/services/datamart.py`: 96%
  - `app/api/routes/sales.py`: 94%
  - `app/models/responses.py`: 100%

---

## 🐳 Docker

### Comandos Principales

#### Iniciar la Aplicación
```bash
# Producción
./scripts/start.sh
# O manualmente:
docker-compose up -d

# Desarrollo (con hot-reload)
./scripts/start-dev.sh
# O manualmente:
docker-compose -f docker-compose.dev.yml up
```

#### Ver Logs
```bash
# Ver logs en tiempo real
docker-compose logs -f api

# Ver últimas 100 líneas
docker-compose logs --tail=100 api

# Ver logs de un periodo específico
docker-compose logs --since 1h api
```

#### Detener la Aplicación
```bash
# Detener contenedores
./scripts/stop.sh
# O manualmente:
docker-compose down

# Detener y eliminar volúmenes
docker-compose down -v
```

#### Reconstruir la Imagen
```bash
# Reconstruir sin cache
docker-compose build --no-cache

# Reconstruir y reiniciar
docker-compose up -d --build
```

#### Ejecutar Tests en Docker
```bash
./scripts/test.sh
```

#### Acceder al Contenedor
```bash
# Bash interactivo
docker-compose exec api bash

# Ejecutar comando específico
docker-compose exec api python -c "from app.main import app; print('OK')"
```

#### Ver Estado de Contenedores
```bash
# Listar contenedores
docker-compose ps

# Ver uso de recursos
docker stats

# Inspeccionar contenedor
docker inspect sales-datamart-api
```

#### Limpiar Todo (Cuidado!)
```bash
# Detener y eliminar todo
docker-compose down -v --rmi all

# Limpiar sistema Docker completo
docker system prune -a --volumes
```

### Estructura de Volúmenes
```
Proyecto/
├── datamart/          # → Montado en /datamart (read-only)
├── logs/             # → Montado en /app/logs
└── app/              # → Código de la aplicación
```

### Variables de Entorno en Docker

En Docker, las variables de entorno se configuran en `docker-compose.yml`:
```yaml
environment:
  - DATAMART_PATH=/datamart  # Siempre /datamart en Docker
  - DEBUG=False
  - LOG_LEVEL=INFO
```

### Troubleshooting Docker

#### La API no encuentra los archivos .parquet
```bash
# Verificar que la carpeta existe
ls -la datamart/

# Verificar montaje del volumen
docker-compose exec api ls -la /datamart/

# Verificar permisos
chmod -R 755 datamart/
```

#### Error de permisos
```bash
# Dar permisos correctos
chmod -R 755 datamart/
chown -R $USER:$USER datamart/

# Reconstruir imagen
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

#### Puerto 8000 ya está en uso
```bash
# Ver qué proceso usa el puerto
lsof -i :8000

# Cambiar puerto en docker-compose.yml
ports:
  - "8001:8000"  # Cambiar 8000 a 8001
```

#### Reiniciar completamente
```bash
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d
docker-compose logs -f api
```

---

## 🔄 CI/CD

### Pipeline de GitHub Actions

El proyecto incluye un pipeline completo de CI/CD que se ejecuta automáticamente en cada push o pull request.

### Workflow Principal

**Archivo**: `.github/workflows/ci-cd.yml`

#### Jobs del Pipeline

1. **🔍 Lint & Code Quality**
   - Black (formateo)
   - Flake8 (linting)
   - isort (imports)
   - Bandit (seguridad)
   - Safety (vulnerabilidades)

2. **🧪 Unit Tests**
   - Ejecución de pytest
   - Cobertura de código (>80%)
   - Upload a Codecov
   - Generación de reportes

3. **🐳 Build Docker Image**
   - Build de imagen Docker
   - Test de imagen
   - Cache de capas

4. **🔒 Security Scan**
   - Trivy vulnerability scanner
   - Upload a GitHub Security

5. **🚀 Deploy to Staging** (branch: develop)
   - Build y push a Docker Hub
   - Deploy automático a staging

6. **🚀 Deploy to Production** (branch: main)
   - Build y push a Docker Hub
   - Deploy automático a producción

### Flujo de Trabajo
```
┌──────────────┐
│  git push    │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Lint & Test  │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Build Docker │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│Security Scan │
└──────┬───────┘
       │
       ├─────────────────┐
       │                 │
       ▼                 ▼
┌──────────────┐  ┌──────────────┐
│   Staging    │  │  Production  │
│  (develop)   │  │    (main)    │
└──────────────┘  └──────────────┘
```

### Configurar GitHub Actions

#### 1. Secrets Necesarios

Ve a: **Settings → Secrets and variables → Actions**

Agregar los siguientes secrets:

| Secret | Descripción | Ejemplo |
|--------|-------------|---------|
| `DOCKER_USERNAME` | Usuario de Docker Hub | `danilo-herazo` |
| `DOCKER_PASSWORD` | Password/Token de Docker Hub | `dckr_pat_xxx` |
| `STAGING_SERVER_HOST` | IP del servidor staging | `192.168.1.100` |
| `STAGING_SERVER_SSH_KEY` | SSH private key staging | `-----BEGIN RSA PRIVATE KEY-----` |
| `PROD_SERVER_HOST` | IP del servidor producción | `192.168.1.200` |
| `PROD_SERVER_SSH_KEY` | SSH private key producción | `-----BEGIN RSA PRIVATE KEY-----` |

#### 2. Crear Token de Docker Hub
```bash
# 1. Ir a: https://hub.docker.com/settings/security
# 2. Click en "New Access Token"
# 3. Nombre: "GitHub Actions"
# 4. Permisos: Read, Write, Delete
# 5. Copiar el token generado
```

#### 3. Configurar SSH Keys
```bash
# Generar par de claves SSH
ssh-keygen -t rsa -b 4096 -C "deploy@sales-api"

# Copiar clave pública al servidor
ssh-copy-id user@server-ip

# Copiar clave privada a GitHub Secrets
cat ~/.ssh/id_rsa
# Pegar contenido completo en GitHub Secret
```

### Monitoreo del Pipeline

#### Ver estado del pipeline
```bash
# En la interfaz de GitHub:
# Repository → Actions → Ver workflows

# O con GitHub CLI:
gh run list
gh run view <run-id>
gh run watch
```

#### Badges de Estado

Agregar al README.md:
```markdown
![CI/CD](https://github.com/tu-usuario/sales-datamart-api/workflows/CI%2FCD%20Pipeline/badge.svg)
![Tests](https://github.com/tu-usuario/sales-datamart-api/workflows/Test%20Pull%20Request/badge.svg)
```

---

## 🚀 Deployment

### Ambientes

#### 1. Development (Local)
```bash
# Desarrollo local sin Docker
uvicorn app.main:app --reload

# Desarrollo local con Docker
docker-compose -f docker-compose.dev.yml up
```

- **URL**: http://localhost:8000
- **Debug**: Activado
- **Hot-reload**: Sí
- **Logs**: Verbose

#### 2. Staging (Automático)

- **Branch**: `develop`
- **URL**: https://staging-api.example.com
- **Deploy**: Automático via GitHub Actions
- **Propósito**: Testing antes de producción

#### 3. Production (Automático)

- **Branch**: `main`
- **URL**: https://api.example.com
- **Deploy**: Automático via GitHub Actions
- **Propósito**: Ambiente de producción

### Workflow de Deployment
```
1. Desarrollo Local
   ↓
2. Commit y Push a branch feature/xxx
   ↓
3. Pull Request a develop
   ↓
4. Review y Tests Automáticos
   ↓
5. Merge a develop
   ↓
6. Deploy Automático a Staging
   ↓
7. Testing Manual en Staging
   ↓
8. Pull Request de develop a main
   ↓
9. Review Final
   ↓
10. Merge a main
    ↓
11. Deploy Automático a Production
```

### Deploy Manual

#### A Staging
```bash
# 1. Build local
docker build -t sales-datamart-api:staging .

# 2. Tag para registry
docker tag sales-datamart-api:staging username/sales-datamart-api:staging

# 3. Push
docker push username/sales-datamart-api:staging

# 4. Deploy en servidor
ssh user@staging-server
docker pull username/sales-datamart-api:staging
cd /opt/sales-api
docker-compose down
docker-compose up -d
```

#### A Production
```bash
# Similar a staging pero con tag 'latest'
docker build -t sales-datamart-api:latest .
docker tag sales-datamart-api:latest username/sales-datamart-api:latest
docker push username/sales-datamart-api:latest

# Deploy en servidor de producción
ssh user@prod-server
docker pull username/sales-datamart-api:latest
cd /opt/sales-api
docker-compose down
docker-compose up -d
```

### Rollback

En caso de problemas en producción:
```bash
# 1. Conectar al servidor
ssh user@prod-server

# 2. Ver tags disponibles
docker images username/sales-datamart-api

# 3. Detener contenedor actual
docker-compose down

# 4. Cambiar a versión anterior
docker pull username/sales-datamart-api:previous-sha

# 5. Actualizar docker-compose.yml con tag anterior
vim docker-compose.yml
# Cambiar: image: username/sales-datamart-api:previous-sha

# 6. Reiniciar
docker-compose up -d

# 7. Verificar
curl http://localhost:8000/health
```

### Monitoreo Post-Deploy
```bash
# Ver logs en tiempo real
docker-compose logs -f api

# Health check
curl https://api.example.com/health

# Métricas
docker stats

# Ver versión desplegada
curl https://api.example.com/ | jq .version
```

### Checklist de Deployment

#### Pre-Deploy

- [ ] Tests pasan localmente
- [ ] Cobertura >80%
- [ ] No hay secrets hardcodeados
- [ ] Variables de entorno configuradas
- [ ] Documentación actualizada
- [ ] CHANGELOG.md actualizado

#### Durante Deploy

- [ ] Pipeline de CI/CD pasa
- [ ] Build de Docker exitoso
- [ ] Security scan sin issues críticos
- [ ] Health check responde OK

#### Post-Deploy

- [ ] Endpoint `/health` responde correctamente
- [ ] Logs no muestran errores
- [ ] Métricas normales
- [ ] Tests de smoke pasan
- [ ] Notificación al equipo

---
## Autor
Danilo David Herazo Acevedo
Senior Python Developer

- Email: danilo.herazo@outlook.es
- GitHub: rangerOverHaul
- LinkedIn: https://www.linkedin.com/in/danilo-herazo-acevedo-0561281a9/
