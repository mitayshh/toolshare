# toolshare
This project was done as a part of a course that I was enrolled in at RIT.
This project basically helps users in the same ShareZone or Shed to easily share their tools and keep track of their requests or decisions they made.

Deployment procedures:
----------------------

1. Unzip the zip file ( how are you reading this? :) and "cd beta_for_R2/"

2. Verify that you have python3 installed. The commands in this readme explicitly use "python3" for clarity but if your system uses "python" as the executable for python3 then please keep that in mind!

3. If you are on a windows machine, skip this step.
3.a Otherwise you need to install PIL/Pillow ( python imaging libraries )
3.b On debian systems: "apt-get install python3-pil"

4. Re-initialize the DB by running: "python3 manage.py ts_create_db"

5. Run the server for testing: "python3 manage.py runserver"

6. Execute the test plan against the server by going to http://localhost:8000/toolshare

6.a Valid users are (username:password)
	admin: admin (admin interface is at http://localhost:8000/admin)
	homer: homer
	marge: marge
	bart: bart
	lisa: lisa
6.b Keep in mind that certain users have tools already added and furthermore, some borrow requests are in the system too. Not all users have tools nor borrow/share requests