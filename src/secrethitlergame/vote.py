class Vote:

    def __init__(self):
        self._value = None
        self._possible_votes = ['Ja', 'Nein', None]

    def upvote(self):
        self.value = 'Ja'

    def downvote(self):
        self.value = 'Nein'

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, to_set):
        if to_set not in self._possible_votes:
            raise ValueError(f'Vote can only be one of {self._possible_votes}')
        else:
            self._value = to_set

    @value.deleter
    def value(self):
        pass

    def is_approval(self):
        return self.value == 'Ja'

    def is_disapproval(self):
        return self.value == 'Nein'

    def is_none(self):
        return self.value is None
