# Instaclone
Yomi Denzel Foundation Graduating Project
Tasked with making a cool project with our new found knowledge in Django.
Team decided to see if we could recreate instagram, as it's main backed is written in Django.
The UI is very poor, given the time constraints and limited UI skill amongst the team members.
The features we were able to include after extending the static code with vanilla javascript are
1. Create, Delete and Update Posts. Posts can contain photos as well (no videos)
2. Like, Unlike Posts
3. Create, Delete comments on posts (security to make sure you can only change your own comment)
4. Follow, Unfollow Users (You can only see the posts of users you follow)
5. Dms (The most technical so far, UI is poor, but the implementation is very good for a beginner) (Security to make sure "/dm/{name}" resolves to dm containing logged in user and requested user)
6. Profile Editing
7. Miscellanous-Document Title updates to reflects logged in user, Certain aspects of the UI reflect to show Users ownership.
The project was developed in a little over 2 weeks. And allowed us to employ basic understanding in reactivity, dynamic rendering with JS, Api, backend security and database management with Django

Note: Make migrations to generate new dbsqlite database for project
py manage.py makemigrations user
py manage.py migrate
