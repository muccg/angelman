Feature: Log in to Angelman as an administrator.
    Log in to Angelman as an administrator.

    Background:
        Given a registry named "Angelman"

    Scenario: Try to login to Angelman as a curator
        Given export "ang.zip"
        When I try to log in
        When I log in as "admin" with "admin" password
