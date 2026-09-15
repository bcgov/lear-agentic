Feature: Furnishings MRAS XML is parsed with an explicit safe parser
  Closes VULN-005 / issue #63 — same safe lxml XMLParser as VULN-004 on the Furnishings MrasService copy.

  @R-63.1
  Scenario: Valid MRAS jurisdiction XML still returns registered jurisdictions
    Given the MRAS service returns well-formed jurisdiction XML with target profile ids
    When jurisdictions are requested for a business identifier
    Then only jurisdictions that include a target profile id are returned
    And each result includes id, names, redirect URL, and target profile id

  @R-63.2
  Scenario: Furnishings MrasService constructs an explicit safe XMLParser for fromstring
    Given the furnishings MrasService source that parses MRAS XML
    When the parse call is inspected
    Then fromstring is invoked with an XMLParser
    And that parser sets resolve_entities to false
    And that parser sets no_network to true

  @R-63.3
  Scenario: Adversarial entity payload does not resolve external entity content
    Given the MRAS service returns XML that declares an external file entity
    When jurisdictions are requested for a business identifier
    Then the response does not include the contents of that external file
    And the call fails closed or leaves the entity unresolved (no local file contents)
