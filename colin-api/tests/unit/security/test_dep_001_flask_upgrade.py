# criterion: @R-701.1 @R-701.2 @R-701.3 @R-701.4
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
"""DEP-001: Flask / Werkzeug stack must meet advisory floors."""
from __future__ import annotations

import re
from pathlib import Path

COLIN_API = Path(__file__).resolve().parents[3]
REQUIREMENTS = COLIN_API / "requirements.txt"
PROD_REQUIREMENTS = COLIN_API / "requirements" / "prod.txt"

PIN_RE = re.compile(r"^([A-Za-z0-9_.\-]+)==([^\s#]+)\s*$")

# Advisory / Flask 2.3 floors for DEP-001 partial secure upgrade.
MIN_PINS = {
    "Flask": (2, 3, 2),
    "Werkzeug": (2, 2, 3),
    "Jinja2": (3, 1, 2),
    "MarkupSafe": (2, 1, 1),
    "itsdangerous": (2, 1, 2),
    "click": (8, 1, 3),
    "blinker": (1, 6, 2),
    "flask-restx": (1, 3, 0),
}


def _version_tuple(ver: str) -> tuple[int, ...]:
    parts = []
    for piece in ver.split("."):
        digits = re.match(r"(\d+)", piece)
        if not digits:
            break
        parts.append(int(digits.group(1)))
    return tuple(parts)


def _pinned_versions(path: Path) -> dict[str, str]:
    pins: dict[str, str] = {}
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or line.startswith("git+"):
            continue
        match = PIN_RE.match(line)
        if match:
            pins[match.group(1)] = match.group(2)
    return pins


def test_flask_and_werkzeug_meet_advisory_floors():
    """@R-701.1 — Flask ≥ 2.3.2 and Werkzeug ≥ 2.2.3."""
    pins = _pinned_versions(REQUIREMENTS)
    assert "Flask" in pins, "Flask pin missing from requirements.txt"
    assert "Werkzeug" in pins, "Werkzeug pin missing from requirements.txt"
    assert _version_tuple(pins["Flask"]) >= MIN_PINS["Flask"], pins["Flask"]
    assert _version_tuple(pins["Werkzeug"]) >= MIN_PINS["Werkzeug"], pins["Werkzeug"]


def test_companion_pins_meet_flask_23_floors():
    """@R-701.2 — Jinja2 / MarkupSafe / itsdangerous / click / blinker floors."""
    pins = _pinned_versions(REQUIREMENTS)
    for name in ("Jinja2", "MarkupSafe", "itsdangerous", "click", "blinker"):
        assert name in pins, f"{name} pin missing"
        assert _version_tuple(pins[name]) >= MIN_PINS[name], f"{name}=={pins[name]}"


def test_flask_restx_upgraded_off_030():
    """@R-701.3 — flask-restx ≥ 1.3.0 (was 0.3.0)."""
    pins = _pinned_versions(REQUIREMENTS)
    assert "flask-restx" in pins
    assert _version_tuple(pins["flask-restx"]) >= MIN_PINS["flask-restx"], pins["flask-restx"]
    assert pins["flask-restx"] != "0.3.0"


def test_flask_script_removed_from_manifests():
    """@R-701.4 — Flask-Script absent from pinned and prod requirements."""
    pinned_text = REQUIREMENTS.read_text(encoding="utf-8")
    prod_text = PROD_REQUIREMENTS.read_text(encoding="utf-8")
    assert "Flask-Script" not in pinned_text
    assert "Flask-Script" not in prod_text
    assert "flask-script" not in pinned_text.lower()
    assert "flask-script" not in prod_text.lower()
