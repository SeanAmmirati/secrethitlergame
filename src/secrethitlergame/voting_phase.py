from secrethitlergame.phase import Phase
# from secrethitlergame.enactment_phase import EnactmentPhase


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
                'Cannot add chancelor who was in previous government.')
        else:
            self.chancelor = player

    def add_president(self, player):
        self.president = player

    # def passed(self):
    #     self.next_phase = EnactmentPhase()
    #     return self.next_phase

    def failed(self):
        self.next_phase = VotingPhase()
        return self.next_phase
