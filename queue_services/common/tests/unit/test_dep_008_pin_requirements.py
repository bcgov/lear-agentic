# criterion: @R-708.1 @R-708.2
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
"""DEP-008: queue-services-common production deps must carry version pins."""
from __future__ import annotations

import re
from pathlib import Path

REQUIREMENTS = Path(__file__).resolve().parents[2] / "requirements.txt"

REQUIRED_PACKAGES = (
    "aiohttp",
    "attrs",
    "python-dotenv",
    "sentry-sdk[flask]",
    "asyncio-nats-client",
    "asyncio-nats-streaming",
)

# PEP 508 environment markers aside: require a version comparison operator.
VERSION_SPEC_RE = re.compile(r"(==|>=|<=|~=|!=|<|>)")


def _requirement_lines() -> list[str]:
    return [
        ln.strip()
        for ln in REQUIREMENTS.read_text(encoding="utf-8").splitlines()
        if ln.strip() and not ln.strip().startswith("#")
    ]


def _line_for(package: str) -> str:
    """Return the requirements line whose name matches package (extras OK)."""
    matches = []
    for line in _requirement_lines():
        name = re.split(r"[<>=!~;\s]", line, maxsplit=1)[0].strip()
        if name == package:
            matches.append(line)
    assert len(matches) == 1, f"expected one line for {package!r}, got {matches!r}"
    return matches[0]


def test_all_required_packages_are_declared():
    """@R-708.1 — the six shared packages remain listed."""
    declared = {
        re.split(r"[<>=!~;\s]", line, maxsplit=1)[0].strip()
        for line in _requirement_lines()
    }
    missing = [pkg for pkg in REQUIRED_PACKAGES if pkg not in declared]
    assert not missing, f"missing packages: {missing!r}; declared={declared!r}"


def test_each_required_package_has_version_specifier():
    """@R-708.1 @R-708.2 — no bare unpinned package names."""
    for package in REQUIRED_PACKAGES:
        line = _line_for(package)
        assert VERSION_SPEC_RE.search(line), (
            f"unpinned or malformed requirement for {package!r}: {line!r}"
        )
