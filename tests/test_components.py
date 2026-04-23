from ui.components import _format_delta, _format_value


def test_format_value_moneda():
    assert _format_value(1234.5, "moneda") == "Bs. 1,234.50"
    assert _format_value(0, "moneda") == "Bs. 0.00"
    assert _format_value(1_000_000.9, "moneda") == "Bs. 1,000,000.90"


def test_format_value_porcentaje():
    assert _format_value(45.678, "porcentaje") == "45.7%"
    assert _format_value(0, "porcentaje") == "0.0%"
    assert _format_value(100, "porcentaje") == "100.0%"


def test_format_value_entero():
    assert _format_value(1234, "entero") == "1,234"
    assert _format_value(0, "entero") == "0"
    assert _format_value(1_000_000, "entero") == "1,000,000"


def test_format_delta_positive_moneda():
    assert _format_delta(150.5, "moneda") == "+Bs. 150.50"


def test_format_delta_negative_moneda():
    assert _format_delta(-150.5, "moneda") == "-Bs. 150.50"


def test_format_delta_porcentaje_uses_pp():
    assert _format_delta(3.2, "porcentaje") == "+3.2pp"
    assert _format_delta(-3.2, "porcentaje") == "-3.2pp"


def test_format_delta_entero():
    assert _format_delta(42, "entero") == "+42"
    assert _format_delta(-42, "entero") == "-42"
