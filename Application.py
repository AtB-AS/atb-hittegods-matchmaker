from flask import Flask
import exception_handling
import database
from flask import render_template

app=Flask(__name__, template_folder='exception_handling/templates', static_folder='exception_handling/static')

@app.route("/")
def root():
    return database.get_all_lost().to_json()

@app.route("/get_score")
def get_score():
    database.myConnection.rollback()
    return database.get_lost("42f8f207-c09a-4b03-8281-726a73b8094").to_json()

@app.route("/name")
def insert_to_database():
    database.insert_match_table("1", "2", "2")
    return "inserted"

@app.errorhandler(400)
def handle_bad_request(error):
    data = {'status': 'error', 'errormessage ': error}
    return render_template('404.html', error=error), 404, data

@app.errorhandler(404)
def not_found_error(error):
    data = {'status': 'error', 'errormessage ': error}
    return render_template('404.html', error=error), 404, data

@app.errorhandler(500)
def internal_error(error):
    data = {'status': 'error', 'errormessage ': error}
    return render_template('500.html', error=error), 500, data



