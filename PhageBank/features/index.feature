Feature: Test authentication

    Scenario: Create a user profile
        When I fill in username with username, password with "pass@123" and email with "testuser@test.com"
        Then the user should be saved in the database.

    Scenario: Give error for invalid credentials
        When I login with username "random" and password "secret"
        Then I should get error "Your username and password didn't match. Please try again."