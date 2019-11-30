import numpy as np
from math import factorial


class Turn:

    def __init__(self, turn_number=None):

        self.turn_number = turn_number


class Claim(list):

    def __init__(self, values):
        if len(values) > 3:
            raise ValueError(
                'Claim must be less than or equal to three values')
        super().__init__()
        for v in values:
            self.append(v)


class Chancelor(Player):

    def __init__(self, )


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

        n_ways_of_getting_liberals = factorial(state.n_liberals_left) / (factorial(
            state.n_liberals_left - n_liberals) * factorial(n_liberals)) if n_liberals < state.n_liberals_left else 0
        n_ways_of_getting_fasc = factorial(state.n_fasc_left) / (factorial(
            state.n_fasc_left - n_fascists) * factorial(n_fascists)) if n_fascists < state.n_fasc_left else 0
        n_pos_draws = factorial(state.cards_in_deck + 3) / \
            ((factorial(state.cards_in_deck)) * 6)

        prob = (n_ways_of_getting_liberals *
                n_ways_of_getting_fasc) / n_pos_draws
        return prob


if __name__ == '__main__':
    from secrethitlergame.state import SecretHitlerState
    c = Claim(1, ['F', 'F'], 'chanc', 3, False, None)
    s = SecretHitlerState()
    c.probability(s)
