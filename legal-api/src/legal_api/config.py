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

from cloud_sql_connector import DBConfig

from .jwt_oidc_test_keys import ephemeral_jwt_oidc_test_material

# this will load all the envars from a .env file located in the project root (api)
load_dotenv(find_dotenv())


class _Config:  # pylint: disable=too-few-public-methods
    """Base class configuration that should set reasonable defaults.

    Used as the base for all the other configurations.
    """

    SERVICE_NAME = "legal-api"
    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
    DEPLOYMENT_PLATFORM = os.getenv("DEPLOYMENT_PLATFORM", "OCP")

    # API Endpoints
    AUTH_API_URL = os.getenv("AUTH_API_URL", "")
    AUTH_API_VERSION = os.getenv("AUTH_API_VERSION", "")
    BUSINESS_API_URL = os.getenv("BUSINESS_API_URL", "")
    BUSINESS_API_GW_URL = os.getenv("BUSINESS_API_GW_URL", "")
    BUSINESS_API_VERSION_2 = os.getenv("BUSINESS_API_VERSION_2", "")
    NAMEX_API_URL = os.getenv("NAMEX_API_URL", "")
    NAMEX_API_VERSION = os.getenv("NAMEX_API_VERSION", "")
    PAY_API_URL = os.getenv("PAY_API_URL", "")
    PAY_API_VERSION = os.getenv("PAY_API_VERSION", "")
    REPORT_API_URL = os.getenv("REPORT_API_URL", "")
    REPORT_API_VERSION = os.getenv("REPORT_API_VERSION", "")
    REPORT_API_GOTENBERG_AUDIENCE = os.getenv("REPORT_API_GOTENBERG_AUDIENCE", "")
    REPORT_API_GOTENBERG_URL = os.getenv("REPORT_API_GOTENBERG_URL", "https://")

    COLIN_URL = f"{os.getenv('COLIN_API_URL', '')}{os.getenv('COLIN_API_VERSION', '')}"
    try:
        COLIN_TIMEOUT = int(os.getenv("COLIN_TIMEOUT", "20"))
    except (TypeError, ValueError):
        COLIN_TIMEOUT = 20

    LEGAL_API_BASE_URL = f"{BUSINESS_API_GW_URL + BUSINESS_API_VERSION_2}/businesses"

    # Temporary while there is inconsistency between OCP / GCP versions of 1pass env
    if NAMEX_API_VERSION and NAMEX_API_VERSION[-1] == "/":
        # remove the slash
        NAMEX_API_VERSION = NAMEX_API_VERSION[:-1]
    NAMEX_SVC_URL = f"{NAMEX_API_URL + NAMEX_API_VERSION}"
    PAYMENT_SVC_URL = f"{PAY_API_URL + PAY_API_VERSION}/payment-requests"
    AUTH_SVC_URL = f"{AUTH_API_URL + AUTH_API_VERSION}"
    REPORT_SVC_URL = f"{REPORT_API_URL + REPORT_API_VERSION}/reports"
    NAICS_API_URL = f"{BUSINESS_API_URL + BUSINESS_API_VERSION_2}/naics"

    REPORT_TEMPLATE_PATH = os.getenv("REPORT_PATH", "report-templates")
    FONTS_PATH = os.getenv("FONTS_PATH", "fonts")

    GO_LIVE_DATE = os.getenv("GO_LIVE_DATE")

    LD_SDK_KEY = os.getenv("LD_SDK_KEY", None)
    SECRET_KEY = "a secret"

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ALEMBIC_INI = "migrations/alembic.ini"
    # POSTGRESQL
    DB_USER = os.getenv("DATABASE_USERNAME", "")
    DB_PASSWORD = os.getenv("DATABASE_PASSWORD", "")
    DB_NAME = os.getenv("DATABASE_NAME", "")
    DB_HOST = os.getenv("DATABASE_HOST", "")
    DB_PORT = os.getenv("DATABASE_PORT", "5432")
    CLOUDSQL_INSTANCE_CONNECTION_NAME = os.getenv("CLOUDSQL_INSTANCE_CONNECTION_NAME", "")
    DB_IP_TYPE = os.getenv("DATABASE_IP_TYPE", "private").lower()

    # POSTGRESQL
    DB_UNIX_SOCKET = os.getenv("DATABASE_UNIX_SOCKET", None)
    if DB_UNIX_SOCKET:
        SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@/{DB_NAME}?host={DB_UNIX_SOCKET}"
    elif DB_HOST:
        SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    elif CLOUDSQL_INSTANCE_CONNECTION_NAME:
        SQLALCHEMY_DATABASE_URI = "postgresql+pg8000://"
        db_config = DBConfig(
            instance_name=CLOUDSQL_INSTANCE_CONNECTION_NAME,
            database=DB_NAME,
            user=DB_USER,
            ip_type=DB_IP_TYPE,
            pool_recycle=60,
            schema="public",
        )
        SQLALCHEMY_ENGINE_OPTIONS = db_config.get_engine_options()

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

    # service accounts
    ACCOUNT_SVC_AUTH_URL = os.getenv("ACCOUNT_SVC_AUTH_URL")
    ACCOUNT_SVC_CLIENT_ID = os.getenv("ACCOUNT_SVC_CLIENT_ID")
    ACCOUNT_SVC_CLIENT_SECRET = os.getenv("ACCOUNT_SVC_CLIENT_SECRET")
    ACCOUNT_SVC_TIMEOUT = os.getenv("ACCOUNT_SVC_TIMEOUT")
    # NAMEX service account creds
    NAMEX_SERVICE_CLIENT_USERNAME = os.getenv("NAMEX_SERVICE_CLIENT_USERNAME")
    NAMEX_SERVICE_CLIENT_SECRET = os.getenv("NAMEX_SERVICE_CLIENT_SECRET")

    # legislative timezone for future effective dating
    LEGISLATIVE_TIMEZONE = os.getenv("LEGISLATIVE_TIMEZONE", "America/Vancouver")


    # determines which year of NAICS data will be used to drive NAICS search
    NAICS_YEAR = int(os.getenv("NAICS_YEAR", "2022"))
    # determines which version of NAICS data will be used to drive NAICS search
    NAICS_VERSION = int(os.getenv("NAICS_VERSION", "1"))

    # Traction ACA-Py tenant settings to issue credentials from
    TRACTION_API_URL = os.getenv("TRACTION_API_URL")
    TRACTION_TENANT_ID = os.getenv("TRACTION_TENANT_ID")
    TRACTION_API_KEY = os.getenv("TRACTION_API_KEY")
    TRACTION_PUBLIC_SCHEMA_DID = os.getenv("TRACTION_PUBLIC_SCHEMA_DID")
    TRACTION_PUBLIC_ISSUER_DID = os.getenv("TRACTION_PUBLIC_ISSUER_DID")

    # Web socket settings
    WS_ALLOWED_ORIGINS = os.getenv("WS_ALLOWED_ORIGINS")

    # Digital Business Card configuration values (required to issue credentials)
    BUSINESS_SCHEMA_NAME = os.getenv("BUSINESS_SCHEMA_NAME")
    BUSINESS_SCHEMA_VERSION = os.getenv("BUSINESS_SCHEMA_VERSION")
    BUSINESS_SCHEMA_ID = os.getenv("BUSINESS_SCHEMA_ID")
    BUSINESS_CRED_DEF_ID = os.getenv("BUSINESS_CRED_DEF_ID")
    WALLET_CRED_DEF_ID = os.getenv("WALLET_CRED_DEF_ID")

    # Cache stuff
    CACHE_TYPE = os.getenv("CACHE_TYPE", "SimpleCache")
    try:
        CACHE_DEFAULT_TIMEOUT = int(os.getenv("CACHE_DEFAULT_TIMEOUT", "300"))
    except (TypeError, ValueError):
        CACHE_DEFAULT_TIMEOUT = 300

    # MRAS
    MRAS_SVC_URL = os.getenv("MRAS_SVC_URL")
    MRAS_SVC_API_KEY = os.getenv("MRAS_SVC_API_KEY")

    # involuntary dissolution
    STAGE_1_DELAY = int(os.getenv("STAGE_1_DELAY", "42"))
    STAGE_2_DELAY = int(os.getenv("STAGE_2_DELAY", "30"))

    # Transparency Register
    TR_START_DATE = os.getenv("TR_START_DATE", "").strip()  # i.e. '2025-02-01'

    # Pub/Sub

    AUDIENCE = os.getenv(
        "AUDIENCE", "https://pubsub.googleapis.com/google.pubsub.v1.Subscriber"
    )
    PUBLISHER_AUDIENCE = os.getenv(
        "PUBLISHER_AUDIENCE", "https://pubsub.googleapis.com/google.pubsub.v1.Publisher"
    )
    SUB_AUDIENCE = os.getenv("SUB_AUDIENCE", "")
    SUB_SERVICE_ACCOUNT = os.getenv("SUB_SERVICE_ACCOUNT", "")
    SBC_CONNECT_GCP_QUEUE_DEBUG = (
        os.getenv("SBC_CONNECT_GCP_QUEUE_DEBUG", "false").lower() == "true"
    )
    BUSINESS_EVENTS_TOPIC = os.getenv("BUSINESS_EVENTS_TOPIC", "business-bn")
    BUSINESS_EMAILER_TOPIC = os.getenv("BUSINESS_EMAILER_TOPIC", "business-emailer")
    BUSINESS_FILER_TOPIC = os.getenv("BUSINESS_FILER_TOPIC", "business-filer")

    # Document Service
    DOCUMENT_API_URL = os.getenv("DOCUMENT_API_URL")
    DOCUMENT_API_VERSION = os.getenv("DOCUMENT_API_VERSION")
    DOCUMENT_SVC_URL = ""
    if DOCUMENT_API_URL and DOCUMENT_API_VERSION:
        DOCUMENT_SVC_URL = f"{DOCUMENT_API_URL + DOCUMENT_API_VERSION}/documents"
    DOCUMENT_PRODUCT_CODE = "BUSINESS"
    DOCUMENT_API_KEY = os.getenv("DOCUMENT_API_KEY")

    TESTING = False
    DEBUG = False


class DevConfig(_Config):  # pylint: disable=too-few-public-methods
    """reates the Development Config object."""

    TESTING = False
    DEBUG = True


class TestConfig(_Config):  # pylint: disable=too-few-public-methods
    """In support of testing only.

    Used by the py.test suite
    """

    DEBUG = True
    TESTING = True
    
    GO_LIVE_DATE = os.getenv("GO_LIVE_DATE", "2019-08-12")

    # POSTGRESQL
    DB_USER = os.getenv("DATABASE_TEST_USERNAME", "")
    DB_PASSWORD = os.getenv("DATABASE_TEST_PASSWORD", "")
    DB_NAME = os.getenv("DATABASE_TEST_NAME", "")
    DB_HOST = os.getenv("DATABASE_TEST_HOST", "")
    DB_PORT = os.getenv("DATABASE_TEST_PORT", "5432")
    # POSTGRESQL
    if DB_UNIX_SOCKET := os.getenv("DATABASE_UNIX_SOCKET", None):
        SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@/{DB_NAME}?host={DB_UNIX_SOCKET}"
    else:
        SQLALCHEMY_DATABASE_URI = (
            f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        )

    # Transparency Register - test cases set this explicitly as needed
    TR_START_DATE = ""

    # JWT OIDC settings
    # JWT_OIDC_TEST_MODE will set jwt_manager to use
    # Private material is generated per-process (SECRET-001) — never commit a static RSA private key.
    JWT_OIDC_TEST_MODE = True
    JWT_OIDC_TEST_AUDIENCE = "example"
    JWT_OIDC_TEST_ISSUER = "https://example.localdomain/auth/realms/example"
    _JWT_OIDC_TEST_MATERIAL = ephemeral_jwt_oidc_test_material()
    JWT_OIDC_TEST_KEYS = _JWT_OIDC_TEST_MATERIAL["keys"]
    JWT_OIDC_TEST_PRIVATE_KEY_JWKS = _JWT_OIDC_TEST_MATERIAL["private_key_jwks"]
    JWT_OIDC_TEST_PRIVATE_KEY_PEM = _JWT_OIDC_TEST_MATERIAL["private_key_pem"]


    # determines which year of NAICS data will be used to drive NAICS search;
    # matches the test seed data loaded by business_model_migrations
    NAICS_YEAR = 2017
    # determines which version of NAICS data will be used to drive NAICS search
    NAICS_VERSION = 3

    LEGAL_API_BASE_URL = "https://LEGAL_API_BASE_URL/api/v2/businesses"
    BUSINESS_API_GW_URL = "https://LEGAL_API_BASE_URL"
    PAYMENT_SVC_URL = "https://PAY_SVC_URL/api/v1/payment-requests"
    AUTH_SVC_URL = "https://AUTH_SVC_URL"
    ACCOUNT_SVC_AUTH_URL = "https://ACCOUNT_SVC_AUTH_URL"
    COLIN_URL = "https://COLIN_API_URL/api/v1"
    ACCOUNT_SVC_CLIENT_SECRET = None

    BUSINESS_SCHEMA_ID = os.getenv("BUSINESS_SCHEMA_ID", "TEST_BUSINESS_SCHEMA_ID")
    BUSINESS_CRED_DEF_ID = os.getenv("BUSINESS_CRED_DEF_ID", "TEST_BUSINESS_SCHEMA_ID")

    TRACTION_API_URL = os.getenv("TRACTION_API_URL", "https://TRACTION_API_URL")
    TRACTION_TENANT_ID = os.getenv("TRACTION_TENANT_ID", "TRACTION_TENANT_ID")
    TRACTION_API_KEY = os.getenv("TRACTION_API_KEY", "TRACTION_API_KEY")
    TRACTION_PUBLIC_SCHEMA_DID = os.getenv("TRACTION_PUBLIC_SCHEMA_DID", "TRACTION_PUBLIC_SCHEMA_DID")
    TRACTION_PUBLIC_ISSUER_DID = os.getenv("TRACTION_PUBLIC_ISSUER_DID", "TRACTION_PUBLIC_ISSUER_DID")

    DOCUMENT_API_URL = "http://document-api.com"
    DOCUMENT_API_VERSION = os.getenv("DOCUMENT_API_VERSION", "/api/v1")
    DOCUMENT_SVC_URL = f"{DOCUMENT_API_URL + DOCUMENT_API_VERSION}/documents"


class ProdConfig(_Config):  # pylint: disable=too-few-public-methods
    """Production environment configuration."""

    SECRET_KEY = os.getenv("SECRET_KEY", None)

    if not SECRET_KEY:
        SECRET_KEY = os.urandom(24)
        print("WARNING: SECRET_KEY being set as a one-shot", file=sys.stderr)

    TESTING = False
    DEBUG = False


class MigrationConfig:  # pylint: disable=too-few-public-methods
    """Config object for migration environment."""

    ALEMBIC_INI = "migrations/alembic.ini"

    # POSTGRESQL
    DB_USER = os.getenv("DATABASE_USERNAME", "")
    DB_PASSWORD = os.getenv("DATABASE_PASSWORD", "")
    DB_NAME = os.getenv("DATABASE_NAME", "")
    DB_HOST = os.getenv("DATABASE_HOST", "")
    DB_PORT = os.getenv("DATABASE_PORT", "5432")
    CLOUDSQL_INSTANCE_CONNECTION_NAME = os.getenv("CLOUDSQL_INSTANCE_CONNECTION_NAME", "")
    DB_IP_TYPE = os.getenv("DATABASE_IP_TYPE", "private").lower()

    # POSTGRESQL
    DB_UNIX_SOCKET = os.getenv("DATABASE_UNIX_SOCKET", None)
    if DB_UNIX_SOCKET:
        SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@/{DB_NAME}?host={DB_UNIX_SOCKET}"
    elif DB_HOST:
        SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    elif CLOUDSQL_INSTANCE_CONNECTION_NAME:
        SQLALCHEMY_DATABASE_URI = "postgresql+pg8000://"
        db_config = DBConfig(
            instance_name=CLOUDSQL_INSTANCE_CONNECTION_NAME,
            database=DB_NAME,
            user=DB_USER,
            ip_type=DB_IP_TYPE,
            pool_recycle=60,
            schema="public",
        )
        SQLALCHEMY_ENGINE_OPTIONS = db_config.get_engine_options()
