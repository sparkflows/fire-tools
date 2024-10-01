import requests
import json
import pandas as pd
import argparse

# Main code for processing users and making API requests
if __name__ == '__main__':
    # Command-line argument parsing
    my_parser = argparse.ArgumentParser(allow_abbrev=False)
    my_parser.add_argument('--fire_host_url', help='Host URL is required', type=str, required=True)
    my_parser.add_argument('--access_token', help='Access Token is required', type=str, required=True)
    my_parser.add_argument('--users_file_path', help='Users file path', type=str, required=True)

    args = my_parser.parse_args()

    fire_host_url = args.fire_host_url
    access_token = args.access_token
    users_file_path = args.users_file_path

    print("fire_host_url:", fire_host_url)
    print("access_token:", access_token)
    print("users_file_path:", users_file_path)

    # API URLs
    update_user_url = f"{fire_host_url}/api/v1/users/profile"

    headers = {
        'token': access_token,
        'Content-Type': 'application/json'
    }

    # Read users from CSV using pandas
    users_df = pd.read_csv(users_file_path)

    # Ensure the file has all required columns
    required_columns = ['username', 'email']
    if not all(col in users_df.columns for col in required_columns):
        print(f"Missing required columns in the file: {users_file_path}")
        print(f"Required columns: {required_columns}")
    else:
        for _, row in users_df.iterrows():
            username = row['username']
            email_update = row['email']

            # Prepare the payload for the update API
            payload = {
                "email": email_update
            }

            # Call the update user profile API
            update_response = requests.put(update_user_url, headers=headers, params={'username': username}, json=payload)

            if update_response.status_code == 200:
                print(f"{update_response.text}")
            else:
                print(f"Failed to update profile for user '{username}': {update_response.status_code} {update_response.text}")
