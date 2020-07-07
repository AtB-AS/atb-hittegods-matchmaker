from flask import Flask

import database
import Mathing

app=Flask(__name__)
@app.route("/")
def hello():
    return database.get_lost("42f8f207-c09a-4b03-8281-726a73b80094").to_json()

@app.route("/name")
def hello2():
    return "route funker"

@app.route("/matching")
def matchingFromDB():

    allLost = database.get_all_lost()
    lost=database.get_lost("42f8f207-c09a-4b03-8281-726a73b80094")

    x=lost
    data=allLost

    print(list(data.columns))
    print("length of x :" + str(len(x)))

    bestMatches=Mathing.doMatching(x,data,5)

    return str(list(bestMatches))