Feature: Merge-train shared-path placeholder

  Scenario: Shared example feature path stays identical across PRs
    Given remediation PRs share spec/features/example-happy-path.feature
    Then unique criteria live in sibling feature files for this slice
