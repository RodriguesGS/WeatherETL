import os
import pandas as pd
from dotenv import load_dotenv
import logging

from sqlalchemy import create_engine
from urllib.parse import quote_plus
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(message)s')

load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / 'config' / '.env')

DB = os.getenv('DB')
USER = os.getenv('DB_USER')
PASSWORD = os.getenv('PASSWORD', '')
HOST = 'host.docker.internal'


def get_engine():
    logging.info(f'-> Conectando em {HOST}:5432/{DB}')
    return create_engine(
        f'postgresql+psycopg2://{USER}:{quote_plus(PASSWORD)}@{HOST}:5432/{DB}')

def load_weather_data(table: str, df: pd.DataFrame):
    engine = get_engine()
    
    df.to_sql(
        name=table,
        con=engine,
        if_exists='append',
        index=False
    )

    logging.info('Dados carregados com sucesso!\n')

    df_check = pd.read_sql(f'SELECT * FROM {table}', con=engine)
    logging.info(f'Total de registros na tabela: {len(df_check)}\n')