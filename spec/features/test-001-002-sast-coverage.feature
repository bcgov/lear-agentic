Feature: SAST tooling and coverage fail-under for primary APIs
  Closes TEST-001 / issue #20 and TEST-002 / issue #21.

  @R-20.1
  Scenario: Committed CodeQL analysis workflow is present
    Given the repository may already run organization or default CodeQL on pull requests
    When a reviewer inspects `.github/workflows`
    Then a `codeql-analysis.yml` workflow is committed
    And existing CI workflows remain enabled

  @R-20.2
  Scenario: Bandit scans Legal API source on pull requests
    Given changes under `legal-api`
    When the Python SAST workflow runs
    Then Bandit analyzes `legal-api/src`
    And the job fails if High severity findings are reported

  @R-20.3
  Scenario: Bandit scans COLIN API source on pull requests
    Given changes under `colin-api`
    When the Python SAST workflow runs
    Then Bandit analyzes `colin-api/src`
    And the job fails if High severity findings are reported

  @R-21.1
  Scenario: Legal API unit tests enforce a coverage floor
    Given Legal API pytest configuration
    When coverage is collected for `src/legal_api`
    Then the run fails if coverage is under 70 percent

  @R-21.2
  Scenario: COLIN API unit tests enforce a coverage floor
    Given COLIN API pytest configuration
    When coverage is collected for `src`
    Then the run fails if coverage is under 25 percent

  @R-21.3
  Scenario: Codecov project status has explicit API flag targets
    Given `codecov.yaml` project status configuration
    When coverage uploads include `legalapi` or `colinapi` flags
    Then those flags have non-zero target thresholds
    And the thresholds are not higher than recently observed Codecov flag totals
