Feature: Tests in progress to ensure correctness of Angelman
    Check that Angelman works as intended.
    Background:
        Given a registry named "Angelman"

    Scenario: Try to register as a parent for Angelman
        Given export "ang.zip"
        Given I try to register as an "Angelman" user
        When I try to log in
        When I log in as "admin" with "admin" password
