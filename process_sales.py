import pandas as pd
import numpy as np


def clean_and_transform_sales_data(
    input_path="ventas_raw.csv", output_path="ventas_procesado.csv"
):
    # 1. Cargar los datos
    df = pd.read_csv(input_path)

    # 2.a. Eliminar filas completamente nulas
    df.dropna(how="all", inplace=True)

    # 2.b. Eliminar duplicados basados en 'venta_id'
    df.drop_duplicates(subset=["venta_id"], keep="first", inplace=True)

    # 3. Validar y corregir tipos de datos
    df["fecha_venta"] = pd.to_datetime(df["fecha_venta"], errors="coerce")
    df = df[df["fecha_venta"].notnull()]

    df["monto"] = pd.to_numeric(df["monto"], errors="coerce")
    df = df[df["monto"].notnull()]

    # 4. Manejar datos inválidos
    # Convertir montos negativos a positivos
    df["monto"] = np.abs(df["monto"])

    # Rellenar NaNs con el promedio
    monto_promedio = df["monto"].mean()
    df.fillna({"monto": monto_promedio}, inplace=True)

    # Filtrar IDs de producto válidos
    valid_products = ["PROD-001", "PROD-002", "PROD-003", "PROD-004", "PROD-005"]
    df = df[df["producto_id"].isin(valid_products)]

    # 5. Enriquecimiento de datos
    df["mes"] = df["fecha_venta"].dt.month
    df["dia_semana"] = df["fecha_venta"].dt.day_name()

    # 6. Guardar el resultado
    df.to_csv(output_path, index=False)
    print(f"Datos procesados y guardados en '{output_path}'")


def generate_sales_report(
    input_path="ventas_procesado.csv", output_path="reporte_ventas.csv"
):
    df = pd.read_csv(input_path)
    report = df.groupby(["mes", "producto_id"])["monto"].sum().reset_index()
    report.to_csv(output_path, index=False)
    print(f"Reporte de ventas generado en '{output_path}'.")
