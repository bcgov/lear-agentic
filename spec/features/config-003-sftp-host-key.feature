Feature: Furnishings SFTP verifies remote host identity
  Closes CONFIG-003 / issue #2 — stop silently accepting unknown SSH host keys.

  @R-03.1
  Scenario: Verified connection requires a known host key
    Given furnishings SFTP verification is enabled
    And no known host key is configured
    When a connection is opened
    Then the connection fails closed without accepting an unknown host

  @R-03.2
  Scenario: Known host key is required for production-style connects
    Given furnishings SFTP verification is enabled
    And a known host key is configured for the endpoint
    When a connection is opened to that endpoint
    Then the client rejects any other host identity

  @R-03.3
  Scenario: Test harness supplies the ephemeral server host key
    Given an automated test SFTP server with an ephemeral host key
    And the furnishings client is configured with that host key
    When a connection is opened
    Then the connection succeeds without AutoAddPolicy
