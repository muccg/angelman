Feature: Automated tests to ensure correctness of Angelman
    Check that the Angelman registration page works as intended.

    Background:
        Given export "ang.zip"
        Given a registry named "Angelman"

    Scenario: Try to register as a parent for Angelman
        When I try to register as an "Angelman" user
        Then I should have successfully registered

        When I try to log in
        When I log in as "admin" with "admin" password
        When the administrator manually activates the user
        Then the user should be activated

        When I try to log in
        When I log in as "sample@email.com" with "admin123" password
        When I login as an Angelman user "John Smith"
        Then I should be at the angelman registry landing page
