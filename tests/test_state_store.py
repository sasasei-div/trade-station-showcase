"""Tests for the standalone public state persistence example."""

from code_samples.state_store import StateStore


def test_save_and_restore(tmp_path):
    store = StateStore(tmp_path / "state.sqlite3")
    original = {"cash": 1_000_000, "positions": [], "label": "研究"}
    store.save("research", original)
    assert store.load("research") == original


def test_modes_are_independent(tmp_path):
    store = StateStore(tmp_path / "state.sqlite3")
    store.save("research", {"cash": 100})
    store.save("demo", {"cash": 200})
    assert store.load("research") == {"cash": 100}
    assert store.load("demo") == {"cash": 200}
    assert store.load("missing") is None


def test_update_existing_mode(tmp_path):
    store = StateStore(tmp_path / "state.sqlite3")
    store.save("demo", {"cash": 100})
    store.save("demo", {"cash": 75})
    assert store.load("demo") == {"cash": 75}
