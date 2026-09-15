Feature: data-tool lockfile and emailer dependency cleanup
  Closes DEP-017 / #36 and DEP-019 / #56.

  @R-36.1
  Scenario: data-tool has a committed requirements.lock
    Given the data-tool dependency manifests
    When transitive PyPI dependencies are resolved
    Then a committed requirements.lock pins resolvable versions

  @R-56.1
  Scenario: business-emailer drops Flask-Script
    Given the business-emailer pyproject
    When dependencies are reviewed
    Then Flask-Script is not declared

  @R-56.2
  Scenario: business-emailer drops legacy-cgi
    Given the business-emailer pyproject
    When dependencies are reviewed
    Then legacy-cgi is not declared
