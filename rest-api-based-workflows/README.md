REST API Based Workflows
====

This folder contains workflows that use REST APIs to generate specific data. Below are the details of each workflow in this folder, along with instructions on how to run them.

## Prerequisite - Generating Access Token

For interacting with Fire REST API's access token is required. The steps to generate the same can be found in the page below:

https://docs.sparkflows.io/en/latest/rest-api/rest-api-authentication/acquire-token-curl.html

## Workflow - PySparkGetWorkflowExeFromAndToDate

This workflow is used to get all the executions of a user from a given from and to date. Below are the steps on how to run the above pyspark workflow -

1. Firstly download the **PySparkGetWorkflowExeFromAndToDate.json**, then to a running sparkflows environment navigate to any project and import the downloaded workflow json file.
2. Once the workflow is imported , edit the workflow and click on **Add Parameters** button and update the following params -

`fire_host` : The URL in the format http://host_ip:port where Sparkflows is running. **(Required field)**

`api_token` : The access token generated from the Administrative tab of Sparkflows. **(Required field)**

`from_date` : The date from which the records should be retrieved. **(Required field)**

**Date Format** - **yyyy-MM-dd** (Ex: 2025-12-03)

`to_date` : The date up to which the records should be retrieved. **(Required field)**

**Date Format** - **yyyy-MM-dd** (Ex: 2025-12-05)

3. Once the fields are correctly updated execute the workflow , and the output will contains the following headers -

* executionId
* workflowId
* workflowName
* projectId
* projectName
* username
* status
* startTime
* endTime
* applicationId
* fireJobId
* logs
* executionType

## Workflow - PySparkWorkflowStatusAgent

This workflow is used to get the latest execution status of all workflows of all projects. Below are the steps on how to run the above pyspark workflow -

1. Firstly download the **PySparkWorkflowStatusAgent.json**, then to a running sparkflows environment navigate to any project and import the downloaded workflow json file.
2. Once the workflow is imported , edit the workflow and click on **Add Parameters** button and update the following params -

`fire_host` : The URL in the format http://host_ip:port where Sparkflows is running. **(Required field)**

`api_token` : The access token generated from the Administrative tab of Sparkflows. **(Required field)**

`project_ids_str` : **none** or Comma separted single quoted project ids whose latest execution status is to be retrieved. **(Required field)**

**Default Value:** **none** , When set as **none** In this case data of latest execution status of all workflows of all projects will be retrieved

**Comma separted single quoted project ids** - In this case data of latest execution status of all workflows of only the projects whose ids are passed like the following will be retrieved - 
Ex: '14788','14865'

3. Once the fields are correctly updated execute the workflow , and the output will contains the following headers -

* workflowId
* workflowName
* projectId
* status
* startTime
* endTime
* username

