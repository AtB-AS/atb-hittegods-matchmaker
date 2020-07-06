from flask import Flask
import os
from os.path import join, dirname
from dotenv import load_dotenv
import psycopg2
import Mathing

test = ""

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")

app=Flask(__name__)
@app.route("/")
def hello():
    return (str(Mathing.testMatching()))

@app.route("/name")
def hello2():
    return str(get_names())

print(Mathing.testMatching())
print("***************")
print(os.getenv('DB_HOST'))

hostname = os.environ.get("DB_HOST")
username = os.environ.get("DB_USER")
password = os.environ.get("DB_PASSWORD")
database = os.environ.get("DB_NAME")

# Simple routine to run a query on a database and print the results:
def doQuery( conn ) :
    cur = conn.cursor()

    cur.execute( "SELECT * from lost" )

    result = cur.fetchall()
    for row in result:
        print(row[0])
    return row

def get_names():
    myConnection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)
    query = doQuery( myConnection )
    myConnection.close()
    return query
