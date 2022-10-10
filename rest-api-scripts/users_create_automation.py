import json
import requests
import argparse

'''
**********CREATE USERS******************

python users_create_automation.py --fire_host_url="https://localhost:8080" --access_token="cacaksncaskjuuonn777-cdck" --users_file_path="new_users_file_path"

Users file content format:
<username>,<password>,<first_name>,<last_name>,<email>,<role_ids>,<group_ids>,<is_superuser>,<is_active>
ex: test,test@123,test,test,test@**.com,role1|role2,group1|group1,true or false, true or false

Multiple role and group ids separated with pipe.   

***********************************
'''

# create update user
def create_update_user(fire_host, token, user_name, pwd, first_name, last_name, user_email,
                       user_roles, user_groups, is_superuser, is_active):

    print("Inside the create_update_user:: user_name: "+user_name)

    create_update_user_api_url = fire_host + "/api/v1/users"

    api_call_headers = {'token': token}

    create_update_user_body = "{\"username\": \"" + user_name + "\",\"password\":\"" + pwd \
                              + "\",\"firstName\":\"" + first_name + "\",\"lastName\":\"" + last_name + "\",\"roles\":" \
                              + user_roles + ",\"groups\":" + user_groups + ",\"email\":\"" + user_email \
                              + "\",\"isSuperuser\": \""+ is_superuser+ "\",\"isActive\":\""+is_active+"\"} "
    print("create_update_user_body:" + create_update_user_body)

    create_update_user_api_body = json.loads(create_update_user_body)

    create_update_user_api_call_response = requests.post(create_update_user_api_url, json=create_update_user_api_body,
                                                         headers=api_call_headers)

    if create_update_user_api_call_response.status_code == 200:

        print("create user response: " + create_update_user_api_call_response.text)
        print("username: "+username+" created successfully")

    else:
        print("Error in create user api: " + create_update_user_api_call_response.reason)
        print(create_update_user_api_call_response.status_code)
        print(create_update_user_api_call_response.text)


if __name__ == '__main__':

    my_parser = argparse.ArgumentParser(allow_abbrev=False)
    my_parser.add_argument('--fire_host_url', help='Host URL is required', type=str, required=True)
    my_parser.add_argument('--access_token', help='Access Token is required', type=str, required=True)
    my_parser.add_argument('--users_file_path', help='Users file path', type=str, required=True)
   
    args = my_parser.parse_args()

    fire_host_url = args.fire_host_url
    access_token = args.access_token
    users_file_path = args.users_file_path
    
    print("fire_host_url: "+fire_host_url)
    print("access_token: "+access_token)
    print("users_file_path: "+users_file_path)
        
    f = open(users_file_path, "r")
    for line in f:
        user_details = str(line).strip().split(",")

        if len(user_details) != 9:
            print("Some Information to create the below user is missing:")
            print(line)
            print("Required information: <username>,<password>,<first_name>,<last_name>,<email>,<role_ids>,<group_ids>,<is_superuser>,<is_active>")

        else:

            username = user_details[0]
            password = user_details[1]
            first_name = user_details[2]
            last_name = user_details[3]
            email = user_details[4]
            role_ids =  "["+(",".join(user_details[5].split("|")))+"]"
            group_ids = "["+(",".join(user_details[6].split("|")))+"]"
            is_superuser = user_details[7]
            is_active = user_details[8]

            create_update_user(fire_host = fire_host_url, token = access_token, user_name = username, pwd = password,
                                   first_name = first_name, last_name = last_name, user_email = email,
                       user_roles = role_ids, user_groups = group_ids, is_superuser = is_superuser, is_active = is_active)

    f.close()
