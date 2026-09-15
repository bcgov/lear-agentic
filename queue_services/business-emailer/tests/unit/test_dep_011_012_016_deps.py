# criterion: @R-711.1 @R-712.1 @R-716.1
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
"""DEP-011 / DEP-012 / DEP-016: emailer LD + protobuf, bn protobuf."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EMAILER_PYPROJECT = ROOT / "queue_services" / "business-emailer" / "pyproject.toml"
BN_PYPROJECT = ROOT / "queue_services" / "business-bn" / "pyproject.toml"
EMAILER_FLAGS = (
    ROOT
    / "queue_services"
    / "business-emailer"
    / "src"
    / "business_emailer"
    / "services"
    / "flags.py"
)


def _dep_line(path: Path, name: str) -> str:
    text = path.read_text(encoding="utf-8")
    match = re.search(rf'^{re.escape(name)}\s*=\s*"([^"]+)"\s*$', text, re.MULTILINE)
    assert match, f"{name} missing from {path}"
    return match.group(1)


def test_emailer_launchdarkly_meets_platform_floor():
    """@R-711.1 — launchdarkly-server-sdk ≥ 9.10."""
    spec = _dep_line(EMAILER_PYPROJECT, "launchdarkly-server-sdk")
    assert "9.10" in spec or re.search(r">=\s*9\.1[0-9]", spec), spec
    assert "<10" in spec or "<10.0.0" in spec, spec
    flags = EMAILER_FLAGS.read_text(encoding="utf-8")
    assert "from ldclient.context import Context" in flags
    assert "ldclient.integrations import Files" in flags
    assert "_FileDataSource" not in flags


def test_emailer_protobuf_constraint_relaxed():
    """@R-712.1 — business-emailer protobuf allows modern 4.x/5.x."""
    spec = _dep_line(EMAILER_PYPROJECT, "protobuf")
    assert "==3.20.*" not in spec
    assert "<6" in spec or "<6.0.0" in spec, spec
    assert ">=4.25" in spec or ">=4." in spec, spec


def test_bn_protobuf_constraint_relaxed():
    """@R-716.1 — business-bn protobuf no longer capped below 3.20."""
    spec = _dep_line(BN_PYPROJECT, "protobuf")
    assert "<3.20" not in spec
    assert ">=4.25" in spec or ">=4." in spec, spec
    assert "<6" in spec or "<6.0.0" in spec, spec
