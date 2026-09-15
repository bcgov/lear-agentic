# criterion: @R-25.1 @R-25.2 @R-25.3
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
"""CONFIG-006 — Oracle CPRD SSL DSN + fail-closed require flag.

Loads ``resources/db.py`` via importlib so the full colin_api package
(and Instant Client) are not required for these unit checks.
"""
import importlib.util
import os
import sys
from pathlib import Path
from types import ModuleType
from unittest.mock import MagicMock

import pytest
from flask import Flask


def _load_db_module():
    """Import db.py with a stubbed cx_Oracle extension module."""
    if 'cx_Oracle' not in sys.modules:
        cx = ModuleType('cx_Oracle')
        cx.SessionPool = MagicMock(name='SessionPool')
        cx.Connection = type('Connection', (), {})
        cx.SPOOL_ATTRVAL_NOWAIT = 0
        sys.modules['cx_Oracle'] = cx

    db_path = Path(__file__).resolve().parents[1] / 'src' / 'colin_api' / 'resources' / 'db.py'
    # Ensure package-relative imports resolve if Flask looks up colin_api.resources
    src = str(Path(__file__).resolve().parents[1] / 'src')
    if src not in sys.path:
        sys.path.insert(0, src)

    spec = importlib.util.spec_from_file_location('colin_api_resources_db_config006', db_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


db = _load_db_module()
build_oracle_dsn = db.build_oracle_dsn
OracleDB = db.OracleDB


def test_build_oracle_dsn_cleartext():
    """@R-25.1 — cleartext Easy Connect when SSL is off."""
    assert build_oracle_dsn('db.host', 1521, 'CPRD', ssl_enabled=False) == 'db.host:1521/CPRD'


def test_build_oracle_dsn_tcps_with_server_dn():
    """@R-25.2 — TCPS DESCRIPTION DSN when SSL is on (wallet still ops-owned)."""
    dsn = build_oracle_dsn(
        'db.host',
        2484,
        'CPRD',
        ssl_enabled=True,
        ssl_server_dn='CN=cprd.example',
    )
    assert 'PROTOCOL=TCPS' in dsn
    assert 'HOST=db.host' in dsn
    assert 'PORT=2484' in dsn
    assert 'SERVICE_NAME=CPRD' in dsn
    assert 'SSL_SERVER_CERT_DN="CN=cprd.example"' in dsn


def _oracle_app(**config):
    app = Flask('colin-api-config006-test')
    app.config.update(config)
    return app


def test_create_pool_fails_closed_when_ssl_required():
    """@R-25.3 — ORACLE_REQUIRE_SSL without ORACLE_SSL refuses pool creation."""
    app = _oracle_app(
        ORACLE_REQUIRE_SSL=True,
        ORACLE_SSL=False,
        ORACLE_USER='u',
        ORACLE_PASSWORD='p',
        ORACLE_HOST='db.host',
        ORACLE_PORT=1521,
        ORACLE_DB_NAME='CPRD',
    )
    with app.app_context():
        with pytest.raises(RuntimeError, match='ORACLE_REQUIRE_SSL'):
            OracleDB._create_pool()  # pylint: disable=protected-access


def test_create_pool_sets_tns_admin_and_tcps_dsn(monkeypatch):
    """Wallet path is exported to TNS_ADMIN; SessionPool receives a TCPS DSN."""
    monkeypatch.delenv('TNS_ADMIN', raising=False)
    app = _oracle_app(
        ORACLE_REQUIRE_SSL=True,
        ORACLE_SSL=True,
        ORACLE_WALLET_LOCATION='/var/oracle/wallet',
        ORACLE_SSL_SERVER_DN='',
        ORACLE_NET_ENCRYPTION='REQUIRED',
        ORACLE_USER='u',
        ORACLE_PASSWORD='p',
        ORACLE_HOST='db.host',
        ORACLE_PORT=2484,
        ORACLE_DB_NAME='CPRD',
    )
    fake_pool = MagicMock()
    pooled = MagicMock(return_value=fake_pool)
    sys.modules['cx_Oracle'].SessionPool = pooled
    # db module holds a reference to SessionPool from import time — patch there too
    db.cx_Oracle.SessionPool = pooled

    with app.app_context():
        OracleDB._create_pool()  # pylint: disable=protected-access

    assert os.environ.get('TNS_ADMIN') == '/var/oracle/wallet'
    assert pooled.called
    kwargs = pooled.call_args.kwargs or {}
    dsn = kwargs.get('dsn')
    if dsn is None and pooled.call_args.args:
        dsn = pooled.call_args.args[2] if len(pooled.call_args.args) > 2 else None
    assert dsn is not None
    assert 'PROTOCOL=TCPS' in dsn
