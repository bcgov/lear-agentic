"""SECRET-008: conftest DB URL is env-based."""
from pathlib import Path

CONF = Path(__file__).resolve().parents[1] / "tests" / "conftest.py"


def test_conftest_uses_env_for_postgres_url():
    text = CONF.read_text(encoding="utf-8")
    assert "SQL_VERSIONING_TEST_DATABASE_URL" in text
    assert "test-only-local-postgres" in text
    assert "postgresql://postgres:postgres@" not in text
