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


def read_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute( query )
        names = [ x[0] for x in cursor.description]
        rows = cursor.fetchall()
        return pd.DataFrame( rows, columns=names)
    finally:
        if cursor is not None:
            cursor.close()


def get_all_lost():
    return read_query(myConnection, "select * from lost;")


def get_all_found():
    return read_query(myConnection, "select * from found;")


def get_all_found(lostID):
    return read_query(myConnection, "select * from lost where lostid = '"+lostID+"';")


def get_all_lost(foundID):
    return read_query(myConnection, "select * from found where foundid = '"+foundID+"';")


def insert_match_table(score, lostID, foundID):
    return read_query(myConnection, "INSERT INTO public.match( score, lostID, foundID) VALUES ('"+score+"','"+lostID+"','"+foundID+"');")