import database
import MatchingFromDB
from flask import render_template
from flask import Flask, request
from flask import jsonify

app = Flask(
    __name__,
    template_folder="exception_handling/templates",
    static_folder="exception_handling/static",
)


@app.route("/")
def root():
    return ""


@app.route("/lost/<lost_id>")
def lost(lost_id):
    lostid = int(lost_id.split("\n")[0])
    print(MatchingFromDB.matchingDB("lost", lostid))
    return "funket"


@app.route("/found/<found_id>")
def found(found_id):
    foundid = int(found_id.split("\n")[0])
    print(MatchingFromDB.matchingDB("found", foundid))
    return "funket"


@app.errorhandler(400)
def handle_bad_request(error):
    data = {"status": "error", "errormessage ": error}
    return data, 400


@app.errorhandler(404)
def not_found_error(error):
    data = {"status": "error", "errormessage ": error}
    return data, 404


@app.errorhandler(500)
def internal_error(error):
    data = {"status": "error", "errormessage ": error}
    return data, 500
