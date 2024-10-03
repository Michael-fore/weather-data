import google.auth
from googleapiclient.discovery import build
import requests

def deploy_function(project_id, location, function_name, source_archive_url, entry_point, runtime):
    credentials, project = google.auth.default()
    service = build('cloudfunctions', 'v1', credentials=credentials)

    function = {
        'name': f'projects/{project_id}/locations/{location}/functions/{function_name}',
        'entryPoint': entry_point,
        'runtime': runtime,
        'httpsTrigger': {},
        'sourceArchiveUrl': source_archive_url
    }

    request = service.projects().locations().functions().create(
        location=f'projects/{project_id}/locations/{location}',
        body=function
    )
    response = request.execute()
    print('Function deployed:', response)

def invoke_function(function_url):
    response = requests.get(function_url)
    print('Function response:', response.text)

# Example usage
project_id = 'your-project-id'
location = 'us-central1'
function_name = 'my-function'
source_archive_url = 'gs://your-bucket/your-source.zip'
entry_point = 'your_entry_point'
runtime = 'python39'

deploy_function(project_id, location, function_name, source_archive_url, entry_point, runtime)

# After deployment, you can invoke the function using its URL
function_url = 'https://us-central1-your-project-id.cloudfunctions.net/my-function'
invoke_function(function_url)