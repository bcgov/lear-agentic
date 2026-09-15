Feature: Internal git dependencies are SHA-pinned
  Closes DEP-005 / issue #10.

  @R-705.1
  Scenario: pyproject.toml git deps do not use floating @main
    Given the repository pyproject.toml files that depend on bcgov/lear or sbc-connect-common
    When dependency URLs are inspected
    Then they reference a full commit SHA instead of the main branch tip
