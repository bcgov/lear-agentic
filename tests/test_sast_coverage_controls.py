# criterion: @R-20.1 @R-20.2 @R-20.3 @R-21.1 @R-21.2 @R-21.3
"""Assert SAST workflows and coverage fail-under config for TEST-001 / TEST-002."""
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[1]
_WORKFLOWS = _REPO_ROOT / ".github" / "workflows"


def test_codeql_analysis_workflow_committed():
    """@R-20.1 — codeql-analysis.yml exists and analyzes pull requests."""
    path = _WORKFLOWS / "codeql-analysis.yml"
    assert path.is_file()
    text = path.read_text(encoding="utf-8")
    assert "codeql-action" in text
    assert "pull_request" in text


def test_bandit_workflow_covers_legal_and_colin():
    """@R-20.2 @R-20.3 — Bandit workflow targets legal-api and colin-api."""
    path = _WORKFLOWS / "python-sast-bandit.yml"
    assert path.is_file()
    text = path.read_text(encoding="utf-8")
    assert "bandit" in text.lower()
    assert "legal-api" in text
    assert "colin-api" in text


def test_legal_api_cov_fail_under_configured():
    """@R-21.1 — legal-api pyproject addopts include --cov-fail-under."""
    text = (_REPO_ROOT / "legal-api" / "pyproject.toml").read_text(encoding="utf-8")
    token = [p for p in text.replace('"', " ").split() if p.startswith("--cov-fail-under=")][0]
    threshold = int(token.split("=", 1)[1])
    assert 40 <= threshold <= 70


def test_colin_api_cov_fail_under_configured():
    """@R-21.2 — colin-api setup.cfg addopts include --cov-fail-under."""
    text = (_REPO_ROOT / "colin-api" / "setup.cfg").read_text(encoding="utf-8")
    token = [p for p in text.replace('"', " ").split() if p.startswith("--cov-fail-under=")][0]
    threshold = int(token.split("=", 1)[1])
    assert 20 <= threshold <= 40


def test_codecov_flag_targets_configured():
    """@R-21.3 — codecov.yaml has explicit legalapi / colinapi targets."""
    text = (_REPO_ROOT / "codecov.yaml").read_text(encoding="utf-8")
    assert "legalapi:" in text
    assert "colinapi:" in text
    assert "target: 70%" in text or "target: 70" in text
    assert "target: 25%" in text or "target: 25" in text
