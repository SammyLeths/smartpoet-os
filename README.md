<h1>Smartpoet</h1>

The project involves development of an online publishing platform for poets where they can publish poems.
The name of the site is Smartpoet and is hosted on a heroku live server here https://smartpoet.herokuapp.com
I developed an online publishing platform for poets because of my interest and love for Poetry. The web app was developed using:

<ul>
  <li>Python</li>
  <li>Django</li>
  <li>Javascript</li>
  <li>PostgreSQL</li>
  <li>HTML</li>
  <li>CSS</li>
  <li>Bootstrap</li>
  <li>Disqus commenting system (Third party integration)</li>
</ul>

<h2>Screenshots</h2>

![Artboard 1v1-min](https://user-images.githubusercontent.com/64320618/210186021-5996d900-674f-438a-80b7-bf06b3fb72ef.png)

![Artboard 1v2-min](https://user-images.githubusercontent.com/64320618/210203253-cac788e4-d5a9-49d6-b44a-308e30dcd1ee.png)


<h2>Some of the features of Smartpoet includes:</h2>

<ol type="A">
  <li><h4>Social login with facebook and google</h4></li>
  <li><h4>Multi-level authentication module with email verification, password retrieval</h4></li>
  <li><h4>Submission of poems for review and approval</h4></li>
  <li><h4>Social sharing of poems to various social platforms</h4></li>
  <li><h4>Commenting system integrated with disqus</h4></li>
  <li><h4>Categorization of poems based on parent category and sub category</h4></li>
    
  <li><h4>4 tier user roles (Superadmin, Admin, Poet, Visitor)</h4>
    <ul>
      <li>Superadmin:
        <ul>
          <li>Manage all site users and settings as well as activities of the lower level roles which include (admin, poet and visitor)</li>
        </ul>
      </li>
      <li>Admin:
        <ul>
          <li>Manage some site users and settings</li>
          <li>Perform CRUD operations on all poems</li>
          <li>Create categories and sub categories</li>
          <li>Approve or disapprove submitted poems</li>
          <li>Perform CRUD operations on all user accounts</li>
          <li>Do everything poets can</li>
        </ul>
      </li> 
      <li>Poets:
        <ul>
          <li>Register an account</li>
          <li>Verify email</li>
          <li>Login to access their account area</li>
          <li>Setup a poet profile</li>
          <li>Link social accounts to their smartpoet account</li>
          <li>Link multiple emails to their account</li>
          <li>Retrieve and Reset forgotten password</li>
          <li>Create/submit poems for approval</li>
          <li>Perform read and update operations on their profile details</li>
          <li>Perform CRUD operations on their poems</li>
          <li>Like/Unlike, Upvote/Downvote, Save/Bookmark poems</li>
          <li>Add comments to poems</li>
        </ul>
      </li>
      <li>Visitors:
        <ul>
          <li>Read poems</li>
            <li>View poet profile</li>
            <li>Use a few filters to skim through data pages such as poems, poets etc.</li>
            <li>Comment on poems through disqus comments</li>
            <li>Register a new account to be a poet</li>
        </ul>
      </li>
    </ul>
  </li>
  <li><h4>Perform social actions like:</h4>
    <ul>
      <li>Follow and Unfollow each other</li>
      <li>Like and Unlike each other poems</li>
      <li>Upvote and Downvote each other poems</li>
      <li>Save or Bookmark each other's poems</li>
    </ul>
  </li>
</ol>

**************************************

<h2>A) Distinctiveness, Complexity requirements and Files</h2>

<ol type="A">
  <li><h4>The django project was structured to contain 3 apps:</h4>
    <ol type="1">
      <li><b>CORE:</b>
        <ul>
          <li>Serves mostly the frontend views and general assets</li>
          <li>Models: 0</li>
          <li>Files:
            <ul>
              <li>apps.py - config for core app, </li>
              <li>views.py - displays core/frontend views, </li>
              <li>urls.py - manages core urls </li>
            </ul>
          </li>
        </ul>
      </li>
      <li><b>POSTS:</b>
        <ul>
          <li>Serves the poems published by registered poets, including categories and sub categories</li>
          <li>Models: 3</li>
          <li>Files:
            <ul>
              <li>filters.py - filter posts data, </li>
              <li>apps.py - config for posts app, </li>
              <li>views.py - displays/manages frontend/backend post views, </li>
              <li>urls.py - manages post urls, </li>
              <li>forms.py - members form classes and definitions, </li>
              <li>models.py - post model classes and definitions </li>
            </ul>
          </li>
        </ul>
      </li>
      <li><b>MEMBERS:</b>
        <ul>
          <li>Serves user and profile management </li>
          <li>Models: 2</li>
          <li>Files:
            <ul>
              <li>filters.py - filter retrieved member data, </li>
              <li>apps.py - config for members app, </li>
              <li>views.py - displays/manages frontend/backend members views, </li>
              <li>urls.py - manages members urls, </li>
              <li>forms.py - posts form classes and definitions, </li>
              <li>models.py - members model classes and definitions, </li>
              <li>signals.py - perform specific autonomous actions based on user activity, </li>
              <li>models.py - members model classes and definitions, </li>
            </ul>
          </li>
        </ul>
      </li>
    </ol>
  </li>
  <li><h4>The django project was setup to include Social Logins:</h4>
    <ul>
      <li>FACEBOOK</li>
      <li>GOOGLE</li>
    </ul>
  </li>
  <li><h4>The django project was setup to integrate Disqus Commenting System</h4></li>
  <li><h4>The django project was setup to include social sharing</h4></li>
  <li><h4>The django project was setup to include post/poem publishing</h4></li>
  <li><h4>The django project was setup to include post/poem voting (upvote and downvote)</h4></li>
</ol>
   
<h2>The application can be run by simply:</h2>
<ol type="1">
  <li>installing dependencies inside requirements.txt file</li>
  <li>creating a postgreSQL database and user</li>
  <li>editing the settings.py file to include new database details</li>
  <li>executing a migrate command ("python manage.py migrate")</li>
  <li>creating a super user</li>
  <li>creating a profile from the django admin for the super user</li>
  <li>adding a site from the django admin by the superuser</li>
  <li>adding social applications using API keys from google and facebook</li>
</ol>

Thanks for the opportunity to learn python and django!
