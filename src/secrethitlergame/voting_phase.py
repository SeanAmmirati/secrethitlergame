from phase import Phase


class VotingPhase(Phase):

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

    def add_chancelor(self, player):
        previous_government = self.get_previous_government()
        if player in previous_government:
            raise ValueError(
                'Cannot find add chancelor who was in previous government.')
        else:
            self.chancelor = player

    def add_president(self, player):
        self.president = player
