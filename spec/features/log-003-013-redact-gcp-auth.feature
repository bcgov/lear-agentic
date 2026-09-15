Feature: GCP auth and payment fee logs omit bearer tokens and JWT claims
  Closes LOG-003–012 / issues #38–#47 and LOG-013 / #57 — stop logging credentials at DEBUG; WARNING on auth failure.

  @R-38.1
  Scenario: GCP JWT verify DEBUG has no bearer token or claim dump
    Given an inbound queue request with an Authorization bearer token
    When verify_gcp_jwt runs successfully
    Then DEBUG logs may note that audience/service-account config is present
    And DEBUG logs do not include the raw Authorization header, bearer token, or full JWT claim dictionary

  @R-38.2
  Scenario: Auth failure emits WARNING with non-PII context
    Given an inbound queue request with an invalid or mismatched GCP JWT
    When verify_gcp_jwt fails verification or service-account checks
    Then a WARNING is logged with a non-PII reason (exception type or mismatch phrase)
    And the WARNING does not include the bearer token or full claim dump
    And the function returns the existing error message string without using finally:return

  @R-38.3
  Scenario: Email-reminder fee lookup DEBUG omits payment bearer token
    Given a payment-service bearer token for AR fee lookup
    When get_ar_fee is called
    Then DEBUG indicates legal type and that a bearer token is present
    And DEBUG does not include the token value

  @R-38.4
  Scenario: Emailer process_email DEBUG omits full event payload
    Given a cloud event with email data that may contain contact PII
    When process_email starts
    Then DEBUG includes event type and data keys only
    And DEBUG does not dump the full ce.data payload
