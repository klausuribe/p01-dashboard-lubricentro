import pandas as pd
import streamlit as st

from config import COLUMNAS_REQUERIDAS


@st.cache_data
def load_data(source) -> pd.DataFrame:
    df = pd.read_excel(source, sheet_name="Datos")

    faltantes = [c for c in COLUMNAS_REQUERIDAS if c not in df.columns]
    if faltantes:
        raise ValueError(f"Faltan columnas requeridas: {', '.join(faltantes)}")

    df["fecha"] = pd.to_datetime(df["fecha"])
    df["monto"] = df["monto"].astype(float)
    df["costo"] = df["costo"].astype(float)

    return df
