Feature: COLIN API sets HTTP security response headers
  Closes CONFIG-002 / issue #4 — add defence-in-depth security headers on COLIN API responses.

  @R-07.1
  Scenario: Required security headers are present on a response
    Given a COLIN API HTTP response
    When the after-request security header hook runs
    Then the response includes Content-Security-Policy
    And the response includes Strict-Transport-Security
    And the response includes X-Frame-Options set to DENY
    And the response includes X-Content-Type-Options set to nosniff
    And the response includes Referrer-Policy
    And the response includes Permissions-Policy

  @R-07.2
  Scenario: Existing API version header remains intact
    Given a COLIN API HTTP response that already has an API version header
    When the after-request security header hook runs
    Then the API version header is unchanged
    And the required security headers are still present

  @R-07.3
  Scenario: Content-Security-Policy stays API-oriented
    Given COLIN API serves JSON rather than an interactive browser app
    When the Content-Security-Policy header is set
    Then it uses default-src 'none' with frame-ancestors 'none'
    And it does not require unsafe-inline script allowances
