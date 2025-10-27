import pandas as pd
from datetime import datetime

# Datos de prueba basados en la estructura real
test_data = {
    'KeySale': [
        '9AF8EF5C-9979-EE11-8C87-18473D93BB19|9BF8EF5C-9979-EE11-8C87-18473D93BB19',
        'FEC2A187-2083-EE11-8115-F4B520236BD7|FFC2A187-2083-EE11-8115-F4B520236BD7',
        '80FCC946-8484-EE11-9067-D39D90B09B04|81FCC946-8484-EE11-9067-D39D90B09B04',
        'TEST001|TEST001',
        'TEST002|TEST002'
    ],
    'KeyDate': [
        '2023-11-02',
        '2023-11-14',
        '2023-11-16',
        '2023-06-15',
        '2023-06-20'
    ],
    'KeyStore': [
        '1|023',
        '1|007',
        '1|098',
        '1|023',
        '1|023'
    ],
    'KeyEmployee': [
        '1|343',
        '1|417',
        '1|569',
        '1|343',
        '1|343'
    ],
    'KeyProduct': [
        '1|44733',
        '1|61889',
        '1|42606',
        '1|101',
        '1|102'
    ],
    'TicketId': [
        'N01-00000385',
        'N01-00000959',
        'F01-00070943',
        'N01-00001234',
        'N01-00001235'
    ],
    'Qty': [-4, -1, 1, 10, 15],
    'Amount': [-24873.95, -19243.7, 12184.87, 1500.50, 2300.00],
    'KeyCustomer': [
        '1|POS|',
        '1|POS|32694425',
        '1|POS|222222222',
        '1|POS|111111111',
        '1|POS|111111111'
    ],
    'KeyCurrency': ['1|COP', '1|COP', '1|COP', '1|COP', '1|COP'],
    'KeyDivision': ['1', '1', '1', '1', '1']
}

df = pd.DataFrame(test_data)

df.to_parquet('.\\test\\fixtures\\sample_datamart.parquet', index=False)

print("Archivo parquet de prueba creado exitosamente")
print(f"Registros: {len(df)}")
print(f"Ubicación: tests/fixtures/sample_datamart.parquet")