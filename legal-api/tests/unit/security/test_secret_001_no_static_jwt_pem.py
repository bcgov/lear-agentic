# criterion: @R-18.1
"""SECRET-001: TestConfig source must not embed a static RSA private key."""
from pathlib import Path

def test_legal_api_config_has_no_static_rsa_pem():
    text = Path(__file__).resolve().parents[3] / "src" / "legal_api" / "config.py"
    content = text.read_text()
    assert "BEGIN RSA PRIVATE KEY" not in content
    assert "ephemeral_jwt_oidc_test_material" in content
