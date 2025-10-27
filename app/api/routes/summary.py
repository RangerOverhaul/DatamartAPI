from fastapi import APIRouter, Depends, Query, HTTPException
from datetime import date
from typing import Dict, Optional
import logging
from app.models.responses import EmployeeSummaryResponse, ProductSummaryResponse, StoreSummaryResponse

from app.services.datamart import get_datamart_service, DatamartService
from app.dependencies import get_current_datamart


router = APIRouter(prefix = "/api/v1/sales", tags=["sales-aggregations"])

@router.get(
    "/employee-summary",
    response_model=EmployeeSummaryResponse,
    summary="Resumen de ventas por empleado (Total y Promedio)" ,
    tags=["sales-aggregations"],
    description="""
    Calcula el total y promedio de ventas por empleado.

    Parámetros:
    - `key_employee`: (Opcional) ID del empleado en formato "1|343"
      - Si se proporciona: Resumen de ese empleado específico
      - Si NO se proporciona: Resumen de TODOS los empleados

    Retorna:
    - Total de ventas (suma de todos los montos)
    - Promedio de ventas por transacción
    - Cantidad total vendida
    - Número total de registros

    Casos de uso:
    - Evaluación de desempeño individual
    - Identificación de top performers
    - Análisis de productividad del equipo
    - Comparación entre empleados
    - KPIs de ventas

    Ejemplos de uso:
```
    # Resumen de un empleado específico
    GET /api/v1/sales/employee-summary?key_employee=1|343

    # Resumen de todos los empleados (sin parámetro)
    GET /api/v1/sales/employee-summary
```
    """,
    response_description="Resumen de ventas del empleado o todos los empleados"
)
async def get_employee_summary(
        key_employee: Optional[str] = Query(
            None,
            description="ID del empleado (formato: '1|343'). Dejar vacío para resumen de todos",
            example="1|343"
        ),
        datamart_service: DatamartService = Depends(get_datamart_service)
) -> EmployeeSummaryResponse:
    """
    Endpoint para obtener resumen de ventas (total y promedio) por empleado.

    Si key_employee es None, retorna el resumen de todos los empleados.
    Si key_employee tiene valor, retorna solo el resumen de ese empleado.
    """
    try:
        # Consultar resumen
        result = datamart_service.get_employee_summary(
            key_employee=key_employee
        )

        return result

    except Exception as e:
        logging.error(f"Error inesperado: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Error al calcular resumen de ventas"
        )


@router.get(
    "/product-summary",
    response_model=ProductSummaryResponse,
    tags=["sales-aggregations"],
    summary="Resumen de ventas por producto (Total y Promedio)",
    description="""
    Calcula el total y promedio de ventas por producto.

    Parámetros:
    - `key_product`: (Opcional) ID del producto en formato "1|44733"
      - Si se proporciona: Resumen de ese producto específico
      - Si NO se proporciona: Resumen de TODOS los productos

    Retorna:
    - Total de ventas (suma de todos los montos)
    - Promedio de ventas por transacción
    - Cantidad total vendida
    - Número total de registros

    Casos de uso:
    - Identificar productos más vendidos
    - Análisis de rendimiento de productos
    - Planificación de inventario
    - Evaluación de rentabilidad por producto
    - KPIs de productos
    - Tendencias de consumo

    Ejemplos de uso:
```
    # Resumen de un producto específico
    GET /api/v1/sales/product-summary?key_product=1|44733

    # Resumen de todos los productos (sin parámetro)
    GET /api/v1/sales/product-summary
```
    """,
    response_description="Resumen de ventas del producto o todos los productos"
)
async def get_product_summary(
        key_product: Optional[str] = Query(
            None,
            description="ID del producto (formato: '1|44733'). Dejar vacío para resumen de todos",
            example="1|44733"
        ),
        datamart_service: DatamartService = Depends(get_datamart_service)
) -> ProductSummaryResponse:
    """
    Endpoint para obtener resumen de ventas (total y promedio) por producto.

    Si key_product es None, retorna el resumen de todos los productos.
    Si key_product tiene valor, retorna solo el resumen de ese producto.
    """
    try:
        # Consultar resumen
        result = datamart_service.get_product_summary(
            key_product=key_product
        )

        return result

    except Exception as e:
        logging.error(f"Error inesperado: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Error al calcular resumen de ventas"
        )


@router.get(
    "/store-summary",
    response_model=StoreSummaryResponse,
    summary="Resumen de ventas por tienda (Total y Promedio)",
    tags=["sales-aggregations"],
    description="""
    Calcula el total y promedio de ventas por tienda.

    **Parámetros:**
    - `key_store`: (Opcional) ID de la tienda en formato "1|023"
      - Si se proporciona: Resumen de esa tienda específica
      - Si NO se proporciona: Resumen de TODAS las tiendas

    **Retorna:**
    - Total de ventas (suma de todos los montos)
    - Promedio de ventas por transacción
    - Cantidad total vendida
    - Número total de registros

    **Casos de uso:**
    - Comparación entre sucursales
    - Evaluación de desempeño por ubicación
    - Análisis geográfico de ventas
    - Identificación de tiendas top performers
    - KPIs por punto de venta
    - Planificación de expansión

    **Ejemplos de uso:**
```
    # Resumen de una tienda específica
    GET /api/v1/sales/store-summary?key_store=1|023

    # Resumen de todas las tiendas (sin parámetro)
    GET /api/v1/sales/store-summary
```
    """,
    response_description="Resumen de ventas de la tienda o todas las tiendas"
)
async def get_store_summary(
        key_store: Optional[str] = Query(
            None,
            description="ID de la tienda (formato: '1|023'). Dejar vacío para resumen de todas",
            example="1|023"
        ),
        datamart_service: DatamartService = Depends(get_datamart_service)
) -> StoreSummaryResponse:
    """
    Endpoint para obtener resumen de ventas (total y promedio) por tienda.

    Si key_store es None, retorna el resumen de todas las tiendas.
    Si key_store tiene valor, retorna solo el resumen de esa tienda.
    """
    try:
        # Consultar resumen
        result = datamart_service.get_store_summary(
            key_store=key_store
        )

        return result

    except Exception as e:
        logging.error(f"Error inesperado: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Error al calcular resumen de ventas"
        )