# criterion: @R-704.1 @R-704.2
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
"""DEP-004: registry_schemas must be pinned to a git commit SHA."""
from __future__ import annotations

import re
from pathlib import Path

REQUIREMENTS = (
    Path(__file__).resolve().parents[3] / "requirements.txt"
)
PIN_RE = re.compile(
    r"^git\+https://github\.com/bcgov/business-schemas\.git"
    r"@([0-9a-f]{40})#egg=registry_schemas\s*$"
)
FLOATING = {"main", "master", "HEAD", "develop", "dev"}


def _registry_schemas_line() -> str:
    lines = [
        ln.strip()
        for ln in REQUIREMENTS.read_text(encoding="utf-8").splitlines()
        if "business-schemas" in ln and "registry_schemas" in ln
    ]
    assert len(lines) == 1, f"expected one registry_schemas line, got {lines!r}"
    return lines[0]


def test_business_schemas_pinned_to_commit_sha():
    """@R-704.1 — dependency uses @<sha>#egg=registry_schemas form."""
    line = _registry_schemas_line()
    match = PIN_RE.match(line)
    assert match, f"unpinned or malformed business-schemas line: {line!r}"


def test_business_schemas_pin_is_not_floating_ref():
    """@R-704.2 — revision after @ is a full hex SHA, not a branch/tag name."""
    line = _registry_schemas_line()
    match = PIN_RE.match(line)
    assert match, f"cannot validate pin form: {line!r}"
    sha = match.group(1)
    assert sha.lower() == sha
    assert sha not in FLOATING
    assert re.fullmatch(r"[0-9a-f]{40}", sha)
