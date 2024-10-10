import json
import requests
from airflow.hooks.base import BaseHook
from include.ADLSArtifacts import DataLakeUtility

class Source2Bronze:

    def __init__(self, tickers):
        self.tickers = tickers

    def load_data(self, ticker):
        api_conn = BaseHook.get_connection('yahoo_api')
        base_url = api_conn.host
        endpoint = api_conn.extra_dejson['endpoint']
        endpoint_ticker = f'{endpoint}/{ticker}'
        headers = api_conn.extra_dejson['headers']
        parameters = api_conn.extra_dejson['parameters']
        response = requests.get(url = f'{base_url}{endpoint_ticker}', headers = headers, params = parameters)
        return json.dumps(response.json()['chart']['result'][0])

    def ingest_data(self):
        dlake = DataLakeUtility()
        dlake.create_containers()

        for ticker in self.tickers:
            data = self.load_data(f'{ticker}')
            dlake.upload_data('bronze', f'{ticker}.json', data)