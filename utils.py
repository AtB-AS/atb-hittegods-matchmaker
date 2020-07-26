import pandas as pd
from dataset import Dataset

def rows_to_df(rows, description):
    element_id = [x[0] for x in description]
    return pd.DataFrame(rows, columns=element_id)

def get_dataframe(fileLocation):
    datafile=open(fileLocation,'r')
    df = pd.read_csv(datafile,sep='\t',skiprows=(0),header=(0))
    return df



def id_is_digit(digit):
    if type(digit) != str:
        raise Exception("ID is not string")
        return False
    if digit.isdigit():
        return True
    else:
        raise Exception("ID is not a digit")
        return False

def remove_first(arr):
    arr.pop(0)
    return arr
