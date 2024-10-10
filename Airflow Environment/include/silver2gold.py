import pandas as pd
from io import StringIO
from include.ADLSArtifacts import DataLakeUtility

class Silver2Gold():
    def run_transformation(self):
        dlake = DataLakeUtility()
        container_client = dlake.get_container_client('silver')
        silver_files = container_client.get_paths()
        for i, csv_file in enumerate(silver_files):
            if csv_file.name.endswith('.csv'):
                # receiving a sequence of immutable bytes
                byte_data = dlake.download_data('silver', csv_file.name)
                # Guessing byte_data is UTF-8 encoded
                # From assumed UTF-8 representation, it is decoded to a string
                csv_string_data = byte_data.decode('utf-8')
                # StringIO to convert string variable into a file-like.
                # read_csv requires a csv file.
                temp_df = pd.read_csv(StringIO(csv_string_data))
                if i == 0:
                    df = temp_df.copy()
                else:
                    df = pd.concat([df, temp_df], axis=0)

        del temp_df
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s').dt.strftime('%Y-%m-%d')
        csv_string = df.to_csv(index=False)
        dlake.upload_data('gold','allstock.csv', csv_string)