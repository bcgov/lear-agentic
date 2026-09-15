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
"""Ephemeral JWT OIDC test key material (SECRET-001)."""
from __future__ import annotations

import base64
from functools import lru_cache


def _b64url_uint(val: int) -> str:
    length = max(1, (val.bit_length() + 7) // 8)
    return base64.urlsafe_b64encode(val.to_bytes(length, "big")).rstrip(b"=").decode("ascii")


@lru_cache(maxsize=1)
def ephemeral_jwt_oidc_test_material(kid: str = "flask-jwt-oidc-test-client") -> dict:
    """Return public JWKS, private JWKS, and PEM for TestConfig JWT_OIDC_TEST_*."""
    from cryptography.hazmat.primitives import serialization
    from cryptography.hazmat.primitives.asymmetric import rsa

    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    priv = private_key.private_numbers()
    pub = priv.public_numbers

    public_jwk = {
        "kid": kid,
        "kty": "RSA",
        "alg": "RS256",
        "use": "sig",
        "n": _b64url_uint(pub.n),
        "e": _b64url_uint(pub.e),
    }
    private_jwk = {
        **public_jwk,
        "d": _b64url_uint(priv.d),
        "p": _b64url_uint(priv.p),
        "q": _b64url_uint(priv.q),
        "dp": _b64url_uint(priv.dmp1),
        "dq": _b64url_uint(priv.dmq1),
        "qi": _b64url_uint(priv.iqmp),
    }
    pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption(),
    ).decode("ascii")

    return {
        "keys": {"keys": [public_jwk]},
        "private_key_jwks": {"keys": [private_jwk]},
        "private_key_pem": pem,
    }
