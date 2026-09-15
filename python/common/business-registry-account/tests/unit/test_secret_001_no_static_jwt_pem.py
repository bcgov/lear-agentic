# criterion: @R-18.2
"""SECRET-001: business-account TestConfig must not embed static RSA PEM."""
from pathlib import Path

def test_business_account_config_has_no_static_rsa_pem():
    root = Path(__file__).resolve().parents[2] / "src" / "business_account" / "config.py"
    content = root.read_text()
    assert "BEGIN RSA PRIVATE KEY" not in content
    assert "ephemeral_jwt_oidc_test_material" in content
