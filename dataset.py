class Dataset:
    """
    Stores if a dataset is "lost" or "found", has one or multiple entries and the pandas dataframe with the data
    """
    def __init__(self, lost_or_found, entries, df):
        self.lost_or_found = lost_or_found
        self.entries = entries
        self.df = df