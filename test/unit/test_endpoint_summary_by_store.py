import pytest
from datetime import date
from unittest.mock import Mock
from fastapi import HTTPException

from app.api.routes.summary import get_store_summary
from app.models.responses import StoreSummaryResponse, StoreSalesResponse, SaleRecord


@pytest.mark.unit
class TestStoreSummaryEndpoint:
    """Tests para endpoint get_store_summary"""

    @pytest.mark.asyncio
    async def test_endpoint_calls_service_with_store_key(self):
        """El endpoint debe llamar al servicio con key_store"""
        # Arrange
        mock_service = Mock()
        mock_service.get_store_summary.return_value = StoreSummaryResponse(
            success=True,
            key_store='1|023',
            total_amount=1000.0,
            average_amount=100.0,
            total_quantity=10,
            records_count=10
        )

        # Act
        result = await get_store_summary(
            key_store='1|023',
            datamart_service=mock_service
        )

        # Assert
        mock_service.get_store_summary.assert_called_once_with(key_store='1|023')

    @pytest.mark.asyncio
    async def test_endpoint_returns_store_summary_response(self):
        """El endpoint debe retornar StoreSummaryResponse"""
        # Arrange
        mock_service = Mock()
        expected_response = StoreSummaryResponse(
            success=True,
            key_store='1|023',
            total_amount=1000.0,
            average_amount=100.0,
            total_quantity=10,
            records_count=10
        )
        mock_service.get_store_summary.return_value = expected_response

        # Act
        result = await get_store_summary(
            key_store='1|023',
            datamart_service=mock_service
        )

        # Assert
        assert isinstance(result, StoreSummaryResponse)
        assert result.success is True


