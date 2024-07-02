import requests
import json
import sys


# It takes the following parameters:
# Fire URL : http://localhost:8080

# create update user
def create_update_user(fire_host, token, user_id, user_name, pwd, first_name, last_name, user_email,
                       user_roles, user_groups):
    create_update_user_api_url = fire_host + "/api/v1/users"

    api_call_headers = {'token': token}

    create_update_user_body = "{\"username\": \"" + user_name + "\",\"id\":\"" + user_id + "\",\"password\":\"" + pwd \
                              + "\",\"firstName\":\"" + first_name + "\",\"lastName\":\"" + last_name + "\",\"roles\":" \
                              + user_roles + ",\"groups\":" + user_groups + ",\"email\":\"" + user_email \
                              + "\",\"isSuperuser\":\"false\"" + ",\"isActive\":\"true\"} "
    print("create_update_user_body:" + create_update_user_body)

    create_update_user_api_body = json.loads(create_update_user_body)

    create_update_user_api_call_response = requests.post(create_update_user_api_url, json=create_update_user_api_body,
                                                         headers=api_call_headers)

    if create_update_user_api_call_response.status_code == 200:

        print("create user response: " + create_update_user_api_call_response.text)

    else:
        print("Error in create user api: " + create_update_user_api_call_response.text)

    return create_update_user_api_call_response.text


# user list
def list_user(fire_host: str, token: str):
    list_user_api_url = fire_host + "/usersJSON"

    api_call_headers = {'token': token}

    list_user_api_call_response = requests.get(list_user_api_url, headers=api_call_headers)
    if list_user_api_call_response.status_code == 200:

        print("get user list response: " + list_user_api_call_response.text)
        write_result_to_file(json.loads(list_user_api_call_response.text))

    else:
        print("Error in get user list api: " + list_user_api_call_response.text)

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


def write_result_to_file(user_list_response):
    user_list = user_list_response[0]
    f = open("user_list.csv", "w")
    f.write("id" + ",")
    f.write("username" + ",")
    f.write("firstName" + ",")
    f.write("lastName" + ",")
    f.write("email" + ",")
    f.write("isSuperuser" + ",")
    f.write("isActive" + "\n")
    for user in user_list:
        f.write(str(user['id']) + ",")
        f.write(str(user['username']) + ",")
        f.write(str(user['firstName']) + ",")
        f.write(str(user['lastName']) + ",")
        f.write(str(user['email']) + ",")
        f.write(str(user['isSuperuser']) + ",")
        f.write(str(user['isActive']) + "\n")
    f.close()


if __name__ == '__main__':
    print(len(sys.argv))
    if len(sys.argv) == 11:
        print("Usage: user_create_automation.py <fire_host_url> <access_token> <username> <password> "
              "<firstName> <lastName> <email> <roles> <groups> <userId>")
        #Example create user: user_create_automation.py http://hosturl:8080 xyz username password firstName lastName test@gmail.com [1] [1] 0
        #Example update user with id 1: user_create_automation.py http://hosturl:8080 xyz username password firstName lastName test@gmail.com [1] [1] 1

        fire_host_url = sys.argv[1]
        access_token = sys.argv[2]
        username = sys.argv[3]
        password = sys.argv[4]
        firstName = sys.argv[5]
        lastName = sys.argv[6]
        email = sys.argv[7]
        roles = sys.argv[8]
        groups = sys.argv[9]
        userId = sys.argv[10]

        create_update_user(fire_host_url, access_token, userId, username, password, firstName, lastName, email, roles,
                           groups)

    if len(sys.argv) == 4:
        print("Usage: user_create_automation.py <fire_host_url> <access_token> <type>")
        '''
         type: user_list
               active_users_and_groups
        '''

        fire_host_url = sys.argv[1]
        access_token = sys.argv[2]
        type = sys.argv[3]

        if type == "user_list":
            list_user(fire_host_url, access_token)

        if type == "active_users_and_groups":
            active_users_and_groups(fire_host_url, access_token)
