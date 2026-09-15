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


def test_missing_host_key_fails_closed(app):
    """@R-03.1 — fail closed when no host key is configured."""
    conn = SftpConnection(
        username="user",
        password="pwd",
        host="sftp.example",
        port=22,
        host_key=None,
    )
    with app.app_context(), pytest.raises(ValueError, match="host_key is required"), conn:
        pass


def test_uses_reject_policy_with_configured_key(app, monkeypatch):
    """@R-03.2 — production path installs RejectPolicy and registers the known key."""
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

    key = paramiko.RSAKey.generate(1024)
    conn = SftpConnection(
        username="user",
        password="pwd",
        host="sftp.example",
        port=22,
        host_key=key.get_base64(),
        host_key_algorithm="ssh-rsa",
    )
    with (
        app.app_context(),
        pytest.raises(RuntimeError, match="stop-before-transport"),
        conn,
    ):
        pass

    assert len(policies) == 1
    assert isinstance(policies[0], paramiko.RejectPolicy)
    assert not any(isinstance(p, paramiko.AutoAddPolicy) for p in policies)


def test_fixture_connection_uses_reject_policy(app, sftpconnection, monkeypatch):
    """@R-03.3 — harness connection is verified (RejectPolicy); never AutoAddPolicy."""
    policies = []
    real_set = paramiko.SSHClient.set_missing_host_key_policy

    def capture(self, policy):
        policies.append(policy)
        return real_set(self, policy)

    monkeypatch.setattr(paramiko.SSHClient, "set_missing_host_key_policy", capture)
    with app.app_context(), sftpconnection as sftp:
        assert sftp is not None
    assert policies
    assert all(isinstance(p, paramiko.RejectPolicy) for p in policies)
