import pandas as pd
from Matching import matching


def rows_to_df(rows, description):
    element_id = [x[0] for x in description]
    return pd.DataFrame(rows, columns=element_id)

def get_dataframe(fileLocation):
    datafile=open(fileLocation,'r')
    df = pd.read_csv(datafile,sep='\t',skiprows=(0),header=(0))
    return df


def test_matching():
    x = [0,'Elektronikk', 'Mobil', 'Svart', 4, '5/1/2020', 'Bose']
    data = get_dataframe('Data/random1000.txt')

    matches = matching(x, data, 5)
    return matches


def id_is_digit(digit):
    if type(digit) != str:
        raise Exception("ID is not string")
        return False
    if digit.isdigit():
        return True
    else:
        raise Exception("ID is not a digit")
        return False

