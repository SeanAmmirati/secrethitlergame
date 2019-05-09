import numpy as np
from math import factorial


class Claim:
    def __init__(self, turn, claim, role,
                 co_governor, conflict, conflict_claim):
        self.turn = turn
        self.claim = claim
        self.role = role
        self.co_governor = co_governor
        self.conflict = conflict
        self.conflict_claim = conflict_claim

    def probability(self, state):
        if len(self.claim) == 0:
            return np.nan

        if isinstance(self.claim[0], list):
            claim = self.claim[0]
        else:
            claim = self.claim

        n_liberals = len([x for x in claim if x.upper() == 'L'])
        n_fascists = state.cards_drawn_on_gov - n_liberals

        n_ways_of_getting_liberals = factorial(state.n_liberals_left) / (factorial(state.n_liberals_left - n_liberals) * factorial(n_liberals)) if n_liberals < state.n_liberals_left else 0
        n_ways_of_getting_fasc = factorial(state.n_fasc_left) / (factorial(state.n_fasc_left - n_fascists) * factorial(n_fascists)) if n_fascists < state.n_fasc_left else 0
        n_pos_draws = factorial(state.cards_in_deck + 2) / (factorial(state.cards_in_deck - 1) * 6)

        prob = (n_ways_of_getting_liberals * n_ways_of_getting_fasc) / n_pos_draws
        return prob
