import requests
import json
import sys
import argparse

def get_execution_result(fire_host, token, app_execution_id):
    get_execution_result_api_url = fire_host + "/viewExecutionResult/" + str(app_execution_id) + "/0"

    api_call_headers = {'token': token}

    get_execution_result_api_call_response = requests.get(get_execution_result_api_url, headers=api_call_headers)
    if get_execution_result_api_call_response.status_code == 200:

        print("get execution result response: " + get_execution_result_api_call_response.text)

    else:
        print("Error in get execution result api: " + get_execution_result_api_call_response.text)

    return json.loads(get_execution_result_api_call_response.text)


def get_job_status(fire_host, token, exe_id):
    get_job_status_api_url = fire_host + "/api/v1/update-status-workflow-execution/{wfeId}"
    api_call_headers = {'token': token}
    get_status_api_call_response = requests.get(get_job_status_api_url.format(wfeId=exe_id),
                                                headers=api_call_headers)
    if get_status_api_call_response.status_code == 200:
        print(" Status: " + get_status_api_call_response.text)

        status = json.loads(get_status_api_call_response.text)
        if status['status'] == 0:
            print("inside loop if status is still running")
            print("Status is still running")
            print(" Status: " + get_status_api_call_response.text)
            get_job_status(fire_host, token, exe_id)

        elif status['status'] == 2:
            # write to file
            write_result_to_file(fire_host, token, status['name'],exe_id)


def write_result_to_file(fire_host, token,name, exe_id):
    results = get_execution_result(fire_host, token, exe_id)
    f = open(str(name)+".json", "w")
    for result in results:
        res = result['result']
        f.write(str(res) + "\n")
    f.close()


if __name__ == '__main__':
    args_parser = argparse.ArgumentParser(allow_abbrev=False)
    args_parser.add_argument('--fire_host_url', help='Host URL is required', type=str, required=True)
    args_parser.add_argument('--access_token', help='Access Token is required', type=str, required=True)
    args_parser.add_argument('--execution_id', help='Execution id is required', type=str, required=True)
    args = args_parser.parse_args()

    fire_host_url = args.fire_host_url
    access_token = args.access_token
    execution_id = args.execution_id

    get_job_status(fire_host_url,access_token,execution_id)