Feature: COLIN API upgrades Flask / Werkzeug off the EOL 1.x pin set
  Closes DEP-001 / issue #6 — move past Flask 1.1.2 / Werkzeug 1.0.1 with companions.

  @R-701.1
  Scenario: Flask and Werkzeug pins meet advisory floors
    Given colin-api/requirements.txt declares Flask and Werkzeug
    When the pinned versions are inspected
    Then Flask is at least 2.3.2
    And Werkzeug is at least 2.2.3

  @R-701.2
  Scenario: Companion pins match the Flask 2.3 line
    Given the same requirements manifest
    When companion pins are inspected
    Then Jinja2, MarkupSafe, itsdangerous, click, and blinker meet Flask 2.3 floors

  @R-701.3
  Scenario: flask-restx is upgraded off the 0.3.0 pin
    Given colin-api previously pinned flask-restx 0.3.0
    When the flask-restx pin is inspected
    Then it is at least 1.3.0

  @R-701.4
  Scenario: Flask-Script is no longer a runtime dependency
    Given Flask-Script does not import on Flask 2.3
    When prod and pinned requirements are inspected
    Then Flask-Script is absent from both manifests
