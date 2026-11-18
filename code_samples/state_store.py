"""Portfolio demonstration: SQLite-backed state persistence (no trading logic)."""

import json
import sqlite3
from pathlib import Path


class StateStore:
    """Save and restore a JSON-compatible application state by mode."""

    def __init__(self, db_path: str | Path):
        self.db_path = str(db_path)

    def save(self, mode: str, state: dict) -> None:
        if not mode:
            raise ValueError("mode must not be empty")
        payload = json.dumps(state, ensure_ascii=False)
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "CREATE TABLE IF NOT EXISTS app_state "
                "(mode TEXT PRIMARY KEY, payload TEXT NOT NULL)"
            )
            conn.execute(
                "INSERT INTO app_state(mode, payload) VALUES (?, ?) "
                "ON CONFLICT(mode) DO UPDATE SET payload=excluded.payload",
                (mode, payload),
            )

    def load(self, mode: str) -> dict | None:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "CREATE TABLE IF NOT EXISTS app_state "
                "(mode TEXT PRIMARY KEY, payload TEXT NOT NULL)"
            )
            row = conn.execute(
                "SELECT payload FROM app_state WHERE mode = ?", (mode,)
            ).fetchone()
        return json.loads(row[0]) if row else None
