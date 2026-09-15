# Copyright © 2025 Province of British Columbia
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
"""Tests for the GCP auth service are contained here."""

from unittest.mock import MagicMock, patch

import pytest

from business_digital_credentials.services.gcp_auth import verify_gcp_jwt


@patch('business_digital_credentials.services.gcp_auth.id_token')
@patch('business_digital_credentials.services.gcp_auth.requests')
def test_verify_gcp_jwt_success(mock_requests, mock_id_token, app):
    """Test successful JWT verification."""
    mock_flask_request = MagicMock()
    mock_flask_request.headers.get.return_value = "Bearer valid_token"
    
    mock_id_token.verify_oauth2_token.return_value = {
        'email': 'test@example.com',
        'email_verified': True
    }
    
    with app.app_context():
        app.config['SUB_AUDIENCE'] = 'test-audience'
        app.config['SUB_SERVICE_ACCOUNT'] = 'test@example.com'
        
        result = verify_gcp_jwt(mock_flask_request)
        
        assert result == ""


@patch('business_digital_credentials.services.gcp_auth.id_token')
@patch('business_digital_credentials.services.gcp_auth.requests')
def test_verify_gcp_jwt_validation_failures(mock_requests, mock_id_token, app):
    """Test various JWT validation failures."""
    with app.app_context():
        app.config['SUB_AUDIENCE'] = 'test-audience'
        app.config['SUB_SERVICE_ACCOUNT'] = 'correct@example.com'
        
        # Test email not verified
        mock_flask_request = MagicMock()
        mock_flask_request.headers.get.return_value = "Bearer token"
        mock_id_token.verify_oauth2_token.return_value = {
            'email': 'correct@example.com',
            'email_verified': False
        }
        result = verify_gcp_jwt(mock_flask_request)
        assert "Invalid service account or email not verified" in result
        
        # Test wrong email
        mock_id_token.verify_oauth2_token.return_value = {
            'email': 'wrong@example.com',
            'email_verified': True
        }
        result = verify_gcp_jwt(mock_flask_request)
        assert "Invalid service account or email not verified" in result


@pytest.mark.parametrize("auth_header,expected_error", [
    (None, "Invalid token:"),
    ("InvalidFormat", "Invalid token:"),
    ("Bearer ", ""),  # Empty token succeeds with mock
])
@patch('business_digital_credentials.services.gcp_auth.id_token')
@patch('business_digital_credentials.services.gcp_auth.requests')
def test_verify_gcp_jwt_malformed_headers(mock_requests, mock_id_token, auth_header, expected_error, app):
    """Test various malformed authorization headers."""
    mock_flask_request = MagicMock()
    mock_flask_request.headers.get.return_value = auth_header
    
    mock_id_token.verify_oauth2_token.return_value = {
        'email': 'test@example.com',
        'email_verified': True
    }
    
    with app.app_context():
        app.config['SUB_AUDIENCE'] = 'test-audience'
        app.config['SUB_SERVICE_ACCOUNT'] = 'test@example.com'
        
        result = verify_gcp_jwt(mock_flask_request)
        
        if expected_error:
            assert expected_error in result
        else:
            assert result == ""


@patch('business_digital_credentials.services.gcp_auth.id_token')
@patch('business_digital_credentials.services.gcp_auth.requests')
def test_verify_gcp_jwt_exceptions(mock_requests, mock_id_token, app):
    """Test exception handling."""
    mock_flask_request = MagicMock()
    mock_flask_request.headers.get.return_value = "Bearer token"
    
    with app.app_context():
        app.config['SUB_AUDIENCE'] = 'test-audience'
        app.config['SUB_SERVICE_ACCOUNT'] = 'test@example.com'
        
        # Test verification exception
        mock_id_token.verify_oauth2_token.side_effect = Exception("Token invalid")
        result = verify_gcp_jwt(mock_flask_request)
        assert "Invalid token: Token invalid" in result
        
        # Test missing claim keys
        mock_id_token.verify_oauth2_token.side_effect = None
        mock_id_token.verify_oauth2_token.return_value = {'aud': 'test'}  # Missing email keys
        result = verify_gcp_jwt(mock_flask_request)
        assert "Invalid token:" in result


@patch('business_digital_credentials.services.gcp_auth.id_token')
@patch('business_digital_credentials.services.gcp_auth.requests')
def test_verify_gcp_jwt_debug_logs_omit_token_and_claim(mock_requests, mock_id_token, app, caplog):
    """DEBUG must not include bearer token or full JWT claim (LOG-005)."""
    import logging

    secret_token = "Bearer super-secret-jwt-value"
    claim_email = "svc-account@example.com"
    mock_flask_request = MagicMock()
    mock_flask_request.headers.get.return_value = secret_token
    mock_id_token.verify_oauth2_token.return_value = {
        'email': claim_email,
        'email_verified': True,
        'sub': 'subject-should-not-log',
    }

    with app.app_context():
        app.config['SUB_AUDIENCE'] = 'test-audience'
        app.config['SUB_SERVICE_ACCOUNT'] = claim_email
        with caplog.at_level(logging.DEBUG):
            result = verify_gcp_jwt(mock_flask_request)

    assert result == ""
    joined = " ".join(r.getMessage() for r in caplog.records)
    assert "super-secret-jwt-value" not in joined
    assert "Bearer" not in joined
    assert "subject-should-not-log" not in joined
    assert claim_email not in joined


@patch('business_digital_credentials.services.gcp_auth.id_token')
@patch('business_digital_credentials.services.gcp_auth.requests')
def test_verify_gcp_jwt_logs_warning_on_failure(mock_requests, mock_id_token, app, caplog):
    """Auth failures must emit WARNING with non-PII context (LOG-010)."""
    import logging

    mock_flask_request = MagicMock()
    mock_flask_request.headers.get.return_value = "Bearer bad-token"
    mock_id_token.verify_oauth2_token.side_effect = Exception("Token invalid")

    with app.app_context():
        app.config['SUB_AUDIENCE'] = 'test-audience'
        app.config['SUB_SERVICE_ACCOUNT'] = 'test@example.com'
        with caplog.at_level(logging.WARNING):
            result = verify_gcp_jwt(mock_flask_request)

    assert "Invalid token: Token invalid" in result
    warnings = [r for r in caplog.records if r.levelno >= logging.WARNING]
    assert warnings, "expected WARNING on auth failure"
    warning_text = " ".join(r.getMessage() for r in warnings)
    assert "GCP JWT verification failed" in warning_text
    assert "bad-token" not in warning_text
    assert "Token invalid" not in warning_text  # exception message may leak; type only
