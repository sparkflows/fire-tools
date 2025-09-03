import argparse
import requests
import json

'''
************Execute pipeline************
----------------------
Script: execute_pipeline.py
This script executes inputted workflows and outputs a link to the execution result. It takes in a firehosturl, an access token,pipeline name and project id.
command:  
   python execute_pipeline.py --fire_host_url="https://localhost:8080" --access_token="cacaksncaskjuuonn777-cdck" --pipeline_name="test_pipeline" --project_id=1"

   This command executes pipeline 1234 and outputs the link to the execution result


----------------------
*************************************************
'''


def execute_pipeline(fire_host, token, pipeline_name,project_id):
    print(pipeline_name)
    execute_pipeline_api_url = (fire_host + "/executePipeline?pipelineName={name}&projectId={id}").format(name=str(pipeline_name),id=str(project_id))
    api_call_headers = {
        "token": token
    }
    data = {
        "workflowParameters": ""
    }
    execute_pipeline_api_response = requests.post(execute_pipeline_api_url, json=data, headers=api_call_headers)
    print(execute_pipeline_api_response.status_code)
    if execute_pipeline_api_response.status_code == 200:
        print(execute_pipeline_api_response.text)


if __name__ == '__main__':
    args_parser = argparse.ArgumentParser(allow_abbrev=False)
    args_parser.add_argument('--fire_host_url', help='Host URL is required', type=str, required=True)
    args_parser.add_argument('--access_token', help='Access Token is required', type=str, required=True)
    args_parser.add_argument('--pipeline_name', help='Pipeline name is required', type=str, required=True)
    args_parser.add_argument('--project_id', help='Project id is required', type=int, required=True)
    args = args_parser.parse_args()

    fire_host_url = args.fire_host_url
    access_token = args.access_token
    pipeline_name = args.pipeline_name
    project_id = args.project_id
    print("fire_host_url: " + fire_host_url)
    print("access_token: " + access_token)
    print("pipeline_name: " + pipeline_name)
    print("project_id: "+str(project_id))

    execute_pipeline(fire_host_url, access_token, pipeline_name,project_id)
