import pandas as pd
import pytest

from core.metrics import build_detail_table, calculate_kpis


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


def _make_full_df():
    return pd.DataFrame(
        {
            "fecha": pd.to_datetime(["2025-01-15", "2025-02-03"]),
            "id_servicio": ["SRV-001", "SRV-002"],
            "vehiculo": ["ABC-1234", "XYZ-9876"],
            "categoria": ["Cambio de aceite", "Revision de frenos"],
            "servicio": ["Aceite 10W40", "Pastillas + discos"],
            "tecnico": ["Juan Pérez", "Ana Gómez"],
            "monto": [250.0, 800.0],
            "costo": [120.0, 450.0],
            "metodo_pago": ["Efectivo", "QR"],
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


def test_build_detail_table_has_spanish_columns_in_expected_order():
    df = _make_full_df()
    detail = build_detail_table(df)

    assert list(detail.columns) == [
        "Fecha",
        "Vehículo",
        "Servicio",
        "Técnico",
        "Monto",
        "Costo",
        "Margen",
    ]


def test_build_detail_table_computes_margen():
    df = _make_full_df()
    detail = build_detail_table(df)

    assert detail["Margen"].tolist() == [130.0, 350.0]


def test_build_detail_table_preserves_row_count():
    df = _make_full_df()
    detail = build_detail_table(df)
    assert len(detail) == len(df)


def test_build_detail_table_empty_dataframe():
    df = _make_full_df().iloc[0:0]
    detail = build_detail_table(df)

    assert list(detail.columns) == [
        "Fecha",
        "Vehículo",
        "Servicio",
        "Técnico",
        "Monto",
        "Costo",
        "Margen",
    ]
    assert len(detail) == 0


def test_build_detail_table_does_not_mutate_input():
    df = _make_full_df()
    original_columns = list(df.columns)
    build_detail_table(df)
    assert list(df.columns) == original_columns
