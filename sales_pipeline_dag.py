from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator
from airflow.providers.standard.operators.python import PythonOperator
from datetime import datetime
from process_sales import clean_and_transform_sales_data, generate_sales_report

default_args = {
    "owner": "isaac_gotta",
    "schedule_interval": "@daily",
    "start_date": datetime(2023, 1, 1),
}

with DAG(
    dag_id="pipeline_ventas_diario",
    default_args=default_args,
    catchup=False,
    tags=["ventas", "e-commerce"],
) as dag:

    generar_datos_crudos = BashOperator(
        task_id="generar_datos_crudos",
        bash_command="python data_pipeline_sales/generate_data.py",
    )

    procesar_datos = PythonOperator(
        task_id="procesar_datos", python_callable=clean_and_transform_sales_data
    )

    generar_reporte = PythonOperator(
        task_id="generar_reporte", python_callable=generate_sales_report
    )

    # Definir dependencias
    generar_datos_crudos >> procesar_datos >> generar_reporte
