import argparse
import requests
import json
import pandas as pd

'''
**********WORKFLOW REPORTER******************
python workflow_reporter.py --fire_host_url="https://localhost:8080" --access_token="cacaksncaskjuuonn777-cdck" --project_id="1" --export_name="out.csv"

This script takes in a project id and a name to the file you want to export and returns a csv file containing
the execution metrics of all executions of a project. 
***********************************
'''


def get_workflow_information(fire_url, token, project_id, export_name):
    get_workflow_information_url = fire_url + "/api/v1/workflows?projectId=" + project_id
    api_call_headers = {'token': token}
    status_code = requests.get(get_workflow_information_url, headers=api_call_headers).status_code
    if(status_code==200):
        get_workflow_information_text = requests.get(get_workflow_information_url,headers=api_call_headers).text
        get_workflow_information_dict = json.loads(get_workflow_information_text)
        total_reporter_dataframe = pd.DataFrame()
        for workflow in get_workflow_information_dict:
            workflow_id = str(workflow["id"])
            execution_dataframe = get_execution_information(fire_url,token,workflow_id)
            total_reporter_dataframe = pd.concat([total_reporter_dataframe,execution_dataframe], ignore_index=True)
        total_reporter_dataframe.to_csv(export_name)

def get_execution_information(fire_url, token, workflow_id):
    get_execution_information_url = fire_url + "/api/v1/workflow-executions/workflows/" + workflow_id
    api_call_headers = {'token': token}
    status_code = requests.get(get_execution_information_url, headers=api_call_headers).status_code
    if(status_code==200):
        get_execution_information_text = requests.get(get_execution_information_url, headers=api_call_headers).text
        get_execution_information_dict = json.loads(get_execution_information_text)
        executionDataframe = pd.DataFrame()
        for execution in get_execution_information_dict:
            execution_id = str(execution["id"])
            analysisFlowId = str(execution["analysisFlowId"])
            workflow_name = execution["name"]
            execution_time = execution["endTime"] - execution["startTime"]
            if(execution["status"]==0):
                status = "RUNNING"
            elif (execution["status"] == 1):
                status = "STOPPED"
            elif (execution["status"] == 2):
                status = "COMPLETED"
            elif (execution["status"] == 3):
                status = "FAILED"
            elif (execution["status"] == 4):
                status = "STARTING"
            elif (execution["status"] == 5):
                status = "STOP"
            elif (execution["status"] == 6):
                status = "KILLED"
            else:
                status = "INVALID STATUS"
            #print(execution_time)
            executionSeries = pd.DataFrame({
                'execution_id':[execution_id],
                'analysisFlowId':[analysisFlowId],
                'workflow_name':[workflow_name],
                'execution_time':[execution_time],
                'status':[status]
            })
            executionDataframe = pd.concat([executionDataframe,executionSeries], ignore_index=True)
        return executionDataframe






if __name__ == '__main__':
    args_parser = argparse.ArgumentParser(allow_abbrev=False)
    args_parser.add_argument('--fire_host_url', help='Host URL is required', type=str, required=True)
    args_parser.add_argument('--access_token', help='Access Token is required', type=str, required=True)
    args_parser.add_argument('--project_id', help='ID of project', type=str, required=True)
    args_parser.add_argument('--export_name', help='name of the csv file you want to export to', type=str, required=True)
    args = args_parser.parse_args()
    fire_host_url = args.fire_host_url
    access_token = args.access_token
    project_ids = args.project_id
    export_name = args.export_name
    args = args_parser.parse_args()
    get_workflow_information(fire_url=fire_host_url, token=access_token, project_id=project_ids, export_name=export_name)