from secrethitlergame.voting_phase import VotingPhase
from secrethitlergame.special_phase import (ExecutionPhase, ChooseNextPresidentPhase,
                                            PeekPlayerPhase, PeekDeckPhase)


class Space:

    def __init__(self, next_space=None, card=None):
        self.card = card
        self.next_space = next_space

    def next_phase(self):
        return VotingPhase

    def get_next_space(self):
        return self.next_space

    def add_card(self, card):
        card.play()
        self.card = card


class FascistSpace(Space):

    def set_next_space(self, space):
        if isinstance(space, FascistSpace):
            self.next_space = space

        else:
            raise TypeError(f'Must enter a value of type: {FascistSpace}')


class LiberalSpace(Space):
    def set_next_space(self, space):
        if isinstance(space, LiberalSpace):
            self.next_space = space

        else:
            raise TypeError(f'Must enter a value of type: {LiberalSpace}')


class ExecutionSpace(FascistSpace):

    def next_phase(self):
        return ExecutionPhase


class ChooseNextPresidentSpace(FascistSpace):

    def next_phase(self):
        return ChooseNextPresidentPhase


class PeekPlayerSpace(FascistSpace):

    def next_phase(self):
        return PeekPlayerPhase


class PeekTopDeckSpace(FascistSpace):

    def next_phase(self):
        return PeekDeckPhase
