from numpy.random import shuffle


class Card:

    def __init__(self, value):
        if value not in ['Fascist', 'Liberal']:
            raise ValueError('Must be either a Liberal or Fascist card.')
        self.value = value
        self.public = False

    def play(self):
        self.public = True

    def is_liberal(self):
        return self.value == 'Liberal'

    def is_fascist(self):
        return self.value == 'Fascist'

    def __eq__(self, other):
        try:
            return self.value == other.value
        except AttributeError:
            return False


class LiberalCard(Card):

    def __init__(self):
        super().__init__('Liberal')


class FascistCard(Card):

    def __init__(self):
        super().__init__('Fascist')


class CardDeck:

    def __init__(self, cards):
        self.cards = cards

    def add_card(self, card):
        self.cards.append(card)

    def remove_card(self):
        return self.cards.pop()

    def shuffle_cards(self):
        shuffle(self.cards)


class DrawDeck(CardDeck):

    def __init__(self, number_of_fascists=11, number_of_liberals=6):
        libs = [LiberalCard()] * number_of_liberals
        fascists = [FascistCard()] * number_of_fascists
        cards = libs + fascists
        super().__init__(cards)
        self.shuffle_cards()

    def top_deck(self):
        return super().remove_card()

    def top(self, n):
        return self.cards[-n:]

    def remove_card(self):
        if len(self.cards) <= 2:
            return 'Reshuffle Condition'
        else:
            return super().remove_card()

    def __add__(self, other):
        if isinstance(other, DiscardDeck):
            other.shuffle_cards()
            self.cards += other


class DiscardDeck(CardDeck):
    pass


if __name__ == '__main__':
    dd = DrawDeck(20, 10)
    print(dd.top(3))
    print(dd.remove_card())
    print(dd.top(3))
    print(dd.add_card(dd.remove_card()))
