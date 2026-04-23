import pandas as pd

_DETAIL_COLUMNS = ["Fecha", "Vehículo", "Servicio", "Técnico", "Monto", "Costo", "Margen"]


def build_detail_table(df: pd.DataFrame) -> pd.DataFrame:
    if len(df) == 0:
        return pd.DataFrame(columns=_DETAIL_COLUMNS)

    return pd.DataFrame(
        {
            "Fecha": df["fecha"].values,
            "Vehículo": df["vehiculo"].values,
            "Servicio": df["servicio"].values,
            "Técnico": df["tecnico"].values,
            "Monto": df["monto"].astype(float).values,
            "Costo": df["costo"].astype(float).values,
            "Margen": (df["monto"].astype(float) - df["costo"].astype(float)).values,
        }
    )


def calculate_kpis(df: pd.DataFrame) -> dict:
    ingresos = float(df["monto"].sum()) if "monto" in df.columns else 0.0
    costos = float(df["costo"].sum()) if "costo" in df.columns else 0.0
    margen = ingresos - costos
    servicios = len(df)
    pct_margen = (margen / ingresos * 100) if ingresos > 0 else 0.0
    ticket = (ingresos / servicios) if servicios > 0 else 0.0
    return {
        "ingresos_totales": ingresos,
        "costo_total": costos,
        "margen_bruto": margen,
        "pct_margen": pct_margen,
        "servicios_realizados": servicios,
        "ticket_promedio": ticket,
    }
