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
myConnection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)


def get_all_lost():
    df_all_lost = pd.read_sql_query("select * from lost;", myConnection)
    return df_all_lost

def get_all_found():
    df_all_found = pd.read_sql_query("select * from found;", myConnection)
    return df_all_found

def get_lost(lostID):
    df_lost = pd.read_sql_query("select * from lost where refnr = '"+lostID+"';",  myConnection)
    return df_lost

def get_found(foundID):
    df_found = pd.read_sql_query("select * from found where refnr = '"+foundID+"';",  myConnection)
    return df_found