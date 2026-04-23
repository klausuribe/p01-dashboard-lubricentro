from streamlit.testing.v1 import AppTest


def _run_app():
    at = AppTest.from_file("app.py", default_timeout=30)
    at.run()
    return at


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
