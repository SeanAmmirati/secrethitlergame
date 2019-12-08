from cards import Card


class Claim:

    def __init__(self, cards):
        self.cards = cards
        for card in self.cards:
            if not isinstance(card, Card) and card is not None:
                raise TypeError(
                    'Cards must either be of the card type or None.')

    def is_hidden(self):
        return any(x is None for x in self.cards)


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

        if not isinstance(recieved, RecievedClaim):
            raise TypeError(
                'Must pass a recieved claim into a policy action class.')

        if not isinstance(discarded, DiscardClaim):
            raise TypeError(
                'Must pass a discard claim into a policy action class.')

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
    rc = RecievedClaim([Card('Liberal'), Card('Fascist')])
    dc = DiscardClaim([Card('Liberal')])
    tc = PolicyAction(rc, dc)
    print(tc.enacted_cards())
