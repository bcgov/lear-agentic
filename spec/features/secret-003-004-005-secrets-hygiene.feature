Feature: Remove weak and hardcoded secrets from configs and fixtures
  Closes SECRET-003 / issue #48, SECRET-004 / issue #49, SECRET-005 / issue #50.

  @R-48.1
  Scenario: Base Flask configs never default SECRET_KEY to a weak literal
    Given the base configuration classes for legal-api, colin-api, and GCP jobs
    When SECRET_KEY is resolved without an environment value
    Then it is not the literal string "a secret"
    And a random one-shot key is generated with a warning

  @R-48.2
  Scenario: Explicit SECRET_KEY from the environment is honoured
    Given SECRET_KEY is set in the process environment
    When configuration classes are loaded
    Then SECRET_KEY equals the environment value

  @R-49.1
  Scenario: Postman collection does not hardcode coops-updater-job password
    Given the legal-api Postman collection in the repository
    When request bodies that previously used coops-updater-job credentials are inspected
    Then username and password use Postman variable placeholders
    And the password is not equal to the literal username "coops-updater-job"

  @R-49.2
  Scenario: Residual rotation is documented for the service account
    Given the credential was previously committed
    When the remediation PR is reviewed
    Then residual risk notes call for rotation of coops-updater-job in OIDC realms

  @R-50.1
  Scenario: data-tool docker-compose has no hardcoded Hasura or Postgres secrets
    Given data-tool/docker-compose.yaml
    When password and admin-secret values are inspected
    Then they use ${VAR:-dev-only-change-me} substitution
    And committed literals test-password and hasura-secret-admin-secret are absent
