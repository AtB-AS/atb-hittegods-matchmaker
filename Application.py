from flask import Flask

import database

app=Flask(__name__)
@app.route("/")
def hello():
    return database.get_from_dataframe().to_json()

@app.route("/name")
def hello2():
    return "test"


