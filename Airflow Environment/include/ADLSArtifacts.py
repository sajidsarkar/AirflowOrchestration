from azure.storage.filedatalake import DataLakeServiceClient
from azure.core.exceptions import ResourceExistsError
# from airflow.hooks.base import BaseHook
import json 


# CONNECTION_STRING = "DefaultEndpointsProtocol=https;AccountName=dummyairflowstorage;AccountKey=gisiiVVpE9z2hxv5u2dvar6Joh6Od/mY4Yn0W/su034olOugS+52KSs28Pv8Y0ayAeTmjD8ISp/++ASt8ta1Bw==;EndpointSuffix=core.windows.net"

class DataLakeUtility:

    def __init__(self):
        # adls_conn = BaseHook.get_connection('adls')
        # self.connection_string = adls_conn.extra_dejson['connection_string']
        self.connection_string = "DefaultEndpointsProtocol=https;AccountName=dummyairflowstorage;AccountKey=gisiiVVpE9z2hxv5u2dvar6Joh6Od/mY4Yn0W/su034olOugS+52KSs28Pv8Y0ayAeTmjD8ISp/++ASt8ta1Bw==;EndpointSuffix=core.windows.net"
        self.containers = ['bronze', 'silver', 'gold']

    def get_service_client(self):
        # creation service connection object
        return DataLakeServiceClient.from_connection_string(conn_str=self.connection_string)    

    def get_container_client(self, container):
        return self.get_service_client().get_file_system_client(container)

    def get_object_client(self, container, file):
        return self.get_container_client(container).get_file_client(file)

    def create_containers(self):
        data_lake_service_client = self.get_service_client()

        # Create the required containers
        for container in self.containers:
            try:
                data_lake_service_client.create_file_system(container)
            except ResourceExistsError:
                print(f'Container, "{container}", already exists.')

    
    def upload_data(self, container, file, data):
        file_client = self.get_object_client(container, file)
        file_client.upload_data(data, overwrite=True)
    
    def download_data(self, container, file):
        file_client = self.get_object_client(container, file)
        if file.endswith('.json'):
            data = file_client.download_file().readall()
            if data:
                return json.loads(file_client.download_file().readall())
            return data
        else:
            return file_client.download_file().readall()
        