Feature: data-tool pins a supported Flask / Werkzeug stack
  Closes DEP-007 / issue #12 — exit EOL Flask 2.0.3 / Werkzeug 2.0.3 pins.

  @R-707.1
  Scenario: Flask pin is on the supported 3.x line
    Given data-tool/requirements.txt declares a direct Flask pin
    When the pinned version is inspected
    Then it is a 3.x release greater than or equal to 3.1.0

  @R-707.2
  Scenario: Werkzeug pin is on the supported 3.x line
    Given data-tool/requirements.txt declares a direct Werkzeug pin
    When the pinned version is inspected
    Then it is a 3.x release greater than or equal to 3.1.0

  @R-707.3
  Scenario: flask-restx pin supports Flask 3
    Given data-tool/requirements.txt declares a direct flask-restx pin
    When the pinned version is inspected
    Then it is greater than or equal to 1.3.0
