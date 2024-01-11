import argparse
import requests
import json

'''
************Execute Update ConnectionID************
----------------------
Script: update_user_connectionid.py
command:
   python update_user_connectionid.py --fire_host_url="https://localhost:8080" --access_token="cacaksncaskjuuonn777-cdck" --connection_id=1"



----------------------
*************************************************
'''


def update_user_connectionid(fire_host, token, connection_id):
    update_user_connectionid_url = (fire_host + "/api/v1/user/currentConnection/"+str(connection_id))
    api_call_headers = {
        "token": token
    }
    data = {
    }
    update_user_connectionid_response = requests.put(update_user_connectionid_url, json=data, headers=api_call_headers)
    print(update_user_connectionid_response.status_code)
    print(update_user_connectionid_response.text)

    if update_user_connectionid_response.status_code == 200:
      print(update_user_connectionid_response.text)


if __name__ == '__main__':
    args_parser = argparse.ArgumentParser(allow_abbrev=False)
    args_parser.add_argument('--fire_host_url', help='Host URL is required', type=str, required=True)
    args_parser.add_argument('--access_token', help='Access Token is required', type=str, required=True)
    args_parser.add_argument('--connection_id', help='Connection id is required', type=int, required=True)
    args = args_parser.parse_args()

    fire_host_url = args.fire_host_url
    access_token = args.access_token
    connection_id = args.connection_id
    print("fire_host_url: " + fire_host_url)
    print("access_token: " + access_token)
    print("connection_id: "+str(connection_id))

    update_user_connectionid(fire_host_url, access_token, connection_id)
