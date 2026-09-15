Feature: COLIN API pins registry_schemas to a git commit
  Closes DEP-004 / issue #9 — stop floating business-schemas on default-branch HEAD.

  @R-704.1
  Scenario: business-schemas dependency includes an explicit commit SHA
    Given colin-api/requirements.txt declares registry_schemas from bcgov/business-schemas
    When the dependency line is inspected
    Then it uses the git+https URL form with @<40-char-sha> before #egg=registry_schemas

  @R-704.2
  Scenario: Pin is not a floating branch or tag reference
    Given the same registry_schemas dependency line
    When the revision after @ is inspected
    Then it is a full lowercase hex commit SHA
    And it is not a branch name such as main or master
