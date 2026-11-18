"""Focused tests for the public, standalone order-form example."""

import pytest

from code_samples.order_validation import validate_order_input


def test_market_order():
    result = validate_order_input("7203", "100", "成行")
    assert result == {"symbol": "7203", "quantity": 100,
                      "order_type": "成行", "limit_price": None}


def test_limit_order():
    result = validate_order_input("7203", "200", "指値", "2500.5")
    assert str(result["limit_price"]) == "2500.5"


@pytest.mark.parametrize("symbol,quantity,kind,price", [
    ("ABC", "100", "成行", ""),
    ("7203", "0", "成行", ""),
    ("7203", "1.5", "成行", ""),
    ("7203", "100", "逆指値", ""),
    ("7203", "100", "指値", ""),
    ("7203", "100", "指値", "-1"),
    ("7203", "100", "指値", "NaN"),
])
def test_invalid_inputs(symbol, quantity, kind, price):
    with pytest.raises(ValueError):
        validate_order_input(symbol, quantity, kind, price)
