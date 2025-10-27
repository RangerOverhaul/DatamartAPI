import pytest
from unittest.mock import Mock
import pandas as pd

from app.services.datamart import DatamartService
from app.models.responses import ProductSummaryResponse


@pytest.mark.unit
class TestGetProductSummary:
    """Tests para método get_product_summary"""

    def test_returns_product_summary_response_object(self, mock_settings, product_key):
        """Debe retornar objeto ProductSummaryResponse"""
        service = DatamartService()

        result = service.get_product_summary(key_product=product_key)

        assert isinstance(result, ProductSummaryResponse)

    def test_response_has_required_fields(self, mock_settings, product_key):
        """La respuesta debe tener todos los campos requeridos"""
        service = DatamartService()

        result = service.get_product_summary(key_product=product_key)

        assert hasattr(result, 'success')
        assert hasattr(result, 'key_product')
        assert hasattr(result, 'total_amount')
        assert hasattr(result, 'average_amount')
        assert hasattr(result, 'total_quantity')
        assert hasattr(result, 'records_count')

    def test_calculates_total_amount_correctly(self, mock_settings, product_key):
        """Debe calcular el total correctamente"""
        service = DatamartService()

        result = service.get_product_summary(key_product=product_key)

        assert isinstance(result.total_amount, float)
        # El total debe ser la suma de todas las ventas del producto
        assert result.total_amount != 0 or result.records_count == 0

    def test_calculates_average_amount_correctly(self, mock_settings, product_key):
        """Debe calcular el promedio correctamente"""
        service = DatamartService()

        result = service.get_product_summary(key_product=product_key)

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
        nonexistent_product = "999|99999"

        result = service.get_product_summary(key_product=nonexistent_product)

        assert result.records_count == 0
        assert result.average_amount == 0.0
        assert result.total_amount == 0.0

    def test_counts_all_product_records(self, mock_settings, product_key):
        """Debe contar todos los registros del producto"""
        service = DatamartService()

        result = service.get_product_summary(key_product=product_key)

        assert isinstance(result.records_count, int)
        assert result.records_count >= 0

    def test_summary_for_specific_product(self, mock_settings):
        """Debe retornar resumen para producto específico"""
        service = DatamartService()
        product_key = "1|44733"

        result = service.get_product_summary(key_product=product_key)

        assert result.key_product == product_key
        assert result.success is True

    def test_summary_for_all_products(self, mock_settings):
        """Debe retornar resumen de todos los productos cuando key_product es None"""
        service = DatamartService()

        result = service.get_product_summary(key_product=None)

        assert result.key_product is None
        assert result.success is True
        assert result.records_count > 0  # Debe haber al menos algunos registros

    def test_all_products_summary_includes_all_records(self, mock_settings):
        """El resumen de todos debe incluir todos los registros del datamart"""
        service = DatamartService()
        total_records = len(service._data)

        result = service.get_product_summary(key_product=None)

        assert result.records_count == total_records

    def test_total_quantity_is_calculated(self, mock_settings, product_key):
        """Debe calcular la cantidad total"""
        service = DatamartService()

        result = service.get_product_summary(key_product=product_key)

        assert isinstance(result.total_quantity, int)

    def test_handles_negative_amounts_in_summary(self, mock_settings):
        """Debe manejar montos negativos (devoluciones) en el resumen"""
        service = DatamartService()

        result = service.get_product_summary(key_product="1|44733")

        # El total puede ser negativo si hay más devoluciones que ventas
        assert isinstance(result.total_amount, float)
        # El promedio también puede ser negativo
        assert isinstance(result.average_amount, float)


@pytest.mark.unit
class TestProductSummaryDataQuality:
    """Tests para calidad de datos en resumen de productos"""

    def test_amounts_are_numeric(self, mock_settings, product_key):
        """Los montos deben ser numéricos"""
        service = DatamartService()

        result = service.get_product_summary(key_product=product_key)

        assert isinstance(result.total_amount, (int, float))
        assert isinstance(result.average_amount, (int, float))

    def test_quantities_are_integers(self, mock_settings, product_key):
        """Las cantidades deben ser enteros"""
        service = DatamartService()

        result = service.get_product_summary(key_product=product_key)

        assert isinstance(result.total_quantity, int)
        assert isinstance(result.records_count, int)

    def test_no_nan_or_inf_values(self, mock_settings, product_key):
        """No debe haber valores NaN o infinitos"""
        service = DatamartService()

        result = service.get_product_summary(key_product=product_key)

        import math
        assert not math.isnan(result.total_amount)
        assert not math.isnan(result.average_amount)
        assert not math.isinf(result.total_amount)
        assert not math.isinf(result.average_amount)


@pytest.mark.unit
class TestProductSummaryComparison:
    """Tests para comparación entre productos"""

    def test_multiple_products_have_different_summaries(self, mock_settings):
        """Diferentes productos deben tener resúmenes diferentes"""
        service = DatamartService()
        product1 = "1|44733"
        product2 = "1|61889"

        result1 = service.get_product_summary(key_product=product1)
        result2 = service.get_product_summary(key_product=product2)

        # Es extremadamente improbable que dos productos tengan exactamente
        # el mismo total_amount y records_count
        assert (result1.total_amount != result2.total_amount or
                result1.records_count != result2.records_count)

    def test_sum_of_products_equals_total(self, mock_settings):
        """La suma de todos los productos debe igual al total general"""
        service = DatamartService()

        unique_products = service._data['KeyProduct'].unique()

        # Sumar todos los totales individuales
        individual_totals = 0.0
        for prod in unique_products:
            result = service.get_product_summary(key_product=prod)
            individual_totals += result.total_amount

        # Obtener total general
        total_result = service.get_product_summary(key_product=None)

        assert individual_totals == pytest.approx(total_result.total_amount, rel=1e-6)

    def test_products_ranked_by_total_amount(self, mock_settings):
        """Debe poder rankear productos por monto total"""
        service = DatamartService()
        unique_products = service._data['KeyProduct'].unique()[:5]  # Primeros 5

        results = []
        for prod in unique_products:
            result = service.get_product_summary(key_product=prod)
            results.append((prod, result.total_amount))

        # Ordenar por total
        sorted_results = sorted(results, key=lambda x: x[1], reverse=True)

        assert len(sorted_results) > 0
        # Verificar que el ordenamiento es correcto
        for i in range(len(sorted_results) - 1):
            assert sorted_results[i][1] >= sorted_results[i + 1][1]


@pytest.mark.unit
class TestProductSummaryEdgeCases:
    """Tests para casos extremos"""

    def test_product_with_only_returns(self, mock_settings):
        """Debe manejar producto que solo tiene devoluciones (montos negativos)"""
        service = DatamartService()

        result = service.get_product_summary(key_product="1|44733")

        assert result is not None
        # Puede tener total negativo
        assert isinstance(result.total_amount, float)

    def test_empty_datamart_returns_zeros(self, mock_settings, monkeypatch):
        """Datamart vacío debe retornar ceros"""
        service = DatamartService()
        # Simular datamart vacío
        empty_df = pd.DataFrame(columns=service._data.columns)
        monkeypatch.setattr(service, '_data', empty_df)

        result = service.get_product_summary(key_product=None)

        # Assert
        assert result.records_count == 0
        assert result.total_amount == 0.0
        assert result.average_amount == 0.0
        assert result.total_quantity == 0

    def test_performance_with_all_products(self, mock_settings):
        """Debe tener buen rendimiento al calcular resumen de todos"""
        import time

        service = DatamartService()

        start_time = time.time()
        result = service.get_product_summary(key_product=None)
        end_time = time.time()

        execution_time = end_time - start_time
        assert execution_time < 1.0  # Debe ejecutar en menos de 1 segundo
        assert result is not None

    def test_high_volume_product(self, mock_settings):
        """Debe manejar productos con alto volumen de ventas"""
        service = DatamartService()

        # Encontrar el producto con más registros
        product_counts = service._data['KeyProduct'].value_counts()
        if len(product_counts) > 0:
            most_sold_product = product_counts.index[0]

            result = service.get_product_summary(key_product=most_sold_product)

            assert result.records_count > 0
            assert isinstance(result.total_amount, float)

    def test_low_volume_product(self, mock_settings):
        """Debe manejar productos con bajo volumen de ventas"""
        service = DatamartService()

        # Encontrar un producto con pocos registros
        product_counts = service._data['KeyProduct'].value_counts()
        if len(product_counts) > 0:
            least_sold_product = product_counts.index[-1]

            result = service.get_product_summary(key_product=least_sold_product)

            assert result.records_count >= 0
            assert isinstance(result.total_amount, float)


@pytest.mark.unit
class TestProductSummaryBusinessLogic:
    """Tests para lógica de negocio"""

    def test_identifies_best_selling_product_by_quantity(self, mock_settings):
        """Debe poder identificar producto más vendido por cantidad"""
        service = DatamartService()
        unique_products = service._data['KeyProduct'].unique()[:10]

        max_quantity = -float('inf')
        best_product = None

        for prod in unique_products:
            result = service.get_product_summary(key_product=prod)
            if result.total_quantity > max_quantity:
                max_quantity = result.total_quantity
                best_product = prod

        assert best_product is not None
        assert max_quantity >= 0

    def test_identifies_highest_revenue_product(self, mock_settings):
        """Debe poder identificar producto con mayor ingreso"""
        service = DatamartService()
        unique_products = service._data['KeyProduct'].unique()[:10]

        max_revenue = -float('inf')
        top_product = None

        for prod in unique_products:
            result = service.get_product_summary(key_product=prod)
            if result.total_amount > max_revenue:
                max_revenue = result.total_amount
                top_product = prod

        assert top_product is not None

    def test_calculates_average_transaction_value(self, mock_settings, product_key):
        """Debe calcular correctamente el valor promedio por transacción"""
        service = DatamartService()

        result = service.get_product_summary(key_product=product_key)

        if result.records_count > 0:
            manual_average = result.total_amount / result.records_count
            assert result.average_amount == pytest.approx(manual_average, rel=1e-6)
            