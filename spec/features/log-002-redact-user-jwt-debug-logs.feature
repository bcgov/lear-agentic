Feature: User JWT paths do not log identity PII at DEBUG
  Closes LOG-002 / issue #17 — stop emitting full JWT token dictionaries in user create/lookup logs.

  @R-09.1
  Scenario: create_from_jwt_token does not log the token dictionary
    Given an authenticated request supplies a JWT token dictionary with identity claims
    When a user record is created from that token
    Then DEBUG logs must not include the full token dictionary
    And DEBUG logs must not include firstname, lastname, idp_userid, loginSource, sub, or iss values

  @R-09.2
  Scenario: get_or_create_user_by_jwt lookup does not log the token dictionary
    Given an authenticated request supplies a JWT token dictionary with identity claims
    When an existing or new user is resolved via get_or_create_user_by_jwt
    Then DEBUG logs must not include the full token dictionary
    And DEBUG logs may at most record token presence and internal user id

  @R-09.3
  Scenario: Missing-user create path remains free of token PII in DEBUG logs
    Given no local user exists for the JWT identity
    When get_or_create_user_by_jwt attempts to create a user
    Then DEBUG logs must not include the JWT token dictionary or identity-pii claim values
