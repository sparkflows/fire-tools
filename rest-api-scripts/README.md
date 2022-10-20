
# CLI Scripts

Following Python scripts allow users to interact with Fire REST API's.

Generating Access Token
-------------------------

For interacting with Fire REST API's access token is required. The steps to generate the same can be found in the page below:

https://docs.sparkflows.io/en/latest/rest-api/rest-api-authentication/acquire-token-curl.html

Fetch All Active Users and Groups
---------------------------

**Script Name**: `active_users_and_groups.py`

This script retrieves all active users and their groups. It then writes these details into a csv file.

Display or hide Apps
----------------------

**Script Name**: `display-hide-apps.py`

This script displays or hide apps based on the customer’s licensed use case. Ex: sales & marketing customers should only see apps that are Sales & Marketing related. It would be done via the usecase of each app.  If the usecase of the fire app matches the use case in yaml (ex: marketing or finance), that app will be displayed. Any usecase of app not matching the customer’s use case will be hidden.


Load Apps
-------------

**Script Name**: `load-app.py`

This script will read `project.json` file and get the Project Tag to fetch the projects to be updated. Then it would read through all the Projects listed one by one and would read all the Apps in the Project. For each App, it would find the corresponding App based on UUID of the App in Fire and:

   1. Update, if it exists. 
   2. Create a new one if it does not exist. 
   3. Hide apps if doesn’t exist in zip file


View, Create, Update and Delete User Details
---------------------------

**Script Name**: `user_create_automation.py`

This script will create_update_user details/delete_user/user_list/active_users_and_groups based on added arguments.


Create and Update List of Users
---------------------------

**Script Name**: `users_create_automation.py`

This script will create_update_user with details based on provided list of users in the file.

Format of each row in the file:

```<username>,<password>,<first_name>,<last_name>,<email>,<role_ids>,<group_ids>,<is_superuser>,<is_active>```

ex: test,test@123,test,test,test@**.com,role1|role2,group1|group1,true or false, true or false

Multiple roles and group ids can be separated with pipe as shown in the example above. Then, pass the file path to --users_file_path argument.
   
Command: 
   users_create_automation.py --fire_host_url="https://localhost:8080" --access_token="cacaksncaskjuuonn777-cdck" --users_file_path="new_users_file_path"

   
Import Project
----------------------

**Script Name**: `import_project.py`

This script will import project workflows, datasets, analytics apps and pipelines present in exported zip file in which it will read through that project folder whose name is given in arguments.
   

Command: import_project.py --fire_host_url="https://localhost:8080" --access_token="cacaksncaskjuuonn777-cdck" --project_zip_path="Projects_133535.zip" --selected_project_name="analytics"

   Projects_133535.zip can have multiple project folders. Above command will create the new project with name analytics.
   
   
Command: import_project.py --fire_host_url="https://localhost:8080" --access_token="cacaksncaskjuuonn777-cdck" --project_zip_path="Projects_133535.zip" --selected_project_name="analytics" --project_id "42"
   
   Above command will update the existing project with id 42.
   
   
Export Project
----------------------

**Script Name**: `export_project.py`

This script will export the project worfklows, datasets, analytics apps and pipelines into zip file. Inside the zip file there will be folder for each projects.
  
Command:  
   export_project.py --fire_host_url="https://localhost:8080" --access_token="cacaksncaskjuuonn777-cdck" --project_ids="1|3"
   
   Above command will create the zipfolder with separate folder for each project ids passed in --project_ids arguments.
   
   
