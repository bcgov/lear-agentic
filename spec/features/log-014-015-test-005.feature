Feature: Security logging and Postman syntax CI
  Closes LOG-014 / #58, LOG-015 / #59, TEST-005 / #66.

  @R-58.1
  Scenario: Document service logs decode failures
    Given document_service.get_content receives non-JSON content
    When decode/parse fails
    Then a warning is logged instead of a bare pass

  @R-59.1
  Scenario: Permission denials include actor and resource context
    Given a user lacks filing permissions
    When a 403 path is taken
    Then logs include actor_id, roles_present, and resource identifiers

  @R-66.1
  Scenario: Postman collections are syntax-validated in CI
    Given legal-api Postman collection files
    When the validate workflow runs
    Then the collection and environment parse without live API calls
