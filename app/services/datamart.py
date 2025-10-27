import pandas as pd
from datetime import date
from typing import Dict, Optional
import logging

from app.config import settings
from app.models.schemas import SaleRecord
from app.models.responses import (EmployeeSalesResponse, ProductSalesResponse, StoreSalesResponse,
                                  EmployeeSummaryResponse, ProductSummaryResponse, StoreSummaryResponse)
from app.utils.exceptions import InvalidDateRangeError

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def _create_detail_list(filtered) -> list:
    sales_list = []
    for _, row in filtered.iterrows():
        sales_list.append(SaleRecord(
            date=row['KeyDate'].date(),
            amount=float(row['Amount']),
            quantity=int(row['Qty']),
            ticket_id=str(row['TicketId']),
            product=str(row['KeyProduct']),
            store=str(row['KeyStore'])
        ))
    return sales_list

def _get_total_details(filtered) -> tuple:
    total_amount = float(filtered['Amount'].sum())
    total_quantity = int(filtered['Qty'].sum())
    records_count = len(filtered)

    return total_amount, total_quantity, records_count

class DatamartService:
    """Servicio para operaciones sobre el datamart"""

    def __init__(self):
        self.data: Optional[pd.DataFrame] = None
        self._load_data()

    def _load_data(self):
        """Carga todos los archivos parquet de la carpeta"""
        try:
            parquet_files = settings.get_parquet_files()
            logger.info(f"Encontrados {len(parquet_files)} archivos parquet")

            # Leer todos los archivos parquet
            dataframes = []
            for file in parquet_files:
                logger.info(f"Leyendo: {file.name}")
                df = pd.read_parquet(file)
                dataframes.append(df)
                logger.info(f"{len(df)} registros cargados")

            # Concatenar todos los DataFrames
            self.data = pd.concat(dataframes, ignore_index=True)

            # Procesando columnas importantes
            logger.info("Procesando datos...")

            # Convertir fecha
            self.data['KeyDate'] = pd.to_datetime(self.data['KeyDate'])

            # Convertir Amount a float
            self.data['Amount'] = pd.to_numeric(self.data['Amount'], errors='coerce')

            # Convertir Qty a int
            self.data['Qty'] = pd.to_numeric(self.data['Qty'], errors='coerce').fillna(0).astype(int)

            logger.info(f"Datamart cargado exitosamente")
            logger.info(f"Total registros: {len(self.data):,}")
            logger.info(f"Rango de fechas: {self.data['KeyDate'].min()} a {self.data['KeyDate'].max()}")

            # Mostrar algunas estadísticas
            logger.info(f"Empleados únicos: {self.data['KeyEmployee'].nunique()}")
            logger.info(f"Productos únicos: {self.data['KeyProduct'].nunique()}")
            logger.info(f"Tiendas únicas: {self.data['KeyStore'].nunique()}")

        except FileNotFoundError as e:
            logger.error(f"Error: {e}")
            raise
        except Exception as e:
            logger.error(f"Error inesperado al cargar datamart: {e}")
            raise Exception(f"Error al cargar datamart: {e}")

    def get_sales_by_employee(
                self,
                key_employee: str,
                date_start: date,
                date_end: date
        ) -> EmployeeSalesResponse:
            """
            Obtiene las ventas de un empleado en un periodo.

            Args:
                key_employee: ID del empleado (ej. "1|343")
                date_start: Fecha de inicio
                date_end: Fecha de fin

            Returns:
                Diccionario con ventas, totales y resumen

            Example:
                -> service.get_sales_by_employee("1|343", date(2023,11,1), date(2023,11,30))
                {'key_employee': '1|343',
                'date_start': date(2023, 11, 1),
                'date_end': date(2023, 11, 30),
                'total_amount': 24873.95,
                'total_quantity': -4,
                'records_count': 1,
                'sales': [...]}
            """
            logger.info(f"Consultando ventas del empleado {key_employee}")
            logger.info(f"Periodo: {date_start} a {date_end}")

            # Validar rango de fechas
            if date_end < date_start:
                raise InvalidDateRangeError(date_start, date_end)

            # Filtrar por empleado y rango de fechas
            mask = (
                    (self.data['KeyEmployee'] == key_employee) &
                    (self.data['KeyDate'] >= pd.Timestamp(date_start)) &
                    (self.data['KeyDate'] <= pd.Timestamp(date_end))
            )
            filtered_employee = self.data[mask].copy()

            if len(filtered_employee) == 0:
                logger.warning(f"No se encontraron ventas para el empleado {key_employee}")

            # Calcular totales
            total_amount, total_quantity,records_count = _get_total_details(filtered_employee)

            # Preparando lista de ventas (detalles)
            sales_list_employee = _create_detail_list(filtered_employee)

            logger.info(f"Registros encontrados: {records_count}")
            logger.info(f"Total ventas: ${total_amount:,.2f}")
            logger.info(f"Cantidad total: {total_quantity}")

            return EmployeeSalesResponse(
                key_employee=key_employee,
                date_start=date_start,
                date_end=date_end,
                total_amount=total_amount,
                total_quantity=total_quantity,
                records_count=records_count,
                sales=sales_list_employee
                )

    def get_sales_by_product(
            self,
            key_product: str,
            date_start: date,
            date_end: date
    ) -> ProductSalesResponse:
        """
        Obtiene las ventas de un producto en un periodo.

        Args:
            key_product: ID del producto (ej. "1|44733")
            date_start: Fecha de inicio
            date_end: Fecha de fin

        Returns:
            ProductSalesResponse con ventas, totales y resumen

        Example:
            -> service.get_sales_by_product("1|44733", date(2023,11,1), date(2023,11,30))
            ProductSalesResponse(success=True,
                key_product='1|44733',
                total_amount=24873.95,
                ...)
        """
        logger.info(f"Consultando ventas del producto {key_product}")
        logger.info(f"Periodo: {date_start} a {date_end}")

        # Validar rango de fechas
        if date_end < date_start:
            raise InvalidDateRangeError(date_start, date_end)

        # Filtrar por producto y rango de fechas
        mask = (
                (self.data['KeyProduct'] == key_product) &
                (self.data['KeyDate'] >= pd.Timestamp(date_start)) &
                (self.data['KeyDate'] <= pd.Timestamp(date_end))
        )
        filtered_product = self.data[mask].copy()

        if len(filtered_product) == 0:
            logger.warning(f"No se encontraron ventas para el producto {key_product}")

        # Calcular totales
        total_amount, total_quantity,records_count = _get_total_details(filtered_product)

        # Preparar lista de ventas (detalles)
        sales_list_products = _create_detail_list(filtered_product)

        logger.info(f"Consulta completada:")
        logger.info(f"Registros encontrados: {records_count}")
        logger.info(f"Total ventas: ${total_amount:,.2f}")
        logger.info(f"Cantidad total: {total_quantity}")

        return ProductSalesResponse(
            success=True,
            key_product=key_product,
            date_start=date_start,
            date_end=date_end,
            total_amount=total_amount,
            total_quantity=total_quantity,
            records_count=records_count,
            sales=sales_list_products
        )

    def get_sales_by_store(
            self,
            key_store: str,
            date_start: date,
            date_end: date
    ) -> StoreSalesResponse:
        """
        Obtiene las ventas de una tienda en un periodo.

        Args:
            key_store: ID de la tienda (ej. "1|023")
            date_start: Fecha de inicio
            date_end: Fecha de fin

        Returns:
            StoreSalesResponse con ventas, totales y resumen

        Example:
            -> service.get_sales_by_store("1|023", date(2023,11,1), date(2023,11,30))
            StoreSalesResponse(key_store='1|023',
                total_amount=24873.95,
                ...)
        """
        logger.info(f"Consultando ventas de la tienda {key_store}")
        logger.info(f"Periodo: {date_start} a {date_end}")

        # Validar rango de fechas
        if date_end < date_start:
            raise InvalidDateRangeError(date_start, date_end)

        # Filtrar por tienda y rango de fechas
        mask = (
                (self.data['KeyStore'] == key_store) &
                (self.data['KeyDate'] >= pd.Timestamp(date_start)) &
                (self.data['KeyDate'] <= pd.Timestamp(date_end))
        )
        filtered_store = self.data[mask].copy()

        if len(filtered_store) == 0:
            logger.warning(f"No se encontraron ventas para la tienda {key_store}")

        # Calcular totales
        total_amount, total_quantity, records_count = _get_total_details(filtered_store)

        # Preparar lista de ventas (detalles)
        sales_list_store = _create_detail_list(filtered_store)

        logger.info(f"Consulta completada:")
        logger.info(f"Registros encontrados: {records_count}")
        logger.info(f"Total ventas: ${total_amount:,.2f}")
        logger.info(f"Cantidad total: {total_quantity}")

        return StoreSalesResponse(
            key_store=key_store,
            date_start=date_start,
            date_end=date_end,
            total_amount=total_amount,
            total_quantity=total_quantity,
            records_count=records_count,
            sales=sales_list_store
        )

    def get_employee_summary(
            self,
            key_employee: Optional[str] = None
    ) -> EmployeeSummaryResponse:
        """
        Obtiene el resumen de ventas (total y promedio) por empleado.

        Args:
            key_employee: ID del empleado (ej: "1|343") o None para todos los empleados

        Returns:
            EmployeeSummaryResponse con totales, promedios y estadísticas

        Example:
            # Resumen de un empleado específico
            -> service.get_employee_summary("1|343")
            EmployeeSummaryResponse(
                success=True,
                key_employee='1|343',
                total_amount=150000.50,
                average_amount=6000.02,
                ...
            )

            # Resumen de todos los empleados
            -> service.get_employee_summary(None)
            EmployeeSummaryResponse(success=True,
                key_employee=None,
                total_amount=5000000.00,
                average_amount=15000.50,
                ...)
        """
        if key_employee:
            logger.info(f"Calculando resumen del empleado {key_employee}")
        else:
            logger.info(f"Calculando resumen de TODOS los empleados")

        # Filtrar datos
        if key_employee:
            filtered_summary_employee = self.data[self.data['KeyEmployee'] == key_employee].copy()

            if len(filtered_summary_employee) == 0:
                logger.warning(f"No se encontraron datos para el empleado {key_employee}")
        else:
            filtered_summary_employee = self.data.copy()

        # Calcular métricas
        total_amount, total_quantity, records_count = _get_total_details(filtered_summary_employee)

        # Calcular promedio (evitar división por cero)
        average_amount = total_amount / records_count if records_count > 0 else 0.0

        logger.info(f"Resumen calculado:")
        logger.info(f"Total registros: {records_count:,}")
        logger.info(f"Total ventas: ${total_amount:,.2f}")
        logger.info(f"Promedio por venta: ${average_amount:,.2f}")
        logger.info(f"Cantidad total: {total_quantity:,}")

        return EmployeeSummaryResponse(
            success=True,
            key_employee=key_employee,
            total_amount=round(total_amount, 2),
            average_amount=round(average_amount, 2),
            total_quantity=total_quantity,
            records_count=records_count
        )

    def get_product_summary(
            self,
            key_product: Optional[str] = None
    ) -> ProductSummaryResponse:
        """
        Obtiene el resumen de ventas (total y promedio) por producto.

        Args:
            key_product: ID del producto (ej: "1|44733") o None para todos los productos

        Returns:
            ProductSummaryResponse con totales, promedios y estadísticas

        Example:
            # Resumen de un producto específico
            -> service.get_product_summary("1|44733")
            ProductSummaryResponse(success=True,
                key_product='1|44733',
                total_amount=250000.75,
                average_amount=5000.02,
                ...)

            # Resumen de todos los productos
            -> service.get_product_summary(None)
            ProductSummaryResponse(success=True,
                key_product=None,
                total_amount=10000000.00,
                average_amount=30000.50,
                ...)
        """
        if key_product:
            logger.info(f"Calculando resumen del producto {key_product}")
        else:
            logger.info(f"Calculando resumen de TODOS los productos")

        # Filtrar datos
        if key_product:
            filtered_summary_product = self.data[self.data['KeyProduct'] == key_product].copy()

            if len(filtered_summary_product) == 0:
                logger.warning(f"No se encontraron datos para el producto {key_product}")
        else:
            filtered_summary_product = self.data.copy()

        # Calcular métricas
        total_amount, total_quantity, records_count = _get_total_details(filtered_summary_product)

        # Calcular promedio (evitar división por cero)
        average_amount = total_amount / records_count if records_count > 0 else 0.0

        logger.info(f"Resumen calculado:")
        logger.info(f"Total registros: {records_count:,}")
        logger.info(f"Total ventas: ${total_amount:,.2f}")
        logger.info(f"Promedio por venta: ${average_amount:,.2f}")
        logger.info(f"Cantidad total: {total_quantity:,}")

        return ProductSummaryResponse(
            success=True,
            key_product=key_product,
            total_amount=round(total_amount, 2),
            average_amount=round(average_amount, 2),
            total_quantity=total_quantity,
            records_count=records_count
        )

    def get_store_summary(
            self,
            key_store: Optional[str] = None
    ) -> StoreSummaryResponse:
        """
        Obtiene el resumen de ventas (total y promedio) por tienda.

        Args:
            key_store: ID de la tienda (ej: "1|023") o None para todas las tiendas

        Returns:
            StoreSummaryResponse con totales, promedios y estadísticas

        Example:
            -> # Resumen de una tienda específica
            -> service.get_store_summary("1|023")
            StoreSummaryResponse(success=True,
                key_store='1|023',
                total_amount=500000.25,
                average_amount=10000.50,
                ...)

            -> # Resumen de todas las tiendas
            -> service.get_store_summary(None)
            StoreSummaryResponse(Success=True,
                key_store=None,
                total_amount=15000000.00,
                average_amount=45000.50,
                ...)
        """
        if key_store:
            logger.info(f"Calculando resumen de la tienda {key_store}")
        else:
            logger.info(f"Calculando resumen de TODAS las tiendas")

        # Filtrar datos
        if key_store:
            filtered_summary_store = self.data[self.data['KeyStore'] == key_store].copy()

            if len(filtered_summary_store) == 0:
                logger.warning(f"No se encontraron datos para la tienda {key_store}")
        else:
            filtered_summary_store = self.data.copy()

        # Calcular métricas
        total_amount, total_quantity, records_count = _get_total_details(filtered_summary_store)

        # Calcular promedio (evitar división por cero)
        average_amount = total_amount / records_count if records_count > 0 else 0.0

        logger.info(f"Resumen calculado:")
        logger.info(f"Total registros: {records_count:,}")
        logger.info(f"Total ventas: ${total_amount:,.2f}")
        logger.info(f"Promedio por venta: ${average_amount:,.2f}")
        logger.info(f"Cantidad total: {total_quantity:,}")

        return StoreSummaryResponse(
            success=True,
            key_store=key_store,
            total_amount=round(total_amount, 2),
            average_amount=round(average_amount, 2),
            total_quantity=total_quantity,
            records_count=records_count
        )

# Instancia singleton del servicio
_datamart_service: Optional[DatamartService] = None

def get_datamart_service() -> DatamartService:
    """
    Dependency para obtener la instancia del servicio.
    Se crea solo una vez y se reutiliza.
    """
    global _datamart_service
    if _datamart_service is None:
        _datamart_service = DatamartService()
    return _datamart_service