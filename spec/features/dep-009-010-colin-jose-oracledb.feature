Feature: COLIN API JWT and Oracle driver dependency remediation
  Closes DEP-009 / issue #28 and DEP-010 / issue #29.

  @R-709.1
  Scenario: python-jose meets the secure floor
    Given colin-api/requirements.txt declares python-jose
    When the pin is inspected
    Then python-jose is at least version 3.4.0

  @R-710.1
  Scenario: Deprecated cx-Oracle is replaced by oracledb in manifests
    Given colin-api production requirements
    When dependency names are inspected
    Then oracledb is declared and cx-Oracle is absent

  @R-710.2
  Scenario: Application uses thin-mode oracledb alias
    Given colin-api Oracle connection modules
    When imports are inspected
    Then modules import oracledb as cx_Oracle without Instant Client init
