# criterion: @R-51.3
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
"""Minimal dbc-message-sender smoke test (TEST-003) — non-zero coverage skeleton."""
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]


def test_message_sender_defines_token_helper():
    """@R-51.3 — message-sender script exposes get_token without claiming live Traction coverage."""
    source = (_ROOT / "message-sender.py").read_text(encoding="utf-8")
    assert "def get_token" in source
    assert "TOKEN_URL" in source
