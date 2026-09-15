# Copyright © 2019 Province of British Columbia
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""All of the configuration for the service is captured here.

All items are loaded, or have Constants defined here that
are loaded into the Flask configuration.
All modules and lookups get their configuration from the
Flask config, rather than reading environment variables directly
or by accessing this configuration directly.
"""

import os
import sys

from dotenv import find_dotenv, load_dotenv


# this will load all the envars from a .env file located in the project root (api)
load_dotenv(find_dotenv())

CONFIGURATION = {
    'development': 'colin_api.config.DevConfig',
    'testing': 'colin_api.config.TestConfig',
    'production': 'colin_api.config.ProdConfig',
    'default': 'colin_api.config.ProdConfig',
}


def _env_flag(name: str, default: bool = False) -> bool:
    """Parse a boolean environment flag (case-insensitive)."""
    raw = os.getenv(name)
    if raw is None or raw.strip() == '':
        return default
    return raw.strip().lower() in ('true', '1', 'yes', 'on')


def _oracle_require_ssl_default() -> bool:
    """Fail closed for non-local Flask envs (CONFIG-006)."""
    flask_env = (os.getenv('FLASK_ENV') or '').strip().lower()
    if flask_env in ('development', 'testing', 'dev'):
        return False
    return True


def get_named_config(config_name: str = 'production'):
    """Return the configuration object based on the name.

    :raise: KeyError: if an unknown configuration is requested
    """
    if config_name in ['production', 'staging', 'default']:
        config = ProdConfig()
    elif config_name == 'testing':
        config = TestConfig()
    elif config_name == 'development':
        config = DevConfig()
    else:
        raise KeyError(f'Unknown configuration "{config_name}"')
    return config


class _Config:  # pylint: disable=too-few-public-methods
    """Base class configuration that should set reasonable defaults for all the other configurations."""

    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

    SECRET_KEY = 'a secret'

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    LD_SDK_KEY = os.getenv('LD_SDK_KEY', None)

    # ORACLE - CDEV/CTST/CPRD
    ORACLE_USER = os.getenv('ORACLE_USER', '')
    ORACLE_PASSWORD = os.getenv('ORACLE_PASSWORD', '')
    ORACLE_DB_NAME = os.getenv('ORACLE_DB_NAME', '')
    ORACLE_HOST = os.getenv('ORACLE_HOST', '')
    ORACLE_PORT = int(os.getenv('ORACLE_PORT', '1521'))
    ORACLE_BNI_DB_LINK = os.getenv('ORACLE_BNI_DB_LINK', '')

    # CONFIG-006 — application-layer TLS hooks for CPRD.
    # ORACLE_SSL=true builds a TCPS DESCRIPTION DSN. Wallet files (cwallet.sso /
    # ewallet.p12) remain ops-owned; set ORACLE_WALLET_LOCATION (exported as TNS_ADMIN).
    # ORACLE_SSL_SERVER_DN optionally pins SSL_SERVER_CERT_DN in the DESCRIPTION.
    # ORACLE_NET_ENCRYPTION documents the intended SQLNET.ENCRYPTION_CLIENT level
    # (e.g. REQUIRED); enforcing native network encryption still needs sqlnet.ora.
    # ORACLE_REQUIRE_SSL defaults true for non-local FLASK_ENV and refuses cleartext pools.
    ORACLE_SSL = _env_flag('ORACLE_SSL', False)
    ORACLE_REQUIRE_SSL = _env_flag('ORACLE_REQUIRE_SSL', _oracle_require_ssl_default())
    ORACLE_WALLET_LOCATION = os.getenv('ORACLE_WALLET_LOCATION', '')
    ORACLE_SSL_SERVER_DN = os.getenv('ORACLE_SSL_SERVER_DN', '')
    ORACLE_NET_ENCRYPTION = os.getenv('ORACLE_NET_ENCRYPTION', '')

    # JWT_OIDC Settings
    JWT_OIDC_WELL_KNOWN_CONFIG = os.getenv('JWT_OIDC_WELL_KNOWN_CONFIG')
    JWT_OIDC_ALGORITHMS = os.getenv('JWT_OIDC_ALGORITHMS')
    JWT_OIDC_JWKS_URI = os.getenv('JWT_OIDC_JWKS_URI')
    JWT_OIDC_ISSUER = os.getenv('JWT_OIDC_ISSUER')
    JWT_OIDC_AUDIENCE = os.getenv('JWT_OIDC_AUDIENCE')
    JWT_OIDC_CLIENT_SECRET = os.getenv('JWT_OIDC_CLIENT_SECRET')
    JWT_OIDC_CACHING_ENABLED = os.getenv('JWT_OIDC_CACHING_ENABLED')
    JWT_OIDC_USERNAME = os.getenv('JWT_OIDC_USERNAME', 'username')
    JWT_OIDC_FIRSTNAME = os.getenv('JWT_OIDC_FIRSTNAME', 'firstname')
    JWT_OIDC_LASTNAME = os.getenv('JWT_OIDC_LASTNAME', 'lastname')
    try:
        JWT_OIDC_JWKS_CACHE_TIMEOUT = int(os.getenv('JWT_OIDC_JWKS_CACHE_TIMEOUT'))
        if not JWT_OIDC_JWKS_CACHE_TIMEOUT:
            JWT_OIDC_JWKS_CACHE_TIMEOUT = 300
    except (TypeError, ValueError):
        JWT_OIDC_JWKS_CACHE_TIMEOUT = 300

    # legal api
    LEGAL_API_URL = os.getenv('BUSINESS_API_URL', '') + os.getenv('BUSINESS_API_VERSION_2', '')

    # service accounts
    ACCOUNT_SVC_AUTH_URL = os.getenv('ACCOUNT_SVC_AUTH_URL')
    ACCOUNT_SVC_CLIENT_ID = os.getenv('ACCOUNT_SVC_CLIENT_ID')
    ACCOUNT_SVC_CLIENT_SECRET = os.getenv('ACCOUNT_SVC_CLIENT_SECRET')
    ACCOUNT_SVC_TIMEOUT = os.getenv('ACCOUNT_SVC_TIMEOUT')

    TESTING = False
    DEBUG = False


class DevConfig(_Config):  # pylint: disable=too-few-public-methods
    """Creates the Development Config object."""

    TESTING = False
    DEBUG = True
    # Local Instant Client sessions often lack wallets; do not fail closed here.
    ORACLE_REQUIRE_SSL = _env_flag('ORACLE_REQUIRE_SSL', False)


class TestConfig(_Config):  # pylint: disable=too-few-public-methods
    """In support of testing only used by the py.test suite."""

    DEBUG = True
    TESTING = True
    ORACLE_REQUIRE_SSL = False
    ORACLE_SSL = False

    # TEST ORACLE
    ORACLE_USER = os.getenv('TEST_ORACLE_USER', '')
    ORACLE_SCHEMA = os.getenv('TEST_ORACLE_SCHEMA', None)
    ORACLE_PASSWORD = os.getenv('TEST_ORACLE_PASSWORD', '')
    ORACLE_DB_NAME = os.getenv('TEST_ORACLE_DB_NAME', '')
    ORACLE_HOST = os.getenv('TEST_ORACLE_HOST', '')
    ORACLE_PORT = int(os.getenv('TEST_ORACLE_PORT', '1521'))


class ProdConfig(_Config):  # pylint: disable=too-few-public-methods
    """Production environment configuration."""

    SECRET_KEY = os.getenv('SECRET_KEY', None)

    if not SECRET_KEY:
        SECRET_KEY = os.urandom(24)
        print('WARNING: SECRET_KEY being set as a one-shot', file=sys.stderr)

    TESTING = False
    DEBUG = False
    # Fail closed unless explicitly opted out (local/break-glass).
    ORACLE_REQUIRE_SSL = _env_flag('ORACLE_REQUIRE_SSL', True)
