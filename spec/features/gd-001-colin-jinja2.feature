Feature: COLIN API Jinja2 meets xmlattr XSS floor
  Closes GD-001 / issue #37 — upgrade Jinja2 past the xmlattr attribute-injection advisory.

  @R-37.1
  Scenario: Jinja2 is pinned at or above 3.1.3
    Given colin-api requirements.txt is the install source of truth
    When dependency pins are inspected
    Then Jinja2 is directly pinned to >= 3.1.3
    And MarkupSafe is raised to a Jinja2 3.x-compatible companion pin
    And the Flask 1.1.2 stack remains until DEP-001 lands
