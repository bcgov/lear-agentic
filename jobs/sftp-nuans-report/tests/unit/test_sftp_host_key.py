# criterion: @R-05.1 @R-05.2 @R-05.3
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
"""Host-key verification default for sftp-nuans-report (CONFIG-004)."""
from unittest.mock import MagicMock

import paramiko
import pytest

from services.sftp import SFTPService


def _base_env(monkeypatch, tmp_path):
    monkeypatch.setenv('SFTP_HOST', 'sftp.example')
    monkeypatch.setenv('SFTP_PORT', '22')
    monkeypatch.setenv('SFTP_USERNAME', 'user')
    monkeypatch.setenv('BCREG_FTP_PRIVATE_KEY', 'dummy-key')
    monkeypatch.setenv('BCREG_FTP_PRIVATE_KEY_PASSPHRASE', '')
    (tmp_path / 'data').mkdir()
    monkeypatch.chdir(tmp_path)


def test_verify_on_missing_host_key_fails_closed(monkeypatch, tmp_path):
    """@R-05.1 — fail closed when verification is on and SFTP_HOST_KEY is missing."""
    _base_env(monkeypatch, tmp_path)
    monkeypatch.setenv('SFTP_VERIFY_HOST', 'true')
    monkeypatch.delenv('SFTP_HOST_KEY', raising=False)

    with pytest.raises(ValueError, match='SFTP_HOST_KEY is required'):
        SFTPService._connect()


def test_verify_default_when_unset_requires_and_installs_host_key(monkeypatch, tmp_path):
    """@R-05.2 — unset SFTP_VERIFY_HOST means verify on; known key is installed."""
    _base_env(monkeypatch, tmp_path)
    monkeypatch.delenv('SFTP_VERIFY_HOST', raising=False)
    key = paramiko.RSAKey.generate(1024)
    monkeypatch.setenv('SFTP_HOST_KEY', key.get_base64())

    captured = {}

    def fake_connection(**kwargs):
        captured.update(kwargs)
        return MagicMock()

    monkeypatch.setattr('services.sftp.Connection', fake_connection)

    SFTPService._connect()

    cnopts = captured['cnopts']
    assert cnopts.hostkeys is not None
    assert cnopts.hostkeys.lookup('sftp.example') is not None


def test_verify_false_disables_hostkeys(monkeypatch, tmp_path):
    """@R-05.3 — explicit local opt-out clears hostkeys."""
    _base_env(monkeypatch, tmp_path)
    monkeypatch.setenv('SFTP_VERIFY_HOST', 'false')
    monkeypatch.delenv('SFTP_HOST_KEY', raising=False)

    captured = {}

    def fake_connection(**kwargs):
        captured.update(kwargs)
        return MagicMock()

    monkeypatch.setattr('services.sftp.Connection', fake_connection)

    SFTPService._connect()

    assert captured['cnopts'].hostkeys is None
