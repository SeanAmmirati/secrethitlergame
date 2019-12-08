class Claim:

    def __init__(self, cards):
        self.cards = cards


class RecievedClaim(Claim):

    def __init__(self, cards):
        if len(cards) not in [2, 3]:
            raise ValueError(
                'A player will recieve two or three cards regardless. Check the list value.')
        super().__init__(cards)

    def __sub__(self, other):
        if not isinstance(other, DiscardClaim):
            raise ValueError('Can only subtract recieved and discard claim.')

        c = self.cards.copy()
        c.remove(other.card)
        return c


class DiscardClaim(Claim):

    def __init__(self, cards):
        if len(cards) != 1:
            raise ValueError(
                'A player must discard exactly one card.')
        super().__init__(cards)
        self.card = self.cards[0]


class PolicyAction:

    def __init__(self, recieved, discarded):
        self.recieved = recieved
        self.discarded = discarded

    def recieved_cards(self):
        return self.recieved.cards

    def discarded_cards(self):
        return self.discarded.cards

    def passed_cards(self):
        return self.recieved - self.discarded

    def enacted_cards(self):
        passed = self.passed_cards()
        return passed if len(passed) == 1 else None


if __name__ == '__main__':
    rc = RecievedClaim([1, 1, 2])
    dc = DiscardClaim([1])
    tc = PolicyAction(rc, dc)
    print(tc.enacted_cards())
