import pytest
import pandas as pd
from datetime import date
from unittest.mock import Mock, patch, MagicMock

from app.services.datamart import DatamartService

@pytest.mark.unit
class TestGetSalesByStore:
    """Tests para metodo get_sales_by_store"""

    def test_validates_date_range_in_service(self, mock_settings, store_key):
        """Debe validar rango de fechas"""
        service = DatamartService()

        with pytest.raises(ValueError):
            service.get_sales_by_store(
                key_store=store_key,
                date_start=date(2023, 12, 31),
                date_end=date(2023, 1, 1)
            )

    def test_returns_correct_response_structure(self, mock_settings, store_key, date_range):
        """Debe retornar estructura correcta de respuesta"""
        service = DatamartService()

        result = service.get_sales_by_store(
            key_store=store_key,
            date_start=date_range['start'],
            date_end=date_range['end']
        )

        assert hasattr(result, 'key_store')
        assert hasattr(result, 'date_start')
        assert hasattr(result, 'date_end')
        assert hasattr(result, 'total_amount')
        assert hasattr(result, 'total_quantity')
        assert hasattr(result, 'records_count')
        assert hasattr(result, 'sales')

    def test_filters_by_store_correctly(self, mock_settings, store_key, date_range):
        """Debe filtrar correctamente por tienda"""
        service = DatamartService()

        result = service.get_sales_by_store(
            key_store=store_key,
            date_start=date_range['start'],
            date_end=date_range['end']
        )

        assert result.key_store == store_key
        # Verificar que todas las ventas son de la tienda correcta
        for sale in result.sales:
            assert sale.store == store_key

    def test_filters_by_date_range_correctly(self, mock_settings, store_key):
        """Debe filtrar correctamente por rango de fechas"""
        service = DatamartService()
        date_start = date(2023, 11, 1)
        date_end = date(2023, 11, 30)

        result = service.get_sales_by_store(
            key_store=store_key,
            date_start=date_start,
            date_end=date_end
        )

        for sale in result.sales:
            assert date_start <= sale.date <= date_end

    def test_calculates_total_amount_correctly(self, mock_settings, store_key, date_range):
        """Debe calcular el monto total correctamente"""
        service = DatamartService()

        result = service.get_sales_by_store(
            key_store=store_key,
            date_start=date_range['start'],
            date_end=date_range['end']
        )

        assert isinstance(result.total_amount, float)
        # Calcular manualmente para verificar
        manual_total = sum(sale.amount for sale in result.sales)
        assert result.total_amount == pytest.approx(manual_total)

    def test_calculates_total_quantity_correctly(self, mock_settings, store_key, date_range):
        """Debe calcular la cantidad total correctamente"""
        service = DatamartService()

        result = service.get_sales_by_store(
            key_store=store_key,
            date_start=date_range['start'],
            date_end=date_range['end']
        )

        assert isinstance(result.total_quantity, int)
        manual_total = sum(sale.quantity for sale in result.sales)
        assert result.total_quantity == manual_total

    def test_counts_records_correctly(self, mock_settings, store_key, date_range):
        """Debe contar los registros correctamente"""
        service = DatamartService()

        result = service.get_sales_by_store(
            key_store=store_key,
            date_start=date_range['start'],
            date_end=date_range['end']
        )

        assert result.records_count == len(result.sales)

    def test_returns_empty_list_for_nonexistent_store(self, mock_settings, date_range):
        """Debe retornar lista vacía para tienda inexistente"""
        service = DatamartService()
        nonexistent_store = "999|999"

        result = service.get_sales_by_store(
            key_store=nonexistent_store,
            date_start=date_range['start'],
            date_end=date_range['end']
        )

        assert result.records_count == 0
        assert len(result.sales) == 0
        assert result.total_amount == 0.0
        assert result.total_quantity == 0

    def test_sales_list_contains_required_fields(self, mock_settings, store_key, date_range):
        """Cada venta debe contener los campos requeridos"""
        service = DatamartService()

        result = service.get_sales_by_store(
            key_store=store_key,
            date_start=date_range['start'],
            date_end=date_range['end']
        )

        if result.records_count > 0:
            sale = result.sales[0]
            assert hasattr(sale, 'date')
            assert hasattr(sale, 'amount')
            assert hasattr(sale, 'quantity')
            assert hasattr(sale, 'ticket_id')
            assert hasattr(sale, 'product')
            assert hasattr(sale, 'store')
