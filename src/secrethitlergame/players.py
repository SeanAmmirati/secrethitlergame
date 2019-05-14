import numpy as np
from secrethitlergame.claim import Claim

class SecretHitlerPlayer():

    def __init__(self, name, seat):
        self.name = name
        self.appointments = []
        self.move_info = []
        self.vote_info = []
        self.status = 'Alive'
        self.seat = seat

    @property
    def conflicts(self):
        conflicts = [move for move in self.move_info if move.conflict]
        return conflicts

    @property
    def aggreeability(self):
        if len(self.move_info) == 0:
            return np.nan
        else:
            return np.mean([not move.conflict for move in self.move_info])

    @property
    def confidence(self):
        if len(self.vote_info) == 0:
            return np.nan
        else:
            return np.mean([vote['vote'].upper() == 'JA' for vote in self.vote_info])


    def appoint(self, turn, co_governor):
        info_dict = {
            'turn': turn,
            'appointed': co_governor
            }
        self.appointments.append(info_dict)

    def add_claim(self, turn, claim, role, co_governor, conflict, conflict_claim):
        claim = Claim(turn, claim, role, co_governor, conflict, conflict_claim)
        self.move_info.append(claim)

    def add_vote(self, turn, vote, vote_on_pres, vote_on_chanc):
        info_dict = {
            'turn': turn,
            'vote': vote,
            'vote_on_pres': vote_on_pres,
            'vote_on_chanc': vote_on_chanc
            }
        self.vote_info.append(info_dict)

