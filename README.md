# Data Pipeline de Ventas

Proyecto de ejemplo para procesar datos de ventas, generar reportes y ejecutar la pipeline con Airflow (opcional).

Contenido

- `generate_data.py` — script que genera/serializa datos crudos de ventas (entrada: `ventas_raw.csv`).
- `process_sales.py` — contiene las funciones:
  - `clean_and_transform_sales_data(input_path="ventas_raw.csv", output_path="ventas_procesado.csv")`: limpia y transforma los datos de ventas.
  - `generate_sales_report(input_path="ventas_procesado.csv", output_path="reporte_ventas.csv")`: agrupa ventas por mes y producto y genera un CSV de reporte.
- `sales_pipeline_dag.py` — definición de DAG de Airflow que orquesta: generar datos -> procesar datos -> generar reporte.
- `ventas_raw.csv` — ejemplo de datos crudos (entrada).
- `ventas_procesado.csv` — salida de la transformación (generada por `process_sales.py`).

Requisitos

- Python 3.8+
- Dependencias principales: `pandas`, `numpy`.
- Airflow (opcional) si quieres ejecutar el DAG.

Recomendado: crear un entorno virtual antes de instalar dependencias.

Instalación

1. Crear y activar un entorno virtual (ejemplo con venv):

```bash
python -m venv .venv
source .venv/Scripts/activate  # Windows (PowerShell/Command Prompt use .venv\Scripts\activate)
```

2. Instalar dependencias mínimas:

```bash
pip install -r requirements.txt
```

Uso local (sin Airflow)

1. Generar datos crudos (si existe `generate_data.py` en el mismo directorio):

```bash
python generate_data.py
```

2. Procesar los datos y generar el CSV procesado:

```bash
python -c "from process_sales import clean_and_transform_sales_data; clean_and_transform_sales_data()"
```

3. Generar el reporte de ventas:

```bash
python -c "from process_sales import generate_sales_report; generate_sales_report()"
```

Uso con Airflow (opcional)

1. Instalar Airflow siguiendo la documentación oficial. Recomendado usar una instalación separada o Docker.
2. Copiar `sales_pipeline_dag.py` al directorio de DAGs de Airflow o hacer que el directorio del proyecto sea escaneado por Airflow.
3. El DAG `pipeline_ventas_diario` realiza las tareas en orden: generar datos crudos -> procesar datos -> generar reporte.

Notas sobre los scripts

- `process_sales.py` realiza validaciones básicas:
  - Elimina filas completamente nulas y duplicados por `venta_id`.
  - Convierte `fecha_venta` a datetime y filtra filas inválidas.
  - Convierte `monto` a numérico, reemplaza NaNs con el promedio y convierte valores negativos a positivos.
  - Filtra `producto_id` por una lista de productos válidos (`PROD-001` a `PROD-005`).
  - Añade columnas `mes` y `dia_semana` y guarda el CSV procesado.

Consideraciones y mejoras posibles

- Validación más estricta de esquemas (p. ej. con `pandera` o `pydantic`).
- Parametrizar rutas mediante variables de entorno o argumentos de línea de comandos.
- Añadir tests unitarios para `process_sales.py`.
- Manejo de grandes volúmenes de datos (usar chunksize, Dask o bases de datos).

Contacto
Si tienes preguntas o quieres mejorar el pipeline, abre un issue o contacta al autor del repositorio.

---

Fecha de creación: 2025-10-19
