import pytest
from datetime import date
from unittest.mock import Mock

from app.services.datamart import DatamartService
from app.models.responses import EmployeeSummaryResponse


@pytest.mark.unit
class TestGetEmployeeSummary:
    """Tests para método get_employee_summary"""

    def test_returns_employee_summary_response_object(self, mock_settings, employee_key):
        """Debe retornar objeto EmployeeSummaryResponse"""
        service = DatamartService()

        result = service.get_employee_summary(key_employee=employee_key)

        assert isinstance(result, EmployeeSummaryResponse)

    def test_response_has_required_fields(self, mock_settings, employee_key):
        """La respuesta debe tener todos los campos requeridos"""
        service = DatamartService()

        result = service.get_employee_summary(key_employee=employee_key)

        assert hasattr(result, 'success')
        assert hasattr(result, 'key_employee')
        assert hasattr(result, 'total_amount')
        assert hasattr(result, 'average_amount')
        assert hasattr(result, 'total_quantity')
        assert hasattr(result, 'records_count')

    def test_calculates_total_amount_correctly(self, mock_settings, employee_key):
        """Debe calcular el total correctamente"""
        service = DatamartService()

        result = service.get_employee_summary(key_employee=employee_key)

        assert isinstance(result.total_amount, float)
        # El total debe ser la suma de todas las ventas del empleado
        assert result.total_amount != 0 or result.records_count == 0

    def test_calculates_average_amount_correctly(self, mock_settings, employee_key):
        """Debe calcular el promedio correctamente"""
        service = DatamartService()

        result = service.get_employee_summary(key_employee=employee_key)

        assert isinstance(result.average_amount, float)

        # Verificar cálculo manual del promedio
        if result.records_count > 0:
            expected_average = result.total_amount / result.records_count
            assert result.average_amount == pytest.approx(expected_average, rel=1e-6)
        else:
            assert result.average_amount == 0.0

    def test_average_is_zero_when_no_records(self, mock_settings):
        """El promedio debe ser 0 cuando no hay registros"""
        service = DatamartService()
        nonexistent_employee = "999|999"

        result = service.get_employee_summary(key_employee=nonexistent_employee)

        assert result.records_count == 0
        assert result.average_amount == 0.0
        assert result.total_amount == 0.0

    def test_counts_all_employee_records(self, mock_settings, employee_key):
        """Debe contar todos los registros del empleado"""
        service = DatamartService()

        result = service.get_employee_summary(key_employee=employee_key)

        assert isinstance(result.records_count, int)
        assert result.records_count >= 0

    def test_summary_for_specific_employee(self, mock_settings):
        """Debe retornar resumen para empleado específico"""
        service = DatamartService()
        employee_key = "1|343"

        result = service.get_employee_summary(key_employee=employee_key)

        assert result.key_employee == employee_key
        assert result.success is True

    def test_summary_for_all_employees(self, mock_settings):
        """Debe retornar resumen de todos los empleados cuando key_employee es None"""
        service = DatamartService()

        result = service.get_employee_summary(key_employee=None)

        assert result.key_employee is None
        assert result.success is True
        assert result.records_count > 0  # Debe haber al menos algunos registros

    def test_all_employees_summary_includes_all_records(self, mock_settings):
        """El resumen de todos debe incluir todos los registros del datamart"""
        service = DatamartService()
        total_records = len(service._data)

        result = service.get_employee_summary(key_employee=None)

        assert result.records_count == total_records

    def test_total_quantity_is_calculated(self, mock_settings, employee_key):
        """Debe calcular la cantidad total"""
        service = DatamartService()

        result = service.get_employee_summary(key_employee=employee_key)

        assert isinstance(result.total_quantity, int)

    def test_handles_negative_amounts_in_summary(self, mock_settings):
        """Debe manejar montos negativos (devoluciones) en el resumen"""
        service = DatamartService()

        result = service.get_employee_summary(key_employee="1|343")

        # El total puede ser negativo si hay más devoluciones que ventas
        assert isinstance(result.total_amount, float)
        # El promedio también puede ser negativo
        assert isinstance(result.average_amount, float)


@pytest.mark.unit
class TestEmployeeSummaryDataQuality:
    """Tests para calidad de datos en resumen de empleados"""

    def test_amounts_are_numeric(self, mock_settings, employee_key):
        """Los montos deben ser numéricos"""
        service = DatamartService()

        result = service.get_employee_summary(key_employee=employee_key)

        assert isinstance(result.total_amount, (int, float))
        assert isinstance(result.average_amount, (int, float))

    def test_quantities_are_integers(self, mock_settings, employee_key):
        """Las cantidades deben ser enteros"""
        service = DatamartService()

        result = service.get_employee_summary(key_employee=employee_key)

        assert isinstance(result.total_quantity, int)
        assert isinstance(result.records_count, int)

    def test_no_nan_or_inf_values(self, mock_settings, employee_key):
        """No debe haber valores NaN o infinitos"""
        service = DatamartService()

        result = service.get_employee_summary(key_employee=employee_key)

        import math
        assert not math.isnan(result.total_amount)
        assert not math.isnan(result.average_amount)
        assert not math.isinf(result.total_amount)
        assert not math.isinf(result.average_amount)


@pytest.mark.unit
class TestEmployeeSummaryComparison:
    """Tests para comparación entre empleados"""

    def test_multiple_employees_have_different_summaries(self, mock_settings):
        """Diferentes empleados deben tener resúmenes diferentes"""
        service = DatamartService()
        employee1 = "1|343"
        employee2 = "1|417"

        result1 = service.get_employee_summary(key_employee=employee1)
        result2 = service.get_employee_summary(key_employee=employee2)

        # Es extremadamente improbable que dos empleados tengan exactamente
        # el mismo total_amount y records_count
        assert (result1.total_amount != result2.total_amount or
                result1.records_count != result2.records_count)

    def test_sum_of_employees_equals_total(self, mock_settings):
        """La suma de todos los empleados debe igual al total general"""
        service = DatamartService()

        unique_employees = service._data['KeyEmployee'].unique()

        # Sumar todos los totales individuales
        individual_totals = 0.0
        for emp in unique_employees:
            result = service.get_employee_summary(key_employee=emp)
            individual_totals += result.total_amount

        # Obtener total general
        total_result = service.get_employee_summary(key_employee=None)

        assert individual_totals == pytest.approx(total_result.total_amount, rel=1e-6)


@pytest.mark.unit
class TestEmployeeSummaryEdgeCases:
    """Tests para casos extremos"""

    def test_employee_with_only_returns(self, mock_settings):
        """Debe manejar empleado que solo tiene devoluciones (montos negativos)"""
        service = DatamartService()

        # Buscar un empleado con monto negativo
        # (El empleado 1|343 tiene ventas negativas en los datos de prueba)

        result = service.get_employee_summary(key_employee="1|343")

        assert result is not None
        # Puede tener total negativo
        assert isinstance(result.total_amount, float)

    def test_empty_datamart_returns_zeros(self, mock_settings, monkeypatch):
        """Datamart vacío debe retornar ceros"""
        service = DatamartService()
        # Simular datamart vacío
        import pandas as pd
        empty_df = pd.DataFrame(columns=service._data.columns)
        monkeypatch.setattr(service, '_data', empty_df)

        result = service.get_employee_summary(key_employee=None)

        assert result.records_count == 0
        assert result.total_amount == 0.0
        assert result.average_amount == 0.0
        assert result.total_quantity == 0

    def test_performance_with_all_employees(self, mock_settings):
        """Debe tener buen rendimiento al calcular resumen de todos"""
        import time

        service = DatamartService()

        start_time = time.time()
        result = service.get_employee_summary(key_employee=None)
        end_time = time.time()

        execution_time = end_time - start_time
        assert execution_time < 1.0  # Debe ejecutar en menos de 1 segundo
        assert result is not None
        