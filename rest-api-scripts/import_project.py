import requests
import json
import sys
import argparse


# import project
#**********COMMAND******************
#python import_project.py --fire_host_url="https://localhost:8080" --access_token="cacaksncaskjuuonn777-cdck" --project_zip_path="/home/user/projects/Projects_133535.zip" --project_id=42 --selected_project_name="pipeline-test"
#***********************************
def import_project(token: str, fire_host: str, file_path: str, proj_id,project_name: str):
    import_project_api_url = fire_host + "/api/v1/projects/import"


    api_call_headers= {'token': token , 'projectId':proj_id,'selectedProjectName':project_name}

    files = {
        'file': (file_path, open(file_path, 'rb'))
    }

    import_project_api_call_response = requests.post(import_project_api_url, headers=api_call_headers, files=files,verify=False)

    if import_project_api_call_response.status_code == 200:

        print("import project response: ")
        dict = json.loads(import_project_api_call_response.text)
        for key in dict:
            print( "Number of "+key+" imported", '->', dict[key])

    else:
        if import_project_api_call_response.text.find("JWT signature does not match locally computed signature")  != -1 or import_project_api_call_response.text.find("Access Denied")  != -1:
            print("Access Token added is not valid.")
        else:
            print("Error in import project api: " + import_project_api_call_response.text)


if __name__ == '__main__':

    my_parser = argparse.ArgumentParser(allow_abbrev=False)
    my_parser.add_argument('--fire_host_url', help='Host URL is required', type=str, required=True)
    my_parser.add_argument('--access_token', help='Access Token is required', type=str, required=True)
    my_parser.add_argument('--project_zip_path', help='Project Zip path is required', type=str, required=True)
    my_parser.add_argument('--project_id', help='Project Id is required', type=str,required = True)
    my_parser.add_argument('--selected_project_name', help='Project name is required', type=str, required=True)
    args = my_parser.parse_args()

    fire_host_url = args.fire_host_url
    access_token = args.access_token
    project_zip_path = args.project_zip_path
    project_id = args.project_id
    selected_project_name = args.selected_project_name

    print("fire_host_url: "+fire_host_url)
    print("access_token: "+access_token)
    print("project_zip_path: "+project_zip_path)
    print("project_id: "+project_id)
    print("selected_project_name: "+selected_project_name)

    try:
        import_project(access_token, fire_host_url, project_zip_path, project_id,selected_project_name)
    except Exception as e:
        if str(e).find("Connection refused") != -1 or str(e).lower().find("connection") != -1:
            print("Host Url is not valid. Please recheck and add proper host url.")
        else :
            print(str(e))
