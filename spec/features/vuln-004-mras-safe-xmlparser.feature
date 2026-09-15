Feature: MRAS jurisdiction XML is parsed with an explicit safe parser
  Closes VULN-004 / issue #54 — stop calling lxml fromstring without a hardened XMLParser.

  @R-54.1
  Scenario: Valid MRAS jurisdiction XML still returns registered jurisdictions
    Given the MRAS service returns well-formed jurisdiction XML with target profile ids
    When jurisdictions are requested for a business identifier
    Then only jurisdictions that include a target profile id are returned
    And each result includes id, names, redirect URL, and target profile id

  @R-54.2
  Scenario: MrasService constructs an explicit safe XMLParser for fromstring
    Given the legal-api MrasService source that parses MRAS XML
    When the parse call is inspected
    Then fromstring is invoked with an XMLParser
    And that parser sets resolve_entities to false
    And that parser sets no_network to true

  @R-54.3
  Scenario: Adversarial entity payload does not resolve external entity content
    Given the MRAS service returns XML that declares an external file entity
    When jurisdictions are requested for a business identifier
    Then the response does not include the contents of that external file
    And the call fails closed (None) or returns no jurisdiction records
