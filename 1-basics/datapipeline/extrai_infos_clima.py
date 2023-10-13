import os
from os.path import join
import pandas as pd
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

data_inicio = datetime.today()
data_fim = data_inicio + timedelta(days=7)

data_inicio = data_inicio.strftime('%Y-%m-%d')
data_fim = data_fim.strftime('%Y-%m-%d')

city = 'Boston'
key = f'{os.getenv("API_KEY")}'

URL = join('https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/'+
    f'{city}/{data_inicio}/{data_fim}?unitGroup=metric&include=days&key={key}&contentType=csv')

dados = pd.read_csv(URL)
print(dados.head())

file_path = f'C:\\Users\\Pichau\\Desktop\\airflow-alura\\datapipeline\\semana={data_inicio}\\'
os.mkdir(file_path)

dados.to_csv(file_path + 'dados_brutos.csv')
dados[['datetime', 'tempmin', 'temp', 'tempmax']].to_csv(file_path + 'temperatura.csv')
dados[['datetime', 'description', 'icon']].to_csv(file_path + 'condicoes.csv')