Feature: CRA BN Hub XML is parsed without unsafe entity expansion
  Closes VULN-006 / issue #64 — use defusedxml for ElementTree.fromstring on BN Hub responses.

  @R-64.1
  Scenario: BN processors import defusedxml ElementTree for fromstring
    Given the business-bn processor modules that parse CRA BN Hub XML
    When their imports are inspected
    Then each uses defusedxml.ElementTree as Et
    And none import stdlib xml.etree.ElementTree as Et for that parse path

  @R-64.2
  Scenario: Benign CRA acknowledgement XML still parses
    Given a well-formed SBNAcknowledgement XML payload
    When it is parsed with the hardened ElementTree API
    Then the root tag and child text are available to the caller

  @R-64.3
  Scenario: Entity expansion payloads are rejected
    Given XML that declares an external or expandable entity
    When it is parsed with the hardened ElementTree API
    Then parsing raises a forbidden-entity or parse error
    And local file contents are not returned as element text
