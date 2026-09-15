"""Guards for LOG-014, LOG-015, TEST-005."""
from pathlib import Path

LEGAL_API = Path(__file__).resolve().parents[3]
REPO = LEGAL_API.parent


def test_document_service_logs_on_decode_failure():
    text = (LEGAL_API / "src/legal_api/reports/document_service.py").read_text(encoding="utf-8")
    assert "except Exception:\n            pass" not in text
    assert "get_content could not decode/parse" in text


def test_permissions_denial_logs_actor_and_resource():
    text = (LEGAL_API / "src/legal_api/services/permissions.py").read_text(encoding="utf-8")
    assert "actor_id=" in text
    assert "roles_present=" in text
    assert "_actor_audit_fields" in text


def test_postman_validate_workflow_exists():
    wf = REPO / ".github/workflows/legal-api-postman-validate.yml"
    assert wf.is_file()
    body = wf.read_text(encoding="utf-8")
    assert "newman" in body
    assert "legal-api.postman_collection.json" in body
