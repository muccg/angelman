Feature: Tests in progress to ensure correctness of Angelman
    Check that Angelman works as intended.

    Background:
        Given export "ang.zip"
        Given a registry named "Angelman"

    Scenario: Try to login to Angelman as a curator
        When I try to log in
        When I log in as "curator" with "curator" password
