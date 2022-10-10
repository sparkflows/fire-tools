
# rest-api-scripts

The below scripts help in interacting with Fire REST API's.

Generating Access Token
-------------------------

For interacting with Fire REST API's access token is required.

The steps to generate the access token are in the page below:

https://docs.sparkflows.io/en/latest/rest-api/rest-api-authentication/acquire-token-curl.html

active_users_and_groups.py
---------------------------

This script gets all active users and their groups. It then writes these details into a csv file.

display-hide-apps.py
----------------------

This script displays or hide apps based on the customer’s licensed use case. Ex: sales & marketing customers should only see apps that are Sales & Marketing related. It would be done via the usecase of each app.  If the usecase of the fire app matches the use case in yaml (ex: marketing or finance), that app will be displayed. Any usecase of app not matching the customer’s use case will be hidden.

load-app.py
-------------

This script will read project.json file and get the Project Tag to fetch the projects to be updated. Then it would read through all the Projects listed one by one and would read all the Apps in the Project. For each App, it would find the corresponding App based on UUID of the App in Fire and:

   1. update it if it exists. 
   2. Or it would create a new one if it does not exist. 
   3. Or hide apps if doesn’t exist in zip file


user_create_automation.py
---------------------------

This script will  create_update_user details/delete_user/user_list/active_users_and_groups based on added arguments.


users_create_automation.py
---------------------------

This script will  create_update_user details/delete_user/user_list/active_users_and_groups based on provided list of users in the file.

format of the file content

<username>,<password>,<first_name>,<last_name>,<email>,<role_ids>,<group_ids>,<is_superuser>,<is_active>
ex: test,test@123,test,test,test@**.com,role1|role2,group1|group1,true or false, true or false
Multiple role and group ids separated with pipe. 

import_project.py
----------------------

This script will import project workflows, datasets, analytics apps and pipelines present in exported zip file in which it will read through that project folder whose name is given in arguments in given Project Id. 

export_project.py
----------------------

This script will import project workflows, datasets, analytics apps and pipelines present in exported zip file in which it will read through that project folder whose name is given in arguments in given Project Id. 
