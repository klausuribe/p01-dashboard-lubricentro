# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

Streamlit dashboard for a lubricentro (auto service shop). Reads operational data from an Excel file and renders six KPIs and four Plotly charts with date-range and category filters. UI, values, and error messages are in Spanish; currency is Bolivianos (`Bs.`).

## Commands

A virtualenv lives at `.venv/`. Activate it before running anything (Windows Git Bash: `source .venv/Scripts/activate`).

- Run the app: `streamlit run app.py`
- Install runtime deps: `pip install -r requirements.txt`
- Install dev deps (adds pytest + ruff): `pip install -r requirements-dev.txt`
- Run all tests: `pytest`
- Run a single test file: `pytest tests/test_metrics.py`
- Run a single test: `pytest tests/test_metrics.py::test_name`
- Lint: `ruff check .`
- Format: `ruff format .`

Python target is 3.11 (`pyproject.toml`). Ruff is configured with line-length 100, rulesets `E,W,F,I,B,UP,SIM,RUF`, and `E501` ignored. Pytest's `testpaths` is `tests/` and it picks up `test_*.py`.

## Architecture

Strict one-way data flow — no module imports from a layer above it:

```
app.py  →  data.loader  →  core.{filters, metrics}  →  ui.{charts, components}
             (I/O)           (pure pandas logic)         (Streamlit + Plotly render)
```

- **`app.py`** — the only Streamlit entry point. Loads data, owns the sidebar filter widgets, composes the KPI grid and charts. There are no other pages; do not introduce multi-page structure without a reason.
- **`config.py`** — central source of truth for `COLORS` (dark palette), `CATEGORIAS` (the allowed service categories), and `COLUMNAS_REQUERIDAS` (the Excel schema). Charts, components, loader, and filters all read from here — change a category or color here, not at call sites.
- **`data/loader.py`** — `load_data(source)` reads the `Datos` sheet of an `.xlsx`, validates `COLUMNAS_REQUERIDAS` and raises `ValueError` if any are missing, coerces `fecha` to datetime and `monto`/`costo` to float. Decorated with `@st.cache_data`, so tests call `load_data.clear()` around each case (see `tests/test_loader.py`).
- **`core/filters.py`** — `apply_filters(df, fecha_inicio, fecha_fin, categorias)` returns a filtered view. Pure pandas, no Streamlit.
- **`core/metrics.py`** — `calculate_kpis(df)` returns the six KPIs as a dict (`ingresos_totales`, `costo_total`, `margen_bruto`, `pct_margen`, `servicios_realizados`, `ticket_promedio`). Guards divide-by-zero when the filtered set is empty.
- **`ui/charts.py`** — four `render_*` functions returning `plotly.graph_objects.Figure`. All figures pass through `_apply_dark_layout()` so the look stays consistent; when adding a chart, use that helper instead of re-specifying layout.
- **`ui/components.py`** — `inject_styles()` (call once, early in `app.py`) injects the Fira Sans/Fira Code CSS and `.kpi-card` styles. `kpi_card(label, value, formato, delta, inverse)` renders one card via `st.markdown(..., unsafe_allow_html=True)`. Formats: `"moneda"` → `Bs. 1,234.56`, `"porcentaje"` → `12.3%`, `"entero"` → `1,234`.

Dark theme is pinned in two places that must stay in sync: `.streamlit/config.toml` (Streamlit chrome) and `config.COLORS` (Plotly figures + injected CSS).

## Testing notes

- Unit tests for `core/`, `data/`, and `ui/` import modules directly and test pure functions.
- Integration tests (`tests/test_app_integration.py`) use `streamlit.testing.v1.AppTest.from_file("app.py")` to run the whole app in-process and assert on rendered markdown and widget interactions. These depend on `data/ejemplo_lubricentro.xlsx` being present.
- `load_data` is `@st.cache_data`-decorated; when writing a test that exercises it with different inputs, wrap with `load_data.clear()` (there's an autouse fixture in `test_loader.py`).
