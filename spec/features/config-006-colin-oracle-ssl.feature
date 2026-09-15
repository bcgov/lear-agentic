Feature: COLIN API Oracle CPRD connections prefer TLS and can fail closed
  Closes CONFIG-006 / issue #25 — stop relying solely on listener-side Oracle encryption.

  @R-25.1
  Scenario: Cleartext Easy Connect remains available when SSL is off
    Given ORACLE_SSL is false and ORACLE_REQUIRE_SSL is false
    When the Oracle DSN is built
    Then the DSN uses host:port/service Easy Connect form

  @R-25.2
  Scenario: Enabling SSL builds a TCPS connect descriptor
    Given ORACLE_SSL is true
    And optional ORACLE_SSL_SERVER_DN / ORACLE_WALLET_LOCATION are configured
    When the Oracle session pool is created
    Then the DSN uses PROTOCOL=TCPS
    And TNS_ADMIN is set from the wallet location when provided

  @R-25.3
  Scenario: Require-SSL fails closed without ORACLE_SSL
    Given ORACLE_REQUIRE_SSL is true
    And ORACLE_SSL is false
    When the Oracle session pool is created
    Then pool creation fails before contacting CPRD
