import sys
import csv
import argparse
import requests
from typing import Optional
import urllib3
from urllib3.exceptions import InsecureRequestWarning

ROLES_PRIMARY = "/api/v1/roles"
ROLES_FALLBACK = "/userRoles"
USERS_DETAILS = "/api/v1/users/details"

def _session_for(fire_host: str) -> requests.Session:
    s = requests.Session()
    if fire_host.lower().startswith("https://"):
        s.verify = False
        urllib3.disable_warnings(InsecureRequestWarning)
    return s

def _get_json(s: requests.Session, url: str, headers: dict, timeout: int):
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

def export_roles_with_users(fire_host: str, token: str, role_filter: Optional[str] = None) -> int:
    fire_host = fire_host.rstrip("/")
    headers = {"token": token}

    s = _session_for(fire_host)

    ok, roles = _get_json(s, f"{fire_host}{ROLES_PRIMARY}", headers, timeout=30)
    if not ok:
        ok_fb, roles_fb = _get_json(s, f"{fire_host}{ROLES_FALLBACK}", headers, timeout=30)
        if not ok_fb:
            print(f"Error fetching roles.\nPrimary: {roles}\nFallback: {roles_fb}")
            return 1
        roles = roles_fb

    if not isinstance(roles, list):
        print("Error: roles response is not a JSON array.")
        return 1

    ok, users = _get_json(s, f"{fire_host}{USERS_DETAILS}", headers, timeout=60)
    if not ok:
        print(f"Error fetching users: {users}")
        return 1
    if not isinstance(users, list):
        print("Error: users response is not a JSON array.")
        return 1

    role_id_to_name = {}
    role_name_to_users = {}

    for r in roles:
        try:
            rid = int(r.get("id"))
            rname = str(r.get("name", ""))
        except Exception:
            continue
        if not rname:
            continue
        role_id_to_name[rid] = rname
        role_name_to_users.setdefault(rname, [])

    for u in users:
        username = str(u.get("username", "") or "")
        user_role_ids = u.get("roles") or []
        if not isinstance(user_role_ids, list):
            continue
        for rid in user_role_ids:
            try:
                rid_int = int(rid)
            except Exception:
                continue
            rname = role_id_to_name.get(rid_int)
            if rname:
                role_name_to_users.setdefault(rname, []).append(username)

    filtered_roles = roles
    if role_filter:
        wanted = role_filter.strip().lower()
        filtered_roles = [x for x in roles if str(x.get("name", "")).lower() == wanted]
        if not filtered_roles:
            print("Role does not exist")
            return 0

    try:
        with open("roles_users.csv", "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["role", "users"])
            for r in filtered_roles:
                rname = str(r.get("name", ""))
                usernames = sorted(role_name_to_users.get(rname, []))
                w.writerow([rname, ",".join(usernames)])
    except OSError as e:
        print(f"Error writing roles_users.csv: {e}")
        return 1

    return 0

if __name__ == "__main__":
    if len(sys.argv) == 4 and not sys.argv[1].lower().startswith(("http://", "https://")):
        role_name, fire_host, token = sys.argv[1], sys.argv[2], sys.argv[3]
        sys.exit(export_roles_with_users(fire_host, token, role_name))

    parser = argparse.ArgumentParser(description="Export role->users CSV")
    parser.add_argument("fire_host_url")
    parser.add_argument("access_token")
    parser.add_argument("-r", "--role", dest="role", help="Filter by role name (case-insensitive)")
    args = parser.parse_args()

    sys.exit(export_roles_with_users(args.fire_host_url, args.access_token, args.role))