from azure.storage.fileshare import ShareFileClient
from django.core.files.storage import Storage
from django.core.exceptions import ImproperlyConfigured
from django.conf import settings
import os

class AzureFileStorage(Storage):
    def __init__(self, option=None):
        self.connection_string = settings.AZURE_CONNECTION_STRING
        self.share_name = settings.AZURE_SHARE_NAME

        if not self.connection_string or not self.share_name:
            raise ImproperlyConfigured("Azure Storage settings are not properly configured.")
    
    def _get_file_client(self, name):
        return ShareFileClient.from_connection_string(self.connection_string, share_name=self.share_name, file_path=name)
    
    def _save(self, name, content):
        file_client = self._get_file_client(name)
        file_client.upload_file(content)
        return name
    
    def _open(self, name, mode='rb'):
        file_client = self._get_file_client(name)
        file_data = file_client.download_file().readall()
        return file_data

    def exists(self, name):
        file_client = self._get_file_client(name)
        return file_client.exists()
    
    def url(self, name):
        file_client = self._get_file_client(name)
        return file_client.url
    
    def delete(self, name):
        file_client = self._get_file_client(name)
        file_client.delete_file()
