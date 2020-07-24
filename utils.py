import pandas as pd
from Matching import Matching


def rowsToDf(rows, description):
    element_id = [x[0] for x in description]
    return pd.DataFrame(rows, columns=element_id)

def getDataFrame(fileLocation):
    datafile=open(fileLocation,'r')
    df = pd.read_csv(datafile,sep='\t',skiprows=(0),header=(0))
    return df


def testMatching():
    x=[0,'Elektronikk','Mobil','Svart', 4,'5/1/2020','Bose']
    data=getDataFrame('Data/random1000.txt')

    matches=Matching(x,data,5)
    return matches
