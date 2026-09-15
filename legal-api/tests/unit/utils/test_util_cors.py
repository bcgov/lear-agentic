# Copyright © 2019 Province of British Columbia
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

"""Tests for Legal API CORS origin allowlist (CONFIG-007)."""
import importlib.util
from pathlib import Path

import pytest

_ROOT = Path(__file__).resolve().parents[3]
_CORS_PATH = _ROOT / "src" / "legal_api" / "utils" / "cors.py"
_UTIL_PATH = _ROOT / "src" / "legal_api" / "utils" / "util.py"
_INIT_PATH = _ROOT / "src" / "legal_api" / "__init__.py"
_ENDPOINTS_PATH = _ROOT / "src" / "legal_api" / "resources" / "endpoints.py"


def _load_cors():
    spec = importlib.util.spec_from_file_location("legal_api_utils_cors", _CORS_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.mark.parametrize(
    "methods",
    ["GET", "PUT", "POST", "GET,PUT", "GET,POST", "PUT,POST", "GET,PUT,POST"],
)
def test_cors_fail_closed_without_allowlist(methods, monkeypatch):
    """@R-26.1 — empty CORS_ORIGINS never emits Access-Control-Allow-Origin."""
    monkeypatch.setenv("CORS_ORIGINS", "")
    cors = _load_cors()

    headers = {
        "Access-Control-Allow-Methods": methods,
        "Access-Control-Allow-Headers": "Authorization, Content-Type, App-Name",
    }
    cors.apply_cors_allow_origin(headers, request_origin="https://evil.example")

    assert "Access-Control-Allow-Origin" not in headers
    assert headers["Access-Control-Allow-Methods"] == methods
    assert cors.resolve_cors_allow_origin("https://evil.example") is None


def test_cors_echoes_only_listed_origins(monkeypatch):
    """@R-26.2 — listed Origin is echoed; unlisted Origin is omitted."""
    monkeypatch.setenv(
        "CORS_ORIGINS",
        "https://www.bcregistry.gov.bc.ca, https://dev.example",
    )
    cors = _load_cors()

    assert (
        cors.resolve_cors_allow_origin("https://www.bcregistry.gov.bc.ca")
        == "https://www.bcregistry.gov.bc.ca"
    )
    assert cors.resolve_cors_allow_origin("https://evil.example") is None

    headers = cors.apply_cors_allow_origin(
        {},
        request_origin="https://dev.example",
    )
    assert headers["Access-Control-Allow-Origin"] == "https://dev.example"
    assert headers["Vary"] == "Origin"

    denied = cors.apply_cors_allow_origin({}, request_origin="https://evil.example")
    assert "Access-Control-Allow-Origin" not in denied


def test_cors_rejects_wildcard_and_clears_hardcoded_star(monkeypatch):
    """@R-26.3 — CORS_ORIGINS=* stays fail-closed; call sites no longer hardcode *."""
    monkeypatch.setenv("CORS_ORIGINS", "*")
    cors = _load_cors()

    assert cors.parse_cors_origins("*") == set()
    assert cors.resolve_cors_allow_origin("https://www.bcregistry.gov.bc.ca") is None

    for path in (_UTIL_PATH, _INIT_PATH, _ENDPOINTS_PATH):
        text = path.read_text(encoding="utf-8")
        assert 'Access-Control-Allow-Origin"] = "*"' not in text
        assert 'Access-Control-Allow-Origin": "*"' not in text
        assert "'Access-Control-Allow-Origin': '*'" not in text
