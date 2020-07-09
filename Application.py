import database
import MatchingFromDB
from flask import render_template
from flask import Flask, request
from flask import jsonify
import json

app = Flask(
    __name__,
    template_folder="exception_handling/templates",
    static_folder="exception_handling/static",
)


@app.route("/")
def root():
    return "Melk"


@app.route("/lost/<lost_id_refnr>")
def lost(lost_id_refnr):

    lost_id = database.get_lost_row_refnr(str(lost_id_refnr))
    lost = int(lost_id["lostid"].iloc[0])

    print("json : ")
    print(type(lost))
    print("number2 : ")
    print(lost)
    MatchingFromDB.matchingDB("lost", lost)
    # print("test-lost : " + lost_id.to_string)
    # print("lost2 : " + lost_id)

    # print("lost id : " + json.dumps(lost_id))

    # lost_id = int(lost_id.split("\n")[0])

    # print(MatchingFromDB.matchingDB("lost", lost_id))
    return str(lost)


@app.route("/found/<found_id>")
def found(found_id):
    foundid = int(found_id.split("\n")[0])
    print(MatchingFromDB.matchingDB("found", foundid))
    return "funket"


@app.route("/actions", methods=["POST"])
def actions():
    title = request.args.get("title")
    request.get_json()
    if not title:
        return "funket ikke"
    return title + "title"


@app.errorhandler(400)
def handle_bad_request(error):
    data = {"status": "error", "errormessage ": error}
    return render_template("400.html", error=error), 404, data


@app.errorhandler(404)
def not_found_error(error):
    data = {"status": "error", "errormessage ": error}
    return render_template("404.html", error=error), 404, data


@app.errorhandler(500)
def internal_error(error):
    data = {"status": "error", "errormessage ": error}
    return render_template("500.html", error=error), 500, data


@app.route("/matching")
def matchingFromDB():
    return MatchingFromDB.matchingDB("found", 1)
