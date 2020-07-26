import database
import Matching
from dataset import Dataset
from utils import rows_to_df


"""

These functions does the network calls to get data, calls the matching algorithm function and writes to the match
relation database

"""

# These functions could possibly have been combined, but it would split the functions in 2 depending on the case
# Having them separate is mostly equivalent

# //TODO these should catch errors and return something like a status

def found_match(foundid):
    """
    gets the data for the found item with the given found id from the DB and matches it against all the data in the
    lost table in the DB. Then writes the 5 best matches to the match relation table in the DB with the lostid,
    foundid and score given that the score is higher than a threshold given.



    :param foundid: found id
    """
    n_matches = 5
    found, found_description = database.get_found(foundid)
    if found is None:
        raise Exception("Cannot find foundid")

    if len(found) == 0:
        raise Exception("Cannot find foundid")
    found_df = rows_to_df(found, found_description)

    lost_data, lost_description = database.get_all_lost()
    if lost_data is None:
        raise Exception("Could not get lost data from database")
    if len(lost_data) == 0:
        raise Exception("Could not get lost data from database")
    lost_df = rows_to_df(lost_data, lost_description)

    if n_matches > len(lost_df):
        n_matches = len(lost_df)

    found_dataset=Dataset('found', 'single', found_df)
    lost_dataset=Dataset('lost', 'multiple', lost_df)

    best_matches = Matching.do_matching(found_dataset, lost_dataset, n_matches)

    insert_bestmatches_to_db(best_matches)


def lost_match(lostid):
    """
    gets the data for the lost item with the given lost id from the DB and matches it against all the data in the
    found table in the DB. Then writes the 5 best matches to the match relation table in the DB with the lostid,
    foundid and score given that the score is higher than a threshold given.



    :param lostif: lost id
    """
    n_matches = 5
    lost, lost_description = database.get_lost(lostid)
    if lost is None:
        raise Exception("Cannot find lostid")

    if len(lost) == 0:
        raise Exception("Cannot find lostid")
    lost_df = rows_to_df(lost, lost_description)

    found_data, found_description = database.get_all_found()
    if found_data is None:
        raise Exception("Could not get found data from database")
    if len(found_data) == 0:
        raise Exception("Could not get found data from database")
    found_df = rows_to_df(found_data, found_description)

    if n_matches > len(found_df):
        n_matches = len(found_df)

    found_dataset = Dataset('found', 'multiple', found_df)
    lost_dataset = Dataset('lost', 'single', lost_df)

    best_matches = Matching.do_matching(lost_dataset, found_dataset, n_matches)

    insert_bestmatches_to_db(best_matches)


def insert_bestmatches_to_db(matches):
    """Inserts best matches to DB"""


    print("\n\n----- SENDING BEST MATCHES TO DATABASE -----\n\n")

    for match in matches:
        if match.score > 0.55:
            print("Sending to db: score: ", match.score, ", lostid: ", match.lostid, ", foundid: ", match.foundid)
            database.insert_match_table(match.lostid, match.foundid, match.score)
        else:
            print("Score (", match.score, ") too low, not sent to DB")

    print("sending to database successful")