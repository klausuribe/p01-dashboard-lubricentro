from io import BytesIO

import pandas as pd
import pytest

from config import COLUMNAS_REQUERIDAS
from data.loader import load_data

XLSX_EJEMPLO = "data/ejemplo_lubricentro.xlsx"


def _xlsx_bytes(df: pd.DataFrame, sheet_name: str = "Datos") -> BytesIO:
    buf = BytesIO()
    with pd.ExcelWriter(buf, engine="openpyxl") as w:
        df.to_excel(w, sheet_name=sheet_name, index=False)
    buf.seek(0)
    return buf


@pytest.fixture(autouse=True)
def _clear_cache():
    load_data.clear()
    yield
    load_data.clear()


def test_load_data_archivo_valido():
    df = load_data(XLSX_EJEMPLO)

    assert len(df) > 0
    for col in COLUMNAS_REQUERIDAS:
        assert col in df.columns
    assert df["fecha"].dtype.kind == "M"
    assert df["monto"].dtype == "float64"
    assert df["costo"].dtype == "float64"


def test_load_data_columnas_faltantes():
    incompleto = pd.DataFrame(
        {
            "fecha": ["2025-01-01"],
            "monto": [100],
            "costo": [60],
        }
    )
    buf = _xlsx_bytes(incompleto)

    with pytest.raises(ValueError, match="Faltan columnas requeridas"):
        load_data(buf)


def test_load_data_archivo_vacio():
    vacio = pd.DataFrame(columns=[*COLUMNAS_REQUERIDAS, "notas"])
    buf = _xlsx_bytes(vacio)

    df = load_data(buf)

    assert len(df) == 0
    for col in COLUMNAS_REQUERIDAS:
        assert col in df.columns
