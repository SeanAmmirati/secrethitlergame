import pytest

from secrethitlergame.gameboard import (GameBoard, FiveSixPlayerGameBoard,
                                        SevenEightPlayerGameBoard,
                                        NineTenPlayerGameBoard)
import secrethitlergame.space as space
from unittest.mock import Mock


class TestGameBoard:

    def test_initialization(self):
        gb = GameBoard()
        assert len(gb.fascist_space_seq) == 6
        assert len(gb.liberal_space_seq) == 5

        assert isinstance(gb.fascist_space_seq, dict)
        assert isinstance(gb.liberal_space_seq, dict)

        assert all([v == space.LiberalSpace
                    for v in gb.liberal_space_seq.values()])
        assert all([v == space.FascistSpace
                    for v in gb.fascist_space_seq.values()])

        test_dict = {
            i: space.ExecutionSpace
            for i in range(10)
        }

        gb = GameBoard(max_lib=5, max_fasc=6,
                       liberal_space_seq=test_dict,
                       fascist_space_seq=test_dict)

        assert len(gb.fascist_space_seq) == 10
        assert len(gb.liberal_space_seq) == 10

        assert isinstance(gb.fascist_space_seq, dict)
        assert isinstance(gb.liberal_space_seq, dict)

        assert all([v == space.ExecutionSpace
                    for v in gb.liberal_space_seq.values()])
        assert all([v == space.ExecutionSpace
                    for v in gb.fascist_space_seq.values()])

    def test_generate_spaces(self):
        space_rule_example = {i: Mock() for i in range(10)}

        # for i, rule in space_rule_example.items():
        #     rule.set_next_space = Mock()

        gb = GameBoard()

        gb._generate_spaces(space_rule_example)

        for i, rule in space_rule_example.items():

            rule.assert_called_once()

        # TODO: This is hard to test because the actual classes
        # are being passed into the sequences here. Ultimately
        # will require changes to the original code, but want
        # to test that the set_next ... is also being called.

    def test_generate_liberal_spaces(self):

        gb = GameBoard()
        liberal_spaces = {
            i: space.LiberalSpace for i in range(gb.max_lib)
        }
        gb._generate_spaces = Mock()
        gb.generate_liberal_spaces()

        gb._generate_spaces.assert_called_once_with(liberal_spaces)

    def test_generate_fascist_spaces(self):
        gb = GameBoard()
        fascist_spaces = {
            i: space.FascistSpace for i in range(gb.max_fasc)
        }
        gb._generate_spaces = Mock()
        gb.generate_fascist_spaces()

        gb._generate_spaces.assert_called_once_with(fascist_spaces)

    def test_increment_liberal(self):
        gb = GameBoard()
        for i in range(gb.max_lib):
            if i < (gb.max_lib - 1):
                assert gb.increment_liberal() is None
            else:
                # TODO: Once this is updated with wining condition class, add an appropriate assertion
                assert gb.increment_liberal() is not None

    def test_increment_fascist(self):
        gb = GameBoard()
        for i in range(gb.max_fasc):
            if i < (gb.max_fasc - 1):
                assert gb.increment_fascist() is None
            else:
                # TODO: Once this is updated with wining condition class, add an appropriate assertion
                assert gb.increment_fascist() is not None

    def test_reset_tracker(self):
        gb = GameBoard()
        gb.cur_tracker = 2
        gb.reset_tracker()
        assert gb.cur_tracker == 0

    def test_increment_tracker(self):
        gb = GameBoard()
        for i in range(1, gb.max_tracker * 3):
            gb.increment_tracker()
            assert (i % gb.max_tracker) == gb.cur_tracker


class TestFiveSizPlayerGameBoard:

    def test_initialization(self):
        fascist_space_seq = {
            0: space.FascistSpace,
            1: space.FascistSpace,
            2: space.PeekTopDeckSpace,
            3: space.ExecutionSpace,
            4: space.ExecutionSpace,
            5: space.FascistSpace
        }

        gb = FiveSixPlayerGameBoard()
        assert len(gb.fascist_space_seq) == 6
        assert len(gb.liberal_space_seq) == 5

        assert isinstance(gb.fascist_space_seq, dict)
        assert isinstance(gb.liberal_space_seq, dict)

        assert all([v == space.LiberalSpace
                    for v in gb.liberal_space_seq.values()])
        assert not all([v == space.FascistSpace
                        for v in gb.fascist_space_seq.values()])

        assert gb.fascist_space_seq == fascist_space_seq


class TestSevenEightPlayerGameBoard:

    def test_initialization(self):
        fascist_space_seq = {
            0: space.FascistSpace,
            1: space.PeekPlayerSpace,
            2: space.ChooseNextPresidentSpace,
            3: space.ExecutionSpace,
            4: space.ExecutionSpace,
            5: space.FascistSpace
        }

        gb = SevenEightPlayerGameBoard()
        assert len(gb.fascist_space_seq) == 6
        assert len(gb.liberal_space_seq) == 5

        assert isinstance(gb.fascist_space_seq, dict)
        assert isinstance(gb.liberal_space_seq, dict)

        assert all([v == space.LiberalSpace
                    for v in gb.liberal_space_seq.values()])
        assert not all([v == space.FascistSpace
                        for v in gb.fascist_space_seq.values()])

        assert gb.fascist_space_seq == fascist_space_seq


class TestNineTenPlayerGameBoard:

    def test_initialization(self):
        fascist_space_seq = {
            0: space.PeekPlayerSpace,
            1: space.PeekPlayerSpace,
            2: space.ChooseNextPresidentSpace,
            3: space.ExecutionSpace,
            4: space.ExecutionSpace,
            5: space.FascistSpace
        }

        gb = NineTenPlayerGameBoard()
        assert len(gb.fascist_space_seq) == 6
        assert len(gb.liberal_space_seq) == 5

        assert isinstance(gb.fascist_space_seq, dict)
        assert isinstance(gb.liberal_space_seq, dict)

        assert all([v == space.LiberalSpace
                    for v in gb.liberal_space_seq.values()])
        assert not all([v == space.FascistSpace
                        for v in gb.fascist_space_seq.values()])

        assert gb.fascist_space_seq == fascist_space_seq
