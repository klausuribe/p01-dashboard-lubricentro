import pandas as pd
import plotly.graph_objects as go

from config import COLORS

_FONT_FAMILY = "Fira Sans, system-ui, sans-serif"
_TEXT_COLOR = "#F0F6FC"


def _apply_dark_layout(
    fig: go.Figure,
    title: str | None = None,
    show_legend: bool = False,
) -> go.Figure:
    fig.update_layout(
        title=(dict(text=title, font=dict(size=14, color=_TEXT_COLOR)) if title else None),
        paper_bgcolor=COLORS["background"],
        plot_bgcolor=COLORS["background"],
        font=dict(family=_FONT_FAMILY, color=_TEXT_COLOR, size=12),
        margin=dict(l=20, r=20, t=40 if title else 20, b=20),
        showlegend=show_legend,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            bgcolor="rgba(0,0,0,0)",
        ),
        hoverlabel=dict(
            bgcolor=COLORS["surface"],
            bordercolor=COLORS["border"],
            font=dict(family=_FONT_FAMILY, color=_TEXT_COLOR),
        ),
    )
    fig.update_xaxes(
        gridcolor=COLORS["border"],
        zerolinecolor=COLORS["border"],
        linecolor=COLORS["border"],
        tickfont=dict(color=COLORS["neutral"]),
    )
    fig.update_yaxes(
        gridcolor=COLORS["border"],
        zerolinecolor=COLORS["border"],
        linecolor=COLORS["border"],
        tickfont=dict(color=COLORS["neutral"]),
    )
    return fig


def render_ingresos_por_dia(df: pd.DataFrame) -> go.Figure:
    serie = df.groupby(df["fecha"].dt.date)["monto"].sum().reset_index()
    serie.columns = ["fecha", "ingresos"]

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=serie["fecha"],
            y=serie["ingresos"],
            mode="lines",
            line=dict(color=COLORS["primary"], width=2.5, shape="spline"),
            fill="tozeroy",
            fillcolor="rgba(88, 166, 255, 0.12)",
            hovertemplate="<b>%{x|%d %b %Y}</b><br>Bs. %{y:,.2f}<extra></extra>",
            name="Ingresos",
        )
    )
    _apply_dark_layout(fig, title="Ingresos por día")
    fig.update_yaxes(tickprefix="Bs. ", tickformat=",.0f")
    return fig


def render_volumen_por_categoria(df: pd.DataFrame) -> go.Figure:
    serie = df.groupby("categoria").size().reset_index(name="volumen")
    serie = serie.sort_values("volumen", ascending=True)

    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=serie["volumen"],
            y=serie["categoria"],
            orientation="h",
            marker=dict(color=COLORS["neutral"], line=dict(width=0)),
            text=serie["volumen"],
            textposition="outside",
            textfont=dict(color=_TEXT_COLOR),
            hovertemplate="<b>%{y}</b><br>%{x} servicios<extra></extra>",
        )
    )
    _apply_dark_layout(fig, title="Volumen de servicios por categoría")
    fig.update_xaxes(showgrid=False, visible=False)
    return fig


def render_ingresos_por_categoria(df: pd.DataFrame) -> go.Figure:
    serie = df.groupby("categoria")["monto"].sum().reset_index()
    serie = serie.sort_values("monto", ascending=False)

    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=serie["categoria"],
            y=serie["monto"],
            marker=dict(color=COLORS["primary"], line=dict(width=0)),
            hovertemplate="<b>%{x}</b><br>Bs. %{y:,.2f}<extra></extra>",
        )
    )
    _apply_dark_layout(fig, title="Ingresos por categoría")
    fig.update_yaxes(tickprefix="Bs. ", tickformat=",.0f")
    fig.update_xaxes(tickangle=-25)
    return fig


def render_ingreso_vs_costo(df: pd.DataFrame) -> go.Figure:
    serie = df.groupby("categoria")[["monto", "costo"]].sum().reset_index()
    serie["margen"] = serie["monto"] - serie["costo"]
    serie = serie.sort_values("monto", ascending=False)

    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            name="Costo",
            x=serie["categoria"],
            y=serie["costo"],
            marker=dict(color=COLORS["danger"], line=dict(width=0)),
            hovertemplate="<b>%{x}</b><br>Costo: Bs. %{y:,.2f}<extra></extra>",
        )
    )
    fig.add_trace(
        go.Bar(
            name="Margen",
            x=serie["categoria"],
            y=serie["margen"],
            marker=dict(color=COLORS["secondary"], line=dict(width=0)),
            hovertemplate="<b>%{x}</b><br>Margen: Bs. %{y:,.2f}<extra></extra>",
        )
    )
    _apply_dark_layout(
        fig,
        title="Ingreso vs Costo por categoría",
        show_legend=True,
    )
    fig.update_layout(barmode="stack")
    fig.update_yaxes(tickprefix="Bs. ", tickformat=",.0f")
    fig.update_xaxes(tickangle=-25)
    return fig
