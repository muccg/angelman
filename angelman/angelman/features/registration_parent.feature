Feature: Tests in progress to ensure correctness of Angelman
    Check that Angelman works as intended.

    Background:
        Given export "ang.zip"
        Given a registry named "Angelman"

    Scenario: Try to register as a parent for Angelman
        When I try to register as an "Angelman" user
