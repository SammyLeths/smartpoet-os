My project was conducted by myself alone

The project involves development of an online publishing platform for poets where they can publish poems.

The name of the site is Smartpoet and is hosted on a heroku live server here https://smartpoet.herokuapp.com

I developed an online publishing platform for poets because of my interest and love for Poetry. The web app was developed using:

- Python
- Django
- Javascript
- PostgreSQL
- HTML
- CSS
- Bootstrap
- Disqus commenting system (Third party integration)

Some of the features of Smartpoet includes:

a) Social login with facebook and google

b) Multi-level authentication module with email verification, password retrieval

c) Submission of poems for review and approval

d) Social sharing of poems to various social platforms

e) Commenting system integrated with disqus

f) Categorization of poems based on parent category and sub category

g) 4 tier user roles (Superadmin, Admin, Poet, Visitor)

Superadmin can:

- Manage all site users and settings as well as activities of the lower level roles which include (admin, poet and visitor)

Visitors can:

- Read poems
- View poet profile
- Use a few filters to skim through data pages such as poems, poets etc.
- Comment on poems through disqus comments
- Register a new account to be a poet

Poets can:

- Register an account
- Verify email
- Login to access their account area
- Setup a poet profile
- Link social accounts to their smartpoet account
- Link multiple emails to their account
- Retrieve and Reset forgotten password
- Create/submit poems for approval
- Perform read and update operations on their profile details
- Perform CRUD operations on their poems.
- Like/Unlike, Upvote/Downvote, Save/Bookmark poems
- Add comments to poems

Admin can:

- Manage some site users and settings
- Perform CRUD operations on all poems
- Create categories and sub categories
- Approve or disapprove submitted poems
- perform CRUD operations on all user accounts
- Do everything poets can

h) Perform social actions like:

- Follow and Unfollow each other
- Like and Unlike each other poems
- Upvote and Downvote each other poems
- Save or Bookmark each other's poems

**************************************
**************************************
**************************************

A) Distinctiveness, Complexity requirements and Files

    1) The django project was structured to contain 3 apps:
    
    CORE
        - which serves mostly the frontend views and general assets
        - Models: 0
        - Files: (apps.py - config for core app, views.py - displays core/frontend views, urls.py - manages core urls)
    
    POSTS 
        - which serves the poems published by registered poets, including categories and sub categories:
        - Models: 3 
        - Files: (filters.py - filter posts data, apps.py - config for posts app, views.py - displays/manages frontend/backend post views, urls.py - manages post urls, forms.py - posts form classes and definitions, models.py - post model classes and definitions)
    
    MEMBERS 
        - which serves user and profile management 
        - Models: 2
        - Files: (filters.py - filter retrieved member data, apps.py - config for members app, views.py - displays/manages frontend/backend members views, urls.py - manages members urls, forms.py - members form classes and definitions, models.py - members model classes and definitions, signals.py - perform specific autonomous actions based on user activity)

    2) The django project was setup to include Social Logins:
       FACEBOOK
       GOOGLE
   
    3) The django project was setup to integrate Disqus Commenting System
    
    4) The django project was setup to include social sharing
    
    5) The django project was setup to include post/poem publishing
    
    6) The django project was setup to include post/poem voting
   

B) The application can be run by simply:

    a) installing dependencies inside requirements.txt file
    b) creating a postgreSQL database and user
    b) editing the settings.py file to include new database details
    e) executing a migrate command ("python manage.py migrate")
    f) creating a super user
    g) creating a profile from the django admin for the super user
    g) adding a site from the django admin by the superuser
    h) adding social applications using API keys from google and facebook


Thanks for the opportunity to learn python and django!
