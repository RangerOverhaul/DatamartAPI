from pydantic import BaseModel, Field, EmailStr
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

class LoginRequest(BaseModel):
    """Modelo para solicitud de login con email/password"""
    email: EmailStr
    password: str


class UserProfile(BaseModel):
    """Modelo para perfil de usuario"""
    user_id: str
    email: str
    email_verified: bool

class RegisterRequest(BaseModel):
    """Modelo para registro de usuario (opcional)"""
    email: EmailStr
    password: str
    confirm_password: str