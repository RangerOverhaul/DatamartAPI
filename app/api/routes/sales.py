from fastapi import APIRouter, Depends, Query, HTTPException
from datetime import date
from typing import Dict, Optional
import logging
from app.models.responses import EmployeeSalesResponse, ProductSalesResponse, StoreSalesResponse
from app.services.datamart import get_datamart_service, DatamartService
from app.dependencies import get_current_datamart
from app.services.auth_service import get_current_user

router = APIRouter(prefix = "/api/v1/sales", tags=["sales-by-period"])

@router.get("/by-employee",
    response_model=EmployeeSalesResponse,
    summary="Ventas por empleado en periodo",
    tags=["sales-by-period"],
    description="""
    Consulta las ventas realizadas por un empleado específico en un rango de fechas.
    
     **Requiere autenticación JWT**
    
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
    datamart_service: DatamartService = Depends(get_current_datamart),
    current_user: Dict = Depends(get_current_user)
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
    
     **Requiere autenticación JWT**

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
        datamart_service: DatamartService = Depends(get_current_datamart),
        current_user: Dict = Depends(get_current_user)
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
    
     **Requiere autenticación JWT**

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
    datamart_service: DatamartService = Depends(get_current_datamart),
    current_user: Dict = Depends(get_current_user)
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


