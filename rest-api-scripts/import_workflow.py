import requests
import json
import sys
import argparse


# import workflow
#**********COMMAND******************
#python import_workflow.py --fire_host_url="https://localhost:8080" --access_token="token123" --workflow_zip_path="Workflow_123.zip" --project_id="456" --uuid_option="createNewUUID"
#***********************************
def import_workflow(token: str, fire_host: str, file_path: str, proj_id: str, uuid_option: str):
    import_wf_api_url = fire_host + "/api/v1/workflows/import"

    api_call_headers = {'token': token, 'projectId': proj_id, 'uuidOption': uuid_option}

    files = {
        'file': (file_path, open(file_path, 'rb'))
    }

    import_wf_api_call_response = requests.post(import_wf_api_url, headers=api_call_headers, files=files, verify=False)

    if import_wf_api_call_response.status_code == 200:
        print("import workflow response: ")
        dict = json.loads(import_wf_api_call_response.text)
        for key in dict:
            print("Number of " + key + " imported", '->', dict[key])
    else:
        if import_wf_api_call_response.text.find("JWT signature does not match locally computed signature") != -1 or import_wf_api_call_response.text.find("Access Denied") != -1:
            print("Access Token added is not valid.")
        else:
            print("Error in import workflow api: " + import_wf_api_call_response.text)


if __name__ == '__main__':
    my_parser = argparse.ArgumentParser(allow_abbrev=False)
    my_parser.add_argument('--fire_host_url', help='Host URL is required', type=str, required=True)
    my_parser.add_argument('--access_token', help='Access Token is required', type=str, required=True)
    my_parser.add_argument('--workflow_zip_path', help='Workflow Zip path is required', type=str, required=True)
    my_parser.add_argument('--project_id', help='Project ID is required', type=str, required=True)
    my_parser.add_argument('--uuid_option', help='UUID option (createNewUUID or createNewUUIDIfExist)', type=str, default='createNewUUID')
    args = my_parser.parse_args()

    fire_host_url = args.fire_host_url
    access_token = args.access_token
    workflow_zip_path = args.workflow_zip_path
    project_id = args.project_id
    uuid_option = args.uuid_option

    print("fire_host_url: " + fire_host_url)
    print("access_token: " + access_token)
    print("workflow_zip_path: " + workflow_zip_path)
    print("project_id: " + project_id)
    print("uuid_option: " + uuid_option)

    try:
        import_workflow(access_token, fire_host_url, workflow_zip_path, project_id, uuid_option)
    except Exception as e:
        if str(e).find("Connection refused") != -1 or str(e).lower().find("connection") != -1:
            print("Host Url is not valid. Please recheck and add proper host url.")
        else:
            print(str(e))