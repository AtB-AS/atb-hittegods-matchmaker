import database
import Mathing
from utils import rowsToDf


def foundMatch(foundid):
    nMatches = 5
    found, foundDescription = database.get_found(foundid)
    foundDf = rowsToDf(found, foundDescription)

    lostData, lostDescription = database.get_all_lost()
    if (lostData is None):
        raise Exception("Could not get lost data from database")
    lostDf = rowsToDf(lostData, lostDescription)

    print(database.test_query())

    if nMatches > len(lostData):
        nMatches = len(lostData)

    bestMatches = Mathing.doMatching(foundDf, lostDf, nMatches)

    for match in bestMatches:
        values = list(match.values())
        if (values[2] > 0.55):
            database.insert_match_table(values[2], values[1], values[0])
        else:
            print("Score too low, not sent to DB")

    return str(list(bestMatches))

def matchingDB(x_type, x_id):

    nMatches = 5

    if x_type == "found":
        data = database.get_all_lost()
        x = database.get_found(x_id)
    elif x_type == "lost":
        data = database.get_all_found()
        x = database.get_lost(x_id)

    if nMatches > len(data):
        nMatches = len(data)


    bestMatches = Mathing.doMatching(x, data, nMatches)

    for match in bestMatches:
        values = list(match.values())
        if(values[2]>0.55):
            if x_type == "found":
                database.insert_match_table(values[2], values[1], values[0])
            elif x_type == "lost":
                database.insert_match_table(values[2], values[0], values[1])
        else:
            print("Score too low, not sent to DB")

    return str(list(bestMatches))