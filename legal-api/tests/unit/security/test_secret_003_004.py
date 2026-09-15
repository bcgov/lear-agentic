# criterion: @R-48.1 @R-48.2 @R-49.1
"""SECRET-003/004: weak SECRET_KEY literals and Postman coops credentials."""
from __future__ import annotations

import json
import re
from importlib import reload
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[4]

CONFIG_PATHS = [
    REPO_ROOT / "legal-api/src/legal_api/config.py",
    REPO_ROOT / "colin-api/src/colin_api/config.py",
    REPO_ROOT / "gcp-jobs/update-legal-filings/src/update_legal_filings/config.py",
    REPO_ROOT / "gcp-jobs/update-colin-filings/src/update_colin_filings/config.py",
    REPO_ROOT / "gcp-jobs/involuntary-dissolutions/src/involuntary_dissolutions/config/config.py",
    REPO_ROOT / "gcp-jobs/future-effective-filings/src/future_effective_filings/config.py",
    REPO_ROOT / "gcp-jobs/furnishings/src/furnishings/config.py",
    REPO_ROOT / "gcp-jobs/expired-limited-restoration/src/expired_limited_restoration/config.py",
    REPO_ROOT / "gcp-jobs/email-reminder/src/email_reminder/config.py",
    REPO_ROOT / "gcp-jobs/bn-retry/src/bn_retry/config.py",
]

WEAK_LITERAL = re.compile(r"""SECRET_KEY\s*=\s*['\"]a secret['\"]""")


@pytest.mark.parametrize("path", CONFIG_PATHS, ids=[str(p.relative_to(REPO_ROOT)) for p in CONFIG_PATHS])
def test_config_files_have_no_weak_secret_key_literal(path: Path):
    """@R-48.1 — committed configs must not default SECRET_KEY to 'a secret'."""
    text = path.read_text(encoding="utf-8")
    assert path.is_file()
    assert not WEAK_LITERAL.search(text)
    assert 'os.getenv("SECRET_KEY"' in text or "os.getenv('SECRET_KEY'" in text
    assert "os.urandom(24)" in text


def test_legal_api_dev_config_uses_env_or_random(monkeypatch):
    """@R-48.1 @R-48.2 — DevConfig inherits env-or-random SECRET_KEY."""
    from legal_api import config

    monkeypatch.delenv("SECRET_KEY", raising=False)
    reload(config)
    generated = config.DevConfig.SECRET_KEY
    assert generated is not None
    assert generated != "a secret"
    assert generated != b"a secret"

    monkeypatch.setenv("SECRET_KEY", "from-env-for-test")
    reload(config)
    assert config.DevConfig.SECRET_KEY == "from-env-for-test"


def test_postman_collection_uses_coops_placeholders():
    """@R-49.1 — coops-updater-job username=password must not appear in bodies."""
    path = (
        Path(__file__).resolve().parents[2]
        / "postman"
        / "legal-api.postman_collection.json"
    )
    data = json.loads(path.read_text(encoding="utf-8"))
    blob = json.dumps(data)
    assert "coops-updater-job" not in blob
    assert "{{coops_updater_username}}" in blob
    assert "{{coops_updater_password}}" in blob
    assert blob.count("{{coops_updater_password}}") >= 11
