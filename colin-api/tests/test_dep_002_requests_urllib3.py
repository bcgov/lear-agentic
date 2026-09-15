# criterion: @R-702.1 @R-702.2
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
"""Pin assertions for DEP-002 (requests / urllib3)."""
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


def test_requests_pin_meets_secure_floor():
    """@R-702.1 — requests is directly pinned at >= 2.32.3."""
    pins = _pinned_versions(_REQUIREMENTS)
    assert "requests" in pins, "requests must be a direct pin"
    assert pins["requests"] >= (2, 32, 3), pins["requests"]


def test_urllib3_pin_meets_secure_2x_floor():
    """@R-702.2 — urllib3 is directly pinned at 2.x >= 2.2.0."""
    pins = _pinned_versions(_REQUIREMENTS)
    assert "urllib3" in pins, "urllib3 must be a direct pin"
    assert pins["urllib3"][0] == 2, pins["urllib3"]
    assert pins["urllib3"] >= (2, 2, 0), pins["urllib3"]
