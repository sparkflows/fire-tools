import argparse
from zipfile import ZipFile
import requests
import json

'''
**********EXECUTE WORKFLOW******************
python execute_workflow.py --fire_host_url="https://localhost:8080" --access_token="cacaksncaskjuuonn777-cdck" --project_ids="1|3"
In project_ids, pass the pipeseparated prject id.
***********************************
'''

def execute_workflow(fire_host,token,workflow_id):
    execute_workflow_api_url = fire_host + "/api/v1/create/workflowexecution/" + workflow_id
    api_call_headers = {
        "token": token,
    }
    data = {
        "userName": "admin",
        "workflowParameters": ""
    }
    execute_workflow_api_url_response = requests.post(execute_workflow_api_url, json=data, headers=api_call_headers)
    if(execute_workflow_api_url_response.status_code == 200):
        execution_id = execute_workflow_api_url_response.text
        print("LINK TO EXEUCTION RESULT IS:   " + fire_host + "/#/view-workflow-result/" + execute_workflow_api_url_response.text)
        print("THE RESULT OF THE EXECUTION IS SHOWN BELOW")
        get_execution_results(fire_host, token, execution_id)

def get_execution_results(fire_host, token, execution_id):
    execution_results_url = fire_host + "/api/v1/execution-results/workflow-executions/" + execution_id + "/resultType/2"
    api_call_headers = {'token': token}
    execution_results_response = requests.get(execution_results_url, headers=api_call_headers)
    status_code = execution_results_response.status_code
    if(status_code == 200):
        execution_results_text_response = execution_results_response.text
        print(execution_results_text_response)
        #execution_results_dict = json.loads(execution_results_text_response)
        #print(json.dumps(execution_results_dict, indent=4))



if __name__ == '__main__':
    args_parser = argparse.ArgumentParser(allow_abbrev=False)
    args_parser.add_argument('--fire_host_url', help='Host URL is required', type=str, required=True)
    args_parser.add_argument('--access_token', help='Access Token is required', type=str, required=True)
    args_parser.add_argument('--workflow_ids', help='Pipe Separated workflow ids', type=str, required=True)
    args = args_parser.parse_args()

    fire_host_url = args.fire_host_url
    access_token = args.access_token
    workflow_ids = args.workflow_ids
    print("fire_host_url: " + fire_host_url)
    print("access_token: " + access_token)
    print("workflow_ids: " + workflow_ids)

    for workflow in workflow_ids.split('|'):
        execute_workflow(fire_host_url, access_token, workflow)

