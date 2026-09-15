Feature: Colin API transitive dependencies are locked
  Closes DEP-003 / issue #8.

  @R-703.1
  Scenario: requirements.lock is present for colin-api
    Given the colin-api dependency manifests
    When an installer resolves transitive PyPI dependencies
    Then a committed requirements.lock pins those versions
