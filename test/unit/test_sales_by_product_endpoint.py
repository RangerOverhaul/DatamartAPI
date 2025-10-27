import pytest
from datetime import date
from unittest.mock import Mock
from fastapi import HTTPException

from app.api.routes.sales import get_sales_by_product
from app.models.responses import ProductSalesResponse, SaleRecord


@pytest.mark.unit
class TestSalesByProductEndpoint:
    """Tests para endpoint get_sales_by_product"""

    @pytest.mark.asyncio
    async def test_endpoint_calls_service_with_correct_params(self):
        """El endpoint debe llamar al servicio con los parámetros correctos"""
        # Arrange
        mock_service = Mock()
        mock_service.get_sales_by_product.return_value = ProductSalesResponse(
            success=True,
            key_product='1|44733',
            date_start=date(2023, 11, 1),
            date_end=date(2023, 11, 30),
            total_amount=1000.0,
            total_quantity=10,
            records_count=1,
            sales=[]
        )

        # Act
        result = await get_sales_by_product(
            key_product='1|44733',
            date_start=date(2023, 11, 1),
            date_end=date(2023, 11, 30),
            datamart_service=mock_service
        )

        # Assert
        mock_service.get_sales_by_product.assert_called_once_with(
            key_product='1|44733',
            date_start=date(2023, 11, 1),
            date_end=date(2023, 11, 30)
        )

    @pytest.mark.asyncio
    async def test_endpoint_returns_product_sales_response(self):
        """El endpoint debe retornar ProductSalesResponse"""
        # Arrange
        mock_service = Mock()
        expected_response = ProductSalesResponse(
            success=True,
            key_product='1|44733',
            date_start=date(2023, 11, 1),
            date_end=date(2023, 11, 30),
            total_amount=1000.0,
            total_quantity=10,
            records_count=1,
            sales=[]
        )
        mock_service.get_sales_by_product.return_value = expected_response

        # Act
        result = await get_sales_by_product(
            key_product='1|44733',
            date_start=date(2023, 11, 1),
            date_end=date(2023, 11, 30),
            datamart_service=mock_service
        )

        # Assert
        assert isinstance(result, ProductSalesResponse)
        assert result.success is True
        assert result.key_product == '1|44733'

    @pytest.mark.asyncio
    async def test_endpoint_validates_date_range(self):
        """El endpoint debe validar que date_end >= date_start"""
        # Arrange
        mock_service = Mock()

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            await get_sales_by_product(
                key_product='1|44733',
                date_start=date(2023, 12, 31),
                date_end=date(2023, 1, 1),
                datamart_service=mock_service
            )

        assert exc_info.value.status_code == 422
        assert "debe ser mayor o igual" in exc_info.value.detail

    @pytest.mark.asyncio
    async def test_endpoint_handles_service_value_error(self):
        """El endpoint debe manejar ValueError del servicio"""
        # Arrange
        mock_service = Mock()
        mock_service.get_sales_by_product.side_effect = ValueError("Error de validación")

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            await get_sales_by_product(
                key_product='1|44733',
                date_start=date(2023, 11, 1),
                date_end=date(2023, 11, 30),
                datamart_service=mock_service
            )

        assert exc_info.value.status_code == 422
        assert "Error de validación" in exc_info.value.detail

    @pytest.mark.asyncio
    async def test_endpoint_handles_service_generic_error(self):
        """El endpoint debe manejar errores genéricos del servicio"""
        # Arrange
        mock_service = Mock()
        mock_service.get_sales_by_product.side_effect = Exception("Error inesperado")

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            await get_sales_by_product(
                key_product='1|44733',
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
        expected_data = ProductSalesResponse(
            success=True,
            key_product='1|44733',
            date_start=date(2023, 11, 1),
            date_end=date(2023, 11, 30),
            total_amount=1500.50,
            total_quantity=25,
            records_count=5,
            sales=[
                SaleRecord(
                    date=date(2023, 11, 15),
                    amount=300.10,
                    quantity=5,
                    ticket_id='T001',
                    product='1|44733',
                    store='1|023'
                )
            ]
        )
        mock_service.get_sales_by_product.return_value = expected_data

        # Act
        result = await get_sales_by_product(key_product='1|44733',
            date_start=date(2023, 11, 1),
            date_end=date(2023, 11, 30),
            datamart_service=mock_service)

        # Assert
        assert result['key_product'] == expected_data['key_product']
        assert result['total_amount'] == expected_data['total_amount']
        assert result['total_quantity'] == expected_data['total_quantity']
        assert result['records_count'] == expected_data['records_count']
        assert result['sales'] == expected_data['sales']
