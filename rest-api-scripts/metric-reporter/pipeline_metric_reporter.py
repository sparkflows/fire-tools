import argparse
import requests
import json
import time
import pandas as pd
from datetime import datetime

'''
************Pipeline Metric Reporter************
----------------------
Script: pipeline_metric_reporter.py
This script will export a csv file containing the latency and status of all pipeline executions of a specified project_id. The summary argument is a Boolean, if set to True additional metrics will be exported (longest_latency, status_count, oldest executions).
command:  
   python pipeline_metric_reporter.py --fire_host_url="https://localhost:8080" --access_token="cacaksncaskjuuonn777-cdck" --project_id="1" --summary=True  

   The command above will create 3 csv files containing information regarding project 1. One general csv file containing all executions, one csv file containing the average latency of each workflow, one containing the workflows sorted by exeuction time, and one csv file containing the execution status count for each workflow. 

   python pipeline_metric_reporter.py --fire_host_url="https://localhost:8080" --access_token="cacaksncaskjuuonn777-cdck" --project_id="1" --summary=False

   The command above will create 1 csv file containing information regarding project 1. One general csv file containing all pipeline executions. 
----------------------
*************************************************
'''


def get_pipeline_information(fire_url, token, project_id, summary):
    get_pipeline_information_url = fire_url + "/api/v1/pipeline/executions/project/" + project_id
    api_call_headers = {'token': token}
    status_code = requests.get(get_pipeline_information_url, headers=api_call_headers).status_code
    if (status_code == 200):
        get_pipeline_information_text = requests.get(get_pipeline_information_url, headers=api_call_headers).text
        get_pipeline_information_dict = json.loads(get_pipeline_information_text)
        total_reporter_dataframe = pd.DataFrame()
        for pipeline in get_pipeline_information_dict:
            pipeline_id = str(pipeline["id"])
            execution_dataframe = get_execution_information(fire_url, token, pipeline_id)
            total_reporter_dataframe = pd.concat([total_reporter_dataframe, execution_dataframe], ignore_index=True)
        export_name = "PROJECT_" + project_id + "_EXECUTION_RESULTS_" + datetime.now().strftime(
            "%Y-%m-%d at %H:%M:%S") + ".csv"
        print("CREATING " + export_name)
        total_reporter_dataframe.to_csv(export_name)
        print("CREATED " + export_name)
        if (summary):
            print("CREATING " + "PROJECT_" + project_id + "_LONGEST_LATENCY_BY_WORKFLOW_" + datetime.now().strftime(
                "%Y-%m-%d at %H:%M:%S") + ".csv")
            get_longest_latency(total_reporter_dataframe, project_id)
            print("CREATED " + "PROJECT_" + project_id + "_LONGEST_LATENCY_BY_WORKFLOW_" + datetime.now().strftime(
                "%Y-%m-%d at %H:%M:%S") + ".csv")
            print("CREATING " + "PROJECT_" + project_id + "_STATUS_COUNT_" + datetime.now().strftime(
                "%Y-%m-%d at %H:%M:%S") + ".csv")
            get_status_count(total_reporter_dataframe, project_id)
            print("CREATED " + "PROJECT_" + project_id + "_STATUS_COUNT_" + datetime.now().strftime(
                "%Y-%m-%d at %H:%M:%S") + ".csv")
            print("CREATING " + "PROJECT_" + project_id + "_OLDEST_EXECUTIONS" + datetime.now().strftime(
                "%Y-%m-%d at %H:%M:%S") + ".csv")
            get_oldest_executions(total_reporter_dataframe, project_id)
            print("CREATED " + "PROJECT_" + project_id + "_OLDEST_EXECUTIONS" + datetime.now().strftime(
                "%Y-%m-%d at %H:%M:%S") + ".csv")


def get_longest_latency(total_reporter_dataframe, project_id):
    pipeline_dataframe = total_reporter_dataframe.groupby(["pipelineId", "pipeline_name"])[
        "execution_time"].mean().sort_values(ascending=False)
    export_name = "PROJECT_" + project_id + "_LONGEST_LATENCY_BY_WORKFLOW_" + datetime.now().strftime(
        "%Y-%m-%d at %H:%M:%S") + ".csv"
    pipeline_dataframe.to_csv(export_name)


def get_status_count(total_reporter_dataframe, project_id):
    pipeline_dataframe = total_reporter_dataframe.groupby(["pipelineId", "pipeline_name", "status"])[
        "status"].count()
    export_name = "PROJECT_" + project_id + "_STATUS_COUNT_" + datetime.now().strftime(
        "%Y-%m-%d at %H:%M:%S") + ".csv"
    pipeline_dataframe.to_csv(export_name)


def get_oldest_executions(total_reporter_dataframe, project_id):
    pipeline_dataframe = total_reporter_dataframe.groupby(['pipelineId', 'pipeline_name'])\
        ["endTime"].mean().to_frame().sort_values('endTime')
    export_name = "PROJECT_" + project_id + "_OLDEST_EXECUTIONS_" + datetime.now().strftime(
        "%Y-%m-%d at %H:%M:%S") + ".csv"
    pipeline_dataframe.to_csv(export_name)


def get_execution_information(fire_url, token, pipeline_id):
    get_execution_information_url = fire_url + "/api/v1/pipelines/execution/" + pipeline_id
    api_call_headers = {'token': token}
    status_code = requests.get(get_execution_information_url, headers=api_call_headers).status_code
    if (status_code == 200):
        get_execution_information_text = requests.get(get_execution_information_url, headers=api_call_headers).text
        get_execution_information_dict = json.loads(get_execution_information_text)
        executionDataframe = pd.DataFrame()
        execution_id = str(get_execution_information_dict["id"])
        pipelineId = str(get_execution_information_dict["pipelineId"])
        pipeline_name = get_execution_information_dict["name"]
        if(get_execution_information_dict["endTime"] is not None):
            execution_time = get_execution_information_dict["endTime"] - get_execution_information_dict["startTime"]
            endTime = datetime.fromtimestamp(get_execution_information_dict["endTime"] / 1000)
        else:
            print(execution_id)
            execution_time = time.time() - ( get_execution_information_dict["startTime"] / 1000)
            endTime = datetime.fromtimestamp(time.time())
        if (get_execution_information_dict["status"] == 0):
            status = "RUNNING"
        elif (get_execution_information_dict["status"] == 1):
            status = "STOPPED"
        elif (get_execution_information_dict["status"] == 2):
            status = "COMPLETED"
        elif (get_execution_information_dict["status"] == 3):
            status = "FAILED"
        elif (get_execution_information_dict["status"] == 4):
            status = "STARTING"
        elif (get_execution_information_dict["status"] == 5):
            status = "STOP"
        elif (get_execution_information_dict["status"] == 6):
            status = "KILLED"
        else:
            status = "INVALID STATUS"
        # print(execution_time)
        executionSeries = pd.DataFrame({
            'execution_id': [execution_id],
            'pipelineId': [pipelineId],
            'pipeline_name': [pipeline_name],
            'execution_time': [execution_time],
            'status': [status],
            'endTime': [endTime]
        })
        executionDataframe = pd.concat([executionDataframe, executionSeries], ignore_index=True)
        return executionDataframe


if __name__ == '__main__':
    args_parser = argparse.ArgumentParser(allow_abbrev=False)
    args_parser.add_argument('--fire_host_url', help='Host URL is required', type=str, required=True)
    args_parser.add_argument('--access_token', help='Access Token is required', type=str, required=True)
    args_parser.add_argument('--project_id', help='ID of project', type=str, required=True)
    args_parser.add_argument('--summary', help='True or False to get the summary metrics of project', type=bool,
                             required=True)
    args = args_parser.parse_args()
    fire_host_url = args.fire_host_url
    access_token = args.access_token
    project_ids = args.project_id
    summary = args.summary
    args = args_parser.parse_args()
    get_pipeline_information(fire_url=fire_host_url, token=access_token, project_id=project_ids, summary=summary)
