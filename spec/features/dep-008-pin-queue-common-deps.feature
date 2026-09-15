Feature: Queue-services-common PyPI dependencies are version-pinned
  Closes DEP-008 / issue #13 — stop unconstrained installs of shared queue common deps.

  @R-708.1
  Scenario: Each declared production dependency has a version constraint
    Given queue_services/common/requirements.txt lists the six shared packages
    When each dependency line is inspected
    Then aiohttp, attrs, python-dotenv, sentry-sdk[flask], asyncio-nats-client, and asyncio-nats-streaming all include a version specifier

  @R-708.2
  Scenario: No bare unpinned package names remain
    Given the same requirements.txt
    When lines for those six packages are parsed
    Then none are bare package names without ==, >=, <=, ~=, or != constraints
