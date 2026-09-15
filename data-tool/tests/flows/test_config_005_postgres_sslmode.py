# criterion: @R-24.1 @R-24.2 @R-24.3
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
"""CONFIG-005 — Postgres URI sslmode enforcement for data-tool."""
import importlib
import sys
from pathlib import Path

import pytest

FLOWS_PATH = Path(__file__).resolve().parents[2] / 'flows'
sys.path.insert(0, str(FLOWS_PATH))

import config as config_module  # noqa: E402


@pytest.fixture
def clean_ssl_env(monkeypatch):
    """Clear SSL-related env so defaults are exercised."""
    for key in (
        'DATABASE_SSLMODE',
        'FLASK_ENV',
        'APP_SETTINGS',
        'DATA_LOAD_ENV',
        'DATABASE_USERNAME',
        'DATABASE_PASSWORD',
        'DATABASE_NAME',
        'DATABASE_HOST',
        'DATABASE_PORT',
        'DATABASE_USERNAME_COLIN_MIGR',
        'DATABASE_PASSWORD_COLIN_MIGR',
        'DATABASE_NAME_COLIN_MIGR',
        'DATABASE_HOST_COLIN_MIGR',
        'DATABASE_PORT_COLIN_MIGR',
        'DATABASE_USERNAME_AUTH',
        'DATABASE_PASSWORD_AUTH',
        'DATABASE_NAME_AUTH',
        'DATABASE_HOST_AUTH',
        'DATABASE_PORT_AUTH',
    ):
        monkeypatch.delenv(key, raising=False)
    yield monkeypatch


def _reload_config():
    return importlib.reload(config_module)


def test_non_local_default_sslmode_require(clean_ssl_env):
    """@R-24.1 — non-local environments default to sslmode=require on all three URIs."""
    clean_ssl_env.setenv('FLASK_ENV', 'production')
    clean_ssl_env.setenv('DATABASE_USERNAME', 'u')
    clean_ssl_env.setenv('DATABASE_PASSWORD', 'p')
    clean_ssl_env.setenv('DATABASE_NAME', 'lear')
    clean_ssl_env.setenv('DATABASE_HOST', 'db.example')
    clean_ssl_env.setenv('DATABASE_PORT', '5432')
    clean_ssl_env.setenv('DATABASE_USERNAME_COLIN_MIGR', 'cu')
    clean_ssl_env.setenv('DATABASE_PASSWORD_COLIN_MIGR', 'cp')
    clean_ssl_env.setenv('DATABASE_NAME_COLIN_MIGR', 'colin')
    clean_ssl_env.setenv('DATABASE_HOST_COLIN_MIGR', 'colin.example')
    clean_ssl_env.setenv('DATABASE_USERNAME_AUTH', 'au')
    clean_ssl_env.setenv('DATABASE_PASSWORD_AUTH', 'ap')
    clean_ssl_env.setenv('DATABASE_NAME_AUTH', 'auth')
    clean_ssl_env.setenv('DATABASE_HOST_AUTH', 'auth.example')

    config = _reload_config()
    cfg = config._Config()  # pylint: disable=protected-access

    assert cfg.DATABASE_SSLMODE == 'require'
    assert cfg.SQLALCHEMY_DATABASE_URI.endswith('?sslmode=require')
    assert cfg.SQLALCHEMY_DATABASE_URI_COLIN_MIGR.endswith('?sslmode=require')
    assert cfg.SQLALCHEMY_DATABASE_URI_AUTH.endswith('?sslmode=require')


def test_local_default_sslmode_prefer(clean_ssl_env):
    """@R-24.2 — local/dev defaults to prefer so TLS-less laptop Postgres still works."""
    clean_ssl_env.setenv('FLASK_ENV', 'development')
    clean_ssl_env.setenv('DATA_LOAD_ENV', 'local_migr_test')
    clean_ssl_env.setenv('DATABASE_USERNAME', 'u')
    clean_ssl_env.setenv('DATABASE_PASSWORD', 'p')
    clean_ssl_env.setenv('DATABASE_NAME', 'lear')
    clean_ssl_env.setenv('DATABASE_HOST', 'localhost')

    config = _reload_config()
    cfg = config._Config()  # pylint: disable=protected-access

    assert cfg.DATABASE_SSLMODE == 'prefer'
    assert '?sslmode=prefer' in cfg.SQLALCHEMY_DATABASE_URI


def test_explicit_database_sslmode_override(clean_ssl_env):
    """@R-24.3 — DATABASE_SSLMODE overrides the secure/local default."""
    clean_ssl_env.setenv('FLASK_ENV', 'production')
    clean_ssl_env.setenv('DATABASE_SSLMODE', 'verify-full')
    clean_ssl_env.setenv('DATABASE_USERNAME', 'u')
    clean_ssl_env.setenv('DATABASE_PASSWORD', 'p')
    clean_ssl_env.setenv('DATABASE_NAME', 'lear')
    clean_ssl_env.setenv('DATABASE_HOST', 'db.example')

    config = _reload_config()
    cfg = config._Config()  # pylint: disable=protected-access

    assert cfg.DATABASE_SSLMODE == 'verify-full'
    assert cfg.SQLALCHEMY_DATABASE_URI.endswith('?sslmode=verify-full')
