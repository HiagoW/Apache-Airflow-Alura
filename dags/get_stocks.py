import yfinance
from airflow.decorators import dag, task
from airflow.macros import ds_add
from pathlib import Path
import pendulum

TICKERS = [
    "AAPL",
    "MSFT",
    "GOOG",
    "TSLA"
]

@task()
def get_history(ticker,ds=None,ds_nodash=None):
    file_path = f"/mnt/c/Users/Pichau/Desktop/airflow-alura/stocks/{ticker}/{ticker}_{ds_nodash}.csv"
    Path(file_path).parent.mkdir(parents=True, exist_ok=True)
    yfinance.Ticker(ticker).history(
        period = "1d",
        interval = "1h",
        start = ds_add(ds, -1),
        end = ds,
        prepost = True
    ).to_csv(file_path)

@dag(
    schedule_interval = "0 0 * * 2-6", # tue - sat
    start_date = pendulum.datetime(2023, 6, 1, tz="UTC"),
    catchup = True
)
def get_stocks_dag():
    for ticker in TICKERS:
        get_history.override(task_id=ticker, pool="small_pool")(ticker)

dag = get_stocks_dag()
