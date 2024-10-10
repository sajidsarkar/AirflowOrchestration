# AirflowOrchestration

## Project Objective and Summary
The main objective was to build a data pipeline for ingesting data from source and transform it over a medallion architecture. The data pipeline was orchestrated using Airflow. Stock data was ingested from Yahoo API and transformation was performed on the semi-structured data using python. A Medallion architecture was created using Azure Data Lake Storage (ADLS) Gen2 storage layers. The Airflow environment was setup on local machine (Windows) using Astro CLI.

**Architecture**
Diagram showing the architecture.

## Environment Setup
Before starting to develop the data pipeline, several environments had to be setup. Below are the setups that were performed prior to starting ETL development work:
1. Install Docker Desktop
2. Setup Airflow Environment in Local Machine (Windows)
3. Setup Azure ADLS Gen2 storage account
4. Create external connections in Airflow for
    - ADLS Gen2
    - Yahoo API


### Setup Airflow Environment in Local Machine (Windows)
Airflow was setup using Astro CLI, so install it first by following the instruction in this [link]([url](https://www.astronomer.io/docs/astro/cli/install-cli)). Once Astro CLI is downloaded, open Docker Desktop. Then open Windows Command Prompt from your desired project directory and type `astro dev init`. This will initialize the Airflow environment. After that type `astro dev start` to start the Airflow environment. As simple as that! Once Airflow is successfully Several folders, sub-folders, and files will be generated in your working directory. The key folders to focus here are _dags_, _include_, and _requirements.txt_. 
- _dags_: Your dag file will reside in this folder.
- _include_: This will contain any Python script and supporting python helper files. 
- _requirements.txt_: This is where you write down any additional Python library required for your application and should be installed in your airflow container. For example, Azure SDK library for Python `apache-airflow-providers-microsoft-azure==10.5.0`

Also, once Airflow is up and running, you should be able to navigate to `http://localhost:8080/home` in a browser to access the Airflow User Interface (UI). By default, `username`: `admin` and `password`: `admin`.
___
Troubleshooting Occupied Port When Starting Airflow - 
When running `astro dev start`, you might come across this error message: `Error: error building, (re)creating or starting project containers: Error response from daemon: Ports are not available: exposing port TCP 127.0.0.1:5432 -> 0.0.0.0:0: listen tcp 127.0.0.1:5432: bind: An attempt was made to access a socket in a way forbidden by its access permissions.`

If so, open a new command prompt window in "Run as administrator" mode, type `netstat -a -n -o | find "5432"`. Here "5432" is the port number shown on the error message. For your case it could be some other port number. You should get something like this below
![image](https://github.com/user-attachments/assets/cd12a0ca-36d9-46ed-b4dc-de561266f0d5)

Then type `taskkill /PID 7464 /F`. This should release the port. Go back to your previous command prompt window and type `astro dev start` again.
___

### Azure Data Lake Storage Gen2 Setup
For this you just create a storage account in Azure. Make sure to enable `hierarchical namespace` when creating storage account, as that will create an ADLS Gen2. After creating account, copy the `Connection String` from `Security + networking` -> `Access keys` and save it in a notepad. This will be used to setup external connection in Airflow UI. 
Go to Airflow UI. Select `Admin` -> `Connections` from top menu and create a connection to setup ADLS Gen2 as an external connection for your Airflow dag.
- **Connection Id**: Any name to identify this connection later in your code.
- **Connection Type**: `Azure Data Lake Storage V2`
- **ADLS Gen2 Account Name**: Name of your storage account.
- **ADLS Gen2 Connection String (optional)**: The Connection String you copied previously.


**Data Source (Yahoo API)**
This is a free API from where you can fetch stock data from Yahoo. As described previously create a connection for this Airflow UI.
- **Connection Id**: Any name to identify this connection later in your code.
- **Connection Type**: `HTTP`
- **Host**: https://query1.finance.yahoo.com/
- **Extra**:
  ```
    {
    "endpoint": "v8/finance/chart/",
    "headers": {
      "Content-Type": "application/json",
      "User-Agent": "Mozilla/5.0"
    },
    "parameters": {
      "metrics": "high",
      "interval": "1d",
      "range": "1y"
    }
  }
  ```


Airflow Operators

Azure SDK to Interact with ADLS Gen2

