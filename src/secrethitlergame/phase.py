class Phase:

    def __init__(self, previous_phase=None, next_phase=None):
        self._previous_phase = previous_phase
        self._next_phase = next_phase

    @property
    def previous_phase(self):
        return self._previous_phase

    @previous_phase.setter
    def previous_phase(self, value):
        if value is None:
            self._previous_phase = None
            return
        if self.previous_phase == value:
            return
        if not self.previous_phase:
            self._previous_phase = value
            value.next_phase = self
        else:
            self._previous_phase = value
            self.previous_phase.next_phase = self

    @property
    def next_phase(self):
        return self._next_phase

    @next_phase.setter
    def next_phase(self, value):
        if value is None:
            self._next_phase = None
            return
        if self.next_phase == value:
            return
        if not self.next_phase:
            self._next_phase = value
            value.previous_phase = self
        else:
            self._next_phase = value
            self.next_phase.previous_phase = self

    @next_phase.deleter
    def next_phase(self):
        del self._next_phase
        self.next_phase = None

    def remove(self):
        if self.previous_phase:
            self.previous_phase.next_phase = self.next_phase
        if self.next_phase:
            self.next_phase.previous_phase = self.previous_phase
        del self

    def is_first(self):
        return self.previous_phase is None

    def is_last(self):
        return self.next_phase is None

    def is_isolated(self):
        return self.is_first() and self.is_last()
