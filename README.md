# AirflowOrchestration

### Project Objective and Summary
The main objective was to build a data pipeline for ingesting data from source and transform it over a medallion architecture. The data pipeline was orchestrated using Airflow. Stock data was ingested from Yahoo API and transformation was performed on the semi-structured data using python. A Medallion architecture was created using Azure Data Lake Storage (ADLS) Gen2 storage layers. The Airflow environment was setup on local machine (Windows) using Astro CLI.

**Architecture**
Diagram showing the architecture.

### Airflow Setup using Astro CLI on Windows Machine
Airflow is setup using Astro CLI, so install it first by following the instruction in this [link]([url](https://www.astronomer.io/docs/astro/cli/install-cli)). Once downloaded, open Windows Command Prompt from your desired project directory and type `astro dev init`. This will initialize the Airflow environment. After that type `astro dev start` to start the Airflow environment. As simple as that!

**Azure Data Lake Storage Gen2 Setup**


**Data Source (Yahoo API)**


**Airflow Operators**

### Azure SDK to Interact with ADLS Gen2

