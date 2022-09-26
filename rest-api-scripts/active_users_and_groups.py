import requests
import json
import sys


# List of active user and associated group
def active_users_and_groups(fire_host: str, token: str):
    list_user_api_url = fire_host + "/api/v1/users"

    api_call_headers = {'token': token}

    list_user_api_call_response = requests.get(list_user_api_url, headers=api_call_headers)
    print(list_user_api_call_response)
    if list_user_api_call_response.status_code == 200:
        print("get user list response: " + list_user_api_call_response.text)
        write_active_users_groups(json.loads(list_user_api_call_response.text))

    else:
        print("Error in get user list api: " + list_user_api_call_response.text)

def write_active_users_groups(data):

    users = data[0]
    groups = data[2]

    usermapping = {}

    for user in users:
        print(user)
        user_id = dict(user).get('id')
        value = dict(user).get('username') + " ," + dict(user).get('firstName') + " ," + dict(user).get(
            'lastName') + " ," + dict(user).get('email')
        is_user_active = dict(user).get('isActive')

        if is_user_active:
            user_group_info = groups[str(user_id)]

            for i in range(len(user_group_info)):
                if i == 0:
                    value = value + "," + user_group_info[i]['name']
                else:
                    value = value + ":" + user_group_info[i]['name']

            usermapping[user_id] = value

    f = open("active_users_groups.csv", "w")
    f.write("user_id, username, firstName, lastName, email, groups"+"\n")
    for user_id in usermapping:

        value = usermapping[user_id]
        f.write(str(user_id) + " ,"+ str(value) +"\n")

    f.close()


if __name__ == '__main__':
    print(len(sys.argv))

    if len(sys.argv) == 3:
        print("Usage: user_create_automation.py <fire_host_url> <access_token>")

        fire_host_url = sys.argv[1]
        access_token = sys.argv[2]

        active_users_and_groups(fire_host_url, access_token)
