import pandas as pd
from io import StringIO
from include.ADLSArtifacts import DataLakeUtility

class Bronze2Silver:
    def run_transformation(self):
        dlake = DataLakeUtility()
        container_client = dlake.get_container_client('bronze')
        bronze_files = container_client.get_paths()
        for file in bronze_files:
            if file.name.endswith('.json'):
                ticker_file = file.name
                ticker = ticker_file.replace('.json', '')
                content = dlake.download_data('bronze',f'{file.name}')
                data = {}
                data['meta'] = content['meta']
                data['timestamp'] = content['timestamp']
                data['quote'] = content['indicators']['quote']
                df = pd.json_normalize(data, record_path='quote', meta=['timestamp', ['meta', 'symbol'], ['meta', 'timezone'], ['meta', 'fiftyTwoWeekHigh'], ['meta', 'fiftyTwoWeekLow'], ['meta', 'shortName']], errors='ignore')
                df_data = df[['high', 'low', 'open', 'close', 'volume', 'timestamp']]
                df_data = df_data.explode([col for col in df_data.columns])
                df_meta = df[['meta.symbol', 'meta.timezone', 'meta.fiftyTwoWeekHigh', 'meta.fiftyTwoWeekLow', 'meta.shortName']]
                df_meta.columns = [col.split('.')[-1] for col in df_meta.columns]
                n = df_data.shape[0]
                df_meta = df_meta.loc[df_meta.index.repeat(n)]
                df = pd.concat([df_data, df_meta], axis=1)
                csv_string = df.to_csv(index=False)
                dlake.upload_data('silver',f'{ticker}.csv', csv_string)