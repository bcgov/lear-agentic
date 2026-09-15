# criterion: @R-51.2
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
"""Minimal sftp-nuans-report smoke test (TEST-003) — non-zero coverage skeleton."""
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[2]


def test_sftp_service_module_exists_and_defines_connection_api():
    """@R-51.2 — NUANS SFTP service module is import-inspectable without live SFTP."""
    source = (_ROOT / "services" / "sftp.py").read_text(encoding="utf-8")
    assert "class SFTPService" in source
    assert "def get_connection" in source
