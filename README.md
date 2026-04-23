# Dashboard Lubricentro

Dashboard interactivo para analizar la operación de un lubricentro: ingresos, costos, márgenes, volumen de servicios y ticket promedio. Construido con **Streamlit** + **Plotly** sobre datos de un archivo Excel.

## Características

- **6 KPIs** en tarjetas: Ingresos Totales, Costo Total, Margen Bruto, % Margen, Servicios Realizados, Ticket Promedio.
- **4 gráficos** (Plotly, tema oscuro):
  - Ingresos por día (línea con área).
  - Volumen de servicios por categoría (barras horizontales).
  - Ingresos por categoría (barras verticales).
  - Ingreso vs Costo por categoría (barras apiladas costo + margen).
- **Filtros en sidebar**: rango de fechas y selección múltiple de categorías.
- **Tabla de detalle** con las transacciones filtradas y **botón de descarga CSV** (UTF-8 BOM, compatible con Excel Windows).
- **Upload de Excel personalizado** desde el sidebar (`st.file_uploader`): si no subís un archivo, se usa el dataset de ejemplo.
- **Manejo de errores claro**: si faltan columnas, el archivo está vacío o es inválido, se muestra un mensaje en español sin traceback.
- Moneda en Bolivianos (`Bs.`) con formato `1,234.56`.

## Requisitos

- Python **3.11+**
- Un archivo Excel (`.xlsx`) con una hoja llamada `Datos` y las siguientes columnas:

  `fecha`, `id_servicio`, `vehiculo`, `categoria`, `servicio`, `tecnico`, `monto`, `costo`, `metodo_pago`

  Si falta alguna, la app levanta `ValueError: Faltan columnas requeridas: ...`.

Hay un archivo de ejemplo en `data/ejemplo_lubricentro.xlsx` que se usa por defecto.

## Instalación

```bash
# Crear y activar entorno virtual
python -m venv .venv
source .venv/Scripts/activate      # Windows (Git Bash)
# source .venv/bin/activate        # Linux / macOS

# Instalar dependencias
pip install -r requirements.txt
```

Para desarrollo (pytest + ruff):

```bash
pip install -r requirements-dev.txt
```

## Uso

```bash
streamlit run app.py
```

Por defecto lee `data/ejemplo_lubricentro.xlsx`. Para usar un archivo propio, subilo desde el sidebar (**Fuente de datos → Subir Excel (.xlsx)**). El Excel debe tener una hoja `Datos` con el schema descrito arriba; si falta alguna columna, la app lo indica en pantalla sin crashear.

## Categorías soportadas

Definidas en `config.py` (`CATEGORIAS`):

- Cambio de aceite
- Lubricacion completa
- Cambio de filtros
- Revision de frenos
- Cambio de liquidos
- Servicio completo
- Otro

## Estructura del proyecto

```
.
├── app.py                  # Entry point de Streamlit
├── config.py               # Colores, categorías, columnas requeridas
├── core/
│   ├── filters.py          # apply_filters(df, fecha_inicio, fecha_fin, categorias)
│   └── metrics.py          # calculate_kpis(df) → dict con los 6 KPIs
├── data/
│   ├── loader.py           # load_data(source) con validación de schema
│   └── ejemplo_lubricentro.xlsx
├── ui/
│   ├── charts.py           # 4 funciones render_* que devuelven go.Figure
│   └── components.py       # inject_styles() + kpi_card()
├── tests/                  # pytest (unitarios + integración con AppTest)
│   ├── test_loader.py
│   ├── test_filters.py
│   ├── test_metrics.py        # calculate_kpis + build_detail_table
│   ├── test_components.py
│   ├── test_charts.py
│   └── test_app_integration.py  # AppTest end-to-end (KPIs, filtros, CSV, errores)
├── .streamlit/config.toml  # Tema oscuro de Streamlit
├── requirements.txt
├── requirements-dev.txt
└── pyproject.toml          # ruff + pytest
```

## Desarrollo

```bash
# Tests
pytest                                     # todos
pytest tests/test_metrics.py               # un archivo
pytest tests/test_metrics.py::test_name    # un test

# Linting y formato
ruff check .
ruff format .
```

Los tests de integración usan `streamlit.testing.v1.AppTest` para correr la app completa y validar los KPIs renderizados y la reactividad de los filtros.

## Deploy — Streamlit Community Cloud

1. Hacé login en [share.streamlit.io](https://share.streamlit.io) con tu cuenta de GitHub.
2. Click en **New app** y seleccioná el repo `klausuribe/p01-dashboard-lubricentro`, branch `main`, entry point `app.py`.
3. Deploy automático en cada push a `main`.

El archivo `data/ejemplo_lubricentro.xlsx` debe estar commiteado en el repo para que el deploy funcione sin configuración adicional (no hay variables de entorno en este proyecto).

## Personalización

- **Colores / tema**: editar `COLORS` en `config.py` (afecta Plotly + CSS de las KPI cards) y `.streamlit/config.toml` (afecta el chrome de Streamlit). Mantené ambos sincronizados.
- **Agregar una categoría**: sumar el string a `CATEGORIAS` en `config.py`; aparece automáticamente en el filtro y los gráficos.
- **Agregar un gráfico**: crear una función `render_*` en `ui/charts.py` que pase por el helper `_apply_dark_layout()` para mantener consistencia visual, y llamarla desde `app.py` con `st.plotly_chart(...)`.
