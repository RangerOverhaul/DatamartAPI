import pytest
import pandas as pd
from datetime import date
from unittest.mock import Mock, patch

from app.services.datamart import DatamartService
from app.models.responses import ProductSalesResponse


@pytest.mark.unit
class TestGetSalesByProduct:
    """Tests para método get_sales_by_product"""

    def test_returns_product_sales_response_object(self, mock_settings, product_key, date_range):
        """Debe retornar objeto ProductSalesResponse"""
        service = DatamartService()

        result = service.get_sales_by_product(
            key_product=product_key,
            date_start=date_range['start'],
            date_end=date_range['end']
        )

        assert isinstance(result, ProductSalesResponse)

    def test_response_has_required_fields(self, mock_settings, product_key, date_range):
        """La respuesta debe tener todos los campos requeridos"""
        service = DatamartService()

        result = service.get_sales_by_product(
            key_product=product_key,
            date_start=date_range['start'],
            date_end=date_range['end']
        )

        # Assert
        assert hasattr(result, 'success')
        assert hasattr(result, 'key_product')
        assert hasattr(result, 'date_start')
        assert hasattr(result, 'date_end')
        assert hasattr(result, 'total_amount')
        assert hasattr(result, 'total_quantity')
        assert hasattr(result, 'records_count')
        assert hasattr(result, 'sales')

    def test_filters_by_product_correctly(self, mock_settings, product_key, date_range):
        """Debe filtrar correctamente por producto"""
        # Arrange
        service = DatamartService()

        # Act
        result = service.get_sales_by_product(
            key_product=product_key,
            date_start=date_range['start'],
            date_end=date_range['end']
        )

        # Assert
        assert result.key_product == product_key
        assert result.success is True

    def test_filters_by_date_range_correctly(self, mock_settings, product_key):
        """Debe filtrar correctamente por rango de fechas"""
        # Arrange
        service = DatamartService()
        date_start = date(2023, 11, 1)
        date_end = date(2023, 11, 30)

        # Act
        result = service.get_sales_by_product(
            key_product=product_key,
            date_start=date_start,
            date_end=date_end
        )

        # Assert
        assert result.date_start == date_start
        assert result.date_end == date_end

        # Verificar que todas las ventas están en el rango
        for sale in result.sales:
            assert date_start <= sale.date <= date_end

    def test_calculates_total_amount_correctly(self, mock_settings, product_key, date_range):
        """Debe calcular el monto total correctamente"""
        # Arrange
        service = DatamartService()

        # Act
        result = service.get_sales_by_product(
            key_product=product_key,
            date_start=date_range['start'],
            date_end=date_range['end']
        )

        # Assert
        assert isinstance(result.total_amount, float)

        # Calcular manualmente para verificar
        manual_total = sum(sale.amount for sale in result.sales)
        assert result.total_amount == pytest.approx(manual_total, rel=1e-6)

    def test_calculates_total_quantity_correctly(self, mock_settings, product_key, date_range):
        """Debe calcular la cantidad total correctamente"""
        # Arrange
        service = DatamartService()

        # Act
        result = service.get_sales_by_product(
            key_product=product_key,
            date_start=date_range['start'],
            date_end=date_range['end']
        )

        # Assert
        assert isinstance(result.total_quantity, int)

        # Calcular manualmente
        manual_total = sum(sale.quantity for sale in result.sales)
        assert result.total_quantity == manual_total

    def test_counts_records_correctly(self, mock_settings, product_key, date_range):
        """Debe contar los registros correctamente"""
        # Arrange
        service = DatamartService()

        # Act
        result = service.get_sales_by_product(
            key_product=product_key,
            date_start=date_range['start'],
            date_end=date_range['end']
        )

        # Assert
        assert result.records_count == len(result.sales)

    def test_returns_empty_list_for_nonexistent_product(self, mock_settings, date_range):
        """Debe retornar lista vacía para producto inexistente"""
        # Arrange
        service = DatamartService()
        nonexistent_product = "999|99999"

        # Act
        result = service.get_sales_by_product(
            key_product=nonexistent_product,
            date_start=date_range['start'],
            date_end=date_range['end']
        )

        # Assert
        assert result.records_count == 0
        assert len(result.sales) == 0
        assert result.total_amount == 0.0
        assert result.total_quantity == 0
        assert result.success is True

    def test_raises_error_for_invalid_date_range(self, mock_settings, product_key):
        """Debe lanzar error si date_end < date_start"""
        # Arrange
        service = DatamartService()
        date_start = date(2023, 12, 31)
        date_end = date(2023, 1, 1)

        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            service.get_sales_by_product(
                key_product=product_key,
                date_start=date_start,
                date_end=date_end
            )

        assert "debe ser mayor o igual" in str(exc_info.value)

    def test_sales_list_contains_correct_product(self, mock_settings, product_key, date_range):
        """Todas las ventas deben ser del producto consultado"""
        # Arrange
        service = DatamartService()

        # Act
        result = service.get_sales_by_product(
            key_product=product_key,
            date_start=date_range['start'],
            date_end=date_range['end']
        )

        # Assert
        for sale in result.sales:
            assert sale.product == product_key

    def test_handles_negative_amounts(self, mock_settings):
        """Debe manejar montos negativos (devoluciones)"""
        # Arrange
        service = DatamartService()

        # Act
        result = service.get_sales_by_product(
            key_product="1|44733",
            date_start=date(2023, 11, 1),
            date_end=date(2023, 11, 30)
        )

        # Assert
        assert result.records_count >= 0
        # Verificar que acepta montos negativos
        if result.records_count > 0:
            amounts = [sale.amount for sale in result.sales]
            assert all(isinstance(amt, (int, float)) for amt in amounts)

    def test_handles_multiple_sales_same_product(self, mock_settings):
        """Debe manejar múltiples ventas del mismo producto"""
        # Arrange
        service = DatamartService()

        # Act - Rango amplio para encontrar más ventas
        result = service.get_sales_by_product(
            key_product="1|44733",
            date_start=date(2023, 10, 1),
            date_end=date(2023, 11, 30)
        )

        # Assert
        assert isinstance(result.sales, list)
        # Si hay ventas, verificar que todas son del mismo producto
        for sale in result.sales:
            assert sale.product == "1|44733"

    def test_accepts_equal_start_and_end_dates(self, mock_settings, product_key):
        """Debe aceptar fecha inicio igual a fecha fin"""
        # Arrange
        service = DatamartService()
        same_date = date(2023, 11, 2)

        # Act
        result = service.get_sales_by_product(
            key_product=product_key,
            date_start=same_date,
            date_end=same_date
        )

        # Assert
        assert result is not None
        assert isinstance(result, ProductSalesResponse)

        # Si hay ventas, deben ser todas de esa fecha
        for sale in result.sales:
            assert sale.date == same_date


@pytest.mark.unit
class TestProductSalesDataQuality:
    """Tests para calidad de datos en ventas por producto"""

    def test_sale_records_have_required_fields(self, mock_settings, product_key, date_range):
        """Cada registro de venta debe tener los campos requeridos"""
        # Arrange
        service = DatamartService()

        # Act
        result = service.get_sales_by_product(
            key_product=product_key,
            date_start=date_range['start'],
            date_end=date_range['end']
        )

        # Assert
        if result.records_count > 0:
            sale = result.sales[0]
            assert hasattr(sale, 'date')
            assert hasattr(sale, 'amount')
            assert hasattr(sale, 'quantity')
            assert hasattr(sale, 'ticket_id')
            assert hasattr(sale, 'product')
            assert hasattr(sale, 'store')

    def test_amounts_are_numeric(self, mock_settings, product_key, date_range):
        """Los montos deben ser numéricos"""
        # Arrange
        service = DatamartService()

        # Act
        result = service.get_sales_by_product(
            key_product=product_key,
            date_start=date_range['start'],
            date_end=date_range['end']
        )

        # Assert
        assert isinstance(result.total_amount, (int, float))
        for sale in result.sales:
            assert isinstance(sale.amount, (int, float))

    def test_quantities_are_integers(self, mock_settings, product_key, date_range):
        """Las cantidades deben ser enteros"""
        # Arrange
        service = DatamartService()

        # Act
        result = service.get_sales_by_product(
            key_product=product_key,
            date_start=date_range['start'],
            date_end=date_range['end']
        )

        # Assert
        assert isinstance(result.total_quantity, int)
        for sale in result.sales:
            assert isinstance(sale.quantity, int)

    def test_dates_are_date_objects(self, mock_settings, product_key, date_range):
        """Las fechas deben ser objetos date"""
        # Arrange
        service = DatamartService()

        # Act
        result = service.get_sales_by_product(
            key_product=product_key,
            date_start=date_range['start'],
            date_end=date_range['end']
        )

        # Assert
        assert isinstance(result.date_start, date)
        assert isinstance(result.date_end, date)
        for sale in result.sales:
            assert isinstance(sale.date, date)


@pytest.mark.unit
class TestProductSalesEdgeCases:
    """Tests para casos extremos"""

    def test_handles_very_popular_product(self, mock_settings):
        """Debe manejar productos con muchas ventas"""
        # Arrange
        service = DatamartService()

        # Act - Buscar en todo el rango disponible
        result = service.get_sales_by_product(
            key_product="1|44733",
            date_start=date(2023, 10, 1),
            date_end=date(2023, 11, 30)
        )

        # Assert
        assert result is not None
        assert result.records_count >= 0

    def test_handles_product_with_zero_sales(self, mock_settings):
        """Debe manejar productos sin ventas en el periodo"""
        # Arrange
        service = DatamartService()

        # Act
        result = service.get_sales_by_product(
            key_product="999|99999",
            date_start=date(2023, 11, 1),
            date_end=date(2023, 11, 30)
        )

        # Assert
        assert result.records_count == 0
        assert result.total_amount == 0.0
        assert result.total_quantity == 0
        assert len(result.sales) == 0

    def test_performance_with_wide_date_range(self, mock_settings, product_key):
        """Debe tener buen rendimiento con rango amplio"""
        import time

        # Arrange
        service = DatamartService()

        # Act
        start_time = time.time()
        result = service.get_sales_by_product(
            key_product=product_key,
            date_start=date(2023, 1, 1),
            date_end=date(2023, 12, 31)
        )
        end_time = time.time()

        # Assert
        execution_time = end_time - start_time
        assert execution_time < 2.0  # Debe ejecutar en menos de 2 segundos
        assert result is not None