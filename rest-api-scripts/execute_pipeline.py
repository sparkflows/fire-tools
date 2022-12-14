import argparse
import requests
import json

'''
************Execute pipeline************
----------------------
Script: execute_pipline.py

This script executes inputted workflows and outputs a link to the execution result. It takes in a firehosturl, an access token, and a pipe-separated pipeline id.

command:  
   python execute_pipline.py --fire_host_url="https://localhost:8080" --access_token="cacaksncaskjuuonn777-cdck" --pipeline_ids="1234"
   
   This command executes pipeline 1234 and outputs the link to the execution result
  
 
----------------------
*************************************************
'''
def execute_pipeline(fire_host,token,pipeline_id):
    print(pipeline_id)
    execute_pipeline_api_url = fire_host + "/api/v1/create/pipelineExecution/" + pipeline_id
    api_call_headers = {
        "token": token
    }
    data = {
        "userName": "admin",
        "workflowParameters": ""
    }
    execute_pipeline_api_url_response = requests.post(execute_pipeline_api_url, json=data, headers=api_call_headers)
    print(execute_pipeline_api_url_response.status_code)
    print(execute_pipeline_api_url)
    get_execution_results(fire_host, token, str(38))
    if(execute_pipeline_api_url_response.status_code == 200):
        print("LINK TO EXEUCTION RESULT IS:   " + fire_host + "/#/view-workflow-result/" + execute_pipeline_api_url_response.text)
        print("THE RESULT OF THE EXECUTION IS SHOWN BELOW")
        get_execution_results(fire_host, token, execute_pipeline_api_url_response.text)
        #print(execute_pipeline_api_url_response.json())

def get_execution_results(fire_host, token, execution_id):
    execution_results_url = fire_host + "/api/v1/pipelines/execution/" + execution_id
    api_call_headers = {'token': token}
    execution_results_response = requests.get(execution_results_url, headers=api_call_headers)
    status_code = execution_results_response.status_code
    if(status_code == 200):
        execution_results_text_response = execution_results_response.text
        #print(execution_results_text_response)
        execution_results_dict = json.loads(execution_results_text_response)
        print(execution_results_dict)
    #print(execution_results_url)



if __name__ == '__main__':
    args_parser = argparse.ArgumentParser(allow_abbrev=False)
    args_parser.add_argument('--fire_host_url', help='Host URL is required', type=str, required=True)
    args_parser.add_argument('--access_token', help='Access Token is required', type=str, required=True)
    args_parser.add_argument('--pipeline_ids', help='Pipe Separated pipeline ids', type=str, required=True)
    args = args_parser.parse_args()

    fire_host_url = args.fire_host_url
    access_token = args.access_token
    pipeline_ids = args.pipeline_ids
    print("fire_host_url: " + fire_host_url)
    print("access_token: " + access_token)
    print("pipeline_ids: " + pipeline_ids)

    for pipeline in pipeline_ids.split('|'):
        execute_pipeline(fire_host_url, access_token, pipeline)

