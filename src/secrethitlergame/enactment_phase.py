from secrethitlergame.phase import Phase
from secrethitlergame.voting_phase import VotingPhase
from secrethitlergame.cards import LiberalCard, FascistCard


class EnactmentPhase(Phase):

    def __init__(self, previous_phase=None, next_phase=None):
        super().__init__(previous_phase, next_phase)
        self.chancelor = None
        self.president = None

    def get_previous_government(self):
        p = self
        while p.previous_phase:
            p = p.previous_phase
            if isinstance(p, VotingPhase):
                return p.chancelor, p.president
        return None, None

    def determine_government(self):
        previous_government = self.get_previous_government()
        self.chancelor, self.president = previous_government

    def enact(self, enactment, liberal_space, fascist_space):
        result = enactment.enacted_policy()
        if isinstance(result, LiberalCard):
            self.next_phase = liberal_space
        elif isinstance(result, FascistCard):
            self.next_phase = fascist_space
        return self.next_phase
