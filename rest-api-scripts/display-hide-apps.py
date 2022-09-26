import requests
import json
import sys
import csv

hide_app_ids = []
show_app_ids = []

def get_all_user_owned_and_shared_project(token: str, fire_host: str):
    get_projects_api_url = fire_host + "/api/v1/projects/users/logged-in"

    api_call_headers = {'token': token}

    get_projects_api_call_response = requests.get(get_projects_api_url, headers=api_call_headers)

    if get_projects_api_call_response.status_code == 200:

        print("get project list api response: " + get_projects_api_call_response.text)

    else:
        print("Error in get project list api: " + get_projects_api_call_response.text)

    project_list = get_projects_api_call_response.text

    return project_list

def get_all_groups(token: str, fire_host: str):
    get_groups_api_url = fire_host + "/api/v1/groups"

    api_call_headers = {'token': token}

    get_groups_api_call_response = requests.get(get_groups_api_url, headers=api_call_headers)

    if get_groups_api_call_response.status_code == 200:

        print("get group list api response: " + get_groups_api_call_response.text)

    else:
        print("Error in get group list api: " + get_groups_api_call_response.text)

    group_list = get_groups_api_call_response.text
    groups = json.loads(group_list)
    return groups[0]

def get_group_by_name(groups:any,group_name:str):
    for i in range(0, len(groups)):
        group_json = groups[i]
        if (group_json['name'] is not None) and (group_json['name'] == group_name):
            return group_json['id']


def check_project_shared(token: str, fire_host: str,project_list:any,group_id:any,use_case:str):
    projects = json.loads(project_list)
    for i in range(0, len(projects)):
        project_json = projects[i]
        if (project_json['sharedGroups'] is not None) and (group_id in project_json['sharedGroups']):
            show_hide_apps(token,fire_host,project_json["id"],use_case)

def get_project_apps(token: str, fire_host: str,project_id:any):
    get_project_apps_api_url = fire_host + "/api/v1/webApps"

    api_call_headers = {'token': token}

    PARAMS = {'projectId': project_id, 'apiCategory':"list",'sortBy':['category','name']}

    get_project_apps_api_call_response = requests.get(get_project_apps_api_url,params = PARAMS, headers=api_call_headers)

    if get_project_apps_api_call_response.status_code == 200:

        print("get project app list api response: " + get_project_apps_api_call_response.text)

    else:
        print("Error in get project app list api: " + get_project_apps_api_call_response.text)

    app_list = get_project_apps_api_call_response.text

    return app_list

def show_hide_apps(token: str, fire_host: str,project_id:any,use_case:str):
    app_list = get_project_apps(token,fire_host,project_id)
    apps = json.loads(app_list)
    for i in range(0, len(apps)):
        app_json = apps[i]
        if (app_json['usecase'] is not None) and (use_case in app_json['usecase'].split(",")):
            show_app_ids.append(app_json['id'])
        else:
            hide_app_ids.append(app_json['id'])

def get_list_of_apps(token: str, fire_host: str,yaml_file_path:str,projects:any,groups:any):

    with open(yaml_file_path, mode='r') as file:
        # reading the CSV file
        csvFile = csv.reader(file)
        i = 0
        # displaying the contents of the CSV file
        for lines in csvFile:
            if i==0:
                instanceNameIndex = lines.index("instance_name")
                groupIndex = lines.index("fire_group_name")
                i = i+1
            else:
               use_case = lines[instanceNameIndex]
               group_name = lines[groupIndex]
               group_id = get_group_by_name(groups,group_name)
               check_project_shared(token,fire_host,projects,group_id,use_case)


# display hide project apps project
def display_hide_project_apps(token: str, fire_host: str, yaml_config_file_path: str):
    project_list = get_all_user_owned_and_shared_project(token,fire_host)
    group_list = get_all_groups(token,fire_host)
    get_list_of_apps(token,fire_host,yaml_config_file_path,project_list,group_list)
    show_hide_app_list(token,fire_host)

def show_hide_app_list(token: str, fire_host: str):
    response = [{"status": "hide", "appIds": hide_app_ids}, {"status": "show", "appIds": show_app_ids}]
    print(response)
    get_project_apps_api_url = fire_host + "/api/v1/webApps/showHideApps"

    api_call_headers = {'token': token}

    get_project_apps_api_call_response = requests.post(get_project_apps_api_url,json = response, headers=api_call_headers)

    if get_project_apps_api_call_response.status_code == 200:

        print("get project app list api response: " + get_project_apps_api_call_response.text)

    else:
        print("Error in get project app list api: " + get_project_apps_api_call_response.text)

    app_list = get_project_apps_api_call_response.text

    return app_list

if __name__ == '__main__':
    print(len(sys.argv))
    if len(sys.argv) != 4:
        print("Usage: display-hide-apps.py <fire_host_url> <access_token> <file_path>")
        exit()

    fire_host_url = sys.argv[1]
    access_token = sys.argv[2]
    file_path = sys.argv[3]

    display_hide_project_apps(access_token,fire_host_url,file_path)