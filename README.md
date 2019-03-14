Simple Django application that will have following functionality:

1) Login/Registration
2) Django admin interface.
3) MySQL data storage
4) Possibility to save and display different DB content.
5) Possibility to send emails.

Here is more detailed description for each item in the list:
1) User must be able to login and register into your application. There must be custom login and registration templates implemented (do not use django templates….). During registration we must save following user information: Email, First Name, Last Name and phone number. Email address must be verified using activation link that must be sent to this email address. User must be able to login using his username and password (Only if he activated his account).
2) Just enable django built-in admin interface and configure it so it will include your custom models.
3) It is required to implement different models that will include required information (Described in next item). 
4) Basically your application must look like a Blog system. User must be able to create a blog, to create messages (posts) in this blog. All posts must be shown in descending order (by posted date). All users must be able to comment each others posts, comments must be shown in ascending order (by comment date.). So you must implement models corresponding to this information.
5) If some user commented other user’s blog post the email must be sent to the blog owner with message that his post was commented. 

No design or styles are required (no css), just simple pages that will allow us to test your application.
