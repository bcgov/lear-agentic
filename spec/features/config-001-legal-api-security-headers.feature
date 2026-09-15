Feature: Legal API sets HTTP security response headers
  Closes CONFIG-001 / issue #3 — add defence-in-depth security headers on Legal API responses.

  @R-06.1
  Scenario: Required security headers are present on a response
    Given a Legal API HTTP response
    When the after-request security header hook runs
    Then the response includes Content-Security-Policy
    And the response includes Strict-Transport-Security
    And the response includes X-Frame-Options set to DENY
    And the response includes X-Content-Type-Options set to nosniff
    And the response includes Referrer-Policy
    And the response includes Permissions-Policy

  @R-06.2
  Scenario: Existing version headers remain intact
    Given a Legal API HTTP response that already has API and SCHEMAS version headers
    When the after-request security header hook runs
    Then the API version header is unchanged
    And the SCHEMAS version header is unchanged
    And the required security headers are still present

  @R-06.3
  Scenario: Content-Security-Policy stays API-oriented
    Given Legal API serves JSON and PDF rather than an interactive browser app
    When the Content-Security-Policy header is set
    Then it uses default-src 'none' with frame-ancestors 'none'
    And it does not require unsafe-inline script allowances
