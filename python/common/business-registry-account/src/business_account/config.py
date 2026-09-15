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

from .jwt_oidc_test_keys import ephemeral_jwt_oidc_test_material

# this will load all the envars from a .env file located in the project root (api)
load_dotenv(find_dotenv())


class _Config:
    """Base class configuration that should set reasonable defaults.

    Used as the base for all the other configurations.
    """

    # BCReg Auth service
    AUTH_API_URL = os.getenv("AUTH_API_URL", "")
    AUTH_API_VERSION = os.getenv("AUTH_API_VERSION", "")
    AUTH_SVC_URL = f"{AUTH_API_URL + AUTH_API_VERSION}"
    # JWT service
    ACCOUNT_SVC_AUTH_URL = os.getenv("ACCOUNT_SVC_AUTH_URL")
    ACCOUNT_SVC_TIMEOUT = os.getenv("ACCOUNT_SVC_TIMEOUT", "20")
    ACCOUNT_SVC_CLIENT_ID = os.getenv("ACCOUNT_SVC_CLIENT_ID")
    ACCOUNT_SVC_CLIENT_SECRET = os.getenv("ACCOUNT_SVC_CLIENT_SECRET")
    # JWT_OIDC Settings
    JWT_OIDC_WELL_KNOWN_CONFIG = os.getenv("JWT_OIDC_WELL_KNOWN_CONFIG")
    JWT_OIDC_ALGORITHMS = os.getenv("JWT_OIDC_ALGORITHMS")
    JWT_OIDC_JWKS_URI = os.getenv("JWT_OIDC_JWKS_URI")
    JWT_OIDC_ISSUER = os.getenv("JWT_OIDC_ISSUER")
    JWT_OIDC_AUDIENCE = os.getenv("JWT_OIDC_AUDIENCE")
    JWT_OIDC_CLIENT_SECRET = os.getenv("JWT_OIDC_CLIENT_SECRET")
    JWT_OIDC_CACHING_ENABLED = os.getenv("JWT_OIDC_CACHING_ENABLED")
    JWT_OIDC_USERNAME = os.getenv("JWT_OIDC_USERNAME", "username")
    JWT_OIDC_FIRSTNAME = os.getenv("JWT_OIDC_FIRSTNAME", "firstname")
    JWT_OIDC_LASTNAME = os.getenv("JWT_OIDC_LASTNAME", "lastname")
    try:
        JWT_OIDC_JWKS_CACHE_TIMEOUT = int(os.getenv("JWT_OIDC_JWKS_CACHE_TIMEOUT"))
        if not JWT_OIDC_JWKS_CACHE_TIMEOUT:
            JWT_OIDC_JWKS_CACHE_TIMEOUT = 300
    except (TypeError, ValueError):
        JWT_OIDC_JWKS_CACHE_TIMEOUT = 300

    TESTING = False
    DEBUG = False


class DevConfig(_Config):
    """Creates the Development Config object."""

    TESTING = False
    DEBUG = True


class TestConfig(_Config):
    """In support of testing only.

    Used by the py.test suite
    """

    DEBUG = True
    TESTING = True

    # BCReg Auth service
    AUTH_API_URL = os.getenv("AUTH_API_TEST_URL", "http://AUTH_API_TEST_URL")
    AUTH_API_VERSION = os.getenv("AUTH_API_TEST_VERSION", "/api/v1")
    AUTH_SVC_URL = f"{AUTH_API_URL + AUTH_API_VERSION}"
    # JWT service
    ACCOUNT_SVC_AUTH_URL = os.getenv("ACCOUNT_SVC_AUTH_TEST_URL", "http://ACCOUNT_SVC_AUTH_TEST_URL")
    ACCOUNT_SVC_TIMEOUT = os.getenv("ACCOUNT_SVC_TIMEOUT")
    ACCOUNT_SVC_CLIENT_ID = os.getenv("ACCOUNT_SVC_TEST_CLIENT_ID", "test-client-id")
    ACCOUNT_SVC_CLIENT_SECRET = os.getenv("ACCOUNT_SVC_TEST_CLIENT_SECRET", "test-client-secret")
    # JWT OIDC settings — ephemeral per-process keys (SECRET-001); never commit static private material.
    JWT_OIDC_TEST_MODE = True
    JWT_OIDC_TEST_AUDIENCE = "example"
    JWT_OIDC_TEST_ISSUER = "https://example.localdomain/auth/realms/example"
    _JWT_OIDC_TEST_MATERIAL = ephemeral_jwt_oidc_test_material()
    JWT_OIDC_TEST_KEYS = _JWT_OIDC_TEST_MATERIAL["keys"]
    JWT_OIDC_TEST_PRIVATE_KEY_JWKS = _JWT_OIDC_TEST_MATERIAL["private_key_jwks"]
    JWT_OIDC_TEST_PRIVATE_KEY_PEM = _JWT_OIDC_TEST_MATERIAL["private_key_pem"]


class ProdConfig(_Config):
    """Production environment configuration."""

    SECRET_KEY = os.getenv("SECRET_KEY", None)

    if not SECRET_KEY:
        SECRET_KEY = os.urandom(24)
        print("WARNING: SECRET_KEY being set as a one-shot", file=sys.stderr)

    TESTING = False
    DEBUG = False
