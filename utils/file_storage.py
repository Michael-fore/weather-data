import os
from datetime import datetime

## HAven't tested with non-GCP storage, will 
#prolly be a few bugs there especially with th config

# AI did alot of this work lol
class Storage:
    '''
    Dependingn on the environment, should handle saving files the correct file storage from 
    the project configurationns
    '''
    def __init__(self, project_config):
        self.project_config = project_config
        self.storage = self.get_storage()

    def get_storage(self):
        if self.project_config['cloud_provider'] == 'GCP':
            return GCP(self.project_config['project_id'])
        elif self.project_config['cloud_provider'] == 'Azure':
            return Azure(self.project_config['storage_account_name'], self.project_config['container_name'])
        elif self.project_config['cloud_provider'] == 'AWS':
            return AWS(self.project_config['access_key'], self.project_config['secret_key'], self.project_config['bucket_name'])
        else:
            raise Exception("Invalid cloud provider")
    
    def save_file(self, file_path):
        self.storage.save_file(file_path, self.project_config['bucket_name'])

    def delete_file(self, file_path):
        self.storage.delete_file(file_path, self.project_config['bucket_name'])       

class GCP:
    def __init__(self, project_id):
        self.project_id = project_id

    def save_file(self, file_path, bucket_name):
        # Code to save file to GCP file storage
        # Example: gsutil cp file_path gs://bucket_name/
        os.system(f"gsutil cp {file_path} gs://{bucket_name}/")

    def delete_file(self, file_path, bucket_name):
        # Code to delete file from GCP file storage
        # Example: gsutil rm gs://bucket_name/file_path
        os.system(f"gsutil rm gs://{bucket_name}/{file_path}")

class Azure:
    def __init__(self, storage_account_name, container_name):
        self.storage_account_name = storage_account_name
        self.container_name = container_name

    def save_file(self, file_path):
        # Code to save file to Azure file storage
        # Example: az storage blob upload --account-name storage_account_name --container-name container_name --name file_name --type block --file file_path
        os.system(f"az storage blob upload --account-name {self.storage_account_name} --container-name {self.container_name} --name {os.path.basename(file_path)} --type block --file {file_path}")

class AWS:
    def __init__(self, access_key, secret_key, bucket_name):
        self.access_key = access_key
        self.secret_key = secret_key
        self.bucket_name = bucket_name

    def save_file(self, file_path):
        # Code to save file to AWS S3 bucket
        # Example: aws s3 cp file_path s3://bucket_name/
        os.system(f"aws s3 cp {file_path} s3://{self.bucket_name}/")
    
    def delete_file(self, file_path):
        # Code to delete file from AWS S3 bucket
        # Example: aws s3 rm s3://bucket_name/file_path
        os.system(f"aws s3 rm s3://{self.bucket_name}/{file_path}")