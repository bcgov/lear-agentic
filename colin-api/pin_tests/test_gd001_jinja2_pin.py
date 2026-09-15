# criterion: @R-37.1
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
"""Pin assertions for GD-001 (Jinja2 xmlattr XSS floor)."""
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
        if "==" not in line:
            continue
        name, version = line.split("==", 1)
        pins[name.strip().lower()] = _parse_version(version.strip())
    return pins


def test_jinja2_pin_meets_xmlattr_floor():
    """@R-37.1 — Jinja2 is directly pinned at >= 3.1.3 with MarkupSafe companion."""
    pins = _pinned_versions(_REQUIREMENTS)
    assert "jinja2" in pins, "Jinja2 must be a direct pin"
    assert pins["jinja2"] >= (3, 1, 3)
    assert pins["jinja2"] == (3, 1, 4)
    assert "markupsafe" in pins
    assert pins["markupsafe"] >= (2, 1, 0)
    # Coordinate with Flask 1.1.2 stack still on this branch; Flask 2.3 bump is DEP-001.
    assert pins.get("flask") == (1, 1, 2)
