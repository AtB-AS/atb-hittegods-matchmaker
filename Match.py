class Match:
    """
    A match with the lost id, found id and similarity score
    """
    def __init__(self, lostid, foundid, score):
        self.lostid = lostid
        self.foundid = foundid
        self.score = score

    def print(self):
        return ("lostid: %s, foundid: %s, score: %s".format(self.lostid,self.foundid,self.score))