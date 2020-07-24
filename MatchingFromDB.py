import database
import Matching
from dataset import dataset
from utils import rowsToDf





def foundMatch(foundid):
    nMatches = 5
    found, foundDescription = database.get_found(foundid)
    if found is None:
        raise Exception("Cannot find foundid")

    if (len(found) == 0):
        raise Exception("Cannot find foundid")
    foundDf = rowsToDf(found, foundDescription)

    lostData, lostDescription = database.get_all_lost()
    if (lostData is None):
        raise Exception("Could not get lost data from database")
    if len(lostData) == 0:
        raise Exception("Could not get lost data from database")
    lostDf = rowsToDf(lostData, lostDescription)

    if nMatches > len(lostDf):
        nMatches = len(lostDf)

    foundDataset=dataset('found','single',foundDf)
    lostDataset=dataset('lost','multiple',lostDf)

    bestMatches = Matching.doMatching(foundDataset, lostDataset, nMatches)

    for match in bestMatches:
        if (match.score > 0.55):
            database.insert_match_table(match.lostid, match.foundid, match.score)
        else:
            print("Score too low, not sent to DB")

def lostMatch(lostid):
    nMatches = 5
    lost, lostDescription = database.get_lost(lostid)
    if lost is None:
        raise Exception("Cannot find lostid")

    if (len(lost) == 0):
        raise Exception("Cannot find lostid")
    lostDf = rowsToDf(lost, lostDescription)

    foundData, foundDescription = database.get_all_found()
    if (foundData is None):
        raise Exception("Could not get found data from database")
    if len(foundData) == 0:
        raise Exception("Could not get found data from database")
    foundDf = rowsToDf(foundData, foundDescription)


    if nMatches > len(foundDf):
        nMatches = len(foundDf)


    foundDataset=dataset('found','multiple',foundDf)
    lostDataset=dataset('lost','single',lostDf)

    bestMatches = Matching.doMatching(lostDataset, foundDataset, nMatches)

    for match in bestMatches:
        if (match.score > 0.55):
            database.insert_match_table(match.lostid, match.foundid, match.score)
        else:
            print("Score too low, not sent to DB")