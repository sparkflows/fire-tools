
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

This script will create/update/delete/list User Details based on added arguments.


Create and Update List of Users
---------------------------

**Script Name**: `users_create_automation.py`

This script will create/update User details based on provided list of users in the file.

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

   ``python users_create_automation.py --fire_host_url="https://localhost:8080" --access_token="cacaksncaskjuuonn777-cdck" --users_file_path="new_users_file_path"``

   
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

``python import_project.py --fire_host_url="https://localhost:8080" --access_token="cacaksncaskjuuonn777-cdck" --project_zip_path="Projects_133535.zip" --selected_project_name="analytics"``

Projects_133535.zip can have multiple project folders. The comand above will create the new project with name analytics.
   
   
**Example to import into an existing project**: 

import_project.py --fire_host_url="https://localhost:8080" --access_token="cacaksncaskjuuonn777-cdck" --project_zip_path="Projects_133535.zip" --selected_project_name="analytics" --project_id "42"
   
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

`--project_ids` : Pass the project ID's of the project that need to be Exported seperated by a Pipe operator

**Example to export multiple projects**:  

   ``python export_project.py --fire_host_url="https://localhost:8080" --access_token="cacaksncaskjuuonn777-cdck" --project_ids="1|3"``
   
   The command above will create one zipfolder with separate sub-folder for each project id that is passed in via the --project_ids argument.

Execute Workflow
----------------------

**Script Name**: `execute_workflow.py`

This script will execute pipe-separated workflows
**Command**:

`python execute_workflow.py --fire_host_url="https://host_name:port" --access_token="xxxxxxxxxxxx" --workflow_ids="yyy|zzz"`

**Arguments**:

The above script expects the below command line arguments:

`--fire_host_url` : The URL in the format http://host_ip:port where Sparkflows is running.

`--access_token` : The access token generated from the Administrative tab of Sparkflows.

`--workflow_ids` : Pass the workflow_ids of the workflows that need to be executed, seperated by a Pipe operator

**Example to export multiple projects**:  

   ``python execute_workflow.py --fire_host_url="https://localhost:8080" --access_token="cacaksncaskjuuonn777-cdck" --workflow_ids="1|3"``
   
   The following command will execute the workflow with an id of 1 and the workflow with an id of 3 and then output the execution result for both

Execute Pipeline
---------------------

**Script Name**: `execute_pipeline.py`

This script will execute pipe-separated pipelines
**Command**:

`python execute_pipeline.py --fire_host_url="https://host_name:port" --access_token="xxxxxxxxxxxx" --pipeline_ids="yyy|zzz"`

**Arguments**:

The above script expects the below command line arguments:

`--fire_host_url` : The URL in the format http://host_ip:port where Sparkflows is running.

`--access_token` : The access token generated from the Administrative tab of Sparkflows.

`--pipeline_ids` : Pass the pipeline_ids of the pipeline that need to be executed, seperated by a Pipe operator

**Example to export multiple projects**:  

   ``python execute_pipeline.py --fire_host_url="https://localhost:8080" --access_token="cacaksncaskjuuonn777-cdck" --pipeline_ids="1|3"``
   
   The following command will execute the pipeline with an id of 1 and the pipeline with an id of 3 and then output the execution result for both

Workflow Metric Reporter
----------------------
**Script Name**: `workflow_metric_reporter.py`

This script will export a csv file containing desired information regarding a specified project_id.

**Command**:

`python workflow_metric_reporter.py --fire_host_url="https://localhost:8080" --access_token="cacaksncaskjuuonn777-cdck" --project_id="1" --summary`  

The script above expects the below command line arguments:

`--fire_host_url` : The URL in the format http://host_ip:port where Sparkflows is running.

`--access_token` : The access token generated from the Administrative tab of Sparkflows.

`--project_id` : The Project ID whose executions you want to export

`--summary` : An optional argument set to true if included. If included, 3 additional csv files will be exported: one csv file containing the average latency of each workflow, one containing the workflows sorted by exeuction time, and one csv file containing the execution status count for each workflow. If not included then only the one general csv file containing all executions will be exported. 


   `python workflow_metric_reporter.py --fire_host_url="https://localhost:8080" --access_token="cacaksncaskjuuonn777-cdck" --project_id="1" --summary`

   The command above will create 3 csv files containing information regarding project 1. One general csv file containing all executions, one csv file containing the average latency of each workflow, one containing the workflows sorted by exeuction time, and one csv file containing the execution status count for each workflow. 
   
   `python workflow_metric_reporter.py --fire_host_url="https://localhost:8080" --access_token="cacaksncaskjuuonn777-cdck" --project_id="1"`
   
   The command above will create 1 csv file containing information regarding project 1. One general csv file containing all executions. 

      
   

