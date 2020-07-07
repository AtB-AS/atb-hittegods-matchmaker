import os
from os.path import join, dirname
from dotenv import load_dotenv
import psycopg2
import pandas as pd

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

hostname = os.environ.get("DB_HOST")
username = os.environ.get("DB_USER")
password = os.environ.get("DB_PASSWORD")
database = os.environ.get("DB_NAME")

def get_from_dataframe():
    myConnection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)
    df = pd.read_sql_query("select * from lost;", myConnection)
    print("****** df *****")
    return df