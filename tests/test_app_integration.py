from pathlib import Path

import pandas as pd
from streamlit.testing.v1 import AppTest

from config import COLUMNAS_REQUERIDAS

APP_SOURCE = Path("app.py").read_text(encoding="utf-8")


def _run_app():
    at = AppTest.from_file("app.py", default_timeout=30)
    at.run()
    return at


def _run_app_with_path(xlsx_path: str) -> AppTest:
    patched = APP_SOURCE.replace(
        'XLSX_PATH = "data/ejemplo_lubricentro.xlsx"',
        f'XLSX_PATH = {xlsx_path!r}',
    )
    at = AppTest.from_string(patched, default_timeout=30)
    at.run()
    return at


def _write_xlsx(path: Path, df: pd.DataFrame) -> None:
    with pd.ExcelWriter(path, engine="openpyxl") as w:
        df.to_excel(w, sheet_name="Datos", index=False)


def test_app_runs_without_exceptions():
    at = _run_app()
    assert not at.exception


def test_app_renders_six_kpis_in_markdown():
    at = _run_app()

    kpi_labels = [
        "Ingresos Totales",
        "Costo Total",
        "Margen Bruto",
        "% Margen",
        "Servicios Realizados",
        "Ticket Promedio",
    ]
    all_markdown = " ".join(m.value for m in at.markdown)
    for label in kpi_labels:
        assert label in all_markdown


def test_filter_reactivity_changes_kpis():
    at = _run_app()
    initial_kpis_html = " ".join(m.value for m in at.markdown)

    at.multiselect[0].set_value(["Cambio de aceite"]).run()

    filtered_kpis_html = " ".join(m.value for m in at.markdown)
    assert initial_kpis_html != filtered_kpis_html
    assert not at.exception


def test_filter_to_single_category_reduces_services_count():
    at_all = _run_app()
    all_data_markdown = " ".join(m.value for m in at_all.markdown)

    at_filtered = _run_app()
    at_filtered.multiselect[0].set_value(["Otro"]).run()
    filtered_markdown = " ".join(m.value for m in at_filtered.markdown)

    assert filtered_markdown != all_data_markdown
    assert not at_filtered.exception


def test_detail_section_renders_header():
    at = _run_app()
    all_markdown = " ".join(m.value for m in at.markdown)
    assert "Detalle" in all_markdown
    assert not at.exception


def test_download_csv_button_present():
    at = _run_app()
    buttons = at.get("download_button")
    labels = [b.proto.label for b in buttons]
    assert "Descargar CSV" in labels
    assert not at.exception


def test_download_csv_button_survives_filter_change():
    at = _run_app()
    at.multiselect[0].set_value(["Cambio de aceite"]).run()
    labels = [b.proto.label for b in at.get("download_button")]
    assert "Descargar CSV" in labels
    assert not at.exception


def test_file_uploader_present_in_sidebar():
    at = _run_app()
    uploaders = at.sidebar.file_uploader
    labels = [u.label for u in uploaders]
    assert any("Subir Excel" in label for label in labels)
    assert not at.exception


def test_default_source_used_when_no_file_uploaded():
    at = _run_app()
    # Con el dataset de ejemplo siempre hay servicios > 0
    all_markdown = " ".join(m.value for m in at.markdown)
    assert "Servicios Realizados" in all_markdown
    assert not at.exception


def test_missing_columns_shows_friendly_error(tmp_path):
    bad = tmp_path / "bad_schema.xlsx"
    _write_xlsx(bad, pd.DataFrame({"fecha": ["2025-01-01"], "monto": [100]}))

    at = _run_app_with_path(str(bad))

    assert not at.exception
    errors = " ".join(e.value for e in at.error)
    assert "Faltan columnas requeridas" in errors


def test_nonexistent_file_shows_friendly_error(tmp_path):
    missing = tmp_path / "does_not_exist.xlsx"

    at = _run_app_with_path(str(missing))

    assert not at.exception
    errors = " ".join(e.value for e in at.error)
    assert "No se pudo leer el archivo" in errors


def test_empty_dataframe_shows_info_message(tmp_path):
    empty = tmp_path / "empty.xlsx"
    _write_xlsx(empty, pd.DataFrame(columns=[*COLUMNAS_REQUERIDAS, "notas"]))

    at = _run_app_with_path(str(empty))

    assert not at.exception
    infos = " ".join(i.value for i in at.info)
    assert "no contiene registros" in infos
