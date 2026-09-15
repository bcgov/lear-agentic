# criterion: @R-707.1 @R-707.2 @R-707.3
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
"""Pin assertions for DEP-007 (Flask / Werkzeug / flask-restx)."""
from pathlib import Path

_REQUIREMENTS = Path(__file__).resolve().parents[1] / "requirements.txt"


def _parse_version(version: str):
    """Parse a dotted version into a comparable integer tuple."""
    parts = []
    for piece in version.split("."):
        digits = "".join(ch for ch in piece if ch.isdigit())
        parts.append(int(digits) if digits else 0)
    return tuple(parts)


def _pinned_versions(path: Path) -> dict:
    """Parse package==version pins from a requirements freeze file."""
    pins = {}
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or line.startswith("git+"):
            continue
        # Drop trailing comments
        if "#" in line:
            line = line.split("#", 1)[0].strip()
        if "==" not in line:
            continue
        name, version = line.split("==", 1)
        pins[name.strip().lower()] = _parse_version(version.strip())
    return pins


def test_flask_pin_is_supported_3x():
    """@R-707.1 — Flask is directly pinned at 3.x >= 3.1.0."""
    pins = _pinned_versions(_REQUIREMENTS)
    assert "flask" in pins, "Flask must be a direct pin"
    assert pins["flask"][0] == 3, pins["flask"]
    assert pins["flask"] >= (3, 1, 0), pins["flask"]


def test_werkzeug_pin_is_supported_3x():
    """@R-707.2 — Werkzeug is directly pinned at 3.x >= 3.1.0."""
    pins = _pinned_versions(_REQUIREMENTS)
    assert "werkzeug" in pins, "Werkzeug must be a direct pin"
    assert pins["werkzeug"][0] == 3, pins["werkzeug"]
    assert pins["werkzeug"] >= (3, 1, 0), pins["werkzeug"]


def test_flask_restx_pin_supports_flask_3():
    """@R-707.3 — flask-restx is directly pinned at >= 1.3.0."""
    pins = _pinned_versions(_REQUIREMENTS)
    assert "flask-restx" in pins, "flask-restx must be a direct pin"
    assert pins["flask-restx"] >= (1, 3, 0), pins["flask-restx"]
