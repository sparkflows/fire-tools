import argparse
from zipfile import ZipFile
import requests
import json


'''
**********EXPORT PROJECTS******************
python export_project.py --fire_host_url="https://localhost:8080" --access_token="cacaksncaskjuuonn777-cdck" --project_ids="1|3"

In project_ids, pass the pipeseparated prject id.
***********************************

'''


def export_project(fire_host, token, project_id_list):
    zipObj = ZipFile('Projects.zip', 'w')
    for project_id in project_id_list:
        project_name = get_project_details(fire_host,token,project_id,zipObj)
        get_workflow_details_by_proj_id(fire_host,token,project_id,project_name,zipObj)
        get_app_details_by_proj_id(fire_host,token,project_id,project_name,zipObj)
        get_pipeline_details_by_proj_id(fire_host,token,project_id,project_name,zipObj)
    zipObj.close();

def get_project_details(fire_host, token, project_id,zipObj):
    project_details_api_url = fire_host + "/api/v1/projects/"+project_id

    api_call_headers = {'token': token}

    project_details_api_call_response = requests.get(project_details_api_url, headers=api_call_headers)
    if project_details_api_call_response.status_code == 200:

        project_detail = json.loads(project_details_api_call_response.text);
        projectMetaFileName = 'Projects' + '/' + project_detail['name'] + '/' + 'project' + '.json';
        project_meta_data = {
            "Id": project_detail['id'],
            "name": project_detail['name'],
            "tag": project_detail['tag'],
            "description": project_detail['description'],
            "createdBy": project_detail['createdBy']
        }
        # Serializing json
        project_meta_data_json_object = json.dumps(project_meta_data)
        zipObj.open(projectMetaFileName,"w").write(project_meta_data_json_object.encode("utf-8"))

    else:
        print("Error in get user list api: " + project_details_api_call_response.text)

    return project_detail['name']

def get_workflow_details_by_proj_id(fire_host, token, project_id,project_name,zipObj):
    workflow_list_to_export_api_url = fire_host + "/api/v1/workflows/list/export?projectId=" + project_id

    api_call_headers = {'token': token}

    workflow_list_to_export_api_call_response = requests.get(workflow_list_to_export_api_url, headers=api_call_headers)
    if workflow_list_to_export_api_call_response.status_code == 200:
        for workflow_detail in json.loads(workflow_list_to_export_api_call_response.text):
            wf_dict = json.loads(workflow_detail);
            wfFileName = 'Projects' + '/'  + project_name + '/' +  'workflows/' + wf_dict['name'].replace(" ","") + '.json';
            # Serializing json
            wf_data_json_object = json.dumps(wf_dict, indent = 1)
            zipObj.open(wfFileName,"w").write(wf_data_json_object.encode("utf-8"))

    else:
        print("Error in get workflow list api: " + workflow_list_to_export_api_call_response.text)



def get_dataset_details_by_proj_id(fire_host, token, project_id,project_name,zipObj):
    dataset_list_to_export_api_url = fire_host + "/api/v1/datasets/list/export?projectId=" + project_id

    api_call_headers = {'token': token}

    dataset_list_to_export_api_call_response = requests.get(dataset_list_to_export_api_url, headers=api_call_headers)
    if dataset_list_to_export_api_call_response.status_code == 200:
        for dataset_detail in json.loads(dataset_list_to_export_api_call_response.text):
            dataset_dict = json.loads(dataset_detail);
            datasetFileName = 'Projects' + '/' + project_name + '/' + 'datasets/' + wf_dict['name'].replace(" ","")+"_"+str(wf_dict['id']) + '.json';
            # Serializing json
            dataset_data_json_object = json.dumps(dataset_dict, indent = 1)
            zipObj.open(datasetFileName, "w").write(dataset_data_json_object.encode("utf-8"))

    else:
        print("Error in get dataset list api: " + dataset_list_to_export_api_call_response.text)


def get_app_details_by_proj_id(fire_host, token, project_id,project_name,zipObj):
    app_list_to_export_api_url = fire_host + "/api/v1/webApps?sortBy=category,name&projectId="+project_id+"&apiCategory=details"

    api_call_headers = {'token': token}

    app_list_to_export_api_call_response = requests.get(app_list_to_export_api_url, headers=api_call_headers)
    if app_list_to_export_api_call_response.status_code == 200:
        for app_detail in json.loads(app_list_to_export_api_call_response.text):
            app_dict = app_detail;
            appFileName = 'Projects' + '/' + project_name + '/' + 'analytics_app/' + app_dict['name'].replace(" ","")+"_"+str(app_dict['id']) + '.json';
            # Serializing json
            app_data_json_object = json.dumps(app_dict, indent = 1)
            zipObj.open(appFileName, "w").write(app_data_json_object.encode("utf-8"))

    else:
        print("Error in get app list api: " + app_list_to_export_api_call_response.text)


def get_pipeline_details_by_proj_id(fire_host, token, project_id,project_name,zipObj):
    pipeline_list_to_export_api_url = fire_host + "/getExportPipelinesDetailsByProjectId/" + project_id

    api_call_headers = {'token': token}

    pipeline_list_to_export_api_call_response = requests.get(pipeline_list_to_export_api_url, headers=api_call_headers)
    if pipeline_list_to_export_api_call_response.status_code == 200:
        for pipeline_detail in json.loads(pipeline_list_to_export_api_call_response.text):
            pipeline_dict = pipeline_detail;
            pipelineFileName = 'Projects' + '/' + project_name + '/' + 'pipelines/' + pipeline_dict['name'].replace(" ","")+"_"+str(pipeline_dict['id']) + '.json';
            # Serializing json
            pipeline_data_json_object = json.dumps(pipeline_dict['content'], indent = 1)
            zipObj.open(pipelineFileName, "w").write(pipeline_data_json_object.encode("utf-8"))

    else:
        print("Error in get pipeline list api: " + pipeline_list_to_export_api_call_response.text)

if __name__ == '__main__':
    args_parser = argparse.ArgumentParser(allow_abbrev=False)
    args_parser.add_argument('--fire_host_url', help='Host URL is required', type=str, required=True)
    args_parser.add_argument('--access_token', help='Access Token is required', type=str, required=True)
    args_parser.add_argument('--project_ids', help='Pipe Separated project ids', type=str, required=True)
    args = args_parser.parse_args()

    fire_host_url = args.fire_host_url
    access_token = args.access_token
    project_ids = args.project_ids
    print("fire_host_url: " + fire_host_url)
    print("access_token: " + access_token)
    print("project_ids: " + project_ids)

    export_project(fire_host=fire_host_url, token=access_token, project_id_list=project_ids.split('|'))
