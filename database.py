import os
from os.path import join, dirname
from dotenv import load_dotenv
import psycopg2
import pandas as pd
from psycopg2 import OperationalError

dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)

hostname = os.environ.get("DB_HOST")
username = os.environ.get("DB_USER")
password = os.environ.get("DB_PASSWORD")
database = os.environ.get("DB_NAME")

try:
    myConnection = psycopg2.connect(
        host=hostname, user=username, password=password, dbname=database
    )
    print("SQL connection is opened")
except OperationalError as err:
    print(err)
    myConnection = None


def read_query(connection, query, do_return=True):
    cursor = connection.cursor()
    print(query)
    try:
        cursor.execute(query)
        connection.commit()
        connection.rollback()
        if do_return:
            element_id = [x[0] for x in cursor.description]
            rows = cursor.fetchall()
            print(pd.DataFrame(rows, columns=element_id))
            return pd.DataFrame(rows, columns=element_id)
    except psycopg2.Error as e:
        print(e)
    except psycopg2.DatabaseError:
        connection.rollback()

    finally:
        if cursor is not None:
            cursor.close()


def get_all_lost():
    return read_query(myConnection, "select * from lost join status on lost.statusid=status.statusid where status='Mistet';")


def get_all_found():
    return read_query(myConnection, "select * from found join status on found.statusid=status.statusid where status='Funnet'  or status='På vei';")


def get_lost(lostID):
    return read_query(myConnection, "select * from lost where lostid = %s;" % (lostID))


def get_found(foundID):
    return read_query(
        myConnection, "select * from found where foundid = %s;" % (foundID)
    )


def insert_match_table(score, lostID, foundID):
    read_query(
        myConnection,
        "INSERT INTO match ( lostid, foundid, score, new) VALUES (%s, %s, %s, true);"
        % (lostID, foundID, score),
        do_return=False,
    )
