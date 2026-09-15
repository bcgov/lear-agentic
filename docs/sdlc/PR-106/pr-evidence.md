# PR evidence

## LOG-014 (issue #58)
- `legal-api/.../document_service.py` logs warning on decode/JSON failures in `get_content`

## LOG-015 (issue #59)
- `permissions.py` denial paths log `actor_id` (JWT `sub`), `roles_present` (bool), and resource id/filing key
- Avoids email/preferred_username in these denial lines

## TEST-005 (issue #66)
- Added `.github/workflows/legal-api-postman-validate.yml` — newman/`postman-collection` syntax validate, no network execution
- Residual: live Newman smoke against deployed envs still manual (needs secrets)
