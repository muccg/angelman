Feature: Log in to Angelman as an administrator.
    Log in to Angelman as an administrator.

    Background:
        Given export "ang.zip"
        Given a registry named "Angelman"

    Scenario: Try to login to Angelman as a curator
        When I try to log in
        When I log in as "admin" with "admin" password
