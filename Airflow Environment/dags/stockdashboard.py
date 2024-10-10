
from datetime import datetime
from airflow.decorators import dag
from include.source2bronze import Source2Bronze
from include.bronze2silver import Bronze2Silver
from include.silver2gold import Silver2Gold
from airflow.operators.python import PythonOperator

TICKERS = ['aapl', 'tsla']
s2b = Source2Bronze(TICKERS)
b2s = Bronze2Silver()
s2g = Silver2Gold()

@dag(
    start_date = datetime(2023,1,1),
    schedule = '51 17 * * *',
    catchup = False,
    tags = ['stockdashboard']
)

def stockdashboard():
    
    source2bronze = PythonOperator(
        task_id = 'source2bronze',
        python_callable = s2b.ingest_data
    )

    bronze2silver = PythonOperator(
        task_id = 'bronze2silver',
        python_callable = b2s.run_transformation
    )

    silver2gold = PythonOperator(
        task_id = 'silver2gold',
        python_callable = s2g.run_transformation
    )

    source2bronze >> bronze2silver >> silver2gold


stockdashboard()