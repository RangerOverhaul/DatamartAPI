import pytest
import pandas as pd
from datetime import date
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path

from app.services.datamart import DatamartService, get_datamart_service


@pytest.mark.unit
class TestDatamartServiceInitialization:
    """Tests para inicialización del servicio"""

    def test_service_initializes_successfully(self, mock_settings):
        """El servicio debe inicializarse correctamente"""
        service = DatamartService()

        assert service is not None
        assert service._data is not None
        assert isinstance(service._data, pd.DataFrame)

    def test_service_loads_parquet_files(self, mock_settings):
        """Debe cargar archivos parquet correctamente"""
        service = DatamartService()

        assert len(service._data) > 0
        assert 'KeyEmployee' in service._data.columns
        assert 'KeyDate' in service._data.columns
        assert 'Amount' in service._data.columns

    def test_service_converts_date_column(self, mock_settings):
        """Debe convertir KeyDate a datetime"""
        service = DatamartService()

        assert pd.api.types.is_datetime64_any_dtype(service._data['KeyDate'])

    def test_service_converts_amount_to_float(self, mock_settings):
        """Debe convertir Amount a float"""
        service = DatamartService()

        assert pd.api.types.is_float_dtype(service._data['Amount'])

    def test_service_converts_qty_to_int(self, mock_settings):
        """Debe convertir Qty a int"""
        service = DatamartService()

        assert pd.api.types.is_integer_dtype(service._data['Qty'])

    def test_service_raises_error_when_no_parquet_files(self, monkeypatch):
        """Debe lanzar error si no hay archivos parquet"""

        class BadSettings:
            DATAMART_PATH = "../fixtures/" #Reemplazar con carpeta de pruebas
            DEBUG = True
            BASE_DIR = Path(__file__).parent.parent

            def get_parquet_files(self):
                raise FileNotFoundError("No hay archivos .parquet")

        monkeypatch.setattr("app.config.settings", BadSettings())

        with pytest.raises(Exception):
            DatamartService()


@pytest.mark.unit
class TestGetDatamartServiceSingleton:
    """Tests para función get_datamart_service"""

    def test_returns_datamart_service_instance(self, mock_settings):
        """Debe retornar una instancia de DatamartService"""
        service = get_datamart_service()

        assert isinstance(service, DatamartService)

    def test_returns_same_instance_on_multiple_calls(self, mock_settings):
        """Debe retornar la misma instancia (singleton)"""
        service1 = get_datamart_service()
        service2 = get_datamart_service()

        assert service1 is service2

    @patch('app.services.datamart._datamart_service', None)
    def test_creates_new_instance_if_none_exists(self, mock_settings):
        """Debe crear nueva instancia si no existe"""
        from app.services import datamart
        datamart._datamart_service = None

        service = get_datamart_service()

        assert service is not None
        assert isinstance(service, DatamartService)
