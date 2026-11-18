"""Standalone portfolio example: basic order-form input validation.

This demonstration does not place orders or implement trading strategies.
"""

from decimal import Decimal, InvalidOperation


SUPPORTED_ORDER_TYPES = {"成行", "指値"}


def validate_order_input(symbol: str, quantity: str, order_type: str,
                         limit_price: str = "") -> dict:
    """Validate form values and return normalized data; raise ValueError on errors.

    This is an educational sample, not a broker's complete order-rule validator.
    """
    symbol = str(symbol).strip()
    if not (symbol.isascii() and symbol.isdigit() and len(symbol) == 4):
        raise ValueError("銘柄コードは4桁の数字で入力してください")

    quantity = str(quantity).strip()
    if not (quantity.isascii() and quantity.isdecimal()):
        raise ValueError("株数は正の整数で入力してください")
    shares = int(quantity)
    if shares <= 0:
        raise ValueError("株数は1以上で入力してください")

    if order_type not in SUPPORTED_ORDER_TYPES:
        raise ValueError("注文種別は成行または指値を指定してください")

    price = None
    if order_type == "指値":
        try:
            price = Decimal(str(limit_price).strip())
        except InvalidOperation as exc:
            raise ValueError("指値価格は数値で入力してください") from exc
        if not price.is_finite() or price <= 0:
            raise ValueError("指値価格は0より大きい有限の数値で入力してください")

    return {"symbol": symbol, "quantity": shares,
            "order_type": order_type, "limit_price": price}
