import pandas as pd
import plotly.graph_objects as go

from ui.charts import (
    render_ingreso_vs_costo,
    render_ingresos_por_categoria,
    render_ingresos_por_dia,
    render_volumen_por_categoria,
)


def _sample_df():
    return pd.DataFrame(
        {
            "fecha": pd.to_datetime(
                [
                    "2025-01-05",
                    "2025-01-05",
                    "2025-01-15",
                    "2025-02-10",
                    "2025-02-20",
                ]
            ),
            "categoria": [
                "Cambio de aceite",
                "Revision de frenos",
                "Cambio de aceite",
                "Cambio de aceite",
                "Otro",
            ],
            "monto": [100.0, 200.0, 150.0, 120.0, 80.0],
            "costo": [60.0, 120.0, 90.0, 70.0, 50.0],
        }
    )


def test_ingresos_por_dia_aggregates_by_date():
    fig = render_ingresos_por_dia(_sample_df())

    assert isinstance(fig, go.Figure)
    assert len(fig.data) == 1
    y_values = list(fig.data[0].y)
    assert 300.0 in y_values
    assert 150.0 in y_values
    assert 120.0 in y_values
    assert 80.0 in y_values


def test_volumen_por_categoria_counts_servicios():
    fig = render_volumen_por_categoria(_sample_df())

    assert isinstance(fig, go.Figure)
    assert len(fig.data) == 1
    volumenes = dict(zip(fig.data[0].y, fig.data[0].x, strict=True))
    assert volumenes["Cambio de aceite"] == 3
    assert volumenes["Revision de frenos"] == 1
    assert volumenes["Otro"] == 1


def test_ingresos_por_categoria_sums_monto():
    fig = render_ingresos_por_categoria(_sample_df())

    assert isinstance(fig, go.Figure)
    assert len(fig.data) == 1
    series = dict(zip(fig.data[0].x, fig.data[0].y, strict=True))
    assert series["Cambio de aceite"] == 370.0
    assert series["Revision de frenos"] == 200.0
    assert series["Otro"] == 80.0


def test_ingreso_vs_costo_has_two_stacked_traces():
    fig = render_ingreso_vs_costo(_sample_df())

    assert isinstance(fig, go.Figure)
    assert len(fig.data) == 2
    assert {trace.name for trace in fig.data} == {"Costo", "Margen"}
    assert fig.layout.barmode == "stack"


def test_charts_use_dark_palette():
    fig = render_ingresos_por_dia(_sample_df())

    assert fig.layout.paper_bgcolor == "#0D1117"
    assert fig.layout.plot_bgcolor == "#0D1117"
