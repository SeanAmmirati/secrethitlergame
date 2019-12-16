from secrethitlergame.phase import Phase
from secrethitlergame.enactment_phase import EnactmentPhase


class SpecialPhase(Phase):

    def __init__(self, previous_phase=None, next_phase=None):
        super().__init__(previous_phase, next_phase)
        self.player = None

    def find_last_president(self):
        p = self.previous_phase

        while p:
            if isinstance(p, EnactmentPhase):
                self.player = p.president
                break
            p = p.previous_phase

        if self.player is None:
            raise NotImplementedError(
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


class PeekDeckPhase(SpecialPhase):

    def peek_deck(self, deck):
        self.player.inform_deck(deck.top(3))

    def action(self, topdeck):
        return self.peek_deck(deck)
