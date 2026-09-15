Feature: Postman environment does not commit live OIDC client secrets
  Closes SECRET-002 / issue #19.

  @R-19.1
  Scenario: Legal-dev Postman environment has no live client_secret
    Given the legal-dev Postman environment file in the repository
    When the client_secret value is inspected
    Then it is empty or an explicit non-secret placeholder
    And it is not a live UUID-formatted OIDC client secret

  @R-19.2
  Scenario: Residual rotation is documented
    Given the secret was previously committed
    When the remediation PR is reviewed
    Then residual risk notes call for IdP rotation of entity-service-account
