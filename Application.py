from MatchingFromDB import matchingDB, foundMatch
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
        matchingDB("lost", int(lost_id))
        return "success"
    except Exception as e:
        logger.warning(e)
        print(e)
        return str(e)


@app.route("/found/<found_id>")
def found(found_id):
    try:
        foundMatch(found_id)
        return "success"
    except Exception as e:
        logger.warning(e)
        print("Exception:")
        print(e)
        return str(e)


@app.errorhandler(400)
def handle_bad_request(error):
    return "400 error", 400


@app.errorhandler(404)
def not_found_error(error):
    return "404 error", 404


@app.errorhandler(500)
def internal_error(error):
    return "500 error", 500
