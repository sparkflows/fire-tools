
# CLI Scripts

Following Python scripts allow users to interact with Fire REST API's.

Prerequisites
-------------

Python 3.7+ is needed.

The following libraries need to be installed:

* `pip install pandas`
* `pip install requests`
* `pip install aiohttp`


Generating Access Token
-------------------------

For interacting with Fire REST API's access token is required. The steps to generate the same can be found in the page below:

https://docs.sparkflows.io/en/latest/rest-api/rest-api-authentication/acquire-token-curl.html

Swagger UI
-------------------------

For information on enabling and accessing SwaggerUI review the docs below:

https://docs.sparkflows.io/en/latest/installation/monitoringandmetrics/rest-api.html

Fetch All Active Users and Groups
---------------------------

**Script Name**: `active_users_and_groups.py`

This script retrieves all active users and their groups. It then writes these details into a csv file.

**Command**:

`python active_users_and_groups.py <fire_host_url> <access_token>`

**Arguments**:

`fire_host_url` : The URL in the format http://host_ip:port where Sparkflows is running.

`access_token` : The access token generated from the Administrative tab of Sparkflows.

**Example**:

`python active_users_and_groups.py http://localhost:8080 cacaksncaskjuuonn777-cdck`

This will write a csv file containing all active users and groups of this url

Display or hide Apps
----------------------

**Script Name**: `display-hide-apps.py`

This script displays or hide apps based on the customer’s licensed use case. Ex: sales & marketing customers should only see apps that are Sales & Marketing related. It would be done via the usecase of each app.  If the usecase of the fire app matches the use case in yaml (ex: marketing or finance), that app will be displayed. Any usecase of app not matching the customer’s use case will be hidden.

**Command**:

`python display-hide-apps.py <fire_host_url> <access_token> <file_path>`

**Arguments**:

`fire_host_url` : The URL in the format http://host_ip:port where Sparkflows is running.

`access_token` : The access token generated from the Administrative tab of Sparkflows.

`file_path` : The file path of the yaml file to get a list of apps

**Example**:

`python display-hide-apps.py http://localhost:8080 cacaksncaskjuuonn777-cdck config.yaml`

Load Apps
-------------

**Script Name**: `load-app.py`

This script will read `project.json` file and get the Project Tag to fetch the projects to be updated. Then it would read through all the Projects listed one by one and would read all the Apps in the Project. For each App, it would find the corresponding App based on UUID of the App in Fire and:

   1. Update, if it exists. 
   2. Create a new one if it does not exist. 
   3. Hide apps if doesn’t exist in zip file

**Command**:
`python load-app.py --fire_host_url="https://localhost:8080" --access_token="cacaksncaskjuuonn777-cdck" --project_zip_path="/sah/trud/" --group_name="abc"`

**Arguments**:

`--fire_host_url` : The URL in the format http://host_ip:port where Sparkflows is running.

`--access_token` : The access token generated from the Administrative tab of Sparkflows.

`--project_zip_path` : The path to a json file that contains project information

`--group_name` : The name of the group you wish to upload the project to

**Example**

`python load-app.py --fire_host_url="https://localhost:8080" --access_token="cacaksncaskjuuonn777-cdck" --project_zip_path="/sah/trud/" --group_name="abc"`



View, Create, Update , Delete User Details and Update Email Ids for multiple users
---------------------------

**Script Name**: `user_create_automation.py`

- Create/update/delete/list User Details based on added arguments.

**Command**:

This command takes in a variable amount of arguments depending on what needs to be done

If you would like to list the user list of your host_url the command would be:

`python user_create_automation.py <fire_host_url> <access token> user_list`

If you would like to list the active user list of your host_url the command would be:

`python user_create_automation.py <fire_host_url> <access token> active_users_and_groups`

If you would like to delete a user the command would be:

`python user_create_automation.py <fire_host_url> <access_token> <user_id>`

If you would like to create or update a user:

`python user_create_automation.py <fire_host_url> <access_token> <username> <password> <firstName> <lastName> <email> <roles> <groups> <userId>`



- Create/update User details based on provided list of users in the file.

**Command**: 

`python users_create_automation.py --fire_host_url="https://host_name:port" --access_token="xxxxxxxxxxxx" --users_file_path="path_of_file_with_list_of_users"`

**Arguments**:

The script above expects the below command line arguments:

`--fire_host_url` : The URL in the format http://host_ip:port where Sparkflows is running.

`--access_token` : The access token generated from the Administrative tab of Sparkflows.

`--users_file_path` : The path of the file which has the list of Users. Format of each row in the file should be in the format below.Multiple roles and group ids can be separated with pipe.

```<username>,<password>,<first_name>,<last_name>,<email>,<role_ids>,<group_ids>,<is_superuser>,<is_active>```

**Example to update only one role and group along with other properties**:

test,test@123,test,test,test@email.com,role1,group1,true,true

**Example to update multiple roles and groups along with other properties**:

test,test@123,test,test,test@email.com,role1|role2,group1|group1,true,true
   
**Example to update the details of users**: 

   `python users_create_automation.py --fire_host_url="https://localhost:8080" --access_token="cacaksncaskjuuonn777-cdck" --users_file_path="new_users_file_path"`

- Update Email Ids for multiple users from a csv file

**Script Name**: `update_users_profile.py`

**Command**:

`python update_users_profile.py --fire_host_url="http://localhost:8080" --access_token="xxxx" --users_file_path="users_email_csv_file_path"`

**Arguments**:

The script above expects the below command line arguments:

`--fire_host_url` : The URL in the format http://host_ip:port where Sparkflows is running.

`--access_token` : The access token generated from the Administrative tab of Sparkflows.

`--users_file_path` : The path of the csv file which contains the list of data having the column names as username and email.

**Example to update email ids for multiple users**:

`python update_users_profile.py --fire_host_url="http://localhost:8080" --access_token="xxxx" --users_file_path="users.csv"`

It will display the below output for the list of users added to the users.csv file

User Profile of testuser updated successfully

User Profile of testuser2 updated successfully

   
Import Projects
----------------------

**Script Name**: `import_project.py`

This script will import project workflows, datasets, analytics apps and pipelines present in exported zip file in which it will read through that project folder whose name is given in arguments.

**Command**:

`import_project.py --fire_host_url="https://host_name:port" --access_token="xxxxxxxxxxxx" --project_zip_path="Projects_xxxx.zip" --selected_project_name="yyyyyyy"`

**Arguments**:

The script above expects the below command line arguments:

`--fire_host_url` : The URL in the format http://host_ip:port where Sparkflows is running.

`--access_token` : The access token generated from the Administrative tab of Sparkflows.

`--project_zip_path` : The zip file of exported projects from which we intend to import projects.

`--selected_project_name` : The Name of the project that needs to be imported.

`--project_id` : Pass the project ID if the project needs to be imported/updated into one of the existing project. This will not create a new project.

   

**Example to import as a new project**:

`python import_project.py --fire_host_url="https://localhost:8080" --access_token="cacaksncaskjuuonn777-cdck" --project_zip_path="Projects_133535.zip" --selected_project_name="analytics"`

Projects_133535.zip can have multiple project folders. The comand above will create the new project with name analytics.
   
   
**Example to import into an existing project**: 

`import_project.py --fire_host_url="https://localhost:8080" --access_token="cacaksncaskjuuonn777-cdck" --project_zip_path="Projects_133535.zip" --selected_project_name="analytics" --project_id "42"`
   
The command above will update the existing project with id 42.
   
   
Export Projects
----------------------

**Script Name**: `export_project.py`

This script will export the project workflows, datasets, analytics apps and pipelines into zip file. Inside the zip file there will be folder for each project.

**Command**:

`python export_project.py --fire_host_url="https://host_name:port" --access_token="xxxxxxxxxxxx" --project_ids="yyy|zzz"`

**Arguments**:

The script above expects the below command line arguments:

`--fire_host_url` : The URL in the format http://host_ip:port where Sparkflows is running.

`--access_token` : The access token generated from the Administrative tab of Sparkflows.

`--project_ids` : Pass the project ID's of the porjects that need to be Exported seperated by a Pipe operator

**Example to export multiple projects**:  

   `python export_project.py --fire_host_url="https://localhost:8080" --access_token="cacaksncaskjuuonn777-cdck" --project_ids="1|3"`
   
   The command above will create one zipfolder with separate sub-folder for each project id that is passed in via the --project_ids argument.

Workflow Metric Reporter
----------------------
**Script Name**: `workflow_metric_reporter.py`

This script will export a csv file containing execution results regarding a specified project_id.

**Command**:

`python workflow_metric_reporter.py --fire_host_url="https://localhost:8080" --access_token="cacaksncaskjuuonn777-cdck" --project_id="1" --summary=True`  

The script above expects the below command line arguments:

`--fire_host_url` : The URL in the format http://host_ip:port where Sparkflows is running.

`--access_token` : The access token generated from the Administrative tab of Sparkflows.

`--project_id` : The Project ID whose executions you want to export

`--summary` : Optional Parameter if included descriptive csv is returned as well. 


   `python workflow_metric_reporter.py --fire_host_url="https://localhost:8080" --access_token="cacaksncaskjuuonn777-cdck" --project_id="1" --summary`

   The command above will create 3 csv files containing information regarding project 1. One general csv file containing all executions, one csv file containing the average latency of each workflow, one containing the workflows sorted by exeuction time, and one csv file containing the execution status count for each workflow. 
   
   `python workflow_metric_reporter.py --fire_host_url="https://localhost:8080" --access_token="cacaksncaskjuuonn777-cdck" --project_id="1"`
   
   The command above will create 1 csv file containing information regarding project 1. One general csv file containing all executions. 

Async Workflow Metric Reporter
----------------------
**Script Name**: `async_workflow_metric_reporter.py`

This script will export a csv file containing execution results regarding a specified project_id. It works the same as workflow_metric_reporter just faster.

**Command**:

`python async_workflow_metric_reporter.py --fire_host_url="https://localhost:8080" --access_token="cacaksncaskjuuonn777-cdck" --project_id="1" --summary=True`  

The script above expects the below command line arguments:

`--fire_host_url` : The URL in the format http://host_ip:port where Sparkflows is running.

`--access_token` : The access token generated from the Administrative tab of Sparkflows.

`--project_id` : The Project ID whose executions you want to export

`--summary` : Optional Parameter if included descriptive csv is returned as well. 


   `python async_workflow_metric_reporter.py --fire_host_url="https://localhost:8080" --access_token="cacaksncaskjuuonn777-cdck" --project_id="1" --summary`

   The command above will create 3 csv files containing information regarding project 1. One general csv file containing all executions, one csv file containing the average latency of each workflow, one containing the workflows sorted by exeuction time, and one csv file containing the execution status count for each workflow. 
   
   `python async_workflow_metric_reporter.py --fire_host_url="https://localhost:8080" --access_token="cacaksncaskjuuonn777-cdck" --project_id="1"`
   
   The command above will create 1 csv file containing information regarding project 1. One general csv file containing all executions. 


   
