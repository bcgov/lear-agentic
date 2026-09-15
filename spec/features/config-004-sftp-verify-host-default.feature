Feature: ETL SFTP jobs verify remote host identity by default
  Closes CONFIG-004 / issue #5 — stop disabling host-key checks without an explicit local opt-out.

  @R-05.1
  Scenario: Missing host key fails closed when verification is on
    Given SFTP host verification is enabled (default)
    And no SFTP_HOST_KEY is configured
    When a connection is opened for gazette, icbc, or nuans
    Then the connection fails closed before contacting the remote host

  @R-05.2
  Scenario: Verification is the default when the flag is unset
    Given SFTP_VERIFY_HOST is unset
    And a known SFTP_HOST_KEY is configured
    When a connection is opened
    Then the client installs the known host key for verification

  @R-05.3
  Scenario: Local development may opt out explicitly
    Given SFTP_VERIFY_HOST is set to false
    When a connection is opened for a local fixture
    Then host key verification may be disabled for that local session only
