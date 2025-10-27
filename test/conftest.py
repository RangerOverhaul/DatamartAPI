import pytest
import pandas as pd
from datetime import date, datetime
from pathlib import Path
import os
from unittest.mock import Mock


@pytest.fixture(scope="session")
def test_datamart_dir():
    """Directorio de fixtures"""
    return Path(__file__).parent / "fixtures"


@pytest.fixture(scope="session")
def test_parquet_file(test_datamart_dir):
    """Ruta al archivo parquet de prueba"""
    return test_datamart_dir / "sample_datamart.parquet"


@pytest.fixture(scope="session")
def test_settings(test_datamart_dir):
    """Mock de settings para tests"""
    from unittest.mock import Mock

    settings_mock = Mock()
    settings_mock.DATAMART_PATH = str(test_datamart_dir)
    settings_mock.DEBUG = True
    settings_mock.get_parquet_files = lambda: [test_datamart_dir / "sample_datamart.parquet"]

    return settings_mock


@pytest.fixture
def sample_dataframe():
    """DataFrame de prueba con estructura del datamart"""
    data = {
        'KeySale': [
            '9AF8EF5C-9979-EE11-8C87-18473D93BB19|9BF8EF5C-9979-EE11-8C87-18473D93BB19',
            'FEC2A187-2083-EE11-8115-F4B520236BD7|FFC2A187-2083-EE11-8115-F4B520236BD7',
            '80FCC946-8484-EE11-9067-D39D90B09B04|81FCC946-8484-EE11-9067-D39D90B09B04',
            'TEST001|TEST001',
            'TEST002|TEST002'
        ],
        'KeyDate': pd.to_datetime([
            '2023-11-02',
            '2023-11-14',
            '2023-11-16',
            '2023-06-15',
            '2023-06-20'
        ]),
        'KeyStore': ['1|023', '1|007', '1|098', '1|023', '1|023'],
        'KeyEmployee': ['1|343', '1|417', '1|569', '1|343', '1|343'],
        'KeyProduct': ['1|44733', '1|61889', '1|42606', '1|101', '1|102'],
        'TicketId': [
            'N01-00000385',
            'N01-00000959',
            'F01-00070943',
            'N01-00001234',
            'N01-00001235'
        ],
        'Qty': [-4, -1, 1, 10, 15],
        'Amount': [-24873.95, -19243.7, 12184.87, 1500.50, 2300.00]
    }
    return pd.DataFrame(data)


@pytest.fixture
def employee_key():
    """Key de empleado de prueba"""
    return "1|343"


@pytest.fixture
def date_range():
    """Rango de fechas de prueba"""
    return {
        'start': date(2023, 11, 1),
        'end': date(2023, 11, 30)
    }


@pytest.fixture
def expected_employee_sales():
    """Ventas esperadas para empleado 1|343 en noviembre 2023"""
    return {
        'total_amount': -24873.95,
        'total_quantity': -4,
        'records_count': 1
    }

@pytest.fixture
def product_key():
    """Key de producto de prueba"""
    return "1|44733"

@pytest.fixture
def expected_product_sales():
    """Ventas esperadas para producto 1|44733 en noviembre 2023"""
    return {
        'total_amount': -24873.95,
        'total_quantity': -4,
        'records_count': 1
    }

@pytest.fixture
def mock_dataframe_empty():
    """DataFrame vacío"""
    return pd.DataFrame(columns=[
        'KeySale', 'KeyDate', 'KeyStore', 'KeyEmployee',
        'KeyProduct', 'TicketId', 'Qty', 'Amount'
    ])


@pytest.fixture
def mock_settings(monkeypatch, test_datamart_dir):
    """Mock de settings usando monkeypatch"""

    class MockSettings:
        DATAMART_PATH = str(test_datamart_dir)
        DEBUG = True
        BASE_DIR = Path(__file__).parent.parent

        def get_parquet_files(self):
            return [test_datamart_dir / "sample_datamart.parquet"]

    mock = MockSettings()

    # Patchear el módulo config
    monkeypatch.setattr("app.config.settings", mock)

    return mock

@pytest.fixture
def store_key():
    """Key de tienda de prueba"""
    return "1|023"


@pytest.fixture
def expected_store_sales():
    """Ventas esperadas para tienda 1|023 en noviembre 2023"""
    return {
        'total_amount': -24873.95 + 5000.00,  # Suma de las ventas de noviembre para store 1|023
        'total_quantity': -4 + 5,  # Suma de las cantidades
        'records_count': 2  # Dos registros en noviembre para store 1|023
    }


@pytest.fixture
def store_sales_data():
    """Datos específicos para pruebas de ventas por tienda"""
    return {
        'store_key': '1|023',
        'date_start': date(2023, 11, 1),
        'date_end': date(2023, 11, 30),
        'expected_total_amount': -24873.95 + 5000.00,
        'expected_total_quantity': 1,
        'expected_records_count': 2
    }


@pytest.fixture
def multiple_stores_data():
    """Datos con múltiples tiendas para pruebas"""
    return {
        'stores': ['1|023', '1|007', '1|098'],
        'store_sales_counts': {'1|023': 2, '1|007': 2, '1|098': 1}  # Conteo en el sample_dataframe
    }

@pytest.fixture
def store_with_no_sales():
    """Key de tienda sin ventas"""
    return "999|999"

@pytest.fixture
def store_sales_november_range():
    """Rango específico para pruebas de tienda en noviembre"""
    return {
        'start': date(2023, 11, 1),
        'end': date(2023, 11, 30),
        'store_key': '1|023',
        'expected_sales_count': 2
    }


@pytest.fixture
def store_sales_june_range():
    """Rango específico para pruebas de tienda en junio"""
    return {
        'start': date(2023, 6, 1),
        'end': date(2023, 6, 30),
        'store_key': '1|023',
        'expected_sales_count': 2
    }


@pytest.fixture
def store_sales_single_day():
    """Prueba para un solo día"""
    return {
        'start': date(2023, 11, 2),
        'end': date(2023, 11, 2),
        'store_key': '1|023',
        'expected_sales_count': 1
    }

@pytest.fixture
def expected_employee_summary():
    """Resumen esperado para empleado 1|343"""
    return {
        'total_amount': -23373.45,  # Ajustar según datos reales
        'average_amount': -11686.725,
        'records_count': 2
    }

# ============= CONFIGURACIÓN DE AMBIENTE =============

@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Configuración automática del ambiente de test"""
    os.environ["TESTING"] = "true"
    os.environ["DEBUG"] = "true"

    yield

    # Limpieza
    os.environ.pop("TESTING", None)