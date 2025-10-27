from pydantic import BaseModel, Field
from datetime import date
from typing import List, Optional

class SaleRecord(BaseModel):
    """Modelo para representar un registro individual de venta"""
    date: date
    amount: float = Field(..., description="Monto de la venta")
    quantity: int = Field(..., description="Cantidad vendida")
    ticket_id: str = Field(..., description="ID del ticket")
    product: str = Field(..., description="Producto vendido")
    store: str = Field(..., description="Tienda donde se realizó la venta")

