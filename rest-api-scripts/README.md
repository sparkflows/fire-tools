
# rest-api-scripts

Scripts helps in interacting with fire rest-api's.

active_users_and_groups.py :
---------------------------
This script gets all active users and there groups and write these details in csv file.

display-hide-apps.py :
----------------------
This script display or hide apps based on the customer’s licensed use case. Ex: sales & marketing customers should only see apps that are Sales & Marketing related. It would be done via the usecase of each app.  If the usecase of the fire app matches the use case in yaml (ex: marketing or finance), that app will be displayed. Any usecase of app not matching the customer’s use case will be hidden

load-app.py :
-------------
This script will read project.json file and get the Project Tag to fetch the projects to be updated. Then it would read through all the Projects listed one by one and would read all the Apps in the Project. For each App, it would find the corresponding App based on UUID of the App in UST Fire and:
   1. update it if it exists. 
   2. Or it would create a new one if it does not exist. 
   3. Or hide apps if doesn’t exist in zip file


user_create_automation.py :
---------------------------
This script will  create_update_user details/delete_user/user_list/active_users_and_groups based on added arguments.
