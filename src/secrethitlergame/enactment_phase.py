from phase import Phase
from voting_phase import VotingPhase


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

    