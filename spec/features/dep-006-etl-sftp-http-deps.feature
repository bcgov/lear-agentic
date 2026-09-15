Feature: SFTP ETL jobs pin secure HTTP client dependencies
  Closes DEP-006 / issue #11 — raise outdated requests / urllib3 / certifi floors
  across sftp-gazette, sftp-icbc-report, and sftp-nuans-report.

  @R-706.1
  Scenario: requests pin meets the remediated floor on each SFTP ETL job
    Given each sftp ETL job requirements.txt declares a direct requests pin
    When the pinned version is inspected
    Then it is greater than or equal to 2.32.3

  @R-706.2
  Scenario: urllib3 pin meets the remediated 2.x floor on each SFTP ETL job
    Given each sftp ETL job requirements.txt declares a direct urllib3 pin
    When the pinned version is inspected
    Then it is a 2.x release greater than or equal to 2.2.0

  @R-706.3
  Scenario: certifi pin is current on each SFTP ETL job
    Given each sftp ETL job requirements.txt declares a direct certifi pin
    When the pinned version is inspected
    Then it is greater than or equal to 2026.7.22
