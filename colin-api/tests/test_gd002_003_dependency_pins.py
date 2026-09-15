# criterion: @R-14.1 @R-15.1
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
"""Pin assertions for GD-002 (ecdsa) and GD-003 (gunicorn)."""
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


def test_ecdsa_pin_meets_minerva_floor():
    """@R-14.1 — ecdsa is directly pinned at >= 0.19.0."""
    pins = _pinned_versions(_REQUIREMENTS)
    assert "ecdsa" in pins, "ecdsa must be a direct pin (wins over python-jose)"
    assert pins["ecdsa"] >= (0, 19, 0)
    assert pins["ecdsa"] == (0, 19, 1)


def test_gunicorn_pin_meets_transfer_encoding_floor():
    """@R-15.1 — gunicorn is pinned at >= 22.0.0 (prefer Legal API 23.x)."""
    pins = _pinned_versions(_REQUIREMENTS)
    assert "gunicorn" in pins
    assert pins["gunicorn"] >= (22, 0, 0)
    assert pins["gunicorn"] == (23, 0, 0)
