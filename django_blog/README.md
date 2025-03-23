Documentation
This implementation provides a comprehensive user authentication system for your Django blog project. Here's a breakdown of each component and how they work together:

User Registration:

The register view handles new user creation using an extended version of Django's UserCreationForm.
Upon successful registration, users are automatically logged in and redirected to the home page.
The form includes an email field in addition to the standard username and password fields.


Login and Logout:

Django's built-in authentication views handle login and logout processes.
Custom templates are used to maintain consistent styling throughout the application.
Upon login, users are redirected to the home page (as configured in settings.py).


Profile Management:

The profile view allows authenticated users to view and edit their profile information.
A custom form (UserUpdateForm) enables users to update their username and email.
The view handles both GET requests (displaying profile) and POST requests (updating profile).


Security Features:

CSRF tokens are included in all forms to protect against cross-site request forgery attacks.
The login_required decorator ensures that only authenticated users can access the profile page.
Django's built-in password hashing is used for secure password storage.



Testing the Authentication System
To test this authentication system, follow these steps:

Registration:

Visit the registration page (/register/) and create a new account.
Verify that the account is created successfully and you're redirected to the home page.
Check that a success message appears confirming your registration.


Login:

Log out and then visit the login page (/login/).
Enter your credentials and verify that login is successful.
Check that you're redirected to the home page.


Profile Management:

Visit the profile page (/profile/) after logging in.
Try updating your username and email address.
Submit the form and verify that the changes are saved correctly.
Check that a success message appears after updating.


Logout:

Click the Logout link in the navigation bar.
Verify that you're logged out and redirected to the logout page.
Try accessing the profile page while logged out to ensure it redirects to the login page.


Security Testing:

Verify that all forms include CSRF tokens.
Check that protected views (like profile) cannot be accessed without authentication.



All templates include CSRF tokens ({% csrf_token %}) in their forms to protect against CSRF attacks, as required in the task. The authentication system is now fully functional and ready for integration with the rest of your Django blog project.