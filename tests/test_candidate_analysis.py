"""Tests for candidate CSV and historical moving-average sample."""
import sqlite3
import pytest
from code_samples.candidate_analysis import analyze_candidates, read_candidates


def test_read_candidates_deduplicates_bom(tmp_path):
    csv = tmp_path / "candidates.csv"
    csv.write_text("\ufeffsymbol\n7203\n6758\n7203\n", encoding="utf-8")
    assert read_candidates(csv) == ["7203", "6758"]


@pytest.mark.parametrize("contents", ["code\n7203\n", "symbol\nABCD\n"])
def test_bad_csv(tmp_path, contents):
    csv = tmp_path / "candidates.csv"
    csv.write_text(contents, encoding="utf-8")
    with pytest.raises(ValueError):
        read_candidates(csv)


def test_cutoff_and_missing_symbols(tmp_path):
    db = tmp_path / "prices.sqlite3"
    with sqlite3.connect(db) as conn:
        conn.execute("CREATE TABLE daily_prices(symbol TEXT, trade_date TEXT, close REAL)")
        conn.executemany("INSERT INTO daily_prices VALUES (?, ?, ?)",
                         [("7203", f"day{i:03d}", float(i)) for i in range(1, 76)]
                         + [("7203", "day076", 9999.0), ("6758", "day001", 100.0)])
    result = analyze_candidates(db, ["7203", "6758", "9999", "7203"], "day075")
    assert len(result) == 3
    assert result[0]["status"] == "ok"
    assert result[0]["close"] == 75.0
    assert result[0]["ma5"] == 73.0
    assert result[0]["ma25"] == 63.0
    assert result[0]["ma75"] == 38.0
    assert result[1]["status"] == result[2]["status"] == "insufficient_data"


def test_invalid_prices_not_silently_used(tmp_path):
    db = tmp_path / "prices.sqlite3"
    with sqlite3.connect(db) as conn:
        conn.execute("CREATE TABLE daily_prices(symbol TEXT, trade_date TEXT, close REAL)")
        conn.executemany("INSERT INTO daily_prices VALUES (?, ?, ?)",
                         [("7203", f"d{i:03d}", None if i == 1 else 100.0)
                          for i in range(75)])
    assert analyze_candidates(db, ["7203"], "z")[0]["status"] == "insufficient_data"
