import pytest
from datetime import date
from unittest.mock import Mock
import pandas as pd

from app.services.datamart import DatamartService
from app.models.responses import StoreSummaryResponse, StoreSalesResponse


@pytest.mark.unit
class TestGetStoreSummary:
    """Tests para metodo get_store_summary"""

    def test_returns_store_summary_response_object(self, mock_settings, store_key):
        """Debe retornar objeto StoreSummaryResponse"""
        service = DatamartService()

        result = service.get_store_summary(key_store=store_key)

        assert isinstance(result, StoreSummaryResponse)

    def test_response_has_required_fields(self, mock_settings, store_key):
        """La respuesta debe tener todos los campos requeridos"""
        service = DatamartService()

        result = service.get_store_summary(key_store=store_key)

        assert hasattr(result, 'success')
        assert hasattr(result, 'key_store')
        assert hasattr(result, 'total_amount')
        assert hasattr(result, 'average_amount')
        assert hasattr(result, 'total_quantity')
        assert hasattr(result, 'records_count')

    def test_calculates_total_amount_correctly(self, mock_settings, store_key):
        """Debe calcular el total correctamente"""
        service = DatamartService()

        result = service.get_store_summary(key_store=store_key)

        assert isinstance(result.total_amount, float)
        assert result.total_amount != 0 or result.records_count == 0

    def test_calculates_average_amount_correctly(self, mock_settings, store_key):
        """Debe calcular el promedio correctamente"""
        service = DatamartService()

        result = service.get_store_summary(key_store=store_key)

        assert isinstance(result.average_amount, float)

        if result.records_count > 0:
            expected_average = result.total_amount / result.records_count
            assert result.average_amount == pytest.approx(expected_average, rel=1e-6)
        else:
            assert result.average_amount == 0.0

    def test_average_is_zero_when_no_records(self, mock_settings):
        """El promedio debe ser 0 cuando no hay registros"""
        service = DatamartService()
        nonexistent_store = "999|999"

        result = service.get_store_summary(key_store=nonexistent_store)

        assert result.records_count == 0
        assert result.average_amount == 0.0
        assert result.total_amount == 0.0

    def test_summary_for_specific_store(self, mock_settings):
        """Debe retornar resumen para tienda específica"""
        service = DatamartService()
        store_key = "1|023"

        result = service.get_store_summary(key_store=store_key)

        assert result.key_store == store_key
        assert result.success is True

    def test_summary_for_all_stores(self, mock_settings):
        """Debe retornar resumen de todas las tiendas cuando key_store es None"""
        service = DatamartService()

        result = service.get_store_summary(key_store=None)

        assert result.key_store is None
        assert result.success is True
        assert result.records_count > 0

    def test_sum_of_stores_equals_total(self, mock_settings):
        """La suma de todas las tiendas debe igual al total general"""
        service = DatamartService()
        unique_stores = service._data['KeyStore'].unique()

        individual_totals = 0.0
        for store in unique_stores:
            result = service.get_store_summary(key_store=store)
            individual_totals += result.total_amount

        total_result = service.get_store_summary(key_store=None)

        assert individual_totals == pytest.approx(total_result.total_amount, rel=1e-6)



@pytest.mark.unit
class TestStoreSummaryPerformance:
    """Tests de rendimiento"""

    def test_performance_with_all_stores(self, mock_settings):
        """Debe tener buen rendimiento al calcular resumen de todas"""
        import time

        service = DatamartService()

        start_time = time.time()
        result = service.get_store_summary(key_store=None)
        end_time = time.time()

        execution_time = end_time - start_time
        assert execution_time < 1.0
        assert result is not None