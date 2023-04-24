import argparse
import json

import requests


'''
**********CREATE GROUP******************
python create_group.py --fire_host_url="https://localhost:8080" --access_token="cacaksncaskjuuonn777-cdck" --group_name="testGroup"
***********************************
'''

def add_group(fire_host, token, grp_name):
    group_create_api_url = fire_host + "/api/v1/groups"

    api_call_headers = {'token': token}

    create_group_body = "{\"name\": \"" + grp_name + "\"}"
    print("create_group_body:" + create_group_body)
    create_group_api_body = json.loads(create_group_body)

    create_group_api_call_response = requests.post(group_create_api_url, json=create_group_api_body,
                                                   headers=api_call_headers)

    if create_group_api_call_response.status_code == 200 or 201:
        print("create group response: " + create_group_api_call_response.text)
    else:
        print("Error in create group api: " + create_group_api_call_response.reason)
        print(create_group_api_call_response.status_code)
        print(create_group_api_call_response.text)


if __name__ == '__main__':
    args_parser = argparse.ArgumentParser(allow_abbrev=False)

    args_parser.add_argument('--fire_host_url', help='Host URL is required', type=str, required=True)
    args_parser.add_argument('--access_token', help='Access Token is required', type=str, required=True)
    args_parser.add_argument('--group_name', help='Group Name is required', type=str, required=True)
    args = args_parser.parse_args()

    fire_host_url = args.fire_host_url
    access_token = args.access_token
    group_name = args.group_name

    add_group(fire_host_url, access_token, group_name)
