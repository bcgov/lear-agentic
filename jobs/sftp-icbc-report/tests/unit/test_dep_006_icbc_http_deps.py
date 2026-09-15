# criterion: @R-706.1 @R-706.2 @R-706.3
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
"""DEP-006: sftp-icbc-report HTTP client pins must meet secure floors."""
from __future__ import annotations

import re
from pathlib import Path

REQUIREMENTS = Path(__file__).resolve().parents[2] / "requirements.txt"
PIN_RE = re.compile(r"^([A-Za-z0-9_.-]+)==([0-9]+(?:\.[0-9]+)*)$")


def _parse_pins() -> dict[str, tuple[int, ...]]:
    pins: dict[str, tuple[int, ...]] = {}
    for raw in REQUIREMENTS.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or line.startswith("git+"):
            continue
        match = PIN_RE.match(line)
        if not match:
            continue
        name, version = match.group(1), match.group(2)
        pins[name.lower()] = tuple(int(p) for p in version.split("."))
    return pins


def _gte(actual: tuple[int, ...], floor: tuple[int, ...]) -> bool:
    width = max(len(actual), len(floor))
    a = actual + (0,) * (width - len(actual))
    f = floor + (0,) * (width - len(floor))
    return a >= f


def test_requests_pin_meets_secure_floor():
    """@R-706.1 — requests pin is >= 2.32.3."""
    pins = _parse_pins()
    assert "requests" in pins, "requests pin missing from requirements.txt"
    assert _gte(pins["requests"], (2, 32, 3)), pins["requests"]


def test_urllib3_pin_meets_secure_2x_floor():
    """@R-706.2 — urllib3 pin is 2.x and >= 2.2.0."""
    pins = _parse_pins()
    assert "urllib3" in pins, "urllib3 pin missing from requirements.txt"
    major = pins["urllib3"][0]
    assert major == 2, f"expected urllib3 2.x, got {pins['urllib3']}"
    assert _gte(pins["urllib3"], (2, 2, 0)), pins["urllib3"]


def test_certifi_pin_is_current():
    """@R-706.3 — certifi pin is >= 2026.7.22."""
    pins = _parse_pins()
    assert "certifi" in pins, "certifi pin missing from requirements.txt"
    assert _gte(pins["certifi"], (2026, 7, 22)), pins["certifi"]
