import requests
import urllib3
import zipfile
from pathlib import Path
from datetime import datetime

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

## -------------------------------------------------------------------------
## Input Parameters - EXPORT PROJECTS FROM SOURCE
## -------------------------------------------------------------------------
SOURCE_HOST = "http://localhost:8080"
SOURCE_TOKEN = "source-token"
SOURCE_PROJECT_IDS = (15418, 15419, 15420)

SOURCE_HEADERS = {
    "token": SOURCE_TOKEN
}

## -------------------------------------------------------------------------
## Input Parameters - IMPORT PROJECTS INTO TARGET
## -------------------------------------------------------------------------
TARGET_HOST = "http://localhost:8080"
TARGET_TOKEN = "target-token"

TARGET_HEADERS = {
    "token": TARGET_TOKEN
}

## -------------------------------------------------------------------------
## Project Components
## -------------------------------------------------------------------------
PROJECT_COMPONENTS = {
    "workflow": True,
    "dataset": True,
    "report": True,
    "analyticsApp": True,
    "pipeline": True,
    "wikiDoc": True,
    "chatbot": False,
    "chart": True,
}

### Main Logic Starts here
def export_and_import_projects():
    print("=========================================")
    print("        STARTING EXPORT PROCESS          ")
    print("=========================================")
    exported_zip_path = export_projects()

    if not exported_zip_path:
        raise Exception("Export did not return a zip file path. Import stopped.")

    print("\n=========================================")
    print("        STARTING IMPORT PROCESS          ")
    print("=========================================")
    import_projects(exported_zip_path)


### Export Logic - SOURCE
def export_projects():
    project_ids_list = normalize_project_ids(SOURCE_PROJECT_IDS)
    url = f"{SOURCE_HOST}/api/v1/projects/export"
    
    # THE FIX IS HERE: Format the IDs as a single comma-separated string
    # to match the frontend request: export?projectIds=15409,15410,15411
    params = {
        "projectIds": ",".join(map(str, project_ids_list))
    }

    print(f"Exporting from source host: {SOURCE_HOST}")
    print(f"Exporting source project ids: {project_ids_list}")

    response = requests.post(
        url,
        headers=SOURCE_HEADERS,
        params=params,
        json=PROJECT_COMPONENTS,
        verify=False
    )

    print("Export Status Code:", response.status_code)

    if response.ok:
        timestamp = datetime.now().strftime("%H%M%S")
        file_path = Path.cwd() / f"Projects_{timestamp}.zip"
        
        # This converts the binary response payload into a Zip file
        file_path.write_bytes(response.content)

        print("Export successful!")
        print(f"Saved to: {file_path}")

        return file_path
    else:
        print("Export failed!")
        print(response.text)
        return None


### Import Logic - TARGET
def import_projects(zip_file_path):
    zip_file_path = Path(zip_file_path)

    if not zip_file_path.exists():
        raise FileNotFoundError(f"Zip file not found: {zip_file_path}")

    project_names = get_project_names_from_zip(zip_file_path)

    if not project_names:
        raise ValueError("No projects found inside zip file")

    import_url = f"{TARGET_HOST}/api/v1/projects/import"

    print(f"Importing into target host: {TARGET_HOST}")
    print(f"Using zip file: {zip_file_path.name}")
    print("Projects found inside zip:")
    for project_name in project_names:
        print(f"- {project_name}")

    for project_name in project_names:
        print(f"\nCreating target project: {project_name}")

        created_project_id = create_project(project_name)

        print(f"Created target project id: {created_project_id}")
        print(f"Importing project data into target project: {project_name}")

        headers = {
            **TARGET_HEADERS,
            "projectId": str(created_project_id),
            "selectedProjectName": project_name,
            "projectOption": "CREATE_NEW",
            "appImportOption": "WORKFLOW_JOB",
            "connectionId": "0",
            "notebookPath": ""
        }

        with open(zip_file_path, "rb") as zip_file:
            files = {
                "file": (zip_file_path.name, zip_file, "application/zip")
            }

            response = requests.post(
                import_url,
                headers=headers,
                files=files,
                verify=False
            )

        print("Import Status Code:", response.status_code)

        if response.ok:
            print(f"Import successful for {project_name}")
            print(response.text)
        else:
            print(f"Import failed for {project_name}")
            print(response.text)


### Helper function to create project first in TARGET
def create_project(project_name):
    url = f"{TARGET_HOST}/api/v1/projects"

    payload = {
        "name": project_name
    }

    response = requests.post(
        url,
        headers={
            **TARGET_HEADERS,
            "Content-Type": "application/json",
            "Accept": "application/json"
        },
        json=payload,
        verify=False
    )

    print("Create Target Project Status Code:", response.status_code)

    if not response.ok:
        raise Exception(f"Failed to create target project {project_name}: {response.text}")

    data = response.json()

    if "id" not in data:
        raise Exception(f"Target project created but id not found in response: {data}")

    return data["id"]


### Helper function to read project names from exported zip
def get_project_names_from_zip(zip_file_path):
    project_names = set()

    with zipfile.ZipFile(zip_file_path, "r") as zip_file:
        for file_name in zip_file.namelist():
            normalized_name = file_name.replace("\\", "/")

            if normalized_name.endswith("/"):
                continue

            parts = normalized_name.split("/")

            if len(parts) >= 2 and parts[0].startswith("Projects_"):
                project_name = parts[1].strip()

                if project_name:
                    project_names.add(project_name)

    return sorted(project_names)


### Helper function to normalize project ids from various input formats
def normalize_project_ids(project_ids):
    if isinstance(project_ids, int):
        return [project_ids]

    if isinstance(project_ids, str):
        items = project_ids.split(",")
    elif isinstance(project_ids, (list, tuple, set)):
        items = project_ids
    else:
        raise ValueError("SOURCE_PROJECT_IDS must be int, string, list, tuple, or set")

    cleaned_ids = []

    for item in items:
        value = str(item).strip()

        if not value:
            continue

        if not value.isdigit():
            raise ValueError(f"Invalid source project id: {item}")

        cleaned_ids.append(int(value))

    if not cleaned_ids:
        raise ValueError("No valid source project ids found")

    return cleaned_ids


if __name__ == "__main__":
    export_and_import_projects()