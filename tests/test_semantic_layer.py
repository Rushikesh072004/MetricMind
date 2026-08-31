from src.semantic_layer import get_metric_value


def test_sales_metric():
    result = get_metric_value("sales")
    assert result == 325000.0


def test_revenue_metric():
    result = get_metric_value("revenue")
    assert result == 180000.0


def test_cost_metric():
    result = get_metric_value("cost")
    assert result == 65000.0