Feature: Test JWT private keys are not committed
  Closes SECRET-001 / issue #18.

  @R-18.1
  Scenario: Legal API TestConfig has no static RSA private PEM in source
    Given the legal-api TestConfig source
    When JWT OIDC test private key fields are defined
    Then they are produced by a runtime generator
    And no BEGIN RSA PRIVATE KEY block is committed in config.py

  @R-18.2
  Scenario: business-registry-account TestConfig has no static RSA private PEM in source
    Given the business-registry-account TestConfig source
    When JWT OIDC test private key fields are defined
    Then they are produced by a runtime generator
    And no BEGIN RSA PRIVATE KEY block is committed in config.py
