# criterion: @R-50.1
"""SECRET-005: data-tool docker-compose must not commit real-looking secrets."""
from __future__ import annotations

from pathlib import Path

COMPOSE = Path(__file__).resolve().parents[1] / "docker-compose.yaml"

FORBIDDEN = (
    "test-password",
    "hasura-secret-admin-secret",
)


def test_docker_compose_uses_env_substitution_for_secrets():
    text = COMPOSE.read_text(encoding="utf-8")
    for token in FORBIDDEN:
        assert token not in text, f"forbidden committed secret token: {token}"
    assert "${POSTGRES_PASSWORD:-dev-only-change-me}" in text
    assert "${HASURA_GRAPHQL_ADMIN_SECRET:-dev-only-change-me}" in text
    assert "PREFECT_SERVER__DATABASE__CONNECTION_URL:" in text
    assert "HASURA_GRAPHQL_DATABASE_URL:" in text
    assert "POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-dev-only-change-me}" in text
