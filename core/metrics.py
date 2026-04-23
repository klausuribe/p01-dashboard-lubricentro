import pandas as pd


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
