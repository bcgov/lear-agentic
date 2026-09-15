Feature: Deprecated NATS client remediation for data-tool and queue-common
  Closes DEP-013 / #32 and DEP-014 / #33. Coordinates with DEP-008 / PR #82.

  @R-713.1
  Scenario: data-tool replaces unused deprecated NATS clients with nats-py
    Given data-tool/requirements.txt
    When messaging client dependencies are inspected
    Then nats-py is declared with a version range and asyncio-nats-* packages are absent

  @R-714.1
  Scenario: queue-common NATS packages are version-pinned
    Given queue_services/common/requirements.txt
    When asyncio-nats-client and asyncio-nats-streaming lines are inspected
    Then both include version specifiers aligned with DEP-008

  @R-714.2
  Scenario: queue-common documents residual deprecation
    Given the same requirements file
    When comments are read
    Then they note deprecation and that JetStream migration is required before removal
