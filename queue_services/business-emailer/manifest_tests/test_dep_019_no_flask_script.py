"""DEP-019: Flask-Script and legacy-cgi removed from manifests."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_pyproject_omits_flask_script_and_legacy_cgi():
    text = (ROOT / "pyproject.toml").read_text(encoding="utf-8").lower()
    assert "flask-script" not in text
    assert "legacy-cgi" not in text


def test_poetry_lock_omits_flask_script_and_legacy_cgi():
    text = (ROOT / "poetry.lock").read_text(encoding="utf-8").lower()
    assert 'name = "flask-script"' not in text
    assert 'name = "legacy-cgi"' not in text
