import boto3
import google.auth
from googleapiclient.discovery import build
from azure.identity import DefaultAzureCredential
from azure.mgmt.web import WebSiteManagementClient


# AI stuff again, only going to test teh GCP for now but if we ever need to pop over
# things shouldn't be too bad

class AWSFunctionDeployer:
    def __init__(self, aws_access_key, aws_secret_key, region_name):
        self.client = boto3.client(
            'lambda',
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key,
            region_name=region_name
        )

    def deploy_function(self, function_name, role, handler, zip_file_path, runtime='python3.8'):
        with open(zip_file_path, 'rb') as f:
            zip_content = f.read()

        response = self.client.create_function(
            FunctionName=function_name,
            Runtime=runtime,
            Role=role,
            Handler=handler,
            Code={'ZipFile': zip_content},
            Publish=True
        )
        print('AWS Function deployed:', response)

class AzureFunctionDeployer:
    def __init__(self, subscription_id, resource_group, function_app_name):
        self.subscription_id = subscription_id
        self.resource_group = resource_group
        self.function_app_name = function_app_name
        self.credential = DefaultAzureCredential()
        self.client = WebSiteManagementClient(self.credential, self.subscription_id)

    def deploy_function(self, zip_file_path):
        with open(zip_file_path, 'rb') as f:
            zip_content = f.read()

        response = self.client.web_apps.begin_create_or_update_function_app(
            self.resource_group,
            self.function_app_name,
            {
                'location': 'westus',
                'server_farm_id': '/subscriptions/{}/resourceGroups/{}/providers/Microsoft.Web/serverfarms/{}'.format(
                    self.subscription_id, self.resource_group, self.function_app_name
                ),
                'site_config': {
                    'app_settings': [
                        {'name': 'FUNCTIONS_WORKER_RUNTIME', 'value': 'python'},
                        {'name': 'WEBSITE_RUN_FROM_PACKAGE', 'value': '1'}
                    ]
                },
                'kind': 'functionapp',
                'reserved': True,
                'https_only': True
            }
        ).result()
        print('Azure Function deployed:', response)

class GCPFunctionDeployer:
    def __init__(self, project_id, location):
        self.project_id = project_id
        self.location = location
        self.credentials, self.project = google.auth.default()
        self.service = build('cloudfunctions', 'v1', credentials=self.credentials)

    def deploy_function(self, function_name, source_archive_url, entry_point, runtime='python39'):
        function = {
            'name': f'projects/{self.project_id}/locations/{self.location}/functions/{function_name}',
            'entryPoint': entry_point,
            'runtime': runtime,
            'httpsTrigger': {},
            'sourceArchiveUrl': source_archive_url
        }

        request = self.service.projects().locations().functions().create(
            location=f'projects/{self.project_id}/locations/{self.location}',
            body=function
        )
        response = request.execute()
        print('GCP Function deployed:', response)



class Deployer:
    def __init__(self, cloud_provider):
        self.cloud_provider = cloud_provider

    def deploy_function(self, function_name, **kwargs):
        if self.cloud_provider == 'AWS':
            aws_deployer = AWSFunctionDeployer(**kwargs)
            aws_deployer.deploy_function(function_name)
        elif self.cloud_provider == 'Azure':
            azure_deployer = AzureFunctionDeployer(**kwargs)
            azure_deployer.deploy_function(function_name)
        elif self.cloud_provider == 'GCP':
            gcp_deployer = GCPFunctionDeployer(**kwargs)
            gcp_deployer.deploy_function(function_name)
        else:
            raise Exception("Invalid cloud provider")

# # Example usage:
# # AWS
# aws_deployer = AWSFunctionDeployer('your-aws-access-key', 'your-aws-secret-key', 'us-west-2')
# aws_deployer.deploy_function('my-aws-function', 'arn:aws:iam::123456789012:role/execution_role', 'lambda_function.lambda_handler', 'path/to/your/function.zip')

# # Azure
# azure_deployer = AzureFunctionDeployer('your-subscription-id', 'your-resource-group', 'your-function-app-name')
# azure_deployer.deploy_function('path/to/your/function.zip')

# # GCP
# gcp_deployer = GCPFunctionDeployer('your-project-id', 'us-central1')
# gcp_deployer.deploy_function('my-gcp-function', 'gs://your-bucket/your-source.zip', 'your_entry_point')