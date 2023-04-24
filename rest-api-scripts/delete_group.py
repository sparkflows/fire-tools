import argparse
import requests

'''
**********DELETE GROUP******************
python delete_group.py --fire_host_url="http://localhost:8080" --access_token="cacaksncaskjuuonn777-cdck" --group_id=1
***********************************
'''

def delete_group(fire_host, token, grp_id):
   delete_group_api_url = fire_host + "/deleteGroup/" + str(grp_id)
   api_call_headers = {'token': token}
   delete_group_api_call_response = requests.delete(delete_group_api_url,headers=api_call_headers)
   if delete_group_api_call_response.status_code == 200 or 201:
        print("deleted group successfully")
   else:
        print("Error in delete group api: " + delete_group_api_call_response.reason)


if __name__ == '__main__':
    args_parser = argparse.ArgumentParser(allow_abbrev=False)

    args_parser.add_argument('--fire_host_url', help='Host URL is required', type=str, required=True)
    args_parser.add_argument('--access_token', help='Access Token is required', type=str, required=True)
    args_parser.add_argument('--group_id', help='Group Id is required', type=int, required=True)
    args = args_parser.parse_args()

    fire_host_url = args.fire_host_url
    access_token = args.access_token
    group_id = args.group_id

    delete_group(fire_host_url, access_token, group_id)
