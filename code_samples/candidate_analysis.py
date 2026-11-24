"""Independent portfolio sample: CSV candidates and SQLite moving averages.

No proprietary stock selection or trading algorithm is included.
DB schema: daily_prices(symbol TEXT, trade_date TEXT, close REAL).
"""
import csv
import math
import sqlite3
from pathlib import Path


def read_candidates(path):
    """Read and deduplicate four-digit symbols from a CSV with a symbol header."""
    with open(path, encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        if not reader.fieldnames or "symbol" not in reader.fieldnames:
            raise ValueError("CSVにsymbol列が必要です")
        symbols = []
        seen = set()
        for row in reader:
            code = str(row.get("symbol") or "").strip()
            if not code:
                continue
            if not (code.isascii() and code.isdecimal() and len(code) == 4):
                raise ValueError(f"銘柄コードが不正です: {code}")
            if code not in seen:
                symbols.append(code)
                seen.add(code)
        return symbols


def analyze_candidates(db_path, symbols, cutoff):
    """Analyze only history through cutoff, without accessing future prices."""
    results = []
    uri = f"file:{Path(db_path).resolve().as_posix()}?mode=ro"
    with sqlite3.connect(uri, uri=True) as conn:
        for code in dict.fromkeys(symbols):
            records = conn.execute(
                "SELECT trade_date, close FROM daily_prices "
                "WHERE symbol=? AND trade_date<=? "
                "ORDER BY trade_date DESC LIMIT 75", (code, cutoff)
            ).fetchall()
            valid = len(records) == 75 and all(
                type(price) in (int, float) and math.isfinite(price) and price > 0
                for _, price in records
            )
            if not valid:
                results.append({"symbol": code, "status": "insufficient_data"})
                continue
            closes = [price for _, price in records]
            results.append({
                "symbol": code, "status": "ok", "date": records[0][0],
                "close": closes[0],
                **{f"ma{n}": round(sum(closes[:n]) / n, 2) for n in (5, 25, 75)}
            })
    return results
