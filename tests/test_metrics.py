import pandas as pd
import pytest

from core.metrics import calculate_kpis


def _make_df(montos, costos):
    n = len(montos)
    return pd.DataFrame(
        {
            "fecha": pd.to_datetime(["2025-01-01"] * n),
            "categoria": ["Cambio de aceite"] * n,
            "monto": montos,
            "costo": costos,
        }
    )


def test_calculate_kpis_known_values():
    df = _make_df([100.0, 200.0, 300.0], [60.0, 80.0, 120.0])
    kpis = calculate_kpis(df)

    assert kpis["ingresos_totales"] == 600.0
    assert kpis["costo_total"] == 260.0
    assert kpis["margen_bruto"] == 340.0
    assert kpis["pct_margen"] == pytest.approx(56.6667, rel=1e-3)
    assert kpis["servicios_realizados"] == 3
    assert kpis["ticket_promedio"] == 200.0


def test_calculate_kpis_returns_all_six_keys():
    df = _make_df([100.0], [50.0])
    kpis = calculate_kpis(df)
    expected = {
        "ingresos_totales",
        "costo_total",
        "margen_bruto",
        "pct_margen",
        "servicios_realizados",
        "ticket_promedio",
    }
    assert set(kpis.keys()) == expected


def test_calculate_kpis_empty_dataframe():
    df = _make_df([], [])
    kpis = calculate_kpis(df)

    assert kpis["ingresos_totales"] == 0.0
    assert kpis["costo_total"] == 0.0
    assert kpis["margen_bruto"] == 0.0
    assert kpis["pct_margen"] == 0.0
    assert kpis["servicios_realizados"] == 0
    assert kpis["ticket_promedio"] == 0.0
