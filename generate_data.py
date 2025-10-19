import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# --- Configuración ---
num_records = 1000
products = {
    "PROD-001": {"name": "Laptop Pro", "price": 1200.00},
    "PROD-002": {"name": "Mouse Inalámbrico", "price": 25.50},
    "PROD-003": {"name": "Teclado Mecánico", "price": 75.99},
    "PROD-004": {"name": "Monitor 4K", "price": 450.00},
    "PROD-005": {"name": "Webcam HD", "price": 60.00},
}
start_date = datetime(2023, 1, 1)

# --- Generación de Datos ---
data = []
for i in range(num_records):
    product_id = np.random.choice(list(products.keys()))

    # Simular algunos datos erróneos y nulos
    if np.random.rand() < 0.1:
        product_id = "PROD-999"  # ID de producto inválido

    date = start_date + timedelta(
        days=np.random.randint(0, 364), hours=np.random.randint(0, 23)
    )

    # Simular precios incorrectos o nulos
    if np.random.rand() < 0.05:
        monto = None
    elif np.random.rand() < 0.05:
        monto = (
            products[product_id]["price"] * (1 + np.random.uniform(-0.2, 0.2))
            if product_id in products
            else 100.0
        )
        monto = round(monto, 2) * -1  # Monto negativo
    else:
        monto = (
            round(products[product_id]["price"] * np.random.randint(1, 4), 2)
            if product_id in products
            else 150.0
        )

    # Simular duplicados
    if i % 100 == 0:
        data.append(
            {
                "venta_id": f"SALE-{i}",
                "producto_id": product_id,
                "fecha_venta": date.strftime("%Y-%m-%d %H:%M:%S"),
                "monto": monto,
            }
        )

    data.append(
        {
            "venta_id": f"SALE-{i}",
            "producto_id": product_id,
            "fecha_venta": date.strftime("%Y-%m-%d %H:%M:%S"),
            "monto": monto,
        }
    )

# Simular filas completamente nulas
for _ in range(5):
    data.append(
        {"venta_id": None, "producto_id": None, "fecha_venta": None, "monto": None}
    )

# --- Crear DataFrame y Guardar a CSV ---
df = pd.DataFrame(data)
df.to_csv("ventas_raw.csv", index=False)

print("Archivo 'ventas_raw.csv' generado con éxito.")
