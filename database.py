import os
from os.path import join, dirname
from dotenv import load_dotenv
import psycopg2
from psycopg2 import OperationalError

dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)

hostname = os.environ.get("DB_HOST")
username = os.environ.get("DB_USER")
password = os.environ.get("DB_PASSWORD")
database = os.environ.get("DB_NAME")

def read_query(query, params=None, do_return=True):
    try:
        connection = psycopg2.connect(
            host=hostname, user=username, password=password, dbname=database
        )
        cursor = connection.cursor()
        cursor.execute(query, params)
        connection.commit()
        if do_return:
            return cursor.fetchall(), cursor.description
    except psycopg2.DatabaseError:
        if connection is not None:
            connection.rollback()
    except psycopg2.Error as e:
        print(e)
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None:
            connection.close()


def get_all_lost():
    return read_query("select * from lost join status on lost.statusid=status.statusid where status='Mistet';")


def get_all_found():
    return read_query("select * from found join status on found.statusid=status.statusid where status='Funnet'  or status='På vei';")


def get_lost(lostID):
    return read_query("select * from lost where lostid = %s;", (lostID,))


def get_found(foundID):
    return read_query("select * from found where foundid = %s;", (foundID,))


def insert_match_table(score, lostID, foundID):
    read_query(
        "INSERT INTO match ( lostid, foundid, score, new) VALUES (%s, %s, %s, true);", (lostID, foundID, score),
        do_return=False,
    )
