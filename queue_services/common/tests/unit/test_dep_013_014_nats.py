# criterion: @R-713.1 @R-714.1 @R-714.2
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
"""DEP-013 / DEP-014: NATS client remediation and residual documentation."""
from __future__ import annotations

import re
from pathlib import Path

COMMON = Path(__file__).resolve().parents[2]
ROOT = Path(__file__).resolve().parents[4]
DATA_TOOL_REQ = ROOT / "data-tool" / "requirements.txt"
QUEUE_COMMON_REQ = COMMON / "requirements.txt"
QUEUE_COMMON_PROD = COMMON / "requirements" / "prod.txt"

VERSION_SPEC_RE = re.compile(r"(==|>=|<=|~=|!=|<|>)")


def _lines(path: Path) -> list[str]:
    return [
        ln.strip()
        for ln in path.read_text(encoding="utf-8").splitlines()
        if ln.strip() and not ln.strip().startswith("#")
    ]


def _line_for(path: Path, package: str) -> str:
    matches = []
    for line in _lines(path):
        name = re.split(r"[<>=!~;\s]", line, maxsplit=1)[0].strip()
        if name == package:
            matches.append(line)
    assert len(matches) == 1, f"{package} in {path}: {matches}"
    return matches[0]


def test_data_tool_uses_nats_py_not_deprecated_clients():
    """@R-713.1 — data-tool declares nats-py; deprecated asyncio-nats-* removed."""
    declared = {
        re.split(r"[<>=!~;\s]", line, maxsplit=1)[0].strip().lower()
        for line in _lines(DATA_TOOL_REQ)
    }
    assert "nats-py" in declared
    assert "asyncio-nats-client" not in declared
    assert "asyncio-nats-streaming" not in declared
    line = _line_for(DATA_TOOL_REQ, "nats-py")
    assert VERSION_SPEC_RE.search(line), line


def test_queue_common_nats_packages_are_pinned():
    """@R-714.1 — queue-common NATS deps carry version pins (coord. DEP-008)."""
    for path in (QUEUE_COMMON_REQ, QUEUE_COMMON_PROD):
        for package in ("asyncio-nats-client", "asyncio-nats-streaming"):
            line = _line_for(path, package)
            assert VERSION_SPEC_RE.search(line), f"{path}: {line}"


def test_queue_common_documents_nats_deprecation_residual():
    """@R-714.2 — requirements comment documents deprecation / JetStream residual."""
    text = QUEUE_COMMON_REQ.read_text(encoding="utf-8")
    assert "DEPRECATED" in text
    assert "JetStream" in text or "jetstream" in text.lower()
    assert "nats-py" in text.lower()
