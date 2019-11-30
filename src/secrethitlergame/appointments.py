
class Government:

    def __init__(self):
        self.chancelor = None
        self.president = None
        self.approved = False
        self.votes = []

    def add_chancelor(self, player):
        self.chancelor = player

    def add_president(self, player):
        self.president = player

    def add_votes(self, votes):
        