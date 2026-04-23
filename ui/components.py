import html

import streamlit as st

from config import COLORS

_STYLES = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@500;600&family=Fira+Sans:wght@400;500;600;700&display=swap');

html, body {{
    font-family: 'Fira Sans', system-ui, sans-serif;
}}

h1, h2, h3, h4, h5, h6,
.stMarkdown, .stMarkdown p, .stMarkdown span, .stMarkdown li,
[data-testid="stSidebar"] .stMarkdown,
[data-testid="stWidgetLabel"] label {{
    font-family: 'Fira Sans', system-ui, sans-serif;
}}

.kpi-card {{
    background: {COLORS["surface"]};
    border: 1px solid {COLORS["border"]};
    border-radius: 8px;
    padding: 18px 20px;
    transition: border-color 200ms ease, transform 200ms ease;
    height: 100%;
}}
.kpi-card:hover {{
    border-color: {COLORS["primary"]};
    transform: translateY(-1px);
}}
.kpi-label {{
    font-family: 'Fira Sans', sans-serif;
    font-size: 11px;
    font-weight: 600;
    color: {COLORS["neutral"]};
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-bottom: 6px;
}}
.kpi-value {{
    font-family: 'Fira Code', monospace;
    font-size: 26px;
    font-weight: 600;
    color: #F0F6FC;
    line-height: 1.2;
}}
.kpi-delta {{
    font-family: 'Fira Sans', sans-serif;
    font-size: 12px;
    font-weight: 500;
    margin-top: 6px;
}}
.kpi-delta.positive {{ color: {COLORS["secondary"]}; }}
.kpi-delta.negative {{ color: {COLORS["danger"]}; }}
</style>
"""


def inject_styles() -> None:
    st.markdown(_STYLES, unsafe_allow_html=True)


def _format_value(value: float, formato: str) -> str:
    if formato == "moneda":
        return f"Bs. {value:,.2f}"
    if formato == "porcentaje":
        return f"{value:.1f}%"
    if formato == "entero":
        return f"{int(value):,}"
    return str(value)


def _format_delta(delta: float, formato: str) -> str:
    sign = "+" if delta > 0 else "-"
    magnitude = abs(delta)
    if formato == "porcentaje":
        return f"{sign}{magnitude:.1f}pp"
    if formato == "moneda":
        return f"{sign}Bs. {magnitude:,.2f}"
    if formato == "entero":
        return f"{sign}{int(magnitude):,}"
    return f"{sign}{magnitude}"


def kpi_card(
    label: str,
    value: float,
    formato: str = "moneda",
    delta: float | None = None,
    inverse: bool = False,
) -> None:
    value_str = _format_value(value, formato)

    delta_html = ""
    if delta is not None and delta != 0:
        is_good = (delta > 0) != inverse
        css_class = "positive" if is_good else "negative"
        delta_str = _format_delta(delta, formato)
        delta_html = f'<div class="kpi-delta {css_class}">{delta_str}</div>'

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">{html.escape(label)}</div>
            <div class="kpi-value">{value_str}</div>
            {delta_html}
        </div>
        """,
        unsafe_allow_html=True,
    )
