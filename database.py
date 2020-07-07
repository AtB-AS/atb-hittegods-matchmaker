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
    print(query)
    try:
        cursor.execute( query )
        connection.commit()
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


def get_lost(lostID):
    return read_query(myConnection, "select * from lost where lostid = %s;"%(lostID))


def get_found(foundID):
    return read_query(myConnection, "select * from found where foundid = %s;"%(foundID))


def insert_match_table(score, lostID, foundID):
    return read_query(myConnection, "INSERT INTO match ( lostid, foundid, score, new) VALUES (%s, %s, %s, true);"%(lostID,foundID,score))