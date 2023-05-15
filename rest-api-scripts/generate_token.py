import argparse
import requests
import json
from datetime import datetime
from datetime import timedelta
import time

'''
************Generate token************
----------------------
Script: generate_token.py
command:  
   python generate_token.py --fire_host_url="https://localhost:8080" --access_token="cacaksncaskjuuonn777-cdck" --expiration_duration=60"

   This command executes to generate the access token

----------------------
*************************************************
'''

def generate_token(fire_host, token, duration):
    generate_token_api_url = fire_host + "/api/v1/tokens"
    api_call_headers = {'token': token}
    currentDate = datetime.now()
    formattedDate = currentDate.date() + timedelta(days=duration)
    formattedDateTime = currentDate.replace(day=formattedDate.day, month=formattedDate.month, year=formattedDate.year,hour=currentDate.hour,minute=currentDate.minute,second=currentDate.second)
    unix_time = time.mktime(formattedDateTime.timetuple())*1000
    generate_token_body = "{\"expiredDuration\": \"" + str(int(unix_time)) + "\"} "
    print("generate_token_body:" + generate_token_body)

    generate_token_api_body = json.loads(generate_token_body)

    generate_token_api_call_response = requests.post(generate_token_api_url, json=generate_token_api_body,
                                                         headers=api_call_headers)

    if generate_token_api_call_response.status_code == 200 or generate_token_api_call_response.status_code == 201:
        response_dict = json.loads(generate_token_api_call_response.text)
        return response_dict['accessToken']
    else:
        print("Error in generating token api: " + generate_token_api_call_response.text)

if __name__ == '__main__':
    args_parser = argparse.ArgumentParser(allow_abbrev=False)
    args_parser.add_argument('--fire_host_url', help='Host URL is required', type=str, required=True)
    args_parser.add_argument('--access_token', help='Access Token is required', type=str, required=True)
    args_parser.add_argument('--expiration_duration', help='Token Expiration Duration(in days) is required', type=int, required=True)
    args = args_parser.parse_args()

    fire_host_url = args.fire_host_url
    access_token = args.access_token
    expiration_duration = args.expiration_duration
    print("fire_host_url: " + fire_host_url)
    print("access_token: " + access_token)
    print("expiration_duration: " + str(expiration_duration))

    access_token_value = generate_token(fire_host=fire_host_url, token=access_token, duration=expiration_duration)
    print("Generated Token "+access_token_value)
