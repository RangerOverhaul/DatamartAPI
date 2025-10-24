from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging

app = FastAPI(
    title="Sales Datamart API",
    description="""
## API de Consulta de Ventas - Datamart Analytics

Esta API proporciona acceso seguro a datos analíticos de ventas con las siguientes capacidades:

###  Consultas Disponibles

#### Por Periodo
* **Ventas por Empleado** - Consultar ventas de un empleado en un rango de fechas
* **Ventas por Producto** - Analizar ventas de productos específicos
* **Ventas por Tienda** - Revisar desempeño de tiendas

#### Agregaciones y Estadísticas
* **Resumen por Tienda** - Totales y promedios de ventas
* **Resumen por Producto** - Análisis de rendimiento de productos
* **Resumen por Empleado** - Métricas de desempeño individual

###  Seguridad
- Autenticación mediante **JWT (JSON Web Tokens)**
- Todos los endpoints de consulta requieren autenticación
- Tokens con expiración configurable (30 minutos por defecto)

###  Características
- Validación automática de parámetros con Pydantic
- Manejo robusto de errores con mensajes descriptivos
- Logging detallado de operaciones
- Respuestas consistentes en formato JSON
- Filtrado por rangos de fechas
- Cálculos agregados (totales y promedios)

###  Tecnologías
- **FastAPI** - Framework web moderno y rápido
- **Pydantic** - Validación de datos
- **Python-JOSE** - Manejo de JWT
- **Pandas/DuckDB** - Procesamiento de datos del datamart
- **Pytest** - Testing y cobertura de código
- **GitHub Actions** - CI/CD automatizado

###  Uso

1. **Autenticación**: Obtener token JWT en `/api/v1/auth/login`
2. **Consultas**: Usar el token en header `Authorization: Bearer {token}`
3. **Documentación Interactiva**: Disponible en `/docs` (Swagger UI)

###  Enlaces Útiles
- [Repositorio GitHub](#)
- [Guía de Inicio Rápido](#)
- [Ejemplos de Uso](#)
    """,
    version="1.0.0",
    contact={
        "name": "Danilo Herazo Acevedo",
        "url": "https://www.getceles.com/",
        "email": "danilo.herazo@getceles.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
    docs_url="/docs",  
    redoc_url="/redoc",  
    openapi_url="/api/v1/openapi.json",  
    
    openapi_tags=[
        {
            "name": "authentication",
            "description": "**Autenticación y autorización**. Endpoints para obtener y validar tokens JWT.",
            "externalDocs": {
                "description": "Documentación de JWT",
                "url": "https://jwt.io/introduction",
            },
        },
        {
            "name": "sales-by-period",
            "description": "**Consultas por periodo**. Obtener ventas filtradas por rangos de fechas para empleados, productos o tiendas específicas.",
        },
        {
            "name": "sales-aggregations",
            "description": "**Agregaciones y estadísticas**. Calcular totales, promedios y métricas de rendimiento.",
        }
    ],
)


@app.get("/")
def root():
    return {
        "mensaje": "Bienvenido a mi API",
        "docs": "/docs",
        "endpoints": {
            "sales": "/sales",
            "auth": "/auth"
        }
    }