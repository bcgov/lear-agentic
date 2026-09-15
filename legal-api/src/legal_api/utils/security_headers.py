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
"""HTTP security response headers for Legal API (CONFIG-001).

Legal API responses are JSON (and PDF downloads). HTML templates are used
server-side for report generation, not as interactive browser pages, so a
strict API-oriented Content-Security-Policy is appropriate.
"""

# Sensible defaults for a JSON API behind TLS termination.
SECURITY_HEADERS = {
    "Content-Security-Policy": "default-src 'none'; frame-ancestors 'none'",
    "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
    "X-Frame-Options": "DENY",
    "X-Content-Type-Options": "nosniff",
    "Referrer-Policy": "no-referrer",
    "Permissions-Policy": "geolocation=(), microphone=(), camera=()",
}


def apply_security_headers(response):
    """Attach standard security headers without clearing existing headers."""
    for header, value in SECURITY_HEADERS.items():
        response.headers[header] = value
    return response
