import pytest
from unittest.mock import Mock
from fastapi import HTTPException

from app.api.routes.sales import get_employee_summary
from app.models.responses import EmployeeSummaryResponse


@pytest.mark.unit
class TestEmployeeSummaryEndpoint:
    """Tests para endpoint get_employee_summary"""

    @pytest.mark.asyncio
    async def test_endpoint_calls_service_with_employee_key(self):
        """El endpoint debe llamar al servicio con key_employee"""
        mock_service = Mock()
        mock_service.get_employee_summary.return_value = EmployeeSummaryResponse(
            success=True,
            key_employee='1|343',
            total_amount=1000.0,
            average_amount=100.0,
            total_quantity=10,
            records_count=10
        )

        result = await get_employee_summary(
            key_employee='1|343',
            datamart_service=mock_service
        )

        mock_service.get_employee_summary.assert_called_once_with(
            key_employee='1|343'
        )

    @pytest.mark.asyncio
    async def test_endpoint_calls_service_without_employee_key(self):
        """El endpoint debe llamar al servicio con None cuando no se especifica empleado"""
        mock_service = Mock()
        mock_service.get_employee_summary.return_value = EmployeeSummaryResponse(
            success=True,
            key_employee=None,
            total_amount=10000.0,
            average_amount=100.0,
            total_quantity=100,
            records_count=100
        )

        result = await get_employee_summary(
            key_employee=None,
            datamart_service=mock_service
        )

        mock_service.get_employee_summary.assert_called_once_with(
            key_employee=None
        )

    @pytest.mark.asyncio
    async def test_endpoint_returns_employee_summary_response(self):
        """El endpoint debe retornar EmployeeSummaryResponse"""

        mock_service = Mock()
        expected_response = EmployeeSummaryResponse(
            success=True,
            key_employee='1|343',
            total_amount=1000.0,
            average_amount=100.0,
            total_quantity=10,
            records_count=10
        )
        mock_service.get_employee_summary.return_value = expected_response

        result = await get_employee_summary(
            key_employee='1|343',
            datamart_service=mock_service
        )

        assert isinstance(result, EmployeeSummaryResponse)
        assert result.success is True
        assert result.key_employee == '1|343'

    @pytest.mark.asyncio
    async def test_endpoint_handles_service_generic_error(self):
        """El endpoint debe manejar errores genéricos del servicio"""
        mock_service = Mock()
        mock_service.get_employee_summary.side_effect = Exception("Error inesperado")

        with pytest.raises(HTTPException) as exc_info:
            await get_employee_summary(
                key_employee='1|343',
                datamart_service=mock_service
            )

        assert exc_info.value.status_code == 500
        assert "Error al calcular resumen" in exc_info.value.detail

    @pytest.mark.asyncio
    async def test_endpoint_returns_all_summary_fields(self):
        """El endpoint debe retornar todos los campos del resumen"""
        mock_service = Mock()
        expected_data = EmployeeSummaryResponse(
            success=True,
            key_employee='1|343',
            total_amount=1500.50,
            average_amount=150.05,
            total_quantity=25,
            records_count=10
        )
        mock_service.get_employee_summary.return_value = expected_data

        result = await get_employee_summary(
            key_employee='1|343',
            datamart_service=mock_service
        )

        assert result.total_amount == 1500.50
        assert result.average_amount == 150.05
        assert result.total_quantity == 25
        assert result.records_count == 10

    @pytest.mark.asyncio
    async def test_endpoint_handles_nonexistent_employee(self):
        """El endpoint debe manejar empleado inexistente correctamente"""
        mock_service = Mock()
        mock_service.get_employee_summary.return_value = EmployeeSummaryResponse(
            success=True,
            key_employee='999|999',
            total_amount=0.0,
            average_amount=0.0,
            total_quantity=0,
            records_count=0
        )

        result = await get_employee_summary(
            key_employee='999|999',
            datamart_service=mock_service
        )

        assert result.records_count == 0
        assert result.total_amount == 0.0
        assert result.average_amount == 0.0

    @pytest.mark.asyncio
    async def test_endpoint_accepts_optional_employee_key(self):
        """El endpoint debe aceptar key_employee como opcional"""
        mock_service = Mock()
        mock_service.get_employee_summary.return_value = EmployeeSummaryResponse(
            success=True,
            key_employee=None,
            total_amount=50000.0,
            average_amount=500.0,
            total_quantity=1000,
            records_count=100
        )

        result = await get_employee_summary(
            key_employee=None,
            datamart_service=mock_service
        )

        assert result.key_employee is None
        assert result.success is True


@pytest.mark.unit
class TestEmployeeSummaryValidation:
    """Tests para validación de datos del endpoint"""

    @pytest.mark.asyncio
    async def test_response_has_numeric_totals(self):
        """La respuesta debe tener totales numéricos"""
        mock_service = Mock()
        mock_service.get_employee_summary.return_value = EmployeeSummaryResponse(
            success=True,
            key_employee='1|343',
            total_amount=1000.0,
            average_amount=100.0,
            total_quantity=10,
            records_count=10
        )

        result = await get_employee_summary(
            key_employee='1|343',
            datamart_service=mock_service
        )

        assert isinstance(result.total_amount, (int, float))
        assert isinstance(result.average_amount, (int, float))
        assert isinstance(result.total_quantity, int)
        assert isinstance(result.records_count, int)

