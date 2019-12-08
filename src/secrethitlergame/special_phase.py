from phase import Phase
from enactment_phase import EnactmentPhase


class SpecialPhase(Phase):

    def __init__(self, previous_phase=None, next_phase=None):
        super().__init__(previous_phase, next_phase)
        self.player = None

    def find_last_president(self):
        p = self

        while p.previous_phase:
            if isinstance(p, EnactmentPhase):
                self.player = p.president
                break

        if self.player is None:
            raise ValueError(
                'There have not been any presidents who could have a special action. Is this being called in the correct place?')

    def action(self, *args, **kwargs):
        pass


class ExecutionPhase(SpecialPhase):

    def execute_player(self, player):
        player.alive = False
        if player.is_hitler:
            return 'Game over -- Hitler has been shot!'

    def action(self, player):
        return self.execute_player(player)


class ChooseNextPresidentPhase(SpecialPhase):

    def choose_next_president(self, player):
        player.is_president = True

    def action(self, player):
        return self.choose_next_president(player)


class PeekPlayerPhase(SpecialPhase):

    def peek_player(self, player):
        self.player.inform_role(player)

    def action(self, player):
        return self.peek_player(player)


class PeekTopDeckPhase(SpecialPhase):

    def peek_topdeck(self, topdeck):
        self.player.inform_topdeck(topdeck.top(3))

    def action(self, topdeck):
        return self.peek_topdeck(topdeck)
