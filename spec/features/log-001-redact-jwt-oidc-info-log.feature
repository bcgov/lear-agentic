Feature: Account-affiliated business INFO logs omit OIDC identity PII
  Closes LOG-001 / issue #16 — stop logging the full g.jwt_oidc_token_info object at INFO.

  @R-08.1
  Scenario: VALID account request INFO log has no JWT / identity PII
    Given a business exists
    And I am authenticated with a system or account-identity role
    And the token claims include preferred_username, email, sub, and realm roles
    When I request the business with an account query parameter
    Then the response is successful
    And the INFO log for the valid account request includes only non-PII correlation fields (account id, business identifier)
    And the INFO log does not include preferred_username, email, sub, realm roles, or the full token info object

  @R-08.2
  Scenario: Affiliated account id is still attached when org matches
    Given a business exists and is affiliated to the requested account
    And I am authenticated with a system or account-identity role
    When I request the business with that account query parameter
    Then the response business payload includes the matching accountId

  @R-08.3
  Scenario: Unmatched account does not attach accountId
    Given a business exists but is not affiliated to the requested account
    And I am authenticated with a system or account-identity role
    When I request the business with that account query parameter
    Then the response is successful
    And the response business payload does not include accountId
