from secrethitlergame.vote import Vote


class Government:

    def __init__(self):
        self.chancelor = None
        self.president = None
        self.approved = False
        self.votes = []

    def add_chancelor(self, player):
        if self.president == player:
            raise ValueError(
                'Chancelor and President must be different people')
        self.chancelor = player

    def add_president(self, player):
        if self.chancelor == player:
            raise ValueError(
                'Chancelor and President must be different people')
        self.president = player

    def remove_president(self):
        self.president = None

    def remove_chancelor(self):
        self.chancelor = None

    def add_vote(self, vote):
        if self.chancelor is None or self.president is None:
            raise NotImplementedError()

        if not isinstance(vote, Vote):
            raise TypeError('Vote must be of class Vote.')
        self.votes.append(vote)

    def add_votes(self, votes):
        for v in votes:
            self.add_vote(v)

    def reset_votes(self):
        if self.votes:
            self.votes = []

    def passed(self):
        return sum((v.is_approval() for v in self.votes))/len(self.votes) > .5

    def failed(self):
        return not self.passed()
