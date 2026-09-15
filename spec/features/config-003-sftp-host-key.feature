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
  Scenario: Test harness may opt out of verification explicitly
    Given furnishings SFTP verification is explicitly disabled for a test fixture
    When a connection is opened to an ephemeral test server
    Then the connection may proceed for automated tests only
