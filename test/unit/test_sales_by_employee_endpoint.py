import pytest
from datetime import date
from unittest.mock import Mock, patch
from fastapi import HTTPException

from app.api.routes.sales import get_sales_by_employee


@pytest.mark.unit
class TestSalesByEmployeeEndpoint:
    """Tests para endpoint get_sales_by_employee"""

    @pytest.mark.asyncio
    async def test_endpoint_calls_service_with_correct_params(self):
        """El endpoint debe llamar al servicio con los parámetros correctos"""
        # Arrange
        mock_service = Mock()
        mock_service.get_sales_by_employee.return_value = {
            'key_employee': '1|343',
            'date_start': date(2023, 11, 1),
            'date_end': date(2023, 11, 30),
            'total_amount': 1000.0,
            'total_quantity': 10,
            'records_count': 1,
            'sales': []
        }

        # Act
        result = await get_sales_by_employee(
            key_employee='1|343',
            date_start=date(2023, 11, 1),
            date_end=date(2023, 11, 30),
            datamart_service=mock_service
        )

        # Assert
        mock_service.get_sales_by_employee.assert_called_once_with(
            key_employee='1|343',
            date_start=date(2023, 11, 1),
            date_end=date(2023, 11, 30)
        )

    @pytest.mark.asyncio
    async def test_endpoint_returns_dict_with_success_flag(self):
        """El endpoint debe agregar flag 'success' a la respuesta"""
        # Arrange
        mock_service = Mock()
        mock_service.get_sales_by_employee.return_value = {
            'key_employee': '1|343',
            'total_amount': 1000.0,
            'sales': []
        }

        # Act
        result = await get_sales_by_employee(
            key_employee='1|343',
            date_start=date(2023, 11, 1),
            date_end=date(2023, 11, 30),
            datamart_service=mock_service
        )

        # Assert
        assert 'success' in result
        assert result['success'] is True

    @pytest.mark.asyncio
    async def test_endpoint_validates_date_range(self):
        """El endpoint debe validar que date_end >= date_start"""
        # Arrange
        mock_service = Mock()

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            await get_sales_by_employee(
                key_employee='1|343',
                date_start=date(2023, 1, 1),
                date_end=date(2023, 12, 31),
                datamart_service=mock_service
            )

        assert exc_info.value.status_code == 422
        assert "debe ser mayor o igual" in exc_info.value.detail

    @pytest.mark.asyncio
    async def test_endpoint_handles_service_value_error(self):
        """El endpoint debe manejar ValueError del servicio"""
        # Arrange
        mock_service = Mock()
        mock_service.get_sales_by_employee.side_effect = ValueError("Error de validación")

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            await get_sales_by_employee(
                key_employee='1|343',
                date_start=date(2023, 11, 1),
                date_end=date(2023, 11, 30),
                datamart_service=mock_service
            )

        assert exc_info.value.status_code == 422

    @pytest.mark.asyncio
    async def test_endpoint_handles_service_generic_error(self):
        """El endpoint debe manejar errores genéricos del servicio"""
        # Arrange
        mock_service = Mock()
        mock_service.get_sales_by_employee.side_effect = Exception("Error inesperado")

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            await get_sales_by_employee(
                key_employee='1|343',
                date_start=date(2023, 11, 1),
                date_end=date(2023, 11, 30),
                datamart_service=mock_service
            )

        assert exc_info.value.status_code == 500
        assert "Error al consultar ventas" in exc_info.value.detail

    @pytest.mark.asyncio
    async def test_endpoint_returns_all_service_data(self):
        """El endpoint debe retornar todos los datos del servicio"""
        # Arrange
        mock_service = Mock()
        expected_data = {
            'key_employee': '1|343',
            'date_start': date(2023, 11, 1),
            'date_end': date(2023, 11, 30),
            'total_amount': 1500.50,
            'total_quantity': 25,
            'records_count': 5,
            'sales': [
                {
                    'date': '2023-11-15',
                    'amount': 300.10,
                    'quantity': 5,
                    'ticket_id': 'T001'
                }
            ]
        }
        mock_service.get_sales_by_employee.return_value = expected_data

        # Act
        result = await get_sales_by_employee(
            key_employee='1|343',
            date_start=date(2023, 11, 1),
            date_end=date(2023, 11, 30),
            datamart_service=mock_service
        )

        # Assert
        assert result['key_employee'] == expected_data['key_employee']
        assert result['total_amount'] == expected_data['total_amount']
        assert result['total_quantity'] == expected_data['total_quantity']
        assert result['records_count'] == expected_data['records_count']
        assert result['sales'] == expected_data['sales']

    @pytest.mark.asyncio
    async def test_endpoint_accepts_valid_employee_key_format(self):
        """El endpoint debe aceptar formato correcto de KeyEmployee"""
        # Arrange
        mock_service = Mock()
        mock_service.get_sales_by_employee.return_value = {
            'key_employee': '1|343',
            'sales': []
        }

        valid_keys = ['1|343', '1|417', '2|100', '999|999']

        # Act & Assert
        for key in valid_keys:
            result = await get_sales_by_employee(
                key_employee=key,
                date_start=date(2023, 11, 1),
                date_end=date(2023, 11, 30),
                datamart_service=mock_service
            )
            assert result is not None