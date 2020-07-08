import database
import Mathing


def matchingDB(x_type, x_id):

    if x_type == "found":
        data = database.get_all_lost()
        x = database.get_found(x_id)
    elif x_type == "lost":
        data = database.get_all_found()
        x = database.get_lost(x_id)

    bestMatches = Mathing.doMatching(x, data, 5)

    for match in bestMatches:
        values = list(match.values())
        if x_type == "found":
            database.insert_match_table(values[2], values[1], values[0])
        elif x_type == "lost":
            database.insert_match_table(values[2], values[0], values[1])

    return str(list(bestMatches))
