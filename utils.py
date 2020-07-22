import pandas as pd

def rowsToDf(rows, description):
    element_id = [x[0] for x in description]
    return pd.DataFrame(rows, columns=element_id)