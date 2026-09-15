Feature: Configurable CORS origins for Legal API and COLIN API
  Closes CONFIG-007 / issue #26 and CONFIG-008 / issue #27.
  Replace Access-Control-Allow-Origin: * with an env-driven allowlist (CORS_ORIGINS).

  @R-26.1
  Scenario: Legal API fails closed when CORS_ORIGINS is empty
    Given Legal API cors_preflight, JWT auth error handler, and redirect OPTIONS paths
    When CORS_ORIGINS is unset or empty
    Then responses do not include Access-Control-Allow-Origin
    And Access-Control-Allow-Origin is never set to *

  @R-26.2
  Scenario: Legal API echoes only listed Origins
    Given CORS_ORIGINS lists one or more exact Origins
    When a request Origin matches a listed value
    Then Access-Control-Allow-Origin echoes that Origin
    And an unlisted Origin receives no Access-Control-Allow-Origin header

  @R-26.3
  Scenario: Legal API rejects wildcard configuration
    Given an operator sets CORS_ORIGINS to *
    When the allowlist is resolved
    Then Access-Control-Allow-Origin is still omitted
    And the former hardcoded * call sites no longer assign *

  @R-27.1
  Scenario: COLIN API fails closed when CORS_ORIGINS is empty
    Given COLIN API cors_preflight decorator
    When CORS_ORIGINS is unset or empty
    Then OPTIONS responses do not include Access-Control-Allow-Origin
    And Access-Control-Allow-Origin is never set to *

  @R-27.2
  Scenario: COLIN API echoes only listed Origins
    Given CORS_ORIGINS lists one or more exact Origins
    When a request Origin matches a listed value
    Then Access-Control-Allow-Origin echoes that Origin
    And an unlisted Origin receives no Access-Control-Allow-Origin header

  @R-27.3
  Scenario: COLIN API rejects wildcard configuration
    Given an operator sets CORS_ORIGINS to *
    When the allowlist is resolved
    Then Access-Control-Allow-Origin is still omitted
    And cors_preflight no longer hardcodes *
