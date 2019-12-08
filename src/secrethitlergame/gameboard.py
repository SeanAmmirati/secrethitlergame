import space


class GameBoard:

    def __init__(self, max_lib=5, max_fasc=6, max_tracker=3,
                 fascist_space_seq=None, liberal_space_seq=None):
        self.max_lib = max_lib
        self.max_fasc = max_fasc
        self.max_tracker = max_tracker

        if not fascist_space_seq:
            self.fascist_space_seq = {
                i: space.FascistSpace for i in range(self.max_fasc)
            }
        else:
            self.fascist_space_seq = fascist_space_seq

        if not liberal_space_seq:
            self.liberal_space_seq = {
                i: space.LiberalSpace for i in range(self.max_lib)
            }
        else:
            self.liberal_space_seq = liberal_space_seq

        self.cur_lib_space = self.generate_liberal_spaces()
        self.cur_fasc_space = self.generate_fascist_spaces()
        self.cur_tracker = 0

    def _generate_spaces(self, space_rule):
        init_space = space_rule[0]()
        cur_space = init_space

        for i in range(1, len(space_rule)):
            sp = space_rule[i]()
            cur_space.set_next_space(sp)
            cur_space = sp
        return init_space

    def generate_liberal_spaces(self):
        return self._generate_spaces(self.liberal_space_seq)

    def generate_fascist_spaces(self):
        return self._generate_spaces(self.fascist_space_seq)

    def increment_liberal(self):
        if self.cur_lib_space.get_next_space():
            self.cur_lib_space = self.cur_lib_space.get_next_space()
        else:
            # TODO: Create winning condition class
            return 'Liberal Winning Condition (yet to be defined)'

    def increment_fascist(self):
        if self.cur_fasc_space.get_next_space():
            self.cur_fasc_space = self.cur_fasc_space.get_next_space()
        else:
            # TODO: Create winning condition class
            return 'Fascist Winning Condition'

    def reset_tracker(self):
        self.cur_tracker = 0

    def increment_tracker(self):
        self.cur_tracker += 1
        if self.cur_tracker == 3:
            self.reset_tracker()


class FiveSixPlayerGameBoard(GameBoard):

    fascist_space_seq = {
        0: space.FascistSpace,
        1: space.FascistSpace,
        2: space.PeekTopDeckSpace,
        3: space.ExecutionSpace,
        4: space.ExecutionSpace,
        5: space.FascistSpace
    }

    def __init__(self, max_tracker=3):
        super().__init__(max_lib=5, max_fasc=6, max_tracker=max_tracker,
                         fascist_space_seq=FiveSixPlayerGameBoard.fascist_space_seq)


class SevenEightPlayerGameBoard(GameBoard):

    fascist_space_seq = {
        0: space.FascistSpace,
        1: space.PeekPlayerSpace,
        2: space.ChooseNextPresidentSpace,
        3: space.ExecutionSpace,
        4: space.ExecutionSpace,
        5: space.FascistSpace
    }

    def __init__(self, max_tracker=3):
        super().__init__(max_lib=5, max_fasc=6, max_tracker=max_tracker,
                         fascist_space_seq=SevenEightPlayerGameBoard.fascist_space_seq)


class NineTenPlayerGameBoard(GameBoard):
    fascist_space_seq = {
        0: space.PeekPlayerSpace,
        1: space.PeekPlayerSpace,
        2: space.ChooseNextPresidentSpace,
        3: space.ExecutionSpace,
        4: space.ExecutionSpace,
        5: space.FascistSpace
    }

    def __init__(self, max_tracker=3):
        super().__init__(max_lib=5, max_fasc=6, max_tracker=max_tracker,
                         fascist_space_seq=NineTenPlayerGameBoard.fascist_space_seq)


if __name__ == '__main__':
    g = GameBoard()
    print(g.cur_fasc_space)
    print(g.increment_fascist())
    print(g.cur_fasc_space)

    sixplayers = FiveSixPlayerGameBoard()
    print(sixplayers.cur_fasc_space)
    sixplayers.increment_fascist()
    print(sixplayers.cur_fasc_space)
    sixplayers.increment_fascist()
    print(sixplayers.cur_fasc_space)

    eightplayers = SevenEightPlayerGameBoard()
    print(eightplayers.cur_fasc_space)
    eightplayers.increment_fascist()
    print(eightplayers.cur_fasc_space)
    eightplayers.increment_fascist()
    print(eightplayers.cur_fasc_space)

    tenplayers = NineTenPlayerGameBoard()
    print(tenplayers.cur_fasc_space)
    tenplayers.increment_fascist()
    print(tenplayers.cur_fasc_space)
    tenplayers.increment_fascist()
    print(tenplayers.cur_fasc_space)
