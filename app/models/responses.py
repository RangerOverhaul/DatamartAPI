from pydantic import BaseModel, Field
from datetime import date
from typing import List, Optional
from app.models.schemas import SaleRecord

class EmployeeSalesResponse(BaseModel):
    """Modelo para la respuesta de ventas por empleado"""
    key_employee: str = Field(..., description="ID del empleado")
    date_start: date = Field(..., description="Fecha de inicio del periodo")
    date_end: date = Field(..., description="Fecha de fin del periodo")
    total_amount: float = Field(..., description="Monto total de ventas")
    total_quantity: int = Field(..., description="Cantidad total vendida")
    records_count: int = Field(..., description="Número total de registros")
    sales: List[SaleRecord] = Field(..., description="Lista de ventas detalladas")

    class Config:
        json_encoders = {
            date: lambda v: v.isoformat()
        }

class ProductSalesResponse(BaseModel):
    """Modelo para la respuesta de ventas por producto"""
    success: bool = Field(default=True, description="Indica si la operación fue exitosa")
    key_product: str = Field(..., description="ID del producto")
    date_start: date = Field(..., description="Fecha de inicio del periodo")
    date_end: date = Field(..., description="Fecha de fin del periodo")
    total_amount: float = Field(..., description="Monto total de ventas")
    total_quantity: int = Field(..., description="Cantidad total vendida")
    records_count: int = Field(..., description="Número total de registros")
    sales: List[SaleRecord] = Field(..., description="Lista de ventas detalladas")

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "key_product": "1|44733",
                "date_start": "2023-11-01",
                "date_end": "2023-11-30",
                "total_amount": 24873.95,
                "total_quantity": 150,
                "records_count": 25,
                "sales": [
                    {
                        "date": "2023-11-02",
                        "amount": 1500.50,
                        "quantity": 10,
                        "ticket_id": "N01-00000385",
                        "product": "1|44733",
                        "store": "1|023"
                    }
                ]
            }
        }


class StoreSalesResponse(BaseModel):
    """Modelo para la respuesta de ventas por tienda"""
    key_store: str = Field(..., description="ID de la tienda")
    date_start: date = Field(..., description="Fecha de inicio del periodo")
    date_end: date = Field(..., description="Fecha de fin del periodo")
    total_amount: float = Field(..., description="Monto total de ventas")
    total_quantity: int = Field(..., description="Cantidad total vendida")
    records_count: int = Field(..., description="Número total de registros")
    sales: List[SaleRecord] = Field(..., description="Lista de ventas detalladas")

    class Config:
        json_schema_extra = {
            "example": {
                "key_store": "1|023",
                "date_start": "2023-11-01",
                "date_end": "2023-11-30",
                "total_amount": 24873.95,
                "total_quantity": 150,
                "records_count": 25,
                "sales": [
                    {
                        "date": "2023-11-02",
                        "amount": 1500.50,
                        "quantity": 10,
                        "ticket_id": "N01-00000385",
                        "product": "1|44733",
                        "store": "1|023"
                    }
                ]
            }
        }

class EmployeeSummaryResponse(BaseModel):
    """Modelo para la respuesta de resumen de ventas por empleado"""
    success: bool = Field(default=True, description="Indica si la operación fue exitosa")
    key_employee: Optional[str] = Field(None, description="ID del empleado o None para todos")
    total_amount: float = Field(..., description="Monto total de ventas")
    average_amount: float = Field(..., description="Promedio de ventas por transacción")
    total_quantity: int = Field(..., description="Cantidad total vendida")
    records_count: int = Field(..., description="Número total de registros")

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "key_employee": "1|343",
                "total_amount": 150000.50,
                "average_amount": 6000.02,
                "total_quantity": 1000,
                "records_count": 25
            }
        }


class ProductSummaryResponse(BaseModel):
    """Modelo para la respuesta de resumen de ventas por producto"""
    success: bool = Field(default=True, description="Indica si la operación fue exitosa")
    key_product: Optional[str] = Field(None, description="ID del producto o None para todos")
    total_amount: float = Field(..., description="Monto total de ventas")
    average_amount: float = Field(..., description="Promedio de ventas por transacción")
    total_quantity: int = Field(..., description="Cantidad total vendida")
    records_count: int = Field(..., description="Número total de registros")

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "key_product": "1|44733",
                "total_amount": 250000.75,
                "average_amount": 5000.02,
                "total_quantity": 2500,
                "records_count": 50
            }
        }