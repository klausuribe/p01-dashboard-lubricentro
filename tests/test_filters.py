import pandas as pd

from core.filters import apply_filters


def _sample_df():
    return pd.DataFrame(
        {
            "fecha": pd.to_datetime(
                [
                    "2025-01-05",
                    "2025-01-15",
                    "2025-02-10",
                    "2025-02-20",
                    "2025-03-01",
                    "2025-03-15",
                ]
            ),
            "categoria": [
                "Cambio de aceite",
                "Revision de frenos",
                "Cambio de aceite",
                "Otro",
                "Revision de frenos",
                "Cambio de aceite",
            ],
            "monto": [100.0, 200.0, 150.0, 80.0, 220.0, 120.0],
            "costo": [60.0, 120.0, 90.0, 50.0, 130.0, 70.0],
        }
    )


def test_apply_filters_rango_fechas():
    df = _sample_df()
    out = apply_filters(df, "2025-02-01", "2025-02-28")

    assert len(out) == 2
    assert out["fecha"].min() >= pd.Timestamp("2025-02-01")
    assert out["fecha"].max() <= pd.Timestamp("2025-02-28")


def test_apply_filters_categoria():
    df = _sample_df()
    out = apply_filters(df, "2025-01-01", "2025-03-31", categorias=["Cambio de aceite"])

    assert len(out) == 3
    assert (out["categoria"] == "Cambio de aceite").all()


def test_apply_filters_fecha_y_categoria_combinados():
    df = _sample_df()
    out = apply_filters(
        df,
        "2025-01-01",
        "2025-02-28",
        categorias=["Cambio de aceite", "Otro"],
    )

    assert len(out) == 3
    assert set(out["categoria"].unique()) <= {"Cambio de aceite", "Otro"}


def test_apply_filters_categorias_vacias_no_filtra():
    df = _sample_df()
    out = apply_filters(df, "2025-01-01", "2025-03-31", categorias=None)
    assert len(out) == len(df)

    out2 = apply_filters(df, "2025-01-01", "2025-03-31", categorias=[])
    assert len(out2) == len(df)


def test_apply_filters_rango_sin_datos():
    df = _sample_df()
    out = apply_filters(df, "2025-06-01", "2025-06-30")
    assert len(out) == 0
