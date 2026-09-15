# criterion: @R-03.1
# Copyright © 2024 Province of British Columbia
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
"""Host-key verification behaviour for furnishings SFTP (CONFIG-003)."""
import paramiko
import pytest

from furnishings.sftp import SftpConnection


def test_verify_host_requires_host_key(app):
    """@R-03.1 — fail closed when verification is on and no host key is configured."""
    conn = SftpConnection(
        username="user",
        password="pwd",
        host="sftp.example",
        port=22,
        verify_host=True,
        host_key=None,
    )
    with app.app_context(), pytest.raises(ValueError, match="host_key is required"):
        with conn:
            pass


def test_verify_host_uses_reject_policy(app, monkeypatch):
    """@R-03.2 — production path installs RejectPolicy, not AutoAddPolicy."""
    policies = []

    class FakeClient:
        def set_missing_host_key_policy(self, policy):
            policies.append(policy)

        def get_host_keys(self):
            class Keys:
                def add(self, *_args, **_kwargs):
                    return None

            return Keys()

        def connect(self, **_kwargs):
            raise RuntimeError("stop-before-transport")

        def close(self):
            return None

    monkeypatch.setattr(paramiko, "SSHClient", FakeClient)

    # Minimal valid RSA key blob (base64 of empty-ish will fail decode) — use a real tiny key.
    # Generate via paramiko RSAKey.generate for the unit test.
    key = paramiko.RSAKey.generate(1024)
    from io import BytesIO
    from base64 import encodebytes

    bio = BytesIO()
    # paramiko expects the raw key data as used by RSAKey(data=...)
    # Use get_base64() which is the key body without headers.
    host_key_b64 = key.get_base64()

    conn = SftpConnection(
        username="user",
        password="pwd",
        host="sftp.example",
        port=22,
        verify_host=True,
        host_key=host_key_b64,
        host_key_algorithm="ssh-rsa",
    )
    with app.app_context():
        with pytest.raises(RuntimeError, match="stop-before-transport"):
            with conn:
                pass

    assert len(policies) == 1
    assert isinstance(policies[0], paramiko.RejectPolicy)


def test_verify_host_false_allows_auto_add(app, monkeypatch):
    """@R-03.3 — explicit harness opt-out may use AutoAddPolicy."""
    policies = []

    class FakeClient:
        def set_missing_host_key_policy(self, policy):
            policies.append(policy)

        def connect(self, **_kwargs):
            raise RuntimeError("stop-before-transport")

        def close(self):
            return None

    monkeypatch.setattr(paramiko, "SSHClient", FakeClient)

    conn = SftpConnection(
        username="user",
        password="pwd",
        host="sftp.example",
        port=22,
        verify_host=False,
    )
    with app.app_context():
        with pytest.raises(RuntimeError, match="stop-before-transport"):
            with conn:
                pass

    assert len(policies) == 1
    assert isinstance(policies[0], paramiko.AutoAddPolicy)
