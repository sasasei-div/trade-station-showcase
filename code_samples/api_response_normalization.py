"""Independent portfolio example: normalize fictional API position responses.

No networking, broker credentials, order placement or proprietary logic.
"""
import math


def normalize_positions(payload):
    """Validate and prepare generic position records for a GUI table."""
    if not isinstance(payload, list):
        raise ValueError("建玉一覧はlistで指定してください")
    rows = []
    for item in payload:
        if not isinstance(item, dict):
            raise ValueError("建玉はdictで指定してください")
        code = item.get("symbol")
        side = item.get("side")
        remaining = item.get("remaining_qty")
        reserved = item.get("reserved_qty", 0)
        price = item.get("average_price")
        if not isinstance(code, str) or not code.strip():
            raise ValueError("銘柄コードが必要です")
        if side not in ("long", "short"):
            raise ValueError("売買区分が不正です")
        if (type(remaining) is not int or remaining < 0
                or type(reserved) is not int or reserved < 0
                or reserved > remaining):
            raise ValueError("株数または拘束株数が不正です")
        if type(price) not in (int, float) or not math.isfinite(price) or price <= 0:
            raise ValueError("取得単価が不正です")
        if remaining:
            rows.append({
                "symbol": code.strip(), "side": side,
                "remaining_qty": remaining, "available_qty": remaining - reserved,
                "average_price": float(price)
            })
    return rows
