"""Tests using fictional broker-like position responses."""
import pytest
from code_samples.api_response_normalization import normalize_positions


def test_position_normalization_and_closed_filter():
    payload = [
        {"symbol": "7203", "side": "long", "remaining_qty": 200,
         "reserved_qty": 100, "average_price": 2500.5},
        {"symbol": "6758", "side": "short", "remaining_qty": 100,
         "average_price": 3500},
        {"symbol": "9432", "side": "long", "remaining_qty": 0,
         "average_price": 100},
    ]
    assert normalize_positions(payload) == [
        {"symbol": "7203", "side": "long", "remaining_qty": 200,
         "available_qty": 100, "average_price": 2500.5},
        {"symbol": "6758", "side": "short", "remaining_qty": 100,
         "available_qty": 100, "average_price": 3500.0}
    ]


@pytest.mark.parametrize("payload", [
    {}, [None],
    [{"symbol": "7203", "side": "long", "remaining_qty": -1,
      "average_price": 100}],
    [{"symbol": "7203", "side": "long", "remaining_qty": 100,
      "reserved_qty": 101, "average_price": 100}],
    [{"symbol": "7203", "side": "long", "remaining_qty": True,
      "average_price": 100}],
    [{"symbol": "7203", "side": "long", "remaining_qty": 100,
      "average_price": float("nan")}]
])
def test_invalid_payload_rejected(payload):
    with pytest.raises(ValueError):
        normalize_positions(payload)
