# criterion: @R-06.1
# Copyright © 2026 Province of British Columbia
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Unit tests for Legal API HTTP security headers (CONFIG-001)."""
import importlib.util
from pathlib import Path

_MODULE_PATH = (
    Path(__file__).resolve().parents[3]
    / "src"
    / "legal_api"
    / "utils"
    / "security_headers.py"
)


def _load_security_headers():
    """Load helper from source without importing the full legal_api package."""
    spec = importlib.util.spec_from_file_location(
        "legal_api_utils_security_headers", _MODULE_PATH
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


_mod = _load_security_headers()
apply_security_headers = _mod.apply_security_headers
SECURITY_HEADERS = _mod.SECURITY_HEADERS


class _FakeResponse:
    """Minimal response stand-in with a mutable headers mapping."""

    def __init__(self, headers=None):
        self.headers = dict(headers or {})


def test_security_headers_present():
    """@R-06.1 — required security headers are set on the response."""
    response = _FakeResponse()
    apply_security_headers(response)

    for header, value in SECURITY_HEADERS.items():
        assert response.headers[header] == value

    assert response.headers["X-Frame-Options"] == "DENY"
    assert response.headers["X-Content-Type-Options"] == "nosniff"
    assert "default-src 'none'" in response.headers["Content-Security-Policy"]
    assert "frame-ancestors 'none'" in response.headers["Content-Security-Policy"]
    assert response.headers["Strict-Transport-Security"].startswith("max-age=")
    assert response.headers["Referrer-Policy"] == "no-referrer"
    assert "camera=()" in response.headers["Permissions-Policy"]


def test_security_headers_preserve_version_headers():
    """@R-06.2 — existing API / SCHEMAS version headers are not cleared."""
    response = _FakeResponse(
        {
            "API": "legal_api/9.9.9",
            "SCHEMAS": "registry_schemas/1.2.3",
        }
    )
    apply_security_headers(response)

    assert response.headers["API"] == "legal_api/9.9.9"
    assert response.headers["SCHEMAS"] == "registry_schemas/1.2.3"
    assert response.headers["X-Content-Type-Options"] == "nosniff"


def test_csp_is_api_oriented_not_browser_app_policy():
    """@R-06.3 — CSP stays suitable for JSON/PDF API responses."""
    response = _FakeResponse()
    apply_security_headers(response)
    csp = response.headers["Content-Security-Policy"]

    # Must not require 'unsafe-inline' / broad script sources (API is not a SPA).
    assert "unsafe-inline" not in csp
    assert "script-src" not in csp
    assert csp.startswith("default-src 'none'")
