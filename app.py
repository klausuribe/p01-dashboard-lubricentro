import streamlit as st

from config import CATEGORIAS
from core.filters import apply_filters
from core.metrics import calculate_kpis
from data.loader import load_data
from ui.charts import (
    render_ingreso_vs_costo,
    render_ingresos_por_categoria,
    render_ingresos_por_dia,
    render_volumen_por_categoria,
)
from ui.components import inject_styles, kpi_card

XLSX_PATH = "data/ejemplo_lubricentro.xlsx"


st.set_page_config(
    page_title="Dashboard Lubricentro",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_styles()

st.markdown(
    "<h1 style='font-family: Fira Sans, sans-serif; font-weight: 600; "
    "font-size: 28px; margin-bottom: 4px;'>Dashboard Lubricentro</h1>"
    "<p style='color: #8B949E; margin-top: 0; margin-bottom: 24px;'>"
    "KPIs operativos y análisis de servicios</p>",
    unsafe_allow_html=True,
)

df = load_data(XLSX_PATH)

with st.sidebar:
    st.markdown("### Filtros")

    min_date = df["fecha"].min().date()
    max_date = df["fecha"].max().date()
    default_start = max_date.replace(day=1)

    fecha_range = st.date_input(
        "Rango de fechas",
        value=(default_start, max_date),
        min_value=min_date,
        max_value=max_date,
    )

    if isinstance(fecha_range, tuple) and len(fecha_range) == 2:
        fecha_inicio, fecha_fin = fecha_range
    else:
        fecha_inicio, fecha_fin = min_date, max_date

    categorias_seleccionadas = st.multiselect(
        "Categorías",
        options=CATEGORIAS,
        default=CATEGORIAS,
    )

df_filtrado = apply_filters(df, fecha_inicio, fecha_fin, categorias_seleccionadas)
kpis = calculate_kpis(df_filtrado)

col1, col2, col3 = st.columns(3, gap="medium")
with col1:
    kpi_card("Ingresos Totales", kpis["ingresos_totales"], formato="moneda")
with col2:
    kpi_card("Costo Total", kpis["costo_total"], formato="moneda")
with col3:
    kpi_card("Margen Bruto", kpis["margen_bruto"], formato="moneda")

st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

col4, col5, col6 = st.columns(3, gap="medium")
with col4:
    kpi_card("% Margen", kpis["pct_margen"], formato="porcentaje")
with col5:
    kpi_card("Servicios Realizados", kpis["servicios_realizados"], formato="entero")
with col6:
    kpi_card("Ticket Promedio", kpis["ticket_promedio"], formato="moneda")

st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)

if len(df_filtrado) == 0:
    st.warning("No hay datos para los filtros seleccionados.")
else:
    st.plotly_chart(render_ingresos_por_dia(df_filtrado), use_container_width=True)

    col_left, col_right = st.columns(2, gap="medium")
    with col_left:
        st.plotly_chart(
            render_volumen_por_categoria(df_filtrado),
            use_container_width=True,
        )
    with col_right:
        st.plotly_chart(
            render_ingresos_por_categoria(df_filtrado),
            use_container_width=True,
        )

    st.plotly_chart(render_ingreso_vs_costo(df_filtrado), use_container_width=True)
