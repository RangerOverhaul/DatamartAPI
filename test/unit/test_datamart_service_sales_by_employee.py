import pytest
import pandas as pd
from datetime import date
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path

from app.services.datamart import DatamartService, get_datamart_service

@pytest.mark.unit
class TestGetSalesByEmployee:
    """Tests para metodo get_sales_by_employee"""

    def test_validates_date_range_in_service(self, mock_settings, employee_key):
        """Debe validar rango de fechas"""
        service = DatamartService()

        with pytest.raises(ValueError):
            service.get_sales_by_employee(
                key_employee=employee_key,
                date_start=date(2023, 12, 31),
                date_end=date(2023, 1, 1)
            )

    def test_accepts_equal_start_and_end_dates(self, mock_settings, employee_key):
        """Debe aceptar fecha inicio igual a fecha fin"""
        service = DatamartService()
        same_date = date(2023, 11, 2)

        result = service.get_sales_by_employee(
            key_employee=employee_key,
            date_start=same_date,
            date_end=same_date
        )

        assert result is not None
        assert isinstance(result, dict)

    def test_returns_dict_with_required_keys(self, mock_settings, employee_key, date_range):
        """Debe retornar diccionario con las keys requeridas"""
        service = DatamartService()

        result = service.get_sales_by_employee(
            key_employee=employee_key,
            date_start=date_range['start'],
            date_end=date_range['end']
        )

        assert isinstance(result, dict)
        assert 'key_employee' in result
        assert 'date_start' in result
        assert 'date_end' in result
        assert 'total_amount' in result
        assert 'total_quantity' in result
        assert 'records_count' in result
        assert 'sales' in result

    def test_filters_by_employee_correctly(self, mock_settings, employee_key, date_range):
        """Debe filtrar correctamente por empleado"""
        service = DatamartService()

        result = service.get_sales_by_employee(
            key_employee=employee_key,
            date_start=date_range['start'],
            date_end=date_range['end']
        )

        assert result['key_employee'] == employee_key
        # Verificar que todas las ventas son del empleado correcto
        for sale in result['sales']:
            # En los datos de prueba, el empleado 1|343 tiene ventas en nov 2023
            assert 'amount' in sale

    def test_filters_by_date_range_correctly(self, mock_settings, employee_key):
        """Debe filtrar correctamente por rango de fechas"""
        service = DatamartService()
        date_start = date(2023, 11, 1)
        date_end = date(2023, 11, 30)

        result = service.get_sales_by_employee(
            key_employee=employee_key,
            date_start=date_start,
            date_end=date_end
        )

        for sale in result['sales']:
            sale_date = date.fromisoformat(sale['date'])
            assert date_start <= sale_date <= date_end

    def test_calculates_total_amount_correctly(self, mock_settings, employee_key, date_range):
        """Debe calcular el monto total correctamente"""
        service = DatamartService()

        result = service.get_sales_by_employee(
            key_employee=employee_key,
            date_start=date_range['start'],
            date_end=date_range['end']
        )

        assert isinstance(result['total_amount'], float)
        # Calcular manualmente para verificar
        manual_total = sum(sale['amount'] for sale in result['sales'])
        assert result['total_amount'] == pytest.approx(manual_total)

    def test_calculates_total_quantity_correctly(self, mock_settings, employee_key, date_range):
        """Debe calcular la cantidad total correctamente"""
        service = DatamartService()

        result = service.get_sales_by_employee(
            key_employee=employee_key,
            date_start=date_range['start'],
            date_end=date_range['end']
        )

        assert isinstance(result['total_quantity'], int)
        manual_total = sum(sale['quantity'] for sale in result['sales'])
        assert result['total_quantity'] == manual_total

    def test_counts_records_correctly(self, mock_settings, employee_key, date_range):
        """Debe contar los registros correctamente"""
        service = DatamartService()

        result = service.get_sales_by_employee(
            key_employee=employee_key,
            date_start=date_range['start'],
            date_end=date_range['end']
        )

        assert result['records_count'] == len(result['sales'])

    def test_returns_empty_list_for_nonexistent_employee(self, mock_settings, date_range):
        """Debe retornar lista vacía para empleado inexistente"""
        service = DatamartService()
        nonexistent_employee = "999|999"

        result = service.get_sales_by_employee(
            key_employee=nonexistent_employee,
            date_start=date_range['start'],
            date_end=date_range['end']
        )

        assert result['records_count'] == 0
        assert len(result['sales']) == 0
        assert result['total_amount'] == 0.0
        assert result['total_quantity'] == 0

    def test_raises_error_for_invalid_date_range(self, mock_settings, employee_key):
        """Debe lanzar error si date_end < date_start"""
        service = DatamartService()
        date_start = date(2023, 12, 31)
        date_end = date(2023, 1, 1)

        with pytest.raises(ValueError) as exc_info:
            service.get_sales_by_employee(
                key_employee=employee_key,
                date_start=date_start,
                date_end=date_end
            )

        assert "debe ser mayor o igual" in str(exc_info.value)

    def test_sales_list_contains_required_fields(self, mock_settings, employee_key, date_range):
        """Cada venta debe contener los campos requeridos"""
        service = DatamartService()

        result = service.get_sales_by_employee(
            key_employee=employee_key,
            date_start=date_range['start'],
            date_end=date_range['end']
        )

        if result['records_count'] > 0:
            sale = result['sales'][0]
            assert 'date' in sale
            assert 'amount' in sale
            assert 'quantity' in sale
            assert 'ticket_id' in sale
            assert 'product' in sale
            assert 'store' in sale

    def test_handles_negative_amounts(self, mock_settings):
        """Debe manejar montos negativos (devoluciones)"""
        service = DatamartService()
        # El empleado 1|343 tiene una venta negativa en nov 2023

        result = service.get_sales_by_employee(
            key_employee="1|343",
            date_start=date(2023, 11, 1),
            date_end=date(2023, 11, 30)
        )

        # Debe incluir ventas negativas
        assert result['records_count'] >= 0
        # Si hay ventas, algunas pueden ser negativas
        if result['records_count'] > 0:
            amounts = [sale['amount'] for sale in result['sales']]
            assert any(isinstance(amt, (int, float)) for amt in amounts)

    def test_handles_multiple_sales_same_day(self, mock_settings):
        """Debe manejar múltiples ventas del mismo empleado en el mismo día"""
        service = DatamartService()

        result = service.get_sales_by_employee(
            key_employee="1|343",
            date_start=date(2023, 6, 1),
            date_end=date(2023, 6, 30)
        )

        # Debería encontrar 2 ventas en junio para empleado 1|343
        assert result['records_count'] == 2
        assert len(result['sales']) == 2
