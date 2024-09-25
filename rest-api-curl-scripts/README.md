REST API Curl Scripts
===========

This folder contains CURL scripts for interacting with the Fire Insights API's.


## How to Generate Access Token for Making CURL Commands
Follow the documentation here to generate access token to be able to make curl requests: https://docs.sparkflows.io/en/latest/rest-api/rest-api-authentication/acquire-token-curl.html


## Example CURL Commands

Below are some of the example curl scripts that can be used 


### [active_users_and_groups.py](https://github.com/sparkflows/fire-tools/blob/main/rest-api-scripts/active_users_and_groups.py)
#### Get Users

```
curl -X GET "http://localhost:8080/api/v1/users" -H "accept: application/json" \
        -H "token: xxxx"
```


### [export_project.py](https://github.com/sparkflows/fire-tools/blob/main/rest-api-scripts/export_project.py)
#### List Projects

```
curl -X GET "http://localhost:8080/api/v1/projects/1" \
        -H "token: xxxx"
```

#### Workflow Details by Project ID

```
curl -X GET "http://localhost:8080/api/v1/workflows/list/export?projectId=39" \
        -H "token: xxxx"
```

#### Get Dataset Details by Project ID

```
curl -X GET "http://localhost:8080/api/v1/datasets/list/export?projectId=39" \
        -H "token: xxxx
```

#### Get App Details by Project ID

```
curl -X GET "http://localhost:8080/api/v1/webApps?sortBy=category,name&projectId=39&apiCategory=details" \
-H "token: xxxx"

```

#### Get Pipleline Details by Project ID

```
curl -X GET "http://localhost:8080/getExportPipelinesDetailsByProjectId/39" \
-H "token: xxxx"

```
---
### [create_group.py](https://github.com/sparkflows/fire-tools/blob/main/rest-api-scripts/create_group.py)
#### Create New Group

```
curl -X POST "http://localhost:8080/api/v1/groups" \
        -H "Content-Type: application/json" \
        -H "token: xxxx" \
        -d '{
      "name": "testGroup1234"
    }'

```

#### Delete Group ID
```
curl -X DELETE "http://localhost:8080/deleteGroup/3" \
        -H "token: xxxx"
```

---

### **[execution_status_of_job.py](https://github.com/sparkflows/fire-tools/blob/main/rest-api-scripts/execution_status_of_job.py)**
#### Get Job Status (`get_job_status` function)
```
curl -X GET "http://localhost:8080/api/v1/update-status-workflow-execution/1" \
-H "Content-Type: application/json" \
-H "token: xxxx"

```

#### Get Execution Result (get_execution_result function)
```
curl -X GET "http://localhost:8080/viewExecutionResult/1/0" \
-H "Content-Type: application/json" \
-H "token: xxxx"

```

#### Write Execution Result to a FIle
```
curl -X GET "http://localhost:8080/viewExecutionResult/1/0" \
-H "Content-Type: application/json" \
-H "token: xxxx" \
> execution_result.json
```
---

### Import and Execute Pipelines

#### Import Single Pipeline from JSON File
```
curl -X POST "http://localhost:8080/api/v1/pipelines/multiple/import?projectId=39" \
        -H "token: xxxx" \
        -F "file1=@/path/to/pipeline/pipeline.json"
```

#### Import Multiple Pipelines from JSON Files
```
curl -X POST "http://localhost:8080/api/v1/pipelines/multiple/import?projectId=39" \
        -H "token: xxxx" \
        -F "file1=@/path/to/pipeline/pipeline.json" \
        -F "file1=@/path/to/pipeline/pipeline_2.json"

{"fail":"0","total":"2","success":"2"}
```


#### Execute Pipeline
```
curl --location --request POST 'http://localhost:8080/executePipeline?pipelineName=pipeline_2&projectId=39' \
        --header 'token: xxxx' \
        --header 'Content-Type: application/json' \
        --data-raw '{"userName": "admin", "workflowParameters":""}'
```

### **[execute_workflow.py](https://github.com/sparkflows/fire-tools/blob/main/rest-api-scripts/execute_workflow.py)**

#### Workflow Execution
```
curl -X POST "http://localhost:8080/api/v1/create/workflowexecution/309" \
        -H "Content-Type: application/json" \
        -H "token: xxxx" \
        -d '{
      "userName": "admin",
      "workflowParameters": ""
    }'
```
### [generate_token.py](https://github.com/sparkflows/fire-tools/blob/main/rest-api-scripts/generate_token.py)

#### Generate Token 
```
curl -X POST "http://localhost:8080/api/v1/tokens" \
        -H "Content-Type: application/json" \
        -H "token: xxxx" \
        -d '{
      "expiredDuration": "60" 
    }'

```

---

### Create and Update a User

#### Create a User
```
curl --location 'http://localhost:8080/api/v1/users' \          
--header 'token: xxxx' \
--header 'Content-Type: application/json' \
--data-raw '{
  "active": true,
  "email": "FnameLname@domain.com",
  "firstName": "FName",
   "groups": [
    1
  ],
  "id":0,
  "isSuperuser": true,
  "lastName": "LName",
  "password": "test@123",
  "persona": 0,
  "roles": [
    1
  ],
  "superuser": true,
  "username": "FL1"
}'
```

Example Output:
```
User FL1 created successfully with user id 38
```

#### Update the User
```
curl --location 'http://localhost:8080/api/v1/users' \          
--header 'token: xxxx' \
--header 'Content-Type: application/json' \
--data-raw '{
  "active": true,
  "email": "NEWFnameLname@domain.com",
  "firstName": "FName",
   "groups": [
    1
  ],
  "id":38,
  "isSuperuser": true,
  "lastName": "LName",
  "password": "test@123",
  "persona": 0,
  "roles": [
    1
  ],
  "superuser": true,
  "username": "FL1"
}'
```

Example Output:
```
User FL1 created successfully with user id 38
```



