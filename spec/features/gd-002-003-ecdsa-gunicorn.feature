Feature: COLIN API pins remediated ecdsa and gunicorn
  Closes GD-002 / issue #14 and GD-003 / issue #15 — raise vulnerable dependency pins.

  @R-14.1
  Scenario: ECDSA pin meets Minerva-mitigated floor
    Given the COLIN API requirements freeze lists ecdsa
    When the pinned ecdsa version is read
    Then the version is greater than or equal to 0.19.0
    And the pin is direct so older transitive suggestions cannot win

  @R-15.1
  Scenario: Gunicorn pin meets Transfer-Encoding validation floor
    Given the COLIN API requirements freeze lists gunicorn
    When the pinned gunicorn version is read
    Then the version is greater than or equal to 22.0.0
    And the pin prefers the Legal API 23.x line when compatible
