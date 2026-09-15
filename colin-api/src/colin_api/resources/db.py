# Copyright © 2019 Province of British Columbia
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
"""Create Oracle database connection.

These will get initialized by the application.
"""
import os

import cx_Oracle
from flask import _app_ctx_stack, current_app


def build_oracle_dsn(host, port, db_name, *, ssl_enabled=False, ssl_server_dn=None):
    """Build a cleartext Easy Connect or TCPS DESCRIPTION DSN (CONFIG-006).

    Full mutual TLS still requires ops-provided wallet files under
    ``ORACLE_WALLET_LOCATION`` / ``TNS_ADMIN``. This helper encodes the
    application-layer protocol choice so cleartext is not the only option.
    """
    if not ssl_enabled:
        return '{0}:{1}/{2}'.format(host, port, db_name)  # pylint: disable=consider-using-f-string

    security = ''
    if ssl_server_dn:
        security = '(SECURITY=(SSL_SERVER_CERT_DN="{0}"))'.format(ssl_server_dn)

    return (
        '(DESCRIPTION='
        '(ADDRESS=(PROTOCOL=TCPS)(HOST={host})(PORT={port}))'
        '(CONNECT_DATA=(SERVICE_NAME={service}))'
        '{security})'
    ).format(host=host, port=port, service=db_name, security=security)


class OracleDB:
    """Oracle database connection object for re-use in application."""

    def __init__(self, app=None):
        """initializer, supports setting the app context on instantiation."""
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """Create setup for the extension.

        :param app: Flask app
        :return: naked
        """
        self.app = app
        app.teardown_appcontext(self.teardown)

    @staticmethod
    def teardown():
        """Oracle session pool cleans up after itself."""
        ctx = _app_ctx_stack.top
        if hasattr(ctx, 'oracle_pool'):
            ctx.oracle_pool.close()

    @staticmethod
    def _create_pool():
        """Create the cx_oracle connection pool from the Flask Config Environment.

        :return: an instance of the OCI Session Pool
        """
        # this uses the builtin session / connection pooling provided by
        # the Oracle OCI driver
        # setting threaded =True wraps the underlying calls in a Mutex
        # so we don't have to that here

        ssl_enabled = bool(current_app.config.get('ORACLE_SSL'))
        require_ssl = bool(current_app.config.get('ORACLE_REQUIRE_SSL'))
        if require_ssl and not ssl_enabled:
            raise RuntimeError(
                'ORACLE_REQUIRE_SSL is enabled but ORACLE_SSL is false. '
                'Set ORACLE_SSL=true (TCPS DSN) and provide wallet files via '
                'ORACLE_WALLET_LOCATION / TNS_ADMIN, or set ORACLE_REQUIRE_SSL=false '
                'for an approved local-only cleartext session.'
            )

        wallet_location = (current_app.config.get('ORACLE_WALLET_LOCATION') or '').strip()
        if ssl_enabled and wallet_location:
            # Instant Client / SQL*Net reads cwallet.sso / ewallet.p12 from TNS_ADMIN.
            os.environ['TNS_ADMIN'] = wallet_location

        # Optional native-network-encryption hint for ops sqlnet.ora (informational in-app).
        # When set to REQUIRED, document that sqlnet.ora must also set
        # SQLNET.ENCRYPTION_CLIENT=REQUIRED (wallet/listener still owned by ops).
        _ = (current_app.config.get('ORACLE_NET_ENCRYPTION') or '').strip().upper()

        def init_session(conn, *args):  # pylint: disable=unused-argument; Extra var being passed with call
            cursor = conn.cursor()
            cursor.execute("alter session set TIME_ZONE = 'America/Vancouver'")

        dsn = build_oracle_dsn(
            current_app.config.get('ORACLE_HOST'),
            current_app.config.get('ORACLE_PORT'),
            current_app.config.get('ORACLE_DB_NAME'),
            ssl_enabled=ssl_enabled,
            ssl_server_dn=(current_app.config.get('ORACLE_SSL_SERVER_DN') or None),
        )

        return cx_Oracle.SessionPool(  # pylint:disable=c-extension-no-member
            user=current_app.config.get('ORACLE_USER'),
            password=current_app.config.get('ORACLE_PASSWORD'),
            dsn=dsn,
            min=1,
            max=10,
            increment=1,
            connectiontype=cx_Oracle.Connection,  # pylint:disable=c-extension-no-member
            threaded=True,
            getmode=cx_Oracle.SPOOL_ATTRVAL_NOWAIT,  # pylint:disable=c-extension-no-member
            waitTimeout=1500,
            timeout=3600,
            sessionCallback=init_session,
            encoding='UTF-8',
            nencoding='UTF-8')

    @property
    def connection(self):  # pylint: disable=inconsistent-return-statements
        """Create connection property for the NROService.

        If this is running in a Flask context,
        then either get the existing connection pool or create a new one
        and then return an acquired session
        :return: cx_Oracle.connection type
        """
        ctx = _app_ctx_stack.top
        if ctx is not None:
            if not hasattr(ctx, '_oracle_pool'):
                ctx._oracle_pool = self._create_pool()  # pylint: disable = protected-access; need this method
            return ctx._oracle_pool.acquire()  # pylint: disable = protected-access; need this method


# export instance of this class
DB = OracleDB()
