from datetime import date

from fastapi import HTTPException, status


class DatamartException(Exception):
    """Excepción base para errores del datamart"""

    def __init__(self, message: str = "Error del datamart"):
        self.message = message
        super().__init__(self.message)


class DatamartNotFoundError(DatamartException):
    """Error cuando no se encuentra el datamart"""

    def __init__(self, message: str = "Datamart no disponible"):
        super().__init__(message)


class InvalidDateRangeError(DatamartException):
    """Error cuando el rango de fechas es inválido"""

    def __init__(self, date_start: date, date_end: date):
        message = f"Rango de fechas inválido: {date_end} debe ser mayor o igual a {date_start}"
        super().__init__(message)

        self.date_start = date_start
        self.date_end = date_end


class EntityNotFoundError(DatamartException):
    """Error cuando no se encuentra la entidad solicitada"""

    def __init__(self, entity_type: str, entity_id: str, period: str = None):
        if period:
            message = f"No se encontraron {entity_type} para {entity_id} en el periodo {period}"
        else:
            message = f"{entity_type} {entity_id} no encontrado"

        super().__init__(message)

        self.entity_type = entity_type
        self.entity_id = entity_id
        self.period = period


class EmployeeNotFoundError(EntityNotFoundError):
    """Error específico cuando no se encuentra un empleado"""

    def __init__(self, employee_id: str):
        super().__init__("empleado", employee_id)


class NoSalesFoundError(EntityNotFoundError):
    """Error específico cuando no se encuentran ventas"""

    def __init__(self, employee_id: str, date_start: date, date_end: date):
        period = f"{date_start} a {date_end}"
        super().__init__("ventas", employee_id, period)

        self.date_start = date_start
        self.date_end = date_end


def raise_http_exception(status_code: int, detail: str):
    """Helper para lanzar excepciones HTTP"""
    raise HTTPException(status_code=status_code, detail=detail)