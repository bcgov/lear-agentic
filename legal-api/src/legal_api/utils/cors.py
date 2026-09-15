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
"""CORS origin allowlist helpers (CONFIG-007).

Fail closed: never emit Access-Control-Allow-Origin: *.
Echo only Origins listed in CORS_ORIGINS (comma-separated env / config).
"""
from __future__ import annotations

import os
from typing import Iterable


def parse_cors_origins(raw: str | Iterable[str] | None) -> set[str]:
    """Parse an allowlist from a comma-separated string or iterable."""
    if raw is None:
        return set()
    if isinstance(raw, str):
        parts = raw.split(",")
    else:
        parts = list(raw)
    # Reject wildcard entries even if operators misconfigure the env.
    return {part.strip() for part in parts if part and part.strip() and part.strip() != "*"}


def cors_origin_allowlist() -> set[str]:
    """Return the configured CORS origin allowlist (empty ⇒ fail closed)."""
    raw: str | Iterable[str] | None = os.getenv("CORS_ORIGINS", "")
    try:
        from flask import current_app, has_app_context

        if has_app_context():
            cfg = current_app.config.get("CORS_ORIGINS")
            if cfg is not None:
                raw = cfg
    except (ImportError, RuntimeError):
        pass
    return parse_cors_origins(raw)


def resolve_cors_allow_origin(request_origin: str | None = None) -> str | None:
    """Return an Origin to echo, or None when the request must fail closed."""
    allowlist = cors_origin_allowlist()
    if not allowlist:
        return None

    origin = request_origin
    if origin is None:
        try:
            from flask import has_request_context, request

            if has_request_context():
                origin = request.headers.get("Origin")
        except RuntimeError:
            origin = None

    if origin and origin in allowlist:
        return origin
    return None


def apply_cors_allow_origin(headers: dict, request_origin: str | None = None) -> dict:
    """Mutate/return headers with Allow-Origin only when the Origin is listed."""
    allowed = resolve_cors_allow_origin(request_origin)
    headers.pop("Access-Control-Allow-Origin", None)
    if allowed:
        headers["Access-Control-Allow-Origin"] = allowed
        existing_vary = headers.get("Vary")
        if existing_vary:
            vary_parts = {part.strip() for part in existing_vary.split(",") if part.strip()}
            vary_parts.add("Origin")
            headers["Vary"] = ", ".join(sorted(vary_parts))
        else:
            headers["Vary"] = "Origin"
    return headers
