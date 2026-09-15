# criterion: @R-715.1 @R-715.2
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
"""DEP-015: furnishings replaces flask-restplus with flask-restx."""
from __future__ import annotations

from pathlib import Path

FURNISHINGS = Path(__file__).resolve().parents[2]
PYPROJECT = FURNISHINGS / "pyproject.toml"


def test_flask_restplus_removed_from_pyproject():
    """@R-715.1 — flask-restplus absent from furnishings dependencies."""
    text = PYPROJECT.read_text(encoding="utf-8").lower()
    assert "flask-restplus" not in text


def test_flask_restx_declared():
    """@R-715.2 — flask-restx declared as the maintained successor."""
    text = PYPROJECT.read_text(encoding="utf-8")
    assert "flask-restx" in text.lower()
    assert ">=1.3.0" in text or ">=1.3" in text
