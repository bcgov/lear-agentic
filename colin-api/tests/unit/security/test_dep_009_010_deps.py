# criterion: @R-709.1 @R-710.1 @R-710.2
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
"""DEP-009 / DEP-010: python-jose floor and oracledb migration."""
from __future__ import annotations

import re
from pathlib import Path

COLIN_API = Path(__file__).resolve().parents[3]
REQUIREMENTS = COLIN_API / "requirements.txt"
PROD_REQUIREMENTS = COLIN_API / "requirements" / "prod.txt"
DB_PY = COLIN_API / "src" / "colin_api" / "resources" / "db.py"
OPS_PY = COLIN_API / "src" / "colin_api" / "resources" / "ops.py"

PIN_RE = re.compile(r"^([A-Za-z0-9_.\-]+)==([^\s#]+)\s*$")


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


def test_python_jose_meets_floor():
    """@R-709.1 — python-jose ≥ 3.4.0."""
    pins = _pinned_versions(REQUIREMENTS)
    assert "python-jose" in pins
    assert _version_tuple(pins["python-jose"]) >= (3, 4, 0), pins["python-jose"]


def test_oracledb_replaces_cx_oracle_in_manifests():
    """@R-710.1 — oracledb declared; cx-Oracle / cx_Oracle absent from manifests."""
    pins = _pinned_versions(REQUIREMENTS)
    assert "oracledb" in pins
    assert _version_tuple(pins["oracledb"]) >= (3, 0, 0), pins["oracledb"]
    req_text = REQUIREMENTS.read_text(encoding="utf-8").lower()
    prod_text = PROD_REQUIREMENTS.read_text(encoding="utf-8").lower()
    assert "cx-oracle" not in req_text
    assert "cx_oracle" not in req_text
    assert "cx_oracle" not in prod_text
    assert "oracledb" in prod_text


def test_oracle_modules_use_oracledb_thin_alias():
    """@R-710.2 — db/ops import oracledb as cx_Oracle (thin-mode alias)."""
    db_src = DB_PY.read_text(encoding="utf-8")
    ops_src = OPS_PY.read_text(encoding="utf-8")
    assert "import oracledb as cx_Oracle" in db_src
    assert "import oracledb as cx_Oracle" in ops_src
    assert "import cx_Oracle\n" not in db_src
    assert "import cx_Oracle\n" not in ops_src
