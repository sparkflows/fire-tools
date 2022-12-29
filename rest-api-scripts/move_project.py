import argparse
import json
import export_project
import import_project

'''
************Move_Project.py************
----------------------
Script: move_project.py
This script will move a project from one instance of fire to another instance of fire.
    python move_project.py --starting_instance="https://localhost:8080" --starting_token="cacaksncaskjuuonn777-cdck" --ending_instance="https://1.2.3.4:8080" --ending_token="dadadadasdfas7777-fdsdf" --project_id="1"   
    
    The command above will export project 1 from the starting instance and import it to the ending instance
----------------------
*************************************************
'''

def move_project(starting_instance, starting_token, ending_instance, ending_token, project_ids, project_name):
    export_project.export_project(starting_instance, starting_token, project_ids)
    project_zip = 'Projects.zip'
    project = import_project.create_project(ending_token, ending_instance, project_name)
    dict = json.loads(project)
    id = str(dict['id'])
    import_project.import_project(ending_token,ending_instance, project_zip, id, project_name)

if __name__ == '__main__':
    args_parser = argparse.ArgumentParser(allow_abbrev=False)
    args_parser.add_argument('--starting_instance', help='Starting Instance URl', type=str, required=True)
    args_parser.add_argument('--starting_token', help='Access Token of Starting Instance', type=str, required=True)
    args_parser.add_argument('--ending_instance', help='Ending Instance URL', type=str, required=True)
    args_parser.add_argument('--ending_token', help='Access Token of End Instance', type=str,
                             required=True)
    args_parser.add_argument('--project_ids',help='pipe separated project ids', type=str,
                             required=True)
    args_parser.add_argument('--project_name', help='name of project', type=str, required=True)
    args = args_parser.parse_args()
    starting_instance = args.starting_instance
    starting_token = args.starting_token
    ending_instance = args.ending_instance
    ending_token = args.ending_token
    project_ids = args.project_ids
    project_name = args.project_name
    move_project(starting_instance=starting_instance, starting_token=starting_token, ending_instance=ending_instance, ending_token=ending_token, project_ids=project_ids.split('|'), project_name=project_name)

