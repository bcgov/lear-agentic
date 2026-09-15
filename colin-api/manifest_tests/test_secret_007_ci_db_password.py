"""SECRET-007: CI workflow avoids literal postgres password."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WF = ROOT / ".github/workflows/colin-api-ci.yml"


def test_colin_api_ci_uses_ephemeral_password_expression():
    text = WF.read_text(encoding="utf-8")
    assert "ci-ephemeral-" in text
    assert "github.run_id" in text
    # Job/service password assignments must not be the bare literal
    assert "DATABASE_TEST_PASSWORD: postgres" not in text
    assert "DATABASE_PASSWORD: postgres" not in text
    assert "POSTGRES_PASSWORD: postgres" not in text
