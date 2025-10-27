from fastapi import APIRouter, Depends, Query, HTTPException
from datetime import date
from typing import Dict
import logging

from app.models.responses import (EmployeeSalesResponse, ProductSalesResponse, StoreSalesResponse,
                                  EmployeeSummaryResponse)
from app.services.datamart import get_datamart_service, DatamartService
from app.dependencies import get_current_datamart

router = APIRouter(prefix = "/api/v1/sales")

@router.get("/by-employee",
    response_model=EmployeeSalesResponse,
    summary="Ventas por empleado en periodo",
    tags=["sales-by-period"],
    description="""
    Consulta las ventas realizadas por un empleado específico en un rango de fechas.
    
    Parámetros:
    - `key_employee`: ID del empleado en formato "1|343" (KeyEmployee del datamart)
    - `date_start`: Fecha de inicio del periodo (formato: YYYY-MM-DD)
    - `date_end`: Fecha de fin del periodo (formato: YYYY-MM-DD)
    
    Retorna:
    - Listado detallado de todas las ventas del empleado
    - Total de ventas en el periodo
    - Cantidad total vendida
    - Número de transacciones
    
    Validaciones:
    - La fecha de fin debe ser mayor o igual a la fecha de inicio
    - El formato de KeyEmployee debe coincidir con el del datamart
    
    Ejemplo de uso:
```
    GET /api/v1/sales/by-employee?key_employee=1|343&date_start=2023-11-01&date_end=2023-11-30
```
    """,
    response_description="Ventas del empleado en el periodo especificado")
async def get_sales_by_employee(
    key_employee: str = Query(
    ...,
    description="ID del empleado (formato: '1|343')",
    example="1|343"
    ),
    date_start: date = Query(
        ...,
        description="Fecha de inicio del periodo",
        example="2023-11-01"
    ),
    date_end: date = Query(
        ...,
        description="Fecha de fin del periodo",
        example="2023-11-30"
    ),
    datamart_service: DatamartService = Depends(get_current_datamart)
) -> EmployeeSalesResponse:
    try:
        # Validar rango de fechas
        if date_end < date_start:
            raise HTTPException(
                status_code=422,
                detail=f"date_end ({date_end}) debe ser mayor o igual a date_start ({date_start})"
            )

        # Consultar ventas
        result = datamart_service.get_sales_by_employee(
            key_employee=key_employee,
            date_start=date_start,
            date_end=date_end
        )

        return result

    except ValueError as e:
        logging.error(str(e))
        raise HTTPException(status_code=422, detail=f"Error al obtener datos del empleado: {str(e)}")
    except Exception as e:
        logging.error(str(e))
        raise HTTPException(
            status_code=500,
            detail="Error al consultar ventas"
        )

@router.get(
    "/by-product",
    response_model=ProductSalesResponse,
    summary="Ventas por producto en periodo",
    tags=["sales-by-period"],
    description="""
    Consulta las ventas de un producto específico en un rango de fechas.

    Parámetros:
    - `key_product`: ID del producto en formato "1|44733" (KeyProduct del datamart)
    - `date_start`: Fecha de inicio del periodo (formato: YYYY-MM-DD)
    - `date_end`: Fecha de fin del periodo (formato: YYYY-MM-DD)

    Retorna:
    - Listado detallado de todas las ventas del producto
    - Total de ventas en el periodo
    - Cantidad total vendida
    - Número de transacciones

    Validaciones:
    - La fecha de fin debe ser mayor o igual a la fecha de inicio
    - El formato de KeyProduct debe coincidir con el del datamart

    Casos de uso:
    - Analizar rendimiento de productos específicos
    - Identificar tendencias de venta
    - Planificación de inventario
    - Evaluación de productos más vendidos

    Ejemplo de uso:
```
    GET /api/v1/sales/by-product?key_product=1|44733&date_start=2023-11-01&date_end=2023-11-30
```
    """,
    response_description="Ventas del producto en el periodo especificado",
)
async def get_sales_by_product(
        key_product: str = Query(
            ...,
            description="ID del producto (formato: '1|44733')",
            example="1|44733",
            min_length=1
        ),
        date_start: date = Query(
            ...,
            description="Fecha de inicio del periodo",
            example="2023-11-01"
        ),
        date_end: date = Query(
            ...,
            description="Fecha de fin del periodo",
            example="2023-11-30"
        ),
        datamart_service: DatamartService = Depends(get_current_datamart)
) -> ProductSalesResponse:
    """
    Endpoint para obtener ventas de un producto en un periodo.
    """
    try:
        # Validar rango de fechas
        if date_end < date_start:
            raise HTTPException(
                status_code=422,
                detail=f"date_end ({date_end}) debe ser mayor o igual a date_start ({date_start})"
            )

        # Consultar ventas
        result = datamart_service.get_sales_by_product(
            key_product=key_product,
            date_start=date_start,
            date_end=date_end
        )

        return result

    except ValueError as e:
        logging.error(f"Error de validación: {str(e)}")
        raise HTTPException(
            status_code=422,
            detail=f"Error de validación: {str(e)}"
        )
    except Exception as e:
        logging.error(f"Error inesperado: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Error al consultar ventas"
        )

@router.get(
    "/by-store",
    response_model=StoreSalesResponse,
    summary="Ventas por tienda en periodo",
    tags=["sales-by-period"],
    description="""
    Consulta las ventas de una tienda específica en un rango de fechas.

    Parámetros:
    - `key_store`: ID de la tienda en formato "1|023" (KeyStore del datamart)
    - `date_start`: Fecha de inicio del periodo (formato: YYYY-MM-DD)
    - `date_end`: Fecha de fin del periodo (formato: YYYY-MM-DD)
    
    Retorna:
    - Listado detallado de todas las ventas de la tienda
    - Total de ventas en el periodo
    - Cantidad total vendida
    - Número de transacciones

    Validaciones:
    - La fecha de fin debe ser mayor o igual a la fecha de inicio
    - El formato de KeyStore debe coincidir con el del datamart

    Casos de uso:
    - Analizar rendimiento de tiendas específicas
    - Comparar desempeño entre sucursales
    - Identificar tendencias geográficas
    - Planificación de recursos por tienda

    Ejemplo de uso:
    GET /api/v1/sales/by-store?key_store=1|023&date_start=2023-11-01&date_end=2023-11-30
        """,
    response_description="Ventas de la tienda en el periodo especificado",
)
async def get_sales_by_store(
    key_store: str = Query(
        ...,
        description="ID de la tienda (formato: '1|023')",
        example="1|023",
        min_length=1
    ),
    date_start: date = Query(
        ...,
        description="Fecha de inicio del periodo",
        example="2023-11-01"
    ),
    date_end: date = Query(
        ...,
        description="Fecha de fin del periodo",
        example="2023-11-30"
    ),
    datamart_service: DatamartService = Depends(get_current_datamart)
) -> StoreSalesResponse:
    """
    Endpoint para obtener ventas de una tienda en un periodo.
    """
    try:
        # Validar rango de fechas
        if date_end < date_start:
            raise HTTPException(
                status_code=422,
                detail=f"date_end ({date_end}) debe ser mayor o igual a date_start ({date_start})"
            )

        # Consultar ventas
        result = datamart_service.get_sales_by_store(
            key_store=key_store,
            date_start=date_start,
            date_end=date_end
        )
        return result

    except ValueError as e:
        logging.error(f"Error de validación: {str(e)}")
        raise HTTPException(
            status_code=422,
            detail=f"Error de validación: {str(e)}"
        )
    except Exception as e:
        logging.error(f"Error inesperado: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Error al consultar ventas por tienda"
        )


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
    response_description="Resumen de ventas del empleado o todos los empleados",
    responses={
        200: {
            "description": "Consulta exitosa",
            "content": {
                "application/json": {
                    "examples": {
                        "specific_employee": {
                            "summary": "Resumen de empleado específico",
                            "value": {
                                "success": True,
                                "key_employee": "1|343",
                                "total_amount": 150000.50,
                                "average_amount": 6000.02,
                                "total_quantity": 1000,
                                "records_count": 25
                            }
                        },
                        "all_employees": {
                            "summary": "Resumen de todos los empleados",
                            "value": {
                                "success": True,
                                "key_employee": None,
                                "total_amount": 5000000.00,
                                "average_amount": 15000.50,
                                "total_quantity": 50000,
                                "records_count": 333
                            }
                        }
                    }
                }
            }
        },
        500: {
            "description": "Error interno del servidor"
        }
    }
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
        logger.error(f"Error inesperado: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Error al calcular resumen de ventas"
        )

@router.get("/product-summary")
async def get_sales_product_summary(key_product: str = None):
    # TODO: Implement the logic to get sales product summary
    pass

@router.get("/employee-summary")
async def get_sales_employee_summary(key_employee: str = None):
    # TODO: Implement the logic to get sales employee summary
    pass
