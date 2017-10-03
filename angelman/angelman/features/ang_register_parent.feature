Feature: Automated tests to ensure correctness of Angelman
    Check that the Angelman registration page works as intended.

    Background:
        Given export "ang.zip"
        Given a registry named "Angelman"

    Scenario: Try to register as a parent for Angelman
        When I try to register as an "Angelman" user called "John Smith" using the email address "sample@email.com" and the password "admin123"
        Then I should have successfully registered and would see a "Thank you for registration" message

        When I try to log in
        When I log in as "admin" with "admin" password
        When the administrator manually activates the user
        Then the user should be activated

        When I try to log in
        When I log in as "sample@email.com" with "admin123" password
        Then I should be logged in as an Angelman user called "John Smith"
        Then I should be at the welcome page and see a message which says "Welcome John Smith to the Angelman Registry"
