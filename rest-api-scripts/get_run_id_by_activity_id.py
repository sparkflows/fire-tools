import sys
import argparse
import requests
import urllib3
from urllib3.exceptions import InsecureRequestWarning
import json

WORKFLOW_EXECUTION_API = "/api/v1/workflowExecution"

def _session_for(fire_host: str) -> requests.Session:
    s = requests.Session()
    if fire_host.lower().startswith("https://"):
        s.verify = False
        urllib3.disable_warnings(InsecureRequestWarning)
    return s

def _get_json(s: requests.Session, url: str, headers: dict, timeout: int = 30):
    try:
        r = s.get(url, headers=headers, timeout=timeout)
    except requests.RequestException as e:
        return False, f"Network error calling {url}: {e}"

    if r.status_code != 200:
        return False, f"HTTP {r.status_code} from {url}: {r.text[:300]}"

    try:
        return True, r.json()
    except ValueError:
        return False, f"Invalid JSON from {url}: {r.text[:300]}"

def get_workflow_execution(fire_host: str, token: str, activity_id: str) -> int:
    if not activity_id.isdigit():
        print("Please enter a valid Activity ID (numbers only).")
        return 1

    fire_host = fire_host.rstrip("/")
    headers = {"token": token}
    s = _session_for(fire_host)

    url = f"{fire_host}{WORKFLOW_EXECUTION_API}/{activity_id}"
    ok, data = _get_json(s, url, headers)

    if not ok:
        print(f"Error fetching the Activity: {data}")
        return 1

    run_id = data.get("applicationId")
    if run_id:
        if run_id.startswith("run_id-"):
            parts = run_id.split("-")
        if len(parts) >= 3 and parts[1].isdigit():
            run_id = parts[1]
        print(f"\n run_id for Activity ID {activity_id} is: {run_id}")
    else:
        print(f"\n run_id not found for Activity ID: {activity_id}")

    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch Run ID using Activity ID")
    parser.add_argument("fire_host_url")
    parser.add_argument("access_token")
    parser.add_argument("--activityId", required=True)
    args = parser.parse_args()

    sys.exit(get_workflow_execution(args.fire_host_url, args.access_token, args.activityId))