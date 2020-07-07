from flask import Flask

import database

app=Flask(__name__)
@app.route("/")
def hello():
    return database.get_lost("42f8f207-c09a-4b03-8281-726a73b80094").to_json()

@app.route("/name")
def hello2():
    return "route funker"


