# tests/unit/test_sales_endpoint_product_summary.py
"""
Unit tests para endpoint de resumen de ventas por producto.
"""
import pytest
from unittest.mock import Mock
from fastapi import HTTPException

from app.api.routes.sales import get_product_summary
from app.models.responses import ProductSummaryResponse


@pytest.mark.unit
class TestProductSummaryEndpoint:
    """Tests para endpoint get_product_summary"""

    @pytest.mark.asyncio
    async def test_endpoint_calls_service_with_product_key(self):
        """El endpoint debe llamar al servicio con key_product"""
        # Arrange
        mock_service = Mock()
        mock_service.get_product_summary.return_value = ProductSummaryResponse(
            success=True,
            key_product='1|44733',
            total_amount=1000.0,
            average_amount=100.0,
            total_quantity=10,
            records_count=10
        )

        # Act
        result = await get_product_summary(
            key_product='1|44733',
            datamart_service=mock_service
        )

        # Assert
        mock_service.get_product_summary.assert_called_once_with(
            key_product='1|44733'
        )

    @pytest.mark.asyncio
    async def test_endpoint_calls_service_without_product_key(self):
        """El endpoint debe llamar al servicio con None cuando no se especifica producto"""
        # Arrange
        mock_service = Mock()
        mock_service.get_product_summary.return_value = ProductSummaryResponse(
            success=True,
            key_product=None,
            total_amount=10000.0,
            average_amount=100.0,
            total_quantity=100,
            records_count=100
        )

        # Act
        result = await get_product_summary(
            key_product=None,
            datamart_service=mock_service
        )

        # Assert
        mock_service.get_product_summary.assert_called_once_with(
            key_product=None
        )

    @pytest.mark.asyncio
    async def test_endpoint_returns_product_summary_response(self):
        """El endpoint debe retornar ProductSummaryResponse"""
        # Arrange
        mock_service = Mock()
        expected_response = ProductSummaryResponse(
            success=True,
            key_product='1|44733',
            total_amount=1000.0,
            average_amount=100.0,
            total_quantity=10,
            records_count=10
        )
        mock_service.get_product_summary.return_value = expected_response

        # Act
        result = await get_product_summary(
            key_product='1|44733',
            datamart_service=mock_service
        )

        # Assert
        assert isinstance(result, ProductSummaryResponse)
        assert result.success is True
        assert result.key_product == '1|44733'

    @pytest.mark.asyncio
    async def test_endpoint_handles_service_generic_error(self):
        """El endpoint debe manejar errores genéricos del servicio"""
        # Arrange
        mock_service = Mock()
        mock_service.get_product_summary.side_effect = Exception("Error inesperado")

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            await get_product_summary(
                key_product='1|44733',
                datamart_service=mock_service
            )

        assert exc_info.value.status_code == 500
        assert "Error al calcular resumen" in exc_info.value.detail

    @pytest.mark.asyncio
    async def test_endpoint_returns_all_summary_fields(self):
        """El endpoint debe retornar todos los campos del resumen"""
        # Arrange
        mock_service = Mock()
        expected_data = ProductSummaryResponse(
            success=True,
            key_product='1|44733',
            total_amount=1500.50,
            average_amount=150.05,
            total_quantity=25,
            records_count=10
        )
        mock_service.get_product_summary.return_value = expected_data

        # Act
        result = await get_product_summary(
            key_product='1|44733',
            datamart_service=mock_service
        )

        # Assert
        assert result.total_amount == 1500.50
        assert result.average_amount == 150.05
        assert result.total_quantity == 25
        assert result.records_count == 10

    @pytest.mark.asyncio
    async def test_endpoint_handles_nonexistent_product(self):
        """El endpoint debe manejar producto inexistente correctamente"""
        # Arrange
        mock_service = Mock()
        mock_service.get_product_summary.return_value = ProductSummaryResponse(
            success=True,
            key_product='999|99999',
            total_amount=0.0,
            average_amount=0.0,
            total_quantity=0,
            records_count=0
        )

        # Act
        result = await get_product_summary(
            key_product='999|99999',
            datamart_service=mock_service
        )

        # Assert
        assert result.records_count == 0
        assert result.total_amount == 0.0
        assert result.average_amount == 0.0

    @pytest.mark.asyncio
    async def test_endpoint_accepts_optional_product_key(self):
        """El endpoint debe aceptar key_product como opcional"""
        # Arrange
        mock_service = Mock()
        mock_service.get_product_summary.return_value = ProductSummaryResponse(
            success=True,
            key_product=None,
            total_amount=50000.0,
            average_amount=500.0,
            total_quantity=1000,
            records_count=100
        )

        # Act
        result = await get_product_summary(
            key_product=None,
            datamart_service=mock_service
        )

        # Assert
        assert result.key_product is None
        assert result.success is True


@pytest.mark.unit
class TestProductSummaryValidation:
    """Tests para validación de datos del endpoint"""

    @pytest.mark.asyncio
    async def test_response_has_numeric_totals(self):
        """La respuesta debe tener totales numéricos"""
        # Arrange
        mock_service = Mock()
        mock_service.get_product_summary.return_value = ProductSummaryResponse(
            success=True,
            key_product='1|44733',
            total_amount=1000.0,
            average_amount=100.0,
            total_quantity=10,
            records_count=10
        )

        # Act
        result = await get_product_summary(
            key_product='1|44733',
            datamart_service=mock_service
        )

        assert isinstance(result.total_amount, (int, float))
        assert isinstance(result.average_amount, (int, float))
        assert isinstance(result.total_quantity, int)
        assert isinstance(result.records_count, int)
