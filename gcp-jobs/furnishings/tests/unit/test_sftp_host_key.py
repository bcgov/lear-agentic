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
import socket

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


def test_ephemeral_server_uses_fetched_host_key(app, sftpserver):
    """@R-03.3 — harness supplies the ephemeral server key; never AutoAddPolicy."""
    with socket.create_connection((sftpserver.host, sftpserver.port), timeout=5) as sock:
        transport = paramiko.Transport(sock)
        try:
            transport.start_client(timeout=5)
            key = transport.get_remote_server_key()
        finally:
            transport.close()

    conn = SftpConnection(
        username="user",
        password="pwd",
        host=sftpserver.host,
        port=sftpserver.port,
        host_key=key.get_base64(),
        host_key_algorithm=key.get_name(),
    )
    with app.app_context(), conn as sftp:
        assert sftp is not None
