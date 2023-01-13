import argparse
import pandas as pd
from datetime import datetime
import asyncio
import aiohttp
import time

'''
************Async Workflow Metric Reporter************
----------------------
Script: async_workflow_metric_reporter.py
This script will export a csv file containing the latency and status of all workflow executions of a specified project_id. The summary argument is a Boolean, if set to True additional metrics will be exported (longest_latency, status_count, oldest executions).
command:  
   python async_workflow_metric_reporter.py --fire_host_url="https://localhost:8080" --access_token="cacaksncaskjuuonn777-cdck" --project_id="1" --summary=True  

   The command above will create 3 csv files containing information regarding project 1. One general csv file containing all executions, one csv file containing the average latency of each workflow, one containing the workflows sorted by exeuction time, and one csv file containing the execution status count for each workflow. 

   python async_workflow_metric_reporter.py --fire_host_url="https://localhost:8080" --access_token="cacaksncaskjuuonn777-cdck" --project_id="1" --summary=False

   The command above will create 1 csv file containing information regarding project 1. One general csv file containing all workflow executions. 
----------------------
*************************************************
'''


async def get_information(fire_url, session, type):
    async with session.get(fire_url) as response:
        if type == "workflow":
            status_code = response.status
            if status_code == 200:
                return await response.json()
            else:
                return await status_code
        elif (type == "execution"):
            status_code = response.status
            executionDataframe = pd.DataFrame()
            if (status_code == 200):
                get_execution_information_dict = await response.json()
                for execution in get_execution_information_dict:
                    execution_id = str(execution["id"])
                    analysisFlowId = str(execution["analysisFlowId"])
                    workflow_name = execution["name"]
                    execution_time = execution["endTime"] - execution["startTime"]
                    endTime = datetime.fromtimestamp(execution["endTime"] / 1000)
                    if (execution["status"] == 0):
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
                    # print(execution_time)
                    executionSeries = pd.DataFrame({
                        'execution_id': [execution_id],
                        'analysisFlowId': [analysisFlowId],
                        'workflow_name': [workflow_name],
                        'execution_time': [execution_time],
                        'status': [status],
                        'endTime': [endTime]
                    })
                    executionDataframe = pd.concat([executionDataframe, executionSeries], ignore_index=True)
                return executionDataframe
            else:
                return executionDataframe


async def write_information(fire_url, token, project_id, summary):
    get_workflow_information_url = fire_url + "/api/v1/workflows?projectId=" + project_id
    api_call_headers = {'token': token}
    async with aiohttp.ClientSession(headers=api_call_headers) as session:
        get_workflow_information_dict = await get_information(get_workflow_information_url, session, type="workflow")
        total_reporter_dataframe = pd.DataFrame()
        for workflow in get_workflow_information_dict:
            workflow_id = str(workflow["id"])
            get_execution_information_url = fire_url + "/api/v1/workflow-executions/workflows/" + workflow_id
            execution_dataframe = await get_information(get_execution_information_url, session, type="execution")
            total_reporter_dataframe = pd.concat([total_reporter_dataframe, execution_dataframe], ignore_index=True)
        export_name = "PROJECT_" + project_id + "_EXECUTION_RESULTS_" + datetime.now().strftime(
            "%Y-%m-%d at %H:%M:%S") + ".csv"
        print("CREATING " + export_name)
        total_reporter_dataframe.to_csv(export_name)
        print("CREATED " + export_name)
        if (summary):
            latency_name = "PROJECT_" + project_id + "_LONGEST_LATENCY_BY_WORKFLOW_" + datetime.now().strftime(
                "%Y-%m-%d at %H:%M:%S") + ".csv"
            status_count_name = "PROJECT_" + project_id + "_STATUS_COUNT_" + datetime.now().strftime(
                "%Y-%m-%d at %H:%M:%S") + ".csv"
            oldest_executions_name = "PROJECT_" + project_id + "_OLDEST_EXECUTIONS_" + datetime.now().strftime(
                "%Y-%m-%d at %H:%M:%S") + ".csv"
            print("CREATING " + "PROJECT_" + project_id + "_LONGEST_LATENCY_BY_WORKFLOW_" + datetime.now().strftime(
                "%Y-%m-%d at %H:%M:%S") + ".csv")
            total_reporter_dataframe.groupby(["analysisFlowId", "workflow_name"])[
                "execution_time"].mean().sort_values(ascending=False).to_csv(latency_name)
            print("CREATED " + "PROJECT_" + project_id + "_LONGEST_LATENCY_BY_WORKFLOW_" + datetime.now().strftime(
                "%Y-%m-%d at %H:%M:%S") + ".csv")
            print("CREATING " + "PROJECT_" + project_id + "_STATUS_COUNT_" + datetime.now().strftime(
                "%Y-%m-%d at %H:%M:%S") + ".csv")
            total_reporter_dataframe.groupby(["analysisFlowId", "workflow_name", "status"])[
                "status"].count().to_csv(status_count_name)
            print("CREATED " + "PROJECT_" + project_id + "_STATUS_COUNT_" + datetime.now().strftime(
                "%Y-%m-%d at %H:%M:%S") + ".csv")
            print("CREATING " + "PROJECT_" + project_id + "_OLDEST_EXECUTIONS" + datetime.now().strftime(
                "%Y-%m-%d at %H:%M:%S") + ".csv")
            total_reporter_dataframe.groupby(['analysisFlowId', 'workflow_name']) \
                ["endTime"].mean().to_frame().sort_values('endTime').to_csv(oldest_executions_name)
            print("CREATED " + "PROJECT_" + project_id + "_OLDEST_EXECUTIONS" + datetime.now().strftime(
                "%Y-%m-%d at %H:%M:%S") + ".csv")


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
    start = time.time()
    asyncio.run(write_information(fire_host_url, access_token, project_ids, summary))
    time_elapsed = time.time() - start
    print("total time elapsed is " + str(time_elapsed))
