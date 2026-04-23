import pandas as pd


def apply_filters(df: pd.DataFrame, fecha_inicio, fecha_fin, categorias=None) -> pd.DataFrame:
    inicio = pd.to_datetime(fecha_inicio)
    fin = pd.to_datetime(fecha_fin)
    mask = (df["fecha"] >= inicio) & (df["fecha"] <= fin)
    if categorias:
        mask &= df["categoria"].isin(categorias)
    return df[mask]
