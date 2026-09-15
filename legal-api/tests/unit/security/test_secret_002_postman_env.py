# criterion: @R-19.1
"""SECRET-002: Postman env must not commit a live OIDC client_secret."""
from __future__ import annotations

import json
import re
from pathlib import Path

UUID_RE = re.compile(
    r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
    re.I,
)


def test_legal_dev_postman_client_secret_is_placeholder():
    path = Path(__file__).resolve().parents[2] / "postman" / "legal-dev.postman_environment.json"
    data = json.loads(path.read_text())
    secrets = [v for v in data["values"] if v.get("key") == "client_secret"]
    assert len(secrets) == 1
    value = secrets[0].get("value") or ""
    assert value == "" or value.startswith("<") or "do-not-commit" in value.lower()
    assert not UUID_RE.match(str(value))
