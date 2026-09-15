# criterion: @R-51.1
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
"""Minimal data-tool smoke tests for TEST-003 (non-zero coverage skeleton).

Does not claim full coverage — only proves pytest can execute against data-tool.
"""
import sys
from pathlib import Path

import pytest

_FLOWS = Path(__file__).resolve().parents[1] / "flows"
_DEV_REQUIREMENTS = Path(__file__).resolve().parents[1] / "requirements" / "dev.txt"


def test_pytest_is_listed_in_dev_requirements():
    """@R-51.1 — data-tool declares pytest so a test suite can run."""
    text = _DEV_REQUIREMENTS.read_text(encoding="utf-8").lower()
    assert "pytest" in text


def test_flows_config_get_int_defaults(monkeypatch):
    """@R-51.1 — smoke-exercise flows.config helper (one real assertion on code)."""
    # Stub dotenv so this smoke can run without the full data-tool dependency set.
    sys.modules.setdefault(
        "dotenv",
        type(sys)("dotenv"),
    )
    sys.modules["dotenv"].find_dotenv = lambda *a, **k: ""
    sys.modules["dotenv"].load_dotenv = lambda *a, **k: False

    sys.path.insert(0, str(_FLOWS))
    import config as flows_config  # noqa: E402

    monkeypatch.delenv("TEST003_MISSING_INT", raising=False)
    assert flows_config._get_int("TEST003_MISSING_INT", 7) == 7
    monkeypatch.setenv("TEST003_MISSING_INT", "42")
    assert flows_config._get_int("TEST003_MISSING_INT", 0) == 42
