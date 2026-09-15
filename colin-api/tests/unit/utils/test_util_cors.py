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

"""Tests for COLIN API CORS origin allowlist (CONFIG-008)."""
import importlib.util
from pathlib import Path

import pytest

_ROOT = Path(__file__).resolve().parents[3]
_CORS_PATH = _ROOT / "src" / "colin_api" / "utils" / "cors.py"
_UTIL_PATH = _ROOT / "src" / "colin_api" / "utils" / "util.py"


def _load_cors():
    spec = importlib.util.spec_from_file_location("colin_api_utils_cors", _CORS_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.mark.parametrize(
    "methods",
    ["GET", "PUT", "POST", "GET,PUT", "GET,POST", "PUT,POST", "GET,PUT,POST"],
)
def test_cors_fail_closed_without_allowlist(methods, monkeypatch):
    """@R-27.1 — empty CORS_ORIGINS never emits Access-Control-Allow-Origin."""
    monkeypatch.setenv("CORS_ORIGINS", "")
    cors = _load_cors()

    headers = {
        "Access-Control-Allow-Methods": methods,
        "Access-Control-Allow-Headers":
            "Authorization, Content-Type, App-Name, Account-Id, X-Apikey",
    }
    cors.apply_cors_allow_origin(headers, request_origin="https://evil.example")

    assert "Access-Control-Allow-Origin" not in headers
    assert headers["Access-Control-Allow-Methods"] == methods
    assert cors.resolve_cors_allow_origin("https://evil.example") is None


def test_cors_echoes_only_listed_origins(monkeypatch):
    """@R-27.2 — listed Origin is echoed; unlisted Origin is omitted."""
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


def test_cors_rejects_wildcard_and_clears_hardcoded_star(monkeypatch):
    """@R-27.3 — CORS_ORIGINS=* stays fail-closed; cors_preflight no longer hardcodes *."""
    monkeypatch.setenv("CORS_ORIGINS", "*")
    cors = _load_cors()

    assert cors.parse_cors_origins("*") == set()
    assert cors.resolve_cors_allow_origin("https://www.bcregistry.gov.bc.ca") is None

    text = _UTIL_PATH.read_text(encoding="utf-8")
    assert "'Access-Control-Allow-Origin': '*'" not in text
    assert '"Access-Control-Allow-Origin": "*"' not in text
