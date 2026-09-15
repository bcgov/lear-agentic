Feature: No commented SFTP credentials in source
  Closes SECRET-009 / issue #65.

  @R-65.1
  Scenario: sftp-gazette has no commented username/password
    Given the sftp-gazette SFTP service module
    When source comments are inspected
    Then no hardcoded SFTP username or password remains
