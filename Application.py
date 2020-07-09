import MatchingFromDB
from flask import Flask
import logging

app = Flask(__name__)
logger = logging.getLogger(__name__)

@app.route("/")
def root():
    return "**Hittegods-Matchmaker**"


@app.route("/lost/<lost_id>")
def lost(lost_id):
    try:
        lost_id_to_db = int(lost_id.split("\n")[0])
        print(lost_id_to_db)
        MatchingFromDB.matchingDB("lost", lost_id_to_db)
        return "success"
    except:
        logger.warning("invalid value for lostid")
        return "invalid value for lostid"


@app.route("/found/<found_id>")
def found(found_id):
    try:
        found_id_to_db = int(found_id.split("\n")[0])
        MatchingFromDB.matchingDB("found", found_id_to_db)
        return "success"
    except:
        return "invalid value for foundid"


@app.errorhandler(400)
def handle_bad_request(error):
    return "400 error", 400


@app.errorhandler(404)
def not_found_error(error):
    return "404 error", 404


@app.errorhandler(500)
def internal_error(error):
    return "500 error", 500
