Feature: Furnishings replaces deprecated flask-restplus with flask-restx
  Closes DEP-015 / issue #34.

  @R-715.1
  Scenario: flask-restplus is removed from furnishings dependencies
    Given gcp-jobs/furnishings/pyproject.toml
    When dependency declarations are inspected
    Then flask-restplus is absent

  @R-715.2
  Scenario: flask-restx is declared instead
    Given the same pyproject
    When dependency declarations are inspected
    Then flask-restx is present with a maintained 1.x range
